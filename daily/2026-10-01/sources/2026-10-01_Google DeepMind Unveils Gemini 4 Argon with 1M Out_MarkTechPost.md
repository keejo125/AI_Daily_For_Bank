---
publish_time: 1790803808
link: https://www.marktechpost.com/2026/09/30/google-deepmind-unveils-gemini-4-argon-with-1m-output-tokens-for-coding-knowledge-work-and-cyber-defense/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MarkTechPost 报道 Gemini 4 Argon：输出上限从 64K 升至 100 万 Token，定价每百万输入 2 美元、输出 10 美元（后续 4/20）；在 18 项基准中 12 项领先、1 项并列，DeepSWE v1.1 77.9% SOTA，Harvey 法律基准 19.6% 远超 Astra 的 5.4%；但在 FrontierSWE v2、Terminal-Bench、OSWorld 落后。
---

# 谷歌 DeepMind 发布 Gemini 4 Argon：百万 Token 输出，覆盖编程、知识工作与网络防御

> 原文链接：https://www.marktechpost.com/2026/09/30/google-deepmind-unveils-gemini-4-argon-with-1m-output-tokens-for-coding-knowledge-work-and-cyber-defense/
> 来源：MarkTechPost

Google DeepMind has just announced Gemini 4 Argon, its new frontier model and the first model of the Gemini 4 generation. It targets long-horizon software engineering, enterprise knowledge work in legal and finance, and cybersecurity defense. The biggest technical change is output length. Argon can generate up to 1M tokens in a single response, up from 64K on earlier Gemini models.

What Google Announced

Google DeepMind described Argon as built for complex workflows across coding, enterprise knowledge work and cybersecurity defense.

Google is taking a phased approach. It is participating in the U.S. government&#8217;s voluntary process for pre-release model access. It will gather feedback from early testers and iterate on guardrails before a wider release.

Pricing is already public. Argon launches at an introductory $2 per 1M input tokens and $10 per 1M output tokens. Cached input tokens get a 95% discount, which works out to $0.10 per 1M. After the introductory period, pricing moves to $4 input and $20 output. Logan Kilpatrick confirmed the introductory $2 in and $10 out pricing.

Why the 1M Output Limit Matters

Current frontier APIs cap a single response far lower. Claude Opus 5.5, Claude Fable 5.1 and GPT-6 Astra each allow 128K output tokens.

Google team states that Argon can think deeply and generate hundreds of thousands of tokens in one trajectory. For developers, that means large refactors or long reports without splitting work across turns. The cost is real, though. A full 1M output tokens costs $10 at introductory pricing and $20 after.

Google has not disclosed Argon&#8217;s input context window.

Benchmarks: Where Argon Leads and Where It Trails

Google compared Argon against GPT-6 Astra, Claude Opus 5.5 and Claude Fable 5.1. Argon leads outright on 12 of 18 benchmarks and ties for first on 1.

Where it leads:

DeepSWE v1.1 (long-horizon software engineering): 77.9%, a new state of the art. Opus 5.5 scores 74.2% and GPT-6 Astra 74.1%.

Vals Index (economic impact across finance, coding, legal and tax): 68.9%, ranked first.

AutomationBench (Zapier, end-to-end business execution): 51.3%, ranked first. Opus 5.5 scores 42.5%.

Harvey Legal Agent Benchmark: 19.6%, against 5.4% for GPT-6 Astra.

LVBench (long video understanding): 91.7%, a new state of the art.

Where it trails:

FrontierSWE v2: 55.0%, behind GPT-6 Astra at 65.5%.

Terminal-Bench 4.0: 57.4%, behind Claude Opus 5.5 at 66.4%.

OSWorld-2.0 (computer use): 69.2%, behind GPT-6 Astra at 72.6%.

Artificial Analysis reported that Argon equals GPT-6 Astra on its Intelligence Index at 60% of the cost per task, using discounted prices.

Cyber Defense: Find, Validate, Patch

Google trained Argon to autonomously find, validate and patch critical software vulnerabilities. Trusted defenders and internal Google teams receive it without cyber guardrails.

On CWE-bench v1, which tests vulnerability remediation, Argon ties for first at 68%. The rival models on that leaderboard run inside their own agent harnesses.

Wiz is already using Argon through its Scan for Good initiative. The model found a critical vulnerability in healthcare software used by hospitals worldwide. Google says previous frontier models had missed it.

Before broad release, Google is strengthening safeguards in 4 areas:

Misuse defenses for cyber and CBRN risks, including activation monitoring, under its Frontier Safety Framework.

Indirect prompt injection resistance, where Argon leads Gray Swan&#8217;s IPI benchmark.

Misalignment monitoring of chain-of-thought and actions, with the ability to stop execution.

Sealed, isolated sandboxes for high-risk training and evaluations.

&

Argon Inside Google

Thousands of Googlers already use Argon. Google shared 4 internal results:

Argon agents applied memory optimizations across data centers, freeing over 300 TiB, with 500 TiB to 1 PiB projected.

Agents replaced 32K lines of SIMD code in the libgav1 Rust port. The decoder runs 2.7x faster with identical output.

Agents are migrating C/C++ codebases to Rust, up to 800K+ lines in the Fuchsia Zircon kernel.

Argon beat a published quantum algorithm baseline by 40% in minutes.

Comparison: Gemini 4 Argon vs Closest Competitors

FeatureGemini 4 ArgonClaude Opus 5.5Claude Fable 5.1GPT-6 AstraDeveloperGoogle DeepMindAnthropicAnthropicOpenAIAvailabilityFairwind Program onlyClaude API and cloudsClaude API and cloudsOpenAI APIMax output per response1M tokens128K128K128KContext windowNot disclosed1M1M1.05MInput / output price (per 1M)$2 / $10 intro, then $4 / $20$4 / $20$10 / $50$10 / $50Cached input (per 1M)$0.10 (intro)$0.20$0.25$1.00Open weightsNoNoNoNoDeepSWE v1.177.9%74.2%67.4%74.1%Vals Index68.9%67.0%65.8%63.1%FrontierSWE v255.0%62.3%56.3%65.5%Terminal-Bench 4.057.4%66.4%57.9%58.2%CWE-bench v168% (tie)67%58%68% (tie)

Sources: Google, Anthropic Opus pricing, Anthropic Fable 5.1 docs, OpenAI GPT-6 Astra docs, OpenRouter. Benchmark scores are from Google&#8217;s published comparison. GPT-6 Astra prices are its short-context tier.

Key Takeaways

Gemini 4 Argon raises the output limit from 64K to 1M tokens.

It leads DeepSWE v1.1 (77.9%) and the Vals Index (68.9%).

It trails on FrontierSWE v2, Terminal-Bench 4.0 and OSWorld-2.0.

Introductory pricing of $2 / $10 is half of Claude Opus 5.5.

Access is limited to Fairwind cyber defenders; no public release date yet.

Check out the technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google DeepMind Unveils Gemini 4 Argon with 1M Output Tokens for Coding, Knowledge Work and Cyber Defense appeared first on MarkTechPost.