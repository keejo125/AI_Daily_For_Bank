---
publish_time: 1789766519
link: https://www.marktechpost.com/2026/09/18/jina-ai-releases-jina-ocr-v1-a-3-4b-moe-document-parser-with-built-in-speculative-decoding-for-low-budget-gpus/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Jina AI（Elastic 旗下）发布端到端视觉文档解析模型 jina-ocr-v1，可将 PDF、扫描件、表格、图表与发票一次性转为干净 Markdown。模型总参数 3.4B，每 token 仅激活约 570M decoder 参数，并在模型内集成投机解码头，面向 NVIDIA L4 等低成本 GPU。技术报告显示其在 OmniDocBench v1.6 达 91.14、olmOCR-Bench 达 83.4；基于 DeepSeek-OCR 后训练并保留其两大效率组件，BF16 权重约 6.8GB，可经 Transformers 或 vLLM 加载，CC BY-NC 4.0 商用需授权。
---

# Jina AI 发布 jina-ocr-v1：3.4B MoE 文档解析模型（含投机解码）

> 原文链接：https://www.marktechpost.com/2026/09/18/jina-ai-releases-jina-ocr-v1-a-3-4b-moe-document-parser-with-built-in-speculative-decoding-for-low-budget-gpus/
> 来源：MarkTechPost

Jina AI, part of Elastic, has released jina-ocr-v1, an end-to-end visual document parser. It takes PDFs, scans, tables, charts or invoices and returns clean Markdown in 1 pass. The model has 3.4B total parameters, with about 570M decoder parameters active per token. A speculative decoding head ships inside the checkpoint. Jina AI built it to serve on low-budget GPUs such as the NVIDIA L4. The technical report lists 91.14 on OmniDocBench v1.6 and 83.4 on olmOCR-Bench.

Is it deployable? Yes, for research and non-commercial use. The open weights are about 6.8 GB in BF16 and run on Transformers or vLLM. The CC BY-NC 4.0 license means commercial use requires contacting Jina AI.

What is jina-ocr-v1?

The model post-trains DeepSeek-OCR and keeps its 2 efficiency components. DeepEncoder has about 380M parameters and chains SAM, a 16x convolutional compressor and CLIP-L. It turns a 1024&#215;1024 page view from 4,096 patches into 256 visual tokens. A dynamic-resolution mode adds up to 9 local tiles at 100 tokens each. That caps a page at 1,156 visual tokens.

The decoder is DeepSeek-3B-MoE with 12 layers, 64 routed experts and 2 shared experts. Top-6 routing activates about 570M parameters per token. The position limit is 32,768. Output is Markdown, with tables in HTML and formulas in LaTeX.

How FastMTP Speculative Decoding Works

OCR output is near-deterministic and locally structured. That makes it a good fit for speculative decoding. Jina AI adds a FastMTP head: 1 dense draft block applied recursively for K=3 steps. Draft parameters stay constant as depth grows.

The decoder then verifies the drafts greedily. It accepts the longest prefix that matches its own choices and commits 1 more token itself. If all 3 drafts match, that extra token is a bonus. The committed text always equals plain greedy decoding, so the speedup is lossless. At K=3 the model commits 2.73 tokens per step on average.

&&&

Post-Training With Dense Verifiable Rewards

Post-training combines instruction alignment, robustness fine-tuning on degraded pages, and GRPO. Every reward term is deterministic code scored against a reference transcription. The terms cover content, formulas, tables, structural validity, unit tests, repetition and format.

The terms are multiplied, and each one is graded, so partly correct pages earn partial credit. Structural, unit-test and format terms are floored at 0.2, and the table term at 0.1. The repetition term has no floor, because loops can inflate the content score.

On natural pages, the formula and table rewards apply to few samples. Jina AI therefore built JinaOCRSynth, synthetic pages packed with both, each carrying olmOCR-Bench-style unit tests. An agent also merges candidate checkpoints under a fixed evaluation budget. The draft head is trained last, against the frozen final verifier.

Benchmarks and Throughput

ModelParams as listed in the paperOmniDocBench v1.6olmOCR-Benchjina-ocr-v13B/570M91.1483.4DeepSeek-OCR3B/570Mnot listed76.0DeepSeek-OCR-23B/570M90.25not listedPaddleOCR-VL-1.60.9B96.34not listedchandra-ocr-24Bnot listed85.8Qwen3-VL-235B235B/22B89.78not listed

For MoE models, params show decoder total and active counts. The whole jina-ocr-v1 model is about 3.4B.

The model does not lead on accuracy. PaddleOCR-VL-1.6 and HunyuanOCR-1.5 (94.74) score higher on OmniDocBench. chandra-ocr-2 and dots.mocr (83.9) score higher on olmOCR-Bench. Post-training does add 7.4 points over the DeepSeek-OCR backbone on olmOCR-Bench.

Throughput is the main result. On 1 A100 40 GB at concurrency 32, jina-ocr-v1 parses 2.57 pages per second. That is the highest of 14 systems Jina AI measured, against 1.22 for olmOCR-2 and 0.38 for chandra-ocr-2. It emits 1,085 output tokens per page. Jina AI says that is the shortest output among systems scoring above 83.

On an NVIDIA L4 at batch size 1, eager decoding rises from 42.7 to 83.1 tokens per second. That is a 1.95x speedup at a 57.6% acceptance rate. With CUDA graphs the baseline is already 158.3 tokens per second. There, K=1 works best at 185.6 tokens per second, a 1.17x gain.

How to Run It

The quickest route is Jina Reader. Send a URL to r.jina.ai with the header X-Respond-With: jina-ocr-v1. Reader fetches the page or PDF, runs the model and returns Markdown. An X-Page header transcribes 1 page of a longer document.

Jina AI also hosts an OpenAI-compatible endpoint at https://api.jina.ai/v1/chat/completions. A hosted demo is available for quick tests.

For self-hosting, weights and custom code ship in 1 repository and load with trust_remote_code=True. FastMTP requires vLLM 0.21 or later and a one-time register() call. The Transformers path runs the MoE decoder alone and ignores the draft weights.

Key Takeaways

3.4B total parameters, about 570M active per token, built on DeepSeek-OCR.

FastMTP drafts 3 tokens per step, and greedy verification keeps decoding lossless.

Scores 91.14 on OmniDocBench v1.6 and 83.4 on olmOCR-Bench.

Reaches 2.57 pages per second on 1 A100, the highest of 14 measured systems.

Available on Hugging Face and through a Jina Reader header today.

Check out the Paper, Model weights, Release post, Model page and Announcement. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Jina AI Releases jina-ocr-v1: A 3.4B MoE Document Parser With Built-In Speculative Decoding for Low-Budget GPUs appeared first on MarkTechPost.