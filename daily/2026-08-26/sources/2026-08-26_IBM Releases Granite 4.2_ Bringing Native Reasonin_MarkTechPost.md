---
publish_time: 1787723290
link: https://www.marktechpost.com/2026/08/25/ibm-releases-granite-4-2-bringing-native-reasoning-and-agentic-rl-to-open-enterprise-models/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  IBM 发布 Granite 4.2 开源推理语言模型家族（3B/8B/30B），告别此前指令遵循定位，改为显式推理：每模型先输出思维链再作答，提供思考/非思考开关与低耗模式。8B 与 30B 经多阶段强化学习，含智能体 RL 模块，可在真实沙箱中改代码、驱动终端、跑搜索。三款均基于 Apache 2.0，并同步推出 470M 参数的 Granite Speech 5.0 Turbo CTC 模型。
---

# IBM 发布 Granite 4.2：原生推理与智能体强化学习的开源企业模型

> 原文链接：https://www.marktechpost.com/2026/08/25/ibm-releases-granite-4-2-bringing-native-reasoning-and-agentic-rl-to-open-enterprise-models/
> 来源：MarkTechPost

IBM has released Granite 4.2, a family of open reasoning language models in 3B, 8B, and 30B parameter sizes. Unlike earlier Granite releases, which were instruction-following assistants, Granite 4.2 is built around explicit reasoning. Every model can emit a chain of thought before answering, and every model exposes a thinking / non-thinking switch plus a low-effort mode that spends a short reasoning budget on easy questions. The models are decoder-only dense transformers, pre-trained from scratch on roughly 15 trillion tokens, then post-trained through a multi-stage reinforcement learning chain. For the 8B and 30B, that chain includes an agentic RL block where the model learns to edit code, drive a terminal, and run web searches inside real sandboxed environments. All three ship under Apache 2.0. IBM also released two 470M-parameter Granite Speech 5.0 Turbo CTC models alongside the LLMs.

Is it deployable?

Yes, All three Granite 4.2 language models ship under Apache 2.0, so download, fine-tuning, and commercial production use carry no licensing gate.

Which companies: The 3B fits solo developers and startups running on a laptop through Ollama or LM Studio, especially with the released GGUF quants down to Q4_K_M. The 8B suits mid-market teams on a single modern GPU. The 30B targets enterprises with A100/H100-class capacity, or FP8/NVFP4 serving on vLLM. Regulated organizations get the additional benefit of on-prem weights.

Industries: Software and developer tooling, financial services, healthcare, telecom, public sector, and contact centers, which is where the new speech models land.

Applications: Software engineering agents, terminal and DevOps automation, deep-research and search agents, long-document RAG, structured tool calling, and high-volume transcription.

Architecture

Granite 4.2 is a decoder-only dense transformer, not a hybrid or MoE design. Core components are Grouped Query Attention with 8 KV heads, RoPE with θ = 10,000,000, SwiGLU MLPs, RMSNorm (ε = 1e-5), untied input/output embeddings, and bfloat16 precision.

The 3B uses 40 layers at embedding size 2560. The 8B uses 40 layers at 4096. The 30B goes to 64 layers with an MLP hidden size of 32,768. The published architecture table lists a 131,072-token (128K) sequence length, while the five-phase pre-training run includes a long-context phase extending to 512K tokens. Pre-training covers roughly 15 trillion tokens from scratch.

The training pipeline is the actual story

Supervised fine-tuning uses about 7.2 million samples, roughly 100B tokens with ~65B trainable. The mixture is 31.6% agentic and 68.4% non-agentic, and software engineering is 69% of the agentic slice. Trajectories were generated across harnesses including OpenHands, SWE-agent, Terminus-2, MiniSWE, Codex, and Goose. Quality control used GPT-OSS-120B and Gemma 4 as judges, plus SHA-256 deduplication over the tools and messages fields.

Post-training is a multi-stage, multi-environment RL chain, not a single pass. Each stage is a separate asynchronous GRPO run that warm-starts from the previous checkpoint, with a leave-one-out baseline instead of a value network and truncated importance sampling to bound off-policy drift. The order is RLVR, then skill boosters, then SWE, Terminal, Search, then RLHF.

The agentic RL block runs only on the 8B and 30B. The 3B takes foundational RL and alignment only. That single design choice explains most of the capability gap across sizes. Training ran on NeMo-RL and NeMo-Gym over an NVIDIA GB200 NVL72 cluster hosted by CoreWeave.

Two supporting pieces matter: 1 trillion tokens of synthetic code from IBM&#8217;s CodeAlchemy pipeline, and a speculative decoding layer for faster serving.

Reported results

IBM&#8217;s numbers, by size (3B / 8B / 30B):

Benchmark3B8B30BSWE-Bench VerifiedNA47.6757.00Terminal-Bench 2.1NA20.5629.24τ³-bench50.9966.3468.05BFCL (v4)52.4150.2961.39AIME2578.3386.6789.17GPQA54.8064.1466.41MMLU-Pro67.8474.0477.60RULER 128K55.3071.4181.38

Speech: 470M parameters, no LLM backbone

The Turbo CTC models come in at 470 million parameters and drop the LLM backbone entirely, using connectionist temporal classification to map audio to text. IBM reports an RTFx throughput near 12,600 on a single H200, against roughly 6,000 for current speed leaders on the Open ASR leaderboard. A WebGPU demo is live.

Key Takeaways

Granite 4.2 ships dense 3B/8B/30B reasoning models under Apache 2.0.

A thinking / low-effort / non-thinking switch is exposed in the chat template.

Agentic RL (SWE, Terminal, Search) trains only the 8B and 30B.

The 30B hits 57.00 on SWE-Bench Verified and 29.24 on Terminal-Bench 2.1.

Granite Speech 5.0 Turbo CTC is 470M parameters with no LLM backbone.

Check out the IBM Research blog, the technical write-up, and the GitHub repo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post IBM Releases Granite 4.2: Bringing Native Reasoning and Agentic RL to Open Enterprise Models appeared first on MarkTechPost.