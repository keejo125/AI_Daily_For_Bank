---
publish_time: 1791699621
link: https://www.marktechpost.com/2026/10/10/orcarouter-releases-orcacyber-zero-1-5-cybersecurity-model-with-1m-context/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  OrcaRouter发布网络安全模型OrcaCyber Zero 1.5，是9月17日Zero 1.0的后继版本，专门用于授权漏洞研究。该模型基于Orca后训练，面向漏洞复现、漏洞利用开发、渗透测试、安全审计与网络推理，配备1M Token上下文、原生函数调用与结构化输出（128K最大输出）。厂商自报成绩：Cybench 39/39任务满分、SWE-bench Pro V2为76.5%（最低），定价每百万Token输入3美元、输出7.5美元。仅通过OrcaRouter托管API提供，不开放权重。对安全团队意味着“更少报告、更多已验证并修复的漏洞”，属于面向红队/授权安全工程的专用前沿模型。
---

# 网络安全模型 OrcaCyber Zero 1.5 发布（1M 上下文）

> 原文链接：https://www.marktechpost.com/2026/10/10/orcarouter-releases-orcacyber-zero-1-5-cybersecurity-model-with-1m-context/
> 来源：MarkTechPost

OrcaRouter has released OrcaCyber Zero 1.5, a model for authorized vulnerability research. The model is the successor to OrcaCyber Zero 1.0, which shipped on September 17, 2026. OrcaCyber Zero 1.5 is a post-trained Orca model for vulnerability reproduction, exploit development and penetration testing. It ships with a 1M-token context window, native function calling and structured outputs. For security teams, this model brings a simple message: fewer reports, more validated and fixed vulnerabilities.

TL;DR

Size: Parameter count not disclosed. 1M-token context, 128K max output, text in and text out.

Runs on: Hosted API only through OrcaRouter. No weights, no quantized variants, hardware not disclosed.

Performance: Vendor-reported scores are near ceiling on cyber benchmarks and strong on coding.

Best: 100% on Cybench (39/39 tasks, unrestricted agent execution).

Worst: 76.5% on SWE-bench Pro V2, its lowest published score.

Bottom line (best): Top-tier cyber scores at $3.00 / $7.50 per 1M tokens.

Bottom line (worst): Every number is self-reported, and CVE-Bench used only 24 evaluable tasks.

What is OrcaCyber Zero 1.5?

OrcaCyber Zero 1.5 is a frontier cybersecurity model and the successor to Zero 1.0. Orca team states that it has post-trained for security research and authorized security engineering. Listed uses include vulnerability reproduction, exploit development, penetration testing, security auditing and cyber reasoning.

The 3 design goals:

Find what others miss: unknown flaws like RCE, sandbox escapes, auth bypasses, privilege escalation and attack chains.

Go beyond detection: reason through attack paths, challenge its own hypotheses and rank flaws by demonstrable exploitability.

Built for autonomous agents: 1M-token context, native tool calling and extended reasoning for large codebases.

How does OrcaCyber Zero 1.5 perform on benchmarks?

The model page lists 4 vendor-reported results, last evaluated October 10, 2026:

Cybench: 100% (39/39, unrestricted agent execution).

CVE-Bench: 95.8% (23/24 evaluable tasks).

HumanEval+: 93.9%.

SWE-bench Pro V2: 76.5%.

Cybench contains 40 professional CTF tasks, so the 100% covers 39 of them. CVE-Bench is built on 40 critical-severity web CVEs. Orca&#8217;s 95.8% covers a 24-task evaluable subset. The SWE-bench Pro V2 score is not directly comparable with standard SWE-bench Pro results.

&&

How does it compare with other cyber models?

FeatureOrcaCyber Zero 1.5OrcaCyber Zero 1.0Claude Mythos PreviewGPT-5.5-CyberSakana Fugu-CyberDeveloperOrca (OrcaRouter)Orca (OrcaRouter)AnthropicOpenAISakana AIReleaseOct 10, 2026Sep 17, 2026Apr 7, 2026Jun 22, 2026 (full)Jul 21, 2026TypePost-trained modelPost-trained coding modelGeneral frontier modelCyber-tuned GPT-5.5Multi-agent orchestrationParametersNot disclosedNot disclosedNot disclosedNot disclosedNot disclosedContext1M1MNot disclosedNot disclosedNot disclosedCyberGymNot disclosed98.07% (harness, pass@1)83.1%85.6%86.9%Other headline scoreCybench 100%Not disclosedSWE-bench Pro 77.8%Not disclosedCTI-REALM 72.1%Price (in / out per 1M)$3.00 / $7.50$3.00 / $7.50$25 / $125 after creditsNot disclosedNot disclosedAccessGated Security Research tierGated, closed betaGlasswing partnersVetted defenders onlyApplication review

All competitor figures come from each vendor&#8217;s own announcement. None are independent replications.

How do developers access OrcaCyber Zero 1.5?

The model uses an OpenAI-compatible API. Developers set base_url to https://api.orcarouter.ai/v1 and call orca/orcacyber-zero-1.5.

Access is gated to the Security Research tier. Orca lists an engagement, a passkey and accepted terms as requirements. The tier targets trusted security researchers, red teams and authorized testing.

Pricing is $3.00 per 1M input tokens and $7.50 per 1M output tokens. Cache reads cost $0.75 per 1M tokens. Over the past 7 days, p50 time-to-first-token was 500 ms and p95 was 2.36 s. That sample is small, at 1.3K tokens of traffic.

Zero 1.0 recorded a 3.43 s p50 over a much larger traffic window. The 2 latency figures are not a clean comparison.

Key Takeaways

OrcaCyber Zero 1.5 is a gated, 1M-context cybersecurity model on OrcaRouter.

It reports 100% on Cybench and 95.8% on a 24-task CVE-Bench subset.

Pricing is $3.00 / $7.50 per 1M tokens, far below Mythos Preview&#8217;s $25 / $125.

The 98% CyberGym claim belongs to Zero 1.0 inside Orca&#8217;s harness.

All results are vendor-reported, with no technical report yet.

Check out the model page, the launch post on X and the OrcaRouter docs. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post OrcaRouter Releases OrcaCyber Zero 1.5 Cybersecurity Model With 1M Context appeared first on MarkTechPost.