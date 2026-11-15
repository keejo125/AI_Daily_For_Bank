---
publish_time: 1789075318
link: https://www.marktechpost.com/2026/09/10/openai-launches-the-agents-api-in-public-beta-putting-the-codex-harness-behind-one-api-call/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  OpenAI 公开测试 Agents API：将驱动 Codex 的同款 harness 与基础设施封装为单次 API 调用，开发者无需自建即可运行长时智能体。OpenAI 托管并维护 harness，计算可在 OpenAI 沙箱、自有设施或合作沙箱中运行。官方围绕 Agent（模型/指令/工具/MCP）、Environment（沙箱）、Session（持久实例）、Events and items（事件与条目）四大概念组织，强调上下文管理、工具高效调用与子智能体协同，支撑可靠运行数天。
---

# OpenAI 公开测试 Agents API：将 Codex Harness 封装为单次 API 调用

> 原文链接：https://www.marktechpost.com/2026/09/10/openai-launches-the-agents-api-in-public-beta-putting-the-codex-harness-behind-one-api-call/
> 来源：MarkTechPost

OpenAI has released the Agents API in public beta. It gives developers the same harness and infrastructure that run Codex. OpenAI hosts and maintains the harness. Developers run the agent&#8217;s compute in an OpenAI-managed sandbox, their own infrastructure, or a partner sandbox. 

Is it deployable? Yes. It is live for all developers in public beta. Data stays US-only, and Zero Data Retention is unsupported.

What OpenAI Shipped

The Agents API is a managed service built on the open-source Codex harness. OpenAI team states scaling Codex and ChatGPT for Work showed what long-running agents need. They need a harness that manages context, uses tools efficiently, and coordinates subagents. They also need infrastructure that keeps them running reliably for days.

The official docs organize the API around 4 concepts:

Agent: the model, instructions, tools, and MCP servers available to it.

Environment: an optional sandbox where the agent accesses files, loads skills, and runs commands.

Session: a durable agent instance that works on tasks and responds to input.

Events and items: the inputs sent to the agent and the output it produces.

A session runs in 4 steps. You create it and give it a task. Then you follow progress through streaming or webhooks. Finally, you continue with a new task or steer the current turn.

One API Call

OpenAI&#8217;s announcement shows an incident-investigation agent created in a single call:

Copy CodeCopiedUse a different Browser

import OpenAI from "openai";

const client = new OpenAI();

const session = await client.beta.agents.sessions.create({
  agent: {
    model: "gpt-6-astra",
    tools: [
      {
        type: "mcp",
        server_label: "observability",
        transport: {
          type: "http",
          server_url: "https://observability.example.com/mcp",
        },
      },
    ],
    multi_agent: { enabled: true, max_concurrent_subagents: 3 },
  },
  vault_ids: ["vault_YOUR_VAULT_ID"],
  environment: {
    type: "openai_hosted",
    capability_directories: ["/workspace/capabilities/skills"],
  },
  input:
    "Investigate service-api's elevated 5xx rate over the last 30 minutes. " +
    "Delegate deployment, error, and dependency analysis to subagents. " +
    "Save findings, evidence, and recommended mitigation in /workspace/outputs.",
});

The quickstart covers API key permissions and SDK setup.

Where the Agent Runs

Environment choice is the main architectural decision. The Agents API supports 3 sandbox options, and it can also run without a sandbox.

OpenAI-hosted sandbox: uses the sandboxing infrastructure behind Codex and ChatGPT. You can configure it with files, packages, skills, and plugins.

Self-hosted: you run codex exec-server inside your environment. It registers with a restricted key and connects over WebSocket. All connections are outbound.

Partner sandboxes: Blaxel, Cloudflare, Daytona, DigitalOcean, E2B, Modal, Oracle, Runloop, and Vercel have first-class integrations.

&&

What the Harness Handles

OpenAI maintains the harness alongside its models, with versioned access at each model launch.

Long sessions: The API automatically compacts earlier context as a session nears its limit. Developers do not write their own compaction logic.

Efficient tool use: Tool search loads tool definitions only when needed. This reduces token usage and cost while preserving the model&#8217;s cache. Programmatic tool calling lets agents run calls in parallel and chain operations. Agents filter or combine results in code, so only relevant data returns into context. Supported tools include MCP, custom functions, and built-in tools like web search.

Subagents: With multi-agent support, the main agent splits complex tasks into independent pieces. Each subagent keeps its own context. The main agent coordinates them and combines the results.

Agents API vs Agents SDK vs Responses API

OpenAI&#8217;s runtime comparison positions the 3 options this way:

Agents APIAgents SDKResponses APIWhere the agent runsOpenAI runs a managed Codex harnessInside your applicationYour application, with optional hosted orchestrationIntegration effortLowMediumHighState between tasksSaved session configuration, turns, and itemsYour storage and SDK sessionsManual history, response chaining, or ConversationsExecution environmentOpenAI-hosted, self-hosted, or no sandboxYour runtime and sandbox providersYour own environment

Early Customer Results

OpenAI published these customer-reported numbers. They are vendor-supplied, not independent benchmarks.

Ciridae: evaluation score rose from 0.71 to 0.85, with a 4x latency reduction on subagent flows.

SafetyKit: 60% lower cost per case after migrating its case review workflow.

Hypha: 86% fewer failed agent responses after separating the harness from the sandbox.

Nash.ai: runs thousands of long-running agents across global logistics networks.

Key Takeaways

OpenAI&#8217;s Agents API exposes the managed Codex harness as a public beta API.

Agents run in OpenAI-hosted, self-hosted, or 9 partner sandboxes.

Compaction, tool search, programmatic tool calling, and subagents come built in.

There is no extra fee; you pay for tokens, tools, and container time.

US-only data residency and no ZDR limit regulated workloads for now.

Check out the Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post OpenAI Launches the Agents API in Public Beta, Putting the Codex Harness Behind One API Call appeared first on MarkTechPost.