---
publish_time: 1789802536
link: https://www.marktechpost.com/2026/09/19/meta-launches-muse-for-mac/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Meta 发布 Muse for Mac，这是 Muse 首个能在用户电脑上「真正完成事情」的版本：它接入本地文件与原生应用，跨文件、邮件、信息、日历与备忘录工作，为九月初登陆 iOS/Android/网页/WhatsApp 的托管消费级智能体补上桌面层。该应用由扎克伯格与首席 AI 官 Alexandr Wang 同日宣布，免费向美国用户开放 macOS 下载，但并非可自托管的开源模型，数据仍走 Meta 托管。
---

# Meta 发布 Muse for Mac：跨文件/邮件/日历的个人 AI 智能体

> 原文链接：https://www.marktechpost.com/2026/09/19/meta-launches-muse-for-mac/
> 来源：MarkTechPost

Meta has released Muse for Mac, the first version of Muse that can complete things on a user&#8217;s computer. The agent works with local files and native apps, where your data already lives. It adds a desktop layer to an agent that launched on phones, the web and WhatsApp earlier this month.

Is it deployable? Yes, for end users. It is a free macOS download today, only available in the US for now. It is a hosted consumer agent, not an open model you can self-host.

What Meta Shipped

Mark Zuckerberg announced the Mac app on X, noting that it works across apps, files, calendar, notes, and messages. His post added, &#8220;The team is shipping fast.&#8221; Meta&#8217;s Chief AI Officer Alexandr Wang also announced the launch the same day.

Muse itself is not new this week. Muse launched on September 8th in the US across iOS, Android, the web and WhatsApp. According to TechCrunch, it quickly rose to the top of the U.S. App Store charts after that launch.

Muse for Mac is out today! It works across apps, files, calendar, notes, and messages on your computer. You control what it can access. The team is shipping fast. Download at https://t.co/BX3oX19Zcl
&mdash; Mark Zuckerberg (@finkd) September 17, 2026

What Muse for Mac Can Do

On the Mac, Muse can interact with your files, messages, calendar, notes and mail, all within their native applications. Meta frames it around everyday tasks that span several apps. You can ask it to organize folders, finish a form using information stored in your files, or build an end-of-day summary from emails, messages, and notes.

The practical shift is context gathering. A normal chatbot needs you to copy and paste information into a prompt. Muse can potentially collate different pieces of context across the computer. One task might touch a Calendar event, a Mail thread, a document in a folder and a Messages conversation.

Muse also runs asynchronously. Meta noted that the agent continues working in the background even when the desktop window is closed. You can start something on your phone, check in from your laptop or nudge it through WhatsApp, with Muse keeping the thread across devices.

How Permissions Work

Local access raises the stakes, so the controls matter most here. Access to your computer is opt-in, while Full Disk Access is optional. You decide what permissions Muse gets and can change them anytime through Settings.

Destructive or outbound actions are gated. Meta says sensitive actions such as deleting files or sending messages require approval. In practice, Muse can sort a folder freely but must stop before it deletes anything. It can draft a summary but must ask before sending it.

The Stack Behind Muse

Muse is powered by Muse Spark, Meta&#8217;s most capable model to date, built for real-world agentic work, per Meta&#8217;s launch post. The same model powers Muse Code, a coding agent available for MacOS and Windows.

The cloud side runs on Muse Secure VM. Muse runs on its own dedicated computer in the cloud, contained so no one else&#8217;s agent can reach it. A separate Sentinel agent runs on that same machine, kept apart from Muse at the system level. Nothing Muse does reaches the internet unless the Sentinel approves it.

There is one caveat worth stating plainly. Secure VM isolates your data from other users, but it does not prevent Meta from accessing your data when necessary to operate the service. Meta plans to introduce Muse Confidential VM later in 2026, encrypting the entire VM with a key only the user holds. Meta also runs a public bug bounty for Muse.

Interactive Explainer: How Muse for Mac Gets a Task Done

&&

Key Takeaways

Muse for Mac is Meta&#8217;s first Muse version that acts directly on your computer.

It works with Files, Mail, Messages, Calendar and Notes in their native apps.

Access is opt-in, Full Disk Access is optional, and settings can change anytime.

Deleting files or sending messages always requires your approval first.

Free up to 100M tokens per week; US only for now.

The post Meta Launches Muse for Mac: A Personal AI Agent That Works Across Your Files, Mail, Messages, Calendar and Notes appeared first on MarkTechPost.