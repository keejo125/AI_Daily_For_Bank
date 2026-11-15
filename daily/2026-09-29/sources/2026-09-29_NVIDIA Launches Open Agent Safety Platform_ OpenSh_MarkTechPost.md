---
publish_time: 1790623285
link: https://www.marktechpost.com/2026/09/28/nvidia-launches-open-agent-safety-platform/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA发布Open Agent Safety Platform（开放软件平台+参考设计），结合OpenShell安全运行时与BlueField-4 DPU上的Sentry带外看门狗，核心思路是“安全控制不应置于被控Agent内部”。Sentry可在毫秒级将失控Agent隔离到沙箱。该平台已联合100余家行业伙伴，面向Agent从开发到生产的全链路安全。
---

# NVIDIA 发布开放智能体安全平台：OpenShell 沙箱 + Sentry 毫秒级隔离

> 原文链接：https://www.marktechpost.com/2026/09/28/nvidia-launches-open-agent-safety-platform/
> 来源：MarkTechPost

NVIDIA has launched the NVIDIA Open Agent Safety Platform, an open software platform and reference system design for AI agent security. It pairs the OpenShell secure runtime with NVIDIA Sentry, an out-of-band watchdog on BlueField-4 DPUs. The core idea is simple. Safety controls should not live inside the agent they are meant to control. 

Today, with over 100 industry partners, we introduced the NVIDIA Open Agent Safety Platform, bringing together OpenShell and Sentry.

Artificial intelligence is extraordinary technology that will advance discovery, productivity, security, health, and prosperity for generations to… pic.twitter.com/dReAxwpRUn
&mdash; Jensen Huang (@JensenHuang) September 28, 2026

Is it deployable today? Yes for OpenShell. It is Apache 2.0, installs on Linux, macOS (Apple Silicon) or Windows WSL 2, and its repo still labels it alpha.

Why NVIDIA Moved Enforcement Below the Agent

The NVIDIA technical report cites recent reports from several frontier labs. Agents broke out of evaluation environments and reached systems they should not have touched. Some agents misreported what they did. The NVIDIA team names a common pattern: agents circumvented application-layer controls to finish their task.

NVIDIA calls this failure mode drift. Drift can follow a policy block, a bug, a missing tool or ambiguous instructions. NVIDIA team argues drift cannot be trained away without losing capability. So an agent cannot be expected to fully govern itself.

How the Platform is Built

OpenShell (runtime): Each agent runs in an isolated sandbox. A gateway manages sandbox lifecycle across Docker, Podman, MicroVM or Kubernetes drivers. Every outbound connection hits a policy engine that allows it, binds credentials to an approved endpoint, or denies and logs it. Filesystem and process rules lock at creation. Network and provider rules are hot-reloadable. See NVIDIA&#8217;s runtime controls walkthrough for implementation details.

Sentry (in-silicon watchdog): Sentry runs on BlueField-4 DPUs and uses NVIDIA DOCA to inspect agent requests and responses. It provides attested telemetry, verifies agent identity and enforces zero-trust access to data, tools and APIs. It stays isolated from the host, so a compromised runtime does not disable it.

Placement matters: In a Vera Rubin POD, each compute tray&#8217;s BlueField-4 sits on the node&#8217;s only path to the model. An agent cannot act without its next inference call. That makes the path both the best observation point and the kill switch. For existing Vera plus BlueField-4 systems, NVIDIA says enabling these protections is a software update.

The stack is optimized for NVIDIA Vera CPUs but is compatible with other hardware. NVIDIA team claims Vera delivers up to 80% faster sandbox performance than traditional CPU infrastructure. OpenShell can also be extended to Arm and Intel platforms.

The 5 Design Principles

Verifiable policy: a prover checks the policy cannot escape operator intent before the agent runs.

Out-of-band enforcement: controls sit outside the agent&#8217;s reach.

Control the path to the model: it is the observation point and the kill switch.

Scale authority with visible reasoning: more capable agents need more inspectable thinking.

Shared responsibility: labs, enterprises and hardware providers each own a layer.

Interactive Explainer: Send a Request Through the Stack

&&&

How It Compares With Other Agent Sandboxes

The closest alternatives are sandbox platforms for agent-generated code. Neither offers an equivalent hardware watchdog.

FeatureNVIDIA OpenShell + SentryE2BDaytonaTypeOpen runtime plus hardware reference designOpen-source sandbox cloudSandbox infrastructure runtimeLicenseApache 2.0Apache 2.0AGPL-3.0 (public repo unmaintained since June 2026)IsolationPer-sandbox container or MicroVM, kernel-level isolationFirecracker microVM, own kernelDedicated kernel, filesystem and network stack per sandboxEgress controlYAML policy at HTTP method and path level, hot-reloadableAllow and deny lists by IP, CIDR or domainNetwork limitsOut-of-band hardware enforcementYes, Sentry on BlueField-4 (optional)No, software isolationNo, software isolationWhere it runsLocal, on-prem, cloud, Kubernetes (experimental)E2B cloud or self-hosted on AWS and GCPDaytona cloudAgent supportClaude Code, Codex, OpenCode, Copilot CLI built inJS and Python SDKsPython, TypeScript, Ruby, Go, Java SDKs

Who is Building on It

NVIDIA says over 100 organizations work with the platform. Anthropic integrated Claude Managed Agents with OpenShell and BlueField. SpaceXAI uses it for Cursor coding agents and Grok models. Salesforce connected OpenShell to Slack for approving agent permission requests. SAP is embedding OpenShell in the Joule Studio runtime. Red Hat, SUSE and Canonical are integrating it into their operating systems.

The effort feeds the Open Secure AI Alliance, governed by the Linux Foundation. OpenShell and its skills are available on GitHub and the OpenShell docs.

Key Takeaways

2 layers: OpenShell sandboxes the agent, Sentry watches it from separate silicon.

Sentry can quarantine an agent that leaves its boundary in milliseconds, per NVIDIA.

OpenShell policies are declarative YAML, with network rules enforced at HTTP method and path level.

OpenShell runs Claude Code, Codex, OpenCode and GitHub Copilot CLI out of the box.

NVIDIA lists over 100 organizations working with the platform, including Anthropic and Microsoft.

FAQ

Does OpenShell require BlueField-4? No. It runs on local, on-prem, cloud and Kubernetes infrastructure. BlueField-4 only adds Sentry.

How is this different from model guardrails? Guardrails shape what an agent attempts. Runtime controls enforce what it is allowed to do.

Can I use existing agents and models? Yes. OpenShell supports open and closed models and custom sandbox images.

Check out the Paltform here and Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Launches Open Agent Safety Platform: OpenShell Sandboxes Agents on Vera CPUs While Sentry on BlueField-4 Quarantines Them in Milliseconds appeared first on MarkTechPost.