---
publish_time: 1790919542
link: https://mp.weixin.qq.com/s/j8TAh7pPf1mDo4iO76OROg
source: InfoQ
status: confirmed
category: 国际
is_model_related: false
digest: |
  Anthropic 为 Claude Code 推出 Mods（修改模块）机制，允许开发者通过主进程内的函数钩子深度定制智能体的界面与运行逻辑，可由 Claude Code 自行编写、安装并在会话中热加载，被视为“进程内拦截”的最高权限插件形态。Mod 以 JS/TS 编写常驻主进程，可重构终端界面、双向拦截工具调用（调用前弹确认、返回前脱敏凭据）、注册自定义命令并按复杂度路由到更便宜的模型。DeepSeek Harness 负责人崔添翼评价其与 DeepSeek Harness 殊途同归，但后者“一切皆插件”的开放范围更广。
title: Claude开放插件最高权限Mods，DeepSeek崔添翼下场评价：与DSH殊途同归，但范围截然不同
---

# Claude开放插件最高权限Mods，DeepSeek崔添翼下场评价：与DSH殊途同归，但范围截然不同

来源：InfoQ
原文链接：https://mp.weixin.qq.com/s/j8TAh7pPf1mDo4iO76OROg

作者 | 青和
编辑 | 四月
Claude Code 刚刚开放 Mods 能力，DeepSeek Harness 团队负责人崔添翼便下场回应：认为
前者与 DeepSeek Harness 的插件架构
正走向
相似的方向
。
10月1日，Anthropic 正式宣布为 Claude Code 引入 Mods（Modifications，修改模块）机制，允许开发者通过主进程内的
函数钩子（Function Hooks）
，
深度定制智能体的界面与运行逻辑
。用户甚至不必亲自编程，可以让 Claude Code 为自己编写、安装 Mods，并在当前会话中热加载。
功能推出后，DeepSeek 智能体底座
DeepSeek Harness
的团队负责人崔添翼在社交平台转发并发表评论。
这位曾任顶级量化基金 Jane Street 技术专家、经典开源教程《背包九讲》作者、于今年春季加盟 DeepSeek 带队 Harness 的技术掌舵人直言：
Claude Mods 和 DeepSeek Harness 在底层思路上“正在走到一起，殊途同归”
。
但崔添翼同时指出了两者的关键差异：
开放的范围截然不同
。Claude Code 里的 Mod 本质上仍是
在既定软件架构
上打补丁的局部插件；而 DeepSeek Harness 从诞生第一天起，就把整套运行时全面建构在“
一切皆插件（Everything is a Plugin）
”的架构上。
崔添翼调侃道，过去行业里研究如何给模型外挂工具和提示词的学问叫
“Plugin Engineering”（插件工程）
，而随着智能体控制权的全面下放，这套技术现在或许应该改名叫
“Mod Engineering”（Mod 工程，模组工程）
。
1
基于Mods：用户可改写Agent内部行为
在此次更新前，Claude Code 的扩展机制主要依赖三套相对割裂的通道，过去只有零散的技术名词“Function Hooks”，大致层次可分为：
MCP（模型上下文协议）：
通过标准 JSON-RPC 暴露外部只读或执行类工具；
Skills：
纯提示词驱动的操作指南；
Settings Hooks：
在特定触发点启动独立外部子进程，运行 Shell 脚本。
这种方式的痛点在于
无法侵入主进程内部
——外部脚本既不能实时获取并修改运行时的中间状态，也无法对终端呈现界面进行像素级的重构。
Claude Code Mods 的核心变化，在于将扩展机制由
“进程外调用”
演进为
“进程内拦截”
，可视为
最高权限的插件形态。
技术本质：
Mod 是一段由 JavaScript 或 TypeScript 编写的代码，直接常驻在 Claude Code 的主进程内，以事件钩子（Hooks）的方式介入执行流。
界面与交互重构：
Mod 拥有终端界面的渲染权。开发者可以在主对话区域旁边绘制代码变动 diff 栏、渲染多智能体调用树，或在状态栏实时显示 Token 消耗速率。甚至可以重绘系统默认的执行等待动画。
工具调用的双向拦截：
在工具触发前，Mod 可以截获请求并向用户弹出确认机制；在执行完成后，Mod 可以在结果喂回大模型之前，自动过滤脱敏敏感凭据（如 API Key）。
轻量级指令与路由：
支持注册自定义 /command 命令，无需调用大模型即可在本地秒级返回；在执行循环中，还能依据任务复杂度将请求分流至更便宜或更快速的模型。
事实上，Anthropic 官方近期推出的
/diff
面板以及针对多智能体协作的
agents.md
支持，在底层都已被重构成内置 Mod。这意味着 Anthropic 自身也在利用 Mod 机制解耦产品功能。
Anthropic 还提供了三个相当直观的 Mods 示例。
第一个叫 Token Weather。
它能在输入框上方绘制一个类似天气预报的图形，动态展示当前上下文窗口的占用情况，把原本不够直观的 Token 消耗变成可视化信息。
第二个叫 Blast Radius。
当 Claude Code 准备执行
rm -rf
、强制推送等可能产生较大影响的命令时，它会暂停操作，向用户展示可能改变的内容，并提供继续或取消按钮。
第三个叫 Replay Theater。
它提供
/replay
命令，允许用户逐步查看 Claude 在上一轮操作中对文件进行了哪些修改。
2
殊途同归背后的“开放范围之争”
崔添翼做出“殊途同归”的判断，核心逻辑在于：
无论是 Anthropic 还是 DeepSeek，都已意识到纯靠“大模型 + 静态提示词”无法解决复杂工程场景的稳定性问题。
要让智能体在真实代码库和终端环境中稳定交付，必须向开发者开放运行时的控制权。但两家团队在“向谁开放、开放到什么程度”上，给出了完全不同维度的方案。
1. Claude Code：宿主中心主义的“局部插件”
Claude Code 依然是一款产品化优先的黑盒工具。它的核心执行机制、会话管理和主状态机是不允许外部改动的。Mods 开放的只是官方预设的几个切面（界面渲染、工具过滤、提示词注入）。用崔添翼的话说，
在 Claude Code 里，Mod 依然是附属在既定宿主上的“插件”
。
2. DeepSeek Harness：“一切皆插件”的微内核设计
与 Claude Code 自顶向下的“开洞放权”不同，DeepSeek 团队自 5 月立项、8 月开源开发者预览版的
DeepSeek Harness (dsh)
，在设计之初就确立了
“Everything is a Plugin”
的原则。
Harness 依托开源微内核框架 Cordis 构建，在它的架构里不存在特权核心，
每一个系统构件全部被实现为独立的插件
：
基础能力插件：
模型适配器（支持 DeepSeek、开源模型端点及其他商业模型）、工具集、外部 Skills、执行沙箱、本地持久化存储；
流程与系统插件：
会话事件日志（Session Log）、任务调度系统（Scheduling）、执行步进循环（Agent Loop）；
表现层插件：
前端 UI（无论是 Web 界面还是终端交互）本身也只是一个可插拔的 Bundle。
在 DeepSeek 的设计中，如果你需要调整智能体的步进机制或修改其思考回退逻辑，你不需要向官方提 Issue 等待开放 Hook，只需直接换掉 Agent Loop 插件即可。
崔添翼的原文如下：
祝贺 Claude Code 团队正式推出 Mods！这是一种挺巧妙的设计，让 Agent Harness（智能体运行框架）变得可扩展、可定制。
有意思的是，双方的思路正在殊途同归：在 Claude Code 中，Mods 本质上就是插件；而 DeepSeek Harness 从一开始，就在围绕插件这一概念进行重新思考和架构设计。
虽然 Claude Code 目前只将
部分（subset）功能
开放为 Mods，但在 DeepSeek Harness 中，
「一切皆插件」（Everything is a Plugin）
：模型、工具、Skills、会话、沙箱、文件系统、Agent Loop、编排机制以及 UI，
全部都是以插件形式实现的
，可以自由组合、搭配、替换和扩展。
在 DeepSeek Harness 的 Creator Mode（创造模式）中，你可以直接通过提示词，让 Agent 检查当前正在运行的系统环境，编写插件，并将其持久化保存。
借助这种方式，你可以修改 UI、调整 Agent Loop 的行为和运行机制、添加新工具，或者引入新的任务编排方式。换句话说，
Agent Harness 的一切都可以在运行过程中即时修改，并将这些修改持久化保存
。
所以，我们其实已经琢磨「
Plugin Engineering
」（插件工程）这个说法有一段时间了……
或者说，现在是不是应该改叫「
Mod Engineering
」（模组工程）了？
😂
3
DeepSeek 近期动作：从开源预览到 Creator Mode
这一场技术交锋并非凭空而来，而是建立在 DeepSeek Harness 近期密集的动作之上。
自 2026 年春季崔添翼加盟 DeepSeek 并组建团队以来，DeepSeek 就开始全力补齐“将聪明的大模型转化为真实执行力”的这一环。8 月中旬，DeepSeek Harness 开发者预览版 v0.1 正式开源；近期，DeepSeek 更是在社区掀起
“从命令行走向桌面端 Agent”
、以大规模 Token 支撑复杂长周期工作流的实操动作。
在 DeepSeek Harness 的四种官方运行模式（Standard 完整编码、Code 编程接口、Minimal 极简评测、Creator 创作者模式）中，最引人注目的正是崔添翼推文中所提到的
Creator Mode（创造模式）
。（
刚刚，DeepSeek Harness 桌面预览版上线！Mac与Windows均可下载
）
这项功能的特殊之处在于：
它赋予了智能体“现场编写自身插件”的自省修改能力。
运行时自省：
在 Creator Mode 下，Agent 拥有对当前系统运行环境的读取权限，可以检查自己当前加载了哪些模型适配器、挂载了哪些工具、启用了什么样的调度策略。
内存现场编码：
面对超出当前能力的复杂任务时，Agent 能直接在内存中编写一段 Cordis 插件代码。
热挂载与持久化：
新插件编写完成后，系统可以立即在沙箱内完成挂载、生效与验证。一旦验证可行，Agent 即可将其实时固化为全新的预设模式。
换句话说，Claude Code 的
Mods
是人类工程师为
智能体装配
的
“功能外设”
；而 DeepSeek Harness 的
Creator Mode
，则是让智能体具备了
“现场改写自身器官与运作逻辑”
的可能。
这正是崔添翼所称“Mod Engineering”的终极体现。
4
从卖 Token 走向“Harness之争”
DeepSeek 内部流传着一个形象的公式：
Model + Harness = Agent
。
如果把大语言模型比作发动机，Harness 就是底盘、变速箱、方向盘和刹车系统；如果把智能体任务比作驯马，模型负责提供野性动力，Harness 则是决定马匹能否精准跨越障碍的马鞍。
过去一年，全球大模型厂商主要在模型参数、推理成本与上下文长度上展开激烈较量。而 Claude Mods 的全量推送与 DeepSeek Harness 的开源推进，标志着竞争维度正全面
延伸至运行时层：
Anthropic
依托成熟的产品形态，试图通过 Mods 降低专业工程团队的定制门槛，把 Claude Code 塑造成
可扩展
的生产力标杆；
DeepSeek
则凭借崔添翼带来的量化级高并发、系统化控制思维，试图通过彻底的
微内核插件化架构
，打造一个没有边界的开源智能体底座。
当两家头部团队在“构件模块化”的十字路口相遇，智能体开发正从黑盒一体机时代，加速步入由开发者与智能体共同重塑系统逻辑的“Mod 时代”。
声明：本文为
InfoQ 原创，
不代表平台观点，也不构成投资建议，未经许可禁止转载。
今日好文推荐
坚决不用行业标准AGENTS.md，Claude Code惹来“封杀令”：Anthropic终于回应了，但开发者更气了
DeepSeek Harness 负责人吐槽“融资材料”吹过头：V4-Pro编程能力仅差Claude旗舰0.3%，前端服务费高达10%
会搭几个Agent，就敢给企业做AI转型了？FDE车祸现场
Pi 爆火真相 ：为什么只给模型一个 bash，反而赢了 Claude Code 和 Codex
OpenAI 只用 15 天，就杀死了估值 100 亿美元的 Jev？
会议推荐
QCon 全球软件开发大会·2026（上海站）将于 10 月 22 日—24 日举办。本届大会聚焦 Harness AI 时代的工程实践，从「构建 AI」到「驾驭 AI」，围绕 AI Native 架构、Agent Runtime、AI Infra、Agent 安全与可观测、Loop Engineering、具身智能与世界模型 等热门技术方向，邀请全球技术社区与产业一线实践者，共同分享 AI Native 时代最具价值的工程经验。限时 9 折优惠立减 680！查看更多详情可扫码或联系票务经理 18514549229 进行咨询。
