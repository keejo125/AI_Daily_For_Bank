---
publish_time: 1792117564
link: https://www.marktechpost.com/2026/10/15/meta-muse-spark-open-816b-open-weight-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Meta Superintelligence Labs 发布 Muse Spark Open 的开放权重版本：816B 参数 MoE，每 token 激活 42B（256 专家、每 token 8 个激活），支持文本/图像/视频/音频输入与 100 万 token 上下文，号称“迄今美国最强开放权重模型”。NVFP4 版本可跑在 2 台 M5 Ultra Mac Studio 或 4 张 Blackwell Ultra / 8 张 H200 上；智能体工具调用 MCP-Atlas 89.2 居首，但编码 Terminal-Bench 76.4 落后于 Kimi K3、GLM 5.3、Qwen3.8。
---

# Meta 发布 Muse Spark Open：816B 开放权重 MoE 模型

> 原文链接：https://www.marktechpost.com/2026/10/15/meta-muse-spark-open-816b-open-weight-model/
> 来源：MarkTechPost

Meta Superintelligence Labs has released Muse Spark Open, the open-weight version of its Muse Spark model. Muse Spark Open is an 816B-parameter Mixture-of-Experts model that activates 42B parameters per token. It takes text, image, video and audio input, returns text, and holds a 1M-token context window. Meta team claims it to be the most capable US open-weight model to date. For developers, the real news is deployment: the NVFP4 build runs on 2 Apple M5 Ultra Mac Studios.

TL;DR

Size: 816B total / 42B active parameters (256 experts, 8 active per token); 1M-token context.

Runs on: 2 Mac Studios (M5 Ultra, 512 GB each) via MLX; 4 Blackwell Ultra GPUs or 8 H200s with NVFP4; about 300 GB setups via Unsloth 2-bit GGUF.

Performance: Strong on agentic tool use; mid-pack among large open models on coding.

Best: MCP-Atlas 89.2, the top score in Meta&#8217;s comparison table.

Worst: Terminal-Bench 2.1 76.4, behind Kimi K3 (85.0), GLM 5.3 (83.9) and Qwen3.8 (82.0).

What is Muse Spark Open?

Muse Spark Open is a natively multimodal MoE model from Meta, built for coding and long-horizon agentic work. Weights ship in BF16 and NVFP4 on Hugging Face. The open version received extra safety post-training. Meta team states that this makes it more robust without system-level guardrails.

How does the architecture work?

The model card lists 62 layers and a hidden dimension of 8192. Each MoE layer holds 256 experts, and top-k routing activates 8 per token. Attention is grouped-query, with 128 query heads and 16 KV heads. A separate 1.8B-parameter Perception Encoder handles visual input. The vocabulary has 202,048 tokens, and training data covers more than 100 languages.

Reasoning depth is set with reasoning_effort: low, medium, high or xhigh. The default is xhigh.

How does Muse Spark Open perform on benchmarks?

Meta compares it with Kimi K3, GLM 5.3, Qwen3.8-2.4T-A95B and others at maximum reasoning effort. Its strongest results are on tool use and knowledge reliability:

MCP-Atlas: 89.2, ahead of Qwen3.8 (84.5) and GLM 5.3 (84.2).

JobBench: 61.8, narrowly ahead of GLM 5.3 (61.4).

HLE-Diamond, no tools: 26.1, versus 22.2 for Kimi K3.

AA Omniscience: 25, the top score in Meta&#8217;s table.

ZeroBench with tools: 50.0, versus 41.0 for Kimi K3.

Coding is the weak spot. On Terminal-Bench 2.1 with the Terminus 2 harness, it scores 76.4. Kimi K3 reaches 85.0, GLM 5.3 scores 83.9 and Qwen3.8 scores 82.0. Its Artificial Analysis Intelligence Index is 39. That sits behind GLM 5.3 (45), Kimi K3 (44) and Qwen3.8 (40). So &#8220;most capable US&#8221; holds, but Chinese open models still lead overall.

Some rival scores are self-reported; the evaluation methodology lists each source. 

&&

What hardware does Muse Spark Open need?

Per Meta&#8217;s developer guide, BF16 weights are about 1.6 TB. NVFP4 quantizes only the experts and lands near 530 GB. The model card recommends at least 700 GB of VRAM for NVFP4 and 2 TB for BF16.

Data center: NVFP4 on 4 Blackwell Ultra GPUs or 8 H200s.

Desktop: 2 M5 Ultra Mac Studios with 512 GB each, linked over Thunderbolt 5 with RDMA. MLX tensor parallelism splits every layer across both machines.

Workstation: Unsloth Dynamic GGUFs down to 2-bit fit in about 300 GB of combined memory.

Where can developers run it?

Day-one engines include SGLang, vLLM, TensorRT-LLM, Hugging Face Transformers, MLX, llama.cpp and Unsloth. Hosted APIs are live on Baseten, Fireworks AI, Groq, Modal, Nebius, OpenRouter and Together AI. OpenRouter lists $1.25 per 1M input tokens and $4.25 per 1M output tokens.

Two draft models speed up decoding: DFlash V2 for SGLang and DSpark for vLLM. Meta reports 3.7x single-request throughput with DFlash V2 on AMD MI355X. Fine-tuning works with TorchTitan, Hugging Face TRL and NVIDIA NeMo AutoModel.

What does the Muse Model License allow?

The Muse Model License permits use, fine-tuning, distillation and redistribution. 2 conditions matter most:

Products must display &#8220;Built with Muse Spark Open.&#8221;

Model-as-a-Service providers above $20M in 12-month revenue need a separate agreement with Meta.

Internal use, research and powering your own product features are exempt from the revenue clause.

Muse Spark Open vs Kimi K3 vs GLM 5.3 vs Qwen3.8

FeatureMuse Spark OpenKimi K3GLM 5.3Qwen3.8-2.4T-A95BTotal params816B2.8T753B2.4TActive params42B104B~40B95BContext1M1,048,5761,048,576262,144 native, up to 1,010,000InputText, image, video, audioText, image, videoTextTextLicenseMuse Model LicenseKimi K3 Licenseglm-5.3 licenseqwen3.8-max licenseReleased weightsBF16, NVFP4MXFP4 (QAT)BF16, FP8BF16AA Intelligence Index (via Meta)39444540Terminal-Bench 2.1, Terminus 2 (via Meta)76.485.083.982.0MCP-Atlas (via Meta)89.282.384.284.5Toolathlon Verified (vendor)72.876.573.072.5HLE with tools (vendor)61.056.062.556.2DeepSWE 1.1 (vendor, own harness)6067.566.956.6Desktop setup2x M5 Ultra Mac StudioNot disclosedNot disclosedNot disclosed

Key Takeaways

816B total, 42B active, 1M context, text/image/video/audio input.

Leads Meta&#8217;s open-model table on MCP-Atlas (89.2) and JobBench (61.8).

Trails Kimi K3, GLM 5.3 and Qwen3.8 on Terminal-Bench 2.1 (76.4).

NVFP4 build runs on 2 M5 Ultra Mac Studios via MLX.

Free for most; MaaS providers above $20M revenue need a deal.

Check out the model weights, research blog, developer guide and evaluation methodology. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Meta Releases Muse Spark Open: 816B Open-Weight MoE With 1M Context appeared first on MarkTechPost.