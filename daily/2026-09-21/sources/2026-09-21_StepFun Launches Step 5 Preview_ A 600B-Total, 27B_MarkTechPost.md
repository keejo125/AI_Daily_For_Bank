---
publish_time: 1789972638
link: https://www.marktechpost.com/2026/09/20/stepfun-launches-step-5-preview/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  阶跃星辰（StepFun）发布Step 5 Preview——总参数600B、激活27B的MoE模型，主打高性价比的推理与Agent能力。文章介绍其在代码、工具调用与长上下文上的定位，作为国产大模型的新一代预览版，面向复杂任务与企业级场景，延续阶跃在开源与商业化之间的双轨策略。
---

# 阶跃星辰发布Step 5 Preview：600B总参数MoE模型

> 原文链接：https://www.marktechpost.com/2026/09/20/stepfun-launches-step-5-preview/
> 来源：MarkTechPost

StepFun has released Step 5 Preview, its new flagship model for agentic work. The target workloads are software engineering, professional knowledge work, and finance. The main pitch is cost. StepFun team states the model delivers comparable intelligence at a substantially lower task cost. That is the &#8216;Pareto frontier&#8217; framing in the launch title.

Is it deployable? Yes, as a hosted API and on the StepFun platform. Self-hosting waits for open weights. StepFun says open weights land on October 15, 2026. By simple arithmetic, 600B parameters need about 1.2 TB in BF16, before KV cache. Plan for multi-GPU server hardware once weights ship.

What StepFun Shipped

Step 5 Preview is a sparse Mixture-of-Experts (MoE) model. It holds about 600B total parameters and activates about 27B per token. That is roughly 4.5% of the weights per token.

The official model documentation lists these specs:

Model ID: step-5-preview

Context window: 1M tokens

Input: text, images, and video

Output: text

Reasoning effort: low, medium, and high

Streaming, tool calling, JSON Mode, JSON Schema, and prompt caching

On research tasks, StepFun team states the model coordinated 950 web fetches in a single agent action. StepFun team also documents a Claude Code integration through its Step Plan.

Architecture: Narrow and Deep

StepFun did not widen the network. It stacked 92 Transformer layers in a narrow-deep layout, according to Pandaily. The research team argues deeper stacks give longer paths for implicit multi-hop reasoning. This matters during long prefill, when agents search, run code, and read tool returns.

Training leans on on-policy, long-horizon reinforcement learning. StepFun cites bit-wise train and inference alignment across MoE routing. Other listed techniques include MTP-3 speculative decoding, FP8 MoE, and KV-cache offload. StepFun reports more than 3x end-to-end speedup for long-horizon RL.

Interactive Explainer

&&&

Benchmarks: Company-Reported vs Independent

Step 5 Preview ran at High effort, while rivals ran at Max.

StepFun reports these results, via RuntimeWire:

BenchmarkStep 5 PreviewClaude Opus 5GPT-6 AstraFrontierFinance66.469.755DRACO83.387.676.8

On coding, StepFun reports 67.7 on DeepSWE v1.1, 49.0 on StepCodeBench, and 80.5 on ProgramBench. GPT-6 Astra and Claude Opus 5 stay ahead on all 3. StepCodeBench is StepFun&#8217;s own benchmark.

StepFun also ran 2 agent experiments lasting 24 hours each. In the first, the model tuned an H100 kernel to 508 TFLOPS, against 493 for Claude Opus 5. In the second, it raised Qwen3-30B-A3B on AIME24 from 53.3% to 60% through automated post-training.

The independent check comes from Artificial Analysis. It scores Step 5 Preview at 44 on its Intelligence Index. The median for reasoning models in a similar price tier is 24. It measured output at 99.8 tokens per second on StepFun&#8217;s API.

Pricing

StepFun&#8217;s API list prices per 1M tokens:

Token typePriceInput, cache miss$1.00Input, cache hit$0.05Output, including reasoning$2.70

Artificial Analysis puts the medians for comparable models at $1.88 input and $10.00 output. There is 1 catch. The model generated 160M output tokens on the index run, against a 92M median. Verbose reasoning eats part of the per-token savings.

Key Takeaways

StepFun&#8217;s Step 5 Preview is a 600B-total, 27B-active MoE model.

It offers a 1M-token context with text, image, and video input.

API pricing is $1.00 input and $2.70 output per 1M tokens.

Artificial Analysis scores it 44 on its Intelligence Index.

Open weights are scheduled for October 15, 2026.

FAQ

What is Step 5 Preview? It is StepFun&#8217;s flagship MoE model for agentic coding, knowledge work, and finance.

Is Step 5 Preview open weight? Not yet. StepFun schedules open weights for October 15, 2026.

How large is the context window? 1M tokens, per StepFun&#8217;s documentation.

How much does it cost? $1.00 per 1M input tokens and $2.70 per 1M output tokens.

Check out the Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post StepFun Launches Step 5 Preview: A 600B-Total, 27B-Active MoE Model With 1M Context for Long-Horizon Agentic Work appeared first on MarkTechPost.