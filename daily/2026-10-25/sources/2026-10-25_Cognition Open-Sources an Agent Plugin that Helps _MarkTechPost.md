---
publish_time: 1792897148
link: https://www.marktechpost.com/2026/10/24/cognition-devin-vulnerability-fixes-plugin-php2shell-nodejs-gitlab/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Cognition 发布 Devin Vulnerability Fixes 插件，一套免费开源的 Agent Skills（fix-php-vuln、fix-node-vuln、fix-gitlab-vuln，MIT 许可），针对近期三起严重远程代码执行（RCE）通告。该技能可在 Devin、Claude Code、Codex、Cursor、GitHub Copilot、Gemini CLI 等任意读取 SKILL.md 的编码智能体中运行。工作流为：盘点→审批→打补丁→测试→每个仓库提交一个 PR。覆盖 PHP2Shell（CVSS 9.2）、Node.js 10 月安全更新（含 Brotli 越界写 CVE-2026-111497）、以及 CVSS 10.0 的自托管 GitLab 整数溢出漏洞（CVE-2026-110264，影响 7.0 起全版本）。Cognition 将其内部 remediation 流程打包开源。
---

# Cognition 开源 Devin 漏洞修复智能体插件

> 原文链接：https://www.marktechpost.com/2026/10/24/cognition-devin-vulnerability-fixes-plugin-php2shell-nodejs-gitlab/
> 来源：MarkTechPost

Cognition has released the Devin Vulnerability Fixes plugin, a free, open-source set of agent skills. It targets three critical remote code execution (RCE) advisories. They cover PHP2Shell, the Node.js October 21, 2026 security release and a CVSS 10.0 self-managed GitLab bug. The skills run in Devin and in any coding agent that reads SKILL.md files. Cognition packaged the remediation workflow it used internally. Developers can do inventory, approve, patch, test, then ship 1 pull request per repository.

TL;DR

Size: Three skills (fix-php-vuln, fix-node-vuln, fix-gitlab-vuln), MIT license.

Runs on: Devin, Claude Code, Codex, Cursor, Factory Droid, GitHub Copilot, Gemini CLI, OpenCode and Windsurf. Needs git, a shell, Docker and registry access. The npx skills install needs Node.js 22.20 or later.

Performance: No remediation benchmark or fix-rate number is published for the plugin.

Best: Covers the week&#8217;s most severe bug, GitLab CVE-2026-110264, rated CVSS 10.0.

Worst: Validation is only as strong as your tests. Managed runtimes, appliances and Electron apps are flagged, not patched.

What is the Devin Vulnerability Fixes plugin?

The Devin Vulnerability Fixes plugin is a set of three Agent Skills from Cognition. They find and patch vulnerable PHP, Node.js and self-managed GitLab deployments. The source is on GitHub under the MIT license. Cognition&#8217;s product page lists it as free and open source.

Which vulnerabilities does it fix?

PHP2Shell (CVE-2026-109618, CVE-2026-109619): PHP rates both flaws CVSS v4.0 9.2. The first corrupts memory after an out-of-memory condition. The second lets stale global state from one request reach the next. PHP says every web-serving setup is at risk, with mod_php rated highest risk. Fixed versions are 8.2.35, 8.3.36, 8.4.27 and 8.5.12. PHP 8.1 and older get no releases, only source backports for 7.4, 8.0 and 8.1.

Node.js October 2026 release: It fixes 10 CVEs, 4 rated High. The lead bug, CVE-2026-111497, is a Brotli decoder out-of-bounds write that can enable RCE. Fixed versions are 22.23.4, 24.22.1 and 26.12.1. Node.js 20 and older are end-of-life and get no fix.

GitLab CVE-2026-110264: An integer overflow in the regular expression compiler allows unauthenticated code execution. It affects GitLab CE/EE from 7.0 onward and scores CVSS 10.0. GitLab.com and GitLab Dedicated are already patched.

How does the plugin work?

Every skill follows the same five-step shape:

Read-only inventory: The agent scans Dockerfiles, base images, distro packages, CI, Helm, Terraform, Packer, Lambda and config management.

Approval gate: Nothing changes until you pick repos. Riskier minor or major upgrades are called out first.

Verified target: Every tag, digest, package version and checksum is confirmed against the official source before editing.

Test before and after: The suite runs on the current version, then inside the new production image. Regressions stop the run.

One PR per repo: Each PR carries versions, test results, runtime diffs, a risk label and a rollback plan.

The skills also encode known patching traps. Debian and Ubuntu backport fixes without changing upstream versions, so php -v can mislead. Ubuntu 24.04&#8217;s fixed package is 8.3.6-0ubuntu0.24.04.13. Digest-pinned images need a new digest. Changing Composer&#8217;s require.php patches nothing.

&&

How do you install and run it?

In Devin, open Customize, then Plugins, then Browse Marketplace, and search for Vulnerability Fixes. The Devin CLI uses devin plugins install CognitionAI/devin-marketplace#plugins/devin-vuln-fixes. For other agents, run npx skills add CognitionAI/devin-vuln-fixes. Claude Code users can add the marketplace and run /plugin install vuln-fixes@cognition-skills.

Then ask in plain language, such as &#8216;Please fix my PHP vulnerability.&#8217; Slash commands also work: /fix-php-vuln, /fix-node-vuln and /fix-gitlab-vuln.

How does it compare with Dependabot, Copilot Autofix and Snyk Agent Fix?

FeatureDevin Vulnerability FixesDependabot security updatesGitHub Copilot AutofixSnyk Agent FixWhat it fixesPHP, Node.js and self-managed GitLab versions for 3 advisoriesVulnerable dependencies with an available patch, plus GitHub ActionsCode scanning alertsSnyk Code findingsWhere it editsDockerfiles, images, distro packages, CI, Helm, Terraform, config managementManifest and lock filesCode suggestions in the repoLocal-file code fixes; no complex inter-file logicApproval before editsYes, read-only inventory firstNo: opens PRs automatically once enabledNot disclosedUser clicks &#8220;Generate AI fix&#8221; and reviewsValidationTests before and after inside the new production imageCompatibility scores from public CI runsNot disclosedRetests fix with the Snyk Code engineRuns whereAny agent that reads SKILL.mdGitHubGitHubSnyk web UI and IDE pluginsLicenseMIT, open sourceNot disclosedNot disclosedNot disclosedCostFreeAvailable for all GitHub repositoriesFree on public repos; private repos need GitHub Code SecurityRequires Snyk Code; price not disclosed

These tools solve adjacent problems. Dependabot and the code-fix agents work on application dependencies and source code. Cognition&#8217;s plugin targets the runtime layer: base images, OS packages and infrastructure-as-code.

Key Takeaways

Three MIT-licensed skills patch PHP2Shell, Node.js and GitLab CVE-2026-110264.

Read-only inventory and an approval gate come before any edit.

Tests run before and after inside the new production image.

Works across Devin, Claude Code, Codex, Cursor and other SKILL.md agents.

No published fix-rate benchmark; results depend on your test coverage.

Check out the GitHub repo, the Cognition blog post and the plugin page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Cognition Open-Sources an Agent Plugin that Helps Secure Systems against Recent Cybersecurity Threats appeared first on MarkTechPost.