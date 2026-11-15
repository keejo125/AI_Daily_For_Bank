---
publish_time: 1792840347
link: https://www.marktechpost.com/2026/10/24/anthropic-sandbox-runtime-ai-agent-sandbox/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  MarkTechPost 介绍 Anthropic 开源的 sandbox-runtime（srt）——Claude Code 沙箱 bash 工具背后的 OS 级沙箱。它在不启动容器、也不绑定 Claude Code 的前提下，限制进程可触碰的文件与可访问的主机，开发者自有的 Agent、本地 MCP 服务与普通命令行程序均可运行其中。该 npm 包（v0.0.81，约 11.4MB，Apache-2.0，需 Node.js 22.12+）可在任意 macOS/Linux 开发机或 CI 运行：macOS 用 Seatbelt，Linux 需 bubblewrap、socat 与 ripgrep，Windows 仍为 alpha。Anthropic 内部使用显示它使 Claude Code 的权限提示减少 84%，把文件与网络限制施加于整个进程树，是 Agent 安全运行的可复用基础设施。
---

# Anthropic 开源 sandbox-runtime：Claude Code 背后的 OS 级沙箱

> 原文链接：https://www.marktechpost.com/2026/10/24/anthropic-sandbox-runtime-ai-agent-sandbox/
> 来源：MarkTechPost

In this article, we will discuss newly trending open sourced Anthropic&#8217;s sandbox-runtime (srt), the OS-level sandbox behind Claude Code&#8217;s sandboxed bash tool. The Anthropic sandbox-runtime limits which files a process can touch and which hosts it can reach. It does this without spinning up a container. It is also not tied to Claude Code. Your own agents, local MCP servers and plain command-line programs can run inside it.

TL;DR

Size: npm package @anthropic-ai/sandbox-runtime v0.0.81, about 11.4 MB unpacked, Apache-2.0, Node.js 22.12+. 

Runs on: any macOS or Linux dev machine or CI box. macOS uses Seatbelt; Linux needs bubblewrap, socat and ripgrep. Windows is alpha.

Performance: sandboxing cut Claude Code permission prompts by 84% in Anthropic&#8217;s internal usage (self-reported).

Best: 84% fewer permission prompts, with file and network limits enforced on the whole process tree.

Worst: still a beta research preview, Windows support is alpha.

What is Anthropic sandbox-runtime?

Anthropic sandbox-runtime is an open-source tool that wraps any process in filesystem and network restrictions. You install it with npm install -g @anthropic-ai/sandbox-runtime, then prefix a command with srt. It works as a CLI and as a TypeScript library.

How does sandbox-runtime work on macOS, Linux and Windows?

srt uses each operating system&#8217;s own isolation primitives. Its restrictions cover the entire process tree, including scripts and subprocesses.

macOS: sandbox-exec with dynamically generated Seatbelt profiles. Only ripgrep is required.

Linux: bubblewrap with the network namespace removed. It also needs socat and ripgrep.

Windows (alpha): a dedicated srt-sandbox account, a Windows Filtering Platform egress fence and explicit file ACLs.

Traffic leaves only through HTTP and SOCKS5 proxies running on the host. On Linux, those proxies sit behind Unix sockets bind-mounted into the sandbox. On macOS, the Seatbelt profile allows only one localhost port. The proxies then apply your domain allowlist and denylist.

Why does it need both filesystem and network isolation?

Anthropic team argues that 1 boundary without the other fails. Without network isolation, a prompt-injected agent could exfiltrate SSH keys. Without filesystem isolation, it could escape the sandbox and gain network access.

srt&#8217;s defaults follow that logic. Reads are allowed everywhere unless denied. Writes are denied everywhere unless allowed. Network access is denied unless a domain is allowlisted.

How do you sandbox an MCP server or your own agent?

For an MCP server, change the command in .mcp.json from npx to srt. Pass the original command as arguments. Rules then live in ~/.srt-settings.json:

Copy CodeCopiedUse a different Browser

{
  "network": { "allowedDomains": ["api.github.com", "*.npmjs.org"], "deniedDomains": [] },
  "filesystem": { "denyRead": ["~/.ssh"], "allowWrite": ["."], "denyWrite": [".env"] }
}

For your own agent, the library exposes SandboxManager. Call initialize(config) to start the proxies. Then wrapWithSandbox() returns a wrapped command string you can spawn.

What does the 84% figure mean?

Anthropic reports that sandboxing reduced permission prompts by 84% in internal Claude Code usage. That is a self-reported number, not an external benchmark. The target is approval fatigue. Developers who click &#8220;approve&#8221; all day stop reading what they approve. A fixed boundary lets the agent work freely inside it and ask only at the edge.

The real trade-off: strict allowlists vs working agents

Coding agents do more than edit files. They install dependencies, pull docs and call APIs. Make the allowlist too strict and npm install fails. Make it too loose and the sandbox protects little. srt ships several knobs for that middle ground:

Wildcards and ports: entries like *.npmjs.org or api.example.com:443.

Ask callback: decides hosts no rule covers, and can return a reason the model reads.

Per-command allow lists: open a registry for 1 invocation only.

Live updates: --control-fd swaps network lists while a command runs.

Resolved-address check: blocks allowed names that resolve to loopback or cloud metadata IPs.

Denied-domain reasons: tell the agent the sanctioned alternative, such as an HTTPS git remote..

How does it compare with other agent sandboxes?

FeatureAnthropic sandbox-runtimeOpenAI Codex CLI sandboxDocker SandboxesE2BIsolationOS primitives: Seatbelt, bubblewrap, Windows account + WFPOS primitives: Seatbelt, bubblewrap, native Windows sandboxmicroVM per sandboxFirecracker microVM per sessionWhere it runsLocal machineLocal machineLocal machineCloud or BYOC (AWS, GCP)Container or VM neededNoNoYes (microVM)Yes (managed microVM)Use outside its own agentYes, CLI + library for any processBuilt into CodexYes, sbx CLI for coding agentsYes, JS and Python SDKsNetwork defaultDeny all; proxy allowlistOff in workspace-write; config togglePolicy picked at first start (e.g. deny-all, balanced)On by default; can be disabledDomain allowlistYes, wildcards + portsNot disclosed (on/off toggle documented)Yes, wildcards + portsYes, allowOut with wildcards (SNI/Host based)LicenseApache-2.0Apache-2.0Not disclosedApache-2.0 (SDK)StatusBeta research preview; Windows alphaShips in Codex CLIShipping productShipping product

Key Takeaways

srt sandboxes any process at the OS level, no container needed.

Seatbelt on macOS, bubblewrap on Linux, Windows in alpha.

Network is deny-by-default; every connection passes a host-side allowlist proxy.

Anthropic reports 84% fewer Claude Code permission prompts (internal).

Allowlist breadth is the real security dial; broad domains can leak data.

Check out the GitHub repo, the Anthropic engineering post and the Claude Code sandboxing docs. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet Anthropic’s sandbox-runtime: OS-Level Sandboxing for AI Agents, No Containers appeared first on MarkTechPost.