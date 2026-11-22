<a href="https://lsma.co.uk/courses"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/lsma-walk-courses.svg" alt="LSMA, London School of Multiomics and AI: learn by doing, on real data" width="100%"></a>

# Module 4 project: Predicting disease progression

LSMA · Introduction to Python · Module 4 project

<p>
<img src="https://img.shields.io/badge/LSMA-free%20course-D9481F?style=flat-square" alt="LSMA free course">
<img src="https://img.shields.io/badge/course-Introduction%20to%20Python-0F1B33?style=flat-square" alt="Course">
<img src="https://img.shields.io/badge/language-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Language">
<img src="https://img.shields.io/badge/checks-automatic-2F7D5B?style=flat-square&logo=githubactions&logoColor=white" alt="Automatic checks">
</p>

## Research question

How well can baseline measurements predict diabetes progression one year later, and which measurements matter most?

## What you will build

| Files in (`data/`) | Files out (`results/`) |
|---|---|
| `diabetes.csv`, 442 patients: age, sex, bmi, bp, s1–s6 and the progression `target` | `metrics.json`, the numbers you record as you go |
| | `correlations.csv` and `explore.png`, from Task 1 |
| | `cv_scores.csv`, cross-validated R² of four models |
| | `predicted_vs_true.png`, the chosen model on the test set |
| | `importance.csv`, permutation importance next to the lasso coefficients |
| | `report.md`, your short report |

`data/diabetes.csv` is exactly what `load_diabetes(as_frame=True, scaled=False).frame` gives in the lessons, saved as a file. Your code lives in `scripts/disease_progression.py`.

`results/metrics.json` holds these keys: `n_patients`, `n_features`, `n_missing` (Task 1), `baseline_test_mae` (Task 2), `chosen_model`, `test_mae` and `test_r2` (Task 4). Round MAE to 1 decimal place and R² to 3.

## Before you start

1. Get your own copy. Use the GitHub Classroom invitation link in the project lesson on [lsma.co.uk](https://lsma.co.uk), or press **Use this template** on this page.
2. Clone your copy to your computer, or open it in GitHub Codespaces.
3. Install the packages once: `pip install pandas matplotlib scikit-learn`.
4. Work in `scripts/`. Run everything from the top folder of your copy: `python scripts/disease_progression.py`.
5. Write every output to `results/`, with the exact file names above.

Fix every random seed the tasks give you (`random_state=42` for the split, `random_state=1` for the folds), and do not look at the test set until Task 4. You can run the checks yourself at any time: `python tests/check_results.py`.

## Tasks

### 1. Explore

Lesson to revisit: lessons 1 and 6.

Load the data; report rows, columns and missing values. Plot the distribution of the target and its correlation with each feature (`results/explore.png`), and save the correlations as `results/correlations.csv` (columns `feature`, `correlation`).

**Checkpoint:** 442 patients, 10 features, no missing values; BMI and s5 have the strongest positive correlation with the target.

### 2. Split and set a baseline

Lesson to revisit: lessons 2 and 6.

Hold out 20% as a test set with `random_state=42`. Compute the MAE of always predicting the training mean.

**Checkpoint:** baseline test MAE of about 64.

### 3. Compare four models

Lesson to revisit: lessons 4, 5 and 6.

Linear regression and lasso (in pipelines with scaling), a random forest (`min_samples_leaf=5`) and gradient boosting (`max_depth=3`). Use the same 5-fold `KFold(shuffle=True, random_state=1)` on the training set; report mean and spread of R² in `results/cv_scores.csv` (columns `model`, `mean_r2`, `sd_r2`; models named `linear`, `lasso`, `random_forest`, `gradient_boosting`).

**Checkpoint:** the linear models land around R² 0.48–0.49 and the random forest a little lower; the tree models do not win here.

### 4. Test once

Lesson to revisit: lessons 6 and 8.

Choose one model from the cross-validation results, fit it on the full training set and score it on the test set. Plot predicted against true values with a diagonal line (`results/predicted_vs_true.png`).

**Checkpoint:** for the lasso, test R² about 0.47 and MAE about 43, clearly better than the baseline.

### 5. Interpret

Lesson to revisit: lesson 8.

Compute permutation importance on the test set. Compare it with the lasso coefficients and explain any difference. Save both side by side in `results/importance.csv` (columns `feature`, `importance`, `lasso_coef`).

**Checkpoint:** BMI and s5 are the two most important features by a wide margin.

### 6. Report

Lesson to revisit: lessons 6 and 8.

Write a short report in `results/report.md`, using the lesson 8 template as a guide. State the limits: 442 patients from one study, a moderate R², no external validation.

**Checkpoint:** your report gives MAE in the target's units next to the baseline, and says the model explains under half the variation.

## Hand in

Commit and push `scripts/` and `results/`. The **Checks** tab (GitHub Actions) then runs. A green tick means every checkpoint passed. You can push as often as you like.

## If a check fails

Open the failed run in the Actions tab and read the log. Each line starts with PASS or FAIL and names the task, for example `FAIL  Task 2 · Split and set a baseline: ...`. The message tells you what to look at, not the answer. Fix that task, run your script again and push.

## Getting help

- The project lesson on lsma.co.uk, and the earlier lessons named in each task.
- Helix, the course tutor.
- Email info@lsma.co.uk.

Never post personal data in public, in an issue, a commit or a file.

**Follow LSMA**

<p>
  <a href="https://lsma.co.uk"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-website.svg" alt="LSMA: lsma.co.uk" height="54"></a>
  <a href="https://www.linkedin.com/showcase/113252126/"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-linkedin.svg" alt="LSMA on LinkedIn" height="54"></a>
  <a href="https://www.instagram.com/lsma.uk/"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-instagram.svg" alt="LSMA on Instagram: @lsma.uk" height="54"></a>
  <a href="mailto:info@lsma.co.uk"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-email.svg" alt="Email: info@lsma.co.uk" height="54"></a>
</p>

Good luck, and enjoy the project.

**Dr. Anas Alzaeem**<br>
Academic Director, LSMA

[![Dr. Anas Alzaeem, Academic Director, LSMA](https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/signature/LSMA_Banner_Anas_Alzaeem.png)](https://lsma.co.uk)

© 2026 MultiOmics Intelligence Ltd. LSMA is the education arm of MultiOmics Intelligence. Code licensed under MIT.
