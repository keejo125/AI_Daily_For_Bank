---
publish_time: 1788240119
link: https://mp.weixin.qq.com/s/qj8Pdhtng6lWyEvPvaSRQA
source: CSDN
status: confirmed
category: 国内
is_model_related: false
digest: |
  技术报告《openJiuwen: Beyond Static Harnesses for Long-Horizon Coding Agents》提出面向长程编码智能体的执行架构，刷新 SWE-bench Verified 与 Terminal-Bench 2.1 两项榜单 SOTA：在 500 个真实 GitHub issue 上取得 82.6%，在真实终端环境复杂指令集上斩获 87.19%。报告核心论点是：当团队用上同一批顶尖模型，驱动其运转的执行架构（harness）差异会显著影响成绩，为编码智能体从「模型能力」竞争转向「执行架构」竞争提供实证参考，并已落地于 WorkSwarm。
title: 再迎突破！openJiuwen技术论文刷新Coding多榜单SOTA，并在WorkSwarm落地
---

# 再迎突破！openJiuwen技术论文刷新Coding多榜单SOTA，并在WorkSwarm落地

来源：CSDN
原文链接：https://mp.weixin.qq.com/s/qj8Pdhtng6lWyEvPvaSRQA

2026 年，编码智能体的竞争正在悄悄换赛道。
过去两年，比拼的重心一直是模型——谁的推理更强、谁的代码补全更准。但当越来越多团队用上同一批顶尖模型，一个值得关注的问题浮出水面：
同样的大脑，换一套驱动它运转的执行架构，成绩到底能差多少？
针对以上问题，一篇名为《
openJiuwen: Beyond Static Harnesses for Long-Horizon Coding Agents
》的技术报告给出了强有力的参考，该报告结果直接
刷新了SWE-bench Verified和Terminal-Bench 2.1两大榜单的SOTA
——在500个真实GitHub issue构成的编程“黄金标准”中拿下82.6%，在真实终端环境复杂指令集中斩获87.19%，双双超越此前最强表现3个百分点以上。笔者了解到，报告背后的openJiuwen是华为 2012 实验室、华为云、终端、计算联合构建的开源 AI Agent 平台，报告同时指出其
Coding Harness核心能力已在面向办公、编程的蜂群智能体WorkSwarm中落地
，一键下载安装即可体验。
在
SWE-bench Verified
上，openJiuwen 与榜单最强系统使用同一款模型（Claude Opus 4.5），最终成绩却高出
3.4 个百分点
，达到
82.6%
；
在
Terminal-Bench 2.1
上，openJiuwen 以
87.19%
的准确率超越 Codex、Claude Code、Terminus 2 等一众强力对手，比官方榜首高出
3.39 个百分点
；
更关键的是一组"同模型"对照实验：换上与榜首 Claude Code、榜二 Terminus 2 完全相同的
Fable 5
模型，openJiuwen 依然拿到
84.04%
，反超 Claude Code 的 83.8%，比 Terminus 2（80.4%）高出
3.6 个百分点
。
同一个模型，差出来的分数，只能来自模型之外的那一层——
Coding Harness，即真正驱动编码智能体理解任务、调用工具、诊断错误、持续推进的执行框架。
论文地址：https://arxiv.org/abs/2608.27969
Coding Harness 的局限：长时复杂任务，既考验结构对开发
者是否友好，也考验运行时能否应对新情况
为什么很多 Code Agent 在演示视频里游刃有余，一到真实、复杂、长链路的任务里就掉链子？
根子在于：多数编码智能体沿用的仍是一套"静态"的 Harness——写死的流程、写死的工具列表、写死的上下文策略。这套机制处理三五步的短任务问题不大，但长程编码任务会带来两方面的压力，让它的短板逐渐显现：
结构上越来越复杂，对开发者不友好。
一个编码 Agent 要用到的能力持续增多——安全策略、代码记忆、任务规划、上下文管理、语义反馈、子任务委派、多智能体协作。如果这些能力各自为战，开发者每新增一种能力都得读懂并改动整个执行内核：新功能牵一发而动全身，排查问题要在纠缠在一起的逻辑里来回跳转，维护成本随能力数量增加而显著上升。
运行时越来越动态
。任务推进过程中会不断冒出"事前无法预知"的新信息：代码改动后有没有新的语义错误、任务到底是真的完成了还是看起来完成了、上下文里哪些该留哪些该扔、这次踩过的坑下一次会不会重蹈覆辙。
一套只会按预设剧本往前走的 Harness，难以应对这些信息。
openJiuwen 把这两类压力概括为
Structural Composability（结构可组合性）
与
Runtime Adaptivity（运行时自适应性）
，并围绕这两个方向，重新设计了整套执行架构。
结构可组合性：执行内核稳定不变，能力模块可插拔扩展，对开发者友好
openJiuwen 的第一处关键设计，是把"能力"和"执行逻辑"彻底解耦——开发者不必啃透整个执行内核，就能像搭积木一样组装、扩展系统，这正是结构可组合性对开发者友好的核心所在。
openJiuwen Coding Agent 整体架构：Inner Loop（观察—推理—行动—验证）与 Outer Loop（目标—计划—执行—评估—更新）之间，由一层可插拔的 Rail 组成稳定执行核心
Inner Loop / Outer Loop：同一套执行内核，覆盖从单个 Agent 到团队协作的所有场景。
不论是独立工作的单个 Agent、被委派处理子任务的 Agent，还是 Swarm 团队里的一名成员，跑的都是同一套"内层负责观察—推理—行动—验证，外层判断要不要再来一轮"的执行引擎。开发者不需要为每一种使用场景重新设计一套调度逻辑。
Rail 机制：能力即插件，想接就接。
安全策略、记忆管理、任务规划、工具治理、语义理解、人机交互……这些能力全部以 “Rail” 的形式挂载在执行生命周期的固定钩子上，通过优先级决定谁先谁后、谁能覆盖谁。
给 Agent 新增一种能力，只需要声明一个新的 Rail，完全不用改动执行内核。
这意味着很低的扩展成本：想加一条自定义规则、接一个内部工具，不必读懂整个框架源码，照着 Rail 的接口写一个 handler 即可。
Swarm Flow：不是一套固定的多智能体架构，而是一组可自由拼装的编排算子。
它提供
budget()
（查询剩余预算）、
parallel()
（并发派发并等待收齐）、
compact()
（过滤空结果）、
pipeline()
（流式传递结果）、
agent_session()
（维护有状态会话）、
human()
（引入人工兜底）等算子，最后以
return
收口。示例中，一个编码 Agent 用它们拼出了"查预算 → 并行生成 → 过滤 → 流式复核 → 仲裁 → 必要时人工 → 返回"的流程——但这只是众多拼法之一，
开发者可以按自己的任务自由重排、增减这些算子
，不必绑定某一种协同架构。
Swarm Flow 编排示例：
budget()
查询预算 →
parallel()
并行生成候选 →
compact()
过滤空结果 →
pipeline()
流式复核 →
agent_session()
有状态仲裁 → 必要时
human()
人工兜底 →
return
返回结果。
运行时自演进：让编码 Agent 真正学会"边做边学"
架构再清晰，如果 Agent 不能根据执行中出现的新信息调整，长任务依然容易出问题。围绕这一核心问题，openJiuwen 给出了四套配套机制：
Goal Mode（目标驱动）：
不再是"跑够固定步数就收工"，而是持续评估目标是否完成、是否被卡住，并把"完成判断"和"预算耗尽"严格区分开——既不会明明做完了还在空转，也不会明明卡住了还在硬撑预算。
LSP-Driven Passive Feedback（语言服务器被动反馈）：
每次代码改动，语言服务器产生的类型错误、悬空引用等诊断信息会被自动过滤、去重、排序后主动推送给下一步决策，不必等 Agent 自己想起来去查——相当于配了一位随时在线的 Code Reviewer。
Context Management（动态上下文管理）：
不再是把系统提示词加完整对话历史直接塞进上下文，而是根据实时压力做渐进式压缩、结构化摘要、死循环折叠，甚至把体积过大的内容卸载到外部存储、按需检索取回——避免长任务被上下文窗口拖累。
Self-Reflection（跨任务经验沉淀）：
任务完成后，系统会从执行轨迹中提炼可复用的经验存入经验库，供未来相似任务检索调用——相当于给 Agent 配了一本自己越写越厚的"复盘笔记"。模型参数没有变，但 Agent 会随着使用不断积累经验。
这四套机制彼此关联，构成一个此消彼长的权衡系统：更丰富的上下文能带来更好的决策，却会挤占有限的上下文预算；更严格的完成判断能减少"假装做完"，却要多付出评估成本。
openJiuwen 的价值，正是把这些原本要靠工程师逐个项目摸索的取舍，沉淀成了可配置、可组合的工程能力。
约束优化视角下的运行时自适应机制：在 Context Construction（上下文构建）、Diagnostic-Feedback Injection（诊断反馈注入）、Acceptance & Stopping（接受与停止）三个维度上，系统不断向"可行且理想"的运行时配置区域逼近。
Benchmark：SWE-bench Verified 与 Terminal-Bench 2.1 双双刷新 SOTA
openJiuwen 在两个差异极大的基准上系统评测了这套架构。
SWE-bench Verified
（500 个源自真实 GitHub issue 的修复任务，考验仓库级长程软件工程能力）：openJiuwen 使用 Claude Opus 4.5，
Resolved 82.6%
，超过当前榜单最强的同模型系统（79.2%）3.4 个百分点。值得注意的是，榜单最强的对比系统用的同样是 Claude 4.5 Opus——
同样的模型，差出来的 3.4 个百分点，只能来自 Harness 本身。
Terminal-Bench 2.1
（89 个容器化终端任务，覆盖软件工程、系统运维、数据处理、模型训练与安全等更广泛场景）：openJiuwen 使用 GPT-5.6 Sol，
Accuracy 87.19%
，超过官方榜单最强结果（Claude Code + Fable 5，83.8%）3.39 个百分点，超过 Codex、Claude Code、Terminus 2 等多个强力系统。
同时还有一组"模型对齐"实验：把 openJiuwen 换成与榜首、榜二完全相同的 Fable 5，成绩依然是
84.04%
，比 Claude Code + Fable 5 高 0.24 个百分点，比 Terminus 2 + Fable 5 高出 3.64 个百分点。这组对比排除了"模型强弱"这个混淆变量——即便模型完全一致，Harness 本
身的贡献依然十分明确。
数据分析：优势来自架构的两个设计维度
总分好看只是结果，把总分拆开看更有意思——正好能看出 Structural Composability 和 Runtime Adaptivity 这两条设计主线各自兑现了多少。
证据一：细看分类目，openJiuwen 在"工具密集型"任务上优势明显——这正是结构可组合性的红利。
在同样使用 Fable 5 的模型对齐设置下：
file-operations（文件操作）
：openJiuwen 0.76，Claude Code 0.56，Terminus 2 0.52；
system-administration（系统运维）
：openJiuwen 0.889，Claude Code 0.778，Terminus 2 0.844；
换成主力配置 GPT-5.6 Sol 后，system-administration 冲到
0.956
，software-engineering 达到
0.908
，data-science 达到
0.950
。
这几类任务高度依赖工具——反复读写文件、操作终端、核对环境状态。openJiuwen
开箱即用的操作型工具
加上 Rail 提供的统一执行接口，让 Agent 不必为每个任务临时现造工具，省下的执行轨迹能更多用在推理和验证上——结构可组合性由此兑现成了具体
的分数差距。
模型对齐设置（均使用 Fable 5）下，openJiuwen 在 data-processing、debugging、security、system-administration、scientific-computing、file-operations 六大类目上的表现均优于或接近 Claude Code、Terminus 2，其中 file-operations 优势最为明显（0.76 vs 0.56 / 0.52）。
证据二：任务越拖越长，优势越明显——这是运行时自适应性在起作用。
把 SWE-bench Verified
的 50
0 个任务按预估修复时长切成四段，只对比同样使用 Claude Opus 4.5 的系统：
耗时最短的两档，openJiuwe
n 表
现最优；在最考验长程执行的 1–4 小时档，拿到 52.38%，逼近成绩最好的 live-SWE-agent（54.76%）。
值得注意的是 mini-swe-agent 的一个反常现象：同样是 Opus 4.5，
推理力度调到 high 反而比调到 medium 更差
（35.71% vs 42.86%）——推理力度越高，模型花在思考上的 token 越多，会挤占长任务里本就有限的上下文窗口。而 openJiuwen 同样用 high 推理力度，却在这一档冲到 52.38%，比 mini-swe-agent 的两种设置都明显更高。
这背后是 Context Management 机制在起作用
：它会根据实时压力动态取舍该留什么、该压缩什么，让更深的推理不必以更少的有效上下文为代价——这正是运行时自适应性要解决的问题：能否实时消化不断累积的信息，而不是被
它拖住手脚。
从论文到应用：能力开源并集成至WorkSwarm，也进入华为云码道
这篇论文的价值不只是刷新了两个榜单，而是
这套架构从设计之初就是为了被真正用起来
——它已经开源，并封装进了可以直接安装使用的产品。
对开发者而言
，openJiuwen SDK 把结构可组合性落到了实处：Rail 机制让你无需读懂整个框架源码就能插入自定义能力；Inner Loop/Outer Loop 统一的执行语义，让单 Agent 脚本可以平滑扩展为多智能体 Swarm 团队；Goal Mode、LSP 被动反馈、上下文管理等工程能力开箱即有。
对普通用户而言
，WorkSwarm 支持 HarmonyOS / Windows / Mac 一键安装下载。打开应用后像聊天一样描述需求，Agent 会自动读文件、搜代码、跑 Shell、装依赖、改代码、跑测试，直到任务完成。
驱动它的，正是拿下 SWE-bench Verified 82.6% 与 Terminal-Bench 2.1 87.19% 的同一套 openJiuwen 架构。
这也是 openJiuwen 团队反复强调的一件事：
Coding Harness 不该只掌握在少数团队手中，它应该像操作系统一样，开发者能扩展，普通用户能直接用。
同时，openJiuwen社区与
华为云码道
深度协同，作为码道的社区联创版本，也持续将开源框架中的优秀能力集成到码道中。
WorkSwarm 官网
：
https://www.openjiuwen.com/workswarm，
支持
HarmonyOS / Windows / Mac 一键下载安装，安装后即可通过自然语言对话方式驱动 Agent 完成任务。
结语：编码智能体竞争的关键已不仅是模型能力
Terminal-Bench 2.1 和 SWE-bench Verified 的难点在于，Agent 必须在真实环境里连续做对很多件事：理解任务、诊断错误、管理上下文、判断何时收手、把结果真正交付出来。模型决定的是 Agent 的基础智力，而 openJiuwen 用两个榜单证明的是：
真正决定 Agent 能走多远的，是那套包裹在模型外面、看不见却始终在起作用的 Coding Harness。
这
一次，openJiuwen 论文公开、代码开源、产品可装。从一篇技术论文，到两个权威基准双双刷新 SOTA，再到一次下载安装就能用上的桌面体验，验证的始终是同一件事——
Harness，不该只活在论文和榜单里，它应该装进每一个人的电脑。
一键下载安装 WorkSwarm，立即体验吧！
相关资源：
论文地址：https://arxiv.org/abs/2608.27969
openJiuwen 官网：https://www.openjiuwen.com/
WorkSwarm GitHub：https://github.com/openJiuwen-ai/jiuwenswarm
WorkSwarm AtomGit：https://atomgit.com/openJiuwen/jiuwenswarm
Swarm Skills Hub：https://swarmskills.openjiuwen.com/
