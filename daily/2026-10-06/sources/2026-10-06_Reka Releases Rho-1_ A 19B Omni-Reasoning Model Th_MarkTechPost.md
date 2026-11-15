---
publish_time: 1791269131
link: https://www.marktechpost.com/2026/10/05/reka-releases-rho-1-a-19b-omni-reasoning-model-that-understands-generates-video-and-outputs-robot-actions-in-one/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Reka 发布 19B 全能推理模型 Rho-1 的研究预览：单一神经网络统一理解并生成文本、图像、视频，还能推理并直接输出机器人动作，意图替代在多模态专家模型间传递任务的 agentic 流水线。架构上每个 transformer 块含“理解”与“生成”两条专家权重流，共享注意力与同一 KV cache；离散 token 承载文本与高层指令，连续 token 承载图像潜变量、视频帧与机器人动作。Rho-1 视频生成约 0.79 倍实时，经蒸馏将去噪从 99 步降至 8 步；在 LIBERO 仿真中输出 7 通道机器人动作。目前仅研究预览，无公开权重。
---

# Reka 发布 Rho-1：19B 全能推理模型，统一文本/图像/视频与机器人动作

> 原文链接：https://www.marktechpost.com/2026/10/05/reka-releases-rho-1-a-19b-omni-reasoning-model-that-understands-generates-video-and-outputs-robot-actions-in-one/
> 来源：MarkTechPost

Reka has released a research preview of Rho-1, a 19B omni-reasoning model trained from scratch. A single neural network understands and generates text, images and video, reasons over them, and outputs robot actions. Reka frames it as a direct replacement for agentic pipelines that pass work between modality-specific models.

What Rho-1 Changes

Most multimodal systems today are pipelines. A central model plans, then hands jobs to specialists for images, video or detection. Each handoff adds latency, and each specialist sees only a narrow request.

Rho-1 removes those handoffs. Text, vision and robotic actions become tokens inside one context window. According to Reka&#8217;s research, one unedited session shows the full loop. The model draws a lighthouse, boxes it, animates it, edits the video into a snowstorm, and explains the difference. That all happens in 5 turns, with no tool call and no second model.

Architecture: Two Streams, One KV Cache

Every input and output uses one of two native formats:

Discrete tokens carry text, symbolic reasoning and high-level commands.

Continuous tokens carry image latents, video frames, robot actions and proprioception.

Each transformer block holds two expert weight streams. The understanding stream handles language and visual parsing. The generation stream denoises latents into images and video. Both streams share attention and operate over the same KV cache.

When a reply needs pixels, the understanding stream emits a discrete handoff token. The generation stream then renders from the full accumulated state. Training combines next-token prediction for discrete sequences with flow matching for continuous outputs.

This design has practical effects. Bounding boxes come out as coordinate tokens, not from a separate detector. A video&#8217;s first frame reuses the in-context image representation instead of a re-encoded copy.

&

Speed: Base vs Distilled

The base model generates video at 0.79x real-time (median), with a watchable stream starting in roughly 6 seconds. Reka team measured 7.0 seconds to a first clip, against an illustrative 13.8 seconds for a multi-agent pipeline.

A distilled variant cuts denoising from 99 steps to 8, with minimal quality loss reported. It returned a 5.3-second clip in about a second. In Reka&#8217;s internal tests, it matched the fastest dedicated image models. It was also the quickest model tested to the first text token. These are vendor-run tests, not independent benchmarks.

World Model and Robotics

Rho-1 streams continuously, clip after clip. New instructions enter through the understanding stream and update state mid-rollout. Reka demonstrates one opening forked into &#8216;bank left&#8217; and &#8216;bank right&#8217; continuations.

For robotics, actions and future frames decode from the same latent state. A LIBERO simulation episode shows Rho-1 emitting 7 action channels. To scale past scarce teleoperation logs, Reka pairs Rho-1 with its Inverse Dynamics Model, which infers control signals from raw video.

How Rho-1 Compares

Data verified on October 5, 2026 from official sources.

FeatureReka Rho-1ByteDance BAGELBAAI Emu3.5Google Genie 3DeveloperRekaByteDance SeedBAAIGoogle DeepMindParameters19B14B total, 7B active (MoT)34BNot disclosedInputsText, image, video, actions, proprioceptionText, imageInterleaved text and imageText prompt, navigation inputsOutputsText, image, video, actions, proprioceptionText, imageInterleaved text and imageInteractive video worldNative video generationYes, capped at 672&#215;384NoNo (image frames, not native clips)Yes, 720p at 24 fpsReal-time steeringYes, continuous rolloutsNoNoYes, promptable world eventsRobot actionsNative continuous action tokensNoEmbodied manipulation demosTakes navigation actions, does not emit themOpen weightsNoYes, Apache 2.0Yes, Apache 2.0NoAccess todayResearch preview via contact@reka.aiHugging Face, GitHubHugging Face, emu.world appProject Genie for Google AI Ultra subscribersSource/ResourcesReka blogGitHubHugging FaceDeepMind blog

Genie 3 access per Project Genie; Emu3.5 parameter count per its Hugging Face model card.

Key Takeaways

Rho-1 is a 19B model that reads and writes text, image, video and robot actions.

Two expert streams share attention and one KV cache in every block.

Distillation cuts denoising from 99 to 8 steps, about 1 second per 5.3 s clip.

Trained on 320 H100s for 3 months; video is capped at 672&#215;384.

Research preview only: no public weights, API or pricing yet.

Check out the Technical details and the announcement on X. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Reka Releases Rho-1: A 19B Omni-Reasoning Model That Understands, Generates Video and Outputs Robot Actions in One appeared first on MarkTechPost.