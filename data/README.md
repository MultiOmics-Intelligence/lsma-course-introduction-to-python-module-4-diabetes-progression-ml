# Data

| File | What it is | Source and licence |
|---|---|---|
| `diabetes.csv` | 442 patients with diabetes. Ten baseline measurements: `age`, `sex`, `bmi` (body mass index), `bp` (average blood pressure) and six blood serum measurements `s1`–`s6` (total cholesterol, LDL, HDL, total/HDL ratio, a triglyceride measure and blood sugar). `target` is a measure of disease progression one year after baseline. Original units (scikit-learn's `scaled=False`). | Efron, B., Hastie, T., Johnstone, I. and Tibshirani, R. (2004), "Least angle regression", Annals of Statistics 32(2), 407–499. Saved unchanged from `sklearn.datasets.load_diabetes(as_frame=True, scaled=False)` (scikit-learn, BSD-3-Clause licence). |

This is a public, anonymised teaching dataset: no names or identifiers. Little is published about how the patients were recruited, so treat it as teaching data, not clinical evidence. Please cite Efron et al. (2004) and scikit-learn (Pedregosa et al. 2011, Journal of Machine Learning Research 12, 2825–2830) if you reuse it.
