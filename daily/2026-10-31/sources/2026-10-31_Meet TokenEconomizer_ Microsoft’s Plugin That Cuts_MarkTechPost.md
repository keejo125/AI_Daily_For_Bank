---
publish_time: 1793382817
link: https://www.marktechpost.com/2026/10/30/microsoft-tokeneconomizer-coding-agent-cost-control/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  微软研究院与 UC Berkeley 联合开源 TokenEconomizer，一款面向编程 Agent 的成本控制器，可作为插件接入 Claude Code、Codex、GitHub Copilot CLI 与 Pi，不改动模型权重或 Agent 代码。它从历史会话中学习，削减后续会话的浪费。在 277 项 SWE-Bench 任务上，5 种 Agent-模型组合的平均成本下降 18.4%–30.9%。研究指出浪费主要来自重复探索、长期加载却从未调用的工具 schema，以及失败重试循环。
---

# 微软 TokenEconomizer：削减编程智能体 Token 成本的插件

> 原文链接：https://www.marktechpost.com/2026/10/30/microsoft-tokeneconomizer-coding-agent-cost-control/
> 来源：MarkTechPost

A team of researchers from Microsoft Research and UC Berkeley have released TokenEconomizer, an open-source cost controller for coding agents. TokenEconomizer is a plugin that learns from past sessions in a repository to cut waste in later ones. It works with Claude Code, Codex, GitHub Copilot CLI and Pi. It does not touch model weights or agent code. On 277 SWE-Bench tasks, it lowered mean cost by 18.4% to 30.9% across 5 agent-model settings.

TL;DR

Package: A standard-library Python package and agent plugins, with 3 switchable mechanisms.

Runs on: Any machine running Claude Code, Codex, Copilot CLI or Pi with Python 3.10+. No GPU and no API key of its own.

Performance: 18.4% to 30.9% lower mean SWE-Bench cost, and cheaper in all 30 repository-setting cells.

Best: 30.9% lower cost on Claude Code with Opus 4.8 (33.2% when combined with RTK).

Worst: Only 6.4% to 9.3% savings on ReposVul audits; Pass@1 drops 1.0 point on Opus 4.8.

Why do coding agents waste tokens?

Every agent turn re-bills the system prompt, every loaded tool schema and the full history. The research team profiled 60 SWE-Bench tasks across 6 repositories using Claude Code with Opus 4.8. They found 3 recurring sources of waste:

Repeated discovery: once 5 tasks precede the current one, 30% of tool calls repeat an earlier action.

Unused tools: 23 tool schemas load every turn. 16 are never called, and 3 cover 98% of calls.

Failure loops: 10 failed runs were 17% of tasks but 32% of total spend.

They also tested 3 fixed open-source strategies: RTK, Serena and Aider&#8217;s RepoMap. None was cheaper everywhere. All 3 cut cost on Django and raised it on SymPy.

How does TokenEconomizer work?

TokenEconomizer is an external controller that treats the agent as a black box. It keeps a state per repository, built from completed traces. Before each task, it sets 3 policies through the prompt, the tool settings and the event stream.

1. Micro-skills

An LLM proposer turns trace digests into 1-line facts, such as the working test command. Each fact carries regex detectors that check later traces without a model call. A fact enters the prompt after 3 confirmations on tasks with non-overlapping edited files. Its need rate must also stay at or above 0.4. One contradiction counts as 5 confirmations, so wrong facts retire quickly.

2. Tool pruning

Shell, read, write and edit tools are always kept. Other tools are masked after 3 consecutive unused tasks, or when an LLM judge marks them irrelevant. The full catalog returns every 5 tasks for a re-audit. On Django with Claude Code, the first request on task 2 fell from 43,351 to 16,295 prompt tokens.

3. Failure-loop intervention

The controller learns a turn budget: 1.25 times the 90th percentile of successful run lengths. Cheap rule checks flag repeated failures or dense errors. An LLM judge then decides if the agent is stuck, at 0.7 confidence or higher. A stuck agent gets 1 redirect, then a stop if the loop recurs.

&&

What do the SWE-Bench results show?

SettingCost vs defaultPass@1 defaultPass@1 TokenEconomizerClaude Code + Sonnet 5-23.6%74.776.0Claude Code + Opus 4.8-30.9%74.073.0Codex + GPT-5.6 Terra-24.7%73.874.7Codex + GPT-5.6 Sol-26.1%80.181.7Copilot CLI + Sonnet 5-18.4%75.077.6

Source: arXiv 2610.22732, Table 1. Costs include all controller calls. 3 seeds per setting.

Pass@1 improved in 4 of 5 settings. Lower reasoning effort saved cost but cut Pass@1 by 1.8 to 10.3 points. RTK alone raised cost in 12 of 30 repository-setting cells, and RepoMap in 15.

Savings build over time. Most repositories cost more at first, but all were cheaper by the sixth task. Alone on Claude Code, tool pruning saved 13.2% to 17.7%, micro-skills 11.8% to 14.3%, and the loop guard 5.4% to 7.1%.

Results also held outside SWE-Bench. Costs fell 16.0% to 21.2% on Web-Bench and 16.5% to 19.6% on CredData. ReposVul saw only 6.4% to 9.3%, because shorter runs leave less to remove.

How does it compare with other token-saving tools?

FeatureTokenEconomizerRTKSerenaAider RepoMapApproachLearns per-repository policies from past sessionsCompresses shell command outputMCP server with symbol-level code toolsRanked map of repository symbols in the promptLearns from earlier tasksYesNoNoNoLicenseApache 2.0Apache 2.0 CLI; BUSL-1.1 engineGPL-3.0-or-later (MIT for SolidLSP)Apache 2.0AgentsClaude Code, Codex, Copilot CLI, Pi18 AI coding toolsAny MCP clientAiderMean SWE-Bench cost change (paper, 5 settings)-18.4% to -30.9%-8.9% to +4.5%Not in main runs (raised pooled cost in profiling)-6.1% to +6.5%Cells with higher cost (of 30)012Not disclosed15

Cost rows: TokenEconomizer paper. Licenses and claims: each project&#8217;s repository or docs.

How do you install TokenEconomizer?

The plugin needs one of the 4 agents and Python 3.10 or newer. On Claude Code, clone the repo, add it as a marketplace, then run claude plugin install tokeneconomizer@tokeneconomizer. Learned data stays local in ~/.tokeneconomizer. Tool pruning and the loop guard are on by default. Micro-skills are off by default, because the proposer adds model calls.

Key Takeaways

TokenEconomizer cuts SWE-Bench cost 18.4% to 30.9% with an unchanged agent.

It was cheaper in all 30 repository-setting cells; RTK and RepoMap were not.

Tool pruning is the biggest single lever, at 13.2% to 17.7%.

Pass@1 rose in 4 of 5 settings and fell 1.0 point on Opus 4.8.

It is Apache 2.0 and installs on Claude Code, Codex, Copilot CLI and Pi.

Check out the Paper, GitHub Repo and Project Page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet TokenEconomizer: Microsoft’s Plugin That Cuts Coding Agent Costs by Up to 30.9% appeared first on MarkTechPost.