---
publish_time: 1793914380
link: https://www.marktechpost.com/2026/11/05/baidu-ernie-5-5-flash-base-280b-moe/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  百度发布 ERNIE 5.5 Flash Base，280B 参数稀疏 MoE、每 token 激活 14B 的预训练检查点（无后期训练），128K 训练上下文、微调/推理支持 1M。作为干净起点供团队对比微调、指令微调或 RL 方法，提供 SGLang 与 vLLM 多 GPU 参考配置。
title: 百度发布 ERNIE 5.5 Flash Base：280B MoE 预训练基座模型
---

# 百度发布 ERNIE 5.5 Flash Base：280B MoE 预训练基座模型

> 原文链接：https://www.marktechpost.com/2026/11/05/baidu-ernie-5-5-flash-base-280b-moe/
> 来源：MarkTechPost

Baidu has released ERNIE 5.5 Flash Base, the raw pre-training checkpoint of its new sparse Mixture-of-Experts language model. ERNIE 5.5 Flash Base is a 280B-parameter text model from Baidu that activates 14B parameters per token. The weights stop at the end of pre-training, with no mid- or post-training applied. This as a clean starting point for teams that want to compare fine-tuning, instruction tuning or RL methods from one checkpoint.

TL;DR

Size: 280B total, 14B active per token; 128K training context, 1M for fine-tuning and inference.

Runs on: Multi-GPU servers. Baidu&#8217;s reference configs use 4-way parallelism in SGLang and vLLM. GPU model and VRAM not disclosed. FP8 and BF16 weights.

Performance: Best score on 24 of 30 base-model benchmarks in Baidu&#8217;s unified pipeline (self-reported).

Best: MMLU-Pro 78.4, ahead of DeepSeek-V4-Flash-Base at 69.2.

Worst: HELMET-Rerank 56.2, behind DeepSeek-V4-Flash-Base at 60.0.

What is ERNIE 5.5 Flash Base?

It is a text-only MoE base model with 43 layers and a 4096 hidden size. It was pre-trained from scratch on 33.5T tokens with the Muon optimizer. The tokenizer has 201,216 entries and groups numbers right-to-left in chunks of up to 3 digits.

Activated compute, KV cache and long-context cost were treated as one budget. Pre-training data leaned on repository-scale code and long-context material, since those are hard to add later.

How does the ERNIE 5.5 Flash architecture work?

Hybrid attention: 37 layers use Heavily Compressed Attention (HCA), which caches 1 entry per 128 tokens. The other 6 layers use Multi-head Latent Attention with sparse attention (MLA + DSA). That means 1 in 7 layers keeps full-context access. HCA layers use 512-dim heads; MLA layers use 256-dim heads.

Gated and mixed heads: The attention output gate comes from the low-rank query latent, cutting gate-projection parameters by 75%. Virtual Head Attention adds a lightweight low-rank mix across heads.

Multi-Router Latent MoE. Each MoE layer has 512 routed experts (top-10) plus 1 shared expert. Several independent sigmoid routers replace a single router, per Baidu&#8217;s Multi-Router paper. Expert FLOPs and communication volume stay unchanged. Experts run in a 2048-d latent space, half the hidden width.

ECHO instead of MTP.:ECHO reuses the backbone&#8217;s final layer to predict future tokens. The same layer doubles as a built-in draft model for speculative decoding. ECHO adds 0.36B parameters, excluded from the headline counts.

Other pieces: The model uses Manifold-constrained Hyper-Connections with expansion rate 4 and a MultiMax output head.

&&

How does ERNIE 5.5 Flash Base perform on benchmarks?

Baidu team evaluated all 4 models with the same pipeline, prompts and few-shot settings. All figures below are self-reported by Baidu.

Exams: MMLU 93.3, MMLU-Redux 94.1, MMLU-Pro 78.4.

Knowledge: SimpleQA 34.1, versus 29.1 for DeepSeek-V4-Flash-Base.

STEM and reasoning: GPQA 60.2, MGSM 87.0, BBH direct 77.1.

Code: HumanEval+ 82.3, MBPP+ 81.5, LiveCodeBench 40.1.

Long context: RepoQA 91.7, LongBench-v2 48.7, HELMET-ICL 85.9.

It loses on 6 tasks. DeepSeek-V4-Flash-Base leads on ChineseSimpleQA, INCLUDE-lite, HELMET-Rerank and InfiniteBench. Hy3-preview-Base leads on BBH CoT and FullStackBench.

Competitor numbers in Baidu&#8217;s pipeline differ slightly from each vendor&#8217;s own report. DeepSeek lists MMLU-Pro 68.3; Baidu measures 69.2. Tencent lists Hy3 MMLU-Pro at 65.76; Baidu AI measures 66.9.

How does it compare with DeepSeek, Tencent and Xiaomi base models?

FeatureERNIE 5.5 Flash BaseDeepSeek-V4-Flash-BaseHy3-preview-BaseMiMo-V2.5-BaseDeveloperBaiduDeepSeekTencentXiaomiTotal params280B284B295B (+3.8B MTP)310BActive params14B13B21B15BContext128K train / 1M inference1M256K256KAttentionHCA + MLA-DSA hybridCSA + HCA hybridGQASWA + global, 5:1Experts512 routed, top-10 + 1 sharedNot disclosed on card192, top-8256, top-8Released weightsFP8, BF16FP8 MixedBF16FP8LicenseERNIE 5.5 Flash Base License v1.0MITTencent Hy Community LicenseMITMMLU-Pro*78.469.266.965.7HumanEval+*82.369.578.074.4LongBench-v2*48.744.539.844.6HELMET-Rerank*56.260.055.756.6

*Scores from Baidu&#8217;s unified evaluation, self-reported.

How do you deploy ERNIE 5.5 Flash Base?

Weights are on Hugging Face and ModelScope, in FP8 and BF16. Baidu documents serving with SGLang and vLLM. The SGLang example uses --tp 4. The vLLM path needs version 0.32.0 plus the vLLM-ERNIE plugin. Both servers accept up to 1,048,576 tokens. As a base model, it runs through the completions endpoint, not chat.

Training ran on FlashMask-4, a kernel for SM90 and SM100 GPUs. On SM100, Baidu team reports up to 175% faster forward and 74% faster backward than FlashAttention-4 MaskMod.

Key Takeaways

280B total, 14B active: a sparse MoE base checkpoint, not a chat model.

MMLU-Pro 78.4 leads DeepSeek-V4-Flash-Base by 9.2 points.

HCA caches 1 entry per 128 tokens in 37 of 43 layers.

ECHO turns the final layer into a built-in speculative draft model.

License is free under US$50M revenue but excludes EU, UK and South Korea.

Check out the Model Weights, Technical Blog, and papers on VHA, Multi-Router MoE and ECHO. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Baidu Releases ERNIE 5.5 Flash Base: A 280B MoE Base Model With 14B Active Parameters appeared first on MarkTechPost.