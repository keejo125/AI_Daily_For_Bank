---
publish_time: 1791240665
link: https://www.marktechpost.com/2026/10/05/meet-together-link-a-free-cli-that-runs-open-models-like-kimi-k3-and-glm-5-3-inside-claude-code-codex-and-opencode/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Together AI 发布 Together Link，一款免费、MIT 许可的 CLI（测试版），可将开发者已在用的编码智能体（Claude Code、Codex、OpenCode、ChatGPT Desktop、Pi 等）连接到其在 Together 平台托管的开源模型。核心理念是“保留 harness、替换模型、降低账单”：通过自动路由器，简单任务路由到 Kimi K3、GLM 5.3、DeepSeek V4.1 Flash 等低成本开源模型，难题再升级到 Opus 5.5。每条会话结束即销毁临时配置，保持 prompt cache；并提供按会话的 token 与费用清单。
---

# Together Link：在 Claude Code/Codex 中调用 Kimi K3、GLM 5.3 等开源模型的免费 CLI

> 原文链接：https://www.marktechpost.com/2026/10/05/meet-together-link-a-free-cli-that-runs-open-models-like-kimi-k3-and-glm-5-3-inside-claude-code-codex-and-opencode/
> 来源：MarkTechPost

Together AI has released Together Link, a free, MIT-licensed CLI now in beta. It connects the coding agents developers already use to open models hosted on Together AI. Supported tools include Claude Code, Claude Desktop, Codex, ChatGPT Desktop, OpenCode, and Pi. The idea is simple: keep the harness, swap the model, and shrink the bill.

Is it deployable today? Yes. It installs with one command on macOS or Linux and needs only a Together API key. It is in beta, so commands, routing, and the model list may change.

The Problem It Targets

Coding agents often send every task to the same premium model, from a one-line fix to a full rewrite. In its launch post, Together team states that engineering orgs spend tens of thousands to millions of dollars monthly on closed models. Its argument is that open models have closed much of the gap. Kimi K3 and GLM 5.3 target hard coding work. GLM 5.3 Flash and DeepSeek V4.1 Flash cover everyday tasks.

How Together Link Works

Installation is a single command:

Copy CodeCopiedUse a different Browser

curl -fsSL https://link.together.ai/install | bash

The installer adds Bun if needed and places commands in ~/.local/bin. Run togetherlink to open a launcher, or start a tool directly with togetherlink claude, togetherlink codex, togetherlink opencode, or togetherlink pi. Shortcuts such as tclaude also work.

According to the official docs, no local proxy or daemon runs. Each tool talks directly to Together&#8217;s hosted gateway. Terminal agents receive a temporary per-launch configuration that is removed when the session ends. Claude Desktop and ChatGPT Desktop use separate, reversible profiles. Commands like togetherlink chatgpt off switch back.

The Auto Router

Sessions default to a virtual auto model. Per the launch post, the router reads each session&#8217;s first task. Quick fixes go to fast, low-cost models, while hard problems get frontier capability. With an Anthropic API key, it routes between Opus 5.5 and GLM 5.3. Without one, it routes between GLM 5.3 and GLM 5.3 Flash. Routing happens once per session, so prompt caching keeps working.

The Opus path applies only to Claude Code and Claude Desktop, billed to your Anthropic account. Codex, OpenCode, Pi, and ChatGPT Desktop always stay on Together models. To pin one model, place the flag before the tool name: togetherlink --main zai-org/GLM-5.3 claude.

Inside Claude Code, the /model menu maps tiers to open models. Opus runs Kimi K3, Fable runs GLM 5.3, Sonnet runs GLM 5.3 Flash, and Haiku runs DeepSeek V4.1 Flash.

Models, Pricing, and Receipts

The docs list Kimi K3, GLM 5.3, GLM 5.3 Flash, and DeepSeek V4.1 Flash, each with 1M context. The product page lists Kimi K3 at $3.00 in and $15.00 out, and GLM 5.3 at $1.40 in and $4.40 out. DeepSeek V4.1 Flash and MiniMax M3 are listed at $0.30 in and $1.20 out. Current rates live on Together&#8217;s pricing page.

Billing runs on your existing Together key, through pay-as-you-go or credit packs. Each session prints token and dollar totals on exit. In Claude Code, the status line shows estimated spend beside the equivalent Opus cost. Running togetherlink usage --last 7d shows gateway-tracked spend across sessions.

Together team also notes it serves the largest OpenRouter token share for DeepSeek V4.1 Flash (40.8%), GLM 5.3 Flash (28.2%), and Kimi K3 (23.1%), as of 9/30/2026.

Together Link vs Closest Alternatives

FeatureTogether LinkOpenRouterClaude Code RouterOllama launchSetupOne curl install, then togetherlink claudeEnv vars in shell profileDesktop app or npm CLIollama launch claudeLocal proxyNo, hosted gatewayNo, direct connectionYes, local gateway on port 3456Local server, or direct to Ollama CloudAgentsClaude Code, Claude Desktop, Codex, ChatGPT Desktop, OpenCode 2, PiGuides for Claude Code, Codex CLI, OpenCode, Cursor, and more10 agents, including Claude Code, Codex, OpenCode, PiClaude Code, OpenCode, Claude and ChatGPT Desktop (macOS)Auto routingAuto router, optional Opus 5.5 escalationopenrouter/auto modelRule-based routing with fallbacksNot documentedCost trackingPer-session receipt plus 7-day usage reportActivity dashboard plus statusline scriptToken usage and cost estimates in logsNot documentedModelsCurated Together lineupOpenRouter catalogAny provider you configureLocal and Ollama Cloud modelsOSmacOS, LinuxWherever Claude Code runsmacOS, Windows, LinuxDesktop app connect is macOSLicenseMIT, freeHosted serviceMIT, freeFree locally, cloud needs API key

Together Link&#8217;s edge is a curated, one-command path with built-in savings receipts. Claude Code Router offers broader provider control, but runs a local gateway you manage.

Interactive Explainer

&&

Key Takeaways

One install command connects 6 existing agents to open models on Together AI.

The default Auto router picks between GLM 5.3, GLM 5.3 Flash, and optionally Opus 5.5.

Together claims over 50% savings, and 50 to 80% versus all-Opus 5.5 sessions.

No local proxy runs, and your normal agent configuration files stay untouched.

Free and MIT-licensed, but limited to macOS and Linux during beta.

Check out the Technical details and GitHub.  All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet Together Link: A Free CLI That Runs Open Models Like Kimi K3 and GLM 5.3 Inside Claude Code, Codex, and OpenCode appeared first on MarkTechPost.