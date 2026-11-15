---
publish_time: 1791097264
link: https://www.marktechpost.com/2026/10/04/aleph-alpha-releases-kolibri-a-78-1b-open-weight-english-german-moe-model-with-only-3-46b-active-parameters/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Aleph Alpha 发布开放权重 MoE 语言模型 Kolibri（Kolibri-1），专攻英德双语，总参数 780.1 亿、每 token 仅激活 34.6 亿（约 4.4%），上下文长达 104 万 token，支持按请求设定推理强度，以 Apache 2.0 许可在 Hugging Face 发布。模型由德国团队端到端研发，训练基础设施位于德国与芬兰，面向欧盟《通用人工智能行为准则》《AI 法案》与 GDPR，数据管线在训练前即对个人数据脱敏。
  
  架构上堆叠 50 个 transformer block，每个 MoE 层用 sigmoid 路由器为全部 384 个路由专家打分，每 token 取 top-6 并常驻 1 个共享专家，辅以精确分位数均衡。FP8 检查点约 78GB，可在单张 B200/B300/H200 或 2 张 H100 上经 vLLM 部署，面向政务、工业、航天等受监管行业的自主可控部署。
---

# Aleph Alpha 发布 Kolibri：780亿参数开放权重英德双语 MoE 模型，仅激活 34.6 亿参数

> 原文链接：https://www.marktechpost.com/2026/10/04/aleph-alpha-releases-kolibri-a-78-1b-open-weight-english-german-moe-model-with-only-3-46b-active-parameters/
> 来源：MarkTechPost

Aleph Alpha has released Kolibri, an open-weight Mixture-of-Experts (MoE) language model built for German and English. Kolibri has 78.1B total parameters but activates only 3.46B, or 4.4%, per token. It accepts up to 1,048,576 tokens of context, lets users set reasoning effort per request, and ships under the Apache 2.0 license on Hugging Face. The target is sovereign deployment in regulated sectors such as public administration, industry and aerospace.

Is it deployable? Yes. The FP8 checkpoint is about 78GB and runs on a single B200, B300 or H200, or on 2 H100 SXM5 GPUs, served through vLLM with dedicated Kolibri reasoning and tool-call parsers.

What is Kolibri?

Kolibri (Kolibri-1) is a bilingual English-German MoE transformer developed end to end by teams in Germany. According to the technical research report, Aleph Alpha team controlled the full pipeline: data, architecture, training infrastructure, post-training and evaluation. Training ran on infrastructure in Germany and Finland. The design targets the EU General-Purpose AI Code of Practice, the EU AI Act and GDPR. Aleph Alpha is a signatory of that Code, and its data pipeline redacts personal data before training.

Architecture: Sparse Experts and Hybrid Attention

Kolibri stacks 50 transformer blocks with a model width of 2,560. Every MoE layer scores all 384 routed experts with a sigmoid router, sends each token to the top 6, and always runs 1 shared expert. Expert load is balanced with Exact Quantile Balancing and Load-Error Injection.

Attention uses grouped-query attention with 48 query heads and 4 KV heads. Every fifth block uses full attention without positional encoding. The other 40 blocks use sliding-window attention over the 512 preceding tokens, with RoPE. Sliding-window layers hold a fixed-size KV cache, so only 10 layers grow with context length. At matched compute, Aleph Alpha team reports the hybrid supports sequences 4 times longer than a full-attention model.

A Tokenizer Built for German

The 128,000-token vocabulary is trained with UniBPE, which builds merges like BPE but scores each merge by Unigram loss. On German text it reaches 4.90 bytes per token, versus 4.35 for the GPT-5 tokenizer. That means 11.2% fewer tokens on German web text. In English, Kolibri reaches 4.58 bytes per token against 4.67 for GPT-5.

Training: 24T Tokens, Then SFT and RL

Pre-training covered 20T tokens on 768 NVIDIA B200 GPUs, followed by 3.44T mid-training tokens at 65,536 sequence length. A 201B-token long-context stage then trained on 262,144-token sequences. Aleph Alpha added more than 2T German tokens it curated from the web or generated synthetically. Post-training combined supervised fine-tuning, mixed with MergeMix, with reinforcement learning on more than 1.2M internal tasks. The Merlin-Arthur protocol trains the model to abstain when retrieved context does not support an answer.

Interactive Explainer: How Kolibri Works

&

Benchmarks

Aleph Alpha team evaluated every model with the same eval-framework setup. In English, Kolibri leads GPQA Diamond (84.3), AIME 2025 (96.9) and AIME 2026 (96.0). It ties Qwen3.5 35B-A3B on the English agentic average at 63.4. It trails on BFCL v4, scoring 61.4 against 70.5 for Qwen3.5. The dense Qwen3.8 27B scores higher overall (80.2 EN, 79.9 DE), but activates about 8 times more parameters per token. Against its internal predecessor Kolibri Origin, Kolibri decodes about 2.7 times more text per GPU while scoring 21.4 points higher in English.

Kolibri vs Closest Competitors

FeatureKolibri-1Qwen3.6 35B-A3BNemotron 3 SuperMistral Small 4DeveloperAleph Alpha (Germany)Alibaba QwenNVIDIAMistral AI (France)Total / active params78.1B / 3.46B~35B / 3B120B / 12B119B / 6.5BArchitectureMoE, sliding-window + full attentionMoE, Gated DeltaNet hybridMamba-2 + MoE + attentionMoEMax context1,048,576 tokens262,144 native, ~1M with YaRN1M tokens256k tokensReasoning controlnone / low / medium / highThinking on / offOn / off, low-effort modenone / highLicenseApache 2.0Apache 2.0NVIDIA Nemotron Open Model LicenseApache 2.0Overall score (EN / DE)75.5 / 70.871.4 / 67.373.0 / 67.963.1 / 61.4Agentic avg (EN)63.462.154.940.7Industry RAG avg (DE)67.565.857.653.4Code avg (EN)89.387.788.382.0

Specs: model cards for Kolibri-1, Qwen3.6-35B-A3B, Nemotron 3 Super and Mistral Small 4.

How to Deploy Kolibri

Install the aleph-alpha-inference package, then serve with vLLM:

Copy CodeCopiedUse a different Browser

pip install 'aleph-alpha-inference>=1'
vllm serve Aleph-Alpha/Kolibri-1 --kv-cache-dtype fp8 \
  --reasoning-parser kolibri1 --tool-call-parser kolibri1 \
  --enable-auto-tool-choice

The default context is 262,144 tokens. Pass --max-model-len 1048576 with a max_position_embeddings override for the full 1M window. Set reasoning_effort through chat_template_kwargs. Aleph Alpha recommends temperature 1.0, top-p 0.97 and top-k 128.

Key Takeaways

78.1B total, 3.46B active: each token uses 6 of 384 routed experts plus 1 shared expert.

40 sliding-window and 10 full-attention layers keep a 1M-token context affordable.

Trained on 24T tokens, with German above 20% of the mix.

Top Overall score in English (75.5) and German (70.8) among the 12 MoE models Aleph Alpha compared.

Apache 2.0 FP8 weights, serveable on a single B200 or H200 via vLLM.

Check out the Model Weights and Technical Report. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Aleph Alpha Releases Kolibri: A 78.1B Open-Weight English-German MoE Model With Only 3.46B Active Parameters appeared first on MarkTechPost.