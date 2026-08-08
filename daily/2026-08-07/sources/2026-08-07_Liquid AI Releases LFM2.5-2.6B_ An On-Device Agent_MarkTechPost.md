---
publish_time: 1786074147
status: pending
---

# Liquid AI Releases LFM2.5-2.6B: An On-Device Agentic Model With 128K Context, Tool Calling, And Open Weights

> 原文链接：https://www.marktechpost.com/2026/08/06/liquid-ai-lfm2-5-2-6b-on-device-agentic-model/
> 来源：MarkTechPost

Liquid AI released LFM2.5-2.6B, an agentic model that runs entirely on-device. It plans, calls tools, and works through multi-step tasks on phones, laptops, PCs, and robots. The model has 2.69B total parameters, a 131,072-token context window, and a 128,000-token vocabulary. Pre-training used approximately 34 trillion tokens. Two checkpoints shipped: LFM2.5-2.6B-Base for fine-tuning, and LFM2.5-2.6B post-trained for agentic workloads. Because inference stays local, data never leaves the device and the marginal cost of each run is near zero. Liquid AI reports tool-use and instruction-following scores competitive with models nearly four times its size.

Is it deployable

The answer is Yes. Both checkpoints are public on Hugging Face under the lfm1.0 license. Weights ship in native, GGUF, MLX, and ONNX formats, with day-one support in llama.cpp, vLLM, SGLang, and LM Studio.

Which companies: Solo developers and startups can pilot on hardware they already own. The model decodes at 220 tokens/s on an M5 Max in under 2.5 GB. Mid-market teams can self-host on one GPU: a single NVIDIA H100 SXM5 serves roughly 1.3B tokens per day. Enterprises and OEMs can push the same weights to device fleets through GGUF and ONNX. Fine-tuning is available via LoRA with TRL and Unsloth.

Which industries: Liquid AI targets automotive, consumer electronics, industrial robotics, healthcare, financial services, e-commerce, and defense. Regulated and air-gapped settings benefit most, since no prompt reaches a third-party API.

Applications: Liquid AI recommends agentic workloads, tool use, data extraction, RAG, and long-context workflows. Practical builds include on-device assistants, offline document triage over 128K inputs, form and invoice extraction, robotics command parsing, and background agents that run continuously without per-token cost. Liquid AI explicitly does not recommend the model for agentic coding or knowledge-heavy tasks.

Architecture and training budget

LFM2.5-2.6B has 2.69B total parameters across 30 layers. The stack is 22 double-gated short convolution blocks plus 8 grouped-query attention blocks. Vocabulary size is 128,000 and context length is 131,072 tokens. Pre-training used approximately 34 trillion tokens.

Liquid AI doubled the vocabulary to 128K by extending the existing tokenizer in place rather than retraining from scratch. A dedicated mid-training phase extends context to 128K. The model covers 16 languages and is text-only.

Four-stage post-training

The base checkpoint becomes an agent through four stages. 

First, two consecutive supervised fine-tuning rounds, with an SFT mix roughly seven times the size used for LFM2.5-8B-A1B. 

Second, teacher specialization: one expert per domain, trained with reinforcement learning with verifiable rewards. 

Third, multi-domain on-policy distillation, where the student rolls out under its own policy and each prompt routes to its domain teacher. 

Fourth, agentic reinforcement learning with GRPO inside real harnesses, including Hermes Agent and OpenClaw.

Benchmarks

Liquid AI compared LFM2.5-2.6B against gemma-4-E2B-it (5.1B), gemma-4-E4B-it (8B), Qwen3.5-4B (4.7B) and Qwen3.5-9B (9.7B).

BenchmarkLFM2.5-2.6Bgemma-4-E4B-itQwen3.5-9BToolSandbox77.8365.0076.44Multi-IF80.0777.3562.55IFStruct85.4976.6578.50IFBench59.1739.2456.47BFCLv456.8846.3960.13

It leads every instruction-following benchmark reported and nearly every tool use benchmark, trailing Qwen3.5-9B only on BFCLv4. Coding is where larger models keep an edge: LiveCodeBenchv6 is 59.41 versus 69.86 for Qwen3.5-9B.

Interactive explainer

Key Takeaways

2.69B params, 30 layers (22 short-conv + 8 GQA), 128K context, ~34T training tokens.

Beats gemma-4-E4B-it and Qwen3.5-9B on ToolSandbox, Multi-IF and IFStruct.

220 tok/s on M5 Max, 30 tok/s on phone, under 2.5 GB memory.

Open weights under lfm1.0, with GGUF, MLX and ONNX from day one.

Check out the Technical details, LFM2.5-2.6B, and LFM2.5-2.6B-Base. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Liquid AI Releases LFM2.5-2.6B: An On-Device Agentic Model With 128K Context, Tool Calling, And Open Weights appeared first on MarkTechPost.