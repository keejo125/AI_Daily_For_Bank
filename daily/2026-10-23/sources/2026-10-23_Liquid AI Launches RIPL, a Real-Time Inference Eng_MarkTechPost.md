---
publish_time: 1792690405
link: https://www.marktechpost.com/2026/10/22/liquid-ai-ripl-real-time-inference-engine/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Liquid AI 发布低延迟推理引擎 RIPL（Real-time Inference Pipeline），在实时请求路径中服务 Liquid 基础模型（LFM2.5，230M–2.6B 参数），端到端响应低于 50ms 且峰值负载下延迟稳定；官方测试称 p95 延迟较 vLLM 上的 Qwen3.5 低 5.6–28.4 倍。
---

# Liquid AI发布RIPL实时推理引擎（sub-50ms）

> 原文链接：https://www.marktechpost.com/2026/10/22/liquid-ai-ripl-real-time-inference-engine/
> 来源：MarkTechPost

Liquid AI just announced Liquid RIPL, short for Real-time Inference Pipeline. RIPL is a low-latency engine that serves Liquid Foundation Models (LFMs) inside a live request path. It returns complete generated responses end-to-end in under 50 ms. It also claims that latency holds while traffic arrives continuously at peak load. For developers, the message is simple. Swap gradient-boosted trees for a generative model, and keep the latency budget.

TL;DR

Engine: Serves LFM2.5 models from 230M to 2.6B parameters

Runs on: Enterprise deployments on NVIDIA H100, H200, B200 and RTX PRO 6000 GPUs. Benchmarks used a single B200.

Performance: 5.6 to 28.4x lower p95 latency than Qwen3.5 on vLLM, per Liquid&#8217;s own tests.

Best: LFM2.5-1.2B hit 155.8 ms p95 vs 4,431 ms for Qwen3.5-0.8B, a 28.4x gap (256 in, 128 out).

Worst: LFM2.5-2.6B gained only 5.6x (449.1 ms vs 2,499 ms). Sub-50 ms fails on longer requests.

What problem does Liquid RIPL solve?

Most serving stacks target large batches and long agentic jobs. A few seconds per request is acceptable there. Search ranking, fraud checks and payment authorization need answers in milliseconds. Liquid AI argues teams default to classical models for these paths because LLM serving is too slow. RIPL is built to remove that trade-off.

How does RIPL work?

Liquid AI describes RIPL as optimizing the full path, from request arrival to completed response. In several workloads, Liquid AI plots the same model, LFM2.5-350M, on vLLM and on RIPL. RIPL&#8217;s p95 line sits well below the vLLM line in each case. That isolates part of the gain to the engine, not just the model architecture.

The LFM2.5 models themselves are hybrids. LFM2.5-1.2B-Instruct has 16 layers: 10 double-gated convolution blocks and 6 GQA blocks. LFM2.5-2.6B has 30 layers: 22 convolution blocks and 8 GQA blocks.

RIPL benchmarks: how fast is it vs vLLM?

Liquid measured p95 end-to-end latency under open-loop Poisson arrivals on one B200. LFMs ran on RIPL. Baselines, including MiniCPM5 and Granite 4.2, ran on vLLM.

WorkloadLoadLFM2.5 on RIPL (p95)Qwen3.5 on vLLM (p95)Gap1B class, 32 in → 32 out1,000 req/s34.6 ms (1.2B)498 ms (0.8B)14.4x1B class, 256 in → 128 out400 req/s155.8 ms (1.2B)4,431 ms (0.8B)28.4x2B class, 32 in → 32 out1,000 req/s76.4 ms (2.6B)586.8 ms (2B)7.7x2B class, 256 in → 128 out300 req/s449.1 ms (2.6B)2,499 ms (2B)5.6x

Source: Liquid AI blog, Figure 2. Sealf-reported.

Liquid AI also mapped 6 real-time workloads against fixed budgets:

Adtech query rewriting: 32 in, 32 out, 50 ms budget, LFM2.5-350M.

Search intent classification: 128 in, 1 out, 20 ms budget.

Search reranking: 1k in, 1 out, 30 ms budget.

Payments risk scoring: 512 in, 16 out, 50 ms budget, LFM2.5-1.2B.

Credit decisioning: 8k in, 64 out, 150 ms budget.

Image alt text: 512×512 image and 64 tokens in, 16 out, 100 ms budget, LFM2.5-VL-450M.

&&
 -->

Competitor Comparison

FeatureLFM2.5-1.2B on RIPLQwen3.5-0.8B on vLLMLFM2.5-2.6B on RIPLQwen3.5-2B on vLLMParameters1.17B0.8B2.69B2BContext32,768262,144131,072262,144License (weights)LFM Open License v1.0Apache 2.0LFM Open License v1.0Apache 2.0ModalityTextText, image, videoTextText, image, videoDefault modeInstructNon-thinkingAlways reasonsNon-thinkingServing engineRIPL (enterprise)vLLM (open source)RIPL (enterprise)vLLM (open source)p95, 32→3234.6 ms498 ms76.4 ms586.8 msp95, 256→128155.8 ms4,431 ms449.1 ms2,499 ms

Is RIPL used in production?

Yes, according to Liquid AI. Shopify is deploying LFMs across latency-sensitive commerce workloads. In search enhancement, LFMs run with sub-20 ms inference on production traffic. According to Liquid AI&#8217;s blog, they use about 50% fewer parameters than alternatives and deliver 2 to 10x faster inference. 

Key Takeaways

RIPL is Liquid AI&#8217;s engine for LLMs inside live request paths.

Liquid claims 5.6 to 28.4x lower p95 latency than Qwen3.5 on vLLM.

Same-model tests (LFM2.5-350M) show RIPL itself beats vLLM.

Shopify runs LFMs at sub-20 ms in production search.

Enterprise-only, closed, and all figures are self-reported.

Check out the RIPL announcement, try the latency calculator, and see the LFM2.5 model cards.. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Liquid AI Launches RIPL, a Real-Time Inference Engine for Sub-50 ms LFMs appeared first on MarkTechPost.