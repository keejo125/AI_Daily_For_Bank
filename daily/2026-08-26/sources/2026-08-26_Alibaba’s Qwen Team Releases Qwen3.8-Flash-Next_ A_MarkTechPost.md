---
publish_time: 1787757600
link: https://www.marktechpost.com/2026/08/26/alibabas-qwen-team-releases-qwen3-8-flash-next-a-125b-multimodal-moe-with-6b-active-parameters-previewing-the-qwen4-architecture/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  阿里通义千问发布并开源 Qwen3.8-Flash-Next，总参 125B、仅激活 6B，定位为预览 Qwen4 架构的开放权重多模态 MoE。关键改动含 Gated DeltaNet 与 Qwen 稀疏注意力混合、Gated Residual、N-gram 嵌入与 Muon 优化器；训练成本约为 Qwen3.7-Plus 的九分之一。FP8 权重 172.78 GiB，建议 TP4 部署于 GB300，亦可经千问办公与 API 获取。
---

# 阿里通义千问发布 Qwen3.8-Flash-Next：预览 Qwen4 架构的 125B 多模态 MoE 模型

> 原文链接：https://www.marktechpost.com/2026/08/26/alibabas-qwen-team-releases-qwen3-8-flash-next-a-125b-multimodal-moe-with-6b-active-parameters-previewing-the-qwen4-architecture/
> 来源：MarkTechPost

Alibaba&#8217;s Qwen team has released Qwen3.8-Flash-Next, an open-weight multimodal Mixture-of-Experts model built for cost per token. The checkpoint pairs a 125B backbone with a 51B N-gram embedding table and a 4B multi-token prediction module. Only 6B parameters activate per token. The team positions it as an early preview of the architecture that will underpin Qwen4, the same role Qwen3-Next played for Qwen3.5. Four changes carry the release: a Gated DeltaNet and Qwen Sparse Attention hybrid, Gated Residual, N-gram Embedding, and the Muon optimizer. Qwen team reports training cost at roughly one-ninth that of Qwen3.7-Plus. 

Is it deployable?

Yes but not on a workstation. The FP8 checkpoint is 172.78 GiB and the BF16 checkpoint is 335.28 GiB. Per vLLM recipes, TP2 is the minimum validated FP8 configuration on GB300 and TP4 is recommended. On an 8×H200 node, use TEP8; plain TP8 is incompatible with the checkpoint&#8217;s 128-wide quantization blocks. Sparse activation cuts compute, not storage.

https://qwen.ai/blog?id=qwen3.8-flash-next

What is actually new

Qwen3.8-Flash-Next pairs a 125B main model with 51B N-gram embedding parameters and a 4B multi-token prediction module, totaling 180B on disk. Only 6B parameters activate per token. Four changes drive this:

Hybrid attention (GDN + QSA): Three of every four layers use Gated DeltaNet, a linear-attention layer that compresses history into a fixed-size recurrent state. The fourth layer runs Qwen Sparse Attention (QSA), which uses a lightweight indexer to select context at micro-block granularity rather than per token. The layer layout is 12 × (3 × GDN → 1 × QSA) across 48 layers, with a QSA budget of 512 blocks or 2048 tokens.

Gated Residual: The residual stream widens into 4 parallel branches, with an element-wise read gate and a per-branch scalar write gate, at bottleneck rank 320.

N-gram Embedding: A 20,000,000-entry bigram/trigram table at layer 2 adds capacity through deterministic lookups. It can be offloaded to host memory with asynchronous prefetch — though offload currently runs only on NVIDIA devices.

Training recipe.:The Muon optimizer is applied alongside AdamW to specific weight categories, with batch-size warmup eliminated and scaling laws refitted.

The MoE layer carries 512 experts, activating 10 routed plus 1 shared, at expert intermediate dimension 640.

&&

Benchmarks

Qwen reports 58.7 on DeepSWE 1.1, 62.5 on SWE-bench Pro, 81.0 on SWE-bench Multilingual, and 91.9 on LiveCodeBench v6. On agentic tasks it posts 73.9 on CoWorkBench, 55.7 on JobBench, and 73.5 on Toolathlon Verified. Multimodal results include 84.5 on AndroidWorld, 76.6 on LVBench, 88.5 on RealWorldQA, and 95.7 on MathVision with code interpreter.

The model does not lead everywhere. Claude Opus 4.6 (Max) takes HLE at 40.0 against Qwen&#8217;s 35.9, and DeepSeek-V4-Flash-0731 leads NL2Repo-Bench at 54.2 versus 48.1. Frontier reasoning remains the gap.

Efficiency

Qwen states training cost roughly 1/9 that of Qwen3.7-Plus. On serving, the announcement cites QSA kernel speedups of up to 7.6× prefill and 4.9× decode at 1M tokens, while the SGLang cookbook and vLLM recipes cite 10.2× and 6.6×. Treat the range as vendor-reported until independently measured. Qwen also reports 8.6× the prefill throughput of Qwen3.7-Plus at a 90% prefix-cache hit rate.

Context is 262,144 tokens natively, extensible to 1,000,000 with YaRN.

Running it

The model serves through vLLM, SGLang, TokenSpeed, transformers serve, and llama.cpp for GGUF quants. Fine-tuning is supported via Unsloth, Swift, and LLaMA-Factory. It already powers the &#8220;Standard&#8221; mode on QwenWork and works with Qwen Code.

Thinking mode is on by default, with reasoning_effort at xhigh, medium, or low. Qwen recommends temperature 1.0 and top_p 0.95 for thinking mode, and temperature 0.7 with top_p 0.80 for instruct mode.

Key Takeaways

125B backbone + 51B N-gram embeddings + 4B MTP, with only 6B parameters active per token.

Three of four layers use Gated DeltaNet; the fourth runs Qwen Sparse Attention at micro-block granularity.

Trained at roughly 1/9 the cost of Qwen3.7-Plus, with 262K native context extensible to 1M via YaRN.

FP8 weights are 172.78 GiB, so self-hosting needs a multi-GPU node, not a workstation.

Licensed under qwen-community-1.0, not Apache-2.0 — verify terms before commercial use.

Check out the GitHub Page, HF Model Card and Technical Details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Alibaba&#8217;s Qwen Team Releases Qwen3.8-Flash-Next: A 125B Multimodal MoE With 6B Active Parameters Previewing the Qwen4 Architecture appeared first on MarkTechPost.