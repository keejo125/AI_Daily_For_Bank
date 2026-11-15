---
publish_time: 1792557220
link: https://www.marktechpost.com/2026/10/20/llm-d-1-0-open-source-distributed-inference-stack/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google 团队发布 llm-d 1.0，这是其分布式推理栈的首个稳定版本——一个 Kubernetes 原生的开源层，将 vLLM 或 SGLang 模型服务器编排为统一协同的资源池，面向自托管 Agent 与 RL 负载（这类场景下轮询负载均衡会失效）。llm-d 由 Red Hat、IBM、Google Cloud、CoreWeave 与 NVIDIA 于 2025 年创立，现已有超 500 名贡献者，是 CNCF Sandbox 项目（Apache 2.0）。1.0 新增多租户 QoS 流控、路由器高可用与零停机升级、会话感知路由等“day 2”能力，并支持 NVIDIA/AMD/Intel GPU 与 Google TPU。其核心是缓存感知路由：路由器追踪各副本持有的缓存前缀，按负载与预测延迟选节点；KV 缓存在显存/主机内存/SSD/Managed Lustre 间分层，Prefill 与 Decode 分离部署。官方基准：Ironwood TPU 上中位 TTFT 降低 85%+、吞吐 2.4x；17000 节点 GKE 跨 3 集群吞吐扩展 2.9x（99.9% 成功率）。
---

# Google Cloud 发布 llm-d 1.0：面向 TPU 与 GPU 集群的缓存感知路由

> 原文链接：https://www.marktechpost.com/2026/10/20/llm-d-1-0-open-source-distributed-inference-stack/
> 来源：MarkTechPost

Google team have released llm-d 1.0, the first stable version of its distributed inference stack. This open-source, Kubernetes-native layer turns vLLM or SGLang model servers into one coordinated pool. They released it at the PyTorch Conference North America. It targets self-hosted agent and RL workloads, where round-robin load balancing breaks down.

TL;DR

A serving stack: Google reports a published benchmark on a 17,000-node multi-region GKE deployment. 

Runs on: Kubernetes with NVIDIA, AMD or Intel GPUs or Google TPUs, over vLLM or SGLang. 

Performance: Vendor-reported gains come from cache-aware routing, tiered KV cache offload and prefill/decode disaggregation.

Best: Median TTFT cut by more than 85%, with 2.4x throughput, on an Ironwood TPU coding workload.

Worst: RL time-slicing lifts accelerator duty cycle only to above 70%, so roughly 30% idle time remains.

What is llm-d 1.0?

llm-d was founded in 2025 by Red Hat, IBM, Google Cloud, CoreWeave and NVIDIA. Red Hat, IBM and Google are the lead maintainers. The project counts more than 500 contributors from over 25 organizations. It is a CNCF Sandbox project, accepted on March 12, 2026, and is licensed under Apache 2.0.

Prefix-aware routing, KV cache offloading, prefill/decode disaggregation, wide expert parallelism and batch inference already shipped. Version 1.0 is about running them reliably in production, which IBM calls day 2 operations.

What is new in llm-d 1.0?

Multi-tenant quality of service: Priority and fairness-aware flow control stops bursty agents from starving latency-sensitive requests.

Stable foundation: v1 APIs and a hardened request path, validated on multiple clouds and accelerators.

Zero-downtime upgrades: Router high availability with hot standby, plus DisaggregatedSet, which rolls prefill and decode pools together.

Agent-aware serving: Session-aware routing, turn-priority scheduling and native Responses API state.

Async inference: llm-d-async-processor pulls jobs from Google Cloud Pub/Sub or Redis into slack capacity.

Expanded TPU support: TorchTPU runs PyTorch models natively inside upstream vLLM and SGLang.

How does llm-d route requests?

The llm-d router builds on the Kubernetes Gateway API Inference Extension. It tracks which replicas hold each cached prefix. It then weighs load and predicted latency before picking a replica. Agents call one endpoint, and each step lands where its context already lives.

When accelerator memory fills, KV cache moves to host memory, then SSD or Managed Lustre. It uses vLLM&#8217;s OffloadingConnector, Mooncake or SGLang&#8217;s HiCache for this. Prefill and decode run as separate pools, because prefill is compute-heavy and decode is memory-bound.

What do the llm-d 1.0 benchmarks show?

All figures below are self-reported by Google and llm-d adopters.

Ironwood TPU (TPU 7x): prefix-aware routing plus host memory offload cut median TTFT by more than 85%. Throughput rose 2.4x versus a plain Kubernetes Service.

Gemini platform: prefix cache hit rate doubled from 35% to 70%. TTFT fell more than 35% for coding agents. P95 TTFT fell more than 50% under bursty chat.

17,000-node GKE benchmark: throughput scaled 2.9x across 3 clusters, with 99.9% success and under 1% overhead.

A3 Mega, 70B model: Lustre plus CPU RAM offload improved TTFT by about 40% on 50k-token prompts. End-to-end latency fell 30% and GPU-hours fell nearly 60%.

RL time-slicing: accelerator duty cycle rose from about 40% to above 70%.

Adopters report similar patterns. Snap reports prefix cache hit rates of up to 75 to 80%. Zenteiq reports over 4x throughput, from 1.47 billion to 5.97 billion daily tokens per 1,000 TPU v6e chips. An IBM demo served 3,000 concurrent coding agents at 5 to 10 times below API pricing.

How does llm-d compare with NVIDIA Dynamo and AIBrix?

Featurellm-d 1.0NVIDIA DynamoAIBrixLatest version1.0 (Oct 20, 2026)v1.5.1 (Oct 6, 2026)v0.7.0 (Jun 16, 2026)LicenseApache 2.0Apache 2.0Apache 2.0GovernanceCNCF SandboxNVIDIA-led (ai-dynamo org)vLLM project org, ByteDance originEnginesvLLM, SGLangSGLang, TensorRT-LLM, vLLMvLLM, SGLang, TensorRT-LLMAcceleratorsNVIDIA, AMD, Intel GPUs, Google TPUNVIDIA GPUs (Blackwell, Hopper, Ada, Ampere)Mixed GPUs (heterogeneous serving)Cache-aware routingYes, prefix and load-awareYes, KV-awareYes, gateway routingKV cache tiersHBM, CPU, SSD, Managed LustreGPU, CPU, SSD, remote storage (KVBM)Distributed KV cacheP/D disaggregationYes, DisaggregatedSetYesYesHeadline result2.9x throughput, 17,000 nodes (self-reported)2x faster TTFT, Qwen3-Coder 480B (Baseten)Not disclosed

These are not strict rivals. CoreWeave runs llm-d alongside Dynamo, and NVIDIA contributes Dynamo components to llm-d.

How do you deploy llm-d 1.0?

On Google Cloud, GKE Inference Gateway runs the llm-d router as a managed service. It can also span clusters and regions with global failover. KEDA and HPA scale pools on queue depth and predicted latency. Kueue enforces per-model quotas. Verified Helm charts deploy TPU and GPU pools behind one endpoint.

Google team suggests a staged path. Start with prefix-aware routing in front of an existing vLLM deployment. Then add flow control, tiered KV offload and disaggregation. Published runs can be compared on Prism.

Key Takeaways

llm-d 1.0 is the first stable release, with v1 APIs.

New: flow control, router HA, DisaggregatedSet and agent-aware routing.

Gemini doubled prefix cache hits from 35% to 70%.

A 17,000-node GKE benchmark scaled throughput 2.9x.

Check out the Google Cloud announcement, the IBM Research post, the GitHub repo and the GKE docs. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Google Cloud Ships llm-d 1.0 With Cache-Aware Routing for TPU and GPU Fleets appeared first on MarkTechPost.