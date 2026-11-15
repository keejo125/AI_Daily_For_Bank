---
publish_time: 1791405510
link: https://www.marktechpost.com/2026/10/07/anthropic-releases-claude-haiku-5-5-a-small-model-with-1m-context-priced-at-0-10-per-million-input-tokens/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Anthropic 发布 Claude Haiku 5.5，是其最便宜、最快的小模型，支持 100 万 token 上下文，输入价格低至每百万 token 0.10 美元，主打高吞吐、成本敏感型任务。官方称其在多项基准上超越上一代 Haiku 4.5 及若干同档竞品，成为新的小模型“守门员”。
---

# Anthropic 发布 Claude Haiku 5.5：百万上下文、每百万输入 token 仅 0.10 美元的小模型

> 原文链接：https://www.marktechpost.com/2026/10/07/anthropic-releases-claude-haiku-5-5-a-small-model-with-1m-context-priced-at-0-10-per-million-input-tokens/
> 来源：MarkTechPost

Anthropic has released Claude Haiku 5.5, its cheapest and fastest small model to date. It targets high-volume work like summaries, compaction, classification and subagent tasks. It keeps a 1M token context window and up to 128K output tokens. Pricing starts at $0.10 per million input tokens and $0.50 per million output tokens. That is 90% below Claude Haiku 4.5 for prompts up to 100K tokens.

Is it deployable? Yes, as a hosted API. Haiku 5.5 is generally available on the Claude API, Amazon Bedrock, Google Cloud, Microsoft Foundry and Claude Platform on AWS. 

What Anthropic Shipped

Haiku 5.5 is the first Haiku-class model with an adjustable effort setting. Adaptive thinking is on by default, and the effort parameter defaults to medium.

It takes text and images, outputs text, and has a June 2026 knowledge cutoff. Batch jobs support up to 300K output tokens in beta.

It is important to note two key things. Non-default temperature, top_p or top_k values return a 400 error. The new tokenizer also counts the same text as roughly 30% more tokens than Haiku 4.5. The migration guide covers both.

Pricing: A 2-Tier Structure

Pricing splits at 100K prompt tokens. Up to 100K, input costs $0.10 and output $0.50 per million. Cache reads cost $0.01 and 5-minute cache writes $0.125. Above 100K, rates rise to $0.50 input and $2.50 output.

Haiku 4.5 charged $1 input and $5 output. Anthropic says about 90% of Haiku 4.5 requests stayed under 100K tokens. After adjusting for the tokenizer, it estimates Haiku 5.5 runs about 75% cheaper on average. Batch processing takes another 50% off.

GPT-6 Luna lists identical short-context rates. Its higher tier starts only above 272K input tokens, at $0.20 and $0.75. For a 150K-token prompt, Luna is cheaper on list price.

Benchmarks

All figures below are Anthropic-reported (see the system card):

OSWorld 2.1 (offline subset): 72.4%, versus 48.9% for GPT-6 Luna and 15.7% for Haiku 4.5.

Terminal-Bench 4.0: 39.2%, versus 16.4% for Luna and 0.0% for Haiku 4.5.

FrontierCode 1.1 (Main): 46.4%, versus 42.4% for Luna.

Humanity&#8217;s Last Exam: 45.9% without tools and 57.4% with tools.

GDPval-AA v2.1: 1620, versus 1437 for Luna and 735 for Haiku 4.5.

Sonnet 5.5 still leads every row, including 70.6% on Terminal-Bench 4.0. Anthropic itself recommends Sonnet 5.5 and Opus 5.5 for complex agentic coding.

Best Use Cases

Three workloads fit Haiku 5.5 best: 

The first is subagent work under Opus 5.5 or Sonnet 5.5. At Rogo, a Haiku 5.5 subagent pulls a 10-K revenue line while a bigger model builds the deck. 

The second is high-volume document Q&A and summarization. AlphaSense tested it on a feature handling about 8M calls a week. 

The third is speed-sensitive work like live customer support and browser use.

Haiku 5.5 vs Its Closest Competitors

FeatureClaude Haiku 5.5GPT-6 LunaGemini 3.5 Flash-LiteInput / output (per 1M)$0.10 / $0.50$0.10 / $0.50$0.30 / $2.50Long-prompt pricing$0.50 / $2.50 above 100K$0.20 / $0.75 above 272KFlat rateCache read (per 1M)$0.01$0.01$0.03 + storageContext window1M tokens1,050,000 tokens1,048,576 tokensMax output128K tokens128,000 tokens65,536 tokensInputsText, imagesText, imagesText, image, video, audio, PDFReasoning controlAdaptive thinking + effort (default medium)reasoning.effort none to max (default medium)Thinking supportedComputer useSDK support in betaSupported (Responses API)Supported (Preview)Batch discount50%50% (Batch and Flex)50%Knowledge cutoffJun 2026May 18, 2026Not listed on model pageWhere to runClaude API, Bedrock, Google Cloud, Microsoft Foundry, Claude Platform on AWSOpenAI APIGemini API

Sources: Anthropic docs, Anthropic announcement, OpenAI model page, OpenAI pricing, Google model page, Google pricing. Standard-tier list prices, verified October 7, 2026.

Interactive Explainer

&

Key Takeaways

$0.10 input and $0.50 output per 1M tokens for prompts up to 100K tokens.

1M context, 128K output, adaptive thinking with an effort setting (default medium).

72.4% on OSWorld 2.1 versus 15.7% for Haiku 4.5 (Anthropic-reported).

Same short-context list price as GPT-6 Luna; Luna is cheaper above 100K tokens.

Positioned as a subagent under Opus 5.5 and Sonnet 5.5, not a coding lead.

Check out the Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

[Sponsored] The web is the one API most agents are missing. Databases, calendars and repos have APIs. The open web mostly doesn’t. The TinyFish MCP server gives any MCP client four tools: TinySearch, TinyFetch (full pages as markdown, JavaScript included), TinyBrowser for logins and forms, and TinyAgent for multi-step jobs. Search and Fetch are free.

The post Anthropic Releases Claude Haiku 5.5: A Small Model With 1M Context Priced at $0.10 per Million Input Tokens appeared first on MarkTechPost.