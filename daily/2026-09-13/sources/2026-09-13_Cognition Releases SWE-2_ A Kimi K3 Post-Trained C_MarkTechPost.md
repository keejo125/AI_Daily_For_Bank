---
publish_time: 1789257363
link: https://www.marktechpost.com/2026/09/12/cognition-releases-swe-2-a-kimi-k3-post-trained-coding-model-that-matches-fable-5-1-on-frontiercode-at-64-lower-cost/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cognition（Devin 背后公司）发布迄今最强编程模型 SWE-2，基于月之暗面 Kimi K3（2.8T 参数开源模型）做强化学习后训练，在 FrontierCode 1.1 Main 取得 50.0% 得分，距 Fable 5.1 仅 1 个百分点、成本却低 64%。这是其首个支持可选推理强度档位的模型，三个档位在同一次 RL 运行中训练完成。相较 SWE-1.7（基于 Kimi K2.7 后训练），本次将 RL 扩展到多万亿参数区间，基础模型参数量近 3 倍，RL 在 K3 之上仍有 5～6 个百分点提升空间。SWE-2 无开放权重、无独立 API，仅运行于 Devin（Desktop/CLI 已上线，Web 与 Fusion 陆续推出）。
---

# Cognition 发布 SWE-2：基于 Kimi K3 后训练的编程模型

> 原文链接：https://www.marktechpost.com/2026/09/12/cognition-releases-swe-2-a-kimi-k3-post-trained-coding-model-that-matches-fable-5-1-on-frontiercode-at-64-lower-cost/
> 来源：MarkTechPost

Cognition, the company behind the Devin coding agent, has released SWE-2, its most capable coding model to date. SWE-2 is post-trained with reinforcement learning from Kimi K3, Moonshot AI&#8217;s 2.8T-parameter open model. Cognition reports a score of 50.0% on FrontierCode 1.1 Main, within 1 point of Fable 5.1 at 64% lower cost. It is also Cognition&#8217;s first model with selectable reasoning-effort levels, all trained in a single RL run.

Is it deployable? Not on your own infrastructure. SWE-2 has no open weights and no standalone API. It runs only inside Devin: Desktop and CLI today, with Devin Web and Fusion rolling out.

What is SWE-2

SWE-2 builds on the infrastructure and recipe behind SWE-1.7, which was post-trained from Kimi K2.7. This time Cognition scaled RL to the multi-trillion-parameter regime, using a base model with almost 3x the parameters. Cognition says its RL still finds substantial headroom on top of K3, adding 5 to 6 points on many benchmarks.

The main change is an RL algorithm that trains all 3 effort levels in one run. Each level carries its own cost penalty, so the whole cost-and-performance frontier moves at once.

Benchmark Results

Cognition published the following table. Public results are used where available; otherwise each model runs in its native harness at best effort.

BenchmarkSWE-2Kimi K3Grok 4.6Fable 5.1GPT-5.6 SolGPT-6 AstraSWE-1.7FrontierCode 1.1 Main50.0%44.2%48.0%50.9%47.5%53.3%42.0%DeepSWE 1.173.0%68.5%67.5%67.4%72.7%74.1%37.7%Terminal-Bench 2.192.8%88.3%88.4%91.4%88.8%89.9%81.5%Terminal-Bench 427.3%21.5%20.3%55.8%37.3%57.9%7.6%

SWE-2 leads on Terminal-Bench 2.1 and beats its K3 base on every row. Cognition says it comes within a few points of GPT-6 Astra at a quarter of the cost. The clear weak spot is Terminal-Bench 4, where SWE-2 trails Fable 5.1 and GPT-6 Astra by roughly 30 points. FrontierCode is Cognition&#8217;s own benchmark, and all rival numbers come from Cognition&#8217;s evaluation.

Model Behavior: Fewer Detours

SWE-1.7 tended to over-explore on simple tasks. SWE-2 addresses this through what Cognition calls focused exploration. On FrontierCode 1.1 Main, SWE-2 medium scores higher than SWE-1.7 while taking 58% fewer turns and costing 81% less. Mean steps per run drop from 127 (SWE-1.7) to 53 (medium), 80 (high), and 98 (max). SWE-2 medium makes its first real edit after a median of 18 steps, versus 48 for SWE-1.7.

Cognition team also reports 3 behavioral patterns: stronger end-to-end test coverage, resourcefulness when a tool is blocked, and verification discipline. When challenged, the model re-derives conclusions instead of re-asserting them.

How It Was Trained

Pareto-informed cost penalties: The reward is R = S minus lambda times C, where S is binary success and C mixes inference cost in USD with rollout time. Cognition proves that only a linear penalty makes the RL objective depend purely on average cost and solve rate. Each effort level&#8217;s lambda is set to the local slope of the base model&#8217;s Pareto curve. That makes the iso-reward line tangent to the frontier, so reward can only rise by pushing the frontier up.

Length-weighted reward baseline: Cognition shares a baseline used since SWE-1.6. Gradient magnitude correlates strongly with rollout length, so the group baseline is weighted by tokens: sum(R x L) divided by sum(L). In ablations this kept inference-to-training KL divergence lower and stabilized training at no extra compute.

Rollout serving and numerics: A prefill delayer batches nearby requests, raising TPM per GPU and TPS per request by 10 to 20%. DSpark speculative decoding accelerates rollouts, with a draft model retrained via SpecForge for 15% longer accept lengths and then trained online alongside the policy. NVFP4 and FP8 kernels with quantization-aware training keep memory usage down and train-inference mismatch below SWE-1.7 levels.

Data: Cognition tripled its RL environments, added instruction-following overlays, and built a flywheel that uses earlier SWE-2 checkpoints to patch false positives and negatives in verifiers.

Trustworthiness Checks

Cognition reran 2 evaluations from its open-source trustworthiness study. On 145 politically sensitive questions about China, SWE-2 passed 98.0% overall: 99.8% in English, 95.2% in Simplified Chinese, and 99.1% in Traditional Chinese. On a context-dependent vulnerability test across customer framings, no framing produced a statistically significant change for any model.

Interactive Explainer

&

Key Takeaways

SWE-2 scores 50.0% on FrontierCode 1.1 Main, within 1 point of Fable 5.1 at 64% lower cost

Post-trained from 2.8T-parameter Kimi K3; RL adds 5 to 6 points on most benchmarks

First Cognition model with effort levels, all trained in 1 RL run via slope-matched cost penalties

SWE-2 medium cuts turns 58% and cost 81% versus SWE-1.7 on FrontierCode

No open weights, no API: Devin only, free for paid tiers through October 10, 2026

Check out the Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Cognition Releases SWE-2: A Kimi K3 Post-Trained Coding Model That Matches Fable 5.1 on FrontierCode at 64% Lower Cost appeared first on MarkTechPost.