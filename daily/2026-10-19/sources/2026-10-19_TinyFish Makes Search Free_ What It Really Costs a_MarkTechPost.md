---
publish_time: 1792347628
link: https://www.marktechpost.com/2026/10/18/tinyfish-free-search-ai-agent-token-cost/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  面向 AI 智能体的 Web 基础设施公司 TinyFish 指出，一个读网页的 AI Agent 要付两类成本：一是检索费（搜索/fetch API 按请求计费），二是模型处理费（抓取页面内容送入模型消耗的 token，以及推理与生成的额外开销）。文章认为团队常为模型预算却低估检索与抓取环节的真实花销，呼吁把“让 Agent 读网页”的全链路成本纳入工程核算。这对构建长期运行、高频检索的 Agent 系统具有成本治理意义。
---

# TinyFish 让搜索免费：AI 智能体读网页的真实成本

> 原文链接：https://www.marktechpost.com/2026/10/18/tinyfish-free-search-ai-agent-token-cost/
> 来源：MarkTechPost

An AI agent that reads the web pays 2 kinds of cost. The first is the retrieval charge: what a search or fetch API bills per request. The second is model processing: content passed from retrieved pages into an AI model consumes tokens, while reasoning and generated responses add further costs. TinyFish, a web infrastructure company for AI agents, argues that teams budget for the model and underestimate how much retrieved content drives it.

This article walks through the token math, the context-window impact, and what the Artificial Analysis Search API leaderboard does and does not show.

TL;DR

What it runs on: TinyFish uses a web-native AI model designed for search, retrieval, and interaction with live websites. The model runs on TinyFish-managed infrastructure, while its cloud browser fleet renders pages and handles website interactions. No local GPU is needed. Access is via REST, Python and TypeScript SDKs, CLI or MCP.

Performance: On the Sep 28, 2026 Artificial Analysis snapshot, TinyFish Search (web) scores 71 at $9.30 per 1,000 benchmark tasks, with 59.0 seconds per task (model plus search time).

Best: $0 retrieval charge within rate limits (Search: 30 requests/min, 500/hour; Fetch: 150 URLs/min, 1,000/day), and the lowest total cost among the 12 configurations displayed on the leaderboard.

Trade-offs: The second longest time per task among displayed configurations, and an Agent product whose built-in model cannot be swapped.

Scores: Highest displayed is Perplexity Search (medium) at 80. Lowest displayed is TinyFish Search (web) at 71. The no-search baseline is 33.

Retrieval charges vs model processing costs

Search and fetch APIs usually bill per request or per page. Whatever they return then enters the model&#8217;s context and is billed as input tokens. Reasoning and output tokens come on top.

Enterprises now route each task to the cheapest capable model, a trend underlined when Stripe agreed to acquire OpenRouter, a gateway spanning 400+ models from 80+ providers. Routing lowers the price per token. It does not change how many tokens a retrieved page contains.

Free Search and Fetch remove TinyFish&#8217;s retrieval charge within its limits. The downstream model still incurs inference costs. That is why the size of each returned page matters.

How big is one page in tokens?

TinyFish ran a fetch quality evaluation on June 2, 2026, across 45 URLs and 5 providers on default settings. For one Daily Mail article with a body of roughly 4,300 characters, the providers returned:

ProviderCharacters returnedEst. tokens*Input cost at $1 / 1M tokens*TinyFish Fetch4,737~1,184~$0.00118Exa Contents65,793~16,448~$0.01645Firecrawl Scrape171,095~42,774~$0.04277Tavily Extract46,433~11,608~$0.01161Parallel Extract600 (excerpt, not the article)~150~$0.00015

*Marktechpost calculation: ~4 characters per token and an illustrative input price of $1 per 1M tokens. Input processing only; excludes retrieval charges, reasoning and output. Real counts vary by tokenizer. Character counts from TinyFish&#8217;s evaluation.

In this example, Firecrawl returned approximately 36 times as many characters as TinyFish.  Parallel also returned only an excerpt rather than the complete article, so its smaller output is not directly comparable to the full-page extractions.

While this illustrates how extraction output size can affect token consumption, the difference comes from a single webpage and should not be generalized across all websites. Those percentages are not used for this individual page comparison because outputs above 30,000 characters were truncated before judging.

Context limits and repeated calls

Assume every extracted character goes into the same context, with no filtering, truncation or summarization. A page containing approximately 42,774 tokens would consume about one-third of a 128K-token context window. Three such pages would require approximately 128,322 tokens, leaving little or no room for system instructions, conversation history, or the agent&#8217;s response.

Agent loops also resend context. Artificial Analysis notes that each turn resends the full conversation, with earlier input billed at the model&#8217;s cached-input price. Caching lowers the cost of rereading a noisy page. It does not remove it, and the page still occupies the window.

In that TinyFish internal evaluation, a result counted as covered only with at least 1,000 characters and a judged signal ratio above 30%. Coverage was TinyFish 93%, Tavily 80%, Exa 73%, Firecrawl 62% and Parallel 58%. Among usable results only, median signal was 90.5% for TinyFish and 89.7% for Exa. TinyFish ran the test on itself, the sample is 45 URLs, and news pages drove most of the gap.

Why TinyFish makes retrieval free

TinyFish frames search as one operation inside execution, like DNS or storage for ordinary software. An agent booking, comparing or filling out a form should care whether the job got done, not which search system found the page. 

TinyFish attributes its free retrieval pricing to three aspects of its infrastructure:

Shared infrastructure: TinyFish built its browser fleet, stealth systems, session hydration and elastic scaling before Search was a product. TinyFish says this changes the marginal economics of search. It does not make the infrastructure free to run.

Specialized models: TinyFish says its web-native AI model is designed for search, fetch, and live-site interaction. Its development draws on agent operational trajectories and large volumes of search activity, helping reduce reliance on general-purpose models for intermediate web tasks.

No giant index: TinyFish says it would rather learn how work gets done than become an indexing company.

TinyFish charges separately for Agent and Browser usage, while Search and Fetch remain free within their published limits. Per the pricing page, Search is free at 30 requests per minute and 500 per hour. Fetch is free at 150 URLs per minute and 1,000 per day. Both keep working at a $0 Wallet balance. Agent costs $0.016 per step with 2 concurrent runs, and Browser costs $0.002 per minute with 5 sessions. New accounts get $8 in Wallet funds.

What the benchmark shows, and what it does not

Artificial Analysis holds the answer model fixed (GPT-5.6 Luna, medium) and changes only the search provider. Model cost covers input, cached, reasoning and output tokens. Differences between providers reflect returned payloads, how many searches the model runs and how much it reasons.

On the Sep 28, 2026 snapshot, model cost ranges from $8.04 to $21.65 per 1,000 tasks across the 12 displayed configurations. These come from 26 products across 13 providers. TinyFish posts $0 for search plus $9.30 for the model, the lowest displayed total.

The trade-offs: TinyFish recorded a Search Index score of 71, the lowest among the displayed configurations, and a DeepSearchQA F1 of 67. Its benchmark time was approximately 59 seconds per task, combining estimated model processing time and measured search time rather than representing API latency alone. Because Artificial Analysis uses its own shared extraction layer, the results do not directly measure TinyFish Fetch. Similarly, benchmark costs per 1,000 tasks should not be confused with API prices per 1,000 requests, since a single task may involve multiple searches.

How TinyFish compares with closest competitors

The table covers 3 selected competitors that appear in both the Artificial Analysis leaderboard and TinyFish&#8217;s fetch test.

FeatureTinyFishExaFirecrawlParallelSearch priceFree (30/min, 500/hr)From $4 per 1k requests (Instant, up to 10 results); $7 Fast/Auto; extra results billed2 credits per 10 results$1 to $5 per 1k requests (10 results)Page fetch / extractFree (150/min, 1,000/day)$1 per 1k pages, per content type1 credit per page$1 per 1kFree allowanceSearch and Fetch at $0 balance, plus $8 Wallet$10 credits/mo1,000 credits/mo$5 credits/mo (up to 5,000 requests, depending on endpoint)Paid automation or research product**Agent $0.016/step; Browser $0.002/minAgent (research) from $0.012/runInteract (browser) 2 credits/minTask API (research) $0.005 to $2.40/requestAA Search Index7174 (auto)7375 (advanced)AA search + model $ per 1k benchmark tasks$0 + $9.30$65.57 + $17.73$30.48 + $12.09$47.93 + $11.29AA time per task (model + search)59.0s32.3s62.0s41.9sFetch coverage (TinyFish internal evaluation, June 2026)93%73%62%58%

**Browser operation and research tasks are different capabilities, so these prices are not directly comparable. Pricing checked Oct 7, 2026: TinyFish, Exa, Firecrawl, Parallel. Benchmark data: Artificial Analysis (Sep 28, 2026) and its methodology. Coverage: TinyFish internal evaluation (June 2026), a single-vendor test separate from the third-party benchmark.

Key Takeaways

Agents pay retrieval charges plus model processing on everything retrieved.

The same article ranged from ~1,184 to ~42,774 estimated tokens by provider.

3 large unfiltered pages can exceed a 128K-token window.

Free Search and Fetch remove TinyFish&#8217;s retrieval charge, not model costs.

TinyFish had the lowest displayed total cost on Artificial Analysis, but the lowest displayed score.

Thanks to the Tinyfish team for the thought leadership / resources for this article. This article is sponsored by TinyFish.

The post TinyFish Makes Search Free: What It Really Costs an AI Agent to Read the Web appeared first on MarkTechPost.