---
publish_time: 1790672496
link: https://www.marktechpost.com/2026/09/29/google-research-open-sources-rrsi-ai-agents-that-improve-their-own-harness-without-overfitting/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google Cloud AI Research联合UNC、Stanford、圣路易斯华盛顿大学发布RRSI（正则化递归自改进），允许LLM智能体重写自身Harness（提示、工具、记忆、控制流与子智能体），模型权重不变。其关键在于约束改进循环本身，使收益在Agent从未优化过的基准上依然成立，避免自改进过拟合。代码Apache 2.0，接受任意LiteLLM模型串。
---

# Google Research 开源 RRSI：不依赖过拟合即可改进自身 Harness 的智能体

> 原文链接：https://www.marktechpost.com/2026/09/29/google-research-open-sources-rrsi-ai-agents-that-improve-their-own-harness-without-overfitting/
> 来源：MarkTechPost

Google Cloud AI Research, with UNC-Chapel Hill, Stanford and Washington University in St. Louis, has released RRSI (Regularized Recursive Self-Improvement). It lets an LLM agent rewrite its own harness: prompts, tools, memory, control flow and sub-agents. Model weights never change. RRSI constrains the improvement loop itself, so gains hold on benchmarks the agent never optimized against.

Deployable? Yes, as a research framework. The code is Apache 2.0, needs Python 3.10+, and accepts any LiteLLM model string. Defaults assume Claude Opus 4.8 on Vertex AI. 

Why Self-Improving Harnesses Overfit

Harness evolution loops propose edits, score them on a fixed evolve set and keep the winner. The same tasks are reused every round, so the loop can memorize them. The RRSI research names 3 failure modes: benchmark-specific fitting, noise chasing and complexity accumulation. Each one widens the gap between evolve-set scores and real transfer.

How RRSI Works

RRSI keeps every harness component editable. It regularizes how the search moves instead.

Proposal side

Annealed edit budget: a cosine schedule lets early rounds bundle several edits. Late rounds allow a single attributable change.

Evidence-aware credit: each candidate is logged with its component, hypothesis, diff, score change and cost change. The proposer reads this ledger, so falsified ideas are not retried.

Structured exploration: when progress stalls inside the noise band, budget shifts to components the run never touched.

Selection side

Leakage critic: rejects task names, entities, answers or benchmark-specific logic before any scoring.

Noise-adjusted floor: gains must clear the variance measured on the unchanged base harness.

Cost rule: extra inference tokens must be paid for by measured gain.

Pruning: components that stop producing gains become deletion targets.

The research team frame these as analogies to classic regularizers. The edit budget maps to L0, pruning to Lasso (L1) and the cost rule to Ridge (L2).

Results Across 8 Benchmarks

Terminal-Bench 2.1 (evolve split): 74.2% to 80.2%.

SWE-bench Verified (never used for selection): 82.0% to 83.8%.

Out of distribution: JobBench +4.7, GDPval +3.5 and APEX-Agents +3.7 points.

EngDesign (evolve) +4.9; Frontier-Eng +4.3 Medal points.

Harvey LAB: +1.1 on the evolve split, +2.3 on its held-out split.

All 6 held-out splits improved. With Gemini 3.5 Flash as the policy, Terminal-Bench 2.1 rose from 64.6 to 78.7. SWE-bench Verified rose from 76.8 to 79.0.

The harness is also lighter. On the agentic workspace instance, RRSI uses 2.42M policy tokens per trial. Unregularized evolution uses 3.80M. The abstract reports this as 30% fewer; the project page says 36%.

RRSI vs Closest Competitors

Scores come from Table 1 of the RRSI research paper. All methods share the same starting harness, policy, evolve split and candidate budget.

FeatureRRSIMeta-HarnessAHETTHEHarnessXCore ideaRegularized proposal and selectionAgentic proposer over code, scores and traces of all prior candidatesObservability-driven loop; edits paired with verified predictionsEvolves harness during test time, no gold labelsModular typed primitives, trace-driven adaptationModel weightsFrozenFrozenFrozenFrozenFrozenCost rule and pruningYesNo*No*No*No*Harvey LAB evolve score90.593.090.791.191.8OOD average (H0 = 39.7)43.640.639.238.039.7

*Per the RRSI research team. OOD average is the mean of JobBench, GDPval and APEX-Agents, computed from Table 1.

Meta-Harness leads on the Harvey LAB evolve split. RRSI has the smallest evolve gain but the only OOD average more than 1 point above H0.

Interactive Explainer

How RRSI Regularizes Agent Self-Improvement

The model stays frozen. The harness (prompts, tools, memory, control flow) evolves, but every edit must pass the regularizers.

1. Run a round
2. Edit budget
3. Acceptance gate
4. Results

Pick a candidate edit, then press Run. Watch where RRSI stops it.

Generic tool fix
Hardcoded task name
Gain inside noise
Token-hungry gain
Stale component
&#9654; Run

ProposerReads full edit ledger, shrinking edit budget

Leakage criticScreens diff before scoring

EvaluateRun on evolve set

GateNoise floor + cost rule

Harness Ht+1Accepted, then pruning check

Candidates are illustrative. The rules they hit are the ones described in the RRSI paper.

// edit ledger: component | hypothesis | &#916;score | &#916;cost | verdict

bt = &#8968; bmin + (bmax &#8722; bmin) &#183; &#189;(1 + cos(&#960;t / T)) &#8969;

bmax (edits per candidate, early) 5
bmin (edits per candidate, late) 1
T (rounds) 16
Early rounds may bundle coordinated edits to find a mechanism. Late rounds get single, attributable changes.

round 0round T&#8722;1

Cosine schedule from the paper (Eq. 4). Slider values are for exploration; the paper lists its own settings in Appendix D.

&#916;S, score gain vs incumbent (pts) 2.0
&#916;C, token cost change (%) 20
&#948;, noise band from repeated base runs (pts) 1.5
&#946;0 + &#946;1&#916;S cost allowance: &#946;1 (% per pt) 8

?Noise-adjusted floor: score must not drop more than &#948; below the best so far

?Clear gain: &#916;S > &#948;, otherwise the paper&#8217;s within-band rule applies

?Cost rule: &#916;C &#8804; &#946;0 + &#946;1&#916;S

&#8230;

Illustrative thresholds (&#946;0 fixed at 5% here). In RRSI, &#948; is estimated on the unchanged base harness and &#946; values are tuned on the evolve set, then frozen.

All 8 benchmarks
vs prior methods
Token cost

Data: RRSI paper &#183; GitHub &#183; project pageBuilt by Marktechpost

&