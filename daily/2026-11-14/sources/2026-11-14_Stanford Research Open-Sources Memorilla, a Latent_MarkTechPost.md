---
publish_time: 1794651681
link: https://www.marktechpost.com/2026/11/14/stanford-memorilla-memory-system-16-memory-tokens/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  斯坦福SNAP团队（含多伦多、宾大、MIT合作者）开源Memorilla——一个为冻结LLM注入“潜在记忆”的模块。它将整个文档集合压缩为固定的16个记忆token，前置到Qwen3-8B输入，编码端Qwen3-Embedding-4B与解码端Qwen3-8B均冻结，仅训练1.94亿参数的记忆模块。在8项基准上，冻结Qwen3-8B配合Memorilla的FactKG准确率达84.33%（全上下文80.43%），平均49.68居首，且较全上下文快约27倍；NarrativeQA上16 token替代6.7万文档token，压缩达4212倍。代码、训练配方与检查点以Apache 2.0公开。
---

# 斯坦福开源 Memorilla：面向冻结 LLM 的潜在记忆模块

> 原文链接：https://www.marktechpost.com/2026/11/14/stanford-memorilla-memory-system-16-memory-tokens/
> 来源：MarkTechPost

Stanford researchers have released Memorilla, an open-source memory system for LLMs. The Memorilla memory system reads a whole document collection and hands a frozen LLM just 16 memory tokens. On FactKG, a frozen Qwen3-8B scored 84.33% with Memorilla, against 80.43% with every document in context. It did that with 108x fewer document tokens. Code, training recipes and checkpoints are public under Apache 2.0. You can check the deployment options and specs here through our GPULeaderboard.com chrome extension.

TL;DR

Size: 194M-parameter trainable memory module. It always outputs 16 memory tokens, whatever the collection size. The encoder (Qwen3-Embedding-4B) and decoder (Qwen3-8B) stay frozen.

Runs on: Linux with CUDA GPUs and Python 3.11. The quickstart needs 1 GPU with 80 GB (recipes ran on H100 80GB). No quantized variants disclosed.

Performance: Highest reported average across 8 benchmarks (49.68), top score on 5 of 8.

Best: PersonaMem-v2 accuracy of 44.60%, versus 27.92% for full context.

Worst: PubMedQA accuracy of 59.00%, versus 69.00% for LLMLingua-2.

What is Memorilla?

Memorilla is a memory module that turns a document collection into 16 vectors for a frozen LLM. The work comes from Jure Leskovec&#8217;s SNAP group, with co-authors from Toronto, Penn and MIT.

A frozen LLM can only use what sits in its context window. Full-context prompting grows slower as history grows. Retrieval pastes the chunks most similar to the question, and can miss weaker clues. Memorilla takes a third route: it learns what each question needs from the whole store.

How does Memorilla work?

The pipeline has 3 steps:

Encode once. A frozen Qwen3-Embedding-4B embeds each document a single time. New documents never force re-encoding of old ones.

Read per question. 16 learned slots attend to the question and the full store. The module uses 2 cross-attention layers with 8 heads.

Inject. The slots are projected into Qwen3-8B&#8217;s input embedding space and prepended to the question.

Only the memory module trains: 194,123,776 parameters for the 8B decoder. Training runs in 3 stages. Stage 1 uses about 1.98M Wikipedia paraphrase-reconstruction examples. Stage 2 adds about 1.34M examples from 10 QA and summarization datasets. Stage 3 fine-tunes on all 8 benchmarks. The full recipe takes about 19 hours on 4 H100 GPUs.

How does Memorilla perform on benchmarks?

All baselines use the same frozen Qwen3-8B, per the paper&#8217;s main table. Scores are self-reported by the research team.

FactKG: 84.33% accuracy, versus 80.43% full context and 80.38% MemoRAG.

PersonaMem-v2: 44.60%, versus 30.90% for xRAG, the next best method.

TriviaQA: 57.00 exact match, just ahead of MemoRAG at 56.60.

LaMP-4 / LaMP-7: 18.15 and 48.37 ROUGE-L, both the best scores.

Average: 49.68, versus 41.92 for xRAG, 40.75 for LLMLingua-2 and 38.02 for Mem0.

Memorilla loses on 3 benchmarks. On PubMedQA it scores 59.00%, while LLMLingua-2 reaches 69.00%. Those abstracts total only 324 tokens, so compression has little to gain. MemoRAG leads on PersonalizationV4 (67.88% vs 66.65%) and NarrativeQA ROUGE-L (20.51 vs 19.31). MemoRAG used about 690x and 50x more document tokens there.

Compression peaks on NarrativeQA: 16 tokens replace 67,385 document tokens, a 4,212x cut. As agent memory, 8 memory tokens lift a Qwen3-4B TextWorld agent from 18.6% to 24.2% average success.

&&&

How fast is Memorilla compared to full context?

On 1 H100, Memorilla answers in 0.74 s at 512 documents (about 128K tokens). Full context slows from 0.75 s to 19.9 s, which is 27x slower. The memory module itself takes about 2 ms.

An optional memory cache precomputes cross-attention keys and values. On 1 B200, a question then takes 8.1 ms at 1M documents and 33 ms at 4M. With torch.compile, the 1M case drops to 5.0 ms. The cache costs 80 GiB at 4M documents.

How do you run Memorilla?

Install with uv on Linux, then load MemoryVLLM.from_pretrained. The first run downloads about 25 GB of models. Checkpoints live at memorilla/Memorilla-Qwen3-8B as Stage 1, 2, 3, PV4 and PMv2 folders.

Each checkpoint must run with the decoder it was trained with (evaluation docs). Custom data needs parquet files with collection_id, question, answer and documents columns. The research team also released PersonalizationV4: 149 synthetic users, 200 conversations each, under CC BY 4.0.

Memorilla vs Mem0, MemoRAG and xRAG

Benchmark scores come from Memorilla&#8217;s paper, which ran every baseline on the same Qwen3-8B. Licenses come from each project&#8217;s repository.

Memorilla (paper)MemoRAG (repo)Mem0 (repo)xRAG (repo)ApproachLearned latent memory tokensMemory model guides retrievalExtracted text memories1-token RAG compression (paper)Doc tokens per query (geo. mean)167842121What the LLM reads16 soft memory embeddingsRetrieved textRetrieved memory text1 projected embeddingLicenseApache 2.0Apache 2.0Apache 2.0Not disclosedFactKG (Acc)84.3380.3872.7978.98PersonaMem-v2 (Acc)44.6028.7627.4830.90PubMedQA (Acc)59.0067.0024.0036.00NarrativeQA (ROUGE-L)19.3120.5113.8016.92Average, 8 benchmarks49.6847.52 (our calc.)38.0241.92

Key Takeaways

16 memory tokens replace whole document collections for a frozen Qwen3-8B.

FactKG: 84.33% vs 80.43% full context, with 108x fewer tokens.

Highest reported 8-benchmark average: 49.68.

Weak spot: PubMedQA at 59.00% and fine-grained facts.

Apache 2.0 code; 194M-parameter checkpoints on Hugging Face.

Check out the paper, browse the GitHub repo, and download the checkpoints. You can check the deployment options and specs here through our GPULeaderboard.com chrome extension.

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Stanford Research Open-Sources Memorilla, a Latent Memory Module for Frozen LLMs appeared first on MarkTechPost.