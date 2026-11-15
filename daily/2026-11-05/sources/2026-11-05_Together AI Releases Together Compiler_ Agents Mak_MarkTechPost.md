---
publish_time: 1793865778
link: https://www.marktechpost.com/2026/11/05/together-ai-together-compiler-continual-compilation-ai-inference/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Together AI 推出 Together Compiler（TKCC），一个由智能体驱动、随生产流量变化持续再优化推理的系统，已在多个无服务器推理端点运行，宣称让推理速度最高提升 2.6 倍。该工具把编译优化从静态调参转向「运行时自适应」，契合 Agent 化运维的趋势。
---

# Together AI发布Together Compiler：智能体驱动推理提速2.6倍

> 原文链接：https://www.marktechpost.com/2026/11/05/together-ai-together-compiler-continual-compilation-ai-inference/
> 来源：MarkTechPost

Together AI has introduced Together Compiler (TKCC), an agent-driven system that keeps re-optimizing inference as production traffic changes. Together Compiler already runs on several of Together&#8217;s serverless endpoints. The core claim for developers: an engine tuned once goes stale, so tuning should never stop.

TL;DR

System: It is an optimization system, tested on Kimi K3, GLM 5.3, MiniMax M3.1 Flash, DeepSeek v4.1 Flash and Llama 1B.

Runs on: NVIDIA B200, B300, GB300, H100, AMD MI355X and AWS Trainium2. Each run used at most 2 nodes per model.

Performance: Up to 2.6x higher TPS than the best published InferenceX configurations, in under 24 hours per setting.

Best: 1,111 P90 TPS per user on MiniMax M3.1 Flash (B200, batch size 1), 1.8x over the 633 TPS baseline.

Worst: GLM 5.3 on MI355X moved only from 463 to 480 TPS (about 4%).

What is Together Compiler?

Together Compiler is a continual compilation loop from Together AI that uses coding agents to rewrite a model&#8217;s forward pass. It takes a server launch command, a traffic profile and a hardware configuration. Agents propose faster forward passes, and a persistent engine measures each one. The winning code ships into the serving engine. When traffic drifts, the loop runs again.

Why does inference need continual compilation?

Together AI team reports that its traffic shape never sits still. Prompt lengths in one country ran about 97K tokens versus 70K elsewhere. One customer&#8217;s P90 input length grew from 18K to 33K tokens in 3 days.

Kernels tuned on random data can also mislead. Random inputs activated 13 to 38% more MoE experts than real traffic. One agent-written top-k kernel took 20 µs on random data. On real data at 70K context, it took up to 62 ms.

How does the persistent engine work?

Most agent loops restart vLLM, SGLang or TensorRT-LLM for every experiment. The research team measures 761 seconds of cold startup for MiniMax M3.1 Flash on TensorRT-LLM. Together Compiler starts the engine once. Agents submit a candidate forward pass over RPC. The server swaps the forward function pointer and re-captures CUDA graphs.

Two measurement tiers balance speed and fidelity. A fast tier serves 12 layers for quick screening. A slow tier serves 60 layers to confirm gains on real distributions. Two tiers tested 8.1x more candidates than one slow tier (1,354 vs 168). They also found a solution 7.2% faster. Together AI team reports 252x higher agent experiment throughput than an engine-restart baseline.

How does it choose a parallelism layout?

A cost model ranks tensor, expert, data and context parallel layouts before agents start. It mixes spec-sheet numbers, microbenchmarks and measured forward passes. It also uses measured MoE expert imbalance and uneven request lengths. On Kimi K3, it found a production layout with up to 24% higher TPS.

What did agents need from human experts?

An expert-curated knowledge base produced 25 to 31% lower speedup after 12 hours. Naive agents told to make the forward pass &#8220;as fast as possible&#8221; beat expert strategies. The ensemble scores were 6.2x versus 4.9x after 10 trials. Custom logging structures ate up to 43% of tool calls. Together AI now gives agents raw engine source code, not an intermediate representation.

Benchmarks: how fast is Together Compiler?

On SemiAnalysis InferenceX&#8216;s AgentX workload, Together Compiler beat the best open configurations by up to 2.6x TPS. Each setting ran under 24 hours on at most 2 nodes.

Batch size 1, P90 TPS per user (Together Compiler vs InferenceX best, self-reported):

MiniMax M3.1 Flash (B200): 1,111 vs 633

DeepSeek v4.1 Flash (GB300): 1,205 vs 943

GLM 5.3 (B200): 417 vs 329

Kimi K3 (GB300): 450 vs 423

GLM 5.3 (MI355X): 480 vs 463

For MiniMax, the cost model picked TP8 over the baseline&#8217;s TP4. That halves each GPU&#8217;s weight traffic in memory-bound decode.

On Llama 1B at batch size 1, it beat Hazy Research megakernels, Mirage and CUDA-graph baselines by up to 1.7x. Beyond LLMs, it sped up 8 scientific models by 1.5x to 6.4x with bit-exact outputs. Claude Code with /goal reached 1.2x to 4.4x and failed on AIFS-ENS 2.0.

How does it compare with other agentic optimization systems?

MetricsTogether Compiler Cursor + NVIDIA multi-agent AMD GEAK Apple RSI-Inference BenchTypeProduction optimization loopMulti-agent kernel optimizerTriton kernel agent frameworkBenchmark for coding agentsScopeFull forward pass inside the serving engine235 standalone CUDA kernels (SOL-ExecBench)Individual Triton kernels37 tasks editing vLLM or SGLangMeasurementPersistent engine, hot reload, 2 tiers, real trafficSOL-ExecBench on 27 B200 GPUsTritonBench-revised and ROCm benchmarkVerifier builds the engine and serves the modelHardwareB200, B300, GB300, H100, MI355X, Trainium2B200AMD Instinct MI300XH100, B200Main resultUp to 2.6x TPS vs InferenceX best1.38x geomean, wins on 149 of 235Up to 2.59x speedup, up to 63.33% correctnessScores agents; no single system resultTime budgetUnder 24 hours per setting3 weeksNot disclosedUp to 8 hours per taskAvailabilityLimited beta for Together customersResults in public repoOpen sourceApple Sample Code License

Key Takeaways

Together Compiler re-optimizes inference continually as traffic shifts.

Persistent engines with hot reload deliver 252x more agent experiments.

Up to 2.6x TPS over the best InferenceX configs within 24 hours.

Naive agents beat expert knowledge bases and curated strategies.

Self-reported; gains range from about 4% to 2.6x across settings.

Check out the paper, the Together Compiler blog and the Polymorphic Inference post. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Together AI Releases Together Compiler: Agents Make Inference Up to 2.6x Faster appeared first on MarkTechPost.