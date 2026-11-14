---
publish_time: 1794586202
link: https://www.marktechpost.com/2026/11/13/perplexity-decider-v1-3-open-weight-decision-models-locate/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Perplexity发布开源决策模型Decider v1.3与Flash v1.3（受TypeSafe Jev启发），返回概率而非生成文本，用于文本/图像的yes/no、多选与打分判断，并新增Locate功能——按类型或指令抽取精确文本跨度（NER、PII、抽取式QA）。模型基于Qwen3.8-27B改造：全注意力层改为双向，输出层接决策头；权重以Apache 2.0发布（27B约49GiB、Flash 4B约8.5GiB）。官方自报：63项查询分类均准91.6%、检索重排nDCG@10达83.99、百万请求与前沿LLM评委一致率93.98%，鲁棒性上答案翻转率仅0.27%（Jev 1.14为2.69–4.84%）；API定价0.02/0.01美元每百万输入token。
---

# Perplexity 发布 Decider v1.3：开放权重决策模型新增 Locate 能力

> 原文链接：https://www.marktechpost.com/2026/11/13/perplexity-decider-v1-3-open-weight-decision-models-locate/
> 来源：MarkTechPost

Perplexity has released pplx-decider-v1.3 and pplx-decider-flash-v1.3, the latest versions of its open-weight decision models. Perplexity Decider v1.3 is a decision model that returns probabilities, not generated text. It answers yes/no, multiple-choice and score questions about a text or image input. The main addition is Locate, which extracts exact text spans by type or instruction. Weights ship under Apache 2.0 on Hugging Face. Both models also run in the Perplexity Decisions API and on OpenRouter. You can check the deployment options and specs here through our GPULeaderboard.com chrome extension.

TL;DR

Size: 27B on Qwen3.8-27B; Flash is 4B on Qwen3.5-4B. Hugging Face lists 26B and 5B params. API input: under 256K tokens. Local default: 32,768.

Runs on: a CUDA GPU fitting ~49 GiB of BF16 weights (v1.3) or ~8.5 GiB (Flash). No quantized variants.

Performance: leads TypeSafe&#8217;s Jev 1.14 on most of Perplexity&#8217;s self-reported evaluations.

Best: 91.6% mean accuracy on 63 query-classification tasks.

Worst: Locate averages 69.0, its lowest absolute score. Flash trails Jev 1.14 in finance, programming and law.

Bottom line: Best: a 0.27% answer-flip rate and $26.47 per 1M production requests. Worst: every figure is self-reported.

What is Perplexity Decider v1.3?

Decider is Perplexity&#8217;s family of decision models, inspired by TypeSafe&#8217;s Jev. Each request has a shared &#8216;state&#8217; plus one or more questions with labeled options. The model returns a probability per option instead of writing an answer. v1.3 succeeds v1.2 and Flash v1.2. Flash v1.3 is distilled from the large model.

How does Decider v1.3 work?

Perplexity adapts a generative LLM backbone into a classifier. The output layer starts from the base model&#8217;s LM head, pruned to option tokens (A, B, C). A linear decision head reads the hidden state at a <|marker|> token and outputs option probabilities.

Full-attention layers are made bidirectional, which Perplexity&#8217;s ablations showed helps.

v1.3 also changes attention between questions. In v1.2, every question saw every other question, so answers could shift. In v1.3, the state sees all questions, but each question sees only the state and itself. All questions about one input still run in a single forward pass.

Training runs in 3 stages:

a full fine-tune on hundreds of public datasets

a LoRA specialization adapter

a LoRA vision adapter

Weights are averaged across 3 seeds. Flash is trained by minimizing KL divergence to the large model&#8217;s outputs.

What does the new Locate feature do?

Locate returns exact text spans with start and end character offsets. Fields can be short labels (&#8216;location&#8217;) or instructions (&#8216;Extract the city name where the job is located.&#8217;). It targets NER, PII detection and extractive QA.

A new <|locate|> token is added per requested field. A span head plus a LoRA adapter is trained, while the backbone and decision head stay frozen. The adapter stays unmerged because merging hurt decision accuracy.

How does Decider v1.3 perform on benchmarks?

All results below are self-reported by Perplexity:

Query classification (63 tasks): 91.6% mean accuracy, 6.54 points above production classifiers.

Domain classification: leads Jev 1.14 in all 7 domains, by up to 12.9 points in finance.

Retrieval and reranking (72 tasks): 83.99 mean nDCG@10. That is 1.81 above Qwen3-Reranker-8B and 2.24 above Jev 1.14.

Multilingual (19 tasks, 8 languages): 88.16% for v1.3, 86.50% for Flash, 85.41% for Jev 1.14.

Locate (17 out-of-domain tasks): 69.0 average for v1.3 and 63.6 for Flash. Liquid d1 scores 43.3 and GLiNER large v2.5 scores 33.6.

Image classification (5 tasks): 76.99% for v1.3, 1.47 points above Jev 1.14. Flash scores 72.77%.

Real-world requests (1M requests, 2,318,887 questions): 93.98% agreement with frontier LLM judges. Jev 1.14 scores 93.35%.

Robustness: answer flips on 0.27% of reorder or relabel transformations. Jev 1.14 flips on 2.69% to 4.84%.

&&

How does Decider v1.3 compare with Jev 1.14 and Qwen3-Reranker-8B?

FeatureDecider v1.3Decider Flash v1.3Jev 1.14Qwen3-Reranker-8BSize27B per docs (HF lists 26B)4B per docs (HF lists 5B)Not disclosed8BContextAPI under 256K; local default 32,768API under 256K; local default 32,768262,14432KLicenseApache 2.0Apache 2.0Not disclosed (hosted API)Apache 2.0ModalityText, images, Locate (text only)Text, images, Locate (text only)Text, imagesTextHardware~49 GiB BF16 weights + working memory~8.5 GiB BF16 weights + working memoryHosted onlyNot disclosedPrice$0.02 / 1M input, output free$0.01 / 1M input, output free$0.042 / 1M input, output freeOpen weights, self-hostRetrieval nDCG@10 (72 tasks)83.99Not disclosed81.75 (derived from reported 2.24 gap)82.18 (derived from reported 1.81 gap)Multilingual accuracy (19 tasks)88.16%86.50%85.41%Not reportedJudge agreement (1M requests)93.98%Not disclosed93.35%Not reportedCost for 1M requests$26.47$13.24$68.10Not reported

Benchmark rows are Perplexity&#8217;s self-reported numbers from its launch post.

How can developers deploy Decider v1.3?

The API endpoint is POST https://api.perplexity.ai/v1/decisions. Model IDs are pplx-decider-v1.3 and pplx-decider-flash-v1.3, with -latest aliases. Pricing is $0.02 and $0.01 per 1M input tokens. Output is free.

Perplexity&#8217;s latency test put an ~243K-token request at 16s on v1.3 and 5s on Flash. Locate requests allow up to 128 questions.

Locally, load the model with Decider.from_pretrained() from the pplx_decider package. Full-attention layers must run noncausally. Perplexity recommends v1.3 for nuanced rubrics and Flash for high-volume routing.

Key Takeaways

Decider v1.3 returns probabilities, not text, for classification and scoring.

New Locate extracts exact spans for NER, PII and extractive QA.

v1.3 scores 91.6% on 63 query-classification tasks (self-reported).

API pricing is $0.02 (v1.3) and $0.01 (Flash) per 1M input tokens.

Weights are Apache 2.0; v1.3 needs ~49 GiB, Flash ~8.5 GiB.

Check out the technical details, Decider v1.3 model card, Flash v1.3 model card and API docs. You can check the deployment options and specs here through our GPULeaderboard.com chrome extension.

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Perplexity Releases Decider v1.3: Open-Weight Decision Models Add Locate appeared first on MarkTechPost.