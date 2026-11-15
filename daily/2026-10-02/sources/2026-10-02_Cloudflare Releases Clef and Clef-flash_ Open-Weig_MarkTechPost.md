---
publish_time: 1790902841
link: https://www.marktechpost.com/2026/10/01/cloudflare-releases-clef-and-clef-flash/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cloudflare 发布 Clef 与 Clef-flash，这是其 Workers AI 团队训练的首批模型，定位为“决策模型”而非聊天机器人：每个模型读取输入状态与一组类型化问题，直接返回每个允许答案的概率，不生成自由文本。两者以 Apache 2.0 开源，兼容 TypeSafe AI 的 Jev API。Clef 由 Qwen3.8-27B 后训练而来，Clef-flash 源自 Qwen3.5-9B，均保留视觉编码器；推理分主干 prefill 与联合 schema 头两阶段。已在 Workers AI 上线，权重开放于 Hugging Face 供自托管。
---

# Cloudflare 开源决策模型 Clef 与 Clef-flash

> 原文链接：https://www.marktechpost.com/2026/10/01/cloudflare-releases-clef-and-clef-flash/
> 来源：MarkTechPost

Cloudflare has released Clef and Clef-flash, the first models trained by its Workers AI team. They are decision models, not chatbots. Each reads an input state and a schema of typed questions. It returns a probability for every allowed answer, with no free-form text. Both are open-weight under Apache 2.0 and compatible with TypeSafe AI&#8217;s Jev API.

Is it deployable? Yes, Both models run today on Workers AI, and the weights are on Hugging Face for self-hosting.

What a Decision Model Does

An LLM generates tokens one at a time, and its output still needs parsing. A decision model only answers a fixed set of questions about an input. Clef supports 3 question types:

noul: yes/no, returns the probability of yes.

choice: picks 1 named option, with per-option probabilities and a confidence value.

score: rates against an ordered rubric, returning a probability-weighted score.

On Workers AI, 1 request carries up to 64 questions and up to 4 images.

TypeSafe AI launched Jev, its first &#8216;System One&#8217; model, on September 15, 2026. Open alternatives like Kev-9B and Laya followed. Clef uses the same System One API. Switching from Jev means changing the endpoint and model name.

How Clef Works

Clef is post-trained from Qwen3.8-27B, and Clef-flash from Qwen3.5-9B. Both keep the backbone&#8217;s vision encoder.

Inference has 2 stages. The backbone first runs a single prefill-only pass over the state and questions. A small transformer, the joint schema head, then reads the final hidden states. It routes evidence to each question, lets fields cross-attend, and scores all options jointly. A per-question softmax turns logits into probabilities.

Training froze both backbones and jointly optimized the routing head with rank-256 low-rank adapters. The loss pairs label-smoothed cross-entropy with a Brier loss for calibration. A secondary objective, Reinforcement Learning for Calibrated Decisions (RLCD), gives partial credit to adjacent ordinal choices.

Interactive Explainer

&&

Benchmarks: Where Clef Wins and Where It Does Not

On Cloudflare&#8217;s 10-benchmark shortlist from the Decision Index 0.2.1 suite, a Clef model scored highest on 7.

BANKING77 (macro-F1): Clef 94.20 vs Jev 79.74.

CLINC150+OOS (macro-F1): Clef 97.43 vs Jev 89.27.

Home appliances (case exact): Clef-flash 97.73 vs Jev 52.27.

Jev keeps clear leads elsewhere. The full model card shows Jev ahead on GPQA Diamond (78.3 vs 48.0). It also leads MMLU-Pro (82.7 vs 65.9) and BBH (92.9 vs 73.7).

On TypeSafe&#8217;s own workflow evals, Clef beat Jev in 3 of 4 areas, by small margins. Invoice processing was 64.7 vs 61.8, customer service 76.3 vs 76.0, and security incidents 62.9 vs 61.7. Jev leads agent trace observability, 71.6 vs 68.5.

In Cloudflare&#8217;s threat intelligence workflow, Clef classified a domain in 2.2 seconds. gpt-oss-120b took 4.7 seconds.

All numbers are vendor-reported, with no independent replication yet.

Feature Comparison

FeatureClefClef-flashJevKev-9BLayaDeveloperCloudflareCloudflareTypeSafe AIJared PalmerConvai InnovationsSize27B9BNot disclosed9B + 45.4M LoRA421MBackboneQwen3.8-27BQwen3.5-9BNot disclosedQwen3.5-9B-BaseModernBERT-largeWeightsApache 2.0Apache 2.0Hosted APIApache 2.0Apache 2.0Image inputYesYesNoNoNoContext65,53665,53632K (per Cloudflare)65,536 (8,192 validated)512 (English)Median latency*209.3 ms38.8 ms524.1 ms51.4 ms5.8 msHosted price (input)$0.24/M$0.09/M$0.042/MSelf-hostSelf-host

*Cloudflare&#8217;s internal Decision Index run. All 5 implement the System One API. Sources: Clef docs, Clef-flash docs, Clef card, Jev post, Kev-9B card, Laya card.

Deployment and Fine-Tuning

Both models are callable through the Workers AI binding (env.AI.run()), the REST API, or AI Gateway. For self-hosting, the model cards list testing on a single H200 with BF16 weights.

Cloudflare also announced a reinforcement learning service for tuning Clef on private data. It starts with Cloudflare&#8217;s forward-deployed engineers, with a self-serve platform later. The pipeline combines AI Gateway, Workers AI, Containers and a new Trainer component. Teams can apply via the design partner form.

Key Takeaways

Clef (27B) and Clef-flash (9B) are Apache 2.0, Jev-compatible decision models.

Median latency: 209.3 ms for Clef, 38.8 ms for Clef-flash, 524.1 ms for Jev.

Clef reads text, JSON, images and video within a 64K-token context window.

Jev still leads on knowledge-heavy tests like GPQA Diamond, MMLU-Pro and BBH.

An RL fine-tuning service starts with Cloudflare&#8217;s forward-deployed engineers.

Check out the Model weight, Demo and Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Cloudflare Releases Clef and Clef-flash: Open-Weight Decision Models That Return Typed Probabilities Instead of Text appeared first on MarkTechPost.