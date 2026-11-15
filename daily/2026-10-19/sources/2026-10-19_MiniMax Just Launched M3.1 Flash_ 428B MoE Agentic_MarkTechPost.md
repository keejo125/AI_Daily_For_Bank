---
publish_time: 1792413478
link: https://www.marktechpost.com/2026/10/19/minimax-m3-1-flash-release/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  MiniMax 于 10 月 19 日在 API 上线 M3.1 Flash，输入价每百万 token 0.15 美元，并确认此前的匿名模型 Space Bunny 即为 M3.1 Flash 的早期版本——该模型已处理超 200T token。规格为 428B 总参数、约 23B 激活（MoE）、100 万 token 上下文，主打接近前沿的 agentic 能力但仅 Flash 级成本。模型权重定于 2026 年 10 月底开源，面向开发者传递“以 Flash 成本拿到近前沿 agentic 表现”的信号。
---

# MiniMax 发布 M3.1 Flash：428B MoE Agentic 模型，输入价 0.15 美元/百万 Token

> 原文链接：https://www.marktechpost.com/2026/10/19/minimax-m3-1-flash-release/
> 来源：MarkTechPost

MiniMax has just released MiniMax M3.1 Flash on its API, priced at $0.15 per 1M input tokens. MiniMax also confirmed that Space Bunny was an earlier M3.1 Flash build. That stealth model processed over 200T tokens. For developers, the message is near-frontier agentic scores at Flash-tier cost. Model weights are due in late October, 2026.

TL;DR

Size: 428B total parameters, about 23B active (MoE); 1,000,000-token context

Runs on: MiniMax API, M Plan and MiniMax Code today. Self-hosting hardware not disclosed; weights arrive Oct 23

Performance: Near-frontier on agentic office work, mid-pack on hard coding, all MiniMax-reported

Best: Automation-Bench v1.0.6 at 62.2, the top score in MiniMax&#8217;s table

Worst: Terminal Bench 4.0 at 38.1, versus 51.8 for Opus 5

What is MiniMax M3.1 Flash?

MiniMax M3.1 Flash is a multimodal mixture-of-experts model from MiniMax. It targets coding, agentic office work and visual reasoning. MiniMax&#8217;s product page lists 428B total parameters and about 23B active. It also mentions sparse attention and a native visual encoder.

The model accepts text, image and video input and returns text. The context window is 1,000,000 tokens. Those parameter totals match MiniMax M3, which ships at ~428B total and ~23B active. MiniMax has not published a technical report on what changed in the Flash variant.

How does reasoning work in M3.1 Flash?

Reasoning is always on and cannot be disabled. Developers choose from 5 effort levels: Low, Medium, High, Xhigh and Max. MiniMax recommends Max as the default.

Migration matters here. Requests sending thinking.type=disabled or effort=none return an error. Reasoning arrives in a separate reasoning_content field, which may be absent. Integrations that parse inline <think> tags from M3 need updating.

How does M3.1 Flash perform on benchmarks?

All scores below are MiniMax-reported. No independent replication exists yet.

On the CoWork set, M3.1 Flash leads Automation-Bench v1.0.6 at 62.2. Opus 5 scores 50.3 and GPT-5.6 Sol 45.8. It ties Opus 5 on BankerToolBench at 76.2. It also tops LOCA-Bench 256K at 60.3. Agents&#8217; Last Exam lands at 29.6.

Coding results are mixed. DeepSWE v1.1 scores 73.7, just above GPT-5.6 Sol at 73.0. DeepSeek-V4.1-Flash-1017 scores higher at 77.0. Terminal Bench 4.0 is the weakest result at 38.1. SWE Refactor Bench sits at 23.0, versus 31.0 for Opus 5.

On vision, BabyVision with tools reaches 91.0 and CharXiv RQ reaches 82.5. HLE without tools scores 43.4.

Spot checks hold up. The Kimi K3 model card reports DeepSWE 67.5 and BabyVision 85.7, matching MiniMax&#8217;s table. One inconsistency: MiniMax&#8217;s cost chart plots Automation-Bench max effort at 62.8, while its table says 62.2.

What does M3.1 Flash cost per task?

MiniMax frames value as cost per task, not per token. On its Automation-Bench chart, all 5 effort levels sit below $0.05 per task. Scores range from 52.8 at low effort to 62.8 at max. A full 152-task Agents&#8217; Last Exam run cost about $111 at 29.6. On DeepSWE, DeepSeek V4.1 Flash-1017 plots both higher and cheaper at max effort.

&

How do you deploy MiniMax M3.1 Flash?

The model is live on platform.minimax.io as MiniMax-M3.1-Flash. MiniMax supports Anthropic-compatible and OpenAI-compatible access, including Chat Completions and Responses. It is also available through M Plan and the MiniMax Code desktop app.

Pricing is a flat $0.15 input and $0.60 output per 1M tokens. Cache reads cost $0.015 per 1M. There is no long-context surcharge. MiniMax M3 costs $0.30/$1.20 up to 512K input and doubles above that. Per token, Flash is half of M3&#8217;s standard rate. MiniMax claims 1/3 the cost of M3 but has not detailed the calculation.

On speed, MiniMax&#8217;s product page lists about 150 tokens per second. The announcement claims 3x the speed of M3. Weights arrive October 23; the license is not yet disclosed. For scale, M3&#8217;s MXFP8 build is about 440 GB.

How does M3.1 Flash compare with DeepSeek, Kimi and GLM?

FeatureMiniMax M3.1 FlashDeepSeek V4.1 FlashKimi K3GLM-5.3Total / active params428B / ~23B (MiniMax)552B / 8B prefill, 16B decode (NVIDIA card)2.8T / 104B (HF)~744B / ~40B, shared GLM-5 baseContext1M1M (DeepSeek docs)1,048,5761,048,576 (Cloudflare)InputsText, image, videoText, imageText, imageTextWeights / licenseDue Oct 23; license not disclosedOpen, MITOpen, Kimi K3 LicenseOpen weightsAPI price in / out (1M)$0.15 / $0.60 flat$0.30 / $1.20 peak; half off-peak$3.00 / $15.00$1.40 / $4.40Self-host hardwareNot disclosedNot disclosedMXFP4 weights; vLLM, SGLangNot disclosedAutomation-Bench v1.0.6*62.254.846.748.8DeepSWE v1.1*73.774.267.566.9Terminal Bench 4.0*38.131.212.637.9BabyVision (w/ tools)*91.089.685.7Not reported

*Scores from MiniMax&#8217;s comparison table. Kimi K3 DeepSWE and BabyVision match its own card.

What are the limitations?

Every benchmark is vendor-reported, and harness choice shifts results. Automation-Bench numbers do not transfer across sources. Kimi K3&#8217;s card reports 30.8 on a 600-task public subset, while MiniMax lists 46.7.

Opus 5 leads by 13.7 points on Terminal Bench 4.0 and 14.1 on NL2Repo-Bench. Always-on reasoning also sets a token and latency floor for simple calls. Self-hosting details remain unknown until October 23.

Key Takeaways

428B MoE with ~23B active and a 1M context.

$0.15/$0.60 per 1M tokens, half of M3&#8217;s per-token rate.

Leads Automation-Bench v1.0.6 at 62.2, MiniMax-reported.

Trails Opus 5 by 13.7 points on Terminal Bench 4.0.

Weights land Oct 23; reasoning cannot be disabled.

Check out the announcement, product page and API docs. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post MiniMax Just Launched M3.1 Flash: 428B MoE Agentic Model at $0.15/M Input appeared first on MarkTechPost.