"""Fit selected models on full training data and write Kaggle submissions."""
from __future__ import annotations

import sys
import warnings

from .baseline import (
    REPO_ROOT,
    SUBMISSION_DIR,
    build_feature_frame,
    feature_columns,
    fit_predict_submission,
)
from .data import ID_COL, load_raw, split_xy

warnings.filterwarnings("ignore")


def main() -> None:
    model_names = sys.argv[1:] or ["catboost", "lightgbm", "xgboost", "logreg"]

    train_raw, test_raw, _ = load_raw()
    train = build_feature_frame(train_raw)
    test = build_feature_frame(test_raw)
    X, y = split_xy(train)
    test_ids = test[ID_COL]
    num_cols, cat_cols = feature_columns(train)

    for name in model_names:
        out = SUBMISSION_DIR / f"{name}_baseline.csv"
        print(f"Fitting {name} -> {out}")
        fit_predict_submission(name, X, y, test, test_ids, num_cols, cat_cols, out)
        print(f"  done: {out}")


if __name__ == "__main__":
    main()
