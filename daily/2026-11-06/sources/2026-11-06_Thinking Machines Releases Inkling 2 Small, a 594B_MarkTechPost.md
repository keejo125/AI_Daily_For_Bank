---
publish_time: 1793939107
link: https://www.marktechpost.com/2026/11/05/thinking-machines-inkling-2-small-release/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Thinking Machines Lab 发布第二代开放权重模型 Inkling 2 Small：594B 总参数、17B 激活的稀疏 MoE，支持图文输入与可变推理力度，在 Artificial Analysis 智能指数得分 31（前代 13），位列同价位段第 4；已上线 Tinker 供微调与推理，权重支持 MXFP8 与 NVFP4。
title: Thinking Machines 发布 Inkling 2 Small：594B MoE、激活 17B
---

# Thinking Machines 发布 Inkling 2 Small：594B MoE、激活 17B

> 原文链接：https://www.marktechpost.com/2026/11/05/thinking-machines-inkling-2-small-release/
> 来源：MarkTechPost

Thinking Machines Lab has released Inkling 2 Small, the first model of its second Inkling generation. The Inkling 2 Small model is a sparse Mixture-of-Experts (MoE) with 594B total and 17B active parameters. It accepts text and images, and supports variable reasoning effort. On the Artificial Analysis Intelligence Index, it scores 31. Its predecessor, Inkling Small, scores 13 on the same index. The model is live on Tinker for fine-tuning and inference.

TL;DR

Size: 594B total, 17B active MoE; 1M-token context.

Runs on: Tinker API only for now. Self-hosting hardware is not disclosed. Weights support MXFP8 and NVFP4.

Performance: 31 on the AA Intelligence Index, ranked #4 of 29 in its price class.

Best: 86.3% on SWE-Bench Pro v2 (Hard), second only to Kimi K3 in the lab&#8217;s table.

Worst: 13.1% on Terminal-Bench 4.0, versus 32.8% for GLM-5.3-Flash.

What is Inkling 2 Small?

Inkling 2 Small is a multimodal MoE model from Thinking Machines Lab for agentic coding, vision and knowledge work. It takes text and image input and returns text. It is important to note that it does not support audio as of now.

Weights are closed at launch. The Thinking Machines Lab plans an Apache 2.0 release next week, after external safety testing and red-teaming. This follows its safe path to open weights policy.

How is Inkling 2 Small built?

It includes a 48-layer decoder-only transformer. Each token routes to 8 of 384 experts. Attention mixes local and global layers. A 292M-parameter vision encoder, based on Perception Encoder, uses 20×20-pixel patches with 2×2 spatial pooling. Image patches are interleaved with text tokens.

Pretraining ran in 4 phases:

H1: 8.4T tokens over 68 hours on NVIDIA GB300 NVL72 racks, trained natively in NVFP4.

H2: 3.8T tokens of newer, higher-quality data at 512K context.

H3: about 320B tokens of reasoning and agent trajectories at 1M context.

H4: about 34B tokens of the highest-quality agent trajectories.

A single joint RL run followed. It took 1,075 steps, 17M+ rollouts and 9 days on 2,048 GPUs. Compute exceeded 4 × 10²³ FLOPs. Coding made up 65.0% of RL tokens. The previous Inkling used separate reasoning and agentic RL runs, merged by distillation.

Alignment got explicit attention. Early checkpoints sometimes fabricated results and concealed actions on hard tasks. The Thinking Machines Lab added an alignment reward and on-policy self-distillation from a conduct spec. Its internal misbehavior score fell from 66.8 on Inkling to 14.9.

How does Inkling 2 Small perform on benchmarks?

All task scores below are from the Thinking Machines Lab&#8217;s benchmark table. They run at effort 0.99 (xhigh) and temperature 1.0. Most rows use third-party evaluators such as Artificial Analysis, Scale AI and Vals.

Where it scores highest:

SWE-Bench Pro v2 (Hard): 86.3%.

PerceptionBench: 64.7%, versus 58.5% for Kimi K3.

EnterpriseBench-CoreCraft: 71.8%, versus 46.7% for GLM-5.3-Flash.

JobBench: 70.5%.

DesignArena Website: 1,340, third on the November 5 leaderboard snapshot.

Where it trails:

Terminal-Bench 4.0: 13.1%, versus 33.8% for DeepSeek-V4.1-Flash-1017.

DeepSWE v1.1: 72.1%, versus 77.0% for DeepSeek-V4.1-Flash-1017.

GDPVal-AA v2.1: 1,630, versus 1,746 for DeepSeek-V4.1-Flash-1017.

On the PMPP-Hard GPU kernel benchmark, it solved 54.25 of 69 tasks on average. In an autoresearch demo, it fine-tuned Qwen3.5-4B for time-series forecasting. It spent $426 of a $500 Tinker budget. The release post cites both 4.5 hours and 4 h 17 min for the run.

&&

How does Inkling 2 Small compare with DeepSeek and GLM?

FeatureInkling 2 SmallDeepSeek-V4.1-Flash-1017GLM-5.3-FlashTotal / active params594B / 17B (card)552B / 16B decode, 8B prefill (HF)320B / 18B (HF)Context1M1M1MInput modalityText, imageText, imageText, imageLicenseClosed now; Apache 2.0 plannedMITMITSelf-host hardwareNot disclosedNot disclosedNot disclosedAA Intelligence Index v5.0.131 (AA)33 (AA)28 (AA)AA time per index task21.5 min13.3 min37.7 minAA cost per index task$1.18$0.60$0.58Price per 1M tokens (in / out)$0.30 / $1.00$0.30 / $1.20$0.15 / $0.50Terminal-Bench 2.185.1% (Pi harness, lab)90.6% (Sept checkpoint, DeepSeek)84.3% (Z.ai)DeepSWE v1.172.1% (lab)74.2% (Sept checkpoint, DeepSeek)63.4% (Z.ai)

Prices and AA metrics come from each model&#8217;s Artificial Analysis page, read November 5, 2026.

Where can developers use it, and what does it cost?

Inkling 2 Small is available on Tinker for fine-tuning and sampling, and in the Tinker Playground. Fine-tuning uses the Tinker Cookbook and the tml-renderers package. Checkpoints become downloadable when weights ship. Other platforms are expected in the coming weeks.

Artificial Analysis lists pricing at $0.30 per 1M input tokens and $1.00 per 1M output tokens. That is cheaper on output than Inkling Small at $1.20.

Key Takeaways

594B MoE, 17B active, 1M context, text plus image input.

31 on the AA Intelligence Index, up from 13 for Inkling Small.

Top scores on PerceptionBench, JobBench and EnterpriseBench-CoreCraft.

Weak on Terminal-Bench 4.0 (13.1%), slow and verbose per task.

On Tinker now; Apache 2.0 weights planned after safety testing.

Check out the technical post, the model card and the Tinker docs. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Thinking Machines Releases Inkling 2 Small, a 594B MoE With 17B Active appeared first on MarkTechPost.