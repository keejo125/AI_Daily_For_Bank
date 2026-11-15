---
publish_time: 1793668189
link: https://www.marktechpost.com/2026/11/02/zyphra-hierarchical-attention-zha-sparse-attention/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Zyphra 发布分层注意力 ZHA，一种围绕树状结构化索引器构建的稀疏注意力方法，针对稀疏注意力长期短板——挑选 token 的索引器仍需全上下文扫描。技术论文显示，ZHA 可用约 4B token 蒸馏进冻结预训练模型；在 Qwen3.6-35B-A3B 上，推理、智能体编程与 256K 检索基准接近稠密注意力。该方法仅向模型增加约 81920 个可训练参数（约 0.00024%），已测至 256K 上下文。
---

# Zyphra 发布分层注意力 ZHA，迈向真正亚二次方注意力

> 原文链接：https://www.marktechpost.com/2026/11/02/zyphra-hierarchical-attention-zha-sparse-attention/
> 来源：MarkTechPost

Zyphra has released Zyphra Hierarchical Attention (ZHA), a sparse attention method built around a tree-structured indexer. ZHA targets a known gap in sparse attention: the indexer that picks tokens still scans the whole context. Zyphra&#8217;s technical paper shows ZHA can be distilled into frozen pretrained models with about 4B tokens. On Qwen3.6-35B-A3B it stays close to dense attention on reasoning, agentic coding and 256K retrieval benchmarks.

TL;DR

Size: It is a method that adds 81,920 trainable parameters to Qwen3.6-35B-A3B (about 0.00024%). Tested up to 256K context.

Runs on: Retrofits frozen pretrained models after a 4B-token KL warmup at 32K context. Speedups come from a modeled H100 BF16 roofline. No optimized kernels released. An FP4 router variant was also tested.

Performance: Within a few points of dense attention on 7 reasoning, coding and retrieval benchmarks.

Best: LongBench v2 hits 63.4% (deep tree) vs 58.0% dense, using about 1.1% of keys.

Worst: On NoPE-based Nemotron-3.5-Lightning-30B-A3B, deep-tree RULER-13 drops 25.3 points below dense.

What is Zyphra Hierarchical Attention (ZHA)?

ZHA is a sparse attention method from Zyphra that finds relevant keys by searching a tree. It keeps the full KV cache. The tree only decides which cached keys each query reads.

Fixed-state methods like SSMs and sliding windows saturate at long contexts. Fine-grained sparse methods like DeepSeek Sparse Attention score every past token with an indexer. The final attention is sparse, but the indexer still grows with the full context.

Near 1M tokens, cited work shows indexing takes 60 to 90% of layer time. ZHA makes the search itself sparse.

How does ZHA&#8217;s tree indexer work?

Building the tree

ZHA splits keys into contiguous chunks and compresses each chunk into a summary key. Summaries are grouped and compressed again, level by level. With chunk size 4, 6 levels cover 4,096 tokens per top node.

Summaries come from a small set of learned reference queries. Each reference query gives a tangent-plane estimate of a chunk&#8217;s log attention mass. The max over these planes approximates how much attention any future query would give the chunk.

How does top-p routing pick tokens?

At decode time, a query scores the top-level nodes. It keeps the smallest set holding a fraction p of estimated attention mass. It then expands only those children, repeating until it reaches raw KV entries.

Top-p makes the budget adaptive. A single-fact lookup touches few branches. A query that needs many scattered facts expands more. The first token is always kept as an attention sink.

How does ZHA perform against dense attention and MSA?

Zyphra team converted Qwen3.6-35B-A3B with 2 trees: deep (chunk 4, 6 levels) and wide (chunk 256, 1 level). Both use 16 reference queries and p = 0.95. It also trained a MiniMax Sparse Attention (MSA) indexer on 40B tokens, 10x ZHA&#8217;s budget.

Benchmark (Qwen3.6-35B-A3B)DenseZHA deepZHA wideMSAAIME 202693.191.290.891.7SWE-bench Verified67.467.468.463.6Terminal-Bench 2.149.946.753.346.1MMLU-Pro84.985.385.285.3GPQA Diamond84.885.085.083.1RULER-13 (256K)96.093.396.277.1LongBench v2 (thinking)58.063.462.449.3

Source: arXiv 2610.42112, Figure 5. All numbers self-reported by Zyphra.

The biggest gap is on retrieval. MSA drops to 77.1% on RULER-13, while both ZHA trees stay above 93%. On LongBench v2, the deep tree and MSA read similar key shares (1.1% vs 1%). The deep tree scores 14.1 points higher.

Across 28 tree geometries, RULER accuracy held steady when attending to 10 to 30% of keys. At fixed compression, deeper trees kept accuracy at higher sparsity. A 4-parameter model predicts RULER accuracy from geometry with 1.44-point RMSE.

How fast is ZHA?

Zyphra released no kernels. It modeled decode latency for one layer at batch size 1 with a roofline. The lightweight setting uses 1 reference query, chunk 8 and p = 0.75.

In that model, ZHA beats dense attention near 48K tokens and MSA near 0.48M tokens. At 1B tokens, projected speedups reach 373 to 417x over dense and 52 to 58x over MSA. The blog post adds 32 to 35x and 4.7 to 5.1x at 10M tokens.

At 256K, the modeled gains are modest. Pareto-frontier settings reach 1.93x to 2.28x over dense, at 92.7 to 96.4% RULER-13. Routing and selection add their own cost.

How is ZHA trained onto existing models?

The base model stays frozen. Only the reference queries train. A KL loss matches dense attention mass per chunk at every level. Qwen and Nemotron runs used 3.98B tokens over 1,900 steps at 32K context.

Zyphra reports models under 1B parameters struggled during conversion. Results improved sharply at 4B and above.

ZHA vs MSA, DSA and NSA

FeatureZHA (Zyphra)MSA (MiniMax)DSA (DeepSeek)NSA (DeepSeek)IndexerMulti-level tree of compressed keysFlat block indexer per GQA groupLightning indexer, token levelCompression + selection + sliding windowSelection ruleTop-p per level (adaptive)Top-16 blocks of 128 tokensTop-2,048 tokens16 blocks of 64 tokens, 512 windowIndexer costSublinear per query (claimed)Quadratic index branchScores every cached keyNot disclosedAdded to pretrained modelYes, ~4B tokens, backbone frozenYes, 400B-token CPTContinued training of V3.1-TerminusNative pretrainingLargest model shown35B MoE (Qwen3.6-35B-A3B)109B MoE, 6B active685B MoE27B MoE, ~3B activeReported speedupModeled only (H100 roofline)14.2x prefill, 7.6x decode at 1M (H800)Not disclosedSpeedups at 64K, figure only

Key Takeaways

ZHA searches the KV cache with a tree, not a flat scan.

Only 81,920 parameters train on a frozen 35B model.

Wide tree hits 96.2% on RULER-13 at 256K vs 96.0% dense.

MSA falls to 77.1% on the same RULER test.

Billion-token speedups are projections, not measurements.

Check out the ZHA paper on arXiv and Zyphra&#8217;s technical blog. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Zyphra AI Introduces Zyphra Hierarchical Attention (ZHA): A Path to True Subquadratic Attention appeared first on MarkTechPost.