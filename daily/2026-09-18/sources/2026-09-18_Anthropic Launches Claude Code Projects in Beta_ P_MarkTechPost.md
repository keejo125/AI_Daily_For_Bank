---
publish_time: 1789677904
link: https://www.marktechpost.com/2026/09/17/anthropic-launches-claude-code-projects-in-beta-parallel-cloud-sessions-that-keep-running-after-you-close-your-laptop/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Anthropic 重构了 Claude Code 的 Projects 功能：旧版是一个文件夹（文件+单次对话），新版是单一持续对话，由 Claude 担任协调器（Coordinator），开发者下达目标后自动拆解为并行工作线程，每个线程运行在独立云端会话与独立代码分支上，关掉笔记本后仍持续运行并向主对话汇报。Anthropic 称之为“自我分裂为并行云端会话”的单一对话。
---

# Anthropic 推出 Claude Code Projects 测试版：关掉笔记本仍在云端并行运行

> 原文链接：https://www.marktechpost.com/2026/09/17/anthropic-launches-claude-code-projects-in-beta-parallel-cloud-sessions-that-keep-running-after-you-close-your-laptop/
> 来源：MarkTechPost

Anthropic redesigned Projects in Claude Code. The old project was a folder: some files plus one chat. The new one is a single ongoing conversation where Claude acts as coordinator. You describe work, and Claude decides what becomes a thread. Each thread is a full Claude Code cloud session running on its own branch and its own copy of the repository. Threads run in parallel, report back to the conversation, and keep going after you close your laptop. Anthropic&#8217;s launch post calls it one conversation that splits itself into parallel cloud sessions.

Coordinator and threads

The architecture has two layers. The project conversation is the coordinator. It reads what you send, answers quick questions in place, and starts threads for actual work. It sees what threads report back, not every step they take. Threads are the workers. A thread opens a pull request when the work calls for one, then watches that pull request with auto-fix enabled. It pushes fixes when CI fails and replies when checks pass.

Threads delegate too. Each can split its assignment further using subagents, loops and workflows.

Anthropic&#8217;s own example: set a goal to reduce checkout p75 latency, then ask Claude to profile each endpoint, test optimizations and open pull requests in parallel threads. A second example retires a deprecated v1 endpoint across API, web and mobile repositories, one thread each, with Claude reporting which pull requests merge first.

When two threads touch the same code, the overlap surfaces as an ordinary git merge conflict.

Interactive: how a Claude Code project routes workClick a task. Watch the coordinator answer in place, save memory, or open a cloud thread on its own branch.

Modeled on Anthropic&#8217;s Claude Code projects documentation. Thread timings are illustrative. &copy; Marktechpost

&

What every thread inherits

Standing context is set once and reaches each new thread: the project's repositories and uploaded files, its project instructions of up to 16,000 characters, and project memory that Claude writes and reads through a MEMORY.md index. Memory in practice: the release moved to Friday, or who to check with before touching billing.

Each thread also clones every project repository and loads CLAUDE.md, skills and plugins from all of them. Permission rules, hooks and env behave differently. They apply only from the directory the thread starts in, so a single repository project honors them and a multi repository project does not. MCP tools arrive through the connectors on your claude.ai account. The project conversation itself has no connectors, so connector work must go to a thread.

The Overview pane groups threads by state: Ready for review, Waiting on you, Working, Landing, Idle and Resolved. A Library tab collects uploaded files and files the threads produced.

What it costs

A project uses plan limits faster than a single session, because every running thread is a full session. Anthropic exposes a per project Usage tab plus separate model and effort settings for the coordinator and for threads. A new project runs Opus everywhere, high effort for threads and low effort for the conversation. Idle threads also wake and spend again when CI fails or a review comment lands. The enforced ceiling is 200 new threads per day across your projects, and a thread that hits a usage limit waits and resumes on its own.

Key Takeaways

One project is one conversation, and Claude starts a thread per piece of work.

Every thread is a full cloud session with its own branch and repository copy.

Shared project memory and instructions reach every new thread automatically.

Parallel threads burn plan limits faster, with a cap of 200 new threads per day.

Beta is limited to select Pro and Max users on web and desktop, not the CLI.

Check out the Anthropic announcement, Claude Code projects documentation and @ClaudeDevs launch post. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Anthropic Launches Claude Code Projects in Beta: Parallel Cloud Sessions That Keep Running After You Close Your Laptop appeared first on MarkTechPost.