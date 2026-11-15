---
publish_time: 1790753554
link: https://www.marktechpost.com/2026/09/30/nvidia-researchers-introduce-physis-lang-self-evolving-physical-language-that-lifts-cosmos-3-past-veo-3-1-on-physics-benchmarks/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  NVIDIA、MIT与牛津团队提出Physis-Lang，将物理语言作为共享、可优化的表示，同一文本驱动数据筛选、模型训练与推理，用于提升视频世界模型的物理一致性。在2026年9月29日Physics-IQ Verified榜单上，Cosmos3-Super以48.2±1.4排名第一，Cosmos3-Nano以43.3±1.5第二，均超越Veo 3.1。论文与框架方法已公开（代码/权重尚未发布，当前为 Paper only），定位为自演化物理语言。
---

# NVIDIA 团队提出 Physis-Lang：自演化物理语言，助力 Cosmos 3 超越 Veo 3.1

> 原文链接：https://www.marktechpost.com/2026/09/30/nvidia-researchers-introduce-physis-lang-self-evolving-physical-language-that-lifts-cosmos-3-past-veo-3-1-on-physics-benchmarks/
> 来源：MarkTechPost

Video world models can render convincing clips that still break physics. Butter spreads like paint. Balls pass through walls. A team from NVIDIA, MIT and the University of Oxford argues the fix can come from language itself, not from extra visual, latent or numerical signals.

Their framework, Physis-Lang, treats physical language as a shared, optimizable representation. The same text drives data curation, model training and inference. On the public Physics-IQ Verified leaderboard snapshot dated September 29, 2026, Physis-Lang on Cosmos3-Super ranks first at 48.2 ± 1.4. The Cosmos3-Nano version ranks second at 43.3 ± 1.5. 

A video world model can make a convincing clip and still get the physics wrong.

Our researchers just released Physis-Lang, an open self-evolving framework that adds physics reasoning to video captions. The captions explain why and how a scene unfolds. We use them to fine-tune… pic.twitter.com/agIHuIB6N2
&mdash; NVIDIA AI (@NVIDIAAI) September 29, 2026

What Problem Does Physis-Lang Solve?

Conventional captions describe what happens, not why. &#8216;Butter melts as the temperature rises&#8217; says nothing about heat transfer or gravity. Physis-Lang adds a physics_reasoning field to each base caption. It spells out entities, causes, interactions, governing principles, temporal evolution and effects.

The pipeline also writes a scene-specific physics_negative_prompt. This text describes likely implausible outcomes, such as a stone floating on water. It acts as negative conditioning at inference time.

How Does the Self-Evolving Caption Loop Work?

The loop keeps the captioner frozen and evolves only its instruction. A GPT-5.5 captioner writes captions for a fixed 20-video development set with 273 human-verified assertions. Gemini-3.1-Pro acts as a physics-aware critic. An evolution agent reads the scores and claim-level failures, then rewrites the prompt.

The critic scores 2 dimensions:

Precision: the caption is split into atomic claims, and each claim is checked against the video.

Recall: each human-curated physical assertion must be explicitly stated or entailed by the caption.

Every revised prompt is validated on PhysCapBench, a new benchmark of 246 videos and 3,794 human-verified assertions. Caption F1 rose from 78.64 at iteration 1 to 87.82 at iteration 9. The path was not smooth. Iteration 2 made captions overly cautious and dropped F1 to 76.28. Iteration 9 required every visible causal step and raised frame sampling from 2 fps to 4 fps.

How Does Language-Guided Data Curation Work?

A GPT-5.5 diagnosis agent maps generated-video failures to physics categories like rigid-body motion, collision and fluid dynamics. That deficiency profile is matched against physics tags on a large video gallery. Retrieval targets physical content, not visual appearance.

The final training set holds 183K videos: 71K filtered from WISA-80K plus 112K retrieved clips. Retrieval alone added 3.01 points on average across 3 benchmarks. On VideoPhy-2, chemical and thermal processes each gained 8.00 points.

&

How Does Physis-Lang Compare With Veo 3.1?

Fine-tuning uses LoRA on attention projections, with no architecture or objective change. Physis-Lang on Cosmos3-Nano versus Google's Veo 3.1:

PhyGenBench: 71.04 vs 65.63

Physics-IQ Verified: 43.41 vs 34.99

PhyGround: 69.90 vs 69.24

VideoPhy-2: 68.02 vs 68.87 on the full set, 62.36 vs 58.43 on the Hard split

Gains hold across backbones: +7.05 on Wan2.1-14B, +3.24 on Cosmos3-Edge-4B, +6.22 on Cosmos3-Nano-16B and +5.02 on Cosmos3-Super-64B. General quality held steady on VBench-I2V, where Cosmos3-Nano moved from 88.32 to 88.69.

Prompting alone also helps. Physics reasoning plus negative prompts lifted a frozen Cosmos3-Nano on PhyGenBench from 61.67 to 67.29.

Can It Run Without Commercial APIs?

The research team distilled the GPT pipeline into 2 Qwen3-VL-4B-Instruct models: PhysThinker-C for captioning and PhysThinker-U for prompt upsampling. On Wan2.1-14B, the commercial pipeline gave +7.05 at about $24.12K in API cost. Swapping in PhysThinker-C kept +6.76 at about $0.12K. A fully local setup cost $0 and still added +4.76.

Physis-Lang vs Closest Competitors

FeaturePhysis-LangPhiZeroPhyGDPOSelf-RefinementDeveloperNVIDIA, MIT, OxfordCASIA (NLPR)Meta (ECCV 2026)Liu et al.Core ideaSelf-evolving natural-language physics captions and negative promptsLearned discrete "physical language", reason-then-renderGroupwise DPO with VLM physics rewardsMultimodal chain-of-thought prompt refinement from VLM feedbackWhere physics entersData curation, training captions and inference promptsQwen3-VL-4B reasoner feeding a diffusion decoderPreference training on PhyVidGen-135KInference prompts onlyTraining neededLoRA SFT (prompt-only mode also helps)YesYes (DPO)No, training-freePhysics-IQ Verified43.4140.91n/r27.20PhyGenBench71.04n/r48.9649.17VideoPhy-2 (All / Hard)68.02 / 62.36n/r59.56 / 44.9447.88 / 28.09PhyGround69.9057.85n/r58.22Code / weights publicPaper only"Coming soon""Released soon"Paper

Scores are from the Physis-Lang paper, Tables 1 to 4, run under one protocol per benchmark (PhyGenBench and VideoPhy-2 use a GPT-5.5 evaluator). Physis-Lang numbers use the Cosmos3-Nano backbone. n/r = not reported in that comparison. Release status checked September 30, 2026.

Key Takeaways

Physis-Lang evolves physics captions with a critic-guided agent while the captioner stays frozen.

PhysCapBench scores captions on 3,794 human-verified cause, law and effect assertions.

Cosmos3-Nano with Physis-Lang beats Veo 3.1 on 3 of 4 benchmarks.

Physics prompts alone lift a frozen model by 5.62 points on PhyGenBench.

No code or weights are public yet; only the paper is released.

Check out the Paper, Project Page and GitHub Repo. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Researchers Introduce Physis-Lang: Self-Evolving Physical Language That Lifts Cosmos 3 Past Veo 3.1 on Physics Benchmarks appeared first on MarkTechPost.