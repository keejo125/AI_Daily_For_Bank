---
publish_time: 1789106485
link: https://www.marktechpost.com/2026/09/10/google-research-releases-toolgrad-answer-first-framework-hits-99-8-pass-rate-for-tool-use-data-generation/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google 联合东京大学、RIKEN AIP、东北大学提出 ToolGrad：一种「答案优先」的工具调用数据生成框架，先构建经过验证的工具调用链，再反写用户查询，突破了 ToolBench/ToolACE 等「查询优先」管线数据稀缺、昂贵的瓶颈，工具调用数据生成通过率从 63.8% 提升至 99.8%。用其 500 条样本微调的 Gemma-3 系列（1B/4B/12B）在 Berkeley Function Calling Leaderboard 上取得 83.1 分，比肩 Gemini 2.5 Pro（83.2）等前沿闭源模型。代码 Apache-2.0，数据集与模型已开源。
---

# Google 发布 ToolGrad：答案优先框架，工具调用数据生成通过率99.8%

> 原文链接：https://www.marktechpost.com/2026/09/10/google-research-releases-toolgrad-answer-first-framework-hits-99-8-pass-rate-for-tool-use-data-generation/
> 来源：MarkTechPost

Training an LLM to call tools reliably requires datasets that pair user queries with correct tool-use chains. Producing that data at scale has been slow and expensive. A team of researchers from Google, the University of Tokyo, RIKEN AIP, and Tohoku University introduce ToolGrad.  The research work inverts the usual pipeline: build a verified tool chain first, then write the query. Gemma-3 models fine-tuned on 500 samples of the resulting data reach scores that sit alongside frontier proprietary models on the Berkeley Function Calling Leaderboard.

Is it deployable? Yes. The code is Apache-2.0, the ToolGrad-500 dataset and the 1B, 4B, and 12B models are on Hugging Face, and there is a PyPI package. 

The problem with query-first generation

Prior pipelines such as ToolBench and ToolACE follow a query-first recipe. The system samples a pool of APIs, asks an LLM to invent a plausible user instruction, and then dispatches a depth-first search (DFS) agent to find a tool-use path that satisfies it. The search has no guarantee of success. When it dead-ends, the compute spent on exploration is wasted, and the sample is discarded. The paper frames this as distilling valuable trajectories from a complex and often failing agent exploration, which is inherently inefficient.

ToolGrad reverses the order. It first constructs a ground-truth tool-use chain by actually executing APIs, then annotates that chain with a matching user query. An explicit, working chain is far less ambiguous than a hypothetical prompt, so the chain-to-query step takes a single LLM call.

Four modules in a loop

Each iteration runs four modules in sequence:

API Proposer narrows a sampled set of APIs down to a few candidates that could extend the current workflow.

API Executors run those candidates in parallel and produce detailed execution reports.

API Selector reviews the reports, picks the single best-performing call, and appends it to the workflow. Its directional feedback is the textual gradient.

LLM Updater rewrites the synthetic user query and AI response so they match the new API set.

Repeating the loop yields one sample: a user query, a verified API workflow, and the final response. The repository&#8217;s default configuration runs 10 iterations over 50 sampled APIs per workflow.

Generation efficiency on ToolBench

The research team evaluated data generation on the ToolBench API database, which contains 16,000+ real-world APIs, and compared ToolGrad against ToolBench&#8217;s DFS-based query-first approach. According to the research paper:

Pass rate rose from 63.8% (DFS) to 99.8% (ToolGrad).

Ground-truth tool uses per sample rose from 2.1 to 3.4, meaning longer chains.

Tool-use steps per sample fell from 34.3 to 20.0.

LLM invocations per sample fell slightly, from 64.5 to 63.9.

The 0.2% failure case occurred when the agent could not get a successful response from 3 selected APIs across all 10 iterations and saved an empty sample.

Interactive explainer

&&

BFCL results with Gemma-3

The researchers generated ToolGrad-500, a 500-sample dataset built with Gemini 2.5 Flash-Lite, and used it to post-train Gemma-3 at 1B, 4B, and 12B parameters. They evaluated on the Berkeley Function Calling Leaderboard, which uses a tool set that differs from ToolBench, making it an out-of-distribution test with unseen tools. Findings reported by the authors:

Fine-tuning on ToolGrad-500 improved tool-use scores at every parameter size.

ToolGrad-12B scored 83.1, compared with Gemini 2.5 Pro at 83.2, Claude 4.5 Opus at 82.8, and GPT-5 at 74.4, as measured at the time of publication.

The 12B student outperformed Gemini 2.5 Flash-Lite, the teacher model that generated its training data.

ToolGrad-12B led open tool-use specialists including ToolACE and Hammer-2.1-7B.

The repository&#8217;s reproduction scripts target BFCL V1 and V2 through a customized fork, run inference in a vLLM Docker image, and were verified on a single NVIDIA A100 40GB.

Key Takeaways

ToolGrad flips tool-use data generation: verify the chain first, write the query second.

Pass rate jumps from 63.8% to 99.8% on ToolBench, with longer chains and fewer tool steps.

Only 500 samples lift Gemma-3-12B to 83.1 on BFCL, next to Gemini 2.5 Pro at 83.2.

The student model beats its Gemini 2.5 Flash-Lite teacher.

Check out the Paper, GitHub Page, and Google Research Blog. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google Research Releases ToolGrad: Answer-First Framework Hits 99.8% Pass Rate for Tool-Use Data Generation appeared first on MarkTechPost.