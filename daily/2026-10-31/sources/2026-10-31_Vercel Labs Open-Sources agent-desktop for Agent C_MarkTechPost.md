---
publish_time: 1793441428
link: https://www.marktechpost.com/2026/10/31/vercel-labs-agent-desktop-computer-use/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Vercel Labs 开源 agent-desktop（Apache-2.0，Rust CLI + C 库），让 AI Agent 通过操作系统无障碍树（而非截图）驱动原生桌面应用，任意具备 shell 能力的编程 Agent 无需视觉模型即可操作 GUI。每个命令输出一个 JSON 快照，含可操作元素的引用，支持 macOS/Windows/Linux。官方称在密集 Electron 应用上通过骨架遍历可节省 78%–96% token。1.0.2 版于 2026-10-30 发布。
---

# Vercel 开源 agent-desktop：让智能体借无障碍树操作桌面应用

> 原文链接：https://www.marktechpost.com/2026/10/31/vercel-labs-agent-desktop-computer-use/
> 来源：MarkTechPost

Vercel Labs has released agent-desktop, an open-source CLI for AI agent computer use on macOS, Windows and Linux. agent-desktop reads each app through the operating system&#8217;s accessibility tree, not through screenshots. An agent gets a JSON snapshot with a ref for every element it can act on. Version 1.0.2 shipped on October 30, 2026, under Apache-2.0. For developers, any shell-capable coding agent can now drive native apps without a vision model.

TL;DR

Library: Rust CLI and a C library. 60 command names, 56 operational. 

Runs on: macOS 13+, Windows 10 1809+ or Server 2019+, Ubuntu 24.04+, on x64 and ARM64. Plain CPU, no GPU.

Performance: Deterministic, retry-safe ref actions. No independent computer-use benchmark yet.

Best: 78% to 96% fewer tokens on dense Electron apps via skeleton traversal (self-reported).

What is agent-desktop?

agent-desktop is a Rust CLI and C library from Vercel Labs for reading and operating desktop apps. It is a tool that agents call, not an agent. It embeds no LLM and has no GUI. Every command prints one JSON envelope and exits. The observe, act and verify loop stays in your agent.

How does agent-desktop work?

Each command flows through a fixed chain. The CLI or C library calls agent-desktop-core, which reaches the OS only through a PlatformAdapter trait. One platform crate then talks to the native accessibility API:

macOS: AX API

Windows: UI Automation

Linux: AT-SPI

Core never imports a platform crate. Each binary is compiled to drive exactly one OS.

Snapshots and refs

A snapshot assigns qualified refs such as @s8f3k2p9:e8. The snapshot ID inside the ref makes it self-describing. A bare @e8 is rejected with INVALID_ARGS. When the UI changes, an action returns STALE_REF or AMBIGUOUS_TARGET. The agent then takes a fresh snapshot.

Every error carries a disposition. Agents should retry only when it says safe. Ref resolution is strict and fails closed rather than guessing.

Skeleton and drill-down

Dense apps can expose thousands of accessibility nodes. A --skeleton snapshot reads only 3 levels deep. Cut containers report a children_count and get a drill ref. snapshot --root then reads one region into the same snapshot.

The builder reported a 78% to 96% token cut versus full-tree dumps in Slack, VS Code and Notion. In Apple Maps, he reported 3,811 tokens per look falling to 273. A simulated 52-step task dropped from 198k to 31k tokens. These are self-reported figures, not an independent benchmark.

Headless by default

Ref actions go through the accessibility API without moving the pointer or taking focus. That is what lets agents work while you keep using the machine. The global --headed flag allows physical input when needed. Every ref action also auto-waits up to 5,000 ms for a visible, enabled, stable target.

How does it compare with pixel-based computer use?

Model-side computer use tools work from screenshots and pixel coordinates. Anthropic&#8217;s docs say each screenshot costs roughly 1,000 to 1,800 input tokens. Its toolset definition adds about 4,500 input tokens per request. OpenAI&#8217;s tool similarly returns click, type and scroll actions your code executes.

agent-desktop is model-agnostic and returns structure, not images. Microsoft&#8217;s UFO² also uses UI Automation, but ships as a full Windows agent.

Featureagent-desktop (Vercel Labs)Claude computer useOpenAI computer useMicrosoft UFO²TypeCLI + C library toolAPI client toolsetAPI toolFull agent frameworkHow it sees the UIOS accessibility treeScreenshotsScreenshots or code (PyAutoGUI, Playwright)UIA + visual hybridModel bundledNone, any agentClaude modelsOpenAI modelsConfigurable LLMPlatformsmacOS, Windows, LinuxAny env you host (reference: Linux Docker)Browser or desktop you hostWindows (UFO²)Moves your cursorNo, headless by defaultYes, pixel clicksYes, pixel clicksGUI + API actionsToken cost per look273 (Apple Maps skeleton, self-reported)~1,000 to 1,800 per screenshotNot disclosedNot disclosedLicenseApache-2.0Proprietary APIProprietary APIMITPriceFreeStandard token pricingStandard token pricingFree (plus LLM costs)

How do you install and use agent-desktop?

Install with npm install -g agent-desktop. Bun, Yarn and pnpm work too. The package bundles native binaries for x64 and ARM64.

macOS: grant Accessibility permission with agent-desktop permissions --guide.

Windows: no grant needed for apps at your terminal&#8217;s integrity level.

Linux: needs a graphical session with at-spi2-core.

Agents learn the tool from bundled docs via agent-desktop skills get desktop. A skill is also listed on skills.sh. The C library lets Python, Swift, Go, Ruby and Node hosts call it in process. For Electron web contents, launch --cdp opens a DevTools port for agent-browser.

Key Takeaways

agent-desktop gives any agent computer use through OS accessibility trees.

It runs on macOS, Windows and Linux, x64 and ARM64, under Apache-2.0.

Headless ref actions never move your pointer or steal focus.

Skeleton snapshots cut tokens 78% to 96% (self-reported).

Apps without an accessibility tree remain out of reach.

Check out the GitHub repo, docs and npm package. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Vercel Labs Open-Sources agent-desktop for Agent Computer Use appeared first on MarkTechPost.