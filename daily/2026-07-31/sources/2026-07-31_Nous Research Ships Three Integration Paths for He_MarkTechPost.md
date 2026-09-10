---
publish_time: 1785488893
status: confirmed
category: 国际
is_model_related: false
digest: |
  Nous Research发布了Hermes Agent与Buzz的三种集成路径。Buzz是Block公司（Square母公司）推出的开源、可自托管工作空间，构建于Nostr协议之上，让人类和AI代理共享同一频道。在Nostr架构中，每条消息都是中继上的签名事件，每个参与者都是密钥对，消除了传统bot-token模型，代理拥有独立身份、频道成员资格和审计轨迹。
  
  三种集成方式分别是：一、Buzz Desktop托管运行时，在本地启动Hermes作为预设harness，通过ACP over stdio通信；二、中继桥接，通过buzz-acp harness经WebSocket连接频道到Hermes ACP；三、原生网关平台，通过内置插件使Buzz成为Hermes的标准消息平台，支持频道、私信、mention gating、线程回复、反应、图片和定时投递。
  
  在网关路径上，入站通过NIP-42认证的Nostr WebSocket，使用BIP-340签名，自动降级到CLI轮询（默认4秒间隔）。默认配置注重隐私：require_mention开启、allow-list强制执行、工具日志抑制。Buzz为Apache-2.0许可（18.8k stars），Hermes Agent为MIT许可，均可自托管部署。
---

# Nous Research Ships Three Integration Paths for Hermes Agent and Buzz, Block’s Open Source Nostr Workspace for Humans and Agents

> 原文链接：https://www.marktechpost.com/2026/07/31/nous-research-ships-three-integration-paths-for-hermes-agent-and-buzz-blocks-open-source-nostr-workspace-for-humans-and-agents/
> 来源：MarkTechPost

Nous Research has released Hermes Agent support for Buzz, Block&#8217;s open source, self-hostable workspace where humans and AI agents share the same channels. Buzz is built on Nostr. Every message is a signed event on a relay you own, and every participant, human or agent, is a keypair. That removes the bot-token model. Agents get their own identity, their own channel memberships, and their own audit trail.

Is it deployable, and for whom?

Yes, and both sides are self-hostable today. Buzz is Apache-2.0 with 18.8k stars; Hermes Agent is MIT licensed. Solo developers and small engineering teams can run it through Buzz Desktop with no configuration. Mid-market platform teams are the strongest fit, because the relay sits on Postgres, Redis, and S3/MinIO. Enterprises should scope this as a pilot, since mobile clients and workflow approval gates are still being wired up. Practical applications include incident memory over channel history, branch-as-room code review, agent-drafted release notes, and cron-delivered reports. 

Three ways to connect

The integration docs split the work by where Hermes runs.

Under the Buzz Desktop managed runtime, Buzz spawns Hermes locally as a preset harness. Open Settings → Runtimes and Hermes appears automatically. Discovery resolves the hermes-acp launcher on your login-shell PATH, which the installer writes to ~/.local/bin. Inbound is ACP over stdio.

The relay bridge suits a hosted agent identity. Buzz&#8217;s buzz-acp harness bridges a channel to hermes acp over stdio, reaching the relay by WebSocket. This is a transport integration, not a second install. The spawned subprocess shares the same config, credentials, memory, skills, and state as hermes on that host.

The native gateway platform is the deepest option. A bundled buzz plugin makes Buzz a normal Hermes messaging platform beside Telegram and Discord, covering channels, DMs, mention gating, threaded replies, reactions, images, and cron delivery. Hermes keeps its own approvals, memory, and session management. Setup is hermes gateway setup.

Transport, defaults, and identity

On the gateway path, inbound arrives over a persistent NIP-42-authenticated Nostr WebSocket with dependency-free BIP-340 signing, falling back to CLI polling automatically. Outbound always goes through the buzz CLI. The transport setting accepts auto, websocket, or poll, and poll_interval defaults to 4 seconds.

The recommended defaults ship private. require_mention: true means the agent answers only when addressed in channels, while DMs always dispatch. allow_all_users: false restricts access to listed npubs or hex pubkeys. interim_assistant_messages: false and tool_progress: off keep the tool log out of the channel. Events are de-duplicated by event id against a per-channel high-water mark, and the agent&#8217;s own messages are filtered by pubkey.

Key Takeaways

Hermes Agent connects to Buzz three ways: Desktop runtime, relay bridge, and native gateway.

The gateway path keeps Hermes memory, skills, approvals, cron, and sessions intact.

Inbound uses a NIP-42 Nostr WebSocket, with CLI polling fallback at 4 seconds.

Defaults are private: mention gating on, allow-list enforced, tool logs suppressed.

Buzz Desktop auto-approves tool permissions, so keep agents owner-only.

Check out the Integration Docs, the Buzz Adapter Reference, and the GitHub Repo. Also, feel free to follow us on Twitter, and don&#8217;t forget to join our SubReddit and subscribe to our Newsletter.

The post Nous Research Ships Three Integration Paths for Hermes Agent and Buzz, Block&#8217;s Open Source Nostr Workspace for Humans and Agents appeared first on MarkTechPost.