---
publish_time: 1792506719
link: https://www.marktechpost.com/2026/10/20/deepseek-deepinfer-open-source-inference-framework/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  DeepSeek 开源其内部生产级推理框架 DeepInfer（Apache 2.0）与 MIT 许可的 Token 编解码层 deepseek-recipe，是支撑 DeepSeek-V4.1-Flash 的 serving 引擎，罕见展示前沿实验室的真实服务栈。框架支持单模型（V4.1-Flash）、100 万 Token 上下文，运行于英伟达 Blackwell（SM100）与华为昇腾平台。
---

# DeepSeek 开源推理框架 DeepInfer：支撑 V4.1-Flash 生产服务

> 原文链接：https://www.marktechpost.com/2026/10/20/deepseek-deepinfer-open-source-inference-framework/
> 来源：MarkTechPost

DeepSeek has open-sourced DeepInfer, the inference framework that runs its production services. The DeepSeek DeepInfer inference framework is the engine behind DeepSeek-V4.1-Flash. It ships under the Apache 2.0 license. DeepSeek also released deepseek-recipe, its MIT-licensed token encoding and decoding layer. For developers, this is a rare look at a frontier lab&#8217;s real serving stack.

TL;DR

Size / scope: 1 supported model (DeepSeek-V4.1-Flash), 1M-token context window per the model card.

Runs on: NVIDIA SM100 (Blackwell) GPUs and Huawei Ascend 950 NPUs. Benchmarks used 4 GPUs for prefill and 64 for decode.

Performance: Production-grade throughput; DeepSeek says 1 cluster serves 155 trillion tokens per day.

Best: Above 25,000 output tokens/s/GPU at 256 requests per rank (EP64, 131,072 context).

Worst: Offline inference only. KV cache system, P/D disaggregation and load balancing are not included.

What is DeepInfer?

DeepInfer is a high-performance inference engine from DeepSeek for its own models. According to it&#8217;s GitHub README, it powers DeepSeek&#8217;s large-scale production services. This release covers offline inference with the core features needed at scale. It was originally built primarily on vLLM, with ideas from SGLang and TensorRT-LLM.

The deployment Q&A gives production context. A single cluster serves 155 trillion tokens per day. DeepSeek reports overall revenue of US$38 per GPU-hour at valley pricing.

How does DeepInfer work?

The engine stacks DeepSeek&#8217;s kernels: FlashMLA, DeepGEMM, DeepEP, TileKernels, DeepSelect and custom TileLang kernels. On top sit 5 system-level ideas.

Parallelism: Attention DP plus Wide-EP

Attention uses data parallelism. The MoE layers use expert parallelism with an expert-parallel load balancer (EPLB). Decode runs EP64 to EP128 inside a supernode. Prefill uses the smallest EP that memory allows, typically EP2 to EP8.

DSpark: confidence-scheduled speculative decoding

A draft model proposes 5 tokens per step. A Confidence Head predicts each draft token&#8217;s acceptance rate. The scheduler then verifies only the most valuable prefix. Per the Q&A, this cuts verified draft tokens by about 30% (5.00 to 3.2 to 4.4). Accepted length barely moves (3.29 vs 3.20).

SWA bounded replay

On a cache hit, DeepInfer recomputes only the last 128 tokens of sliding-window attention state. That makes recomputation cost constant, regardless of context length. In the decoder layers, DeepSeek says this nearly halves total prefill compute.

Asynchronous scheduling, determinism and structured output

CPU batch scheduling overlaps with GPU execution, so the GPU never idles between steps. Batch-invariant inference and deterministic sampling are available on NVIDIA only. Structured outputs support regex, JSON schema and EBNF grammars.

&&

How fast is DeepInfer?

DeepSeek publishes Pareto curves for DeepSeek-V4.1-Flash at 131,072 context. Prefill ran on 4 SM100 GPUs; decode ran on 64. Figures below are read from those charts and are self-reported.

Decode (EP64DP64, nextn=3, 75% acceptance): Above 25,000 tokens/s/GPU at 256 requests per rank, near 100 tokens/s per user. At 8 requests, per-user speed passes 300 tokens/s.

Prefill (EP4DP4, 140-token bounded replay): About 60,000 non-cached tokens/s/GPU at 4,096 tokens per rank. Throughput nears 90,000 at 65,536 tokens, with roughly 730 ms per step.

Wide-EP payoff: An EP8 vs EP64 chart shows EP64 ahead at every batch size.

DSpark&#8217;s dynamic verification adds 4% to 7% throughput at about 60 sequences per rank. At 16 sequences per rank it is 1.5% slower than fixed 5-token verification.

How does DeepInfer compare with vLLM, SGLang and TensorRT-LLM?

FeatureDeepInfervLLMSGLangTensorRT-LLMMaintainerDeepSeekvLLM projectSGLang projectNVIDIALicenseApache 2.0Apache 2.0Apache 2.0Apache 2.0Model coverage1 (DeepSeek-V4.1-Flash)200+ architecturesLLMs, VLMs, diffusionSupport matrixHardwareNVIDIA SM100, Huawei Ascend 950NVIDIA, AMD, Intel, CPUs, plugins incl. Ascend, TPUNVIDIA, AMD, TPU, Intel, Apple, Ascend, Moore ThreadsNVIDIA GPUsExpert parallelismYes, with EPLBYesYesWide-EPSpeculative decodingDSpark, confidence-scheduledn-gram, suffix, EAGLE, DFlashYes, via SpecForge draftsYesP/D disaggregationNot in this releaseYes (prefill, decode, encode)Via llm-d, Dynamo and othersYesOnline servingOffline inference onlyOpenAI-compatible serverYesYes

What are DeepInfer&#8217;s limitations?

A full service still needs a KV cache system and VE/Prefill/Decode disaggregation. It also needs load balancing across data-parallel replicas. DeepSeek team states that those components are tightly coupled to internal infrastructure.

Hardware is narrow. Builds require Linux, GCC 13 or later, Python 3.12, and CUDA 13 or CANN 9.2. The smallest efficient production unit is 64 prefill GPUs plus 64 decode GPUs. The internal FlashMLA decoding kernel is 5% to 10% faster than the public one. End-to-end, DeepSeek puts the gap at 5% or less.

Key Takeaways

DeepInfer is DeepSeek&#8217;s production engine, now Apache 2.0 on GitHub.

It supports only DeepSeek-V4.1-Flash, on NVIDIA SM100 and Ascend 950.

Decode tops 25,000 tokens/s/GPU on 64 GPUs (self-reported).

DSpark cuts verified draft tokens about 30% with near-equal acceptance.

Offline only: no KV cache store, P/D disaggregation or load balancer.

Check out the GitHub repo, deployment Q&A, deepseek-recipe and the model card. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post DeepSeek Open-Sources DeepInfer, the Inference Framework Behind DeepSeek-V4.1-Flash appeared first on MarkTechPost.