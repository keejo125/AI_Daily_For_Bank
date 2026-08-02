---
publish_time: 1785610902
status: confirmed
category: 国际
is_model_related: true
digest: |
  AMD发布Instella-MoE-16B-A3B，一个完全开放的混合专家（MoE）语言模型。总参数160亿，活跃参数约28亿，从零开始在AMD Instinct MI300X加速器上训练完成。模型采用标准MoE架构，推理时仅激活约18%的参数，兼顾性能和效率。AMD同步发布了完整训练代码、数据集、模型权重和评估结果，成为少数提供全开源训练配方的大模型厂商。此举标志着AMD在AI软件生态上的持续加码，直接与NVIDIA在模型开源层面展开竞争。
---


# AMD Releases Instella-MoE-16B-A3B: A Fully Open Mixture-of-Experts LLM With 2.8B Active Parameters Trained On Instinct GPUs

> 原文链接：https://www.marktechpost.com/2026/08/01/amd-instella-moe-16b-a3b-fully-open-mixture-of-experts-llm/
> 来源：MarkTechPost

AMD released Instella-MoE-16B-A3B, a fully open Mixture-of-Experts language model trained from scratch on Instinct MI300X and MI325X GPUs. The model holds 16B total parameters but activates only 2.8B per token. AMD is publishing weights from every training stage, along with data mixtures, training configs, and inference code. Two systems-level choices carry the release: Gated Multi-head Latent Attention and FarSkip-Collective connectivity. 

Is it deployable?

Partly. The weights ship under a ResearchRAIL license for academic and research purposes only, so this is not a drop-in commercial model. The training codebase is MIT licensed, and that is the more reusable asset here.

Company level: AI research labs, university groups, and enterprise R&D teams with data-center GPU capacity. Not a fit for lean startups wanting a hosted commercial endpoint.

Industries: semiconductor and cloud infrastructure, AI tooling vendors, and academic research.

Applications: reproducing an end-to-end MoE recipe, studying expert-parallel serving, evaluating 64K long-context behavior, and running RL post-training experiments.

Serving cost: 16B parameters in BF16 need roughly 32 GB of weight memory, so one high-memory accelerator suffices. AMD ships SGLang inference code.

https://rocm.blogs.amd.com/artificial-intelligence/instella-moe/README.html

Architecture

Instella-MoE is a decoder-only MoE with 27 layers, hidden size 2048, 16 attention heads, and a 128,896-token vocabulary. Each MoE layer uses 2 shared experts plus 6 routed experts selected from 64. That yields 2.8B active parameters against 16B total. A Multi-Token Prediction objective is used during pre-training and mid-training.

There are two structural choices that are important to know. Gated MLA adds a lightweight learned output gate to Multi-head Latent Attention. A dedicated linear projection derives an input-conditioned gate, applied multiplicatively before the output projection. FarSkip-Collective passes outdated and partial activations into the MoE and attention layers, overlapping expert-parallel communication with computation. AMD reports a 12.7% pre-training speedup and up to a 39.2% reduction in time to first token when serving with expert parallelism.

Training pipeline

Pre-training covers 7.1T tokens from open corpora including Nemotron-CC-v2, MegaMath, FineMath, RefineCode, and TxT360. Mid-training uses Dolma3 Dolmino 100B across three data variants, merged by weight averaging. A long-context stage extends the window from 4K to 64K using YaRN, an increased RoPE theta, and document masking.

Post-training runs SFT on Dolci-Think-SFT-7B plus Nemotron mixtures, ending on a feedback-driven 512K-example set targeting measured weaknesses. DPO follows, with router bias updates and the auxiliary load-balancing loss disabled to prevent degradation. RL runs in the Miles framework: 1,400 steps of instruction-following RLVR, then Multi-Teacher On-Policy Distillation to fold that gain back without losing math or code.

Results

The base checkpoint averages 76.7, the strongest among fully open models, ahead of Moonlight-16B-A3B (76.2), SmolLM3-3B-Base (70.5), OLMo-3-7B (70.1), and OLMoE-1B-7B (61.9). It trails Qwen3.5-4B-Base (79.5). It leads on WinoGrande (86.5) and scores 65.7 on HumanEval+. Long-context averages are 41.5 on HELMET and 79.4 on RULER.

Post-training climbs from SFT (71.58) to DPO (72.67) to Think (73.22), above Olmo3-7B-Think (71.97), Gemma-4-E4B think (70.47), and Qwen3.5-4B (69.73). IFEval rises from 77.08 to 83.70.

Interactive explainer

&

Key Takeaways

16B total parameters, 2.8B active per token: 2 shared plus 6 of 64 routed experts.

Gated MLA and FarSkip-Collective give a 12.7% training speedup and 39.2% lower TTFT.

Trained end-to-end on AMD Instinct MI300X and MI325X with ROCm, Primus, and Miles.

Base averages 76.7 and Think averages 73.22, both leading fully open peers.

ResearchRAIL weights limit commercial use; the MIT-licensed training code does not.

Check out the ROCm blog, Hugging Face collection and GitHub. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

Sources: ROCm blog · Hugging Face collection · GitHub

The post AMD Releases Instella-MoE-16B-A3B: A Fully Open Mixture-of-Experts LLM With 2.8B Active Parameters Trained On Instinct GPUs appeared first on MarkTechPost.