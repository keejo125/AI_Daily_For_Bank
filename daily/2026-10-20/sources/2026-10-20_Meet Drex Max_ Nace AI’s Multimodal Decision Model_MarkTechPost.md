---
publish_time: 1792454618
link: https://www.marktechpost.com/2026/10/19/nace-ai-drex-max-multimodal-decision-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Nace AI 发布多模态决策模型 Drex Max，面向使用电脑与浏览器的智能体：读取文本与图像并返回校准概率，不直接生成文本，每个点击只需一次廉价、类型化的调用。在公开 Decision Index 0.3.2 上得分 67.59，较 TypeSafe 的 Jev 1.14 高 6.9 分。API 单问题最多 262144 Token（含图像），仅托管 API 提供。对 Agent 构建者，Drex Max 提供确定性的"下一步点击"决策能力。
---

# Nace AI 发布 Drex Max 多模态决策模型：智能体点击决策

> 原文链接：https://www.marktechpost.com/2026/10/19/nace-ai-drex-max-multimodal-decision-model/
> 来源：MarkTechPost

Nace AI has released Drex Max, a multimodal decision model for agents that use computers and browsers. The Drex Max multimodal decision model reads text and images and returns calibrated probabilities. It writes no text. Nace team reports 67.59 on the public Decision Index 0.3.2, 6.9 points above TypeSafe&#8217;s Jev 1.14. For agent builders, that means one cheap, typed call per click.

TL;DR

Size: Parameters not disclosed. Up to 262,144 tokens per question on the API, including image tokens.

Runs on: Hosted API only (drex-max on Nace Console). No open weights or quantized builds announced.

Performance: 67.59 on Decision Index 0.3.2 (public), the top score Nace lists for any decision model.

Best: 98.2 on BFCL tool calling, and 92.2 on JevBench versus 86.7 for Jev 1.14.

Worst: 19.0 on HLE, and 72.5 on MMLU-Pro versus 82.1 for Jev 1.14.

What is Drex Max?

Drex Max is a decision model from Nace AI that answers typed questions about text and images. It is the most accurate model in the Drex family, and the only one that reads images.

A decision model does not generate tokens. You send a state and named questions. Each question is one of 3 types: noul (yes/no), choice (pick a label) or score (ordered scale). The model returns a probability distribution for each answer in 1 HTTP call. Drex can only answer with the options you gave it.

How does Drex Max work with images?

Drex Max uses the same POST /v1/systemone endpoint as every Drex model. You select it with "model": "drex-max". It is a pinned ID, so drex-latest does not route to it.

Images go in an images array. Every question sees the same images, before the state and questions. You refer to them as &#8216;Image 1&#8217; and &#8216;Image 2&#8217; in plain text. Each entry is either an uploaded workspace file or inline base64.

Key image rules from the Drex Max guide:

Formats: still PNG, JPEG or WebP.

Up to 8 images per request, 16 MiB each, 32 MiB total.

Each image is resized to at most 1,638,400 pixels (1,280 × 1,280).

Each image costs up to 1,602 tokens in every question.

Up to 16 questions per request, with a 4 MiB request body.

How does Drex Max perform on benchmarks?

All scores below come from Nace&#8217;s Drex page. They are self-reported. Nace says Drex trains on the index&#8217;s official training splits and is scored on held-out splits.

Decision benchmarks: Drex Max scores 67.6 on the public Decision Index 0.3.2. Jev 1.14 scores 60.7 and Drex 2.0 scores 61.3. On JevBench, Drex Max reaches 92.2 against 86.7 for Jev 1.14.

Agentic benchmarks: Drex Max posts 0.780 on OSWorld-Verified and 98.2 on BFCL. It scores 85.2 on When2Call and 84.8 on RAGTruth.

Vision: On the Decision Index Vision public suite, Drex Max scores 74.5. GPT-6 Luna Decisions scores 63.9. Mind2Web reaches 88.6 and InfographicVQA reaches 98.8.

Where it trails: Jev 1.14 leads on MMLU-Pro (82.1 vs 72.5), HLE (19.4 vs 19.0) and ARC-Challenge (97.6 vs 97.4). On Hateful Memes, Drex Max trails GPT-6 Luna Decisions, 70.6 vs 71.2.

How fast and how cheap is Drex Max?

Nace lists a 174 ms median per screenshot decision. Jev 1.14 takes 253 ms on the same 243 questions. Nace says Drex Max accepts every screenshot size, while Jev 1.14 rejects 15.9% by size.

Across its benchmark table, Nace reports a 183 ms median latency. The launch post cites 34 ms per decision and under 1 second at 262K tokens. Those figures use different setups, so treat them as separate claims.

Pricing is $0.06 per 1M input tokens. Output tokens are not billed. New accounts get $25 in signup credit, and failed requests cost nothing.

How does Drex Max compare with other decision models?

FeatureDrex MaxJev 1.14Drex 2.0d3-flashDeveloperNace AITypeSafe AINace AIvLLM Semantic RouterParametersNot disclosedNot disclosed35B total, about 3B active (MoE)8.39BContext262,144 tokens per question64K per request, 262K with long-context header16,384 default, up to 131,072Not disclosedInputsText, imagesText (TypeSafe docs)TextText, images, videoLicenseProprietary (hosted)Proprietary (hosted)Nace.AI Open RAIL-MApache-2.0Decision Index (public)67.6 (0.3.2)60.7 (0.3.2, per Nace)61.25 (0.3.1)57.8 (0.3.2)Vision index (public)74.5Not disclosedNot applicable69.9Price per 1M input tokens$0.06$0.042$0.06Self-host, free trialRuns onNace Console APITypeSafe APISingle accelerator, bf16 about 70 GB1 AMD Instinct MI325X tested

Note: d3-flash&#8217;s vision figure is its own evaluation on the 0.3.2 vision board. Drex Max&#8217;s figure is Nace&#8217;s own run. Cross-vendor numbers are not a controlled comparison.

Key Takeaways

Drex Max is Nace AI&#8217;s first multimodal decision model.

It scores 67.59 on Decision Index 0.3.2, 6.9 above Jev 1.14.

Screenshot decisions take 174 ms, versus 253 ms for Jev 1.14.

Pricing is $0.06 per 1M input tokens, with output free.

Size is undisclosed, weights are closed, and scores are self-reported.

Check out the Drex Max guide, the Drex product page and the launch post. Also read our earlier coverage of Drex 1.5. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Meet Drex Max: Nace AI’s Multimodal Decision Model for Computer-Use Agents with a Score 67.59 appeared first on MarkTechPost.