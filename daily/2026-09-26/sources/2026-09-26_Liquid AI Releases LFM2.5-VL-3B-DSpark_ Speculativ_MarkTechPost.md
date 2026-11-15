---
publish_time: 1790377919
link: https://www.marktechpost.com/2026/09/25/liquid-ai-releases-lfm2-5-vl-3b-dspark-speculative-decoding-for-vision-language-models-with-up-to-3-13x-faster-decoding/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Liquid AI 发布 LFM2.5-VL-3B 视觉语言模型的推测解码草稿模型 LFM2.5-VL-3B-DSpark（实验性）。该草稿模型新增约 2.8 亿参数，在不改变原模型输出的前提下加速解码：在 Apple 芯片上最高提速 3.13 倍，在 NVIDIA H100 上最高 2.66 倍。权重已在 Hugging Face 以 Safetensors 与 GGUF 格式发布，并在 SGLang、MLX-VLM、llama.cpp 首日支持，采用 LFM Open License v1.0 许可。
---

# Liquid AI 发布 LFM2.5-VL-3B-DSpark 视觉语言模型推测解码

> 原文链接：https://www.marktechpost.com/2026/09/25/liquid-ai-releases-lfm2-5-vl-3b-dspark-speculative-decoding-for-vision-language-models-with-up-to-3-13x-faster-decoding/
> 来源：MarkTechPost

Liquid AI has announced LFM2.5-VL-3B-DSpark, an experimental speculative-decoding draft model for its LFM2.5-VL-3B vision-language model. The drafter adds about 280M parameters and speeds up decoding without changing the model&#8217;s output. Liquid AI team reports up to 3.13x faster decoding on Apple silicon and up to 2.66x on an NVIDIA H100.

Is it deployable? Yes, Weights are live on Hugging Face in Safetensors and GGUF, with day-one support in SGLang, MLX-VLM, and llama.cpp. Liquid AI team labels the release experimental, and it ships under the LFM Open License v1.0, which allows free commercial use only for companies under $10M in annual revenue.

What Speculative Decoding Changes for a VLM

A standard model generates one token per forward pass. Speculative decoding adds a small drafter that proposes several tokens ahead. The large target model then checks the whole block in one pass and keeps the tokens it agrees with.

DSpark follows the recipe from Liquid AI&#8217;s text-model DSpark drafters, described in the DSpark paper. The drafter reads the target model&#8217;s hidden states from several layers and predicts the next k tokens.

The key design point: modality does not matter to the drafter. By the time tokens reach the hidden layers, text and image patches are both just tensors. So Liquid AI team reuses the exact same inference algorithm for its vision-language model.

&

Drafter Architecture and Training

The drafter is a simplified attention-only model. Ablations picked 4 layers and a block size of 9. Liquid AI recommends a block size of 8 or 9 at inference, depending on hardware. Apple silicon runs use 8.

ComponentParametersDecoder stack (4 layers)193.0MHidden-state projection21.0MMarkov head65.5MNorms + confidence head6.4kTotal279.5M

The embedding and LM head are tied to the target, so the drafter does not carry them. Liquid AI says this raises the deployed parameter count by 8.9%. Training used supervised fine-tuning data covering common vision-language tasks for 10 epochs. All ablations and training ran exclusively on AMD hardware.

Benchmark Results

Evaluation follows the MMSpec benchmark across 6 task types: General VQA, Text VQA, Image Captioning, Chart VQA, Complex Reasoning, and Multi-turn Conversation. All runs used batch size 1, temperature 0, and 16-bit weights for the vision encoder and backbone. Data was collected on Pipette, Liquid AI&#8217;s public device-benchmarking infrastructure.

StackDecode speedupEnd-to-end speedupAccepted tokens per passMLX-VLM, M5 Max MacBook Pro (block 8)2.30x to 3.13x1.56x to 2.62x3.24 to 4.34llama.cpp, M3 Ultra (block 8)1.57x to 2.14x1.30x to 1.77x3.31 to 4.50SGLang, 1x H100 80GB (block 9)2.04x to 2.66x1.64x to 2.27x3.46 to 4.57

The &#8216;up to&#8217; decode and end-to-end figures often come from different tasks. On the M5 Max, 3.13x decode is from COCO captioning, while 2.62x end-to-end is from MMMU-Pro.

Acceptance landed in a similar range on both Apple stacks. Liquid AI reads this as acceptance depending on the drafter and workload, not the runtime.

At higher concurrency, DSpark kept a throughput advantage at every measured level on a single H100 in SGLang. The gap narrows as concurrency rises.

Output Quality and Temperature

Under greedy decoding, the target verifies every proposed token, so output is identical to the base model. At non-zero temperatures with matched sampling, speculative decoding preserves the target&#8217;s output distribution, as proven by Leviathan et al.

Temperature does affect speed. Higher temperatures spread probability across more candidate tokens, so drafter and target disagree more often. In Liquid AI&#8217;s tests, this lowered acceptance and throughput.

Why End-to-End Gains Are Smaller on Edge

Speculative decoding only accelerates decoding. Image encoding and prefill run at the same speed. A VLM must encode the image, then process hundreds of visual tokens alongside the prompt.

On edge devices with less compute than data center GPUs, prefill takes a larger share of latency. Liquid AI frames this as Amdahl&#8217;s law: total speedup is bounded by the part left unaccelerated. This explains cases like TextVQA on the M5 Max, where 2.69x faster decoding yields 1.56x end to end.

How to Run It

SGLang requires v0.5.19 or newer. Launch LiquidAI/LFM2.5-VL-3B with --speculative-algorithm DSPARK and point --speculative-draft-model-path at the drafter. On Apple silicon, MLX-VLM v0.7.2 or newer accepts the drafter through --draft-model. DSpark in MLX-VLM currently supports greedy sampling only, so set temperature to 0. For llama.cpp, pair the GGUF drafter with the LFM2.5-VL-3B-GGUF target.

Integration work is public in the llama.cpp, SGLang, and MLX-VLM pull requests. Acceleration of quantized models is outside the scope of this release.

Key Takeaways

A 279.5M drafter adds 8.9% parameters to LFM2.5-VL-3B.

Decoding runs up to 3.13x faster on M5 Max, 2.66x on H100.

Output is identical under greedy decoding; distribution preserved when sampling.

Prefill and vision encoding cap end-to-end gains, especially on edge.

Tested at 16-bit only; quantized acceleration is not covered yet.

Check out the Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Liquid AI Releases LFM2.5-VL-3B-DSpark: Speculative Decoding for Vision-Language Models With Up to 3.13x Faster Decoding appeared first on MarkTechPost.