---
publish_time: 1784084563
---

# 翁荔长文谈Harness自进化：Agent越用越强，评测难点怎么破？

> 原文链接：https://mp.weixin.qq.com/s/_9KACIPUZhPYfqvhpffzVQ
> 公众号：机器之心

机器之心发布

近日，翁荔发布长文 《Harness Engineering for Self-Improvement》，系统梳理了 harness engineering 在 AI 自我改进中的作用。她指出，原始模型与真实世界任务之间的 harness layer 正在变得和模型本身一样重要：它决定模型如何规划、调用工具、管理上下文、保存状态、评估结果，并在长期任务中持续迭代。

这也揭示了当下 LLM Agent 研究中的一个关键转向：Agent 的能力提升不再只来自模型参数更新，也越来越来自模型外部系统的演化。

Prompt、memory、tools、workflow、middleware、permission control、runtime state 等组件共同构成 agent harness，而这些组件正在成为自进化系统的核心优化对象。

但随之而来的问题是：如果 Agent 会不断修改自己的 harness，我们应该如何评测这种「自我改进」？

现有 Agent benchmark 大多仍然面向静态系统：给定一个固定 Agent，在一组独立任务上运行，然后报告最终成功率。这种评测方式无法回答 harness evolution 中更关键的问题：一次更新到底改进了什么？提升是否能迁移到未见任务？是否只是过拟合近期反馈？是否遗忘了旧能力？是否引入了更高成本或运行时不稳定？

针对这一评测空白，清华大学团队提出了 SEAGym: An Evaluation Environment for Self-Evolving LLM Agents。

如果说 harness engineering 正在成为自进化 Agent 的重要技术路线，那么 SEAGym 关注的就是这条路线的评测基础设施：不只评估 Agent 最终得了多少分，而是评估它在更新过程中如何变强、何时退化、是否泛化、是否遗忘，以及付出了什么成本。

论文标题：SEAGym: An Evaluation Environment for Self-Evolving LLM Agents

论文地址：https://arxiv.org/abs/2606.17546

代码地址：https://github.com/antropy-research/SEAGym

从静态 benchmark 到动态自进化环境

SEAGym 将自进化 Agent 形式化为一个和强化学习算法训练过程对齐的评测过程。

每个 Agent snapshot 被表示为：

。其中 M 是固定的基础模型和不可变运行组件，

是可更新的 harness state，包括 prompts、memories、skills、tools、middleware、runtime configuration 等。

在每一步中，环境采样一批训练任务

，

Agent 在这些任务上执行，产生轨迹和反馈，然后根据自身的更新规则修改 harness：

这里，SEAGym 并不规定具体的更新算法。不同自进化方法可以保留自己的 native update rule，只需要通过统一的 rollout /update interface 接入即可。

这种设计使得 SEAGym 可以在同一套协议下比较不同类型的自进化方法，例如：

ACE：

主要积累 prompt-visible skillbook 或过程经验；

TF-GRPO：

利用 grouped rollout evidence 更新 experience/context store；

AHE：

直接编辑更广义的 agent harness，包括 prompts、tools、middleware 和 runtime 行为。

另外，通过将 agent 自进化过程与强化学习算法训练过程对齐，

SEAGym 能够将静态的 benchmark 通过 train batch 组织为自进化过程中的某个任务，

并且利用 harbor 实现了对不同类型的 benchmark 的适配兼容，

将复杂的 agent 自进化过程统一用简洁清晰的超参数控制，为后续自进化 agent 研究提供了统一的训练评测协议。

多视角评测：不只问「有没有变强」，还问「怎样变强」

SEAGym 的关键设计是将传统数据 split 与评测 view 区分开来。训练任务只用于产生更新证据，评测视角则被拆分为多个部分：

Train batch：

提供 Agent 更新所需的轨迹和反馈；

Update-validation：

冻结中间 snapshot，观察更新过程是否带来阶段性提升；

ID transfer：

测试更新是否能迁移到同分布但未见过的任务；

OOD transfer：

测试更新是否能迁移到分布外任务；

Replay：

回放旧任务，检查是否出现遗忘或回归；

Cost records：

记录 token、工具调用、运行时间和更新成本。

这使得研究者可以看到自进化过程中的细粒度动态。例如，一个 snapshot 可能在 validation 上提升，但在 OOD 上下降；一个中间版本可能短暂变强，之后因为错误的 middleware 修改而崩溃；一个最终版本可能整体得分更高，但同时遗忘了一部分原本能解决的任务。

SEAGym 不只是输出一个 leaderboard 分数，而是保存每个阶段的 snapshot、trajectory、public feedback、update summary、harness diff 和 metric records，用于后续诊断。

实验设置：Terminal-Bench 2.0 + HLE

论文在两个互补任务源上实例化 SEAGym：

Terminal-Bench 2.0：

偏 execution-heavy，包含命令行、软件工程和环境交互任务；

HLE：

偏 reasoning-heavy，论文使用其中 text-only Math / Physics 作为 source task，并使用 CS/AI 与 Engineering 作为 OOD transfer task。

论文比较了 ACE、TF-GRPO 和 AHE 三类自进化方法，并进一步做了 batch size、source diversity 和 cross-model transfer 等分析。

主要结果一：validation 提升不等于稳定泛化

在主实验中，三种方法呈现出明显不同的更新动态。

AHE 在 validation、ID 和 OOD 三个视角上都取得了提升：

validation：

40.0 → 57.1，提升 17.1 个百分点；

ID test：

40.0 → 49.1，提升 9.1 个百分点；

OOD test：

22.5 → 28.8，提升 6.3 个百分点。

ACE 的提升更温和：

validation 提升 2.9 个百分点；

ID 提升 3.6 个百分点；

OOD 提升 2.5 个百分点。

TF-GRPO 则展现出另一种现象：它在 validation 上提升明显，达到 +17.1 个百分点，但 OOD 下降 2.5 个百分点。这说明 grouped rollout evidence 可以强化 source distribution 上的行为，却不一定带来稳定的分布外迁移。

论文据此指出：

只看 validation curve 很容易高估自进化方法的真实泛化能力。

主要结果二：自进化可能引入中间崩溃，final score 会掩盖这一点

SEAGym 的 replay diagnostics 揭示了一个非常关键的现象：自进化过程并不总是单调变好。

在 AHE 的 train replay 实验中，初始 Agent 可以解决 34/80 个训练回放任务，最终 Agent 可以解决 43/80 个任务，看起来是一个正向提升。但如果观察中间 snapshot，会发现第 4 个 epoch 后 replay performance 一度跌到 6/80，并产生大量 rollout errors。

进一步分析发现，这不是普通意义上的 “模型忘记了怎么做题”，而是 harness evolution 修改了 middleware /runtime contract，导致 message construction 出现系统性错误。之后的更新修复了该路径，性能又恢复上来。

这说明，对于 self-evolving Agent，遗忘和退化不一定表现为知识能力下降，也可能表现为：

工具调用路径被破坏；

middleware contract 被破坏；

completion protocol 被错误修改；

validation 或 artifact 检查逻辑变得过度约束；

runtime 行为发生系统性回归。

如果只报告初始分数和最终分数，这种中间崩溃完全不可见。而 SEAGym 通过 snapshot-level replay 和 task-level churn，将这类过程风险暴露出来。

主要结果三：batch size 影响 harness 更新稳定性，且不是越大越好

论文进一步研究了 AHE 在不同 batch size 下的表现：10、20、40、80。

结果呈现明显的非单调关系：

batch 10：

validation 从 37.1 降到 22.9，ID 从 38.2 降到 23.6；

batch 20：

validation 从 40.0 升到 57.1，ID 从 40.0 升到 49.1；

batch 40：

validation 从 37.1 升到 40.0，ID 从 41.8 升到 43.6；

batch 80：

validation 从 42.9 降到 25.7，ID 从 41.8 降到 25.5。

这说明，对于 harness-level evolution，batch size 不是简单的统计效率问题。batch 太小会导致更新证据不足、更新频率过高，从而增加 runtime regression 的机会；batch 太大则会让单次更新需要分析过多轨迹，稀释每个任务的注意力，诱发粗糙或脆弱的 harness 修改。

在该实验中，batch 20 是 evidence diversity、per-task analysis depth、update frequency 和 harness stability 之间较平衡的设置。

主要结果四：训练来源多样性影响恢复能力

论文比较了 mixed-source training 和 HLE-only training。

mixed-source 设置使用 Terminal-Bench + HLE，而 HLE-only 只使用 HLE Math/Physics。结果显示，HLE-only run 在中间 snapshot 上也能取得有用提升，但最终 snapshot 出现 collapse：

HLE-only final validation、ID、OOD 均降到 0；

但其 best intermediate snapshot 仍能达到 ID +7.3、OOD +3.8 的提升。

论文认为，单一 benchmark 可能会把 harness 推向 benchmark-specific local optimum。相比之下，Terminal-Bench 提供了工具、环境、执行路径和 runtime 错误方面的多样信号，HLE 提供 reasoning-heavy 信号，两者结合可以帮助后续更新从坏状态中恢复。

主要结果五：

harness 更新具有 backend 依赖

论文还考察了 cross-model transfer：用 DeepSeek、GLM 和 GPT-5.4 分别训练 AHE harness，再交换到不同 rollout model 上评估。

结果显示，同 backend transfer 通常更稳定：

DeepSeek-evolved harness 在 DeepSeek 上 ID +9.1；

GLM-evolved harness 在 GLM 上 ID +3.6；

GPT-5.4-evolved harness 在 GPT-5.4 上 ID +5.5。

但 cross-backend transfer 明显不对称。例如：

DeepSeek-evolved harness 能让 GLM ID +7.3，但让 GPT-5.4 ID -3.6；

GPT-5.4-evolved harness 能让 GPT-5.4 ID +5.5，但让 GLM ID -7.3；

OOD 结果更不稳定，多个 cross-backend OOD gain 为 0 或负数。

这说明 harness 更新并不是完全模型无关的。不同模型在 rollout 中暴露出的 failure surface 不同：

有的更容易暴露工具恢复问题，有的更偏向文本推理失败，有的更强调 artifact constraints 和 validation sufficiency。因此，一个 backend 上学到的 harness 修改，不一定适合另一个 backend。

这篇工作的意义

自进化目前已成为大家押注的下一代技术范式迁移的主流方向，SEAGym 从更本质的智能体环境构建的角度出发，

将自进化过程建模为清晰的强化学习过程，提出了评测自进化 Agent 的统一系统框架和协议。

SEAGym 不再只关注智能体任务完成的结果，而是从过程出发去研究智能体的进化机制和规律。

它将研究问题从「最终 Agent 的成功率是多少？」推进到：不同自进化机制到底更新了 Agent 的哪个部分？是否存在 OOD 泛化？是否遗忘了旧能力？性能提升是否伴随更高成本？

随着 Agent 被用于软件工程、数据分析、科研自动化、网页操作和长期任务执行，这类问题会越来越重要。一个能够持续修改自身工具、memory 和 middleware 的 Agent，如果没有过程级评测，很可能在某些任务上表现更强，同时在另一些任务上悄悄引入不可见的风险。

SEAGym 的价值就在于，它让这些风险变得可观测、可回放、可诊断。

未来方向

论文也指出，当前 SEAGym 的实验主要集中在 Terminal-Bench 2.0 和 HLE 两类任务源上，覆盖了 execution-heavy 和 reasoning-heavy 场景，但还没有扩展到 web interaction、desktop interaction、long-horizon software engineering、data-analysis workflows、多智能体协作和 continuous online task streams 等更复杂场景。

此外，SEAGym 的多视角评测带来了明显的 cost /coverage tradeoff。保存多个 snapshot，并在 validation、ID、OOD、replay 等视角上重复评测，会消耗大量 token 和时间。未来需要研究更高效的 snapshot selection、adaptive replay 和 budget-aware evaluation。

总体来看，SEAGym 为自进化 LLM Agent 提供了一套更细粒度的评测语言：它不再把 Agent 视为一个固定模型，而是把其 prompt、memory、tools、middleware 和 runtime state 共同构成的 harness 视为会随经验变化的对象。对于理解下一代长期运行 Agent 的可靠性、可迁移性和安全性，这是一项基础设施式的工作。

团队介绍

SEAGym 由清华大学自动化系团队提出，作者包括 Congjie Zheng、Chuanyi Xue、Bin Liang、Jun Yang 和 Changshui Zhang。

其中，Congjie Zheng 与 Chuanyi Xue 为共同第一作者，Jun Yang 与 Changshui Zhang 为通讯作者。

团队长期关注大模型智能体、agent harness、自进化机制和智能体评测基础设施等方向。

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com