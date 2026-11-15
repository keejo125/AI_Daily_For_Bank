---
publish_time: 1793105866
link: https://www.marktechpost.com/2026/10/27/mirendil-fern-10m-token-context-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  初创公司 Mirendil 发布其首款模型 Fern 0.1，支持 1000 万 Token（10M）上下文窗口，定位超长上下文理解场景，面向需要长文档与代码库分析的应用。
---

# Mirendil 发布首款模型 Fern 0.1，支持 1000 万 Token 上下文

> 原文链接：https://www.marktechpost.com/2026/10/27/mirendil-fern-10m-token-context-model/
> 来源：MarkTechPost

Mirendil has released Fern, its first AI model. Mirendil Fern is a from-scratch coding model with a context window of up to 10M tokens. Mirendil explains how that equals about 23 MB of code, or roughly half a million lines. That is a codebase on the scale of Megatron-LM, held in context at once. Fern 0.1 is the first version, built from Mirendil-Base after a short round of post-training. For developers, its like, you load a whole repo, a full training log or days of agent traces at once.

TL;DR

Size: 0.1 to 0.5T parameters (exact count and active params not disclosed); context up to 10M tokens.

Runs on: Hosted early access only; no open weights or quantized builds announced.

Performance: Strong long-context retrieval, mid-pack agentic coding versus open-weight models, well behind frontier models.

Best: 100% on RULER single-needle retrieval at every length from 32K to 10M tokens (base model).

Worst: 6.1% on Terminal Bench 4.0, versus 66.4% for Claude Opus 5.5 in Mirendil&#8217;s own table.

What is Mirendil Fern?

Fern is a language model from Mirendil, an AI R&D lab. 

Fern is aimed at AI R&D work, not general chat. Mirendil lists 6 target uses:

Working across larger codebases

Agentic coding that runs commands until tests pass

Research code: training loops, data pipelines and evaluations

Debugging training runs from long logs and stack traces

Reading full agent or training traces end to end

Auditing pretraining shards for duplicates, contamination and junk

How was Fern built?

Fern sits on Mirendil-Base, which Mirendil says one researcher pretrained in 3.5 months. Total compute was under $10M, including experiments, agent token spend and data processing. AI agents wrote over 99% of the code. The researcher chose what to try and when to intervene.

Training data came only from public sources: GitHub, public code, web pages and public datasets. Mirendil says it used no distillation, no synthetic data and no licensed data. The code was written from scratch on PyTorch and JAX.

Fern is the smallest of 3 planned models. Mirendil-Base-Large (0.5 to 2T parameters) is over 80% through pretraining. Mirendil-Base-XL (2 to 10T) is over 20% through.

Does longer context actually help?

Mirendil tested next-token prediction on its own repositories, concatenated into a 42.9 MB stream. It measured cross-entropy in bits per byte, where lower is better. Window sizes here are measured in bytes, not tokens.

Fern&#8217;s loss fell from 0.246 at a 32K-byte window to 0.155 at 16M and 23M bytes. The other models were scored up to about 1M tokens, their advertised limit. At a 1M-byte window, Kimi-K3 scored 0.140 and Fern 0.165. So Fern is not the best predictor at equal context. Its advantage is that the curve keeps going past where others stop.

How does Fern score on RULER?

RULER is a standard long-context benchmark. Mirendil ran 5 RULER tasks on Mirendil-Base, the pre-post-training model. It used greedy decoding, thinking off and exact string matching.

RULER task32K1M4M10MSingle needle100100100100Multi-key retrieval100989890Multi-key, all needles100100100100Variable tracking1009575100Multi-hop QA (HotpotQA)65656045

Retrieval holds up well. Multi-hop reasoning drops to 45% at 10M. Each 10M cell uses only 20 examples, versus 100 elsewhere. Mirendil says broader long-context results are coming.

&&

How does Fern 0.1 do on agentic benchmarks?

Mirendil compared Fern 0.1 with open-weight and frontier models. Scores for other models come from model cards, leaderboards or Mirendil&#8217;s own runs.

Benchmark (pass %)Fern 0.1Kimi-K3GLM-5.3Claude Opus 5.5DeepSWE v1.144.267.366.974.2Terminal Bench 4.06.112.641.966.4SWE Atlas QnA53.266.159.466.4SWE-Pro v2 Hard76.588.284.3100.0SWE-Bench Verified73.493.495.498.2

Fern 0.1 beats Inkling and Nemotron 3 Ultra on 4 of 5 tests. It ties Beam on SWE-Pro v2 Hard at 76.5. It trails Beam on SWE-Bench Verified, 73.4 versus 81.6. Every frontier and large open model in the table leads it.

How does Fern compare with similar models?

FeatureFern 0.1Kimi-K3GLM-5.3DeveloperMirendilMoonshot AIZ.aiTotal params0.1 to 0.5T2.8T753BActive paramsNot disclosed104B~40BContextUp to 10M tokens1,048,576 tokens1,048,576 tokensInputText, codeText, image, videoTextLicenseNot disclosedKimi K3 LicenseGLM-5.3 LicenseWeightsNot releasedOpenOpenAccessEarly access requestOpen weights, APIsOpen weights, APIsSWE-Bench Verified*73.493.495.4Bits per byte at 1M bytes*0.1650.1400.170

*Figures from Mirendil&#8217;s announcement charts.

Key Takeaways

Fern 0.1 supports up to 10M tokens, about 23 MB of code.

Bits per byte keeps falling to 0.155 at a 23M-byte window.

RULER single needle stays at 100% from 32K to 10M tokens.

Agentic coding lags: 6.1% on Terminal Bench 4.0.

Base model built by 1 researcher plus agents for under $10M.

Check out the Fern announcement, the Mirendil-Base pretraining post, and request early access. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Mirendil Launches Fern 0.1, Its First Model, With 10M-Token Context appeared first on MarkTechPost.