"""Data loading + light cleaning for the Steve's Luxury Resort competition."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "raw"

TARGET = "Churned"
ID_COL = "GuestID"

# Feature groups
SPEND_COLS = ["RoomService", "Dining", "Retail", "Spa", "Entertainment"]
NUMERIC_COLS = ["Age", "LoyaltyPoints", "SurveyScore", "DaysSinceEmail"] + SPEND_COLS
BOOL_COLS = ["AllInclusive", "VIP"]
CAT_COLS = [
    "PromoCode",
    "Region",
    "PackageType",
    "BookingChannel",
    "AgeGroup",
    "ReferralSource",
]
DATE_COLS = ["BookingDate"]
RAW_TEXT_COLS = ["Room"]  # Wing/Floor/View — split in features.py


def load_raw(data_dir: Path | str = DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load train, test, and sample_submission CSVs."""
    data_dir = Path(data_dir)
    train = pd.read_csv(data_dir / "resort_train.csv")
    test = pd.read_csv(data_dir / "resort_test.csv")
    sample = pd.read_csv(data_dir / "sample_submission.csv")
    return train, test, sample


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Light cleaning: parse dates, fix dtypes. Returns a copy."""
    df = df.copy()

    # Parse BookingDate
    if "BookingDate" in df.columns:
        df["BookingDate"] = pd.to_datetime(df["BookingDate"], errors="coerce")

    # Strip whitespace from string cols, normalize empty/"nan"
    for col in CAT_COLS + RAW_TEXT_COLS:
        if col in df.columns and df[col].dtype == object:
            df[col] = (
                df[col].astype(str).str.strip().replace({"nan": np.nan, "": np.nan})
            )

    # Treat PromoCode null as a category (no promo) — done AFTER strip
    if "PromoCode" in df.columns:
        df["PromoCode"] = df["PromoCode"].fillna("NoPromo")

    return df


def split_xy(train: pd.DataFrame, target: str = TARGET) -> tuple[pd.DataFrame, pd.Series]:
    y = train[target].astype(int)
    X = train.drop(columns=[target])
    return X, y
