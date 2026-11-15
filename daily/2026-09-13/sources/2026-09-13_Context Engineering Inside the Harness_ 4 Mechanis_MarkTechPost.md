---
publish_time: 1789278963
link: https://www.marktechpost.com/2026/09/12/context-engineering-inside-the-harness-4-mechanisms-that-beat-context-overflow-and-goal-loss-on-long-horizon-tasks/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  本文拆解 Agent harness 中对抗长程任务『上下文溢出』与『目标丢失』的四类机制：压缩（compaction）、记忆策略、上下文预算（context budgeting）与待办状态（todo-state）。AWS 自主云编码 Agent 设计指南指出，浅层 Agent 在约 200 次工具调用、一小时任务中会出现上下文溢出与注意力涣散；更大上下文窗口并非解药——Chroma 评测 18 个 LLM 发现输入越长性能越不稳定，Anthropic 亦强调注意力预算随 token 递减。文章逐一对比 LangChain Deep Agents、Claude Code、Manus、OpenAI Codex、Amazon Bedrock AgentCore 的具体实现阈值，说明 harness（而非模型）才是把浅层循环变成深度 Agent 的关键层。
---

# Harness 内的上下文工程：对抗长程任务溢出与目标丢失的 4 机制

> 原文链接：https://www.marktechpost.com/2026/09/12/context-engineering-inside-the-harness-4-mechanisms-that-beat-context-overflow-and-goal-loss-on-long-horizon-tasks/
> 来源：MarkTechPost

An agent, in its simplest form, is an LLM calling tools in a loop. That loop works for short jobs. Give it a task that runs for an hour and 200 tool calls, and it breaks in 2 predictable ways. The AWS Samples design guide for autonomous cloud coding agents names them directly: shallow agents suffer from context overflow, get distracted (goal loss), and do not maintain state over long periods. The layer that fixes this is not the model. It is the harness, which AWS describes as managing everything but the model.

This article opens up that layer. Compaction, memory strategy, context budgeting, and todo-state are the machinery that turns a shallow loop into a deep agent. We look at how LangChain Deep Agents, Claude Code, Manus, OpenAI Codex, and Amazon Bedrock AgentCore implement each one, with the actual thresholds they ship.

Why a bigger window does not fix it

The obvious fix is a larger context window. The evidence says it helps less than expected. Chroma&#8217;s Context Rot report evaluated 18 LLMs, including GPT-4.1, Claude 4, Gemini 2.5, and Qwen3, and found that performance grows increasingly unreliable as input length grows, even on simple retrieval tasks. Anthropic&#8217;s context engineering guide explains the mechanism: attention creates n² pairwise relationships for n tokens, so every added token depletes a finite &#8220;attention budget.&#8221; Context is a resource with diminishing returns, not a bucket.

For an agent loop, this is worse than it sounds. Manus reports that a typical task needs around 50 tool calls, and that the input-to-output token ratio runs near 100:1. Each observation lands in context and stays there. The original instruction drifts toward the middle of the window, which is exactly where recall degrades. Goal loss is not only a model bug. It is the expected outcome of an unmanaged context on a long enough task.

Mechanism 1: Context budgeting and offloading

The first job of a harness is deciding what never enters the window at all. Deep Agents ships 2 offloading rules with hard numbers. When a tool response exceeds 20,000 tokens, it is written to the filesystem and replaced with a file path plus a preview of the first 10 lines. When session context crosses 85% of the model&#8217;s window, older write and edit tool calls, whose full file contents already live on disk, are truncated to a pointer. Only after offloading runs out of room does the harness fall back to summarization.

Claude Code applies the same budgeting to what loads before the first prompt. Auto memory is capped at the first 200 lines or 25KB. MCP tool schemas stay deferred by default, with only tool names listed, and full schemas load on demand via tool search. After compaction, any re-read file over 5,000 tokens comes back as a path reference rather than content. The context window simulation in the Claude Code docs makes the payoff concrete: a research subagent reads 6,100 tokens of files and returns a 420-token result to the parent.

That subagent pattern is budgeting at the architecture level. Anthropic&#8217;s guide notes that each subagent may burn tens of thousands of tokens exploring, but returns a distilled summary, often 1,000 to 2,000 tokens. The AWS AgentCore walkthrough builds exactly this: a coordinator spawns 3 browser subagents in parallel, each in its own MicroVM, and an analyst subagent receives only their structured findings. AWS reports a 4 to 6 minute expected runtime, and notes that sequential processing would take up to 3x longer.

Mechanism 2: Compaction

When offloading is not enough, the harness summarizes. Compaction is the practice of taking a conversation nearing the window limit, summarizing it, and reinitiating a new context with the summary. It is also where goal loss most often happens, because a lossy summary can drop the one constraint that mattered.

The implementations differ in what they promise to keep. Claude Code&#8217;s compaction prompt preserves architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs. Right after compaction it re-reads up to 5 of the files modified most recently, reloads the rules matching those files, and re-injects invoked skill bodies, capped at 5,000 tokens per skill and 25,000 total. The docs are explicit that detailed instructions from early in the conversation may be lost, which is why persistent rules belong in the project-root CLAUDE.md, which is re-injected from disk. Users can steer the pass with /compact focus on the auth bug fix or move the trigger point with /autocompact.

Deep Agents made goal preservation a structural feature. Its summary is a structured document with dedicated fields for session intent, artifacts created, and next steps. The LangChain team added those fields after forced-summarization experiments showed the change improved performance. The full original transcript is also written to the filesystem, so a fact that was summarized away can be recovered by read_file later.

Compaction has moved into the API layer too. OpenAI&#8217;s Responses API offers server-side compaction via context_management with a compact_threshold, plus a standalone /responses/compact endpoint that returns a compacted context window containing an opaque encrypted compaction item; OpenAI instructs developers to pass that returned window unchanged into the next call. OpenAI says Codex relies on this mechanism to sustain long-running coding tasks. The Claude Developer Platform exposes a compact_20260112 context-management edit with custom instructions and a pause_after_compaction option for inserting content before the model continues. When you write custom instructions there, they replace the default prompt entirely, so a compaction prompt is a real engineering artifact, not a setting.

Mechanism 3: Todo-state and recitation

Compaction protects the goal at the moment of summarization. Todo-state protects it on every turn in between. Manus described the trick plainly: its agent creates a todo.md and rewrites it step by step, checking items off. Rewriting the list recites the objectives into the end of the context, pushing the global plan into the model&#8217;s recent attention span and reducing &#8220;lost in the middle&#8221; drift. No architecture change is required. It is natural language used to bias the model&#8217;s own attention.

The evidence on todo-state is not one-sided. Deep Agents shipped a write_todos tool by default until v0.7 in July 2026, when LangChain made TodoListMiddleware opt-in after its evals across 3 task categories showed slightly better reward and lower cost with todos disabled. LangChain still recommends turning it back on for long multi-step tasks, less capable models, and UIs that show progress. Claude Code keeps a todo list and re-injects the plan written in plan mode from disk after compaction. Anthropic&#8217;s guide calls the general pattern structured note-taking: the agent writes a NOTES.md or TODO file outside the window and reloads it. Its Claude Plays Pokémon example maintained tallies across thousands of game steps, then read its own notes after each context reset and resumed multi-hour sequences.

The pattern behind all of these is that the goal exists as a mutable artifact, not only as a message in history. Messages age and get summarized. A file that is rewritten every few turns is always recent, always short, and survives any reset. Whether that is worth its per-turn token cost depends on the model and the task length, which is exactly what the Deep Agents evals measured.

Mechanism 4: Memory strategy across sessions

The last piece is what persists after the task ends. Claude Code re-injects the project-root CLAUDE.md and auto memory from disk after every compaction. AgentCore Memory stores events and runs configured extraction strategies in the background, so a coordinator can call a recall tool on the next run instead of re-researching. AWS warns that without at least 1 extraction strategy configured, raw events are stored but nothing is extracted for retrieval. Anthropic&#8217;s file-based memory tool serves the same purpose on the Claude platform.

The limitation is that persistent context is not free. The ETH Zurich study we covered in February found that repository context files like AGENTS.md do not generally improve task success while raising inference cost: LLM-generated files increased cost by 20% and 23% on the 2 benchmarks, and developer-committed files by up to 19%. Memory that reloads every session is a standing tax on the attention budget. The Claude Code docs give the matching advice: keep CLAUDE.md under 200 lines and move reference material into skills or path-scoped rules that load only when needed.

Interactive explainer: watch a 200K window fill up

The simulator below runs a 60-step migration task through a 200K token window. Toggle the 4 mechanisms, set the compaction trigger, and press Run. With everything off, the window overflows before the task is half done. With offloading, compaction, todo recitation, and subagent delegation on, the same task finishes with the goal still in recent attention. Token counts are illustrative; the thresholds match Deep Agents defaults.

&

Testing whether the harness actually holds the goal

Context management is only useful if the agent can still finish the task and recover details it no longer sees. LangChain maintains targeted evals for exactly this: tests that trigger summarization mid-task and check whether the agent continues toward its objective, and needle-in-a-haystack cases where a fact is summarized away and must be recovered through filesystem search. To generate enough events to compare prompt variants, the team triggers summarization at 10 to 20% of the window instead of the 85% default, and used a 25% trigger with Claude Sonnet 4.5 on terminal-bench-2 to study the effect.

The failure to watch for, in LangChain&#8217;s view, is goal drift: an agent that asks for clarification right after a summary, or wrongly declares the task complete. AgentCore Evaluations ships a goal success rate evaluator that can score the same traces. If you run a harness and have not forced a compaction in a test, you do not yet know what your summary prompt drops.

Key Takeaways

Shallow agents fail from context overflow and goal loss; the harness, not the model, is where the fix lives.

Budget first: Deep Agents offloads tool results over 20,000 tokens and evicts old edits at 85% of the window.

Compaction must name what it keeps; Deep Agents adds session intent and next steps fields, Claude Code re-reads 5 recent files.

Todo recitation keeps the goal at the end of context, but Deep Agents v0.7 evals show it is not a free win.

Persistent memory costs attention: ETH Zurich measured 20 to 23% higher inference cost from LLM-generated context files.

The post Context Engineering Inside the Harness: 4 Mechanisms That Beat Context Overflow and Goal Loss on Long-Horizon Tasks appeared first on MarkTechPost.