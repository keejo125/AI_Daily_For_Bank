---
publish_time: 1789445000
link: https://www.marktechpost.com/2026/09/14/agent-net-open-sources-webagent-a-go-harness-that-turns-any-website-into-a-guarded-ai-agent/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  构建 Agent 间交易市场的 Agent-net 开源 Webagent，一个把任意网站变成受控公开业务智能体的 Go Harness。企业只需填写声明式 JSON 规格、为 9 个可插拔槽位各选一个提供方即可运行，无需写编排代码。当前以 Apache 2.0 发布，已可运行 Slack、WhatsApp、HTTP 智能体（基于 MCP 工具），但仍是 v0：浏览器动作提供方、OAuth 网关 MCP、OTel 导出及身份计费层尚未完成。
---

# Agent-net 开源 Webagent：用 Go Harness 把任意网站变成受控 AI 智能体

> 原文链接：https://www.marktechpost.com/2026/09/14/agent-net-open-sources-webagent-a-go-harness-that-turns-any-website-into-a-guarded-ai-agent/
> 来源：MarkTechPost

Agent-net, the team building an agent-to-agent marketplace where AI agents discover, trust, and pay each other, has released Webagent, an open source harness for standing up public-facing business agents. So, basically you give it your website, get an agent, and let it talk to other agents. Instead of writing orchestration code, a business fills in a declarative JSON spec, picks 1 provider for each of 9 pluggable slots, and runs webagent serve.

Is it deployable? Yes, with caveats. The repo ships under Apache 2.0, builds green, and runs live Slack, WhatsApp, and HTTP agents backed by MCP tools today. It is still labeled v0, and the browser action provider, OAuth-gated MCP, OTel export, and the AgentNet identity and billing layer are listed as not yet built.

Slots, providers, picks

Webagent is written in Go. An agent is 1 Brain (an LLM plus instruction) over a set of slots defined in core/. Each slot is a Service Provider Interface with a registry of providers in spi/ and a designated default:

SlotBuilt-in providersDefaultRetrievallive, keyword, hybridliveMemorysessionsessionGuardrailbasic, offbasicChannela2a, web, slack, whatsapp (telegram stub)a2aSecretsenv, file, staticenvPresentertext, terminal (QR), webtextModelecho, openrouter, gatewayechoActionnone, demo, mcpnoneObservabilitynone, log, memorynone

The design serves 3 audiences on 1 contract: businesses that configure by picking from the menu, businesses that extend by registering a custom provider, and partner companies that ship adapters. Nobody forks the core. Every provider must pass its slot&#8217;s conformance suite to be certified.

Safety is code-enforced, not prompt-enforced

The most important architectural decision is action.Guard. Every tool the agent holds, whether it comes from the action provider or is injected by the host, is wrapped so the chosen guardrail runs on the action before it executes. The model cannot bypass it. The DESIGN.md frames the whole project around a research finding that architecture, not model capability, decides agent success, citing arXiv 2511.19477 and an 85% versus 50% task-success gap on the same models.

What runs today

The default echo brain needs no credentials, so webagent validate and webagent serve work out of the box on the 2 example specs, zomato.json and bakery.json. To drive a real model, webagent keys set openrouter stores a key in the OS config directory with mode 0600. Keys are never written into a spec, and an exported environment variable always wins. Both openrouter and gateway are OpenAI-compatible clients with a tool-calling loop.

A business with an existing MCP server becomes an acting agent with 1 spec block. The mcp action provider connects over Streamable HTTP (JSON and SSE) with bearer or API-key auth, performs the handshake at build time, and hands each tool to the agent behind the guard, so validate reports the real tool count.

The Slack and WhatsApp channel adapters verify every inbound webhook signature, acknowledge immediately, reply through the platform API, ignore their own messages, and de-duplicate retried deliveries. Slack points at /slack/events; Meta&#8217;s callback goes to /whatsapp/webhook.

Secrets follow a naming rule: any config key ending in Secret is a reference resolved through the selected vault at build time, so specs are safe to commit. A reference that cannot be resolved fails the build rather than starting a channel without a credential. Observability emits a per-turn TurnTrace aligned to the OpenTelemetry GenAI conventions, and an eval/ harness runs scenarios with checks.

&
 -->

Key Takeaways

1 JSON spec, 9 slots, 1 provider each; webagent serve does the rest

Every tool call passes through action.Guard before execution

Live today: OpenRouter or gateway brains, MCP tools, Slack, WhatsApp, HTTP channels

Not yet: browser actions, OAuth MCP, OTel export, AgentNet billing

Apache 2.0, Go, v0; read the deferred-hardening list before production

Check out the GitHub repo and the launch post. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Agent-net Open Sources Webagent: A Go Harness That Turns Any Website into a Guarded AI Agent appeared first on MarkTechPost.