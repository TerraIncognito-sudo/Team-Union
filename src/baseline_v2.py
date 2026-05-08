"""Baseline v2: native categorical handling for CatBoost/LightGBM, +domain features.

Compares against v1 by re-running 5-fold CV macro-F1 on:
  - logreg (OHE pipeline, baseline)
  - random_forest (OHE pipeline, baseline)
  - lightgbm with NATIVE categorical handling
  - xgboost (still uses OHE; XGB doesn't natively handle string cats)
  - catboost with NATIVE categorical handling
"""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import (
    ID_COL,
    REPO_ROOT,
    TARGET,
    basic_clean,
    load_raw,
    split_xy,
)
from .features import add_all_features

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
N_SPLITS = 5

REPORTS = REPO_ROOT / "reports"
SUBMISSIONS = REPO_ROOT / "submissions"
REPORTS.mkdir(exist_ok=True)
SUBMISSIONS.mkdir(exist_ok=True)


def feature_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return (numeric, categorical) feature columns. Drops raw cols replaced by FE."""
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


def make_ohe_preprocessor(num_cols: list[str], cat_cols: list[str]) -> ColumnTransformer:
    """OHE preprocessor (used by LogReg/RandomForest/XGBoost)."""
    return ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
                ),
                num_cols,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="constant", fill_value="Missing")),
                        (
                            "ohe",
                            OneHotEncoder(
                                handle_unknown="ignore", min_frequency=10, sparse_output=False
                            ),
                        ),
                    ]
                ),
                cat_cols,
            ),
        ],
        remainder="drop",
    )


def prep_native_cats(X: pd.DataFrame, num_cols: list[str], cat_cols: list[str]) -> pd.DataFrame:
    """Prepare a frame for models that handle categoricals natively.
    Numeric cols stay as float (with NaN). Cat cols are filled with 'Missing' and cast to category.
    """
    X = X[num_cols + cat_cols].copy()
    for c in num_cols:
        X[c] = pd.to_numeric(X[c], errors="coerce")
    for c in cat_cols:
        X[c] = X[c].fillna("Missing").astype(str)
    return X


def cv_with_ohe(model, X, y, num_cols, cat_cols) -> list[float]:
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    scores = []
    for tr, va in cv.split(X, y):
        prep = make_ohe_preprocessor(num_cols, cat_cols)
        pipe = Pipeline([("prep", prep), ("clf", model)])
        pipe.fit(X.iloc[tr], y.iloc[tr])
        pred = pipe.predict(X.iloc[va])
        scores.append(f1_score(y.iloc[va], pred, average="macro"))
    return scores


def cv_lightgbm_native(X, y, num_cols, cat_cols) -> list[float]:
    from lightgbm import LGBMClassifier

    Xn = prep_native_cats(X, num_cols, cat_cols)
    for c in cat_cols:
        Xn[c] = Xn[c].astype("category")

    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    scores = []
    for tr, va in cv.split(Xn, y):
        clf = LGBMClassifier(
            n_estimators=500,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbose=-1,
        )
        # Re-build categorical dtype consistently
        Xtr, Xva = Xn.iloc[tr].copy(), Xn.iloc[va].copy()
        for c in cat_cols:
            cats = Xtr[c].cat.categories.union(Xva[c].cat.categories)
            Xtr[c] = pd.Categorical(Xtr[c], categories=cats)
            Xva[c] = pd.Categorical(Xva[c], categories=cats)
        clf.fit(Xtr, y.iloc[tr], categorical_feature=cat_cols)
        pred = clf.predict(Xva)
        scores.append(f1_score(y.iloc[va], pred, average="macro"))
    return scores


def cv_catboost_native(X, y, num_cols, cat_cols) -> list[float]:
    from catboost import CatBoostClassifier

    Xn = prep_native_cats(X, num_cols, cat_cols)

    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    scores = []
    for tr, va in cv.split(Xn, y):
        clf = CatBoostClassifier(
            iterations=500,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
            verbose=False,
            cat_features=cat_cols,
        )
        clf.fit(Xn.iloc[tr], y.iloc[tr])
        pred = clf.predict(Xn.iloc[va])
        scores.append(f1_score(y.iloc[va], pred.astype(int).ravel(), average="macro"))
    return scores


def main() -> None:
    print("Loading + cleaning + adding features...")
    train_raw, test_raw, _ = load_raw()
    train = add_all_features(basic_clean(train_raw))
    test = add_all_features(basic_clean(test_raw))
    X, y = split_xy(train)
    num_cols, cat_cols = feature_columns(train)
    print(f"  num={len(num_cols)}, cat={len(cat_cols)}")

    print("\nRunning CV (5-fold, F1 macro)")
    rows = []

    # LogReg + RF + XGBoost on OHE
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from xgboost import XGBClassifier

    for name, model in [
        ("logreg_v2", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
        (
            "random_forest_v2",
            RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=RANDOM_STATE),
        ),
        (
            "xgboost_v2",
            XGBClassifier(
                n_estimators=500,
                learning_rate=0.05,
                random_state=RANDOM_STATE,
                n_jobs=-1,
                eval_metric="logloss",
                tree_method="hist",
            ),
        ),
    ]:
        scores = cv_with_ohe(model, X, y, num_cols, cat_cols)
        print(f"  {name:22s}  {np.mean(scores):.4f} ± {np.std(scores):.4f}")
        rows.append({"model": name, "cv_f1_macro_mean": float(np.mean(scores)), "cv_f1_macro_std": float(np.std(scores)), "cv_scores": scores})

    # LightGBM native
    scores = cv_lightgbm_native(X, y, num_cols, cat_cols)
    print(f"  lightgbm_native_v2     {np.mean(scores):.4f} ± {np.std(scores):.4f}")
    rows.append({"model": "lightgbm_native_v2", "cv_f1_macro_mean": float(np.mean(scores)), "cv_f1_macro_std": float(np.std(scores)), "cv_scores": scores})

    # CatBoost native
    scores = cv_catboost_native(X, y, num_cols, cat_cols)
    print(f"  catboost_native_v2     {np.mean(scores):.4f} ± {np.std(scores):.4f}")
    rows.append({"model": "catboost_native_v2", "cv_f1_macro_mean": float(np.mean(scores)), "cv_f1_macro_std": float(np.std(scores)), "cv_scores": scores})

    df = pd.DataFrame(rows).sort_values("cv_f1_macro_mean", ascending=False).reset_index(drop=True)
    df.to_csv(REPORTS / "baseline_v2_cv.csv", index=False)
    print("\n=== Final v2 leaderboard ===")
    print(df.drop(columns=["cv_scores"]).to_string(index=False))


if __name__ == "__main__":
    main()
