---
publish_time: 1791164848
link: https://www.marktechpost.com/2026/10/04/can-an-open-model-do-security-research-cantinas-apex-flash-1-solves-40-of-60-held-out-bug-tasks/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cantina Security联合Yeta Labs发布开源安全研究模型apex-flash-1（MIT许可），基于智谱GLM-5.3-Flash以GRPO微调，总参数321.3B、激活18B，可经vLLM等本地部署。在60道漏洞研究任务上以66.7%（40/60）通过率、约2.38美元成本解题，逼近Claude Opus 5 High的71.7%（43/60）但成本仅其1/31（每解约0.06美元对1.74美元）。Cantina将其定位为“由更大模型编排的worker”，面向防御方“可自主运行与控制”的诉求。这印证了开源模型在专业安全研究任务上已具备实用竞争力。
---

# 开源模型能否胜任安全研究？Cantina 发布 apex-flash-1

> 原文链接：https://www.marktechpost.com/2026/10/04/can-an-open-model-do-security-research-cantinas-apex-flash-1-solves-40-of-60-held-out-bug-tasks/
> 来源：MarkTechPost

Cantina Security, with Yeta Labs, has released apex-flash-1, an open-weights model trained specifically for vulnerability research. It is a reinforcement learning fine-tune of Z.ai&#8217;s GLM-5.3-Flash, released on Hugging Face under the MIT license.

Is it deployable? Yes, the MIT weights serve on vLLM, SGLang or Transformers, but BF16 needs roughly 640 GB of GPU memory.

What Cantina Built

apex-flash-1 has 321.3B total parameters, per its Hugging Face safetensors metadata. The GLM-5.3-Flash base is a Mixture-of-Experts model with 18B active parameters.

Cantina trained it with GRPO using a rank-256 LoRA plus selective full-parameter training. The data covers 150 tasks built from 50 real vulnerability cases.

Each case appears in 3 variants: guided whitebox, focused whitebox and focused blackbox.

Authorization, identity and scope flaws make up 72% of cases. Accounting and numerical precision bugs add 18%. Time validation, business rules and SSRF cover the rest.

As per the model card on HF, RL rollouts ran inside the Codex agent harness on production-like software and protocol environments.

Benchmark Results

Cantina evaluated 60 tasks from 20 held-out vulnerability cases. Each model ran the set once, with costs estimated from provider pricing.

apex-flash-1: 40/60 solved (66.7% pass@1), about $2.38

GLM-5.3-Flash (base): 36/60 solved (60.0%), about $4.56

Claude Opus 5 High: 43/60 solved (71.7%), about $74.68

Opus solved 3 more tasks but cost about 31x more per run. That is roughly $0.06 per solved task for apex-flash-1 versus $1.74 for Opus. These are company-reported numbers on an internal benchmark.

A Worker Model, Not an Orchestrator

Cantina positions apex-flash-1 as a worker orchestrated by a larger model. The card lists code reading, tool use, exploit development and verification as target skills.

An experimental apex-flash-1-abliterated variant ships with modified refusal behavior. It was not separately evaluated.

Cantina&#8217;s rationale is that defenders need capable models they can run and control locally.

Interactive Explainer

&&&

How It Compares

Featureapex-flash-1Aikido Altar-1Cisco Foundation-Sec-8B-ReasoningGLM-5.3-FlashDeveloperCantina Security + Yeta LabsAikido SecurityCisco Foundation AIZ.aiBase modelGLM-5.3-FlashGLM-5.3 (pruned)Llama 3.1 8BOwn pretrainingSize321.3B total, BF16328 GB, INT4 (W4A16)8B320B total, 18B activeLicenseMITInherits GLM-5.3 licenseCustom (see NOTICE.md)MITSecurity methodGRPO RL on 50 real vulnerability casesExpert pruning (REAP) + quantizationInstruction tuning + RLHF on security QAGeneral-purpose basePrimary useAgentic vuln research workerAir-gapped autonomous pentestingSOC triage and threat defenseGeneral coding and agentsHardwareMulti-GPU node (~642 GB BF16 weights)4x H200 with vLLMSingle GPUMulti-GPU nodePublished security result66.7% pass@1, 60 tasks60.4% recall, 32-CVE internal setCisco-reported security benchmarks60.0% on Cantina&#8217;s set

Sources: Cantina, Aikido, Cisco, Hugging Face model cards. © Marktechpost

Key Takeaways

apex-flash-1 is a 321.3B open-weights security model under MIT.

GRPO training on 50 real vulnerability cases produced 150 tasks.

It scored 66.7% pass@1 versus 71.7% for Claude Opus 5 High.

Its 60-task run cost about $2.38 versus $74.68 for Opus.

BF16 needs a multi-GPU node; community 4-bit ports exist.

Check out the Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Can an Open Model Do Security Research? Cantina&#8217;s apex-flash-1 Solves 40 of 60 Held-Out Bug Tasks appeared first on MarkTechPost.