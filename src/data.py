"""Loading and basic cleaning for the Steve's Luxury Resort data."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "raw"

TARGET = "Churned"
ID_COL = "GuestID"

# Column groups we reuse across modules.
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
# Room comes in as Wing/Floor/View. We split it apart in features.py.
RAW_TEXT_COLS = ["Room"]


def load_raw(data_dir: Path | str = DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Read the train, test and sample submission CSVs."""
    data_dir = Path(data_dir)
    train = pd.read_csv(data_dir / "resort_train.csv")
    test = pd.read_csv(data_dir / "resort_test.csv")
    sample = pd.read_csv(data_dir / "sample_submission.csv")
    return train, test, sample


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Parse the date column and tidy up string columns. Returns a copy."""
    df = df.copy()

    if "BookingDate" in df.columns:
        df["BookingDate"] = pd.to_datetime(df["BookingDate"], errors="coerce")

    # Strip whitespace, turn nan and empty strings into real NaN.
    for col in CAT_COLS + RAW_TEXT_COLS:
        if col in df.columns and df[col].dtype == object:
            df[col] = (
                df[col].astype(str).str.strip().replace({"nan": np.nan, "": np.nan})
            )

    # Treat a missing PromoCode as its own category (no promo).
    if "PromoCode" in df.columns:
        df["PromoCode"] = df["PromoCode"].fillna("NoPromo")

    return df


def split_xy(train: pd.DataFrame, target: str = TARGET) -> tuple[pd.DataFrame, pd.Series]:
    y = train[target].astype(int)
    X = train.drop(columns=[target])
    return X, y
