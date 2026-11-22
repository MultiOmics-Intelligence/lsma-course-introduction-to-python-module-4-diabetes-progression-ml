"""Automatic checks for LSMA Introduction to Python, Module 4 project.

Run from the top folder of your copy:   python tests/check_results.py
It reads only the files you commit in results/ and scripts/, uses the Python
standard library only, and prints PASS or FAIL for each task.
"""
import csv
import hashlib
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
SCRIPTS = ROOT / "scripts"
DATA = ROOT / "data"
_failed = []


class Fail(Exception):
    pass


def check(label):
    """Run one labelled check and print PASS or FAIL."""
    def wrap(fn):
        try:
            fn()
        except Fail as err:
            print(f"FAIL  {label}: {err}")
            _failed.append(label)
        except Exception as err:  # an unreadable file should guide, not crash
            print(f"FAIL  {label}: could not read your results ({type(err).__name__}: {err})")
            _failed.append(label)
        else:
            print(f"PASS  {label}")
        return fn
    return wrap


def finish():
    print()
    if _failed:
        print(f"{len(_failed)} check(s) failed. Read the messages above, fix that task and push again.")
        sys.exit(1)
    print("Every checkpoint passed. Well done.")


def need(path):
    path = Path(path)
    if not path.exists():
        raise Fail(f"{path.relative_to(ROOT)} not found; create it and commit it")
    return path


def read_rows(path):
    """Read a CSV (or tab-separated) file into a list of dicts with lower-case keys."""
    text = need(path).read_text(encoding="utf-8-sig")
    dialect = "excel-tab" if "\t" in text.splitlines()[0] else "excel"
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    return [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in rows]


def column(rows, *names, path=""):
    if not rows:
        raise Fail(f"{path} has no data rows")
    for n in names:
        if n in rows[0]:
            return n
    raise Fail(f"{path} needs a column called {names[0]}; found {', '.join(rows[0])}")


def num(value, what):
    try:
        return float(str(value).replace("%", "").strip())
    except ValueError:
        raise Fail(f"{what}: '{value}' is not a number")


def near(a, b, tol):
    return abs(a - b) <= tol


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("\r", "")).strip()


def sha(path):
    return hashlib.sha256(_norm(Path(path).read_text(encoding="utf-8")).encode()).hexdigest()


def edited(path, starter_sha):
    path = need(path)
    if sha(path) == starter_sha:
        raise Fail(f"{path.relative_to(ROOT)} is still the untouched starter; write your code in it")
    return path


def png_info(path):
    """Width, height and dpi (None if not stored) of a PNG file."""
    data = Path(path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    dpi = None
    i = 8
    while i + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[i:i + 8])
        if kind == b"pHYs":
            x, _, unit = struct.unpack(">IIB", data[i + 8:i + 17])
            if unit == 1:
                dpi = x * 0.0254
            break
        if kind == b"IDAT":
            break
        i += 12 + length
    return w, h, dpi


def image(path, min_px=300, min_bytes=5000):
    """Check that a PNG or SVG is a real image of sensible size; return PNG info."""
    path = need(path)
    rel = path.relative_to(ROOT)
    size = path.stat().st_size
    if size < min_bytes:
        raise Fail(f"{rel} is only {size} bytes; it looks empty")
    if path.suffix.lower() == ".svg":
        head = path.read_text(encoding="utf-8", errors="replace")[:5000]
        if "<svg" not in head:
            raise Fail(f"{rel} is not a valid SVG file")
        return None
    info = png_info(path)
    if info is None:
        raise Fail(f"{rel} is not a real PNG file (was it renamed from another format?)")
    w, h, _ = info
    if w < min_px or h < min_px // 3:
        raise Fail(f"{rel} is only {w} x {h} pixels; save it with a higher dpi")
    return info


def text_of(path, min_words=0):
    path = need(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    words = len(re.findall(r"\w+", text))
    if words < min_words:
        raise Fail(f"{path.relative_to(ROOT)} has {words} words; write at least {min_words}")
    return text

import json
import statistics


@check("Setup · Your script")
def _():
    edited(SCRIPTS / "disease_progression.py", "c654e6ca2a3636690936d7a0caf5720d625ea8d9a0d2f88e48fbc13e7fa8ae21")


def metrics():
    try:
        return json.loads(need(RESULTS / "metrics.json").read_text())
    except json.JSONDecodeError as err:
        raise Fail(f"results/metrics.json is not valid JSON ({err})")


def metric(m, key, what):
    if key not in m:
        raise Fail(f"results/metrics.json has no \"{key}\" ({what})")
    return num(m[key], key)


DATA_ROWS = read_rows(DATA / "diabetes.csv")
FEATURES = [k for k in DATA_ROWS[0] if k != "target"]


@check("Task 1 · Explore")
def _():
    m = metrics()
    if metric(m, "n_patients", "number of rows") != 442 or metric(m, "n_features", "number of features") != 10:
        raise Fail("results/metrics.json: check the number of patients and of features (the target is not a feature)")
    if metric(m, "n_missing", "missing values in the whole table") != 0:
        raise Fail("results/metrics.json: count the missing values again (isna().sum())")
    path = "results/correlations.csv"
    rows = read_rows(RESULTS / "correlations.csv")
    f = column(rows, "feature", path=path)
    c = column(rows, "correlation", "r", path=path)
    got = {r[f].lower(): num(r[c], "correlation") for r in rows}
    target = [float(r["target"]) for r in DATA_ROWS]
    for feat in FEATURES:
        if feat not in got:
            raise Fail(f"{path} has no row for {feat}")
        want = statistics.correlation([float(r[feat]) for r in DATA_ROWS], target)
        if not near(got[feat], want, 0.01):
            raise Fail(f"{path}: the correlation of {feat} with the target is not right")
    top = sorted(got, key=lambda k: got[k], reverse=True)[:2]
    if set(top) != {"bmi", "s5"}:
        raise Fail(f"{path}: expected bmi and s5 to have the strongest positive correlation")
    image(RESULTS / "explore.png")


@check("Task 2 · Split and set a baseline")
def _():
    b = metric(metrics(), "baseline_test_mae", "MAE of always predicting the training mean")
    if not near(b, 64.0, 1.0):
        raise Fail(f"baseline test MAE is {b}; expected about 64. Use test_size=0.2, random_state=42, "
                   "no stratify, and the mean of the training targets")


@check("Task 3 · Compare four models")
def _():
    path = "results/cv_scores.csv"
    rows = read_rows(RESULTS / "cv_scores.csv")
    mcol = column(rows, "model", path=path)
    mean = column(rows, "mean_r2", path=path)
    sd = column(rows, "sd_r2", "std_r2", path=path)
    if len(rows) != 4:
        raise Fail(f"expected 4 models in {path}, found {len(rows)}")
    kinds = {"linear": "linear", "lasso": "lasso", "forest": "forest", "boost": "boost"}
    found = {}
    for r in rows:
        name = r[mcol].lower()
        for key in kinds:
            if key in name and not (key == "linear" and "lasso" in name):
                found[key] = (num(r[mean], "mean_r2"), num(r[sd], "sd_r2"))
    missing = [k for k in kinds if k not in found]
    if missing:
        raise Fail(f"{path}: could not find the {missing[0]} model; name the models linear, lasso, "
                   "random_forest and gradient_boosting")
    for k, (mu, s) in found.items():
        if not 0.25 <= mu <= 0.6:
            raise Fail(f"{path}: the mean R² of the {k} model ({mu}) is far from the checkpoint; "
                       "use the training set and scoring='r2'")
        if not 0 < s < 0.3:
            raise Fail(f"{path}: the spread (standard deviation) of R² for {k} looks wrong")
    if not near(found["linear"][0], 0.488, 0.015):
        raise Fail(f"{path}: the linear regression R² does not match the checkpoint; use "
                   "KFold(n_splits=5, shuffle=True, random_state=1) on the training set")
    if max(found["linear"][0], found["lasso"][0]) < max(found["forest"][0], found["boost"][0]):
        raise Fail(f"{path}: the tree models should not win here; check the settings "
                   "min_samples_leaf=5 and max_depth=3")


@check("Task 4 · Test once")
def _():
    m = metrics()
    chosen = str(m.get("chosen_model", "")).lower()
    if not chosen:
        raise Fail("results/metrics.json has no \"chosen_model\"")
    mae = metric(m, "test_mae", "MAE of the chosen model on the test set")
    r2 = metric(m, "test_r2", "R² of the chosen model on the test set")
    base = metric(m, "baseline_test_mae", "baseline")
    if mae >= base:
        raise Fail("the chosen model is not better than the baseline on the test set")
    if "lasso" in chosen and not (near(r2, 0.47, 0.02) and near(mae, 43, 1.5)):
        raise Fail("for the lasso, expected test R² about 0.47 and MAE about 43; fit on the full "
                   "training set and score the test set once")
    if not (0.38 <= r2 <= 0.55 and 38 <= mae <= 48):
        raise Fail(f"test R² {r2} and MAE {mae} are far from the checkpoint; check the split and the fit")
    image(RESULTS / "predicted_vs_true.png")


@check("Task 5 · Interpret")
def _():
    path = "results/importance.csv"
    rows = read_rows(RESULTS / "importance.csv")
    f = column(rows, "feature", path=path)
    i = column(rows, "importance", path=path)
    column(rows, "lasso_coef", path=path)
    if sorted(r[f].lower() for r in rows) != sorted(FEATURES):
        raise Fail(f"{path} should have one row for each of the 10 features")
    ranked = sorted(rows, key=lambda r: num(r[i], "importance"), reverse=True)
    top = {ranked[0][f].lower(), ranked[1][f].lower()}
    if top != {"bmi", "s5"}:
        raise Fail(f"{path}: the two most important features are not the ones the checkpoint expects; "
                   "compute permutation importance on the test set with a regression score")


@check("Task 6 · Report")
def _():
    text = text_of(RESULTS / "report.md", min_words=120)
    low = text.lower()
    m = metrics()
    numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]
    base = metric(m, "baseline_test_mae", "baseline")
    mae = metric(m, "test_mae", "test MAE")
    if not any(near(x, mae, 0.5) for x in numbers):
        raise Fail("results/report.md should give the test MAE in the target's units")
    if not any(near(x, base, 0.5) for x in numbers):
        raise Fail("results/report.md should put the baseline MAE next to the model's MAE")
    if not re.search(r"(under|less than|below)\s+(half|50)", low):
        raise Fail("results/report.md should say how much of the variation the model explains (R²)")
    for pat, what in ((r"442", "the number of patients"), (r"one study|single study", "that the data come from one study"),
                      (r"external", "that there is no external validation")):
        if not re.search(pat, low):
            raise Fail(f"results/report.md: in the limits, state {what}")


finish()
