---
publish_time: 1789724695
link: https://www.marktechpost.com/2026/09/18/best-open-source-agent-harnesses-for-local-llms-in-2026/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  文章提出“智能体=模型+harness”的框架：harness 负责跑工具、持有状态、管理权限、把上下文回灌给模型；在本地模型下，harness 的重要性被放大——小上下文窗口与较弱的工具调用会暴露所有设计缺陷。指南按“本地推理文档完整度”对 11 个开源 harness 排名，权重为 OSI 许可、文档化的本地运行时、维护状态与安全控制四项，并给出三条通用规则，首条即“先扩大上下文窗口”。对银行自研或选型 Agent 平台有参考意义：模型能力之外，harness 的工程化与评测才是生产落地的分水岭。
---

# 2026 年本地大模型最佳开源 Agent Harness 盘点

> 原文链接：https://www.marktechpost.com/2026/09/18/best-open-source-agent-harnesses-for-local-llms-in-2026/
> 来源：MarkTechPost

An agent is a model and a harness. The harness runs tools, holds state, manages permissions, and feeds context back to the model. With a local model, the harness matters more. Small context windows and weaker tool calling expose every design flaw.

This guide ranks 11 open-source harnesses by how well they document local inference. All repo facts were read from GitHub on September 18, 2026. The ranking weighs 4 things: OSI-approved license, documented local runtimes, maintenance status, and safety controls.

The 3 rules that apply to every harness

1. Raise the context window first: Per Ollama&#8217;s context length docs, defaults depend on VRAM: 4k under 24 GiB, 32k from 24 to 48 GiB, and 256k at 48 GiB or more. The same page says agents and coding tools should get at least 64,000 tokens. The fix is one line: OLLAMA_CONTEXT_LENGTH=64000 ollama serve.

2. Pick a model that supports tool calling: Goose&#8217;s provider docs state that models without tool calling can only do chat completion. With llama.cpp, Pi&#8217;s docs note the --jinja flag enables compatible chat templates and tool calling.

3. Budget memory honestly: Cline&#8217;s local guide maps 16 to 32GB RAM to small quantized models, 32 to 64GB to mid-size coding models, and 64GB or more to larger models. Ollama&#8217;s Hermes page lists gemma4 at about 16 GB VRAM and qwen3.6 at about 24 GB VRAM.

&

1. OpenCode

OpenCode documents 3 local paths in its own provider docs: Ollama, LM Studio, and llama.cpp&#8217;s llama-server. Each uses the @ai-sdk/openai-compatible package with a local baseURL. The docs claim support for 75+ providers overall.

Setup can be one command. Ollama&#8217;s OpenCode page shows ollama launch opencode. It recommends a context window of at least 64k tokens. OpenCode&#8217;s own docs add a practical tip. If tool calls fail, raise num_ctx to around 16k to 32k.

It ships 2 built-in agents. build has full access. plan is read-only and asks before running bash commands.

Best for: Developers who want the widest documented local setup in one terminal tool.

2. Pi

Pi is the minimalist pick. Its README gives the model 4 tools: read, write, edit, and bash. It deliberately skips MCP, sub-agents, plan mode, and permission popups. Those features arrive through TypeScript extensions and packages.

Pi has native support for the llama.cpp router server. The router discovers multiple GGUF files and loads them on demand. You manage models inside Pi with /llama. Ollama supports it too. ollama launch pi installs Pi, configures the provider, and opens a session.

One caveat matters for local use. Pi has no built-in permission system. It runs with your user&#8217;s permissions. The README recommends Docker, a micro-VM extension, or a policy sandbox for isolation.

The old badlogic/pi-mono URL now redirects to earendil-works/pi. Earendil acquired Pi in April 2026, and creator Mario Zechner joined the company. The Pragmatic Engineer reports that Pi is the foundation OpenClaw is built on.

Best for: Small local models, where a short tool list leaves more context for code.

3. Goose

Goose documents the most local runtimes of any harness here. Its provider docs list Ollama, LM Studio, Docker Model Runner, Ramalama, and Atomic Chat. vLLM and KServe work through the OpenAI-compatible provider. Custom providers can skip the API key for local servers.

Governance is a differentiator. The Linux Foundation formed the Agentic AI Foundation on December 9, 2025, with Block contributing goose. The repo now lives at aaif-goose/goose. Goose is written in Rust and ships a desktop app, a CLI, and an API. The README cites 70+ MCP extensions.

Ollama setup is short. Run goose configure, select Ollama, and enter a model name.

Best for: General automation beyond code, under neutral foundation governance.

4. Cline

Cline is the strongest editor-based option. Its local guide recommends one setting above all: enable &#8220;Use Compact Prompt&#8221; for local inference. It also advises focused tasks and fresh sessions when context grows.

Every file edit and command needs approval by default. Auto-approve is optional. Plan and Act modes separate strategy from execution.

One licensing detail deserves attention. Cline&#8217;s own README says the JetBrains plugins are not open-sourced. The VS Code extension, CLI, and SDK are in the Apache-2.0 repo.

Best for: VS Code users who want human-in-the-loop approvals with a local model.

5. OpenHands

OpenHands publishes the most specific local guidance. Its local LLM guide recommends Qwen3.6-35B-A3B as the first local model to try, as of May 21, 2026. Hardware needs are stated plainly. Quantized variants need at least 24GB of VRAM, or an Apple Silicon Mac with 64GB of unified memory.

Context guidance is equally direct. Set context length to at least 22,000 tokens, with 32,768 recommended. The guide warns that Ollama&#8217;s 4,096 default cannot even fit the system prompt.

Linux users face one trap. LM Studio binds to 127.0.0.1 by default, so a Dockerized OpenHands cannot reach it. Enabling &#8220;Serve on Local Network&#8221; fixes it.

Best for: Containerized, longer-running tasks on a workstation or server GPU.

6. Aider

Aider handles weak tool calling differently. Its edit formats have the model return edits as text. The whole format returns full files. The diff format returns search and replace blocks. Aider also sends a repository map of key symbols with each request.

Its Ollama docs flag a real hazard. Ollama silently discards context beyond the window. Aider counters this by sizing the window per request, plus 8k tokens for the reply. Note that the page still cites an older 2k Ollama default.

Maintenance is the concern. PyPI shows version 0.86.2 on February 12, 2026. The prior release was August 13, 2025.

Best for: Git-native pair programming with models that struggle at function calling.

7. Codex CLI

Codex CLI is Apache-2.0 and ships 2 built-in local providers. The source code defines ollama on port 11434 and lmstudio on port 1234. Per Ollama&#8217;s Codex page, codex --oss defaults to gpt-oss:20b. The -m flag selects another model.

There is one hard constraint. Codex now speaks only the Responses API at /v1/responses. The source rejects wire_api = "chat" and points to this discussion. Your local server must expose that endpoint.

The repo includes dedicated sandbox crates for Linux and Windows.

Best for: Teams standardized on gpt-oss who want built-in sandboxing.

8. Qwen Code

Qwen Code&#8217;s README lists OpenAI, Anthropic, Gemini, and Qwen protocols. It names Ollama and vLLM for local models. The project began from Google Gemini CLI v0.8.2. It stopped syncing upstream at v0.1. The npm install requires Node.js 22 or newer.

Best for: Pairing open-weight Qwen models with a harness tuned by the same lab.

9. Kilo Code

Kilo&#8217;s README states that the Kilo CLI is a fork of OpenCode. Kilo says it started as a Roo fork in 2025. It shipped a rebuilt VS Code extension on April 2, 2026. Its local model docs cover Ollama, LM Studio, and Atomic Chat. The same page warns that local models often lack prompt caching and computer use.

Best for: Former Roo Code users who want a maintained path with local support.

10. Hermes Agent

Hermes Agent from Nous Research is a general-purpose agent, not a coding tool. Its README describes a learning loop that creates skills from experience. Ollama says it ships with 70+ skills and cross-session memory. Setup points Hermes at http://127.0.0.1:11434/v1, and context length can auto-detect. Messaging gateways include Telegram, Discord, Slack, WhatsApp, Signal, and Email.

Best for: A persistent personal agent running on local models.

11. OpenClaw

OpenClaw is the most-starred project in this guide. Ollama describes it as a personal assistant that bridges messaging services to AI agents through a central gateway. For local models, Ollama recommends at least a 64k context window. First launch shows a security notice explaining the risks of tool access. Take it seriously. This harness connects to your messaging accounts.

Best for: Messaging-first assistants, for users prepared to manage the security surface.

Key Takeaways

OpenCode documents the most local paths among coding harnesses: Ollama, LM Studio, and llama.cpp.

Set context to 64,000 tokens before blaming the harness or the model.

Pi&#8217;s 4-tool design suits small models, but it needs a sandbox you provide.

Codex CLI works locally only through servers exposing the Responses API.

Check licenses per component: Crush is FSL, and Cline&#8217;s JetBrains plugin is closed.

The post Best Open-Source Agent Harnesses for Local LLMs in 2026 appeared first on MarkTechPost.