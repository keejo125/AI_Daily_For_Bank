---
publish_time: 1788325920
link: https://www.marktechpost.com/2026/09/01/perplexity-releases-hybrid-compute-on-mac-cloud-agents-orchestrate-down-to-a-local-model-gated-on-device/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Perplexity 在 Mac 端推出混合计算：单个 Computer 任务在云端前沿模型与用户 Mac 上的本地小模型间拆分，由端侧隐私闸门决定哪些数据可跨边界。云端负责搜索、规划与长程推理，涉及隐私文件时下沉到本地模型执行再合并结果。其开源的 PII-Tracer（基于 Qwen3 的 0.6B 双向编码器）在长对话 PII 识别一致性上领先 GPT-5.6-sol；配套基准 PII-TRACE 含 13 语言 1.3 万合成对话。需 Apple silicon Mac、macOS 15 及至少 24GB 内存。
---

# Perplexity 在 Mac 推出混合计算：云端智能体编排下沉至本地模型、端侧隐私闸门管控

> 原文链接：https://www.marktechpost.com/2026/09/01/perplexity-releases-hybrid-compute-on-mac-cloud-agents-orchestrate-down-to-a-local-model-gated-on-device/
> 来源：MarkTechPost

Agentic assistants have a structural problem: the context that makes them useful — deal documents, privileged files, client records — is exactly the context users cannot send to a cloud endpoint. This week, Perplexity shipped its answer for Mac. Hybrid compute splits a single Perplexity Computer task between frontier models in the cloud and a compact model on the user&#8217;s Mac, with an on-device privacy gate deciding what may cross the boundary. Perplexity also open-sourced the classifier behind that gate.

Is it deployable? Yes, hybrid compute is live for Pro, Max, and Enterprise subscribers on any Apple silicon Mac running macOS 15 or later with at least 24GB of unified memory (32GB recommended). The local model installs in one click from the Mac app, with no Ollama, no separate runtime, and no API key, and local work consumes no cloud credits.

What hybrid compute actually does

The direction of orchestration is the design decision. Computer starts every task in the cloud, where frontier models handle web search, planning, and long-horizon reasoning. When a step touches private files or sensitive data, Computer hands that step down to the local model on the Mac without restarting the task or losing context then merges both halves into one result.

This inverts the local compute mode Perplexity shipped on NVIDIA DGX Spark a week earlier, which starts on the user&#8217;s hardware and escalates up to cloud models with permission. Same orchestrator, opposite default.

Because Computer works with iPhone, a task can be triggered remotely while sensitive steps execute on the Mac at the desk. Perplexity positions an always-on Mac mini as a dedicated local inference node for exactly this pattern.

The privacy gate is the load-bearing component

Before anything from a protected file reaches the cloud, an on-device classifier inspects it and the gate applies one of four outcomes: keep it local, mask the sensitive spans, refuse the action, or ask the user for consent. Credentials, payment card numbers, and government IDs get the strictest handling. Masked values are swapped for stand-ins on the way out and restored when the cloud answer returns.

PII-Tracer is a 0.6B bidirectional encoder adapted from a Qwen3 backbone, replacing the causal mask with padding-aware bidirectional attention over a 4,096-token window. A linear tagging head emits 37 labels, one outside-span label plus BIOES position labels for each of nine PII types, and an auxiliary head predicts whether a conversation contains sensitive material. Training ran three epochs on roughly 714,000 samples; a constrained Viterbi decoder resolves the label sequence at inference.

PII-TRACE, the accompanying benchmark, contains 13,148 synthetic conversations across 13 languages and 10 writing systems, with 37,431 character-level identifier mentions. Its central claim is that finding most PII in a long conversation is not the same as finding every copy of it.

On results: across 12 detectors, PII-Tracer records the highest character F1 (0.629) and the second-best span-overlap and span-containment F1, behind GPT-5.6-sol. On consistency it leads by a wide margin — every mention found for 79.4% of recurring identifiers and 77.6% of cross-turn identifiers, versus 57.0% and 55.1% for GPT-5.6-sol. In the hardest bucket (6–10 mentions) it scores 0.691 against 0.464 for GPT-5.6-sol, 0.073 for GLiNER2-PII, and 0.045 for Claude Opus 4.8.

It is very interesting to know that single-window recall drops from 0.975 on conversations under 1,000 characters to 0.687 at 10,000 characters or more. Perplexity&#8217;s fix is decoding, not retraining: 50%-overlap sliding windows lift overall character recall from 0.830 to 0.965 and multi-mention consistent detection from 0.794 to 0.954 on the same checkpoint.

Explainer: how one task splits across cloud and Mac

&&

Models, controls, and availability

Perplexity&#8217;s announcement lists three local models at launch: Gemma 4 E4B, Qwen3.6 35B-A3B, and a Perplexity model post-trained for Computer. The product page&#8217;s setup flow points to a one-click download of PPLX Qwen 3.8 27B; Perplexity&#8217;s Hugging Face org carries matching pplx-computer-qwen-3-8-27b builds alongside pplx-pii-masking-vllm, the 0.6B token-classification model behind the gate.

For Enterprise, admins can set org-wide rules for what must stay on device, what may be masked, and what requires explicit approval — plus audit logs for when information leaves a machine. That is the piece that makes this usable for legal, healthcare, and financial teams rather than just interesting.

Key Takeaways

Hybrid compute starts tasks in the cloud and hands sensitive steps down to a local model on the Mac, mid-task.

An on-device PII classifier gates the boundary: keep local, mask, refuse, or ask.

PII-Tracer (0.6B) leads 12 detectors on character F1 (0.629) and on finding every recurring mention (79.4%).

Long-context recall drops to 0.687 past 10K characters; sliding-window decoding recovers it to 0.965.

Runs on Apple silicon, macOS 15+, 24GB unified memory minimum, for Pro, Max, and Enterprise.

Check out the Perplexity announcement, the PII-TRACE research post, and the model on Hugging Face. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Perplexity Releases Hybrid Compute on Mac: Cloud Agents Orchestrate Down to a Local Model, Gated On Device appeared first on MarkTechPost.