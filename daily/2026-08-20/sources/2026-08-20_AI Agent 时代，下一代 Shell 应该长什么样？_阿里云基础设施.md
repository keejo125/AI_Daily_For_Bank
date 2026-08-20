---
publish_time: 1787221977
status: confirmed
category: 国内
is_model_related: false
digest: |
  文章介绍 ANOLISA（面向 AI Agent 的操作系统）的终端入口 cosh（Copilot Shell），它叠在原有 bash/zsh 之上，让用户与 Agent 共享同一份 CLI 体验，无需更换终端或迁移会话。核心理念是"主驾始终是你"：命令、别名、脚本照旧，AI 作为"副驾"有三种介入模式——一句话接手执行（带风险分级审批卡）、命令挂了顺 exit code 主动补位（提示卡+幽灵建议）、登录即先扫一遍机器状态给出健康卡与建议提示词。
  文章以新建 Vite 项目、cargo 测试失败修复、OOM 诊断三个现场演示共驾流程，并指出 cosh 兼容性是入场券、AI 是增益。ANOLISA 还内置 Token 效率、AgentSight、AgentSecCore 等开箱组件，随 Alibaba Cloud Linux 4 Agentic 版镜像内置。
link: https://mp.weixin.qq.com/s/WsMhBJTI5vhuf-N2PnFK_w
source: 阿里云基础设施
title: AI Agent 时代，下一代 Shell 应该长什么样？
---

# AI Agent 时代，下一代 Shell 应该长什么样？

> 原文链接：https://mp.weixin.qq.com/s/WsMhBJTI5vhuf-N2PnFK_w
> 来源：阿里云基础设施

不换终端、不搬会话——把 AI 叠在你原来的 bash/zsh 上，键盘就是方向盘，还握在你手里；AI 坐副驾，有三种介入模式。
光标在提示符上闪。同事甩来一句：“这台机器前几天挂过，你看看。”
dmesg
？
journalctl
？还是先
top
感受一下？——选哪个，是经验问题。
通用 bash/zsh 依然是无状态的输入输出转发器：能显示你打的字，能回显命令跑出来的结果，但不理解你在处理什么。它不知道你在排查一台机器，也不知道刚才那条命令为什么会异常退出。
AI 本该改变这种局面——让 shell 知道你在做什么。但今天常见的做法是把你从原来的会话里搬走：AI 要么住在一个独立的聊天窗口里，要么跑在一个新起的隔离会话里。你熟悉的目录、历史、上下文，都留在了外面。
cosh
，全称 Copilot Shell，
是
ANOLISA
（面向 AI Agent 的操作系统）的终端入口
，让人和 Agent 第一次共享同一份 CLI 体验。
它不是新的终端软件，也不是又一款 Agent CLI，而是叠在你原有 bash/zsh 上的一层 AI 能力增强
——你原本的命令、别名、脚本、快捷键、提示符配置一个都不用改，AI 无缝融入同一个会话里，不打断任何一个既有习惯。这一层增强的用法是人机共驾。
“主驾”始终是你
：终端不换、会话不搬、提示符不动。
git
、
grep
、
awk
、你自己写的脚本、你熟的 alias 和补全，一切照旧——键盘握在你手里，方向盘从没离过手。
“副驾”是 AI
，有三种介入模式：一句人话，它就能接手执行；命令挂了，它顺着 exit code 主动补位；你还没敲第一条命令，它已经先扫过一遍机器状态。三种模式在同一个 shell 里无缝切换，不用换窗口、不用起隔离进程、也不用记谁是主谁是副。
三种模式，三段现场——先看第一种
。
姿势一：一句话，“副驾”接手
这是共驾里最基础的一种——你有明确意图，一句话说出去，“副驾”接手把流程走完；方向盘没离开过你的手。
用户敲了一句话：“帮我新建一个 Vite 项目，叫
admin-demo
，create 过程的交互问题我自己来答，装好后帮我跑起来。”
AI 给出计划，命令仍然摆在终端里——审批卡上看得清风险分级
（
Bash · 中风险
）
和将要执行的完整命令，默认选中「允许一次」，确认后才真正触发。等脚手架进入交互式问答
（
Install with npm and start now?
）
，AI 让出前台，用户直接在原 TTY 里回答——屏幕下方同时亮起「命令正在等待输入」的提示卡，交互照原生命令行走完。
静图看得到审批卡和命令全文，但看不到“AI 让出前台
”
这个动作发生得多自然——下面这段动图还原了从确认到交互接管的完整节拍。
这几秒里最容易被忽略的一点是——脚手架的交互式问答仍然停在前台 TTY，cosh 没有为了“能被接管
”
而重写这段交互；交互等待时还有明确的提示卡告诉你“它在等你
”
。
AI 接得住你自然语言里的意图，但从没抢过你终端上的键盘
。 命令、确认、交互和接管都还在你熟悉的位置发生。一句人话能起项目——那如果一句人话都还没说，命令就先跑挂了呢？
姿势二：命令挂了，“副驾”主动补位
命令跑挂那一秒，是共驾里最考验副驾的一秒——你没开口，副驾要不要动？动到什么程度？
用户照常
git diff
看改动，照常
cargo test -q
跑测试。
报错信息
出现——
cargo test
先走一遍
cargo build
，
E0308: mismatched types
挂在编译期，测试根本没轮到跑。
用户没有切窗口、没有复制粘贴——甚至连一句话都没说。cosh 检测到命令以非零退出码返回，顺着刚才那段
报错信息
在提示符下方递出一行提示：「洞察：构建或测试失败」，旁边躺着一条幽灵建议——「Tab 填入后按 Enter 提交；继续输入可忽略」。用户看了一眼，Tab 填入、回车提交，分析开始。
主动接住不等于抢过控制权：默认就是提示符下方一行提示加一条幽灵建议，不占前台、不锁 shell；Tab 加 Enter 才提交，不理会就继续敲你的命令——是帮忙，不是打扰。
失败现场、根因定位——同一会话里顺着报错信息组织出来：
同一 shell 会话里，
cargo test
刚才那段
报错信息
还留在屏幕上，cosh 的分析就是顺着这段输出组织起来的——不需要用户复制粘贴，也不需要跳到别的窗口再问一遍：「
E0308
挂在编译期，
src/config.rs
第 9 行类型不匹配——
timeout_ms
需要
u64
，环境变量读到的是字符串。」
（本例故意选短链条——重点不在推理深度，而在"分析一冒出来就在提示符下方"这件事。）
分析之后，cosh 用 edit 工具把改动直接落盘：
timeout.parse::<u64>().unwrap_or(5000)
，解析失败时回落到 5s 默认超时——落盘动作有一张「edit 已完成」摘要卡，改了哪个文件、替换了几处，一眼可审。
副驾出改动，主驾做确认
：复验依然由用户在原 shell 里完成——再来一次 cargo test -q。终端输出刷新——
test result: ok. 1 passed; 0 failed
。
从编译失败到
test result: ok
，中间没有跨过任何一个窗口，也没有把日志复制到别处。
命令挂了副驾会主动补一句，但 Tab + Enter 才走，不理会就散
。 错误发生时副驾能补位——那还没发生的呢？
姿势三：登录那一刻，“副驾”先扫一遍状态
前两种姿势都发生在你动手之后——你开口副驾接手，命令挂了副驾补位。能不能更早一步？第三种姿势把起点往前挪：你还没敲第一条命令的那一刻，副驾就已经动起来了。
回到开头那一幕：
dmesg
？
journalctl
？还是先
top
？——熟手有自己的套路，新人常常要从零摸索。这个“先敲哪一句
”
的迟疑，本身就是可以前移的信息。
cosh 把
“
登录后先看什么
”
这件事，挪到了 shell 启动那一瞬——登录时先给你一份健康检查卡，列出风险项，再顺手把该问的第一句话递到你手边。
这次登录，健康检查卡跟着提示符一起打了出来——它从
dmesg
/
journalctl -k
里扫过最近的内核事件，把一条 OOM 记录
标为风险项
（「最近一次 OOM 已发生；应回溯被杀进程、cgroup 和当时内存水位」），紧接着「可以试试」卡片给出一条
可直接采纳的建议提示词
：“帮我分析最近一次 OOM 的原因，重点看被杀进程、cgroup 和当时内存水位。
”
用户不需要自己想从哪儿问起——Tab 填入、Enter 提问，诊断开始。
初步分析之后，用户再追问一句：“用 SysOM 诊断技能深入诊断一下这次 OOM，给出根因和处置建议。
”
——深度诊断由
SysOM 诊断技能
承接：
memory classify
→
memory oom
，被杀进程、cgroup 归属、当时的内存水位逐项对齐。（在其他发行版上 cosh 会退化到
dmesg
/
journalctl
原生数据源，结论粒度粗一档但流程一致。）结论指向 cgroup 限额 178 MB 打满，OOM 类型
CONSTRAINT_MEMCG
——是容器 memcg 内存触顶，不是整机 OOM。这个区分在 SRE 看来很关键：排查方向从“这台机器内存不够
”
，
转向“这个容器的 limits 或负载有问题
”
。
登录后的健康概览、一次初步分析、一次技能深诊、一个最终结论，都发生在同一个会话里，不必跳到任何外部工具。
登录那一刻副驾已经把健康视图摆在首屏了
。 你不必自己回忆“该从哪儿开始查
”
，Tab 采纳、看结论就够了。
所以，下一代 shell 应该长什么样？
大概不是聊天窗口，也不是把命令藏起来的自动化后台。
它更像一个工作现场——
主驾还是你
，命令、别名、脚本、快捷键一切照旧；你一开口，副驾便接手执行；命令挂了，副驾顺着 exit code 主动补位；你还没敲第一条命令，一份健康检查卡加一条建议提示词已经摆在首屏。
cosh 不是新终端，也不是 Agent CLI——它是你原来的 shell，多了一位副驾。兼容性是这一层增强的入场券，AI 能力是兼容之上的增益。键盘还在你手里，需要时一句人话就能让它接手一段路。
Shell first. AI enhanced.
快速开始
1、
创建一台 Agentic 版 ECS
：镜像选 Alibaba Cloud Linux 4 Agentic 版，cosh 随镜像内置。
2、
登录即进入
：cosh 就是这台机器的登录 shell，命令和习惯照旧。
3、
配一次模型
：输入 /
auth
，ECS 上首选 SysOM 免费尝鲜
（RAM 角色免密）
。
4、
开始共驾
：一句人话副驾接手；命令挂了看提示；登录先看健康卡。
也可以用 DashScope 或任意 OpenAI 兼容服务；没配模型时首屏会提示你 /
auth
。完整文档参看 cosh 使用指南，项目开源地址见下。
附演示 Demo：
cosh 是 ANOLISA 的终端入口。在终端之外，ANOLISA 还把 Agent 运行所需的能力做成同一系统层的开箱组件：Token 效率（Token-less、Agent Memory、SkillFS）、运行可观测（AgentSight）、安全执行环境（AgentSecCore、ws-ckpt）——与 cosh 一样随镜像内置，按需启用。
相关链接
（复制链接至浏览器打开）
：
ANOLISA 开源地址（
如果喜欢这个项目，请点 Star 支持
）：
https://github.com/alibaba/anolisa
cosh 使用指南
：
https://help.aliyun.com/zh/alinux/how-to-use-cosh-ng
SysOM 诊断技能链接：
https://skills.aliyun.com/skills/alibabacloud-sysom-diagnosis
入群交流
ANOLISA 交流
群（微信
）
ANOLISA 交流群（钉钉，群号：90400034325）
相关文章阅读：
ANOLISA 亮相 WAIC“共赢金砖”论坛，入选“智用·人工智能国际公共产品图谱”
人和 Agent 第一次共享同一份 CLI 体验 —— ANOLISA v1.0发布
你在用 Hermes？它也能拥有 ANOLISA 全套能力了
阿里云亮出 Agent 基础设施全景图，ANOLISA 要做每一个 Agent 的运行底座
Agent 越能干，你越不敢放手？ANOLISA 给它穿上全套防护
Agent 烧钱如流水？Agentic OS (ANOLISA) 帮你逐笔看清 Token 账单
Agentic OS 实战指南：手把手教你从 ANOLISA 源码安装
阿里云发布 Agentic OS：首个面向 Agent 的操作系统
—— 完 ——
ANOLISA：Agent 系统管家，致力于打造更高效更安全的 Agent Native 环境。我们正在进入新的智能操作系统范式 Agentic OS 时代，而 ANOLISA 是落地新范式的入口，是传统操作系统上叠加的一层转换层，能更好地支持 Agent 使用操作系统，并且使 Agent 获得更好的性能。我们通过 ANOLISA 重新定义了操作系统，为您带来完整的 Agentic OS 体验。用 ANOLISA，构建你的 Agentic OS！如果喜欢这个项目，请点 Star 支持一下！
开源使用
（复制链接至浏览器打开）
：
https://github.com/alibaba/anolisa/blob/main/README.md
阿里云产品上使用
（复制链接至浏览器打开）
：
https://help.aliyun.com/zh/alinux/agentic-os-getting-started
注：ANOLISA 音译为“安诺丽萨（拼音Ān Nuò Lì Sà），系 Agentic Nexus Operating Layer & Interface System Architecture 的缩写。
