---
publish_time: 1791089382
link: https://www.marktechpost.com/2026/10/03/deepseek-harness-v0-2-brings-official-desktop-apps-to-its-open-source-agent-harness/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  DeepSeek 为其开源智能体运行时 DeepSeek Harness（dsh）发布 v0.2 预览版官方桌面应用，提供 macOS（Apple 芯片）与 Windows（64 位）安装包，也可经 npx @deepseek-ai/dsh web 启动。dsh 是将模型变为智能体的运行时，负责读文件、跑命令、维护计划，v0.2 面向日常办公与编程。
  
  内置能力包括常用办公与开发工具、插件管理页、文件与 diff 预览侧栏、文档图表/幻灯片生成，以及可按频率调度的自动化任务插件；桌面版捆绑 dsh 命令，免装 Node.js/pnpm，支持 DeepSeek 账号登录或 API Key（账户模型免额外 Key 即可联网搜索）。架构延续"一切皆插件"的微内核设计，基于 Cordis 框架，团队提醒后续仍有不兼容变更。
---

# DeepSeek Harness v0.2 发布官方桌面应用

> 原文链接：https://www.marktechpost.com/2026/10/03/deepseek-harness-v0-2-brings-official-desktop-apps-to-its-open-source-agent-harness/
> 来源：MarkTechPost

DeepSeek has released an official desktop app for DeepSeek Harness (dsh), its open-source agent harness. The app ships with the v0.2 preview. Installers cover macOS (Apple silicon) and Windows (64-bit).

Is it deployable? Yes, today, as a preview. Download it from deepseek.com/harness or run npx @deepseek-ai/dsh web. DeepSeek warns that compatibility-breaking changes will follow.

What Shipped in v0.2

A harness is the runtime that turns a model into an agent. It reads files, runs commands and keeps a plan. The v0.2 preview targets everyday work as well as coding.

Built-in capabilities: commonly used tools for office work and development come preloaded.

Plugin management: a new page installs, configures, enables and disables plugins.

File and diff review: a right-hand sidebar previews generated files and code changes.

Document work: users can send documents, spreadsheets or PDFs and ask for charts or slides.

Automation Task: a plugin schedules recurring prompts, with run history and editable frequency.

The desktop build also bundles the dsh command. Users no longer need a separate Node.js or pnpm install. Users can sign in with a DeepSeek account or add an API key. Per the rc.1 notes, account models get web search without an extra key.

Architecture: Everything is a Plugin

DeepSeek first open-sourced dsh in August 2026, under MIT. It runs on Cordis as described in the research paper &#8216;A Programming Paradigm for Spatiotemporal Composability&#8216;. The model adapter, tool registry and agent loop are all plugins. Any layer can be replaced.

The harness is not locked to DeepSeek models. The provider guide covers third-party providers and custom OpenAI-compatible endpoints. The repository has passed 240,000 GitHub stars and 29,000 forks.

dsh also doubles as DeepSeek&#8217;s evaluation rig. The API changelog says Code Agent benchmarks ran on &#8216;DeepSeek Harness minimal mode.&#8217; DeepSeek-V4-Flash-0731 scored 82.7 on Terminal Bench 2.1 in that setup.

4 Session Modes

Sessions run in 1 of 4 modes, per 36Kr&#8217;s hands-on and the release notes:

Standard: general work, and now the built-in default.

Creator: describe a plugin in chat; the agent builds and installs it.

PTC: programmatic tool calling, with Node code run in a separate process.

Minimal: the lean loop DeepSeek uses for benchmark runs.

So, What Changed Now

The v0.2.1-alpha.1 build adds an experimental Claude Code Mods compatibility layer. DeepSeek frames it as a test of whether the Mods API is broadly a subset of dsh plugins. It does not promise full compatibility. The build also adds a &#8216;Let Agent create a plugin&#8217; entry, an optional Developer Tools bundle and a --public-url flag for reverse proxies. It removes runtime invariant plugins, a breaking change for some extensions.

DeepSeek Harness vs Claude Code vs OpenAI Codex

FeatureDeepSeek Harness v0.2Claude CodeOpenAI CodexDeveloperDeepSeekAnthropicOpenAILicenseMITProprietaryApache-2.0StatusDeveloper previewGenerally availableGenerally availableSurfacesDesktop app (macOS Apple silicon, Windows x64), Web UI, headless CLITerminal, IDE, GitHub (@claude)CLI, IDE extension, desktop app, Codex WebModel accessDeepSeek account or API key, plus custom OpenAI-compatible providersAnthropic Claude modelsChatGPT plan sign-in or OpenAI API keyExtension modelEverything is a plugin, including the agent loopPlugins with custom commands and agentsMCP servers, plugins, skillsQuick startnpx @deepseek-ai/dsh webcurl -fsSL https://claude.ai/install.sh | bashnpm install -g @openai/codex

Key Takeaways

DeepSeek Harness v0.2 ships official macOS (Apple silicon) and Windows x64 apps.

The MIT harness treats every layer, including the agent loop, as a plugin.

Creator mode lets the agent write and install its own plugins.

It works with non-DeepSeek models through OpenAI-compatible endpoints.

It is a developer preview; expect breaking changes between builds.

Check out the Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post DeepSeek Harness v0.2 Brings Official Desktop Apps to Its Open-Source Agent Harness appeared first on MarkTechPost.