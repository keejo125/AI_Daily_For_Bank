---
publish_time: 1787701688
link: https://www.marktechpost.com/2026/08/25/liquid-ai-open-sources-pipette-a-reproducible-benchmarking-suite-that-measures-on-device-models-quantization-runtime-and-hardware-together/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Liquid AI 联合 Artificial Analysis 开源 Pipette，一套面向端侧基础模型的基准测试平台，把模型表现视为『模型+量化+运行时+设备』完整配置的属性而非孤立模型指标。首发数据集覆盖 1000+ 模型×量化×运行时×设备×上下文配置，横跨 30+ 模型与 llama.cpp 在 macOS/iOS/Windows/Android 的构建，上下文长度 256–8192 Token，含五项端侧性能指标。
---

# Liquid AI 开源 Pipette：端侧模型+量化+运行时+设备的可复现基准平台

> 原文链接：https://www.marktechpost.com/2026/08/25/liquid-ai-open-sources-pipette-a-reproducible-benchmarking-suite-that-measures-on-device-models-quantization-runtime-and-hardware-together/
> 来源：MarkTechPost

Model cards report quality under server-class, full-precision conditions. Those numbers rarely predict how the same model behaves on a phone. This week, Liquid AI released Pipette. It is an open-source platform for benchmarking foundation models on edge devices, built in partnership with Artificial Analysis as an independent methodology validator. Pipette treats on-device behavior as a property of the deployed system, not the model in isolation. Its unit of measurement is a full configuration: model + quantization + runtime + device. The launch dataset covers five on-device performance metrics across more than 1,000 model × quantization × runtime × device × context configurations, spanning 30+ models, llama.cpp builds for macOS, iOS, Windows and Android, and context lengths from 256 to 8,192 tokens. Initial verified results come from a MacBook Pro with M5 Max, an iPhone 17 Pro and a Galaxy S26 Ultra. The practical claim is testable: two 350M models at the same quantization on the same phone retain 78.4% and 33.8% of decode throughput at 4,096 tokens.

Is it deployable?

Yes, Pipette ships as Apache 2.0 infrastructure (pipette-mgmt, pipette-clients, pipette-scores), a public results dataset, a hosted dashboard, and native iOS and Android benchmark apps. Nothing is waitlisted. Publication of community-submitted results is still in beta.

Which companies: Any team shipping a model onto hardware it does not own. Solo developers and seed-stage startups can use the dashboard and apps without infrastructure. Mid-market product teams can run the clients across an internal device fleet. Large OEMs, chip vendors and enterprises can operate the whole pipeline behind their own firewall.

Industries: Consumer electronics and smartphone OEMs, automotive, industrial and robotics, healthcare devices, financial services, defense — anywhere latency, privacy or connectivity forces inference onto the device.

Applications: Model and quantization selection before a sprint commits; SoC and hardware procurement validation; regression testing when a runtime, OS or driver updates; context-length capacity planning; independent verification of vendor performance claims.

What Liquid AI shipped

Liquid AI released Pipette in partnership with Artificial Analysis, an independent validator that reviewed and verified the methodology. The premise is narrow and useful: on-device behavior is a property of the deployed system, not of the model in isolation.

The launch dataset covers five on-device performance metrics across more than 1,000 model × quantization × runtime × device × context configurations. It spans 30+ models, multiple quantization formats, llama.cpp builds for macOS, iOS, Windows and Android, and context lengths from 256 to 8,192 tokens. Initial published results come from a MacBook Pro with M5 Max, an iPhone 17 Pro and a Galaxy S26 Ultra, with AMD Ryzen AI Max+ 395 and Radeon 8060S results listed as coming soon.

In Pipette, the unit of measurement is a deployment configuration: model + quantization + runtime + device. A benchmark then defines the metric and token shape, producing a latency, throughput or memory result. Quality is tracked separately on IFBench, GPQA Diamond and MATH-500. Those quality scores currently come from llama.cpp evaluation runs on NVIDIA H100 80GB reference systems, then get matched to on-device runs sharing the same model and quantization — a quality number shown next to phone throughput was not produced on the phone.

Why the deployment context changes the answer

Four published comparisons show how far a configuration can move a decision:

Context scaling can diverge at identical parameter counts. At Q4_K_M on Galaxy S26 Ultra, Granite-4.0-H-350M retains 78.4% of its decode throughput from 256 to 4,096 input tokens, while Granite-4.0-350M retains only 33.8%.

Sparse activation buys speed, not memory. At 2,048 input tokens on the same phone, LFM2.5-8B-A1B decodes 2.4x faster than Qwen3.5-4B and 2.6x faster than Ministral-3-3B-Instruct-2512. It activates 1.5B of 8.5B parameters per token, yet still peaks at 5.29 GiB because all expert weights occupy memory.

Speed and quality do not co-locate. On iPhone 17 Pro at Q4_K_M, MiniCPM5-1B completes a 2,048-in / 256-out workload in 3.47 seconds versus 4.12 seconds for LFM2.5-1.2B-Instruct, a 15.8% reduction in elapsed time. On the same artifacts, LFM scores 9.0 points higher on MATH-500.

Near-identical system profiles can hide task-level reversals. At Q4_K_M and 2,048 input tokens on M5 Max, Granite-4.1-8B and Ministral-3-8B-Instruct-2512 differ by 2.4% in decode throughput and 1.2% in peak RAM. Granite leads IFBench by 7.3 points; Ministral leads GPQA Diamond by 14.0 points.

How the measurements are produced

Performance runs follow a published methodology: fixed token shapes, greedy decoding, a discarded warm-up, five measured repetitions and readiness gating. Before each timed repetition, a platform-specific check verifies thermal and load conditions; failing runs are not published. Evaluations use a separate protocol with deterministic, model-blind scoring, and pipette-scores never sees generation provenance. Every submission records benchmark version, token shape, model artifact, quantization, runtime version and settings, and device hardware and OS.

Interactive explainer

&&

Key Takeaways

Pipette benchmarks configurations, not models: model + quantization + runtime + device.

Apache 2.0 stack, 1,000+ configurations, 30+ models, three verified devices at launch.

Quality evals run on H100 references and are matched to on-device performance, not measured on-device.

Identical parameter counts can differ 78.4% vs 33.8% in context-scaling retention.

Check out the Technical Details and Leaderboard. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Liquid AI Open-Sources Pipette: A Reproducible Benchmarking Suite That Measures On-Device Models, Quantization, Runtime and Hardware Together appeared first on MarkTechPost.