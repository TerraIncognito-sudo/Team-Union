"""Feature engineering for the resort churn data."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .data import SPEND_COLS


def split_room(df: pd.DataFrame) -> pd.DataFrame:
    """Break the Room string (Wing/Floor/View) into three columns."""
    df = df.copy()
    if "Room" not in df.columns:
        return df

    parts = df["Room"].astype(str).str.split("/", expand=True)
    if parts.shape[1] >= 3:
        df["Room_Wing"] = parts[0].replace({"None": np.nan, "nan": np.nan})
        df["Room_Floor"] = pd.to_numeric(parts[1], errors="coerce")
        df["Room_View"] = parts[2].replace({"None": np.nan, "nan": np.nan})
    return df


def date_features(df: pd.DataFrame) -> pd.DataFrame:
    """Pull common calendar parts out of BookingDate."""
    df = df.copy()
    if "BookingDate" not in df.columns:
        return df
    bd = pd.to_datetime(df["BookingDate"], errors="coerce")
    df["BookingYear"] = bd.dt.year
    df["BookingMonth"] = bd.dt.month
    df["BookingDayOfWeek"] = bd.dt.dayofweek
    df["BookingDayOfYear"] = bd.dt.dayofyear
    df["BookingIsWeekend"] = (bd.dt.dayofweek >= 5).astype(float)
    df["BookingQuarter"] = bd.dt.quarter
    return df


def spend_features(df: pd.DataFrame) -> pd.DataFrame:
    """Totals, ratios and log spend per category."""
    df = df.copy()
    spend = df[SPEND_COLS].fillna(0)
    df["TotalSpend"] = spend.sum(axis=1)
    df["SpendCategoriesUsed"] = (spend > 0).sum(axis=1)

    # Per-category share of total spend, safe against zero totals.
    total = df["TotalSpend"].replace(0, np.nan)
    for col in SPEND_COLS:
        df[f"{col}_Ratio"] = (spend[col] / total).fillna(0)

    # Spend is heavily right-skewed, so log1p tends to help linear models.
    for col in SPEND_COLS + ["TotalSpend"]:
        df[f"{col}_Log"] = np.log1p(df[col].fillna(0))
    return df


def missingness_flags(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    """Add a 0/1 flag for each column that has nulls in it."""
    df = df.copy()
    if cols is None:
        cols = ["Age", "Room", "Region", "AllInclusive", "VIP", "PackageType"] + SPEND_COLS
    for col in cols:
        if col in df.columns:
            df[f"{col}_Missing"] = df[col].isna().astype(float)
    return df


def domain_features(df: pd.DataFrame) -> pd.DataFrame:
    """A few cross-features that came out of the EDA pass."""
    df = df.copy()
    # In our EDA, guests with no promo code churned at about 66.9% vs roughly
    # 36% for guests with any promo, so a simple flag was worth keeping.
    if "PromoCode" in df.columns:
        df["HasPromo"] = (df["PromoCode"].fillna("NoPromo") != "NoPromo").astype(float)

    # All-Inclusive guests usually report zero dining spend, so a non-zero
    # dining value can act as an indirect signal about that flag.
    if "Dining" in df.columns:
        df["DiningPerDollar"] = (df["Dining"].fillna(0) > 0).astype(float)

    # Cohort flags for the two strongest churn segments we saw in EDA.
    if "AllInclusive" in df.columns and "Region" in df.columns:
        ai = df["AllInclusive"].fillna(0).astype(float)
        eu = (df["Region"].fillna("UNK") == "Europe").astype(float)
        df["AI_Europe"] = ai * eu

    if "AllInclusive" in df.columns and "PackageType" in df.columns:
        ai = df["AllInclusive"].fillna(0).astype(float)
        adv = (df["PackageType"].fillna("UNK") == "Adventure").astype(float)
        df["AI_Adventure"] = ai * adv

    return df


def add_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """Run every step in the feature pipeline."""
    df = split_room(df)
    df = date_features(df)
    df = spend_features(df)
    df = missingness_flags(df)
    df = domain_features(df)
    return df
