---
publish_time: 1791307846
link: https://www.marktechpost.com/2026/10/06/mistral-ai-releases-mistral-large-4-le-chonk-a-1-05t-parameter-open-weight-multimodal-moe/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Mistral 发布旗舰模型 Mistral Large 4（Le Chonk）公开预览：细粒度 MoE，总参 1.05 万亿、每 token 激活 490 亿，原生支持图像输入，100 万 token 上下文，1.6B 视觉编码器；在 Mistral 自有欧洲数据中心以约 3800 张 Nvidia Grace Blackwell GPU 从头训练。API 现价 $1.36 / $4.18 每百万 token，权重将于 10 月底开放。亮点在网络安全：Cybench 93%、CyberGym-E2E 82%，Mistral 称若干闭源前沿模型因安全拒绝在该类任务近零分；Agent 编程 DeepSWE 61.7%、SWE-Atlas 59.4%。盲测 3.74/5，仅次于 Claude Opus 5（4.22）。
---

# Mistral 发布 Large 4（Le Chonk）：1.05 万亿参数多模态 MoE 模型

> 原文链接：https://www.marktechpost.com/2026/10/06/mistral-ai-releases-mistral-large-4-le-chonk-a-1-05t-parameter-open-weight-multimodal-moe/
> 来源：MarkTechPost

Mistral AI has just announced the release of Mistral Large 4 (ML4), internally nicknamed Le Chonk, as a public preview. ML4 is a granular Mixture of Experts model with 1.05 trillion total parameters, 49 billion active per token, a 1.6 billion parameter vision encoder, and a 1 million token context window, per the model documentation. It was trained from scratch on 3,800 NVIDIA Grace Blackwell GPUs in Mistral&#8217;s own European datacenters.

TL;DR

Mistral AI released Mistral Large 4 (&#8216;Le Chonk&#8217;) as a public preview on 6 October 2026: a 1.05T parameter granular MoE with 49B active per token, native image input, and a 1M context window, trained from scratch on 3,800 NVIDIA Grace Blackwell GPUs in Mistral&#8217;s own EU datacenters. The API is live now at $1.36 per 1M input and $4.18 per 1M output tokens, but the weights do not ship until end of October, so self hosting is not yet possible. Its standout results are in cybersecurity, where Mistral reports 93% on Cybench and 82% on CyberGym-E2E and notes that several closed frontier models score near zero because they refuse the task. 

What is the architecture?

ML4 is a hybrid instruct-and-reasoning MoE that takes image input natively. Only about 4.7% of the weights activate per token, which is how a 1 trillion class model serves at mid-tier pricing. The full 1.05T still has to sit in memory, so the activation count sets compute, not your hardware bill.

Mistral has not yet published the expert count, top-k routing, or layer layout; those arrive with the weights. Training data spanned more than 160 languages, including every official EU language.

Interactive Explainer

How does it perform?

In cybersecurity, Mistral reports 93% on Cybench and 82% on CyberGym-E2E, placing ML4 in the global top 5 on the Artificial Analysis Cyber Index. The more interesting claim is structural: Mistral states several frontier closed models score near zero on CyberGym-E2E because they refuse outright. Reproducing a vulnerability to prove it is real is standard defensive work, and provider-level refusals block it.

In agentic coding, Mistral reports 61.7% on DeepSWE v1.1, 59.4% on SWE-Atlas-QnA, and 28.3% on Terminal-Bench 4.0, for a combined Artificial Analysis Coding Agent Index of 49.8%. Mistral notes these were evaluated privately ahead of the harness going public, so they are not yet independently reproducible.

A blind human evaluation run with Surge AI is the more honest signal. Professional annotators rated ML4 Preview 3.74 out of 5, second of 5 models, ahead of GLM-5.3 (3.60) and Kimi K3 (3.59), but behind Claude Opus 5 at 4.22.

On safety, ML4 resists 93.3% of attacks on Lakera&#8217;s B3 benchmark and scores 1.691 of a maximum 2.0 on KORABench.

How does it compare to its closest open-weight rivals?

FeatureMistral Large 4DeepSeek V4 ProKimi K3GLM-5.3Total parameters1.05T1.6T2.8TNot officially publishedActive per token49B49B~104BNot officially publishedContext window1M1M1M1MNative image inputYesNoYesNoWeights availableNot yet, due end Oct 2026Yes, on Hugging FaceYes, since 27 Jul 2026Yes, per Artificial AnalysisLicenseNot yet announcedMITModified MITGLM-5.3 LicenseAPI price per 1M in/out$1.36 / $4.18Varies by provider$3.00 / $15.00$1.40 / $4.40Released6 Oct 2026Aug 2026 (0813 build)16 Jul 202614 Aug 2026

What can you build with it today?

The preview API supports function calling, structured outputs, document QnA, batching, and the Agents and Conversations endpoints. Cached input is priced at $0.14 per 1M tokens, which materially changes the economics of long-context agent loops at a 1M window.

Key Takeaways

1.05T total parameters, 49B active per token, 1M context, 1.6B vision encoder.

Trained on 3,800 Grace Blackwell GPUs in Mistral&#8217;s own EU datacenters.

API preview live now at $1.36 per 1M input and $4.18 per 1M output tokens.

Weights promised by end of October 2026, so self hosting is not yet possible.

Strongest results are in cybersecurity, where closed models often refuse the task.

Check out the Mistral Large 4 announcement, Mistral Large 4 model docs and Artificial Analysis model comparisons. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

[Sponsored] The web is the one API most agents are missing. Databases, calendars and repos have APIs. The open web mostly doesn&#8217;t. The TinyFish MCP server gives any MCP client four tools: TinySearch, TinyFetch (full pages as markdown, JavaScript included), TinyBrowser for logins and forms, and TinyAgent for multi-step jobs. Search and Fetch are free.

The post Mistral AI Releases Mistral Large 4 (Le Chonk): A 1.05T Parameter Multimodal MoE Model appeared first on MarkTechPost.