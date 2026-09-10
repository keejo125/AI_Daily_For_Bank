---
publish_time: 1788392927
link: https://www.marktechpost.com/2026/09/02/qwen-developers-open-sources-zg-zvec-grep-a-local-first-search-layer-unifying-ripgrep-bm25-and-vector-search/
source: Qwen
status: confirmed
category: 国内
is_model_related: false
digest: |
  Qwen开发者团队开源zg（zvec-grep），本地优先的搜索层，将语义搜索、BM25与ripgrep统一于一个接口，供人与Agent使用，Apache 2.0。Coding Agent大量工具预算花在搜索上，zg一次性索引工作区，提供混合默认、--fts（BM25）、向量等多条检索路由，无需GPU，npm安装，减少猜测术语与整文件读取的token与耗时浪费。
---

# Qwen 开发者开源 zg（zvec-grep）：统一 ripgrep、BM25 与向量搜索的本地优先搜索层

> 原文链接：https://www.marktechpost.com/2026/09/02/qwen-developers-open-sources-zg-zvec-grep-a-local-first-search-layer-unifying-ripgrep-bm25-and-vector-search/
> 来源：MarkTechPost

Coding agents spend a large share of their tool budget on search. When the target is a known symbol, ripgrep answers it exactly. When the target is a behavior described in plain language, keyword matching often misses, and the agent falls back to guessing terms, reading whole files, and assembling context by hand. Each of those detours costs tool calls, tokens, and wall-clock time.

The Qwen Developer team announced zg (zvec-grep), an open-source local-first search layer that puts semantic search, BM25, and ripgrep behind one interface for both humans and agents. The code ships under the zvec-ai GitHub organization with an Apache 2.0 license.

Is it deployable? Yes, today. It installs from npm as @zvec/zvec-grep, requires Node.js 22 or newer on macOS, Linux, or Windows, needs no GPU with the default model, and the Apache 2.0 license permits commercial use. 

One index, four retrieval routes

zg indexes a workspace once and then exposes several ways to query it. The retrieval pipeline docs define four routes: a hybrid default that combines intent with lexical anchors, --fts for BM25-ranked exact terms, --vector for conceptual similarity with no lexical ranking, and --rg for exhaustive literal or regex matching. The first three read the index. The --rg route needs no index at all, which matters when a repository has not been indexed yet.

An anonymous workspace index lives in <root>/.zvec-grep/. Both .git and .zvec-grep are always excluded, along with common dependency, build, cache, and log directories, plus anything the repository&#8217;s own ignore rules exclude. Re-running zg index updates incrementally; changing the embedding model requires an explicit --rebuild because vector spaces from different models are incompatible even at matching dimensions.

Indexed results report a freshness state of fresh or possibly_stale, so an agent can act on a good-enough result instead of running a status preflight first.

The MCP surface agents actually see

zg install detects Codex, Claude Code, Cursor, and OpenCode on the machine and wires up the local MCP integration. The server speaks Streamable HTTP MCP on a loopback-only endpoint at http://127.0.0.1:7999/mcp, with optional bearer authentication.

The design decision worth noting is restraint. Per the MCP guide, the default agent toolset exposes exactly two tools: zvec_grep_search for when the intent is known but the exact string is not, and zvec_grep_rg for when a symbol, path, or regex is known. Index lifecycle stays with the CLI. A six-tool compatibility set that adds index create, drop, status, and server status exists but is opt-in through zg server on --mcp-toolset full, and the docs state that an agent must never silently create, rebuild, or delete a persistent index.

Output is shaped for context economy. Results come back grouped by file with line spans, and indexed source previews are omitted by default unless requested. zg also rejects output-changing ripgrep flags such as --json, --count, -l, and --vimgrep so the compact result format holds.

Embeddings run on device by default

The embedding catalog currently documents ten local models and three remote Qwen endpoints. The quickstart default, local/potion-code-16m-v2, is a Model2Vec static model with a 256-dimension output and an 8,192-token input limit; because it uses static vector lookup, selecting a GPU does not speed it up. Heavier local options include jina-embeddings-v2-base-code, embeddinggemma-300m, and qwen3-embedding-0.6b. Remote options run to qwen/qwen3.7-text-embedding at 128,000 input tokens and the multimodal qwen/qwen3-vl-embedding.

Remote use is gated. Configuring a provider credential does not authorize data transfer; that requires either --allow-remote for a single command or a signed workspace grant via zg auth grant, revocable with zg auth revoke. The launch post cites eleven on-device models against ten in the current docs, a small discrepancy worth flagging.

What the benchmark numbers say

The evaluation numbers appear in the launch post, not in the repository, where the benchmarks section is still a placeholder. Both runs were paired A/B tests holding agent, model, prompt, runtime, and task constraints fixed, with the zg condition adding only a prebuilt index, MCP tools, and usage guidance. Index build cost is excluded from the tables.

On a 20-question SWE-QA-Bench sample, zg cut tool calls by more than half and input tokens by nearly half while raising the Judge score by 1.50 points. On an 80-question BrowseComp-Plus sample, accuracy moved from 98.67% to 99.00% while input tokens fell 37.56%, tool calls 43.52%, and agent time 38.58%. Separately, indexing the Django repository (3,457 files) is reported to finish in under 30 seconds on an Apple M4 Pro.

Sample sizes of 20 and 80 questions are small, and the reported reductions come from the vendor&#8217;s own runs, so independent replication is the obvious next step.

Interactive explainer

Key Takeaways

zg unifies ripgrep, BM25, and vector search behind one local-first interface for humans and agents.

The default MCP toolset exposes only two tools; index lifecycle stays with the CLI by design.

Indexing, embedding, and retrieval run on device; remote embeddings need explicit per-command or workspace authorization.

Vendor A/B runs report roughly 40% to 50% cuts in tool calls and input tokens on small samples.

Apache 2.0, npm-installable, Node.js 22+, no GPU needed with the default model.

Check out the zvec-ai/zvec-grep, Qwen Developers launch post and Roadmap. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Qwen Developers Open-Sources zg (zvec-grep): A Local-First Search Layer Unifying ripgrep, BM25, and Vector Search appeared first on MarkTechPost.