---
publish_time: 1790802564
link: https://www.marktechpost.com/2026/09/30/openai-releases-gpt-6-1-sol-near-astra-coding-and-computer-use-at-one-fifth-of-astras-token-price/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  OpenAI 发布 GPT-6 家族中端模型 GPT-6.1 Sol，主打智能体编程、电脑操作与专业工作，号称以约 Astra 五分之一的 Token 价格获得接近 Astra 的能力。定价每百万输入 2 美元、输出 10 美元，缓存输入 0.1 美元（较 GPT-6 Sol 再降 50%）。上下文窗口 105 万 Token、最大输出 12.8 万，提供 5 档推理强度。基准上 DeepSWE v1.1 与 Astra 持平、较 GPT-6 Sol 高 6.4 个百分点；AutomationBench 较 Opus 5.5 高 2.2 分且成本约三分之一；OSWorld 2.0 距 Astra 仅 2.1 分。仅通过 API、ChatGPT Work 与 Codex 提供，闭源权重，最难的科研任务仍由 Astra 领跑。
---

# OpenAI 发布 GPT-6.1 Sol：近 Astra 编程能力、价格仅五分之一

> 原文链接：https://www.marktechpost.com/2026/09/30/openai-releases-gpt-6-1-sol-near-astra-coding-and-computer-use-at-one-fifth-of-astras-token-price/
> 来源：MarkTechPost

This week, OpenAI released GPT-6.1 Sol. It upgrades GPT-6 Sol, the mid-tier model in the GPT-6 family. OpenAI&#8217;s claim is specific: near-Astra results on agentic coding, computer use, and professional work. The price is one-fifth of GPT-6 Astra&#8217;s standard input and output rates. Cached input drops to $0.10 per million tokens, 50% below GPT-6 Sol.

Is it deployable? Yes, as a hosted model. It is live today in the OpenAI API as gpt-6.1-sol, and in ChatGPT Work and Codex. 

Where Sol Sits in the GPT-6 Lineup

OpenAI now ships 3 GPT-6 tiers. GPT-6 Astra costs $10 input, $50 output, and $1 cached input per million tokens. GPT-6.1 Sol costs $2, $10, and $0.10. GPT-6 Luna costs $0.10, $0.50, and $0.01.

The cached price is quite important most for agents. Agents resend the same system prompt, tool schemas, and history on every step. Cached reads now cost 5% of the uncached input rate, down from 10% on GPT-6 Sol.

Benchmark Results

All figures below are vendor-reported in OpenAI&#8217;s launch post. OpenAI states that competitor numbers came from public reports.

Coding: On DeepSWE v1.1, GPT-6.1 Sol matches GPT-6 Astra at roughly one-fifth of the cost. It beats GPT-6 Sol&#8217;s best score by 6.4 percentage points, at a lower reasoning effort.

Professional work: On GDP.pdf, which tests answers over complex professional PDFs, Sol beats Claude Opus 5.5 with fallbacks. It does so at less than half the cost per task. On AutomationBench 1.0.6, Sol scores 2.2 points above Opus 5.5 at medium effort. That result comes at roughly one-third the cost.

Computer use: On the OSWorld 2.0 offline set, Sol gains 7 points over GPT-6 Sol at maximum effort. It lands within 2.1 points of Astra at roughly one-seventh the cost per task.

Science: On Terminal-Bench Science 0.1, Sol more than doubles GPT-6 Sol&#8217;s score at max effort. Average cost per task is $5.47, versus $23.21 for Opus 5.5 and $23.80 for Astra. Astra still leads at 68.1%, and OpenAI recommends it for the hardest research.

Factuality: At low effort, the share of responses with a factual error falls from 11.4% to 7.7%. That is a reduction of about 32%. The eval uses deliberately difficult conversations where users had flagged earlier model errors.

API Details Developers Need

From the GPT-6.1 Sol model page:

Context window of 1,050,000 tokens, 128,000 max output tokens, and an April 30, 2026 knowledge cutoff.

Text and image input; text output.

reasoning.effort accepts low, medium (default), high, xhigh, and max. The none and minimal settings are not supported.

Use the Responses API for tool calling. Chat Completions works without tool calling.

Prompts above 272K input tokens cost 2x input and cache rates, and 1.5x output, for the full request.

Batch and Flex are 50% cheaper. Fast mode costs 2x standard.

US and EU data residency are supported. Fast mode is unavailable with EU residency.

Fine-tuning is not supported.

OpenAI also plans a GPT-6.1 Sol Ultrafast option in Codex within days. It promises up to 8x faster token generation than standard speed.

Interactive Explainer

&&

How GPT-6.1 Sol Compares

FeatureGPT-6.1 SolClaude Opus 5.5Claude Sonnet 5.5Gemini 3.1 Pro PreviewDeveloper / API IDOpenAI / gpt-6.1-solAnthropic / claude-opus-5-5Anthropic / claude-sonnet-5-5Google / gemini-3.1-pro-previewStatusGenerally availableGenerally availableGenerally availablePreviewInput price (per 1M)$2.00$4.00$2.00$2.00 (≤200K prompt)Output price (per 1M)$10.00$20.00$10.00$12.00 (≤200K prompt)Cached input read (per 1M)$0.10$0.20$0.20$0.20 + $4.50/1M tokens/hr storageLong-prompt surcharge>272K input: 2x input and cache, 1.5x outputNone; 1M at standard ratesNone; 1M at standard rates>200K: $4 input, $18 outputContext window1,050,0001M1M1,048,576Max output tokens128,000128K128K65,536Input modalitiesText, imageText, imageText, imageText, image, video, audio, PDFReasoning controllow to max (5 levels), default mediumAdaptive thinking, always on; default mediumAdaptive thinking; default highThinking supportedBatch pricing (in / out)50% off standard$2 / $10$1 / $5$1 / $6Knowledge cutoffApr 30, 2026Jun 2026Jun 2026Not listedOpen weightsNoNoNoNo

Standard first-party API list prices, verified September 30, 2026.

Claude Sonnet 5.5 matches Sol&#8217;s $2 and $10 list price, but Sol&#8217;s cached input costs half as much. OpenAI&#8217;s benchmarks compare Sol against Opus 5.5, not Sonnet 5.5. Gemini 3.1 Pro matches Sol on input, charges $12 for output, and remains in preview. List prices are not direct cost comparisons. Anthropic notes its newer tokenizer produces roughly 30% more tokens for the same text.

Key Takeaways

GPT-6.1 Sol matches GPT-6 Astra on DeepSWE v1.1 at about one-fifth the cost.

Pricing is $2 input, $10 output, and $0.10 cached input per 1M tokens.

It beats Claude Opus 5.5 on AutomationBench by 2.2 points at about one-third the cost.

It offers a 1,050,000-token context, 128K output, and 5 reasoning effort levels.

It is API-only and closed-weight; Astra still leads the hardest science tasks.

FAQ

What is GPT-6.1 Sol? It is OpenAI&#8217;s mid-tier GPT-6 model, released September 29, 2026, for coding, computer use, and professional work.

How much does GPT-6.1 Sol cost? Standard API pricing is $2 per million input tokens, $0.10 cached input, and $10 output.

Can I self-host GPT-6.1 Sol? No. It is available only through the OpenAI API, ChatGPT Work, and Codex.

The post OpenAI Releases GPT-6.1 Sol: Near-Astra Coding and Computer Use at One-Fifth of Astra&#8217;s Token Price appeared first on MarkTechPost.