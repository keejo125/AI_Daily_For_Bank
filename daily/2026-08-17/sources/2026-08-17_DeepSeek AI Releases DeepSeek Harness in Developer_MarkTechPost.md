---
publish_time: 1786957592
link: https://www.marktechpost.com/2026/08/17/deepseek-ai-releases-deepseek-harness-in-developer-preview/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  DeepSeek以MIT许可发布DeepSeek Harness v0.1开发者预览版（dsh），定位「Agent=模型+Harness」。与传统把agent loop/工具注册/session写死不同，dsh以Cordis插件边界将模型、工具、技能、会话、沙箱、存储、调度、UI全部开放为可配置、可替换、可扩展的组件，是一套组装Agent运行时的工具包而非固定编码助手。可本地自托管，适合受监管企业试点。（同主题合并主条）
---
# DeepSeek 发布 DeepSeek Harness：一个万物皆插件的 MIT 许可智能体框架（开发者预览）

> 原文链接：https://www.marktechpost.com/2026/08/17/deepseek-ai-releases-deepseek-harness-in-developer-preview/
> 来源：MarkTechPost

DeepSeek released DeepSeek Harness v0.1 in developer preview and published the full source code under the MIT license. The project ships as dsh at deepseek-ai/deepseek-harness. A harness is the layer between a model and the environment it acts in — the tools, files, sandboxes, and control loop that let an agent keep working. DeepSeek frames it as Agent = Model + Harness. Most harnesses hard-code that layer: the agent loop, the tool registry, and the session store are fixed, and extension happens only at whatever hooks the authors exposed. Harness takes the opposite position, stated in the first lines of its README: everything is a plugin. Models, tools, skills, sessions, sandboxes, storage, loops, scheduling, and the UI all sit behind Cordis plugin boundaries, and any of them can be selected, swapped, or extended in configuration without changing Harness source code. That makes this a kit for assembling agent runtimes rather than a fixed coding assistant, and it is why the release matters more than the model announcement it shipped alongside.

Is it deployable?

Yes, but as developer infrastructure, not as a production agent product. v0.1 is a developer preview.

Company level: AI-native startups and platform or developer-experience teams inside mid-to-large enterprises that already run internal tooling. Regulated enterprises can pilot it locally because it is MIT-licensed and self-hosted.

Industries: Software and devtools, financial services and insurance (auditable agent runs), healthcare and pharma R&D, cloud and semiconductor vendors publishing reference agent stacks, and academic or industrial research labs benchmarking models.

Applications: Internal coding agents over private repositories, model evaluation inside a controlled two-tool environment, agent observability and run replay, custom sandbox and approval policies, and packaging house tooling as reusable plugins.

The Cordis kernel

Harness runs on Cordis, a meta-framework whose design is set out in A Programming Paradigm for Spatiotemporal Composability. The kernel handles plugin mounting, unmounting, and dependencies. Capabilities live in the plugins, not in a privileged core.

Plugins cover models, tools, skills, sessions, sandboxes, storage, loops, scheduling, and the UI. Cordis services and events let them work together. Developers select, swap, or extend any capability in configuration, without changing Harness source code.

Four runtime modes

Standard is the full coding agent: file editing, shell, file and web search, skills, planning, goals, subagents, and workflows. Code mode exposes those tools through a Code Mode SDK, so the model can combine multi-step operations in one TypeScript program. Minimal keeps two tools, a persistent bash and str_replace_editor, for benchmarking models in a bare environment. Creator mode adds runtime inspection, in-memory plugin experiments, and preset-authoring guidance.

Every run is traceable

Everything the model sees is written to an append-only session log. That includes system prompts, reasoning, tool calls and results, subagent scheduling, and every context injection. The Trajectory view inspects those records by source. Resume, fork, search, and replay all operate on the same event stream. Most agent frameworks log tool calls; recording every context injection is the sharper claim here.

Model routing is also a plugin

In Settings → Models, a DeepSeek API key takes effect on the next request without restarting the server. The installed catalog adds providers such as Anthropic and OpenAI by API key. Bedrock, Vertex, Azure, and Codex need native credentials instead: AWS credentials and a region, an ADC project, an api-version, and OAuth respectively. Custom providers accept any OpenAI-compatible base URL and protocol. Keys are write-only and stored in $DSH_HOME/.credentials.yaml; settings retain only a credential reference.

Running it

npx @deepseek-ai/dsh web starts the Web UI, served at http://127.0.0.1:3080 by default. From a checkout: git clone, pnpm install, pnpm run build, then pnpm dsh web. A Python SDK ships as deepseek-harness-sdk and needs Python 3.10 or newer, on Linux x64, Linux arm64, or macOS 14+ on arm64. Its bundled runtime requires no system Node.js.

Key Takeaways

MIT-licensed, ships as dsh, and is a developer preview.

The Cordis kernel makes models, tools, skills, sessions, sandboxes, storage, loops, scheduling, and UI swappable plugins.

Four modes — Standard, Code, Minimal, Creator — each load a different default plugin set.

An append-only session log captures every context injection; resume, fork, search, and replay share one event stream.

Provider-agnostic by design: DeepSeek, Anthropic, OpenAI, Bedrock, Vertex, Azure, Codex, and OpenAI-compatible endpoints.

Check out the DeepSeek Harness product page, GitHub repository, Developer docs, DeepSeek announcement on X and Cordis. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post DeepSeek AI Releases DeepSeek Harness in Developer Preview: An MIT-Licensed Agent Harness Where Everything is a Plugin appeared first on MarkTechPost.