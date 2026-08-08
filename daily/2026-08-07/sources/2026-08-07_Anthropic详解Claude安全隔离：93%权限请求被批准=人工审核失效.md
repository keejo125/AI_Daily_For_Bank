---
title: Anthropic 详解 Claude 的安全隔离架构：如何在 Web、开发和桌面环境中约束 Agent 行为
source: InfoQ
link: https://mp.weixin.qq.com/s/R9KZ8uM4XyaqhTE9Mf4TfQ
publish_date: 2026-08-07
status: confirmed
---

> 来源：微信公众号 | 2026-08-07

作者 ｜ Eran Stiller
译者 ｜ 马可薇
Anthropic 近日详细介绍了 Claude 在 Web、开发者和桌面产品中的 安全隔离架构。该公司认为，Agent 的安全不能仅依赖权限确认或模型自身的安全机制，更关键的是通过文件系统、网络以及执行环境等基础设施，对 Agent 建立确定性的安全边界。文章重点分析了多个发生在信任边界和允许出口路径上的安全事件，以及这些事件如何促使 Anthropic 调整相关设计。
Anthropic 将 Agent 面临的风险归纳为三类：用户误用、模型自身的错误行为，以及通过文件、工具或网络内容发起的攻击。Anthropic 的核心观点是，分类器、系统提示词以及模型训练等机制虽然能够影响模型行为，但无法提供绝对的保证。真正决定 Agent 能够访问什么、能够向外发送什么数据的，是运行环境本身所施加的限制。
Anthropic 将 Agent 系统划分为三个层次：具有概率性的模型、执行环境，以及可能影响模型行为的外部内容。（来源：Anthropic）
以 Claude.ai 为例，其代码执行环境运行在隔离基础设施上的临时 gVisor 容器中，完全无法访问用户本地文件系统。而 Claude Code 则直接运行在开发者本机。最初，它采用逐项授权机制：每次写入文件、执行 Shell 命令或访问网络时，都需要用户确认。Anthropic 发现，用户最终批准了约 93% 的权限请求，使持续依赖人工确认的安全价值大打折扣。随后，Anthropic 为 Claude Code 引入了操作系统级沙箱：macOS 使用 Seatbelt，Linux 使用 bubblewrap。新的设计允许 Agent 在当前工作区内读写文件，但默认禁止访问网络。Anthropic 表示，这一调整使权限确认弹窗数量减少了 84%。
文章还披露了一起安全事件。Anthropic 收到报告称，在用户尚未确认是否信任某个项目目录之前，Claude Code 就已经开始解析其中的本地配置文件。其中一个案例中，代码仓库里的
.claude/settings.json
定义了一个会在启动时自动执行的 Hook。针对这一问题，Anthropic 修改了实现方式：只有在用户明确选择信任该项目之后，才会解析并执行项目中的本地配置。
Anthropic 还分享了一次受控红队测试，用于验证仅依赖权限确认或分类器判断用户意图所存在的局限。在测试中，攻击者首先通过钓鱼攻击诱导员工，随后让 Claude Code 收到一条看似合理的指令：读取 AWS 凭证，并发送到一个外部地址。Anthropic 表示，在 25 次测试中，有 24 次 Claude 都执行了数据外传操作。这一结果表明，即使请求看起来来自合法用户，也不能仅依赖授权机制判断其安全性。无论请求来自真实用户、模型自身的误判，还是恶意工具生成的输出，文件系统隔离和出站网络限制等底层安全机制，都必须能够阻止凭证被窃取。
相比 Claude Code，Claude Cowork 面向的用户更难判断 Shell 命令是否安全，因此采用了更严格的隔离机制。最初的设计中，Agent 完全运行在一台虚拟机内，仅将用户指定的工作目录挂载到虚拟机，同时将各种凭证保存在宿主机的密钥链中。后来，为了提升系统可靠性，Anthropic 将 Agent 的主循环迁移到宿主机，而代码执行仍然保留在虚拟机内部。
Claude Cowork 的初始全虚拟机架构，以及后续采用宿主机 Agent Loop 的架构。（来源：
Anthropic
）
不过，这套设计也暴露出域名白名单机制的一个重要局限。Anthropic 提到，一位第三方安全研究人员披露了一项漏洞：恶意文件能够诱导 Claude 通过 Anthropic 自身的 Files API，将工作区文件上传到攻击者控制的账户。这是因为
api.anthropic.com
已被加入白名单，所以请求能够顺利通过目的地址检查。
对此，Anthropic 调整了系统设计，在虚拟机内部增加了一层代理。新的代理只接受当前虚拟机会话生成的 Session Token，同时会拦截与服务端抓取相关的请求头，从而阻止这一类攻击。Anthropic 认为，这一事件说明，一个被加入白名单的域名，并不意味着它的所有能力都是可信的。将某个域名加入白名单，实际上意味着允许访问该域名所提供的全部功能，而不仅仅是其中某一个接口。
域名白名单让攻击者得以通过 Anthropic Files API 实现数据外传；新的代理机制仅允许使用虚拟机会话生成的 Token 发起请求。（来源：Anthropic）
文章最后指出，Agent 的安全隔离机制，应当根据用户能够提供的有效监督程度进行设计。Anthropic 强调，Agent 安全不能仅依赖识别恶意意图，更重要的是通过运行环境本身建立严格的边界，使即便 Agent 执行了不安全的操作，其造成的影响也始终受到限制。
查看英文原文：
Anthropic Details How it Contains Claude across Web, Code, and Cowork - InfoQ
(https://www.infoq.com/news/2026/07/anthropic-claude-containment/)
声明：本文由 InfoQ 翻译，未经许可禁止转载。
点击底部
阅读原文
访问 InfoQ 官网，获取更多精彩内容！
今日好文推荐
Jeff Dean离职前最后一次对话：我低估了AI，也看清了创业者的唯一生路
刚刚，哈萨比斯卸任谷歌 DeepMind CEO，27 年老将 Jeff Dean 离职创业
从“小卡拉米” 杀入 CNCF，创始人却说：HAMi火了，我们每天仍如履薄冰
AI 真的太贵了