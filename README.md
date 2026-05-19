# Team-Union, MMAI 869 Project

This is our group submission for the Steve's Luxury Resort churn competition in MMAI 869. The task is binary classification on guest booking and spending data, scored with macro F1.

Course repo: https://github.com/stepthom/869_course

## Where we ended up

Our best 5-fold CV macro F1 was 0.8523, from a weighted blend of CatBoost, LightGBM and XGBoost. The strongest single model was CatBoost at 0.8513. The final submission we sent to Kaggle is `submissions/ensemble_weighted.csv`. The slide deck lives at `reports/Team-Union_MMAI869_Final.pptx` and the main EDA is in `notebooks/01_eda_and_modeling.ipynb`.

## Main thing we found in EDA

Guests on the All-Inclusive package churn far more often than non-AI guests (about 81.9% vs 32.8% in the training set). The effect is even stronger for All-Inclusive guests in the Europe region, where 722 rows show roughly 98.6% churn. A few features in `src/features.py` (`AI_Europe`, `AI_Adventure`, `HasPromo`) try to capture that.

## Repo layout

```
Team-Union/
  data/
    raw/         # Kaggle CSVs, gitignored
    processed/   # cleaned and feature engineered, gitignored
  notebooks/     # Jupyter EDA and modelling
  src/           # reusable Python modules
  submissions/   # CSVs for Kaggle, gitignored
  reports/       # deck and figures
  requirements.txt
  README.md
```

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name team-union
```

## How we ran things

We roughly followed this notebook order. First, `notebooks/01_eda.ipynb` for the exploratory pass. Then `notebooks/02_baseline.ipynb` for the first set of models and our first Kaggle submission. From there we iterated on feature engineering in `notebooks/03_features.ipynb`, tuned the top two or three models in `notebooks/04_tuning.ipynb`, and built the final ensemble and submission file in `notebooks/05_final.ipynb`.

## Submission format

A CSV with columns `GuestID,Churned`. See `data/raw/sample_submission.csv` for the exact shape.
