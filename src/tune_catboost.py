"""Optuna tuning for CatBoost (top baseline model)."""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import optuna
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold

from .baseline_v2 import feature_columns, prep_native_cats
from .data import ID_COL, REPO_ROOT, basic_clean, load_raw, split_xy
from .features import add_all_features

warnings.filterwarnings("ignore")
optuna.logging.set_verbosity(optuna.logging.WARNING)

RANDOM_STATE = 42
N_SPLITS = 5
N_TRIALS = 30


def objective_factory(Xn: pd.DataFrame, y: pd.Series, cat_cols: list[str]):
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

    def objective(trial: optuna.Trial) -> float:
        params = {
            "iterations": trial.suggest_int("iterations", 300, 1500),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
            "depth": trial.suggest_int("depth", 4, 10),
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1.0, 10.0, log=True),
            "border_count": trial.suggest_int("border_count", 32, 255),
            "bagging_temperature": trial.suggest_float("bagging_temperature", 0.0, 1.0),
            "random_strength": trial.suggest_float("random_strength", 1e-3, 10.0, log=True),
            "cat_features": cat_cols,
            "random_state": RANDOM_STATE,
            "verbose": False,
            "allow_writing_files": False,
        }

        scores = []
        for tr, va in cv.split(Xn, y):
            clf = CatBoostClassifier(**params)
            clf.fit(Xn.iloc[tr], y.iloc[tr])
            pred = clf.predict(Xn.iloc[va]).astype(int).ravel()
            scores.append(f1_score(y.iloc[va], pred, average="macro"))
        return float(np.mean(scores))

    return objective


def main() -> None:
    print("Preparing data...")
    train_raw, _, _ = load_raw()
    train = add_all_features(basic_clean(train_raw))
    X, y = split_xy(train)
    num_cols, cat_cols = feature_columns(train)
    Xn = prep_native_cats(X, num_cols, cat_cols)

    print(f"Running Optuna ({N_TRIALS} trials)...")
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=RANDOM_STATE))
    study.optimize(objective_factory(Xn, y, cat_cols), n_trials=N_TRIALS, show_progress_bar=False)

    print(f"\nBest CV F1 macro: {study.best_value:.4f}")
    print(f"Best params:      {json.dumps(study.best_params, indent=2)}")

    out = REPO_ROOT / "reports" / "catboost_optuna.json"
    out.write_text(
        json.dumps(
            {
                "best_value": study.best_value,
                "best_params": study.best_params,
                "n_trials": N_TRIALS,
                "trials": [
                    {"value": t.value, "params": t.params} for t in study.trials if t.value is not None
                ],
            },
            indent=2,
        )
    )
    print(f"Saved -> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
