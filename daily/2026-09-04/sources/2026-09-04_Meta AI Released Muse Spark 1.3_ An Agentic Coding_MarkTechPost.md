---
publish_time: 1788461512
link: https://www.marktechpost.com/2026/09/03/meta-ai-released-muse-spark-1-3-an-agentic-coding-model-that-uses-20-fewer-tool-calls-and-25-fewer-tokens-than-muse-spark-1-2/
source: Meta AI
status: confirmed
category: 国际
is_model_related: true
digest: |
  Meta 超级智能实验室发布智能体编程模型 Muse Spark 1.3，这是该系列五个月内第四次迭代。相比 1.2 版本，新模型在完成任务时使用约 20% 更少的工具调用与约 25% 更少的 token，在 agentic coding 场景下兼顾效果与成本，延续 Meta 在高效智能体编程上的工程路线。
---

# Meta 发布 Muse Spark 1.3：工具调用减少约 20%、Token 减少约 25% 的智能体编程模型

> 原文链接：https://www.marktechpost.com/2026/09/03/meta-ai-released-muse-spark-1-3-an-agentic-coding-model-that-uses-20-fewer-tool-calls-and-25-fewer-tokens-than-muse-spark-1-2/
> 来源：MarkTechPost

This week, Meta Superintelligence Labs released Muse Spark 1.3. It is the fourth Muse Spark release in five months, and the target is long-horizon agentic and coding work rather than single-turn generation. The framing in Meta&#8217;s post is usability: sustaining a long thread, collaborating with the user, and knowing when it is stuck. 

Is it deployable? Yes, but with two limits. Muse Spark 1.3 ships today in Muse Code and the Meta Model API, so you can call it in production now. You cannot self-host it, because the weights are closed, and the max reasoning mode is still gated behind further safety testing.

What actually changed for agents

Meta trained Muse Spark 1.3 across multiple agent harnesses so behavior generalizes past one environment. The model is built to hold several workflows inside a single long thread. Given an open-ended objective, it gathers its own context from messy and conflicting sources, then patches gaps in its plan.

The collaboration changes are the more practical part. Muse Spark 1.3 asks clarifying questions on ambiguous prompts, pulls the user in when it stalls, and confirms before consequential actions. On long runs it adapts to preference: frequent status updates, or silent background execution. Meta also reports better calibration on the model&#8217;s own limits, so it flags hurdles instead of hallucinating an outcome.

Multitasking improved too. Meta says the model maps an incoming prompt to the correct task inside a cluttered single thread, whether the user is steering or interrupting.

Coding and efficiency

Muse Spark 1.3 was trained on more long-horizon coding tasks. Relative to Muse Spark 1.2, Meta describes fewer unnecessary turns, less verbosity, and a cleaner code style. In internal comparisons by Meta engineers, it used approximately 20% fewer tool calls and approximately 25% fewer tokens. For agentic workloads, that is the number that maps to cost: fewer round trips and fewer billed tokens per completed task.

Benchmarks

On Meta&#8217;s own numbers, Muse Spark 1.3 posts 75.4 on DeepSWE v1.1, ahead of Claude Opus 5 at 74.0 and GPT-5.6 Sol at 72.7. It reaches 59.4 on SWE-Atlas Codebase QnA and ties GPT-5.6 Sol at 88.8 on Terminal-Bench 2.1, with Opus 5 at 86.7. Long-context retrieval is the widest gap: MRCR v2 scores of 98.5 (256K–512K) and 98.1 (512K–1M), against 91.5 and 73.8 for GPT-5.6 Sol.

The mode split matters on agentic rows. Meta reports OSWorld 2.0 at 66.9 for max versus 57.2 for xhigh, GDPval-AA v2 Elo at 1,754 versus 1,709, and JobBench at 64.9 versus 61.2. DeepSearchQA ties at 89.4 for both. Since Muse Spark 1.2 was evaluated at xhigh, part of the generational jump is a reasoning-tier change.

Artificial Analysis scores the shipping xhigh variant at 61 on its Intelligence Index and the preview max variant at 62. That places xhigh level with GPT-5.6 Sol (max) and Grok 4.6 (high), behind Claude Opus 5 (max, 63) and Claude Fable 5.1 (max, 66). Artificial Analysis also measured Tau3-Bench Banking at 47% for xhigh and 52% for max, the top score it has recorded on that evaluation.

Key Takeaways

Muse Spark 1.3 is live in Muse Code and the Meta Model API, with a 1M-token context window.

Meta engineers measured ~20% fewer tool calls and ~25% fewer tokens versus Muse Spark 1.2.

Meta&#8217;s launch scorecard uses the max mode, which is not the mode developers can call today.

Pricing is unchanged at $1.25/M input and $4.25/M output, with a $0.10/$0.20 contributor tier.

Weights stay closed, though Meta lists a Muse Spark open weights release on its roadmap.

Check out the full release post and the evaluation methodology report. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meta AI Released Muse Spark 1.3: An Agentic Coding Model That Uses ~20% Fewer Tool Calls and ~25% Fewer Tokens Than Muse Spark 1.2 appeared first on MarkTechPost.