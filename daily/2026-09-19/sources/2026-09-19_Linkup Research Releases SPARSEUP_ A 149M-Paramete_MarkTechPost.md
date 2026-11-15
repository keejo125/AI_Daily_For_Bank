---
publish_time: 1789804118
link: https://www.marktechpost.com/2026/09/19/linkup-research-releases-sparseup/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Linkup Research 发布开源稀疏向量模型 SPARSEUP，基于 1.49 亿参数 ModernBERT 骨干，采用 Apache 2.0 协议，在 BEIR-13 上平均 nDCG@10 达 56.4，团队称其为 1.5 亿参数以下最强的公开词表式稀疏编码器。与主流稠密向量不同，稀疏模型输出词表上的权重，可天然对接倒排索引且人类可读，对罕见词匹配更友好；权重已上 Hugging Face，可通过 Transformers 或 Sentence Transformers 加载（trust_remote_code=True）。
---

# Linkup Research 发布 SPARSEUP：1.49 亿参数开源稀疏向量模型

> 原文链接：https://www.marktechpost.com/2026/09/19/linkup-research-releases-sparseup/
> 来源：MarkTechPost

Linkup research team releases SPARSEUP, an open-source learned sparse embedding model. The model runs on a 149M-parameter ModernBERT backbone and ships under Apache 2.0. Linkup team reports 56.4 average nDCG@10 on BEIR-13. It calls this the strongest public vocabulary-based sparse encoder it knows of under 150M parameters.

Is it deployable? Yes. The weights are on Hugging Face under Apache 2.0. The model loads through Transformers or Sentence Transformers with trust_remote_code=True. 

Why a Sparse Model, and Why Now

Most open retrieval models are dense: 1 vector per text. Sparse models output weights over a vocabulary instead. Each dimension maps to a real token, so vectors fit inverted indexes and humans can read them. They also tend to match rare words well.

The trigger was LightOn&#8217;s DenseOn and LateOn release. LightOn published open data, a training recipe, a dense model and a late-interaction model. SPARSEUP fills the missing sparse slot. It uses the same backbone family and fine-tuning data, so all 3 retrieval styles can be compared side by side.

How is SPARSEUP Built

Training starts from LateOn-unsupervised. That checkpoint had no MLM head, so the team grafted back ModernBERT&#8217;s original one. Fine-tuning used LightOn&#8217;s fine-tuning mixture with contrastive learning only. Each query gets 7 hard negatives sampled from a pool of 50, and in-batch negatives. There is no cross-encoder distillation, and training fits on a single H100.

A vanilla SPLADE on this backbone produced huge bags full of stopwords. Linkup fixed this with 3 changes:

Logit shifting: The encoder computes log(1 + ReLU(x - 15)). ModernBERT&#8217;s MLM logits sat too high, saturating the log and making bags dense at initialization.

Per-position top-k: Each input token keeps only its 12 strongest vocabulary dimensions before max pooling. This caps expansion per token, not total vector size.

Case folding: Byte-level BPE stores heat, Heat, Ġheat and ĠHeat as separate ids. SPARSEUP folds them onto 1 id and keeps the largest weight. Output dimensions drop from about 50k to about 34k.

Queries and documents take [Q] and [D] prefixes, and scoring is a dot product. Evaluation max lengths are 128 tokens for queries and 512 for documents.

&

Benchmark Results

Against other sparse encoders on BEIR-13 (nDCG@10, without MS MARCO), per the model card:

ModelBEIR-13 avgSPARSEUP56.4opensearch-neural-sparse-encoding-doc-v3-gte54.6opensearch-neural-sparse-encoding-v152.44ModernBERT-VT52.4splade-v351.7granite-embedding-30m-sparse50.6LACONIC-1B (1B parameters, different size class)58.7

The controlled comparison is less flattering. With backbone and data fixed, LateOn scores 58.9, DenseOn 57.9 and SPARSEUP 56.4. SPARSEUP uses approximate Seismic search, while LightOn reports exact search. SPARSEUP wins ArguAna and Touché and beats DenseOn on HotpotQA. It lags on more semantic sets, with FiQA showing the largest gap. DBPedia is another weak spot.

On decontaminated BEIR, the gap to DenseOn shrinks to 0.17 points. Linkup warns that decontaminated NQ and MS MARCO have only 21 and 46 queries, so those results are noisy. 

Speed and Sparsity

On MS MARCO, SPARSEUP averages 47 non-zero terms per query and 190 per document. SPLADE-v3 averages 25 and 170. With the Seismic inverted index, it reaches over 97% recall against exact search in about 380 microseconds per query, single-threaded. Linkup says inflating vector size could add 1 to 2 BEIR points, but it chose to stay sparse.

Key Takeaways

SPARSEUP is Linkup Research&#8217;s first open model: a 149M-parameter sparse encoder under Apache 2.0.

It scores 56.4 nDCG@10 on BEIR-13, top among public sparse encoders under 150M, per Linkup.

3 fixes drive it: a logit shift of 15, top-12 expansion per token, and case folding.

With identical data, it trails DenseOn by 1.52 points and LateOn by 2.5 on BEIR-13.

It reaches over 97% recall in about 380µs per query with Seismic on MS MARCO.

Check out the Model Weights and Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Linkup Research Releases SPARSEUP: A 149M-Parameter Open-Source Sparse Embedding Model appeared first on MarkTechPost.