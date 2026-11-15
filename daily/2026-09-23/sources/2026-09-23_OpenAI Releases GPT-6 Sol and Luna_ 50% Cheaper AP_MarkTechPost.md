---
publish_time: 1790140716
link: https://www.marktechpost.com/2026/09/22/openai-releases-gpt-6-sol-and-luna-50-cheaper-api-pricing-and-benchmarks/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  OpenAI 发布 GPT-6 Sol 与 GPT-6 Luna 两款新模型，位于本月稍早发布的 GPT-6 Astra 之下。两者采用与 Astra 相似的训练方法，通过缓存与推理效率优化降低成本，API 价格较 GPT-5.6 促销价下调 50%，已以 gpt-6-sol、gpt-6-luna 名称上线 API，无权重可供自托管。
---

# OpenAI 发布 GPT-6 Sol 与 Luna：API 价格下调 50%

> 原文链接：https://www.marktechpost.com/2026/09/22/openai-releases-gpt-6-sol-and-luna-50-cheaper-api-pricing-and-benchmarks/
> 来源：MarkTechPost

OpenAI has released GPT-6 Sol and GPT-6 Luna, 2 new models in its GPT-6 family. They sit below GPT-6 Astra, which launched earlier this month. OpenAI trained both with methods similar to Astra&#8217;s. The aim is to bring Astra&#8217;s advances to faster, more affordable models.

Deployable today? Yes. Both models are live in the OpenAI API as gpt-6-sol and gpt-6-luna. They are API-only models, so there are no weights to self-host.

Three tiers, one recipe

The GPT-6 family now has 3 tiers. Astra is the top model for the hardest work. Sol targets complex coding and professional tasks at lower cost. Luna targets fast, high-volume everyday work.

OpenAI team states better caching and inference let it serve these models more cheaply. It is cutting Sol and Luna API prices by 50% against their GPT-5.6 promotional pricing.

ModelInput (per 1M tokens)Output (per 1M tokens)GPT-6 Astra$10.00$50.00GPT-6 Sol$2.00 (was $4)$10.00 (was $20)GPT-6 Luna$0.10 (was $0.20)$0.50 (was $1.20)

One detail is worth noting. Luna&#8217;s output price falls from $1.20 to $0.50, a cut of about 58%, not 50%.

Benchmarks: what OpenAI reports

Professional work: On AutomationBench 1.0.6, Sol at xhigh effort scores 33.2% at $0.27 per task. Claude Opus 5 at max effort scores 26.9% at 11.1x that cost. Low-effort Astra scores 30.3% at 3.9x Sol&#8217;s cost. Luna at high effort gains 5.4 points over its predecessor at 58% lower cost per task.

On Agents&#8217; Last Exam, Sol at max effort scores 56.4%. That beats Claude Opus 5&#8217;s best score at 60% lower cost per task.

Coding: On DeepSWE v1.1, Sol at max effort scores 68.8%. That is 1.1 points behind Claude Fable 5 at xhigh, at about 80% lower cost per task. Luna at max effort scores 66.6%, comparable to Opus 5 and Fable 5 at medium effort. In those comparisons, Luna costs 93% less per task than Opus 5 and 96% less than Fable 5.

On FrontierCode 1.1 Main, which grades whether code is ready to merge, Sol matches Claude Fable 5.1 at xhigh at much lower cost.

Computer use: On OSWorld 2.0 offline, Sol at xhigh scores 60.5% versus 60.3% for Opus 5 at medium. Sol&#8217;s cost per task is about 80% lower. Luna at max beats GPT-5.6 Sol at medium for 1/10 of the cost.

Factuality: OpenAI&#8217;s internal test uses de-identified ChatGPT conversations where users flagged model errors. Sol makes about half as many mistakes as its predecessor. Luna at higher effort matches GPT-5.6 Sol at about 1/100 of its cost.

OpenAI also carried Astra&#8217;s communication style over. Expect clearer, slightly shorter answers with less jargon, especially in coding conversations.

Prompt caching for long-running agents

Agents resend the same instructions, tools and history on every turn. GPT-6 ships an improved prompt caching system with higher cache hit rates by default. Cached input reads get discounts of up to 90%. Eligible shared prefixes reused within a 30-minute window now qualify.

New controls for developers:

A Prompt Caching Dashboard tracks hit rates over time.

A diagnostics tool explains misses, for example "reason": "tools_changed".

Explicit breakpoints let you choose where a cached prefix ends.

Reasoning effort can change mid-conversation via configuration_update without breaking cache.

allowed_tools restricts callable tools while keeping definitions stable.

Prewarming prepares known context before the first user request.

The full prompt caching guide covers each pattern. GitHub reports these changes cut the share of prompt tokens needing fresh processing by more than 50%, helping Copilot respond faster.

Availability

API: gpt-6-sol and gpt-6-luna.

ChatGPT Work and Codex: Plus, Pro, Business, Enterprise and Edu users.

Free and Go: Luna in the ChatGPT desktop app.

Not yet in Chat. The ChatGPT rollout is gradual through launch day.

Interactive Explainer

&&&

Key Takeaways

Sol costs $2/$10 and Luna $0.10/$0.50 per 1M tokens.

Sol at xhigh beats Opus 5 max on AutomationBench at 9% of the cost.

Luna scores 66.6% on DeepSWE v1.1, costing 93% less per task than Opus 5.

Cached input reads get up to 90% off, with new cache controls.

Both are live in the API, ChatGPT Work and Codex; not yet in Chat.

Check out the Technical Blog. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post OpenAI Releases GPT-6 Sol and Luna: 50% Cheaper API Pricing and Benchmarks appeared first on MarkTechPost.