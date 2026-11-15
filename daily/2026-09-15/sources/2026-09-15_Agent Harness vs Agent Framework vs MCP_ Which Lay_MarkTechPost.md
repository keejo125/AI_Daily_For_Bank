---
publish_time: 1789422862
link: https://www.marktechpost.com/2026/09/14/agent-harness-vs-agent-framework-vs-mcp-which-layer-owns-the-loop-state-tools-permissions-and-recovery/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  文章厘清 Agent 架构中被混用的三个概念：Harness 是包裹模型、将其变为可用智能体的执行系统，统一管理执行循环、状态、工具传输、权限与恢复（如 OpenAI Codex、Claude Agent SDK）；Framework 是组合智能体的原语库（模型客户端、工具抽象等）；MCP 是工具/资源的传输协议。三者分处不同层、职责不同，但在边缘日益重叠。理解“哪一层拥有执行循环与状态”是设计可控 Agent 系统的关键。
---

# Agent Harness、Framework 与 MCP：执行循环、状态与工具到底归哪一层

> 原文链接：https://www.marktechpost.com/2026/09/14/agent-harness-vs-agent-framework-vs-mcp-which-layer-owns-the-loop-state-tools-permissions-and-recovery/
> 来源：MarkTechPost

Harness, framework, and MCP get used interchangeably in agent architecture discussions. They are not the same thing. They sit at different layers, own different responsibilities, and increasingly overlap at the edges. This article separates the 3 with 1 question. Which layer owns the execution loop, state, tool transport, permissions, and recovery?

The 3 categories

Agent harness: The harness is the execution system that wraps a model and turns it into a working agent. OpenAI&#8217;s Codex as a platform post (August 19, 2026) defines it directly. The harness manages conversation state, streams execution, and uses tools. It also enforces sandbox and approval policies and carries work across turns. Anthropic&#8217;s Claude Code docs call the same thing an agentic harness. The Claude Agent SDK exposes &#8216;the same tools, agent loop, and context management that power Claude Code.&#8217; A harness is opinionated. It ships a loop, a permission model, a sandbox, and a context strategy as one unit.

Agent framework: A framework is a library of primitives for composing agents. It covers model clients, tool abstractions, graph orchestration, memory interfaces, and observability hooks. Examples include LangGraph, the OpenAI Agents SDK, and Microsoft Agent Framework, which reached 1.0 GA in April 2026. A framework gives you the parts and the loop skeleton. You decide the policy.

MCP: The Model Context Protocol is a wire protocol, not a runtime. It standardizes how an LLM application (the host) discovers and calls capabilities exposed by servers: tools, resources, and prompts. MCP uses JSON-RPC 2.0 messages between hosts, clients, and servers. Since December 2025 the Linux Foundation&#8217;s Agentic AI Foundation has governed it, alongside goose, AGENTS.md, and now A2A. MCP owns no loop and no agent state. It owns the contract between the agent and its tools.

Ownership matrix

The table maps each responsibility to the layer that owns it by default. &#8220;Owns&#8221; means the layer defines and enforces the behavior. &#8220;Exposes&#8221; means the layer surfaces a hook but does not decide policy.

ResponsibilityAgent harnessAgent frameworkMCPExecution loopOwns: Fixed, product-grade loop with turn limits and compaction.Owns skeleton: You configure termination, handoffs, and turn caps.None: Request/response only.Agent state and memoryOwns: Sessions, resume, fork, file checkpointing.Exposes: Checkpointers, session stores, thread IDs.None at protocol level since 2026-07-28.Tool transportConsumes: Built-in tools plus MCP client.Consumes: Function tools plus MCP client.Own: JSON-RPC over stdio or Streamable HTTP.Permissions and approvalsOwns: Permission modes, hooks, sandbox.Exposes: Guardrails, interrupts, middleware.Delegates to host: Cannot enforce.RecoveryOwns: Session resume, checkpoint rewind, compaction.Exposes: Durable execution, replay, retries.Partial: Tasks extension for long-running calls.Isolation and sandboxingOwns: OS sandbox, worktrees, containers.Optional: Hosted sandboxes or micro-VMs.None.Multi-agent orchestrationOwns patterns: Subagents, dynamic workflows.Owns primitives: Graphs, handoffs, fan-out.None: A2A covers agent-to-agent.

The rest of this article justifies each row with sources.

Who owns the execution loop

Every agent runs a loop. Send context to the model, read the response, execute tool calls, feed results back, repeat. The harness and the framework both implement this loop. They differ in how much you control it.

Harness loop: The Claude Agent SDK documents its loop as 5 steps. Receive prompt, evaluate and respond, execute tools, repeat, return result. Each full cycle is 1 turn, and the loop ends when Claude produces a response with no tool calls. Hooks can intercept, modify, or block tool calls before they run. The loop itself is not yours to rewrite. OpenAI&#8217;s Codex harness exposes the loop through app-server, a documented client protocol. Applications create threads, start turns, receive events, and handle approval requests.

Framework loop: The OpenAI Agents SDK loop terminates on final output. It re-runs on handoff, or executes tool calls and continues. Exceeding max_turns raises MaxTurnsExceeded, and a guardrail tripwire raises GuardrailTripwireTriggered. In LangGraph, the loop is whatever graph you draw. Nodes, edges, and conditional routing define control flow.

MCP: MCP has no loop. Since the 2026-07-28 specification, it does not even have a handshake. The initialize/initialized exchange and Mcp-Session-Id header were retired. Every request travels alone, carrying its protocol version and client capabilities in _meta. The host&#8217;s loop decides when to call tools/call. MCP only defines what that call looks like on the wire.

Who owns state

Harness: State lives in the harness and persists across sessions. The Claude Agent SDK supports sessions that resume or fork later. File checkpointing restores files to any previous state. Microsoft&#8217;s harness layer ships a FileMemoryProvider for session-scoped notes and automatic context compaction that monitors token usage mid-loop. Anthropic&#8217;s long-running harness work goes further. It hands off state between context windows through artifacts on disk. Each new session begins with no memory of the last.

Framework: Frameworks expose state primitives but do not decide the persistence policy. LangGraph&#8217;s durable execution requires you to attach a checkpointer and pass a thread ID. It offers 3 durability modes. "exit" persists only when the graph exits, "async" writes while the next step runs, and "sync" writes before each step. Pick wrong and a crash mid-run loses state. The OpenAI Agents SDK offers Sessions for automatic conversation history, with SQLite, SQLAlchemy, and encrypted backends.

MCP: The 2026-07-28 release made the protocol core stateless. The maintainers&#8217; guidance is explicit. If a server needs state across calls, mint a handle from a tool. The model passes it back as an argument. State is the agent&#8217;s problem, not the protocol&#8217;s.

Who owns tool transport

This is the 1 row MCP owns outright.

MCP defines 3 server-side primitives: tools (functions the model executes), resources (context and data), and prompts (templated workflows). Clients may offer elicitation, which lets a server request more input from the user. Transport is JSON-RPC 2.0 over stdio or Streamable HTTP. The 2026-07-28 revision made Mcp-Method and Mcp-Name headers mandatory on HTTP requests. Gateways and rate limiters can now route on headers without parsing bodies. It also made tools/list responses cacheable with ttlMs and cacheScope, and deprecated the legacy HTTP+SSE transport with a 12-month offramp.

Server-initiated sampling, roots, and logging are now deprecated. Their replacement is Multi Round-Trip Requests (MRTR). A server returns resultType: "input_required", and the client retries the original call with answers attached. This matters for the permissions row below.

Harnesses and frameworks both sit on top of MCP as clients. Claude Code and the Claude Agent SDK connect to MCP servers. They also let you define custom tools through an in-process MCP server. Codex connects to MCP servers, and OpenAI&#8217;s Relay sample embeds Codex beside a dashboard driven by application-owned MCP tools. Microsoft Agent Framework 1.0 ships MCP and A2A support. The protocol is the shared substrate. Adoption numbers back that up. The MCP maintainers report close to half a billion SDK downloads per month across Tier 1 SDKs. The TypeScript and Python SDKs have each passed 1 billion total downloads.

Who owns permissions

The MCP specification is unambiguous here. Hosts must obtain explicit user consent before invoking any tool. Tool descriptions and annotations should be treated as untrusted unless the server is trusted. And then the key sentence: &#8220;MCP itself cannot enforce these security principles at the protocol level&#8220;. Permissions belong to the host.

Harness: Harnesses own the permission model end to end. Claude Code ships 6 permission modes: default, acceptEdits, plan, auto, dontAsk, and bypassPermissions. Deny rules block in every mode except bypassPermissions, which skips the permission layer entirely. auto mode routes each tool call through a background classifier. Hooks add custom logic at PreToolUse and PermissionRequest points. Codex takes the same shape. The app-server can pause a turn and issue an approval request the client must answer before work continues.

Framework: Frameworks give you the hook, not the policy. The OpenAI Agents SDK has input, output, and tool guardrails, and a tripwire halts the run. LangGraph uses interrupt() inside a node to pause for approval and Command(resume=...) to continue. Microsoft Agent Framework adds a ToolApprovalAgent middleware with &#8220;don&#8217;t ask again&#8221; rules. In each case you write the approval logic and the UI.

MCP: MCP now carries the approval request across the wire through elicitation over MRTR. Supabase, for instance, plans to use it so tools can confirm cost or a destructive query before acting. The server can ask. Only the host can decide.

Who owns recovery

Harness: Recovery is where harnesses earn their keep. The Claude Agent SDK can resume a session and rewind file changes to a checkpoint. It compacts context when a window fills. Claude Code&#8217;s dynamic workflows resume where they left off if a terminal is closed. Anthropic&#8217;s harness design post (March 2026) separates a generator from an evaluator agent because self-graded work skews positive. OpenAI&#8217;s harness post from February 2026 reports the outcome of this discipline. Codex produced roughly 1,500 merged pull requests in 5 months. The repository reached on the order of 1 million lines of code. The team grew from 3 to 7 engineers, averaging 3.5 PRs per engineer per day. OpenAI also reports a harness effect on ARC-AGI-3. Retained reasoning and context compaction lifted GPT-5.6 Sol from 13.3% to 38.3% while cutting output tokens sixfold . Same model, different harness, different score.

Framework: LangGraph&#8217;s durable execution is explicit that recovery depends on determinism. Wrap side effects in tasks, keep nodes idempotent, and a run can resume a week later. The OpenAI Agents SDK exposes error_handlers and preserves completed guardrail results when a run fails. The framework replays. You make replay safe.

MCP: MCP&#8217;s answer to long-running work is the io.modelcontextprotocol/tasks extension, contributed by AWS, with poll-based tasks/get and tasks/update. This covers a single long tool call. It does not cover agent-level recovery.

Architecture comparison

                    +------------------------------------------+
  Application       |  Your product: UI, records, business     |
                    |  rules, consent flows                    |
                    +------------------------------------------+
                          |                     |
                          v                     v
  Runtime layer     +----------------+   +-----------------------+
  (pick one, or     |  AGENT HARNESS |   |  AGENT FRAMEWORK      |
   combine)         |  fixed loop    |   |  composable loop      |
                    |  sessions      |   |  checkpointers        |
                    |  permissions   |   |  guardrails/interrupt |
                    |  sandbox       |   |  graphs, handoffs     |
                    |  compaction    |   |  middleware, tracing  |
                    +----------------+   +-----------------------+
                          |                     |
                          +----------+----------+
                                     v
  Transport layer   +------------------------------------------+
                    |  MCP (JSON-RPC 2.0, stdio / Streamable   |
                    |  HTTP): tools, resources, prompts,       |
                    |  elicitation, Tasks extension            |
                    +------------------------------------------+
                                     |
                                     v
  Capability layer  +------------------------------------------+
                    |  MCP servers: GitHub, Figma, Supabase,   |
                    |  Sentry, Linear, internal APIs           |
                    +------------------------------------------+

OpenAI draws a near-identical picture for Relay. The application owns product context, business rules, and tools. Codex app-server provides the agent loop and sandboxed execution.

Where the categories overlap

The boundaries are blurring in 3 directions:

Frameworks are absorbing harnesses: Microsoft Agent Framework now ships an &#8220;Agent Harness&#8221; layer. It turns any chat client into a full harness with 1 method call. It includes context compaction, file memory, a todo provider, and plan versus execute modes. It also adds background subagents and a sandboxed shell executor. Microsoft describes the harness as &#8220;the layer where model reasoning meets real execution.&#8221; A framework vendor is conceding that raw primitives are not enough.

Harnesses are becoming platforms: OpenAI open-sourced the Codex harness and now offers 3 integration tiers. codex exec runs bounded jobs, the Codex SDK gives programmatic control, and app-server embeds the loop in a product. Anthropic&#8217;s Claude Agent SDK does the same for Claude Code. DeepSeek released DeepSeek Harness v0.1 on August 13, 2026, under the MIT license. Its premise is that every component, including the loop, is a plugin. Once a harness is a library with a documented protocol, it competes with frameworks.

MCP is growing agent-shaped features: Elicitation, MRTR, the Tasks extension, Skills over MCP, and MCP Apps all push the protocol outward. These are interaction patterns that used to live in the runtime. The maintainers have drawn a line, though. Roots, sampling, and logging are deprecated, and the core is now request/response. MCP is standardizing the interface, not becoming the agent.

One term that does not overlap: A2A. Agent-to-agent communication is a separate protocol, now also housed at the Agentic AI Foundation. MCP connects an agent to tools. A2A connects an agent to other agents.

How to assemble the stack

The decision comes down to 3 questions:

Do you want to own the loop? Start with a framework if you need custom control flow or a graph you can test node by node. LangGraph, the OpenAI Agents SDK, and Microsoft Agent Framework each let you shape the loop. Expect to write the permission policy, the persistence policy, and the sandbox yourself.

Do you want a proven loop with permissions and recovery built in? A harness gets you further faster when the task resembles coding, operations, or research. Claude Agent SDK and Codex app-server ship sessions, approvals, sandboxes, and compaction as defaults. You trade loop control for production behavior. OpenAI&#8217;s own numbers show harness design moving benchmark scores by 25 points on the same model.

Which tools does the agent need? Answer with MCP regardless of the layer above. Every harness and every major framework speaks it. The 2026-07-28 stateless core means a remote MCP server is now an ordinary HTTP workload behind a load balancer. Build the tool surface once and reuse it across runtimes.

The common production shape in late 2026 is a hybrid. A framework orchestrates the outer graph. A harness runs each heavy step inside its own sandbox. MCP carries every tool call. The categories are layers, not rivals.

Key Takeaways

The harness owns the loop, state, permissions, and recovery as 1 opinionated unit.

The framework exposes the same hooks but leaves policy, persistence, and sandboxing to you.

MCP owns only tool transport and states it cannot enforce consent at the protocol level.

Frameworks now ship harness layers and harnesses now ship SDKs, so the boundary is converging.

Assemble by layer: framework or harness for the loop, MCP for every tool call.

Sources

Model Context Protocol, Specification 2026-07-28

MCP Blog, The 2026-07-28 Specification (July 28, 2026)

MCP Blog, The New MCP Roadmap (August 22, 2026)

Linux Foundation, Formation of the Agentic AI Foundation (December 9, 2025)

Linux Foundation, AAIF launches MCPA certification (September 2026)

OpenAI, Harness engineering: leveraging Codex in an agent-first world (February 11, 2026)

OpenAI Developers, Codex as a platform: build on the open agent harness (August 19, 2026)

OpenAI, Codex app-server and Codex SDK docs

OpenAI Agents SDK, Running agents, Guardrails, Sessions

Anthropic, Claude Agent SDK overview, How the agent loop works, Hooks, Sessions, File checkpointing

Anthropic, Claude Code permission modes

Anthropic Engineering, Effective harnesses for long-running agents (November 2025)

Anthropic Engineering, Harness design for long-running application development (March 24, 2026)

Anthropic Engineering, Code execution with MCP (November 4, 2025)

Claude Blog, A harness for every task: dynamic workflows in Claude Code (June 2, 2026)

Microsoft, Microsoft Agent Framework Version 1.0 (April 2026)

Microsoft, Microsoft Agent Framework at BUILD 2026: Agent Harness, Hosted Agents, CodeAct (June 3, 2026)

LangChain, LangGraph durable execution and Interrupts

DeepSeek, DeepSeek Harness (August 13, 2026)

The post Agent Harness vs Agent Framework vs MCP: Which Layer Owns the Loop, State, Tools, Permissions, and Recovery appeared first on MarkTechPost.