---
publish_time: 1791147596
link: https://www.marktechpost.com/2026/10/04/gpt-6-astra-vs-gpt-6-1-sol-vs-gemini-4-argon-vs-claude-fable-5-1-which-frontier-model-fits-which-job/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  2026年9月，Anthropic、OpenAI与Google DeepMind在30天内接连发布四款前沿大模型：Claude Fable 5.1（9月1日）、GPT-6 Astra（9月3日）、GPT-6.1 Sol与Gemini 4 Argon（9月底）。本文横向对比四款模型的规格、定价与基准表现。值得注意的是，OpenAI于9月28日取消了GPT-6.1 Astra（未通过内部范围与授权测试），GPT-6 Astra仍是OpenAI当前最强模型。基准上，Gemini 4 Argon领先知识工作与长周期编程，GPT-6 Astra领跑前沿软件工程与计算机操作；价格层面Astra与Fable为每百万token输入/输出10/50美元，Sol与Argon仅为其五分之一。对Agent场景而言，Astra缓存读取单价最高，而Argon以100万token输出上限成为结构性特例。
---

# 前沿四强对决：GPT-6 Astra、GPT-6.1 Sol、Gemini 4 Argon 与 Claude Fable 5.1

> 原文链接：https://www.marktechpost.com/2026/10/04/gpt-6-astra-vs-gpt-6-1-sol-vs-gemini-4-argon-vs-claude-fable-5-1-which-frontier-model-fits-which-job/
> 来源：MarkTechPost

Anthropic, OpenAI and Google DeepMind shipped 4 frontier-class models within 30 days. Claude Fable 5.1 arrived on September 1. GPT-6 Astra followed on September 3. GPT-6.1 Sol and Gemini 4 Argon landed in the last days of September.

We covered each launch on its own. This piece puts them side by side. The benchmark scores overlap more than the launch posts suggest. The prices, access rules and cost per task do not.

One change frames the lineup. OpenAI cancelled GPT-6.1 Astra on September 28 after it failed internal scope and authorization tests. GPT-6 Astra stays OpenAI&#8217;s top model for now.

Specs, Pricing and Access

Astra and Fable 5.1 share the same $10 input and $50 output list price. Sol and Argon list at one-fifth of that. Argon&#8217;s price is introductory and doubles later.

FeatureGPT-6 AstraGPT-6.1 SolGemini 4 ArgonClaude Fable 5.1DeveloperOpenAIOpenAIGoogle DeepMindAnthropicReleasedSep 3, 2026Sep 29, 2026Announced Sep 30, 2026Sep 1, 2026AccessOpenAI API, ChatGPT, CodexOpenAI API, ChatGPT Work, CodexFairwind Program onlyClaude API, Bedrock, Google Cloud, Microsoft FoundryInput / output (per 1M)$10 / $50$2 / $10$2 / $10 intro, then $4 / $20$10 / $50Cached input (per 1M)$1.00$0.10$0.10 intro$0.25Long-prompt pricingAbove 272K: $20 / $75Above 272K: 2x input, 1.5x outputNot disclosedFlat to 1MContext window1.05M1.05MNot disclosed1MMax output per response128K128K1M128KReasoning control5 effort levels, low to max5 effort levels, low to maxNot disclosedEffort levels incl. low, medium, highOpen weightsNoNoNoNo

Sources: OpenAI GPT-6.1 Sol coverage, Gemini 4 Argon coverage, GPT-6 Astra long-context pricing, Claude Fable 5.1 specs. Standard first-party list prices, short-context tier.

The cached-input row matters most for agents. Agents resend system prompts, tool schemas and history on every step. Astra&#8217;s $1.00 cache read is 4x Fable 5.1&#8217;s and 10x Sol&#8217;s.

Argon&#8217;s 1M output cap is the only structural outlier. The other 3 stop at 128K tokens per response.

Benchmarks: Where Each Model Leads

No model sweeps the board. Argon leads the knowledge-work and long-horizon coding rows. Astra leads frontier software engineering and computer use. Opus 5.5, not in this lineup, leads Terminal-Bench 4.0.

BenchmarkWhat it testsGemini 4 ArgonGPT-6 AstraClaude Fable 5.1DeepSWE v1.1Long-horizon software engineering77.9%74.1%67.4%Vals IndexFinance, coding, legal and tax work68.9%63.1%65.8%FrontierSWE v2Frontier software engineering55.0%65.5%56.3%Terminal-Bench 4.0Agentic work in a terminal57.4%58.2%57.9%CWE-bench v1Vulnerability remediation68% (tie)68% (tie)58%OSWorld-2.0Computer use69.2%72.6%Not in Google&#8217;s table

Source: Google DeepMind&#8217;s published comparison, as reported in our Gemini 4 Argon coverage. Vendor-reported.

GPT-6.1 Sol is not in Google&#8217;s table. OpenAI&#8217;s own numbers place it close to Astra:

DeepSWE v1.1: Sol matches Astra at roughly one-fifth of the cost.

OSWorld 2.0 offline set: Sol lands within 2.1 points of Astra at about one-seventh the cost per task.

AutomationBench 1.0.6: Sol scores 2.2 points above Claude Opus 5.5 at medium effort.

Terminal-Bench Science 0.1: Astra still leads at 68.1%. OpenAI recommends Astra for the hardest research.

Independent signals point the other way on raw intelligence. On the Artificial Analysis Intelligence Index, Astra scores 61. Fable 5.1 scores 5 points higher. On its coding-agent index, Fable 5.1 in Claude Code scores 70 against Astra&#8217;s 67. Artificial Analysis also reports that Argon equals Astra on the Intelligence Index.

On ARC-AGI-2, Astra scores 95% and Fable 5.1 scores 90%.

Cost per Task: Same List Price, Different Bill

Artificial Analysis puts Claude Fable 5.1 at $9.18 per task, against $4.72 for GPT-6 Astra. That is about 1.9x, at identical list prices. 

The gap comes from token volume, not rates. Cost per task multiplies price by tokens spent. With equal rates, the gap implies Fable 5.1 spent more tokens per task in that run. Anthropic also notes its newer tokenizer produces roughly 30% more tokens for the same text.

The two cheaper models change the picture further:

Gemini 4 Argon: Artificial Analysis reports Argon equals Astra&#8217;s Intelligence Index at 60% of Astra&#8217;s cost per task, using introductory prices.

GPT-6.1 Sol: On Terminal-Bench Science, OpenAI reports $5.47 per task for Sol against $23.80 for Astra.

Caching can reverse the ranking for agents. The per-task figures above do not model heavy cache reuse. A long-running agent rereads the same context on every step. Here is the arithmetic for a 200K-token cached context, before output tokens:

ModelCached rate (per 1M)Per stepPer 100 stepsGPT-6 Astra$1.00$0.20$20.00Claude Fable 5.1$0.25$0.05$5.00GPT-6.1 Sol$0.10$0.02$2.00Gemini 4 Argon (intro)$0.10$0.02$2.00

Illustrative math from list cache rates. Astra&#8217;s 200K context stays under its 272K long-prompt threshold.

In cache-heavy loops, Fable 5.1 reads context at a quarter of Astra&#8217;s rate. Measure both on your own traces before you pick on per-task headlines.

Which Model for Which Job

Pick by workload, not by leaderboard rank. GPT-6.1 Sol is the default for most teams. The other 3 earn their price on narrower jobs.

JobPickWhyRunner-upHigh-volume coding agents, CI bots, PR reviewGPT-6.1 SolMatches Astra on DeepSWE v1.1 at $2 / $10 and $0.10 cachedGemini 4 Argon, once publicHardest open-ended engineeringGPT-6 AstraLeads FrontierSWE v2 at 65.5%Claude Fable 5.1Computer use and browser agentsGPT-6 AstraLeads OSWorld-2.0 at 72.6%GPT-6.1 Sol, within 2.1 pointsLong coding sessions inside a harnessClaude Fable 5.1Top Artificial Analysis coding-agent score (70) in Claude Code; $0.25 cache readsGPT-6 Astra (67)Hard science and researchGPT-6 AstraLeads Terminal-Bench Science at 68.1%GPT-6.1 Sol at $5.47 per taskLegal, finance and business automationGemini 4 ArgonLeads Vals Index (68.9%), AutomationBench (51.3%) and Harvey Legal (19.6%)GPT-6.1 Sol; Claude Fable 5.1Very long single outputs: big refactors, full reportsGemini 4 ArgonOnly model with 1M output tokens per responseAny of the 3 others, split across turnsVulnerability finding and patchingGemini 4 Argon or GPT-6 AstraTied at 68% on CWE-bench v1Claude Fable 5.1 (58%)Tightest budget at frontier qualityGPT-6.1 SolLowest public price; Argon matches it only inside FairwindGemini 4 Argon

Access decides 2 of these rows. Argon is only available to Fairwind cyber defenders today. Astra&#8217;s full offensive-security capability sits behind OpenAI&#8217;s Daybreak program; the public release refuses advanced offensive cyber tasks. Anthropic gates its unrestricted twin, Claude Mythos 5.1, behind trusted access programs.

What to Check Before You Switch

Most numbers here are vendor-reported, and vendors disagree at the margins. OpenAI reports Astra at 57.9% on Terminal-Bench 4.0. Google&#8217;s comparison table lists 58.2%.

Safeguards affect Fable 5.1 scores: Anthropic ran its benchmarks with production safeguards on. Flagged cyber and biology tasks route to other Claude models, which likely lowered OSWorld and AutomationBench results.

Argon&#8217;s pricing is temporary: $2 / $10 is introductory. It moves to $4 / $20 later, with no end date announced.

Argon&#8217;s context window is undisclosed: Google published the 1M output cap but not the input limit.

Per-task costs are a snapshot: The $9.18 and $4.72 figures come from Artificial Analysis&#8217; early-September Astra run. Effort settings shift them a lot.

Anthropic has a cheaper option: Our Argon coverage cites reports that Claude Opus 5.5 beats Fable 5.1 on key agentic benchmarks at a lower API price. It also leads Terminal-Bench 4.0 at 66.4%.

Key Takeaways

GPT-6.1 Sol matches Astra on DeepSWE v1.1 at one-fifth the price.

GPT-6 Astra leads FrontierSWE v2 (65.5%) and OSWorld-2.0 (72.6%).

Gemini 4 Argon leads DeepSWE, Vals Index and AutomationBench, but only inside Fairwind.

Fable 5.1 costs $9.18 per task vs $4.72 for Astra, at equal list prices.

For cache-heavy agents, Fable 5.1&#8217;s $0.25 cache read undercuts Astra&#8217;s $1.00 by 4x.

FAQ

Which is cheapest? GPT-6.1 Sol, at $2 input, $10 output and $0.10 cached per 1M tokens. Argon matches that only at introductory pricing, inside Fairwind.

Which is best for coding? Sol for volume. Astra for the hardest tasks. Fable 5.1 tops Artificial Analysis&#8217; coding-agent index in Claude Code.

Can I use Gemini 4 Argon today? Only through Google&#8217;s Fairwind Program for cyber defenders.

The post GPT-6 Astra vs GPT-6.1 Sol vs Gemini 4 Argon vs Claude Fable 5.1: Which Frontier Model Fits Which Job appeared first on MarkTechPost.