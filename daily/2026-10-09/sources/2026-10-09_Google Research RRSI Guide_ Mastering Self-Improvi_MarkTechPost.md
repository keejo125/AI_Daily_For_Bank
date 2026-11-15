---
publish_time: 1791522377
link: https://www.marktechpost.com/2026/10/08/google-research-rrsi-guide-mastering-self-improving-ai-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google Research 发布 RRSI（Regularized Recursive Self-Improvement）教程，给出一种让 LLM 智能体在不针对任务过拟合的前提下改写自身 harness、提示、工具、记忆与控制流的方法。完整循环用 Claude Opus（Vertex AI）起草改动并在 Docker 基准中打分，核心在于决定哪些改动可被采纳的规则。
---

# Google Research RRSI 指南：掌握自我改进的 AI 智能体

> 原文链接：https://www.marktechpost.com/2026/10/08/google-research-rrsi-guide-mastering-self-improving-ai-agents/
> 来源：MarkTechPost

In this tutorial, we implement RRSI (Regularized Recursive Self-Improvement), a method that lets an LLM agent rewrite its own harness, prompts, tools, memory, control flow, and sub-agents around a frozen model, without the harness overfitting to the tasks it evolves on. The full RRSI loop drafts edits with Claude Opus on Vertex AI and scores them inside Docker benchmarks, which is not something a free notebook can run. The part of RRSI that actually carries the paper&#8217;s idea, the rules that decide which proposed edits to keep, is plain Python, and that is what we drive directly. We install the package from the official repository, walk through its estimator, its calibrated noise band, both branches of its selection algorithm, its annealed edit budget, its deterministic leakage screen, and its edit history, and then plug a simulated agent into RRSI&#8217;s own Domain interface. Because we built the simulated environment ourselves, we know the true effect of every edit, which lets us audit RRSI&#8217;s decisions against ground truth and compare them with an unregularized search that simply keeps whatever scores highest.

Copy CodeCopiedUse a different Browser

import os
import sys
import json
import math
import copy
import random
import tempfile
import textwrap
import traceback
import subprocess
import statistics as st
from pathlib import Path

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

banner("1. Install RRSI and map the paper onto the code")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "git+https://github.com/google-research/rrsi.git@be50316e1db05914068a973f322770ef08ed7ba1"], check=True)

from importlib.metadata import version
from rrsi.config import RRSIConfig
from rrsi.evaluate import TaskResult, EvalResult, aggregate, evaluate
from rrsi.calibrate import calibrate
from rrsi.selection import Candidate, cost_rule, judge, select_round
from rrsi.schedule import edit_budget, budget_table
from rrsi.history import History, stall_flag, exploration
from rrsi.components import K, K_STR, normalize, novelty
from rrsi.critic import precheck, review
from rrsi.domain import Domain

print(f"  rrsi {version('rrsi')}  |  anthropic {version('anthropic')}  |  Python {sys.version.split()[0]}")
print("\n  RRSI evolves an agent's HARNESS (prompts, tools, memory, control flow, sub-agents) around a")
print("  frozen model. The full loop drafts edits with Claude Opus on Vertex AI and scores them in Docker")
print("  benchmarks. The part that decides which edits to KEEP is plain Python, and that is what we drive:")
for symbol, where in [
    ("S_hat, C_hat       Eq. (estimate)", "rrsi.evaluate.aggregate"),
    ("delta              noise band", "rrsi.calibrate.calibrate"),
    ("Algorithm 2        floor + cost rule", "rrsi.selection.judge / select_round"),
    ("b_t                Eq. (anneal)", "rrsi.schedule.edit_budget"),
    ("Critic             leakage screen", "rrsi.critic.precheck / review"),
    ("L_t, g_t, B_t      history, yield, prune", "rrsi.history.History"),
    ("sigma_t, U_t       stall + exploration", "rrsi.history.stall_flag / exploration"),
    ("nu                 structural novelty", "rrsi.components.novelty"),
]:
    print(f"    {symbol:40s} -> {where}")

CFG = RRSIConfig()
print(f"\n  paper defaults: T={CFG.T} rounds, k={CFG.k} trials/task, m={CFG.m} candidates/round,"
      f" b in [{CFG.b_min},{CFG.b_max}]")
print(f"                  beta0={CFG.beta0}  beta1={CFG.beta1}  w_s={CFG.w_s}  w_c={CFG.w_c}  w_n={CFG.w_n}"
      f"  delta_z={CFG.delta_z}")
print("\n  Nothing below needs an API key, a GPU or a dataset download.")

We install RRSI from the google-research repository, pinned to the commit this notebook was written against, since the package is not on PyPI. Its only dependency is the Anthropic client, which the search roles use to call Claude and which we never exercise. We then print the mapping the repository itself documents between the paper&#8217;s symbols and the functions that implement them: the empirical score and cost estimate in evaluate, the noise band in calibrate, Algorithm 2 in selection, the annealed edit budget in schedule, the leakage screen in critic, and the edit history with its yield, prune, stall and exploration summaries in history. RRSIConfig holds the paper&#8217;s hyperparameters, and every function below receives it exactly as the real loop does.

Copy CodeCopiedUse a different Browser

@section("2. Evaluate(H): a score and a cost, and why a crash counts as zero")
def estimator():
    base = {
        "task_000": TaskResult(rewards=[1, 1], tokens=[11_800, 12_400]),
        "task_001": TaskResult(rewards=[1, 0], tokens=[15_100, 14_600]),
        "task_002": TaskResult(rewards=[0, 0], tokens=[21_000, 19_500]),
    }
    ev = aggregate("H0", 2, base)
    print(f"  three tasks x k=2 trials -> S_hat = {ev.S:.3f}   C_hat = {ev.C:,.0f} tokens/trial"
          f"   ({ev.n_expected} trials expected, {ev.missing} missing)")

    crashy = dict(base)
    crashy["task_002"] = TaskResult(rewards=[0.0, 0.0], tokens=[None, None], missing=2)
    ev_crash = aggregate("crashy", 2, crashy)
    dropped = {t: r for t, r in crashy.items() if not r.missing}
    naive = sum(sum(r.rewards) for r in dropped.values()) / sum(len(r.rewards) for r in dropped.values())
    print("\n  A candidate crashes on the hardest task instead of failing it:")
    print(f"    an estimator that drops missing trials reports  {naive:.3f}   <- looks like a gain")
    print(f"    RRSI's aggregate (missing = 0, full denominator) {ev_crash.S:.3f}   <- no reward for crashing")
    print(f"    ...and C_hat uses only recorded token counts: {ev_crash.C:,.0f}")

    rubric = {"memo": TaskResult(rewards=[0.5, 1.0], weights=[10, 10]),
              "brief": TaskResult(rewards=[0.0, 0.0], weights=[90, 90])}
    ev_w = aggregate("rubric", 2, rubric)
    print("\n  Weighted rewards (Harvey LAB style: weight = number of rubric criteria):")
    print(f"    mean of per-task means = {st.mean(r.mean for r in rubric.values()):.3f}"
          f"   vs   RRSI's S_hat = {ev_w.S:.3f} (fraction of all criteria passed)")
    return f"crash scored {ev_crash.S:.3f} under RRSI vs {naive:.3f} if dropped"

estimator()

RRSI measures two numbers per harness: S, the reward averaged over every trial of every task, and C, the mean policy tokens per trial. TaskResult records one task&#8217;s trials and aggregates them. The detail worth copying into any agent evaluation is how missing trials are handled. When a candidate crashes on the hardest task, an estimator that drops the missing trials reports 0.750 and makes the crash look like an improvement. At the same time, RRSI counts each missing trial as zero reward with the full denominator and reports the same 0.500 as before, so a candidate cannot look better by destroying the trials it finds hard. Weighted rewards cover rubric-graded suites such as Harvey LAB, where S becomes the fraction of all criteria passed rather than the mean of per-task means.

Copy CodeCopiedUse a different Browser

FAMILIES = ["parse", "search", "edit", "test"]
H0 = {"skill": {f: 0.0 for f in FAMILIES}, "memo": [], "cost": 1.0}

def make_world(seed, n_evolve, n_heldout=80):
    """Tasks with a family and a difficulty. Evolve ids are task_NNN, held-out ids held_NNN."""
    r = random.Random(seed)
    world = {f"task_{i:03d}": (FAMILIES[i % 4], r.gauss(0, 1)) for i in range(n_evolve)}
    world.update({f"held_{i:03d}": (FAMILIES[i % 4], r.gauss(0, 1)) for i in range(n_heldout)})
    return world

def p_success(h, world, task):
    """The frozen policy: a logistic in harness skill minus task difficulty, or 0.97 if memorised."""
    if task in h["memo"]:
        return 0.97
    family, difficulty = world[task]
    return 1 / (1 + math.exp(-(0.3 + h["skill"][family] - difficulty)))

def run_trials(h, world, ids, k, rng):
    return {t: TaskResult(rewards=[float(rng.random() < p_success(h, world, t)) for _ in range(k)],
                          tokens=[round(12_000 * h["cost"] * math.exp(rng.gauss(0, 0.08))) for _ in range(k)])
            for t in ids}

def true_score(h, world, ids):
    return sum(p_success(h, world, t) for t in ids) / len(ids)

def calibrated_delta(world, k, seed, repeats=3):
    """delta from `repeats` independent evaluations of the SAME harness H0."""
    ids = [t for t in world if t.startswith("task_")]
    rng = random.Random(10_000 + seed)
    evals = [aggregate(f"base{j}", k, run_trials(H0, world, ids, k, rng)) for j in range(repeats)]
    return calibrate(evals, z=CFG.delta_z, reps=200), evals

@section("3. The noise band: how far one harness's score moves between two evaluations")
def noise_band():
    world = make_world(0, 40)
    ids = [t for t in world if t.startswith("task_")]
    rng = random.Random(1)
    scores = [aggregate(f"H0#{j}", 2, run_trials(H0, world, ids, 2, rng)).S for j in range(6)]
    print(f"  H0 evaluated 6 times on 40 tasks x k=2: {[round(s, 3) for s in scores]}")
    print(f"  true expected score {true_score(H0, world, ids):.3f}; spread of the estimates"
          f" {max(scores) - min(scores):.3f}. Nothing about the harness changed.")

    print(f"\n  calibrate() turns repeated evaluations into delta = z * sd(null dS), z = {CFG.delta_z}:")
    print(f"  {'evaluator':>12s} {'trials':>7s} {'delta':>8s}   method")
    deltas = {}
    for n, k in [(40, 2), (100, 4), (400, 8)]:
        cal, _ = calibrated_delta(make_world(0, n), k, seed=0)
        deltas[f"{n}x{k}"] = cal["delta"]
        print(f"  {f'{n} x k={k}':>12s} {n * k:>7d} {cal['delta']:>8.4f}   {cal['method']}")
    print("\n  The paper's calibrated bands are 0.017 (coding), 0.004 (workspace) and 0.020 (engineering).")
    print("  A gain smaller than delta is indistinguishable from re-running the same harness, and")
    print("  Algorithm 2 treats it that way. Remember the first row: it becomes the lesson of step 11.")
    return "delta " + ", ".join(f"{k}={v:.3f}" for k, v in deltas.items())

noise_band()

Before any rule can separate a real gain from luck, it needs to know how far one harness&#8217;s score moves on its own. We build a small simulated agent, whose success on each task is a logistic function of harness skill minus task difficulty, and evaluate the unchanged starting harness six times on forty tasks with two trials each: the scores spread by 0.113 although nothing changed. calibrate turns repeated evaluations of the same harness into delta, twice the standard deviation of the difference between two runs. With 80 trials delta is about 0.108; with 3,200 trials it falls to about 0.013, in the range the paper reports for its instances (0.004 to 0.020). For selection purposes, any gain smaller than delta is indistinguishable from re-running the same harness.

Copy CodeCopiedUse a different Browser

def ev_at(S, C, job, n=200):
    """An EvalResult with exactly score S (in steps of 1/n) and C tokens per trial."""
    hits = round(S * n)
    return aggregate(job, 1, {f"task_{i:03d}": TaskResult(rewards=[1.0 if i < hits else 0.0], tokens=[C])
                              for i in range(n)})

INCUMBENT = ev_at(0.630, 10_000, "incumbent")
S_STAR, DELTA = 0.640, 0.020

@section("4. Algorithm 2, branch by branch: the floor, the cost rule and the noise band")
def algorithm_2():
    print(f"  incumbent S = {INCUMBENT.S:.3f}, C = {INCUMBENT.C:,.0f}   best ever S* = {S_STAR}   delta = {DELTA}")
    print(f"  floor = S* - delta = {S_STAR - DELTA:.3f}\n")
    cases = [
        ("A  slipped below the floor", 0.600, 10_000, ["prompt"], None),
        ("B  real gain, pays for its tokens", 0.690, 12_000, ["prompt"], None),
        ("C  real gain, far too expensive", 0.660, 25_000, ["subagent"], None),
        ("D  slightly WORSE but cheaper", 0.625, 8_000, ["context_mgmt"], None),
        ("E  in the band but costlier", 0.640, 11_500, ["prompt"], None),
        ("F  in the band, new sub-agent", 0.630, 10_000, ["subagent"], None),
        ("F' in the band, prompt tweak", 0.630, 10_000, ["prompt"], None),
        ("G  like B, breaks a domain guard", 0.690, 12_000, ["prompt"], ["valid-output rate fell"]),
    ]
    rows = []
    for label, S, C, comps, guards in cases:
        cand = Candidate(label[:2].strip(), [{"id": "C1", "component": c} for c in comps], ev=ev_at(S, C, label))
        dec = judge(cand, INCUMBENT, S_STAR, DELTA, CFG, incumbent_counts={}, guards=guards)
        rows.append((label, dec))
        print(f"  {label:36s} S={S:.3f} C={C:>6,}  {'ADMIT ' if dec.admissible else 'reject'}")
        print(textwrap.indent(textwrap.fill(dec.reason, 88), " " * 6))

    print("\n  Three rules, in the order RRSI applies them:")
    print("    1. never fall below the best score ever seen, minus the noise band        (A)")
    print("    2. a gain bigger than delta must pay for any extra tokens: dC <= 0.10 + 40*dS  (B, C)")
    print("    3. inside the band scores are a tie, so prefer the cheaper harness, and let a")
    print("       never-tried structural component break the tie                          (D, E, F, F')")
    print("  D is the surprising one: RRSI admits a harness that scored LOWER than the incumbent.")
    return f"{sum(d.admissible for _, d in rows)}/{len(rows)} admissible; D admitted at dS={rows[3][1].delta_S:+.3f}"

algorithm_2()

Algorithm 2 is implemented as pure functions, so we can hand it candidates and read its reasons verbatim. We fix an incumbent at S 0.630 and 10,000 tokens, a best-ever score of 0.640 and delta 0.020, and send eight candidates through judge. A candidate below the floor, the best score ever seen minus delta, is rejected outright. A gain larger than delta must pay for its extra tokens under the rule that the relative cost change stays below 0.10 plus 40 times the gain; a +6 point gain at +20% tokens is admitted, and a +3 point gain at +150% tokens is not. Inside the band, scores are treated as a tie and a shaped score of 100 times the gain minus 15 times the cost change, plus a small bonus for a never-accepted structural component, decides; that is how RRSI admits candidate D, which scored lower than the incumbent but costs 20% fewer tokens, and how a new sub-agent breaks a tie that an equally scoring prompt tweak does not. A domain guard vetoes regardless of score.

Copy CodeCopiedUse a different Browser

@section("5. One round of selection: the highest score does not always win")
def one_round():
    c_hi = Candidate("C", [{"id": "C1", "component": "subagent"}], ev=ev_at(0.660, 25_000, "C"))
    d_lo = Candidate("D", [{"id": "C1", "component": "context_mgmt"}], ev=ev_at(0.625, 8_000, "D"))
    leak = Candidate("X", [{"id": "C1", "component": "memory"}], gate_failure="critic_reject")
    winner, decisions = select_round([c_hi, d_lo, leak], INCUMBENT, S_STAR, DELTA, CFG, incumbent_counts={})
    for d in decisions:
        print(f"  {d.variant}: {'admissible' if d.admissible else 'rejected  '}  {d.reason[:92]}")
    new_star = max(S_STAR, winner.ev.S)
    print(f"\n  winner: {winner.variant}  (S {winner.ev.S:.3f}, C {winner.ev.C:,.0f})")
    print(f"  the new incumbent scores {winner.ev.S - INCUMBENT.S:+.3f} vs the old one and costs"
          f" {(winner.ev.C - INCUMBENT.C) / INCUMBENT.C:+.0%} tokens; S* stays {new_star:.3f}")
    print("\n  C scored highest and still lost: its +3pp does not pay for +150% tokens. D moved the")
    print("  incumbent DOWN inside the noise band because it is 20% cheaper. Because S* only ever")
    print("  rises, the floor never follows the incumbent down, so a chain of 'cheaper but slightly")
    print("  worse' swaps cannot walk the score away. X never reached evaluation at all.")
    return f"winner {winner.variant} at dS={winner.ev.S - INCUMBENT.S:+.3f}, dC={(winner.ev.C - INCUMBENT.C) / INCUMBENT.C:+.0%}"

one_round()

select_round applies judge to every candidate in a round and keeps the highest-scoring admissible one. We give it the expensive candidate, the cheaper slightly worse one, and a candidate the critic already rejected. The highest scorer loses because its three-point gain does not pay for 150% more tokens, the critic-rejected candidate never reaches evaluation, and the winner moves the incumbent down by half a point while cutting its token cost by a fifth. The detail that keeps this safe is S*, which only ever rises: the floor is anchored to the best score ever measured rather than to the incumbent, so a chain of cheaper-but-slightly-worse swaps cannot walk the score away over many rounds.

Copy CodeCopiedUse a different Browser

@section("6. The proposal side: an edit budget that anneals from 4 toward 1")
def edit_budget_schedule():
    table = budget_table(CFG.T, CFG.b_min, CFG.b_max)
    print("  b_t = ceil(b_min + (b_max - b_min) * (1 + cos(pi t / T)) / 2)")
    print(f"  T={CFG.T}, b in [{CFG.b_min}, {CFG.b_max}]:")
    print("    t   : " + " ".join(f"{t:>2d}" for t in range(CFG.T)))
    print("    b_t : " + " ".join(f"{b:>2d}" for b in table))
    print(f"    round {CFG.T} (after the run) -> {edit_budget(CFG.T, CFG.T, CFG.b_min, CFG.b_max)}")
    print("\n  Early candidates may bundle up to 4 coordinated edits. Note the ceil(): the cosine term is")
    print(f"  only exactly zero at t = T, so inside a {CFG.T}-round run the budget bottoms out at"
          f" {min(table)}, not {CFG.b_min}.")
    print("  Every edit in a bundle inherits the bundle's single measurement, so the shrinking budget is")
    print("  what makes late history attributable to fewer components. It caps how MANY edits ride")
    print("  together, never WHICH mechanisms the harness may eventually contain.")
    return "budget " + "".join(str(b) for b in table)

edit_budget_schedule()

The proposal side regularizes how edits are drafted, not which ones are kept. edit_budget implements the annealed L0 budget from the paper: a cosine schedule from b_max to b_min, and by default it allows up to four coordinated edits per candidate for the first eight rounds, three for the next five, and two for the last seven. The ceiling in the formula means the budget only reaches its minimum of one at t = T, one step after the run ends, which is easy to miss when reading the equation. Because every edit in a bundle inherits the bundle&#8217;s one measurement, the shrinking budget is what makes late-run history attributable to fewer components. The budget limits how many edits travel together and never restricts which mechanisms the harness may eventually contain.

Copy CodeCopiedUse a different Browser

CRITIC_PATTERNS = [
    (r"\btask_\d{3}\b", "hard-codes an evolve-set task id"),
    (r"expected_output|grader|rubric\[", "reads the grader or the expected answer"),
]
COMPONENT_SIGNALS = [
    ("control_flow", [r"\bretry\(", r"max_attempts"]),
    ("context_mgmt", [r"compress_context", r"keep_last"]),
    ("config", [r"CONFIG\["]),
]

class ScreenOnly(Domain):
    name = "screen"
    critic_patterns = CRITIC_PATTERNS
    briefs = {"critic": "A coding agent harness."}

@section("7. The critic's deterministic layer, and how edits are tagged")
def critic_and_tags():
    dom = ScreenOnly()
    diffs = {
        "memorise answers": "+ memory = Memory('answers')\n+ memory.remember('task_007', cached_patch)",
        "peek at the grader": "+ if os.path.exists('/grader/expected_output.txt'): return read_it()",
        "leaked credential": "+ api_key = 'sk-live-0123456789abcdefghijkl'",
        "empty diff": "   ",
        "general retry rule": "+ for attempt in range(max_attempts): result = retry(step)",
    }
    for label, diff in diffs.items():
        try:
            verdict = review(dom, diff, summary=label, targets_mode="evolve")
            print(f"  {label:20s} -> {verdict['verdict']:6s} {verdict['reasons']}")
        except ZeroDivisionError as e:
            print(f"  {label:20s} -> passed the deterministic layer; the LLM layer raised"
                  f" ZeroDivisionError: {e}")
    print("\n  Gotcha: with RRSI_VERTEX_PROJECTS unset, rrsi.llm.generate computes `x % len(projects)`")
    print("  outside its try block, so the helpful 'set RRSI_VERTEX_PROJECTS' error is never reached.")
    print("  A clean diff is supposed to go to Claude for an intent review; here there is no Claude.")

    print("\n  Every edit is tagged with the component it touches, and a tag needs evidence in the diff:")
    tag_cases = [
        ("skill", "+ \"Remember to run the tests before finishing.\""),
        ("control_flow", "+ for attempt in range(max_attempts): result = retry(step)"),
        (None, "+ review = subcall('reviewer', transcript)"),
        ("memory", "+ context = compress_context(context, keep_last=8)"),
    ]
    for declared, diff in tag_cases:
        tag = normalize(declared, diff, COMPONENT_SIGNALS)
        print(f"    declared {str(declared):13s} -> tagged {tag:13s} {diff[2:60]!r}")
    print("  A proposer cannot label a prompt tweak as a new 'skill' to look novel: without evidence")
    print("  the tag falls back to what the diff actually is.")
    counts = {"prompt": 3, "subagent": 1}
    print(f"\n  novelty(nu) counts STRUCTURAL components {K_STR} the incumbent has never accepted.")
    print(f"  against an incumbent with accepted edits {counts}:")
    for comps in (["memory"], ["subagent"], ["prompt", "client_tool", "memory"]):
        print(f"    {str(comps):38s} nu = {novelty(comps, counts)}")
    return "precheck rejected 4/5 diffs without an LLM call"

critic_and_tags()

The critic screens every candidate diff before any evaluation is spent, in two layers. The first is a deterministic precheck against a generic credential pattern plus the domain&#8217;s own denylist; with patterns for evolve-set task ids and grader paths it rejects a diff that memorises the answer to task_007, one that reads the expected output, one that leaks an API key, and an empty diff, all without calling a model. A clean diff falls through to the second layer, an intent review by Claude, and here the notebook surfaces a real gotcha: with RRSI_VERTEX_PROJECTS unset, rrsi.llm.generate computes an index modulo the number of projects outside its try block and raises ZeroDivisionError, so the helpful configuration error in the code is never reached. We also look at how edits are tagged: normalize keeps a declared component only when the diff carries evidence for it, so a prompt tweak cannot pose as a new skill to win the novelty bonus, and a mislabelled context-management change is tagged as what it is.

Copy CodeCopiedUse a different Browser

@section("8. The edit history: what was tried, what paid off, what to prune")
def edit_history():
    with tempfile.TemporaryDirectory() as tmp:
        h = History(Path(tmp) / "history.jsonl")
        log = [
            (0, "A", [("prompt", "tell the agent to read the failing test first")], "ACCEPTED", 0.030, 0.02, True, 0.66),
            (1, "A", [("prompt", "ask for a plan before editing")], "REJECTED", -0.010, 0.05, False, 0.65),
            (1, "B", [("subagent", "add a reviewer sub-agent"), ("memory", "persist lint rules")],
             "REJECTED", -0.020, 0.40, False, 0.64),
            (2, "A", [("config", "raise the step limit")], "ACCEPTED", 0.005, -0.03, True, 0.665),
            (3, "A", [("prompt", "shorter system prompt")], "LOST", -0.001, -0.10, False, 0.664),
            (4, "B", [("memory", "cache task_014 solution")], "critic_reject", None, None, False, None),
            (5, "A", [("prompt", "stricter output format")], "REJECTED", -0.004, 0.00, False, 0.661),
        ]
        for t, v, edits, outcome, dS, dC, acc, S in log:
            h.append_candidate(t, v, [{"id": f"C{i + 1}", "component": c, "hypothesis": hyp}
                                      for i, (c, hyp) in enumerate(edits)],
                               outcome, dS, dC, acc, S, 12_000 if S else None, diff=None)
        t_now = 6
        print(f"  {len(h.records())} per-edit records from {len(log)} candidates"
              f" (the two-edit bundle in round 1 wrote two records with ONE measurement)")
        print(f"  T_t, tried components : {sorted(h.tried())}   (the critic-rejected edit is not 'tried')")
        g_t = h.yield_g(t_now, CFG.n_prune)
        print("  g_t, best gain in the last n_prune rounds: "
              + ", ".join(f"{c} {'none measured' if g == -math.inf else f'{g:+.3f}'}" for c, g in sorted(g_t.items())))
        prune = h.prune_set(t_now, CFG.n_prune)
        print(f"  B_t, prune set        : {[p['component'] for p in prune]}")
        for p in prune:
            if p["accepted_edits_in_incumbent"]:
                print(f"      {p['component']}: still in the incumbent but no recent gain ->"
                      f" {[e['hypothesis'] for e in p['accepted_edits_in_incumbent']]}")

        trajectory = [0.630, 0.660, 0.660, 0.665, 0.665, 0.665, 0.665]
        sigma = stall_flag(trajectory, t_now, CFG.w, DELTA)
        ex = exploration(t_now, sigma, h.tried(), CFG.m_draft)
        print(f"\n  S over rounds {trajectory}: moved {trajectory[t_now] - trajectory[t_now - CFG.w]:+.3f}"
              f" in the last w={CFG.w} rounds -> sigma_t = {sigma}")
        print("  what the proposer is told next round:")
        print(textwrap.indent(textwrap.fill(ex["text"], 84), "    "))
    print("\n  The proposer sees this history, so a falsified hypothesis ('ask for a plan first', -1pp)")
    print("  is not redrawn, and a stalled run is pushed toward components it has never touched.")
    return f"prune set {[p['component'] for p in prune]}, stall flag {sigma}"

edit_history()

History writes one JSONL record per edit, and the loop derives four summaries from it. The tried set excludes edits the critic dropped, since they were never measured. The recent yield g_t is the best measured gain per component within the last n_prune rounds, and every component whose recent yield is not positive enters the prune set B_t, together with any machinery from that component that is still in the incumbent; in our history that flags a prompt edit accepted in round zero that has not paid off since. The stall flag fires when the score has moved less than delta over the last w rounds, and exploration then writes the directive the proposer receives, reserving a candidate slot for components the run has never exercised. Because the proposer is conditioned on all of this, a falsified hypothesis is not drawn again.

Copy CodeCopiedUse a different Browser

def write_harness(root, h):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "harness.json").write_text(json.dumps(h))
    return root

class SimulatedAgentDomain(Domain):
    """A Domain adapter over the simulated agent: the same contract RRSI's coding,
    workspace and engineering instances implement."""
    name = "simulated"
    critic_patterns = CRITIC_PATTERNS
    component_signals = COMPONENT_SIGNALS
    briefs = {"critic": "A coding agent harness evaluated on parse/search/edit/test tasks."}

    def __init__(self, world, seed):
        self.world, self.rng = world, random.Random(seed)

    def evolve_ids(self):
        return [t for t in self.world if t.startswith("task_")]

    def heldout_ids(self):
        return [t for t in self.world if t.startswith("held_")]

    def smoke_ids(self, incumbent_per_task=None):
        return self.evolve_ids()[:3]

    def run(self, root, runs_dir, job, ids, k, log_prefix=""):
        out = Path(runs_dir) / "jobs" / job
        if (out / "trials.json").exists():
            return                                        # resume-safe, as the contract requires
        h = json.loads((Path(root) / "harness.json").read_text())
        per = run_trials(h, self.world, ids, k, self.rng)
        out.mkdir(parents=True, exist_ok=True)
        (out / "trials.json").write_text(json.dumps(
            {t: {"rewards": r.rewards, "tokens": r.tokens} for t, r in per.items()}))

    def score(self, runs_dir, job, ids, k):
        d = json.loads((Path(runs_dir) / "jobs" / job / "trials.json").read_text())
        return {t: TaskResult(rewards=d[t]["rewards"], tokens=d[t]["tokens"]) for t in ids}, {}

@section("9. A Domain adapter: plugging an environment into RRSI's own evaluate()")
def domain_adapter():
    dom = SimulatedAgentDomain(make_world(0, 40), seed=3)
    with tempfile.TemporaryDirectory() as tmp:
        root, runs = write_harness(Path(tmp) / "wt_H0", H0), Path(tmp) / "runs"
        ev = evaluate(dom, root, runs, "H0", dom.evolve_ids(), k=2)
        files = sorted(str(p.relative_to(tmp)) for p in Path(tmp).rglob("*") if p.is_file())
        print(f"  evaluate(domain, worktree, runs_dir, 'H0', 40 ids, k=2) -> S={ev.S:.3f}  C={ev.C:,.0f}")
        print(f"  files: {files}")
        again = evaluate(dom, root, runs, "H0", dom.evolve_ids(), k=2)
        print(f"  evaluate() again on the same job -> S={again.S:.3f} (read back, not re-run)")
    print("\n  The harness lives in files under a worktree root, exactly as RRSI's real instances keep")
    print("  one git worktree per candidate. RRSI never runs an agent or grades anything itself; the")
    print("  adapter's run() and score() do, and everything in steps 2-8 consumes what they return.")
    return f"adapter evaluated H0 at S={ev.S:.3f} through rrsi.evaluate.evaluate"

domain_adapter()

RRSI never runs an agent or grades a deliverable itself; a Domain adapter does, and the same interface backs the paper&#8217;s coding, workspace and engineering instances. We implement one for the simulated agent: evolve and held-out task splits, a run method that reads the harness from files under a worktree root and writes trial results under a runs directory, a score method that reads them back as TaskResult objects, and the domain&#8217;s critic patterns and component signals. RRSI&#8217;s own evaluate function then scores the starting harness through the adapter, and calling it a second time on the same job reads the stored trials back rather than re-running them, the resume-safety the contract requires.

Copy CodeCopiedUse a different Browser

def propose_edit(r, evolve_ids):
    """The scripted proposer. Each draw is one edit whose TRUE effect we know."""
    u = r.random()
    if u < 0.35:
        fam = r.choice(FAMILIES)
        comp = r.choice(["prompt", "control_flow", "context_mgmt"])
        diff = {"prompt": f"+ \"On {fam} tasks, check the edge cases before finishing.\"",
                "control_flow": f"+ for attempt in range(max_attempts): result = retry({fam}_step)",
                "context_mgmt": f"+ context = compress_context(context, keep_last=12)  # {fam}"}[comp]
        return {"kind": "general", "component": comp, "family": fam, "effect": r.gauss(0.20, 0.30),
                "dcost": 0.02, "diff": diff}
    if u < 0.55:
        ids = r.sample(evolve_ids[:40], 3)
        return {"kind": "leaky", "component": "memory", "ids": ids, "dcost": 0.03,
                "diff": "+ memory = Memory('solutions')\n" + "\n".join(
                    f"+ memory.remember('{i}', cached_patch)" for i in ids)}
    if u < 0.70:
        return {"kind": "inert", "component": "config", "dcost": r.uniform(-0.02, 0.05),
                "diff": "+ CONFIG['log_level'] = 'debug'"}
    if u < 0.85:
        return {"kind": "expensive", "component": "subagent", "effect": 0.15, "mult": 1.5,
                "diff": "+ review = subcall('reviewer', transcript)"}
    return {"kind": "compress", "component": "context_mgmt", "effect": -0.03, "mult": 0.85,
            "diff": "+ context = compress_context(context, keep_last=6)"}

def apply_edit(h, e):
    h = copy.deepcopy(h)
    if e["kind"] == "general":
        h["skill"][e["family"]] += e["effect"]
        h["cost"] *= 1 + e["dcost"]
    elif e["kind"] == "leaky":
        h["memo"] = sorted(set(h["memo"]) | set(e["ids"]))
        h["cost"] *= 1 + e["dcost"]
    elif e["kind"] == "inert":
        h["cost"] *= 1 + e["dcost"]
    else:                                                  # expensive / compress: every family
        for f in FAMILIES:
            h["skill"][f] += e["effect"]
        h["cost"] *= e["mult"]
    return h

def search(world, mode, *, seed, k, delta, T=CFG.T, m=CFG.m):
    """One run of harness search. mode: 'greedy' | 'critic only' | 'rrsi'. Same proposer stream in all."""
    dom = SimulatedAgentDomain(world, seed=seed * 7 + 1)
    proposer = random.Random(seed * 13 + 5)
    ids = dom.evolve_ids()
    with tempfile.TemporaryDirectory() as tmp:
        tmp, h = Path(tmp), copy.deepcopy(H0)
        runs, hist = tmp / "runs", History(tmp / "history.jsonl")
        inc = evaluate(dom, write_harness(tmp / "H0", h), runs, "H0", ids, k)
        S_star, audit, n_evals = inc.S, [], 1
        for t in range(T):
            b_t = edit_budget(t, T, CFG.b_min, CFG.b_max)
            cands, drafts = [], []
            for v in "AB"[:m]:
                edits = [propose_edit(proposer, ids) for _ in range(proposer.randint(1, b_t))]
                hc = h
                for e in edits:
                    hc = apply_edit(hc, e)
                diff = "\n".join(e["diff"] for e in edits)
                tags = [{"id": f"C{i + 1}", "component": normalize(e["component"], e["diff"], COMPONENT_SIGNALS),
                         "hypothesis": e["kind"]} for i, e in enumerate(edits)]
                c = Candidate(f"r{t}{v}", tags)
                if mode != "greedy" and precheck(diff, dom.critic_patterns):
                    c.gate_failure = "critic_reject"      # screened BEFORE any evaluation is spent
                else:
                    c.ev = evaluate(dom, write_harness(tmp / c.variant, hc), runs, c.variant, ids, k)
                    n_evals += 1
                cands.append(c)
                drafts.append((hc, edits))
            if mode == "rrsi":
                winner, decisions = select_round(cands, inc, S_star, delta, CFG,
                                                 hist.incumbent_component_counts())
                for c, d in zip(cands, decisions):         # the records loop.round() writes
                    outcome = (c.gate_failure if c.ev is None else
                               "ACCEPTED" if c is winner else "LOST" if d.admissible else "REJECTED")
                    hist.append_candidate(t, c.variant, c.edits, outcome, d.delta_S, d.delta_C,
                                          c is winner, d.S, d.C, None, d.reason)
            else:                                          # unregularized: keep the best score if it rose
                live = [c for c in cands if c.ev is not None and c.ev.S > inc.S]
                winner = max(live, key=lambda c: c.ev.S) if live else None
            for c, (hc, edits) in zip(cands, drafts):
                audit += [(e["kind"], c is winner) for e in edits]
            if winner is not None:
                h, inc = drafts[cands.index(winner)][0], winner.ev
                S_star = max(S_star, inc.S)
        return {"evolve_measured": inc.S, "evolve_true": true_score(h, world, ids),
                "heldout_true": true_score(h, world, dom.heldout_ids()), "tokens": h["cost"],
                "memorised": len(h["memo"]), "evals": n_evals, "audit": audit}

MODES = ["greedy", "critic only", "rrsi"]

def compare(n_evolve, k, seeds):
    out = {mode: [] for mode in MODES}
    deltas = []
    for s in seeds:
        world = make_world(s, n_evolve)
        cal, _ = calibrated_delta(world, k, seed=s)
        deltas.append(cal["delta"])
        for mode in MODES:
            out[mode].append(search(world, mode, seed=s, k=k, delta=cal["delta"]))
    return out, st.mean(deltas)

def fmt(xs, d=3):
    return f"{st.mean(xs):.{d}f}±{st.pstdev(xs):.{d}f}"

@section("10. Greedy vs RRSI in a world where we know the truth")
def miniature():
    seeds = range(8)
    out, delta = compare(40, 2, seeds)
    globals()["MINIATURE"] = (out, delta)                  # step 11 reuses this row
    h0_held = st.mean(true_score(H0, make_world(s, 40), [f"held_{i:03d}" for i in range(80)]) for s in seeds)
    print(f"  40 evolve tasks x k=2, 80 held-out tasks, T={CFG.T}, m={CFG.m}, {len(seeds)} seeds,"
          f" mean calibrated delta {delta:.3f}")
    print(f"  H0 held-out (true) = {h0_held:.3f}\n")
    print(f"  {'mode':12s} {'evolve meas':>12s} {'evolve TRUE':>12s} {'held-out TRUE':>14s}"
          f" {'tokens':>11s} {'memorised':>10s} {'evals':>6s}")
    for mode in MODES:
        rs = out[mode]
        print(f"  {mode:12s} {fmt([r['evolve_measured'] for r in rs]):>12s} {fmt([r['evolve_true'] for r in rs]):>12s}"
              f" {fmt([r['heldout_true'] for r in rs]):>14s} {fmt([r['tokens'] for r in rs], 2) + 'x':>11s}"
              f" {st.mean(r['memorised'] for r in rs):>10.1f} {st.mean(r['evals'] for r in rs):>6.1f}")

    print("\n  Ground-truth audit: share of proposed edits of each kind that ended up in the incumbent")
    kinds = ["general", "expensive", "compress", "inert", "leaky"]
    print(f"  {'mode':12s}" + "".join(f"{k:>11s}" for k in kinds))
    for mode in MODES:
        tally = {k: [0, 0] for k in kinds}
        for r in out[mode]:
            for kind, accepted in r["audit"]:
                tally[kind][0] += 1
                tally[kind][1] += accepted
        print(f"  {mode:12s}" + "".join(f"{tally[k][1]:>5d}/{tally[k][0]:<5d}" for k in kinds))

    print("\n  Where the evolve-set score stops transferring, split in two:")
    print(f"  {'mode':12s} {'winner curse':>14s} {'memorisation':>14s}   (evolve meas - evolve true | evolve true - held-out true)")
    for mode in MODES:
        curse = st.mean(r["evolve_measured"] - r["evolve_true"] for r in out[mode])
        memo = st.mean(r["evolve_true"] - r["heldout_true"] for r in out[mode])
        print(f"  {mode:12s} {curse:>+14.3f} {memo:>+14.3f}")
    print("  Selecting the best of noisy scores inflates every mode about equally; no rule here removes")
    print("  that - only re-measuring on tasks the search never saw does. The critic removes almost all")
    print("  of the memorisation, and it does so before evaluation, which is why its runs cost fewer evals.")
    g, c, r_ = (st.mean(x["heldout_true"] for x in out[m_]) for m_ in MODES)
    tg, tc, tr = (st.mean(x["tokens"] for x in out[m_]) for m_ in MODES)
    return f"held-out {g:.3f} / {c:.3f} / {r_:.3f}, tokens x{tg:.2f} / x{tc:.2f} / x{tr:.2f} (greedy / critic / rrsi)"

miniature()

Now we run the whole selection side as a search: twenty rounds, two candidates a round, bundles sized by the annealed budget, edits tagged by normalize, candidates screened by precheck and scored through the adapter, winners chosen by select_round, and every outcome written to History in the order RRSI&#8217;s loop uses. The scripted proposer draws five kinds of edit whose true effects we know: usually helpful general changes, leaky edits that memorize evolve-task answers, inert configuration changes, expensive sub-agents that help a little everywhere at 1.5 times the tokens, and cheaper context compression. We compare three acceptance rules on the same candidate stream over eight seeds: greedy keeps the best score if it rose, critic only adds the leakage screen, and RRSI adds Algorithm 2 with a calibrated delta. Greedy reaches the highest held-out score, 0.681 against 0.616 for RRSI, while memorizing about ten answers and nearly tripling its token cost; RRSI memorizes none, ends at about half the token cost (1.53 times the starting harness against 2.97 times), and uses a third fewer evaluations. Splitting the evolve-to-held-out gap is the most useful result here: selecting the best of noisy scores inflates every mode by about nine points, which no rule in this loop removes. At the same time, the critic eliminates almost all of the memorization component.

Copy CodeCopiedUse a different Browser

@section("11. Turn the evaluator up: RRSI's caution is calibrated, not configured")
def noise_sweep():
    rows = [("40x2", MINIATURE[1], MINIATURE[0], 8)]      # from step 10
    for n, k in [(100, 4), (400, 8)]:
        out, delta = compare(n, k, range(5))
        rows.append((f"{n}x{k}", delta, out, 5))
    print(f"  {'evaluator':>10s} {'seeds':>5s} {'delta':>7s}  "
          + "".join(f"{m_ + ' held / tokens':>26s}" for m_ in MODES))
    for label, delta, out, n_seeds in rows:
        cells = "".join(f"{st.mean(r['heldout_true'] for r in out[m_]):>13.3f} /"
                        f" x{st.mean(r['tokens'] for r in out[m_]):<9.2f}" for m_ in MODES)
        print(f"  {label:>10s} {n_seeds:>5d} {delta:>7.3f}  {cells}")
    first, last = rows[0], rows[-1]
    rr_first = st.mean(r["heldout_true"] for r in first[2]["rrsi"])
    rr_last = st.mean(r["heldout_true"] for r in last[2]["rrsi"])
    tok_ratio = (st.mean(r["tokens"] for r in last[2]["greedy"]) /
                 st.mean(r["tokens"] for r in last[2]["rrsi"]))
    print(f"\n  As the evaluator sharpens, delta falls from {first[1]:.3f} to {last[1]:.3f} (the paper: 0.004-0.020),"
          f" and RRSI's held-out score rises from {rr_first:.3f} to {rr_last:.3f}.")
    print(f"  At the sharpest setting the unregularized search is spending {tok_ratio:.1f}x RRSI's tokens.")
    print("\n  Read the table honestly: this world has no diminishing returns, so every sub-agent the")
    print("  greedy search stacks keeps buying accuracy. That is the most favourable world possible for")
    print("  spending, and the greedy search does score higher. RRSI trades some of that score for a")
    print("  bounded token bill, zero memorised answers and fewer wasted evaluations - and the size of")
    print("  the trade is set by delta, which it measures from your evaluator rather than taking from you.")
    return (f"delta {first[1]:.3f} -> {last[1]:.3f}; RRSI held-out {rr_first:.3f} -> {rr_last:.3f};"
            f" greedy uses {tok_ratio:.1f}x the tokens")

noise_sweep()

Our first evaluator was noisy, and delta was calibrated from it, so RRSI&#8217;s caution in step 10 reflected the evaluator rather than the method. We repeat the comparison with larger evolve sets and more trials. As the evaluator sharpens, delta falls from 0.096 to 0.025, and RRSI&#8217;s held-out score rises from 0.616 to 0.759, while the unregularized search at the sharpest setting uses 6.5 times as many tokens as RRSI. Greedy still scores higher, and the notebook says why: this simulated world has no diminishing returns, so every sub-agent the greedy search stacks keeps buying accuracy, which is the most favorable world possible for spending. RRSI trades part of that score for a bounded token bill, no memorized answers, and fewer wasted evaluations, and the size of the trade is set by delta, which it measures rather than asks for.

Copy CodeCopiedUse a different Browser

banner("SUMMARY")
for name, res in RESULTS.items():
    print(f"  {name:<76s}  {res}")
print("""
What the miniature does not model
 - Edits that help the evolve suite but hurt a different suite. The paper's LLM critic and its
   held-out and out-of-distribution splits exist for those; a regex screen cannot catch them.
 - A proposer that reads the history. Ours is scripted, so it redraws falsified ideas freely.
Where to go next
 - Run a real instance: `python3 rrsi.py --domain coding smoke` after configuring Claude on Vertex AI
   (RRSI_VERTEX_PROJECTS) and harbor; see domains/coding/README.md.
 - Add a domain: implement rrsi.domain.Domain in domains/<name>/adapter.py, as step 9 did in the notebook.
 - Re-adjudicate a stored round under a different delta or cost rule without re-running anything:
   `python3 rrsi.py --domain <name> readjudicate --t <t>`.
 - Paper: arxiv.org/abs/2609.24972    Code: github.com/google-research/rrsi
""")

The summary prints the one-line result each section returned, states plainly what the miniature does not model, namely edits that help the evolve suite while hurting a different suite, which is what the paper&#8217;s LLM critic and held-out splits exist for, and a proposer that reads the history, and then points at running a real instance, adding a domain, and re-adjudicating a stored round under a different delta without re-running anything.

In conclusion, we took RRSI apart along the line where the paper&#8217;s idea actually lives, the rules that decide which edits a self-improving agent keeps, and ran them offline on a CPU without a model or an API key. The estimator refuses to reward a crash, the noise band is measured rather than chosen, and Algorithm 2 turns out to be subtler than &#8216;reject noisy gains&#8217;: it never lets the score fall below the best seen minus the noise band, it makes a real gain pay for its extra tokens, and inside the band it deliberately prefers the cheaper harness, even one that scored slightly lower. Auditing those rules against a world whose ground truth we controlled was the most informative part: the deterministic critic removed almost all of the memorization before any evaluation was spent, Algorithm 2 held the token bill several times below an unregularized search, and neither removed the inflation that comes from picking the best of noisy scores, which only re-measurement on unseen tasks can do. The honest caveat is equally clear: in a world where tokens always buy accuracy, the unregularized search scores higher, so the value of RRSI&#8217;s regularization depends on how expensive tokens are and how much a leaked answer would cost you, and the notebook gives you the machinery to measure both on your own evaluator.

Check out the FULL CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Google Research RRSI Guide: Mastering Self-Improving AI Agents appeared first on MarkTechPost.