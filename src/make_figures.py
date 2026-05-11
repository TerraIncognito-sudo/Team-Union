"""Generate all EDA figures used in the presentation. Saves PNGs to reports/figures/."""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .data import REPO_ROOT, basic_clean, load_raw

warnings.filterwarnings("ignore")

FIG_DIR = REPO_ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Brand-ish theme
sns.set_theme(style="whitegrid", palette="muted", context="talk")
PRIMARY = "#1f4e79"
ACCENT = "#c00000"
NEUTRAL = "#7f7f7f"


def save(fig: plt.Figure, name: str) -> Path:
    out = FIG_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def fig_target_balance(df: pd.DataFrame) -> Path:
    counts = df["Churned"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(["Retained (0)", "Churned (1)"], counts.values, color=[PRIMARY, ACCENT])
    for i, v in enumerate(counts.values):
        ax.text(i, v + 50, f"{v:,}\n({v/counts.sum():.1%})", ha="center", fontsize=12)
    ax.set_title("Target is balanced — no resampling needed")
    ax.set_ylabel("Number of guests")
    ax.set_ylim(0, counts.max() * 1.18)
    return save(fig, "01_target_balance.png")


def fig_allinclusive_paradox(df: pd.DataFrame) -> Path:
    """The headline Eureka moment."""
    g = df.groupby("AllInclusive")["Churned"].agg(["mean", "count"]).reset_index()
    g["AllInclusive"] = g["AllInclusive"].map({0.0: "Not All-Inclusive", 1.0: "All-Inclusive"})

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(g["AllInclusive"], g["mean"], color=[PRIMARY, ACCENT])
    ax.set_ylabel("Churn rate")
    ax.set_ylim(0, 1.05)
    for b, m, n in zip(bars, g["mean"], g["count"]):
        ax.text(
            b.get_x() + b.get_width() / 2,
            m + 0.02,
            f"{m:.1%}\n(n={n:,})",
            ha="center",
            fontsize=13,
        )
    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    return save(fig, "02_allinclusive_paradox.png")


def fig_ai_x_region_heatmap(df: pd.DataFrame) -> Path:
    pivot = (
        df.groupby([df["Region"].fillna("Missing"), df["AllInclusive"].fillna(-1)])["Churned"]
        .mean()
        .unstack()
    )
    pivot = pivot.rename(columns={0.0: "Not AI", 1.0: "All-Inclusive", -1.0: "Missing"})
    pivot = pivot.loc[["Americas", "AsiaPacific", "Europe"]]

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".1%",
        cmap="Reds",
        ax=ax,
        cbar_kws={"label": "Churn rate"},
        vmin=0.0,
        vmax=1.0,
        annot_kws={"size": 16, "weight": "bold"},
    )
    ax.set_title("All-Inclusive × Region churn rate")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=13)
    return save(fig, "03_ai_x_region_heatmap.png")


def fig_promo_impact(df: pd.DataFrame) -> Path:
    promo = df.copy()
    promo["PromoCode"] = promo["PromoCode"].fillna("NoPromo")
    g = (
        promo.groupby("PromoCode")["Churned"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = [ACCENT if i == g.index[0] else PRIMARY for i in g.index]
    bars = ax.bar(g.index, g["mean"], color=colors)
    for b, m, n in zip(bars, g["mean"], g["count"]):
        ax.text(b.get_x() + b.get_width() / 2, m + 0.02, f"{m:.1%}\n(n={n:,})", ha="center")
    ax.set_ylim(0, 0.85)
    ax.set_ylabel("Churn rate")
    ax.set_title("Promo codes nearly halve churn")
    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    return save(fig, "04_promo_impact.png")


def fig_dining_spend(df: pd.DataFrame) -> Path:
    """Dining is the only spending category that strongly differs by churn."""
    fig, ax = plt.subplots(figsize=(8, 5))
    spend_cols = ["RoomService", "Dining", "Retail", "Spa", "Entertainment"]
    means = (
        df.groupby("Churned")[spend_cols]
        .mean()
        .T.rename(columns={0: "Retained", 1: "Churned"})
    )
    means.plot(kind="bar", ax=ax, color=[PRIMARY, ACCENT], width=0.7)
    ax.set_ylabel("Average spend ($)")
    ax.set_xlabel("Spending category")
    ax.set_title("Dining drives the spending signal — Churned guests dine $2.4k less")
    ax.legend(title=None)
    plt.xticks(rotation=20)
    return save(fig, "05_spend_by_churn.png")


def fig_survey_useless(df: pd.DataFrame) -> Path:
    g = df.groupby("SurveyScore")["Churned"].agg(["mean", "count"]).reset_index()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(g["SurveyScore"].astype(int), g["mean"], color=NEUTRAL)
    ax.axhline(0.5, ls="--", color=ACCENT, label="overall churn rate")
    for b, m, n in zip(bars, g["mean"], g["count"]):
        ax.text(b.get_x() + b.get_width() / 2, m + 0.01, f"{m:.1%}", ha="center")
    ax.set_xlabel("Post-stay survey score (1–5)")
    ax.set_ylabel("Churn rate")
    ax.set_ylim(0.4, 0.6)
    ax.set_title("Surprise: survey score is essentially useless")
    ax.legend(loc="upper right")
    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    return save(fig, "06_survey_useless.png")


def fig_missing_pattern(df: pd.DataFrame) -> Path:
    nulls = df.isnull().sum().sort_values(ascending=False)
    nulls = nulls[nulls > 0]
    pct = (nulls / len(df) * 100).round(1)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(pct.index[::-1], pct.values[::-1], color=PRIMARY)
    ax.set_xlabel("% missing")
    ax.set_title("Missing-value pattern (train)")
    for bar, v in zip(bars, pct.values[::-1]):
        ax.text(v + 0.6, bar.get_y() + bar.get_height() / 2, f"{v:.1f}%", va="center", fontsize=10)
    ax.set_xlim(0, max(pct.values) * 1.15)
    return save(fig, "07_missing_pattern.png")


def fig_model_leaderboard(reports_dir: Path) -> Path:
    """CV leaderboard across all models we tried."""
    rows = [
        ("Logistic Regression", 0.8199),
        ("Random Forest",       0.8225),
        ("XGBoost",             0.8416),
        ("LightGBM (native cats)", 0.8467),
        ("CatBoost",            0.8513),
        ("Weighted Ensemble",   0.8523),
    ]
    df = pd.DataFrame(rows, columns=["Model", "CV F1 macro"])
    df = df.sort_values("CV F1 macro")
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    colors = [PRIMARY] * (len(df) - 1) + [ACCENT]
    bars = ax.barh(df["Model"], df["CV F1 macro"], color=colors)
    for b, v in zip(bars, df["CV F1 macro"]):
        ax.text(v + 0.001, b.get_y() + b.get_height() / 2, f"{v:.4f}", va="center")
    ax.set_xlim(0.81, 0.86)
    ax.set_xlabel("5-fold CV F1 macro")
    ax.set_title("Model journey — CatBoost wins solo, ensemble adds the final push")
    return save(fig, "08_model_leaderboard.png")


def fig_confusion_matrix(reports_dir: Path) -> Path:
    """Final ensemble OOF confusion matrix."""
    oof = pd.read_csv(reports_dir / "oof_predictions.csv")
    weighted = 0.5 * oof["p_catboost"] + 0.3 * oof["p_lightgbm"] + 0.2 * oof["p_xgboost"]
    pred = (weighted >= 0.5).astype(int)
    from sklearn.metrics import confusion_matrix, classification_report

    cm = confusion_matrix(oof["Churned"], pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt=",d",
        cmap="Blues",
        xticklabels=["Pred Retained", "Pred Churned"],
        yticklabels=["Actual Retained", "Actual Churned"],
        cbar=False,
        ax=ax,
        annot_kws={"size": 16, "weight": "bold"},
    )
    ax.set_title("Final ensemble — OOF confusion matrix")
    print(classification_report(oof["Churned"], pred, target_names=["Retained", "Churned"]))
    return save(fig, "09_confusion_matrix.png")


def main() -> None:
    train_raw, _, _ = load_raw()
    train = basic_clean(train_raw)

    paths = [
        fig_target_balance(train),
        fig_allinclusive_paradox(train),
        fig_ai_x_region_heatmap(train),
        fig_promo_impact(train),
        fig_dining_spend(train),
        fig_survey_useless(train),
        fig_missing_pattern(train),
        fig_model_leaderboard(REPO_ROOT / "reports"),
        fig_confusion_matrix(REPO_ROOT / "reports"),
    ]
    print("\nFigures written:")
    for p in paths:
        print(f"  {p.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
