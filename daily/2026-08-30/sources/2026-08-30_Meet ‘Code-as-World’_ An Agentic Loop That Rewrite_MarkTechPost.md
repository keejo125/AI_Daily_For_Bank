---
publish_time: 1788053702
link: https://www.marktechpost.com/2026/08/29/mirros-code-as-world-executable-world-representations/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MirroS 发布 Code-as-World，提出用“可执行世界表示”（EWR）刻画物理场景的新范式：视频模型能预测像素却无法表征质量、接触与重力，Code-as-World 因此把场景表示为可执行的 scene.json（由 MuJoCo 运行、可被智能体对照原视频验证、可由人编辑重仿真）。一个智能体循环最多五轮“提议→实例化→执行→渲染→验证”从真实视频恢复程序，验证后的世界成为带精确物理标签的训练数据。团队基于 Qwen3.5 微调出 VL-4B 与 VL-9B（Apache 2.0），在 QuantiPhy 验证集上 9B 取得 55.4 的 MRA，高于 Gemini-3.1 Flash 的 54.8，约领先最强开源权重基线 15 分。
---

# Code-as-World：将真实视频重写为可执行 MuJoCo 物理程序的智能体循环

> 原文链接：https://www.marktechpost.com/2026/08/29/mirros-code-as-world-executable-world-representations/
> 来源：MarkTechPost

MirroS released Code-as-World: a paradigm that represents physical worlds through executable world representations. The argument is narrow and testable: pixels are evidence of a physical scene, not its ontology. A video model can predict plausible frames without ever representing mass, contact, or gravity. So instead of pixels, latents, or captions, Code-as-World represents a scene as executable code — a scene.json that MuJoCo can run, that an agent can verify against the source video, and that anyone can edit and re-simulate. An agentic loop recovers those programs from real footage in up to five rounds. The verified worlds then become training data with exact physical labels, which real video does not carry. Trained on that supervision, Code-as-World-VL-9B scores 55.4 MRA on QuantiPhy-validation, above Gemini-3.1 Flash at 54.8 and roughly 15 points above the strongest open-weight baseline.

Is it deployable?

Yes, at the research and internal-prototype tier. MirroS shipped the GitHub repo and two checkpoints — Code-as-World-VL-4B and Code-as-World-VL-9B — under Apache 2.0, fine-tuned from Qwen3.5-4B and Qwen3.5-9B. Both are BF16 safetensors served by vLLM behind an OpenAI-compatible /v1 endpoint, with 16 sampled frames per video and --max-model-len 4608. 

&&

The idea: pixels are evidence, not ontology

The MirroS technical report argues that video models, 3D reconstruction, and captions each recover part of a scene but none recovers its mechanism. Code-as-World represents a scene as an executable world representation (EWR), a triple p = (C, E, A):

Composition: objects, geometry, metric dimensions, mass, friction, gravity. Floors and walls are static physical entities so they can support and collide.

Evolution: initial states, forces, contacts, collisions, termination conditions, duration. Executing it expands composition into a full state trajectory.

Appearance: camera, lighting, materials, background, frame rate, render config. Changing it never changes the physics.

In the released implementation, that triple compiles into a scene.json executed in MuJoCo, with two interchangeable engines: an animation engine (kinematic poses) and a physics engine (forces and contacts).

Agentic discovery instead of one-shot prediction

Recovering an EWR from a video is an inverse problem, so the team frames it as abductive search. An agent runs propose → instantiate → execute → render → verify for up to K = 5 rounds. For video input, SAM 3 supplies instance masks and image-plane tracks, VGGT-Omega estimates depth and camera geometry, and SAM 3D generates per-object meshes. Candidate rollouts are projected back into the input view and compared at selected key frames on RGB, depth, masks, and trajectories. Frame-level discrepancies aggregate into structured feedback Δ that guides the next revision; when the budget runs out without acceptance, the hypothesis is rejected.

At a matched five-evaluation budget, the loop beats Best-of-5 independent sampling on Visual Alignment, Object IoU, Traj-ADE, and Accuracy@2%D — and the result repeats under the second execution engine. Candidate videos come from WISA-80K after motion-focused filtering; sim-to-real re-rendering uses Wan2.2-VACE plus an internal video model.

Verified worlds as training supervision

Phase 1 is supervised fine-tuning on 73,335 image-space QA pairs built from RefCOCO/+/g, RefCLEF and GOT-10K, covering extent, position, displacement, velocity and acceleration in raw pixels. Phase 2 applies GRPO to world-space VQA drawn from 1,585 text-driven and 988 video-driven executable worlds, rewarded on scale-normalized numerical accuracy plus unit and format terms. Training used eight NVIDIA H100 GPUs.

On QuantiPhy-validation (159 items, MRA macro-averaged over 2S/2D/3S/3D): 4B = 50.6, 9B = 55.4, 27B reasoning = 58.6, against Gemini-3.1 Flash at 54.8, ChatGPT-5.1 at 48.4, and the strongest open-weight baseline Qwen3-VL-32B-Instruct at 40.2. The ablation is the more useful number: image-space-only scores 44.2 (4B) and 50.9 (9B); adding both world-space sources lifts them to 50.6 and 55.4. Pixel-level grounding improves too — the 9B goes 63.7 → 68.3 on RefCOCO and 20.1 → 26.6 on GOT-10K after world-space RL.

Key Takeaways

Code-as-World turns a video into an editable scene.json that MuJoCo can execute and verify.

Five-round propose→verify search beats Best-of-5 sampling at the same compute budget.

Verified worlds supply exact physical labels that real video simply does not carry.

9B hits 55.4 MRA on QuantiPhy, above Gemini-3.1 Flash at 54.8; 4B and 9B are Apache 2.0.

Rigid-body only, and the model never learns the discovery loop itself.

Check out the Technical report, MirroS blog, Project page, GitHub and Announcement on X. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet &#8216;Code-as-World&#8217;: An Agentic Loop That Rewrites Real Videos Into Executable MuJoCo Physics Programs appeared first on MarkTechPost.