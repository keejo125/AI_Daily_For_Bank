---
publish_time: 1792927949
link: https://www.marktechpost.com/2026/10/25/anthropic-launches-oss-scanner-a-free-ai-vulnerability-scanner/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Anthropic 于 10 月 8 日推出 OSS Scanner，一项面向关键开源项目的免费、可选漏洞扫描服务。该工具用公司最强模型（含 Claude Mythos）对注册代码库做审计，结果直接发给维护者、不经人工复核，以更快发现漏洞，但把分诊压力转嫁给项目方。截至 10 月 19 日，已从约 650 份申请中接收 114 个项目，在隔离 VM 中运行、无外网。上线 11 天即报出 77 个严重、803 个高危模型评级漏洞；已审计的 97 个关键/高危发现中 88% 达到披露门槛，仅 1 个误报。设计借鉴 Google OSS-Fuzz，以语言模型替代模糊测试器，每个报告含可复现步骤、根因分析与候选补丁。
---

# Anthropic 推出 OSS Scanner 免费 AI 漏洞扫描器

> 原文链接：https://www.marktechpost.com/2026/10/25/anthropic-launches-oss-scanner-a-free-ai-vulnerability-scanner/
> 来源：MarkTechPost

Anthropic has launched OSS Scanner, a free, opt-in vulnerability scanner for critical open-source projects. The Anthropic OSS Scanner runs the company&#8217;s strongest models, including Claude Mythos, against enrolled codebases. Reports go straight to maintainers without human review. That trade delivers faster findings, but shifts triage work onto project teams. 11 days after the October 8 launch, Anthropic reported 77 critical and 803 high model-rated findings.

TL;DR

Scale: 114 projects accepted from about 650 applications, as of October 19.

Runs on: Anthropic&#8217;s infrastructure, free. Maintainers supply a Dockerfile; audits run in an isolated VM with no Internet.

Performance: 85 of 97 audited critical and high findings (88%) met Anthropic&#8217;s disclosure bar.

Best: Only 1 of 97 audited findings was a false positive. wolfSSL says 72 of 74 reports were valid.

Worst: No human review before delivery. 11 of 97 audited findings duplicated known issues; maintainers report inflated severity.

What is Anthropic OSS Scanner?

OSS Scanner is a free application from Anthropic that periodically audits open-source repositories with its strongest models. The Frontier Red Team and Safeguards Research team run it together. The design borrows from Google&#8217;s OSS-Fuzz, but swaps fuzzers for language models.

The main goal is a review bottleneck. Over 6 months, Anthropic&#8217;s models surfaced over 29,000 candidate vulnerabilities. Human reviewers triaged roughly 6,000 of them. Nearly 5,000 more reports went directly to maintainers who asked for everything, validated or not. OSS Scanner turns that ad hoc request into an opt-in program.

How does OSS Scanner work?

Core maintainers enroll by opening a pull request on anthropics/oss-scanner. The PR adds projects/<project>/project.yaml, based on the project template.

Required fields: repo, primary_contact, and a Dockerfile path.

Optional fields: threat_model, pgp for encrypted reports, auto_ccs, homepage, and disabled.

The Dockerfile builds the project with network access. The VM then moves to a network without Internet for the audit. Agents in the pipeline double-check bugs, run root cause analysis and propose patches.

Each report contains a self-contained reproducer and an explanation of the bug. Where possible, it includes a bisection to the commit that introduced it. A candidate patch is attached when available.

An optional threat_model.md defines adversarial inputs, out-of-scope code and a severity rubric. Without it, the scanner guesses.

How accurate are OSS Scanner reports?

Anthropic team asked its penetration testers to check 97 critical and high findings across 48 projects.

85 (88%) met the bar for Anthropic&#8217;s coordinated vulnerability disclosure (CVD) process.

11 were real but duplicated known issues or other scan findings.

1 was invalid.

Maintainer data points in the same direction. wolfSSL received 74 reports; all but 2 were valid, and 5 became CVEs. curl patched CVE-2026-92392, a High-severity HTTP/2 upload use-after-free. It affects curl 8.12.0 to 8.22.0 and is fixed in 8.23.0, released October 14, 2026.

Anthropic links the timing to benchmark progress. On CyberGym, LLMs went from finding under 20% of vulnerabilities to over 85%. Its broader CVD dashboard lists 6,157 disclosed vulnerabilities across 591 projects, as of October 2. 516 of those are patched.

&&

OSS Scanner vs other open-source security programs

FeatureAnthropic OSS ScannerGoogle OSS-FuzzOpenAI Codex for OSSGoogle DeepMind CodeMenderApproachLLM agents (Claude Mythos and others) audit sourceFuzzing: libFuzzer, AFL++, Honggfuzz plus sanitizersCodex Security agent, run by approved maintainersGemini Deep Think agent finds and patches bugsCost to maintainersFree; Anthropic covers full costFreeApproved maintainers get ChatGPT Pro, API credits, conditional Codex Security accessNot disclosedEnrollmentPR with project.yaml and DockerfilePR with project files to google/oss-fuzzApplication, reviewed by OpenAINot disclosed (research project)Human review before maintainer sees itNoNot disclosedMaintainer runs and reviews scansYes, every patch before upstreamReport contentsReproducer, explanation, bisection, candidate patchCrash reports with reproducersFindings with validation and patchesPatches submitted upstreamDisclosure deadlineNone on unvalidated findings90 days or fix release, plus 14-day graceNot disclosedNot disclosedPublished track record77 critical + 803 high model-rated findings in 11 days13,000+ vulnerabilities, 50,000 bugs, 1,000 projects (May 2025)14 CVEs in OSS projects72 security fixes upstreamed (Oct 2025)Precision data88% of 97 audited critical/high validNot disclosedFalse positives cut by 50%+ in betaNot disclosed

Sources: OSS-Fuzz disclosure guidelines, OpenAI Codex Security, DeepMind CodeMender.

Key Takeaways

OSS Scanner gives critical open-source projects free Claude Mythos audits.

Reports skip human review; 88% of 97 audited critical/high findings were valid.

First 11 days: 77 critical and 803 high model-rated findings.

Enrollment is a PR with a Dockerfile; audits run offline.

No 90-day deadline applies to unvalidated findings.

Check out the launch post, the OSS Scanner FAQ and the GitHub repo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Anthropic Launches OSS Scanner, a Free AI Vulnerability Scanner appeared first on MarkTechPost.