---
publish_time: 1792644991
link: https://www.marktechpost.com/2026/10/21/perplexity-jolt-joint-on-policy-learning-teaching/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Perplexity 与 NVIDIA 团队提出 JOLT（Joint On-policy Learning and Teaching），一种语言模型后训练方法，基于 OPSD（在线策略自蒸馏）。它用单个共享模型同时扮演师生两角：教师持有特权信息，并依据结果奖励加 KL 约束进行训练，使其反馈始终贴近学生；学生仅见任务，从教师的 token 级蒸馏信号学习。JOLT+ 再叠加学生自身的结果奖励。
  
  在 MATH 上，JOLT 以少 6.5 倍的处理训练 token 达到与 GRPO 相当的准确率；JOLT+ 在 GSM8K、MATH、LiveCodeBench、AppWorld、Terminal-Bench 等所有设定中均取得最高均分，AppWorld 上比 GRPO 高 9.9 个百分点（论文已发布于 arXiv，代码尚未开源）。
---

# Perplexity 与 NVIDIA 研究者提出 JOLT：联合在线策略学习与教学的方法

> 原文链接：https://www.marktechpost.com/2026/10/21/perplexity-jolt-joint-on-policy-learning-teaching/
> 来源：MarkTechPost

Perplexity, along with NVIDIA team, has introduced JOLT, a new post-training method for language models. JOLT stands for Joint On-policy Learning and Teaching. It trains a single model in 2 roles. The teacher sees privileged information; the student does not. The key change is that the teacher is trained too, so its feedback stays usable. On MATH, JOLT matched GRPO&#8217;s accuracy with 6.5x fewer processed training tokens. For teams running RL post-training, that is a direct compute question.

TL;DR

What it is: a post-training method.

Size: tested on Qwen3-0.6B, Qwen3-4B-Instruct, Qwen3-8B, Qwen3-30B-A3B-Instruct and DeepSeek-V2-Lite.

Runs on: 1 shared model plays both roles, so no separate teacher model. Training hardware: Not disclosed.

Performance: JOLT+ posts the highest mean score in every setting tested against GRPO, OPSD and π-Distill.

Best: AppWorld state-test pass rate of 72.09% with JOLT+, vs 62.20% for GRPO (+9.9 points).

Worst: JOLT without student reward scores 51.92% on AppWorld, below GRPO.

What is Perplexity JOLT?

JOLT is a self-distillation method from Perplexity and NVIDIA that trains one model as teacher and student. It builds on On-Policy Self-Distillation (OPSD).

Why does RL post-training need a better teacher?

Outcome-reward RL, such as GRPO, gives one reward per attempt. That signal is sparse. It does not say which tokens helped. On long agentic tasks, successes are rare, so learning is slow.

On-Policy Distillation fixes sparsity by having a stronger teacher score each student token. OPSD removes the separate teacher. The same model becomes the teacher when given privileged context, such as a verified solution.

The research team argues this is not enough. A teacher holding the answer can take shortcuts the student cannot follow. Its guidance may sit beyond the student&#8217;s reach. In the paper, OPSD&#8217;s teacher-student disagreement grows during MATH training.

How does JOLT work?

JOLT trains both roles of one shared model at the same time:

Teacher: gets privileged information. It learns from outcome rewards, plus a KL penalty that keeps it close to the student.

Student: sees only the task. It learns from the teacher&#8217;s token-level distillation signal on its own attempts.

On-policy: each role learns from trajectories generated under its own context.

JOLT+: adds the student&#8217;s own outcome reward to the student update.

The research stands in the center on a &#8216;reward-consistent&#8217; teacher. Its distillation update should point the same way as the student&#8217;s reward gradient. The ideal teacher favors high-advantage actions while staying near the student&#8217;s policy. 

&&

How does JOLT perform on benchmarks?

The research team tested 5 settings, each with a different base model and type of privileged information:

GSM8K: DeepSeek-V2-Lite; teacher gets the verified answer.

MATH: Qwen3-0.6B; teacher gets worked reference solutions.

LiveCodeBench v6: Qwen3-8B on 131 problems; teacher gets a passing sibling solution or execution feedback.

AppWorld: Qwen3-4B-Instruct; teacher gets summaries of past attempts.

Terminal-Bench 2.1: Qwen3-30B-A3B-Instruct trained on TMax; teacher gets private verifier files.

JOLT+ had the highest mean score in every setting. Against GRPO, the strongest baseline, it gained 1.5 points on GSM8K. It also gained 4.2 on MATH, 3.0 on LCBv6 and 9.9 on AppWorld. On Terminal-Bench 2.1, JOLT+ reached 10.96% pass@1 and 34.83% pass@32. GRPO scored 8.25% and 30.34%.

Even plain JOLT, with no student reward, beat GRPO on MATH: 72.14% versus 68.36%.

How much training compute does JOLT save?

On MATH, the research team fit accuracy curves against training-token budgets. At 63.44% accuracy, GRPO&#8217;s checkpoint used 8.40M processed training tokens. JOLT&#8217;s fitted curve needed 1.30M, a 6.5x reduction. Counting completion tokens only, the gap widens to about 13x. Across 55% to 65% accuracy targets, savings range from 4.3x to 7.4x on processed tokens.

JOLT also levels off higher. It plateaus near 72%, against about 70% for GRPO and 62% for OPSD.

How does JOLT compare with GRPO, OPSD and π-Distill?

All scores below come from Perplexity&#8217;s own runs in the JOLT paper, with hyperparameters tuned per method. Method descriptions link to each method&#8217;s own paper.

FeatureJOLTJOLT+GRPOOPSDπ-DistillSeparate teacher modelNoNoNo teacherNo (self-teacher)No (shared model)Teacher is trainedYes (reward + KL to student)Yes (reward + KL to student)Not applicableNoYes (KL-regularized)Student signalDense distillation, on-policyDistillation + outcome rewardGroup-relative outcome rewardDense distillation, on-policyOff-policy, teacher trajectoriesMATH, Qwen3-0.6B (%)72.14 ± 0.9072.59 ± 1.1768.36 ± 3.7361.20 ± 2.1042.25 ± 1.10LCBv6, Qwen3-8B (%)47.64 ± 1.1049.08 ± 0.4146.13 ± 1.8345.34 ± 1.5038.23 ± 1.72AppWorld, Qwen3-4B (%)51.92 ± 5.3072.09 ± 6.0162.20 ± 2.8329.49 ± 2.4859.85 ± 2.97Terminal-Bench 2.1 pass@1 (%)6.5610.968.252.824.99Terminal-Bench 2.1 pass@32 (%)25.6934.8330.3416.9022.31CodeNot yet releasedNot yet releasedNot disclosedGitHubNot disclosed

Terminal-Bench base model: 5.18% pass@1, 22.81% pass@32.

Key Takeaways

1 model plays teacher and student, and the teacher is trained too.

6.5x fewer processed tokens than GRPO at matched MATH accuracy.

JOLT+ beats GRPO by 9.9 points on AppWorld.

Plain JOLT still trails GRPO on AppWorld and Terminal-Bench.

Check out the paper on arXiv and the Perplexity research blog post. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Perplexity and NVIDIA Researchers Introduce JOLT: a Joint Teacher-Student Reinforcement Learning Method appeared first on MarkTechPost.