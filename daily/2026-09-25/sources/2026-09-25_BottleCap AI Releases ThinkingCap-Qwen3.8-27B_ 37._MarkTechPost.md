---
publish_time: 1790276336
link: https://www.marktechpost.com/2026/09/24/bottlecap-ai-releases-thinkingcap-qwen3-8-27b-37-2-fewer-thinking-tokens-at-a-0-86pp-accuracy-cost/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  BottleCap AI 发布 ThinkingCap 系列第二款模型 ThinkingCap-Qwen3.8-27B，在 Qwen 团队的 Qwen3.8-27B 上微调，唯一目标是缩短推理轨迹。在 12 项基准上平均少用 37.2% 的 thinking token，宏平均准确率由 86.65% 微降至 85.79%（仅降 0.86pp）。可在 vLLM/SGLang 直接替换部署，提供 FP8、NVFP4、GGUF、MLX 版本。团队刻意保守：不新增知识、不改变回答风格，推理/指令遵循/安全行为尽量原样透传，重点压降数学、推理、长上下文与 agentic 类任务的冗余 token。
---

# BottleCap发布ThinkingCap-Qwen3.8-27B：推理token减37%

> 原文链接：https://www.marktechpost.com/2026/09/24/bottlecap-ai-releases-thinkingcap-qwen3-8-27b-37-2-fewer-thinking-tokens-at-a-0-86pp-accuracy-cost/
> 来源：MarkTechPost

BottleCap AI has released ThinkingCap-Qwen3.8-27B, the second model in its ThinkingCap series. It is a fine-tune of the Qwen team&#8217;s Qwen3.8-27B with one narrow goal: shorter reasoning traces. Across 12 benchmarks, it spends 37.2% fewer thinking tokens on average. Macro-average accuracy moves from 86.65% to 85.79%, a 0.86pp drop. 

Deployable? Yes. It drops in for Qwen3.8-27B on vLLM or SGLang, with FP8, NVFP4, GGUF and MLX builds. The repo is gated, and commercial use beyond the small-business license needs a BottleCap agreement.

What Problem Does ThinkingCap Target?

Reasoning models often spend more thinking tokens than a question needs. BottleCap&#8217;s position is that many of those extra tokens do not change the final answer. The first release in the series applied this idea to Qwen3.6-27B.

The objective this time was deliberately conservative. BottleCap did not try to add knowledge or change answer style. Reasoning ability, instruction following and safety behaviour were meant to pass through untouched. The research team also focused harder on math, reasoning, long-context and agentic benchmarks.

Benchmark Results at xhigh Effort

All main numbers use reasoning_effort=xhigh, the chat template default. Every benchmark gets shorter, with cuts ranging from 10.7% to 65.5%.

Knowledge and multilingual tasks shrink the most. MMMLU drops 65.5% (1,656 to 571 tokens) and MMLU-Pro drops 57.3%. GPQA-Diamond falls from 12,772 to 7,267 tokens, a 43.1% cut. IFBench thinks 46.4% less with accuracy nearly flat (79.75% to 79.71%).

Long-context retrieval improves. AA-LCR accuracy rises 2.25pp, from 81.75% to 84.00%, with 38.6% fewer thinking tokens. LiveCodeBench v6 edges up 0.07pp while thinking 20.3% less.

Agentic results hold close to the base. τ²-bench gives up 1.01pp for a 30.9% cut. Terminal-Bench 2.1 loses 0.56pp, well inside its ±4.26 interval, for a 10.7% cut.

The most expensive trade is AIME 2026. Accuracy falls 3.85pp, from 98.13% to 94.27%, for 30.2% less thinking.

Please note that the 37.2% figure is the mean of the 12 per-benchmark reductions. Pooled mean thinking tokens fall from 15,735 to 12,144.

BottleCap also reports a budget curve. Under a 16K-token cap per response, ThinkingCap scores higher than the base model. Truncated traces fall from 0.51% to 0.34%, and looping from 0.06% to 0.05%.

&&&

How It Interacts With the Effort Dial

Qwen3.8-27B exposes a reasoning-effort setting, and the compression stacks with it. All deltas below compare against the base model at xhigh, averaged over 11 benchmarks.

At medium, the base model cuts 52.1% of thinking for -9.16pp. ThinkingCap cuts 60.2% for -9.90pp. At low, the figures are -55.4% and -9.71pp for the base, versus -62.3% and -10.79pp for ThinkingCap. With thinking off, ThinkingCap trails the base by 5.7pp.

BottleCap team recommends xhigh for the best accuracy-to-token balance. It says individual thinking modes will get attention in a future release.

How the Evaluation was Run

Both models ran through the same harness on one NVIDIA H200 with vLLM 0.29.0. Sampling was identical: temperature 1.0, top_p 0.95, top_k 20, min_p 0.0. Multi-seed accuracy is the mean with a 95% interval. Seeds range from 32 on AIME 2026 to 1 on MMLU-Pro and MMMLU. MMMLU uses a fixed 10,000-question sample; the other 11 benchmarks run complete sets.

MTP speculative decoding (3 draft tokens) was measured as accuracy-neutral on AIME 2026. It accepted 53% of drafted tokens, about 2.6 tokens per step, matching the base model.

Deployment: Builds, Serving and License

The bf16 checkpoint has 28B parameters and accepts image and text input. BottleCap publishes 5 quantized builds:

FP8: 31 GB, vLLM, Hopper and Blackwell.

NVFP4 weight-only: 21 GB, vLLM, Hopper (Marlin kernel) and Blackwell.

NVFP4 W4A4 (AWQ): 23 GB, Blackwell only.

GGUF: 16 to 55 GB, for llama.cpp, LM Studio and Ollama.

MLX 4-bit DWQ: 21 GB, for Apple Silicon Macs with 32 GB.

Serving uses the base model&#8217;s recipe: --reasoning-parser qwen3 with the qwen3_xml tool-call parser on vLLM. Thinking returns in a separate reasoning field.

The license is PolyForm Small Business 1.0.0 plus a BottleCap personal-use grant. Upstream Qwen materials stay under Apache-2.0. Hugging Face lists no inference provider hosting the model yet.

Key Takeaways

37.2% fewer thinking tokens on average across 12 benchmarks.

Macro accuracy drops 0.86pp, from 86.65% to 85.79%.

AA-LCR long-context accuracy rises 2.25pp; AIME 2026 falls 3.85pp.

Drop-in for Qwen3.8-27B: same sampling, same vLLM or SGLang flags.

Gated weights under PolyForm Small Business; commercial use needs a license.

Check out the technical blog and model weights. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post BottleCap AI Releases ThinkingCap-Qwen3.8-27B: 37.2% Fewer Thinking Tokens at a 0.86pp Accuracy Cost appeared first on MarkTechPost.