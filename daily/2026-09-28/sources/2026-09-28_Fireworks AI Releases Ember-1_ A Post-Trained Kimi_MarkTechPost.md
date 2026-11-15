---
publish_time: 1790580153
link: https://www.marktechpost.com/2026/09/28/fireworks-ai-releases-ember-1-a-post-trained-kimi-k3-that-uses-about-40-fewer-tokens/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Fireworks AI 通过后训练 Moonshot AI 的开权重模型 Kimi K3，推出专用模型 Ember-1。它学习生成更短的思考轨迹，在保持任务准确率的同时将 Kimi K3 的质量以约 40% 更少的 Token 实现。其与在推理时调低推理强度（reasoning effort）的做法不同：Fireworks 团队观察到推理模型如 Kimi K3 有时会将 90% 以上的生成 Token 花在内部推理上，多轮调用时成本被显著放大。Ember-1 目前仅通过 Fireworks 无服务器 API 以研究预览形式提供，未开源权重、训练代码与算法，暂不支持自托管。
---

# Fireworks AI 发布 Ember-1：后训练的 Kimi K3，推理省 40% Token

> 原文链接：https://www.marktechpost.com/2026/09/28/fireworks-ai-releases-ember-1-a-post-trained-kimi-k3-that-uses-about-40-fewer-tokens/
> 来源：MarkTechPost

Fireworks AI has released Ember-1, a specialized model from Fireworks Research built by post-training Moonshot AI&#8217;s open-weight Kimi K3. Ember-1 learns to produce shorter reasoning traces while keeping task accuracy. This is different from lowering the reasoning effort setting at inference time. According to the Fireworks release post, Ember-1 delivers Kimi K3&#8217;s quality with about 40% fewer tokens.

Is it deployable? Yes, but only through the Fireworks serverless API as a Research Preview. Fireworks has not released Ember-1&#8217;s weights, training code, or exact training algorithms, so self-hosting is not an option today.

The Problem: Reasoning Models Think Too Much

Fireworks team reports that reasoning models like Kimi K3 sometimes spend more than 90% of generated tokens on internal reasoning. That cost compounds in multi-turn agentic workloads. Each turn replays prior reasoning back to the model. Context grows roughly quadratically with the number of turns. Long traces from early turns get re-read, and re-billed, on every later call.

Fireworks team explains how customers wanted K3&#8217;s coding capability at lower cost. Turning down K3&#8217;s reasoning effort did not solve it. Lower effort settings gave up too much quality. So the team trained the model to reason more efficiently instead.

How Fireworks Research Built Ember-1

Not all of K3&#8217;s reasoning is waste. Some of it is useful self-reflection, like revisiting an assumption or reacting to feedback. Ember-1 keep that behavior while cutting redundant reasoning and unproductive loops.

The training collection spans mathematics, coding, instruction following, conversation, search, tool use, and software engineering. It covers both standalone problems and extended multi-step interactions. Task and environment feedback guides on-policy planning and learning. Fireworks team ran more than 50 training experiments and over 200 evaluations. They also developed new training algorithms, which it has not published. All training ran on Fireworks Serverless Training. Fireworks states it used its own data and no customer data.

Benchmark Results

Fireworks compared Ember-1 with Kimi K3 at three reasoning effort levels. Cost was computed with public Kimi K3 API pricing. These are Fireworks&#8217; own published evaluations.

BenchmarkNK3 LowK3 HighK3 MaxEmber-1Ember-1 vs K3 Max (cost)Terminal Bench 2.18976.4%77.6%80.9%82.0%-51.9% / -23.1 USDSWE-bench Verified50080.4%86.0%93.2%92.2%-15.5% / -68.1 USDSWE-Interact756.7%13.3%21.3%20.0%-32.5% / -60.8 USDDeepSWE 1.111355.8%62.8%66.4%75.2%-23.7% / -126.9 USDτ-2 Bench Airline5064%64%64%66%-5.9% / -0.3 USD

Ember-1 leads K3 Max on Terminal Bench 2.1 and DeepSWE 1.1. It trails slightly on SWE-bench Verified and SWE-Interact. Across seven benchmarks and two customers&#8217; production traffic, Fireworks says K3&#8217;s reasoning was shortened by 35 to 50% without sacrificing accuracy.

On Doximity&#8217;s Bedside Bench, a physician-validated set of 500 clinical cases, Ember-1 set a new cost-per-task Pareto frontier. That result comes from Fireworks&#8217; new Specialized Intelligence Index.

Production A/B Test Results

Fireworks ran live A/B tests with 2 customers on production coding workloads. Both saw roughly 35% fewer tokens per task at comparable quality. In the published run, output tokens fell from 49.3K to 29.9K per task. Reasoning tokens dropped 71.3% and total tokens dropped 39%. The task score was essentially unchanged: 0.753 for Ember-1 versus 0.751 for K3. Average steps fell from 23.8 to 21.4. One customer now runs Ember-1 in production.

Ember-1 costs the same per token as Kimi K3 on Fireworks: $3.00 input, $0.30 cached input, and $15.00 output per 1M tokens. The savings come entirely from generating fewer tokens. At that output rate, the A/B figures work out to about $0.74 versus $0.45 in output cost per task (our calculation, output only).

Interactive Explainer

Key Takeaways

Ember-1 is Kimi K3 post-trained to reason in fewer tokens, not run at lower effort.

Fireworks reports about 40% fewer tokens with accuracy held across its evaluations.

In a production A/B test, output fell from 49.3K to 29.9K tokens per task at a 0.753 vs 0.751 score.

It beats K3 Max on Terminal Bench 2.1 (82.0%) and DeepSWE 1.1 (75.2%), trailing on SWE-bench Verified (92.2%).

API-only Research Preview at K3 pricing; weights and training code are not released.

Check out the Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Fireworks AI Releases Ember-1: A Post-Trained Kimi K3 That Uses About 40% Fewer Tokens appeared first on MarkTechPost.