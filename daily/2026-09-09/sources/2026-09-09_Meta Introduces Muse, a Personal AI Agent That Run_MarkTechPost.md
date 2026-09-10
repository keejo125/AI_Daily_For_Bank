---
publish_time: 1788928693
link: https://www.marktechpost.com/2026/09/08/meta-introduces-muse-a-personal-ai-agent-that-runs-on-its-own-dedicated-secure-cloud-computer/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Meta 推出个人 AI Agent Muse：它不只是回答问题，而是主动执行任务——发邮件、订行程、谈判账单、推进长期目标；用户关闭 App 后仍持续运行，仅在需审批时返回。架构上每位用户独享一台隔离云虚拟机 Muse Secure VM，Agent、浏览器与凭证均在其中隔离运行。消费端已在美国 iOS/Android/muse.ai 上线；底层模型 Muse Spark 1.3 通过 Meta Model API 与 Muse Code 开放，开源权重列入路线图。
---

# Meta 发布个人 AI Agent Muse：独享隔离云虚拟机

> 原文链接：https://www.marktechpost.com/2026/09/08/meta-introduces-muse-a-personal-ai-agent-that-runs-on-its-own-dedicated-secure-cloud-computer/
> 来源：MarkTechPost

Today, Meta has introduced Muse, a personal AI agent that takes actions rather than just answering questions. Muse can send emails, book travel, negotiate bills, and pursue long term goals. It keeps working after you close the app and returns only when it needs approval. The bigger story for AI devs is architectural. Each user gets a dedicated cloud virtual machine, called Muse Secure VM, where the agent, its browser, and all credentials live in isolation. Is it deployable? Muse itself is a consumer service, rolling out now in the US on iOS, Android, and muse.ai, with a free tier and paid plans. Developers cannot self host Muse, but its underlying model, Muse Spark 1.3, is available today through Meta Model API and Muse Code, with an open weights release on Meta&#8217;s stated roadmap.

What Muse Actually Does

Muse is built around messaging. Users describe a task or a goal, and the agent plans and executes. It can open its browser, fill forms, and negotiate on a person&#8217;s behalf. Meta&#8217;s examples include selling a car for more, lowering a bill, and adapting a training plan. Muse also remembers context across conversations. It can turn a saved Instagram recipe reel into a grocery list and recall friends&#8217; dietary restrictions. Sensitive steps, such as sending an email or completing a purchase, always pause for user approval. A full audit trail shows everything the agent has done and plans to do.

The Model: Muse Spark 1.3

Muse runs on Muse Spark 1.3, released last week by Meta Superintelligence Labs. The model targets long horizon agentic work: zero shot CLI tool calling, multi workflow threads, and self correction across messy sources. In internal comparisons by Meta engineers, it used roughly 20% fewer tool calls and 25% fewer tokens than Muse Spark 1.2. Meta says the model is close to state of the art at resisting prompt injection. Developers can use it now in Muse Code and the Meta Model API at dev.meta.ai.

Muse Secure VM and the Sentinel

The security design is the most technically interesting part of this launch. The agent harness runs inside a systemd-nspawn runtime cell with filtered syscalls and limited kernel capabilities. Security critical services sit outside that cell, on the same VM. A separate Sentinel agent approves every connector action and every network request, at both layer 4 and layer 7. Muse proposes; only Sentinel permits. Credentials are handled through surrogation. The agent only ever sees placeholder tokens, and Sentinel injects real secrets at the network boundary. That makes credential exfiltration via prompt injection structurally futile, since there is nothing real to steal. Kernel level eBPF taint tracking distinguishes clean requests from those that touched user data, gating approvals accordingly. The browser sub agent sees an accessibility tree, not the raw DOM, and cannot execute JavaScript. The email connector even filters out one time passcodes and password reset links by default.

Interactive Explainer: How 1 Muse Action Gets Approved

The embed below walks through the approval pipeline in 5 stages, in Meta&#8217;s blue theme. It includes 2 scenarios: a normal purchase and a blocked prompt injection attempt. 

Key Takeaways

Muse is a proactive personal agent, usable in its own app or directly inside WhatsApp

Each user&#8217;s agent runs in an isolated per user cloud VM with a real browser

A separate Sentinel agent is the sole authority for network egress and connector actions

The agent never sees real credentials; surrogate tokens are swapped at the network boundary

Check out the Muse Spark 1.3, How Meta Built Safety Into Muse and Muse on X. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meta Introduces Muse, a Personal AI Agent That Runs on Its Own Dedicated Secure Cloud Computer appeared first on MarkTechPost.