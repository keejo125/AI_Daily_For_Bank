---
publish_time: 1793078796
link: https://www.marktechpost.com/2026/10/26/baidu-unlimited-ocr-2-open-source-long-document-ocr/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  百度开源长文档 OCR 模型 Unlimited OCR 2（3.34B 参数，MIT 许可）。该视觉语言模型单次请求可解析数百页书籍、财报与报告，核心改进 SR-SWA 稀疏注意力使逐 token 解码成本近乎持平；在 MarathonDocBench 百页文档基准上以 77.1 分领先，单卡 A800 即可运行。
---

# 百度开源 Unlimited OCR 2 长文档解析模型

> 原文链接：https://www.marktechpost.com/2026/10/26/baidu-unlimited-ocr-2-open-source-long-document-ocr/
> 来源：MarkTechPost

Baidu has released Unlimited OCR 2, an open-source OCR model built for very long documents. The 3B model parses books, filings and reports of hundreds of pages in one request. Its core change is SR-SWA, a sparse attention scheme that keeps per-step decoding cost nearly flat. Weights ship under the MIT license, with code on GitHub.

TL;DR

Size: 3.34B parameters. Active parameters not disclosed. Max position length 131,072 tokens.

Runs on: 1 CUDA GPU in BF16. Baidu tested on an NVIDIA A800-80GB. BF16 weights total about 6.7 GB. 

Performance: first place on both multi-page benchmarks Baidu tested, against 9 other models (self-reported).

Best: 77.1 overall on MarathonDocBench (hundreds of pages). The next model, Kimi-K3, scores 33.7.

Worst: 48.2 on heading hierarchy (TEDS) on MarathonDocBench, its lowest sub-score.

What is Unlimited OCR 2?

Unlimited OCR 2 is a 3B vision-language model from Baidu that turns ordered page images into structured text. Output covers text, tables, formulas, figures, headings and reading order. It succeeds Unlimited-OCR, released in June 2026 to push DeepSeek-OCR further.

The config keeps a DeepSeek-OCR style layout. A SAM ViT-B plus CLIP-L encoder feeds a 12-layer mixture-of-experts decoder. Each token routes to 6 of 64 experts, plus 2 shared experts. The DeepSeek-OCR paper describes this decoder as DeepSeek3B-MoE-A570M. Baidu does not state an active count for version 2. In multi-page mode, each page costs 273 image tokens.

How does SR-SWA work?

Full attention cost grows quadratically with sequence length. During decoding, each new token scans a longer KV cache. At 273 image tokens per page, 100 pages add 27,300 input tokens before any output.

SR-SWA stands for Sparse Reference Sliding Window Attention. It compresses text-visual attention into a fixed set of working references. Baidu&#8217;s model card gives 512 tokens as the example size. The config pairs a 128-token local window with top-16 selection over 32-token blocks. That is 16 blocks of 32 tokens, matching the 512-token budget.

This keeps per-step latency and memory nearly constant as documents grow. It calls the result &#8216;unlimited-horizon&#8217; parsing within a finite context window. Image encoding and total runtime still rise with page count.

&&&

How does it score on MPDocBench and MarathonDocBench?

Baidu team tests on MPDocBench, with dozens of pages per document, and MarathonDocBench, with hundreds. MPDocBench-Parse is a public benchmark of 433 documents and 3,246 pages. We could not find a public MarathonDocBench release.

Per Baidu&#8217;s leaderboard chart, Unlimited OCR 2 scores 84.6 on MPDocBench. Qwen3.8-Max follows at 78.3, then Qwen-3.8-Flash-Next at 77.4. On MarathonDocBench it scores 77.1. Kimi-K3 is next at 33.7, then Gemini-3.8-Flash at 28.6.

The drop between benchmarks is the real story. Qwen3.8-Max falls from 78.3 to 22.9 on hundred-page documents. Unlimited OCR 2 falls 7.5 points. Its predecessor, Unlimited-OCR, scores 0.0 on MarathonDocBench.

Sub-scores (MPDocBench / MarathonDocBench):

Text: 94.8 / 89.6

Formula: 89.4 / 87.9

Reading order: 92.3 / 85.3

Tables: 87.8 / 74.8

Heading hierarchy: 60.1 / 48.2

Single-metric margins on MPDocBench are thin. Qwen3.8-Max scores 94.3 on text and 89.2 on formulas. All figures are self-reported and appear only in a chart image.

Comparison with other open OCR models

Unlimited OCR 2Unlimited-OCRDeepSeek-OCR-2PaddleOCR-VL-1.6DeveloperBaiduBaiduDeepSeekBaidu PaddlePaddleParameters3.34B3.34B3.39B0.96BActive parametersNot disclosedNot disclosedNot disclosedNot disclosedLicenseMITMITApache 2.0Apache 2.0Paper / releaseOct 2026 (report)Jun 2026 (arXiv)Jan 2026 (arXiv)Jun 2026 (arXiv)Long-document mechanismSR-SWA, 512-token reference setMulti-page infer_multi, no SR-SWANot disclosedNot disclosedMPDocBench overall84.6 (Baidu)61.9 (Baidu)Not reportedNot reportedMarathonDocBench overall77.1 (Baidu)0.0 (Baidu)Not reportedNot reportedServingTransformers, custom SGLangTransformers, vLLM, SGLangTransformers, SGLangPaddleOCR, Transformers

Parameter counts and licenses from each model&#8217;s Hugging Face page. Benchmark scores from Baidu&#8217;s chart.

How do you run Unlimited OCR 2?

The model card lists Transformers for quick tests and SGLang for serving. In Transformers, infer handles 1 page with dynamic tiling, called gundam mode. infer_multi parses every page of a document in 1 request, so the model keeps cross-page context. Loading requires trust_remote_code=True, which runs Python code from the repo.

SGLang serving uses a customized wheel from Baidu, not upstream SGLang. Baidu&#8217;s example schedules 10 pages per window and reuses the previous window&#8217;s KV tail. Smaller windows cut peak memory but weaken cross-page merging. Baidu warns a default bias setting can trigger a 462 MiB allocation and run out of memory.

Key Takeaways

Unlimited OCR 2 is a 3.34B, MIT-licensed OCR model from Baidu.

SR-SWA caps attention at a fixed 512-token reference set.

It scores 77.1 on MarathonDocBench, against 33.7 for the next model.

Heading hierarchy is the weak spot, at 48.2 on long documents.

All benchmark numbers are Baidu&#8217;s own.

Check out the model card, the technical report and the GitHub repo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Baidu Open-Sources Unlimited OCR 2 for Hundred-Page Document Parsing appeared first on MarkTechPost.