# Team-Union — MMAI 869 Project

Kaggle competition: **Steve's Luxury Resort (MMAI)** — predict guest churn using booking and on-site spending data. Metric: F-Score (Macro).

Course repo: https://github.com/stepthom/869_course

## TL;DR

| Item | Value |
|---|---|
| Best CV F1-macro | **0.8523** (weighted ensemble) |
| Best solo model | CatBoost — 0.8513 |
| Final submission | `submissions/ensemble_weighted.csv` |
| Presentation deck | `reports/Team-Union_MMAI869_Final.pptx` |
| EDA notebook | `notebooks/01_eda_and_modeling.ipynb` |

## Headline finding

**The All-Inclusive paradox:** Premium All-Inclusive guests churn at 81.9% vs 32.8% for non-AI. The All-Inclusive × Europe cohort hits **98.6% churn** (n=722).

## Repo layout

```
Team-Union/
├── data/
│   ├── raw/             # Kaggle CSVs (gitignored)
│   └── processed/       # Cleaned/feature-engineered (gitignored)
├── notebooks/           # Jupyter EDA + modelling notebooks
├── src/                 # Reusable Python modules (loaders, features, eval)
├── submissions/         # CSV files for Kaggle (gitignored)
├── reports/             # Final deck + figures
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name team-union
```

## Workflow

1. Run `notebooks/01_eda.ipynb` for data exploration.
2. Run `notebooks/02_baseline.ipynb` for first models + first Kaggle submission.
3. Iterate on feature engineering in `notebooks/03_features.ipynb`.
4. Tune top models in `notebooks/04_tuning.ipynb`.
5. Ensemble + final submission in `notebooks/05_final.ipynb`.

## Submission format

CSV with columns `GuestID,Churned` — see `data/raw/sample_submission.csv`.
