---
publish_time: 1788726317
link: https://www.marktechpost.com/2026/09/06/meta-fair-introduces-ai-research-preference-models-rpms-ranking-ml-experiments-before-spending-gpu-hours/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Meta FAIR 联合牛津大学、伦敦大学学院提出 AI Research Preference Models（RPMs），用于在耗费 GPU 工时训练候选模型之前，对机器学习实验进行偏好排序。随着 AI 研究智能体已能自行提出、实现并给实验打分，候选方案远多于可负担运行的量，RPMs 通过学习研究者对实验的偏好，在投入算力前筛选高价值候选，把“哪些实验值得跑”变成研究进展的真正杠杆。
---

# Meta FAIR 发布 AI 研究偏好模型（RPMs）

> 原文链接：https://www.marktechpost.com/2026/09/06/meta-fair-introduces-ai-research-preference-models-rpms-ranking-ml-experiments-before-spending-gpu-hours/
> 来源：MarkTechPost

AI research agents can already propose, implement and score their own machine learning experiments. Idea generation is cheap; verification is not. Training one candidate can consume hours to days of GPU time, so an agent proposes far more candidates than it can afford to run. Which ones get run is the real lever on research progress.

A research team from FAIR at Meta, the University of Oxford and University College London formalizes that lever as research preference and introduces AI Research Preference Models (RPMs). An RPM ranks unexecuted candidates and picks one to execute. It never forecasts an absolute score, the team found language models unreliable at predicting metrics or execution outcomes.

Is it deployable? Partially. RPMs use frozen pretrained LLMs with no fine-tuning, the scaffold AIRA-dojo and benchmark AIRS-Bench are open source, and the backbone Qwen3.6-27B is open weights. 

Where the RPM sits in the agent loop

AIRA-dojo is an evolutionary tree search: greedy parent selection, Draft / Improve / Debug operators, highest-validation-score node returned at the end. The RPM intervenes at child creation only. Instead of generating one child and executing it, the agent applies the operator 15 times in parallel to yield 15 unexecuted candidates, then compares them pairwise in a knockout tournament. Only the winner is executed. Each comparison is grounded in context nodes collected by a BFS walk of the explored tree, each shown with the validation score it obtained.

Two variants, two compute budgets

Inference-only RPM: An LLM-as-a-judge over candidate plans, code and search history. Its prompt was optimized with MIPROv2 from DSPy, converging on a principal-investigator rubric that tolerates fixable bugs, rewards extensibility and penalizes redundant directions, offline accuracy 57.7% to 59.0%.

Agentic RPM: The same judge and a sandbox that clones the agent&#8217;s environment, including a single H200. Tools are python, bash and submit_solution. It runs small-scale pilot experiments, then a feedback model either proposes the most informative next experiment or ends the loop. Two design choices carry weight: the remaining budget is deliberately overstated (2,700s reported against a real 300s) so the agent does not stop early, and pilots are capped at 30 with a 60-second threshold. Pilot time competes with the agent&#8217;s own clock, so the agentic selector runs only on Draft and Improve steps; Debug reverts to random.

Results on AIRS-Bench

Setup: 20 public text and tabular tasks, 24 hours on a single H200 per task, 10 seeds, Qwen3.6-27B as backbone for both the operators and the RPM, so the gain comes from the selection layer, not a stronger judge.

Child selectionAvg. normalized scoreNo RPM (random pick)0.684Inference-only RPM0.711Agentic RPM0.729Validation oracle (ceiling)0.748Test oracle (ceiling)0.759

Probability of improvement over No-RPM is 0.5923 and 0.5913, with 95% CI lower bounds at 0.5066 and 0.5018.

Efficiency is the more practical result. Inference-only reaches the baseline&#8217;s final 0.684 in 14.88 hours (1.61×), agentic in 15.50 hours (1.55×). Self-hosted inference adds 0.660 hours per run; adjusting for it still gives 0.708 at 23.34 hours.

Two new reported SOTA results: WinoGrande 94.1% with the Agentic RPM against a prior agentic SOTA of 90.4% from AIRA₂, and SVAMP 95.7% with inference-only against a prior human SOTA of 94.2%.

Key Takeaways

RPMs rank unexecuted candidates so an AI research agent runs only the most promising one.

Two frozen-LLM variants: an inference-only judge, and an agentic judge that runs short pilots.

On AIRS-Bench, average normalized score rises from 0.684 to 0.711 and 0.729.

Both hit the baseline&#8217;s 24-hour score in roughly 15 hours, a 1.5–1.6× speedup.

New reported SOTA on WinoGrande (94.1%) and SVAMP (95.7%).

Check out the Paper and the LinkedIn announcement. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meta FAIR Introduces AI Research Preference Models (RPMs): Ranking ML Experiments Before Spending GPU Hours appeared first on MarkTechPost.