---
publish_time: 1787481899
status: confirmed
category: 国际
is_model_related: false
source: MarkTechPost
link: https://www.marktechpost.com/2026/08/23/meet-freetoken-an-edge-native-moe-serving-engine-that-runs-753b-glm-5-2-on-a-single-workstation-gpu/
digest: |
  UC Berkeley 与 UT Austin 的研究团队提出 FreeToken，一款边缘原生 MoE 推理服务引擎，把个人机器（含消费级 GPU）当作统一的弹性推理平台，将计算与模型状态持续映射到机器实际拥有的 GPU/CPU/内存/互联带宽上。它可在 8GB 笔记本 GPU 上以交互速度跑 35B 模型、游戏主机上跑 284B、单张工作站卡跑 753B 的 GLM-5.2。FreeToken 以 Apache-2.0 开源（PyPI freetoken v0.1.2），提供 ft serve（兼容 OpenAI/Anthropic 端点）与 ft launch claude（对接 Claude Code/Codex/OpenCode）。其带宽自适应执行、语义感知缓存与弹性内存管理三项机制，在 RTX 5090 上较 llama.cpp/Ollama/KTransformers 基线提速 1.5—2.3 倍，最适合医疗、法律、金融、IP 密集研发等数据不出本机的场景。
---

# 边缘原生 MoE 推理引擎 FreeToken：单张工作站 GPU 跑起 753B 的 GLM-5.2

> 原文链接：https://www.marktechpost.com/2026/08/23/meet-freetoken-an-edge-native-moe-serving-engine-that-runs-753b-glm-5-2-on-a-single-workstation-gpu/
> 来源：MarkTechPost

Frontier open-weight models are shipping faster than the hardware assumptions around them. Kimi-K3, GLM-5.2 and DeepSeek-V4-Flash are closing the capability gap with proprietary systems, but releasing parameters only determines who can obtain a model — not who can afford to run it. Serving them still assumes datacenter-class GPU clusters, and as agentic workloads push inference demand up, that cost lands hardest on individual developers and small teams. Meanwhile, more than a hundred million consumer machines already carry discrete GPUs. A team of researchers from UC Berkeley and UT Austin propose FreeToken. The research team argued the missing piece is not hardware but a serving system: it treats a personal machine as a unified, elastic inference platform rather than a small GPU, and continuously maps computation and model state onto whatever GPU, CPU, memory and interconnect bandwidth the machine actually has. The result is a 35B model at interactive speed on an 8 GB laptop GPU, 284B on a gaming desktop, and the 753B GLM-5.2 on a single workstation card.

Is it deployable?

Yes, FreeToken is Apache-2.0 on GitHub, published on PyPI as freetoken v0.1.2 (uv pip install "freetoken[accel]"), and shipped as a one-click desktop app for Windows and Linux at flashml.ai. The CLI targets Linux x86_64 with an NVIDIA GPU on driver r580+ (CUDA 13). ft serve exposes OpenAI- and Anthropic-compatible endpoints on port 1919, and ft launch claude wires up Claude Code, Codex, OpenCode or OpenClaw against your own box.

Who it fits: solo developers, startups and SMB engineering teams whose agent token bills already exceed the cost of a GPU they own; enterprises should treat it as an air-gapped or regulated-workload path, not a datacenter replacement. Strongest industry fit: healthcare and legal (data never leaves the machine), defense, finance, and IP-heavy R&D. Typical applications: local coding agents, private code review, offline contract analysis, synthetic-data generation, batch evals. 

The gap it targets

Mixture-of-Experts makes local frontier inference arithmetically feasible. DeepSeek-V4-Flash activates 6 of 256 routed experts in each of 43 layers, so only 13B of its 284B parameters participate in any single token. Sparsity does not shrink the expert pool, though — at FP4 the full set is roughly 140 GB, so inactive experts sit in host memory and enter the execution path on demand.

The research team isolates three failure modes in existing engines (llama.cpp, KTransformers, Ollama, MoE-Infinity):

Prefill destroys sparsity: Thousands of tokens per layer route to nearly the whole expert set, so a prefill pass streams the entire pool across PCIe — about two seconds on an RTX 5090, five on PCIe 4.0 desktops, ten or more on the x8 links common in laptops.

Static placement misses decode traffic: llama.cpp assigns MoE tensors at load time; KTransformers pins a &#8220;hot&#8221; subset. Routing shifts every token, so most expert evaluations fall to the CPU while the GPU and the PCIe link sit idle.

Consumer CPUs cannot carry the remainder: Dual-channel DDR5 delivers 80–90 GB/s against the 1–1.8 TB/s an RTX 4090 or 5090 draws from on-package memory.

&&

Three mechanisms

Bandwidth-adaptive execution (the q* policy): Because DMA transfers and CPU expert execution read from the same host-memory subsystem, a saturated PCIe link leaves a residual bandwidth of B_H − B_P. FreeToken splits each step&#8217;s m cache misses accordingly: q* ≈ m × B_P / B_H experts are filled into the GPU cache, the rest are computed in place on the CPU, and the two partial sums merge exactly — no approximation, no router modification. Both bandwidths are profiled on the deployed machine (ft bench bw), which matters: measured B_P:B_H is 52.7:77.3 on an RTX 5090 server but 11.8:47.5 on a 4060 laptop.

Semantic-aware caching: During prefill, full-layer double buffering streams layer l+1 while the GPU computes layer l. Recurrent-state checkpoints are anchored at special-token boundaries — thinking blocks, tool calls, tool outputs — precisely where agent harnesses truncate context, so an edit re-prefills only the new suffix. During decode, a shared LRU expert cache spanning all MoE layers follows the router instead of a placement frozen at load time.

Elastic memory management: At scheduler safe points the GPU expert cache is rebuilt under a revised VRAM budget without restarting the engine or reloading the host pool. Experts are read from disk straight into their final host layout, then pinned; no GPU warmup is required because the first request is served with a cold cache.

Results

On an RTX 5090, FreeToken sustains 77–83 tok/s on Qwen3.6-35B-A3B (BF16) and 22–25 tok/s on DeepSeek-V4-Flash (MXFP4) — 1.5–2.3× the strongest baseline, with decode staying within 12% of the single-turn rate across three agentic workloads. Worst-case TTFT stays below 44 s in every cell; llama.cpp hits 232 s, Ollama 179 s and KTransformers 946 s somewhere in the matrix, past the point where agent clients time out.

At equal cache capacity (37% of the Qwen3.6 pool), the global LRU misses 16% of decode-time expert reads against 41% for KTransformers and 62% for llama.cpp. On an 8 GB RTX 4060 laptop the NVFP4 build serves 35B at 39.3 tok/s — above the 33 tok/s median decode speed measured for Codex in production traces. On a single RTX PRO 6000, GLM-5.2 (753B, 40B active) runs at 14.9 tok/s versus llama.cpp&#8217;s 7.3.

Data Check

Reality Check &#183; FlashML FreeToken
INFLATION SCORE 59/100

As of Aug 23, 2026 &#183; default mode &#183; audited: arXiv:2608.16157, GitHub repo, flashml.ai

3Verified

9Self-rep.

4Misleading

0Contradicted

0Not found

Score formula: 8 &times; misleading + 15 &times; contradicted + 3 &times; self-reported, capped at 100. The score is driven by the self-reported column, not by dishonesty &#8212; the code went public six days before this audit, so no independent reproduction exists yet.

Claim table &#183; 16 claims

ClaimTheir numberIndependent checkVerdict & source

Decode, Qwen3.6-35B-A3B BF16, RTX 509077&#8211;83 tok/sNone foundSELF-REPORTEDPaper Fig 3
Decode, DeepSeek-V4-Flash MXFP4, RTX 509022&#8211;25 tok/sNone foundSELF-REPORTEDPaper Fig 3
Decode speedup vs strongest baseline1.5&#8211;2.3&times;Recomputes exactly from Fig 3SELF-REPORTEDPaper &#167;5.2
Decode stability across agent workloadswithin 12% of W1None foundSELF-REPORTEDPaper &#167;5.2
Worst-case TTFT vs baselines<44 s vs 232 / 179 / 946 sNone foundSELF-REPORTEDPaper &#167;5.2
4060 laptop &#8220;exceeds Codex median 33 tok/s&#8221;39.3 vs 33TraceLab 33.9 is normalized; Codex pure decode median 57.1, w.avg 61.0MISLEADINGarXiv:2606.30560
Laptop is &#8220;92% of the RTX 4090 rate&#8221;39.3 / 42.9Arithmetic correct, but 39.3 is NVFP4 and 42.9 is BF16MISLEADINGPaper Fig 5
GLM-5.2 753B on one RTX PRO 600014.9 vs llama.cpp 7.3None foundSELF-REPORTEDPaper &#167;5.3
Cross-hardware lead, five consumer systems1.3&#8211;2.1&times;Recomputes exactly from Fig 5SELF-REPORTEDPaper Fig 5
Decode expert miss rate at equal capacity16% / 39%None found; trace replay, not live servingSELF-REPORTEDPaper Fig 4b
Prefill 8,192-tok chunk; overlap penalty1.19&#8211;1.22 s; 19/25/26%None foundSELF-REPORTEDPaper Fig 4a
&#8220;753B on a single workstation GPU&#8221; framing1 GPUTrue for VRAM; hosts carry 512 GiB and 192 GB DRAMMISLEADINGPaper Table 1
Baselines run at 6 CPU threads on rented servers6 threadsKTransformers&#8217; core contribution is many-core AMX CPU kernelsMISLEADINGPaper &#167;5.1
&#8220;Supports more than 20 MoE models&#8221;20+Public docs/models.md itemizes ~17 known-good MoE checkpointsSELF-REPORTEDrepo docs
License and distributionApache-2.0, PyPI v0.1.2LICENSE file and PyPI JSON API both confirmVERIFIEDGitHub, PyPI
Consumer discrete-GPU install base (Steam basis)~72% NVIDIA; 4060 Laptop 3.81%Matches Valve June 2026 survey per multiple outletsVERIFIEDValve, Jul 2026
Internal arithmetic across abstract and &#167;5all ratiosEvery published ratio recomputes from Figures 3 and 5; zero errorsVERIFIEDrecomputed

Flags explained

Denominator games &#8212; the Codex comparison mixes two metricsFreeToken reports decode throughput and TTFT separately, so its 39.3 tok/s is a pure decode rate. TraceLab&#8217;s 33.9 tok/s is a normalized rate that folds per-step TTFT into decode; the same paper puts Codex&#8217;s pure decode median at 57.1 tok/s. Like-for-like, 39.3 does not exceed Codex &#8212; it is roughly two thirds of it.

Denominator games &#8212; &#8220;92% of the RTX 4090 rate&#8221; compares 4-bit to 16-bitThe 39.3 tok/s laptop figure is the NVFP4 build; the 42.9 tok/s RTX 4090 figure is BF16. Disclosed in the Figure 5 caption, but the prose states the ratio without the precision caveat.

Denominator games &#8212; &#8220;single GPU&#8221; omits the host requirementThe 753B GLM-5.2 tier sits behind 512 GiB of DDR5 on a Xeon Platinum 8559C; the 284B &#8220;gaming desktop&#8221; carries 192 GB. One GPU is accurate. One machine at consumer prices is not what those configurations describe.

Settings mismatch &#8212; baselines capped at 6 CPU threadsDisclosed and defensible: the paper caps rented dual-socket servers to emulate edge hosts and validates on two real edge machines at full threads. But KTransformers is built around AMX-optimized many-core CPU expert execution, so read its column as &#8220;KTransformers on an edge-class host,&#8221; not as its ceiling.

Counterweight &#8212; the arithmetic is cleanEvery ratio in the abstract and results recomputes correctly: 1.81 / 1.87 / 2.10 / 2.25&times; for Qwen3.6, 1.92 / 1.84 / 1.52 / 1.65&times; for DeepSeek-V4-Flash, 2.04&times; for GLM-5.2. No inflated rounding, no unexplained gaps between figures and prose.

Key takeaways

The paper is arithmetically clean &#8212; every published ratio recomputes from its own figures.

Nothing is independently reproduced yet; 9 of 16 claims are self-reported by necessity, not evasion.

Sharpest flag: 39.3 tok/s beats Codex&#8217;s normalized 33.9, not its pure decode median of 57.1.

&#8220;Single GPU&#8221; headlines quietly require 192&#8211;512 GB of host DRAM.

Baseline KTransformers runs at 6 CPU threads, below the many-core AMX config it targets.

Reality Check by Marktechpost &#183; verified Aug 23, 2026

Key Takeaways

FreeToken splits MoE cache misses between PCIe fills and CPU execution using measured bandwidths, not a fixed offload rule.

Expert output stays bit-exact — no router changes, no expert substitution, no precision relaxation.

1.5–2.3× decode throughput over llama.cpp, Ollama and KTransformers, with tail TTFT under 44 s.

35B at 39.3 tok/s on an 8 GB laptop GPU; 753B GLM-5.2 on one workstation GPU.

Apache-2.0, on PyPI and as a Windows/Linux desktop app — deployable this afternoon.

Check out the PAPER, GITHUB REPO and PROJECT. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet FreeToken: An Edge-Native MoE Serving Engine that Runs 753B GLM-5.2 on a Single Workstation GPU appeared first on MarkTechPost.