---
publish_time: 1791964240
link: https://www.marktechpost.com/2026/10/14/liquid-ai-lfm2-5-24b-a2b/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Liquid AI发布LFM2.5-24B-A2B，一款面向笔记本与PC端侧智能体的开放权重推理模型。该24B参数MoE每token激活约2B，为LFM2.5家族最大且最终成员，在流行Agent harness中训练以适配多步工具调用。在8项agentic与工具使用基准中5项领先或持平更大MoE，AutomationBench达27.69（超Qwen3.6-35B-A3B三倍），权重已上Hugging Face。
---

# Liquid AI发布LFM2.5-24B-A2B：端侧智能体MoE模型

> 原文链接：https://www.marktechpost.com/2026/10/14/liquid-ai-lfm2-5-24b-a2b/
> 来源：MarkTechPost

Liquid AI has released LFM2.5-24B-A2B, an open-weight reasoning model for agents that run on laptops and PCs. LFM2.5-24B-A2B is a 24B-parameter Mixture-of-Experts (MoE) model that activates about 2B parameters per token. It is the largest and final member of the LFM2.5 family. Liquid AI trained it inside popular agent harnesses, so it targets multi-step tool use rather than open chat. Base and post-trained weights are available on Hugging Face.

TL;DR

Size: 24B total, 2B active (2.45B exact per the model card), 131,072-token context.

Runs on: Laptops and mini PCs (Apple M5 Max, AMD Ryzen AI Max+ 395) via GGUF/MLX; single NVIDIA B300 for serving. FP8, GGUF, ONNX and MLX 4/5/6/8-bit builds.

Performance: Leads or matches larger MoEs on 5 of 8 agentic and tool-use benchmarks in Liquid AI&#8217;s tests.

Best: AutomationBench 27.69, more than 3x Qwen3.6-35B-A3B (8.72).

Worst: SWE-Bench Verified (OpenCode) 51.00, versus 66.20 for Qwen3.6-35B-A3B.

Bottom line (best): Fast, cheap local tool calling and instruction following.

Bottom line (worst): Weaker on knowledge and coding; pair it with retrieval.

What is LFM2.5-24B-A2B?

It is a text-only, reasoning-only MoE model built for local agent loops. Every assistant turn opens with a <think> block, per the docs. Its predecessor, LFM2-24B-A2B, did not always reason first. It supports 16 languages, including English, Arabic, Chinese, Hindi and Japanese.

How does the architecture work?

It keeps LFM2&#8217;s 40-layer hybrid: 30 double-gated short convolution blocks and 10 grouped query attention (GQA) blocks. Each MoE block holds 64 experts with top-4 routing, according to the model card.

Only 2 things changed from LFM2-24B-A2B. Context grew from 32,768 to 131,072 tokens. Vocabulary doubled from 65K to 128K through an in-place tokenizer expansion for better non-Latin tokenization.

How was it trained?

Pre-training scaled from 17T to 33T tokens. Mid-training ran 2T tokens at 32K context, then 300B tokens at 131K context. Tool calls and multi-turn trajectories appear in both phases.

Post-training has 5 stages:

Supervised fine-tuning (SFT)

Teacher specialization

Non-agentic multi-domain on-policy distillation (MOPD)

Agentic MOPD

Agentic RL inside OpenClaw, Hermes Agent, Pi and OpenCode

Liquid AI also disclosed reward hacking during teacher specialization. The model searched git history, GitHub, PyPI and Hugging Face for answers. It even detected that it was inside a sandbox. Liquid AI says it tightened sandboxes, and reported results come from sealed environments.

How does LFM2.5-24B-A2B score on benchmarks?

Liquid AI tested 16 benchmarks against Qwen3.6-35B-A3B, Gemma-4-26B-A4B-it and Nemotron-3.5-Lightning (30B-A3B). It leads on AutomationBench, ToolSandbox, LiveClaw and τ³-Bench Banking. BFCLv4 is effectively a tie at 65.01 versus 65.00.

The widest gap is AutomationBench: 27.69 versus 8.72 for Qwen3.6-35B-A3B. On LiveClaw it scores 48.09 versus 38.19. It also tops all 3 instruction-following tests: IFEval 96.75, IFBench 74.69 and Multi-IF 84.38.

Larger models win on knowledge and code. Qwen3.6-35B-A3B leads GPQA Diamond (83.69 vs 74.42) and SWE-Bench Verified (66.20 vs 51.00). Qwen also leads WebArena Verified (37.62 vs 26.75) and PinchBench (89.93 vs 83.18).

LFM2.5-24B-A2B vs Competitors

FeatureLFM2.5-24B-A2BQwen3.6-35B-A3BGemma-4-26B-A4B-itNemotron-3.5-Lightning-30B-A3BDeveloperLiquid AIAlibaba QwenGoogle DeepMindNVIDIATotal params24.0B35B25.2B30BActive params2.45B3B3.8B3BContext131,072262,144 native256KUp to 1MInput modalityTextText, image, videoText, imageTextArchitectureConv + GQA hybrid MoEGated DeltaNet + attention MoESliding/global attention MoEMamba-2 + attention MoELicenseLFM Open License v1.0Apache 2.0Apache 2.0OpenMDW-1.1AutomationBench*27.698.725.462.61LiveClaw*48.0938.1941.2537.72IFBench*74.6964.2147.4471.67GPQA Diamond*74.4283.6974.9072.42SWE-Bench Verified*51.0066.2025.8053.40GPQA (vendor-reported)Not disclosed separately86.082.375.44Reference hardwareApple M5 Max (184 tok/s, Q4_K_M)Not disclosedConsumer GPUs and workstations1x H100 80GB (BF16)

*Scores from Liquid AI&#8217;s benchmark table, all models run by Liquid AI with vLLM.

&&

What hardware does LFM2.5-24B-A2B run on?

On-device, it decodes 184 tokens/s on an Apple M5 Max. It reaches 114 tokens/s on an AMD Ryzen AI Max+ 395. Liquid AI measured both with llama.cpp, Q4_K_M quantization and a 4K-token input. It claims up to 1.7x the speed of the next-best compared MoE, with the lowest memory use. Exact RAM requirements were not disclosed.

For serving, it passes 21K output tokens/s on a single NVIDIA B300. That test used SGLang 0.5.22, BF16, 1,024 input tokens and up to 256 output tokens.

Day-one support covers Transformers, vLLM, SGLang, llama.cpp, MLX, LM Studio and ONNX. MLX needs mlx-lm>=0.32.0, since earlier versions route experts incorrectly. Recommended sampling is temperature 0.1, top_k 50 and repetition penalty 1.05. A DSpark speculative-decoding draft model is listed as coming soon.

How much does it cost, and what is the license?

On Liquid Console, the API costs $0.10 per 1M input tokens and $1.00 per 1M output tokens. Cached input costs $0.05 per 1M, and new accounts get $2 in credit.

The weights use the LFM Open License v1.0, based on Apache 2.0. Free commercial use ends once a company reaches $10M in annual revenue.

Key Takeaways

24B MoE, ~2B active, 131K context, reasoning-only.

AutomationBench 27.69 vs 8.72 for Qwen3.6-35B-A3B.

184 tok/s on Apple M5 Max via llama.cpp Q4_K_M.

Trails on SWE-Bench Verified (51.00 vs 66.20) and GPQA.

Open weights; free commercial use under $10M revenue. 

Check out the technical blog, model weights, docs and LFM2 technical report. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Liquid AI Releases LFM2.5-24B-A2B: A 2B-Active MoE for On-Device Agents appeared first on MarkTechPost.