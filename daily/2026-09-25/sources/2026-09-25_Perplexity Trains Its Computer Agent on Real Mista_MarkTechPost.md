---
publish_time: 1790346626
link: https://www.marktechpost.com/2026/09/25/perplexity-trains-its-computer-agent-on-real-mistakes-with-hint-guided-self-distillation/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Perplexity Research 发布一项训练研究：在 Perplexity Computer 内部用真实用户会话（含失败会话）训练模型，方法结合拒绝采样微调（RFT）与提示引导自蒸馏（hint-guided self-distillation）。其关键在于不只模仿成功轨迹——成功不代表每步都对，而把错误回合用带验证提示的 KL 散度损失“纠正”。线上 A/B 显示，两个训练检查点间工具调用失败率从 2.24% 降至 1.77%，相对下降 21.2%（统计显著）。权重与训练代码未开源，仅作为 Perplexity Computer 内模型选项，底座 GLM 5.2 已公开。
---

# Perplexity用真实错误训练计算机智能体（提示引导自蒸馏）

> 原文链接：https://www.marktechpost.com/2026/09/25/perplexity-trains-its-computer-agent-on-real-mistakes-with-hint-guided-self-distillation/
> 来源：MarkTechPost

Perplexity Research published a new post-training study. It trains a model inside Perplexity Computer on real user sessions, including failed ones. The method pairs rejection sampling fine-tuning with hint-guided self-distillation. In a live A/B test, tool-call failures fell from 2.24% to 1.77% between 2 trained checkpoints. Perplexity team reports this as a statistically significant 21.2% relative reduction.

Is it deployable? Not directly. Perplexity has not released the post-trained weights or training code. The model runs only as a model option inside Perplexity Computer. The base model, GLM 5.2, is openly available on Hugging Face.

Why Outcome-Only Filtering Falls Short

Standard rejection sampling fine-tuning (RFT) judges each session and imitates only the successful ones. A successful outcome does not mean every step was correct. An agent can recover from a bad tool call and still deliver the right answer. Imitating that full trajectory can reinforce the error. Discarding failed sessions also throws away clear evidence of avoidable mistakes.

Imitate, Correct, or Keep as Context

Perplexity team separates 2 decisions: which sessions hold behavior worth imitating, and which turns hold mistakes worth correcting. 

Each assistant turn gets 1 of 3 treatments:

Imitate: non-error turns in successful sessions receive cross-entropy (CE) loss.

Correct: error turns with a validated hint receive Kullback-Leibler (KL) divergence loss, in any session.

Keep as context: remaining turns stay in the input but receive no loss.

Successful sessions can supply both imitation and correction targets. Unsuccessful sessions supply only correction targets.

How a Hint Becomes a Training Signal

A hint is a short corrective instruction grounded in information the model already had. In one example, a search call set recency_filter to &#8216;year.&#8217; The schema allowed only &#8216;day,&#8217; &#8216;week,&#8217; or &#8216;month.&#8217; The hint names the failed call, includes the validation error, and suggests an allowed value or omitting the optional field.

The corrective part uses On-Policy Self-Distillation (OPSD). The trainer runs the same GLM 5.2 checkpoint twice on the recorded turn. The teacher pass sees the hint; the student pass does not. Both use teacher forcing, so no replacement answer is generated. The teacher&#8217;s next-token probabilities are detached and act as a soft target through forward KL.

The combined loss is (CE + λ × KL), divided by the number of imitated tokens. Setting λ to 0 recovers standard SFT. The CE term matters. Correction-only training can let teacher and student agree by ignoring context.

Tracing Complaints to the Real Mistake

The pipeline draws from training-eligible Computer sessions served by GLM 5.2. Sessions with personally identifiable information and users who opted out are excluded. An LLM judge keeps tasks rated 4 or 5 on a 5-point difficulty scale. Two LLM judges must both approve the final delivery for a session to count as successful.

For user feedback, threes LLM judges locate the responsible turn, and at least 2 must agree. This is important because the last assistant turn before a complaint is the root cause only about half the time. Each hint is also checked against information available before the mistake. That check reduces hindsight bias.

One example: a user asked for their &#8216;w3&#8217; on Paychex. The model assumed a W-2 typo and searched for the wrong form. The hint targets that earlier interpretation, not just the final answer.

Interactive Explainer

&&

What the Evaluations Show

Hints work before training: On 985 held-out tool-error turns, the unchanged base model avoided the original failure in 93.7% of cases with hints, up from 75.1%. The share taking the corrected action rose from 60.6% to 82.3%. On user-feedback turns, fixed or on-track rates rose from 40.0% to 75.0% for explicit evidence. For inferred intent, they rose from 32.5% to 80.0%.

Offline tool errors fell: Recorded tool-error rates were 2.79% for stock GLM 5.2 and 1.35% for RFT only. The RFT plus OPSD checkpoint reached 0.87%. Perplexity notes these checkpoints used different training data, so this is not a matched ablation. Task-level benchmark results on suites like BrowseComp and SpreadsheetBench were mixed.

Live results are narrower: Each A/B test used about 100,000 users per condition. An early checkpoint versus stock GLM 5.2 showed 2.82% versus 2.94% failures, which was not significant. The later checkpoint comparison produced the significant 21.2% drop, without hints at inference. Strong dissatisfaction moved from 2.58% to 2.54%, which was also not significant. Perplexity did not compare the later checkpoint directly against stock GLM 5.2 online.

Key Takeaways

Perplexity learns from failed sessions, not just successful ones.

Validated hints turn avoidable mistakes into KL correction targets.

1 model acts as teacher (with hint) and student (without).

Live tool-call failures fell from 2.24% to 1.77%.

User dissatisfaction showed no significant change.

Check out the Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Perplexity Trains Its Computer Agent on Real Mistakes With Hint-Guided Self-Distillation appeared first on MarkTechPost.