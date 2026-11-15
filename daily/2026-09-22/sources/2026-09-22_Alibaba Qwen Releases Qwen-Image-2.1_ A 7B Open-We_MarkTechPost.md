---
publish_time: 1790008844
link: https://www.marktechpost.com/2026/09/21/alibaba-qwen-releases-qwen-image-2-1/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  阿里 Qwen 团队发布 Qwen-Image-2.1，一个统一的文生图与图像编辑模型，视觉生成部分含 32 层单流 DiT、共 7B 参数。单一权重覆盖文生图、多参考编辑、局部修改与透明 RGBA 输出。发布即获 Diffusers、ComfyUI、vLLM-Omni、SGLang、LightX2V 等 Day 0 支持，可用于研究与评估，商业部署需申请。
---

# 阿里发布 Qwen-Image-2.1：7B 开源图像生成与编辑模型

> 原文链接：https://www.marktechpost.com/2026/09/21/alibaba-qwen-releases-qwen-image-2-1/
> 来源：MarkTechPost

Alibaba&#8217;s Qwen team has released Qwen-Image-2.1, a unified text-to-image generation and image editing model. Its visual generation component has 7B parameters across 32 single-stream DiT layers. One checkpoint covers text-to-image, multi-reference editing, local edits, and transparent RGBA output. 

Is it deployable? Yes, for research and evaluation. Day 0 support covers Diffusers, ComfyUI, vLLM-Omni, SGLang, and LightX2V. Commercial deployment needs a separate license from Qwen.

From 20B to 7B

The original Qwen-Image shipped in August 2025 as a 20B model under Apache 2.0. Editing lived in a separate Qwen-Image-Edit checkpoint. Qwen-Image-2.1 folds both jobs into one model at about a third of the size. Qwen team calls it the most balanced and cost-effective model in the Qwen-Image series. One important thing to note here for capacity planning: the 7B figure covers the diffusion transformer only. The pipeline also loads an 8B Qwen3-VL encoder.

Architecture

The GitHub Repo lists 4 components:

Transformer: 32 layers, 7B parameters, single-stream design with block-causal attention.

Text encoder: Qwen3-VL 8B, which encodes text instructions and condition images into one representation.

VAE: 64-channel RGBA autoencoder with 16x spatial compression and native transparency.

Scheduler: Flow Matching with Euler discrete scheduling and dynamic shifting.

The attention mask is where the speed comes from. Text tokens use a token-level causal mask. Image tokens use a chunk-level bidirectional mask within each image. Qwen calls this mixed-granularity attention. The condition prefix sits before the noisy latent, so it never attends to it. Its keys and values therefore stay fixed across denoising steps. The model computes text and input images once, at the first step. It reuses that prefix KV cache for every remaining step. Savings grow with the number of reference images, which explains the multi-image speed claim.

What It Can Do

Native transparency: Generates RGBA images from text, edits transparent layers, and extracts subjects from photos. Qwen recommends a fixed prompt template for transparent output.

Multi-reference editing: Accepts up to 10 reference images. README examples include a group photo from 6 portraits and an outfit from 5 references.

Local control: Edits can target regions using circles, painted annotations, or separate masks. Identity is preserved for people and products.

Native 2K: Defaults to 2048 x 2048, with 7 supported aspect ratios up to 2752 x 1536.

Aesthetics: Improved typography, portrait lighting, and fine detail. Qwen highlights panoramas, infographics, storyboards, and virtual try-ons.

Benchmark: Qwen&#8217;s Own Chart

The research team compares models on Qwen-Image-Bench, Qwen&#8217;s in-house benchmark. On that chart, Qwen-Image-2.1 scores 60.28 overall. That places it above Nano Banana 2.0 at 59.82 and every listed open-weight model. FLUX 2 Max, a 32B open model, sits at 55.33. 6 closed models score higher, led by GPT Image 2.5 Sunburst at 67.01. 

Interactive Explainer

&

Running It

Install PyTorch 2.4.0 or later, transformers 5.17 or later, Diffusers from source, accelerate, and pillow. Then:

Copy CodeCopiedUse a different Browser

import torch
from diffusers import QwenImage21Pipeline

pipe = QwenImage21Pipeline.from_pretrained(
    "Qwen/Qwen-Image-2.1", torch_dtype=torch.bfloat16
).to("cuda")

image = pipe(
    prompt="A neon shop sign that reads \"QWEN IMAGE 2.1\", rainy night",
    num_inference_steps=40,
).images[0]
image.save("t2i.png")

The same pipeline handles editing when you pass image= with 1 or more references. On smaller GPUs, pipe.enable_model_cpu_offload() reduces memory pressure.

For serving, vLLM-Omni adds FP8 quantization, prefix KV caching, CUDA Graph decode, and tensor parallelism. SGLang adds Cache-DiT, CUDA graphs, multi-GPU parallelism, and component offload. ComfyUI ships native nodes and converted weights. Beyond NVIDIA, the release covers AMD Radeon GPUs via ROCm and 8 chip platforms via FlagOS.

Qwen team also released 2 prompt-rewriting models, fine-tuned Qwen3.5-VL 9B checkpoints for text-to-image and editing. They expand short prompts into detailed ones and can pick an aspect ratio.

Key Takeaways

Qwen-Image-2.1 unifies generation and editing in a 7B DiT with a Qwen3-VL 8B encoder.

Native RGBA output and up to 10 reference images come from one checkpoint.

Prefix KV cache reuse computes text and reference images once per generation.

It scores 60.28 on Qwen&#8217;s own benchmark, first among listed open-weight models.

The Qwen Research License bars commercial use without a separate agreement.

Check out the Model Weights, GitHub Repo, and Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Alibaba Qwen Releases Qwen-Image-2.1: A 7B Open-Weight Model for Image Generation and Editing appeared first on MarkTechPost.