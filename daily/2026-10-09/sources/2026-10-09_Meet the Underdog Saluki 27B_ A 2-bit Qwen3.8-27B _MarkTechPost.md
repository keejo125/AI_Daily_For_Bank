---
publish_time: 1791530616
link: https://www.marktechpost.com/2026/10/09/meet-the-underdog-saluki-27b-a-2-bit-qwen3-8-27b-that-beats-the-original-at-tool-calling/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Conway Research 的端侧助手 Underdog 以 Apache 2.0 发布 Saluki 27B——一个 2-bit GGUF 量化的 Qwen3.8-27B，仅 7.89GB（BF16 需 54GB）即可在原生 llama.cpp 中运行。量化专门保护工具调用能力（把聊天模型变成智能体的关键技能），让 27B 级智能体模型能在消费级显卡上运行。
---

# Saluki 27B：在端侧 llama.cpp 跑通的 2-bit Qwen3.8-27B

> 原文链接：https://www.marktechpost.com/2026/10/09/meet-the-underdog-saluki-27b-a-2-bit-qwen3-8-27b-that-beats-the-original-at-tool-calling/
> 来源：MarkTechPost

Underdog, the on-device assistant from Conway Research, has released Saluki 27B under Apache 2.0. Underdog Saluki 27B is a 2-bit GGUF of Qwen3.8-27B that fits in 7.89 GB. The full BF16 model needs 54 GB. Underdog tuned the compression to protect tool calling, the skill that turns a chat model into an agent. For developers, that means a 27B-class agent model that runs in stock llama.cpp.

TL;DR

Size: 27B dense parameters. 7.89 GB GGUF versus 54 GB for BF16. 

Runs on: stock llama.cpp and apps built on it, with full GPU offload. Optional 629 MB or 928 MB vision add-on. 

Performance: 96% average retention across 9 benchmarks versus full Qwen3.8-27B.

Best: Parallel tool calls, 42 versus 35 for the full model (120% retention).

Worst: AIME 2025, 79.2 versus 96.7 (about 82% retention).

Bottom line: 

Best: beats the 54 GB original at tool calling in a sub-8 GB file. 

Worst: competition math and multi-step reasoning drop 12 to 18 points.

What is Underdog Saluki 27B?

Saluki 27B is a 2-bit, mixed-precision GGUF of Qwen3.8-27B built for local agents. It stacks 3 layers of work:

The base is Qwen3.8-27B, a dense 27B model from the Qwen team. It has 64 layers, mixes Gated DeltaNet linear attention with gated attention, and supports 262,144 tokens natively.

The second layer is ISTA-DASLab&#8217;s Qwen3.8-27B-GSQ-RCO-GGUF. GSQ learns accurate low-bit scalar grids per tensor. RCO assigns a quantization type to each tensor under a fixed size budget. ISTA&#8217;s smallest file, IQ2_XS, is 8.4 GB at 2.50 bits per weight.

The third layer is Underdog&#8217;s own pass. It shrank the file to 7.89 GB and targeted tool calling. The file is named IQ2-mix and carries an imatrix tag. Underdog has not published the full recipe for this pass.

How does Saluki perform on benchmarks?

Underdog splits its results into 2 groups. 

The first group ran both models in the same harness:

Underdog Bench: 120 tasks from BFCL v4, frozen before testing. Thinking off, temperature 0. Saluki scores 88, the full model 84, and PrismML&#8217;s Bonsai 2 scores 70.

Parallel tool calls: 100 BFCL v4 parallel tasks with the official checker. Saluki 42, full model 35.

SWE-bench Verified: 50 issues. Saluki fixes 30, the full model 33.

The second group compares Saluki with public full-size scores:

BenchmarkSaluki 27BQwen3.8-27B (public)IFEval (prompt-loose)93.591.5IFBench (prompt-loose)72.771.0MBPP+78.083.9MuSR67.579.6AIME 2025 (avg@4)79.296.7AIME 2026 (avg@4)80.094.6

&&&

How does Saluki compare with other compact Qwen3.8-27B builds?

FeatureUnderdog Saluki 27BQwen3.8-27B (BF16)ISTA GSQ-RCO IQ2_XSPrismML Bonsai 2 27B (PTQ1_0)OrgUnderdog (Conway Research)Qwen teamISTA-DASLabPrismMLParameters27B27B27B27.36BFile size7.89 GB54 GB8.4 GB5.95 GBBits per weightNot disclosed (2-bit mix)162.501.75ContextNot disclosed262,144 nativeNot disclosed262KVisionAdd-on, 629 or 928 MBNative0.9 GB mmprojOptional 0.63 GBRuntimeStock llama.cppTransformers, vLLM, SGLangStock llama.cpp, Ollama, LM StudioPrismML llama.cpp forkUnderdog Bench (of 120)8884Not disclosed70Vendor headline96% avg retention, 9 benchmarksBaseline100.3% zero-shot recovery98.2% of FP16, 14 benchmarksLicenseApache 2.0Apache 2.0Apache 2.0Apache 2.0

Bonsai 2 is smaller and reports 98.2% retention across 14 thinking-mode benchmarks. It also posts stronger math, including 95.00 on AIME25. However, it needs PrismML&#8217;s llama.cpp fork, since stock llama.cpp rejects its packing formats. Saluki runs on stock llama.cpp. Each vendor uses its own harness, so cross-vendor scores are not directly comparable.

Key Takeaways

Saluki 27B fits Qwen3.8-27B into 7.89 GB, down from 54 GB.

It beats the full model on tool calling: 88 versus 84.

Parallel tool calls rise to 42 from 35.

Math and reasoning take the biggest hit, down to about 82 to 85%.

It runs in stock llama.cpp under Apache 2.0.

Check out the Model Card on Hugging Face, the Underdog launch page and the announcement on X. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Meet the Underdog Saluki 27B: A 2-bit Qwen3.8-27B That Beats the Original at Tool Calling appeared first on MarkTechPost.