---
publish_time: 1793381655
link: https://www.marktechpost.com/2026/10/30/ai-security-agents-claude-codex-mantis-cloudflare/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Anthropic、OpenAI、Cloudflare 与 Google 相继推出自动发现代码安全漏洞的 AI Agent。文章对比四家实现，指出它们收敛于同一设计范式：一个 Agent 负责发现漏洞，另一个独立 Agent 负责证伪，仅通过验证的漏洞才生成补丁。差异主要体现在运行位置、使用者与验证强度。Google 安全团队称粗糙的 AI 代码扫描会产生大量幻觉漏洞、真阳性率不足 7%，分离职责（发现者永不兼验证者）是四家的共同解法。Cloudflare 的 skill 采用 MIT 协议、模型无关，星标最高（47.5K）。
---

# AI 安全智能体横评：Claude、Codex、Mantis 与 Cloudflare 殊途同归

> 原文链接：https://www.marktechpost.com/2026/10/30/ai-security-agents-claude-codex-mantis-cloudflare/
> 来源：MarkTechPost

Anthropic, OpenAI, Cloudflare and Google now each ship an AI agent that hunts security bugs in source code. We checked the repos, docs and technical details behind each one.

The key finding: all 4 tools converge on one design. One agent finds a bug, a separate agent tries to disprove it, and only survivors get a patch. The differences are in where they run, who can use them and how much proof they demand.

Key Takeaways

4 labs, 1 pattern: find, independently disprove, then patch.

Claude Security runs inside Claude Code; no extra API key needed.

Codex Security&#8217;s CLI is Apache-2.0, but scanning still needs OpenAI access.

Cloudflare&#8217;s skill is MIT, model-agnostic and the most-starred at 47.5K.

Google&#8217;s Mantis reproduces bugs in a sandbox; Google says isolate it.

Why 4 labs shipped the same thing in 2026

The problem every one of them is solving is noise. Google&#8217;s security team writes that sloppy AI code scanning produces hallucinated bugs and true-positive rates under 7%. A scanner that is wrong 93% of the time costs reviewers more than it saves.

The shared fix is separation of duties. The agent that reports a finding never gets to confirm it. Cloudflare states the rule directly in its README: the verifier is never the agent that found the bug. Anthropic, OpenAI and Google each describe a similar validation step before anything reaches a report.

The second driver is offense. Anthropic team states that it built its scanner partly because attackers were already using AI models to find exploitable flaws, per The Hacker News. Google opens its Mantis post by noting that models can now discover and exploit bugs with little human help.

1. Claude Security by Anthropic

What it is: A multi-agent vulnerability scanner that runs inside a Claude Code session. It is the local version of Anthropic&#8217;s hosted Claude Security product, per the plugin README.

How it works: Agents map the architecture, build a threat model, hunt across every component and verify each finding independently. The plugin offers 3 jobs from one menu: scan the codebase, scan changes, or suggest patches, per Claude Code docs.

Output: A Markdown report along with a SARIF 2.1.0 file for GitHub code scanning. Each finding carries severity, a CWE category, impact and reproduction steps. Patches are drafted in a scratch copy and land as F<n>.patch files. The plugin never commits, pushes or opens a pull request on its own.

Cost and access: It makes no model calls of its own, so there is no separate API key. Scans count against your Claude plan&#8217;s usage limits.

Copy CodeCopiedUse a different Browser

/plugin install claude-security@claude-plugins-official
/claude-security

Timeline: Anthropic opened a limited preview called Claude Code Security in February 2026. The hosted product reached public beta for Enterprise customers on Claude Opus 4.7. The Claude Code plugin entered beta on July 22, 2026, per Cybersecurity News. In August, the hosted scanner moved to Claude Mythos 5, per Dataconomy.

Where it fits: Anthropic positions it as one layer. The security-guidance plugin checks code as Claude writes it, and /security-review does a single pass on a branch. Claude Security is the on-demand deep scan.

2. Codex Security by OpenAI

What it is: A CLI and TypeScript SDK, published as @openai/codex-security, for finding, validating and fixing vulnerabilities. 

How it works: It scans a whole repo, selected paths, or a Git diff. A &#8211;mode deep flag runs parallel discovery workers. It validates candidate findings, generates patches and can verify existing fixes. A cs policy command drafts a SECURITY.md that tells future scans what counts as a vulnerability in your project.

Output: Threat models, SARIF, JSON or CSV exports, plus publishing to Linear. It can import GitHub code-scanning alerts and suggest owners from Git history. A GitHub Action runs scheduled or pull-request scans; findings are report-only by default.

Copy CodeCopiedUse a different Browser

npm install --global @openai/codex-security
cs login
cs scan 

Cost and access: The client is Apache-2.0, but the scanner behind it is not. DevOps.com notes the CLI and SDK stay in limited beta for approved customers. The README lists OpenAI, Amazon Bedrock, OpenRouter and Fireworks AI as providers. Requires Node.js 22.13+ and Python 3.10+.

3. Security Audit Skill by Cloudflare

What it is: An MIT-licensed skill that turns any capable coding agent into a security auditor. 

How it works: A 6-phase audit:

Reconnaissance: map architecture, trust boundaries and input surfaces into architecture.md and a coverage ledger.

Coverage-led hunting: isolated hunters each take ledger units; coverage critics look for gaps.

Candidate validation: a fresh verifier tries to disprove every unique candidate.

Structured output: confirmed, needs_validation and rejected records go to findings.json, checked against a schema.

Independent record verification: new agents re-verify every final source claim.

Target-neutral reporting: REPORT.md and detail files are derived from the verified records.

Requirements: A coding agent that supports tool use and parallel sub-agents, plus Node.js for the validators. It also wants an OS-enforced sandbox with no external network. Without one, leads stay needs_validation instead of being executed.

npx skills add https://github.com/cloudflare/security-audit-skill &#8211;skill security-audit

Then ask the agent: &#8220;security audit this codebase.&#8221; Output defaults to ~/security-audit-skill/<repo-name>/run-<N>, outside your repo.

The data behind it: Cloudflare published the skill on June 18, 2026, with its post Build your own vulnerability harness. The roughly 450-line skill seeded an internal harness that now scans 128 repos. Cloudflare reports these lifetime numbers:

20,799 raw candidates from discovery, about 12,057 of which survived validation.

13,841 findings in the shared triage pool across 145 repos, including another harness&#8217;s output.

5,442 folded away as duplicates and 1,154 routed out as wrong-repo or low-risk.

7,245 actionable findings sent to engineering teams.

Better recon context cut the first-pass rejection rate from 40% to 11%. Cloudflare also uses one model for discovery and a different model for triage, so models check each other.

4. Mantis by Google

What it is: An Apache-2.0 set of security-review skills plus an ADK reference harness for AI coding agents. Google team states that it is part of how it finds and fixes bugs internally.

How it works: Mantis reads the repo&#8217;s history to learn from past security fixes. It builds a hierarchical summary tree, condensing files into directory and root summaries. Google team states that this cut token overhead by over 85%. It then generates a threat model and hypotheses, hunts, deduplicates and critiques findings.

What sets it apart: Reproduction and patch verification. Mantis tries to reproduce each bug, from a static exploit sketch up to a unit test or mock server. It patches with an adversarial loop that attacks the fix. It also calibrates severity against a rubric to stop &#8220;thousands of criticals.&#8221; A mantis-advise skill then feeds what it learned back into code generation.

Setup: Clone the repo and point any coding agent at it, or run the ADK harness directly. The harness supports a &#8211;focus prompt such as &#8220;look for IDOR&#8221; and a &#8211;max-tokens spend ceiling.

Copy CodeCopiedUse a different Browser

git clone https://github.com/google/mantis.git
cd mantis/reference && ./install.sh
./run.sh path/to/code

Side-by-side

ToolLicenseRuns whereModel lock-inProof stepPatchesSecurity Audit Skill (Cloudflare)MITAny coding agent with parallel sub-agentsNoneFresh agent disproves; second independent verificationNoCodex Security (OpenAI)Apache-2.0 client; hosted scannerCLI, SDK, GitHub ActionOpenAI-gated; Bedrock, OpenRouter, Fireworks supportedValidates candidates; verifies fixesYesMantis (Google)Apache-2.0Any coding agent or ADK harness, isolated envNoneSandboxed reproduction; adversarial patch loopYesClaude Security (Anthropic)Plugin in Anthropic&#8217;s official marketplaceClaude Code sessionClaude modelsIndependent verifier panelYes, as .patch files

Beyond the big 4: other AI bug hunters launched in 2026

At least 12 more agent-based vulnerability tools shipped or went public in 2026. Almost all repeat the same find-then-independently-verify loop. They split into free harnesses you run yourself and commercial or internal platforms.

Open-source harnesses

ToolFromReleasedWhat stands outVisa Vulnerability Agentic Harness (VVAH)VisaJun 10, 2026Built after testing Claude Mythos Preview via Project Glasswing. A 4-phase, 11-stage pipeline with policy gates and human review; works with Claude or OpenAI-compatible models. Remediation and fix validation added later.OpenHackHadrianMay 25, 2026MIT. Runs inside Claude Code, Codex or Cursor with all state kept in plain files. Expert agents prove or reject scenarios; an independent triage agent picks final findings.deepsecVercel LabsMay 4, 2026MIT. A regex prefilter picks security-sensitive files, agents investigate, a second pass revalidates. Vercel fans scans out to 1,000+ concurrent sandboxes.

AppSec Santa also tracks harnesses from Anthropic (defending-code-reference-harness), Trail of Bits, Capital One (vulnhunter) and Cisco (ai-deep-sast). Cisco&#8217;s runs fully local on Foundation-Sec-8B, so no code leaves the machine.

Commercial platforms and internal systems

ToolFromLaunchedStatusWhat stands outSignal Agentic FixBlack DuckOct 28, 2026LaunchedScan, triage, fix, validate, submit. Works alongside coding agents such as Claude Code; every change goes to a human.Continuum for code vulnerabilitiesAWSGA Oct 22, 2026 (preview Jun 17)GA in 2 US regionsChecks exploitability against your actual AWS setup and opens fix pull requests. Absorbed the former AWS Security Agent. Every fix needs human approval.Evo Agentic AppSecSnykOct 15, 2026PreviewAgents drive Snyk&#8217;s deterministic engines as tools. Snyk&#8217;s own VulnBench found 49.7% of LLM-only review findings vanish on the next run.PageBreakGoogle Product SecurityDisclosed Sep 24, 2026Internal only500+ verified XSS bugs in Google&#8217;s own web apps. Separate, non-AI validators fire each exploit at a running app before anyone sees it.Agentic WorkflowsSemgrepJul 28, 2026Public beta9 prebuilt workflows covering 70+ CWEs. Pairs deterministic taint analysis with frontier models such as Claude Opus.Patch the PlanetOpenAI + Trail of BitsJun 22, 2026ProgramEngineers using Codex Security and GPT-5.5-Cyber across 19 open-source projects. First week: 64 PRs and 51 issues.MDASHMicrosoftMay 12, 2026Expanded preview100+ agents on an ensemble of models. Found 16 new Windows bugs, 4 of them critical RCEs.Red AgentWizRSA 2026; preview Apr 22GAAttacks live APIs and apps from outside rather than reading source. Runs on Claude Opus among other models.Xint CodeTheoriDisclosed Apr 29, 2026CommercialFound &#8220;Copy Fail&#8221; (CVE-2026-31431), a 9-year-old Linux root bug, in about 1 hour of scanning. CISA added it to its exploited-vulnerabilities list.

The pattern holds across vendors: deterministic engines or validators do the proving, models do the reasoning, and a human approves every fix.

Which one to run first

Already on Claude Code: start with the Claude Security plugin. It installs in 1 line and uses your existing plan.

Need CI gating and SARIF in GitHub: Codex Security has the most mature pipeline tooling, if your org has access.

Want no vendor lock-in: Cloudflare&#8217;s skill runs on any agent with parallel sub-agents and is fully MIT.

Have a security team and a sandbox: Mantis gives the deepest proof loop, with reproduction and adversarial patch testing.

Cloudflare&#8217;s own architecture suggests a practical combination. Run discovery with one tool or model, then validate with a different one. Different models surface different shares of the bugs.

The post AI Security Agents Compared: Claude, Codex, Mantis, Cloudflare appeared first on MarkTechPost.