---
publish_time: 1785577969
status: pending
---

# Supabase Releases Evals: an Open Source Benchmark That Scores Claude Code, Codex and OpenCode on Real Supabase Tasks

> 原文链接：https://www.marktechpost.com/2026/08/01/supabase-releases-evals-an-open-source-benchmark-that-scores-claude-code-codex-and-opencode-on-real-supabase-tasks/
> 来源：MarkTechPost

Supabase has open sourced Supabase Evals, its benchmark and framework for testing how well AI agents build using Supabase. It runs coding agents including Claude Code, Codex, and OpenCode against real tasks, such as building a schema, debugging a failed Edge Function, or fixing a broken RLS policy, then scores the result. It powers the public leaderboard at supabase.com/evals and an internal regression suite monitored daily.

Is it deployable?

Yes, today. supabase/evals is public under Apache-2.0 and runs locally via pnpm.

Industries: Developer tooling, cloud infrastructure, data platforms, and regulated backends in fintech or healthcare, where an agent writing a wrong RLS policy is a security incident.

Applications: Regression-testing docs and skill edits, gating SDK releases, and comparing agent harnesses head to head.

Constraints: Local-stack runs need a Docker daemon, provider API keys, and ports 54321–54329 free.

How the harness works

Supabase defined three dimensions: products (database, auth, storage, edge-functions, realtime, cron, queues, vectors, data-api), topics (RLS, security, migrations, SQL, SDK, observability, self-hosting, tests, declarative-schema), and stages (build, deploy, investigate, resolve). It then picked the smallest scenario set touching each dimension once, grounded in support tickets, bug reports, and GitHub issues.

Scenarios split into two suites. Benchmark scenarios cover breadth and are published. Regression scenarios cover known failure modes, refresh daily, and do not move published scores.

Every scenario runs against a real environment. The framework boots a hosted-like stack and a local CLI project in containers, so agents call the actual MCP server and CLI. A platform-lite runtime exposes a Management API-compatible surface backed by @supabase/lite. Scoring combines deterministic checks with LLM-as-a-judge. Agents get one retry before grading.

Each eval directory holds PROMPT.md (task plus frontmatter), EVAL.ts (the scorer), and optional remote/ and local/ starting states. Shipping a local/ workspace, or declaring interface: cli, boots a Docker sandbox with the real CLI installed.

Findings

Agents pass most scenarios with no skill loaded. In the Build stage, Opus 5 and Kimi K3 both scored 100% unaided. Skills closed the rest of the gap: Sonnet 5 rose from 78% to 100%, GPT-5.6 Sol from 89% to 100%, and GPT-5.4 mini from 78% to 89%.

Three weaknesses surfaced. Agents hand-write migrations instead of using declarative schemas, prompting a skill guidance update. Agents verify auth by hand rather than reaching for @supabase/server, prompting a package selection guide. And docs usage varies sharply: Codex / GPT-5.6 reads roughly 8 docs pages per scenario versus about 2 for Claude Code, which checks docs in under 40% of scenarios even with skills loaded.

Key Takeaways

Supabase open sourced supabase/evals under Apache-2.0.

Scenarios run against real containerized Supabase stacks, not mocks.

Scoring mixes deterministic checks with LLM-as-a-judge; one retry allowed.

Skills mattered least for top models, most for smaller ones.

Check out the Technical details and GitHub Repo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Supabase Releases Evals: an Open Source Benchmark That Scores Claude Code, Codex and OpenCode on Real Supabase Tasks appeared first on MarkTechPost.