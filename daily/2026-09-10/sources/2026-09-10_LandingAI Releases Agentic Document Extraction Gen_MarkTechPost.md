---
publish_time: 1789006392
link: https://www.marktechpost.com/2026/09/09/landingai-releases-agentic-document-extraction-gen2-with-dpt-3-pro-and-dpt-3-verity/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  LandingAI 发布 Agentic Document Extraction（ADE）Gen2，围绕全新 DPT-3 模型族重构文档智能栈。Gen1 将文档视为扁平的 chunk 列表，Gen2 将其建模为树状结构，按返回字符数而非每页计费，并把每个答案溯源到页面具体的行或词。发布围绕三主题：可负担、面向 Agent 的输出、原子级溯源。该版本已正式可用，支持美/欧云端、自有 VPC、Snowflake 及离线环境部署。Gen2 将解析拆分为 DPT-3 Verity（确定性转录，成本约为 Pro 的 40%）与 DPT-3 Pro（先读版式再读词，处理扫描件、手写、非拉丁文与 LaTeX）两模型，按负载选型。计费改为「页数 + 输出字符」双分量，混合负载预计降本 25%–80%。响应结构为 markdown、metadata、structure 三字段，每个块带语义 ID 与 grounding 对象；原子溯源让 PII 按坐标擦除、文档比对与人工审阅 UI 得以工程化实现。
---

# LandingAI 发布 Agentic Document Extraction Gen2 文档智能提取

> 原文链接：https://www.marktechpost.com/2026/09/09/landingai-releases-agentic-document-extraction-gen2-with-dpt-3-pro-and-dpt-3-verity/
> 来源：MarkTechPost

LandingAI has shipped Agentic Document Extraction (ADE) Gen2, a rebuild of its document intelligence stack around a new model family called DPT-3. Gen1 treated a document as a flat list of chunks. Gen2 treats it as a tree, prices it by the characters it returns rather than by the page, and grounds every answer back to a specific line or word on the page. LandingAI team frames the release around three themes: affordability, agent ready outputs, and atomic grounding.

Is it deployable? Yes. ADE Gen2 is generally available now. Developers start free in the ADE playground. Enterprises can run it in US or EU cloud, in their own VPC on AWS, Azure or Google Cloud, inside Snowflake, or on premises including air gapped environments.

Two parsing models instead of one

Gen2 splits parsing into two models so the workload picks the price. DPT-3 Verity transcribes digitally created documents deterministically and returns a bounding box and a confidence score for every word. It targets high volume text, tables and simple form fields. DPT-3 Pro reads page layout before words, detects block types from tables and figures through marginalia and signatures, returns them in reading order, and handles scanned pages, handwriting, non Latin scripts and LaTeX math. LandingAI team states DPT-3 Verity charges roughly 40% of the credits DPT-3 Pro charges, and also state automated routing between the two is planned for fall 2026.

The pricing change is the real story

Under DPT-2, every page cost a flat 3 credits. Under DPT-3, credit consumption is the sum of a page component and an output character component. On the priority tier, DPT-3 Pro bills 1 credit per page plus 0.5 credits per 1,000 output characters. DPT-3 Verity bills 0.3 credits per page plus 0.2 credits per 1,000 output characters. The standard tier halves both rates, so a 12 page Pro parse returning 48,120 characters comes to 36.1 credits on priority and roughly half that on standard. Totals round up to the nearest 0.1 credit, and the response metadata reports every input to the calculation.

Service tiers are the second lever. Priority is for when a person or an agent is waiting. Standard runs asynchronously at 0.5x price and suits pipelines that tolerate minutes to hours. Note that synchronous calls always bill at priority, and the playground itself runs on priority. LandingAI projects 25% to 80% cost reductions on mixed workloads and claims parsing under one cent per page with Verity on standard. Treat those as vendor figures until you benchmark your own document mix, since the character component means a dense page can cost more than it did before.

Blocks, not chunks

The Parse v2 response has three top level fields: markdown in reading order, metadata, and structure. The structure is a document node whose children are pages, whose children are blocks. Block types include text, table, table_cell, figure, marginalia, attestation, logo, card and scan_code. Every block carries a semantic ID in the form type-index, stable within a response but not across re parses, plus a grounding object with the page number, a range into the markdown string, and a normalized bounding box.

Markdown output is standardized too. Figures use <figure type="CHART"> style elements with generated prose isolated inside <description> tags, so transcription is never mistaken for model commentary. Attestations emit stacked labels such as [STAMPED][SIGNED], with [ILLEGIBLE_SIGNATURE] and [ILLEGIBLE_TEXT] as fixed literals. Tables ship as HTML by default to preserve merged cells.

Atomic grounding and what it unlocks

Atomic grounding is the release&#8217;s most consequential capability. Every leaf block carries an atomic_grounding array: one entry per visual line with DPT-3 Pro, one entry per word with DPT-3 Verity. Verity attaches a confidence value from 0 to 1 per word, computed as the lowest per character score in that word, giving teams a signal for routing uncertain transcriptions to review. Table cells now carry their own bounding boxes, though Pro leaves cell level atomic grounding empty. Extract V2 draws citations from this grounding, so an extracted field traces to a specific word on a specific page. That makes PII redaction by coordinate, document diffing and reviewer UIs buildable rather than approximate.

Interactive explainer

Key Takeaways

DPT-3 Pro and DPT-3 Verity (public preview) replace DPT-2 as the parsing models.

Parse billing is now a per page rate plus an output character rate, not a flat 3 credits per page.

DPT-3 Pro grounds to the line, DPT-3 Verity grounds to the word with a confidence score.

Chunks are retired; the response is a document, page and block tree with stable IDs.

Gen1 client code will not run against Gen2 endpoints, so migration is required.

Check out the Technical details here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post LandingAI Releases Agentic Document Extraction Gen2 with DPT-3 Pro and DPT-3 Verity appeared first on MarkTechPost.