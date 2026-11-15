---
publish_time: 1793604509
link: https://www.marktechpost.com/2026/11/01/qwengpu-simt-gpu-compiled-into-qwen3-5-2b-weights-runs-cuda/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  开发者 Vixhal 在 GitHub 以 MIT 许可发布实验模型 qwenGPU：把一块 SIMT GPU 直接「编译」进 Qwen3.5-2B 的权重中，使其在前向推理过程中运行真实 CUDA（编译为 NVIDIA PTX）。模型由 Qwen3.5-2B（24 层）外加 45 个编译得到的 GPU 层共 69 层组成，上下文 262144 Token，可在 Apple 芯片、NVIDIA GPU 或 CPU 上以约 16GB 空闲内存运行。其思路是让精确计算发生在预训练 LLM 内部而非其外部，作为对「模型内计算」可行性的技术验证。
---

# qwenGPU：将 GPU 编译进 Qwen3.5 权重的实验模型

> 原文链接：https://www.marktechpost.com/2026/11/01/qwengpu-simt-gpu-compiled-into-qwen3-5-2b-weights-runs-cuda/
> 来源：MarkTechPost

qwenGPU is an experimental model that compiles a SIMT GPU directly into the weights of Qwen3.5-2B. Developer Vixhal (@TheVixhal) released it on GitHub under the MIT license. The model runs real CUDA, compiled to NVIDIA PTX, inside its own forward passes. For developers, it tests one idea: exact computation inside a pretrained LLM, not beside it. 

TL;DR

Size: Qwen3.5-2B (24 layers) along with 45 compiled GPU layers, 69 in total. Context: 262,144 tokens (base model).

Runs on: Apple silicon, an NVIDIA GPU or a CPU, with about 16 GB of free memory. No quantized build.

Performance: Every launch in the developer&#8217;s runs was exact; text drift is a KL of about 7e-4.

Best: The reference interpreter matched a real NVIDIA Tesla T4 on 49 of 49 kernels.

Worst: About 10 to 15 tokens per second on Apple MPS; Qwen-written CUDA passed 4 of 5.

What is qwenGPU?

qwenGPU is Qwen3.5-2B with 45 compiled transformer layers placed in front of Qwen&#8217;s own 24. None of those layers are trained. A compiler computes every weight. 

How does a GPU fit inside model weights?

The GPU is a 4-lane SIMT machine. It has 15 registers per lane, a 4-stage pipeline, a 32-block ROM and 126 memory words. It uses only Qwen3.5&#8217;s own layer types: Gated DeltaNet linear attention and SwiGLU MLPs.

The trick is the Gated DeltaNet recurrent state. In the circuit&#8217;s heads, the gate is held open and the write strength is 1. Every key is one-hot. Each update overwrites exactly 1 row, and a one-hot query reads it back. So each row works as a memory cell.

That state holds the program ROM, registers and global memory. The README lists 16 register rows per lane, with 1 that always reads zero. That matches the 15 usable registers in the X post.

The GPU supports integer arithmetic, predicates, divergent branches and loops. It also supports shared memory, atomicAdd, __syncthreads() and warp shuffles.

&&

What happens during a CUDA launch?

The host plays the role of NVRTC and the CUDA driver. It compiles CUDA to PTX with clang, then lowers PTX to machine blocks. It feeds the program and input arrays to the model as tokens.

From there, the model writes the launch itself. Each EXEC(b, w) token runs block b for warp w in 1 forward pass. The VAL tokens after it carry register results. Memory writes return as MEM records. The host reads results from the recurrent state and computes none of them.

In the demo video, a dot product of [1, 2, 3] and [4, 5, 6] returns 32. The model wrote that launch in 47 tokens.

Meet qwenGPU: Qwen3.5-2B with a SIMT GPU inside its weights, 45 compiled layers in front of Qwen’s own, using its Gated DeltaNet layers as registers and memory.

It runs real CUDA in its forward passes. The host compiles the kernel to PTX and loads it, then the model writes every… pic.twitter.com/iM5IETEbIv
&mdash; vixhaℓ (@TheVixhal) November 1, 2026

Does the GPU break Qwen&#8217;s text ability?

Not by the developer&#8217;s measure. The circuit is muted on text tokens, and Qwen&#8217;s own weights are unchanged. The merged model&#8217;s next-token distribution stays within a KL of about 7e-4 of the original.

How accurate is qwenGPU?

All numbers are self-reported, measured on Apple silicon with MPS in bf16:

Every launch was exact under --check replay.

The reference interpreter matched an NVIDIA Tesla T4 on 49 of 49 test kernels.

Normal mode answered 20 of 24 sampled chat questions with GPU-computed numbers.

Advanced mode wrote a correct kernel first try on 4 of 5 questions.

In normal mode, Qwen writes an expression like [1, 2, 3] @ [4, 5, 6] for ready-made kernels. In advanced mode, Qwen writes the CUDA kernel itself. The README warns that a 2B model&#8217;s CUDA is still unreliable.

How does qwenGPU compare with Qwenputer and Percepta?

qwenGPU uses the transformer compiler from Qwenputer by Divyansh Agrawal. Qwenputer compiles a 32-bit RISC-V CPU into Qwen3.5-4B. Percepta built a WebAssembly interpreter into a transformer with 2D attention heads in March 2026.

FeatureqwenGPUQwenputer (RISC-V)PerceptaBase modelQwen3.5-2B, 24 layersQwen3.5-4BCustom transformer with 2D attention headsMachine compiled in4-lane SIMT GPU32-bit RISC-V (RV32IM + Zba + bignum)WebAssembly interpreterPrograms it runsCUDA, lowered from PTXC and MicroPythonC, compiled to WebAssemblyCompiled layers4511Not disclosedWhere state livesGated DeltaNet stateGated DeltaNet stateExecution trace in contextHost roleCompiles CUDA to PTX, loads tokens, reads resultsLoads firmware; runs no computationNot disclosedCorrectness checkInterpreter matched Tesla T4 on 49 of 49 kernels0 mismatches in about 230,000 replayed positionsClaims millions of reliable stepsReported speed10 to 15 tokens/s (Apple MPS)About 3,200 trace tokens/s (L4, Triton)30,000+ tokens/s (CPU)Text drift vs baseKL about 7e-4KL 6e-4Not applicableLicenseMIT code; Apache-2.0 checkpointMIT code; Apache-2.0 weightsNot disclosed

The speed figures use different hardware and token types, so they are not directly comparable.

What do you need to run it?

The quickstart needs Python 3.11+, uv, just and about 16 GB of free memory. Advanced mode also needs clang with the NVPTX backend. just build downloads Qwen3.5-2B and compiles the GPU into it. No prebuilt checkpoint is published. A built checkpoint falls under Qwen&#8217;s Apache-2.0 license.

Key Takeaways

qwenGPU compiles a 4-lane SIMT GPU into Qwen3.5-2B as 45 untrained layers.

Gated DeltaNet state serves as registers, program ROM and global memory.

The model writes every CUDA launch step; the host only compiles and loads.

The interpreter matched a Tesla T4 on 49 of 49 kernels.

At 10 to 15 tokens per second, it is a research demo, not a runtime.

Check out the GitHub repo, the qgpu CUDA reference, the Qwen3.5-2B model card and the original X post. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet qwenGPU: Qwen3.5-2B With 45 Compiled GPU Layers That Run CUDA appeared first on MarkTechPost.