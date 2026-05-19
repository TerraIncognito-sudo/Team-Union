"""First-pass baseline pipeline.

Trains LogisticRegression, RandomForest, LightGBM, XGBoost and CatBoost
with their default settings, runs 5-fold stratified CV on macro F1,
keeps the best by mean CV score, refits on the full training set and
writes submissions/<model>_baseline.csv.

Run with: python -m src.baseline
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import (
    BOOL_COLS,
    CAT_COLS,
    ID_COL,
    NUMERIC_COLS,
    REPO_ROOT,
    SPEND_COLS,
    TARGET,
    basic_clean,
    load_raw,
    split_xy,
)
from .features import add_all_features

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
N_SPLITS = 5
# Kaggle scores us on macro F1, so we use the same thing in CV.
SCORING = "f1_macro"

SUBMISSION_DIR = REPO_ROOT / "submissions"
SUBMISSION_DIR.mkdir(exist_ok=True)


def build_feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw frame and tack on the engineered features."""
    df = basic_clean(df)
    df = add_all_features(df)
    return df


def feature_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return (numeric_features, categorical_features) used by the models."""
    # Raw cols that have been replaced by engineered features.
    drop = {ID_COL, TARGET, "BookingDate", "Room"}
    numeric, categorical = [], []
    for col in df.columns:
        if col in drop:
            continue
        if df[col].dtype == object:
            categorical.append(col)
        else:
            numeric.append(col)
    return numeric, categorical


def make_preprocessor(num_cols: list[str], cat_cols: list[str]) -> ColumnTransformer:
    numeric_pipe = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    cat_pipe = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="constant", fill_value="Missing")),
            (
                "ohe",
                OneHotEncoder(handle_unknown="ignore", min_frequency=10, sparse_output=False),
            ),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, num_cols),
            ("cat", cat_pipe, cat_cols),
        ],
        remainder="drop",
    )


def get_models() -> dict:
    from lightgbm import LGBMClassifier
    from xgboost import XGBClassifier
    from catboost import CatBoostClassifier

    # Using class_weight / scale_pos_weight where the library supports it,
    # since the churn classes are not balanced and we are scored on macro F1.
    return {
        "logreg": LogisticRegression(
            max_iter=2000, random_state=RANDOM_STATE, class_weight="balanced"
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            n_jobs=-1,
            random_state=RANDOM_STATE,
            class_weight="balanced",
        ),
        "lightgbm": LGBMClassifier(
            n_estimators=500,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbose=-1,
            class_weight="balanced",
        ),
        "xgboost": XGBClassifier(
            n_estimators=500,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            eval_metric="logloss",
            tree_method="hist",
        ),
        "catboost": CatBoostClassifier(
            iterations=500,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
            verbose=False,
            auto_class_weights="Balanced",
        ),
    }


def cross_validate_all(
    X: pd.DataFrame, y: pd.Series, num_cols: list[str], cat_cols: list[str]
) -> pd.DataFrame:
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    rows = []
    for name, clf in get_models().items():
        preprocessor = make_preprocessor(num_cols, cat_cols)
        pipe = Pipeline([("prep", preprocessor), ("clf", clf)])
        scores = cross_val_score(pipe, X, y, cv=cv, scoring=SCORING, n_jobs=-1)
        rows.append(
            {
                "model": name,
                "cv_f1_macro_mean": scores.mean(),
                "cv_f1_macro_std": scores.std(),
                "cv_scores": scores.tolist(),
            }
        )
        print(f"  {name:14s}  CV F1 = {scores.mean():.4f} +/- {scores.std():.4f}")
    return pd.DataFrame(rows).sort_values("cv_f1_macro_mean", ascending=False).reset_index(drop=True)


def fit_predict_submission(
    model_name: str,
    X: pd.DataFrame,
    y: pd.Series,
    test_X: pd.DataFrame,
    test_ids: pd.Series,
    num_cols: list[str],
    cat_cols: list[str],
    out_path: Path,
) -> Path:
    clf = get_models()[model_name]
    preprocessor = make_preprocessor(num_cols, cat_cols)
    pipe = Pipeline([("prep", preprocessor), ("clf", clf)])
    pipe.fit(X, y)
    preds = pipe.predict(test_X)
    sub = pd.DataFrame({ID_COL: test_ids.values, TARGET: preds.astype(int)})
    sub.to_csv(out_path, index=False)
    return out_path


def main() -> None:
    print("Loading data...")
    train_raw, test_raw, sample_sub = load_raw()
    print(f"  train={train_raw.shape}, test={test_raw.shape}")

    print("Cleaning + feature engineering...")
    train = build_feature_frame(train_raw)
    test = build_feature_frame(test_raw)

    X, y = split_xy(train)
    test_ids = test[ID_COL]
    test_X = test

    num_cols, cat_cols = feature_columns(train)
    print(f"  num features: {len(num_cols)}, cat features: {len(cat_cols)}")
    print(f"  target balance: churn rate = {y.mean():.4f}  ({len(y)} rows)")

    print(f"\nRunning 5-fold stratified CV (scoring={SCORING})")
    results = cross_validate_all(X, y, num_cols, cat_cols)

    print("\nLeaderboard (CV mean F1 macro):")
    print(results.drop(columns=["cv_scores"]).to_string(index=False))

    reports_dir = REPO_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    results.to_csv(reports_dir / "baseline_cv.csv", index=False)
    print(f"\nSaved CV table -> reports/baseline_cv.csv")

    # Refit the best model and write its submission.
    best_model = results.iloc[0]["model"]
    out = SUBMISSION_DIR / f"{best_model}_baseline.csv"
    print(f"\nFitting best model ({best_model}) on full train and predicting test...")
    fit_predict_submission(best_model, X, y, test_X, test_ids, num_cols, cat_cols, out)
    print(f"  wrote {out}")

    # Also write a non-tree and a tree submission so we have both on hand.
    boost_models = {"lightgbm", "xgboost", "catboost", "random_forest"}
    non_tree = "logreg"
    best_tree = next(
        (r["model"] for _, r in results.iterrows() if r["model"] in boost_models), None
    )
    if best_tree and best_tree != best_model:
        out2 = SUBMISSION_DIR / f"{best_tree}_baseline.csv"
        fit_predict_submission(best_tree, X, y, test_X, test_ids, num_cols, cat_cols, out2)
        print(f"  also wrote {out2}")
    if non_tree != best_model:
        out3 = SUBMISSION_DIR / f"{non_tree}_baseline.csv"
        fit_predict_submission(non_tree, X, y, test_X, test_ids, num_cols, cat_cols, out3)
        print(f"  also wrote {out3}")

    print("\nDone.")


if __name__ == "__main__":
    main()
