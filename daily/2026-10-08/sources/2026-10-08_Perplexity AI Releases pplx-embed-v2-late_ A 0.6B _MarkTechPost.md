---
publish_time: 1791437949
link: https://www.marktechpost.com/2026/10/07/perplexity-ai-releases-pplx-embed-v2-late-a-0-6b-edge-model-and-a-9b-model-scoring-92-4-on-madqa/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Perplexity 发布 pplx-embed-v2-late，包含两款 embedding 模型：一款 0.6B 的边缘（edge）模型与一款 9B 模型，其中 9B 模型在 MADQA 基准上取得 92.4% 的得分。该发布补足了 Perplexity 在检索/向量表示环节的自研能力，并兼顾端侧轻量化部署需求。
---

# Perplexity 发布 pplx-embed-v2-late：0.6B 边缘模型与 9B 模型 MADQA 得分 92.4%

> 原文链接：https://www.marktechpost.com/2026/10/07/perplexity-ai-releases-pplx-embed-v2-late-a-0-6b-edge-model-and-a-9b-model-scoring-92-4-on-madqa/
> 来源：MarkTechPost

Perplexity has released pplx-embed-v2-late, a pair of ColBERT-style multimodal embedding models. They come in 2 sizes: 0.6B for fast, cheap queries and 9B for maximum quality. Both models retrieve text, images and rendered PDF pages, and they share one embedding space.

Is it deployable? Yes, if you host it yourself. Both models are on Hugging Face under the MIT license. A hosted Perplexity API endpoint is planned but not live.

TL;DR

The best

The 0.6B model uses about 340M active parameters for images and stays close to 8B rivals.

A 9B index can be searched with 0.6B queries, recovering about half the 9B quality gap on text at 0.6B query cost.

Its 128-dim token vectors are 16x to 32x narrower than rivals at 2,048 to 4,096 dims.

MIT license, with commercial use allowed.

The worst

It stores 1 vector per token, so index size grows with document length.

It is not #1 on ViDoRe v3 image retrieval; Tencent&#8217;s EVIE scores higher.

A single input cannot mix text and images.

All scores are self-reported, and the technical report is not out yet.

Model Size and What It Runs On

Metricspplx-embed-v2-late-0.6bpplx-embed-v2-late-9bTotal parameters594M9B (Hugging Face lists 8B)Active parameters~240M text, 340M image7.4BBase modelQwen3.5-0.8B, pruned to 12 text layersQwen3.5Output128 dims per token128 dims per tokenWeights in memory (bf16, our estimate)~1.2 GB~16 to 18 GBIntended machineLaptop, edge device or small GPUDatacenter or high-memory GPUPerplexity&#8217;s suggested roleLive query encoder, 100% localBuilding the document index

Perplexity designed the 0.6B model as a lightweight query encoder that can also run on edge devices. Both model cards show CUDA GPU usage. They need sentence-transformers >= 6.0.0 and transformers >= 5.4.0. The memory figures are our estimate at 2 bytes per parameter, for weights only. The published checkpoints are stored in F32, which doubles the download size.

How Well It Performs: Best and Worst Scores

All numbers below are from Perplexity&#8217;s announcement:

Benchmark0.6B9BWhere it standsMADQA (agentic PDF QA, accuracy)90.1%92.4% (best)Beats Mixedbread&#8217;s retriever (88.9%); trails Mixedbread Agentic Search (93.4%)Domain-specific text (72 tasks, nDCG@10)78.0%81.3%9B leads all tested models by 1.6pp; 0.6B is 0.3pp behind gemini-embedding-2Q2D-Web (Recall@1000)73.6%74.8%Both beat the previous best of 69.3%ViDoRe v3 image (nDCG@10)62.3%65.2%0.6B is within 1.2pp of nemotron-colembed-v2-8b; EVIE leadsViDoRe v3 Markdown (nDCG@10)61.2% (worst)64.7%Both beat every external model testedBrowseComp+ (accuracy)Not given64.0% (lowest)Still 4.9pp above the next ColBERT model

The strongest result: 92.4% on MADQA, set by the 9B model. The biggest margin is on BrowseComp+, at 8.7pp over the best dense model.

The weakest result: 61.2% on ViDoRe v3 Markdown, from the 0.6B model. It is still the 2nd-best score on that benchmark. Image search is the real gap: Gemini Embedding 2 beats the 9B model on MIRACL-Vision and by 2pp on PPLX-Q2I.

Mixing sizes: a 9B index queried by the 0.6B model scored 63.5% on ViDoRe v3 image retrieval. That beats 62.3% with 0.6B on both sides, at the same query cost.

How It Works

Dense models compress a document into 1 vector. pplx-embed-v2-late instead keeps a 128-dim vector for every token. It scores with MaxSim: each query token finds its best document token, and those maxima are summed. Pages are encoded as images, so no OCR step is needed. Perplexity distilled both models from an 18B teacher using LEAF-style token-level training. That training is what creates the shared space.

Best Use Cases

The best fit is visual document search over PDFs, slides and scanned reports. 

Low-latency search: index in the cloud with 9B, then query on-device with 0.6B. 

Agentic RAG over large PDF or web collections.

Interactive Explainer

&

How It Compares

Featurepplx-embed-v2-lateNVIDIA nemotron-colembed-vl-8b-v2TopK topk-embed-v1Google Gemini Embedding 2Size0.6B, 9B~8.8B0.8B, 2B openNot disclosedVector width128 per token4,096 per token2,048 per token (small)128 to 3,072, 1 vectorInputsText, images, page rendersText queries, page imagesText, page imagesText, image, video, audio, PDFRuns onYour GPU; 0.6B on edgeNVIDIA A100/H100, LinuxCUDA GPU (Ampere+)Google APIShared space across sizesYesNot statedNot statedNot applicableLicenseMITCC-BY-NC-4.0Apache 2.0 (small)Proprietary

Key Takeaways

The 0.6B model fits edge devices; the 9B model is built for index-time quality.

Best score: 92.4% on MADQA. Weakest: 61.2% on ViDoRe v3 Markdown.

0.6B queries over a 9B index beat 0.6B on both sides.

Storage growth and self-reported scores are the main caveats.

Check out the Model weights on HF and Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

[Sponsored] The web is the one API most agents are missing. Databases, calendars and repos have APIs. The open web mostly doesn’t. The TinyFish MCP server gives any MCP client four tools: TinySearch, TinyFetch (full pages as markdown, JavaScript included), TinyBrowser for logins and forms, and TinyAgent for multi-step jobs. Search and Fetch are free.

The post Perplexity AI Releases pplx-embed-v2-late: A 0.6B Edge Model and a 9B Model Scoring 92.4% on MADQA appeared first on MarkTechPost.