---
publish_time: 1791011111
link: https://www.marktechpost.com/2026/10/03/meta-openai-and-uber-just-taught-ai-agents-to-talk-first-what-about-when-to-stay-quiet/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Meta Muse、OpenAI Dots 与 Uber 司机助手近期不约而同地让智能体“先开口”：从被动应答转为主动推送。Muse 可在 App 关闭时持续工作并主动建议；Dots 做只读监控，在 Slack/Teams 捕获遗漏的发票或 Bug；Uber 助手把实时供需信号转为接单建议。文章指出，主动式 Agent 的真正难题从“回答什么”转向“何时打断、走哪个渠道、给什么 offer”，需借助经典 ML 与决策模型平衡打扰与时效。
---

# Meta、OpenAI 与 Uber 让智能体先开口：何时该沉默成新难题

> 原文链接：https://www.marktechpost.com/2026/10/03/meta-openai-and-uber-just-taught-ai-agents-to-talk-first-what-about-when-to-stay-quiet/
> 来源：MarkTechPost

TL;DR: Meta&#8217;s Muse, OpenAI&#8217;s Dots and Uber&#8217;s driver assistant share one bet: the agent speaks first. That moves the hard problem from what to answer to when to interrupt, on which channel, and with what offer. Classic ML and new decision models can solve it.

Three launches, one pattern

Meta Muse (Sept 8). A personal agent that books, emails and keeps working with the app closed. It remembers details, makes unprompted suggestions and checks in for approval, in its own app and in WhatsApp.

OpenAI Dots (Sept 29). Always-on agents that run &#8220;proactive research,&#8221; read-only monitoring of your apps, to catch a forgotten invoice or a bug in Slack. They reach you in ChatGPT, Slack and Teams, with text and voice coming.

Uber&#8217;s driver assistant. It turns live marketplace signals into advice. In a recent talk, Uber&#8217;s product team described a driver idle for 33 minutes being pointed to a better zone, with evidence. Their principles: stay &#8220;always on the driver&#8217;s side,&#8221; surface opportunities proactively, and measure whether drivers acted. A hands-free voice version was announced Sept 24.

From pull to push

Chatbots were a pull interface: the user chose the moment, the channel and the question. Proactive agents invert that. Interrupt too often and users mute you. Interrupt too late and the surge has ended or the invoice is overdue. Pick the wrong channel and a good message fails. The LLM can write the message; it is the wrong tool to decide whether to send it.

The rule: value must beat interruption cost

Every proactive message is a bet. Send only when its expected value to the user exceeds the cost of interrupting them. Value has four parts: how much is at stake, how likely the user is to act, how fast the opportunity expires, and whose value it is, the user&#8217;s or the platform&#8217;s.

Value then sets both decisions. High-value, expiring messages go now; modest ones wait for a digest; the rest are never sent. And the more a message is worth, the more intrusive a channel it has earned.

&#8220;When&#8221; and &#8220;how&#8221; are prediction problems

Notification and growth teams have solved versions of this for years:

Uplift models estimate whether a nudge causes the action.

Contextual bandits learn the best moment and channel for each user.

Receptivity models predict whether the user can engage right now: driving or parked, in a meeting or free.

Channels have a price of admission. An in-app card costs little, chat costs more, SMS more still, and a voice call is reserved for urgent, hands-busy moments. Uber&#8217;s outcome tracking supplies the labels these models need.

Where decision models fit

A new model class suits this job. Decision models such as TypeSafe&#8217;s Jev and the open-weights Julia 1 from Supersonic Labs return no text, only a typed judgment: a choice from a short list, a score, or a yes/no, each with a probability. Julia 1 runs on a CPU, from about 33 ms per decision.

An always-on agent evaluates far more triggers than it sends, so each candidate can get cheap, structured questions before any LLM call: Is this worth an interruption? How valuable, how urgent? Send now, wait, batch or drop? Card, chat, SMS or voice?

The limits matter. These models judge only the context they are given, so they will not learn that one user ignores mornings;

Cross-sell, carefully.

An agent that speaks first is a powerful distribution channel. Meta says it is exploring commerce in Muse and has already launched Muse for Small Business; OpenAI announced Dots alongside a new $500 monthly tier; Uber has delivery and other services to promote. But an offer is just another message. It must clear the same bar, measured on value to the user. Once users suspect the agent is selling instead of serving, every message loses credibility.

The takeaway

All three companies have strong models. The race will be won on judgment about attention: speaking rarely, at the right moment, in the right place, on the user&#8217;s side. Companies with years of notification data may have a head start.

The post Meta, OpenAI and Uber Just Taught AI Agents to Talk First. What About When to Stay Quiet? appeared first on MarkTechPost.