---
publish_time: 1786139568
status: pending
---

# Tencent Cloud Open-Sources TencentDB Agent Memory v2.0: A Team-Level Memory Hub for AI Coding Agents

> 原文链接：https://www.marktechpost.com/2026/08/07/tencent-cloud-open-sources-tencentdb-agent-memory-v2-0/
> 来源：MarkTechPost

Tencent Cloud has open-sourced TencentDB Agent Memory v2.0, a team-level memory hub for AI agents. The idea is super simple: if project context was already explained once, a new session should not need it repeated. The system turns conversations, documents and code into four reusable memory assets — Chat Memory, Skill, LLM-Wiki and Code-Graph — that are versioned, permissioned and equipped to specific agents. Single-agent memory is not new. What is new here is the governance layer, which lets a teammate&#8217;s agent read what your agent learned, without leaking anything you marked private. The stable 2.0.0 release is published on August 3, 2026.

Is it deployable?

Yes, it is deployable. TencentDB Agent Memory is MIT-licensed and self-hosted. Three Docker images published to Docker Hub start with one command, and multi-arch builds cover linux/amd64 and linux/arm64.

Which companies: Solo builders and small engineering teams get the most value now. The project explicitly targets the one-person company. Mid-size orgs with a platform or DevEx function can run it as shared infrastructure. Large regulated enterprises should pilot rather than standardize, because private-repo CodeGraph and automated memory routing are still being refined.

Industries: Software and developer tooling, SaaS, fintech, consulting and agencies, plus any regulated team that needs memory to stay inside its own network.

Applications: Onboarding a new agent to an existing codebase, impact analysis before refactoring, release checklists, incident runbooks, code review standards, and turning product docs into agent-readable pages.

Four memory assets

The system converts work into four asset types: 

Chat Memory retains preferences, facts, decisions and interaction history. 

Skill distills reusable procedures from completed tasks, carrying versions, resource files, trigger boundaries, execution steps and validation rules. 

Wiki turns documents into structured pages with a link graph, an approach informed by Andrej Karpathy&#8217;s LLM-maintained knowledge base idea. 

CodeGraph indexes symbols, files, call relationships and impact paths.

All four register uniformly as Memory Assets, so ownership, version, status and visibility behave identically across them.

Layered distillation, budgeted retrieval

Chat Memory is not flat. Conversations save as L0, then an async pipeline refines them into L1 Atom, L2 Scenario and L3 Core/Persona. Retrieval is layered too. L2 and L3 provide a fast context bootstrap. When specific facts are needed, BM25 plus vector retrieval plus RRF falls back to L1 and L0. Results are capped by item count, character budget and timeout, so memory does not crowd out the context window.

Governance is the actual differentiator

Standard RAG answers what can be found. The Hub also answers who may use it, which version is valid, and which agent receives it. Visibility runs private, team and restricted, with agent for targeted equipping. Per the README, private is owner-only, not readable even by team admins. New Chat Memory and Skills default to private, making sharing an explicit action.

Memory Hub uses fixed binding plus ACL: narrow by team, user, agent and visibility first, then retrieve.

Wiring agents in

Memory Proxy speaks both Anthropic and OpenAI protocols, exposing /claude-code/<spaceId>/v1/messages and /v1/chat/completions. On the first turn, sessionInit uses Claude Code&#8217;s native AskUserQuestion tool to pick team, agent and task. Every subsequent turn injects that agent&#8217;s L2/L3 memory, matched skills and knowledge into the system prompt before forwarding upstream.

Default ports are 8420 for Memory Core, 8125 for the panel, 8424 for the knowledge service and 8096 for the proxy, per INSTALL.md. Official SDKs ship for TypeScript and Python. Supported integrations are OpenClaw, Hermes, Claude Code, CodeBuddy and direct SDK use.

The 2.0.0 release adds Skill forced archiving, scheduled CodeGraph repository sync, system-admin asset management, English/Chinese panel switching, and a Cost Guard that assigns cheaper models to specific agents.

Reported results

It reports PersonaMem accuracy rising from 48% to 76%, a 59% relative improvement. That figure is self-reported, and no independent reproduction has been published.

Key Takeaways

MIT-licensed, self-hosted, one-command Docker deploy — no vendor API dependency.

Four asset types replace chat logs: Chat Memory, Skill, Wiki, CodeGraph.

L0→L3 distillation with BM25 + vector + RRF retrieval under strict budget caps.

ACL-governed sharing is the real differentiator over standard RAG.

PersonaMem 48%→76% is self-reported; private-repo CodeGraph is unfinished.

Check out the GitHub repository, CHANGELOG, INSTALL.md, and Knowledge OpenAPI. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Tencent Cloud Open-Sources TencentDB Agent Memory v2.0: A Team-Level Memory Hub for AI Coding Agents appeared first on MarkTechPost.