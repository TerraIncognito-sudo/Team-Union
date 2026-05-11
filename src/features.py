"""Feature engineering for the Steve's Luxury Resort competition."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .data import SPEND_COLS


def split_room(df: pd.DataFrame) -> pd.DataFrame:
    """Split Room (Wing/Floor/View) into 3 features."""
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
    df = df.copy()
    spend = df[SPEND_COLS].fillna(0)
    df["TotalSpend"] = spend.sum(axis=1)
    df["SpendCategoriesUsed"] = (spend > 0).sum(axis=1)

    # Ratios (safe div)
    total = df["TotalSpend"].replace(0, np.nan)
    for col in SPEND_COLS:
        df[f"{col}_Ratio"] = (spend[col] / total).fillna(0)

    # Log transform spend (heavy right tails)
    for col in SPEND_COLS + ["TotalSpend"]:
        df[f"{col}_Log"] = np.log1p(df[col].fillna(0))
    return df


def missingness_flags(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    """Add binary columns indicating null."""
    df = df.copy()
    if cols is None:
        cols = ["Age", "Room", "Region", "AllInclusive", "VIP", "PackageType"] + SPEND_COLS
    for col in cols:
        if col in df.columns:
            df[f"{col}_Missing"] = df[col].isna().astype(float)
    return df


def domain_features(df: pd.DataFrame) -> pd.DataFrame:
    """Domain-driven features informed by EDA."""
    df = df.copy()
    # HasAnyPromo: NoPromo gets 66.9% churn vs ~36% with promo
    if "PromoCode" in df.columns:
        df["HasPromo"] = (df["PromoCode"].fillna("NoPromo") != "NoPromo").astype(float)

    # Spend-implies-AllInclusive-False: AllInclusive guests usually have $0 dining
    # Useful imputation signal, plus may catch label noise
    if "Dining" in df.columns:
        df["DiningPerDollar"] = (df["Dining"].fillna(0) > 0).astype(float)

    # Risk segment flag: brittle but the highest-signal cohort
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
    """Apply the full FE pipeline."""
    df = split_room(df)
    df = date_features(df)
    df = spend_features(df)
    df = missingness_flags(df)
    df = domain_features(df)
    return df
