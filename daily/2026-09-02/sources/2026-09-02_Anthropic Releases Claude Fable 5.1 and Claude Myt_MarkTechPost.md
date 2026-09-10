---
publish_time: 1788294621
link: https://www.marktechpost.com/2026/09/01/anthropic-releases-claude-fable-5-1-and-claude-mythos-5-1-52-6-on-terminal-bench-science-and-75-cheaper-cache-reads/
source: Anthropic
status: confirmed
category: 国际
is_model_related: true
digest: |
  Anthropic 发布 Claude Fable 5.1 与 Claude Mythos 5.1，两者基于同一底层模型，区别在安全等级：Fable 5.1 面向公众与企业开放，Mythos 5.1 仅经审核的网络安全和生命科学机构可访问。Fable 5.1 在智能体科学研究基准 Terminal-Bench-Science 0.1 达 52.6%（前代 Fable 5 为 24.7%、GPT-5.6 Sol 为 22.4%），并在编程、知识工作、长任务全面升级；缓存读取降价 75% 至每百万 token 0.25 美元，典型负载成本降约 25%、高智能体负载降约 45%。其安全护栏误判更少，并引入反蒸馏机制。
---

# Anthropic 发布 Claude Fable 5.1 与 Mythos 5.1：Terminal-Bench-Science 达 52.6%、缓存读取降价 75%

> 原文链接：https://www.marktechpost.com/2026/09/01/anthropic-releases-claude-fable-5-1-and-claude-mythos-5-1-52-6-on-terminal-bench-science-and-75-cheaper-cache-reads/
> 来源：MarkTechPost

Anthropic has released Claude Fable 5.1 and Claude Mythos 5.1, three months after the Fable 5 line shipped in June 2026. The two are the same underlying model behind different safeguard layers. Fable 5.1 is generally available as claude-fable-5-1; Mythos 5.1 stays restricted to vetted organizations. Both carry a 1M token context window and 128K max output tokens, with adaptive thinking always on. The headline capability number is 52.6% on Terminal-Bench-Science 0.1, against 24.7% for Fable 5 and 29.0% for Opus 5. The headline commercial number is a 75% cut to cache reads, from $1.00 to $0.25 per million tokens, which Anthropic measures as roughly 25% lower cost on typical workloads and up to 45% on agentic ones. Base input and output pricing is unchanged at $10 and $50 per million.

Is it deployable?

Yes, Claude Fable 5.1 is generally available as claude-fable-5-1 on the Claude API, Amazon Bedrock, Claude Platform on AWS, Google Cloud, and Microsoft Foundry. Claude Mythos 5.1 is not: it is restricted to vetted US organizations inside Project Glasswing.

The benchmark numbers

On Terminal-Bench-Science 0.1, an agentic scientific research benchmark, Fable 5.1 scores 52.6% against 29.0% for Opus 5, 24.7% for Fable 5, and 22.4% for GPT-5.6 Sol. Anthropic reports a standard error of 3.5 to 4.5 points per model, so treat the margin, not the ranking, with care.

On Terminal-Bench 4.0, Fable 5.1 reaches 55.8% and Mythos 5.1 reaches 60.9%. The gap between two identical models is the cost of safeguard interventions, which is an unusually honest disclosure. Elsewhere: CursorBench 3.2.0 at 73.4%, Humanity&#8217;s Last Exam at 60.9% without tools and 65.0% with tools, AutomationBench at 31.4%, OSWorld 2.0 at 41.7% strict, and GDPval-AA v2 at 1853.

Where the cost cut comes from

Base input and output pricing is unchanged. Cache reads drop 75%, from $1.00 to $0.25 per million tokens, which is 0.025 times base input against 0.1 on every other Claude model. Anthropic measures roughly 25% lower cost on typical workloads and up to about 45% on context-heavy agentic ones. Batch processing is $5 and $25 per million tokens.

Three breaking changes teams will hit

Forced tool use is gone: tool_choice set to any or tool returns a 400. Use auto with strict tool use or structured outputs instead.

Thinking blocks are model-bound: Fable 5.1 reads earlier models&#8217; thinking, but no earlier model reads its own. Router and fallback setups lose reasoning when they switch down.

Editing earlier turns invalidates thinking blocks: Injecting and deleting per-turn reminders, or rebuilding the system or tools array mid-conversation, now errors. The check is enforced for accounts created on or after August 31, 2026. The fixes are turn-scoped system messages and server-side context editing.

Additive changes: per-message effort, turn-scoped system messages, and thinking.display: "updates" are all in beta behind headers. Content provenance is not optional, with a statistical text watermark on all output and C2PA credentials on files.

Anthropic also documents real regressions. Parallel tool calling is more variable, so agent loops may issue one call per turn where Fable 5 batched several. The model narrates less, answers from memory more often at low effort, and prefers whole-file rewrites over targeted edits.

Safeguards and science

Cyber safeguards now permit vulnerability discovery but not exploit development, cutting interventions in Claude Code by roughly 60% per session. Biology safeguards fire 85% less often on benign requests. Penetration testing, exploit generation, and binary-based vulnerability scanning still redirect to Opus.

On research, Mythos 5.1 designed protein binders with roughly 50% hit rate across 12 targets against a 10 to 15% norm, Fable 5.1 built a Venus elevation map at 2 to 3 km resolution, and custom GPU kernels sped up seven open-source genomics models by up to 2.5x.

Key Takeaways

Fable 5.1 and Mythos 5.1 are one model behind two safeguard layers; only Fable is generally available.

52.6% on Terminal-Bench-Science 0.1, roughly double Fable 5&#8217;s 24.7%.

Cache reads fall 75% to $0.25 per million; base rates are untouched.

Three breaking API changes hit any agent that edits conversation history.

30-day retention applies; zero data retention needs express authorization.

Check out the Technical Details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Anthropic Releases Claude Fable 5.1 and Claude Mythos 5.1: 52.6% on Terminal-Bench-Science and 75% Cheaper Cache Reads appeared first on MarkTechPost.