---
publish_time: 1793001405
link: https://www.marktechpost.com/2026/10/26/tsinghua-akv-kv-cache-engineering-llm-agents/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  清华与港中文（CUHK）开源 AKV，一套面向 LLM Agent 的 KV 缓存工程服务系统与策略库（Apache 2.0，基于 SGLang）。与传统上下文工程“总结历史”不同，AKV 让 Agent 丢弃并保留选定的 KV 缓存条目，文本轨迹不变、保留条目免重算。在 3 个模型、4 个 Agent 基准上平均成本降 27.7%、任务分升 1.7 点。
---

# 清华大学开源 AKV：面向 LLM Agent 的 KV 缓存工程系统

> 原文链接：https://www.marktechpost.com/2026/10/26/tsinghua-akv-kv-cache-engineering-llm-agents/
> 来源：MarkTechPost

Tsinghua University and CUHK researchers open-sourced AKV, a serving system for KV cache engineering in LLM agents. Instead of summarizing old history, agents drop selected KV cache entries and keep reusing the rest. Across 3 models and 4 agent benchmarks, average cost falls 27.7%. Average task score rises 1.7 points. The code is Apache-2.0 licensed and builds on SGLang.

TL;DR

What it is: Serving system plus policy library, no weights. Tested on GPT-OSS-120B (5.1B active), MiniMax-M2.7 (230B total, 10B active) and MiroThinker-1.7-Mini (30B total, 3B active).

Runs on: NVIDIA GPUs via SGLang. Paper used 8 A800-80GB GPUs in BF16. Quick start serves GPT-OSS-120B on 2 GPUs (tensor parallel 2).

Performance: 27.7% lower average cost and +1.7 points average score versus threshold summarization.

Best: GPT-OSS-120B on SWE-bench Verified: cost per task 20.0 to 9.7 cents, score 40.0 to 43.2.

Worst: MiniMax-M2.7 on BrowseComp-Plus scores 58.9, 3.4 points below Text Engineering&#8217;s 62.3.

What is cache engineering, and how is it different from context engineering?

AKV is a Tsinghua serving system that lets LLM agents drop and reposition their own KV cache.

Context engineering trims or summarizes the text history. Editing that prefix invalidates every later KV state. The retained suffix must then be re-prefilled. Harnesses therefore summarize late and aggressively, which can lose details from middle rounds.

Cache engineering leaves the text trajectory untouched. It only changes which KV entries stay visible to attention. Retained entries are reused without recomputation. They can still carry information from dropped messages. In the research paper&#8217;s cost analysis, KV cache reads made up 82.4% of total API cost.

How does AKV work?

AKV defines 3 cache operations. Append is the standard update for new tokens. Drop removes selected entries from future attention without changing positions. Repos rewrites retained keys to positions 0 through r-1 using a RoPE rotation. Values stay unchanged, so no hidden states are recomputed. In ablations, adding Repos raised GPT-OSS-120B&#8217;s BrowseComp-Plus pass rate from 55% to 62%.

The hard part is serving. Identical tokens can produce different cache states under different operation histories. Plain prefix matching could reuse the wrong states. AKV extends SGLang&#8217;s radix tree with drop and reposition nodes. It frees dropped KV only when no active request still needs it. Segment-batch attention restores evicted states in 1 prefill pass.

What does the AKV API look like?

The interface is stateless and OpenAI-compatible. Clients send the full message history and two optional fields. drop_message maps a trigger message index to the messages to drop. reposition lists the indices after which positions get compacted.

A CachePolicy builds those fields from a trigger, a selector and a reposition rule. Built-in policies are turn-based, token-based or model-based. A CacheTool lets the model call drop_context itself.

How does AKV perform on agent benchmarks?

The main policy is a tool-response rolling drop that keeps the latest 12 tool responses. The Standard baseline summarizes at 96K tokens (192K for MiroThinker). Text Engineering summarizes at 48K. Benchmarks are BrowseComp-Plus, GAIA-Text, SWE-bench Verified and xbench-DeepSearch-2510.

ModelStandard score / costText Eng. score / costAKV score / costMiniMax-M2.752.4 / 5.052.8 / 5.753.7 / 4.4GPT-OSS-120B51.0 / 11.248.3 / 10.253.1 / 7.3MiroThinker-1.7-Mini44.1 / 20.437.1 / 18.145.8 / 14.8

Average pass rate (%) and cost (US cents per task) across 4 benchmarks. Source: Table 1 of the paper.

AKV also cuts cost 21.9% versus Text Engineering. The accuracy gap opens on long runs. On BrowseComp-Plus at 96K tokens and above, GPT-OSS-120B scores 37% with AKV. Standard scores 24% and Text Engineering 32%, per the project page.

Costs are API-equivalent estimates from published rates. Repositioned tokens are charged at the cache-hit rate, a deliberately conservative choice.

How fast is AKV in serving benchmarks?

Serving tests ran GPT-OSS-120B on 80 long-context SWE-bench Verified tasks. At each method&#8217;s peak setting, AKV delivers 1.18x output throughput and 1.53x input throughput. P95 request latency is 1.51x faster.

At concurrency 16, Standard&#8217;s P95 latency hits 229.90 seconds versus 30.63 for AKV. KV pressure pushes Standard into repeated re-prefill. Per decode step, full-attention time falls from 7.082 to 2.849 ms.

On 100 SWE-bench Verified tasks under a GPU budget, AKV reached about 47% pass rate. Standard reached 40.7% and Text Engineering 32.3%.

Can agents tune their own cache policy?

MiniMax-M2.7 refined policies on 20 BrowseComp-Plus tasks, then ran 100 held-out tasks. The iteration-6 policy cut cost 17.8% versus Standard at baseline accuracy. The abstract reports 7.1% savings beyond the expert-designed policy.

Exposing cache control as a tool also helped accuracy. GPT-OSS-120B rose from 52.1 to 61.0 on a 100-task subset. MiniMax-M2.7&#8217;s cost rose, though, from 5.4 to 5.9 cents.

AKV vs other KV cache approaches

MetricsAKVThreshold summarizationSGLang RadixAttentionStreamingLLMSnapKVWorks onKV cache, agent-directedText historyKV cache, prefix reuseKV cache, fixed windowPrompt KV cacheWhat gets droppedChosen by policy or model tool callHistory older than a token thresholdNothing, shared prefixes reusedMiddle tokens; keeps sinks and recent tokensLow-attention prompt positionsRe-prefill after reductionNoYes, retained suffixNot applicableNo cache refresh neededNot applicableTarget workloadMulti-turn tool-calling agentsAgent harnessesGeneral and agentic servingStreaming dialogueLong promptsReported headline-27.7% cost, +1.7 ptsBaseline in AKV paperUp to 6.4x throughputUp to 22.2x vs sliding-window recompute3.6x faster generation at 16KModelsQwen, GPT-OSS, MiniMax-M2AnyBroadLlama-2, MPT, Falcon, PythiaLlama, Mistral, MixtralFine-tuning neededNoNoNoNoNoLicenseApache-2.0Harness-dependentApache-2.0MITApache-2.0

The main numbers come from each project&#8217;s own paper and use different setups. They are not directly comparable.

Key Takeaways

AKV lets agents drop and reposition KV cache instead of rewriting history.

Average cost falls 27.7% and score rises 1.7 points across 3 models.

Repos lifts GPT-OSS-120B on BrowseComp-Plus from 55% to 62%.

At concurrency 16, P95 latency drops from 229.90 to 30.63 seconds.

Support covers only Qwen, GPT-OSS and MiniMax-M2 text models today.

Check out the Paper, GitHub Repo and Project Page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Tsinghua AI Open-Sources AKV, a Cache Engineering Server for LLM Agents on SGLang appeared first on MarkTechPost.