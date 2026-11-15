---
publish_time: 1791755021
link: https://www.marktechpost.com/2026/10/11/what-is-decision-3-0-vllm-semantic-routers-new-open-decision-models/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  MarkTechPost 详解 vLLM Semantic Router 开源的 Decision 3.0 多模态决策模型族：读取文本、JSON 与图片，返回类型化问题的概率答案，共 5 款（0.85B—26.09B），均 Apache-2.0。开发者可免解析生成文本即可完成分类、路由与门控。旗舰 d3 在文档抽取 KIE 达 97.7；但该文提醒其评分为内部自报，并与线上榜单对比。
---

# Decision 3.0 是什么：vLLM Semantic Router 开源决策模型

> 原文链接：https://www.marktechpost.com/2026/10/11/what-is-decision-3-0-vllm-semantic-routers-new-open-decision-models/
> 来源：MarkTechPost

The vLLM Semantic Router team has released Decision 3.0, a family of multimodal decision models. Decision 3.0 multimodal decision models read text, JSON and images, then answer typed questions about them. There are 5 sizes, from 0.8B to 27B, all under Apache-2.0. For developers, this is a fast way to classify, route and gate requests without parsing generated text.

TL;DR

Size: 5 models: d3-lite (0.85B), d3-nano (2.21B), d3-mini (4.54B), d3-flash (8.39B), d3 (26.09B). Context length: not disclosed.

Runs on: latency measured on 1 AMD Instinct MI325X GPU. BF16 weights; no official quantized variants listed.

Performance: the 27B d3 leads both the text and vision tables in its card, but on internal evaluation.

Best: 97.7 on KIE (CORD+FUNSD) document extraction (d3).

Worst: 34.1 on R-Bench-M (d3).

Bottom line: 

Best: a 9B model now beats last generation&#8217;s 27B. 

Worst: scores are self-reported against live board data.

What is Decision 3.0?

Decision 3.0 is a set of open decision models from vLLM Semantic Router that return probabilities instead of text. You pass a state (text or JSON), optional images, and named questions. Each question is a Choice, a Yes/No, or a Score on a scale. The model answers all questions in one call and returns a probability for every answer.

This is the &#8216;system one&#8217; pattern for routers and guardrails. Instead of prompting an LLM and parsing its output, you get calibrated scores you can threshold.

How does d3 work?

Each model is a fine-tune of a Qwen base. The 27B d3 is built on Qwen3.8-27B. The smaller 4 build on Qwen3.5 checkpoints at 0.8B, 2B, 4B and 9B.

Every size carries a vision encoder: 0.10B in d3-lite, 0.33B in d3-nano and d3-mini, and 0.46B in d3-flash and d3. Requests accept several PNG, JPEG or WebP images, each read at up to 1.6 megapixels. Every question sees all images.

Each question gets its own forward pass over the input. Install targets transformers==5.17.0, and the optional flash-linear-attention package speeds up the linear-attention layers. Loading needs trust_remote_code=True.

How does Decision 3.0 perform on benchmarks?

Through the model card, the research team state the Jev Decision Index 0.3.1, a board that ranks open reproductions of TypeSafe&#8217;s Jev decision system. d3 numbers are the team&#8217;s internal evaluation. 

On text, d3 scores 64.1, ahead of Perplexity Decider v1.1 (62.8) and Jev (60.1). One caveat: Torchcast Decision 27B posts a higher public-suite score (65.1 vs 64.9). On the vision board, d3 scores 71.6 against 70.6 for Perplexity Decider v1.1.

The size story is the strongest part. d3-flash (9B) scores 59.0, above Decision 2.0&#8217;s 27B at 55.9. On the public suite, gains over Decision 2.0 range from +8.0 (27B) to +15.1 (0.8B).

Class leadership is not uniform, though:

d3-mini (4B) and d3-flash (9B) lead both their text and vision tables.

d3-lite (0.8B) leads on text but ranks 3rd on vision (41.1, behind JPT-0.8B at 42.1).

d3-nano (2B) leads its vision table but trails LiquidAI d1-3B on text (35.8 vs 40.1).

On public vision tasks, d3 scores 97.3 on InfographicVQA and 89.9 on Mind2Web, both approximate rebuilds. It is weaker on MMMU-Pro vision (46.2) and Hateful Memes moderation (44.6).

&&

How fast are the models?

Medians below are for 1 request at a time on 1 AMD Instinct MI325X, per each card:

d3-nano: 21.7 ms text, 92.0 ms with an image

d3-lite: 23.5 ms text, 60.7 ms with an image

d3-mini: 28.5 ms text, 115.0 ms with an image

d3-flash: 29.7 ms text, 171.8 ms with an image

d3: 84 ms text, 342 ms with an image

All models were trained on AMD Instinct MI325X GPUs.

How does d3 compare with other decision models?

Featured3 (vLLM SR)Perplexity Decider v1.1Decision 2.0 Vega-27BLiquidAI d1-3BParameters26.09B26B (HF listing)29.37B3.12BBase modelQwen3.8-27BQwen3.8-27BQwen3.8-27BLFM2.5-VL-3BInputsText, JSON, imagesText, imagesText, JSONText, JSON, imagesContextNot disclosed8,192 tokens per decision32,768 tokens32,768 tokensLicenseApache-2.0Apache-2.0Apache-2.0LFM 1.0Decision Index (own card)64.1 (v0.3.1, internal)61.56 (version not stated)56.5 (v0.2.1)48.57 (v0.2.1)Index 0.3.1 board (per d3 cards)64.162.855.940.1Vision board 0.3.171.670.6Not disclosed (text only)Not disclosedMedian latency (own card)84 ms text, 1 MI325XNot disclosed71.4 ms, 1 GPU9 ms, 1 MI325X

Key Takeaways

5 Apache-2.0 decision models, 0.8B to 27B, all with image input.

d3 (27B) tops its text (64.1) and vision (71.6) tables, on internal evals.

The 9B d3-flash (59.0) beats Decision 2.0&#8217;s 27B (55.9).

The 0.8B and 2B models do not lead every board.

Median text latency runs 21.7 to 84 ms on 1 MI325X.

Check out the Hugging Face collection, the d3 model card and the vLLM Semantic Router GitHub repo. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post What is Decision 3.0? vLLM Semantic Router’s New Open Decision Models appeared first on MarkTechPost.