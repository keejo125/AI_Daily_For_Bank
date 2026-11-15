---
publish_time: 1791528476
link: https://www.marktechpost.com/2026/10/08/google-cloud-launches-gemini-agent-one-universal-agent-for-enterprise-work/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  MarkTechPost 报道，Google Cloud 推出 Google Cloud Gemini agent——一个面向企业工作的单一智能体，从一个提示框与一个 API 出发，回答问题、做知识工作、创建媒体、编写并运行代码，可从 Web、移动、桌面、CLI、Workspace、Microsoft 365、Slack 或 headless 方式触达，Bloomberg Media 等客户已落地。
---

# Google Cloud 推出 Gemini Agent：一个面向企业工作的通用智能体

> 原文链接：https://www.marktechpost.com/2026/10/08/google-cloud-launches-gemini-agent-one-universal-agent-for-enterprise-work/
> 来源：MarkTechPost

Google Cloud has introduced the Google Cloud Gemini agent, a single agent for enterprise work. The Gemini agent is a cloud-hosted agent from Google Cloud that answers questions, does knowledge work, creates media, and writes and runs code. It does all of this from 1 prompt box and 1 API. For developers, the agent is the product and the model is a routing decision.

TL;DR

Runs on: Google Cloud (AI Hypercomputer). Reached from web, mobile, desktop, CLI, Workspace, Microsoft 365, Slack, or headless.

Best: Bloomberg Media lifted SQL query accuracy by 63% by grounding data agents in Knowledge Catalog.

Bottom line: 

Best: 1 governed agent with cloud memory, sub-agents and hard spend caps. 

Worst: buyers must evaluate it on customer anecdotes, not reproducible numbers.

What is the Google Cloud Gemini agent?

It is a delegation layer, not a chatbot. You give it objectives, not instructions. It plans the work, picks skills and tools, connects to company systems, and returns finished output.

Google lists 6 architectural principles:

Unified agent: chat, autonomous objectives and code generation share 1 interface.

Omnipresent access: any device or channel, plus embedding in third-party apps.

Persistent execution: it runs in the cloud with 1 set of memories and 1 personalization graph. Jobs lasting hours or days keep running after you close the laptop.

Multi-agent orchestration: it creates temporary sub-agents, each with its own identity, and runs parallel or sequential steps.

Deeply contextual: it learns your tools, data and work history over time.

Model choice flexibility: each job runs on the best-fit model.

Today at Google Cloud’s Gemini at Work event, we announced Gemini, a new single universal agent for work that has all of your business context and can be used for everything from knowledge work to answering questions, and content creation to coding, all from a single prompt box.… pic.twitter.com/2Z1PZg74Ui
&mdash; Thomas Kurian (@ThomasOrTK) October 8, 2026

How does the Gemini agent remember and reason?

It keeps 4 kinds of memory. Session memory covers the current task, even across days. Semantic memory is a structured knowledge base it builds from documents and people. Procedural memory stores how jobs get done, including skills it writes for itself. Episodic memory records everything it has done before.

Skills are modular prompts stored in a shared company registry. Tools come from an enterprise tools registry. Connectors cover Slack, Jira, Salesforce, ServiceNow, BigQuery, Snowflake, desktop files and any Model Context Protocol server.

Which models does it use?

Today it orchestrates across Google&#8217;s Gemini models and Claude models from Anthropic, with other private and open models planned. Google&#8217;s own lineup is Argon for frontier reasoning, Flash for speed and volume, Omni for generative media, and Gemma for open-weights edge work.

What are coworker agents?

A coworker agent is a persistent teammate with a defined role. In Workspace it receives its own account: email address, calendar, Drive and a directory entry. Colleagues @mention it in Chat or Docs, and its edits appear under its own name in version history. It sees only what is shared with it.

The agent also works inline across Gmail, Docs, Sheets, Slides, Chat and Calendar, and offers 1-click delegation of tasks it spots.

What does it add for data teams?

Data and ML engineers describe outcomes in plain language. The agent then writes PySpark code, provides notebooks, trains models and fixes pipeline issues. Business users get saved BigQuery reports that rerun without token costs.

Three services ground the answers. Knowledge Catalog maps business definitions once for every agent. Smart Storage enriches unstructured objects in place; Google says 90% of enterprise data is unstructured. Borderless Lakehouse queries Amazon S3 and Azure Data Lake with no variable egress fees.

&&&

How is the agent governed?

Google frames governance as 4 questions: who, what it may do, what it did, and what it must never touch.

Identity: each agent gets a cryptographically attested identity with least-privilege permissions.

Authorization: role-based access, mapped to external systems through standards such as OAuth.

Auditing: every action is logged to the agent, not a person.

Policy: agents run in an Agent Sandbox. All traffic passes through Agent Gateway, an AI network firewall that applies 1 policy to every agent.

How does Google control cost?

Three levers: multi-model orchestration, Smart Routing that triages workloads to the cheapest capable model, and real-time spend caps. Teams set a hard project limit in the Cloud Billing Console. When it triggers, that project&#8217;s agent pauses until someone resumes it. Underneath, Google team states its TPU 8i system delivers 80% better price-performance than the prior generation.

How does it compare?

FeatureGoogle Cloud Gemini agentMicrosoft 365 CopilotOpenAI ChatGPT WorkAmazon QuickModelsGemini family + Anthropic Claude; more plannedNot disclosed on source pageGPT-5.6 at launchNot disclosed (Fast, Balanced, Smart modes)SurfacesWeb, iOS, Android, Windows, Mac, CLI, Workspace, M365, Slack, headlessM365 apps, Teams, Copilot ChatWeb, mobile, Mac and Windows desktop, Slack, TeamsDesktop, web, mobile, browser and M365 extensionsPersistent agent identityCoworker agents with own email, calendar, DriveNot disclosedNot disclosedNot disclosedLong-running workHours or days in cloudNot disclosedHours; Scheduled TasksQuick Flows; Quick Automate (Enterprise)

Key Takeaways

1 agent, 1 API: Q&A, knowledge work, media and code.

Routes jobs across Gemini and Claude models today.

Coworker agents get their own Workspace identity.

Hard per-project spend caps pause runaway agents.

No benchmarks, price or GA date yet.

Check out the Google Cloud announcement. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Google Cloud Launches Gemini Agent, One Universal Agent for Enterprise Work appeared first on MarkTechPost.