---
publish_time: 1793831105
link: https://www.marktechpost.com/2026/11/04/webai-twil-8b-reasoning-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  webAI 发布 TwIL-8B，一款 88 亿参数的推理模型，面向数学、代码与指令遵循，基于 IBM Granite 4.2 8B 后训练，在 MATH-500 上取得 98.2 分，权重以非商业许可发布于 Hugging Face。该模型延续了小参数推理模型的路线，主打在受限许可下提供高质量数学与代码能力。
---

# webAI发布TwIL-8B推理模型：8.8B参数MATH-500得分98.2

> 原文链接：https://www.marktechpost.com/2026/11/04/webai-twil-8b-reasoning-model/
> 来源：MarkTechPost

webAI has released TwIL-8B, an 8.8B reasoning model for math, code and instruction following. The TwIL-8B reasoning model is post-trained from IBM&#8217;s Granite 4.2 8B. Weights are on Hugging Face under a non-commercial license. webAI&#8217;s launch post frames the pitch around cost per task, not raw scale. The 4-bit build is 4.98 GiB, sized for CPU or modest-VRAM GPU inference.

TL;DR

Size: 8.79B parameters, dense. 131,072-token context, inherited from the base model.

Runs on: CPU or modest-VRAM GPU via a 4.98 GiB Q4_K_M GGUF. Full bf16 weights are 16.38 GiB.

Performance: Leads its size class on math and code, trails on knowledge benchmarks.

Best: MATH-500 at 98.2, the top score in webAI&#8217;s comparison.

Worst: GPQA Diamond at 70.2, 11.5 points behind Qwen3.5-9B. HLE is 12.6 (verbose variant).

What is TwIL-8B?

TwIL-8B is a dense decoder-only reasoning model from webAI. It has 40 layers, hidden size 4096, and 32 attention heads with 8 KV heads. Input and output are English text only. The model writes a <think> block before each answer.

It ships in 2 variants with the same architecture and tokenizer. Balanced is the default and produces shorter reasoning traces. Verbose reasons longer and targets hard contest-style problems.

TwIL-8B extends webAI&#8217;s TwIL family. The first members were 1.7B and 3B formal-logic models released in August 2026.

How was TwIL-8B trained?

webAI used 3 post-training stages:

Full-parameter SFT on reasoning traces for math, STEM and instruction following.

GRPO/DAPO reinforcement learning on math, code, STEM and instruction prompts. This produces the verbose variant.

Length-aware RL with a reward that favors shorter traces against per-domain length references. This produces the balanced variant.

Training pools were decontaminated with 13-gram matching against AIME, HMMT, MATH-500, GPQA and other evals. 

How does TwIL-8B perform on benchmarks?

All TwIL-8B scores are self-reported, high-effort pass@1 with thinking enabled. Scores marked † were measured on the verbose variant only.

Math: TwIL-8B scores 98.2 on MATH-500. Qwen3.5-9B lists 96.6 on a third-party leaderboard. Gemma 4 31B scored 87.9 in Red Hat&#8217;s lighteval run. On AIME 2025, TwIL-8B posts 88.3 against 87.1 for Gemma 4 31B. On AIME 2026 it scores 88.3, behind Qwen3.5-9B at 92.5 and Gemma 4 31B at 89.2.

Code: LiveCodeBench† is 81.6, against 65.6 for Qwen3.5-9B and 80.0 for Gemma 4 31B. webAI notes its LiveCodeBench version was not recorded. Competitor scores are v6.

Instruction following: IFBench† is 74.4, 9.9 points above Qwen3.5-9B at 64.5. IFEval is level, at 91.8 vs 91.5.

Knowledge: This is the weak spot. GPQA Diamond is 70.2, against 81.7 for Qwen3.5-9B and 84.3 for Gemma 4 31B. MMLU-Pro† is 76.5 vs 82.5 for Qwen3.5-9B.

Across 13 shared benchmarks, TwIL-8B goes 7-6 against Qwen3.5-9B. Against Gemma 4 31B, about 3.5x its size, it goes 3-11.

Does TwIL-8B use fewer reasoning tokens?

Yes, against its closest open peer. On AIME 2026, TwIL-8B averages about 19.5k output tokens per problem. Qwen3.5-9B uses 31.2k, so TwIL-8B uses 38% fewer. It scores 4.2 points lower. On HMMT Feb 2026 the gap is 32.9k vs 40.6k, or 19% fewer.

Frontier models remain far leaner. webAI cites about 5k tokens per AIME 2026 problem for GPT-5.5. webAI states that harnesses and tokenizers differ, so treat this as directional.

TwIL-8B vs Qwen3.5-9B vs Gemma 4

MetricsTwIL-8BQwen3.5-9BGemma 4 12BGemma 4 31BParameters8.79B dense9B (language model)11.95B dense30.7B denseContext131,072262,144 native256K256KModality (input)TextText, image, videoText, image, audioText, imageLicensewebAI Non-Commercial 1.0Apache 2.0Apache 2.0Apache 2.0Smallest official local build4.98 GiB (Q4_K_M)Not disclosedNot disclosedNot disclosedMATH-50098.296.6 (3rd party)Not disclosed87.9 (Red Hat)AIME 202688.392.5 (MathArena)77.589.2LiveCodeBench81.6 †65.6 (v6)72.0 (v6)80.0 (v6)GPQA Diamond70.281.778.884.3MMLU-Pro76.5 †82.577.285.2

TwIL-8B figures from the model card. † = verbose variant. All scores self-reported by each vendor unless marked.

&

How do you run TwIL-8B locally?

from_pretrained("webAI-Official/TwIL-8B") loads the balanced variant. Pass subfolder="verbose" for the verbose one. The model card lists GGUF builds for llama.cpp:

Q4_K_M, 4.98 GiB, for both variants

Q8_0, 8.70 GiB, verbose only

F16, 16.38 GiB, verbose only

Give it a large generation budget. The card&#8217;s example sets max_new_tokens=32768. A short budget truncates reasoning and scores far worse. All reported scores used bf16 weights, so expect small drops at Q4_K_M. No hosted inference provider serves the model on Hugging Face yet.

Key Takeaways

TwIL-8B is an 8.79B dense reasoning model post-trained from IBM Granite 4.2 8B.

It posts 98.2 on MATH-500 and 81.6† on LiveCodeBench.

It uses 38% fewer tokens than Qwen3.5-9B on AIME 2026.

Knowledge is weak: GPQA Diamond trails Qwen3.5-9B by 11.5 points.

Weights are open but licensed for non-commercial use only.

Check out the model card and weights on Hugging Face and webAI&#8217;s announcement on X. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post webAI Releases TwIL-8B, an 8.8B Reasoning Model Scoring 98.2 on MATH-500 appeared first on MarkTechPost.