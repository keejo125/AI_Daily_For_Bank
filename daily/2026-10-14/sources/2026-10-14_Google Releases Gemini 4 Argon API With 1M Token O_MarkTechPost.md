---
publish_time: 1791954214
link: https://www.marktechpost.com/2026/10/13/google-gemini-4-argon-api-release/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MarkTechPost报道Gemini 4 Argon正式GA，开发者与企业可用。该稀疏MoE前沿模型专为长链路、多步骤工作设计，覆盖编码、金融、法律、科学与网安，输入2美元、输出10美元/百万token，关键变化是单次响应可输出多达100万token。性能上长视频理解LVBench达91.7%领先，但FrontierSWE v2仅55.0%居末。
---

# Gemini 4 Argon API开放：输出上限100万token

> 原文链接：https://www.marktechpost.com/2026/10/13/google-gemini-4-argon-api-release/
> 来源：MarkTechPost

Google DeepMind has made Gemini 4 Argon generally available to developers, enterprises and paid Gemini subscribers. Gemini 4 Argon is a sparse mixture-of-experts frontier model from Google built for long, multi-step work. Its target domains are coding, finance, legal, science and cybersecurity. Google first announced Argon on September 30 for a small group of cyber defenders. It now reaches the paid Gemini API at $2 input and $10 output per million tokens. The key change for developers is output length: Argon can write up to 1M tokens in one response.

TL;DR

Size: Parameter count not disclosed (sparse MoE). 1M token window shared by input and output.

Runs on: Google&#8217;s cloud only, via Gemini API, AI Studio and Gemini platform. Trained on TPUs. No open weights.

Performance: Leads Google&#8217;s table on knowledge work, long context and video. Mixed on agentic coding.

Best: 91.7% on LVBench (long video understanding).

Worst: 55.0% on FrontierSWE v2, last of 4 models in Google&#8217;s table.

What is Gemini 4 Argon?

According to the model card, Argon is a new model, not a fine-tune of an earlier Gemini. It is a large-scale sparse MoE transformer with native multimodal support. It accepts text, images, audio and video, and it outputs text. Google trained it on TPUs using JAX and ML Pathways. The knowledge cutoff is March 2026. Google has not disclosed total or active parameter counts.

How does the 1M token output limit work?

Google raised the output limit to 1M tokens, up from 64K on earlier Gemini models. The model card describes a combined input plus output window of up to 1M tokens. So a long prompt reduces the room left for output. Google documents a new continuation protocol for long decodes in its developer docs and enterprise docs. At introductory pricing, a full 1M token response costs $10 in output tokens.

How does Gemini 4 Argon perform on benchmarks?

Google compares Argon with GPT-6 Astra, Claude Fable 5.1 and Claude Opus 5.5. Argon posts the top score on most rows.

DeepSWE v1.1: 77.9%, ahead of Opus 5.5 (74.2%) and GPT-6 Astra (74.1%).

Vals Index: 68.90%, ranked #1 by Vals AI ahead of Claude Sonnet 5.5 (67.04%).

AutomationBench: 51.3%, versus 42.5% for Opus 5.5.

Harvey&#8217;s Legal Agent Benchmark: 19.6%, nearly 3x the next model, but still a low absolute score.

GraphWalks, 256K to 1M tokens: 84.2%, versus 71.8% for GPT-6 Astra.

CWE-bench v1: 68.0%, tied with GPT-6 Astra.

Google also reports 87% on the ERQA embodied reasoning benchmark. Read the evaluation methodology before drawing conclusions. Most rival scores are self-reported or pulled from public leaderboards. Argon&#8217;s DeepSWE score is self-computed with a mini-swe-agent harness. The rival DeepSWE numbers come from system cards and a leaderboard.

Where does Gemini 4 Argon fall short?

Argon trails on 5 rows of Google&#8217;s own table:

FrontierSWE v2: 55.0%, versus 65.5% for GPT-6 Astra.

Terminal-Bench 4.0: 57.4%, versus 66.4% for Opus 5.5.

Terminal-Bench Science 0.1: 57.6%, versus 68.1% for GPT-6 Astra.

PostTrainBench: 45.3%, versus 49.3% for Opus 5.5.

OSWorld-2.0 (offline subset): 69.2%, versus 72.6% for GPT-6 Astra.

The model card also lists hallucinations and occasional slowness or timeouts. Under Google&#8217;s Frontier Safety Framework, Google says it cannot rule out the biological and cybersecurity critical capability levels. It reports deploying safeguards it assesses as lowering that risk.

Gemini 4 Argon vs GPT-6 Astra vs Claude Opus 5.5 vs Claude Fable 5.1

FeatureGemini 4 ArgonGPT-6 AstraClaude Opus 5.5Claude Fable 5.1ArchitectureSparse MoE transformerNot disclosedNot disclosedNot disclosedTotal / active paramsNot disclosedNot disclosedNot disclosedNot disclosedContext window1M (input + output combined)1,050,0001M1MMax outputUp to 1M128K128K128KInput modalitiesText, image, audio, videoText, imageText, imageText, imageKnowledge cutoffMar 2026Apr 30, 2026Jun 2026Jun 2026API price (in / out per 1M)$2 / $10 intro, $4 / $20 after Nov 30$10 / $50$4 / $20$10 / $50License / accessProprietary, API onlyProprietary, API onlyProprietary, API onlyProprietary, API onlyVals Index68.90%63.13%66.97%65.83%DeepSWE v1.1 (Google table)77.9%74.1%74.2%67.4%Terminal-Bench 4.0 (Google table)57.4%58.2%66.4%57.9%FrontierSWE v2 (Google table)55.0%65.5%62.3%56.3%

What did Google use Argon for before launch?

Google shared internal results in its launch post:

Argon in Antigravity raised agentic code submissions by over 35% and cut rollbacks by nearly a third.

It delivered a 2.85x end-to-end vLLM inference speedup for Gemma 4 E2B on an A100.

In Google&#8217;s open-source Agent Development Kit, it cut session prep time by 40%. Cold imports got 21% faster.

On Gray Swan&#8217;s indirect prompt injection benchmark, attack success fell to 0.7% across 15 adaptive attempts.

How much does Gemini 4 Argon cost, and where can you use it?

Introductory pricing is $2 input and $10 output per million tokens. Cached input tokens are 95% off. After November 30, 2026, the price rises to $4 and $20. That matches Claude Opus 5.5 and sits below GPT-6 Astra&#8217;s $10 and $50.

Access paths, per the developer post:

Developers: Gemini API paid tier in AI Studio and Android Studio.

Enterprises: Gemini platform, Gemini for business and Google Antigravity.

Consumers: Gemini app and AI Mode in Search for Google AI Pro and Ultra subscribers.

Cyber defenders: the Fairwind Program, with access to Argon without cyber guardrails.

Key Takeaways

Argon is a sparse MoE model with a 1M token output limit.

It ranks #1 on the Vals Index at 68.90%.

Intro pricing is $2/$10 per million tokens until November 30.

It trails rivals on FrontierSWE v2 and Terminal-Bench 4.0.

Most rival scores in Google&#8217;s table are self-reported.

Check out the Model Card, Evaluation Methodology and Developer Guide. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Google Releases Gemini 4 Argon API With 1M Token Output Limit appeared first on MarkTechPost.