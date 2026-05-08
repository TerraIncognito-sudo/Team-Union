"""Soft-vote ensemble: average predicted probabilities from top models.

Models in the ensemble:
  - CatBoost (OHE pipeline, the v1 baseline winner)
  - LightGBM (native categoricals, v2)
  - XGBoost (OHE)

Computes:
  - Out-of-fold (OOF) ensemble CV F1 macro
  - Per-model OOF for comparison
  - Final fit on full train -> submission CSV
"""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold

from .data import ID_COL, REPO_ROOT, TARGET, basic_clean, load_raw, split_xy
from .features import add_all_features
from .baseline_v2 import feature_columns, make_ohe_preprocessor, prep_native_cats

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
N_SPLITS = 5
SUBMISSION_DIR = REPO_ROOT / "submissions"
REPORTS_DIR = REPO_ROOT / "reports"


def cb_pipe():
    from catboost import CatBoostClassifier
    from sklearn.pipeline import Pipeline

    # CatBoost via OHE (v1 baseline winner).
    return Pipeline(
        [
            ("prep", None),  # set per-call
            (
                "clf",
                CatBoostClassifier(
                    iterations=500,
                    learning_rate=0.05,
                    random_state=RANDOM_STATE,
                    verbose=False,
                    allow_writing_files=False,
                ),
            ),
        ]
    )


def xgb_pipe():
    from xgboost import XGBClassifier
    from sklearn.pipeline import Pipeline

    return Pipeline(
        [
            ("prep", None),
            (
                "clf",
                XGBClassifier(
                    n_estimators=500,
                    learning_rate=0.05,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                    eval_metric="logloss",
                    tree_method="hist",
                ),
            ),
        ]
    )


def fit_lgbm_native(Xn_tr, y_tr, cat_cols):
    from lightgbm import LGBMClassifier

    Xn_tr = Xn_tr.copy()
    for c in cat_cols:
        Xn_tr[c] = Xn_tr[c].astype("category")
    clf = LGBMClassifier(
        n_estimators=500,
        learning_rate=0.05,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=-1,
    )
    clf.fit(Xn_tr, y_tr, categorical_feature=cat_cols)
    return clf


def predict_proba_lgbm(clf, Xn_va, cat_cols):
    Xn_va = Xn_va.copy()
    for c in cat_cols:
        Xn_va[c] = Xn_va[c].astype("category")
    return clf.predict_proba(Xn_va)[:, 1]


def fit_ohe_model(model_pipe, X_tr, y_tr, num_cols, cat_cols):
    from sklearn.pipeline import Pipeline

    pipe = Pipeline(
        [
            ("prep", make_ohe_preprocessor(num_cols, cat_cols)),
            ("clf", model_pipe.named_steps["clf"]),
        ]
    )
    pipe.fit(X_tr, y_tr)
    return pipe


def main() -> None:
    print("Loading + features...")
    train_raw, test_raw, _ = load_raw()
    train = add_all_features(basic_clean(train_raw))
    test = add_all_features(basic_clean(test_raw))
    X, y = split_xy(train)
    test_ids = test[ID_COL]
    num_cols, cat_cols = feature_columns(train)

    Xn = prep_native_cats(X, num_cols, cat_cols)
    test_native = prep_native_cats(test, num_cols, cat_cols)

    # OOF predictions for each model
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    oof = {"catboost": np.zeros(len(X)), "lightgbm": np.zeros(len(X)), "xgboost": np.zeros(len(X))}

    print(f"\nRunning {N_SPLITS}-fold OOF for ensemble members...")
    for fold, (tr, va) in enumerate(cv.split(X, y)):
        print(f"  Fold {fold + 1}/{N_SPLITS}")
        # CatBoost (OHE)
        cb = fit_ohe_model(cb_pipe(), X.iloc[tr], y.iloc[tr], num_cols, cat_cols)
        oof["catboost"][va] = cb.predict_proba(X.iloc[va])[:, 1]

        # XGBoost (OHE)
        xb = fit_ohe_model(xgb_pipe(), X.iloc[tr], y.iloc[tr], num_cols, cat_cols)
        oof["xgboost"][va] = xb.predict_proba(X.iloc[va])[:, 1]

        # LightGBM (native cats)
        lg = fit_lgbm_native(Xn.iloc[tr], y.iloc[tr], cat_cols)
        oof["lightgbm"][va] = predict_proba_lgbm(lg, Xn.iloc[va], cat_cols)

    print("\nPer-model OOF F1 macro (threshold=0.5):")
    for name, p in oof.items():
        f1 = f1_score(y, (p >= 0.5).astype(int), average="macro")
        print(f"  {name:10s}  {f1:.4f}")

    # Soft vote (equal weights)
    ens = np.mean([oof["catboost"], oof["lightgbm"], oof["xgboost"]], axis=0)
    ens_f1 = f1_score(y, (ens >= 0.5).astype(int), average="macro")
    print(f"\nEqual-weight soft vote F1 = {ens_f1:.4f}")

    # Threshold tune the ensemble
    best_thr, best_f1 = 0.5, ens_f1
    for thr in np.arange(0.40, 0.61, 0.005):
        f = f1_score(y, (ens >= thr).astype(int), average="macro")
        if f > best_f1:
            best_thr, best_f1 = thr, f
    print(f"Tuned threshold (soft vote): {best_thr:.3f}  F1 = {best_f1:.4f}")

    # CatBoost-heavy weighted vote
    w_ens = 0.5 * oof["catboost"] + 0.3 * oof["lightgbm"] + 0.2 * oof["xgboost"]
    w_f1 = f1_score(y, (w_ens >= 0.5).astype(int), average="macro")
    print(f"Weighted vote (.5/.3/.2):  F1 = {w_f1:.4f}")

    # Save OOF for later analysis
    pd.DataFrame(
        {
            ID_COL: train_raw[ID_COL],
            TARGET: y.values,
            "p_catboost": oof["catboost"],
            "p_lightgbm": oof["lightgbm"],
            "p_xgboost": oof["xgboost"],
            "p_ensemble": ens,
        }
    ).to_csv(REPORTS_DIR / "oof_predictions.csv", index=False)
    print(f"Saved OOF -> reports/oof_predictions.csv")

    # ==================================================================
    # Fit on full train, predict on test, write final submission
    # ==================================================================
    print("\nFitting final models on full train...")
    cb = fit_ohe_model(cb_pipe(), X, y, num_cols, cat_cols)
    xb = fit_ohe_model(xgb_pipe(), X, y, num_cols, cat_cols)
    lg = fit_lgbm_native(Xn, y, cat_cols)

    p_cb = cb.predict_proba(test)[:, 1]
    p_xb = xb.predict_proba(test)[:, 1]
    p_lg = predict_proba_lgbm(lg, test_native, cat_cols)

    # 1) Weighted vote (best on OOF) -> primary submission
    test_weighted = 0.5 * p_cb + 0.3 * p_lg + 0.2 * p_xb
    test_pred_w = (test_weighted >= 0.5).astype(int)
    sub_path_w = SUBMISSION_DIR / "ensemble_weighted.csv"
    pd.DataFrame({ID_COL: test_ids.values, TARGET: test_pred_w}).to_csv(sub_path_w, index=False)
    print(f"Wrote {sub_path_w.relative_to(REPO_ROOT)} (weighted .5/.3/.2, threshold=0.5)")
    print(f"  predicted churn = {test_pred_w.sum()} / {len(test_pred_w)} ({test_pred_w.mean():.3f})")

    # 2) Equal-weight + tuned threshold -> secondary
    test_ens = (p_cb + p_lg + p_xb) / 3.0
    test_pred = (test_ens >= best_thr).astype(int)
    sub_path = SUBMISSION_DIR / "ensemble_top3.csv"
    pd.DataFrame({ID_COL: test_ids.values, TARGET: test_pred}).to_csv(sub_path, index=False)
    print(f"Wrote {sub_path.relative_to(REPO_ROOT)} (equal weight, threshold={best_thr:.3f})")


if __name__ == "__main__":
    main()
