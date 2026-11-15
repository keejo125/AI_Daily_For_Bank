---
publish_time: 1789077426
link: https://www.marktechpost.com/2026/09/10/nvidia-details-bionemo-inference-runtime-bioir-2-90x-higher-boltz-2-folding-throughput-and-58-5k-residues-per-gpu-hour-on-8xh100/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA 详解 BioNeMo Inference Runtime（BioIR）：在保持标准 PyTorch 工作流的同时加速受支持的结构预测模型。BioIR 已在生产规模运行，支撑 AlphaFold Database 扩展——跨4777个蛋白质组生成约3100万候选复合物、释放181万高置信预测。在8×H100上，Boltz-2 折叠吞吐提升2.90倍，达5.85万残基/GPU·小时。BioIR 以开源仓库（含预编译 CUBIN 的 wheel）形式提供。
---

# NVIDIA 详解 BioNeMo 推理运行时 BioIR：折叠吞吐2.90倍，8×H100单卡5.85万残基/小时

> 原文链接：https://www.marktechpost.com/2026/09/10/nvidia-details-bionemo-inference-runtime-bioir-2-90x-higher-boltz-2-folding-throughput-and-58-5k-residues-per-gpu-hour-on-8xh100/
> 来源：MarkTechPost

Biomolecular structure prediction has shifted from single-target runs to proteome-scale worklists. The bottleneck is no longer whether a model can fold a protein. It is how fast an entire queue of independent targets moves through parsing, featurization, GPU inference, and output writing. NVIDIA&#8217;s new technical deep dive walks through BioNeMo Inference Runtime (BioIR), a Python library that accelerates supported structure-prediction models on NVIDIA GPUs while keeping the standard PyTorch workflow. BioIR has already run at production scale. It powered the recent expansion of the AlphaFold Database, generating protein-complex structures across 4,777 proteomes, about 31 million candidate complexes, with 1.81 million released as high-confidence predictions.

Is it deployable? Yes. BioIR is available now as an open GitHub repository with a wheel containing precompiled CUBINs. Runtime use needs Python 3.12+, a compatible NVIDIA GPU and driver, a staged model checkpoint, and per-chain A3M MSAs. It does not require nvcc, CUDA source, CMake, or the CUDA toolkit.

What is BioIR

BioIR targets the operations that general-purpose inference stacks do not fully optimize. These include Pairformer and Evoformer stacks, triangle operations, pairwise attention, diffusion transformers, and atom-level modules. Models stay ordinary torch.nn.Module objects. There is no engine build, export step, or separate artifact between a checkpoint and a forward pass.

There are 2 ways to use it. The end-to-end processor moves an InputRequest through parsing, tokenization, feature generation, GPU inference, and PDB or mmCIF writing. Direct PyTorch integration lets developers construct a supported model or reuse selected optimized modules inside custom code. The tutorial demonstrates the processor path with Boltz-2 (model_source="boltz-2"). Each protein chain requires an A3M MSA. Paired or unpaired MSAs are accepted for inputs with multiple non-identical protein chains. Templates can be supplied manually because BioIR does not run HHsearch or HMMsearch. The processor supports ligand structure prediction but not ligand-affinity prediction.

Three Layers of Acceleration

BioIR optimizes at 3 distinct layers, each targeting a different bottleneck:

Kernel selection: Supported operations pick compatible BioIR custom, cuEquivariance, or PyTorch fallback implementations based on model configuration, GPU, data type, and tensor shape.

Module optimization: A separate optimize() mechanism enables CUDA Graph capture for compatible modules, cutting launch overhead.

Pipeline scaling: A Ray executor places 1 complete model replica on each visible GPU in a node and distributes independent inputs among them. CPU stages (parsing, featurization, writing) overlap with GPU folding.

Note: Ray does not split a single forward pass across GPUs. Replica mode scales worklists, not individual targets. Per the support matrix, context-parallel folding is planned but not yet available. The capacity rule is simple: engine_stage.compute x num_gpus must not exceed visible GPUs.

At the model-forward level, NVIDIA&#8217;s early benchmarking reports geometric-mean speedups over an OSS torch.compile baseline of 1.55x (OpenFold3), 1.78x (Boltz2), and 2.56x (OpenFold2 monomer) on H100. H200 numbers are similar at 1.54x, 1.75x, and 2.61x. These were measured across 17 inputs spanning 29 to 1,734 residues.

&&

The Benchmark: 1,000 Human Dimers on 8xH100

To quantify end-to-end delivery, NVIDIA team ran a matched benchmark on 1,000 human dimer targets with combined sequence lengths below 2,800 residues. The comparison pitted BioIR-accelerated Boltz-2 against a torch-compiled open-source Boltz-2 implementation on 8xH100 80GB GPUs. Both used identical targets, staged MSAs, inference recipe (3 recycles, 200 sampling steps, 5 diffusion samples), and GPU configuration.

The results:

BioIR completed all 1,000 targets and delivered 58.5K successfully folded residues per allocated GPU-hour.

The public implementation delivered 20.2K residues per GPU-hour and ran out of memory on 29 targets.

Net result: a 2.90x improvement in residue-normalized throughput.

These numbers are folding-stage measurements specific to this dataset and hardware. They exclude MSA generation, preprocessing CPU allocations, storage, data transfer, and retries. The blog explicitly warns against generalizing them to all BioIR-supported models or datasets.

Energy at One Million Targets

Extrapolating the benchmark linearly to 1 million comparable targets, BioIR is estimated to need 11 MWh versus 35 MWh for the public implementation using 8-GPU TDP equivalents. Using full-node maximum-power equivalents, the estimate is 21 MWh versus 64 MWh. These are rated-power, folding-only estimates for IT equipment, not metered measurements, and exclude data center overhead such as PUE. Still, a 23 to 43 MWh saving per million targets is a material number for proteome-scale campaigns.

Key Takeaways

BioIR accelerates Boltz-2, OpenFold2, and OpenFold3 inference on NVIDIA GPUs while staying in plain PyTorch.

Matched 8xH100 benchmark: 58.5K vs 20.2K folded residues per GPU-hour, a 2.90x throughput gain.

Ray replica mode scales independent worklists; it never splits 1 forward pass across GPUs.

Estimated energy for 1M targets drops from 35 MWh to 11 MWh at 8-GPU TDP equivalents.

Already proven at scale: 31M candidate complexes generated for the AlphaFold Database expansion.

Check out the technical blog, GitHub repo, docs, and the BioNeMo Agent Toolkit for agentic orchestration. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Details BioNeMo Inference Runtime (BioIR): 2.90x Higher Boltz-2 Folding Throughput and 58.5K Residues per GPU-Hour on 8xH100 appeared first on MarkTechPost.