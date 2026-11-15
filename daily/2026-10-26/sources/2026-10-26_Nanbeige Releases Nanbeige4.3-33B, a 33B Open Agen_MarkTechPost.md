---
publish_time: 1792962921
link: https://www.marktechpost.com/2026/10/25/nanbeige-releases-nanbeige4-3-33b-open-agentic-coding-model/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  南大模型实验室（BOSS 直聘旗下）在 Hugging Face 开源 Nanbeige4.3-33B，33B 稠密语言模型，面向 Agentic Coding 与办公协作（cowork）任务，Apache 2.0，上下文 512K。在标准 Llama 架构上，其自有对比中 20 项里领先 17 项（对比 Qwen3.8-27B 等），Terminal-Bench 2.1 达 80.9；并发布 Base 版供定制后训练，策略是先建强教师再蒸馏小模型。
---

# 南大模型实验室开源 Nanbeige4.3-33B 智能体编程模型

> 原文链接：https://www.marktechpost.com/2026/10/25/nanbeige-releases-nanbeige4-3-33b-open-agentic-coding-model/
> 来源：MarkTechPost

Nanbeige LLM Lab has released Nanbeige4.3-33B on Hugging Face under the Apache 2.0 license. Nanbeige4.3-33B is a 33B dense language model built for agentic coding and office-style &#8216;cowork&#8217; tasks. The lab sits inside the recruitment platform BOSS Zhipin. It also published Nanbeige4.3-33B-Base for custom post-training. The model supports a 524,288-token context window. In the lab&#8217;s own table, it leads 17 of 20 benchmarks against 3 open models near 30B.

TL;DR

Size: 33B parameters, dense (no MoE), 524,288-token (512K) context, BF16 weights.

Runs on: Multi-GPU servers. The card&#8217;s SGLang and vLLM recipes use 4-way tensor parallelism. BF16 weights need about 66 GB (our arithmetic). 1 community quantization is listed.

Performance: Leads 17 of 20 rows in Nanbeige&#8217;s own comparison against Qwen3.8-27B, Muse-Glimmer-30B and Gemma4-31B.

Best: 80.9 on Terminal-Bench 2.1, versus 73.0 for Qwen3.8-27B.

Worst: 23.8 on Terminal-Bench 4.0 (its lowest score). It also trails Qwen3.8-27B on SWE-Bench Pro, 60.3 vs 61.7.

What is Nanbeige4.3-33B?

Nanbeige4.3-33B is the flagship &#8216;teacher&#8217; model of the Nanbeige4.3 series. The lab&#8217;s stated strategy is to build a strong teacher first. It then plans to distill agentic skills into smaller models, starting with Nanbeige4.3-3B. 

How is Nanbeige4.3-33B built?

The config.json declares a standard LlamaForCausalLM architecture. There is no expert routing, so all 33B parameters run on every token.

52 layers, hidden size 7,168

56 query heads and 8 key-value heads (grouped-query attention), head dimension 128

FFN intermediate size 22,016, vocabulary of 166,912 tokens

RoPE theta of 120,000,000 and 524,288 max positions

The chat template exposes 3 controls. enable_thinking toggles reasoning and is on by default. preserve_thinking keeps reasoning from earlier turns. Nanbeige recommends it for multi-turn tool use and code agents. Passing tools enables tool calling, and an XML call format is recommended.

How does Nanbeige4.3-33B perform on benchmarks?

Nanbeige compared the model with Qwen3.8-27B, Muse-Glimmer-30B and Gemma4-31B. Every model ran at its highest thinking effort, with shared hyperparameters and harnesses. All scores in this section are self-reported.

Agentic coding: It scores 80.9 on Terminal-Bench 2.1, against 73.0 for Qwen3.8-27B. DeepSWE shows the widest gap: 65.5 versus 42.5. On Terminal-Bench 4.0, it scores 23.8 while Gemma4-31B scores 0.0.

Agentic cowork: It posts 54.2 on Automation Bench versus 38.3, and 44.8 on JobBench versus 34.5. On YC-bench, simulated earnings reach $1,025,437 versus $641,290.

Reasoning: It reports 95.2 on AIME 2026 and 84.0 on AA-LCR.

It loses 3 of 20 rows. Qwen3.8-27B leads SWE-Bench Pro (61.7 vs 60.3) and GDPval (86.4 vs 84.8). Gemma4-31B leads GPQA Diamond in Nanbeige&#8217;s table, 91.3 vs 89.5.

The Base model beats Gemma4-31B-Base on all 8 reported tasks. Examples include MMLU-Pro (66.9 vs 59.3) and GPQA (62.0 vs 41.5).

How does it compare with competitors&#8217; own model cards?

SpecNanbeige4.3-33BQwen3.8-27BMuse-Glimmer-30BGemma 4 31BDeveloperNanbeige LLM Lab (BOSS Zhipin)Qwen (Alibaba)Meta Superintelligence LabGoogle DeepMindParameters33B dense27B dense LM plus vision encoder~29.6B dense, incl. ~1.8B vision encoder30.7B denseContext524,288262,144 native, up to 1M131,072+256KInput modalityTextText, image, videoText, imageText, imageLicenseApache 2.0Apache 2.0Apache 2.0Apache 2.0Terminal-Bench 2.180.9*73.051.7Not disclosedSWE-Bench Pro60.3*61.751.2Not disclosedGPQA Diamond89.5*89.283.5 (AA)84.3AIME 202695.2*Not disclosed94.789.2Local hardware guidance4-GPU tensor-parallel recipeNot disclosed24 GB or 32 GB VRAM at ~4-bitConsumer GPUs and workstations

*Self-reported by Nanbeige. Competitor values come from each lab&#8217;s own Hugging Face model card.

Some competitor figures in Nanbeige&#8217;s table differ from what those labs publish:

Meta reports Muse-Glimmer-30B at 51.2 on SWE-Bench Pro and Gemma4-31B at 36.9. Nanbeige lists the reverse.

Google lists Gemma 4 31B at 84.3 on GPQA Diamond. Nanbeige&#8217;s table shows 91.3.

Meta reports Muse-Glimmer-30B at 51.7 on Terminal-Bench 2.1. Nanbeige measured 61.8.

Different harnesses explain some gaps. The SWE-Bench Pro pair looks swapped. Treat these rows as provisional until independent runs appear.

How do you deploy Nanbeige4.3-33B?

The model card provides Transformers, SGLang and vLLM recipes. Its server examples use 4-way tensor parallelism with Qwen3 reasoning and tool-call parsers. Recommended agent settings are temperature 1.0, top_p 0.95 and 65,536 max new tokens. Reasoning and chat use temperature 0.6 and 262,144 max new tokens.

By arithmetic from config.json, BF16 weights need about 66 GB. The KV cache adds about 208 KiB per token in BF16. A full 524,288-token sequence therefore needs roughly 112 GB of KV cache. At publication, no Hugging Face Inference Provider hosts the model.

Key Takeaways

33B dense, Apache 2.0, 512K context, text-only.

Self-reported 80.9 on Terminal-Bench 2.1 and 65.5 on DeepSWE.

Leads 17 of 20 rows in Nanbeige&#8217;s own table.

Several competitor figures conflict with official cards.

Built as the teacher for the upcoming Nanbeige4.3-3B.

Check out the model weights, the Base model and the launch post on X. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Nanbeige Releases Nanbeige4.3-33B, a 33B Open Agentic Coding Model appeared first on MarkTechPost.