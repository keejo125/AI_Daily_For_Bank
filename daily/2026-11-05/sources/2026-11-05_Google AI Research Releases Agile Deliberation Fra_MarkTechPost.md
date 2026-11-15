---
publish_time: 1793857338
link: https://www.marktechpost.com/2026/11/04/google-agile-deliberation-subjective-image-classifiers/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google Research 开源 Agile Deliberation 框架，面向「健康食品」「鼓舞人心的艺术」等主观概念构建图像分类器，采用人在回路（human-in-the-loop）方式处理灰色地带的标注分歧。该框架把主观判断显式建模为可协商的环节，为内容审核、质量分级等难以客观量化的场景提供了工程化参考。
---

# 谷歌开源Agile Deliberation框架：主观图像分类人机协作

> 原文链接：https://www.marktechpost.com/2026/11/04/google-agile-deliberation-subjective-image-classifiers/
> 来源：MarkTechPost

Google Research has released Agile Deliberation, a human-in-the-loop framework for building image classifiers around subjective concepts. Think &#8216;healthy food&#8217;, &#8216;inspiring artwork&#8217; or clickbait in content moderation. Most tooling assumes users already know the concept boundary. Agile Deliberation assumes they do not, and helps them find it. 

TL;DR

Framework: It prompts Gemini 2.5 Pro and Gemini 2.5 Flash through the API, without fine-tuning.

Runs on: A Jupyter or Colab notebook. Retrieval uses CLIP embeddings and a FAISS index on CPU or GPU. The demo index starts at about 260 MB.

Performance: 10.5 F1 points above zero-shot Gemini 2.5 Flash on average, across 2 concepts and 18 live sessions.

Best: Paid to play F1 of 0.59 vs 0.48 zero-shot, with precision up 22 points (0.35 to 0.57).

Worst: Recall drops 17 points on paid to play (0.80 to 0.63) and 15 points on healthy food.

What is Agile Deliberation?

Agile Deliberation is a Google Research&#8217;s framework that turns a vague concept into a structured written definition. That definition does two jobs. It is a human-readable policy, and it is the text prompt for a VLM classifier. Each round keeps the candidate definition with the best F1 on the user&#8217;s labels.

The design came from interviews with a group of content moderation experts. Experts scoped a concept first, then refined it on borderline images. Finding those images was the slow part.

How does concept scoping work?

Stage 1 breaks the concept into at most 3 unit concepts, using prompt chaining with Gemini 2.5 Pro. Each unit gets candidate positive and negative subconcepts, shown with retrieved images. For healthy food, positives might be salads or grain bowls. Negatives might be processed food or raw, unprepared ingredients. The user keeps, flips or drops each one.

How does concept iteration find borderline images?

Stage 2 skips classic uncertainty sampling. The classifier is a prompted generative VLM, so its confidence scores are often uncalibrated. Instead, the system hunts for images that are borderline in meaning. 

The pipeline runs 4 steps:

Gemini 2.5 Flash writes borderline queries, such as &#8216;salads with heavy mayo dressings&#8217;. Each query retrieves 50 to 100 images.

Images are de-duplicated, encoded, and grouped into clusters with dictionary learning.

A UCB multi-armed bandit picks the next cluster. It favors clusters where users corrected the model or left rich feedback.

A VLM summarizes each image in 1 sentence. The user sees at least 5 images that share 1 ambiguity.

Users label each image and add short notes on disagreements. An LLM turns those notes into candidate definitions. A greedy update keeps the best-scoring one.

How was it evaluated?

Subjective concepts have no fixed ground truth, so Google team skipped static benchmarks. It ran 18 live sessions of about 90 minutes each. 9 participants without professional moderation experience did 2 sessions each. One session used Agile Deliberation, the other used manual deliberation. Each participant spent about 45 minutes defining a concept, then labeled 200 held-out test images.

The two concepts were &#8216;paid to play&#8217; clickbait and &#8216;healthy food&#8217;. Retrieval ran over a proprietary 100M-image dataset and WebLI, respectively.

What do the benchmarks show?

F1 (Agile Deliberation group)Zero-shotModeling CollaboratorAgile DeliberationGain vs zero-shotPaid to play0.480.530.59+11 pointsHealthy food0.480.500.58+10 points

Source: Table 1 of the CVPR 2026 paper. F1 averaged over participants.

How does it compare with other subjective classifier methods?

FeatureAgile DeliberationModeling CollaboratorAgile ModelingZero-shot VLMVenueCVPR 2026CVPR 2024ICCV 2023Baseline in paperCore ideaDeliberation on semantic borderline images, then automatic prompt optimizationLLM agent decomposes the concept and auto-labels dataUser labels images in a real-time loopClassify from the initial descriptionHuman effortAbout 45 min of labeling and feedbackAbout 100 labels plus chat (vs about 2,000)Under 30 min in a 14-person study1 concept descriptionHandles evolving definitionsYesNo (static)No (static)NoClassifierPrompted Gemini 2.5 FlashLightweight distilled classifierNot disclosedPrompted Gemini 2.5 FlashF1, paid to play0.590.53Not tested0.48F1, healthy food0.580.50Not tested0.48CodeApache 2.0, GitHubNot disclosedNot disclosedGemini API

&&

How can developers run it?

The repo ships a Demo.ipynb that walks through the healthy food example. It needs a Gemini API key and defaults to gemini-2.5-pro and gemini-2.5-flash. A setup script builds a FAISS index over LAION-400M CLIP embeddings. The default 2 shards take about 260 MB. All 100 shards take about 13 GB.

Key Takeaways

Agile Deliberation helps users discover a subjective concept&#8217;s boundary, not just label it.

It finds borderline images by meaning, not by classifier confidence.

F1 rose 10.5 points over zero-shot Gemini 2.5 Flash on average.

Users reported significantly lower effort and stress than with manual prompt editing.

The code is open on GitHub, with a Gemini-based demo notebook.

Check out the paper, arXiv version, GitHub repo and Google Research blog. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google AI Research Releases Agile Deliberation Framework for Gray-Area Image Classifiers appeared first on MarkTechPost.