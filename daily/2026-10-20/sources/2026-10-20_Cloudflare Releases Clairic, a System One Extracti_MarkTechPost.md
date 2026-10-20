---
publish_time: 1792482341
link: https://www.marktechpost.com/2026/10/20/cloudflare-releases-clairic-a-system-one-extraction-model-on-workers-ai/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cloudflare 在 Workers AI 上预览 Clairic 结构化抽取模型：读取文本或图像并返回类型化字段值，而非生成自由文本，直击开发者通常用 LLM 完成的"抽取总额、日期、ID 进 JSON"任务。Clairic 对每请求字段一次性前向输出，无需推理与输出 Token。其上下文窗口 65536 Token、单请求最多 4 张图，以 Cloudflare 托管 GPU 运行。对 Agent 与数据管线，这是一种低成本、确定性的结构化抽取替代方案。
---

# Cloudflare 发布 Clairic 结构化抽取模型（Workers AI）

> 原文链接：https://www.marktechpost.com/2026/10/20/cloudflare-releases-clairic-a-system-one-extraction-model-on-workers-ai/
> 来源：MarkTechPost

Cloudflare has released a preview of Clairic, a new System One extraction model on Workers AI. The Cloudflare Clairic extraction model reads text or images and returns typed values, not generated text. It targets a job developers usually give to LLMs: pulling totals, dates and IDs into JSON. Clairic answers every requested field in 1 forward pass, with no reasoning and no output tokens. 

TL;DR

Size: Parameter count not disclosed. 65,536-token context window, up to 4 images per request.

Runs on: Cloudflare-hosted GPUs via Workers AI (@cf/cloudflare/clairic). No local option until weights ship.

Performance: Sub-second extraction in Cloudflare&#8217;s tests. No standard accuracy benchmark is published yet.

Best: Extraction step took 0.46 s vs 16.1 s for GLM-5.3 in Cloudflare&#8217;s claims pipeline.

Worst: 4 of 21 TSA next-day forecasts fell outside its 80% interval. Multi-step arithmetic is unreliable.

What is Clairic?

Clairic is a Cloudflare model that extracts, computes, estimates and forecasts typed values from unstructured inputs. It builds on the System One idea from TypeSafe&#8217;s Jev, named for Kahneman&#8217;s fast, intuitive thinking.

Jev and Cloudflare&#8217;s own Clef are decision models. They score options you list in advance. Clairic covers answers you cannot list, such as an invoice total, a date or a repair cost.

Cloudflare frames a 3-part stack. Extraction models turn raw input into typed values. Decision models turn values into decisions. LLMs turn decisions into words.

How does a Clairic request work?

A request has a state (text plus up to 4 images) and a map of named, typed fields. Each field can carry plain-language instructions. Supported types are text, number, date, time, datetime, duration, list, estimate and forecast, per the Workers AI changelog.

Every scalar answer includes p_null, the probability that the value is absent, plus a confidence score. Text answers return exact spans with character offsets. Estimates and forecasts return a median and an 80% interval, from p10 to p90. Forecasts cover up to 64 steps.

There is no field limit. Fields that do not fit beside the input in one 8,192-token pass split into parallel passes. Each pass sees the whole input. In the docs example, a 61-token invoice ran in 3 passes. It billed 655 input tokens, including 472 schema tokens. Wide schemas can cost more than the document itself.

What did Cloudflare&#8217;s tests show?

In a support-email example, Clairic added price and tax into $701.10. It also computed 11 days since delivery. Neither number appears in the email. A missing tracking number returned null instead of a plausible guess.

On a skewed receipt photo, it read all 7 present values and returned null for the absent discount. Its lowest confidence was 0.776, on the order number.

For forecasting, Cloudflare predicted daily TSA checkpoint counts for 21 days. Average error was 3.3%. 17 of 21 actual counts fell inside the 80% interval. 3 of the 4 misses fell on Columbus Day weekend.

The main test is a damaged-product claims pipeline. Clairic extracted facts, Clef chose refund or repair, and GLM-5.3 wrote the reply. Cloudflare compared this against GLM-5.3 handling all 3 steps.

&&&

The cascade finished in 19.3 s versus 61.7 s, about 3.2x faster. Extraction took 0.46 s against 16.1 s. The decision step took 0.22 s against 21.9 s. Cost per million claims fell 49%, from $11,740 to $6,032. The reply step still dominated, at 18.6 of the 19.3 s.

Both pipelines got the facts and decision right. Clairic&#8217;s repair estimate was identical across runs. GLM-5.3 returned $250, $250 and $220. Cloudflare says Gemma 4 and Qwen failed the all-LLM version.

How does Clairic compare with Clef, Jev and GLM-5.3?

MetricsClairicClefJevGLM-5.3 DeveloperCloudflareCloudflareTypeSafe AIZ.aiClassSystem One extractionSystem One decisionSystem One decisionSystem Two LLM (reasoning)OutputTyped values: spans, numbers, dates, durations, lists, estimates, forecastsProbabilities over options you listTyped decisions with calibrated probabilitiesFree-form textParametersNot disclosed27BNot disclosedNot disclosedContext window65,536 tokens65,536 tokensNot disclosed1,048,576 tokensImage inputYes, up to 4Yes (text, JSON, images, video)Not disclosedNot disclosedInput price$0.10 / M tokens$0.24 / M tokens$0.042 / M tokens$1.40 / M tokensOutput priceNoneNoneFree$4.40 / M tokensSpeed0.46 s extraction step (Cloudflare test)209.3 ms median (Cloudflare evals)70 to 500 ms end to end (TypeSafe)16.1 s extraction step (Cloudflare test)AvailabilityWorkers AI preview; open weights plannedWorkers AI; Apache 2.0 weightsTypeSafe API, early accessWorkers AI, Paid plan

Where can developers use it, and what does it cost?

Clairic is live as a preview at @cf/cloudflare/clairic. Call it through the Workers AI binding with env.AI.run() or the REST API. AI Gateway works with the same endpoints.

Pricing is $0.10 per million input tokens with no output charge. That undercuts Clef&#8217;s $0.24 but sits above Jev&#8217;s $0.042. Weights are promised but not yet released.

Key Takeaways

Clairic returns typed values, not text, in 1 forward pass.

$0.10 per million input tokens; output tokens cost nothing.

Extraction ran in 0.46 s vs 16.1 s for GLM-5.3.

Every answer carries confidence, p_null, spans or intervals.

Check out the Cloudflare blog post, the Clairic model docs, the extraction models explainer and the Workers AI changelog. Also read our earlier coverage of Drex 1.5. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Cloudflare Releases Clairic, a System One Extraction Model on Workers AI appeared first on MarkTechPost.