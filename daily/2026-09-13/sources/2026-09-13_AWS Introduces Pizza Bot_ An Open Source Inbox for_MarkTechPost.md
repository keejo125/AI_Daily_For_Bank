---
publish_time: 1789287051
link: https://www.marktechpost.com/2026/09/13/aws-introduces-pizza-bot-an-open-source-inbox-for-background-ai-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  AWS 开源异步 AI Agent 工作台 Pizza Bot，面向在用户离开时持续运行的后台 Agent 任务。它将已完成结果与待决事项归入邮件式收件箱（All/Unread/Action 三视图），支持手动、cron 与 webhook 触发，断线后仅补跑一次错过的 cron 而非全部重放。底层基于 DeepAgents + LangGraph 做有状态执行，Hono API 服务运行时，Electron/浏览器/终端客户端共用 React 界面，LangGraph checkpoint 保留线程状态与审批暂停。已在 Amazon 内部服务超 2000 人，现以 Apache 2.0 开源，提供 macOS/Windows/Linux 桌面端与本地/独立后端部署。
---

# AWS 开源后台 AI Agent 收件箱 Pizza Bot

> 原文链接：https://www.marktechpost.com/2026/09/13/aws-introduces-pizza-bot-an-open-source-inbox-for-background-ai-agents/
> 来源：MarkTechPost

AWS introduced Pizza Bot, as a self-hosted application for AI tasks that continue while users work elsewhere. It organizes completed results and pending decisions into an email-style inbox. Earlier versions served more than 2,000 people inside Amazon, supporting meeting preparation, email drafting, Slack summaries, CRM logging, and research. The public application was rebuilt as an open source project.

Deployable: Yes. Pizza Bot offers macOS, Windows, and Linux desktop builds, and browser and terminal clients connected to a local or standalone backend. Its code is licensed under Apache 2.0.

An Inbox for Asynchronous Work

Pizza Bot separates tasks into All, the thread history; Unread, completed work awaiting review; and Action, work paused for approval or an answer. Users can organize threads into folders and inspect delegated workers in the Activity panel. Tasks can start manually, through cron schedules, or through webhooks. 

The server owns scheduling. After downtime, missed cron intervals produce 1 catch-up run instead of replaying every missed interval. Trigger occurrences are recorded durably.

How the Runtime Works

The application uses DeepAgents and LangGraph for stateful execution. A Hono API server owns runtime execution and storage. Electron and browser clients share a React interface, while all clients communicate with the server over HTTP and server-sent events. LangGraph checkpoints retain thread state and approval pauses; separate SQLite stores hold cross-thread memory and application metadata. Reconnecting clients can replay buffered events. 

Closing a thread or disconnecting a client does not stop a running server. However, quitting the desktop app stops its embedded server and ends active runs. Checkpoints preserve the thread, but the step in flight can be lost. An always-on backend is required for work to continue after that desktop app exits. 

Skills, Tools, and Approval Controls

Pizza Bot supports Amazon Bedrock, Anthropic, Google Gemini, OpenAI, OpenRouter, and Ollama. Configure a provider under Settings > Providers before running tasks. 

The agent has scratch-file operations and a sandboxed JavaScript interpreter without network or host-filesystem access. It can delegate through task when ready skill workers exist. The filesystem layer separately supports explicit folder grants and persistent memory. 

MCP servers expose external tools. Each SKILL.md defines a worker&#8217;s instructions and scoped tool access. A skill becomes callable only when its declared dependencies are available. Existing Claude Code-compatible .mcp.json configurations are supported, and plugins package skills with MCP servers.

Skill authors configure interruptOn and allowedDecisions to require approval for specific tools. Depending on that policy, users can approve, edit proposed arguments, or reject an action. These controls must be configured for the relevant tools. 

Interactive Explainer

Run the illustrative custom-skill workflow below. Compare an always-on backend with an embedded desktop server, close the client during execution, and approve, edit, or reject the proposed action. Animation timing is illustrative; no external actions occur.

    PIZZA BOT / BACKGROUND WORKIllustrative custom skill

      Backend locationAlways-on serverEmbedded in desktop
      Run example
      Close desktop

    Client: OpenServer: RunningCheckpoint: None

      WorkerApprovalResult

    Start a research brief, then close the desktop while it runs.

          All 0
          Unread 0
          Action 0

        Prepare a research brief
        The custom skill gates its publish tool with interruptOn.

          publish_brief({title: "Research brief"})
          Proposed title
          ApproveEditReject

        Read result

      Desktop closedOpen the desktop to review its inbox.

    Simulation only. No external calls.Approval specification

  &&&&&&&

Key Takeaways

An inbox for background agents: Pizza Bot organizes task history in All, completed work in Unread, and requests for approval or input in Action. Tasks support manual, cron, and webhook triggers.

Persistent execution with DeepAgents and LangGraph: Checkpoints preserve thread state and approval pauses. Tasks continue after client disconnection while the backend remains running.

Multiple model providers: Pizza Bot supports Amazon Bedrock, Anthropic, Google Gemini, OpenAI, OpenRouter, and local models through Ollama. Configured providers and tools can receive task data.

Scoped skills and configurable approvals: MCP servers expose tools, while SKILL.md files define specialist workers. Tool-specific policies let users approve, edit, or reject proposed actions.

Self-hosted and deployable: Apache 2.0 code, desktop builds, and standalone backend options are available. Each SQLite data directory supports 1 backend process. 

Check out the Technical details and GitHub Repo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post AWS Introduces Pizza Bot: An Open Source Inbox for Background AI Agents appeared first on MarkTechPost.