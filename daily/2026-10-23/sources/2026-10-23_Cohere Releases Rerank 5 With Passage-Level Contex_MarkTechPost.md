---
publish_time: 1792686691
link: https://www.marktechpost.com/2026/10/22/cohere-rerank-5-context-focus/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cohere 发布重排序模型家族 Rerank 5（Pro 与 Fast 两档），在检索结果送入 LLM 前重排；新增 Context Focus（返回文档内相关段落）与校准相关性分数两项能力，面向 RAG 与 Agent 构建者「向 LLM 发送更少更好的 Token」，支持托管、Foundry、SageMaker 及私有 VPC/本地部署。
---

# Cohere发布Rerank 5重排序模型

> 原文链接：https://www.marktechpost.com/2026/10/22/cohere-rerank-5-context-focus/
> 来源：MarkTechPost

Cohere AI has released Rerank 5, a new reranker family in Pro and Fast tiers. Cohere Rerank 5 is a retrieval model that reorders search results before they reach an LLM. It adds 2 developer features: Context Focus, which returns relevant passages inside each document, and calibrated relevance scores. For RAG and agent builders, the message is simple. Send fewer, better tokens to the LLM.

TL;DR

Size: Parameter count not disclosed. 32K token context window. Two tiers: rerank-v5.0-pro and rerank-v5.0-fast.

Runs on: Hosted API, Model Vault, Microsoft Foundry, Amazon SageMaker, or private VPC and on-prem. Cohere benchmarks speed on a single NVIDIA A100. No open weights or quantized builds.

Performance: Pro ranks first on 39 of 46 composite datasets in Cohere&#8217;s own evaluation.

Best: Pro scores 82.2 on BRIGHT (RCP-nDCG@10), 5.8 points above Voyage AI Rerank 3.

Worst: Pro median latency is 11.7 s per 96-document request, versus 4.1 s for Fast.

What is new in Cohere Rerank 5?

Rerank 5 ships as two models. Pro targets ranking quality on reasoning-heavy queries and long, domain-specific documents. Fast targets low latency and high throughput for agents running many searches.

Both models support over 100 languages and a 32K context window. They also rerank semi-structured data such as JSON, tables and YAML records. Upgrading needs no re-indexing. Developers change the model parameter and keep their existing keyword, vector or hybrid search.

How does Context Focus work?

Context Focus is an optional feature, off by default. A single Rerank call returns document scores plus scored character spans. Each span carries start and end offsets into the original text. Developers set it through the relevant_spans field, with a threshold and max_spans value.

Cohere tested it on 30 QA datasets. Removing half the retrieved text kept 96% of answer quality. Removing three quarters kept 87%. Cohere says teams can push to 10x less context at some quality cost.

In a search-agent test across 17 datasets, BM25 alone scored 46% accuracy. Adding Rerank 5 Pro raised it to 49%. Context Focus at the default 0.1 threshold cut tokens per task by 19% and reached 57%. At 0.4, tokens fell 34% and accuracy hit 58%. Versus BM25 alone, the full stack used 35% fewer tokens. On 6 deep-search benchmarks, tokens fell 41% and accuracy rose from 39% to 52%.

What do calibrated relevance scores change?

Rerank 5 scores read as probabilities. A score of 0.7 means a 70% chance the document is useful.

Cohere team measured expected calibration error (ECE) against blind human graders and NIST TREC-DL assessors. Rerank 5 scores about 0.06 on both. Voyage AI Rerank 3 scores 0.234 and 0.307. Rerank 4 Pro scores 0.384 and 0.309. In practice, dev teams can filter by threshold instead of a fixed top-k. An agent can also detect when nothing relevant came back.

How does Rerank 5 perform on benchmarks?

All scores below are self-reported by Cohere using RCP-nDCG@10, a Cohere-developed variant of nDCG. Cohere ran the competitor models itself.

Pro leads all four main benchmarks. It scores 92.2 on ViDoRe V3, 90.4 on BEIR, 82.2 on BRIGHT and 87.3 on nanoMTEB. BRIGHT shows the largest jump: 12.4 points over Rerank 4 Pro.

Fast beats Voyage AI Rerank 3 Lite, Qwen3-Reranker-8B and Rerank 4 Pro on all 4. It ties Voyage AI Rerank 3 on ViDoRe V3 at 90.6. It trails it on BEIR, 88.1 versus 88.6.

On parsed PDFs, averaged over 47 datasets, Pro scores 89.9 and Fast 88.5. Voyage AI Rerank 3 scores 88.4. Pro ranks first on 14 of 19 non-English languages in Cohere&#8217;s internal suite. 

&&

How does Rerank 5 compare with competing rerankers?

FeatureCohere Rerank 5 ProCohere Rerank 5 FastVoyage AI rerank-3Voyage AI rerank-3-liteQwen3-Reranker-8BParametersNot disclosedNot disclosedNot disclosedNot disclosed8BContext window32K32K32,00032,00032KLanguages100+100+Not disclosedNot disclosed100+License / accessProprietary API, VPC, on-premProprietary API, VPC, on-premProprietary APIProprietary APIApache 2.0 open weightsAPI price per 1M tokens$0.05$0.02$0.05$0.02Self-hostedPassage extractionContext FocusContext FocusNot disclosedNot disclosedNot disclosedBRIGHT*82.277.576.469.469.8ViDoRe V3*92.290.690.687.985.1BEIR*90.488.188.686.183.8nanoMTEB*87.385.183.980.782.1ECE, human judges* (lower is better)0.0580.0580.2340.226Not disclosed

*Scores are RCP-nDCG@10 or ECE from Cohere&#8217;s Rerank 5 post, measured by Cohere. Not independently verified.

How can developers deploy Rerank 5?

Rerank 5 is generally available on the Cohere API and Model Vault. It also runs on Microsoft Foundry (Pro, Fast) and Amazon SageMaker (Pro, Fast). It is also available to all North users. API pricing is $0.05 per 1M tokens for Pro and $0.02 for Fast. Model Vault lists $4.00 per instance-hour for both tiers on its Medium tier.

Integrations include LangChain, Haystack, Elasticsearch and Weaviate, per Cohere&#8217;s integration docs.

Key Takeaways

Rerank 5 ships in Pro ($0.05) and Fast ($0.02) per 1M tokens, both with 32K context.

Pro scores 82.2 on BRIGHT, 5.8 points above Voyage AI Rerank 3.

Context Focus returns scored passages in 1 call, cutting agent tokens 35% to 41%.

Calibrated scores reach about 0.06 ECE, so 1 threshold works across domains.

All benchmarks are self-reported on Cohere&#8217;s RCP-nDCG@10 metric.

Check out the official announcement, the Rerank 5 changelog and the full results sheet. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Cohere Releases Rerank 5 With Passage-Level Context Focus and Calibrated Scores appeared first on MarkTechPost.