---
publish_time: 1794519936
link: https://www.marktechpost.com/2026/11/12/copilotkit-openbot-1-0-open-source-ai-coworker/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  CopilotKit 于 11 月 9 日发布 OpenBot 1.0，一个 MIT 许可、可自托管的智能体工作区，反其道而行——企业自带模型、智能体与基础设施。每个 Bot 拥有独立容器（含专属浏览器、登录态与文件），仅触达被授予的工具；所有浏览器点击、文件写入、MCP 调用与组件都经由统一网关，先写审计行再执行，拒绝规则优先于允许规则，治理内置、动作可审。
---

# CopilotKit 发布 OpenBot 1.0：可自托管的 MIT 许可 AI 同事

> 原文链接：https://www.marktechpost.com/2026/11/12/copilotkit-openbot-1-0-open-source-ai-coworker/
> 来源：MarkTechPost

Most AI coworker products are vendor locked. They pick the model, host the data, and write the rules. CopilotKit is taking the opposite route. OpenBot 1.0, was released November 9th, an MIT-licensed, self-hostable agent workspace. What sets it apart is, a company brings their own models, agents and infrastructure. Governance is fully baked in, and every Bot action is checked against a policy before it runs.

What is OpenBot?

OpenBot is a modular agent workspace from CopilotKit, the team behind the AG-UI protocol. You give a Bot a task and watch it work. You review findings, interact with results and approve next steps in the same conversation.

Each Bot gets a computer of its own. That is a container with its own Chromium browser, logins and files. It reaches only the tools you grant. Answers can come back as charts, checklists, tables and cards. In the new v1.0, Bots now reply in Markdown by default and draw components when they help.

How does the governance gateway work?

Every browser click, file write, MCP tool call and component goes through one gateway. It evaluates a CEL policy, writes the audit row first, then acts. Deny rules run before allow rules, and a broken rule refuses rather than opens.

On top of that, the business tier adds:

Single sign-on and SCIM sync for users and groups. The README documents Google, Microsoft (Entra) and Okta, plus SAML and OIDC.

On-behalf-of tokens, usually scoped to a subset of the person&#8217;s permissions.

Tool grants per Bot, per role or per person, with access requests to an admin.

Policies that block actions or route sensitive work to a human for approval.

Spend visibility per Bot, role, team or person, plus daily, weekly or monthly token limits.

A full audit trail with SIEM export, multi-tenancy and an admin plane.

EU AI Act content labeling, retention controls and deletion on request. CopilotKit itself holds SOC 2 Type II.

Which agents and models can you bring?

Any agent that speaks AG-UI plugs in. The site lists 8 frameworks: Claude Agent SDK, OpenAI Agents SDK, LangChain, Google ADK, Mastra, AWS Strands, Microsoft Agent Framework, CrewAI. The repo also ships Agno, AG2, LlamaIndex and Pydantic AI examples.

For models, teams can use OpenAI, Claude, Gemini or Grok through existing subscriptions or API keys. Open models such as Kimi, DeepSeek, Qwen, Nemotron and Mistral are also supported. Sandboxes, MCP hubs and browsers are swappable lanes.

What is new in OpenBot 1.0?

Desktop app for Mac (Apple Silicon and Intel) and Windows, with signed updates and backup before upgrade.

Teach a Bot: record a task once, and Learning turns the recording into a reusable skill you review.

Multiple accounts per app through Composio and Arcade, with approval rules saved per account. Composio alone brokers a few hundred apps.

Orchestration: one Bot can hand work to specialist Bots, within admin-granted pairs and depth limits.

Early access for iOS, Android, Slack (through OpenTag) and Microsoft Teams.

How do you deploy it?

Personal use runs locally, with workspace data and API keys stored on your machine. For companies, 1 Helm chart deploys into AWS (EKS), Azure (AKS), Google Cloud (GKE) or any Kubernetes cluster.

Pricing is free for personal projects. OpenBot for Business costs up to $29 per active user per month. A 5% charge applies only to model spend above $5,000 per month. The Annual plan adds air-gapped deployment and 24/7 support. Forward-deployed engineers help teams roll it out.

Example use cases

Ticket triage: route new support tickets, then post to Slack after a person approves.

Expense review: check each claim line against policy and flag overages.

Ops workflows: find problems and draft fixes for a human to approve.

How does OpenBot compare?

FeatureOpenBot 1.0OpenAI dots OpenClaw Code licenseMITClosedMIT Where it runsLaptop, your VPC, any KubernetesOpenAI cloud computer per dotYour machine, VPS or serverModelsOpenAI, Claude, Gemini, Grok, Kimi, DeepSeek, Qwen, Nemotron, MistralGPT-6 AstraModel-agnosticBring your own agentAny AG-UI agent, 8+ frameworksNot disclosedBuilt around its own agentPolicy before each actionYes, CEL gateway, fail closedUser-set approval rulesNot disclosedSSO / SCIMYes (business tier)Enterprise admin controls, betaNot disclosedApps / toolsComposio, Arcade, MCP4,000+ appsPlugins and skillsPriceFree personal; up to $29/user/monthFirst dot included in ChatGPT Pro and Business PremiumFree; you pay for models and hosting

Key Takeaways

OpenBot 1.0 is MIT-licensed and self-hostable, from laptop to Kubernetes.

Any AG-UI agent and 9 model families plug in.

Every Bot action passes a policy check before it runs.

Business tier: up to $29 per active user per month.

Check out the GitHub repo, v1.0.0 release notes and open.bot.

Thanks to the Copilotkit team for the thought leadership / resources for this article. This article is sponsored by Copilokit.

The post CopilotKit Releases OpenBot 1.0: An MIT-Licensed, Self-Hostable AI Coworker With Built-In Governance appeared first on MarkTechPost.