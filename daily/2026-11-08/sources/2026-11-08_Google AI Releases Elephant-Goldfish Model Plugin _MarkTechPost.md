---
publish_time: 1794134778
link: https://www.marktechpost.com/2026/11/08/google-elephant-goldfish-model-plugin-spec-review-coding-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google 开源 Elephant-Goldfish Model（EGM）插件，为 AI 编程智能体提供“先写规格、再写代码”的设计与评审层。其核心是让一个持有项目上下文的长会话（Elephant）起草规格，再由多个无状态的“金鱼”子智能体独立攻击该规格，在 PR 之前而非之中捕获错误假设。包含 7 个技能、9 类评审角色、6 个头脑风暴视角与 5 段式评审，可跑在 Antigravity、Claude Code、Codex 等任意能派发新鲜上下文的 harness 上。Google 称数千名工程师已在用，但代价是 token 消耗大、部分宿主隔离未经验证。
---

# 谷歌开源 Elephant-Goldfish 模型插件：为 AI 编程智能体引入“先写规格再写代码”的评审层

> 原文链接：https://www.marktechpost.com/2026/11/08/google-elephant-goldfish-model-plugin-spec-review-coding-agents/
> 来源：MarkTechPost

Google has open-sourced the Elephant-Goldfish Model (EGM) plugin, a design-and-review layer for AI coding agents. The Elephant-Goldfish Model plugin makes an agent write a specification before it writes code. Fresh subagents with no conversation history then attack that spec. Google says thousands of its engineers use it. It is quite simple: catch wrong assumptions in a Markdown file, not in a pull request.

TL;DR

Size: 7 skills, 9 reviewer personas, 6 brainstorm lenses, 5 review stages. No model weights; your agent supplies the LLM.

Runs on: any harness that can spawn fresh subagents: Antigravity, Claude Code 2.1.271+, Claude Cowork, Codex, ChatGPT. Uses your existing model quota.

Performance: no accuracy benchmark published. Evidence is adoption and end-to-end harness test runs.

Best: Codex 0.163.0 completed 15 native fresh-context reviewers in order. 2 live tests passed in 573.13s.

Worst: the Claude Cowork run stopped after stages 5 to 7 on a usage limit. Issue #237 reports AGENTS.md leaking into Codex reviewers.

Bottom line: best thing, forced independent review before code. Worst thing, heavy token use and unverified isolation on some hosts.

What is Google&#8217;s Elephant-Goldfish Model plugin?

EGM is an Apache 2.0 plugin of skills, reviewer personas and document standards. It is not a new language model. The method comes from Dave Rensin&#8217;s essay on elephants and goldfish. The Google Open Source blog frames it as a fix for AI &#8220;slop&#8221; and session context collapse. The README states it is not an officially supported Google product.

How does the Elephant-Goldfish workflow work?

The Elephant is a long session holding project context and earlier decisions. It drafts the spec and writes no code. Each Goldfish is a stateless subagent. It reads only the draft and the files it references. You resolve trade-offs and approve the design.

The core loop has 3 commands:

/egm-brainstorm clarifies the idea, then runs a 6-lens Goldfish swarm. Lenses cover YAGNI, token cost, UX, migration, observability and tech debt. Output: concepts_brief.md.

/egm-draft turns the brief into a design doc under docs/designs/, section by section.

/egm-review runs the Goldfish review.

/egm-drift-report later compares code with the spec. The docs recommend running it weekly.

What happens in the 5-stage Goldfish review?

The review skill runs 5 sequential stages:

Initial Zoom Out: checks the whole document at a high level.

Comprehension Test: a Goldfish paraphrases the design. A wrong paraphrase means the doc is ambiguous.

Critic Review: design, structural and style reviewers hunt gaps and edge cases.

Intermediate Zoom Out: rechecks architecture after fixes.

Implementation Readiness: checks file paths, data structures and signatures.

Each stage allows at most 1 re-audit. Findings are ranked Blocker, Major or Nit. If a host has no subagent tool, EGM stops. A same-context review is not a Goldfish review.

&&

Which coding agents does EGM support?

Launch coverage described Antigravity-only support, with more coming. The current harness guide covers Antigravity CLI and App, Claude Code, Claude Cowork, Codex, ChatGPT, omp and Muse. Antigravity CLI, Claude Code and Codex pass automated end-to-end fixtures.

Claude Code needs version 2.1.271 or later. Reviewers there get only Read, Grep and Glob tools. CLAUDE.md files are excluded from their context.

The test record gives concrete run data:

Antigravity CLI 1.4.5: 16 native reviewers ran, stages in order.

Codex 0.163.0: 15 native reviewers, 2 live tests in 573.13s.

Codex CLI with the v0.1.0 ZIP: full suite passed in 482.30s.

How does EGM compare with Spec Kit, Kiro and Superpowers?

FeatureGoogle EGMGitHub Spec KitKiro SpecsSuperpowersTypePlugin (skills + personas)Toolkit + Specify CLIFeature of an agentic IDE/CLI/webSkills pluginLicenseApache 2.0MITCommercial (pricing)MITWorkflowBrainstorm, draft, review, drift reportConstitution, specify, plan, tasks, implement, convergeRequirements, design, tasksBrainstorm, plan, subagent build, TDD, reviewSpec reviewed by fresh-context subagentsYes, 5 stages before codeNot disclosedNot disclosed (Analyze Requirements pass)No; fresh subagents review code per taskHarnessAntigravity, Claude Code, Codex, ChatGPT, moreCopilot and other agentsKiro only16 harnesses listedSetupPlugin installPython 3.11+, uvKiro accountPlugin installCostFree plugin; host model usageFree toolkit; host model usageSubscriptionFree plugin; host model usage

EGM&#8217;s distinct move is reviewing the spec with zero-context agents. Spec Kit and Kiro center on human review between phases. Superpowers isolates subagents mainly at implementation time.

Key Takeaways

EGM is a plugin, not a model: Elephant drafts, Goldfish reviews.

Specs get 5 zero-context review stages before any code.

Works across Antigravity, Claude Code, Codex and ChatGPT.

Codex test runs completed 15 fresh-context reviewers end to end.

Reviewer isolation still leaks host instruction files on some CLIs.

Check out the GitHub repo, the project site and the Google Open Source blog post. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google AI Releases Elephant-Goldfish Model Plugin for Spec-First Coding appeared first on MarkTechPost.