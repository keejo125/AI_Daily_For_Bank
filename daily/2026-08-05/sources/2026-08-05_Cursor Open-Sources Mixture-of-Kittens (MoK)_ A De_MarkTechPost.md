---
publish_time: 1785868721
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cursor Research 开源了 Mixture-of-Kittens（MoK），这是其 Composer 系列模型背后的 MoE 训练巨型内核。MoK 将所有 MoE 通信与计算步骤融合为单个确定性内核，相比最强公开基线实现最高 2.37 倍吞吐提升，已在数万张 GPU 上支撑 Composer 训练。MoK 以 Apache-2.0 协议发布在 GitHub，但硬件门槛较高：要求 NVIDIA Blackwell SM100/SM103 GPU（GB200/GB300 NVL72 机架），需 Python 3.12+、PyTorch 2.10+、CUDA Toolkit 13.0+，跨 GPU 缓冲区依赖 PyTorch 对称内存。这是业界首个面向 Blackwell 架构的开源 MoE 训练内核，对大规模 MoE 模型训练基础设施具有重要意义。
---

# Cursor Open-Sources Mixture-of-Kittens (MoK): A Deterministic MoE Training Megakernel for GB300 NVL72 Racks

> 原文链接：https://www.marktechpost.com/2026/08/04/cursor-open-sources-mixture-of-kittens-mok-a-deterministic-moe-training-megakernel-for-gb300-nvl72-racks/
> 来源：MarkTechPost

Cursor Research has open-sourced Mixture-of-Kittens (MoK), the mixture-of-experts training megakernel behind its Composer models. MoK fuses every MoE communication and computation step into a single deterministic kernel. Cursor team reports up to 2.37x higher throughput than the strongest public baseline. It already powers Composer training across tens of thousands of GPUs.

Is it deployable

Yes, but the hardware floor is high. MoK is on GitHub under Apache-2.0. It requires NVIDIA Blackwell SM100 or SM103 GPUs, which means GB200 NVL72 or GB300 NVL72 racks. It also needs Python 3.12+, PyTorch 2.10+, and CUDA toolkit 13.0+. Inter-GPU buffers rely on PyTorch symmetric memory.

That limits realistic adopters to organizations that own or rent NVL72 capacity. Frontier labs, funded model startups, GPU neoclouds, and national computing centers fit. Single-node teams and 8-GPU shops do not.

Applications are narrow but high-value. They include pretraining and post-training of DeepSeek-V3-style MoE models. Determinism also makes it useful for on-policy RL post-training and internal ablations. Relevant industries are AI model development, cloud GPU infrastructure, code-generation tooling, and quantitative research.

MoE layer as the bottleneck

Cursor&#8217;s earlier work covered the compute side. The research team wrote its own MXFP8 and NVFP4 training kernels and a &#8216;warp decode&#8217; path for MoE inference. Those assumed inter-GPU communication was handled separately.

In production, communication became the limiting factor. The MoE layer can consume more than half of end-to-end training time. Moving to GB300 NVL72s changed the problem again. A rack is 72 GPUs inside one NVLink domain, which allows fine-grained overlap. But the integrated Grace CPUs are slow relative to the GPUs. CPU-GPU synchronization therefore has to be minimized aggressively.

Three design decisions that matter

Communication direction is chosen per operation: Existing approaches such as DeepEP lean on push-based transfers. Cursor&#8217;s microbenchmarks show push moves fewer total bytes in one direction. That leaves the reverse NVLink lane mostly idle. Pull-based dispatch delivers up to 29% higher NVLink bandwidth utilization under expert imbalance. It also eliminates cross-GPU completion signals. Push dispatch signalling measured 103 µs against 18 µs for pull, roughly 5.8x. MoK therefore uses pull-based forward dispatch and push-based forward combine. The backward pass mirrors this with pull reverse-combine and push reverse-dispatch. One schedule table serves all four, costing under 3% of MoE runtime.

Overlap granularity sits between the extremes: Comet is fine-grained; DeepEP is coarse-grained. Cursor team argues the optimum is in the middle and workload-dependent. The heuristic targets at least two full SM waves per expert-grouped GEMM. For Kimi 2.5 shapes, the base model for Composer 2.5, the floor is 2,368 tokens. Measured latency matches that estimate closely.

A ring token buffer removes the CPU from the loop: The alternatives are dropping tokens or asking the CPU to size buffers. MoK instead cycles a fixed ring buffer of a few hundred megabytes. It does so at minibatch granularity, interleaving dispatch and combine at macrobatch boundaries. The ring is walked in reverse to minimize forward activation replay during backward.

MoK is built as a megakernel and is fully deterministic. It supports BF16 and MXFP8 precision modes. Scheduling runs through Blackwell&#8217;s Cluster Launch Control, so inter-rack RDMA does not serialize behind it. Router weight gradients use a SonicMoE-style calculation fused into the SwiGLU backward.

https://cursor.com/blog/mixture-of-kittens

Results

Layer benchmarks ran in a single NVL72 rack at EP degree 64. Each GPU held 2,048 tokens before routing. Baselines were NCCL+PyTorch, DeepEP+PyTorch, DeepEP+TransformerEngine, and HybridEP+Megatron. Shapes covered Kimi K2.7 Code, GLM-5.2, Qwen3.5-397B-A17B, and DeepSeek-V4-Pro.

Against the fastest baseline, MoK is up to 2.37x faster for MXFP8 forward. The other figures are 1.78x MXFP8 backward, 1.92x BF16 forward, and 1.58x BF16 backward. End-to-end testing used 512 GPUs across several GB300 NVL72 racks. Tokens per second per GPU rose from 760.9 to 1,070.2, a 1.41x gain. 

Key Takeaways

MoK fuses all MoE communication and computation into one deterministic megakernel for NVL72 racks.

Pull dispatch plus push combine cuts signalling from 103 µs to 18 µs.

A ring token buffer drops zero tokens and removes CPU-GPU synchronization entirely.

Up to 2.37x over the fastest public baseline; 1.41x end-to-end on 512 GPUs.

Apache-2.0, but it demands Blackwell SM100/SM103, CUDA 13.0+, and PyTorch 2.10+.

Check out the GitHub Repo and Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Cursor Open-Sources Mixture-of-Kittens (MoK): A Deterministic MoE Training Megakernel for GB300 NVL72 Racks appeared first on MarkTechPost.