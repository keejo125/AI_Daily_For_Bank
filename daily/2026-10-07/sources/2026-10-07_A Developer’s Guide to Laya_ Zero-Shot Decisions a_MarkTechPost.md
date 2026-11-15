---
publish_time: 1791334383
link: https://www.marktechpost.com/2026/10/06/a-developers-guide-to-laya-zero-shot-decisions-and-calibration/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Laya 是 Convai Innovations 开源的决策引擎（421M 参数编码器），以非自回归方式在单次前向传播中完成分类、打分、是非判断等“零样本决策”并输出校准概率，被称为 TypeSafe Jev 的开源替代。本文用银行意图分类数据集 CLINC150 实测：仅以意图描述做零样本路由即达 0.804 准确率，与需每意图 3–10 条标注训练的 TF-IDF 分类器相当；裸意图名（0.878）优于带描述版本，反转选项顺序会改变 4.2% 的个别答案。文章同时揭示默认温度隐患——11 项以上选择题被钳制为 0.5 导致过度自信（ECE 0.102），在自有验证集上仅拟合所测分桶温度后降至 0.059；并给出按选项数分桶设置弃权门限、在标注数据上设定是非题阈值的工程建议，对构建生产级路由 / Agent 决策层有参考价值。
---

# Laya 决策引擎开发指南：零样本决策与概率校准

> 原文链接：https://www.marktechpost.com/2026/10/06/a-developers-guide-to-laya-zero-shot-decisions-and-calibration/
> 来源：MarkTechPost

In this tutorial, we work with Laya, the open-source decision engine from Convai Innovations that became one of the most-starred machine-learning repositories of September 2026. Laya is a non-autoregressive System 1 model: instead of generating text, a 421-million-parameter encoder reads a piece of text and a set of typed questions, a choice between labels, a score on a scale, or a yes/no, and returns a probability for every option in a single forward pass with zero output tokens. Its pitch is speed and calibrated probabilities, the open answer to TypeSafe&#8217;s Jev. Rather than repeat the README&#8217;s examples, we put those promises to work on real labelled data with known answers, the banking domain of the CLINC150 intent dataset, and measure what a production router actually gets: zero-shot accuracy against a trained classifier, how much the wording and order of the options matter, how honest the shipped probabilities are, what fitting a temperature on validation data fixes and what it quietly breaks, an abstention gate fitted to an error budget, out-of-scope traffic, a yes/no question that temperature cannot repair, and typed outputs from a pydantic schema.

Copy CodeCopiedUse a different Browser

import os
import sys
import time
import json
import warnings
import traceback
import subprocess
import urllib.request

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

banner("1. Install Laya and load the English checkpoint at its reviewed revision")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "laya==0.3.27"], check=True)

import numpy as np
import pandas as pd
import torch
import laya
from laya.calibrate import records_from_labeled
from laya.evals import selective_accuracy, aurc
from laya.common import temp_bucket

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# laya.load() follows the Hub's main branch unless told otherwise. The package ships the commit
# its authors reviewed for each checkpoint; pinning it keeps this notebook's weights fixed.
REVISION = laya.PINNED_REVISIONS["convaiinnovations/laya"]
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    agent = laya.load("convaiinnovations/laya", device=DEVICE, revision=REVISION)
# On CUDA Laya autocasts to fp16/bf16. Turning that off keeps every device in fp32, so a GPU run
# reproduces the CPU numbers printed below to within floating-point noise.
agent.amp_enabled = False
SHIPPED = (list(agent.temperature), dict(agent.temperature_by_options))

n_params = sum(p.numel() for p in agent.model.parameters())
print(f"  laya {laya.__version__}  |  torch {torch.__version__}  |  device {DEVICE}, fp32")
print(f"  checkpoint convaiinnovations/laya @ {REVISION[:7]}  |  {n_params / 1e6:.0f}M parameters"
      f"  |  max_len {agent.cfg['max_len']}, head_max_len {agent.cfg['head_max_len']}")
print("\n  Temperatures shipped with the checkpoint (probabilities = softmax(logits / T)):")
for qt, name in enumerate(["choice", "score", "noul"]):
    print(f"    {name:7s} type-level T = {SHIPPED[0][qt]:.3f}")
for bucket, t in sorted(SHIPPED[1].items()):
    print(f"    {bucket:12s} T = {t:.3f}")
for w in caught:
    if "temperature" in str(w.message):
        print("\n  Warning at load time:\n    " + str(w.message).replace("; ", ";\n    "))
print("\n  T > 1 softens probabilities and T < 1 sharpens them. Remember the choice:11+ row: the")
print("  checkpoint ships 0.10 there, which the loader clamps to 0.5, so any choice question with")
print("  11 or more options gets probabilities SHARPENED by 2x. Step 6 measures what that costs.")

We install the released package, laya 0.3.27, and load the English checkpoint. Two choices here keep the run reproducible. By default laya.load follows the Hugging Face main branch, so we pin the revision the library&#8217;s own authors reviewed, which it exposes as laya.PINNED_REVISIONS. And on CUDA Laya autocasts to half precision, so we switch that off to keep every device in fp32 and let a GPU run reproduce the CPU numbers shown here. Printing the checkpoint&#8217;s shipped temperatures turns up the first finding before any prediction: the entry for choice questions with eleven or more options is 0.10, outside the valid range, so the loader clamps it to 0.5 and warns. A temperature below one sharpens probabilities, so every answer to a question with that many options will look twice as certain as the raw model is.

Copy CodeCopiedUse a different Browser

TICKET = "Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."
TRIAGE = {
    "department": {"type": "choice", "instructions": "Which department should handle this?",
                   "criteria": {"billing": "invoices, payments, refunds",
                                "technical": "bugs, outages, system errors",
                                "other": "everything else"}},
    "urgency": {"type": "score", "instructions": "How urgent is this?",
                "criteria": ["not urgent", "soon", "blocking"]},
    "churn_risk": {"type": "noul", "instructions": "Does the user threaten to cancel or leave?"},
}

@section("2. One forward pass, three typed questions, zero output tokens")
def first_decision():
    r = agent.predict(TICKET, TRIAGE)
    a = r["answers"]
    d, u, c = a["department"], a["urgency"], a["churn_risk"]
    print(f"  state: {TICKET!r}\n")
    print(f"  department (choice)  -> {d['choice']!r}   probabilities {d['probabilities']}")
    print(f"  urgency    (score)   -> {u['score']:.2f} on 0..2   level probabilities {u['probabilities']}")
    print(f"  churn_risk (noul)    -> P(yes) = {c['noul']:.3f}")
    print("\n  Two confidence fields, two different quantities:")
    for qid, ans in a.items():
        print(f"    {qid:11s} answer_confidence {ans['answer_confidence']:.3f}   confidence {ans['confidence']:.3f}")
    print("  answer_confidence is the probability of the reported answer, max(p): the number that")
    print("  calibration, the abstention gate and every metric below use. confidence is 1 - normalised")
    print("  entropy, whose scale depends on the number of options. Do not threshold on it.")
    print(f"\n  usage: {r['usage']}")
    print("  output_tokens is always 0: Laya scores the options it is given and never generates text.")
    return f"{d['choice']} / urgency {u['score']:.2f} / P(churn) {c['noul']:.2f} in one pass"

first_decision()

One call to predict answers three typed questions about a support ticket in a single forward pass: the department as a choice, the urgency as a score from 0 to 2, and the churn risk as a yes/no. The result carries a probability for every option and two confidence fields that are easy to confuse. answer_confidence is the probability of the reported answer, and it is the quantity that calibration, the abstention gate and every metric later in this tutorial use. confidence is one minus the normalized entropy, whose scale depends on how many options a question has. The usage block shows zero output tokens, because Laya scores the options it is given and never generates text.

Copy CodeCopiedUse a different Browser

@section("3. What a pass costs: questions are rows, options are nearly free")
def cost_model():
    def median_ms(q, n=7):
        agent.predict(TICKET, q)
        times = []
        for _ in range(n):
            t0 = time.perf_counter()
            r = agent.predict(TICKET, q)
            times.append(1000 * (time.perf_counter() - t0))
        return float(np.median(times)), r["usage"]["input_tokens"]

    print(f"  {'one state, asking ...':34s} {'ms (median of 7)':>16s} {'input_tokens':>13s}")
    rows = {}
    for n in (1, 4, 16):
        q = {f"q{i}": {"type": "noul", "instructions": f"Does the message mention topic number {i}?"} for i in range(n)}
        rows[f"{n} yes/no"] = median_ms(q)
        print(f"  {f'{n:2d} yes/no questions':34s} {rows[f'{n} yes/no'][0]:16.1f} {rows[f'{n} yes/no'][1]:13d}")
    for k in (3, 15, 40):
        q = {"pick": {"type": "choice", "instructions": "Pick one", "criteria": [f"option {i}" for i in range(k)]}}
        rows[f"{k} options"] = median_ms(q)
        print(f"  {f'1 choice question, {k:2d} options':34s} {rows[f'{k} options'][0]:16.1f} {rows[f'{k} options'][1]:13d}")
    print("\n  Every question is encoded as its own (state, question) row, so 16 yes/no questions cost")
    print("  roughly 16 rows. All options of one choice question share a single row and its head")
    print("  budget, so 40 options cost far less than 40 yes/no questions. Design rule: ask one")
    print("  choice question with many options, not many yes/no questions.")
    return (f"16 yes/no {rows['16 yes/no'][0]:.0f} ms vs one 40-option choice "
            f"{rows['40 options'][0]:.0f} ms")

cost_model()

Before building on Laya, we measure the cost of a forward pass on a single message. Each question becomes its own row, paired with the message, so sixteen yes/no questions take about eight times as long as one. All the options of a choice question share one row and its head budget, so a forty-option choice costs barely twice a three-option one and a quarter of what sixteen yes/no questions do on our CPU. That gives a design rule that shapes everything after it: ask one choice question with many options rather than many yes/no questions.

Copy CodeCopiedUse a different Browser

CARD = json.load(urllib.request.urlopen("https://huggingface.co/api/datasets/clinc/clinc_oos"))["cardData"]
PLUS = next(c for c in CARD["dataset_info"] if c["config_name"] == "plus")
NAMES = {int(k): v for k, v in PLUS["features"][1]["dtype"]["class_label"]["names"].items()}

def clinc(split):
    df = pd.read_parquet(f"https://huggingface.co/api/datasets/clinc/clinc_oos/parquet/plus/{split}/0.parquet")
    return df.assign(label=df.intent.map(NAMES))

# The banking domain of CLINC150 (15 intents), with the one-line descriptions a developer would write.
DESCRIBED = {
    "balance": "checking how much money is in an account",
    "transactions": "looking up recent transactions on an account",
    "transfer": "moving money between accounts or to another person",
    "freeze_account": "freezing or locking an account",
    "account_blocked": "an account that is blocked or locked and cannot be used",
    "pay_bill": "paying a bill",
    "bill_balance": "how much is owed on a bill",
    "bill_due": "when a bill is due",
    "interest_rate": "the interest rate on an account",
    "min_payment": "the minimum payment that is due",
    "order_checks": "ordering new checks or a checkbook",
    "pin_change": "changing a PIN",
    "report_fraud": "reporting fraud or suspicious activity",
    "routing": "the bank routing number",
    "spending_history": "how much was spent over a period or on a category",
}
INTENTS = list(DESCRIBED)
ASK = "Which banking request is this?"

def route(states, criteria, **kw):
    """One choice question over `criteria` for every state; returns choices, confidences, results."""
    res = agent.predict_batch(list(states), {"intent": {"type": "choice", "instructions": ASK, "criteria": criteria}},
                              batch_size=32, **kw)
    return (np.array([r["answers"]["intent"]["choice"] for r in res]),
            np.array([r["answers"]["intent"]["answer_confidence"] for r in res]), res)

@section("4. Real labelled data: CLINC150 banking, zero-shot vs. a trained classifier")
def zero_shot_vs_trained():
    global train, val, test, BTRAIN, BVAL, BTEST
    train, val, test = clinc("train"), clinc("validation"), clinc("test")
    BTRAIN, BVAL, BTEST = (d[d.label.isin(INTENTS)].reset_index(drop=True) for d in (train, val, test))
    print(f"  CLINC150 'plus': {len(train):,} / {len(val):,} / {len(test):,} train / validation / test queries,"
          f" 150 intents + out-of-scope")
    print(f"  banking domain: {len(INTENTS)} intents; {len(BTRAIN)} train, {len(BVAL)} validation, {len(BTEST)} test queries")
    print(f"  e.g. {BTEST.text[0]!r} -> {BTEST.label[0]}")

    t0 = time.time()
    pred, conf, _ = route(BTEST.text, DESCRIBED)
    secs = time.time() - t0
    acc = float((pred == BTEST.label).mean())
    globals()["DESCRIBED_ACC"], globals()["DESCRIBED_PRED"] = acc, pred
    print(f"\n  Laya, zero-shot, 15 options with descriptions: accuracy {acc:.3f}"
          f"   ({secs:.0f}s for {len(BTEST)} queries on {DEVICE})")

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    print("\n  TF-IDF + logistic regression trained on k labelled queries per intent (5 draws for k < 100):")
    curve = {}
    for k in (1, 3, 10, 30, 100):
        accs = []
        for seed in range(5 if k < 100 else 1):
            sub = BTRAIN.groupby("label", group_keys=False).sample(k, random_state=seed)
            vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
            clf = LogisticRegression(max_iter=3000, C=10).fit(vec.fit_transform(sub.text), sub.label)
            accs.append(float((clf.predict(vec.transform(BTEST.text)) == BTEST.label).mean()))
        curve[k] = float(np.mean(accs))
        print(f"    k = {k:3d}  ({k * len(INTENTS):5,d} labels)   accuracy {curve[k]:.3f}  (sd {np.std(accs):.3f})")
    globals()["CURVE"] = curve
    print("\n  Zero-shot Laya, with nothing but the intent descriptions, lands between what a classic")
    print("  classifier reaches with three and with ten labelled examples per intent. Step 5 shows the")
    print("  descriptions are the weak part.")
    return f"zero-shot {acc:.3f}; TF-IDF needs 10/intent for {curve[10]:.3f}"

zero_shot_vs_trained()

For real labeled data, we use CLINC150, a public intent-classification benchmark of 150 intents across ten domains plus a set of out-of-scope queries, read straight from the Hugging Face Hub as a parquet file. We take its banking domain, fifteen intents with 100 training, 20 validation, and 30 test queries each, and ask Laya to route the 450 test queries zero-shot, giving it each intent&#8217;s name and a one-line description of the kind a developer would write. It reaches 0.804 accuracy with no labeled examples. For scale, a TF-IDF and logistic-regression classifier reaches 0.651 with three labeled queries per intent, 0.848 with ten, and 0.904 with thirty.

Copy CodeCopiedUse a different Browser

@section("5. Criteria wording and option order change the answers")
def wording_and_order():
    t0 = time.time()
    pred_n, conf_n, res_n = route(BTEST.text, INTENTS)
    secs = time.time() - t0
    acc_n = float((pred_n == BTEST.label).mean())
    pred_r, _, _ = route(BTEST.text, INTENTS[::-1])
    acc_r = float((pred_r == BTEST.label).mean())
    flips = float((pred_r != pred_n).mean())
    print(f"  {'criteria':44s} {'accuracy':>8s}")
    print(f"  {'15 names with one-line descriptions (step 4)':44s} {DESCRIBED_ACC:8.3f}")
    tok = {name: agent.predict(BTEST.text[0], {"intent": {"type": "choice", "instructions": ASK, "criteria": c}})
           ["usage"]["input_tokens"] for name, c in (("described", DESCRIBED), ("names", INTENTS))}
    print(f"  {'15 bare intent names':44s} {acc_n:8.3f}   ({secs:.0f}s; {tok['names']} input tokens per query"
          f" vs {tok['described']})")
    print(f"  {'15 bare intent names, order reversed':44s} {acc_r:8.3f}")
    print(f"\n  Reversing the option order changes {flips:.1%} of individual answers, even where the")
    print("  overall accuracy barely moves: the model has a position prior, so fix the order you deploy.")
    changed = pd.DataFrame({"label": BTEST.label, "described": DESCRIBED_PRED, "names": pred_n})
    gained = changed[(changed.names == changed.label) & (changed.described != changed.label)]
    lost = changed[(changed.names != changed.label) & (changed.described == changed.label)]
    print(f"\n  Bare names fixed {len(gained)} answers the descriptions got wrong and broke {len(lost)};"
          f" the most common fixes:")
    for (lab, was), n in gained.groupby(["label", "described"]).size().sort_values(ascending=False).head(3).items():
        print(f"    {lab:16s} had been routed to {was:16s} x{n}")
    print("\n  More text is not more signal. The descriptions we wrote blurred intents the names keep")
    print("  apart, and only labelled data could tell us. From here on we route on the bare names.")
    globals().update(PRED=pred_n, CONF=conf_n)
    return f"descriptions {DESCRIBED_ACC:.3f} -> names {acc_n:.3f}; reversed order flips {flips:.1%}"

wording_and_order()

Next we change only the wording of the options. Giving Laya the fifteen bare intent names, without our descriptions, lifts accuracy from 0.804 to 0.878 and halves the time, because the options take less than half the tokens. The descriptions blurred intents the names keep apart: account_blocked was routed to freeze_account ten times, and interest rate questions to balance. Reversing the order of the bare names changes 4.2 percent of individual answers even though overall accuracy barely moves, a sign of a position prior, so the option order you deploy should be the order you tested. Only labeled data could tell us either thing; from here on we route on the bare names.

Copy CodeCopiedUse a different Browser

def reliability(conf, correct, title):
    bins = np.linspace(0, 1, 11)
    idx = np.clip(np.digitize(conf, bins) - 1, 0, 9)
    print(f"  {title}\n    {'confidence':>12s} {'answers':>8s} {'mean conf':>10s} {'accuracy':>9s}")
    for i in range(10):
        m = idx == i
        if m.sum():
            print(f"    {bins[i]:5.1f}-{bins[i + 1]:.1f}   {m.sum():8d} {conf[m].mean():10.3f} {correct[m].mean():9.3f}")

@section("6. How honest are the probabilities as shipped?")
def shipped_calibration():
    ok = PRED == BTEST.label.values
    ece = laya.ece_score(CONF, ok)
    bucket = temp_bucket(laya.QTYPES["choice"], len(INTENTS))
    print(f"  15-option question -> temperature bucket {bucket!r}, T = {agent.temperature_by_options.get(bucket):.2f}\n")
    reliability(CONF, ok, "Reliability on the 450 test queries:")
    print(f"\n  accuracy {ok.mean():.3f}, mean answer_confidence {CONF.mean():.3f}, ECE {ece:.3f} (15 bins)")
    top = CONF >= 0.9
    print(f"  {top.mean():.0%} of answers claim >= 0.9 confidence; {ok[top].mean():.1%} of those are right.")
    print("\n  The model is over-confident here, and the clamp is part of why: with T = 0.5 every")
    print("  15-option answer is sharpened before you see it. 'Calibrated' in a model card describes a")
    print("  training objective, not a property of your question. Measure it on your own labels.")
    globals()["ECE_SHIPPED"] = ece
    return f"ECE {ece:.3f} as shipped; accuracy {ok.mean():.3f} at mean confidence {CONF.mean():.3f}"

shipped_calibration()

We then ask how honest the probabilities are. A fifteen-option question falls into the checkpoint&#8217;s choice:11+ temperature bucket, the one clamped to 0.5. The reliability table on the 450 test queries shows the result: 92 percent of answers claim a confidence of at least 0.9, but 91.1 percent of those are right, and the mean confidence of 0.974 sits well above the accuracy of 0.878, an expected calibration error of 0.102. Laya&#8217;s training objective uses proper scoring rules, which is what the model card means by calibrated. Still, calibration is a property of a question on a distribution, and you have to measure it on your own labels.

Copy CodeCopiedUse a different Browser

@section("7. Fit a temperature on validation data, without breaking the other questions")
def fit_temperature():
    eye = np.eye(len(INTENTS))
    pairs = [(s, {"intent": {"type": "choice", "instructions": ASK, "criteria": INTENTS}},
              {"intent": eye[INTENTS.index(l)]}) for s, l in zip(BVAL.text, BVAL.label)]
    t0 = time.time()
    records = records_from_labeled(agent, pairs)
    print(f"  {len(records)} labelled validation records (raw logits + one-hot targets) in {time.time() - t0:.0f}s")

    fit = agent.fit_temperatures(records)
    after = (list(agent.temperature), dict(agent.temperature_by_options))
    print(f"  fitted on bucket counts {fit['n_by_bucket']}; choice temperature {fit['temperature'][0]:.3f}")
    print("\n  What agent.fit_temperatures() just installed, next to what shipped:")
    print(f"    {'':14s} {'shipped':>8s} {'after':>8s}")
    for qt, name in enumerate(["choice", "score", "noul"]):
        print(f"    {name + ' (type)':14s} {SHIPPED[0][qt]:8.3f} {after[0][qt]:8.3f}")
    for bucket in sorted(SHIPPED[1]):
        now = after[1].get(bucket)
        print(f"    {bucket:14s} {SHIPPED[1][bucket]:8.3f} {('%.3f' % now) if now is not None else '  (gone)':>8s}")
    print("\n  One fit on choice questions replaced the whole map: every per-bucket entry is gone (a bucket")
    print("  needs 2,000 records to keep its own temperature) and the score and noul temperatures were reset")
    print("  to 1.0 because there were no records of those types. Every yes/no question now uses a")
    print("  different temperature than it did a minute ago. Install only what you measured instead:")
    agent.temperature, agent.temperature_by_options = list(SHIPPED[0]), dict(SHIPPED[1])
    agent.temperature_by_options["choice:11+"] = fit["temperature"][0]
    print(f"    agent.temperature_by_options['choice:11+'] = {fit['temperature'][0]:.3f}   (all else as shipped)")

    pred, conf, _ = route(BTEST.text, INTENTS)
    ok = pred == BTEST.label.values
    ece = laya.ece_score(conf, ok)
    print()
    reliability(conf, ok, "Reliability on the same 450 test queries, after the fit:")
    print(f"\n  ECE {ECE_SHIPPED:.3f} -> {ece:.3f}; accuracy unchanged at {ok.mean():.3f} (temperature never changes the argmax)")
    agent.save_calibration("laya_banking_calibration.json")
    saved = json.load(open("laya_banking_calibration.json"))
    print(f"  saved with agent.save_calibration(): keys {sorted(saved)}; reload with laya.load(..., calibration=path)")
    globals().update(RECORDS=records, CONF_FIT=conf, OK_FIT=ok)
    return f"ECE {ECE_SHIPPED:.3f} -> {ece:.3f} from {len(records)} validation queries"

fit_temperature()

Laya&#8217;s calibration module turns labeled examples into records of raw logits and targets, and fits a temperature to them. We build 300 records from the validation split and call agent.fit_temperatures, which fits a choice temperature of 1.258 and installs it, then prints the full temperature table next to what shipped. The fit replaced the entire map: every per-option-count entry is gone, because a bucket needs 2,000 records to keep its own temperature, and the score and yes/no temperatures were reset to 1.0 because there were no records of those types. One fit on a choice question silently changed how every yes/no question in the agent is calibrated. So we restore the shipped values and install only the bucket we measured. On the test set, calibration error falls from 0.102 to 0.059 with accuracy unchanged, since temperature never changes which option wins, and save_calibration writes the result to a JSON file that laya.load can read back.

Copy CodeCopiedUse a different Browser

@section("8. An abstention gate fitted to an error budget")
def abstention_gate():
    t = agent.temperature_by_options["choice:11+"]
    z = np.array([r[1] for r in RECORDS]) / t
    p_val = np.exp(z - z.max(1, keepdims=True)); p_val /= p_val.sum(1, keepdims=True)
    conf_val = p_val.max(1)
    ok_val = np.array([np.argmax(r[1]) == np.argmax(r[2]) for r in RECORDS])
    print(f"  {'target':>6s} {'threshold':>10s}   {'validation: kept / error':>25s}   {'test: kept / error':>19s}")
    gates = {}
    for target in (0.02, 0.05, 0.10):
        thr = laya.fit_abstention_thresholds(RECORDS, agent.temperature, agent.temperature_by_options,
                                             target_error=target)
        cut = thr["choice:11+"]
        kv, kt = conf_val >= cut, CONF_FIT >= cut
        gates[target] = thr
        print(f"  {target:6.0%} {cut:10.3f}   {kv.mean():14.1%} / {1 - ok_val[kv].mean():5.1%}"
              f"   {kt.mean():11.1%} / {1 - OK_FIT[kt].mean():5.1%}")
    _, _, res = route(BTEST.text, INTENTS, min_confidence=gates[0.05])
    states = pd.Series([r["answers"]["intent"]["abstention"] for r in res]).value_counts().to_dict()
    print(f"\n  The 5% gate applied by Laya itself, predict_batch(min_confidence=...): {states}")
    conf, ok = CONF_FIT.tolist(), OK_FIT.tolist()
    print(f"  selective accuracy on test: top 50% by confidence {selective_accuracy(conf, ok, 0.5):.3f},"
          f" top 80% {selective_accuracy(conf, ok, 0.8):.3f}, all {np.mean(ok):.3f};  AURC {aurc(conf, ok):.3f}")
    print(f"\n  On validation every cut meets its target, by construction. On test the realised error is")
    print(f"  higher, because the test queries are harder: accuracy is {ok_val.mean():.3f} on validation and"
          f" {OK_FIT.mean():.3f}")
    print("  on test. A gate fitted to an error budget holds only for traffic that looks like the data it")
    print("  was fitted on. Fit it on a sample of real traffic, re-check it as traffic drifts, and leave")
    print("  margin. Thresholds are per option-count bucket because one number does not transfer between")
    print("  a 2-way and a 15-way question.")
    globals()["GATE"] = gates[0.05]
    kept = CONF_FIT >= gates[0.05]["choice:11+"]
    return f"5% target: {1 - OK_FIT[kept].mean():.1%} error on test at {kept.mean():.1%} coverage"

abstention_gate()

laya.fit_abstention_thresholds takes the same validation records and, for each option-count bucket, returns the loosest confidence cut that keeps the validation error within a target. For a 5 percent target, it picks 0.602, which keeps 95.7 percent of the validation queries at 4.5 percent error, and Laya applies the same cut itself when it is passed to predict_batch as min_confidence, marking 35 of the 450 test answers as abstained. On the test set, though, that gate keeps 92.2 percent of the queries at 9.2 percent error, nearly twice the budget, and the 2 percent target realizes 5.3 percent. The data explains it: Laya is right on 92.7 percent of the validation queries but only 87.8 percent of the test queries, so an error budget fitted on one sample holds only for traffic that looks like it. The ranking itself is sound, with the most confident half of the test answers 97.8 percent correct, but an error target needs margin and periodic re-fitting on real traffic. The thresholds stay per option-count bucket because one number doesn&#8217;t transfer between a two-way and a fifteen-way question.

Copy CodeCopiedUse a different Browser

@section("9. Out-of-scope traffic: the gate vs. an explicit 'other' option")
def out_of_scope():
    global OOS, OTHER
    OOS = test[test.label == "oos"].sample(150, random_state=0).reset_index(drop=True)
    OTHER = test[~test.label.isin(INTENTS + ["oos"])].sample(150, random_state=0).reset_index(drop=True)
    print(f"  {len(OOS)} out-of-scope queries (e.g. {OOS.text[0]!r})")
    print(f"  {len(OTHER)} in-scope queries from other CLINC domains (e.g. {OTHER.text[0]!r})\n")

    groups = {"banking": BTEST.text, "other domains": OTHER.text, "out of scope": OOS.text}
    conf = {g: route(s, INTENTS)[1] for g, s in groups.items()}
    thr = GATE["choice:11+"]
    print(f"  A) 15 intents + the 5% gate (threshold {thr:.3f}): share of each group the gate stops")
    for g in groups:
        print(f"     {g:14s} mean confidence {conf[g].mean():.3f}   abstained {(conf[g] < thr).mean():6.1%}")

    with_other = INTENTS + ["not a banking request"]
    print(f"\n  B) 16 options: the 15 intents + 'not a banking request', no gate")
    picks = {g: route(s, with_other)[0] for g, s in groups.items()}
    for g in groups:
        print(f"     {g:14s} routed to 'not a banking request' {(picks[g] == 'not a banking request').mean():6.1%}")
    acc_b = float((picks["banking"] == BTEST.label.values).mean())
    print(f"     banking accuracy with the extra option {acc_b:.3f} (15 intents alone: {OK_FIT.mean():.3f})")
    print("\n  Neither tool is free. The gate needs labelled data and gives up some in-scope coverage;")
    print("  the extra option needs no data but changes the question every intent is scored against.")
    stop = (conf["out of scope"] < thr).mean()
    return f"gate stops {stop:.1%} of out-of-scope queries; 'other' option catches {(picks['out of scope'] == 'not a banking request').mean():.1%}"

out_of_scope()

Production traffic includes requests the router was never built for, so we add 150 out-of-scope CLINC queries and 150 queries from other CLINC domains. The calibrated confidence separates them sharply: banking queries average 0.912, the others about 0.25, and the 5 percent gate stops 89.3 percent of other-domain queries and 93.3 percent of out-of-scope ones while abstaining on 7.8 percent of banking queries. The alternative needs no labeled data: a sixteenth option, not a banking request, catches 80.0 and 90.0 percent of them, at the cost of routing 2.0 percent of banking queries away and lowering banking accuracy from 0.878 to 0.864, because the new option changes what every intent is scored against.

Copy CodeCopiedUse a different Browser

IN_SCOPE = {"in_scope": {"type": "noul", "instructions": "Is this a request about the user's bank account, bills, or payments?"}}

@section("10. A biased yes/no question, and why temperature cannot fix it")
def biased_noul():
    states = pd.concat([BTEST.text, OTHER.text, OOS.text], ignore_index=True)
    y = np.r_[np.ones(len(BTEST)), np.zeros(len(OTHER) + len(OOS))].astype(bool)
    res = agent.predict_batch(list(states), IN_SCOPE, batch_size=32)
    p = np.array([r["answers"]["in_scope"]["noul"] for r in res])
    from sklearn.metrics import roc_auc_score
    auc = roc_auc_score(y, p)
    print(f"  'Is this a request about the user's bank account, bills or payments?' on 450 banking")
    print(f"  queries and 300 that are not:")
    print(f"    mean P(yes): banking {p[y].mean():.3f}, not banking {p[~y].mean():.3f}   AUROC {auc:.3f}")
    print(f"    at the 0.5 cut: recall {(p[y] >= 0.5).mean():.1%}, specificity {(p[~y] < 0.5).mean():.1%}")

    vstates = pd.concat([BVAL.text, val[~val.label.isin(INTENTS + ["oos"])].sample(150, random_state=0).text,
                         val[val.label == "oos"].text], ignore_index=True)
    vy = np.r_[np.ones(len(BVAL)), np.zeros(len(vstates) - len(BVAL))]
    recs = records_from_labeled(agent, [(s, IN_SCOPE, {"in_scope": np.array([1 - t, t])}) for s, t in zip(vstates, vy)])
    t_fit = laya.fit_temperature_map(recs)["temperature"][2]
    print(f"\n  Temperature fitted on {len(recs)} validation answers: T = {t_fit:.2f} (the ceiling is 5.0)")
    print("  Any T leaves the 0.5 cut where it is: dividing two logits by T never changes which is larger.")
    t_ship = agent.temperature_by_options.get("noul:2", agent.temperature[2])
    logits = np.array([r[1] for r in recs])
    p_val = 1 / (1 + np.exp(-(logits[:, 1] - logits[:, 0]) / t_ship))
    cuts = np.linspace(0.01, 0.99, 99)
    bal = [((p_val[vy == 1] >= c).mean() + (p_val[vy == 0] < c).mean()) / 2 for c in cuts]
    cut = float(cuts[int(np.argmax(bal))])
    print(f"\n  What does work is moving the cut. Chosen on validation (best balanced accuracy): {cut:.2f}")
    print(f"    on test at {cut:.2f}: recall {(p[y] >= cut).mean():.1%}, specificity {(p[~y] < cut).mean():.1%}")
    print("\n  The question ranks well and is biased towards 'no'. Temperature scaling repairs a scale,")
    print("  not an offset. Treat P(yes) as a score, and pick its cut on labeled data like any other.")
    globals()["IN_SCOPE_CUT"] = cut
    return f"recall at 0.5 {(p[y] >= 0.5).mean():.1%} -> {(p[y] >= cut).mean():.1%} at a validated cut of {cut:.2f}"

biased_noul()

A dedicated yes/no question looks like the natural in-scope check, so we ask whether each message is about the user&#8217;s bank account, bills, or payments. It ranks well, with an AUROC of 0.945, but it is biased towards no: banking queries average a probability of only 0.361, so at the default 0.5 cut it recognizes just 28.9 percent of them. Fitting a temperature on 550 validation answers runs to the ceiling of 5.0 and changes nothing at that cut, because dividing two logits by any temperature never changes which is larger. Temperature scaling repairs a scale, not an offset. What works is treating the probability as a score and choosing its cut on labeled data: a cut of 0.09 picked on the validation split gives 92.0 percent recall and 83.0 percent specificity on the test set.

Copy CodeCopiedUse a different Browser

from typing import Literal, Optional
from pydantic import BaseModel, Field

class BankingRequest(BaseModel):
    intent: Optional[Literal[tuple(INTENTS)]] = Field(description=ASK)
    in_scope: bool = Field(description=IN_SCOPE["in_scope"]["instructions"])

@section("11. Typed decisions from a pydantic schema")
def schema_decisions():
    planned = laya.structured.questions_from_pydantic(BankingRequest)
    crit = planned["intent"]["criteria"]
    print(f"  questions_from_pydantic(BankingRequest): 'intent' -> {planned['intent']['type']} with "
          f"{len(crit)} options, criteria values {set(crit.values())};  'in_scope' -> {planned['in_scope']['type']}")
    print("  A Literal becomes a choice over bare names (what step 5 found works best here); a bool becomes")
    print("  a yes/no question that the projection cuts at 0.5.\n")
    demo = pd.concat([BTEST.iloc[[0, 120, 300]], OOS.iloc[[0, 1]]], ignore_index=True)
    out = laya.decide_batch(agent, list(demo.text), schema=BankingRequest, return_details=True,
                            min_confidence=GATE, batch_size=8)
    for (text, label), d in zip(zip(demo.text, demo.label), out):
        typed = BankingRequest(**d.values)
        p_yes = d.probabilities["in_scope"]["true"]
        print(f"  {text[:46]!r:50s} truth {label}")
        print(f"      -> {typed!r}   P(in_scope) {p_yes:.2f}, at our cut {p_yes >= IN_SCOPE_CUT}")
    print("\n  min_confidence=GATE turns a gated answer into None, so 'intent=None' means 'ask a human',")
    print("  and the pydantic model still validates. in_scope is decided at a fixed 0.5 inside decide();")
    print("  read d.probabilities['in_scope']['true'] and apply the cut from step 10 instead.")
    nones = sum(BankingRequest(**d.values).intent is None for d in out)
    return f"{len(out)} typed objects, {nones} intents gated to None"

schema_decisions()

Finally, we wire this into application code through a pydantic schema. laya.decide_batch turns a Literal field into a choice question over the bare names, which step 5 showed is the better wording here, and a bool into a yes/no question, then projects the answers back into a validated model instance. Passing the gate from step 8 as min_confidence turns an uncertain intent into None, which the Optional field accepts, so None becomes an explicit ask-a-human signal; the two out-of-scope queries come back as intent=None. The boolean, however, is cut at a fixed 0.5 inside decide, so a fraud report is marked in_scope=False at a probability of 0.29. Reading the probability from the result details and applying the cut from step 10 gives the right answer.

Copy CodeCopiedUse a different Browser

banner("SUMMARY")
for name, res in RESULTS.items():
    print(f"  {name:<76s}  {res}")
print("""
What to carry over
 - Pin the checkpoint (laya.PINNED_REVISIONS) and know its shipped temperatures before trusting a
   probability: 15-option questions were sharpened by a clamped 0.5.
 - Measure criteria wording and option order on labeled data. Bare names beat our descriptions.
 - Fit temperatures on held-out data, and install only the bucket you measured: fit_temperatures()
   replaces the whole map, including question types you did not fit.
 - Gate per option-count bucket with fit_abstention_thresholds, and leave margin below the target.
 - A yes/no question can rank well and still be biased; choose its cut on labeled data.
Where to go next
 - Fine-tuning: laya.train on the repository's main branch (not yet in the 0.3.27 wheel) and the
   repo's Kaggle / Apple-silicon notebooks train with RLCD and refit temperatures.
 - Other languages: laya.Router() detects the script and routes to laya-multilingual, which ships with
   no fitted temperatures at all.
 - Serving: pip install "laya[serve]" for an HTTP server; laya[mcp] for an MCP tool server.
 - Docs: nandhakishorm.github.io/laya    Code: github.com/NandhaKishorM/laya
""")

The summary prints the one-line result of each step and the habits worth carrying over: pin the checkpoint and read its shipped temperatures, test criteria wording and option order on labeled data, fit temperatures on held-out data and install only the bucket you measured, gate per option-count bucket with margin, and choose a yes/no cut on labeled data. It closes with where to go next: fine-tuning, which lives in laya.train on the repository&#8217;s main branch but is not yet in the 0.3.27 wheel, the multilingual checkpoint behind laya.Router, and serving.

In conclusion, Laya delivers most of what it promises: one forward pass answers several typed questions with no generated tokens, the bare-name router reached 0.878 on fifteen real banking intents with no training data, which a TF-IDF classifier needs between ten and thirty labeled examples per intent to match, and its calibrated confidence separated in-scope from out-of-scope traffic well enough to stop more than nine in ten out-of-scope queries. What the probabilities are worth, though, depends on work the library leaves to you, and several of its defaults point the wrong way. The shipped temperature for questions with eleven or more options sharpens rather than softens, the one-line calibration call wipes temperatures for question types it never saw, an error budget fitted on validation data held only for traffic that looked like it, and a yes/no question can rank well yet sit on the wrong side of 0.5, which no temperature can fix and which the schema projection then hard-codes. Each of these has a few-line fix shown above, and each would otherwise pass silently. The practical lesson is the same one this library&#8217;s own model card states and its defaults make easy to forget: a calibrated decision model is one you have calibrated, on your own labels, for your own questions.

Check out the FULL CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

[Sponsored] The web is the one API most agents are missing. Databases, calendars and repos have APIs. The open web mostly doesn’t. The TinyFish MCP server gives any MCP client four tools: TinySearch, TinyFetch (full pages as markdown, JavaScript included), TinyBrowser for logins and forms, and TinyAgent for multi-step jobs. Search and Fetch are free.

The post A Developer&#8217;s Guide to Laya: Zero-Shot Decisions and Calibration appeared first on MarkTechPost.