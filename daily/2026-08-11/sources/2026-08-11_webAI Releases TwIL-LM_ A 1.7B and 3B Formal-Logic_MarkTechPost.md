---
publish_time: 1786429209
link: https://www.marktechpost.com/2026/08/10/webai-releases-twil-lm-a-1-7b-and-3b-formal-logic-model-family-for-autoformalization-on-local-hardware/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  webAI发布TwIL-LM，一个包含1.7B和3B参数的双模型形式逻辑推理家族。3B版本TwIL-LM3基于SmolLM3-3B微调合并，1.7B版本为SmolLM2-1.7B-Instruct的LoRA适配器。二者均面向自动形式化：将英语翻译为一阶逻辑并判断结论是否从前提中得出。

  模型可在本地运行，提供1.06GB（1.7B）和1.78GB（3B）的量化版本。webAI宣称在五项形式推理基准中的四项上超越了gpt-oss-120b。训练采用四阶段流程：LoRA监督微调到检查点融合到WiSE-FT插值回预训练基座到熵加权GRPO对抗程序化验证器。适用场景包括合规审查、金融服务、医疗、法律合同和形式化方法研究，但当前仅限非商业使用。
---

# webAI发布TwIL-LM：面向本地硬件的1.7B与3B形式逻辑模型家族

> 原文链接：https://www.marktechpost.com/2026/08/10/webai-releases-twil-lm-a-1-7b-and-3b-formal-logic-model-family-for-autoformalization-on-local-hardware/
> 来源：MarkTechPost

webAI has released TwIL-LM, a two-model family of formal-logic reasoners at 1.7B and 3B parameters. The 3B member, TwIL-LM3, is a merged fine-tune of SmolLM3-3B; the 1.7B member is a PEFT LoRA adapter for SmolLM2-1.7B-Instruct. Both target autoformalization: translating English into first-order logic and checking whether a conclusion follows from its premises. Both run locally, with a 1.06 GB quantized build for the 1.7B and a 1.78 GiB Q4_K_M GGUF for the 3B. webAI&#8217;s announcement frames the release around beating gpt-oss-120b on four of five formal-reasoning lanes. 

Is it deployable?

Partially. Non-commercial use only, as of now.

Both checkpoints ship under the webAI Non-Commercial License ver. 1.0. Revenue-generating deployment requires a separate agreement with webAI.

Company level: any size. The 3B Q4_K_M GGUF is 1.78 GiB and runs on CPU or 4 GB of VRAM. The 1.7B Q4_K_M is 1.06 GB.

Industries: compliance and RegTech, financial services, healthcare and pharma, legal and contract operations, formal-methods research. webAI positions local execution for environments where data cannot leave the device.

Applications: first-order logic (FOL) translation, entailment classification over premise sets, natural language to structured query, Lean formalization drafting and critique, and a verifier layer that checks a larger model&#8217;s output.

How TwIL-LM3 was built?

Four stages sit on top of the base model. LoRA supervised fine-tuning on a synthetic formal-logic corpus. Checkpoint fusion, averaging intermediate SFT checkpoints in parameter space. WiSE-FT interpolation back toward the pretrained base at λ = 0.25. Then MGPO, an entropy-weighted GRPO stage run against a programmatic verifier. The published checkpoint is step 2071.

That λ is load-bearing: only a quarter of the fine-tuned delta is retained. A sibling arm that skipped the interpolation scored higher in-domain, at macro gate 0.515, but gave back roughly twelve points of held-out capability. webAI did not publish that arm.

Performance

webAI's announcement lists 96.4 on rule induction, 87.6 on semantic parsing, 64.6 on Lean formalization, 52.0 on exact-format answering, and 68.7 on entailment labeling. 

It reports two tracks. On Track A, in-domain formal logic, TwIL-LM3 scores 0.4488 on the six-lane average and 0.4218 on the macro gate, the metric the training pipeline gates on. It leads every arm up to and including LFM2.5-8B-A1B on all six objective lanes, at 0.4218 against 0.3757 with a third of the parameters. It does not lead the two largest arms. Qwen3-8B takes the gate 0.5336 to 0.4218, but most of that is loose-match credit; under strict-7 the two sit at 0.2093 and 0.1971. gpt-oss-120b takes the six-lane average 0.5192 to 0.4488.

Efficiency is where the model card is unambiguous. TwIL-LM3 produces the shortest generations of any arm, 482 tokens on Track B, and consequently the most answers per second at 32.9 against the 120B's 4.2.

https://www.webai.com/blog/webai-releases-twil-lm-a-family-of-formal-logic-models-that-outreason-a-120b-model-and-run-on-an-iphone

Held-out transfer

TwIL-LM3 improves in-domain by +26% relative, macro gate 0.336 to 0.422, while also gaining +0.022 on the held-out core average. The model card calls it the only arm in the project that gains on both tracks. LogicBench moves to 0.7167 from 0.6467. GSM8K slips slightly to 0.8733 from 0.8833, and IFEval regresses to 0.6433 from 0.6767.

The 1.7B is a different trade. Its macro-primary score is 0.361 against 0.185 for the unadapted base. Out-of-distribution results are mixed: LogicBench BQA improves to 0.590 from 0.563, while GSM8K falls to 0.380 from 0.413 and ARC-C chain-of-thought falls to 0.463 from 0.587.

Key Takeaways

TwIL-LM3 (3B) and TwIL-LM (1.7B) target formal logic, both under a non-commercial license.

Shipping TwIL-LM3 trails gpt-oss-120b on the six-lane average, 0.4488 to 0.5192.

Its real edge is efficiency: 32.9 answers/sec from 482-token generations.

WiSE-FT at λ = 0.25 is why in-domain gains do not collapse held-out performance.

Check out the Model weights and Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post webAI Releases TwIL-LM: A 1.7B and 3B Formal-Logic Model Family for Autoformalization on Local Hardware appeared first on MarkTechPost.