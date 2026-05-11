"""Generate model explanations: feature importances + 3 right + 3 wrong examples.

Rubric: "Show at least three training instances (i.e., feature values) that your
model predicted correctly and three that it predicted incorrectly. Draw insights
from these examples."
"""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .baseline_v2 import feature_columns, prep_native_cats
from .data import ID_COL, REPO_ROOT, TARGET, basic_clean, load_raw, split_xy
from .features import add_all_features

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", context="talk")
PRIMARY = "#1f4e79"

FIG_DIR = REPO_ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    train_raw, _, _ = load_raw()
    train = add_all_features(basic_clean(train_raw))
    X, y = split_xy(train)
    num_cols, cat_cols = feature_columns(train)
    Xn = prep_native_cats(X, num_cols, cat_cols)

    # Fit a CatBoost native model (close to ensemble top contributor)
    from catboost import CatBoostClassifier

    clf = CatBoostClassifier(
        iterations=500,
        learning_rate=0.05,
        random_state=42,
        verbose=False,
        cat_features=cat_cols,
        allow_writing_files=False,
    )
    clf.fit(Xn, y)

    # Feature importances
    imp = pd.DataFrame(
        {"feature": Xn.columns, "importance": clf.feature_importances_}
    ).sort_values("importance", ascending=False)
    top = imp.head(15).iloc[::-1]

    fig, ax = plt.subplots(figsize=(8.5, 6))
    ax.barh(top["feature"], top["importance"], color=PRIMARY)
    ax.set_xlabel("Importance (CatBoost)")
    ax.set_title("Top 15 features driving the model")
    fig.savefig(FIG_DIR / "10_feature_importance.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    imp.to_csv(REPO_ROOT / "reports" / "feature_importance.csv", index=False)
    print("Top 10 features:")
    print(imp.head(10).to_string(index=False))

    # 3 right + 3 wrong examples — use OOF predictions to be honest
    oof = pd.read_csv(REPO_ROOT / "reports" / "oof_predictions.csv")
    weighted = 0.5 * oof["p_catboost"] + 0.3 * oof["p_lightgbm"] + 0.2 * oof["p_xgboost"]
    pred = (weighted >= 0.5).astype(int)
    oof["pred"] = pred
    oof["proba"] = weighted
    oof["correct"] = (oof["pred"] == oof[TARGET]).astype(int)

    # Join back to the cleaned features for context
    full = train_raw.merge(oof[[ID_COL, "pred", "proba", "correct"]], on=ID_COL, how="left")

    # Compute TotalSpend BEFORE building the most_conf frame so we can show it
    spend_cols = ["RoomService", "Dining", "Retail", "Spa", "Entertainment"]
    full["TotalSpend"] = full[spend_cols].sum(axis=1)

    # Most confident correct (highly confident prediction matched truth)
    most_conf = full.assign(distance_from_50=lambda d: abs(d["proba"] - 0.5))
    correct = most_conf[most_conf["correct"] == 1].sort_values("distance_from_50", ascending=False).head(3)
    wrong = most_conf[most_conf["correct"] == 0].sort_values("distance_from_50", ascending=False).head(3)

    cols_to_show = [
        ID_COL,
        TARGET,
        "pred",
        "proba",
        "AllInclusive",
        "Region",
        "PackageType",
        "PromoCode",
        "Age",
        "VIP",
        "Dining",
        "TotalSpend",
        "SurveyScore",
    ]

    correct_show = correct[cols_to_show]
    wrong_show = wrong[cols_to_show]

    print("\n=== 3 CORRECT examples (high confidence) ===")
    print(correct_show.to_string(index=False))
    print("\n=== 3 WRONG examples (high confidence — model was confidently wrong) ===")
    print(wrong_show.to_string(index=False))

    correct_show.to_csv(REPO_ROOT / "reports" / "examples_correct.csv", index=False)
    wrong_show.to_csv(REPO_ROOT / "reports" / "examples_wrong.csv", index=False)
    print("\nSaved examples to reports/examples_correct.csv and reports/examples_wrong.csv")


if __name__ == "__main__":
    main()
