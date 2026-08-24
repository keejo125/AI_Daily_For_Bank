---
publish_time: 1787579819
link: https://www.marktechpost.com/2026/08/24/google-research-introduces-me-pois-a-mobility-informed-framework-that-adds-how-a-place-is-used-to-text-based-poi-embeddings/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google Research 与 USC 发布 ME-POIs（Mobility-Embedded POIs）框架，把聚合人类出行数据融入基于文本的 POI（兴趣点）嵌入。语言模型能描述「场所是什么」，却说不清「怎么被使用」——两家咖啡店类目相同，一家做通勤周转、一家留客 90 分钟。ME-POIs 将每次访问表示为坐标+到达/离开时间三元组，经 Space2Vec、Time2Vec 与 4 层 Transformer 编码，用对比学习对齐到每个 POI 的可学习原型；对长尾 POI 以多带宽高斯核+KL 项迁移。在洛杉矶/休斯顿地图增强任务中 34/35 配对提升，访问意图 F1 相对涨 81.9%、繁忙度 MAE 降 24.7%；纯出行变体甚至在价格分级上超越 Gemini 文本嵌入。模型约 5370 万参数、单张 V100 可训，但无公开代码/权重，门槛在出行数据授权。
---

# Google Research 推出 ME-POIs：为文本 POI 嵌入加入「场所如何被使用」的出行信息框架

> 原文链接：https://www.marktechpost.com/2026/08/24/google-research-introduces-me-pois-a-mobility-informed-framework-that-adds-how-a-place-is-used-to-text-based-poi-embeddings/
> 来源：MarkTechPost

A team from Google Research and USC has released Mobility-Embedded POIs (ME-POIs), a framework that folds aggregate human movement into text-based place embeddings. The premise is that language models describe what a place is, but not how it is used. Two coffee shops can share a category, an address block, and a text vector, while one runs commuter turnover and the other holds customers for ninety minutes. ME-POIs encodes each visit as a contextualized vector, then uses contrastive learning to align those visits with one learnable prototype per POI. Across five map-enrichment tasks on Los Angeles and Houston mobility data, adding ME-POIs to strong text encoders improved 34 of 35 model-task pairings in Los Angeles, with relative gains up to 81.9% F1 on visit intent and a 24.7% MAE reduction on busyness. Notably, a variant trained on mobility alone beat Gemini embeddings on price-level classification.

Is it deployable?

Partially, it is a framework you rebuild, not a checkpoint you download. As of publication, Google Research has released the paper but no public code or weights. The compute bar is low: the model is ~53.7M parameters and was pretrained on a single NVIDIA Tesla V100 16GB. The real gate is data — you need licensed foot-traffic or first-party visit logs plus POI polygons.

How the framework works

Each visit is a triple: coordinates, arrival time and departure time. Three factorized encoders handle them: Space2Vec for multi-scale location, and two Time2Vec encoders for arrival and departure separately, so start time and dwell duration stay distinguishable. The concatenated vectors get sinusoidal positional encoding and pass through a 4-layer, 8-head Transformer (d_h = 512) to produce contextualized visit embeddings.

The core objective is contrastive. Every POI owns a learnable prototype, and an InfoNCE loss pulls each visit embedding toward its own POI&#8217;s prototype while pushing away the other POIs in the minibatch. The prototype becomes a functional centroid that averages out individual user schedules.

Sparsity is the hard part. Only 9.07% of Los Angeles POIs and 7.04% of Houston POIs cleared the anchor threshold (100 and 50 total visits respectively). For the long tail, ME-POIs computes normalized Gaussian kernels at three bandwidths — 0.3 km, 1.0 km, 3.0 km — and transfers anchor visit histograms to sparse POIs, then adds a KL term forcing the sparse embedding to predict that prior. A second KL term supervises anchors against their own empirical distributions. A fourth loss maximizes cosine similarity with projected text embeddings, whose prompts follow the GeoLLM recipe: coordinates, category, address, and the ten nearest POIs with distance and direction.

What the numbers say

Evaluation covers two anonymized mobility datasets — Los Angeles (39,557 POIs, 6.9M visits, full-year 2019) and Houston (28,419 POIs, 715,604 visits, 20 days in March 2020) — across five map-enrichment tasks with frozen-embedding probing. Labels come from SafeGraph for opening hours and closures, and Google Maps for visit intent, busyness, and price level.

Adding ME-POIs improved 34 of 35 model-task pairings in Los Angeles. Peak relative gains: 16.2% F1 on weekly opening hours (OpenAI-large), 81.9% F1 on visit intent (Gemini), 6.5% F1 on permanent closure (E5), and a 24.7% MAE reduction on busyness (Gemini). In Houston, price-level F1 rose 75.1% for GTR-T5. The single regression was Gemini on permanent closure, down 0.4%.

The more interesting result is the mobility-only variant. Trained with no text alignment at all, it reaches 0.600 accuracy on Los Angeles price level against Gemini&#8217;s 0.559 — collective behavior outperforming the words used to label the place. It also beats every trajectory-based baseline on every task.

Explainer: the mechanism, step by step

Key Takeaways

ME-POIs learns one context-independent vector per POI, not a trajectory-conditioned one.

Contrastive alignment plus multi-scale KL transfer fixes the long tail: 91% of LA POIs are sparse.

Gains reach 81.9% F1 on visit intent and 24.7% MAE reduction on busyness.

Mobility-only embeddings beat Gemini text embeddings on price-level classification.

No public code or weights yet; licensed visit data is the real barrier, not compute.

Check out the Paper and Technical details. Feel free to check out our GitHub Page for Tutorials, Codes and Notebooks.

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google Research Introduces ME-POIs: A Mobility-Informed Framework that Adds &#8220;How a Place Is Used&#8221; to Text-Based POI Embeddings appeared first on MarkTechPost.