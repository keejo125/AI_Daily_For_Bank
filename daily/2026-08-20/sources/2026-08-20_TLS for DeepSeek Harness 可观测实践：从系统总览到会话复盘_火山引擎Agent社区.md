---
publish_time: 1787223900
status: confirmed
category: 国内
is_model_related: false
digest: |
  火山引擎介绍 TLS for DeepSeek Harness 可观测插件，将 DSH 会话中的模型请求与工具调用转为 OpenTelemetry Trace 上报到 TLS 日志服务，开发者无需改使用方式即可从系统总览下钻到单次请求与会话复盘。插件将执行过程组织为 agent.turn、llm.request、tool.call 三类核心 Span。
  文章以"分析 DSH 源码并梳理核心设计"的真实任务演示分析路径：总览感知（近 7 天 5 会话、33 次模型请求、45 次工具调用、约 119 万 Token）→ Trace 定位→ Span 分析→会话复盘（示例两轮共 115 万 Token，主要成本来自输入上下文）。插件监听 DSH EventLog 增量转 Span，并面向 Codex、Claude Code、OpenCode、TRAE、Cursor、Pi 等 Agent 适配；TLS 正在建设基于 GenAI 语义检测与 TLS Agent 大模型分析的轨迹异常检测与智能归因能力。
link: https://mp.weixin.qq.com/s/LJMHb4nwDOqIUqDL795dcw
source: 火山引擎Agent社区
title: TLS for DeepSeek Harness 可观测实践：从系统总览到会话复盘
---

# TLS for DeepSeek Harness 可观测实践：从系统总览到会话复盘

> 原文链接：https://mp.weixin.qq.com/s/LJMHb4nwDOqIUqDL795dcw
> 来源：火山引擎Agent社区

点击上方
👆
蓝字
关注我们！
TLS for DeepSeek Harness 可观测插件，将 DSH（DeepSeek Harness）会话中的模型请求和工具调用转换为 OpenTelemetry Trace，并上报到火山引擎日志服务 TLS。开发者无需改变原有使用方式，就能从系统总览一路下钻到单次模型请求和工具调用，定位性能、成本与执行问题。
💡 本文以一次真实的“分析 DSH 源码并梳理核心设计”任务为例，演示如何沿着“总览感知 → Trace 定位 → Span 分析 → 会话复盘”的路径分析 Agent 执行过程。
一
为什么需要 Agent 可观测
一次 Coding Agent 任务通常包含多轮模型请求、代码检索、文件读取、命令执行和结果整理。终端输出虽能看到执行片段，但很难快速回答：
当前系统是否出现请求、成本或性能异常？
哪个会话、哪轮调用消耗了大部分时间和 Tokens？
模型生成了什么工具调用，工具实际执行了什么？
Agent 是否重复读取文件、反复检索或在失败后重试？
问题来自模型、上下文、工具，还是运行环境？
TLS 将这些执行过程组织为三类核心 Span：
agent.turn
表示一轮 Agent 执行，
llm.request
表示一次模型请求，
tool.call
表示一次工具调用。开发者可以先看系统整体状态，再逐层下钻到需要分析的会话、调用链和 Span。
agent.turn
├─ llm.request
├─ tool.call
├─ llm.request
└─ tool.call
二
接入与快速验证
接入前需要准备：
Node.js 版本不低于 22.13；
本地已经可以正常运行 DSH；
已在 TLS 创建 DSH 可观测应用；
已获取 Region、Trace Topic ID，以及 API Key 或 AK / SK。
一键安装
使用 API Key：
npm
exec
-
y \
--registry=https://registry.npmjs.org/ \
--package=@volcengine/tls-observer-dsh-install@latest \
--tls-observer-dsh-install install \
--profile web \
--non-interactive \
--force \
--region <region> \
--trace-topic-id <trace-topic-id> \
--api-key <api-key> \
--capture-content true
也可以将
--api-key
替换为
--ak <tls-ak> --sk <tls-sk>
，使用 AK / SK 鉴权。
安装器通过 DSH 官方 Profile 插件机制完成安装，不用修改 DSH 源码或安装目录。TLS 配置会持久化到
$DSH_HOME/.env
；未设置
DSH_HOME
时，默认路径为
~/.dsh/.env
。
重启并验证
安装完成后，重启 DSH：
dsh
web
然后发起一个会同时触发模型请求和工具调用的任务，例如：
帮我分析一下 DSH 源码，梳理核心设计。
任务完成后进入 TLS 的 AI 观测应用。Trace 通过
BatchSpanProcessor
批量上报，页面出现数据前可能有短暂延迟。
插件卸载
npm
exec
-
y
\
--registry=https:
//r
egistry.npmjs.org/ \
--
package
=
@volcengine
/tls-observer-dsh-install
@latest
\
--tls-observer-dsh-install uninstall \
--profile web
卸载只会从指定 Profile 移除 TLS Observer 插件，并在没有其他 Profile 使用时移除安装器管理的配置块；不会删除 DSH 会话数据，也不会修改无关 Profile 配置。
三
场景化分析
一次源码分析任务为什么消耗较高
示例任务要求 DSH 分析自身源码并梳理核心设计。对应会话包含两轮 Agent 调用，总耗时约 6 分钟，总 Tokens 超 115 万。接下来不直接翻阅全部调用日志，而是沿着 TLS 提供的分析路径逐步定位成本和执行过程。
先看总览：第一时间感知系统状态
总览大盘围绕 Agent 开发者最关心的四个板块组织信息：
板块
先回答什么问题
请求详情
当前有多少会话、对话轮次、模型请求和工具调用？请求量是否发生变化？
成本消耗
总 Tokens 由输入、输出、Cache Read、Reasoning 等哪些部分构成？
工具情况
哪些工具调用最频繁、最慢或失败最多？
模型性能
当前使用哪些模型和 Provider？它们的调用量与 P90 耗时如何？
在示例环境中，近 7 天共记录 5 个会话、6 轮对话、33 次模型请求和 45 次工具调用，总 Tokens 约 119 万。输入 Tokens 占绝大部分，说明后续分析应优先关注上下文规模和重复读取，而不是只看最终输出长度。
图 1：请求与成本总览，
从会话、模型请求、工具调用和 Token 趋势感知系统状态
图 2：工具与模型性能总览，
对比调用频次、失败情况与 P90 耗时
从 Trace 列表找到目标调用链
总览用于发现异常，Trace 列表用于定位具体的一轮 Agent 执行。
TLS 从每轮 Trace 根 Span 的
gen_ai.input.messages
和
gen_ai.output.messages
中提取 GenAIInput、GenAIOutput，并与状态、耗时、总 Tokens、输入 Tokens 一同展示。开发者可直接按输入内容搜索任务，不必提前记住 Trace ID。
在示例中，通过“帮我分析一下 DSH 源码，梳理核心设计”即可找到主调用链。该 Trace 执行正常，但耗时约 5 分 57 秒，总 Tokens 为 1,045,634，其中输入 Tokens 为 1,033,719。列表已经揭示第一个分析结论：主要成本来自输入上下文，而非模型最终输出。
图 3：Trace 分析列表，通过根 Span 的
GenAIInput、GenAIOutput 快速定位目标调用链
下钻 Trace：分析模型与工具的执行过程
点击目标 Trace 后，页面按调用类型识别 LLM、Tools 和其他 Span，并通过调用树和耗时瀑布展示父子关系。开发者可以快速比较各步骤耗时，判断时间主要消耗在模型请求还是工具执行。
选择
llm.request
后，TLS 会提取并格式化
gen_ai.input.messages
，按 user、assistant 等角色展示消息，同时保留原始 JSON 视图。面对包含 System Instructions、历史消息和长上下文的模型请求，开发者无需直接阅读一整段 JSON，就能定位本轮真正的用户输入及上下文组成。
图 4：Trace 调用链、执行耗时与模型输入详情
gen_ai.output.messages
同样会按消息类型格式化展示。对于上游明确上报的 Reasoning 内容和 Tool Call，页面会分别呈现，并将工具的
name
、
arguments
、
command
、
path
、
pattern
、
Call ID
等字段展开。
在示例调用链中，可以看到 Agent 先通过
bash
确认工作目录，再使用
glob
、
read
等工具读取 DSH 包内文件。结合调用树中的耗时，可以进一步判断是否存在高耗时检索、重复读取或过多模型往返。
图 5：输出中格式化展示
上游提供的 Reasoning 与 Tool Call 参数
回到会话：复盘多轮 Agent 交互
一条 Trace 表示一轮 Agent 执行，一个 Session 可能包含多轮 Trace。会话分析按
gen_ai.conversation.id
聚合同一 DSH Session，并展示首次输入、末次输出、总 Tokens、调用链数量、耗时、模型和开始时间。
开发者可以按 Tokens、耗时或调用链数量排序，快速定位高成本、长耗时或多轮会话。示例会话的首次输入是“帮我分析一下 DSH 源码，梳理核心设计”，共包含 2 条调用链，总 Tokens 为 1,153,056。
图 6：会话分析按 Session 聚合调用链、
Token、耗时、模型及首次输入、末次输出
进入会话详情后，左侧按时间顺序展示每次 Agent 调用及对应的 Tokens、耗时；右侧展示当前调用的输入和输出。
示例中第一轮源码分析耗时 5 分 57 秒，消耗 1,045,634 Tokens；第二轮“简单总结，不要太长了”耗时 18.87 秒，消耗 107,422 Tokens。开发者既能从会话层理解多轮交互如何累积成本，也可以点击“调用链详情”回到对应 Trace，继续分析具体模型请求和工具调用。
这形成了一条完整的复盘路径：
Session 识别高成本会话
↓
逐轮查看 Agent
Input
/ Output
↓
选择异常轮次
↓
下钻 Trace 和
Span
细节
图 7：会话详情逐轮展示 Agent 输入、
输出、Token 和耗时，并支持下钻调用链详情
从数据形成优化动作
结合示例中的总览、Trace 和 Session，可以得到四项直接可执行的分析方向：
优先检查上下文规模：
主调用链超过 104 万 Tokens，其中输入约 103 万，成本主要来自输入上下文。
检查重复读取与检索：
工具调用中
read
、
glob
、
bash
较多，可结合调用树确认是否重复访问相同文件或扩大不必要的检索范围。
区分模型与工具耗时：
总览分别提供模型、Provider 和工具的 P90 耗时，Trace 再定位到具体 Span，避免仅凭整体耗时猜测瓶颈。
比较多轮调用收益：
会话详情把每轮输入、输出、Tokens 和耗时放在同一时间线上，可判断追加追问是否带来与成本匹配的结果。
对应的优化动作可能包括：缩小文件注入范围、减少重复上下文、收敛检索路径、优化 Prompt 的完成条件，或调整模型与 Provider。优化后可以重新执行同类任务，再用相同指标验证耗时和成本是否改善。
四
数据如何进入 TLS
插件监听 DSH 已提交的 EventLog，并将事件增量转换为 OpenTelemetry Span：
DeepSeek
Harness EventLog
↓
TLS Observer Plugin
↓
OpenTelemetry GenAI Trace
↓
TLS Trace Topic
↓
总览 / Trace / 会话 / Token 分析
主要事件映射如下：
DSH 事件
TLS Span 行为
turn/start
创建
agent.turn
根 Span
step/start
创建
llm.request
Span
tool/call
创建
tool.call
Span
assistant/message
补充模型输出并结束对应 LLM Span
tool/result
补充工具结果、状态并结束 Tool Span
llm/retry
记录可恢复重试信息
turn/end
结束本轮 Agent Trace 并触发非阻塞刷新
插件不会逐条上报流式
assistant/chunk
。第一个有效输出分片用于计算首包时间，完整输出结束后再生成 LLM Span。Trace 上报失败不会中断当前 DSH 会话。
五
内容采集与数据边界
正文内容采集默认关闭。本文安装示例显式设置
--capture-content true
，用于展示：
用户输入、模型输出和 System Instructions；
Tool Definitions、工具参数和执行结果；
部分与执行相关的本地路径；
Trace 的输入、输出，以及会话的首次输入、末次输出。
关闭内容采集后，TLS 仍保留 Trace 层级、耗时、状态、模型、Provider、Token、Session 关系、重试和错误信息，但不再上报 Prompt、回复和工具正文。
🔒 Prompt、模型输出、工具参数和结果可能包含源代码、路径或业务数据。启用内容采集前，应先确认数据安全要求。配置只影响新产生的 Trace，历史数据无法补齐。
Token 统计遵循上游实际数据：
Total
Tokens
=
Input Tokens + Output Tokens
Cache Read 和 Cache Creation 已包含在输入 Tokens 中，Reasoning Tokens 已包含在输出 Tokens 中，不应重复累加。只有上游提供独立计数字段时，TLS 才能展示对应指标；字段缺失时显示为 0 属于正常情况。
六
从 DSH 扩展到
TLS Agent 可观测体系
DSH 只是 TLS Agent 可观测体系的适配对象之一。TLS 还面向 Codex、Claude Code、OpenCode、TRAE、Cursor、Pi 等 Coding Agent 提供适配能力。
不同 Agent 可能通过 Hooks、插件事件、会话日志或 EventLog 暴露运行数据。TLS 统一的不是采集入口，而是采集后的 Session、Agent、LLM、Tool、Token、Error 模型，以及总览、Trace、会话、成本、工具和模型分析体验。
因此，开发者可以用一致的路径处理不同 Agent 的问题：先从总览感知系统状态，再定位 Session 或 Trace，最后下钻到模型请求和工具调用。
通过这套观测路径，开发者无需从海量终端输出中猜测 Agent 做了什么，而是可以从系统状态、会话成本、调用链结构和工具细节逐层定位问题，并用同一套数据验证优化结果。
七
轨迹异常检测与智能归因
TLS 正在建设面向 Agent 轨迹的异常检测与智能归因能力。目标是通过“低成本 GenAI 语义检测 + TLS Agent 大模型分析”的分层方式，让客户无需配置或仅需少量配置，就能开箱即用地发现异常、分析原因并获得可执行洞察。
平台首先基于 GenAI 语义规范，从 Trace 中提取模型请求、工具调用、执行结果、Token、延迟和错误等标准化信息，通过预置 Detector 持续检测 Token 异常增长、工具失败率上升、延迟分布漂移、完成率下降等信号。低成本检测覆盖全量 Trace，负责回答“哪些指标和执行轨迹值得关注”，避免对全部轨迹直接调用大模型。
当 Detector 发现异常后，平台会将重复出现的信号聚合为 Signal Group，并筛选代表性异常 Trace。TLS Agent 再结合正常对照、模型、工具、版本和运行环境进行深度分析，判断问题是否成立、影响范围有多大，并给出已验证原因、候选因素和处理建议。
全量 Trace
→ 低成本 GenAI 语义检测
→ Signal
Group
与代表性 Trace
→ TLS Agent 大模型分析
→ 洞察 Issue
最终，相关信号和 Trace 会沉淀为可持续跟踪的洞察 Issue，包含问题摘要、影响范围、发生趋势、代表性 Trace、归因证据和建议动作。客户无需先编写复杂规则或人工翻阅大量调用链，即可快速找到优先处理的问题，并进一步开展修复、观察或回归验证。
