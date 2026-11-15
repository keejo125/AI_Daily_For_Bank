---
publish_time: 1789160755
link: https://www.marktechpost.com/2026/09/11/anthropic-adds-plugin-evals-to-claude-code-6-grader-types-a-no-plugin-baseline-and-a-ci-gate-for-skills/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Anthropic 为 Claude Code 发布 plugin eval 评测工作流。claude plugin eval 命令针对真实 prompt 运行插件、对 Claude 产出评分，并与未加载插件的运行对比，回答插件开发者此前无法衡量的三个问题：skill 是否触发、能否在编辑或新模型下存活、是否优于裸模型。支持 Claude Code v2.1.269+，每项评测为真实模型调用，并内置 CI 门禁，便于在技能开发流水线中持续验证插件质量。
---

# Anthropic 为 Claude Code 新增插件评测：6类评分器与CI门禁

> 原文链接：https://www.marktechpost.com/2026/09/11/anthropic-adds-plugin-evals-to-claude-code-6-grader-types-a-no-plugin-baseline-and-a-ci-gate-for-skills/
> 来源：MarkTechPost

Anthropic has published a new plugin evals workflow for Claude Code. The claude plugin eval command runs a plugin against realistic prompts, grades what Claude produced, and compares the result with a run where the plugin is not loaded. It answers 3 questions plugin developers could not previously measure: does the skill trigger, does it survive an edit or a new model, and does it beat a bare model.

Deployable: Yes. It runs on Claude Code v2.1.269 or later against any directory with a plugin.json or .claude-plugin/plugin.json manifest, or a skills-directory plugin. Every eval run and judge grader is a real model call billed to your plan or API account.

What a case looks like

An eval suite lives in an evals/ directory inside the plugin. Each case is a subdirectory holding a prompt.md and a graders/ folder. The prompt body goes to Claude exactly as written, and @path mentions are not expanded. Frontmatter on prompt.md can set max_turns (default 10), timeout_seconds (default 300), model, tags, and allowed_tools.

Graders are markdown files whose frontmatter sets a type, an optional weight, and an optional arm. There are 6 types. Four cost nothing because they are computed from the transcript and the files on disk: regex, tool_used, tool_order, and file_exists. Two call a judge model and add to the bill: llm, which scores the reply against prose criteria you write, and baseline, which compares it against a reference answer.

claude plugin eval init reads the plugin, asks what a good result looks like, proposes cases and graders, tries them, and writes the files. In CI, --bare <name> writes a blank template instead.

The number that matters is Δ

By default every case runs twice: a with-arm where the plugin is loaded and a without-arm where it is not. Their difference, Δ, is what the plugin contributed. If a case scores 1.0 in both arms, the plugin is not why it passed. The docs example output shows a single case at WITH 1.00, W/OUT 0.33, Δ +0.67 across 6 runs, costing an estimated $0.41 and taking 74 seconds. A grader marked with-only, typically tool_used: Skill, is reported as an indicator and excluded from the score, since the without-arm has no skill to fire.

Anthropic calls out the most common first finding: a Δ near zero with the tool_used: Skill grader failing, which means Claude is not choosing the skill on natural phrasing. That is the defect claude plugin validate cannot see, because it checks manifest syntax and schema rather than behavior.

Results land under evals/results/<timestamp>/report.html with per-grader verdicts and judge votes. Where the account supports it, the report is also published to claude.ai unless --no-publish is set.

Cost and CI

A suite makes roughly cases × runs × arms agent runs, plus 3 short judge calls per llm or baseline grader per run, and results vary between runs. The documented CI invocation is:

Copy CodeCopiedUse a different Browser

claude plugin eval . \
  --trust-plugin \
  --json results.json \
  --threshold 0.8 \
  --model claude-sonnet-5 \
  --judge-model claude-haiku-4-5 \
  --no-publish \
  --max-cost-usd 20

The runner needs a Claude Code install and credentials such as ANTHROPIC_API_KEY. Without --trust-plugin, an untrusted checkout is refused with exit 1 when there is no terminal. Report problems never change the exit code, and --json suppresses progress output.

Interactive explainer

&&

Key Takeaways

claude plugin eval scores realistic prompts with 6 grader types; 4 are free, llm and baseline bill a judge model.

Every case runs with and without the plugin by default; Δ is the only number that proves the plugin did the work.

A Δ near zero with a failing tool_used: Skill grader means the skill never triggers on natural phrasing.

--threshold, --max-cost-usd, and --trust-plugin turn it into a CI gate; usage-limit errors can fake a regression.

Requires Claude Code v2.1.269+; claude plugin eval init writes the first suite for you.

Check out the Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Anthropic Adds Plugin Evals to Claude Code: 6 Grader Types, a No-Plugin Baseline, and a CI Gate for Skills appeared first on MarkTechPost.