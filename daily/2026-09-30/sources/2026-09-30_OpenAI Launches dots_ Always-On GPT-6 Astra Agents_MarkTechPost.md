---
publish_time: 1790706613
link: https://www.marktechpost.com/2026/09/29/openai-launches-dots-always-on-gpt-6-astra-agents-that-work-from-their-own-cloud-computers/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  OpenAI在DevDay发布dots——由GPT-6 Astra驱动的常驻型智能体，每个dot拥有独立云端电脑与浏览器，通过ChatGPT插件连接4000+应用，用户下线后仍持续运行。每个用户起始有1个主dot，给定目标、名称与边界后它全天候自主推进并据反馈学习。面向Pro与Business Premium用户开放，企业、教育、医疗工作区在管理员开启后进入beta，无自托管或开源权重选项。
---

# OpenAI 发布 dots：由 GPT-6 Astra 驱动的常驻型云端智能体

> 原文链接：https://www.marktechpost.com/2026/09/29/openai-launches-dots-always-on-gpt-6-astra-agents-that-work-from-their-own-cloud-computers/
> 来源：MarkTechPost

OpenAI just introduced dots at their DevDay today. Dots are persistent AI agents powered by GPT-6 Astra. Each dot gets its own cloud computer and browser. It works across 4,000+ apps through ChatGPT plugins and keeps going after you log off. 

Is it deployable today? Yes, as a managed product. Dots are rolling out in ChatGPT for Pro and Business Premium users in eligible markets. Enterprise, Edu and Healthcare workspaces get a beta once an admin turns it on. There is no self-hosted or open-weights option.

What is a dot

A dot turns ChatGPT from a request and response loop into a standing assignment. You give it a goal, a name and boundaries. It then pursues that goal around the clock and learns from your feedback. Each user starts with 1 primary dot. 

To be honest, much of this was already possible with Codex and similar agent harnesses. The change here is packaging: 1 persistent agent, 1 identity, 1 dedicated machine.

How a dot works

Own computer: Each dot runs on a separate cloud computer with a browser. Your laptop stays isolated unless you connect it. You can open the dot&#8217;s computer at any time to inspect its work.

Tools: It uses the plugins you connect across 4,000+ apps. It can also start tasks in Codex and ChatGPT Work for research, analysis, documents and software.

Surfaces: You can message or call your dot in ChatGPT on web, desktop and mobile. Slack and Teams are supported, and texting is coming soon.

Proactive research: When you are not working with it, the dot looks for ways to help. In this background mode, connected apps are read-only, so it cannot send messages or change content.

The model underneath is also important to know. In OpenAI&#8217;s latency simulations, GPT-6 Astra scores 72.6% on OSWorld 2.0 at roughly 40 minutes per task. GPT-5.6 Sol scored 65.7% at roughly 75 minutes.

Control and safety layer

Built-in rules decide when a dot acts alone and when it asks for approval.

Custom Rules let you allow, block or require approval for specific actions.

Auto-review checks any action that could affect your accounts or share information.

Activity View shows progress, including background work, so you can redirect the dot.

Credential handling: Dots sign in with saved passwords without exposing them to the model. Sensitive tasks, such as changing a password, stay with you.

Monitoring can pause or stop a dot if it detects a safety concern.

OpenAI details this in a separate safety post. It also states that dots can still make mistakes, so consequential work needs review. The caution is timely. A day before launch, OpenAI team stated that its agents had posted users&#8217; images online, affecting 53 ChatGPT users. 

Specialist dots for organizations

OpenAI is also previewing specialist dots. Each gets its own identity, credentials and access to company systems for a fixed role. OpenAI tested them internally across procurement, invoice processing, email marketing, customer support and commercial contracting. Rollout starts with enterprise pilots. OpenAI is working with Microsoft to bring specialist dots to Agent 365.

Pricing and usage limits

The first dot is included in Pro and Business Premium plans at no extra cost. Conversations with a dot do not count toward ChatGPT usage limits. Tasks it starts in Codex or ChatGPT Work do count. OpenAI also added a $500 paid tier the same day. Check the ChatGPT pricing page for current plan limits.

Dots vs Meta Muse vs Instinct: Feature Comparison

FeatureOpenAI dotsMeta MuseInstinctLaunchSep 29, 2026Sep 8, 2026Invite-only since Aug 2026Underlying modelGPT-6 AstraMuse SparkNot disclosedWhere the agent runsOwn cloud computer and browserMuse Secure VM, a dedicated cloud computerOwn computer and phone numberAction gateCustom Rules, auto-review, safety monitorSeparate Sentinel agent approves outbound actionsNo public details foundInterfacesChatGPT web, desktop, mobile; Slack; Teams; texting sooniOS, Android, muse.ai, WhatsAppSMS and texting; no mobile app yetStandout featureRead-only proactive research; 4,000+ appsDeep ties to Meta appsConcierge phone calls; agent-to-agent plans with friendsOrg or team agentsSpecialist dots; Agent 365 work with MicrosoftConsumer launch; Axios reports a shift toward work useConsumer-focused personal assistantAvailabilityPro and Business Premium, eligible marketsUS onlyInvite-onlyPriceIncluded in Pro and Business PremiumFree, $20 or $100 per monthNo public pricing found

The split is clear. Muse chases mass consumer reach. Instinct lives in text messages. Dots start with high-end subscribers, mostly developers.

Interactive explainer: inside a dot&#8217;s work loop

Key Takeaways

Dots are always-on GPT-6 Astra agents, each on its own cloud computer.

They reach 4,000+ apps, but background work stays read-only.

Custom Rules, auto-review and a safety monitor gate risky actions.

Specialist dots start as enterprise pilots, with Microsoft Agent 365 support in progress.

Available now for Pro and Business Premium; no self-hosting.

Check out the Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post OpenAI Launches dots: Always-On GPT-6 Astra Agents That Work From Their Own Cloud Computers appeared first on MarkTechPost.