---
publish_time: 1792195752
link: https://www.marktechpost.com/2026/10/16/perplexity-open-sources-space-firecracker-microvm-sandbox-ai-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Perplexity 开源了驱动 Perplexity Computer 每一任务的沙箱平台 SPACE（Sandboxed Platform for Agentic Code Execution），以 Apache 2.0 发布于 GitHub。SPACE 为每个 Agent 任务分配一个 Firecracker 微虚拟机（独立 guest 内核），凭证与出站流量由 VM 外部的网关管控，密钥从不进入 guest，为构建编码与浏览类 Agent 的团队提供可自托管的、经生产验证的隔离层。生产中沙箱创建中位延迟由 185ms 降至 60ms；在 9 个前沿模型上，108 次 VM 逃逸尝试 0 成功。
---

# Perplexity 开源 SPACE：面向 AI 智能体的隔离沙箱

> 原文链接：https://www.marktechpost.com/2026/10/16/perplexity-open-sources-space-firecracker-microvm-sandbox-ai-agents/
> 来源：MarkTechPost

Perplexity has open-sourced SPACE, the sandbox platform behind every task in Perplexity Computer. The Perplexity SPACE sandbox gives each agent task its own Firecracker microVM. Credentials and outbound traffic are controlled from outside that VM. The code ships under Apache 2.0 on GitHub. For teams building coding or browsing agents, this is a production-tested isolation layer they can self-host.

TL;DR

Size: Rust codebase, release 0.8.0, the public baseline. HTTP API plus server-sent events.

Runs on: A Linux x86_64 host with KVM, /dev/kvm, btrfs and Docker. Local Kind (Kubernetes) or direct mode. No macOS.

Performance: In production, median create latency fell from 185 ms to 60 ms versus Perplexity&#8217;s previous provider.

Best: 0 of 108 VM-to-host escape attempts succeeded across 9 frontier models.

Worst: Before fixes, agents bypassed the egress policy in 11 of 54 partial-network runs.

What is Perplexity SPACE?

SPACE (Sandboxed Platform for Agentic Code Execution) is Perplexity&#8217;s platform for running agent code in isolated microVMs. Applications call its HTTP API to create Linux environments, run commands and stream output.

A template supplies the starting filesystem. A sandbox is one instance of that template, with its own VM and writable disk. Many commands can run inside one sandbox.

Perplexity&#8217;s launch thread explains the design goal. Agents run commands, install packages and call services with root inside the sandbox. The host stays outside the guest&#8217;s control. Agent work is long-running, stateful and branching, so it must survive restarts.

How does SPACE isolate agents?

Each sandbox is a Firecracker microVM with its own guest kernel. A per-sandbox network gateway on the host enforces egress policy on every outbound connection.

Secrets never enter the guest. Per Perplexity&#8217;s July engineering post, credentials are injected at the network layer. The credential store adds hierarchical scoping, rate limits and audit logging.

The architecture guide splits the system into 4 parts. These are a PostgreSQL-backed API, controllers, worker services and a data plane. Worker services manage VMs, networking, volumes, templates and credentials. btrfs copy-on-write creates each root filesystem.

How do pause, suspend and restore work?

Sandboxes move through 4 states: running, paused, suspended and deleted.

Paused: VM memory stays resident on the worker. This is not a durable snapshot.

Suspended: VM memory, runtime state and root filesystem are snapshotted. Active resources are released.

Idle default: sandboxes suspend after 6 hours without activity.

For fast creates, Kubernetes deployments use warm pools of booted sandboxes. Single-node setups use base snapshots instead.

In production, the 90th-percentile create latency dropped from 447 ms to 89 ms. Perplexity reports that 100% of Computer sessions run on SPACE.

Did SPACE survive a red-team test?

Perplexity&#8217;s Escaping SPACE: Part I report tested 9 models with root inside the guest. The study ran 216 runs across 2 tasks and 4 settings.

Sandbox escape: 0 of 108 runs reached the host-side secret.

No-network bypass: 0 of 54 runs succeeded.

Partial-network bypass: 11 of 54 runs succeeded before fixes. 4 models found a path.

Claude Opus 5.0, GPT-5.6 Sol, GPT-5.6 Cyber and Kimi K3 found bypasses. The attacks used DNS spoofing and shared CDN IP addresses.

Perplexity then added source-address validation through nftables. The gateway now terminates TLS and checks both SNI and HTTP host against the allowlist. In the retest, no model produced a verified bypass.

The same team tested 10 third-party platforms. 8 showed at least one network-policy bypass. Perplexity disclosed the results to every affected vendor.

How does SPACE compare with other open sandboxes?

FeaturePerplexity SPACEE2B RuntimemicrosandboxDaytonaIsolationFirecracker microVM per sandboxFirecracker microVM per sandboxlibkrun microVMDedicated kernel per sandboxLicenseApache 2.0Apache 2.0Apache 2.0Public repo, unmaintained since June 2026LanguageRustGoRustNot disclosedHost needsLinux x86_64 + KVMNot disclosedLinux with KVMNot disclosedEgress controlPer-sandbox gateway, TLS terminationnftables firewall, SNI/Host listsNot disclosedNot disclosedPerplexity egress test0 bypasses after fixHTTPS bypass, mitigation plannedHTTP + HTTPS bypass, fix in v0.6.18HTTPS bypass, mitigation releasedE2B SDK supportYes, via ECW wrapperNativeNot disclosedNot disclosed

How do developers deploy SPACE?

The installation guide deploys SPACE into a local Kind cluster. The host needs /dev/kvm, /dev/net/tun, loop devices and btrfs. Running it inside a VM requires nested virtualization.

Teams already on E2B can try the E2B Compatibility Wrapper. Its tested baseline is the Python package e2b==2.21.1. A reference AWS EKS deployment ships in the repository.

Key Takeaways

SPACE runs each agent task in its own Firecracker microVM.

Credentials and egress policy live outside the guest VM.

0 of 108 escape attempts reached the host in red-team tests.

Egress bypasses hit 11 of 54 runs before fixes, 0 after.

Apache 2.0, Rust, needs a Linux x86_64 host with KVM.

Check out the GitHub repo, the docs and the red-team report. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Perplexity Open-Sources SPACE, a Firecracker MicroVM Sandbox for AI Agents appeared first on MarkTechPost.