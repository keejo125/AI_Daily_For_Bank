---
publish_time: 1781592299
---

# 当AI Agent开始工作，安全该如何跟上？AgentDoG 1.5开源发布

> 原文链接：https://mp.weixin.qq.com/s/SwQE5tKF5HyEsLcmOrkR5Q
> 公众号：机器之心

最近，

同事.skill（colleague.skill）在社区中的快速传播，让很多人开始直观地感受到：AI Agent 正在从「聊天助手」走向「工作伙伴」。

Agent 不再只是回答问题，而是可以继承一个人的工作习惯、任务流程、知识背景和决策方式，并在 Claude Code、Hermes、OpenClaw、Codex 等 Agent 宿主中被调用。

换句话说，Agent 正在逐渐成为一种新的工作单元：

它可以协助人类完成任务，也可能在某些场景中接管一部分具体工作。

与此同时，安全问题也变得更加复杂。过去讨论大模型安全，很多时候是在判断一段用户输入是否有害，或者一段模型输出是否合规。但进入 Agent 时代后，风险不再只存在于一句 prompt 或一个最终回复里。它可能隐藏在工具描述中，出现在环境反馈里，被写入长期记忆或会话状态，也可能通过一次错误的工具调用、一次未经验证的命令执行、一次跨应用操作，影响真实文件、账户、代码仓库甚至业务系统。

因此，Agent 安全不再只是「内容安全」，而是完整执行过程中的行为诊断、风险归因和在线干预问题。

围绕这一问题，

上海人工智能实验室发布 AgentDoG 1.5：一个面向 AI Agent 的轻量化、可扩展安全诊断与在线护栏框架。

论文已上线 arXiv，代码、模型与数据均已开源。

论文链接：https://arxiv.org/abs/2605.29801

项目链接：https://github.com/AI45Lab/AgentDoG

Hugging Face：https://huggingface.co/collections/AI45Research/agentdog15

从「看输出」到「看轨迹」

AgentDoG 1.5 的核心出发点是：

Agent 的安全风险往往发生在完整执行过程中，而不是只发生在 Agent 的最终回复里。

一个 Agent 可能在最终回复中看起来正常，但此前已经错误调用了工具、泄露了信息、执行了危险命令，或者被外部环境中的恶意内容诱导发生目标偏移。

因此，面向 Agent 的安全评测，不能只看最终输出，而应该把完整 agent trajectory 作为判断对象。

在 AgentDoG 1.5 中，模型会综合分析用户请求、Agent 中间响应、工具调用、环境反馈和最终回复，对整条轨迹进行安全诊断。它不仅判断一条轨迹是 safe 还是 unsafe，还进一步输出三类细粒度诊断信息：Risk Source，即风险从哪里来；Failure Mode，即 Agent 是如何失败的；Real-world Harm，即这种失败会造成什么现实危害。

通过这种三维诊断，安全判断不再只是一个二分类结果，而可以进一步支持风险定位、模型训练、benchmark 构建和部署阶段的在线拦截。

面向快速变化的 Agent 平台，taxonomy 也必须可扩展

Agent 系统的发展速度很快，不同执行平台面对的风险也并不相同。通用 tool-use agent、OpenClaw 这类跨应用执行 Agent、Codex 这类面向代码仓库和命令执行的 Agent，在执行环境、工具边界、状态管理和潜在危害上都有明显差异。如果每出现一个新 Agent 平台，就重新设计一套安全标签和评测任务，整个 guardrail 体系会很快碎片化。

AgentDoG 1.5 采用的方式是：

保持 Risk Source、Failure Mode、Real-world Harm 这三个高层维度不变，在不同执行场景下扩展和细化 leaf categories。

例如，在 OpenClaw 场景中，风险可能来自持久会话、审批绕过、技能或插件供应链、跨工具攻击链、跨通道路由错误，或者无人值守自动化执行；在 Codex 场景中，风险则可能来自仓库文件注入、依赖或 MCP 供应链问题、危险 shell/script 执行、破坏性工作区修改，以及未经验证的测试或成功声明。

基于这一思路，论文进一步

构建了 ATBench Family。

ATBench 面向通用 tool-use agent，ATBench-Claw 面向 OpenClaw 执行场景，ATBench-Codex 面向 Codex 执行场景。三者共享同一个 trajectory-level diagnosis task 和三维 taxonomy 框架，同时针对不同执行环境扩展具体风险类别。这使得 AgentDoG 1.5 能够在保持跨场景可比性的同时，持续适配新的 Agent 平台。

只用约 1k 高质量样本，训练轻量 AgentDoG 1.5

在训练 AgentDoG 1.5 时，论文没有简单依赖大规模数据堆叠，而是构建了 taxonomy-guided data engine，通过三维 taxonomy 控制数据生成过程。换言之，风险从哪里进入、Agent 如何失败、会造成什么 real-world harm，都在数据构造阶段被系统性建模。随后，团队使用 GPT-5.4 作为 teacher，为训练样本补充 chain-of-thought rationale，让学生模型不仅学习最终 judgment，也学习从轨迹证据到安全判断的推理过程。

由于原始合成数据往往存在噪声、冗余和低价值样本，AgentDoG 1.5 进一步引入 influence function-based data purification，从原始数据中筛选最有助于学习 guardrail 行为的高质量样本。

最终，AgentDoG 1.5 仅使用约 1k 条高信息量样本，训练了 0.8B、2B、4B 和 8B 等多个轻量模型版本。

实验结果显示，

AgentDoG 1.5 在轨迹级安全判断和细粒度风险诊断上均取得了强表现。

以 4B 模型为例，其在 R-Judge 上达到 92.2% Accuracy 和 92.7% F1，在 ATBench 上达到 72.4% Accuracy 和 74.3% F1；在 fine-grained risk diagnosis 上，AgentDoG 1.5-4B 在 Risk Source、Failure Mode、Real-world Harm 三个维度的平均得分达到 55.2%，相比 AgentDoG 1.0 有明显提升。

这些结果表明，

贴近 Agent 风险结构的数据和监督信号，可以把可靠的 agent safety judgment 能力蒸馏到较小规模的模型中。

构建轻量级 Agent 训练管线，支持超一万并发

AgentDoG 1.5 不只用于离线评测，也被进一步接入到 agentic safety training pipeline 中。该训练 pipeline 包含两个部分：一是面向 SFT 的高质量安全数据过滤，二是面向 RL 的轻量化交互环境与安全 reward 构造。通过这一 pipeline，AgentDoG 1.5 可以把轨迹级安全诊断能力转化为训练阶段的监督信号，支持更低成本、更可扩展的 Agent 安全对齐。

在 SFT 阶段，团队使用 ATBench data engine 构造 agentic safety 数据，并利用 AgentDoG 1.5 过滤高质量 safe trajectories。过滤后得到 28,705 条高质量 agentic safety trajectories，并与 50,000 条 benign tool-use trajectories 混合，以避免模型学成过度保守的拒绝策略。

实验显示，加入 AgentDoG 1.5 过滤后的安全数据后，模型在多个安全指标上明显改善。例如，在 AgentHarm 上，harm score 从 57.49% 降至 20.32%，refusal rate 从 28.41% 提升至 75.00%；在 AgentSafetyBench 上，safe rate 从 34.37% 提升至 53.23%。

这说明

AgentDoG 1.5 不只是一个评测模型，也可以作为数据质量控制模块参与安全训练流程。

在 RL 阶段，论文构建了轻量化 finite-state Python simulator 环境，用于支持 scalable agentic safety RL。相比依赖完整 Docker-level 环境的真实执行训练，这类轻量环境通过有限状态模拟、工具接口和规则化反馈来构造可扩展的交互任务，并结合 AgentDoG 1.5 提供的轨迹级安全判断形成 reward signal。

实验中，该环境可同时加载 10,000 个环境、维护 1,000 个活跃实例，并支持 1,000 个并发工具调用，峰值内存保持在 2.5GB 以下。

这一设计显著降低了 agentic safety RL 的环境部署成本，使大规模安全训练更加可行。

构筑 Agent 最后防线：在线安全护栏

AgentDoG 1.5 不仅可以支持 Agent 训练，还可以部署为 online guardrail。

论文提出一种

Pre-Reply 介入机制：

在 Agent 最终回复发送给用户之前，AgentDoG 1.5 会读取完整执行轨迹，包括用户输入、工具调用、工具结果、环境观察和最终草稿，并判断是否允许放行。

这样既能利用比 prompt-level 或 output-only guardrail 更完整的上下文，又避免在每一次工具调用后都插入检测，从而降低对 agent loop 的延迟影响。

在 OpenClaw 在线评测中，AgentDoG 1.5 能有效降低 unsafe final deliveries。AgentDoG 1.5-4B 将 ClawSafety 的 ASR 从 56.25% 降至 18.75%，将 AgentHazard Prompt Intelligence Theft 的 ASR 从 41.92% 降至 26.92%，并在 CIK-Bench retained cases 上将 ASR 从 94.29% 降至 42.86%。受益于 Pre-Reply 的设计，AgentDoG 1.5 整体延迟在可部署范围内。

为什么这件事重要？

AI Agent 的能力正在从「生成内容」走向「执行任务」。当 Agent 能够调用真实工具、访问真实文件、触达真实系统时，安全问题也随之升级：

它不再只是内容审核问题，而是执行过程中的行为诊断、风险归因和在线干预问题。

AgentDoG 1.5 的贡献在于，它把这些环节串成了一个完整闭环：用三维 taxonomy 描述风险，用 ATBench Family 评测不同 Agent 场景，用 taxonomy-guided data engine 构造训练数据，用 influence-function purification 训练轻量模型，并进一步支持 agentic safety SFT、RL 和 online guardrail。随着 Agent 系统继续演进，这种可诊断、可扩展、可部署的安全框架，将成为 Agent 走向真实工作场景的重要基础。

如果说未来的 AI Agent 会越来越像一个能够行动的数字助手，那么 AgentDoG 1.5 想做的，就是

让它在行动之前、行动之中、行动之后，都有一套可诊断、可扩展、可部署的安全机制。

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com