---
publish_time: 1794382737
link: https://www.marktechpost.com/2026/11/10/ifm-pan-2-open-world-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MBZUAI 基础模型研究所发布 PAN 2，一个面向物理智能的开源世界模型，输入场景图与文本动作、输出视频模拟结果，权重与训练/推理代码以 Apache 2.0 开源。模型为 29B 参数扩散 Transformer，输出 704×1248、24fps、最长 20 秒视频，供机器人与智能体开发者在行动前于仿真中验证计划。
---

# MBZUAI 发布 PAN 2：29B 参数开源物理世界模型

> 原文链接：https://www.marktechpost.com/2026/11/10/ifm-pan-2-open-world-model/
> 来源：MarkTechPost

The Institute of Foundation Models (IFM) at MBZUAI released PAN 2, an open world model for physical intelligence. The PAN 2 world model takes a scene and a text action and simulates the outcome as video. IFM announced it on X on November 10, 2026. Weights, training code and inference code ship under Apache 2.0. For robotics and agent developers, the pitch is simple: test a plan in simulation before acting on it.

TL;DR

Size: 29B-parameter diffusion transformer (MMDiT), dense. Inputs: text plus an optional first frame. Output: 704&#215;1248 video at 24 fps, up to 20 s.

Runs on: Data-center GPUs. Each worker holds the full 29B model in BF16, with block offloading as fallback. 

Performance: Leads 6 tested models on full plans. Trails MiniMax-H3 on single actions and human preference.

Best: 34.0% full-plan completion on 100 multi-step tasks, the highest of all models tested (self-reported).

Worst: About 2 in 3 plans miss a step. Physics-IQ system default: 37.48 vs 42.91 for MiniMax-H3.

Bottom line: Best: a fully open world model that leads on multi-step plans. Worst: long plans still fail often, and hardware needs are high.

What is PAN 2?

PAN 2 is a general-purpose world model from IFM that simulates how a scene changes after an action. It follows the Generative Latent Prediction (GLP) architecture from IFM&#8217;s Critique of World Models paper. It succeeds PAN, released in November 2025.

The goal is simulative reasoning. An agent proposes plans, PAN 2 simulates each one, and the agent acts on the best.

How does PAN 2 work?

PAN 2 splits simulation into 2 kinds of reasoning:

Conceptual reasoning: An LLM reads the observation and the requested actions. It writes the next world state as structured JSON: events, timed actions bound to actors, and camera motion. Any instruction-following LLM can fill this role. IFM&#8217;s report uses Kimi K3 by default.

Perceptual reasoning: A 29B MMDiT predicts the video latents. IFM trained it from scratch on hundreds of millions of annotated videos. A frozen Qwen3.5-9B text encoder conditions it. The Wan 2.2 VAE decoder renders the final frames.

IFM&#8217;s ablation shows the LLM matters. With no conceptual reasoning, full-plan completion drops from 34.0% to 0.0%. Step completion falls from 75.1% to 8.7%. A format-only rewrite recovers part of the gap, reaching 27.8% full-plan completion.

IFM also dropped gameplay, animation and simulation footage after early training. A 9B test model trained without it won 58% of blinded votes.

How does PAN 2 perform on benchmarks?

All numbers below are self-reported by IFM. Its own test suite covers 6 capabilities across 300 single-action cases, plus 100 multi-step tasks.

Full-plan completion: 34.00% vs 32.50% for MiniMax-H3, 26.77% for FLUX 3 and 24.49% for Seedance 2.5.

Step completion: 75.10%, level with MiniMax-H3 at 75.12%.

6 capabilities overall: 84.48% vs 87.20% for MiniMax-H3. MiniMax-H3 leads in all 6 categories.

Physics-IQ Verified (leaderboard setting): 49.38, first among open models. Closed FLUX 3 scores 51.11.

RBench: 57.04 vs 56.16 for MiniMax-H3 and 50.64 for Cosmos 3 Super.

Human Elo: 1595 with a GPT-6 Astra reasoner, behind MiniMax-H3 at 1620.

PAN 2 vs MiniMax-H3, Cosmos 3 Super and LTX-2.5

FeaturePAN 2MiniMax-H3Cosmos 3 SuperLTX-2.5DeveloperIFM (MBZUAI)MiniMaxNVIDIALightricksGenerator size29B MMDiT33B dense transformer (~13B in cacheable AdaLN branches)64B Mixture-of-Transformers22B transformer (per checkpoint file names)Planner / encoderAny LLM + frozen Qwen3.5-9B encoderQwen3-VL-32B encoder; hosted Context-IRBuilt-in autoregressive towerGemma-based text encoderMax clip20 s, 704&#215;1248, 24 fps15 s, 24 fps, 768p (2K via hosted module)400 framesNot disclosedAudioNoYes, stereoYesYesLicenseApache 2.0MiniMax H3 Community LicenseOpenMDW 1.1LTX-2.x Community LicenseTraining codeYesNot disclosedFramework on GitHubNot disclosedFull-plan completion*34.00%32.50%13.83%13.00%Physics-IQ Verified (leaderboard)*49.3839.7948.62Not reportedHuman Elo*1595162013801346

*Scores from IFM&#8217;s PAN 2 model card, run by IFM. The blog reports different Cosmos 3 Super and LTX-2.5 plan scores.

How do you run PAN 2?

PAN 2 supports text-to-video and image-to-video. You can run it through Hugging Face Diffusers, vLLM, FastVideo or the repo&#8217;s generate.py.

The default sampler uses 50 steps, flow shift 9 and guidance 2.5. A clip defaults to 241 frames, about 10 seconds. Each GPU worker loads the full 29B model in BF16. IFM publishes no VRAM figure or generation time.

Prompts work best as structured captions. IFM ships a Conceptual Reasoner skill for Claude Code and Codex that rewrites free text. Captions have a hard budget of 1,536 tokens.

IFM strongly recommends the separate pan2-guardrail. In IFM tests, it cut unsafe outputs from harmful T2V requests from 33.9% to 1.5%. It also blocked 11.5% of benign T2V requests.

Key Takeaways

PAN 2 pairs an LLM planner with a 29B diffusion model trained from scratch.

It leads 6 tested models on full-plan completion at 34.0%.

MiniMax-H3 still wins single actions and human preference.

Weights, training and inference code are Apache 2.0.

Removing the LLM planner drops full-plan completion to 0%.

Check out the model weights, GitHub repo, technical blog and press release. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post MBZUAI&#8217;s IFM Releases PAN 2, an Open 29B World Model for Physical AI appeared first on MarkTechPost.