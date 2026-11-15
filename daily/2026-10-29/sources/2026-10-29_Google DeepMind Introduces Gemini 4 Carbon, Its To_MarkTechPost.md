---
publish_time: 1793209718
link: https://www.marktechpost.com/2026/10/28/google-deepmind-gemini-4-carbon-frontier-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MarkTechPost详解Gemini 4 Carbon：第二大Gemini 4模型，针对长程智能体编程与网安防御，智能指数59分登顶。对比Argon、GPT-6 Astra、Opus 5.5、Fable 5.1在17项基准中领先15项，WebDev Arena Elo +89至1769；OSWorld-2.1（81.5%）落后Opus 5.5。普通开发者暂无法调用，先向网安防御者开放。
---

# Google DeepMind 介绍 Gemini 4 Carbon：迄今最强的 Gemini 4 模型

> 原文链接：https://www.marktechpost.com/2026/10/28/google-deepmind-gemini-4-carbon-frontier-model/
> 来源：MarkTechPost

Google DeepMind has introduced Gemini 4 Carbon, its strongest model to date. Gemini 4 Carbon is a frontier model from Google built for long-horizon agentic coding and cybersecurity defense. It ranks #1 on the updated v5.0 Artificial Analysis Intelligence Index with a score of 59. For developers, the catch is access. Carbon starts with a vetted group of cyber defenders, not the public API.

TL;DR

Size: Parameter count and context window not disclosed. Its predecessor, Gemini 4 Argon, has a 1,048,576-token context.

Runs on: Google-hosted only. No open weights, no self-hosting, no quantized variants.

Performance: Leads 15 of 17 published benchmarks versus Argon, GPT-6 Astra, Opus 5.5 and Fable 5.1.

Best: 96.2% BFS F1 on GraphWalks (256K to 1M tokens), versus 84.2% for Argon.

Worst: 81.5% on OSWorld-2.1, trailing Claude Opus 5.5 at 87.2%.

Bottom line: Best: state-of-the-art vulnerability finding, exploitation and patching. Worst: you probably cannot call it yet.

What is Gemini 4 Carbon?

Carbon is the second Gemini 4 model, following Gemini 4 Argon. Google team states that the model targets hard, long-running engineering work. Internal teams saw Carbon run for days on single tasks. Examples include root-causing and patching subtle bugs across large codebases and low-level systems.

Google also tuned Carbon for full-stack web development and multimodal understanding. On WebDev Arena, Carbon gained 89 Elo points to reach #4 at 1769.

How does Gemini 4 Carbon perform on benchmarks?

Google published a 17-row comparison in its launch post. Carbon was run at the highest thinking setting. Most rival numbers are self-reported by each provider, per Google&#8217;s evaluation methodology.

Agentic coding: Carbon scores 65.2% on Terminal-Bench 4.0 (AA), ahead of Opus 5.5 at 59.6%. It hits 9.6% on SWE-sweep, narrowly ahead of GPT-6 Astra at 9.5%. On FrontierSWE, GPT-6 Astra leads at 65.5% versus Carbon&#8217;s 61.2%.

Computer use and knowledge work: Carbon reaches 77.4% on Agents&#8217; Last Exam v1.1. On Vending-Bench 2, it ends with a $16,484 bank balance, the highest listed.

Long context and science: GraphWalks is the widest gap: 96.2% versus 71.8% for GPT-6 Astra. Carbon also posts 80.0% on RiemannBench.

Why does Carbon relevant for cybersecurity?

Google frames Carbon around the full defense lifecycle: find, validate, then fix. Cyber benchmarks were evaluated without guardrails.

Finding: 88.2% on SEC-bench Pro, versus 85.4% for GPT-6 Astra.

Exploiting: 54.8% on ExploitGym, versus 42.4% for GPT-6 Astra and 34.5% for Opus 5.5.

Patching: 71.0% on Collinear&#8217;s CWE-bench, versus 68.0% for Argon and GPT-6 Astra.

Google computed SEC-bench Pro and ExploitGym scores itself, using its Antigravity harness. ExploitGym ran with mitigations off. Internally, Carbon showed more than 2x higher success at generating secure code than Argon. Google team states that the Chrome team found Carbon over 10x better than another lab&#8217;s model at high-quality patches. Wiz reports Carbon leading its web penetration testing benchmarks.

What safety changes ship with Carbon?

Carbon keeps Argon&#8217;s layered stack: training, real-time misuse defenses, prompt-injection resilience and chain-of-thought monitoring. Google reports several alignment gains:

Successful cheating on Terminal-Bench 4.0 fell to 0.0%, with cheating attempts at 0.4%.

High-severity misalignment alerts in live internal coding dropped by almost 80%.

Unsupported claims fell roughly 2x versus Argon.

Overreach fell 26% and under-service fell 29%.

Attack success on Gray Swan&#8217;s Indirect Prompt Injection benchmark is 0.0%, down from Argon&#8217;s 0.7%.

These are Google&#8217;s internal or self-run figures. Independent replication is not yet available.

How can developers access Gemini 4 Carbon?

Not yet, for most. Google is participating in the U.S. government&#8217;s voluntary pre-release testing process. This week, a subset of cyber defenders gets access. More trusted partners follow through the Fairwind Program, which prioritizes governments, critical infrastructure operators and core tech platforms. Developers, businesses and consumers get Carbon later, with no date given.

Pricing matches Argon&#8217;s introductory rate: $2 per million input tokens and $10 per million output tokens. Cached input is 95% off. After the introductory period, prices rise to $4 and $20.

Gemini 4 Carbon vs competitors

FeatureGemini 4 CarbonGemini 4 ArgonGPT-6 AstraClaude Opus 5.5Claude Fable 5.1ParametersNot disclosedNot disclosedNot disclosedNot disclosedNot disclosedContext windowNot disclosed1,048,5761,050,0001M1MMax outputNot disclosed65,536 (1,048,576 long decode)128,000128K128KPrice in / out (per 1M)$2 / $10 intro, then $4 / $20$2 / $10 intro (Google)$10 / $50$4 / $20 (pricing)$10 / $50 (pricing)AccessVetted cyber defenders, FairwindGemini APIOpenAI APIClaude APIClaude APIAA Index v5.05950575849SEC-bench Pro88.2%83.4%85.4%Not disclosedNot disclosedExploitGym54.8%42.0%42.4%34.5%Not disclosedOSWorld-2.181.5%74.7%80.9%87.2%76.8%FrontierSWE61.2%55.0%65.5%62.3%56.3%

Benchmark rows: Google launch post; rival scores mostly self-reported per methodology.

Key Takeaways

Gemini 4 Carbon ranks #1 on Artificial Analysis Index v5.0 at 59.

It leads SEC-bench Pro (88.2%), ExploitGym (54.8%) and CWE-bench (71.0%).

GraphWalks long context hits 96.2%, its widest margin.

Claude Opus 5.5 still wins OSWorld-2.1; GPT-6 Astra wins FrontierSWE.

Access starts with cyber defenders at $2/$10 per million tokens.

Check out the Google&#8217;s launch post, the evaluation methodology and the Fairwind Program page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google DeepMind Introduces Gemini 4 Carbon, Its Top Model for Cyber Defense and Coding appeared first on MarkTechPost.