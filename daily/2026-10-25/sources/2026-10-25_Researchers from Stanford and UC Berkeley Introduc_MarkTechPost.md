---
publish_time: 1792930338
link: https://www.marktechpost.com/2026/10/25/stanford-berkeley-tokengate-learned-token-pruning-llm-prefill/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  斯坦福与 UC 伯克利研究者发布 TokenGate，一个为长上下文预填充设计的“即插即用”模块：通过可学习的 token 剪枝，让现有 LLM 略读输入、只让关键 token 走完整计算。团队报告首 token 延迟（TTFT）提升 1.4×—11.3× 且无精度损失，峰值预填充显存下降 1.5×—3.4×；代码与 Apache-2.0 权重已开源。方法在 Qwen3-1.7B / Qwen3.5-2B 上加一个小型 MLP 门控与 LoRA（r=16），在 128k 上下文上测试。前向分三阶段：门层以下正常处理全部 token、门控按分数保留 Top-K、门层以上只处理 K 个 token 且不建被剪 token 的 KV 条目。Top-K 不可导，借用 MoE 路由技巧把分数作为注意力 logit 偏置以回传梯度。
---

# 斯坦福与 UC 伯克利提出 TokenGate：长上下文预填充提速最高 11.3 倍

> 原文链接：https://www.marktechpost.com/2026/10/25/stanford-berkeley-tokengate-learned-token-pruning-llm-prefill/
> 来源：MarkTechPost

Stanford and UC Berkeley researchers released TokenGate, a module for long-context prefill. TokenGate learned token pruning lets an existing LLM skim its input. Only the tokens that matter get full processing. The research team reports 1.4x to 11.3x faster time-to-first-token (TTFT) with no accuracy loss. Peak prefill memory drops 1.5x to 3.4x. Code and checkpoints are on GitHub under Apache-2.0.

TL;DR

MLP gate: A small MLP gate and LoRA (r=16) added to Qwen3-1.7B or Qwen3.5-2B.  Tested on contexts up to 128k tokens.

Runs on: Paper timings use 1 A100 at batch size 1. Training used 4 A100s. 

Performance: Pareto-optimal on 5 tasks against 6 baselines.

Best: NIAH 16k at 11.3x faster TTFT and 3.42x lower memory. TTFT gain hits 13.0x at 128k.

Worst: Speedup drops to 1.4x on some tasks. 

What is TokenGate?

TokenGate is a drop-in component that adds trainable token pruning to pretrained LLMs. Transformers push every token through every layer. Attention cost grows quadratically with length. Training-free pruning is cheap but loses accuracy at high pruning rates. Architectural changes often need pre-training from scratch.

How does TokenGate learned token pruning work?

The forward pass splits into 3 phases:

Standard forward: layers below gate layer L process all N tokens as usual.

Gate module: an MLP scores each token from its post-attention residual at layer L. A top-K selector keeps the highest-scoring tokens.

Pruned forward: layers above L process only those K tokens and never create KV entries for pruned ones.

Only the document part of the prompt is prunable. The question is never pruned.

What is token-gated attention?

Top-K selection is not differentiable, which blocks end-to-end training. TokenGate borrows the Mixture-of-Experts router trick. Each kept token&#8217;s score becomes a bias on attention logits above the gate. That bias gives gradients a path back to the scorer.

A learnable per-head gain and a learnable temperature refine this. The temperature corrects for each query seeing fewer keys. Training uses plain next-token loss. Each step averages a full-context loss and a random-budget loss. So 1 trained gate works across budgets.

&&

How does TokenGate perform on benchmarks?

The research team tested Qwen3-1.7B on RepoBench-P, 2WikiMultihopQA, MultiNews, BioDEX and needle-in-a-haystack (NIAH). Baselines were FastKV, SlimInfer, DASH, GemFilter, FlexPrefill and MInference, on the same LoRA backbone.

Versus full prefill: 1.4x to 11.3x faster TTFT and 1.5x to 3.4x lower memory.

Versus the next-best baseline: 1.2x to 6.4x faster TTFT and up to 2.1x lower memory.

2WikiMultihopQA: at 95% of full-context accuracy, prefill runs 3.0x faster with 2.7x less memory.

Longer contexts: a gate trained at 16k reaches 12.8x at 32k and 13.0x at 64k and 128k. Memory savings stay near 3.43x.

The learned selector beats FastKV&#8217;s heuristic at the same layer. Even random-K selection scores higher on the TokenGate backbone. The research team credits backbone co-adaptation.

Does it work on hybrid-attention models?

Yes, Qwen3.5-2B mixes Gated DeltaNet and full-attention layers. On NIAH 32k, TokenGate at layer 3 matched full-prefill accuracy. It ran 3.8x faster than full prefill and 2.1x faster than FastKV. Gating at layers 1 or 2 reached 7.8x, within 6% accuracy. FastKV can only prune attention layers.

TokenGate vs FastKV, SlimInfer, GemFilter and DASH

FeatureTokenGateFastKVSlimInferGemFilterDASHToken selectionLearned MLP gateAttention from last queriesBlock attention, multi-stageLast-query attention at filter layerHidden-state stabilityTraining neededYes (gate + LoRA r=16)NoNoNoNoPruning layer in TokenGate&#8217;s Qwen3-1.7B runs113 (default)8, 17, 251211Prunes at Gated DeltaNet layersYesNo (attention layers only)Not disclosedNot disclosedNot disclosedBest self-reported prefill gain (own setup)11.3x TTFT, 3.4x memory1.82x prefill2.53x TTFT (LLaMA3.1-8B, RTX 4090)2.4x speed, 30% less GPU memory vs SOTANot disclosedCodeGitHubGitHubGitHubGitHubAnnounced

Self-reported gains use different setups, so they are not directly comparable. Pruning layers come from TokenGate&#8217;s Appendix C.2.

How do you deploy TokenGate?

The GitHub Repo needs Python 3.10+ and CUDA PyTorch 2.9+. An optional FlashAttention-2 key-bias kernel speeds up dense Qwen3. It costs 1.0x to 1.1x a plain call. Without it, inference falls back to FlexAttention.

A {state} placeholder marks the prunable document. generate takes a max_kept_prefill_tokens budget. Checkpoints cover all 5 tasks on Qwen3-1.7B, plus a Qwen3.5-2B NIAH gate. Example: liana313/tokengate-niah-qwen3-1.7b.

Training mirrors a TRL/PEFT recipe. Each step is 1.3x slower than plain LoRA. Runs converged faster on 4 of 5 tasks. Mean training time was 1.8 versus 2.2 A100 hours.

Key Takeaways

TokenGate adds learned token pruning to existing LLMs via a small gate and LoRA.

Prefill runs 1.4x to 11.3x faster with 1.5x to 3.4x lower peak memory.

Token-gated attention makes top-K selection trainable, MoE-router style.

It beats the next-best pruning baseline by up to 6.4x on TTFT.

It works on hybrid Qwen3.5-2B, where FastKV cannot prune DeltaNet layers.

Check out the Paper, GitHub repo and Hugging Face paper page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Researchers from Stanford and UC Berkeley Introduce TokenGate: Token-Gated Attention Makes Long-Context Prefill Up to 11.3x Faster appeared first on MarkTechPost.