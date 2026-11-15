---
publish_time: 1792620939
link: https://www.marktechpost.com/2026/10/21/vercel-durable-harness-crash-proof-coding-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Vercel 开源 durable-harness（Apache-2.0，版本 0.0.x 实验阶段），为现有编程 harness（Pi、OpenCode、Claude Code、Codex 等）提供持久化适配，使其会话在崩溃、超时或云环境错误后不丢失工作。每个回合的步骤都写入持久化日志：调用前记录意图、完成后记录结果；函数崩溃后由队列把回合交给新函数，从日志续跑。
  
  已完成的模型与工具调用从日志读回，不重复计费；只读类工具可安全重放，退款等危险工具绝不二次执行。支持 Vercel、本地文件与自托管 Postgres 等多种运行环境；Claude Code 与 Codex 需运行在 Vercel Sandbox。目前无公开性能基准。
---

# Vercel 开源 durable-harness：为抗崩溃的编程智能体而生

> 原文链接：https://www.marktechpost.com/2026/10/21/vercel-durable-harness-crash-proof-coding-agents/
> 来源：MarkTechPost

Vercel has released durable-harness, an open-source package that keeps coding agent sessions alive through crashes and timeouts. Vercel durable-harness wraps existing harnesses, including Pi, OpenCode, Claude Code and Codex, without changing them. Each session lives in a durable log. A dead function no longer means lost work. For teams moving agents off laptops and into the cloud, that closes a real gap.

TL;DR

Size: npm package, version 0.0.x, Apache-2.0. Adapters cover 5 harnesses: Pi, OpenCode, fx, Claude Code, Codex.

Runs on: Vercel Functions plus Vercel Queues, Node.js 22+ with Postgres, or laptop files. Claude Code and Codex need a Vercel Sandbox.

Performance: No latency or throughput benchmarks published. All recovery claims are self-reported by Vercel.

Best: Finished model and tool calls are read back from the log, never re-run or billed twice.

Worst: Experimental 0.0.x API. Claude Code and Codex run only in a Vercel Sandbox, even self-hosted.

What is durable-harness?

durable-harness is a set of adapters from Vercel that store a harness session in a Workflow SDK World. A World bundles storage, a queue and a stream behind one interface. The package uses the same machinery that powers Vercel&#8217;s Workflow SDK. 

Why do coding agents lose work in the cloud?

Harnesses like Pi and Claude Code were designed as long-lived local processes. They keep the session in memory. Locally, the workspace and history sit on the same disk, so resuming takes 1 prompt. In the cloud, a VM with persistent storage does not track which calls completed. Vercel team notes a failed turn or network error then means lost work.

How does durable-harness work?

It writes each step of a turn to a durable log. Before a model or tool call runs, it records an intent. When the call finishes, it records the outcome. Each turn is backed by a message on Vercel Queues. If the function dies, the queue hands the turn to a new function. That function reads the log and continues.

After a crash, the log shows what finished, what was running and what never started:

Completed calls are read from the log, so finished model tokens are not billed again.

replay: 'safe' tools, such as lookups, can run again.

replay: 'never' tools, such as refunds, never run twice. The model is told the call may have happened.

Harness session files are mirrored into the log as well. That covers Claude Code&#8217;s transcript, Codex&#8217;s rollout and OpenCode&#8217;s event store.

Where do files and shell commands run?

Model-chosen commands never run on the function&#8217;s own disk. The tools docs list 3 workspace options:

virtual() keeps files in the session log, with a bash-compatible shell and no network. It holds about 500 files.

virtual({ durable: false }) keeps scratch files in memory and clears them every turn.

sandbox() gives each session a Vercel Sandbox, with /workspace on a Drive.

Typed JSON documents, such as a to-do list, also live in the log. Each holds at most 64 KB.

Where can you run durable-harness?

The agent code stays the same across Worlds:

Vercel: the Vercel World, with every session traced in Agent Runs.

Local: files on your machine, with no configuration.

Self-hosted: the Postgres World, version 5.0.4 or later, on Node.js 22+. Vercel&#8217;s blog also lists MongoDB, Redis and Turso.

2 environment variables, WORKFLOW_TARGET_WORLD and WORKFLOW_POSTGRES_URL, move an agent to Postgres.

How does durable-harness compare?

Featuredurable-harnessTemporal + OpenAI Agents SDKInngest AgentKitCloudflare Agents SDKWhat it isDurability adapters for existing coding harnessesDurable execution wrapper for OpenAI Agents SDKTypeScript multi-agent frameworkStateful agents on Durable ObjectsWraps Claude Code / CodexYes, experimental, Sandbox-onlyNot disclosedNot disclosedNot disclosedDurability backendWorkflow SDK World (Vercel, local, Postgres)Temporal server or Temporal CloudInngest orchestration engineDurable Objects, Cloudflare WorkflowsLanguageTypeScriptPythonTypeScriptTypeScriptLicenseApache-2.0MIT (server)Apache-2.0MITStatus0.0.x, experimentalGA since Mar 23, 2026Not disclosedNot disclosed

Key Takeaways

durable-harness logs every model and tool call, then resumes crashed turns on a new function.

Finished calls are never repeated, so tokens are not billed twice.

Pi and OpenCode run in your function; Claude Code and Codex need a Vercel Sandbox.

Self-hosting works with 2 env vars and a Postgres World.

It is 0.0.x and experimental, with no published benchmarks.

Check out the GitHub repo, docs and Vercel&#8217;s announcement. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Vercel Open-Sources durable-harness for Crash-Proof Coding Agents appeared first on MarkTechPost.