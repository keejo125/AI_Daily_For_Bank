---
publish_time: 1787861149
link: https://www.marktechpost.com/2026/08/27/cohere-releases-parse-5-parse-v5-0-a-2-3b-vision-language-model-that-turns-enterprise-documents-into-markdown/
source: Cohere
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cohere发布文档解析模型Parse 5（parse-v5.0），采用23亿参数视觉语言模型架构，上下文窗口8192、体积约4.6GB，可直接将PDF、PPT、JPEG转为按阅读顺序排版的Markdown，并输出表格、表单键值、图像描述与边界框坐标，无需独立OCR环节。已在Cohere Parse API、Microsoft Foundry、AWS SageMaker及私有部署全面可用，定价每千页1.5美元。
---

# Cohere 发布 Parse 5：将企业文档转为 Markdown 的 23 亿参数视觉语言模型

> 原文链接：https://www.marktechpost.com/2026/08/27/cohere-releases-parse-5-parse-v5-0-a-2-3b-vision-language-model-that-turns-enterprise-documents-into-markdown/
> 来源：MarkTechPost

Cohere has released Parse (parse-v5.0), a document parsing model aimed at high-volume enterprise ingestion. It is a 2.3B-parameter vision language model with an 8,192-token context window and a ~4.6GB footprint, built on Cohere Labs&#8217; North-Micro-Vision-Instruct architecture. Parse takes a PDF, PPT or JPEG page as a base64-encoded data URI and returns Markdown containing text in reading order, tables rendered as HTML, lists, form key-value pairs, image descriptions and bounding box coordinates. There is no separate OCR stage in front of it. Cohere prices the Parse API at $1.50 per 1,000 pages and positions the model on price-performance rather than peak accuracy — a claim the company supports with a self-reported ParseBench score of 79.2 that, as we detail below, measures three of that benchmark&#8217;s five dimensions.

Is it deployable?

Yes, in production. Parse is generally available through the Cohere Parse API, Microsoft Foundry, AWS SageMaker, and single-tenant Model Vault. There is no waitlist and no research license.

Which companies: Mid-market teams that already run a RAG stack can start on metered API calls with a free trial key. Large enterprises with residency or air-gap requirements go straight to Model Vault or private deployment. Seed-stage startups can use it, but the economics only start to matter above roughly 100K pages a month.

Which industries: Cohere targets financial services, insurance, healthcare and life sciences, public sector, telecom, energy and manufacturing — the document-heavy verticals where scanned forms and dense tables are the norm.

Applications: RAG ingestion, intelligent document processing, claims and invoice pipelines, contract and filing search, and giving document context to agents.

What is Parse?

Parse is a 2.3B-parameter vision language model built on Cohere Labs&#8217; North-Micro-Vision-Instruct architecture, with an 8,192-token context window and a ~4.6GB footprint. It accepts PDF, PPT and JPEG pages as base64-encoded data URIs and returns Markdown containing document text, lists, tables rendered as HTML, bounding box coordinates and image descriptions.

There is no separate OCR stage in front of it. The model recovers text and reading order, tables, lists, forms and key-value pairs, images and captions, and the locations of page boundaries and visual elements in one pass. Nine languages are listed as stable — Arabic, English, French, German, Italian, Japanese, Korean, Portuguese and Spanish — with zero-shot support elsewhere at lower accuracy.

Two output modes matter in practice. The default returns a Markdown string per page. Setting output_format="blocks" returns typed blocks, where a table block carries its HTML, its bounding box and a description. That second mode is what makes citation-level traceability possible. 

&&

The Benchmark

Cohere reports a ParseBench score of 79.2 for Parse, averaged across tables, content faithfulness and semantic formatting, ahead of Mistral OCR 4 (74.5), Azure Document Intelligence (74.3) and Databricks AI Parse (72.4).

ParseBench is a LlamaIndex benchmark of ~2,078 human-verified enterprise pages scored on five dimensions: tables, charts, content faithfulness, semantic formatting and visual grounding. Cohere&#8217;s figure averages three of them and drops charts and visual grounding — the two dimensions where most parsers collapse.

Against the public leaderboard, the same vendors score far lower on the full five-dimension overall: Mistral OCR 4 at 60.68, Databricks AI Parse at 60.68, Azure Document Intelligence (Layout) at 59.64. Azure&#8217;s three-dimension average works out to 74.3, which matches Cohere&#8217;s figure exactly and confirms the methodology. Cohere Parse is not currently listed on that leaderboard, where LlamaParse Agentic leads at 84.88.

So 79.2 is a vendor-reported subset score, not a leaderboard position. It is a reasonable claim to test on your own documents.

What it Costs

Cohere prices the Parse API at $1.50 per 1,000 pages. On Model Vault, Parse 5 runs $4.00/hour or $2,500/month for a Medium instance, and $7.00/hour or $4,300/month for XL.

The crossover nobody publishes: at $0.0015 per page, a single Medium instance breaks even at roughly 1.67M pages per month, and XL at roughly 2.87M. Below that, metered API calls are cheaper. Above it, dedicated capacity wins on price alone — before any argument about data residency, which is usually the real reason enterprises move to Vault.

Key Takeaways

Cohere shipped parse-v5.0, a 2.3B VLM that converts PDFs, slides and images into Markdown with HTML tables and bounding boxes.

API pricing is $1.50 per 1,000 pages; Model Vault runs $2,500/month (Medium) or $4,300/month (XL).

Dedicated capacity only beats metered pricing above roughly 1.67M pages per month.

The 79.2 ParseBench figure is vendor-reported across three of five dimensions and omits charts and visual grounding.

Check out the Technical details here and Try it on HF. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Cohere Releases Parse 5 (parse-v5.0): A 2.3B Vision Language Model That Turns Enterprise Documents Into Markdown appeared first on MarkTechPost.