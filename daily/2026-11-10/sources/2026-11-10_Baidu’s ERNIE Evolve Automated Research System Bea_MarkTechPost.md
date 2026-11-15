---
publish_time: 1794241919
link: https://www.marktechpost.com/2026/11/09/baidu-ernie-evolve-automated-research-system/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  百度发布 ERNIE Evolve 自动化研究系统：给定代码仓库、目标与评估标准，系统自主挑选研究方向、修改代码并跑实验，仅保留通过隐藏评估器与独立评审的改动。在三项公开基准上优化 ERNIE-5.5-Flash 推理，昆仑芯 P800 上经四轮研究生成速度达基线 623.6%，并在四项公开指标中三项超越最佳公开结果。
---

# 百度发布 ERNIE Evolve 自动化研究系统

> 原文链接：https://www.marktechpost.com/2026/11/09/baidu-ernie-evolve-automated-research-system/
> 来源：MarkTechPost

Baidu has just released ERNIE Evolve, an automated research system that improves AI training and inference code. Given a repository, an objective and evaluation criteria, it picks research directions, edits code and runs experiments. Only changes that pass a hidden evaluator and a separate reviewer are kept. Baidu team tested the ERNIE Evolve automated research system on three public benchmarks. It then optimized inference for ERNIE-5.5-Flash, still in development. 

TL;DR

Size: It is an agent system; Baidu has not disclosed which LLMs power its agents.

Runs on: Benchmarks used 1 NVIDIA B200 (NanoChat, SOL-ExecBench) and 8×H100 (Speedrun Track 1). Production tests ran on Kunlunxin P800 and GPUs (GPU model not disclosed).

Performance: Beat the best public result on 3 of 4 public metrics, and cleared production checks on ERNIE-5.5-Flash.

Best: Generation speed on Kunlunxin P800 reached 623.6% of baseline after 4 research rounds.

Worst: SOL-ExecBench mean SOL of 0.819, behind the 0.827 leaderboard best.

Bottom line (best): Real production inference gains: +33.7% deterministic throughput, +14.9% decode speed.

Bottom line (worst): Self-reported, system not released, and public-benchmark margins are small.

What is ERNIE Evolve?

ERNIE Evolve is an automated research system from Baidu that optimizes code against a fixed, measurable objective. Baidu announced it on X as a practical step toward recursive self-improvement (RSI). In RSI, AI systems improve the software that builds and serves AI.

How does ERNIE Evolve work?

The system runs 2 nested loops. The outer loop decides what to investigate. The inner loop develops and tests improvements inside each direction.

Director: picks the next research direction and a starting code version. It reads an Experience Bank of past results and a Knowledge Base of papers and code.

Selector: chooses a candidate from a lane&#8217;s tree and names the next hypothesis to test.

Executor: implements that plan in an isolated environment.

Evaluator: a fixed program kept outside the repository. No agent can see it. Gains must exceed the noise threshold.

Reviewer: checks whether a change follows the intended direction or exploits an evaluation loophole.

Several research lanes run in parallel, each with its own tree of code versions. Failed experiments are recorded, so later rounds can avoid repeating them.

How did ERNIE Evolve score on public benchmarks?

Baidu ran the same loop on NanoChat AutoResearch, NanoGPT Speedrun and SOL-ExecBench.

NanoChat AutoResearch: 0.8763 validation BPB within a 5-minute, single-GPU budget. It added an n-gram branch and a document-retrieval branch beside the network, mixed by a learned gate.

NanoGPT Speedrun Track 1: 38.9 s to target loss on 8×H100, versus the 39.9 s record. The results repo reports 38.92 s over 18 runs.

NanoGPT Speedrun Track 3: 2,590 steps, versus 2,690. It decomposed weights into direction and magnitude, then added EMA-Nesterov extrapolation.

SOL-ExecBench: 0.819 mean SOL across 235 kernel problems on B200, short of the 0.827 leader.

ERNIE Evolve vs other automated research systems

MetricsERNIE Evolve (Baidu)RecursiveHyra-1.0 (Tencent Hunyuan)(auto)²-research (rekursiv.ai)NanoChat val BPB ↓0.87630.91090.90150.8878Speedrun Track 1 ↓38.9 s77.5 s76.4 sNot reportedSpeedrun Track 3 ↓2,590 stepsNot reportedNot reportedNot reportedSOL-ExecBench, self-reported ↑0.8190.7540.771Not reportedSOL-ExecBench, per Baidu (Eval Stack v1.1) ↑0.8190.6760.736Not reportedProduction use reportedERNIE-5.5-Flash inferenceNot disclosedScience tasks (math, molecules)Not disclosedWhat is releasedFinal code + logsRun artifactsResults repoRecipe + harness tools

Recursive and Hyra-1.0 Speedrun times were set against the older ~79.7 s record, so they are not like-for-like. Hyra SOL self-report via Tencent coverage.

&&

What did ERNIE Evolve do for ERNIE-5.5-Flash inference?

Baidu team then pointed the system at 3 live engineering tasks on ERNIE-5.5-Flash. Baselines had already been tuned by engineers.

Low latency on Kunlunxin P800: generation speed rose to 623.6% of baseline over 4 rounds. Round 1 enabled fused mHC and speculative decoding via the model&#8217;s multi-token prediction layer (282.9%). Round 2 cut host-side overhead (588.8%). Round 4 fixed dispatch so DeepEP&#8217;s low-latency path engaged.

Deterministic inference for RL: under SGLang&#8217;s deterministic mode, throughput rose 33.7% in about 3 days. Time per output token fell 26% and time to first token fell 12%. A Triton kernel for deterministic sampling, which used about 14% of GPU time, gave the largest single gain.

Single-request decoding on GPUs: speed rose 14.9% with accuracy unchanged. 3 of 7 research directions produced gains. Key changes: FP16 instructions for tiny FP8 matmuls and a 2-level MoE expert scheduler.

Key Takeaways

Two nested loops: a Director picks directions, lanes evolve code trees.

A hidden Evaluator plus a Reviewer guards against reward hacking.

Public wins on NanoChat (0.8763 BPB) and Speedrun (38.9 s, 2,590 steps).

ERNIE-5.5-Flash: 623.6% speed on Kunlunxin P800, +33.7% deterministic throughput.

System stays closed; only results and logs are on GitHub.

Check out the ERNIE Evolve research post and the results repo on GitHub. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Baidu’s ERNIE Evolve Automated Research System Beats NanoChat and NanoGPT Records appeared first on MarkTechPost.