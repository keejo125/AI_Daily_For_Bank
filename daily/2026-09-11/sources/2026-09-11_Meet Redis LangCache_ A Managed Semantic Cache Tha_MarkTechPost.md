---
publish_time: 1789079688
link: https://www.marktechpost.com/2026/09/10/meet-redis-langcache-a-managed-semantic-cache-that-cuts-llm-api-costs-by-up-to-90-and-returns-cache-hits-up-to-15x-faster/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Redis 推出全托管语义缓存服务 LangCache，位于应用与模型之间，按语义（而非逐字）匹配历史问答，命中即返回已存响应。Redis 称可将 LLM API 成本最高降低90%，缓存命中响应比重新查询模型快最多15倍。已以公开预览形式上线 Redis Cloud，提供 REST API 与 Python/JS SDK。对客服助手、RAG 等高频重复意图场景，语义缓存可显著降低推理账单。
---

# Redis 推出 LangCache：托管语义缓存，LLM API 成本最高降90%

> 原文链接：https://www.marktechpost.com/2026/09/10/meet-redis-langcache-a-managed-semantic-cache-that-cuts-llm-api-costs-by-up-to-90-and-returns-cache-hits-up-to-15x-faster/
> 来源：MarkTechPost

Production LLM applications rarely receive a question nobody has asked before. Support assistants and RAG pipelines field the same intents thousands of times a day, each phrased differently, and most stacks treat every phrasing as a fresh, fully billed request. Redis LangCache is a fully managed semantic caching service that sits between the application and the model, matches incoming prompts against previously answered ones by meaning rather than exact text, and returns the stored response when a close enough match exists. Redis reports API cost savings of up to 90% and cache-hit responses up to 15x faster than re-querying the model.

Is it deployable? Yes. LangCache is available today as a public preview on Redis Cloud, accessed through a REST API with Python and JavaScript SDKs, and Redis notes that features and behavior may change during the preview.

The Problem: Paraphrases Are Still Full LLM Calls

Consider three requests to a customer-support assistant:

&#8220;Can I get a refund after buying the monthly plan?&#8221;

&#8220;Is the monthly subscription refundable?&#8221;

&#8220;Can I cancel the plan and get my money back?&#8221;

The wording differs, but the question and answer are identical. Without a semantic cache, each version triggers a complete generation: input tokens processed, output tokens decoded, user waiting.

Prefix caching only removes part of that cost. When requests share a system prompt or context, the engine reuses the KV states computed for that prefix, but the request still reaches the LLM, new tokens still get processed, and the full answer still gets decoded. A prefix-cache hit is a cheaper generation call, not an avoided one.

How LangCache Works

LangCache moves the cache outside the model and stores the generated response itself. The architecture is a two-call loop:

Before invoking the model, the app sends the prompt to POST /v1/caches/{cacheId}/entries/search.

LangCache generates an embedding for the prompt and runs a vector search over stored entries.

If a semantically similar entry clears the configured similarity threshold, the cached response is returned and no LLM call occurs.

On a miss, the app calls its chosen LLM as usual, then stores the prompt and new response through POST /v1/caches/{cacheId}/entries for future matches.

Embedding generation is handled by the service, with default models or bring-your-own. Cache behavior is controlled through similarity thresholds, TTLs, and eviction policies, plus adaptive controls that tune precision and recall. Built on Redis&#8217;s vector database and exposed as a REST API, it works with any LLM provider and language. Hit rates and savings are monitored from the Redis Cloud console.

&

What a Cache Hit Actually Saves

A cache hit removes the input tokens, the output tokens, and the decoding latency of an additional model call. In a demo run comparing both paths on a paraphrased question, direct inference took 2.232 seconds and consumed 514 input tokens plus 250 output tokens. LangCache returned the earlier response in 0.37 seconds with zero LLM input or output tokens, roughly 6x faster in that run.

The Redis documentation is careful about how savings accrue. On a cached response you do not pay for output tokens, while input token costs are typically offset by embedding and storage costs. The suggested estimate is:

Est. monthly savings = (Monthly output token costs) x (Cache hit rate)

With $200 of monthly LLM spend, 60% of it on output tokens, and a 50% hit rate, that works out to $60 saved per month. Redis also publishes a savings calculator for annual estimates.

Redis&#8217;s public preview announcement cited up to 15x faster responses on cache hits and up to 70% lower token usage, while the current product page states savings of up to 90%. Customer Mangoes.ai reports a 70% hit rate on its patient-care voice app, cutting LLM spend by 70% with 4x faster responses. The actual result depends on how much safe repetition exists in the traffic.

Where Semantic Caching Needs Care

Deciding which questions can safely share an answer is a production concern, not a configuration detail. A threshold set too low returns a refund policy to a customer asking about upgrades. Set too high, nearly every paraphrase goes back to the model and the cache stops paying for itself. Production setups need well-tuned thresholds, expiration policies so stale answers age out, data isolation between tenants, and monitoring for incorrect matches.

LangCache covers these with access scopes, custom filtering, TTL and eviction controls, and monitoring through Redis Cloud. Data stays on the customer&#8217;s Redis servers, and Redis states it does not access that data or use it to train models.

Key Takeaways

Prefix caching cuts prompt-processing cost; semantic caching eliminates the LLM call entirely on a hit.

LangCache is a two-call REST integration: search before the model, store after it.

Savings come mainly from avoided output tokens; the docs give the formula output cost x hit rate.

Redis claims up to 90% cost savings and up to 15x faster cache hits; a demo run showed 6x.

Thresholds, TTLs, isolation, and false-match monitoring decide whether a semantic cache is safe.

Check out redis.io/langcache and follow the API and SDK examples. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet Redis LangCache: A Managed Semantic Cache That Cuts LLM API Costs by Up to 90% and Returns Cache Hits Up to 15x Faster appeared first on MarkTechPost.