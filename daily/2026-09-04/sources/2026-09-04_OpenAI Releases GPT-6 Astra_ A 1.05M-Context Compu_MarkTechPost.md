---
publish_time: 1788470171
link: https://www.marktechpost.com/2026/09/03/openai-releases-gpt-6-astra-a-1-05m-context-computer-use-model-gated-behind-a-critical-cyber-threshold/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MarkTechPost 报道，OpenAI 发布 GPT-6 Astra，主打 1.05M token 超长上下文与计算机操作（computer use）能力。模型被置于一道"关键"网络阈值（cyber threshold）之后进行受限开放，反映厂商在开放强 agentic 能力与安全风险管控之间的权衡。文章分析了其上下文架构与开放策略。
---

# OpenAI 发布 GPT-6 Astra：1.05M 上下文的计算机操作模型，受网络阈值管控

> 原文链接：https://www.marktechpost.com/2026/09/03/openai-releases-gpt-6-astra-a-1-05m-context-computer-use-model-gated-behind-a-critical-cyber-threshold/
> 来源：MarkTechPost

Today, OpenAI released GPT-6 Astra. The company calls it its most intelligent and aligned model, and positions it primarily as a computer-use system rather than a chat model. The pitch is that Astra operates software the way a person does, across browsers, spreadsheets, desktop applications and terminals, and finishes multi-step jobs instead of describing how to do them. 

Is it deployable? Partly, and not on your own hardware. Astra is a closed, hosted model with no released weights, so self-hosting is not an option. It is live today only for organizations in OpenAI&#8217;s Trusted Access and Daybreak programs. 

What is actually new

The main change for devs is context handling. Codex previously used compaction, summarizing earlier turns once context filled up. That process discards the detail an agent later needs: why a fix failed, which tests ran, which requirement was added early. Astra instead keeps notes across context windows and searches back into earlier messages and tool output. The feature ships experimental behind a config.toml setting and becomes the Codex default in the coming weeks.

Astra can also ask the user a question while continuing work that does not depend on the answer. That removes a common agent failure where one unresolved decision stalls an entire job.

On the model page, Astra lists a 1,050,000-token context window, 128,000 max output tokens and an April 30, 2026 knowledge cutoff. Input is text and image, output is text only. reasoning.effort adds two new levels above high: xhigh and max. Tool support covers computer use, hosted shell, apply patch, skills, MCP and tool search. Fine-tuning is not supported.

The benchmark picture

OpenAI reports 72.6% on OSWorld V2-Offline against 65.7% for GPT-5.6 Sol, with average task time falling from roughly 75 minutes to 40. Anthropic reports 77.9% for Claude Fable 5.1 but says it used a different OSWorld release and should not be compared directly.

Astra scores 99.9% on ARC-AGI-3. That number was produced with a Responses API harness that retains reasoning between turns and uses compaction for long contexts, and OpenAI has previously shown those settings move ARC-AGI-3 scores substantially without changing the model. The result measures the model plus the agent system.

Other reported figures: 97.6% on FrontierMath Tier 4, 95.9% on BenchCAD Vision2Code against 84.3% for Fable 5.1, and 64.6% on Terminal-Bench Science against Anthropic&#8217;s reported 52.6%. Epoch AI notes OpenAI funded FrontierMath and has exclusive access to part of it.

Coding is the weak spot in the story. Astra scores 74.1% on DeepSWE v1.1 versus 72.7% for Sol. Meta reported 75.4% for Muse Spark 1.3 at maximum reasoning, and the public leaderboard puts Gemini 3.8 Flash and Claude Opus 5 near 74%. On a 113-task benchmark, those gaps are one or two tasks.

Cyber capability drives the access model

Astra is the first model OpenAI has designated as reaching the Critical cybersecurity threshold in its Preparedness Framework. In testing it developed exploits for hardened browsers and operating systems, and found two previously unknown V8 vulnerabilities that OpenAI says it is disclosing to maintainers.

The consequences are practical. Standard access refuses advanced cybersecurity work including exploit discovery. For API developers, a cybersecurity safety check stops a task outright rather than pausing for approval. OpenAI&#8217;s Mia Glaese warned that users outside trusted-access programs may hit slowdowns, pauses or blocks, sometimes during unrelated work.

OpenAI reports 100% on ExploitBench, an aggregate capability-coverage score rather than a pass rate, and 42.4% on ExploitGym against 30.3% for Sol, with the usual six-hour time limit removed for both.

Pricing

Astra costs $10 per million input tokens and $50 per million output, with cached input at $1.00. Requests above 272K input tokens bill at 2x input and 1.5x output for the full request. Batch and Flex run at 50%, Fast mode at 2x. Pro, Business and Enterprise users also get Astra Pro.

Key Takeaways

Astra is a computer-use model first: 72.6% OSWorld V2-Offline, task time down from ~75 to ~40 minutes.

Notes replace compaction in Codex, so long agent runs stop losing failure detail.

Coding gains are marginal: 74.1% DeepSWE v1.1 sits inside the leaderboard pack.

First model at OpenAI&#8217;s Critical cyber threshold; standard access refuses exploit work.

No open weights, $10/$50 per million tokens, 1.05M context, API and AWS in coming days.

Check out the OpenAI announcement, OpenAI on X and GPT-6 Astra model page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post OpenAI Releases GPT-6 Astra: A 1.05M-Context Computer-Use Model Gated Behind a &#8216;Critical&#8217; Cyber Threshold appeared first on MarkTechPost.