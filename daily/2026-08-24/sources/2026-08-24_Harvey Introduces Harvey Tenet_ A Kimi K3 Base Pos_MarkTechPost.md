---
publish_time: 1787507516
link: https://www.marktechpost.com/2026/08/23/harvey-tenet-post-trained-kimi-k3-legal-agent-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Harvey 发布首个后训练模型 Harvey Tenet（研究预览），以 Kimi K3 为基座、联合 Fireworks 用异步强化学习在长程法律任务上后训练，训练语料含合成/公开/专家数据、未用客户数据。相较基座 K3，Tenet 在 Harvey 法律 Agent 基准（LAB）上完成近两倍留出任务、LAB:Contracts 全通过率分别 +9/+2 个百分点，登顶 LAB:Contracts、居 LAB 第二；能力未训练即迁移至 Mercor APEX 与 Crosby Redline Bench。训练约 150 张 B300 GPU、两月，用 GSPO+rank-64 LoRA，奖励塑造偏好短轨迹使质量与成本同升。Tenet 目前仅发布方法、无权重/API，目标是在开放权重上建前沿法律智能并让律所拥有自有模型。
---

# Harvey 推出 Harvey Tenet：基于 Kimi K3 基座、面向长程法律 Agent 的后训练模型

> 原文链接：https://www.marktechpost.com/2026/08/23/harvey-tenet-post-trained-kimi-k3-legal-agent-model/
> 来源：MarkTechPost

Harvey has released Harvey Tenet, its first post-trained model, as a research preview as of today. Tenet is a Kimi K3 base post-trained with Fireworks through asynchronous reinforcement learning on long-horizon legal work. The training corpus combined synthetic data, publicly available legal data, and human expert data. Harvey states no customer data was used. Against the base K3 model, Tenet completes almost twice as many held-out tasks on Harvey&#8217;s Legal Agent Benchmark (LAB) and 20% more on LAB: Contracts, raising all-pass rate by 9 and 2 percentage points respectively. Harvey reports state-of-the-art on LAB: Contracts and second place on LAB. The gains also transferred, untrained, to Mercor&#8217;s APEX Agents and Crosby&#8217;s Redline Bench. The stated goal is twofold: build frontier legal intelligence on open-weight models, and give law firms a path to own their own specialized models.

Is it deployable?

Not yet, Harvey Tenet is a research preview announced on August 20, 2026. Harvey has not published weights, a model card, or an API endpoint. The base model is open-weight; Tenet itself is Harvey&#8217;s own checkpoint, and the company says the work will move &#8220;from research to production&#8221; inside Harvey&#8217;s products over time. What ships today is the recipe, not the artifact.

Company tier: Enterprise only. Access runs through Harvey&#8217;s platform, which is sold to law firms, mid-sized firms, and in-house legal teams. A lab with an RL stack could reproduce the method; training used roughly 150 NVIDIA B300 GPUs over two months.

Industries: Legal services, corporate in-house legal, private equity and investment banking (M&A diligence), plus regulated sectors where contract volume drives cost — insurance, financial services, healthcare, energy.

Applications: M&A due diligence memos over datarooms, contract drafting, review and redlining, structured extraction across up to 10,000 documents, and precedent search over a firm&#8217;s accumulated knowledge.

What the numbers say

Against the base K3 model, Tenet completes almost twice as many held-out tasks on Harvey&#8217;s Legal Agent Benchmark (LAB) and 20% more on LAB: Contracts, lifting all-pass rate by 9 and 2 percentage points respectively. Harvey reports state-of-the-art on LAB: Contracts and second place on LAB, using base-model scores from Vals.

The more interesting result is transfer. Tenet also improves substantially on Mercor&#8217;s APEX Agents (corporate law) and Crosby&#8217;s Redline Bench — neither seen during training — while holding performance on knowledge benchmarks including LegalBench, CUAD, MAUD, and Scale&#8217;s PRBench. Agentic training did not erode textbook legal reasoning.

Cost is co-optimized rather than traded away. Open weights lower price per token; reward shaping that prefers shorter trajectories at equal quality lowers tokens consumed. Harvey reports significant quality gains at stable cost.

How it was trained

Training used asynchronous reinforcement learning in sandboxed legal environments built like LAB tasks: a partner-style instruction averaging about 50 words, a client matter of key and peripheral documents, and an expert rubric of atomic pass/fail criteria — roughly 50 per task, hundreds at the extreme. A single rollout can exceed 1,000 turns.

Rollouts are graded by LLM-as-a-judge; ablations settled on Kimi 2.6. Reward combines the fraction of rubric criteria satisfied, a holistic count of legal issues solved, and an all-pass bonus. The policy is optimized with GSPO using a rank-64 LoRA over the full K3 network, eight task groups of eight rollouts per optimizer step, across ~1,750 environments and >10,000 rollouts per epoch. Fireworks co-built trainer and rollout deployments at the kernel level, with token-in-token-out and router replay, to keep a large MoE numerically aligned across training and inference. 

&

Three capabilities trained separately

Harvey team also post-trained specialist models that Tenet can route to as tools or sub-agents:

M&A diligence: On LAB: Diligence, a single task can traverse up to 80M tokens; no baseline passed more than 43.8% of criteria. With Baseten, Harvey moved to a Recursive Language Model harness where a root agent holds the dataroom in a REPL and delegates to sub-agents. A GLM-5.2 orchestrator alone reached 46.1%; post-training it in that harness via self-distillation reached 60.1%.

Review Table: With Applied Compute, a post-trained GLM-5.2 improved answer quality by 3.6 points and citation quality by 12.1 points at roughly one-tenth the cost per cell, learning to abstain when a question does not apply.

Firm knowledge: With Engram, a Qwen3.8-27B model studies ~100M tokens of client matters into 1M tokens of structured knowledge plus parametric memory. Criteria pass rate rose more than 15%, tokens in completed trajectories fell 58%, and cost per query dropped roughly 90% — 190.8 intelligence-per-token versus 129.3 for the best frontier configuration.

Key Takeaways

Tenet is a post-trained Kimi K3 checkpoint, not a public open-weight release — no weights, no API.

Gains transferred untrained to APEX Agents and Redline Bench, suggesting learned behavior, not benchmark fitting.

Reward shaping on trajectory length made quality and cost improve together instead of trading off.

The specialist stack — RLM diligence, Review Table, firm memory — is where the largest deltas landed.

Check out the TECHNICAL DETAILS here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Harvey Introduces Harvey Tenet: A Kimi K3 Base Post-Trained with Fireworks for Long-Horizon Legal Agent Work appeared first on MarkTechPost.