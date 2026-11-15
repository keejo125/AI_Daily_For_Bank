---
publish_time: 1791607894
link: https://www.marktechpost.com/2026/10/09/nace-ai-open-sources-drex-1-5-a-9b-decision-model-that-scores-options-not-text/
source: Nace AI
status: confirmed
category: 国际
is_model_related: true
digest: |
  Nace.AI开源Drex 1.5，一款面向智能体与后端工作流的9B决策模型。它不写文本，而是读取状态与带类型的提问、为每个选项返回概率，单次前向即可完成。模型稠密8.95B参数、bf16权重约18GB，上下文默认16,384 token（可扩至131,072），单张24GB A10G即可运行，并提供Q8_0 GGUF版本。在公开Decision Index 0.3.1上取得58.08分（10B以下最高），与Jev 1.13.0处于同一区间；长文档（32K–128K token）准确率达93.4%，但细粒度情感较弱。
---

# Nace AI 开源 Drex 1.5：9B 决策模型（为智能体评分而非生成文本）

> 原文链接：https://www.marktechpost.com/2026/10/09/nace-ai-open-sources-drex-1-5-a-9b-decision-model-that-scores-options-not-text/
> 来源：MarkTechPost

Nace.AI has open-sourced Drex 1.5, a 9B decision model for agents and backend workflows. The Drex 1.5 decision model does not write text. It reads a state and typed questions, then returns a probability for every option. Nace reports 58.08 on the public Decision Index 0.3.1, the top score under 10B parameters. Weights are on Hugging Face, and a hosted version is live on OpenRouter.

TL;DR

Size: 8.95B parameters (dense), bf16 weights about 18 GB. Context is 16,384 tokens by default, up to 131,072.

Runs on: 1 CUDA GPU in bf16 (tested on a 24 GB A10G). A Q8_0 GGUF (about 9.5 GB) runs on Apple silicon and CPU.

Performance: 58.08 on Decision Index 0.3.1 (public), within the board&#8217;s tie band of Jev 1.13.0 (57.96).

Best: 93.4% accuracy on 32K to 128K token documents.

Worst: 7.4% per-review F1 on ACOS aspect sentiment, versus 29.5% for Jev.

Bottom line: 

Best: open weights that match a closed model on 1 GPU. 

Worst: weak on broad knowledge and fine-grained sentiment.

What is Drex 1.5?

Drex 1.5 is a decision model from Nace.AI that scores a fixed set of options in 1 forward pass. You send a state (text or JSON) and named questions. It supports 3 question types: choice, noul (yes/no) and ordinal score. No tokens are sampled, so temperature and top_p do not apply. The model can only answer with options you supplied.

It serves the POST /v1/systemone API. That is the same request format used by TypeSafe&#8217;s Jev, the closed model that started this category. Nace says existing Jev clients work after changing a few environment variables.

How does Drex 1.5 work?

The backbone is MiMo-V2.6-Distill-Qwen-9B, a distilled Qwen 3.5 9B model. It has 32 layers with hybrid attention: 3 linear-attention layers per full-attention layer. A separate pointer head (head.pt) scores each option from the backbone&#8217;s hidden states.

Each question runs 1 pass over the state plus that question. In llama.cpp, the state is encoded once and shared across questions. Nace&#8217;s Drex page says the model was trained on the official training splits of the index benchmarks. It was evaluated only on held-out splits.

How does Drex 1.5 perform on benchmarks?

On the public Decision Index 0.3.1 (37 benchmarks, chance-corrected), the model card reports:

Drex 1.5: 58.08

Jev 1.13.0: 57.96

Bespoke Nimble 9B v3: 57.19

Cloudflare clef-flash: 56.15

Drex 1.5, Jev and Nimble sit within the board&#8217;s 0.9-point tie band. Drex leads Jev on 20 of 37 benchmarks. The Drex score comes from Nace&#8217;s own run of the official kit. Its area scores are strongest in Tools (75.0) and weakest in Knowledge and Reasoning (44.6). Nace&#8217;s launch chart uses the older Decision Index 0.2.1, where Drex scored 58.28 against Jev&#8217;s 57.91.

On JevBench (231 public items), Drex scores 86.2% against Jev&#8217;s 87.0%. Both reach 73.9% on hard items. In a head-to-head across 8 OpenSpiel games, Drex recorded 122 wins, 47 draws and 87 losses against Jev (56.8%).

Long documents are a clear strength:

8K to 32K tokens: 89.5% accuracy, median 0.65 s

32K to 128K tokens: 93.4% accuracy, median 2.0 s

Truncating the same requests to 8K tokens drops accuracy to 76.5% and 78%.

&

How can developers run Drex 1.5?

There are 4 deployment paths, all serving the same API:

Python (Kev runtime): inference.py and serve.py on a CUDA GPU.

llama.cpp: a Nace fork with GGUF in bf16 or Q8_0, on CUDA, Metal or CPU.

Ollama: a Nace fork that adds a decision capability.

Hosted: OpenRouter lists $0.04 per 1M input tokens and $0 output, served by DeepInfra. Nace also runs its own Console API.

Nace tested bf16 and Q8_0 on an AWS g5.2xlarge (A10G 24 GB) and got identical answers. The Q8_0 GGUF also matched on an Apple M5 Pro on both Metal and CPU.

A Drex agent skill plugs the model into Claude Code, Codex, Cursor, OpenCode, Hermes Agent, Gemini CLI and GitHub Copilot. Nace&#8217;s launch post also offers a $25 sign-up bonus for cloud users.

How does Drex 1.5 compare with other decision models?

FeatureDrex 1.5Jev 1.13.0Bespoke Nimble 9B v3DeveloperNace.AITypeSafe AIBespoke LabsParameters8.95BNot disclosedLoRA on Qwen3.5-9BWeightsOpenClosed (API only)Open (adapter)LicenseNace.AI Open RAIL-MProprietaryCC BY-NC 4.0Context16,384 default, up to 131,07264K per request, 32K state plus longest questionNot disclosedDecision Index 0.3.1 (public)58.0857.9657.19Decision Index 0.2.158.2857.9156.88JevBench (231 items)86.2%87.0%Not disclosedLocal hardware1 CUDA GPU (bf16), Apple silicon or CPU (Q8_0)Not applicableQwen3.5-9B base plus adapterAPI price (input / output per 1M)$0.04 / $0 (OpenRouter)$0.042 / $0Not disclosed

Decision Index 0.3.1 rows are from the Drex 1.5 model card, which cites the public leaderboard for Jev and Nimble. Nimble&#8217;s 0.2.1 score is from its own model card.

What are the limitations?

Drex 1.5 is a decision layer, not a general model. It cannot generate text, code or explanations. Knowledge-heavy tests are its weak spot: 45.4% on GPQA Diamond versus Jev&#8217;s 78.6%, and 58.7% on MMLU-Pro versus 82.7%.

Training on the index benchmarks&#8217; training splits helps it on familiar decision types. Results on new domains may differ. Local deployment through Ollama and llama.cpp needs Nace&#8217;s forks, not mainline builds. The weights use a RAIL-M license with use restrictions, so check the terms before commercial use.

Key Takeaways

Drex 1.5 is a 9B open decision model that scores options in 1 pass.

It scores 58.08 on Decision Index 0.3.1, tied with closed Jev 1.13.0.

Long-document accuracy reaches 93.4% at 32K to 128K tokens.

It runs on 1 GPU or as a 9.5 GB Q8_0 GGUF on a Mac.

Weak spots: GPQA Diamond (45.4%) and ACOS sentiment (7.4%).

Check out the model weights on Hugging Face, the GitHub repo and the Drex product page. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Nace AI Open-Sources Drex 1.5: A 9B Decision Model That Scores Options, Not Text appeared first on MarkTechPost.