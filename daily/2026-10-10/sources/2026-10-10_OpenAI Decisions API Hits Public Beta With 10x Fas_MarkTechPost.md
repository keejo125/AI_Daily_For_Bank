---
publish_time: 1791576307
link: https://www.marktechpost.com/2026/10/09/openai-decisions-api-hits-public-beta-with-10x-faster-typed-answers/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  OpenAI在DevDay发布Decisions API公开测试版，将文本与图像转换为代码可分支的类型化答案；官方称其速度约为Responses API的10倍，仅支持gpt-6-luna，按输入计费（每百万token 0.10美元、无输出费用）。该条目为OpenAI Decisions API报道的MarkTechPost版本，与主条InfoQ报道合并呈现。
---

# OpenAI Decisions API 开放公测：类型化决策结果提速 10 倍

> 原文链接：https://www.marktechpost.com/2026/10/09/openai-decisions-api-hits-public-beta-with-10x-faster-typed-answers/
> 来源：MarkTechPost

OpenAI has released the Decisions API in public beta. It turns text and images into typed answers your code can branch on. OpenAI team states the OpenAI Decisions API runs about 10x faster than the Responses API. It targets a common pattern: prompt an LLM, then parse its text into a label.

TL;DR

Size: GPT-6 Luna parameter count is not disclosed. Its model card lists a 1,050,000-token context window.

Runs on: OpenAI-hosted API only, via POST /v1/decisions. No open weights, no self-hosting.

Performance: About 10x faster than the Responses API, per OpenAI.

Best: $0.10 per 1M input tokens, with no output, cache-read or cache-write charges.

Bottom line: 

Best: fast, typed decisions with probabilities. 

Worst: 1 model, beta status, no independent evals yet.

What is the OpenAI Decisions API?

The Decisions API is an OpenAI endpoint that evaluates text, images or both and returns typed answers. It does not generate prose. A request has 3 fields: model, input and questions. The only supported model today is gpt-6-luna. OpenAI expects general availability in the coming weeks.

How does the Decisions API work?

Each request carries shared evidence plus a list of questions. Each question has a unique name, a type and instructions. The response returns an answers array keyed by those names.

What are the 3 question types?

predicate: checks a condition and returns a probability from 0 to 1. Example: does a product photo show a crack, tear or dent?

choice: picks 1 value from options you supply. It also returns per-option probabilities and a confidence field.

score: rates input against ordered levels, indexed from 0. The score is a probability-weighted average of level indices.

OpenAI&#8217;s severity example makes the math concrete. Level probabilities of 0.1, 0.7 and 0.2 yield a score of 1.1. That value sits between &#8216;Workaround available&#8217; and &#8216;Fully blocked&#8217;.

When should you use Structured Outputs instead?

OpenAI draws a clear line. Use Decisions for probabilities, choices or scores. Use Structured Outputs to fill your own JSON schema or write explanations. Use function calling when a model must request a tool call with arguments.

How fast is it, and what is the evidence?

OpenAI&#8217;s document claims about 10x faster responses than the Responses API. DevDay coverage put a decision near 150 ms, versus about 1.6 seconds for regular Luna calls. OpenAI has not published accuracy or calibration data for the endpoint. The docs advise setting thresholds with labeled examples from your own application.

&&

How much does it cost, and where can you deploy it?

With gpt-6-luna, input costs $0.10 per 1M tokens. There are no output-token, cache-read or cache-write charges. Regional processing premiums and long-context multipliers still apply. Luna&#8217;s model card prices prompts above 272K tokens at 2x input rates.

Endpoint: POST /v1/decisions on the OpenAI API, plus a Playground.

SDK minimums: Python 3.26.0, JavaScript 7.30.0, Go 3.73.0, Ruby 0.101.0, Java 4.78.0.

Compliance: Zero Data Retention and HIPAA for eligible customers.

Residency: United States and Europe (EEA plus Switzerland).

Voice: decisions can drive actions via client delegation with the Live API.

How does it compare with TypeSafe Jev?

The closest rival is TypeSafe Jev, launched September 15, 2026. Jev is a System One model that returns typed values with calibrated probabilities. TypeSafe prices input at $0.042 per 1M tokens, with free output. That makes OpenAI&#8217;s base rate about 2.4x higher. TypeSafe reports 70 to 500 ms end-to-end, measured from the US West Coast. Jev supports up to 255 choices but remains in early access. OpenAI&#8217;s edge is image input, compliance options and open beta access.

FeatureOpenAI Decisions APITypeSafe Jev 1.13GPT-6 Luna via Responses APIReleaseBeta, Oct 6, 2026Early access, Sep 15, 2026GA, Sep 22, 2026Underlying modelgpt-6-lunaJev (System One model)gpt-6-lunaParametersNot disclosedNot disclosedNot disclosedInputText, images (inline base64)Text and structured stateText, imagesOutputProbability, choice or scoreTyped values with probabilitiesGenerated text (JSON via Structured Outputs)Max options per questionNot disclosedUp to 255Not applicableSpeed (vendor-stated)About 10x faster than Responses API70 to 500 ms end-to-endBaselineInput price per 1M tokens$0.10$0.042$0.10Output price per 1M tokens$0$0$0.50ComplianceZDR, HIPAA (eligible); US and EU residencyNot disclosedEU data residency available

Key Takeaways

OpenAI Decisions API returns probabilities, choices and scores, not prose.

Input costs $0.10 per 1M tokens; output is free.

OpenAI claims about 10x faster than the Responses API.

TypeSafe Jev is cheaper at $0.042 per 1M input tokens.

Check out the Technical details here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post OpenAI Decisions API Hits Public Beta With 10x Faster Typed Answers appeared first on MarkTechPost.