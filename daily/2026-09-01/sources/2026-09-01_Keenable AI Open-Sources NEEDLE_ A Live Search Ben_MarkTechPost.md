---
publish_time: 1788219806
link: https://www.marktechpost.com/2026/08/31/keenable-ai-open-sources-needle-a-live-search-benchmark-that-rebuilds-its-query-set-every-hour/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Keenable AI 开源实时搜索基准 NEEDLE，其核心挑战在于：被测试的搜索 API 本身可读取答案，传统静态基准易被「作弊」。NEEDLE 每小时重构查询集，使评测问题随时间变化，防止搜索 Agent 直接下载公开数据集中的标准答案、绕过真实检索。该基准面向 Web 搜索类 Agent 的能力评测，填补了「会读答案键」导致评测失真的空白，推动搜索智能体评测更贴近真实检索。
---

# Keenable AI 开源实时搜索基准 NEEDLE（每小时重构查询集）

> 原文链接：https://www.marktechpost.com/2026/08/31/keenable-ai-open-sources-needle-a-live-search-benchmark-that-rebuilds-its-query-set-every-hour/
> 来源：MarkTechPost

How do you benchmark a web search API when the thing being tested can read the answer key? A search agent has a fetch tool. If the gold labels sit in a public dataset, the agent can download them mid-evaluation and skip retrieval entirely. A similar problem arises when the answers are already encoded in the model’s parametric memory: a correct response no longer demonstrates that web search worked. Keenable&#8217;s answer is NEEDLE, a live open-source benchmark that rebuilds its query set from fresh public sources rather than freezing one. News queries are regenerated hourly from RSS feeds and Google Trends; finance, scholar, legal, and rare-entity queries are regenerated daily from SEC XBRL, arXiv, Europe PMC, CourtListener, and public agent logs. Fifteen search APIs run against the same query text under one protocol, and every score is read against ultimate, a pooled oracle engine that marks what the whole field managed to find.

Is it reproducible?

Yes, as an open source evaluation harness rather than a product. needle is a Python CLI installed with uv sync and driven by two subcommands per benchmark, generate and run. It needs an OpenRouter key for judging and one API key per engine tested, and runs on a laptop or in CI. It allows recreated all query streams that are being used in addition to the ranking quality judgements.

What NEEDLE measures

NEEDLE stands for News, Everyday, Expert, Deep-tail, and Legal Evaluation. Each vertical models a different agent intent. News projects the newest item from ~124 curated RSS feeds and Google Trends into a keyword query. Finance asks registry facts from Wikidata and GLEIF plus single-quarter 10-Q figures from SEC XBRL. Scholar turns one paper into four query styles: a degraded title, a full-text-only detail, a natural-language clue, and a hedged tip-of-the-tongue description. Deep-tail samples rare-word queries from public agent-trajectory releases including DeepResearchGym, OpenResearcher and LRAT. Legal pulls recent CourtListener opinions across 14 federal courts and eCFR sections.

Scoring splits along the same line. News and deep-tail have no single correct result, so an LLM judge rates each result 0 to 4 and the harness reports nDCG@5 with a duplicate-URL penalty. Finance reports answer-recall@5: does the fact reach the agent inside a top-5 snippet. Scholar and legal are known-item tasks scored by identifier match.

The ceiling is the interesting part

Every engine receives the same query text. The runner issues one call at a time, so latency percentiles are comparable and no engine takes concurrent load. Judging happens on the engine&#8217;s own ranking, titles and snippets. Pages are never fetched and results are never re-ranked. Evidence is clipped to 2,000 characters for everyone, and the judge does not see the engine name.

The more interesting number is the ultimate ceiling. For each query, NEEDLE pools the results returned by every engine into a synthetic oracle engine, then orders that combined set by relevance. That creates an empirical ceiling based on what the entire field was able to retrieve.

The gap to ultimate is therefore an upper bound on agentic search quality as it stands today. A large gap means better results existed but every engine failed to surface or rank them well. A weak ultimate score means something different: even after pooling every provider, the benchmark found little strong evidence. In other words, NEEDLE can distinguish a ranking problem from a retrieval problem shared by the whole market.

Where the field actually stands

Numbers below are published 7-day means for the window ending 2026-08-28.

Finance is close to solved: Exa 0.910, Keenable 0.872, Perplexity 0.871, Google 0.847, against an ultimate of 0.965. Scholar spreads out, Keenable 0.774 to Tavily 0.310 against a 0.869 ceiling, because title queries are answerable from metadata and body queries are not. Deep-tail is hardest and closest to real agent traffic: Exa leads at 0.557 of ultimate, Keenable follows at 0.470, Bing sits at 0.199. The gap between delivered and achievable quality widens as queries approach how agents actually search.

Latency is another important metric here, because agents call search dozens of times per task. Same window: Keenable-realtime 193 ms p50 / 284 ms p95, Exa 1,876 / 2,955, Bing 2,767 / 9,381.

Key Takeaways

NEEDLE regenerates queries hourly for news and daily for the other four verticals, so there is no fixed set to overfit.

Five verticals, 15 search APIs, one protocol: same query text, same 2,000-character evidence cap, one request at a time.

Every leaderboard is read against ultimate, a pooled oracle engine marking the ceiling the whole field reached.

On rare-entity queries from real agent logs the top engine reaches 0.557 of that ceiling; on finance most engines cluster between 0.77 and 0.91.

Code is MIT, runs execute in public GitHub Actions, and per-run artifacts ship to a Hugging Face dataset.

Check out the live dashboard, the GitHub repo, the technical write-up, and the archived artifacts. All credit goes to the researchers of this project.

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Keenable AI Open-Sources NEEDLE: A Live Search Benchmark That Rebuilds Its Query Set Every Hour appeared first on MarkTechPost.