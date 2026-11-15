---
publish_time: 1789164068
link: https://www.marktechpost.com/2026/09/11/can-llms-engineer-their-own-agent-harness-bytedance-seeds-harnessdev-says-only-34-of-64-changes-generalize/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  字节 Seed 联合新加坡科技大学设计、佐治亚理工等机构提出 HarnessDev，将评测对象从“模型答案”转为“模型写出的可运行 Agent Harness”（执行循环、工具、上下文、状态、恢复、验证）。在 Terminal-Bench 2.1 上，相同权重的 GPT-5 在 Terminus 2 仅解 35.2% 任务，在 Codex CLI 达 49.6%，说明 Harness 影响巨大。HarnessDev 经 Creation/Evolution 两阶段自动生成 Harness，但 64 项改动仅 34 项可泛化，揭示 LLM 自研 Harness 的局限。
---

# 大语言模型能否自研 Agent Harness？字节 Seed 的 HarnessDev 仅 34/64 改动可泛化

> 原文链接：https://www.marktechpost.com/2026/09/11/can-llms-engineer-their-own-agent-harness-bytedance-seeds-harnessdev-says-only-34-of-64-changes-generalize/
> 来源：MarkTechPost

An agent harness is the code around a model: execution loop, tools, context, state, recovery, and verification. Per the Terminal-Bench 2.1 leaderboard, GPT-5 solves 35.2% of tasks inside Terminus 2 but 49.6% inside Codex CLI with identical weights. Most benchmarks keep that harness fixed. HarnessDev proposed by team of researchers from ByteDance Seed, Singapore University of Technology and Design, Georgia Institute of Technology, M-A-P, and TokenWave.AI, flips the target: the artifact under evaluation is the runnable harness the model writes, not the answer it produces.

2 stages: Creation and Evolution

In Creation, every creator receives the same weak seed: passive file, search, and process primitives plus result and trajectory writers, with no loop, planner, verifier, retry, or stopping rule. Unmodified, it scores 0 everywhere. The creator gets a task-family spec, a short design tutorial, and 1 to 3 development cases, builds a full harness, and the harness is frozen before hidden tasks.

In Evolution, the creator starts from its own frozen Creation code harness and revises it using execution feedback from a fixed set of 100 SWE-bench Pro tasks and all 89 Terminal-Bench 2.1 tasks. Each official candidate must complete both evaluations as a pair, with a budget of 10 pairs and at most 2 five-task probes between pairs. Every official version is later scored on 630 held-out SWE-Pro instances the creator never sees.

Harnesses are graded on capability (task success) and efficiency (executor tokens, with creator tokens excluded).

Setup

6 creator LLMs were tested: Opus 4.8, GPT-5.5, Gemini 3.1 Pro, DeepSeek V4 Pro, Qwen 3.7 Max, and Seed 2.0 Pro, working inside Claude Code 2.1.177 (GPT-5.5 used Codex 0.144.3). Creation spans 4 domains and 5 benchmarks totaling 2,207 instances: SWE-bench Pro public split (731), Terminal-Bench 2.1 (89), MLE-bench (75), EQ-Bench3 (46), and BrowseComp (1,266). Each creator builds 3 harnesses per benchmark, reported as avg@3. Self-Eval runs each harness with its creator; Unified-Eval runs all with Gemini 3.1 Pro.

Creation results

Under Self-Eval, Opus 4.8 posts the highest average score at 67.8 against a human-engineered reference of 86.2. The gap depends on domain:

Code: Opus 4.8 reaches 69.3 on SWE-Pro versus the 80.0 reference. Gemini 3.1 Pro leads Terminal-Bench at 68.8 versus 88.8.

Search: the widest gap. The best BrowseComp score is 52.6 (GPT-5.5) against a 92.2 reference.

Writing: Opus 4.8 scores 84.6 on EQ-Bench3, above the 83.7 reference.

ML experimentation: Opus 4.8 (32.9) and Gemini (32.4) beat the 24.0 MLE-bench reference.

The SWE-Pro, Terminal-Bench, and BrowseComp references are external results from OpenAI&#8217;s GPT-5.6 report, not re-runs.

Code volume did not predict quality: the 18 code harnesses added 17,111 net lines, yet Gemini added the fewest (1,006) and led Terminal-Bench. Self-test count barely correlated with score (Spearman 0.13 to 0.26); revision calls reached 0.57.

Much generated machinery is inert. Of 108 code component instances, 72 trigger in real runs and 18 never fire, all of them state and memory. 11 of 18 harnesses define a State class, yet no checkpoint event appears across 26,679 trajectories. 124 of 587 writing features are dead code.

Cost and executor transfer

MLE-bench token use varied roughly 19-fold. GPT-5.5 hit a 19.1 medal rate with 29.3M tokens while DeepSeek V4 hit 19.6 with 208.4M. Swapping the executor to Gemini reshuffled rankings: Qwen gained 17.6 points on BrowseComp and 12.9 on MLE-bench, while Opus 4.8&#8217;s SWE-Pro score fell from 69.3 to 33.0, partly because one harness hard-coded a 120-step limit around its original executor. The Opus search harness&#8217;s duplicate-query rate jumped from 10.1% to 88.2% after the switch.

Evolution results

9 lineages (5 self-runtime, 4 fixed-Gemini) produced 73 official versions and 64 adjacent switches. All 5 self-runtime creators improved on held-out tasks, from +1.43 to +4.44 points (mean +3.11). Under fixed Gemini, only Opus improved; GPT-5.5 regressed 10.32 points.

Progress was not monotonic. Of 64 switches, 8 regressed on both benchmarks, 16 on one, 27 gained only within the noise band, and 2 showed clear positive evidence. A single commit can vary by about ±4.75 pair-score points. Feedback and held-out scores moved in the same direction only 34 of 64 times (53.1%), and only 2 of 9 declared final versions were held-out optimal. Of 169 new functions or classes, 25 have no caller.

The clearest win: Opus 4.8 noticed 99 of 100 runs reported success while only 48 passed, traced it to premature completion, and added a completion gate. Failure diagnosis was otherwise the weakest step: the dedicated trajectory interface was called only twice.

Interactive explainer

&&

Key Takeaways

HarnessDev scores the harness a model builds, not the answer it returns.

Self-built harnesses match or beat references on writing and ML experimentation but trail badly on code and search.

Harness quality is executor-specific; Opus 4.8 drops from 69.3 to 33.0 on SWE-Pro under Gemini.

Evolution gains are small, noisy, and only 34 of 64 changes point the same way on held-out tasks.

Much generated state and memory code never executes.

Check out the Paper and Project Page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Can LLMs Engineer Their Own Agent Harness? ByteDance Seed&#8217;s HarnessDev Says Only 34 of 64 Changes Generalize appeared first on MarkTechPost.