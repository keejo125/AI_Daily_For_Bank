---
publish_time: 1792814189
link: https://www.marktechpost.com/2026/10/23/nvidia-nemotron-3-5-bolt-e4b-4gb/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  NVIDIA 发布 Nemotron 3.5 Bolt E4B 4GB，一款面向快速对话 Agent 的开放小语言模型，目标是在 RTX、Jetson 与 Spark 硬件本地运行的语音助手、游戏 NPC 与机器人接口。该模型以谷歌 Gemma 4 E4B 为基础、仅用强化学习后训练，约 8B 总参数、4B 有效参数、64K 上下文；Q4_K_M 构建在 RTX 上仅占 3.1–4.3GB 显存，为语音与视觉模型留出余量。NVIDIA 测得其在 21 项基准中 15 项优于 Gemma 4 E4B、Qwen3.5-4B 与 Nemotron 3 Nano 4B；IHEval 达 84.8（Gemma 4 E4B 为 67.0），但 Tau2-Bench 仅 55.1，落后 Qwen3.5-4B 的 75.1，呈现小模型本地化的能力—开销权衡。
---

# 英伟达发布 Nemotron 3.5 Bolt E4B：4GB 开放小语言模型

> 原文链接：https://www.marktechpost.com/2026/10/23/nvidia-nemotron-3-5-bolt-e4b-4gb/
> 来源：MarkTechPost

NVIDIA has just released Nemotron 3.5 Bolt E4B 4GB, an open small language model for fast conversational agents. It targets voice assistants, game NPCs and robot interfaces running locally on RTX, Jetson and Spark hardware. The model is post-trained from Google&#8217;s Gemma 4 E4B using reinforcement learning only. For developers, this is agent behavior in about 4GB of VRAM. That leaves room for speech and vision models.

TL;DR

Size: 8B total parameters, 4B effective, 64K context.

Runs on: GeForce RTX, Jetson, RTX Spark and DGX Spark. The Q4_K_M build used 3.1 to 4.3 GB VRAM on RTX in NVIDIA tests.

Performance: Top score on 15 of 21 benchmarks against Gemma 4 E4B, Qwen3.5-4B and Nemotron 3 Nano 4B (NVIDIA-measured).

Best: IHEval 84.8, versus 67.0 for Gemma 4 E4B and 60.6 for Qwen3.5-4B.

Worst: Tau2-Bench 55.1, about 20 points behind Qwen3.5-4B at 75.1.

What is Nemotron 3.5 Bolt E4B?

Nemotron 3.5 Bolt E4B is a small language model from NVIDIA that powers local conversational agents. It combines natural dialogue with multi-turn tool calling. NVIDIA lists 3 target workloads: device and voice assistants, interactive characters, and embedded or industrial agents.

The research report shows a Reachy Mini robot running on a Jetson Orin Nano 8GB. In that demo, Cosmos 3 Edge handles vision while Bolt handles speech replies and tool calls. NVIDIA team also calls Bolt the third-generation small model for NVIDIA ACE game characters.

Core features from the launch post:

Multi-turn tool use, with guidance for asynchronous tool calls.

A conversational_mode flag for short, speech-ready replies.

Configurable reasoning, plus a runtime thinking budget to cap latency.

64K context for history, tool definitions and application state.

How was Bolt E4B trained?

NVIDIA skipped supervised fine-tuning entirely. As per the research report, SFT improved tool calling but hurt Gemma&#8217;s conversational quality and verbosity. Instead, the research team used RLVR and RLHF through NeMo-RL and NeMo-Gym.

Every training sample ran in both reasoning and non-reasoning modes. Each batch kept a 2:1 ratio of non-reasoning to reasoning samples. Length penalties in the GenRM environment stopped answers from growing during training. The datasets and the full recipe are public.

For deployment, NVIDIA quantized the BF16 checkpoint to Q4_K_M with importance-matrix calibration. Calibration used about 1M tokens of RL rollouts. The release also ships a DFlash drafter for speculative decoding. On an RTX 5070, Bolt with DFlash reached 272.6 tokens/s. Gemma 4 E4B with its MTP drafter reached 225.9 tokens/s, so Bolt is 1.21x faster.

How does Nemotron 3.5 Bolt E4B perform on benchmarks?

NVIDIA grouped 21 benchmarks into 5 capability areas. All scores here are BF16, measured by NVIDIA in its own NeMo-Gym harness. Bolt led 15 of 21 rows in reasoning mode.

NVIDIA also reports roughly 40% higher average scores than Nemotron 3 Nano 4B. It claims up to 80% fewer output tokens in reasoning-enabled comparisons. Separately, Scale Labs ranked Bolt first among small models on MultiChallenge at 56.03%, per an X post.

Bolt does not win everywhere. Qwen3.5-4B leads on Tau2-Bench (75.1 vs 55.1) and RULER 64K (95.1 vs 87.0). It also leads LongBench v2 (59.9 vs 50.5) and BFCL-v3 (70.9 vs 68.5). Gemma 4 E4B keeps a narrow edge on EQ-Bench v3 (41.1 vs 39.4).

How does Bolt E4B compare with other small models?

FeatureNemotron 3.5 Bolt E4BGemma 4 E4BQwen3.5-4BNemotron 3 Nano 4BParameters8B total, 4B effective8B with embeddings, 4.5B effective4B (language model)3.97BArchitectureGemma 4 E4B, RL post-trainedDense with Per-Layer EmbeddingsGated DeltaNet + attention hybridMamba-2 + Transformer hybridContext64K128K262K262KLicenseOpenMDW-1.1Apache 2.0Apache 2.0NVIDIA Nemotron Open Model LicenseInputsText (card); NIM also accepts image and audioText, image, audioText, image, videoTextIHEval*84.867.060.651.3MultiChallenge*53.142.151.835.3Tau2-Bench*55.138.575.129.2RULER 64K*87.086.595.191.5AvailabilityOpen weights; free API on build.nvidia.comOpen weightsOpen weightsOpen weights

*Benchmark rows are NVIDIA-measured BF16 scores from the Bolt launch post. Vendor-reported scores differ.

What hardware does it run on?

NVIDIA measured the Q4_K_M build with llama.cpp at batch size 1. The figures below use 3K input and 50 output tokens.

DeviceVRAM (GB)Time to first token (ms)Tokens/sRTX 5070 (12GB)3.5548133.4RTX Spark (32GB)3.193067.0Jetson AGX Orin (32GB)4.23,68724.0Jetson Orin Nano (8GB)4.25,78515.5

The &#8216;4GB&#8217; label describes a target memory envelope, not the file size. The Q4_K_M GGUF on Hugging Face is 6.18 GB.

Bolt is available on Hugging Face, Ollama, LM Studio, Unsloth and Jetson AI Lab. It also ships as an NVIDIA NIM and through the In-Game Inferencing SDK.

Key Takeaways

Gemma 4 E4B, post-trained by NVIDIA with RL only, no SFT.

Leads 15 of 21 agent benchmarks in NVIDIA&#8217;s own harness.

IHEval 84.8 is the standout; Tau2-Bench 55.1 is the weak spot.

&#8216;4GB&#8217; is the VRAM target; the GGUF file is 6.18 GB.

Open weights, data and recipes under OpenMDW-1.1.

Check out the technical report, GGUF model, BF16 model and training recipe. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Releases Nemotron 3.5 Bolt E4B 4GB: An Open Small Language Model for Local Voice Agents, Game Characters and Robots appeared first on MarkTechPost.