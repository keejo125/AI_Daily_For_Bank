---
publish_time: 1788464819
link: https://www.marktechpost.com/2026/09/03/anthropic-released-claude-commerce-agents-an-apache-2-0-blueprint-for-shopping-and-merchant-agents-across-retail-travel-telecom-and-entertainment/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Anthropic 发布 Claude Commerce Agents 开源蓝图（Apache-2.0），为零售、旅游、电信与娱乐等场景的购物与商家智能体提供可复用的脚手架。该蓝图抽象了订单、支付与对话等通用模块，帮助团队避免重复搭建，加速客服、导购与履约类 agent 的落地。
---

# Anthropic 发布 Claude 商业智能体：覆盖零售、旅游、电信与娱乐的开源蓝图

> 原文链接：https://www.marktechpost.com/2026/09/03/anthropic-released-claude-commerce-agents-an-apache-2-0-blueprint-for-shopping-and-merchant-agents-across-retail-travel-telecom-and-entertainment/
> 来源：MarkTechPost

Most teams building a shopping assistant or agent rebuild the same scaffolding: an agent loop, a tool layer over the catalog, an approval gate, and an eval suite. Anthropic has now released that scaffolding as code. This week, they published anthropics/commerce-agents, a reference blueprint containing a shopping agent and a merchant agent, along with four runnable verticals: retail, travel, telecom and entertainment. It ships alongside two write-ups: a product announcement and an engineering deep-dive, A guide to the anatomy of effective commerce agents.

Is it deployable? Yes. The repository is Apache 2.0, runs locally on Python 3.11+ and Node 22 with an ANTHROPIC_API_KEY, and the runtimes accept any anthropic client, so the same code deploys on the Claude API, Amazon Bedrock, Microsoft Foundry or Google Cloud Vertex AI. 

The two agents

The shopping agent lives inside a merchant&#8217;s own app. It searches the catalog, handles multi-item requests, compares options, builds the cart, and answers order and returns questions in the same conversation. Its five skills are search-discovery, purchase-research, planning-goals, customer-care and memory-personalization. A deployment implements a StorefrontBackend over its catalog, cart, order and policy systems.

The merchant agent supports store staff: sales performance questions, inventory alerts, pricing and promotion recommendations, and campaign drafts. Its skills are performance-insights, catalog-listings, inventory-operations, pricing-promotions and marketing-campaigns, over a MerchantBackend.

Both run three ways — the Messages API, the Claude Agent SDK, and Claude Managed Agents (beta) — from one definition of prompts, skills, tool contracts and gates. A Claude Code plugin, commerce-builder, scaffolds a new agent (/scaffold-commerce-agent) or reviews an existing one (/review-commerce-agent).

Skills, not subagents

The architectural claim is the most transferable part. Anthropic argues against an intent router and against one subagent per domain. A commerce session is one tightly coupled conversation, and every handoff is state-lossy: the orchestrator holds the cart, preferences and history, and each handoff can cost several times the tokens and add seconds of latency. Domains also overlap, a returns flow needs order history, the cart and the catalog at once.

Agent skills give the same modularity without that tax, because skill instructions load into the agent that already holds the history. Across several enterprise deployments, Anthropic reports a single agent with skills beat both the one-big-prompt design and the subagent design on quality, often at lower cost and latency. Subagents still earn a place for narrow, self-contained work such as deep research.

The prompt-versus-skill split is decided by frequency: roughly a third or more of traffic goes in the system prompt, the rest into skills. Safety rules, brand constraints and key user facts always go in the prompt.

UI components are tools

Most commerce responses are components, not prose. Rather than prompting the model to emit custom tags, the blueprint makes each component a tool — present_products, present_itinerary, present_plan_comparison — with typed arguments the server validates before the client renders. Because those calls sit in the messages array natively, reloading history needs no custom parser, and the agent can resolve &#8220;the first hotel&#8221; from the last presentation call. For token-level streaming, eager_input_streaming: true skips server-side buffering and its schema guarantee.

Explainer: the five decisions, interactive

&

Latency, caching, memory

A rendered response runs 500–700 output tokens, which without streaming is five seconds of spinner. Anthropic separates end-to-end latency from perceived latency, streaming components as they form and rendering plain-language progress lines. Eager tool dispatch — executing each call as its arguments finish streaming, the Agent SDK default — reportedly cuts multi-second gaps to a few hundred milliseconds.

Prompt caching is the main cost lever. Requests are ordered global → session → volatile, since caching is prefix-based and a timestamp at the top of the system prompt breaks the cache on every request. Cached reads cost a tenth of fresh tokens, cache writes carry a ~1.25x premium, and the best deployments run at 90–99% hit rates. Memory extraction runs asynchronously in a separate process; Anthropic measured 13% higher fact recall than an in-turn save tool.

Key Takeaways

Apache 2.0 blueprint with shopping and merchant agents, four verticals, and a Claude Code plugin.

One agent loop plus skills outperformed subagent and single-prompt designs in Anthropic&#8217;s deployments.

UI components ship as typed tools, so history stays native and layout is resolvable.

Prompt caching targets 90–99% hit rates; volatile data belongs last, never first.

Money, writes and IDs are gated in code — the model proposes, the harness applies.

Check out the Anthropic engineering deep-dive, Product announcement, GitHub repository and Commerce demos. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Anthropic Released Claude Commerce Agents: An Apache-2.0 Blueprint for Shopping and Merchant Agents Across Retail, Travel, Telecom and Entertainment appeared first on MarkTechPost.