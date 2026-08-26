---
publish_time: 1787685139
link: https://www.marktechpost.com/2026/08/25/perplexity-ships-portable-computer-on-nvidia-dgx-spark-local-harness-os-enforced-sandbox-and-zero-per-token-cost-for-local-steps/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Perplexity 发布 Portable Computer，将智能体套件（harness、编排器、规划器、工具路由与后训练模型）本地化部署于 NVIDIA DGX Spark，任务先在本地设备启动、本地步骤零按 token 计费；需联网或前沿推理时再由编排器暂停征询后发往 15+ 云模型。系统以 OS 强制沙箱隔离，落地门槛为 GB10 级设备或 24GB 显存的 RTX 显卡。
---

# Perplexity 发布 Portable Computer：本地优先的智能体电脑（基于 DGX Spark）

> 原文链接：https://www.marktechpost.com/2026/08/25/perplexity-ships-portable-computer-on-nvidia-dgx-spark-local-harness-os-enforced-sandbox-and-zero-per-token-cost-for-local-steps/
> 来源：MarkTechPost

Perplexity has released Portable Computer, a local-first build of its agentic Computer platform that runs the agent harness, orchestrator, planner, tool router and post-trained models directly on NVIDIA DGX Spark. The local model, inference engine, tool sandbox and app connectors ship as one packaged system, every task begins on the device, and work handled by local models carries no per-token charge. When a step needs the live web or frontier reasoning, the orchestrator stops and asks before sending that single step to one of 15+ cloud models.

Is it deployable?

Yes, with a hard hardware gate. This is shipping software, not a preview binary, but it needs a GB10-class box or an RTX GPU with 24 GB of VRAM under the desk.

Company level: Enterprises and mid-market teams that already own NVIDIA workstations, plus well-funded AI-native startups. Not viable for general SMBs — the machine is the price of entry.

Industries: Finance, legal, healthcare, government and defense, and IP-heavy engineering — anywhere data residency or contractual confidentiality blocks cloud inference.

Applications: Fee and disclosure review across document sets, PII-bounded research, repo-scale migrations, batch summarization of local corpora, and PR triage that ends in Slack.

What actually ships on the device

Portable Computer is not a local chat app with a file picker. Perplexity packages the local model, inference engine, agent harness, tool sandbox and app connectors as one system, which removes the usual work of standing up an inference server and wiring tools by hand. Users select either Qwen 3.8 27B or PPLX 27B — Perplexity&#8217;s post-trained variant tuned for its own harness — with NVIDIA Nemotron 3.5 Lightning, an open 30B MoE model, listed as coming soon. Bring-your-own model and inference server is also supported.

Code and tool calls execute inside an OS-enforced sandbox that restricts processes, filesystem paths and network access. If the sandbox is unavailable, tool execution is disabled rather than silently downgraded. Gmail, Outlook, Slack and GitHub connectors route through the local orchestrator.

The escalation gate is the actual design decision

Local-first is not local-only. When a step needs the live web or frontier reasoning, the orchestrator stops and asks. Before any call, the harness selects the relevant context, runs a PII classifier over it, and shows the user exactly what would leave the machine. The approved step routes to one of 15+ cloud models; the remote adviser returns text guidance and never receives direct access to local files, tools or the conversation.

Perplexity also engineered around small-model context limits. Qwen 3.8 27B advertises a 260K-token window but degrades past roughly 100K, so the harness keeps the system prompt and toolset small, loads specialized skills on demand, exposes connectors as compact CLI tools instead of full MCP definitions, and compacts stale context mid-run. 

&&

Benchmarks

On its 53-task Local Knowledge Work Bench — spanning deep research, financial analysis and document creation, which Perplexity says it plans to open-source — Computer running Qwen 3.8 27B on a DGX Spark scored 82.6%, against 77.6% for the open-source Pi harness and 74.0% for Hermes on the identical model. PPLX 27B raised it to 85.4%.

On BrowseComp, Computer hit 66.7% versus 50.2% (Pi) and 43.9% (Hermes), using 51% less wall time and 70% fewer tokens than Pi. On ParseBench-100 for visual document understanding, it scored 65.1% against 34.6% and 13.9%.

The most informative result is the hybrid one. On Terminal Bench 2.1, the fully local run scored 59.6% at effectively zero marginal cost; adviser escalation lifted it to 73.0% at roughly $0.415 per rollout, compared with 82.4% at about $0.65 for Claude Opus 5 alone. Escalation narrows the gap to frontier models without closing it.

Hardware, pricing model and limits

DGX Spark installs need the GB10 superchip, 128 GB of memory and at least 1 TB of storage. The Qwen 3.8 27B orchestrator ships at 3-bit quantization, a 17.4 GB download, requiring 32 GB RAM; Nemotron 3.5 Lightning is 4-bit, 19 GB, requiring 36 GB. Other systems need DGX OS or Ubuntu on ARM or x64 with an RTX GPU carrying 24 GB or more of VRAM. Installation is a standard apt repository add.

Availability is Linux-first for Pro, Max, Enterprise Pro and Enterprise Max subscribers; Windows follows in September, and macOS is not on the roadmap. Only one DGX Spark is supported at launch — clustering is roadmap, not shipped. Work handled by local models carries no per-token charge, which is what makes repo-scale migrations and long verification loops economically sane on owned hardware.

Key Takeaways

Portable Computer runs the full agent harness, orchestrator and sandbox locally on DGX Spark — not just a local LLM.

Every step starts on-device; escalation to 15+ cloud models requires explicit per-step approval after a PII check.

Perplexity&#8217;s own tests: 85.4% with PPLX 27B on its 53-task bench, versus 77.6% for Pi on the same model.

Terminal Bench 2.1: 59.6% local, 73.0% with adviser at ~$0.415/rollout, against 82.4% at ~$0.65 for Opus 5 alone.

Check out the Perplexity Portable Computer and NVIDIA local AI blog.

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Perplexity Ships Portable Computer on NVIDIA DGX Spark: Local Harness, OS-Enforced Sandbox, and Zero Per-Token Cost for Local Steps appeared first on MarkTechPost.