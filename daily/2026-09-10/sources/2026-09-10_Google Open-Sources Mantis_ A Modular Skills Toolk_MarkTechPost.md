---
publish_time: 1788994709
link: https://www.marktechpost.com/2026/09/09/google-open-sources-mantis-a-modular-skills-toolkit-that-lets-coding-agents-find-reproduce-and-patch-vulnerabilities/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google 开源 Mantis，一套与技术栈无关的模块化安全审查技能工具包，使 AI 编程智能体能够自动完成漏洞发现、复现与补丁修复的完整生命周期。Mantis 面向代码安全审查场景，降低安全左移的门槛，让 coding agent 在开发流程中持续把关代码质量。
---

# Google 开源 Mantis：让编程智能体自动发现并修复漏洞的模块化技能工具

> 原文链接：https://www.marktechpost.com/2026/09/09/google-open-sources-mantis-a-modular-skills-toolkit-that-lets-coding-agents-find-reproduce-and-patch-vulnerabilities/
> 来源：MarkTechPost

Google has open-sourced Mantis, a stack-agnostic toolkit of security review skills that lets an AI coding agent run the whole vulnerability lifecycle. It finds a suspected flaw, strips the false positives, reproduces the bug inside a sandbox, writes a minimal patch, re-attacks that patch, and scores the residual risk. 

Mantis is not a scanner you aim at a repository and walk away from. It is a set of slash commands your existing coding agent loads, plus a strict set of rules about where that agent is allowed to execute code.

Is it deployable? Yes for local and internal evaluation, not yet for production. You can clone it today and run it with Gemini CLI, Antigravity CLI, the Google ADK, or any comparable agent framework. 

The pipeline

Mantis publishes each stage as a separate skill directory, invoked as a slash command and chained sequentially. A supervisor skill, /mantis-meta-agent, can drive the whole loop in a long-lived session.

The early stages learn the target: /mantis-history mines version control history for past security fixes, /mantis-summarize writes the directory maps, /mantis-architecture builds a Markdown knowledge base, /mantis-threat-model derives trust boundaries, and /mantis-plan produces a targeted roadmap.

The middle stages find and filter: /mantis-researcher sweeps files against the plan, then /mantis-dedupe, /mantis-review and /mantis-critic collapse duplicates, apply negative rules, and drop issues that cannot occur in a release build.

The late stages prove and fix: /mantis-reproduce executes payloads in gVisor or a VM with networking disabled, /mantis-chain assembles multi-step exploit chains from individually confirmed findings, /mantis-patch applies and verifies the fix, /mantis-calibrate assigns a risk score from 1 to 10, /mantis-reflect writes learnings back for the next pass, and /mantis-report produces the human-readable review packet.

A newer skill, /mantis-advise, inverts the flow. It queries the accumulated threat model, past bug lineages and verified patch patterns before you write code, so the same class of bug does not land twice.

But why?

Most agentic security tooling stops at generating findings. Mantis is interesting because it treats the reproducer and the re-attack as the trust boundary, and because it publishes the inter-stage contracts so teams can wrap the skills in a deterministic harness instead of trusting an LLM to orchestrate shell commands. 

Key Takeaways

Mantis is a modular skills toolkit for coding agents, not a standalone scanner or a supported Google product.

Its differentiator is grounding: sandboxed reproduction and patch re-attack, not model confidence.

A hierarchical summary tree cuts token overhead by over 85 percent, per Google.

Google cites sub-7 percent true-positive rates for naive AI code scanning as the problem Mantis targets.

Deployable locally under Apache 2.0 but not recommended yet for production.

Check out the google/mantis on GitHub, Agent Reference Guide, Cloud CISO Perspectives, and Getting started with Mantis. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google Open-Sources Mantis: A Modular Skills Toolkit That Lets Coding Agents Find, Reproduce and Patch Vulnerabilities appeared first on MarkTechPost.