---
publish_time: 1792302965
link: https://www.marktechpost.com/2026/10/17/how-to-make-zero-training-tabular-predictions-with-nvidia-structured-data-models/
source: MarkTechPost
status: confirmed
category: 其他
is_model_related: false
digest: |
  NVIDIA 发布 Structured Data Models 库，将多个面向表格数据的预训练基础模型统一封装在一个 PyTorch 接口之后，使开发者无需自行训练即可对表格数据做预测。文章以教程形式演示如何加载该库、调用预训练表格基础模型完成零训练（zero-training）的表格预测任务，适用于需要快速从结构化数据中获取预测结果、而又缺乏标注数据或训练资源的场景。该内容属于传统机器学习/表格建模工具实践，与生成式大模型主线无关。
---

# 用 NVIDIA 结构化数据模型实现零训练表格预测

> 原文链接：https://www.marktechpost.com/2026/10/17/how-to-make-zero-training-tabular-predictions-with-nvidia-structured-data-models/
> 来源：MarkTechPost

In this tutorial, we implement Structured Data Models, NVIDIA&#8217;s new library that puts several pretrained foundation models for tables behind one PyTorch interface, and use it to make predictions without training. The library wraps TabICLv2 and KumoTabular for single tables and KumoRelational for whole relational databases, and each of them answers by in-context learning: we hand the model a set of labeled rows and the rows we want predicted, and it returns probabilities or a full predictive distribution in one forward pass. We start with the library&#8217;s typed table tensors, compare the two tabular models against trained scikit-learn baselines, reuse an encoded context across many queries, read calibrated prediction intervals off a regression, and scale to twenty classes. We then look at the places where the defaults quietly do the wrong thing: a preprocessing recipe that drops timestamp and text columns and an explainer with two traps in it, before building a small three-table shop database and predicting customer activity from it directly, including the one argument that separates an honest relational model from a leaky one. Check out the Full CODES here.

Copy CodeCopiedUse a different Browser

import os
import sys
import time
import textwrap
import traceback
import subprocess

RESULTS = {}

def banner(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

def section(name):
    def wrap(fn):
        def run(*a, **kw):
            banner(name)
            try:
                out = fn(*a, **kw)
                RESULTS[name] = out if isinstance(out, str) else "ok"
                return out
            except Exception as e:
                RESULTS[name] = f"SKIPPED / FAILED -> {type(e).__name__}: {e}"
                print(f"\n[!] {name} did not complete: {type(e).__name__}: {e}")
                traceback.print_exc(limit=3)
                return None
        return run
    return wrap

banner("1. Install SDM, and the one wheel URL its own error message gets wrong")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "git+https://github.com/NVIDIA/structured-data-models.git@b982fbf4188ea8db17249fe81338723106100b63"], check=True)

import torch

# The relational sampler needs pyg-lib on CPU. Its wheels are published per MINOR torch version
# (torch-2.14.0+cpu.html), but SDM's own ImportError builds the URL from the exact patch version
# (torch-2.14.1+cpu.html), which is an empty page. Build it from MAJOR.MINOR.0 instead.
major, minor = torch.__version__.split("+")[0].split(".")[:2]
flavour = "cpu" if torch.version.cuda is None else "cu" + torch.version.cuda.replace(".", "")
PYG_INDEX = f"https://data.pyg.org/whl/torch-{major}.{minor}.0+{flavour}.html"
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pyg-lib", "-f", PYG_INDEX], check=True)

import numpy as np
import pandas as pd
import pyg_lib
import sdm
import sdm.processing as sp
from sklearn.datasets import load_breast_cancer, load_diabetes, make_classification
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, RidgeCV
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DEVICE = "cpu"   # verified end to end on CPU; on a T4 runtime set "cuda" for the tabular models
print(f"  sdm {sdm.__version__}  |  torch {torch.__version__}  |  pyg-lib {pyg_lib.__version__}"
      f"  |  device {DEVICE}")
print(f"  pyg-lib wheels from {PYG_INDEX}")
print("\n  One interface over several pretrained structured-data foundation models:")
for name, what, weights in [
    ("TabICLv2", "tabular, in-context learning (ICML '26)", "~110 MB per task head, BSD-3"),
    ("KumoTabular", "tabular, small / medium / large", "small ~110 MB, large ~855 MB, OpenMDW"),
    ("KumoRelational", "multi-table, KumoRFM-2", "~120 MB, OpenMDW"),
    ("TabFM, TimesFM 3", "Google tabular / time series", "6.5 GB / 1.3 GB, non-commercial: not used here"),
]:
    print(f"    {name:18s} {what:42s} {weights}")
print("\n  No model below is trained or fine-tuned. Every prediction is a forward pass that reads")
print("  labelled 'context' rows and answers 'query' rows, like a prompt with examples in it.")

We install Structured Data Models from the GitHub repository, pinned to the commit this notebook was verified against, since the package on PyPI is only a placeholder. The relational sampler also needs pyg-lib, and that is where the first trap lies. pyg-lib wheels are published per minor PyTorch release, on pages named like torch-2.14.0+cpu, but the library&#8217;s own ImportError builds the URL from the exact patch version, torch-2.14.1+cpu, which is an empty page, so following its advice fails. We build the index URL from the major and minor version instead. We run everything on the CPU, which is the path verified end to end here, and print the models the library exposes together with their checkpoint sizes and licenses; the two Google models it also wraps, TabFM and TimesFM 3, are large and non-commercial and are left out. Check out the Full CODES here.

Copy CodeCopiedUse a different Browser

@section("2. Typed tables: what infer_stypes decides, and what a round trip changes")
def typed_tables():
    rng = np.random.default_rng(0)
    words = ["late", "refund", "great", "broken", "fast", "charged", "app", "order", "support", "item"]
    df = pd.DataFrame({
        "ticket_id": np.arange(400),
        "amount": rng.gamma(2, 30, 400).round(2),
        "units": pd.array(rng.integers(1, 5, 400), dtype="Int64"),
        "channel": rng.choice(["web", "app", "phone", None], 400),
        "opened_at": pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 86_400 * 90, 400), unit="s"),
        "comment": [" ".join(rng.choice(words, rng.integers(3, 9))) + f" #{i}" for i in range(400)],
    })
    df.loc[rng.choice(400, 25, replace=False), "units"] = pd.NA

    print("  infer_stypes(df) with the defaults, then asking it to look for text and ids:")
    for kw in ({}, {"text": "infer", "id": "infer"}):
        stypes = sdm.infer_stypes(df, **kw)
        print(f"    {str(kw or 'defaults'):34s} {', '.join(f'{c}={s}' for c, s in stypes.items())}")
    print("  With the defaults the free-text comment becomes a 400-level categorical and the id column a")
    print("  number. Both would reach the model as features. Override, or ask: text='infer', id='infer'.")

    table = sdm.TableTensor.from_pandas(df, sdm.infer_stypes(df, text="infer", id="infer"))
    print("\n" + textwrap.indent(repr(table), "  "))

    back = table.to_pandas()
    print("\n  to_pandas() round trip:")
    for col in df.columns:
        a, b = df[col], back[col]
        if col in ("amount", "units"):
            equal_values = bool(np.allclose(a.astype(float), b.astype(float), equal_nan=True))
        else:
            na_a, na_b = a.isna().to_numpy(), b.isna().to_numpy()
            equal_values = bool((na_a == na_b).all() and
                                (a[~na_a].astype(str).to_numpy() == b[~na_b].astype(str).to_numpy()).all())
        print(f"    {col:10s} {str(a.dtype):16s} -> {str(b.dtype):16s} values preserved: {equal_values}")
    print("  Values survive, including the missing ones; dtypes do not always. Numbers come back float32")
    print("  (the numerical block is one float tensor), nullable Int64 becomes float with NaN, and strings")
    print("  marked categorical come back as a pandas category.")

    base = pd.to_datetime(["2026-01-01 08:00:00"] * 3).as_unit("ns")
    whole = pd.DataFrame({"t": base})
    nanos = pd.DataFrame({"t": base + pd.to_timedelta([0, 0, 1], unit="ns")})
    print(f"\n  datetime64[ns], whole seconds:      {sdm.TableTensor.from_pandas(whole, {'t': 'datetime'}).size()} OK")
    try:
        sdm.TableTensor.from_pandas(nanos, {"t": "datetime"})
    except Exception as e:
        print(f"  same column, one value 1 ns later:  {type(e).__name__}: {str(e).split(':')[0]}")
    ok = sdm.TableTensor.from_pandas(nanos.assign(t=nanos.t.dt.floor("us")), {"t": "datetime"})
    print(f"  floor('us') first:                  {ok.size()} OK")
    print("  SDM stores datetimes as int64 microseconds and Arrow refuses any cast that drops a digit. The")
    print("  unit is not the problem; a single value with nanosecond digits fails the whole column.")
    return "6 columns -> 5 typed blocks; text and id need opting in"

typed_tables()

Everything in the library flows through TableTensor, a PyTorch tensor subclass that keeps one typed block per semantic type: numerical, categorical, datetime, text and id. infer_stypes decides the types, and with its defaults it gets two things wrong on a realistic support-ticket frame: the free-text comment becomes a categorical with four hundred levels and the ticket id becomes a number, so both would reach a model as features. Passing text and id inference flags fixes that. The round trip back to pandas preserves every value, missing ones included, but not every dtype: numbers return as float32 because the numerical block is a single float tensor, nullable integers become floats with NaN, and categorical strings return as a pandas category. On pandas 2.x the string columns print as object rather than str and the timestamp goes in at nanosecond resolution; the same values come back either way. One more trap is worth knowing before you load a real event log: the library stores datetimes as integer microseconds, and Arrow refuses any cast that would drop a digit. A nanosecond column of whole seconds converts fine, but a single value with nanosecond digits fails the whole column, so we floor timestamps to microseconds first. Check out the Full CODES here.

Copy CodeCopiedUse a different Browser

def as_table(df, target):
    return sdm.TableTensor.from_pandas(df, sdm.infer_stypes(df, overrides={target: "categorical"}), device=DEVICE)

@section("3. Zero-training classification: two foundation models vs. two trained baselines")
def zero_training():
    df = load_breast_cancer(as_frame=True).frame.sample(frac=1, random_state=0).reset_index(drop=True)
    table = as_table(df, "target")
    n_ctx = 300
    x_ctx, y_ctx = table[:n_ctx].drop_columns("target"), table[:n_ctx, "target"]
    x_q, y_q = table[n_ctx:].drop_columns("target"), df.target.to_numpy()[n_ctx:]
    rows = []
    for name, make in [("TabICLv2", lambda: sdm.models.TabICLv2(device=DEVICE)),
                       ("KumoTabular (small)", lambda: sdm.models.KumoTabular(size="small", device=DEVICE))]:
        model = make()
        torch.manual_seed(0)
        proba = model(x_context=x_ctx, y_context=y_ctx, x_query=x_q, num_estimators=4).to_pandas()
        rows.append((name, "none", proba.idxmax(axis=1).astype(int).to_numpy(), proba["1"].to_numpy()))
    X, y = df.drop(columns="target"), df.target
    for name, est in [("LogisticRegression", make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))),
                      ("HistGradientBoosting", HistGradientBoostingClassifier(random_state=0))]:
        est.fit(X[:n_ctx], y[:n_ctx])
        rows.append((name, "fit on 300 rows", est.predict(X[n_ctx:]), est.predict_proba(X[n_ctx:])[:, 1]))
    print(f"  breast cancer: {n_ctx} labelled rows, {len(y_q)} to predict, 30 numeric features\n")
    print(f"  {'model':22s} {'training':16s} {'accuracy':>9s} {'AUC':>7s}")
    for name, training, pred, score in rows:
        print(f"  {name:22s} {training:16s} {np.mean(pred == y_q):9.3f} {roc_auc_score(y_q, score):7.3f}")
    print("\n  The output is itself a TableTensor: one probability column per class, named by label.")
    best = max(rows[:2], key=lambda r: np.mean(r[2] == y_q))
    return f"{best[0]} {np.mean(best[2] == y_q):.3f} accuracy with no training"

zero_training()

The tabular models take labelled context rows and unlabelled query rows and return a TableTensor with one probability column per class, named by label, so there is no fit step and no hyperparameters. On the breast cancer dataset, with three hundred labelled rows and two hundred and sixty-nine to predict, TabICLv2 and KumoTabular reach 0.970 accuracy and AUCs of 0.996 and 0.995 with no training, against 0.970 and 0.993 for a logistic regression and 0.967 and 0.992 for gradient boosting, both fitted on the same three hundred rows. num_estimators sets how many differently preprocessed views of the data the model averages over, which is the library&#8217;s built-in ensembling.

Copy CodeCopiedUse a different Browser

@section("4. fit() once, predict() many: the cached context")
def kv_cache():
    df = load_breast_cancer(as_frame=True).frame.sample(frac=1, random_state=0).reset_index(drop=True)
    table = as_table(df, "target")
    x_ctx, y_ctx = table[:400].drop_columns("target"), table[:400, "target"]
    batches = [table[400 + 30 * i: 430 + 30 * i].drop_columns("target") for i in range(5)]
    model = sdm.models.TabICLv2(device=DEVICE)

    torch.manual_seed(0)
    t0 = time.time()
    for b in batches:
        model(x_context=x_ctx, y_context=y_ctx, x_query=b, num_estimators=4)
    t_forward = time.time() - t0

    torch.manual_seed(0)
    t0 = time.time()
    model.fit(x=x_ctx, y=y_ctx, num_estimators=4)
    t_fit = time.time() - t0
    t0 = time.time()
    for b in batches:
        model.predict(b)
    t_predict = time.time() - t0
    model.clear()
    print("  five batches of 30 query rows against the same 400 context rows:")
    print(f"    forward() x5                      {t_forward:6.2f}s  (context re-encoded every call)")
    print(f"    fit() once + predict() x5         {t_fit + t_predict:6.2f}s  (fit {t_fit:.2f}s, predicts {t_predict:.2f}s)")
    print(f"    per batch: {t_forward / 5:.2f}s vs {t_predict / 5:.2f}s")
    print("\n  fit() encodes the context once into a key/value cache; predict() only runs the queries.")
    print("  clear() frees it. Nothing is learned: fit() here means 'remember these examples'.")
    return f"{t_forward / (t_fit + t_predict):.1f}x faster for five batches"

kv_cache()

Calling the model directly re-encodes the context on every call. When the same labelled rows will answer many batches of queries, fit encodes the context once into a key and value cache and predict then runs only the query rows; clear frees the cache. Nothing is learned in fit, which here means remember these examples. Answering five batches of thirty rows against the same four hundred context rows finished several times faster this way on our CPU, and once the context was cached, each further batch cost a small fraction of a full forward pass. The exact ratio depends on the machine, which is why the cell measures it rather than assuming it.

Copy CodeCopiedUse a different Browser

@section("5. Regression returns a distribution: 999 quantiles, and how honest they are")
def quantile_regression():
    df = load_diabetes(as_frame=True).frame.sample(frac=1, random_state=0).reset_index(drop=True)
    table = sdm.TableTensor.from_pandas(df, sdm.infer_stypes(df), device=DEVICE)
    model = sdm.models.TabICLv2(device=DEVICE)
    torch.manual_seed(0)
    q = model(x_context=table[:300].drop_columns("target"), y_context=table[:300, "target"],
              x_query=table[300:].drop_columns("target"), num_estimators=4).to_pandas()
    y = df.target.to_numpy()[300:]
    print(f"  output: {q.shape[1]} columns {list(q.columns[:3])} ... {list(q.columns[-2:])} per query row")

    X, Y = df.drop(columns="target"), df.target
    rmse = lambda p: float(np.sqrt(np.mean((np.asarray(p) - y) ** 2)))
    print(f"\n  {'point prediction':34s} {'RMSE':>7s}")
    print(f"  {'TabICLv2 median (q500), no training':34s} {rmse(q['q500']):7.2f}")
    print(f"  {'RidgeCV, fit on 300 rows':34s} {rmse(RidgeCV().fit(X[:300], Y[:300]).predict(X[300:])):7.2f}")
    print(f"  {'HistGradientBoosting, fit on 300':34s} "
          f"{rmse(HistGradientBoostingRegressor(random_state=0).fit(X[:300], Y[:300]).predict(X[300:])):7.2f}")

    print(f"\n  {'interval':12s} {'nominal':>8s} {'empirical coverage':>19s} {'mean width':>11s}")
    coverage = {}
    for lo, hi in [("q250", "q750"), ("q100", "q900"), ("q050", "q950")]:
        nominal = (int(hi[1:]) - int(lo[1:])) / 1000
        coverage[nominal] = float(np.mean((y >= q[lo]) & (y <= q[hi])))
        print(f"  {lo}-{hi:6s} {nominal:8.0%} {coverage[nominal]:19.3f} {np.mean(q[hi] - q[lo]):11.1f}")
    print("\n  The quantiles come from one forward pass over 300 examples, yet the 80% and 90% intervals")
    print("  cover close to 80% and 90% of held-out targets. The 50% band runs a little narrow.")
    return f"median RMSE {rmse(q['q500']):.1f}; 80% interval covers {coverage[0.8]:.1%}"

quantile_regression()

For regression, the model does not return a single number. It returns 999 quantiles per query row, a full predictive distribution read off one forward pass. On the diabetes dataset with three hundred labelled rows, the median of that distribution has an RMSE of 53.6, slightly better than RidgeCV at 54.3 and clearly better than gradient boosting at 64.7, both trained on the same rows. The more useful property is calibration: the interval between the 10th and 90th percentiles contains 81.0 percent of the held-out targets and the 5th to 95th percentile interval 91.5 percent, close to their nominal 80 and 90 percent, while the 50 percent band runs somewhat narrow at 43.7 percent.

Copy CodeCopiedUse a different Browser

@section("6. Twenty classes from one forward pass")
def many_classes():
    X, y = make_classification(n_samples=800, n_features=12, n_informative=8, n_redundant=2, n_classes=20,
                               n_clusters_per_class=1, class_sep=1.5, random_state=0)
    df = pd.DataFrame(X, columns=[f"f{i}" for i in range(12)])
    df["label"] = [f"c{v:02d}" for v in y]
    table = as_table(df, "label")
    model = sdm.models.TabICLv2(device=DEVICE)
    torch.manual_seed(0)
    t0 = time.time()
    proba = model(x_context=table[:600].drop_columns("label"), y_context=table[:600, "label"],
                  x_query=table[600:].drop_columns("label"), num_estimators=1).to_pandas()
    secs = time.time() - t0
    acc = float(np.mean(proba.idxmax(axis=1).to_numpy() == df.label.to_numpy()[600:]))
    hgb = HistGradientBoostingClassifier(random_state=0).fit(X[:600], y[:600])
    acc_hgb = float(np.mean(hgb.predict(X[600:]) == y[600:]))
    print(f"  20 balanced classes, 600 labelled rows (30 per class), 200 queries")
    print(f"    TabICLv2, no training          {proba.shape[1]} probability columns, accuracy {acc:.3f}  ({secs:.1f}s)")
    print(f"    HistGradientBoosting, trained  accuracy {acc_hgb:.3f}")
    print("\n  The pretrained head has a fixed number of class slots. Past that, SDM splits the problem")
    print("  into error-correcting output codes (sdm.models.ecoc) and recombines the log-probabilities,")
    print("  so the caller still gets one column per label without doing anything.")
    return f"20 classes: {acc:.3f} vs {acc_hgb:.3f} for gradient boosting"

many_classes()

The pretrained classification head has a fixed number of class slots, and the library handles problems with more classes than that through error-correcting output codes, splitting the problem into smaller coded subproblems and recombining the log-probabilities. The caller never sees this: on a balanced twenty-class synthetic problem with thirty labelled rows per class, TabICLv2 returns twenty probability columns and reaches 0.760 accuracy in a single forward pass, against 0.615 for gradient boosting trained on the same rows.

Copy CodeCopiedUse a different Browser

def make_tickets(n=1600, seed=1):
    """Support tickets whose escalation depends on WHEN they were opened and WHAT they say."""
    rng = np.random.default_rng(seed)
    opened = pd.Timestamp("2026-03-02") + pd.to_timedelta(rng.integers(0, 86_400 * 56, n), unit="s")
    neutral = ["order", "item", "delivery", "account", "app", "invoice", "question", "help", "update", "status"]
    hot = ["refund", "broken", "charged", "twice"]
    comments, has_hot = [], []
    for _ in range(n):
        words = list(rng.choice(neutral, rng.integers(4, 9)))
        flag = rng.random() < 0.3
        if flag:
            words.insert(rng.integers(len(words)), rng.choice(hot))
        comments.append(" ".join(words))
        has_hot.append(flag)
    hour, weekend = np.asarray(opened.hour), np.asarray(opened.dayofweek >= 5)
    amount = rng.gamma(2, 40, n).round(2)
    logit = (-1.6 + 2.2 * np.array(has_hot) + 1.4 * ((hour >= 22) | (hour < 6)) + 1.0 * weekend
             + 0.004 * (amount - 80))
    escalated = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return pd.DataFrame({"amount": amount, "channel": rng.choice(["web", "app", "phone"], n),
                         "opened_at": opened, "comment": comments, "escalated": escalated})

@section("7. Recipes: the default one drops your timestamps and your text, and says so once")
def recipes():
    df = make_tickets()
    stypes = sdm.infer_stypes(df, overrides={"escalated": "categorical"}, text="infer")
    table = sdm.TableTensor.from_pandas(df, stypes, device=DEVICE)
    x_ctx, y_ctx = table[:1000].drop_columns("escalated"), table[:1000, "escalated"]
    x_q, y_q = table[1000:].drop_columns("escalated"), df.escalated.to_numpy()[1000:]
    print(f"  columns: {', '.join(f'{c}={s}' for c, s in stypes.items())}")
    print("  escalation is driven by night-time / weekend opening and by words like 'refund'\n")

    default = sdm.models.TabICLv2.default_recipe()
    with_calendar = sdm.models.TabICLv2.default_recipe()
    with_calendar.prepend_features(sp.StypeDispatch(
        datetime=sp.AddCalendarFields(["hour", "weekday"], encoding="cyclic")))
    calendar_and_text = sp.StypeDispatch(
        datetime=sp.AddCalendarFields(["hour", "weekday"], encoding="cyclic"),
        text=sp.TFIDF(ngram_range=(1, 1), max_features=64))
    with_both = sdm.models.TabICLv2.default_recipe()
    with_both.prepend_features(calendar_and_text)

    model = sdm.models.TabICLv2(device=DEVICE)
    aucs = {}
    for label, recipe in [("default recipe", default),
                          ("+ AddCalendarFields(hour, weekday)", with_calendar),
                          ("+ AddCalendarFields + TFIDF(64 terms)", with_both)]:
        torch.manual_seed(0)
        proba = model(x_context=x_ctx, y_context=y_ctx, x_query=x_q, num_estimators=4, recipe=recipe).to_pandas()
        aucs[label] = roc_auc_score(y_q, proba["1"])
        print(f"  {label:40s} AUC {aucs[label]:.3f}")

    print("\n  The default TabICLv2 recipe dispatches on stype and only has branches for categorical and")
    print("  numerical columns, so datetime and text columns never become features. SDM does say so, in")
    print("  the RuntimeWarning above, but it is a warn-once: it fires the first time and is suppressed for")
    print("  the rest of the process. Every later model in the same notebook or service drops those columns")
    print("  in silence. The fix is two processors, prepended to the features:")
    print(textwrap.indent(repr(calendar_and_text), "    "))
    return " -> ".join(f"{v:.3f}" for v in aucs.values()) + " AUC"

recipes()

Preprocessing in the library is a Recipe of composable processors, and the default TabICLv2 recipe dispatches on semantic type with branches only for categorical and numerical columns. Timestamp and text columns therefore never become features. On support tickets whose escalation depends on when they were opened and on words such as refund, the default recipe scores an AUC of 0.525, close to chance. The library does emit a RuntimeWarning naming the ignored column types. Still, it is a warn-once: it fires the first time and is suppressed for the rest of the process, so every later model in the same notebook or service drops those columns in silence. Prepending two processors fixes it: AddCalendarFields turns the timestamp into cyclic hour and weekday features, lifting the AUC to 0.634, and TFIDF adds the comment&#8217;s terms, lifting it to 0.789.

Copy CodeCopiedUse a different Browser

@section("8. Explaining a prediction: two traps inside the explainer")
def explain():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(500, 8))
    true = {"x0": 2.0, "x3": -1.5, "x5": 1.0}
    logit = sum(w * X[:, int(c[1:])] for c, w in true.items())
    df = pd.DataFrame(X, columns=[f"x{i}" for i in range(8)])
    df["y"] = (rng.random(500) < 1 / (1 + np.exp(-logit))).astype(int)
    table = as_table(df, "y")
    model = sdm.models.TabICLv2(device=DEVICE)
    ctx = dict(x_context=table[:400].drop_columns("y"), y_context=table[:400, "y"])
    x_q = table[400:].drop_columns("y")
    p1 = lambda pred: pred.numerical[..., pred.columns[sdm.Stype.numerical].index("1")]   # P(y=1), by NAME

    seen = []
    def peek(pred):
        seen.append(pred.columns[sdm.Stype.numerical])
        return pred.numerical.sum() * 0
    torch.manual_seed(0)
    sdm.explain.GradientExplainer(output=peek).explain(model, x_q, num_estimators=4, **ctx)
    print(f"  num_estimators=4: the output function is called {len(seen)} times, class order per call:")
    print(f"    {seen}")

    def only_call(n):
        calls = {"i": 0}
        def f(pred):
            calls["i"] += 1
            return p1(pred) if calls["i"] == n else p1(pred) * 0
        return f
    sizes = {}
    for n in (1, len(seen)):
        torch.manual_seed(0)
        g = sdm.explain.GradientExplainer(output=only_call(n)).explain(model, x_q, num_estimators=4, **ctx)
        sizes[n] = float(g.x.to_pandas().abs().mean().mean())
    print(f"\n  Trap 1 - only the LAST estimator is explained. Output function live only on call 1:"
          f" mean |grad| {sizes[1]:.4f};")
    print(f"  live only on call {len(seen)}: {sizes[len(seen)]:.4f}. Each call overwrites the previous result, so")
    print("  with several estimators you get one of them, not their average. Explain with num_estimators=1.")

    print("\n  Trap 2 - class order differs per estimator. num_estimators=1, six seeds, P(y=1) selected two ways:")
    print(f"  {'seed':>6s} {'order':>12s}   " + "".join(f"{c + f' ({true[c]:+.1f})':>20s}" for c in true))
    print(f"  {'':6s} {'':12s}   " + "".join(f"{'position / name':>20s}" for _ in true))
    by_name = []
    flipped = name_ok = 0
    for seed in range(6):
        order = []
        def note(pred):
            order.append(pred.columns[sdm.Stype.numerical])
            return pred.numerical.sum() * 0
        torch.manual_seed(seed)
        sdm.explain.GradientExplainer(output=note).explain(model, x_q, num_estimators=1, **ctx)
        res = {}
        for label, fn in (("position", lambda pred: pred.numerical[..., 1]), ("name", p1)):
            torch.manual_seed(seed)
            res[label] = sdm.explain.GradientExplainer(output=fn).explain(
                model, x_q, num_estimators=1, **ctx).x.to_pandas().mean()
        by_name.append(res["name"])
        flipped += any(np.sign(res["position"][c]) != np.sign(w) for c, w in true.items())
        name_ok += all(np.sign(res["name"][c]) == np.sign(w) for c, w in true.items())
        print(f"  {seed:>6d} {str(order[0]):>12s}   " +
              "".join(f"{res['position'][c]:>10.2f} /{res['name'][c]:>7.2f}" for c in true))
    avg = pd.concat(by_name, axis=1).mean(axis=1)
    noise = float(avg.drop(list(true)).abs().max())
    print(f"\n  When the shuffle puts class '1' first, column 1 is P(y=0) and every sign flips. Selecting by")
    print(f"  name gives the right sign on {name_ok}/6 seeds. Averaged over the seeds, by name: " +
          ", ".join(f"{c} {avg[c]:+.2f}" for c in true) + f"; largest noise feature {noise:.2f}.")
    print("  Gradients are with respect to the PREPROCESSED, i.e. standardized, inputs.")
    return f"position flipped signs on {flipped}/6 seeds; name correct on {name_ok}/6; last estimator only"

explain()

The library&#8217;s GradientExplainer returns the gradient of a chosen output with respect to the preprocessed query inputs, and we test it on synthetic data where only three of eight features matter, with known signs. It has two traps, both visible only by looking at what the output function receives. First, the function is called once per estimator and each call overwrites the previous result, so with four estimators an output function that is live only on the first call yields an all-zero explanation, and the explanation you get is only the last estimator&#8217;s. Second, each estimator&#8217;s raw output has its own class order, because the default recipe shuffles class labels per estimator. Explaining with a single estimator across six seeds, selecting the probability of class one by column position flips the sign of every feature on the two seeds whose order is reversed, while selecting it by column name gives the right sign on all six, and averaging over the seeds recovers the three real features with the noise features near zero.

Copy CodeCopiedUse a different Browser

def make_shop(seed=0, n_customers=800, n_products=60):
    """Customers, products and a year of orders. Some customers' activity collapses at a random date."""
    rng = np.random.default_rng(seed)
    plans = rng.choice(["basic", "pro"], n_customers, p=[0.7, 0.3])
    customers = pd.DataFrame({"customer_id": np.arange(n_customers),
                              "region": rng.choice(["NA", "EU", "APAC", "LATAM"], n_customers), "plan": plans})
    products = pd.DataFrame({"product_id": np.arange(n_products),
                             "category": rng.choice(["books", "tech", "home", "toys"], n_products),
                             "price": rng.gamma(2.0, 20.0, n_products).round(2)})
    weekly_rate = rng.gamma(1.5, 0.6, n_customers) * np.where(plans == "pro", 1.6, 1.0)
    fade_day = rng.uniform(60, 500, n_customers)
    rows, start = [], pd.Timestamp("2025-01-01")
    for c in range(n_customers):
        t = 0.0
        while True:
            rate = weekly_rate[c] / 7 * (1.0 if t < fade_day[c] else 0.08)
            t += rng.exponential(1 / max(rate, 1e-6))
            if t > 364:
                break
            p = int(rng.integers(n_products))
            rows.append((c, p, start + pd.Timedelta(float(t), unit="D"), float(products.price[p] * rng.integers(1, 4))))
    orders = pd.DataFrame(rows, columns=["customer_id", "product_id", "order_date", "amount"])
    orders.insert(0, "order_id", np.arange(len(orders)))
    orders["order_date"] = orders["order_date"].dt.floor("s")
    return customers, products, orders

def task_rows(customers, orders, cutoff, horizon_days=30):
    """Label: does the customer order again within 30 days of the cutoff?"""
    window = orders[(orders.order_date > cutoff) & (orders.order_date <= cutoff + pd.Timedelta(horizon_days, unit="D"))]
    active = set(window.customer_id)
    return pd.DataFrame({"customer_id": customers.customer_id, "timestamp": cutoff,
                         "label": [int(c in active) for c in customers.customer_id]})

@section("9. A relational database as input: tables, keys, and a time-aware sampler")
def relational_setup():
    customers, products, orders = make_shop()
    data = sdm.RelationalData(
        tables={
            "customers": sdm.TableTensor.from_pandas(customers, {"customer_id": "id", "region": "categorical",
                                                                 "plan": "categorical"}),
            "products": sdm.TableTensor.from_pandas(products, {"product_id": "id", "category": "categorical",
                                                               "price": "numerical"}),
            "orders": sdm.TableTensor.from_pandas(orders, {"order_id": "id", "customer_id": "id", "product_id": "id",
                                                           "order_date": "datetime", "amount": "numerical"}),
        },
        relationships=[
            dict(left_table="orders", left_column="customer_id", right_table="customers", right_column="customer_id"),
            dict(left_table="orders", left_column="product_id", right_table="products", right_column="product_id"),
        ],
    )
    cutoffs_ctx = [pd.Timestamp(d) for d in ("2025-06-01", "2025-07-01", "2025-08-01")]
    cutoff_q = pd.Timestamp("2025-09-15")
    task_df = pd.concat([task_rows(customers, orders, c) for c in cutoffs_ctx + [cutoff_q]], ignore_index=True)
    task = sdm.TableTensor.from_pandas(task_df, {"customer_id": "id", "timestamp": "datetime", "label": "categorical"})
    n_ctx = len(cutoffs_ctx) * len(customers)
    link = dict(task_link={"task_column": "customer_id", "table": "customers", "table_column": "customer_id"},
                num_neighbors=[16, 16], task_time_column="timestamp")

    print(f"  {len(customers)} customers, {len(products)} products, {len(orders):,} orders over 2025")
    print("  relationships: orders.customer_id -> customers, orders.product_id -> products")
    print(f"  task: will the customer order in the 30 days after a cutoff? positive rate {task_df.label.mean():.2f}")
    print(f"  context: cutoffs {[str(c.date()) for c in cutoffs_ctx]} ({n_ctx:,} rows); query: {cutoff_q.date()}")

    sampler = data.sampler(time_columns={"orders": "order_date"})
    sample, related = sampler(task[:3].drop_columns("label"), **link)
    print("\n  what the sampler hands the model for the first 3 task rows (16 neighbours, then 16 more):")
    for name, tbl in related.tables.items():
        print(f"    {name:10s} {tuple(tbl.size())}")
    latest = related.tables["orders"].to_pandas()["order_date"].max()
    print(f"  latest order the sampler returned: {latest}   task timestamp: {cutoffs_ctx[0]}")
    print("  The sampler walks the foreign keys backwards in time: no order dated after the task row's")
    print("  own timestamp is eligible, so the rows that define the label cannot leak in.")
    globals().update(SHOP=dict(customers=customers, orders=orders, data=data, task=task, task_df=task_df,
                               n_ctx=n_ctx, link=link, cutoffs=cutoffs_ctx + [cutoff_q]))
    return f"{len(orders):,} orders across 3 linked tables"

relational_setup()

KumoRelational takes a relational database instead of a single table. We generate a small shop with eight hundred customers, sixty products and a year of orders, in which some customers&#8217; activity collapses at a random date, and ask whether each customer will order again within thirty days of a cutoff. RelationalData holds the tables and the foreign keys between them, and its sampler walks those keys outwards from each task row, collecting up to sixteen neighbours per hop. Declaring the order date as a time column makes the walk temporal: we check that the latest order the sampler returns for a task row dated the first of June was placed on the thirty-first of May, so the rows that define the label are out of reach.

Copy CodeCopiedUse a different Browser

def relational_auc(time_columns):
    s = SHOP
    sampler = s["data"].sampler(time_columns=time_columns)
    model = sdm.models.KumoRelational(device=DEVICE)
    torch.manual_seed(0)
    context, related = sampler(s["task"][:s["n_ctx"]], **s["link"])
    model.fit(x=context.drop_columns("label"), y=context["label"], related_tables=related,
              generator=torch.Generator().manual_seed(0))
    query = s["task"][s["n_ctx"]:].drop_columns("label")
    proba = model.predict(*sampler(query, **s["link"])).to_pandas()
    return roc_auc_score(s["task_df"].label.to_numpy()[s["n_ctx"]:], proba["1"])

def history_features(customers, orders, cutoff):
    """The feature engineering a data scientist would write by hand, strictly before the cutoff."""
    past = orders[orders.order_date <= cutoff]
    by_customer = past.groupby("customer_id")
    f = pd.DataFrame({"customer_id": customers.customer_id})
    for days in (30, 90):
        recent = past[past.order_date > cutoff - pd.Timedelta(days, unit="D")].groupby("customer_id")
        f[f"orders_{days}d"] = f.customer_id.map(recent.size()).fillna(0)
        f[f"spend_{days}d"] = f.customer_id.map(recent.amount.sum()).fillna(0)
    f["days_since_last"] = f.customer_id.map((cutoff - by_customer.order_date.max()).dt.days).fillna(999)
    f["orders_total"] = f.customer_id.map(by_customer.size()).fillna(0)
    return f.merge(customers, on="customer_id").drop(columns="customer_id")

def flat_auc(frame_fn):
    s = SHOP
    X = pd.concat([frame_fn(c) for c in s["cutoffs"]], ignore_index=True)
    X["label"] = s["task_df"].label.values
    table = as_table(X, "label")
    model = sdm.models.TabICLv2(device=DEVICE)
    torch.manual_seed(0)
    proba = model(x_context=table[:s["n_ctx"]].drop_columns("label"), y_context=table[:s["n_ctx"], "label"],
                  x_query=table[s["n_ctx"]:].drop_columns("label"), num_estimators=4).to_pandas()
    return roc_auc_score(s["task_df"].label.to_numpy()[s["n_ctx"]:], proba["1"]), list(X.columns[:-1])

@section("10. KumoRelational vs. hand-built features: the same question, three ways")
def relational_vs_features():
    s = SHOP
    results = []
    t0 = time.time()
    auc, cols = flat_auc(lambda c: s["customers"].drop(columns="customer_id"))
    results.append(("TabICLv2 on the customers table only", auc, f"{len(cols)} raw columns", time.time() - t0))
    t0 = time.time()
    auc, cols = flat_auc(lambda c: history_features(s["customers"], s["orders"], c))
    results.append(("TabICLv2 on hand-engineered features", auc, f"{len(cols) - 2} engineered + 2 raw", time.time() - t0))
    t0 = time.time()
    results.append(("KumoRelational on the raw tables", relational_auc({"orders": "order_date"}), "3 raw tables", time.time() - t0))
    print(f"  {'approach':40s} {'AUC':>6s}   {'inputs':22s} {'seconds':>7s}")
    for label, auc, inputs, secs in results:
        print(f"  {label:40s} {auc:6.3f}   {inputs:22s} {secs:7.1f}")
    print("\n  Demographics alone barely beat a coin. Purchase history is where the signal is, and the")
    print("  relational model reaches it without anyone writing orders_30d, spend_90d or days_since_last:")
    print("  it reads the order rows themselves through the keys, as of each task row's timestamp.")
    globals()["REL_AUC"] = results[2][1]
    return (f"customers only {results[0][1]:.3f} / hand-built {results[1][1]:.3f}"
            f" / KumoRelational {results[2][1]:.3f} AUC")

relational_vs_features()

We then answer the same question three ways. TabICLv2 on the customers table alone, with only region and plan to go on, reaches an AUC of 0.556. TabICLv2 on six engineered history features, orders and spend in the last thirty and ninety days, days since the last order and lifetime order count, computed strictly before each cutoff, reaches 0.828. KumoRelational on the raw tables, with no features written by anyone, reaches 0.823. The relational model gets within a rounding error of the hand-built pipeline by reading the order rows themselves through the keys, as of each task row&#8217;s timestamp.

Copy CodeCopiedUse a different Browser

@section("11. The one argument that keeps a relational model honest")
def leakage():
    leaky = relational_auc(None)
    print(f"  KumoRelational with time_columns={{'orders': 'order_date'}}   AUC {REL_AUC:.3f}")
    print(f"  KumoRelational with time_columns=None                     AUC {leaky:.3f}")
    print("\n  Without a time column the sampler is free to return orders placed AFTER the cutoff, which")
    print("  are exactly the orders that define the label. The model is not predicting anymore, it is")
    print("  reading the answer. Nothing errors and the number looks like a breakthrough. On a real")
    print("  database, a relational model that is suspiciously better than your hand-built baseline")
    print("  should be the first thing you re-run with every time column declared.")
    return f"{REL_AUC:.3f} honest vs {leaky:.3f} with future rows visible"

leakage()

Finally we run the same relational model without declaring the time column. The AUC rises to 0.940. Without a time column the sampler is free to return orders placed after the cutoff, which are exactly the orders that define the label, so the model is no longer predicting but reading the answer, and nothing errors. On a real database, a relational model that is suspiciously better than the hand-built baseline is the first thing to re-run with every time column declared.

Copy CodeCopiedUse a different Browser

banner("SUMMARY")
for name, res in RESULTS.items():
    print(f"  {name:<76s}  {res}")
print("""
What to carry over
 - Declare stypes deliberately: text and id columns are not detected unless you ask, and the
   default TabICLv2 recipe drops datetime and text columns with a warning that fires once.
 - In an explainer output function, select classes by name, never by position.
 - Every table with a time column goes in time_columns. A relational model that is not time-aware
   is a leakage detector, not a forecaster.
Where to go next
 - Fine-tuning: examples/tabular/finetune.py disables the output recipe and trains on raw logits.
 - Real relational benchmarks: examples/relational/rel_bench.py runs KumoRelational on RelBench.
 - On a T4 runtime, set DEVICE = "cuda" for the tabular models; cudf keeps dataframe work on GPU.
 - Docs: nvidia.github.io/structured-data-models    Code: github.com/NVIDIA/structured-data-models
""")

The summary prints the one-line result each section returned and the three habits worth carrying over: declare semantic types and recipes deliberately, select classes by name inside an explainer and explain with one estimator, and put every table with a time column into time_columns. It then points at fine-tuning, the RelBench example, and GPU execution.

In conclusion, NVIDIA&#8217;s Structured Data Models delivers on its central promise: across classification, regression, a twenty-class problem, and a three-table database, its pretrained models matched or beat scikit-learn baselines trained on the same rows without being trained themselves, returned calibrated predictive distributions for free, and in the relational case reached the accuracy of a hand-built feature pipeline from the raw tables. The defaults deserve more scrutiny than the models. Free text and IDs are not detected unless requested, the default recipe drops timestamp and text columns and warns only once per process, the explainer reports only the last estimator and needs classes selected by name, the pyg-lib URL in the library&#8217;s own error message points to an empty page, and a relational model without its time column produces an impressive and meaningless number. Each of these has a one-line fix, and each would otherwise pass silently, which is the practical lesson to carry into real data: check what reaches the model before trusting what comes out of it.

Check out the Full CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post How to Make Zero-Training Tabular Predictions with NVIDIA Structured Data Models appeared first on MarkTechPost.