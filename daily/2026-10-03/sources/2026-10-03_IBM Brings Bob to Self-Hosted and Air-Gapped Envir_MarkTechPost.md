---
publish_time: 1791010515
link: https://www.marktechpost.com/2026/10/02/ibm-brings-bob-to-self-hosted-and-air-gapped-environments/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  IBM 将其智能体软件开发平台 Bob 的自托管部署正式发布（GA），企业可在本地、私有云、主权云及空气隔离（air-gapped）网络中运行，代码与数据不出域。Bob 覆盖理解代码、规划、执行变更与验证的完整生命周期，支持 IDE、BobShell、并行工具调用、agent harness、skills 与多种模式；模型由客户按 IBM 支持清单自带（BYOL），推理位置由模型层决定。
---

# IBM 推出 Bob 自托管与空气隔离部署：代码不出域的智能体开发平台

> 原文链接：https://www.marktechpost.com/2026/10/02/ibm-brings-bob-to-self-hosted-and-air-gapped-environments/
> 来源：MarkTechPost

IBM has made a self-hosted deployment option for IBM Bob generally available. Bob is IBM&#8217;s agentic software development platform. It covers the full lifecycle: understanding code, planning work, executing changes and validating results. The new option lets enterprises run Bob on premises, in private or sovereign clouds, and in air-gapped networks. 

Is it deployable today? Yes. The self-hosted option is generally available to enterprise customers. You must source, license and host a supported model yourself. IBM has not published pricing and routes buyers to a demo request.

What IBM Shipped at GA

The self-hosted deployment includes:

Bob running in customer-managed enterprise environments.

Core Bob capabilities: the IDE experience, BobShell, parallel tool calling, the agent harness, skills and modes.

Self-hosted, air-gapped and hybrid model configurations.

Bring-your-own-license (BYOL) for eligible models on IBM&#8217;s supported list.

Integration with supported IDE and infrastructure environments.

Optional Premium Packages for Java Modernization, IBM i and IBM Z.

The Model Layer Decides Where Inference Runs

Bob self-hosted does not bundle a model. Customers bring one from IBM&#8217;s supported list. IBM groups the list by deployment method:

Deployment methodWho hosts the modelSupported models at GASelf-hostedCustomer, on its own infrastructureNVIDIA Nemotron, Poolside LagunaHybrid or private SaaSExternal service via an approved private connectivity patternClaude Sonnet 5.0, Claude Opus 4.8, Gemini 3.7 Flash, OpenAI GPT 5.6 Sol

This choice determines where code and context get processed. With a self-hosted model, code, development context and build artifacts can remain inside the customer environment.

IBM gives a concrete example. A bank could run on-premises inference for core banking applications. The same bank could route a less restricted workload to an approved external model. Developers see a consistent core Bob experience in both cases, while platform and security teams control the architecture underneath.

IBM also plans to expand the model portfolio and add multi-model routing. Treat that as roadmap, not a shipped feature.

Interactive Explainer

&&

How Bob Self-Hosted Compares With Its Closest Competitors

FeatureIBM Bob (self-hosted)GitLab Duo Agent Platform Self-HostedMistral Vibe for Code (Enterprise)GitHub Copilot CLI (BYOK)On-prem or private cloudYesYes, on GitLab Self-ManagedYes, on-prem or private cloudCLI only; core Copilot runs on GitHub.com or GHE.comAir-gappedYes, with supported self-hosted modelsYes, with an offline licenseOpen-weight Devstral models suit air-gapped useYes, offline mode with a local modelHybrid local plus external modelsYes, per workloadYes, hybrid AI GatewayOn-prem, private cloud or Mistral CloudYes, via BYOK providersModels when self-hostedNVIDIA Nemotron, Poolside LagunaSupported list on vLLM, Bedrock or Azure OpenAIMistral models, fine-tuning via ForgeAny provider with tool calling and streamingDeveloper surfacesIDE, BobShellGitLab UI, IDE, CLI (beta)CLI; VS Code, JetBrains, ZedTerminalCommercial modelEnterprise, via IBM salesPremium or Ultimate plus add-onEnterprise, contact salesNo Copilot license needed with BYOK

Sources: IBM, GitLab docs, Mistral Vibe, Mistral coding stack, GitHub changelog, GitHub Docs.

The differentiator is scope. GitLab and GitHub bring agents to their own DevOps platforms. Mistral pairs its agent with its own open-weight models. IBM targets modernization of long-lived estates, especially Java, IBM i and mainframe code, inside environments that cannot touch the public internet.

Key Takeaways

IBM Bob self-hosted is GA for on-prem, sovereign cloud and air-gapped use.

Customers bring their own model: Nemotron or Poolside Laguna for full isolation.

Hybrid mode routes selected workloads to Claude, Gemini or GPT models.

Premium Packages extend Bob to Java, IBM i and IBM Z modernization.

Check out the Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post IBM Brings Bob to Self-Hosted and Air-Gapped Environments: Agentic Software Development Without Moving Your Code appeared first on MarkTechPost.