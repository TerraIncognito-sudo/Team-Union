"""Create cleaned data files and data quality reports.

Raw CSVs in datasets/ are treated as read-only inputs. Cleaned copies and
quality checks are written to data/processed/.

Run:
    python -m src.clean_data
"""
from __future__ import annotations

import pandas as pd

from .data import PROCESSED_DIR, basic_clean, data_quality_summary, load_raw


def duplicate_summary(df: pd.DataFrame, name: str) -> dict[str, int | str]:
    """Return simple duplicate checks for one dataset."""
    result: dict[str, int | str] = {
        "dataset": name,
        "duplicate_rows": int(df.duplicated().sum()),
    }
    if "GuestID" in df.columns:
        result["duplicate_guest_ids"] = int(df["GuestID"].duplicated().sum())
    return result


def write_cleaned_data() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    train_raw, test_raw, sample_submission = load_raw()
    raw_frames = {
        "train_raw": train_raw,
        "test_raw": test_raw,
        "sample_submission": sample_submission,
    }

    train_clean = basic_clean(train_raw)
    test_clean = basic_clean(test_raw)

    train_clean.to_csv(PROCESSED_DIR / "resort_train_clean.csv", index=False)
    test_clean.to_csv(PROCESSED_DIR / "resort_test_clean.csv", index=False)
    sample_submission.to_csv(PROCESSED_DIR / "sample_submission.csv", index=False)

    quality = pd.concat(
        [
            data_quality_summary(train_raw, "train_raw"),
            data_quality_summary(test_raw, "test_raw"),
            data_quality_summary(train_clean, "train_clean"),
            data_quality_summary(test_clean, "test_clean"),
        ],
        ignore_index=True,
    )
    quality.to_csv(PROCESSED_DIR / "data_quality_report.csv", index=False)

    duplicates = pd.DataFrame(
        [duplicate_summary(frame, name) for name, frame in raw_frames.items()]
    )
    duplicates.to_csv(PROCESSED_DIR / "duplicate_report.csv", index=False)

    print("Cleaned files written to data/processed/")
    print(f"  train: {train_raw.shape} -> {train_clean.shape}")
    print(f"  test:  {test_raw.shape} -> {test_clean.shape}")
    print("Reports written:")
    print("  data/processed/data_quality_report.csv")
    print("  data/processed/duplicate_report.csv")


if __name__ == "__main__":
    write_cleaned_data()
