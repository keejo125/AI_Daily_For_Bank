---
publish_time: 1787251989
link: https://www.marktechpost.com/2026/08/20/liquid-ai-releases-lfm2-5-dspark-draft-models-that-deliver-up-to-3-18x-faster-decoding/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Liquid AI发布LFM2.5-DSpark草稿模型checkpoint，针对三款模型提供草稿模型，在不改变模型输出的前提下实现最高3.18倍解码加速。DSpark面向推理加速场景，通过草稿模型机制降低自回归生成延迟。
---

# Liquid AI 发布 LFM2.5-DSpark 草稿模型，解码提速最高 3.18 倍且不改变输出

> 原文链接：https://www.marktechpost.com/2026/08/20/liquid-ai-releases-lfm2-5-dspark-draft-models-that-deliver-up-to-3-18x-faster-decoding/
> 来源：MarkTechPost

Liquid AI has released DSpark draft model checkpoints for three models in its LFM2.5 family: LFM2.5-1.2B-Instruct, LFM2.5-2.6B, and LFM2.5-8B-A1B. Each drafter adds a speculative decoding path to an existing target model. A roughly 300M-parameter draft proposes a block of nine candidate tokens, and the target model verifies the whole block in a single forward pass. The trade is a small memory increase for a large decoding speedup: up to 3.18x on an H100 and up to 2.87x on an M4 Max MacBook Pro. Output does not change. Under greedy decoding, the emitted sequence is identical to the target model running alone, so benchmark accuracy is unchanged. Both llama.cpp and SGLang have day-one support.

Is it deployable?

Yes, if you self-host. The weights ship as Safetensors and GGUF, and the drafter checkpoints are not served by any hosted inference provider on Hugging Face today. Running them needs an SGLang or llama.cpp build with DSpark support for LFM2 targets.

Company level: The LFM Open License v1.0 allows free commercial use only while your entity stays under $10M in annual revenue. Indie developers, startups and SMBs are covered; larger enterprises must contact Liquid AI for a commercial license first.

Industries: Developer tooling, consumer apps that run locally, robotics and embedded systems, plus healthcare, finance and defense workloads that keep data on-premise or on-device.

Applications: Local coding assistants, on-device agents that reason before each tool call, single-user chat where batch size is 1, and offline copilots on laptop-class hardware.

What are Drafters?

Speculative decoding uses a small model to propose tokens that a larger model verifies. Each LFM2.5 drafter is roughly 300M parameters: 295.7M for the 1.2B-Instruct target and 327.7M for the 2.6B and 8B-A1B targets. The backbone is 5 full-attention layers with hidden_size=2048, intermediate_size=6144, GQA at 32 heads over 8 KV heads, and a block size of 9. The drafter ships no vocabulary weights; embedding and LM head are tied from the target at load time. The 2.6B drafter repository is 655 MB in BF16, which is the real memory cost you are adding.

DSpark combines three parts. A DFlash-style parallel backbone, conditioned on the target&#8217;s context features, produces hidden states for all draft tokens in one forward pass. A lightweight sequential head, modeled as a Markov chain between neighboring tokens at rank 256, restores inter-token dependency and lifts acceptance at later block positions. A confidence-scheduled verifier predicts each token&#8217;s survival probability and prunes low-confidence suffixes when verification would cost more than it saves.

The Measured Results

Liquid AI reports throughput on 1xH100 in BF16 via SGLang, and on an M4 Max MacBook Pro via llama.cpp with Metal and FP16 GGUF weights. Both use block size 9, batch size 1 and temperature 0, across MATH500, HumanEval, MBPP, GSM8K and MT-Bench.

TargetH100 meanBest H100 caseM4 Max meanBest M4 Max caseLFM2.5-1.2B-Instruct2.10x (656 → 1384 tok/s)2.56x on MATH5002.54x (138 → 350 tok/s)2.87x on HumanEval (136 → 389)LFM2.5-2.6B2.67x (323 → 864 tok/s)3.06x on MATH5002.27x (61 → 139 tok/s)2.63x on HumanEvalLFM2.5-8B-A1B2.54x (418 → 1074 tok/s)3.18x on MATH500 (428 → 1362)1.18x (90 → 106 tok/s)1.44x on GSM8K

Speedup tracks acceptance rate, which tracks how predictable the output is. LFM2.5-8B-A1B accepts 8.27 of 10 tokens per step on MATH500 and only 4.02 on GSM8K, so the same model swings from 3.18x to 1.29x on the same GPU. On the 1.2B model, MT-Bench acceptance drops to 3.90 and the H100 gain falls to 1.66x.

The MoE result on Apple silicon is the clearest caveat: LFM2.5-8B-A1B gains only 1.18x on average on the M4 Max. Liquid AI attributes this to the current MoE implementation in llama.cpp&#8217;s Metal backend, and to the fact that verifying k tokens activates more experts, and therefore more weight traffic, than a single decode step.

&

The Agentic Case

The gain concentrates where the user waits through reasoning before every tool call. Across multi-tool function-calling scenarios, Liquid AI reports that DSpark cuts latency by 57% on average for LFM2.5-2.6B. Test it against your own traces: an agent that plans, calls, and re-plans pays the decode cost several times per user turn.

On SGLang, launch the target with the drafter attached:

Copy CodeCopiedUse a different Browser

python -m sglang.launch_server \
  --model-path LiquidAI/LFM2.5-2.6B \
  --speculative-algorithm DSPARK \
  --speculative-draft-model-path LiquidAI/LFM2.5-2.6B-DSpark \
  --speculative-draft-attention-backend flashinfer \
  --disable-radix-cache --mem-fraction-static 0.75 --port 30000

The block size is read from the drafter&#8217;s config.json, and the baseline is the same command without the three --speculative-* flags.

Key Takeaways

DSpark drafters add ~300M parameters and up to 3.18x faster decoding on an H100.

Greedy output is identical to baseline, so benchmark accuracy is unchanged.

Speedup follows acceptance rate and varies by workload, from 1.04x to 3.18x.

On-device MoE is the weak spot: LFM2.5-8B-A1B gains only 1.18x on M4 Max.

Multi-tool function calling gets the biggest practical win: 57% lower latency on LFM2.5-2.6B.

Check out the model card on 8B-A1B and the full technical write-up. All credit for this research goes to the researchers of this project.

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Liquid AI Releases LFM2.5-DSpark Draft Models That Deliver Up to 3.18x Faster Decoding Without Changing Model Outputs appeared first on MarkTechPost.