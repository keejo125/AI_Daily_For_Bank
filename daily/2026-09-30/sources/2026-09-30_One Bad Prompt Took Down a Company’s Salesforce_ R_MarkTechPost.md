---
publish_time: 1790731817
link: https://www.marktechpost.com/2026/09/29/rsa-launches-agent-id-to-discover-secure-and-govern-ai-agents-in-regulated-industries/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  RSA在旧金山AI大会上发布RSA Agent ID，面向金融、政府、医疗等受监管行业的智能体身份安全平台。Gartner预计典型全球500强企业到2028年将运行约15万个AI智能体（2025年不足15个），仅13%组织认为自己具备完善的智能体治理。Agent ID用于发现、保护并治理企业内隐藏的影子智能体——它们持有凭证、拥有权限并操作系统记录，多数企业却无法掌握其运行状态与归属。
---

# RSA 发布 Agent ID：治理企业内隐藏的 4000 个影子 AI 智能体

> 原文链接：https://www.marktechpost.com/2026/09/29/rsa-launches-agent-id-to-discover-secure-and-govern-ai-agents-in-regulated-industries/
> 来源：MarkTechPost

AI agents are moving into production faster than security teams can track them. They hold credentials, carry entitlements, and act on systems of record, yet most enterprises cannot say which agents are running, who owns them, or whether anyone can stop them. Gartner expects a typical Global Fortune 500 enterprise to run roughly 150,000 AI agents by 2028, up from fewer than 15 in 2025, while only 13% of organizations believe they have the right agent governance in place.

At The AI Conference in San Francisco, RSA announced RSA Agent ID, an agentic identity security platform for regulated industries such as finance, government, healthcare, and critical infrastructure. We sat down with Jim Taylor, President and Chief Product and Strategy Officer at RSA, to dig into how it works.

Why Agents Break the Identity Model

“What changes with agents? Everything. They’re not a service account. They’re not static. They’re dynamic. You give an agent a task, and if you badly word that task, it will do whatever it deems necessary to perform it. Agents don’t get tired at two o’clock in the morning. They just go.”

Agents also accumulate permissions, data, and access over time, and nobody follows up. “Employees create an agent to hit a deadline, but once it’s off in the wild, that’s it. We don’t check when its permissions change. We don’t delete or disable agents.”

The scale surprises even regulated firms. A medium-sized global bank told RSA it had no agents, since policy prohibited them. “Agents don’t tend to respect policy,” Taylor said. “We did an audit and found more than 4,000 agents running around in their enterprise.” According to IBM, incidents involving shadow AI cost $670,000 more on average than standard incidents.

When a Prompt Becomes a Denial-of-Service Attack

Taylor’s failure scenario involved no attacker at all. A customer success employee at an unnamed company asked an agent to “go to Salesforce and get all the data” to build customer health charts. The agent began downloading the entire Salesforce database. Salesforce’s defenses read the traffic as an attack, shut down the instance, and warned the company that it appeared to be under a denial-of-service attack.

“One operator on the customer service desk took the whole company’s Salesforce instance down by essentially having an agent perform a denial-of-service attack. He didn’t do anything wrong.”

Discover, Secure, Govern

RSA Agent ID ships as three modules, available standalone or as one system on the RSA Unified Identity Platform.

Discover scans endpoints (via connectors into tools such as CrowdStrike and Zscaler), devices, network, and applications in real time. It finds agents and MCP servers, sanctioned and shadow, and registers each as a first-class identity with a named owner, risk tier, and lifecycle state, linked to existing identity providers such as Microsoft Entra ID, Okta, and AWS IAM. “Every agent should have an owner,” Taylor said. “It should be attached to a human identity.”

Secure is an inline AI/MCP Gateway that checks every tool call against policy at tool and argument depth. Calls within policy are allowed, calls against policy are denied, and high-risk calls are escalated to the registered owner. Approvals go through an out-of-band, authenticated channel with phishing-resistant credentials that agents cannot access.

Govern logs every governed action and maps the evidence to ten regulatory and industry frameworks out of the box, streaming it to the customer’s SIEM. “Regulators want to know if you had a policy in place at the time of an incident, who approved it, what actions took place, and they want to see that in indelible logs,” Taylor said.

Human Assurance, Not Human in the Loop

Taylor rejects the approve/deny fatigue of today’s AI tools. “A hundred prompts a day is just an invitation to say yes. It’s another form of denial-of-service attack.”

Instead, a risk engine scores each action on the user (is this expected behavior?), the action (read, write, or something riskier?), and the data and endpoint (how sensitive is the target?). Only actions that cross a threshold go to a human. A refund agent might process refunds under $500 automatically, while larger ones need the owner’s approval, or a second approver through a built-in workflow.

The customer defines what counts as high-risk, with AI-assisted suggestions. “I don’t know what’s important to everyone else on the planet,” Taylor said. “Organizations know their business risk.”

Layered Defense, Not a Silver Bullet

Asked about a prompt-injected support ticket requesting a fraudulent refund, Taylor said hidden malicious instructions are evaluated against policy and would be caught. A legitimate-looking refund from a fraudster on a stolen device is a different problem. “Models have good guardrails, but they’re not enough. You need a fraud detection system too.”

He was just as candid about gateway bypass, such as coding agents lifting another team’s API keys from a repository. “We don’t walk on water,” he said. API gateways, firewalls, and traffic inspection should also catch credential theft. “We don’t need to reinvent security. We need to layer agentic security on top of effective security that’s already in place.” The key design principle is to keep the authorization channel separate from the agent’s channel: “Tell an agent to do really well on an exam, and the easiest way is to steal the answers.”

Taylor also argued that CI/CD and DevSecOps pipelines are now an identity attack surface, and deserve the same controls as admin access to a production server.

Delegation: “Agents Cannot Give What They Don’t Get”

When agents spawn sub-agents or hand off tasks, Agent ID intercepts at tool-execution time and enforces an inherited permission model:

“An agent can only enable another agent with the entitlements it was granted. It cannot leverage another agent’s permissions. We would see that at runtime and say: who’s asking you to do that task? He doesn’t have those permissions. Denied.”

That closes a privilege-escalation path through delegation chains, a growing concern as multi-agent orchestration spreads.

The 30-Day Pilot: Three Questions

For a CISO evaluating Agent ID, Taylor starts with three questions:

What agents are running in your environment? Not your AI initiatives, but the agents actually running.

Who owns them? Not who created them, but which human is responsible.

Can you kill them? If an agent misbehaves, would you even know?

“Most CIOs and CISOs can’t answer those,” he said. His recommended pilot is to connect a few key systems and run Discovery. “They’re usually surprised by what comes back. That gives them the internal ammunition to start assigning agents to people and building policy.”

Availability

RSA Agent ID Discover and Secure will be generally available November 16, 2026, with Govern following in the first half of 2027.

Key Takeaways

Agents are identities, not service accounts. They are dynamic, accumulate permissions, and usually lack an owner.

Shadow AI is already widespread. One bank with a “no agents” policy had more than 4,000.

Enforcement happens at the tool call. An inline AI/MCP Gateway allows, denies, or escalates every call.

Human assurance replaces approval spam. Only risk-scored, high-risk actions reach a human, out of band.

Delegated permissions are inherited, never expanded.

Before granting more autonomy, make sure you can discover, authorize, limit, and kill your agents.

The post One Bad Prompt Took Down a Company’s Salesforce: RSA’s Jim Taylor on Agent ID and Taming the 4,000 Shadow AI Agents Hiding in Your Enterprise appeared first on MarkTechPost.