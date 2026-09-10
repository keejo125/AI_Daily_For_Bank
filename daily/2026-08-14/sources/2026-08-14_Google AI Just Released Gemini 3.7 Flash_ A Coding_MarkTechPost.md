---
publish_time: 1786643261
link: https://www.marktechpost.com/2026/08/13/google-ai-just-released-gemini-3-7-flash/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google DeepMind于8月13日发布Gemini 3.7 Flash，定位为迄今最智能的“workhorse”（主力）编码与Agent模型，距3.6 Flash仅三周，源于开发者反馈与算法创新。编码显著进步：FrontierCode 1.1 Main 43.6% vs 34.4%，DeepSWE v1.1 65.3% vs 49.0%；Web开发WebDev Arena Elo 1588 vs 1538。知识密集领域同步提升：GDP.pdf（复杂文档处理）34.0% vs 22.0%，AutomationBench（真实业务工作流）30.4% vs 17.0%。开发者体验改善：更好适应障碍、澄清意图、更谨密地做多步规划与工具调用，减少人工监督与重试。价格方面，年内 introductory 价为$0.75/百万输入token、$3.75/百万输出token，为3.6 Flash原价一半。Gemini Spark（160+国Pro/Ultra订阅）即日起换用该模型，提升Workspace工具调用与多技能工作流质量。安全上更新CBRN与网络进攻防护。开发者可通过Gemini API、AI Studio、Antigravity及Gemini Enterprise等渠道使用。
---
# Google AI Just Released Gemini 3.7 Flash: A Coding and Agent Model at $0.75/1M Input Tokens

> 原文链接：https://www.marktechpost.com/2026/08/13/google-ai-just-released-gemini-3-7-flash/
> 来源：MarkTechPost

Google has released Gemini 3.7 Flash, the newest model in its Flash tier, three weeks after Gemini 3.6 Flash. The model card describes it as a refinement of 3.6 Flash with algorithmic improvements to the core reasoning foundation — not a new pretraining run. It accepts text, images, audio, and video across a 1M-token context window, returns up to 64K output tokens, and supports customizable thinking configurations that trade quality against cost and latency. The knowledge cutoff stays at March 2026. The gains concentrate in three places: software engineering, document-heavy knowledge work, and web development. The sharper argument is price. Gemini 3.7 Flash ships at $0.75 per 1M input tokens and $3.75 per 1M output tokens — half the original 3.6 Flash list rate, and roughly a third the blended cost of Claude Sonnet 5 or GPT-5.6 Terra.

Is it Deployable?

Yes, API and enterprise only. There are no open weights. Access runs through hosted surfaces: the Gemini API and Google AI Studio, Google Antigravity, Android Studio, the Gemini Enterprise Agent Platform, and the Gemini Enterprise app. Consumers reach it through Gemini Spark on Google AI Pro and Ultra plans.

Company fit: Startups and mid-market teams gain the most, because the introductory price makes always-on agents affordable without a Pro-tier budget. Regulated enterprises get a governed path through Gemini Enterprise. Teams with data-residency or air-gap requirements are excluded — there is nothing to self-host.

Industries: Google&#8217;s own eval set points at legal, financial services, biosciences, and enterprise operations. The Harvey LAB-AA, GDP.pdf, and AutomationBench results are the tells.

Applications: Long-running coding agents, document-heavy back-office automation, UI generation from screenshots or design systems, and PDF-to-structured-data pipelines.

The Benchmark Picture

On FrontierCode 1.1 Main, which measures production code quality, Gemini 3.7 Flash scores 43.6% against 34.4% for 3.6 Flash. On DeepSWE v1.1, a long-horizon software engineering eval, it reaches 65.3%. On WebDev Arena it posts an Elo of 1588 versus 1538, the top score in Google&#8217;s comparison table.

Document and workflow results move further. GDP.pdf, an expert PDF comprehension eval, goes from 22.0% to 34.0%. AutomationBench, a private enterprise workflow set, goes from 17.0% to 30.4% — ahead of both Claude Sonnet 5 at 10.7% and GPT-5.6 Terra at 23.6%. Long-context retrieval on GDM-MRCR v2 at 128k reaches 97.0%.

GPT-5.6 Terra is ahead on DeepSWE (69.6%), Terminal-bench 2.1 (87.4%), Terminal-bench 3.0 (20.8%), and OSWorld-2.0 (50.2%). On GDPval-AA v2 knowledge work, 3.7 Flash scores 1525 Elo against 1598 for Sonnet 5 and 1628 for Muse Spark 1.2. CharXiv Reasoning is a regression: 84.5% without tools, down from 85.2% for 3.6 Flash. On the Artificial Analysis Intelligence Index, 3.7 Flash scores 56, against 57 for both GPT-5.6 Terra and Muse Spark 1.2.

&&

Pricing is the real argument

Gemini 3.7 Flash lists at $0.75 per 1M input tokens and $3.75 per 1M output tokens. That rate is introductory and expires December 31, 2026; from January 1, 2027 it becomes $1.50 and $7.50. In Google's own table, Claude Sonnet 5 sits at $2.00/$10.00 and GPT-5.6 Terra at $2.00/$12.00.

At an 80/20 input-output mix, that is a blended $1.35 per 1M tokens today against $3.60 for Sonnet 5 and $4.00 for GPT-5.6 Terra. For teams running agents at volume, the intelligence-per-dollar gap is the reason to evaluate, not the individual eval wins.

Key Takeaways

Gemini 3.7 Flash is a refinement of 3.6 Flash, not a new base model, shipped just three weeks later.

Coding gains are real: FrontierCode 43.6% vs 34.4%, DeepSWE 65.3% vs 48.6%, WebDev Arena 1588 Elo.

Price is the strongest claim — $0.75/$3.75 per 1M until December 31, 2026, then it doubles.

GPT-5.6 Terra still leads on terminal and computer-use agents; CharXiv is a small regression.

API and enterprise only. No open weights, so no self-hosting or air-gapped deployment.

Check out the Technical Details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google AI Just Released Gemini 3.7 Flash: A Coding and Agent Model at $0.75/1M Input Tokens appeared first on MarkTechPost.