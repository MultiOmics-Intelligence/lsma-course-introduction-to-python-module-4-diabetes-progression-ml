"""Module 4 project: predicting disease progression.

Run from the top folder of your copy:   python scripts/disease_progression.py
You can explore in a notebook first, but keep this script as the final,
rerunnable version. Fix every random seed the tasks give you.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)
metrics = {}   # numbers for results/metrics.json, filled in as you go

# data/diabetes.csv is load_diabetes(as_frame=True, scaled=False).frame:
# ten features and the target, in their original units.
df = pd.read_csv(DATA / "diabetes.csv")

# ---------------------------------------------------------------------------
# Task 1 · Explore (lessons 1 and 6)
# ---------------------------------------------------------------------------
# TODO: rows, features and missing values -> metrics["n_patients"],
#       metrics["n_features"], metrics["n_missing"].
# TODO: correlation of each feature with the target -> results/correlations.csv
#       (columns feature, correlation).
# TODO: one figure with the distribution of the target and the correlations
#       -> results/explore.png

# ---------------------------------------------------------------------------
# Task 2 · Split and set a baseline (lessons 2 and 6)
# ---------------------------------------------------------------------------
# TODO: hold out 20% as a test set with random_state=42 (no stratify).
# TODO: MAE of always predicting the training mean -> metrics["baseline_test_mae"]

# ---------------------------------------------------------------------------
# Task 3 · Compare four models (lessons 4, 5 and 6)
# ---------------------------------------------------------------------------
# TODO: linear regression and lasso (in pipelines with scaling), a random forest
#       (min_samples_leaf=5) and gradient boosting (max_depth=3).
# TODO: the same KFold(n_splits=5, shuffle=True, random_state=1) on the training set,
#       scoring="r2" -> results/cv_scores.csv (columns model, mean_r2, sd_r2).

# ---------------------------------------------------------------------------
# Task 4 · Test once (lessons 6 and 8)
# ---------------------------------------------------------------------------
# TODO: write down which model you choose and why BEFORE you score the test set.
# TODO: fit it on the full training set, score it on the test set once
#       -> metrics["chosen_model"], metrics["test_mae"], metrics["test_r2"].
# TODO: predicted against true values with a diagonal line -> results/predicted_vs_true.png

# ---------------------------------------------------------------------------
# Task 5 · Interpret (lesson 8)
# ---------------------------------------------------------------------------
# TODO: permutation importance on the test set (a regression score such as R2),
#       next to the lasso coefficients -> results/importance.csv
#       (columns feature, importance, lasso_coef).

# ---------------------------------------------------------------------------
# Task 6 · Report (lessons 6 and 8)
# ---------------------------------------------------------------------------
# TODO: write results/report.md (see the README for what it must say).

# Save the numbers you recorded:
# (RESULTS / "metrics.json").write_text(json.dumps(metrics, indent=2))
