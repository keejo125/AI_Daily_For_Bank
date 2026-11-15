---
publish_time: 1792094030
link: https://www.marktechpost.com/2026/10/15/nvidia-nemotron-3-5-super-vl-release/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  NVIDIA 发布 Nemotron 3.5 Super VL，一个面向常驻企业智能体的 120B 参数 MoE 开放视觉语言模型，每 token 激活 12B，读取文本/图像/文档/视频后可在同一模型内推理、调用工具并写代码，单个开放检查点替代独立文本与视觉模型。另发 2 个边缘模型 Bolt 74B-A9B 与 Bolt E4B。官方称单 GPU 吞吐最高达开源同侪 5 倍，GPQA-Diamond 89.90，但 tau3-bench banking 仅 17.78。
---

# 英伟达发布 Nemotron 3.5 Super VL：120B 开放多模态智能体模型

> 原文链接：https://www.marktechpost.com/2026/10/15/nvidia-nemotron-3-5-super-vl-release/
> 来源：MarkTechPost

NVIDIA just released Nemotron 3.5 Super VL, an open vision-language model built for always-on enterprise agents. Nemotron 3.5 Super VL is a 120B-parameter mixture-of-experts model from NVIDIA that activates 12B parameters per token. It reads text, images, documents and video, then reasons, calls tools and writes code in one model. For developers, 1 open checkpoint replaces a separate text model along with a separate vision model. NVIDIA also shipped 2 edge models, Nemotron 3.5 Bolt 74B-A9B and Bolt E4B.

TL;DR

Size: 120B total parameters, 12B active (MoE). Context up to 1M tokens.

Runs on: 1x DGX Spark, 1x H200, 2x H100 or 1x GB200 with the NVFP4 checkpoint. A BF16 checkpoint is also published.

Performance: Strong reasoning, agentic coding and document vision. NVIDIA claims up to 5x higher single-GPU throughput than open peers.

Best: 89.90 on GPQA-Diamond (NVFP4).

Worst: 17.78 on tau3-bench banking (NVFP4).

What is Nemotron 3.5 Super VL?

It is an open multimodal agent model. Weights ship under the OpenMDW-1.1 license. NVIDIA also released open datasets, training recipes and RL environments in NeMo Gym.

The model card lists text, image and video inputs with text output. Video is limited to MP4 clips up to 2 minutes. Reasoning can be toggled on or off through the chat template.

How does the architecture work?

The backbone interleaves Mamba-2, mixture-of-experts and attention layers. Each MoE layer holds 512 routed experts. A C-RADIO vision encoder and a connector feed images, document pages and video frames into the language backbone.

Speed comes from four techniques:

Multi-token prediction: a native drafter proposes several tokens, verified in 1 forward pass.

LiLiCorr: a speculative drafter for DGX Spark, up to 2.3x faster token generation.

NVFP4 with quantization-aware distillation: 4-bit weights and activations on Blackwell, 4-bit weights with 16-bit activations elsewhere.

Context reuse: prefix caching keeps both attention caches and Mamba states across agent turns.

The model was distilled from Nemotron 3 Ultra. NVIDIA team states that it trained on about 26 trillion tokens. Post-training used roughly 3.8 million samples plus RL across dozens of environments. Continued pretraining added 10B Indic tokens.

How does it perform on benchmarks?

All scores below are NVIDIA-reported, from the NVFP4 checkpoint on the model card.

AreaBenchmarkScoreReasoningGPQA-Diamond89.90CodingSWE-bench Verified71.07CodingTerminal-Bench 2.160.80Web agentBrowseComp77.5Instruction followingIFBench71.50ChartsCharXiv reasoning79.88DocumentsMMLongBench-Doc62.82Computer useOSWorld-Verified52.3Long-horizon agenttau3-bench banking17.78

On agent harness evals, Super VL beats Nemotron 3 Ultra. It scores 63.44% on Hermes Bench versus 56.33%. On LangChain evals it scores 87.05% versus 84.3%. Ultra carries about 4.6x more total parameters.

NVIDIA team reports over 600 output tokens per second on Artificial Analysis agentic tasks via a Baseten endpoint. Its chart marks a 5x speed gap over Inkling Small.

How does it compare with similar open models?

FeatureNemotron 3.5 Super VLQwen3.5-122B-A10BInkling-SmallNemotron 3 UltraDeveloperNVIDIAAlibaba QwenThinking Machines LabNVIDIATotal / active params120B / 12B122B / 10B276B / 12B550B / 55BContextUp to 1M262,144 native, extensible to 1,010,000Not disclosed on model cardEvaluated at 1M (Ruler @1M)InputsText, image, videoText, image, videoText, image, audioNot disclosedLicenseOpenMDW-1.1Apache 2.0Apache 2.0OpenMDW-1.1Reference hardware1x DGX Spark, 1x H200, 2x H100 or 1x GB2008-GPU tensor-parallel serving exampleNot disclosedNot disclosedGPQA Diamond89.9086.689.5Not disclosedSWE-bench Verified71.0772.080.2 (bash-only harness)65 to 70.4 (across 5 harnesses)IFBench71.5076.182.282CharXiv reasoning79.8877.277.4Not disclosedBrowseComp77.563.877.4 (with context management)Not disclosedTerminal-Bench60.80 (v2.1)49.4 (v2)64.7 (v2.1, best harness)54 (v2.0)

Scores are self-reported by each vendor. Harnesses and benchmark versions differ, so treat gaps of a few points with caution.

How can developers deploy it?

Super VL is available on Hugging Face, OpenRouter, ModelScope and as an NVIDIA NIM. Supported runtimes are vLLM, SGLang and TensorRT-LLM on Blackwell and Hopper. Local paths include llama.cpp and Unsloth.

For production, Dynamo recipes add KV-aware routing. On 16 B200 GPUs at 50 tokens per second per user, NVIDIA reports 8x more users served. First-token latency drops 85%.

Customization runs through NeMo AutoModel for SFT and LoRA, and NeMo RL for reinforcement learning. NVIDIA cites early results:

Scale AI for Skydance vendor credit processing: 40x lower inference cost and 5x lower latency.

Ramp receipt-to-JSON extraction: up to 50% higher throughput and 10x lower latency expected.

AI21 for Alice threat intelligence: 40% higher accuracy.

What are the Nemotron 3.5 Bolt models?

Nemotron 3.5 Bolt 74B-A9B targets local agents. NVIDIA&#8217;s launch notes describe it as distilled from Super VL. Native 2-bit quantization fits it into 24GB of memory on RTX and DGX Spark systems. NVIDIA says it ranks #1 among open models in its class on PinchBench. It ranks #2 on BrowseComp among open models. It is available now on Hugging Face with llama.cpp, Ollama, LM Studio, Unsloth and vLLM support.

Bolt E4B 4GB arrives October 23. It targets voice assistants and embedded agents on GeForce RTX, Jetson and RTX or DGX Spark.

Key Takeaways

120B MoE, 12B active, 1M context, open weights under OpenMDW-1.1.

1 model handles text, images, documents, video, tools and code.

NVFP4 checkpoint runs on a single DGX Spark, H200 or GB200.

89.90 GPQA-Diamond, but only 17.78 on tau3-bench banking.

Bolt 74B-A9B brings a 24GB local agent model to RTX PCs.

Check out the technical report, model card and usage cookbook. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post NVIDIA Releases Nemotron 3.5 Super VL, a 120B Open Multimodal Agent Model appeared first on MarkTechPost.