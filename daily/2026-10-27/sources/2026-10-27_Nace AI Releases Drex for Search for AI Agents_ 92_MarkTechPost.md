---
publish_time: 1793033169
link: https://www.marktechpost.com/2026/10/26/nace-ai-releases-drex-for-search-for-ai-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Nace AI 发布面向 AI 智能体的搜索模型 Drex，在 BrowseComp-Plus 基准上取得 92.05% 的成绩（平均 12.6 次搜索调用），专为智能体自主检索与信息整合设计。
---

# Nace AI 发布面向 AI 智能体的搜索模型 Drex

> 原文链接：https://www.marktechpost.com/2026/10/26/nace-ai-releases-drex-for-search-for-ai-agents/
> 来源：MarkTechPost

Nace AI has released Drex for Search, which brings its Drex decision models to document search. Drex for Search is a retrieval layer that helps people and agents find evidence. Coding agents such as Claude Code, Codex, Cursor and OpenCode call it through CLI, SDKs, MCP or REST. In Nace&#8217;s evaluation, it scores 92.05% on BrowseComp-Plus with GPT-5, using 12.6 search calls per question.

TL;DR

Size: a hosted search system built to search over 1M+ files. It pairs with an answering model such as GPT-5, Gemini 3.5 Flash or Qwen 27B.

Runs on: Nace&#8217;s managed cloud, a dedicated cloud, your own AWS or Azure account, or on-prem and air-gapped.

Performance: ranked #1 or #2 on 3 of 4 public leaderboards, per Nace.

Best: 77.5% R@1 on VisDocAgentBench, 10 points above Claude Opus 5 (67.5%).

What did Nace AI release?

Nace AI frames search as a series of decisions. Drex for Search applies its Drex models to those decisions. Drex scores given options with a calibrated probability each, in 1 forward pass. That makes it cheap enough for every agent step.

The release targets classic RAG, which Nace sums up as chunk, embed, top-k, hope.

The pipeline breaks in 3 cases:

the answer sits in a table on page 23

the answer needs 2 hops across files

the answer is inside a scanned PDF

How does Drex for Search work inside an agent?

Nace describes 3 steps:

Classify: Before any search runs, Drex decides if the question needs a quick lookup or an agent. The agent route reads documents and queries tables.

Squeeze: Drex walks the workspace level by level: folder, file, section, page. Inside a sheet, it narrows to table and column. Each level keeps only what can hold the answer.

Answer: Only the kept pages and tables reach the LLM. The answer cites the file and page.

Depth is fixed, so Nace says a million files take as many steps as a thousand.

How much does it help coding agents?

Nace AI tested 9 agent and model pairs on OfficeQA Pro, a 133-question benchmark over U.S. Treasury Bulletins. Key highlights: 6% more answers right, 62% fewer steps, 56% fewer tokens, and 2.3x faster.

HarnessModelAccuracy as shippedAccuracy with Drex for SearchAgent turns as shippedAgent turns with Drex for SearchGemini CLIGemini 3.1 Pro54.9%61.7%22.910.4CodexGPT-6 sol66.2%70.7%14.38.6Hermes AgentOpus 5.564.3%68.4%8.53.7Hermes AgentQwen3.8-27B56.4%60.2%20.16.5Claude CodeOpus 5.566.5%69.9%18.59.1piOpus 5.565.4%68.4%7.73.7OpenCodeQwen3.8-27B51.1%53.4%23.710.0piQwen3.8-27B43.6%45.9%24.311.1CodexGPT-6 luna54.9%53.4%16.811.3

What does a workspace include?

Files: PDFs and scans, xlsx, csv and Parquet, mp3 and mp4, docx, pptx, md, json and txt.

Citations: every answer names the file and the page, row or minute it came from.

Workspaces: isolated, with their own index and knowledge graph, and shareable with invited members.

Storage: upload files or folders, or keep workspaces in your own S3 bucket or Azure Blob container.

Zero retention: available with your own storage.

Domains: Tax, M&A, SEC 10-K, Contracts, or your own.

How does it perform on BrowseComp-Plus?

BrowseComp-Plus asks a deep-research agent 830 multi-hop questions over about 100K fixed web documents. With GPT-5, Nace AI reports:

92.05% accuracy, #2 of 86 entries on the leaderboard.

12.61 search calls per question, 16.6x fewer than the only entry ahead (209.27 calls).

87.32% in a single pass with 8.93 search calls, the best of any entry under 10 calls.

+20.4 points over the Qwen3-Embed-8B baseline, with the same GPT-5 model.

&

How does it score on document benchmarks?

On VisDocAgentBench, an agent finds 1 target page among 2,375 arXiv pages. Drex for Search scores 77.5% R@1 with an open-weight Qwen 27B planner. The best published agent, Claude Opus 5, scores 67.5%. R@1 is 97.5% on direct questions, 77.5% on one bridge, and 57.5% on two.

On MADQA, agents answer over 800 PDFs and cite pages. Nace reports 94.7% accuracy with Gemini 3.5 Flash and a page-attribution F1 of 88.2. Its effort calibration (Kuiper) is 6.66. Nace ranks it #1, based on the leaderboard as read on October 20. With open-weight Qwen 27B, Nace reports 93.4%.

On EnterpriseRAG-Bench, with 500,000+ internal company documents, Nace reports an overall score of 88.22, which it ranks #3. That is 27.2 points above OpenAI File Search (61.03).

How does it compare with the best published results?

Ranks and scores are as published by Nace AI, from leaderboards read October 20, 2026.

Benchmark (Drex rank, per Nace)SystemOrganizationAnswer modelScoreBrowseComp-Plus, accuracy and search calls per question (#2 of 86)Hybrid Qwen2-7B + Reason-ModernColBERTAI21 LabsGPT-595.18%, 209.27 callsDrex for SearchNace AIGPT-592.05%, 12.61 callsMixedbread Search (v3)MixedbreadGPT-590.48%, 11.53 callsReason-ModernColBERTLightOnGPT-587.59%, 13.27 callsVisDocAgentBench, R@1 (#1)Drex for SearchNace AIQwen 27B (planner)77.5%Tool-using agentAnthropicClaude Opus 567.5%Tool-using agentAnthropicClaude Fable 562.5%Tool-using agentOpenAIGPT-5.6-sol61.67%MADQA, accuracy (#1)Drex for SearchNace AIGemini 3.5 Flash94.7%Agentic RAGProgress SoftwareGemini 3.5 Flash + 3.6 Flash94.3%Agentic SearchMixedbreadGemini 3.5 Flash93.4%PPLX Embed 2 RAGPerplexityGemini 3.5 Flash92.1%File SearchOpenAIGPT-549.6%EnterpriseRAG-Bench, overall score (#3 of 31)Flexor.aiFlexor.aiGPT-6.1 Sol91.48CDLCausal Dynamics LabNot listed90.91Drex for SearchNace AINot listed88.22MixedbreadMixedbreadClaude Opus 586.58OpenAI File SearchOpenAIManaged product61.03Azure AI SearchMicrosoftManaged product48.42Vertex AI SearchGoogleManaged product41.87

How can developers get access?

Drex for Search runs in the Nace API Console, with 4 ways in on one key:

CLI: nace-cli on PyPI.

SDKs: nace-sdk for Python and nace-sdk for TypeScript.

MCP: nace-mcp, for Claude Code, Codex, Cursor or OpenCode.

REST: an OpenAPI spec.

Key Takeaways

Drex for Search gives agents cited pages and tables, not top-k chunks.

92.05% on BrowseComp-Plus with 16.6x fewer search calls than the only entry ahead.

77.5% R@1 on VisDocAgentBench, 10 points above Claude Opus 5.

On OfficeQA Pro, agent turns fell for all 9 harness and model pairs Nace tested.

Check out the Drex for Search page, API Console, Docs and Hugging Face.

Thanks to the Nace AI team for the thought leadership / resources for this article. This article is sponsored by Nace AI.

The post Nace AI Releases Drex for Search for AI Agents: 92.05% on BrowseComp-Plus With 12.6 Search Calls appeared first on MarkTechPost.