---
publish_time: 1792837771
link: https://www.marktechpost.com/2026/10/24/stateful-engineering-copilots-letta-tutorial/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  MarkTechPost 教程演示用 Letta 构建“有状态工程 Copilot”，说明 Agent 记忆如何超越传统基于 Prompt 的对话。作者先创建可由 Agent 自主更新的可检视核心记忆块，再将其暴露用于跨多 Agent 的程序化状态同步与共享访问；并扩展出档案向量记忆做语义检索、自定义服务端工具做确定性风险估计、流式观察执行、服务端消息历史做持久会话，以及 .af 导出便于移植。这些组件共同构成一套实用记忆架构，使持久状态、检索、工具、多 Agent 协作与执行轨迹作为集成化的 Agent 系统协同工作，对工程研发场景下的状态化智能体设计有直接参考价值。
---

# 用 Letta 构建有状态工程 Copilot：Agent 记忆超越 Prompt 对话

> 原文链接：https://www.marktechpost.com/2026/10/24/stateful-engineering-copilots-letta-tutorial/
> 来源：MarkTechPost

In this tutorial, we build a stateful engineering copilot with Letta that demonstrates how agentic memory extends beyond conventional prompt-based conversations. We begin by creating inspectable core memory blocks that the agent can autonomously update, then expose those blocks for programmatic state synchronization and shared access across multiple agents. We further extend the architecture with archival vector memory for semantic retrieval, a custom server-side tool for deterministic risk estimation, streaming for observing agent execution, server-side message history for persistent conversations, and .af export for portability. Together, these components demonstrate a practical memory architecture in which persistent state, retrieval, tools, multi-agent collaboration, and execution traces work as an integrated agentic system.

Copy CodeCopiedUse a different Browser

import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "letta-client"], check=True)
import os, json, time, textwrap
from getpass import getpass
from letta_client import Letta
def flex(*attempts, label=""):
   err = None
   for fn in attempts:
       try:
           return fn()
       except Exception as e:
           err = e
   raise RuntimeError(f"All call variants failed for {label or 'call'}: {err}") from err
API_KEY  = os.environ.get("LETTA_API_KEY") or getpass("Letta API key (platform.letta.com/api-keys): ")
BASE_URL = os.environ.get("LETTA_BASE_URL", "").strip()
client = flex(
   lambda: Letta(base_url=BASE_URL, api_key=API_KEY) if BASE_URL else Letta(api_key=API_KEY),
   lambda: Letta(base_url=BASE_URL, token=API_KEY)   if BASE_URL else Letta(token=API_KEY),
   label="client init",
)
def hr(title):
   print("\n" + "=" * 92 + f"\n  {title}\n" + "=" * 92)
def as_text(content):
   if isinstance(content, str):
       return content
   if isinstance(content, list):
       return "".join(getattr(p, "text", "") or "" for p in content)
   return str(content or "")
def show(response, hide_reasoning=False):
   for m in getattr(response, "messages", response) or []:
       kind = getattr(m, "message_type", None) or getattr(m, "type", "?")
       if kind == "reasoning_message" and not hide_reasoning:
           print(" reasoning :", textwrap.shorten(getattr(m, "reasoning", "") or "", 220))
       elif kind == "tool_call_message":
           tc = getattr(m, "tool_call", None)
           print(" tool call :", getattr(tc, "name", "?"), textwrap.shorten(str(getattr(tc, "arguments", "")), 200))
       elif kind == "tool_return_message":
           print("  tool ret  :", textwrap.shorten(str(getattr(m, "tool_return", "")), 260))
       elif kind == "assistant_message":
           print(" assistant :", as_text(getattr(m, "content", "")))
       elif kind == "approval_request_message":
           print("  approval  : agent is waiting for you to approve a tool call")
   u = getattr(response, "usage", None)
   if u:
       print(f"   ↳ steps={getattr(u, 'step_count', '?')} tokens={getattr(u, 'total_tokens', '?')}")
def chat(agent_id, text, max_steps=12, quiet=False):
   r = flex(
       lambda: client.agents.messages.create(agent_id=agent_id, input=text, max_steps=max_steps),
       lambda: client.agents.messages.create(agent_id=agent_id, input=text),
       lambda: client.agents.messages.create(agent_id=agent_id,
                                             messages=[{"role": "user", "content": text}]),
       label="messages.create",
   )
   if not quiet:
       print(f"\n user      : {text}")
       show(r)
   return r
PREFERRED = ["openai/gpt-4.1", "openai/gpt-4o-mini", "anthropic/claude-sonnet-4-20250514"]
try:
   handles = [getattr(m, "handle", None) for m in client.models.list()]
   MODEL = next((h for h in PREFERRED if h in handles), None) or handles[0]
except Exception:
   MODEL = PREFERRED[0]
print(f" connected · model handle = {MODEL}")
hr("1. Create a stateful agent with custom memory blocks")
def make_agent(**kw):
   return flex(
       lambda: client.agents.create(model=MODEL, embedding="openai/text-embedding-3-small", **kw),
       lambda: client.agents.create(model=MODEL, **kw),
       label="agents.create",
   )
copilot = make_agent(
   name=f"copilot-{int(time.time())}",
   description="Engineering copilot with inspectable long-term memory",
   tags=["tutorial", "copilot"],
   memory_blocks=[
       {"label": "persona",
        "value": "I am Mnemo, an engineering copilot. I am terse, concrete, and I never "
                 "invent facts — if I don't know something I say so and then go look it up.",
        "limit": 3000},
       {"label": "human",
        "description": "Durable facts about the engineer I work with: name, role, stack, "
                       "preferences, working style. Update this whenever I learn something stable.",
        "value": "Unknown so far.",
        "limit": 3000},
       {"label": "project_state",
        "description": "Live state of the project we are shipping: milestones, blockers, "
                       "decisions and their rationale. Keep it dense and current; delete stale lines.",
        "value": "(empty)",
        "limit": 5000},
       {"label": "lessons",
        "description": "Hard-won lessons and mistakes to never repeat. Append-only, one line each.",
        "value": "(empty)",
        "limit": 2000},
   ],
)
print("agent id:", copilot.id)
def get_block(agent_id, label):
   return flex(
       lambda: client.agents.blocks.retrieve(agent_id=agent_id, block_label=label),
       lambda: client.agents.blocks.retrieve(agent_id, label),
       label="agents.blocks.retrieve",
   )
def set_block(agent_id, label, value):
   return flex(
       lambda: client.agents.blocks.update(agent_id=agent_id, block_label=label, value=value),
       lambda: client.agents.blocks.modify(agent_id=agent_id, block_label=label, value=value),
       lambda: client.agents.blocks.update(agent_id, label, value=value),
       label="agents.blocks.update",
   )
def dump_memory(agent_id, title="core memory"):
   blocks = flex(lambda: client.agents.blocks.list(agent_id=agent_id),
                 lambda: client.agents.blocks.list(agent_id), label="agents.blocks.list")
   print(f"\n──── {title} ────")
   for b in blocks:
       ro = " [read-only]" if getattr(b, "read_only", False) else ""
       print(f"▸ {b.label}{ro} ({len(b.value or '')}/{getattr(b, 'limit', '?')} chars)")
       print(textwrap.indent(textwrap.fill(b.value or "", 100), "    "))
   return blocks
dump_memory(copilot.id, "core memory at birth")

We set up the Letta client, install the SDK, and add compatibility helpers that handle API variations across Letta versions. We dynamically select an available model and create a stateful engineering copilot with structured core memory blocks. We then inspect the initial memory state to establish the agent&#8217;s persistent context.

Copy CodeCopiedUse a different Browser

hr("2. Self-editing memory — talk once, then read the block back")
chat(copilot.id,
    "Hi, I'm Priya, staff engineer at Northwind. We're shipping 'Halo', a Rust ingestion "
    "service, on Nov 14. I hate long explanations — give me bullets or code, never essays. "
    "Current blocker: the Kafka consumer rebalances every ~4 minutes under load.")
chat(copilot.id,
    "Update: we traced the rebalance to a 5s max.poll.interval.ms with slow batch commits. "
    "Decision: move commits off the poll loop. Also remember we already tried bumping "
    "session.timeout.ms and it did nothing — don't suggest that again.")
dump_memory(copilot.id, "core memory after 2 turns (note what moved where)")
hr("3. Your code writes into the context window")
live = get_block(copilot.id, "project_state")
set_block(copilot.id, "project_state",
         (live.value or "") + "\n[CI 09:41Z] main is RED: integration/kafka_rebalance_test failing (flaky x3).")
chat(copilot.id, "Anything I should know before I start the day?")
hr("4. Shared memory between two agents")
policies = client.blocks.create(
   label="policies",
   description="Non-negotiable engineering policies. Read-only: obey, never edit.",
   value="1. No direct pushes to main.\n2. Every fix ships with a regression test.\n"
         "3. Customer data never leaves EU regions.",
   limit=2000,
   read_only=True,
)
scratchpad = client.blocks.create(
   label="team_scratchpad",
   description="Shared working notes between the copilot and the reviewer agent. "
               "Both agents read and write here; keep entries prefixed with your name.",
   value="(empty)",
   limit=4000,
)
for bid in (policies.id, scratchpad.id):
   flex(lambda: client.agents.blocks.attach(agent_id=copilot.id, block_id=bid),
        lambda: client.agents.blocks.attach(copilot.id, bid),
        label="agents.blocks.attach")
reviewer = make_agent(
   name=f"reviewer-{int(time.time())}",
   description="Strict code reviewer sharing memory with the copilot",
   tags=["tutorial", "reviewer"],
   block_ids=[policies.id, scratchpad.id],
   memory_blocks=[{"label": "persona",
                   "value": "I am Argus, a paranoid staff reviewer. I look for the failure mode "
                            "everyone else skipped, and I cite the team policies by number."}],
)
print("reviewer id:", reviewer.id)
chat(copilot.id, "Write your proposed fix for the rebalance issue into the team_scratchpad "
                "block so the reviewer can see it. Keep it to 4 lines.")
print("\n what the REVIEWER sees in the shared block (written by the other agent):")
print(textwrap.indent(client.blocks.retrieve(scratchpad.id).value, "    "))
chat(reviewer.id, "Read team_scratchpad and review the proposed fix. Cite any policy it violates, "
                 "then append your verdict to the same block.")
print("\n shared block after the reviewer replied:")
print(textwrap.indent(client.blocks.retrieve(scratchpad.id).value, "    "))
print("\nagents attached to this block:",
     [a.name for a in flex(lambda: client.blocks.agents.list(block_id=scratchpad.id),
                           lambda: client.blocks.agents.list(scratchpad.id),
                           label="blocks.agents.list")])

We demonstrate self-editing memory by providing the copilot with durable information about the engineer, project, decisions, and known failure modes. We also update project state directly from application code and create shared read-only and writable blocks for multi-agent collaboration. We then connect a reviewer agent to the shared memory and observe how both agents exchange persistent working context.

Copy CodeCopiedUse a different Browser

hr("5. Archival memory: bulk-load knowledge, then let the agent retrieve it")
KNOWLEDGE = [
   ("Postmortem 2024-08-02: Halo dropped 1.2M events when the consumer group rebalanced during a "
    "deploy. Root cause: commits inside the poll loop blocked past max.poll.interval.ms.",
    ["postmortem", "kafka", "halo"]),
   ("ADR-017: Halo uses at-least-once delivery with idempotent writes keyed on (tenant_id, event_id). "
    "Exactly-once via Kafka transactions was rejected for throughput reasons.",
    ["adr", "architecture", "halo"]),
   ("Runbook: to drain a Halo node, set DRAIN=1, wait for lag<1000, then SIGTERM. Never SIGKILL — "
    "in-flight batches are only checkpointed on graceful shutdown.",
    ["runbook", "ops", "halo"]),
   ("Benchmark 2025-01: rdkafka 2.3 with 8 partitions sustained 240k events/s at p99 32ms on "
    "c6i.4xlarge; the bottleneck was JSON parsing, not the network.",
    ["benchmark", "performance"]),
   ("Priya's preference on file layout: one module per bounded context, integration tests live "
    "next to the module, no tests/ mega-directory.", ["preference", "style"]),
   ("Incident 2025-03-19: an EU tenant's payload was mirrored to us-east-1 for 40 minutes. "
    "Fixed by region-pinning the DLQ. This is why policy 3 exists.", ["incident", "compliance"]),
]
def archive(agent_id, content, tags):
   return flex(
       lambda: client.agents.passages.insert(agent_id=agent_id, content=content, tags=tags),
       lambda: client.agents.passages.create(agent_id=agent_id, text=content, tags=tags),
       lambda: client.agents.passages.create(agent_id=agent_id, text=content),
       label="agents.passages.insert",
   )
for content, tags in KNOWLEDGE:
   archive(copilot.id, content, tags)
print(f"inserted {len(KNOWLEDGE)} passages")
hits = flex(
   lambda: client.agents.passages.search(agent_id=copilot.id, query="losing messages during a deploy"),
   lambda: client.agents.passages.list(agent_id=copilot.id, search="losing messages during a deploy"),
   label="agents.passages.search",
)
print("\n programmatic semantic search for 'losing messages during a deploy':")
for h in list(hits)[:3]:
   print("   •", textwrap.shorten(getattr(h, "content", None) or getattr(h, "text", ""), 150))
chat(copilot.id, "Before I restart a node tonight: is there anything in our history I should "
                "worry about, and what's the safe procedure?")
hr("6. Give the agent a custom tool")
def estimate_release_risk(open_bugs: int, days_to_deadline: int, test_coverage: float) -> str:
   """Estimate the risk of shipping a release on time.
   Args:
       open_bugs (int): Number of open P0/P1 bugs.
       days_to_deadline (int): Calendar days left before the ship date.
       test_coverage (float): Line coverage as a fraction between 0.0 and 1.0.
   Returns:
       str: A risk score from 0-100 and a verdict.
   """
   import math
   pressure = open_bugs / max(days_to_deadline, 1)
   score = max(0.0, min(100.0, 100 * (1 - math.exp(-1.4 * pressure)) * (1.3 - test_coverage)))
   verdict = "SHIP" if score < 35 else ("SLIP ONE WEEK" if score < 70 else "DO NOT SHIP")
   return f"risk_score={score:.1f} verdict={verdict}"
tool = flex(
   lambda: client.tools.upsert_from_function(func=estimate_release_risk),
   lambda: client.tools.create_from_function(func=estimate_release_risk),
   label="tools.upsert_from_function",
)
flex(lambda: client.agents.tools.attach(agent_id=copilot.id, tool_id=tool.id),
    lambda: client.agents.tools.attach(copilot.id, tool.id),
    label="agents.tools.attach")
print("attached tool:", tool.name, "| agent tools:",
     [t.name for t in flex(lambda: client.agents.tools.list(agent_id=copilot.id),
                           lambda: client.agents.tools.list(copilot.id), label="agents.tools.list")])
chat(copilot.id, "We have 9 open P0/P1 bugs, 12 days to the Nov 14 date, coverage is 0.61. "
                "Score the risk with the tool, then record the verdict in project_state.")

We populate archival memory with tagged engineering knowledge and use semantic search to retrieve relevant information without relying on exact keyword matches. We then allow the agent to query this archival knowledge autonomously when answering an operational question. Finally, we create and attach a custom server-side release-risk tool so the agent can perform deterministic calculations and record the resulting decision in memory.

Copy CodeCopiedUse a different Browser

hr("7. Streaming the agent's steps")
def stream_chat(agent_id, text):
   print(f" user      : {text}")
   s = flex(
       lambda: client.agents.messages.stream(agent_id=agent_id, input=text),
       lambda: client.agents.messages.stream(agent_id=agent_id,
                                             messages=[{"role": "user", "content": text}]),
       lambda: client.agents.messages.create_stream(agent_id=agent_id,
                                                    messages=[{"role": "user", "content": text}]),
       label="messages.stream",
   )
   for chunk in s:
       kind = getattr(chunk, "message_type", None) or getattr(chunk, "type", "")
       if kind == "reasoning_message":
           print("", textwrap.shorten(getattr(chunk, "reasoning", "") or "", 160))
       elif kind == "tool_call_message":
           print("", getattr(getattr(chunk, "tool_call", None), "name", "?"))
       elif kind == "assistant_message":
           print("", as_text(getattr(chunk, "content", "")))
try:
   stream_chat(copilot.id, "One-line status of Halo, from memory only. No tools.")
except Exception as e:
   print("streaming unavailable on this SDK version:", e)
hr("8. Server-side conversation history")
hist = flex(lambda: client.agents.messages.list(agent_id=copilot.id, limit=8),
           lambda: client.agents.messages.list(copilot.id, limit=8),
           label="agents.messages.list")
for m in hist:
   kind = getattr(m, "message_type", "?")
   body = as_text(getattr(m, "content", "")) or getattr(m, "reasoning", "") or ""
   print(f"  [{kind:<24}] {textwrap.shorten(str(body), 110)}")
print("\n  reconnect from a fresh process with just the id:")
print("    client.agents.messages.create(agent_id='%s', input='...')" % copilot.id)

We use Letta&#8217;s streaming interface to observe reasoning, tool calls, and assistant responses as the agent executes a task. We then inspect server-side conversation history to verify that the interaction state persists independently of the local Python process. We also demonstrate how the agent can be reconnected from a fresh process using only its persistent identifier.

Copy CodeCopiedUse a different Browser

hr("9. Export / import the agent")
try:
   dump = flex(lambda: client.agents.export_file(agent_id=copilot.id),
               lambda: client.agents.export_file(copilot.id), label="agents.export_file")
   blob = dump if isinstance(dump, (str, bytes)) else json.dumps(dump, default=str)
   path = "/content/copilot.af" if os.path.isdir("/content") else "copilot.af"
   with open(path, "wb" if isinstance(blob, bytes) else "w") as f:
       f.write(blob)
   print(f"exported → {path} ({len(blob)} bytes) — memory, tools and history travel with it.")
   print("re-import later with: client.agents.import_file(file=open(path,'rb'))")
except Exception as e:
   print("export not available on this SDK/deployment:", e)
CLEANUP = False
if CLEANUP:
   for aid in (copilot.id, reviewer.id):
       try: client.agents.delete(aid)
       except Exception as e: print("agent delete:", e)
   for bid in (policies.id, scratchpad.id):
       try: client.blocks.delete(bid)
       except Exception as e: print("block delete:", e)
   print("deleted.")
else:
   hr("Done")
   print(f"copilot  : {copilot.id}\nreviewer : {reviewer.id}")
   print("Inspect them visually in the ADE at https://app.letta.com")

We export the complete agent state to an .af file, providing a portable representation of the agent&#8217;s memory, tools, and conversation state. We then include optional cleanup logic that removes the agents and shared blocks created during the tutorial. We finish by displaying the persistent agent identifiers and the Letta ADE location for further inspection.

In conclusion, we now have a complete view of how Letta supports persistent, inspectable agent workflows rather than treating every interaction as an isolated prompt. We saw how core memory maintains high-value state in context, archival memory provides scalable retrieval, shared and read-only blocks coordinate multiple agents, and application code can directly synchronize external state. We also used custom tools and streaming to extend and observe agent behavior while server-side history and agent export provide persistence and portability. Through this workflow, we established a practical foundation for building engineering copilots that continuously retain context, reason over accumulated knowledge, collaborate across agents, and operate with explicit, controllable memory.

Check out the FULL CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Stateful Agentic Engineering Copilots with Letta: Core Memory, Shared State, Semantic Retrieval, Custom Tools, Streaming, and Portable Agent Workflows appeared first on MarkTechPost.