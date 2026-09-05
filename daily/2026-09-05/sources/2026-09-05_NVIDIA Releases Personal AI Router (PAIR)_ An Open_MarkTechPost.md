---
publish_time: 1788580343
link: https://www.marktechpost.com/2026/09/04/nvidia-releases-personal-ai-router-pair-an-open-source-virtual-inference-router-that-distributes-local-ai-requests-across-rtx-dgx-spark-and-mac-nodes/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA发布个人AI路由器PAIR（Personal AI Router）：一个开源虚拟推理路由器，发现家庭网络中的兼容机器，把独立的本地推理请求调度到不同节点（RTX、DGX Spark、Mac），解决多智能体工作流中单引擎请求互相争抢、同网其他设备闲置的瓶颈。PAIR不是新推理引擎，Ollama或LM Studio仍负责实际执行。本周以v0.1.1公测放出，提供Windows/macOS/Linux签名安装包，源码以Apache 2.0发布在GitHub，完全本地运行，仅下载模型需联网。它代理Ollama/LM Studio兼容接口，无缝接管各引擎默认端口。
---

# 英伟达发布个人 AI 路由器 PAIR：开源本地推理调度器

> 原文链接：https://www.marktechpost.com/2026/09/04/nvidia-releases-personal-ai-router-pair-an-open-source-virtual-inference-router-that-distributes-local-ai-requests-across-rtx-dgx-spark-and-mac-nodes/
> 来源：MarkTechPost

Multi-agent workflows have changed the shape of local inference. A lead agent decomposes a task and spawns subagents. What looked like one user request becomes dozens of independent model calls. Pointed at a single local engine, those calls compete for the same execution slots. The queue grows while a workstation, laptop, or DGX Spark on the same network sits idle.

NVIDIA Personal AI Router (PAIR) targets exactly that bottleneck. Announced this week, PAIR is a virtual inference router. It discovers compatible machines on a home network and schedules independent inference requests across them. It is not a new inference engine. Ollama or LM Studio still executes the model on whichever node PAIR selects.

Is it deployable? Yes. PAIR ships today as a public beta (v0.1.1) with signed installers for Windows, macOS, and Linux, and the full source is on GitHub under Apache 2.0. It runs entirely on the local network, with internet needed only to download models. 

No new API

The design decision that matters most is that PAIR introduces no cluster API. It proxies the Ollama-compatible and LM Studio-compatible interfaces agents already speak, taking over the default port each engine uses. If a harness listens elsewhere, the proxy port is configurable in PAIR&#8217;s engine settings. The repository also exposes OpenAI-compatible proxy endpoints.

The consequence: existing agent harnesses need no changes. The agent decides what work to request. PAIR decides where it runs.

Discovery, pairing, and transport

PAIR uses mDNS to find nearby systems automatically. A node can be added by IP address when discovery fails. Trust is established by a six-digit PIN shown on the inviting machine and entered on the invited one. All node-to-node communication is blocked until that pairing completes. Traffic between paired nodes is then secured with mTLS using generated certificates.

Each node runs Ollama or LM Studio. PAIR can install an engine and start model downloads on paired systems, removing most cross-machine setup work.

How the scheduler picks a node

A node becomes eligible for a request only when the required engine is enabled and the exact requested model is present. Models do not need to be identical across the cluster, different systems can hold different models, and PAIR routes according to model location. Loading the same tag on more nodes simply widens the eligible pool.

For each request the scheduler weighs five signals. Is the node online and ready. Is a supported engine enabled. Is the exact model present. What is the current node and engine job load. What is existing GPU utilization.

This is workload-level concurrency, and the boundary is explicit. PAIR assigns each request to one eligible node, where it stays for its lifetime. It does not pool VRAM, merge GPUs into one larger accelerator, or shard a single request across machines.

&&

The demo numbers, with their caveats

NVIDIA&#8217;s demonstration pairs PAIR with Hermes Desktop, which creates a five-subagent workload over a synthetic household inbox. Ollama executes Qwen 3.6 35B A3B on each selected node.

On one RTX Spark laptop, the workload took 18 minutes on average. On a three-device PAIR cluster consisting of an RTX Spark laptop, a DGX Spark, and an RTX 5090, it averaged 8 minutes and 48 seconds.

Supported hardware and requirements

PAIR supports GeForce RTX 20 Series GPUs and newer, RTX PRO workstation GPUs from Turing onward, DGX Spark, and Apple M4 or newer silicon. Windows, Linux, and macOS nodes can all be paired with each other, on x64 and arm64, though Windows on ARM is experimental. Validated configurations list 8 GB RAM or higher and a recommended 20 GB of disk. Other Linux distributions build from source.

Key Takeaways

PAIR routes each independent request to one node; it never pools VRAM or shards a model.

It proxies existing Ollama and LM Studio endpoints, so agent harnesses need no changes.

Eligibility depends on node readiness, enabled engine, exact model presence, job load, and GPU utilization.

NVIDIA&#8217;s five-subagent demo went from 18 minutes on one laptop to 8:48 on three devices, unofficially.

Apache 2.0 and beta: one scheduling policy today, blind to VRAM, GPU class, and model warmness.

Check out the NVIDIA PAIR product page, NVIDIA Technical Blog, GitHub repository, Playbook and FAQ. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Releases Personal AI Router (PAIR): An Open Source Virtual Inference Router that Distributes Local AI Requests Across RTX, DGX Spark, and Mac Nodes appeared first on MarkTechPost.