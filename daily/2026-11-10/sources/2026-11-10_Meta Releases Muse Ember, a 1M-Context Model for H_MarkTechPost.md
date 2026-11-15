---
publish_time: 1794292570
link: https://www.marktechpost.com/2026/11/09/meta-muse-ember-small-agent-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Meta 发布最小最高效模型 Muse Ember：托管多模态推理模型，100 万上下文、最高 51.2 万输出，面向 Agent 内重复步骤（工具调用、编码子任务、路由、抽取、长文解析），AA 智能指数 36 分持平 Haiku 5.5 最高档，单任务约 0.14 美元，AutomationBench 37.8 领先，权重不开放。
---

# Meta 发布 Muse Ember 百万上下文模型

> 原文链接：https://www.marktechpost.com/2026/11/09/meta-muse-ember-small-agent-model/
> 来源：MarkTechPost

Meta Superintelligence Labs has released Muse Ember, its smallest and most efficient model. Meta Muse Ember is a hosted multimodal reasoning model built for the repetitive steps inside agents. Meta lists tool calls, coding subtasks, routing, extraction and long document parsing as targets. It scores 36 on the Artificial Analysis Intelligence Index, level with Claude Haiku 5.5 at max effort. Meta puts its cost at about $0.14 per index task.

TL;DR

Size: 1M-token context window, up to 512K output tokens.

Runs on: Meta&#8217;s hosted infrastructure only (Meta Model API and Muse Code). Weights are private, so there is no local GPU, laptop or quantized option.

Performance: Ties Claude Haiku 5.5 (max) at 36 on the AA Intelligence Index, ahead of GPT-6 Luna (28).

Best: AutomationBench-AA at 37.8, versus 20.2 for GPT-6 Luna and 13.9 for Claude Haiku 5.5.

Worst: FrontierCode 2.0-AA at 27.2, behind Claude Haiku 5.5 at 34.9.

Bottom line: Best: Haiku-level intelligence at $0.136 per task versus $0.411. Worst: closed weights and weaker on mergeable real-repo code.

What is Meta Muse Ember?

Muse Ember is a small reasoning model from Meta for high-volume agent subtasks. It is the fourth model under the Muse brand, after Spark, Glimmer and Wonder. 

Meta positions it below its larger models. Muse Wonder handles the hardest problems and Muse Spark covers coding and agentic workflows. Ember takes repeatable coding and agent tasks at scale. Meta&#8217;s own framing: Muse Wonder plans, Muse Ember handles the volume.

How does Muse Ember work?

Muse Ember is the first model Meta trained using Muse Wonder Full, its largest model.

The model natively accepts text, images, audio and video. That lets an agent read screenshots, charts, scanned pages, voice memos and meeting recordings without a separate model. It also operates desktop apps from screenshots.

The 1M-token context window fits a full codebase or document set in one call. Output runs up to 512K tokens, 4x the 128K cap on both rivals.

How does Muse Ember perform on benchmarks?

All results below are at max reasoning effort, as reported by Meta. Some come from Artificial Analysis (AA), others from Meta&#8217;s internal suite.

Agents: On AutomationBench-AA, 657 Zapier business workflows, Ember completes 37.8% of tasks. GPT-6 Luna reaches 20.2% and Claude Haiku 5.5 reaches 13.9%. On Agents&#8217; Last Exam (internal), Ember scores 61.6 versus 57.1 and 57.0.

Coding: Ember leads Terminal-Bench 4.0 with 40.9 versus Haiku&#8217;s 39.2 and Luna&#8217;s 16.4. It also leads the AA Coding Agent Index, 46 to 37 to 31. It loses FrontierCode 2.0-AA, where Haiku scores 34.9 and Ember 27.2.

Multimodal: Ember ties GPT-6 Luna on GDP.pdf-AA at 22.8. It edges Haiku on OSWorld 2.1, 69.5 versus 68.9 on partial credit. PerceptionBench with tools gives Ember 80.6, Haiku 78.6 and Luna 62.8.

&&

Why is Muse Ember cheaper per task if token prices match?

Muse Ember costs $0.10 per million input tokens and $0.50 per million output tokens. Cached input costs $0.004 per million. Claude Haiku 5.5 and GPT-6 Luna list the same base rates.

With identical list prices, the cost gap must come from tokens used per task. On Meta&#8217;s chart, Ember at max scores 35.8 for $0.136 per task. Haiku 5.5 at max scores 36.2 for $0.411. Luna&#8217;s best setting scores 27.8 for $0.152. Artificial Analysis summarised this as matching Haiku at a third of the cost per task.

Long prompts widen the gap on paper. Haiku 5.5 charges $0.50 and $2.50 above 100K prompt tokens. GPT-6 Luna doubles input rates above 272K input tokens. Meta lists no long-context tier for Ember.

Muse Ember vs Claude Haiku 5.5 vs GPT-6 Luna

FeatureMuse EmberClaude Haiku 5.5GPT-6 LunaDeveloperMetaAnthropicOpenAIReleasedNov 9, 2026Oct 7, 2026Sep 22, 2026 (source)ParametersNot disclosedNot disclosedNot disclosedContext window1M1M1.05MMax output512K128K128KInputsText, image, audio, videoText, imageText, imageWeightsClosedClosedClosedInput / output per 1M$0.10 / $0.50$0.10 / $0.50 (up to 100K prompt)$0.10 / $0.50 (up to 272K input)Cached input per 1M$0.004$0.01$0.01AA Intelligence Index (max)*363628Cost per AA task (max)*$0.136$0.411$0.152AutomationBench-AA*37.813.920.2Terminal-Bench 4.0*40.939.216.4FrontierCode 2.0-AA*27.234.925.2OSWorld 2.1 (partial / binary)*69.5 / 33.868.9 / 27.850.5 / 17.0

*Benchmark rows as published by Meta in its launch post and evaluation report, sourced from Artificial Analysis Intelligence Index v5 and Meta internal runs.

How can developers access Muse Ember?

Ember is available on the Meta Model API and in Muse Code, Meta&#8217;s coding agent. It supports the Responses API. Partners in early testing included Box, Cline, Oracle, Cloudflare and You.com.

Key Takeaways

Muse Ember ties Claude Haiku 5.5 at 36 on the AA Intelligence Index.

Same $0.10 / $0.50 token prices, about a third of Haiku&#8217;s cost per task.

Strongest on agent workflows: 37.8 on AutomationBench-AA.

Weakest on mergeable code: 27.2 on FrontierCode 2.0-AA.

Closed weights, hosted only via Meta Model API and Muse Code.

Check out the launch post and the evaluation report, or try it on dev.meta.ai.. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meta Releases Muse Ember, a 1M-Context Model for High-Volume Agent Work appeared first on MarkTechPost.