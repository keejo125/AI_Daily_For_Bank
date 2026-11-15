---
publish_time: 1789373067
link: https://www.marktechpost.com/2026/09/14/nvidia-open-sources-osmo-one-yaml-orchestrates-physical-ai-training-simulation-and-robot-testing/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA 开源 OSMO，一个 Kubernetes 原生的物理 AI 工作流编排器，用单个 YAML 文件描述从训练、仿真到部署的完整流水线并在各层运行，无需触碰基础设施代码。它将物理 AI 的「三计算机问题」（数据中心 GPU 训练、RTX 工作站仿真、Jetson 边缘部署）统一为一个控制平面，各后端作为注册到 CLI 的 K8s 集群，工作流只声明平台（如 gb200、jetson-agx-thor）由 OSMO 路由。OSMO 以 Apache-2.0 许可发布，提供 Helm chart 与容器，支持本地 KIND 快速启动。
---

# NVIDIA 开源 OSMO：一个 YAML 编排物理AI训练、仿真与机器人测试

> 原文链接：https://www.marktechpost.com/2026/09/14/nvidia-open-sources-osmo-one-yaml-orchestrates-physical-ai-training-simulation-and-robot-testing/
> 来源：MarkTechPost

Robot developers do not have one compute problem. They have 3. A policy is trained on GB200 or H100 clusters, tested in Isaac Sim on RTX GPUs, then validated on a Jetson mounted inside a real robot. Each tier has its own cluster, its own scheduler, and its own glue scripts. NVIDIA OSMO is NVIDIA&#8217;s answer to that fragmentation: an open-source, Kubernetes-native workflow orchestrator that lets a team describe the whole pipeline in a single YAML file and run it across every tier without touching infrastructure code.

Deployable? Yes. OSMO is Apache-2.0 licensed, ships Helm charts and containers on NGC, and has a local quickstart that runs the full control plane on a workstation with KIND. 

The Three Computer Problem

NVIDIA frames physical AI as a three computer problem. Training happens on data-center GPUs. Simulation, physics, and sensor rendering happen on workstation-class RTX hardware. Deployment and hardware-in-the-loop (HIL) testing happen on edge devices such as Jetson AGX Thor, usually on premises. Each tier usually gets its own tooling, and the handoffs are where custom scripts accumulate.

OSMO treats all 3 as backends of one control plane. Each backend is a Kubernetes cluster registered through the CLI. Workflows never name a cluster. They name a platform (for example gb200, rtx-pro-6000, or jetson-agx-thor) and OSMO routes the task to a pool that offers it.

What a Workflow Looks Liake

The Repo&#8217;s canonical example is 3 tasks cAhained by data:A

simulation runs an Isaac Sim container on rtx-pro-6000

train-policy runs a PyTorch container on gb200 with 8 GPUs, taking the simulation task&#8217;s output as input

evaluate-thor runs a ROS app on jetson-agx-thor, consuming the trained policy and writing results to a named dataset

Dependencies come from inputs, persistence from outputs, and placement from platform. The user guide covers serial and parallel task groups, Jinja templating for parameterized workflows, retry policies, and HIGH/NORMAL/LOW priorities with preemption and GPU borrowing across pools.

Key Capabilities

Portability: The same YAML runs on a laptop (Docker/KIND) or on EKS, AKS, GKE, on-premise, or air-gapped clusters. The 6.3.0 release added a multi-provider deploy-k8s.sh that provisions OSMO on Azure AKS, AWS EKS, microk8s, or any existing cluster, with storage wiring for MinIO, Azure Blob, AWS S3, or bring-your-own S3.

Interactive development: Developers can launch VS Code, Jupyter, or SSH sessions on a remote GPU node, exec into running tasks, port-forward services, and rsync files in both directions. Version 6.3.0 added osmo workflow rsync download with a live progress bar.

Scheduling: OSMO uses the NVIDIA KAI Scheduler by default. Release 6.2.8 added NVLink topology-aware placement for multi-GPU tasks. Release 6.3.0 made exec_timeout and queue_timeout per group, so a stalled simulation group no longer kills sibling training groups.

Data: The project describes content-addressable datasets with deduplication that it claims can cut storage by 10 to 100x. Note that the standalone osmo dataset CLI and /datasets API were deprecated in 6.3.0 and are slated for removal in 6.4, with workflow-managed dataset outputs as the replacement.

Security and identity: Since 6.2.8 OSMO ships an RBAC authorization sidecar, OAuth2 proxy integration with device-code login, and identity-provider user mapping. Release 6.3.0 added TLS termination at the Envoy gateway and cloud workload identity (Azure Workload Identity, AWS IRSA/Pod Identity) so services no longer mount storage keys as Kubernetes Secrets. Release 6.3.1 tightened the default osmo-user role to the default pool.

Agent integration: The repository ships an AGENTS.md, a skills directory, and an MCP deployment guide. At GTC 2026 NVIDIA said OSMO integrates with Claude Code, OpenAI Codex, and Cursor so coding agents can submit, monitor, and debug pipelines.

Interactive Explainer: Watch OSMO Route One Workflow Across 3 Compute Tiers

Press Run workflow to see how OSMO schedules the README example task by task. Click any tier or step number to inspect what happens there.

&&

Key Takeaways

OSMO orchestrates training, simulation, and edge HIL tasks from one YAML across heterogeneous Kubernetes clusters

Apache-2.0, Helm charts on NGC, latest release 6.3.1 (June 2026), local KIND quickstart available

KAI Scheduler default, NVLink-aware placement, per-group timeouts, RBAC and OAuth2 built in

Battle-tested on GR00T, Isaac Lab, Isaac Sim, and Isaac ROS; Azure and Nebius integrations exist

Dataset CLI is deprecated in 6.3 and removed in 6.4; plan migrations accordingly

Check out the GitHub, Documentation, Releases, Cookbook and NVIDIA OSMO page. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Open-Sources OSMO: One YAML Orchestrates Physical AI Training, Simulation, and Robot Testing appeared first on MarkTechPost.