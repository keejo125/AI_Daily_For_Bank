---
publish_time: 1788590909
link: https://www.marktechpost.com/2026/09/04/datasets-invent-api-training-data-without-labeling-adaptive-data-autoscientist/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Adaption Labs本周发布Invent a Dataset功能：用户无需准备种子语料、预定义schema或标注指南，只需描述“希望模型学会的行为”，即可生成结构化、可直接训练的数据集，支持以JSONL/JSON/CSV/Parquet下载。该功能已在Adaption应用、Python SDK与REST API上线，生成过程运行于托管平台并消耗额度。官方称其区别于此前的合成数据工具——后者仍需人工先定义schema与任务，而本工具从任务描述直接生成训练数据，瞄准专有、 specialised任务中“现有数据难以转化为聚焦训练集”的痛点。
---

# Adaption Labs 推出 Invent a Dataset：按任务描述生成训练数据

> 原文链接：https://www.marktechpost.com/2026/09/04/datasets-invent-api-training-data-without-labeling-adaptive-data-autoscientist/
> 来源：MarkTechPost

This week, Adaption Labs released Invent a Dataset. The feature generates a structured, training-ready dataset from a description of the behavior you want a model to learn. You do not arrive with a seed corpus, a predefined schema, or a labeling guide. 

Is it deployable? Yes, with one caveat. Invent a Dataset is live now in the Adaption app and through the Python SDK and REST API. Generated rows download as JSONL, JSON, CSV, or Parquet, so the artifact is a portable file you own and can train on anywhere. Generation itself runs on Adaption&#8217;s hosted platform and consumes credits. No self-hosted generation path is documented.

The problem being targeted

Most dataset workflows begin with data that already exists. Teams then spend weeks labeling, filtering, and reshaping it to approximate the target task. Adaption&#8217;s argument is that this caps model quality at how closely the available data matches the intended behavior. For proprietary and specialized tasks, the relevant signal usually sits in internal systems, unstructured text, or workflow logs. It rarely converts cleanly into a focused training set.

The research team also draws a line against existing synthetic-data tooling. Those tools automate generation after a human has already defined the schema, task distribution, and generation strategy. Invent a Dataset starts one level earlier, at the behavior itself.

How the API works

The mechanics are documented and concrete. A single call to datasets.invent creates the dataset and starts generation, returning immediately with status running. You then poll datasets.get until the status reads succeeded or failed, and download the rows.

Domain codes are the primary control. You fetch current codes with datasets.invent_domains rather than hardcoding them. You then pass values such as medical, optionally narrowed by qualified subdomain codes such as medical.symptoms_diagnosis. At least one domain or subdomain is required. Multiple domains contribute to the same run. A domain passed without subdomains draws from its full scope.

Two output formats are supported. instruction_dataset is the default and produces prompt-completion pairs for supervised fine-tuning. preference_pairs produces chosen and rejected completions for preference-based training such as DPO.

Three parameters matter for production use. estimate=True prices the exact request and returns estimated versus available credits without creating or charging anything. prompt accepts up to 10,000 characters to steer what the rows are actually about. idempotency_key accepts up to 255 characters and makes network retries safe by returning the original dataset instead of launching a second run. Row counts are subject to a per-launch limit set by your plan.

Language and locale expansion

language_expansion runs in two modes. translate produces a new row variant for each target language. localize produces a variant for each country and language pair, using locale-specific wording rather than direct translation. A sample_rate between 0.01 and 1 controls what fraction of invented rows gets expanded, and credits are billed on the expanded output row count, not the original. Unsupported codes return a 400 with a sample of valid values.

The zero-data loop

Invent a Dataset is the first half of a loop. The dataset ID passes directly to autoscientist.create, which co-optimizes the data and the training recipe against your objective. AutoScientist launched in May 2026 and is the training-side counterpart to the Adaptive Data pillar.

Adaption reports that AutoScientist beats training configured by its own research staff, by an average of 35%. Win rates moved from 48% to 64%. Those figures come from in-house domain-specialized evaluations across eight verticals. Dataset sizes ranged from 5,000 to 100,000 rows, on architectures offered for fine-tuning by Together AI. 

Key Takeaways

Invent a Dataset generates training rows from a task description, with no seed corpus, schema, or labels.

One datasets.invent call sets domains, row count, format, and language expansion; generation is async.

Output is instruction pairs or preference pairs, downloadable as JSONL, JSON, CSV, or Parquet.

Dataset IDs feed straight into AutoScientist, closing an intent-to-trained-model loop.

Check out the Technical details here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Adaption Labs Introduces &#8216;Invent a Dataset&#8217;: Training Data Generated From a Task Description, Not a Seed Corpus appeared first on MarkTechPost.