---
publish_time: 1792379958
link: https://www.marktechpost.com/2026/10/18/nvidia-runai-open-source-gpu-orchestration-kubernetes/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA 将完整的 Run:ai 平台以 Apache 2.0 协议开源，源码已发布于 GitHub。Run:ai 提供生产级 GPU 调度、配额与负载管理能力，现成为 NVIDIA DSX AI Factory 平台的一部分。平台团队可自由查看、fork 并自托管整套栈，无需付费许可即可获得生产级 GPU 编排能力。此举把此前商业化的 GPU 调度能力交到开发者与平台团队手中，降低了大规模 GPU 集群的资源利用率与多租户管理门槛，也强化了 NVIDIA 在 AI 工厂基础设施层的生态绑定。
---

# 英伟达开源 Run:ai：Kubernetes GPU 编排平台

> 原文链接：https://www.marktechpost.com/2026/10/18/nvidia-runai-open-source-gpu-orchestration-kubernetes/
> 来源：MarkTechPost

NVIDIA has released the full NVIDIA Run:ai platform as open source software. The source code ships under the Apache 2.0 license on GitHub. NVIDIA Run:ai open source puts production GPU scheduling, quotas and workload management in developers&#8217; hands. The release, makes Run:ai part of the NVIDIA DSX AI Factory platform. Platform teams can now inspect, fork and self-host the stack without a paid subscription.

TL;DR

Size: Monorepo with control plane, cluster services, installer, CLI and MCP server. Local dev builds about 50 Go services.

Runs on: Kubernetes or OpenShift clusters with NVIDIA GPUs. Local dev runs on macOS or Linux with 8 simulated Tesla-A10 GPUs, no GPU needed.

Performance: NVIDIA published no platform-level benchmark for this release.

Best: The related Model Streamer loaded models 3x to 6x faster on 8 NVIDIA H100 VMs on Azure.

Worst: The community edition has no NVIDIA enterprise support. Local builds need 16 GB RAM and 100 GB disk on Linux.

What is NVIDIA Run:ai?

NVIDIA Run:ai is an AI workload and GPU orchestration platform for Kubernetes from NVIDIA. It schedules development, training and inference workloads across shared GPU clusters. It runs on top of Kubernetes and does not replace it.

The control plane handles workload submission, resource management and monitoring. Cluster services run on each Kubernetes cluster and add GPU-aware scheduling. Users reach it through a web UI, CLI, REST API and an MCP server for AI assistants.

What are the 4 modular components?

NVIDIA split the release into 4 components that teams can adopt independently:

KAI Scheduler is the Kubernetes-native scheduling engine. It is Apache 2.0 and a CNCF Sandbox project. It covers gang scheduling, time-based fair-share, topology awareness, bin-packing and DRA support.

GPU Fractioning Operator brings CUDA 13.4-native GPU fractions to Kubernetes. The CUDA driver enforces a hard memory limit per workload. NVIDIA retired its older proprietary fractioning in favor of this approach. The operator is scheduler-agnostic and exports per-pod metrics.

KAI Resource Management adds projects, departments, quotas and node pools. NVIDIA&#8217;s example guarantees 50% of a cluster to a research team.

Workload Map is a Go library that describes workload types such as PyTorchJob, RayCluster and KServe services. It works offline and does not schedule, queue or autoscale.

How do developers run NVIDIA Run:ai locally?

The local development guide stands on 1 script, local-dev.sh. It builds about 50 Go services from source inside containers. It then creates a 5-node Kind cluster pinned to Kubernetes v1.32.5. A fake GPU operator simulates 8 Tesla-A10 GPUs, so no GPU hardware is required.

Supported hosts: macOS or Linux, on amd64 or arm64. Windows is not supported.

Linux hosts need 4 CPUs, 16 GB RAM and 100 GB free disk.

macOS Podman VMs need at least 12 GB RAM.

1 full build leaves about 44 GB of caches.

The --gpu-operator flag switches to real NVIDIA GPUs. That mode needs Linux, Docker and the NVIDIA Container Toolkit. AMD and Intel accelerators are not supported.

How can teams deploy it in production?

Dev teams can deploy from source or from the NGC Community Product Helm chart. That edition needs no paid subscription but excludes NVIDIA enterprise support.

Teams can also adopt it through 8 DSX ecosystem partners. These are Crusoe, Mirantis, Nebius, OpenNebula Systems, Rafay, Saturn Cloud, Spectro Cloud and vCluster. Supported commercial editions continue through NVIDIA AI Enterprise, NVIDIA Mission Control and select cloud marketplaces.

What related open source projects ship alongside?

Two adjacent projects round out the stack. Model Streamer streams model weights directly into GPU memory. vLLM and SGLang enable it with --load-format runai_streamer.

Microsoft&#8217;s published benchmark used 8 NVIDIA H100 VMs. It showed 3x to 6x faster loading than the default loader. Throughput held at 80 Gbps versus about 40 Gbps on the default path.

Grove orchestrates multicomponent inference workloads. It starts components such as prefill and decode as all-or-nothing units.

&&&

How does NVIDIA Run:ai compare with other open source Kubernetes schedulers?

FeatureNVIDIA Run:ai (open source)VolcanoKueueApache YuniKornLicenseApache 2.0Apache 2.0Apache 2.0Apache 2.0GovernanceNVIDIA DSX AI Factory org (KAI Scheduler: CNCF Sandbox)CNCF Incubatingkubernetes-sigs (wg-batch)Apache Software FoundationScopeFull platform: control plane, UI, CLI, REST API, MCP serverBatch scheduling systemJob queueing controllerScheduler, alternative to defaultReplaces kube-schedulerNo, extends it with KAI SchedulerNot disclosedNoYes, as an alternativeGang schedulingYesYesTimeout-based all-or-nothingYesQuota hierarchyProjects, departments, node poolsMulti-level queuesCohorts, fair sharingHierarchical queuesGPU sharingCUDA 13.4-native fractions with hard memory limitsvGPU, dynamic MIGDRA-based GPU quota; fractioning not in overviewNot disclosedTopology-awareYesYesYesNot disclosedMulti-clusterYes, via control planeYesYes, MultiKueueNot disclosedWeb UIYesSeparate dashboard projectNot disclosedNot disclosed

The key difference is scope. Volcano, Kueue and YuniKorn focus on scheduling or queueing. Run:ai ships a full management platform on top of its scheduler.

Key Takeaways

NVIDIA Run:ai is now fully open source under Apache 2.0.

4 components ship standalone: KAI Scheduler, GPU Fractioning, Resource Management, Workload Map.

GPU fractioning now uses CUDA 13.4-native memory isolation.

Local dev runs on a 5-node Kind cluster with 8 simulated GPUs.

The free edition excludes NVIDIA enterprise support.

Check out the GitHub repo, the local dev guide and NVIDIA&#8217;s technical blog. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post NVIDIA Open Sources Run:ai Under Apache 2.0 for Kubernetes GPU Orchestration appeared first on MarkTechPost.