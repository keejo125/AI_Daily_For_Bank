---
publish_time: 1786135322
status: pending
---

# NVIDIA AI Releases NOOA: An Object-Oriented Python Framework That Turns an AI Agent Into a Single Python Class

> 原文链接：https://www.marktechpost.com/2026/08/07/nvidia-ai-releases-nooa-an-object-oriented-python-framework/
> 来源：MarkTechPost

NVIDIA Labs has open-sourced NOOA (NVIDIA Object-Oriented Agents), a model-agnostic Python framework for building AI agents. Agent development today is split across prompt templates, tool schemas, callback code, and workflow graphs. NOOA collapses all of it into one Python class. Methods are the actions the model can take. Fields are agent state. Docstrings are prompts. Type annotations are contracts the runtime enforces. A method whose body is ... is completed at runtime by an LLM-driven loop, while a method with a normal body stays deterministic Python. Developers and models therefore share one interface, so agent behavior can be tested, traced, refactored, and version-controlled like ordinary software. NVIDIA reports 82.2% on SWE-bench Verified, 86.8% on CyberGym L1, and 85.1% mean RHAE on ARC-AGI-3 — at roughly half the tokens of the open harnesses it was compared against.

Is it deployable?

Yes, but only inside OS-level isolation. NOOA is Apache 2.0, installs with pip install nooa (v0.0.8, released July 30, 2026), and requires Python 3.12–3.13. PyPI classifies it as alpha, and NVIDIA describes it as a research preview. Agents can execute LLM-generated code, and NVIDIA states directly that its AST checks and module deny-lists are defense-in-depth guardrails, not a containment boundary. The containment boundary is a container, a VM, or NVIDIA OpenShell. Models are pluggable through LiteLLM, so hosted APIs, Ollama, and vLLM endpoints all work.

Company level: AI-native startups and mid-market platform teams building internal agents. Enterprise AI platform and applied-research groups running evaluations or pilots. Regulated production workloads should wait for a stable release.

Industries: developer tooling, cybersecurity, cloud and DevOps, data analytics, financial services operations, customer support.

Applications: repository issue triage and patching, terminal and infrastructure automation, vulnerability validation pipelines, large-batch classification and extraction over in-memory data, typed multi-agent orchestration.

An agent is a Python object

NVIDIA Labs released NOOA (NVIDIA Object-Oriented Agents), a model-agnostic Python framework for building agents. Traditional agent development splits source across prompt templates, tool schemas, callbacks, and workflow graphs. NOOA collapses that into one class.

Methods are the actions the model can take. Fields are state. Docstrings are prompts. Type annotations are contracts enforced by the runtime. A method whose body is ... becomes an agentic method, completed at runtime by an LLM-driven loop; a method with a normal body stays deterministic Python the model can call as a tool.

Two strategies ship. PredictStrategy is a single typed LLM call with a local retry loop on validation failure. CodeActStrategy runs an iterative Python REPL where the model calls execute_python(...) until it submits return_result(...), which is validated against the return annotation.

Six capabilities on one surface

The research team identifies six model-facing ideas it claims to be the first to combine: typed input/output, pass by reference over live objects, code as action, programmable loop engineering, explicit object state, and model-callable harness APIs. NVIDIA scored fourteen frameworks and harnesses—LangGraph, Google ADK, PydanticAI, smolagents, Claude Agent SDK, OpenAI Codex, OpenHands, and others—against the same axes, and reports partial coverage everywhere else.

Pass by reference is the load-bearing one. Arguments arrive as live Python objects; the model sees only a bounded preview with the concrete type, true length, and a head/tail sample. A hundred-element list renders in about thirty tokens while the full variable stays in the REPL. Context is split into a cacheable static prefix, an append-only typed event history, and dynamic blocks at the tail, which preserves KV-cache reuse across turns.

An optional memory subsystem attaches to an unmodified agent. Seven model-callable tools write and recall records ranked by ACT-R activation, all in one human-inspectable SQLite file.

Performance

Capability tests ran 88 tests five times across ten models: 4,309 of 4,400 records passed (97.9%). A six-family stress subset covering batching, error recovery, and decomposition passed 84.7%, where the gap between small and frontier models widens from 3.2 to 23 points.

End-to-end, a benchmark-agnostic 253-line agent reaches 82.2% on SWE-bench Verified with GPT-5.5 at xhigh effort, against 78.6% for OpenCode and 78.2% for PI, and 79.8% with Opus 4.6. On Terminal-Bench 2.0 it reaches 73.0% at high effort versus 60.7% and 68.5%, though PI leads at xhigh with 75.3%. On CyberGym L1 it solves 86.8% with network access blocked, the top open-source result reported. On ARC-AGI-3, one agent with a one-page world-model skill reaches 50.2% mean RHAE with GPT-5.5 and 85.1% with GPT-5.6-sol, under $20 per game.

Efficiency is the more interesting result: 82.2% at roughly 1.1M tokens and ~28 model calls per task, against 2.2M tokens and 66 calls for PI at 78.2%. Trace analysis also credits validated termination—OpenCode stops when the model replies without a tool call, while NOOA requires a typed TaskResult carrying evidence and a verification command.

Key Takeaways

An agent is one Python class—methods are actions, fields are state, docstrings are prompts, annotations are enforced contracts.

A ... method body becomes an LLM loop; a real body stays deterministic Python the model can call.

Pass by reference keeps large data live in the REPL, so no context compaction was needed on SWE-bench.

82.2% SWE-bench Verified and 86.8% CyberGym L1 at roughly half the tokens of the compared open harnesses.

Apache 2.0 and pip-installable, but alpha—execute generated code only inside OS-level isolation.

Check out the Paper, GitHub Repo and Technical Blog. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA AI Releases NOOA: An Object-Oriented Python Framework That Turns an AI Agent Into a Single Python Class appeared first on MarkTechPost.