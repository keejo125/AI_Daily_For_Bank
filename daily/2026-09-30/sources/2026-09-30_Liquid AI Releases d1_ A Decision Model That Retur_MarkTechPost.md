---
publish_time: 1790718429
link: https://www.marktechpost.com/2026/09/29/liquid-ai-releases-d1-a-decision-model-that-returns-calibrated-probabilities-with-zero-output-tokens/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Liquid AI发布d1，一款面向结构化决策而非文本生成的决策模型。给定上下文与一组类型化问题，d1在单次调用中返回跨固定结果集的校准概率，零生成token，目标场景是原本交由通用LLM的分类、工单路由、评分、审核、重排与LLM-as-judge。d1已作为托管API（模型名d1:free）上线，仅API、不可训练，无GGUF/MLX/ONNX权重可自托管。
---

# Liquid AI 发布 d1：零输出 token 的校准概率决策模型

> 原文链接：https://www.marktechpost.com/2026/09/29/liquid-ai-releases-d1-a-decision-model-that-returns-calibrated-probabilities-with-zero-output-tokens/
> 来源：MarkTechPost

Liquid AI has released d1, a decision model built for structured choices instead of text generation. You give it context and a set of typed questions. It returns calibrated probabilities across a fixed set of outcomes in a single call, with zero generated tokens. The target is the work many teams still send to general LLMs: classification, ticket routing, scoring, moderation, reranking and LLM-as-judge checks. 

Is it deployable? Yes, today, as a hosted API. d1 runs on the Liquid API under the model name d1:free. Liquid&#8217;s model library lists it as API only and not trainable, so there are no GGUF, MLX or ONNX weights to self-host.

What is a Decision Model?

A decision model evaluates a situation and returns a typed answer from options you define before the call. It does not write text. In every response, usage.output_tokens is 0. Liquid AI&#8217;s migration guide gives a simple rule: if the answer is one of N known options, use a decision model. If the model must compose a new string, keep your LLM.

The 3 Primitives: Noul, Choice and Score

Noul is a yes/no question that returns a probability between 0 and 1. In Liquid&#8217;s example, &#8216;Is this message a complaint?&#8217; returned 0.999.

Choice picks one option from a named set. It returns the top pick, the full distribution and a confidence value. A double-charge ticket scored 0.9997 on &#8216;billing.&#8217;

Score rates input on an ordered rubric and returns a probability-weighted position. Levels are indexed from 0, so a 4-level urgency rubric spans 0 to 3. A production outage scored 2.9995.

You can mix all 3 types in one request. The model evaluates every question against the same state in one round trip.

How a d1 API Call Works

Each request has 3 parts: the model, the state (plain text or a JSON object) and the questions. Calls go to POST https://api.liquid.ai/decisions/v1/systemone. Keys come from console.liquid.ai and start with liquid_. The clients are TypeSafe AI&#8217;s typesafe-sdk for Python and @typesafe-ai/sdk for TypeScript.

Copy CodeCopiedUse a different Browser

from typesafe_sdk import TypeSafeClient, Noul

client = TypeSafeClient(api_key=os.environ["LIQUID_API_KEY"],
                        base_url="https://api.liquid.ai")
result = client.system_one(
    model="d1:free",
    state="I have been waiting over three weeks for my order...",
    questions={"is_complaint": Noul(
        instructions="Is this message a complaint from the customer?")},
)
print(result.answers["is_complaint"].noul)  # 0.999

Why Move LLM Classification Calls to d1

The migration guide lists the concrete differences against an LLM with structured output:

No billed output tokens: An LLM bills output even for a one-word label.

Predictable latency: There is no decoding loop that grows with output length.

No schema errors: Answers always match the question type, so malformed JSON and retries go away.

Usable uncertainty: You get calibrated probabilities instead of a self-reported number.

Fewer round trips: 3 sequential classification calls become 1.

Probabilities make thresholds practical. Liquid&#8217;s moderation example blocks above 0.8, allows below 0.2 and sends the middle band to human review. Its routing example falls back to the most capable model tier when router confidence drops below 0.5. Liquid also says repeated evaluations of the same input are more consistent, which reduces verdict flips.

Keep an LLM for summarization, drafting, multi-turn chat, code generation and complex multi-step reasoning.

Demo: Road Decider

Liquid&#8217;s road-decider cookbook is a pixel-art survival racer. d1 uses a Choice question to pick left, center or right on every decision tick, about 2 to 5 times per second depending on game speed. The app is vanilla JavaScript on Node.js 18+, with a Vite proxy that keeps the API key server-side. A &#8220;Jev vs d1&#8221; mode races d1 against TypeSafe&#8217;s typesafe/jev-1.13 through OpenRouter. The most useful lesson is about state design. Per-lane summaries with distance to the first obstacle produced more confident decisions than a raw grid of the road.

Interactive Explainer: d1 Step by Step

&

d1 vs Closest Competitors

d1 enters a small but fast-moving category of non-generative decision models. Here is how it compares on published features.

FeatureLiquid AI d1TypeSafe Jev 1.13Convai LayaAutoTrust JEV-27BAccessLiquid API onlyOpenRouter APIOpen weightsOpen weightsPrimitivesNoul, Choice, ScoreNoul, Choice, ScoreNoul, Choice, ScoreTrue/false, Choice (2 to 16), Score (0 to 5)Output tokens00 (output billed at $0)0 (encoder)0 for decisions; can also generate textContext windowNot published32K tokens512 (English), 1,024 (multilingual)4,096 tokensModel sizeNot disclosedNot disclosed421M (English), 322M (multilingual)27B backbone, 108.9M trainablePricingd1:free tier; paid rates not published$0.042 per 1M input tokensSelf-hostedSelf-hostedLicenseHosted APIHosted APIApache 2.0Apache 2.0Fine-tuningNot trainableNot documentedYesYes (LoRA adapter)SDKTypeSafe SDK (Python, TS)TypeSafe SDK, OpenRouter SDKsHugging FaceHugging Face

Data checked September 29, 2026 against each vendor&#8217;s primary page.

Key Takeaways

d1 returns typed decisions with calibrated probabilities and 0 output tokens.

3 primitives cover most bounded tasks: Noul, Choice and Score.

Deployable now through the Liquid API as d1:free; no self-hosted weights.

Best fit: routing, moderation, triage, reranking and LLM-as-judge replacement.

Keep LLMs for generation, conversation and multi-step reasoning.

Check out the Decision Models docs, the Migration Guide and the Road Decider demo. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Liquid AI Releases d1: A Decision Model That Returns Calibrated Probabilities With Zero Output Tokens appeared first on MarkTechPost.