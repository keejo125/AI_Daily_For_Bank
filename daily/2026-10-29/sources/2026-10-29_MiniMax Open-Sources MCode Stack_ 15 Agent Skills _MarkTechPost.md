---
publish_time: 1793208029
link: https://www.marktechpost.com/2026/10/28/minimax-open-sources-mcode-stack-agent-skills/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  MiniMax开源其内部MiniMax Code团队日常使用的MCode Stack（MIT许可）：17个技能、5个检查清单与笔记，直接安装进MiniMax Code或Claude Code，将harness工程习惯转为可运行步骤。涵盖subagents、工具上下文、压缩与记忆、长bash命令审计等，其中long-command-check为10点长命令与后台任务审计清单。
---

# MiniMax 开源 MCode Stack：AI 编程日常使用的 15 个 Agent 技能

> 原文链接：https://www.marktechpost.com/2026/10/28/minimax-open-sources-mcode-stack-agent-skills/
> 来源：MarkTechPost

MiniMax has open-sourced MCode Stack, the workflows and agent skills its team uses to build MiniMax Code. The MiniMax MCode Stack agent skills went public on October 28, 2026 under the MIT license. It is not a prompt collection. Each piece is a SKILL.md skill or checklist that installs directly into MiniMax Code. For developers, it turns harness engineering habits into steps an agent can actually run.

TL;DR

Size: 2 stacks, 17 skills (15 from Ronny, 2 from Jiachen), 5 checklists, 5 companion notes.

Runs on: Any machine running MiniMax Code (Node.js 22.19+) or Claude Code. No GPU. Skills are plain Markdown.

Performance: No benchmarks or eval results published.

Best: long-command-check, a 10-point audit for long shell commands and background tasks.

We just open-sourced MCode Stack: the actual workflows and skills the MiniMax Code team uses every day to build MiniMax Code. https://t.co/vREt7i8m2M
&mdash; RonnyHe (@Ronny_MiniMax) October 28, 2026

What is MiniMax MCode Stack?

MCode Stack is an open-source repo of agent skills from MiniMax&#8217;s MiniMax Code team. MiniMax Code is the MiniMax&#8217;s open-source terminal coding agent, also MIT-licensed. The stack holds no MiniMax Code source code. It holds only workflows, skills and checklists.

The repo pairs with a column called MCode Engineering Notes. Each note explains one idea. The repo makes that idea runnable. Published notes cover subagents, tool context, compaction versus memory and long bash commands. A note on per-turn context tax is marked upcoming.

What skills are inside Ronny&#8217;s stack?

MiniMax&#8217;s stack ships 15 skills, grouped by moment in the working day:

Plan and split (3): subagent-split-check, engineering-small-prs, engineering-change-descriptions.

Context and tools (2): tool-budget-audit, context-tax-audit.

Long sessions and commands (3): long-session-check, handoff-doc, long-command-check.

Review (4): independent-review, engineering-code-review, engineering-review-comments, engineering-review-feedback.

Experiments and hotfixes (3): harness-experiment, trajectory-review, engineering-emergency-changes.

A few ideas stand out. independent-review gives the reviewer exactly 3 inputs: the diff, the requirement and test results. It deliberately withholds the author&#8217;s conversation. The reasoning: a reviewer inheriting the author&#8217;s context repeats the author&#8217;s blind spots.

subagent-split-check says to split work only when context is the measured problem. Splitting by team or question type is not a valid reason.

tool-budget-audit separates 2 costs: tool definitions and tool results. Tool search mainly cuts the first. Programmatic tool calling mainly cuts the second.

harness-experiment enforces 1 change per experiment. It tracks flipped tasks, requests per task, tokens, cache hit rate and wall-clock time.

The long-command checklist has 10 items. It asks whether moving a command to background re-runs the process. It also asks whether unread results survive compaction.

The 6 engineering-* skills are adapted from Google Engineering Practices. That material stays under CC-BY 3.0, per the stack&#8217;s NOTICE.

&&

How do you install MCode Stack?

There are 3 paths, per the README:

One skill: clone the repo and copy a skill folder into ~/.agents/skills/.

Whole stack as a local plugin: copy stacks/ronny into MiniMax Code&#8217;s local plugin directory.

Marketplace: in MiniMax Code desktop, add the MiniMax-AI/mcode-stack marketplace. This option is rolling out gradually.

The same catalog works in Claude Code with /plugin marketplace add MiniMax-AI/mcode-stack. MiniMax Code also reads ~/.claude/skills/ and ~/.codex/skills/. The skills use the common SKILL.md format, so most work in other agents that support skills.

How does MCode Stack compare with other skill packs?

FeatureMiniMax MCode Stackanthropics/skillsobra/superpowersPublisherMiniMax Code teamAnthropicJesse Vincent (obra), Prime Radiant LicenseMIT; engineering-* skills CC-BY 3.0Apache 2.0 for many skills; document skills source-availableMITSkill count17 (15 + 2)Not disclosed15 listed in READMEFocusHarness engineering, review, context budgets, long sessionsCreative, development, enterprise, documentsBrainstorming, planning, TDD, subagent-driven development, debuggingAgents namedMiniMax Code, Claude CodeClaude Code, Claude.ai, Claude API16 harnesses, incl. Claude Code, Codex, Cursor, Gemini CLIClaude Code install/plugin marketplace add MiniMax-AI/mcode-stack/plugin marketplace add anthropics/skills/plugin install superpowers@claude-plugins-officialPublished evalsNot disclosedNot disclosedNot disclosed

MCode Stack is narrower than both. It targets people who design agent harnesses, not only people who use agents. Superpowers covers far more harnesses today.

Key Takeaways

MiniMax open-sourced 17 SKILL.md skills and 5 checklists under MIT.

Skills pair with MCode Engineering Notes, turning essays into runnable checks.

independent-review feeds a reviewer only the diff, requirement and test results.

Installs into MiniMax Code or Claude Code via a plugin marketplace.

No published evals yet, so treat it as a playbook, not proof.

Check out the GitHub repo and MiniMax Code. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post MiniMax Open-Sources MCode Stack: 15 Agent Skills Its Coding Team Uses Daily appeared first on MarkTechPost.