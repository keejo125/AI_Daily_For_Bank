---
publish_time: 1793605632
link: https://www.marktechpost.com/2026/11/01/nvidia-auto-ontology-open-source-semantic-layer-ai-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA 以 Apache 2.0 许可开源 Auto Ontology，一个为 AI Agent 编写 SQL 提供语义层框架。它从企业元数据构建上下文层，让 Agent 基于经过认证的业务定义生成 SQL，避免「数字算得快却算错」的问题。默认 LLM 采用 nvidia/nemotron-3-nano-30b-a3b，并配套 Nemotron 的嵌入与重排模型；部署支持本地 Docker Compose 或 Kubernetes（Helm）。该库面向企业数据分析场景，强调在 Agent 调用数据库时绑定权威业务口径，提升结果可信度。
---

# NVIDIA 开源 Auto Ontology 语义层

> 原文链接：https://www.marktechpost.com/2026/11/01/nvidia-auto-ontology-open-source-semantic-layer-ai-agents/
> 来源：MarkTechPost

NVIDIA has released Auto Ontology, an open library under the Apache 2.0 license. NVIDIA Auto Ontology is a semantic layer framework that builds a context layer from enterprise metadata. Agents use that layer to write SQL against certified business definitions. The repository states the problem plainly: a fast revenue answer is worthless if the number is wrong. 

TL;DR

Library: Default LLM is nvidia/nemotron-3-nano-30b-a3b, with Nemotron embedding and reranking models. 

Runs on: Docker Compose for a local stack, or Kubernetes via Helm. Inference uses hosted NVIDIA NIM endpoints or self-hosted NIMs. 

Performance: Strong engineering, thin public evidence. 

Best: Ontology creation time cut by 90% in NVIDIA testing (self-reported).

Worst: 0 published text-to-SQL accuracy scores. The eval repo ships a harness, not results.

Bottom line: An open, MCP-ready context layer that any agent harness can query. But you must run the benchmarks yourself to trust it.

What is NVIDIA Auto Ontology?

It is a context layer that sits between an agent and the data warehouse. It tells the agent where data lives and what fields mean. It also says whether to use a field, how to use it, and where it came from.

Here are the five jobs:

Discover: generate ontologies from metadata and connect existing semantic models.

Ground: give agents trusted meaning for metrics, entities and relationships.

Validate: check generated queries against certified definitions and lineage.

Expose: serve context through MCP, CLI and API.

Learn: fold certified corrections back into the ontology.

NVIDIA&#8217;s developer page frames the output as a starting ontology. Business experts still test, refine and certify it.

How does Auto Ontology work?

The stack has 4 core services. A Next.js 16 frontend handles the web UI and authentication on port 3000. A FastAPI backend with LangChain runs chat, NL-to-SQL and catalog APIs on port 3001. An ingestion worker writes embeddings on port 3002. Postgres with pgvector stores the catalog, the ontology and the vectors.

Source databases can be Databricks, Postgres, Snowflake or DuckDB. Models are set through environment &#8220;triplets&#8221; of endpoint, key and model. Separate roles exist for reasoning, non-reasoning, embedding and reranking. Any OpenAI-compatible endpoint works.

&&

What does the MCP server expose?

The MCP server docs describe 9 read-only tools. ask_question returns the answer, the SQL and the rows as separate fields. Results cap at 100 rows. check_readiness confirms a compiled semantic layer and a live database connection exist.

There is no tool for browsing raw schemas. NVIDIA chose that on purpose, so agents reach data through the semantic layer. The underlying OpenAPI spec publishes 87 operations. Sign-in runs through OAuth, and every call carries the signed-in user&#8217;s permissions.

How is it benchmarked?

NVIDIA ships a separate harness, auto-ontology-eval. It runs 2 arms in NeMo Gym: a schema-only LLM control and the ontology-grounded agent. Scoring is deterministic execution match, with no LLM judge.

Bundled datasets include BIRD Dev (1,534 questions, 11 databases) and Mini-Dev (500 questions). FDABench-Lite adds 169 questions, and BEAVER defaults to a 100-question sample. 

The harness repo adds 2 limitations. Optional few-shot exemplars and value anchors go to the ontology arm only. A delta measured with them covers those inputs, not grounding alone. Its tested configuration also routes both arms through a Claude model on NVIDIA&#8217;s inference gateway.

How does it compare with other semantic layers?

FeatureNVIDIA Auto OntologyWren AICube Coredbt MetricFlowLicenseApache 2.0Apache 2.0 core (open core)Apache 2.0 backend, MIT clientApache 2.0 (v0.209.0+)How the layer is builtGenerated from metadata, then certifiedAgent-assisted context files in GitDefined in codeDefined in code in a dbt projectAgent interfaceMCP, CLI, REST APIMCP, CLI, SDKsSQL, REST, GraphQL APIsPython library and CLIData sourcesDatabricks, Postgres, Snowflake, DuckDB22+All SQL data sourcesVia dbt adaptersDefault modelsNemotron via NVIDIA NIMNot disclosedNot applicableNot applicable

Deployment and availability

Local setup is docker compose up -d --build after filling in .env. Kubernetes users get a Helm chart and a DEPLOYMENT.md guide. NVIDIA team also publishes the backend as an NGC container. An NVIDIA API key from build.nvidia.com covers the default models.

Key Takeaways

Auto Ontology generates a starting semantic layer from enterprise metadata.

Agents query it through 9 read-only MCP tools, plus CLI and API.

NVIDIA reports 90% faster ontology creation in its own testing.

No text-to-SQL accuracy scores are published yet.

Defaults to Nemotron on NIM, but accepts any OpenAI-compatible endpoint.

Check out the GitHub repo, the eval harness and the MCP docs. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Releases Auto Ontology: An Open Semantic Layer That Grounds AI Agent SQL appeared first on MarkTechPost.