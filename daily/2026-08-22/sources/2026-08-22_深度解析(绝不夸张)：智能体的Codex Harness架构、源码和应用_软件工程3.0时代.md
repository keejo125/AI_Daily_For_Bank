---
publish_time: 1787359238
status: confirmed
category: 国际
is_model_related: false
digest: |
  OpenAI 开源了可嵌入任意产品的 agent harness（智能体执行系统）Codex Harness，标志着 Codex 从“编码助手”向“智能体平台”的定位转变。文章深度拆解其源码：codex-core 是一个抵制膨胀的 Rust 核心（约33万行上限），通过 Thread/Session/Turn 三级状态管理驱动 agent loop，支持工具调用、并行执行、上下文压缩与人工审批；app-server 以 MCP 风格的 JSON-RPC 2.0 协议对外暴露，使任何应用都能以编程方式接入；安全体系采用“统一策略+三套原生沙箱（macOS Seatbelt / Linux bubblewrap / Windows restricted token）”的纵深防御，并将审批流作为协议一等公民。

  工程启示包括：单一核心多前端、协议优先的平台化、执行与判定分离、核心抵制膨胀、远程 exec-server 实现异 OS 执行。实测数据显示，在 ARC-AGI-3 基准上，保留推理+上下文压缩将 GPT-5.6 Sol 得分从13.3%提升至38.3%，输出 token 减少6倍，印证“harness 质量与模型质量同等重要”。
link: https://mp.weixin.qq.com/s/neYcA33iylKCh-CFpDUpbA
source: 软件工程3.0时代
title: 深度解析(绝不夸张)：智能体的Codex Harness架构、源码和应用
---

# 深度解析(绝不夸张)：智能体的Codex Harness架构、源码和应用

来源：软件工程3.0时代
原文链接：https://mp.weixin.qq.com/s/neYcA33iylKCh-CFpDUpbA

昨天我刚在AiDD峰会上做“未来每一个企业都需要构建或部署AgentOS”，有朋友让我看看下面这篇文章，OpenAI也急着宣布从"编码助手"到"智能体平台"，推出Codex Harness。这很可能是被DeepSeek Harness开源逼的。
因为昨天白天开会，忙得没有时间分析Codex Harness，只能熬夜分析Codex Harness，把深度分析的结果向大家做一个汇报。
（昨夜我做的Codex Harness文件Index分析）
（昨夜我做的Codex Harness 架构的深度分析）
大多数人认识 Codex，是通过 App、命令行或 IDE 插件。但在这三张"面孔"背后，藏着一个更重要的东西——
一个被 OpenAI 开源出来的、可嵌入任何产品的 agent harness
（智能体执行系统，即相当于我昨天分享的主题AgentOS）。
这篇文章将带你从"它是什么"一路拆到"它怎么做到的"。
一、 先弄懂三个词：Agent、Harness 与 Platform
在进入代码之前，我们需要先把几个被滥用得最厉害的概念讲清楚。
Agent（智能体）
指的是能自主完成任务的程序：它理解任务、收集信息、调用工具、做出决策。但请注意——一个 agent 绝不仅仅是"一个提示词 + 一个模型回复"。一个能真正干活的 agent，至少需要：
理解任务并维护跨时间的上下文；
按需检查外部信息（读文件、查库、搜索网页）；
调用工具并处理结果；
把进度暴露给用户；
在失败时恢复；
在需要时请求人工审批；
最终返回有用的结果。
Harness（执行系统 / 缰绳）
就是围绕模型构建的这整套"周围执行系统"。如果说模型是大脑，harness 就是大脑之外的一切：神经系统（上下文管理）、手脚（工具）、安全护栏（沙箱）、以及和外部世界对话的话筒（协议）。
Platform（平台）
意味着它不止服务于一个产品，而是可以被任何产品"嵌入"。
这就是 Codex 最核心的定位转变
：
它不是一个要你把工作搬进去的助手，而是一个可以被搬进你现有工作流里的引擎
。
🚗
一个通俗的类比
：传统编码助手像"整车销售"——你想用车，就得开它的车，坐它的座椅，用它的导航。而 Codex harness 像"发动机+底盘销售"——它把最难的动力总成（agent loop）给你，但方向盘、仪表盘、座椅（界面）、导航数据（上下文）、甚至交通规则（审批策略）都由你决定。你可以把它装进一辆货车、一台救护车、甚至一台拖拉机里。
二、一个反直觉的事实：App、CLI、IDE 只是三种"皮肤"
官方文档的第一句话就点破了这个事实：
"Most people know Codex through the App, Command-Line Interface, or IDE Extension. Those experiences are important, but they are only a few of the ways the same underlying system can be used."
这句话的潜台词是：
同一个codex-core，驱动了 ChatGPT App、VS Code/Cursor/Windsurf 扩展、命令行 TUI、非交互式codex exec，以及——通过codex app-server和官方 SDK——第三方产品自己应用里的 agent。
从产品视角看，这意味着什么？
意味着：
界面可以完全归应用所有
。一个客服团队不需要在聊天窗口里干活，他们可以在自己的客服控制台里，让 agent 看着客户的账户历史、产品日志和内部文档，起草回复。安全分析师可以在自己的告警队列里，让 agent 调查受影响服务，并在开工单前请求审批。
上下文和工具由应用决定
。应用可以暴露它自己的系统、文档、数据、操作——包括应用自己拥有的 MCP 服务。
运行边界由宿主应用设定
。agent 跑在哪台机器上、能访问哪些文件、哪些操作需要审批、结果如何回流到业务系统——全部可配置。
官方还给出了一个生动的示例
Relay
：一个虚构的货运运营应用。用户在仪表盘上选中一个异常包裹，点击"Compare recovery"，应用把上下文喂给 agent，agent 通过应用自有的 MCP 工具拉取最新运营数据、给出方案，而任何有后果的写操作（比如重新预订货运）都必须经过人工审批。
更震撼的是实测数据：
在 ARC-AGI-3 基准上，保留推理 + 上下文压缩把 GPT-5.6 Sol 的得分从 13.3% 提升到 38.3%，同时输出 token 减少了 6 倍。
harness 的设计不是"锦上添花"，而是能直接、可度量地改变模型任务表现的关键变量。
三、一次任务的旅程：建立直觉
在拆代码之前，让我们先以"用户视角"走一遍 Codex 处理一次任务的完整旅程。假设在终端里运行 codex "修复这个 bug"：
启动
：CLI 启动一个本地进程，内部启动一个 app-server（进程内模式），并创建一个
thread
（线程，即一次对话）。
开轮
：消息被包装成一个
turn
（轮次）——用户消息开始，agent 消息结束，这就是对话的基本单位。
采样循环
：
codex-core
读取当前上下文（世界状态、模型指令、工具清单），构建请求，流式调用 OpenAI Responses API。
工具调用
：模型说"我需要先看看代码"→ 触发
exec_command
工具 → 在沙箱里执行
ls
/
rg
/
cat
→ 输出回流给模型。
审批
：模型决定执行
git push
→ 命中执行策略 → 弹出审批请求 → 你点了允许。
应用补丁
：模型产出
apply_patch
调用 → 修改文件 → 生成 diff 展示给你。
结束轮次
：agent 总结完成 → turn 结束 → 整轮对话被持久化到 JSONL rollout 日志，并镜像进 SQLite。
整个过程中，模型的"大脑"只负责思考，而
谁在思考、用什么工具思考、能碰什么、必须问谁
——全部由 harness 决定。
下面我们进入源码，看这套系统到底由什么组成。
四、进入源码：一个 135 个 crate 的 Rust 工作区
codex-main 仓库的整体规模相当惊人：
指标
数值
Rust 源码文件
3,287 个
Rust 代码行数
约
146 万行
Cargo 工作区成员
135 个
TypeScript/JavaScript
705 个文件
GitHub Actions
工作流
30 个
三方补丁
约 20 个
整个仓库按职责划分为几大区域：
其中 codex-rs/ 是全部精华所在。它的组织结构本身就是一份架构说明书：
那就先上Codex Harness架构图
值得注意的是，codex-core 被明确标注为"
抵制增长
"的 crate——33 万行已经是上限，任何新功能都被要求放进行为可插拔的扩展 crate，而不是塞进核心。这是一个重要的工程哲学，我们后面会再谈。
五、心脏解剖：codex-core 的 Agent Loop
codex-core 的设计目标用一句话概括就是：
业务逻辑与 UI 完全解耦，任何前端都可以驱动它。
它通过三个层级组织所有状态：
5.1 线程 → 会话 → 轮次
ThreadManager
线程管理器，负责创建/恢复/fork/关闭线程，持有全局共享的
AuthManager
、
ModelsManager
、
EnvironmentManager
、MCP/插件/skills 服务。
CodexThread
对外暴露的线程句柄——提交操作、
start_or_steer_turn
（开始或引导一轮）、事件流、状态监视。
Session
线程内部的实际运行单元，跑一个
submission_loop
——这是整个 agent 状态机的入口。
submission_loop
本质上是一个基于消息通道的无限循环
：它从队列里读取 Op（操作）消息，然后分派处理。Op 的类型揭示了系统支持的全部"动作"：
UserTurn（用户新消息）
TurnInput（轮次输入）
Interrupt（中断）
ExecApproval / PatchApproval（审批响应）
Compact（压缩）
Review（评审）
InterAgentCommunication（子智能体间通信）
Shutdown（关闭）
5.2 核心采样循环：run_turn
每一轮对话的核心是 run_turn，它的流程像一条精密的生产线：
预压缩
（pre-sampling compact）：如果上下文过长，先压缩再采样；
解析输入
：解析用户输入所需的 MCP 服务、插件、skills；
捕获
StepContext
：每请求一次快照——记录当前模型、工具路由、MCP 绑定、世界状态。这是"请求之间状态隔离"的关键；
构建采样请求
：通过
ContextManager::for_prompt
生成模型可见的输入；
流式采样
：SSE/WebSocket 流式接收 Responses API 事件；
并行工具执行
：工具调用进入
FuturesOrdered
并行队列（
drain_in_flight
），可以同时执行多个工具；
决策
：根据结果决定 follow-up（继续）、steer（引导）、auto-compact（自动压缩）还是结束。
5.3 任务可插拔
会话的工作流被抽象成 SessionTask trait，目前有四种实现：
RegularTask：常规任务；
ReviewTask：评审任务；
CompactTask：压缩任务；
UserShellCommandTask：用户的 !shell 命令。
这意味着"一轮对话里跑什么流程"本身就是可插拔的——这是把 Codex 从"聊天工具"变成"工作流引擎"的底层支撑。
5.4 工具面：模型能看到什么
工具按轮次构建（tools/spec_plan.rs），并通过 feature flag 控制，分为几大类：
执行类
：
exec_command
、
write_stdin
、
apply_patch
；
环境类
：
current_time
、
sleep
、
get_context_remaining
、
new_context_window
、
request_permissions
、
request_user_input
；
检索类
：
view_image
、
web_search
、
tool_search
（延迟加载）、MCP 资源工具；
多智能体类
：
spawn_agent
、
send_input
、
wait_agent
、
close_agent
等；
扩展类
：图像生成、记忆、目标、插件安装建议。
工具还有暴露等级之分：Direct（直接可见）、Deferred（延迟加载）、Hidden（隐藏）等——防止一次性把几百个工具塞进上下文，这是上下文工程的一部分。
六、上下文工程：被低估的核心竞争力
如果说 agent loop 是 Codex 的"发动机"，那么
上下文管理就是它的"变速箱"
——它决定了模型每次能"看到"多少、以什么顺序看到、以及看到什么粒度。
6.1 增量式、有界、可缓存
codex-core 的上下文设计有几个精妙的原则：
ContextManager
维护模型可见的转录（transcript），线性追加、规范化更新；
ContextualUserFragment
（约 40 种类型）负责有界注入——仓库的
AGENTS.md
里有六条硬规则约束注入物必须
有界
、
≤10K tokens
；
WorldState
引擎按差异渲染——只有变化的部分才重新注入，而不是每次全量重发。
为什么要这样较真？因为
提示缓存
。Responses API 的提示缓存按前缀计费，上下文越稳定、变化越少，缓存命中率越高，成本越低、延迟越低。这是把"上下文工程"从技巧升级为架构原则的直接动机。
6.2 三条压缩路径
当对话超过上下文窗口时，Codex 有三条退路：
本地摘要
（
compact.rs
）：用专门的 SUMMARIZATION_PROMPT 在本地生成摘要；
远程压缩
（
/responses/compact
v1/v2）：调用服务端压缩接口，带 64K token 保留预算、重试预算和模型回退；
Token 预算直接开新窗口
（
compact_token_budget.rs
）：当预算耗尽时，直接开启新上下文窗口。
还有个细节值得一提：
InitialContextInjection
机制——在轮次中压缩时，规范上下文被插到"最后一条真实用户消息"之上，因为模型习惯"总结在最后"；而轮次前压缩则不注入。这种对模型行为习惯的精细建模，正是 harness 的价值所在。
6.3 数据说话
回到开头的 ARC-AGI-3 数据：13.3% → 38.3%，输出 token 减少 6 倍。这组数据想传达的信息是：
在 agent 系统里，harness 的质量和模型的质量同等重要，甚至在长任务场景下更重要。
七、平台化的桥梁：app-server 与 JSON-RPC 协议
如果说 codex-core 是"发动机"，那么
codex app-server就是"标准化接口"
——它让任何应用都能以编程方式控制这台发动机。这是 Codex 从"工具"走向"平台"的分水岭。
7.1 传输层：五种连接方式
应用可以通过五种传输方式连接 app-server：
传输
用途
stdio://
（JSONL）
默认方式，进程间通信
ws://
实验性 WebSocket，带健康检查端点
unix://
Unix 控制套接字
in-process
TUI/exec 直接进程内通道
remote-control
远程设备控制
还实现了背压机制：
有界队列，满时返回 JSON-RPC -32001 "Server overloaded; retry later."——防止慢消费者拖垮 agent。
7.2 协议设计：MCP 风格的 JSON-RPC 2.0
协议是 MCP（Model Context Protocol）启发下的 JSON-RPC 2.0 变体，有三个顶层原语：
Thread（线程）
：一次对话，包含多个轮次；
Turn（轮次）
：从用户消息开始、到 agent 消息结束的一个完整往返；
Item（条目）
：轮次内的输入输出单元——
userMessage
、
agentMessage
、
reasoning
、
commandExecution
、
fileChange
、
mcpToolCall
……
方法按 / 组织，资源覆盖极广：
thread/
（start/resume/fork/compact/queue）、turn/
（start/steer/interrupt）、item/
、fs/
、process/
、command/
、model/
、config/
、plugin/
、mcpServer/
、skills/
、hooks/
、app/
、environment/
……
7.3 双向通信
协议不只是"客户端调服务端"，还有两个重要的反向通道：
服务端通知流
（server→client）：
thread/started
、
turn/completed
、
item/agentMessage/delta
、
commandExecution/outputDelta
、
fileChange/patchUpdated
……应用可以实时流式渲染 agent 的一举一动，且可按
optOutNotificationMethods
精确退订不需要的通知。
服务端发起请求
（server→client）：
item/commandExecution/requestApproval
（命令执行审批）、
item/fileChange/requestApproval
（文件变更审批）、
item/tool/requestUserInput
（向用户提问）、
mcpServer/elicitation/request
（MCP 授权请求）……
这第二个通道极其重要——它让"人工审批"成为了协议的一等公民，而不是应用自己 hack 出来的旁路。
任何应用接入 Codex，审批流是现成的。
7.4 类型安全与生命周期
协议类型用宏生成 TypeScript 绑定和 JSON Schema（
codex app-server generate-ts
/
generate-json-schema
），保证多语言 SDK 与协议永不脱节；
生命周期管理精细：最后一个订阅者退订后 30 分钟无活动，线程被卸载并触发
SessionEnd
hooks——空闲资源被及时回收；
实验性 API 用
#[experimental]
宏门控，保证协议演进可控。
八、安全边界：一套策略，三套原生沙箱
Agent 要干活，就必须能执行命令、读写文件、访问网络。但一个"能干活"的 agent 同时也是一个"能闯祸"的 agent。Codex 的沙箱设计走的是
统一抽象 + 原生实现
的路线。
8.1 统一策略模型
用户只面对一个概念：
SandboxMode
（read-only / workspace-write / danger-full-access），它被渲染成统一的
PermissionProfile
（文件系统策略 + 网络策略）。这个 profile 再由 codex-sandboxing 翻译成三套完全不同的 OS 原生机制：
OS
文件系统隔离
网络隔离
macOS
Seatbelt（
sandbox-exec
，deny-default 闭式策略 + 受保护元数据名排除）
Seatbelt 网络规则，代理模式仅放行 loopback→代理端口
Linux
bubblewrap 命名空间 + 绑定挂载（
--ro-bind
/
--tmpfs
分层 root），
内层 seccomp BPF 网络过滤
+
no_new_privs
--unshare-net
+ seccomp 拦截 connect/accept/socket
Windows
restricted token（
CreateRestrictedToken
+ capability SID + deny-ACE ACL），可选 elevated 专用账号
WFP 持久过滤器（拦 ICMP/DNS/SMB）
关键设计是：
策略语义（允许/拒绝/询问）只写一次，强制执行由各平台的原生机制完成。
这就是"一处定义、处处一致"的工程落地。
8.2 纵深防御不止一层
沙箱只是第一层。Codex 的安全体系是明显的纵深防御（defense in depth）：
进程加固
（
codex-process-hardening
）：主进程设置
PT_DENY_ATTACH
/
PR_SET_DUMPABLE=0
、
RLIMIT_CORE=0
、剥离
LD_*
/
DYLD_*
环境变量——防调试、防转储、防注入；
特权升级管控
（
shell-escalation
）：用打过补丁的 zsh
EXEC_WRAPPER
协议，沙箱内的
execve
被拦截并回传 Codex 判定：允许直接跑 / 允许升级（sudo）/ 拒绝；
执行策略引擎
（
codex-execpolicy
）：Starlark 编写的
*.rules
规则文件（
prefix_rule
、
network_rule
、
host_executable
），判定结果为
Allow / Prompt / Forbidden
，最严格者胜；危险命令（如
rm -rf
）有专门启发式强制要求审批；
受管网络代理
（
network-proxy
）：HTTP/SOCKS5 + MITM + 证书管理，网络策略在代理层强制执行，还能做凭据代理与审计。
这一整套体系回答了一个关键问题：
当 agent 变得足够强大，我们凭什么信任它？答案是——不信任它，只信任边界。
九、多智能体与扩展生态
9.1 多智能体：让agent学会协作
Codex 内建了多智能体机制（v1 和 v2 两代）。核心是 AgentControl 控制面：
每个根线程/会话树共享一个
AgentControl
，持有
AgentRegistry
（限制子智能体数量、昵称唯一）、
V2Residency
（agent path ↔ thread 映射）、
AgentExecutionLimiter
（并发上限）；
子智能体按
角色
（default / explorer / worker）继承环境 + 执行策略，做有界配置覆盖；
通信走每个子线程的
mailbox
（
input_queue.rs
），
MailboxDeliveryPhase::CurrentTurn/NextTurn
决定迟到消息进当前轮还是下一轮；
子智能体完成时注入
SubagentNotification
给父线程；
Guardian 审批
：
on-request
审批可以交给 Guardian 子会话自动审查，fail-closed（审查失败即拒绝）。
这相当于在 harness 内部实现了"管理层级"：主 agent 可以派 explorer 去侦察、派 worker 去执行，然后汇总决策。
9.2 MCP：双向打通工具生态
MCP（Model Context Protocol）是 agent 工具生态的事实标准，Codex 在双向都做了完整实现：
作为 MCP 客户端
（
codex-mcp
）：支持 stdio / streamable-HTTP+SSE 传输、OAuth/PKCE 授权、elicitation（向用户请求授权/表单）、工具消毒/去重/
mcp__
命名空间隔离；
作为 MCP 服务器
（
codex mcp-server
）：把 Codex 自己的工具（
codex
、
codex-reply
）暴露成 MCP 服务，供其他 agent 或应用调用。
配合
connectors
（ChatGPT 托管应用的连接器：Google Drive、Gmail 等），Codex 的工具面覆盖了"自有系统 + 第三方服务 + 被其他 agent 调用"三种形态。
9.3 插件、Hooks、Skills
插件 + Marketplace
（
codex-core-plugins
）：插件可以声明 MCP server、apps（
.app.json
）、hooks、skills，支持市场安装/升级/远程安装——这是能力分发的"应用商店"模式；
Hooks
（
codex-hooks
）：生命周期钩子引擎——
PreToolUse
、
PostToolUse
、
Pre/PostCompact
、
SessionStart/End
、
UserPromptSubmit
、
Stop
……应用可以在 agent 的任何关键动作前后注入自己的逻辑（审计、改写、阻断）；
Skills
（
codex-skills
）：
SKILL.md
格式的团队知识注入，支持
@skill
提及、显式/隐式调用——让 agent 学会"你们团队特有的干活方式"。
十、执行环境远程化：本地界面，远程大脑，异OS执行
一个容易被忽略但非常前瞻的设计是
codex exec-server
——执行环境服务器。
它的角色是：在（通常是
远程
的）机器上承载进程控制与文件系统操作。app-server 可以同时连接多个 exec-server（本地默认 + environments.toml 配置的远程环境），而且
app-server 与 exec-server 可以运行在不同操作系统上
——比如 Linux 上的 app-server 驱动一台 Windows 机器执行。
远程通信的线格式相当硬核：
Noise 加密通道内的 protobuf relay 帧
（RelayMessageFrame，含流 id、seq/ack、traceparent），每条虚拟会话一个 stream id，解复用后各跑一个 ConnectionProcessor。
这意味着什么？意味着
"安全上下文"可以在执行器（executor）侧强制执行
——代码在哪里跑，安全边界就在哪里落地，而不是在用户本地。这对企业级部署（SSH 场景、云工作负载）是决定性的能力。
十一、 工程启示：从135个crate中学到什么
把整个仓库当作一个"作品"来读，有几个工程决策非常值得借鉴：
1 单一核心，多前端
codex-core 只有一套业务逻辑，CLI/TUI/exec/app-server/IDE 全部复用它。换来的是
行为一致性
：无论从哪个入口使用，agent 的决策逻辑、上下文管理、审批语义完全一致。产品层只换"皮"不换"脑"。
2 协议优先的平台化
codex-app-server-protocol 是独立的 crate，类型定义用宏自动生成 TS/JSON-Schema，SDK 层只是协议的薄封装。
协议即契约
——这让"第三方应用嵌入 Codex"从"逆向工程内部 API"变成了"对接公开契约"。
3 执行与判定分离
PermissionProfile（语义）→ 三套 OS 后端（实现）→ Starlark execpolicy（策略判定），三层彻底解耦。策略专家写规则，OS 专家写后端，互不阻塞。
4 核心抵制膨胀
codex-core 33 万行后"拒绝增长"，新能力全部放进 ext/ 下的 13 个内置扩展 crate。核心保持稳定，外围疯狂生长——这是一个成熟平台的标准形态。
5 构建系统的严谨
Bazel 8 + bzlmod + hermetic 工具链（自带 LLVM、Windows SDK、甚至 Wine 用于在 Linux CI 里跑 Windows 二进制）+ RBE 远程构建。还有 ~20 个三方补丁（LLVM、v8、ring、zstd……）——为了可复现构建，不惜代价。
结语：Harness 的哲学
回到文章开头的三个词。Codex 的工程本质，是把"一个能自主干活的 agent"打包成一套
可嵌入、可观察、可编程、可沙箱化、可扩展
的（和我昨天分享的AgentOS类似）平台运行时，让任何应用都能通过 codex app-server / SDK 把智能体接到自己已有的界面、数据、工具和审批流中。
用一句话总结这种分工：
应用的责任是"拥有产品上下文"——界面、业务规则、数据、工具、审批流；Codex 的责任是"跑好 agent loop"——思考、执行、压缩、协作、落盘，并且永远在边界内运行。
这就是为什么官方反复强调"可复用部分是 agent loop"：模型会过时，但 harness 不会——它是应用与模型之间那个
可替换、可观察、可编程
的稳定层。
对开发者而言，这意味着一个新的选择题
：当你需要为产品加入 AI 能力时，不再需要在"造一个 agent 运行时"和"用别人的聊天窗口"之间二选一。你可以选择第三条路——
把现成的 harness 嵌进你自己的产品
，然后用你的界面、你的数据、你的规则，定义这个 agent 在你业务里的样子。
毕竟，最好的 agent 不是"长得像 ChatGPT 的工具"，而是"长在你工作流里的同事"。
