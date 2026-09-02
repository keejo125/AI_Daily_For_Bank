---
publish_time: 1788334698
link: https://www.marktechpost.com/2026/09/02/anthropic-enterprise-frontier-safeguards-efs/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Anthropic 发布企业级前沿防护架构 Enterprise Frontier Safeguards（EFS），试图同时满足受监管客户的零数据留存（ZDR）隐私需求与跨会话滥用检测需求。EFS 将监控数据存储在客户自有云账户（密钥、审计、人工复核归客户），检测能力留在 Anthropic；目前分阶段推出，此前已与百余家金融、医疗、制造企业及 AWS、谷歌云、微软 Azure 共建。EFS 与同日发布的 Claude Fable 5.1/Mythos 5.1 配套，Fable 5.1 缓存读取降价 75% 至每百万 token 0.25 美元。
---

# Anthropic 发布企业级前沿防护 EFS：零数据留存隐私与跨会话滥用检测

> 原文链接：https://www.marktechpost.com/2026/09/02/anthropic-enterprise-frontier-safeguards-efs/
> 来源：MarkTechPost

Enterprise AI buyers have been stuck between two things they both need. Regulated teams need a zero data retention (ZDR) guarantee, so no prompt or agent transcript sits on a vendor&#8217;s servers. Security teams need misuse detection, which historically required the vendor to hold that same data long enough to correlate it.

This week, Anthropic announced Enterprise Frontier Safeguards (EFS), an architecture that tries to give both. EFS stores monitoring data in cloud infrastructure the customer controls, not Anthropic&#8217;s. Detection stays with Anthropic. Custody, keys, and human review stay with the customer.

Is it deployable today? Not yet. EFS rolls out in phases with the goal of broad availability later this fall, and access is request-based. Until it ships, eligible customers can run Claude Fable 5 and Fable 5.1 under ZDR.

The technical problem EFS is solving

Anthropic&#8217;s stated reason for retention is detection quality, not training data. The company introduced 30-day data retention starting with Fable 5, and says plainly that it has never trained on enterprise data without explicit permission.

The argument for holding data is narrow and worth restating. The most sophisticated misuse Anthropic has observed spreads across many tasks, sessions, and accounts, including cases involving stolen or misappropriated enterprise credentials. Running an automated classifier on each interaction and instantly discarding it cannot catch that shape of attack. Correlation needs a window. Anthropic has documented this pattern in its own espionage disruption work.

Regulated customers understood the security logic and still could not adopt it. So Anthropic moved the window rather than removing it.

What EFS actually changes

Anthropic built EFS with more than 100 customers across financial services, healthcare, manufacturing, telecom, law, retail, and the public sector, together with AWS, Google Cloud, and Microsoft Azure. Contributors included the Analysis and Resilience Center for Systemic Risk, whose membership includes CISOs at Goldman Sachs, Morgan Stanley, Citi, Bank of America, and Wells Fargo, plus teams at Comcast, KPMG, Mastercard, Salesforce, and Visa. Anthropic says the design conversations covered a quarter of the Fortune 100 and every US global systemically important bank.

Three design decisions came out of that process:

Storage moves to the customer: Activity data used for monitoring can live in the customer&#8217;s own cloud account, under their encryption keys, access policies, and audit logging. Enterprises told Anthropic that onboarding another trusted data vendor triggers customer notifications and contract updates, so the architecture avoids creating one.

Review moves to the customer: When monitoring detects a pattern worth attention, the signal goes directly to the customer. Anthropic&#8217;s position is that automated review handles the scan; a person still adds value confirming real misuse and clearing false positives, and in regulated environments that person must be cleared for privileged legal material, non-public information, or drug-safety reports. EFS runs automated safety monitoring with no Anthropic human review required.

Detection stays with Anthropic: Automated systems analyze a rolling window of traffic for serious misuse, specifically attempts to build offensive cyber or biological capability and signs of stolen or leaked credentials. 

Where this sits in the model roadmap

EFS is one of three enterprise concessions shipped alongside Claude Fable 5.1 and Mythos 5.1. The other two are pricing and precision. Fable 5.1 cut cache reads by 75% to $0.25 per million tokens, which works out to roughly 25% lower cost on typical workloads and up to about 45% on highly agentic ones. Its cybersecurity safeguards now produce around 60% fewer interventions per Claude Code session than Fable 5&#8217;s, partly because Fable 5.1 is permitted to identify software vulnerabilities without developing exploits for them.

Key Takeaways

EFS pairs ZDR-equivalent privacy with automated detection that spans sessions and accounts.

Activity data lands in the customer&#8217;s own S3, Azure Blob, or Google Cloud Storage bucket.

Flags route to the customer; no Anthropic human review is required.

Customer-owned storage, customer-managed keys, and automated review are each opt-in.

Anthropic charges nothing for EFS; the customer&#8217;s cloud provider bills storage and egress.

Check out Technical details here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Anthropic Introduces Enterprise Frontier Safeguards (EFS): Zero-Data-Retention Privacy Plus Cross-Session Misuse Detection appeared first on MarkTechPost.