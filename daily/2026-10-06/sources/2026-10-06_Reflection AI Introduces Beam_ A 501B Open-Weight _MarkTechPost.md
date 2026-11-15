---
publish_time: 1791234260
link: https://www.marktechpost.com/2026/10/05/reflection-ai-introduces-beam-a-501b-open-weight-moe-model-with-23b-active-parameters-for-coding-and-agentic-workloads/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Reflection AI 发布首款开源权重模型 Beam：一个 501B 总参数、23B 激活参数的稀疏 MoE 模型，专注编程、推理与智能体负载，以“西方开源前沿”定位对标 GLM 5.2 等更大模型，宣称以 3–4 倍更少的推理算力取得相近基准。Beam 预训练于 23.8T token（6,144 张 GB300 上不到 4 周完成），RL 阶段在 10.5K 张 GB300 上生成超 1 亿次 rollout，SWE-bench Verified 达 80.9、Terminal Bench v2.1 达 80.1。采用异步策略梯度、可调控长度惩罚，Apache 2.0 权重计划本月晚些时候开放。
---

# Reflection AI 发布 Beam：501B 参数开源 MoE 模型，专注编程与智能体

> 原文链接：https://www.marktechpost.com/2026/10/05/reflection-ai-introduces-beam-a-501b-open-weight-moe-model-with-23b-active-parameters-for-coding-and-agentic-workloads/
> 来源：MarkTechPost

Reflection AI has introduced Beam, its first open-weight model. Beam is a sparse Mixture-of-Experts (MoE) model with 501B total parameters and 23B active per token, built for coding, reasoning and agentic workloads. As per the Reflection AI team, Beam directly competes with larger open models like GLM 5.2 while using 3 to 4x less inference compute on reasoning benchmarks. 

Is it deployable today? Not for self-hosting yet. Beam is in final red-teaming. Early access runs through a waitlist on the Reflection platform. 

What is Reflection Beam?

Beam is a general agent model trained from scratch by Reflection AI. It targets enterprise coding and agentic workloads. Reflection positions Beam as advancing the Western open-weight frontier. The research team is candid about the gap. Kimi K3 stays ahead on raw capability, so Beam&#8217;s pitch is efficiency at inference time.

Users get a reasoning effort parameter. Lower settings favor short answers. Higher settings allow longer reasoning on hard tasks. Teams can match effort to task difficulty and compute budget.

How Beam was Pretrained

Beam was pretrained on 23.8 trillion tokens from the web, public sources and proprietary licensed datasets. Reflection team states that its curation removed about 95% of raw internet tokens. It also kept roughly 1.8 trillion high-quality tokens that conventional filters would have dropped.

The architecture interleaves local and global attention with fine-grained routed experts. Load balancing builds on auxiliary-loss-free balancing from DeepSeek-V3, adding cosine decay of expert-bias updates. The busiest expert reached just 1.04x average load at the end of pretraining. Across all 52 layers, residual norms stayed bounded using depth-based scaling, SandwichNorm, attention gating and FP32 residual accumulation.

Pretraining finished in under 4 weeks on 6,144 NVIDIA GB300 NVL72 GPUs. Goodput reached 92.3% near the end, with 9 semi-automatic rewinds. Midtraining extended effective context to 1M tokens.

High-Compute Reinforcement Learning

RL is Beam&#8217;s central scaling axis. The run used 10.5K NVIDIA GB300 GPUs for 4 weeks and generated over 100 million rollouts. Maximum rollout context was 256K tokens. Training and grading consumed about 1.3 billion sandboxes across nearly 1 million coding, agentic and STEM environments.

Reflection trained with fully asynchronous policy gradients. Every token is tagged with the policy version that produced it. New algorithms kept learning stable even at one-day staleness, 107 weight versions behind the current policy. The team reports no plateau as RL compute increased.

Infrastructure numbers are notable. The system sustained 110K concurrent rollouts on average. New weights reached the inference fleet in a median of about 12 seconds. 71 inference incidents were handled without stopping training.

A controllable length penalty taught Beam to solve tasks with fewer tokens. Browsing skills also improved without browsing tasks in the RL mix, which suggests transfer across agentic domains.

Safety and Alignment

Reflection trained a separate safety and alignment teacher from the pretrained checkpoint. It merged that teacher with the RL teacher using multi-teacher on-policy distillation. Safety training used deliberative alignment. Safety evaluation results will appear in the technical report.

Benchmarks (Reflection-Reported)

On SWE-bench Verified, Beam scores 80.9 versus 70.7 for Nemotron 3 Ultra. On Terminal Bench v2.1, Beam scores 80.1, close to GLM 5.2 at 81.0. DeepSeek V4.1 Flash (90.6) and Kimi K3 (88.3) lead there. These numbers come from Reflection&#8217;s table, which sources rival scores from Artificial Analysis and DataCurve.

Beam vs Closest Open-Weight Competitors

FeatureReflection BeamGLM-5.2Nemotron 3 UltraDeepSeek V4.1 FlashKimi K3DeveloperReflection AI (US)Z.ai (China)NVIDIA (US)DeepSeek (China)Moonshot AI (China)Total params501B~753B550B552B backbone + 196B Engram2.8TActive params23B~40B55B8B prefill / 16B decode104BContext1M (effective)1MUp to 1M1M1MInputTextTextTextText + imageText + imageLicenseApache 2.0 (planned)MITOpenMDW-1.1MITKimi K3 LicenseWeightsLater in Oct 2026AvailableAvailableAvailableAvailableTerminal Bench v2.1*80.181.056.490.688.3SourceReflectionHugging FaceNVIDIAHugging FaceHugging Face

*Scores as published in Reflection&#8217;s Beam announcement. Specs verified October 5, 2026.

Beam is the smallest model here by total parameters. Its 23B active count sits below GLM-5.2, Nemotron 3 Ultra and Kimi K3. Apache 2.0 and MIT are standard permissive licenses. Kimi K3&#8217;s custom license adds attribution requirements for very large products.

&

Key Takeaways

Beam is a 501B MoE with 23B active parameters, text-only, and 1M effective context.

Pretraining used 23.8T tokens on 6,144 NVIDIA GB300 GPUs in under 4 weeks.

RL ran 100M+ rollouts on 10.5K GB300 GPUs over 4 weeks.

Reflection reports 80.9 on SWE-bench Verified and 80.1 on Terminal Bench v2.1.

Apache 2.0 weights are scheduled for later this month.

Check out the Technical details and Early Access.

The post Reflection AI Introduces Beam: A 501B Open-Weight MoE Model With 23B Active Parameters for Coding and Agentic Workloads appeared first on MarkTechPost.