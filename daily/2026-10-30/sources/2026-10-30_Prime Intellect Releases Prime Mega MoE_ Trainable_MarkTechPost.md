---
publish_time: 1793298537
link: https://www.marktechpost.com/2026/10/29/prime-intellect-prime-mega-moe-fused-moe-kernel-training/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Prime Intellect发布Prime Mega MoE，在DeepSeek开源DeepGEMM的Mega MoE内核基础上增加快速、可重叠的反向传播，使融合内核可用于训练而非仅推理。在其prime-rl训练器中，Qwen3 MoE模型完整训练步速最高提升34%，较TorchTitan快48%–55%，直接削减MoE模型的GPU小时开销，已支持Hopper与Blackwell GPU。
---

# Prime Intellect发布Prime Mega MoE：可训练融合MoE内核，前向提速3.11倍

> 原文链接：https://www.marktechpost.com/2026/10/29/prime-intellect-prime-mega-moe-fused-moe-kernel-training/
> 来源：MarkTechPost

Prime Intellect has released Prime Mega MoE, a training extension of DeepSeek&#8217;s fused Mega MoE kernel. DeepSeek&#8217;s kernel only ran the forward pass. Prime Intellect added a fast, overlapping backward pass. That makes the fused kernel usable for training, not just inference. In its prime-rl trainer, full training steps on Qwen3 MoE models run up to 34% faster. Against TorchTitan, the gain reaches 55%. For teams training mixture-of-experts (MoE) models, that is a direct cut in GPU hours.

TL;DR

Size: A GPU kernel, not a model. Tested on Qwen3-30B-A3B and Qwen3-235B-A22B (128 experts, top-8 routing).

Runs on: NVIDIA Hopper (blockwise FP8) and Blackwell (MXFP8) GPUs, BF16 on both. Published numbers use 8×H200 nodes, 32 to 128 GPUs.

Performance: 32% to 34% faster full training steps than the prime-rl baseline. 48% to 55% faster than TorchTitan.

Best: 3.11x faster forward pass on a Qwen3-30B-A3B MoE layer (12.0 ms to 3.9 ms).

Worst: 1.24x backward pass on a Qwen3-235B-A22B MoE layer (30.5 ms to 24.6 ms).

What is Prime Mega MoE?

Prime Mega MoE is a fused, overlapping MoE kernel for training from Prime Intellect. It builds on the Mega MoE kernel in DeepSeek&#8217;s open-source DeepGEMM library. 

Why is MoE training communication-bound?

In an MoE model, each token goes to a small subset of experts. Those experts sit on different GPUs. So every layer sends tokens out, runs expert math, and sends results back. This happens in the forward pass and again in the backward pass.

In a standard setup, these are separate operations. The GPU sorts tokens and waits on the transport layer. Then it computes, hands results back, and waits again. Those waits are idle GPU time.

How does the fused kernel work?

DeepSeek&#8217;s Mega MoE, added to DeepGEMM in April 2026, replaces that chain with one kernel call. It fuses expert-parallel dispatch, the 2 expert linear layers, SwiGLU, and combine. While one token group is in transit, the kernel computes on a group that already arrived. It also skips intermediate tensors by using GPU-only scratch buffers. But it only shipped a forward implementation.

Prime Intellect wrote the missing backward kernel, also overlapping. Supported types are BF16, MXFP8 (Blackwell only) and blockwise FP8 (Hopper only). The prime-rl config also exposes an fp8_bwd mode: BF16 forward, FP8 backward.

&&&&

How fast is Prime Mega MoE?

All numbers below are self-reported by Prime Intellect. Training steps use 8×H200 nodes, FP8, 16,384-token sequences and full activation checkpointing. Each result is the mean of steps 6 to 20.

Full training step, seconds (lower is better):

Model (cluster)prime-rl baselineTorchTitan (FP8)Prime Mega MoEGain vs baselineGain vs TorchTitanQwen3-30B-A3B (32 H200)2.783.072.0834%48%Qwen3-235B-A22B (128 H200)12.7214.989.6532%55%

Against TorchTitan, throughput rose from 5,337 to 7,886 tokens/s/GPU on the 30B model. On the 235B model, it rose from 1,094 to 1,697. The prime-rl baseline uses torch all-to-all plus DeepGEMM FP8 experts.

Single MoE layer, milliseconds (1 node, 8×H200, EP=8, 128 experts, top-8, random routing):

LayerForwardBackwardFull layer (2x fwd + bwd)Qwen3-30B-A3B12.0 to 3.9 (3.11x)15.4 to 8.2 (1.87x)39.3 to 15.9 (2.47x)Qwen3-235B-A22B20.7 to 9.5 (2.17x)30.5 to 24.6 (1.24x)71.9 to 43.7 (1.64x)

The pattern is clear. Forward gains are large, and backward gains are smaller. The headline &#8220;up to 3.11x&#8221; refers to the forward pass only.

How does it compare with other fused MoE options?

FeaturePrime Mega MoEDeepGEMM Mega MoETorchTitan + DeepEPAMD Primus MegaMoEDeveloperPrime IntellectDeepSeekPyTorch, NebiusAMDTraining (backward)Yes, fused and overlappingNo, forward onlyYes (separate dispatch kernels)Yes, per design docsCompute and comms fusedYesYesNoYes (dispatch+GEMM1, GEMM2+combine)GPUsHopper, BlackwellSM90, SM100 (library)B200 in published runsMI355X (gfx950)Data typesBF16, MXFP8, blockwise FP8FP8xFP8, FP8xFP4BF16, MXFP8 grouped GEMMsBF16, MXFP8Published speedupUp to 55% step time vs TorchTitanNot disclosedUp to 41% on DeepSeek-V3 671BNot disclosedLicenseApache 2.0 (prime-rl)MITBSD-3-ClauseMIT

TorchTitan&#8217;s 41% gain comes from a different setup (B200, 671B model, BF16 baseline). It is not directly comparable.

How do developers use it?

Prime Mega MoE is a dispatch backend in prime-rl. Set type = "mega_moe" under [trainer.model.moe.dispatch]. Choose precision from bf16, mxfp8, fp8 or fp8_bwd. The training kernels ship in a prebuilt DeepGEMM wheel from prime-kernels. The stock DeepGEMM build lacks them.

Key Takeaways

Prime Mega MoE adds a fused, overlapping backward pass to DeepSeek&#8217;s Mega MoE.

Full training steps run 32% to 34% faster than the prime-rl baseline.

Against TorchTitan, steps run 48% to 55% faster on Qwen3 MoE models.

Forward gains reach 3.11x, but backward gains drop to 1.24x on large layers.

It ships in prime-rl as the mega_moe dispatch backend.

Check out the Prime Mega MoE blog post, the announcement on X, and the prime-rl repo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Prime Intellect Releases Prime Mega MoE: Trainable Fused MoE Kernel, 3.11x Faster Forward Pass appeared first on MarkTechPost.