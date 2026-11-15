---
publish_time: 1791311768
link: https://www.marktechpost.com/2026/10/06/google-deepmind-releases-embeddinggemma-2-a-740m-open-multimodal-embedding-model-built-on-gemma-4/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google DeepMind 发布 EmbeddingGemma 2，将文本、代码、图像、视频、音频统一映射到同一 768 维嵌入空间的开源多模态嵌入模型，基于 Gemma 4 架构、Apache 2.0 许可，参数 7.4 亿，8K 上下文。采用模块化编码器（文本 270M、视觉 170M、音频 300M 可选），量化后可在 Pixel 11 Pro 以约 191MB（纯文本）/ 567MB（全模态）内存本地运行；借助 Matryoshka 表示学习可将向量截断至 128 维，本地向量库存储最高降 6 倍。在 MTEB Code 上较上代提升 9.92 分，适合本地代码索引、语义检索与隐私优先 RAG。本文补充横向对比：其参数量与 Qwen3-VL-Embedding-2B、LCO-Embedding-Omni-3B 接近，且是唯一同时支持文 / 图 / 视频 / 音频的开源嵌入模型。
---

# Google DeepMind 发布 EmbeddingGemma 2：基于 Gemma 4 的 7.4 亿参数多模态嵌入模型

> 原文链接：https://www.marktechpost.com/2026/10/06/google-deepmind-releases-embeddinggemma-2-a-740m-open-multimodal-embedding-model-built-on-gemma-4/
> 来源：MarkTechPost

Google DeepMind has released EmbeddingGemma 2, an open model that embeds text, code, images, video and audio into one 768-dimensional space. It has 740M parameters, an 8K token context window and an Apache 2.0 license. It targets on-device search, classification and privacy-first RAG. This article analyzes, compares and showcase how EmbeddingGemma 2 fits in the space.

Deployable today? Yes. Weights are live on Hugging Face and Kaggle, with Ollama, llama.cpp GGUF and LiteRT builds available now. 

What an Embedding Model Does

An embedding model converts content into a vector of numbers that captures meaning. Similar items land close together, so they are easy to search and compare. In a RAG pipeline, these vectors let an LLM retrieve fresh information it was not trained on. Generating embeddings locally keeps data on the device, cuts latency and works offline.

One Vector Space for Every Modality

EmbeddingGemma 2 is built on the Gemma 4 architecture. A text query can retrieve a photo. A voice memo can retrieve a video clip. Interleaved inputs, like a product listing with text, images and a demo video, produce a single embedding.

The design is modular. It has three parts:

Text and code backbone: 270M parameters (130M transformer plus 140M embedder)

Vision encoder: 170M parameters, optional

Audio encoder: 300M parameters, optional

Developers load only what they need: 270M for text, 440M for text and vision, 570M for text and audio, or 740M for everything. All setups share one vector space. A query embedded with the text-only setup can match documents embedded by the full model.

The context window is 8,192 tokens, 4x larger than version 1. That fits about 29 images, 58 video frames or 5.5 minutes of audio.

Benchmarks

Google research team reports leading scores among sub-1B multimodal embedders on MTEB Code and MAEB. Full-precision results at 768 dimensions:

BenchmarkEmbeddingGemma 2EmbeddingGemma 1MTEB multilingual v261.3661.15MTEB Code v178.6868.76MIEB lite (image)64.64n/aMMEB v2 overall59.01n/aMSEB retrieval (sound)69.54n/aMAEB (audio)49.39n/a

Source: EmbeddingGemma 2 model card

Code retrieval gains 9.92 points, roughly 14%. Multilingual text quality holds steady. Bigger models still lead some boards. Qwen3-VL-Embedding-2B reports 73.2 on its own MMEB-V2 run, with about 2.7x the parameters and no audio support.

Built for Phones and Laptops

With quantization on a Pixel 11 Pro, active RAM is about 191MB for text-only weights. The full multimodal model needs about 567MB. Quantization-aware training compresses weights to INT4 and INT8. The Google AI Edge team measured 37.3 ms per image on a MacBook M5 Pro GPU, using a 70-token vision budget.

Matryoshka Representation Learning (MRL) lets developers truncate vectors to 512, 256 or 128 dimensions. Moving from 768 to 128 dimensions cuts storage up to 6x. At 256 dimensions, MTEB multilingual only slips from 61.36 to 60.41. At 128 dimensions, MMEB drops to 45.65, so Google recommends 128d mainly for text-only workloads.

Interactive Explainer

&&&

EmbeddingGemma 2 vs. Closest Competitors

FeatureEmbeddingGemma 2EmbeddingGemma 1Qwen3-VL-Embedding-2BLCO-Embedding-Omni-3BGemini Embedding 2DeveloperGoogle DeepMindGoogle DeepMindAlibaba QwenLCO-Embedding (research)GoogleParameters740M (270M text-only)308M2B3B backbone (5B listed on HF)Not disclosedText / codeYesYesYesYesYesImagesYesNoYesYesYesVideoYesNoYesYesYesAudioYesNoNoYesYesOutput dims (MRL)768 (512, 256, 128)768 (down to 128)Up to 2048 (64 to 2048)Not stated3072 (128 to 3072)Context8,192 tokens2K tokens32K tokensNot stated8,192 tokensLanguages100+100+30+Not stated100+License / accessApache 2.0, open weightsOpen weights (Gemma terms)Apache 2.0, open weightsApache 2.0, open weightsPaid API onlyPublished on-device RAM~191MB text, ~567MB fullUnder 200MBNot publishedNot publishedCloud onlySourceModel cardDocsHF cardHF cardAPI docs

How to Run It

It runs on sentence-transformers v6.1.0+, Transformers, vLLM, SGLang, MLX, llama.cpp, Ollama, LM Studio, LiteRT and MediaPipe. Qdrant covers vector storage and Unsloth covers fine-tuning. ML Kit support for Android, with NPU acceleration, is coming within weeks.

Copy CodeCopiedUse a different Browser

pip install -U "sentence-transformers[image,audio,video]" transformers

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("google/embeddinggemma-2")
q = model.encode("What causes the northern lights?", prompt_name="SearchQuery")
d = model.encode("Charged particles from the sun.", prompt_name="Document")
print(model.similarity(q, d))

On Ollama, run ollama pull embeddinggemma-2. Tags range from 270m (378MB) to 740m (1.3GB). Demos live in Google AI Edge Gallery. See the developer guide for more.

Key Takeaways

One 740M open model embeds text, code, images, video and audio into a shared 768d space.

Modular encoders scale the footprint from 270M (text) to 740M (full multimodal).

Code retrieval jumps from 68.76 to 78.68 on MTEB Code.

Runs in ~191MB to ~567MB of RAM on a Pixel 11 Pro with quantization.

FAQ

Can EmbeddingGemma 2 be used commercially? Yes. It is released under the Apache 2.0 license.

How much memory does EmbeddingGemma 2 need? Google reports about 191MB of active RAM for text-only use and 567MB for full multimodal use, quantized, on a Pixel 11 Pro.

Check out the Model Weights on HF and Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

[Sponsored] The web is the one API most agents are missing. Databases, calendars and repos have APIs. The open web mostly doesn’t. The TinyFish MCP server gives any MCP client four tools: TinySearch, TinyFetch (full pages as markdown, JavaScript included), TinyBrowser for logins and forms, and TinyAgent for multi-step jobs. Search and Fetch are free.

The post Google DeepMind Releases EmbeddingGemma 2, a 740M Open Multimodal Embedding Model Built on Gemma 4 appeared first on MarkTechPost.