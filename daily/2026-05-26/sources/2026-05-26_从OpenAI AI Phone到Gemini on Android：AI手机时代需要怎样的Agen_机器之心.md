---
publish_time: 1779796081
---

# 从OpenAI AI Phone到Gemini on Android：AI手机时代需要怎样的Agent Harness？

> 原文链接：https://mp.weixin.qq.com/s/I2ztL6sFiHGxAiCfh_FTqg
> 公众号：机器之心

过去一年，AI 与手机的关系正在被重新定义：OpenAI AI Phone / AI Agent Phone 把「AI 原生手机」推到台前，Gemini on Android 也在把系统级助手从问答带向跨 App、多步骤任务协助。

这些信号指向同一个趋势：

AI 不再只是聊天框里的回答者，而是正在进入手机这个最日常、最复杂、也最具状态性的计算环境。

腾讯混元

牵头，联合 The Chinese University of Hong Kong、The Chinese University of Hong Kong, Shenzhen、Tsinghua University

等机构的

最新研究 PhoneHarness:

A Mixed-Action Orchestration Harness and Benchmark for Phone Agents across CLI, GUI, and MCP Tools 关注一个更基础的问题：

当 AI 真正在手机上行动，我们如何让它真正完成任务，并验证它确实完成了？

作者团队给出的结论是：

手机 Agent 的核心不只是「更会点屏幕」，而是能根据任务选择 CLI、GUI、MCP 工具等合适的行动面；

真实手机 workflow 需要可验证的副作用：文件是否生成、设置是否改变、邮件 / 日历对象是否真的创建，都不能只靠模型口头回答；

PhoneHarness 提供 mixed-action 执行 harness；PhoneHarness Bench 则用 trace、系统状态、App 结果和安全策略评估任务是否真的完成。

论文地址：

https://phoneharness.github.io/assets/paper.pdf

项目主页：https://phoneharness.github.io/

GitHub：https://github.com/PhoneHarness/PhoneHarness

HuggingFace Dataset：https://huggingface.co/datasets/PhoneHarness/phoneharness-bench

先看三个执行片段：手机 Agent 不只是点屏幕

下面三个 demo 展示了 PhoneHarness 想表达的核心差异：真实手机任务往往不是一条更长的 GUI 点击链，而是 CLI、GUI、MCP-style tools 与 verifier 共同组成的执行 workflow。

Demo 1｜CLI-first：先读设备状态，再决定是否进入 GUI

Demo 2｜Mixed workflow：MCP 检索 + GUI 执行 + verifier 复核

Demo 3｜Virtual display：后台 GUI 执行与过程留痕

先把第一个问题说清楚：手机 Agent 真的「做了」吗？

在很多手机 Agent 评测里，任务被拆成一连串 GUI 操作。模型观察屏幕，决定下一步点哪里、滑哪里、输什么。如果最后 UI 状态看起来对，就算任务完成。

这套范式当然有价值。毕竟，手机确实是一个强 GUI 环境，真实 App 的搜索、浏览、点击和输入都需要视觉 grounding。

但对于 AI 手机时代的 Agent 来说，

只会 GUI 操作远远不够。

传统 GUI-centric 视角：

把手机任务看成 screenshot → tap /swipe/type；

视觉感知几乎是所有动作执行的前置操作；

更适合单 App、强视觉、低副作用任务。

PhoneHarness 的 mixed-action 视角：

把手机任务看成跨 CLI、GUI、MCP 工具的完整 workflow；

评估重点不是「看起来完成」，而是副作用是否真实发生、trace 是否可审计；

更适合系统设置、文件、搜索、邮件、日历和跨 App 任务。

例如，「查一个 App 内的信息，再结合网页搜索补充背景，并整理成邮件」这类任务，不是一个更长的点击链。它同时包含 App 内 GUI 交互、外部信息检索、文本处理、邮件副作用，以及最终结果验证。

如果评测只看最终回答，就会漏掉最关键的问题：模型到底有没有查对来源、有没有真的创建文件、有没有真的发出邮件、有没有绕过了应该被确认的高风险操作？

核心判断：

PhoneHarness 的出发点很直接：

手机 Agent 的评测不能只问「它会不会点屏幕」，而要问「它能不能在真实手机环境里把一件事做完，并留下可验证证据」。

PhoneHarness：让手机 Agent 的行动空间不止 GUI

PhoneHarness 的核心不是再造一个 GUI 点击器，而是

把手机任务放进一个混合动作空间里。

关键区别：

问题不是「纯 GUI 理论上能不能做」，而是「纯 GUI 是否是可靠、高效、可验证的动作抽象」。真实手机 workflow 往往同时跨越系统状态、App 界面、文件、网页、邮件、日历和安全边界。GUI 是重要入口，但不应该是唯一入口。

因此，mixed-action 不是给 GUI agent 加几个外挂工具，而是让 agent 在执行过程中为不同子目标选择合适的 action surface：能用确定性命令读取状态，就不必反复点设置页；必须进入 App 内完成交互时，才交给 GUI；需要外部信息、文件处理或结果复核时，则调用 host-side tools 或 verifier。

为什么 mixed-action 比纯 GUI 更稳

PhoneHarness 架构图：host-side orchestration 与 Android device-side execution 共同构成 mixed-action harness。

在 PhoneHarness 中，agent 可以在三类行动面之间切换：CLI /device-side commands、GUI delegation、以及 MCP-style host tools。

图解：PhoneHarness 的三类行动面

PhoneHarness 的 mixed action space：CLI、GUI 与 MCP-style tools 在同一个 phone-agent loop 中共存。

这意味着，PhoneHarness 里的 agent 不必把所有任务都硬塞进 GUI 点击链。它可以判断：什么时候该走系统命令，什么时候该交给 GUI worker，什么时候该调用搜索、文档、邮件、日历等工具。

这种设计更接近 AI 手机时代的真实需求。AI 手机不是「在手机里放一个聊天机器人」，而是让智能体能在复杂手机环境里理解目标、选择行动、执行任务，并产生可检查的结果。

PhoneHarness Bench：如何构建并验证手机 workflow

有了 mixed-action harness，还需要一个能真正检验执行结果的 benchmark。原因很简单：对手机 Agent 来说，

能行动不等于真的完成了任务。

PhoneHarness Bench 建立在 PhoneHarness 之上，不把任务写成抽象问答题，而是写成一段可以执行、记录和复核的 phone workflow。Agent 在执行过程中会留下截图、CLI / MCP 操作、文件变化、系统状态和 App 侧结果；benchmark 再通过 task-specific verifier 判断任务副作用是否真实发生。

Bench 的关键：

PhoneHarness Bench 不问「模型有没有说自己做完」，而是看「任务证据链是否支持它真的做完」。这也是它区别于纯问答式评测和纯 GUI 状态评测的关键。

PhoneHarness Bench 如何验证任务完成

Bench 是怎么构建的？

每个 PhoneHarness Bench task 都包含一个用户目标、一组可调用行动面，以及一个面向副作用的 verifier。这样，benchmark 评估的不是单步 GUI 操作，而是完整 workflow：任务输入、agent loop、混合动作执行、trace 记录、结果验证和失败归因。

PhoneHarness Bench 的任务分布：覆盖 device/system、single-app GUI、tool-assisted workflow 与 cross-app workflow。

为什么这能帮助分析失败？

这条链路让失败不再只是一个笼统的「没做对」。我们可以进一步区分：是外层 controller 没有规划好，是 GUI worker 没有点对，是工具调用失败，是环境不稳定，还是 verifier 没有看到预期副作用。

代表性执行轨迹：截图、CLI / MCP 操作卡片与 verifier 信号共同构成可审计证据链。

实验发现：收益来自 mixed-action routing，不是单纯更会点屏幕

在论文实验中，我们没有把 PhoneHarness 描述成一个「所有场景都更强」的 GUI agent。相反，实验更清楚地显示了它的边界和价值。

PhoneHarness 的收益主要来自那些存在确定性路径、工具辅助路径或可验证副作用的任务。比如设备状态查询、文件处理、网页检索、日历 / 邮件 / 文档相关 workflow，以及需要跨行动面组合的手机任务。

对于纯 GUI-heavy 的任务，视觉 grounding、权限弹窗、登录状态、广告、搜索结果不稳定等问题仍然会带来挑战。

实验解读：

这个结论反而更重要：

手机智能体的未来不是「把 GUI 点击模型做得更大」，而是要让 agent 学会选择合适的行动面，并让每一步执行都能被验证。

mixed-action affordance 任务上的行动空间拆解。

不同任务类型下的执行步数，辅助理解效率差异。

当 AI 手机真正到来，我们会看到什么新瓶颈？

OpenAI AI Phone 和 Gemini on Android 之所以值得关注，不只是因为「大厂要做 AI 手机」。更重要的是，它们共同指向了一个产品范式变化：

手机正在从 App-centric device 走向 Agent-centric device。

在 App-centric 时代，用户自己负责拆解任务：打开哪个 App、点哪里、复制什么、搜什么、确认什么。

在 Agent-centric 时代，

用户表达目标，agent 负责调度行动。

AI 手机时代的新瓶颈

PhoneHarness 的切入点正是在这里：

AI 手机时代需要的不只是更强的模型，还需要能承载真实执行的 harness，以及能验证执行结果的 benchmark。

PhoneHarness 和 PhoneHarness Bench，到底推进了什么？

PhoneHarness 与 PhoneHarness Bench 的分工

这两个产物是相互依赖的。

没有 harness，benchmark 很难覆盖真实混合任务。没有 benchmark，harness 的执行能力也很难被系统性评估。

如果说过去手机 Agent 的竞争更像「谁更会看屏幕点按钮」，那么 AI 手机时代真正重要的问题会变成：

谁能把真实手机 workflow 做完，谁能留下可信证据，谁能在安全边界内稳定执行。

PhoneHarness 回答的是「怎么让手机 Agent 真的行动」。PhoneHarness Bench 回答的是「怎么确认它真的做成」。

写在最后

AI 手机不是简单地把大模型塞进系统。它意味着手机从 App-centric device 走向 Agent-centric device：用户表达目标，agent 负责选择路径、调用工具、操作 App，并完成可验证的结果。

这背后的基础设施问题，比「模型会不会点屏幕」更复杂，也更关键。

PhoneHarness 和 PhoneHarness Bench 想推进的，正是这一层基础设施：

让手机 Agent 的行动空间更接近真实世界，也让评测更接近真实完成。

一句话总结：

AI 手机时代，关键问题不只是模型能不能理解屏幕，而是它能否在真实手机环境里选择正确行动面、完成可验证任务，并留下可审计的执行轨迹。

作者信息

共同一作：

Jason、Zhengyao Fang、Zhengyang Tang、Pengyuan Lyu。

完整作者：

Jason, Zhengyao Fang, Zhengyang Tang, Pengyuan Lyu, Xingran Zhou, Xin Lai, Fei Tang, Liang Wu, Yiduo Guo, Weinong Wang, Junyi Li, Yi Zhang, Yang Ding, Huawen Shen, Sunqi Fan, Shangpin Peng, Zheng Ruan, Anran Zhang, Benyou Wang, Chengquan Zhang, Han Hu.

机构：

Tencent Hunyuan; The Chinese University of Hong Kong; The Chinese University of Hong Kong, Shenzhen; Tsinghua University.

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com