---
publish_time: 1788369624
link: https://www.marktechpost.com/2026/09/02/google-deepmind-releases-gemini-3-8-flash-and-gemini-3-8-flash-cyber-one-core-model-two-access-envelopes/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google发布Gemini 3.8 Flash及3.8 Flash Cyber，三周内第三款Flash、六周第三款。两者基于同一基础智能，经长时Agentic loop递归评估优化，差别在安全边界与开放对象。3.8 Flash已全面开放，沿用1M上下文、65K输出，编程、智能体、多步推理提升；3.8 Flash Cyber面向漏洞检测与自动修补，通过Fairwind计划按案开放。
---

# 谷歌Gemini 3.8 Flash与3.8 Flash Cyber发布：同一核心模型，两种访问边界

> 原文链接：https://www.marktechpost.com/2026/09/02/google-deepmind-releases-gemini-3-8-flash-and-gemini-3-8-flash-cyber-one-core-model-two-access-envelopes/
> 来源：MarkTechPost

Google just announced Gemini 3.8 Flash and Gemini 3.8 Flash Cyber, three weeks after Gemini 3.7 Flash and marking the third Flash release in six weeks. Both variants run on the same foundational intelligence, refined through long-running agentic loops that recursively evaluate the underlying models. What separates them is not architecture, it is the safety envelope and who is allowed through it.

Is it deployable? Gemini 3.8 Flash is generally available today through the Gemini API, Google AI Studio, Antigravity, Android Studio, and Gemini Enterprise, so you can route production traffic to it now. Weights are closed, so there is no self-hosted or on-premises path. Gemini 3.8 Flash Cyber is not openly deployable at all: access is granted case by case through the new Fairwind Program.

What actually changed in 3.8 Flash

The research team explains that 3.8 Flash is based on 3.7 Flash. Specs are unchanged: a 1,048,576-token context window, 65,536-token maximum output, text, image, audio, and video input, and text output. Thinking levels remain LOW, MEDIUM, and HIGH with MEDIUM as the default. One breaking detail for anyone migrating: MINIMAL is not supported on 3.8 Flash and setting it returns an API validation error.

The behavioral change is the point. Google describes the gain bluntly: 3.8 Flash works harder. On complex tasks it executes extra reasoning steps and calls tools iteratively, and it may burn more tokens at higher effort levels. Google&#8217;s own developer guide is candid that this buys better accuracy at the cost of higher token consumption, and it recommends staying on 3.7 Flash when compute efficiency is the binding constraint. That is an unusually direct admission that the newer model is not the right default for every workload.

https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/

Where the gains show up

On DeepSWE v1.1, a long-horizon software engineering benchmark, Google reports 3.8 Flash outperforming most larger frontier models at a fraction of the cost. It records 54.9% on HLE-Verified, and gains over 3.7 Flash and other frontier models on Vals Finance Agent V2 and Harvey&#8217;s Legal Agent Benchmark. Note that the finance and legal results are reported as relative wins, without absolute scores in the announcement. 

Flash Cyber, and why it is gated

On CyberGym, the standard vulnerability discovery benchmark, Google reports frontier-level performance that surpasses both 3.5 Flash Cyber and significantly larger frontier models, though no absolute figure is published. Because CyberGym is mostly C and C++, Google also ran an internal benchmark across 20 programming languages and reports a discovery success rate above 70%.

For patching, CWE-Bench, run by Collinear, puts Flash Cyber at 47.2% pass@1 against a leading frontier model&#8217;s 47.8%. Near-parity at materially lower cost is the claim, and Google frames it as sitting on the Pareto frontier rather than topping the leaderboard.

Chrome Security reports 2.6x more correct patches than the best, much larger commercial models. Wiz measures 7.5 to 9.7 percentage points higher recall on its internal penetration testing benchmark at 2.3x to 5.2x lower cost. Google&#8217;s Cloud Vulnerability Research team found a critical foundational vulnerability in under two hours, work that normally takes months.

Google is explicit that it prioritized vulnerability fixing over offensive capabilities like exploitation. Flash Cyber ships with a more permissive set of cyber mitigations, which is precisely why it is restricted to trusted defenders: government authorities, critical infrastructure operators, and software maintainers who apply through Fairwind.

Interactive explainer

Key Takeaways

Two variants ship on one shared core, split by safety mitigations rather than model size.

3.8 Flash holds 3.7 Flash pricing at $0.75/$3.75 per 1M tokens through December 31, 2026.

It trades tokens for accuracy: more reasoning steps, more tool calls, higher spend per task.

Flash Cyber hits 47.2% pass@1 on CWE-Bench against a frontier model&#8217;s 47.8%, at far lower cost.

Cyber access is gated to vetted defenders, not sold on a price sheet.

Check out Technical details here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google DeepMind Releases Gemini 3.8 Flash and Gemini 3.8 Flash Cyber: One Core Model, Two Access Envelopes appeared first on MarkTechPost.