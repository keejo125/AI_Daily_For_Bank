---
publish_time: 1786517558
status: confirmed
category: 国际
is_model_related: false
digest: |
  微软将 Agent Framework 从 SDK 阶段推进至受支持的生产运行时。该框架于 2026 年 4 月 2 日发布 1.0 版，Build 2026 上 Agent Harness、GitHub Copilot SDK、Claude Agent SDK 连接器及多代理编排进入稳定发布，随后 Harness 与 Foundry Hosted Agents 正式发布。

  Harness 是核心：仅凭模型只能生成文本，需运行时封装才能调用工具、处理多步骤任务并持续运行。框架内置函数调用、历史持久化、上下文压缩、待办列表、文件记忆、技能、网络搜索、工具审批与 OpenTelemetry，整合 Semantic Kernel 与 AutoGen（已转维护模式），作为单二进制跨本地、容器与托管环境运行。
link: https://mp.weixin.qq.com/s/Mrs-MJIiGpLdAVFNEGZbog
source: InfoQ
title: 微软正式发布 Agent Framework Harness 和 Hosted Agents
---

# 微软正式发布 Agent Framework Harness 和 Hosted Agents

来源：InfoQ
原文链接：https://mp.weixin.qq.com/s/Mrs-MJIiGpLdAVFNEGZbog

作者 ｜ Steef-Jan Wiggers
译者 ｜ 平川
微软已经将 Agent Framework 从 SDK 阶段推进至受支持的生产运行时。该框架于 2026 年 4 月 2 日 正式发布 1.0 版本；在 6 月 2 日至 3 日举行的 Build 2026 大会上，Agent Harness、GitHub Copilot SDK 和 Claude Agent SDK 连接器以及多代理编排模式均已进入稳定发布阶段。此后，Harness 和 Foundry Hosted Agents 正式发布，为平台团队提供了运行和管理代理的途径，而不仅仅是一个用于构建代理的库。作为单个二进制文件，它可以跨本地开发环境、容器环境和托管部署环境运行。
此前，InfoQ 曾报道过该框架的发布，将其看成是对开源项目 Semantic Kernel 和 AutoGen 的整合。1.0 版本的发布解决了构建时应该选用哪个框架的问题，并将这两个作为前身的项目转入了维护模式。该构建的发布公告则针对后续的运行时问题进行了说明：代理在何处执行、允许其访问哪些资源，以及其行为如何在现有的可观测性和策略系统中体现。
Harness 正是这一故事的核心。正如微软首席软件工程师 Wes Steyn 所言：
仅凭模型本身，只能生成文本。
为了使其能够调用工具、处理多步骤任务，并持续运行直至任务完成，需要将其封装在运行时环境中；该运行时环境即为 Harness。Agent Framework 现在已经内置了该运行时环境，因此团队不需要重新构建它。本次发布包含函数调用、每个历史调用记录的持久化、上下文压缩、带计划和执行模式的待办事项列表、文件记忆、技能、网络搜索、工具审批以及内置的 OpenTelemetry，这些功能均已默认启用，而且可以单独禁用。Shell 工具、文件访问、后台子代理和自动循环仍然是可选功能，启用时仍然会发出警告。Foundry Hosted Agents（托管部署目标）按使用量计费。
开发者只需要提供聊天客户端、操作指南和工具；Harness 框架将通过单次调用提供其余内容：
client = FoundryChatClient(credential=AzureCliCredential())
# 一个调用即可处理规划、历史数据持久化、
# 压缩、审批、网页搜索和遥测等功能。
agent = create_harness_agent(
client=client,
agent_instructions=
&quot;You are a research assistant. Plan your work, then execute it.&quot;
,
tools=[],
# add your own callable tools here
)
response = await agent.run(
&quot;Research the outlook for renewable energy stocks.&quot;
)
为什么一个受支持的 Harness 比表面上看起来更重要：Harness 占据了系统的大部分。MBZUAI 旗下的 VILA 实验室于 2026 年 4 月发表一片论文“深入解析 Claude Code”，其中对此给出了具体的数据。研究人员分析了 Claude Code v2.1.88 版本——该版本的完整 TypeScript 源代码曾于 3 月 31 日短暂曝光，当时 Anthropic 发布了一个包含源映射包的 npm 版本——并且经过统计得出，该版本包含 1884 个文件，总计约 512000 行代码。据其估算：代码库中约 98.4% 的代码属于 Harness 基础设施、权限管理、上下文管理、沙箱机制、工具路由以及恢复机制，而 AI 决策逻辑仅占约 1.6% 。该数据加了星号，作者明确指出：这是针对所泄露的包进行的代码行分类，其中包含生成的代码和压缩后的代码，而并非全面的审计。即使不考虑这一因素，这一趋势依然成立：多个独立开发的代理（包括 Codex CLI 和 Aider）都采用了相同的 Harness 结构。这表明这是一种问题约束，而非设计选择。
有 一项早期进行的基准测试 也得出了相同的结论，但有一点需要明确说明一下：该测试由微软人工智能首席架构师 Aqib Sherwani 执行，对比了微软旗下的两个运行时 Agent Framework 与 GitHub Copilot SDK。他所采用的测试方法比大多数厂商的基准测试更为严谨：固定模型参数，并首先运行一个确定性的模拟测试，从而确保差异可追溯至 Harness。他总结说，“推理相同，工程实现不同”：两者在相同的步数内得出了相同的答案，差异仅存在于运行时中。最关键的差异在于安全防护失控。Agent Framework 在经过 40 次往返循环后会自行终止循环并返回“达到限制”的消息；而在关闭主机端停止控制机制的情况下， Copilot SDK 会持续运行至 300 次而不自行停止。一种 Harness 将“刹车”机制置于循环内部；另一种则期望由主机提供该机制。
编码代理连接器使治理方案得以落地。 Agent Framework 的编排功能不需要自定义适配器即可将任务委托给 GitHub Copilot SDK 或 Claude Agent SDK；每个代理都运行自己的自主循环，并通过封装使编码代理能够与 Azure OpenAI、Anthropic 或自定义代理在同一个工作流中协同工作。其中有一个关键的细节，这些连接器严格遵循为代理集群设置的身份、内容安全以及可观测性策略。编码代理的流量与其他所有流量一样，都会进入相同的 OpenTelemetry 跟踪和 Foundry 仪表板，而不是成为一项具有独立访问模型的独立集成。这也是可以在 亚马逊云科技的 Loom 参考平台中看到的控制层关注点：治理的核心问题已经从“代理能做什么”转变为“谁运行了它”、“依据什么策略”以及“跟踪信息最终流向何处”。
这些编排模式与测试框架同步发布了稳定版，涵盖了顺序管道、并行协作以及源自微软研究院 Magentic-One 的 Magentic 模式（参见 InfoQ 相关报道）。其 2024 年的评估报告显示，在 GAIA 基准测试中达到 38%，在 AssistantBench 中达到 27.7%，在 WebArena 中达到 32.8%。在前两个基准测试中，其成绩在统计上与当前最先进的水平相当；而在 WebArena 测试中也颇具竞争力。微软之所以如此报告，是因为该基准测试没有隐藏的测试集。这些模式共享一个 API，团队无需重写代理代码即可更改协调风格。
对于正在权衡此次发布的平台团队而言，与云相关的关键之处在于运行时，而非 SDK：一个受支持的治理框架、按使用量计费的托管目标环境，以及将第三方编码代理视为集群中受管控成员的策略和可观测性模型。该框架、治理框架和连接器现在已经在 GitHub 上发布 .NET 和 Python 版本。
原文链接：
https://www.infoq.com/news/2026/08/agent-framework-harness-ga/
声明：本文为 InfoQ 翻译，未经许可禁止转载。
点击底部
阅读原文
访问 InfoQ 官网，获取更多精彩内容！
今日好文推荐
小扎万字长文炮轰闭源：蒸馏无罪，Meta 正式重回开源模型路线
“写代码从来都不是难点”，这是对全世界所有程序员的严重侮辱
Rust 给 AI 编程立新规：能帮你看，不能替你写，用多了还会“熔断”
MiniMax H3 团队 Reddit 上回应一切：2K 要开源，图像模型在路上，Apache 2.0 也在考虑了
