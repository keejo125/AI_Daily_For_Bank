---
publish_time: 1789109842
link: https://www.marktechpost.com/2026/09/10/cohere-releases-north-small-translate-a-218b-moe-translation-model-that-scores-83-6-on-wmt26-across-50-languages/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cohere 与 Cohere Labs 发布开源权重机器翻译模型 North Small Translate：218B 总参数、25B 激活参数的稀疏 MoE 架构，覆盖阿尔巴尼亚语到越南语等50种语言，在 WMT26 评测平均得分83.6，宣称超越 DeepL、Google 翻译及 GLM 5.2、Mistral Large 3 等开源方案。可免费调用 API（限流）、非商业自托管或商业授权。Cohere 将翻译定位为「主权」问题——无法全球沟通的组织将处于劣势。
---

# Cohere 发布 218B MoE 翻译模型 North Small Translate（WMT26 跨50语言83.6分）

> 原文链接：https://www.marktechpost.com/2026/09/10/cohere-releases-north-small-translate-a-218b-moe-translation-model-that-scores-83-6-on-wmt26-across-50-languages/
> 来源：MarkTechPost

Cohere has released North Small Translate, an open-weight machine translation model from Cohere and Cohere Labs. It is a sparse Mixture-of-Experts (MoE) model with 218B total and 25B active parameters. It covers 50 languages, from Albanian to Vietnamese. On Cohere&#8217;s WMT26 evaluation, it scores 83.6 averaged across all languages. Cohere says that beats DeepL and Google Translate, plus open options like GLM 5.2 and Mistral Large 3.

Is it deployable? Yes. Call it free on Cohere&#8217;s API until rate limits, self-host it non-commercially, or license it commercially.

Back to Where the Transformer Started

Google researchers introduced the Transformer in 2017 with Attention Is All You Need. Its main results came from WMT 2014 English-to-German and English-to-French translation. 9 years later, Cohere is returning to that original problem with a dedicated model. Cohere&#8217;s launch post on X frames translation as a sovereignty issue. Organizations that cannot communicate globally cannot stay sovereign.

North Small Translate is the first translation model in Cohere&#8217;s North family. It follows Tiny Aya and Command A Translate in Cohere&#8217;s multilingual lineage. Cohere built it with RWS, whose Language Weaver scientists and language experts shaped its real-world quality.

Architecture

The model structure describes a decoder-only sparse MoE Transformer. Here are the key details:

Experts: 128 experts, 8 activated per token, plus shared experts applied to every token.

Router: A sigmoid over expert logits, normalized over the selected top-k.

Attention: Sliding-window layers (window 4096, RoPE) and global layers without positional embeddings, interleaved 3:1.

Lineage: That attention layout was first introduced in Command A.

Context: 16K input and 16K output tokens, text only.

Training: Post-trained specifically for translation quality.

About 11.5% of the weights are active per token. Per-token compute tracks the 25B active parameters. Memory still has to hold all 218B.

&&

Benchmarks

Cohere team reports these WMT26 all-languages scores in its launch blog:

ModelWMT26 scoreNorth Small Translate (Agentic)84.36North Small Translate83.60Qwen 3.5 397B A17B81.56DeepL NextGen81.37Gemma 4 31B (on)79.46GLM 5.2 FP876.50Google Translate68.20

The Agentic variant runs a multi-pass workflow that finds and fixes its own errors. Cohere&#8217;s scoring bands treat 80 to 100 as perfect or minor errors only. One caveat matters here. These are Cohere&#8217;s own runs, with GPT-5.6-Sol as the judge. Treat them as vendor-reported until independent WMT26 results appear.

Regionally, both versions beat Gemma 4 31B (on) across Europe. On EU languages, the standard model scores 82.17 against Gemma&#8217;s 72.73. South Asia is close, at 86.16 for North against 88.04 for Gemma. 

Speed, Long Documents and Cost

In Cohere&#8217;s tests, the model produced 112 output tokens per second against 81 for Gemma 4 31B. That was at low concurrency on identical hardware. At high concurrency, the figures were 39 against 30. Cohere calls this up to 1.4x higher throughput.

Long documents are a stronger point. The model scores 48.9 when translating 2 book chapters in 1 call. Google Translate scores 21.3 and Gemma 4 31B scores 19.4. Quality is measured per paragraph with xCOMET-XL.

In Cohere&#8217;s cost chart, the model scores 80.1 at $0.000676 per task, averaging 661 tokens. Gemini 3.1 Pro Preview (high) costs $0.038928 per task, about 58x more. Qwen 3.5 397B A17B costs $0.004525 and Command A+ costs $0.005158.

How to Run It

The fastest path is Cohere&#8217;s Chat V2 API. The model is free there until rate limits:

Copy CodeCopiedUse a different Browser

from cohere import ClientV2

co = ClientV2(api_key="<YOUR_API_KEY>")
response = co.chat(
    model="north-small-translate-1-0",
    messages=[{"role": "user",
               "content": "Translate everything that follows into French:\n\nEnterprises need accurate translations of business-critical documents."}],
)
print(response.message.content[0].text)

For self-hosting, Cohere publishes 3 checkpoints, the same ones it serves in production:

CheckpointBlackwellHopperBF164x B2008x H100FP82x B2004x H100NVFP4 W4A161x B2002x H100

Key Takeaways

Cohere&#8217;s North Small Translate is a 218B MoE with 25B active parameters.

It scores 83.6 on WMT26 across all languages, 84.36 in agentic mode.

All scores are vendor-reported and judged by GPT-5.6-Sol.

The 4-bit checkpoint runs on 1x B200 or 2x H100.

Check out the Model here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Cohere Releases North Small Translate: A 218B MoE Translation Model That Scores 83.6 on WMT26 Across 50 Languages appeared first on MarkTechPost.