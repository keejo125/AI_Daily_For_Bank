---
publish_time: 1791577997
link: https://www.marktechpost.com/2026/10/09/alibaba-qwen-releases-qwen-image-2-1-turbo-an-8-step-7b-image-model/
source: 阿里通义千问
status: confirmed
category: 国内
is_model_related: true
digest: |
  阿里通义千问团队发布Qwen-Image-2.1-Turbo，是其开源图像模型Qwen-Image-2.1的加速版：在保持7B视觉生成架构与2K出图、编辑能力不变的前提下，将去噪步数从40步压缩到8步（5倍提速），并支持Diffusers直接加载与云端API。该模型采用单流DiT、32层、7B参数，搭配Qwen3-VL 8B文本编码器，CFG默认设为1，通过前缀KV缓存复用文本与参考图上下文。在Qwen-Image-Bench上取得60.28的开源权重最高分，仅限研究许可、商用需单独授权。
---

# 阿里通义千问发布 Qwen-Image-2.1-Turbo：8 步 7B 图像模型

> 原文链接：https://www.marktechpost.com/2026/10/09/alibaba-qwen-releases-qwen-image-2-1-turbo-an-8-step-7b-image-model/
> 来源：MarkTechPost

Alibaba&#8217;s Qwen team has released Qwen-Image-2.1-Turbo, an accelerated checkpoint of its open-weight Qwen-Image-2.1 model. It generates and edits images in 8 denoising steps instead of the base model&#8217;s 40-step default. For developers, that means 5x fewer denoising steps on the same 7B architecture, plus a hosted API option.

TL;DR

Size: 7B parameters in the visual generator, paired with a Qwen3-VL 8B text encoder. 

Runs on: CUDA GPUs in BF16 via Diffusers. Qwen publishes no Turbo VRAM minimum. Unsloth estimates the base model runs on 11 GB VRAM with GGUF and 24 GB with INT8/FP8.

Performance: Same 2K output and editing feature set as Qwen-Image-2.1, at 8 steps instead of 40.

Best: Base Qwen-Image-2.1 scores 60.28 on Qwen-Image-Bench, the top open-weight score Qwen reports.

Bottom line (best): 8-step 2K generation and editing in one open checkpoint.

Bottom line (worst): Research license only, so commercial self-hosting needs separate permission.

What is Qwen-Image-2.1-Turbo?

Qwen-Image-2.1-Turbo is an 8-step image generation and editing checkpoint from Alibaba&#8217;s Qwen team. It is built on Qwen-Image-2.1. Turbo keeps the same 7B visual generation architecture. It loads directly with QwenImage21Pipeline in Diffusers.

The checkpoint ships with its recommended 8-step sampling schedule saved inside. Generation uses CFG=1 by default. Prefix KV caching reuses the text and reference-image context across denoising steps.

How does Qwen-Image-2.1-Turbo work?

The underlying architecture is a single-stream DiT with 32 layers and 7B parameters. It uses block-causal attention. Text tokens get a token-level causal mask, while images use a chunk-level bidirectional mask.

Text encoder: Qwen3-VL 8B encodes both instructions and condition images.

VAE: a 64-channel RGBA autoencoder with 16x spatial compression, which enables native transparency.

Scheduler: Flow Matching with Euler discrete scheduling and dynamic shifting.

The attention design is what makes prefix caching work. Input images and text are computed once at the first step. Every later step reuses that cache. With only 8 steps, the cached prefix covers most of the conditioning cost.

What can it generate and edit?

The Turbo model card showcase covers 8 categories. These include portraits, human poses, transparent images, typography and posters, and UI layouts. Editing examples include single-image transformation, multi-reference composition and 4-image interior composition. The base model supports up to 10 reference images and local edits via circles, painted annotations or masks.

How do you run Qwen-Image-2.1-Turbo?

Setup requires Diffusers from source, along with transformers>=5.17.0. The checkpoint needs Diffusers PR #14950, which adds pipeline-configured sampling sigmas.

Copy CodeCopiedUse a different Browser

import torch
from diffusers import QwenImage21Pipeline

pipe = QwenImage21Pipeline.from_pretrained(
    "Qwen/Qwen-Image-2.1-Turbo", dtype=torch.bfloat16
).to("cuda")

image = pipe(
    prompt="A ceramic teapot on a wooden table, soft window light",
    width=2048, height=2048, use_kv_cache=True,
).images[0]

For editing, pass image=input_image with an instruction prompt. Supported presets run from 2048&#215;2048 square to 2752&#215;1536 at 16:9.

One thing to note here. Setting num_inference_steps alone does not override the saved schedule. Only an explicit sigmas argument does, and Qwen notes other schedules are untested.

What does the API cost?

Alibaba Cloud Model Studio now hosts both Turbo and Pro. qwen-image-2.1-turbo costs CNY 0.1 per image in most regions, with a 120 RPM limit. qwen-image-2.1-pro costs CNY 0.25 per image, with 20 RPM. Turbo is 2.5x cheaper per image and allows 6x the request rate.

Qwen-Image-2.1-Turbo vs competing fast image models

FeatureQwen-Image-2.1-TurboQwen-Image-2.1Z-Image-TurboFLUX.2 klein 9BOrgAlibaba QwenAlibaba QwenAlibaba Tongyi-MAIBlack Forest LabsGenerator size7B7B6B9BText encoderQwen3-VL 8BQwen3-VL 8BNot disclosedQwen3 8BDefault steps8408 NFEs4EditingYes, multi-referenceYes, up to 10 referencesNo (separate Edit model)Yes, multi-referenceTransparent RGBA outputYesYesNot disclosedNot disclosedNative resolution2K (2048&#215;2048)2K (2048&#215;2048)1024&#215;1024 in examples1024&#215;1024 in examplesHardware guidanceNot disclosed11 GB GGUF / 24 GB FP8 (Unsloth)Fits 16 GB VRAM~29 GB VRAM, RTX 4090+LicenseQwen Research LicenseQwen Research LicenseApache 2.0FLUX Non-CommercialQwen-Image-BenchNot disclosed60.28 (vendor)Not disclosedNot disclosedHosted APICNY 0.1/imagePro: CNY 0.25/imageNot disclosedBFL API

Key Takeaways

Qwen-Image-2.1-Turbo cuts denoising from 40 steps to 8 on the same 7B architecture.

One checkpoint handles 2K text-to-image, multi-reference editing and transparent RGBA output.

The API costs CNY 0.1 per image, 2.5x cheaper than Pro.

Weights are research-licensed, so commercial self-hosting needs separate permission.

No Turbo-specific benchmark exists yet; base Qwen-Image-2.1 scores 60.28 on Qwen-Image-Bench.

Check out the ModelScope page, Hugging Face page, Pro API and Turbo API. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Alibaba Qwen Releases Qwen-Image-2.1-Turbo, an 8-Step 7B Image Model appeared first on MarkTechPost.