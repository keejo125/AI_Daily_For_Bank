---
publish_time: 1786517980
status: confirmed
category: 国际
is_model_related: true
digest: |
  NVIDIA 发布两项面向「常驻 AI 智能体」的开源技术：Nemotron 3.5 Lightning 轻量可定制开源模型，以及 NeMo Switchyard 开源路由库。前者是 30B 参数的混合专家（MoE）模型、3B 激活参数，采用 Mamba-2 + MoE + Attention 混合架构，专为高吞吐的 Agent 任务设计。

  两者共同解决一个结构性问题：长时运行的 Agent 把大量时间花在工具调用、结果校验与子智能体委派上，每步都送往前沿推理模型带来成本与延迟。Switchyard 将 Agent 工作流的每一步路由到最合适、最高效的模型，实现成本与能力间的动态平衡。
link: https://www.marktechpost.com/2026/08/11/nvidia-ai-releases-nemotron-3-5-lightning-and-nemo-switchyard/
source: MarkTechPost
---

# 英伟达发布 Nemotron 3.5 Lightning：30B 开源 MoE 模型与 NeMo Switchyard 路由库

> 原文链接：https://www.marktechpost.com/2026/08/11/nvidia-ai-releases-nemotron-3-5-lightning-and-nemo-switchyard/
> 来源：MarkTechPost

NVIDIA introduced open technologies for building always-on AI agents from systems of specialized models. Two artifacts shipped together. Nemotron 3.5 Lightning is a lightweight, customizable open model built for high-volume agentic tasks, and NeMo Switchyard is an open source routing library that directs each step of an agent workflow to the most capable and efficient model available. The problem both address is structural: long-running agents spend most of their time on tool calls, result validation, and subagent delegation, and sending every one of those steps to a frontier reasoning model adds cost and latency. Lightning is a 30B mixture-of-experts model with 3B active parameters, built on a hybrid Mamba-2 + MoE + Attention architecture with a 1M-token context window. NVIDIA reports up to 4x faster output speed than similar-sized models, and 30% faster completion of 10,000 PinchBench tasks than Qwen3.6 35B at comparable accuracy. Many industry players like CrowdStrike, Harvey, CodeRabbit, Fastino Labs, and Lila Sciences are already customizing it for cybersecurity, legal, coding, finance, and healthcare workloads.

Is it deployable?

Yes. Nemotron 3.5 Lightning is generally available under the permissive OpenMDW-1.1 license, with open weights, training data, and recipes. NVIDIA states the model is ready for commercial use.

Which companies: Anyone with a single modern GPU. NVIDIA lists single-GPU deployment on 1x DGX Spark (GB10) or 1x H100. That puts solo developers and seed-stage startups on the same footing as enterprises. Mid-market teams can serve it from Baseten, Together AI, or Nebius; regulated enterprises can keep it fully on-premises.

Industries: Cybersecurity, legal services, software engineering, financial services, healthcare, and life sciences all appear in NVIDIA&#8217;s named customer set.

Applications: Tool calling, result validation, subagent delegation, code review routing, log triage, contract parsing, and long-context retrieval across a 1M-token window.

The execution layer, not the planning layer

Long-running agents spend most of their time on high-volume execution. Tool calls, result validation, and subagent delegation dominate the token budget. Routing every one of those steps to a frontier reasoning model adds cost and latency.

Nemotron 3.5 Lightning targets that execution layer. It is a 30B mixture-of-experts model with 3B active parameters, built on a hybrid Mamba-2 + MoE + Attention architecture. Context length reaches 1M tokens. Pre-training covered more than 20 trillion tokens using an NVFP4 recipe.

The model is the smallest member of the Nemotron 3 family. Frontier models such as Nemotron 3 Ultra handle orchestration and planning, while Lightning handles the routine calls beneath them.

Where the speed comes from

Two mechanisms:

First, Speculative Decoding: Multi-token prediction was baked in during a dedicated pre-training stage, then improved with an MTP-boosting phase. NVIDIA also ships two external draft models: DSpark, a semi-autoregressive drafter recommended for DGX Spark and low-concurrency data center workloads, and DFlash, which uses a lightweight block-diffusion model.

Second, Quantization: An NVFP4 checkpoint ships alongside BF16. The same checkpoint serves Blackwell and Hopper natively, and extends to Ampere through W4A16 kernels.

NVIDIA reports up to 4x output speed versus similar-sized models. On PinchBench, it reports 86% accuracy while completing 10,000 tasks 30% faster than Qwen3.6 35B at comparable accuracy.

Published model card results (BF16 / NVFP4): MMLU Pro 81.94 / 81.62, GPQA Diamond 75.44 / 75.57, SWE-bench Verified 51.56 / 52.80, Terminal-Bench 2.1 24.58 / 23.46, AA-LCR 52.00 / 49.19. Recommended sampling is temperature 1.0 and top_p 0.95.

NeMo Switchyard

NeMo Switchyard is an open source library that routes each step of an agent workflow to the most capable and efficient model available.

It offers tuning-free routers, including an LLM classifier with session affinity, a stage router that reads recent tool activity, and an escalation router that starts cheap and promotes on sustained difficulty. A tunable prefill router learns from the model&#8217;s residual stream to predict which candidate will succeed. The reference server accepts OpenAI, Anthropic, and Responses API requests.

Two published results: LangChain benchmarked 145 multi-turn agentic tasks. Routing between Lightning and Claude Opus 4.8 with the escalation router cut cost 74% versus a frontier-only baseline, sending 7% of calls to the frontier model, at a roughly 6-point accuracy tradeoff. Cognition implemented staged routing in Devin Desktop. On FrontierCode Main, routing between Opus 5 and Kimi K2.7 reached 50.6% at a $3.11 mean cost, within 2.8 points of Opus 5 accuracy at approximately 28% lower mean cost.

Interactive explainer

Key Takeaways

30B open MoE with 3B active parameters, 1M context, OpenMDW-1.1 license, commercial use permitted.

Up to 4x output speed; PinchBench 10,000 tasks completed 30% faster than Qwen3.6 35B.

Speed comes from multi-token prediction plus DSpark and DFlash drafters, and an NVFP4 checkpoint.

Runs on 1x DGX Spark or 1x H100, and locally via Ollama, LM Studio, llama.cpp, and Unsloth.

NeMo Switchyard cut cost 74% in LangChain&#8217;s 145-task benchmark at a ~6-point accuracy tradeoff.

Try it on build.nvidia.com or OpenRouter, and download weights from Hugging Face or ModelScope. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA AI Releases Nemotron 3.5 Lightning: A 30B Open MoE with 3B Active Parameters, and NeMo Switchyard Model Router appeared first on MarkTechPost.