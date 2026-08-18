---
publish_time: 1786374711
link: https://www.marktechpost.com/2026/08/10/meta-ai-releases-muse-glimmer/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
is_merged: true
merge_target: "2026-08-10_Meta重回开源MuseSpark12_AI寒武纪.md"
digest: |
  Meta以Apache 2.0协议发布Muse Glimmer，一个从Muse Spark蒸馏而来的300亿参数多模态模型，专为本地Agent工作流优化。模型通过4-bit量化压缩至20GB以下搭配DFlash推测解码，可在单张消费级GPU或Mac上运行。训练分三个阶段：预训练使用logit蒸馏、中训练加入长上下文Agent数据、后训练结合SFT与强化学习。支持文本图像双模态输入、131K+上下文、32个query head/2个KV head的GQA注意力机制，覆盖桌面Agent、编程Agent、文档理解、合成数据生成等场景。
---
# Meta AI 发布 Muse Glimmer：300 亿参数开放权重 Agentic 模型，单 GPU 即可运行

> 原文链接：https://www.marktechpost.com/2026/08/10/meta-ai-releases-muse-glimmer/
> 来源：MarkTechPost

Meta has released Muse Glimmer, a 30-billion-parameter multimodal model distilled from Muse Spark. It is tuned for always-on local agent workflows, and ships under Apache 2.0. A 30B model normally needs over 55 GB of memory at full precision. Meta compresses it to roughly 4-bit, then adds block-level speculative decoding so it answers fast enough to sit inside a real agent loop. The result runs on one consumer GPU or a Mac, with no network call.

Is it deployable?

Yes, the weights are open under Apache 2.0. The Hugging Face collection carries BF16 weights, GGUF k-quants, ExecuTorch builds, and the DFlash drafter. Self-hosting is the day-one path.

Which companies: Solo developers and startups can run it on one 24 GB GPU or an M4/M5 Max Mac. Mid-market teams get on-prem inference without a per-token bill. Regulated enterprises get an air-gappable agent. Meta advises adding system-level guardrails rather than shipping the model as a bare endpoint.

Industries: Healthcare, legal, financial services, defense and public sector, manufacturing, and field service. These are the settings where data residency, offline operation, or latency rule out a cloud call.

Applications: Desktop agents that read screenshots, coding agents, and schema-based function calling. Also document and chart understanding, synthetic data generation, and LLM-as-a-judge evaluation.

Model and training

Muse Glimmer is a dense causal transformer with a dedicated perception encoder. Total parameters are roughly 30B, including the vision tower. Grouped-query attention uses 32 query heads and 2 KV heads. Attention repeats a [Local, Local, Local, Global] pattern with a 2,048 sliding window. RoPE is applied to local layers only, with theta 500,000. The vision side is a ~1.8B ViT-G/14 perception encoder accepting up to 4,096 visual tokens per image. Context length is 131,072+, vocabulary is 202,048 tokens, and the knowledge cutoff is January 4, 2026. Input is text and image; output is text. Audio is not supported, and video is processed as individual frames.

Training ran in three phases: 

Pre-training used logit distillation on Muse Spark&#8217;s outputs. 

Mid-training added longer-context, agent-heavy data with richer reasoning traces. 

Post-training combined supervised fine-tuning with on-policy distillation and reinforcement learning across general, reasoning, coding, and agentic domains.

Fitting 30B onto consumer hardware

At full precision the model needs over 55 GB of memory. Meta compresses weights to approximately 4-bit precision, which brings the language model under 20 GB. That leaves headroom inside a 24 GB or 32 GB envelope. The KV cache, perception encoder, and drafter share it. Two quantized builds ship. K-Quant-Dynamic targets 32 GB VRAM at 0.2% average degradation. K-Quant-17GB targets 24 GB VRAM at 1.0%. Degradation is averaged over accuracy metrics across 15 common benchmarks.

Generation speed comes from DFlash, a block-diffusion drafter that predicts 16 tokens in one forward pass. The main model verifies the block in parallel. The drafter uses 5 layers, sliding-window attention at 2,048, and 32 query / 8 KV heads. Meta measured K-Quant-17GB at batch size 1 with greedy decoding. On an RTX 5090, throughput rises from 74.9 to 233.4 tok/s, a 3.1x speedup. Apple M5 Max moves from 26.6 to 50.2 tok/s, and M4 Max from 23.7 to 37.8 tok/s.

Benchmarks

Meta compares Muse Glimmer against Gemma4-31B and Qwen3.6-27B in thinking mode. It leads on MCP Atlas at 75.5, against 54.2 and 62.5. It also leads on DeepSearch QA at 74.6, Gaia2 at 43.3, and SWE-Bench Pro at 51.2. Reasoning scores follow: AIME 2026 at 94.7, IFBench at 77.0, AA-LCR at 80.0. Qwen3.6-27B stays ahead on OSWorld-Verified, 75.6 versus 65.9. It also leads TerminalBench 2.1 at 60.7 and SWE-Bench Verified at 77.2. The pattern is consistent. Muse Glimmer wins on agentic orchestration and reasoning. It trails on computer-use and terminal work.

On safety, Siren AgentDojo attack success rate is 28.4 with utility 94.2. Meta states the model does not meet the Frontier AI definition in its Advanced AI Scaling Framework. It rates chem/bio, cyber, and loss-of-control risk at moderate or lower.

Key Takeaways

30B open-weights agentic model, Apache 2.0, distilled from Muse Spark.

4-bit quantization fits it in 24 GB VRAM at 1.0% degradation.

DFlash 16-token block speculation gives 3.1x decode speedup on RTX 5090.

Beats both comparators on MCP Atlas, DeepSearch QA, and SWE-Bench Pro.

Trails Qwen3.6-27B on OSWorld-Verified and TerminalBench 2.1.

Check out the Model weights on HF, Details and Meta Blog. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meta AI Releases Muse Glimmer: A 30B Open-Weights Agentic Model That Runs on One Consumer GPU appeared first on MarkTechPost.