---
publish_time: 1791841310
link: https://www.marktechpost.com/2026/10/12/alibaba-qwen-introduces-qwengyre-elastic-reinforcement-learning-rl-for-xlong-horizon-agents/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  阿里 Qwen 团队发布 QwenGyre，一个面向极长程 Agent 训练的弹性强化学习（RL）框架。它是在线 RL 系统，通过未修改的黑盒 harness 训练 coding agent，支持运行数小时、处理近百万 token 的 rollout，已在旗舰模型 Qwen 3.8 2.4T 上验证。两大核心：在 rollout 与训练间调度闲置 GPU，以及对 Agent 历史做分支以高效探索。
---

# 阿里 Qwen 团队发布 QwenGyre：面向极长程 Agent 的弹性强化学习框架

> 原文链接：https://www.marktechpost.com/2026/10/12/alibaba-qwen-introduces-qwengyre-elastic-reinforcement-learning-rl-for-xlong-horizon-agents/
> 来源：MarkTechPost

Alibaba&#8217;s Qwen team has introduced QwenGyre, an elastic reinforcement learning RL framework for extreme-long-horizon agent training. QwenGyre is an online reinforcement learning system from Alibaba that trains coding agents through unmodified, black-box harnesses. It targets rollouts that run for hours and process close to 1M tokens. The QwenGyre elastic RL framework was used on Qwen&#8217;s flagship Qwen 3.8 2.4T model. It rests on 2 core ideas. It moves idle GPUs between rollout and training. It also turns branching agent histories into bounded training samples.

TL;DR

Size: A training framework, not a model. Tested on Qwen 3.6 122B and Qwen 3.8 2.4T (A95B per Qwen), with ~700K tokens per rollout.

Runs on: Multi-node GPU clusters. The 122B runs used 24 to 32 nodes; the 2.4T run used 192 nodes (4 cells of 48). GPU model not disclosed. Megatron trains, SGLang serves rollouts.

Performance: 1.38x to 1.78x faster than Async, 1.21x to 1.85x faster than Colocate, at matched scores.

Best: 1.85x end-to-end speedup over Colocate on TerminalBench.

Worst: Only 1.21x over Colocate on the 2.4T model, where many queries ran near the timeout.

Bottom line: 

Best: NL2RepoBench rises from 52.5% to 58.5% in 48 steps. 

Worst: the paper links no public code release.

What problem does QwenGyre solve?

The research team defines &#8216;XLong-horizon&#8217; tasks as agent runs spanning hours and hundreds of model and tool interactions. Examples include generating full repositories from specs, as in NL2Repo-Bench.

Two problems appear at this scale:

First, rollouts have long tails. In a Colocate setup, training waits for the slowest execution while GPUs idle. In an Async setup, fixed GPU pools cannot lend spare capacity to each other.

Second, harnesses like Claude Code compact context, spawn sub-agents and retry. One execution becomes a branching tree, not a single trajectory. Expanding every path duplicates shared prefixes and inflates training cost.

How does the Elastic Scheduler work?

QwenGyre splits GPUs into cells that share a training layout. Each cell can serve rollouts or host a full training replica. A core cell owns the authoritative weights and optimizer state. Satellite cells join training later.

The scheduler tracks a rollout waterlevel: queued and running executions. As executions finish, cells switch to training once the remaining cells can still serve all live work. Model calls are rerouted through a proxy, so the harness keeps running.

Key mechanics:

KV-cache blocks migrate over RDMA during rerouting, reducing prefix recomputation.

Satellites pull core weights through Mooncake&#8217;s Transfer Engine and join an ongoing batch.

Streaming training lets cells claim micro-steps as data becomes ready.

Average role switches took 8.52 s (rollout to training) and 3.46 s (training to rollout).

How does the Trajectory Processor build training samples?

A proxy records exact token IDs and behavior log-probabilities using token-in, token-out (TITO). Calls are stored as prefix-shared trajectory trees.

Partial scoring: Timed-out executions are still scored on their preserved workspace. Evaluator failures are excluded, never treated as a zero reward.

Bounded sampling: At most 5 trajectories per execution are kept, ranked main > main-summary > sub-agent > sub-agent-summary.

Deduplication: Shared targets count once, and only policy-generated tokens are trained.

Fair weighting: Losses average within each execution, so extra branches do not inflate its weight.

A cap of 5 matched uncapped training scores while cutting forward-backward time by 25.2%. Training uses an adapted GSPO with 16 rollouts per group.

How fast is QwenGyre? Benchmark results

All runs used Claude Code 2.1.220 as the harness, with equal GPU budgets and matched staleness.

Workload (model)vs Asyncvs ColocateNL2RepoBench (Qwen 3.6 122B, 48 steps)1.42x to 1.53x1.36x to 1.47xDeepSWE (Qwen 3.6 122B, 24 steps)1.569x to 1.572x1.610x to 1.824xTerminalBench (Qwen 3.6 122B, 24 steps)1.383x to 1.430x1.809x to 1.849xNL2RepoBench (Qwen 3.8 2.4T, 48 steps)1.78x1.21x

On the 2.4T model, QwenGyre finished 48 steps in 75.42 hours. Async took 134.55 hours and Colocate took 91.47 hours. Evaluation pass rate rose from 52.48% to 58.54%.

&&

How does QwenGyre compare with other agentic RL frameworks?

FeatureQwenGyreveRLAReaLAgent LightningDeveloperAlibaba QwenByteDance Seed + communityTsinghua IIIS + Ant GroupMicrosoftLicenseNot disclosedApache-2.0Apache-2.0MITGPU placementElastic cells, switch mid-rolloutFlexible device mapping, HybridEngine reshardingFully asynchronousNot disclosedBlack-box harnessYes, via proxyNot disclosedYes, via base_url swapYes, near-zero code changeTraining / rolloutMegatron / SGLangFSDP, Megatron / vLLM, SGLangMegatron, FSDP, Archon / vLLM, SGLangNot disclosedLargest stated scaleQwen 3.8 2.4T671B modelsNot disclosedNot disclosedHeadline speedupUp to 1.85x vs ColocateNot disclosed2.77x vs synchronous (v0.3)Not disclosedPublic codeNot disclosedYesYesYes

Speedups come from each project&#8217;s own setup and are not directly comparable.

Key Takeaways

QwenGyre moves GPUs between rollout and training without stopping live agents.

Trajectory trees cap samples at 5 per execution and train shared prefixes once.

Timed-out runs still get scored on their partial work.

Up to 1.85x faster than Colocate and 1.78x faster than Async.

Qwen 3.8 2.4T NL2RepoBench improved from 52.5% to 58.5% in 48 steps.

Check out the full QwenGyre paper on arXiv and Qwen&#8217;s announcement post. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Alibaba Qwen Introduces QwenGyre: Elastic Reinforcement Learning RL for XLong-Horizon Agents appeared first on MarkTechPost.