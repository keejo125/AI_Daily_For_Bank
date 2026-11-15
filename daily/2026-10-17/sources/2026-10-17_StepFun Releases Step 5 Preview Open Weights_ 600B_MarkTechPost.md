---
publish_time: 1792218595
link: https://www.marktechpost.com/2026/10/16/stepfun-releases-step-5-preview-open-weights-600b-moe-27b-active-1m-context/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  阶跃星辰（StepFun）发布旗舰 Agent 模型 Step 5 Preview 的开放权重（FP8/BF16 已在 HuggingFace、ModelScope 上线，API 已于 9 月 20 日推出）。该稀疏 MoE 模型总参数 600B、每 token 激活 27B、上下文最长 1M，面向软件工程、专业知识工作与金融等长周期 Agent 任务：可导航大型代码库、协调多文件改动、运行代码并迭代，也能分析长文档、图表、截图、视频产出结构化报告。架构采用 92 层窄深设计、门控滑窗与全注意力 3:1 交错、MTP-3 投机解码提速约 30%；编码接近 GLM-5.3、Kimi K3，弱于 GPT-6 Astra、Claude Opus 5。
---

# 阶跃星辰发布 Step 5 Preview 开放权重模型（600B MoE）

> 原文链接：https://www.marktechpost.com/2026/10/16/stepfun-releases-step-5-preview-open-weights-600b-moe-27b-active-1m-context/
> 来源：MarkTechPost

StepFun has released Step 5 Preview as open weights. FP8 and BF16 checkpoints are live on Hugging Face and ModelScope. Step 5 Preview is a sparse Mixture-of-Experts model from StepFun built for long-horizon agentic work. It has 600B total parameters, 27B active per token and up to 1M tokens of context. For developers, this is a new self-hostable option for coding agents, document analysis and finance workflows.

TL;DR

Size: 600B total, 27B active per token, up to 1M-token context.

Runs on: data-center GPUs only. FP8 needs 4x B300 or 8x H200. BF16 needs 8x B300 or 16x H200.

Performance: near open-weight peers GLM-5.3 and Kimi K3 on coding. Behind GPT-6 Astra and Claude Opus 5.

Best: 88.3% on AA-LCR long-context reasoning (Artificial Analysis).

Worst: 33.3% on Terminal-Bench 4.0, versus 41.9% for GLM-5.3.

What is Step 5 Preview?

Step 5 Preview is StepFun&#8217;s flagship model for agentic work. StepFun positions it for software engineering, professional knowledge work and finance. The model navigates large codebases, coordinates multi-file changes, runs code and iterates on results. It also analyzes long documents, charts, screenshots and video to produce structured reports.

The API launched September 20. Weights followed on October 14.

How does the architecture work?

Only 27B of the 600B parameters activate per token. StepFun&#8217;s tech team adds the internals:

Depth: 92 transformer blocks in a narrow, deep design.

Attention mix: gated sliding-window attention and full attention layers, interleaved 3:1.

Sparse GQA: full-attention layers pick 4,096 history tokens per query, scored in blocks of 8.

Speculative decoding: an MTP-3 head gives roughly 30% end-to-end speedup.

Training: FP8 mixed precision, with RL on million-level verifiable agentic environments.

How does Step 5 Preview perform on benchmarks?

StepFun ran its own evaluations at the High reasoning setting. Rivals in its chart ran at Max effort, so the comparison is not like-for-like.

Results reported on the Hugging Face card:

DeepSWE v1.1: 67.7 (SWE-agent harness, temperature 1.0, top_p 0.95)

Terminal-Bench 4.0: 33.3

Agents&#8217; Last Exam (ALE-CLI): 29.5

Independent numbers come from Artificial Analysis via OpenRouter. The model scores 43.7 on the Intelligence Index. It hits 88.3% on AA-LCR and 46.5% on Humanity&#8217;s Last Exam. GDPval-AA lands at 54.3%.

Vals AI results show clear weak spots. SRE Bench is 0.4%. Harvey&#8217;s Legal Agent Benchmark is 9.2%.

On finance, StepFun&#8217;s chart shows 66.4% on FrontierFinance. That beats GLM-5.3 and Kimi K3, but trails Claude Opus 5 at 69.7%.

&

How does it compare with other open-weight models?

FeatureStep 5 PreviewGLM-5.3Kimi K3Total parameters600B753B (HF file size)2.8TActive parameters27BNot disclosed104BContext window1M1M1MInput modalitiesText, image (API adds video)Text onlyText, imageWeight formatsFP8, BF16BF16, FP8MXFP4 weightsLicenseStepFun Model License 1.0GLM-5.3 licenseKimi K3 LicenseMinimum listed self-host setup4x B300 (FP8)Not disclosedNot disclosedDeepSWE v1.1 (StepFun-reported)67.766.967.5Terminal-Bench 4.0 (StepFun-reported)33.341.912.6FrontierFinance (StepFun-reported)66.464.162.6API price per 1M tokens (in / out)$1.00 / $2.70Not disclosed$3.00 / $15.00

Benchmark rows come from StepFun&#8217;s comparison chart, as transcribed by CellCog and eesel.

What hardware does Step 5 Preview need to run?

This is a data-center model. The FP8 checkpoint alone is 650.32 GB. Listed configurations:

FP8 on vLLM or SGLang: 4 B300 GPUs or 8 H200 GPUs, each on 1 node.

BF16 on vLLM: 1 node with 8 B300 GPUs, or 2 nodes with 16 H200 GPUs.

Transformers: offline generation only. The full BF16 shard workflow is not yet validated end to end.

vLLM and SGLang ship dedicated Docker images with OpenAI-compatible APIs. On Blackwell, expert-parallel modes use the MegaMoE backend. StepFun recommends temperature 1.0, top_p 0.95 and top_k 0.

How much does the API cost?

The StepFun API charges $1.00 per 1M input tokens and $2.70 per 1M output tokens. Cache hits cost $0.10 per 1M. Output pricing includes reasoning tokens. The API supports low, medium and high reasoning effort, tool calling and JSON Schema output.

Key Takeaways

600B MoE, 27B active, 1M context, now open weights in FP8 and BF16.

Smallest listed self-host setup: 4x B300 GPUs with FP8.

Best independent score: 88.3% on AA-LCR long-context reasoning.

Weakest spot: 33.3% on Terminal-Bench 4.0.

API costs $1.00 in and $2.70 out per 1M tokens.

Check out the model weights on Hugging Face, GitHub repo, tech blog, BF16 weights, ModelScope and API docs. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post StepFun Releases Step 5 Preview Open Weights: 600B MoE, 27B Active, 1M Context appeared first on MarkTechPost.