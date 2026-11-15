---
publish_time: 1791263521
link: https://www.marktechpost.com/2026/10/05/beyond-domain-specific-world-models-jepa-anything-uses-1-recipe-for-7-fields/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  PhAI Labs、港中文、复旦、斯坦福、牛津、普林斯顿等机构联合发布 JEPA-Anything，一个领域无关的世界模型构建框架。它将联合嵌入预测架构（JEPA）扩展为正交预测分解（OPF），用同一套学习“配方”适配视觉、生物、临床轨迹、控制、分子动力学、物理场与天气等七个差异巨大的领域。OPF 将 latent 目标分解为 K 个正交子空间并各配专用预测器，配合正交性、因子活性、编码器方差三项正则，解决了标准 JEPA 的“容量分配”问题。实验显示其在 10 个动力学任务上全部超越对照 JEPA，单干预误差降 34.83%，并开源 Apache-2.0 核心代码与 HF 检查点。
---

# JEPA-Anything：一套方法覆盖七领域的通用世界模型框架

> 原文链接：https://www.marktechpost.com/2026/10/05/beyond-domain-specific-world-models-jepa-anything-uses-1-recipe-for-7-fields/
> 来源：MarkTechPost

Researchers from PhAI Labs, CUHK, Fudan, Stanford, Oxford and Princeton have released JEPA-Anything, a domain-agnostic framework for building world models. Instead of designing a new predictive model for each field, it applies one shared learning recipe to very different systems. It extends joint-embedding predictive architectures (JEPAs) with a method called Orthogonal Predictive Factorization (OPF). The research team tested it across 7 domains: vision, biology, clinical trajectories, control, molecular dynamics, physical fields and weather.

What problem does JEPA-Anything solve?

A standard JEPA, such as I-JEPA or V-JEPA 2, uses a context encoder, an EMA target encoder and one predictor. The predictor outputs one monolithic target embedding. The research team call this a capacity-allocation problem: high-variance structure dominates, and weaker modes get conflicting gradients.

How does Orthogonal Predictive Factorization work?

OPF splits the latent target of width d into K learned subspaces of width r, with d = K × r. Most experiments use K = 4. Each factor gets a dedicated predictor. The factor predictions are then recombined through the Moore-Penrose pseudoinverse of the projector matrix. The result is 1 complete latent state for decoding, planning or rollout.

Three regularizers keep the factors useful:

Orthogonality loss: keeps columns within each projector orthonormal and different projectors in non-overlapping subspaces.

Factor-activity loss: a hinge on per-coordinate standard deviation so no factor goes dead.

Encoder-variance loss: sends a direct anti-collapse signal to the online encoder.

The OPF loss is simply added to each domain&#8217;s original training loss. Domain adapters handle tokenization and encoders; the core library exposes the shared core as OrthogonalFactorProjection.

Orthogonality matters for stable synthesis. On CITRIS Interventional Pong, a capacity-matched unconstrained multi-head model had a condition number of 438.52. The orthogonal version reached 1.00005, with cross-factor overlap near zero.

&&

What results does the research report?

Group I, terminal readout: On single-cell data, zero-shot PBMC clustering (AvgBIO) rose to 0.7752 versus 0.7194 for Cell-JEPA. Norman perturbation Pearson rose from 0.787 to 0.814. For forecasting over 1,000 clinical events on UK Biobank data, mean PRAUC was 0.718 versus 0.711 for the matched standard JEPA.

Group II, latent world dynamics: On Interventional Pong, single-intervention MSE fell 34.83%. Unseen combined interventions improved 12.90%, and 6-step free rollout improved 8.58%. JEPA-Anything improved reported metrics on all 10 matched dynamics tasks. Benchmarks include CausalWorld, DeepMind Control, PDEBench and WeatherBench2. On APEBench Burgers, 6-step rollout error dropped about 44.7%, improving in every seed. For 100-step molecular rollouts with a TrajCast-style backbone, it posted the lowest MAE and RMSD on water, quartz, paracetamol and benzene.

Planning results are mixed. With parameters matched within 0.3%, JEPA-Anything improved CEM return on Walker2d and HalfCheetah. Hopper favored standard JEPA.

Group III, scientific analysis: Factor analysis nominated IL-18 plus CD73 blockade as a cancer intervention. Wet-lab tests supported it in co-cultures, patient-derived organoids, tumor fragments and mice. Latent orbital modes also recovered Kepler&#8217;s law with a fitted slope of −1.4991 against the theoretical −1.5.

How does JEPA-Anything compare with other world models?

FeatureJEPA-AnythingV-JEPA 2DINO-WMDreamerV3TD-MPC2Core ideaJEPA with K orthogonal predictive factorsVideo JEPA plus action-conditioned V-JEPA 2-ACWorld model on pretrained visual featuresWorld model plus actor-critic trained in imaginationDecoder-free latent dynamics plus MPCTarget structureFactorized, recombined via pseudoinverseSingle latent targetSingle latent targetCategorical latent statesSingle latent stateDomains shown7: vision, cells, clinical, control, molecules, PDEs, weatherVideo understanding, robot manipulationPointMaze, PushT, Wall, deformablesDiverse RL domains, fixed hyperparameters104 continuous-control tasks, 4 domainsPlanning / rolloutLatent rollout, CEM planningPlanning from image goalsCEM planningPolicy from imagined rolloutsMPC planningPublic checkpointsPer-domain research checkpoints on HFYes, 300M to 1B (V-JEPA 2)PointMaze, PushT, WallNot listed in repo300+ checkpoints, up to 317MLicenseApache-2.0MIT (some files Apache-2.0)MITMITMIT

Sources: each project&#8217;s GitHub README, linked in the header row. JEPA-Anything checkpoint status from its Hugging Face card. Verified October 5, 2026.

Key Takeaways

OPF splits 1 JEPA target into K orthogonal factors with dedicated predictors.

It beat matched JEPA baselines on all 10 dynamics tasks.

Interventional Pong single-intervention error fell 34.83%.

Planning gains are environment-dependent; Hopper favored standard JEPA.

Core code is Apache-2.0; research checkpoints sit on Hugging Face.

Check out the Paper, GitHub Repo and Model Checkpoints. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Beyond Domain-Specific World Models: JEPA-Anything Uses 1 Recipe for 7 Fields appeared first on MarkTechPost.