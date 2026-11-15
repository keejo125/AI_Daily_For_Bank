---
publish_time: 1792735510
link: https://www.marktechpost.com/2026/10/22/google-cloud-agent-compute-engine-microvm-ai-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google Cloud 发布面向 AI 智能体的计算服务 Agent Compute Engine，为每个 Agent 会话提供硬件隔离的微虚拟机（microVM），沙箱零凭证，已支撑 Gemini 作为工作 Agent。该服务于 AGNTCon+MCPCon 亮相，客户预览将在未来数月开放，开源版 Agent Substrate 可跑在任何 K8s 集群。
---

# Google Cloud发布Agent Compute Engine：每智能体独立微虚拟机

> 原文链接：https://www.marktechpost.com/2026/10/22/google-cloud-agent-compute-engine-microvm-ai-agents/
> 来源：MarkTechPost

Google Cloud has announced Agent Compute Engine, a compute service built specifically for AI agents. Google Agent Compute Engine gives each agent its own hardware-isolated microVM. The sandbox holds zero credentials. The service already powers Gemini as an agent for work tasks. Google unveiled it this week at AGNTCon + MCPCon. Customer preview is targeted for the coming months. The pitch: VM-grade isolation with container-like speed and density.

TL;DR

Unit: One hardware-isolated microVM per agent session, with its own guest kernel, root access and Hyperdisk.

Runs on: Google-managed hosts using Titan silicon and the Titanium IPU. Open-source sibling Agent Substrate runs on any Kubernetes cluster.

Performance: Idle agents are checkpointed to zero active resources and resumed from snapshots. Google gives no ACE boot or density numbers.

Best: Agent Substrate hit 500 activations/s at under 500 ms suspend/resume across 200,000 agents.

Worst: No published boot time, density, pricing or preview date for Agent Compute Engine itself.

What is Google Agent Compute Engine?

Agent Compute Engine is a Google Cloud service that runs each AI agent inside a dedicated microVM. Per the technical post, it powers Gemini, Antigravity, and internal evaluation and RL pipelines.

Google splits every agent into 2 parts. The harness, or &#8216;brain,&#8217; calls the model. The sandbox, or &#8216;hands,&#8217; runs code, shell commands and browsers. The harness runs fully outside the sandbox and dispatches explicit commands into it.

How does the microVM isolation work?

Each session runs in a single-tenant microVM behind a Cloud Hypervisor boundary. Hosts are stateless appliances with a read-only root filesystem enforced by dm-verity. Titanium holds attestation keys outside the guest.

The networking design is the unusual part:

MicroVMs have no standard network interface, no default gateway and no direct VPC access.

All traffic crosses a virtio-vsock boundary to a local proxy, then to an external gateway.

Guests get only a session-scoped SPIFFE certificate and a short-lived identity token.

Agent Gateway swaps in the real backend credential in flight, after policy checks.

Google assumes an attacker controls everything inside the sandbox. A prompt-injected agent finds no secrets to steal.

What are the Four Agent Identities?

Google defines 4 identities for every agent workload:

User identity: authenticates the overall task only.

Delegated on-behalf-of identity: a scoped grant stored in a central authorization service, never on the node.

Agent Workload Identity: a short-lived SPIFFE identity, the only one used for sandbox traffic.

Agent Workforce Identity: an agent&#8217;s own account and resources.

The workload identity is useless for direct API calls if exfiltrated. It only identifies which sandbox sent a packet.

How does it keep idle agents cheap?

Google team found agents spend most of their time waiting on models or users. So the sandbox signals when a tool call finishes. The host checkpoints the idle microVM to zero active resources. It resumes on the next call.

Density comes from copy-on-write memory sharing. Pre-warmed snapshot images are mapped with DAX, so microVMs on a host share base OS and library pages. Only each agent&#8217;s modified pages consume private memory. Harnesses also get cloning, snapshot/forking, rewind and rollback.

Storage is split 3 ways: disposable scratch overlays, shared read-only volumes, and persistent user workspaces on Hyperdisk.

What does Agent Substrate add?

Agent Substrate is the open-source, Kubernetes-native counterpart, available on GKE since September 15, 2026. It offers Cloud Hypervisor microVMs or gVisor sandboxes. Google reports these figures:

Up to 10x higher compute density than traditional compute.

500 activations per second at under 500 ms suspend/resume, in a 200,000-agent benchmark.

Over 1,000 dormant agents per host.

It works with harnesses including Claude Code, OpenClaw and Hermes. It is open to all GKE customers for non-production use. Production GA is allowlist-only. Source code is at https://github.com/agent-substrate/substrate.

How does it compare with other agent sandboxes?

FeatureGoogle Agent Compute EngineGoogle Agent SubstrateAWS AgentCore RuntimeAzure dynamic sessionsE2BIsolationCloud Hypervisor microVM (source)Cloud Hypervisor microVM or gVisor (source)Dedicated microVM per session (source)Hyper-V sandbox per session (source)Firecracker microVM (source)Idle handlingCheckpoint to zero active resourcesSnapshot, free CPU and RAMCPU billing typically skips I/O waitDestroyed after cooldownPause saves filesystem and memory (source)PersistenceHyperdisk per microVMFilestore agent volumes (optional)Filesystem persists across stop/resumeEphemeral sessionsSnapshot on pauseMax sessionNot disclosedNot disclosed8 hours (microVMs), 14 days (Instances)Configurable cooldownNot comparedCredentials in sandboxNone (gateway token swap)Injected by egress proxyManaged by AgentCore IdentityNot disclosedNot disclosedPublished resume/start figureNot disclosedUnder 500 ms resumeNot disclosedMillisecond allocation from prewarmed poolsAbout 1 s resumeOpen sourceNoYesNoNoNot comparedAvailabilityPreview in coming monthsGKE non-production; GA via allowlistAvailable38 listed regionsAvailable

How is Google expanding agent governance?

Google is extending Gemini for business agent governance to Agent Runtime, Cloud Run, Agent Sandboxes, GKE and ACE. The stack includes Agent Gateway, Agent Registry, Agent Identity and OpenTelemetry-based observability.

New pieces arrive in stages:

Preview soon: Envoy-based enforcement points for multicloud and hybrid setups.

Preview soon: governance for local coding agents like Claude Code and Antigravity CLI on managed devices.

Preview this quarter: token management, model routing, Service Extensions bindings and Express Link for Cloud Run.

Preview this quarter: delegated authorization with Ping Identity, SailPoint and Saviynt.

Key Takeaways

1 hardware-isolated microVM per agent, with zero credentials inside.

Idle agents checkpoint to zero active resources, then resume from snapshots.

4 separate identities; only a short-lived SPIFFE ID touches the sandbox.

Agent Substrate: 500 activations/s, under 500 ms resume, 200,000 agents.

No public pricing, boot time or preview date for Agent Compute Engine yet.

Check out the launch post, the technical deep dive, and the Agent Substrate announcement. Register interest for the preview here.. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google Cloud Launches Agent Compute Engine: A MicroVM per AI Agent appeared first on MarkTechPost.