---
publish_time: 1794113159
link: https://www.marktechpost.com/2026/11/07/nous-research-arete-27b-qwen3-8-27b-propaganda-fine-tune/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Nous Research 发布 Arete-27B，一个对阿里 Qwen3.8-27B 的监督微调（SFT）开放权重模型，仅剥离原模型回答中的国家叙事框架。在 Nous 自建 803 题评测中，含宣传内容的回答比例从基础模型的 22% 降至 0.9%，能力在跑过的基准上基本不变。训练仅用约 5280 万 token、2 轮、1202 步，教师模型为 Thinking Machines 的开源模型 Inkling，权重、评测与训练数据全部公开，采用 Apache 2.0 许可。事实分项满分 5 分得 2.98，仍有 216/803 回答评 0 分。
---

# Nous Research 发布 Arete-27B：将 Qwen3.8-27B 的宣传倾向从 22% 压至 0.9%

> 原文链接：https://www.marktechpost.com/2026/11/07/nous-research-arete-27b-qwen3-8-27b-propaganda-fine-tune/
> 来源：MarkTechPost

Nous Research has released Arete-27B, a supervised fine-tune of Alibaba&#8217;s Qwen3.8-27B. Arete-27B is a 27B open-weight model that strips Chinese state framing from Qwen&#8217;s answers. On Nous&#8217;s own 803-prompt eval, answers containing propaganda fell from 22% to 0.9%. Developers get Qwen-class agentic skill without state-aligned answers. The weights, eval and training data are all public.

TL;DR

Size: 27B dense parameters (all active). Trained at 64k context. Base Qwen3.8-27B supports 262,144 tokens natively.

Runs on: BF16 weights are 53.81 GB. A community Q4_K_M quant is 17.20 GB, sized for 24 GB consumer GPUs.

Performance: Capability unchanged on the benchmarks Nous ran; political framing now matches Western models.

Best: Propaganda rate 0.9%, down from 22% for base Qwen3.8-27B.

Worst: Fact score 2.98 of 5; 216 of 803 answers still score 0.

What is Arete-27B?

Arete-27B is Qwen3.8-27B after supervised fine-tuning only. Nous used no RL, no preference optimization and no architecture changes. The license is Apache 2.0, matching the base model.

Nous team states that it saw refusals, deflections and CCP-framed answers on sensitive topics in the base model. It picked Qwen3.8-27B because it was the most capable local model and showed the target behavior.

How was Arete-27B trained?

The teacher was Inkling, an open model from Thinking Machines. Nous chose an open teacher to avoid terms-of-use limits on distillation. It rejected Nemotron 3 Ultra after finding a checkered record on China topics.

Training covered about 52.8 million tokens at 64k context, without sequence packing. The run took 2 epochs and 1,202 steps at batch size 48. It used AdamW, a 1e-5 peak learning rate and tensor parallel 4.

All language-model weights were trained. The vision encoder stayed frozen, since the data is text-only. The multi-token-prediction head was disabled.

The released arete-data-pairs set holds 34,878 prompts across 7 topics. Each prompt has both an Inkling answer and a Qwen answer. 29,236 accepted teacher answers form the SFT split.

How does the propaganda eval work?

The Propaganda_Eval set has 803 prompts across 7 value categories. These include freedom of expression, state ideology, data privacy and democracy. Each prompt carries 2 to 4 required facts from a cited source.

A Grok 4.7 judge grades two things separately:

Fact mean (0 to 5): how many required facts the answer states. One opposed fact scores 0.

Any propaganda: share of answers that adopt the state&#8217;s account as their own.

The judge must quote the exact phrase to flag propaganda. Nous removed every training prompt that overlapped the eval. The eval is MIT licensed and includes grading scripts.

&

What do the benchmarks show?

On the model card page, Arete-27B raised fact mean from 2.32 to 2.98. Propaganda fell from 22% to 0.9%. Answers scoring 0 dropped from 359 to 216 of 803.

The biggest change came in freedom of expression. Fact score rose from 0.89 to 2.44, and propaganda fell from 60% to 1%.

Capability held on Nous&#8217;s tests. Hermes Bench moved from 65.77% to 65.60%, which Nous calls noise. Terminal-Bench-2.1 rose from 67% to 70% in Nous&#8217;s harness. Nous does not claim credit for that gain.

How does Arete-27B compare?

MetricsArete-27BQwen3.8-27BMuse Glimmer 30BGemma 4 31BDeveloperNous ResearchAlibaba QwenMetaGoogle DeepMindParameters27B dense27B LM, dense29.6B incl. vision, dense30.7B, denseContextNot disclosed (trained at 64k)262,144 native, up to 1M131,072+256KLicenseApache 2.0Apache 2.0Apache 2.0Apache 2.0InputText, image (encoder frozen)Text, image, videoText, imageText, image4-bit footprint17.20 GB Q4_K_M (community)Not disclosedUnder 20 GB, 24 GB VRAM targetNot disclosedFact mean, Nous eval2.982.323.022.58Any propaganda, Nous eval0.9%22%0.5%0.5%Terminal-Bench 2.170% (Nous harness)67% Nous harness; 73.0 official51.7 (Meta, terminus2)Not disclosed by GoogleGPQA DiamondNot disclosed89.283.584.3

Note: Arete and Qwen ran at temperature 0 in the Nous eval. Muse Glimmer and Gemma ran at 0.6. Terminal-Bench figures come from different harnesses.

How can developers run it?

Weights ship in BF16 on Hugging Face. No hosted inference provider serves the model yet. Community GGUF quants run in llama.cpp, LM Studio and Ollama, from 8.64 GB to 53.81 GB. The GGUF build also includes the image projector.

Key Takeaways

Arete-27B cuts Qwen3.8-27B propaganda answers from 22% to 0.9%.

The fix took only 52.8M tokens of plain SFT, no RL.

Hermes Bench held at 65.60% versus 65.77% for the base.

Fact recall rose to 2.98 of 5 but still trails peers.

Weights, eval and training data are open under Apache 2.0 and MIT.

Check out the model weights, technical blog, evaluation set and training data. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Nous Research Releases Arete-27B that Cuts Qwen3.8-27B Propaganda From 22% to 0.9% appeared first on MarkTechPost.