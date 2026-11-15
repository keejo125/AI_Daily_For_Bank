---
publish_time: 1790349285
link: https://www.marktechpost.com/2026/09/25/aikido-security-releases-altar-1-an-open-weight-security-model-pruned-from-glm-5-3-to-328-gb/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Aikido Security 发布首款开源权重安全模型 Altar-1，由 Z.AI 的 GLM-5.3（753B MoE）压缩而来，驱动其本地/空气隔离网络的自主体渗透测试设备 Aikido Machine。权重已公开于 HuggingFace，4×H200 即可运行。针对银行数据驻留、OT 无外网等“安全上下文不得出网”场景，改用开源权重化解合规风险，却带来部署开销；团队用两步压缩化解：先 AWQ INT4 量化，再以 Cerebras REAP 按路由权重与输出幅度剪枝，每层保留 256 个专家中的 168 个（去 34.4%），全程无需重训练。
---

# Aikido发布Altar-1：从GLM-5.3剪枝的开源安全模型

> 原文链接：https://www.marktechpost.com/2026/09/25/aikido-security-releases-altar-1-an-open-weight-security-model-pruned-from-glm-5-3-to-328-gb/
> 来源：MarkTechPost

Aikido Security has released Altar-1, its first open-weight security model. It is a compressed version of Z.AI&#8217;s GLM-5.3, built to run inside infrastructure the customer controls. Altar-1 powers Aikido Machine, the company&#8217;s autonomous pentesting appliance for on-prem and air-gapped networks. 

Is it deployable? Yes, the weights are public on Hugging Face and run with vLLM on a single node of 4x NVIDIA H200 GPUs.

The Problem: Security Context Cannot Leave the Network

Closed frontier models run on someone else&#8217;s infrastructure. Using them sends source code, architecture docs, and unremediated findings outside the network. Aikido points to banks under data-residency mandates and OT operators with no internet route.

Open-weight models solve the residency problem but create a deployment gap. Mixture-of-experts (MoE) models must store every expert, even when a workload uses only a few of them. Security agents also build long-running context. That KV cache competes with model weights for the same GPU memory.

How Altar-1 Was Built

GLM-5.3 is a 753B parameter MoE model. Each token routes to 8 of 256 experts per layer, which is about 40B active parameters. Aikido applied 2 compression steps:

Step 1-Quantization: Altar-1 starts from the cyankiwi GLM-5.3-AWQ-INT4 checkpoint. AWQ stores routed expert weights in 4 bits, with 16-bit activations (W4A16). Attention, the shared expert, dense layers, and the head stay in BF16.

Step 2- Expert pruning: Aikido used Cerebras REAP (Router-weighted Expert Activation Pruning). REAP scores each expert by router weight and output magnitude, not just by how often it is selected. Altar-1 keeps 168 of 256 routed experts per layer and removes 88 (34.4%). No retraining is involved.

Calibration used traces from Aikido&#8217;s pentesting harness, plus coding, tool calling, reasoning, and multilingual Wikipedia text. Aikido states no customer data was used. Each expert is scored by its largest share of any single domain&#8217;s routed work. That protects the specialist experts for code, rare languages, and structured output.

Routing is unchanged. The router still picks 8 experts per token, now from 168, with about 40B active parameters.

CheckpointStored weightsGLM-5.3, BF161,506.7 GBGLM-5.3, AWQ INT4488.2 GBAltar-1, pruned W4A16328.0 GB

Altar-1 is 78.2% smaller than BF16 and 32.8% smaller than the AWQ parent. On fidelity, Altar-1 has a KL divergence of 0.506 nats against full BF16 on a sealed 25-prompt panel. An EXL3 build of the same cut scores 0.511. The details are in the public fidelity study.

&&

Benchmark Results

Aikido team tested Altar-1 on its internal CVE benchmark. The benchmark covers 32 known vulnerabilities across 30 repositories, with 3 runs per case.

ModelAvg recall per runFound at least onceGLM-5.3, BF1665.6%25 of 32GLM-5.3, AWQ INT461.5%23 of 32Altar-160.4%23 of 32

Compared with the AWQ checkpoint, pruning cost about 1 point of recall and no coverage. Compared with the parent, Altar-1 keeps 23 of 25 covered vulnerabilities (92%) at 5.2 points lower recall.

The benchmark&#8217;s scope is narrow. It measures targeted CVE rediscovery inside a pipeline that uses other models for the surrounding stages. It does not measure blind discovery, exploit validation, or fix proposals. Aikido also reports that Altar-1 found a valid critical-severity vulnerability during a client&#8217;s production pentest. That is a single result reported by the vendor.

Deployment and License

The model card requires Hopper GPUs (H100 or H200). Aikido says 328 GB across 4x H200 leaves room for a 128k-context KV cache at production batch sizes.

Copy CodeCopiedUse a different Browser

vllm serve AikidoSec/altar-1 --tensor-parallel-size 4 --trust-remote-code --max-model-len 131072

vLLM selects the Marlin MoE kernel automatically. A 4x H100 80 GB node has only 320 GB of memory, which is less than the 328 GB of weights.

Altar-1 inherits the GLM-5.3 License. The license permits commercial use, modification, and redistribution. Model-as-a-Service operators with more than $10B in revenue over 12 months must first pass a Z.AI security review. Altar-1 is open-weight, not OSI-approved open source.

Altar-1 also powers Aikido Attack, AI Code Analysis, and Deep Review. Next, Aikido plans to try lower-bit formats like EXL3 so it can keep more experts. It also plans to fine-tune models for security workflows.

Key Takeaways

Altar-1 compresses GLM-5.3 from 1,506.7 GB to 328 GB, a 78.2% cut.

REAP pruning keeps 168 of 256 experts per layer, with 8 active per token.

Recall drops from 65.6% to 60.4%, keeping 92% of the parent&#8217;s CVE coverage.

It runs on 1 node of 4x H200 with vLLM, including air-gapped setups.

The GLM-5.3 License allows commercial use, with a review clause above $10B revenue.

Check out the Model Weights and Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Aikido Security Releases Altar-1: An Open-Weight Security Model Pruned From GLM-5.3 to 328 GB appeared first on MarkTechPost.