---
publish_time: 1790103575
link: https://www.marktechpost.com/2026/09/22/anthropic-claude-opus-5-5-release/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Anthropic 发布 Claude 5.5 系列首款模型 Claude Opus 5.5，官方称其在多数任务上达到 Claude Fable 5.1 水平，典型任务运行成本较 Opus 5 降低约 40%、输出速度提升超 30%。在智能体编程、计算机操作与知识工作基准上领先，通过托管 API 提供、未开源权重，已上线 Claude 及 AWS、Google Cloud、Azure 等平台。
---

# Anthropic 发布 Claude Opus 5.5：运行成本较 Opus 5 降低 40%

> 原文链接：https://www.marktechpost.com/2026/09/22/anthropic-claude-opus-5-5-release/
> 来源：MarkTechPost

Anthropic has released Claude Opus 5.5, the first model in its new Claude 5.5 family. The team states it performs at the level of Claude Fable 5.1 on most work. It also costs 40% less to run than Opus 5 on typical workloads at default settings. On Anthropic&#8217;s own benchmarks, it leads in agentic coding, computer use, and knowledge work. 

Is it deployable? Yes, as a managed API model. Anthropic has not released weights, so self-hosting is not an option. Developers can call claude-opus-5-5 on the Claude Platform, Amazon Web Services, Google Cloud, and Microsoft Azure. Zero data retention is available, as with previous Opus models.

Benchmarks: Strong Lead, Not a Clean Sweep

Opus 5.5 scores use adaptive thinking at max effort, with production safeguards enabled.

BenchmarkOpus 5.5Fable 5.1Opus 5GPT-6 AstraTerminal-Bench 4.066.4%55.8%52.3%57.9%FrontierCode v1.154.4%50.3%48.0%53.3%CursorBench 4.057.8%51.8%46.6%n/rGDPval-AA v2.1 (Elo)1846173517081542OSWorld 2.081.8%80.7%74.0%n/rTerminal-Bench-Science 0.158.7%52.6%29.0%64.6%AutomationBench40.0%31.4%26.9%41.4%

Terminal-Bench 4.0 is reported at xhigh effort for Opus 5.5. GPT-6 Astra still leads on Terminal-Bench-Science and AutomationBench. Zapier ran AutomationBench without fallback models, so safeguard interventions counted as failures. Anthropic also cautions that benchmark margins are becoming a less reliable guide. In its own use, the gap to Fable 5.1 is narrower than the scores suggest.

The cost-adjusted results are more telling. At default (medium) effort, Opus 5.5 scores 54.6% on FrontierCode. That beats GPT-6 Astra&#8217;s top score of 53.3% at about a fifth of the cost per task. On CursorBench, medium effort scores 52.5%. That is 11 points above GPT-5.6 Sol&#8217;s best, at about a third of the cost.

Pricing and Speed

Opus 5.5 needs less compute to serve than Opus 5, and pricing reflects that.

Per 1M tokensOpus 5.5Opus 5Input$4$5Output$20$25Cache reads$0.20$0.50Cache writes$5$6.25

Cache reads make up most agentic and coding costs, and they drop 60%. Opus 5.5 also uses fewer tokens per task. Together, that nets out to the 40% cost reduction. Output generation is more than 30% faster than Opus 5. Fast mode in Claude Code and the Claude Platform offers up to 2.5x speed at $8 input and $40 output per million tokens.

Anthropic is also raising five-hour usage limits on Pro, Max, Team, and seat-based Enterprise plans. Subscribers get a rate limit reset they can save and use later.

What Early Testers Reported

One tester completed a 680,000-line code migration in less than a day.

Another audited and fixed a 200,000-line codebase in under 3 hours. Opus 5 took over 20 hours and 2.5x the tokens.

In an internal C to Rust port of HAProxy, Opus 5.5 finished in 9.5 hours. Fable 5.1 took 12 hours, and Opus 5.5 cost 51% less.

Deloitte says Opus 5.5 at lowest effort caught 72% of known review bugs. Opus 5 at high effort caught 56%.

In a hard-to-source earnings report test, 16 of 18 Opus 5.5 reports cleared Anthropic&#8217;s quality bar. Fable 5.1 and Opus 5 never did.

Writing style also changed. Opus 5.5 puts key information first, uses less jargon, and follows the writing rules you give it.

Safety, Safeguards, and API Changes

Opus 5.5 is Anthropic&#8217;s first release since CEO Dario Amodei called for pacing the frontier. External evaluators including METR and Frontier Design tested it before release. It posts the best score to date on Anthropic&#8217;s automated behavioral audit, which covers nearly 2,000 scenarios. In a new containment test, it tried to circumvent boundaries about 85% less often than Opus 5. Anthropic also notes the model often suspects it is being evaluated.

Its biology and cyber capabilities are comparable to Claude Mythos 5.1. So Opus 5.5 ships with safeguards similar to Fable 5.1:

Cybersecurity: Routine bug finding and fixing works. Most other cybersecurity tasks are re-routed to Opus 4.8. The Cyber Verification Program will expand to Opus 5.5.

Biology: Vetted organizations can apply to the Life Sciences Verification Program.

Distillation: Preserved thinking stops API users from editing prior context to extract reasoning. It applies to API accounts created on or after August 31, 2026.

Two more changes affect integrations. Thinking can no longer be disabled. Outputs also carry watermarking for EU AI Act compliance. Full details are in the Opus 5.5 System Card.

Interactive Explainer

Key Takeaways

Opus 5.5 matches Fable 5.1 on most work and beats both Opus 5 and Fable 5.1 on nearly every reported benchmark.

API pricing drops to $4/$20 per 1M tokens, and cache reads fall 60% to $0.20.

Anthropic puts typical workload savings at 40%, with output over 30% faster than Opus 5.

Cyber and biology requests hit Fable 5.1-class safeguards, and thinking cannot be switched off.

Closed weights: claude-opus-5-5 runs via Claude Platform, AWS, Google Cloud, and Azure.

Check out the Technical details here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Anthropic Releases Claude Opus 5.5: Fable 5.1-Level Performance at 40% Lower Running Cost Than Opus 5 appeared first on MarkTechPost.