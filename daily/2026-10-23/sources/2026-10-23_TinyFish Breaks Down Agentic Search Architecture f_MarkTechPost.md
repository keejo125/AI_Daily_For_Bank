---
publish_time: 1792745927
link: https://www.marktechpost.com/2026/10/23/tinyfish-agentic-search-architecture-deep-research/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  AI 搜索智能体在演示中可用、生产负载下却常因检索证据不全、重试无效动作、超时超预算而失败。TinyFish 发布两份技术指南，定义生产级 Agentic Search 架构，并分享构建 deep research 系统的工程经验：规划检索、评估证据、处理失败、划分模型推理与确定性执行边界。
---

# TinyFish拆解生产级Agent搜索架构

> 原文链接：https://www.marktechpost.com/2026/10/23/tinyfish-agentic-search-architecture-deep-research/
> 来源：MarkTechPost

An AI search agent can work in a demo but fail under production workloads when retrieval returns incomplete evidence, retries repeat unsuccessful actions, or execution exceeds time and cost limits. TinyFish, which provides web infrastructure for AI agents, has published two technical guides addressing these challenges. The first defines a production agentic search architecture, while the second shares lessons from building a deep research system. Together, they examine how an autonomous search agent can plan retrieval, evaluate evidence, handle failures, and manage the boundary between model reasoning and deterministic execution. 

TL;DR

TinyFish introduced its agentic search architecture and key engineering lessons from building deep research systems. Built on four web primitives (TinySearch, TinyFetch, TinyBrowser, and TinyAgent), the system operates via a seven-phase control loop around the base model. On OpenBenchmarks, TinyFish achieved a 79.0% completion rate on coding tasks while delivering the lowest median task cost ($0.050) and token footprint, highlighting the importance of rigid control loops, failure-specific retries, and unified reasoning over standalone planners.

What is Agentic Search Architecture?

Agentic search architecture enables an AI agent to plan retrieval, access sources, evaluate evidence, and adapt its approach as new information becomes available. The model provides reasoning, while the surrounding application manages state, tool execution, evidence handling, runtime policies, and output validation. Together, these components allow an agent to handle incomplete results, recoverable failures, and changing information requirements.

TinyFish’s architecture draws foundational concepts from a February 2026 architecture preprint, which decouples reasoning from execution through typed tool interfaces. The paper establishes essential system guardrails, including detailed tracing alongside strict caps on tokens, execution time, overall cost, and tool invocations.

How does a production search run work?

TinyFish splits a run into 7 phases:

Define the task: Turn the goal into an &#8220;evidence contract&#8221;: required fields, sources, freshness and completion rules.

Plan retrieval: Separate independent needs from dependent ones. Dependent queries wait for earlier answers.

Pick the first route: Choose a tool based on what the system knows about the evidence.

Discover, select, retrieve: Treat search results as candidates until the page content arrives.

Evaluate: Label evidence as sufficient, incomplete, conflicting, inaccessible or budget exhausted.

Recover or escalate: Revise the query, retry, change sources or change access method.

Stop and validate: Return completed, incomplete, failed, cancelled or human review required.

Phase 2 addresses a known failure. ChainRAG (ACL 2025) calls it the ‘lost-in-retrieval’ problem, where key entities disappear during multi-hop question decomposition. Phase 6 draws on Search-R1, which demonstrates how models can learn to generate additional search queries during reasoning when earlier retrieval is insufficient. Across 7 QA datasets, its learned multi-turn search beat RAG baselines by 41% (Qwen2.5-7B) and 20% (Qwen2.5-3B).

How should a search agent route tools?

Routing should follow the information gap, not a fixed ladder.

Starting conditionPrimitiveWhat the app still ownsSource location unknownSearchQuery planning, source policy, stoppingURL known and readableFetchCompleteness checks, claim validationApp must control page actionsBrowserEvery action, retry and checkpointDecisions across several pagesWeb AgentBusiness rules, budgets, validation

Escalation is not always the fix. Weak results need a better query. Conflicting sources need stronger evidence. A heavier tool fixes neither.

Retries should be based on the failure type and remain within defined limits. Transient errors may justify repeating a request, while incomplete or conflicting evidence requires a different approach. Browser retries must also account for actions already completed to avoid unintended consequences, such as submitting the same form twice.

What did TinyFish learn building deep research?

The deep research agent searches, browses, and generates comprehensive, cited reports. Most engineering challenges centered around context management, system orchestration, and product design.

Lesson #1: Removing the separate planner

Initial iterations used a standalone planner called fresh each time. Only structured state crossed into it. On follow-up queries like &#8220;focus only on pricing risks in Southeast Asia,&#8221; the agent drifted back to broad market research. TinyFish subsequently moved planning into the orchestrator&#8217;s own unified reasoning loop.

Lesson #2: Removing subagents: 

TinyFish initially assigned a separate subagent to each search query, increasing context-switching overhead, latency, and cost. The team later replaced these subagents with tool calls for repeatable tasks such as ranking search results, classifying sources, and extracting evidence. This reduced the information passed back to the orchestrator, allowing it to focus on research planning and deciding what to investigate next.

Lesson #3- Matching researchers: 

TinyFish initially optimized its research system for source coverage, but users placed greater importance on the quality and relevance of supporting evidence. The team adjusted source ranking to account for the research objective and added controls for prioritizing, excluding, or restricting domains. It also developed an internal evaluation harness using an LLM judge to assess reports for relevance, evidence strength, citation trust, and source diversity.

How do cost and latency add up?

TinyFish budgets the full task, not single calls:

Task latency = planning + search + retrieval + evaluation + retries + interactive steps + queueing.

Task cost = tokens + tool calls + page or browser usage + retries + infrastructure.

SearchAgent-X (ICLR 2026) shows why. Exact retrieval added overhead, and coarse retrieval forced extra reasoning. Its fixes reached up to 3.4x throughput and 5x lower latency versus tested baselines.

How does TinyFish compare on search and fetch?

OpenBenchmarks fixes the model (gpt-5.6-sol), 100 tasks and budgets, and varies only the provider. Scores are means of 3 runs.

MetricTinyFishExa deepPerplexityFirecrawlSearch + fetch completion79.0% ± 2.083.0% ± 1.077.7% ± 1.576.0% ± 1.0Median task time24s37s22s34sMedian task cost$0.050$0.127$0.083$0.082Median task tokens12,84423,66020,06217,379Search-only completion59.3%66.3% (Exa fast)77.3%70.3%Search list price$0$0.012$0.005$0.005

Source: OpenBenchmarks board, updated 26 Sept 2026. Tasks cover enterprise documentation only.

OpenBenchmarks also reports search-only results separately. In that configuration, TinyFish achieved 59.3% task completion, compared with 77.3% for Perplexity, 70.3% for Firecrawl, and 66.3% for Exa Fast. These results should not be directly compared with the search-and-fetch scores because the available retrieval capabilities differ.

Key Takeaways

Control the whole trajectory, not 1 search call.

Route by information gap; escalate only when access fails.

Keep planning and execution in 1 reasoning loop.

Move deterministic steps into tool calls, not subagents.

Rank sources by research objective, not one quality score.

Read the architecture guide, the deep research lessons and the TinyFish docs.

Thanks to the Tinyfish team for the thought leadership / resources for this article. This article is sponsored by TinyFish.

The post TinyFish Breaks Down Agentic Search Architecture for Production AI Agents appeared first on MarkTechPost.