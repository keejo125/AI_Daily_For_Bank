---
publish_time: 1777009570
---

# Coordination Engineering关键一环，JiuwenClaw再发布Team Skills技能新范式

> 原文链接：https://mp.weixin.qq.com/s/H-E3lZta82swqJoeLb4-vg
> 公众号：量子位

允中 发自 凹非寺

量子位 | 公众号 QbitAI

AI工程范式的演进，正从单智能体的“驾驭与治理”，大步迈向多智能体的“协同与进化”。

前不久，

华为支持的openJiuwen社区

发布的最新版JiuwenClaw，率先提出

了

Coordination Engineering

。

其凭借Agent Team实现了多智能体自主分工、高效沟通与无缝协作，完成了从“单兵作战”到“精锐团队”的关键跨越。

但一个新的命题随之而来：

如何让团队协作不再从零开始，让优秀的协作模式可沉淀、可复用、可进化？

答案，正是

Team Skills

。

Agent Team之后，

openJiuwen社区

再度重磅发布——

JiuwenClaw

Team Skills

，这是

业界首个面向多Agent协作的标准化能力包规范

。

其将多智能体团队的协作流程、任务范式、沟通策略、执行规范沉淀为团队协作SOP。

同时，他们发布了配套的创建技能

“团队技能自动生成专家（teamskill-creator）”

和共享平台

Team Skills Hub

。

Team Skills让每一次协同都站在上次的最优解之上，高效协作不再是单次任务的临时配合，而是可批量复制、持续进化的标准化能力。

关于JiuwenClaw

JiuwenClaw，是由华为2012实验室、华为云AgentArts与社区开发者联合，在openJiuwen开源社区共建的“小龙虾”AI Agent，主打“懂你所想，自主演进”。

项目地址：

https://gitcode.com/openJiuwen/jiuwenclaw

https://github.com/openJiuwen-ai/jiuwenclaw

从Agent Team到Team Skills：Coordination Engineering再升级

Agent Team解决了

当下怎么协作

的问题：Leader智能编排、成员自主执行、共享工作区协同、全生命周期管控，让多智能体像精锐团队一样完成复杂目标。

但会话结束后，这些经验全部消失。

下次遇到同类任务，Leader仍然要从零开始规划：需要几个角色、如何分工、谁先谁后、什么条件算完成。

Team Skills正是为破解这些问题而来。

Team Skills即为面向多Agent协作的标准化能力包规范

，它可以将Agent Team一次成功的协作全链路，包括需求拆解、团队组建、任务分配、通信机制、冲突处理、交付规范等，封装为

标准化

的

团队技能

，让“一支优秀团队”变成“一套可复制的团队能力”。

简单来说：

Agent Team让团队

“自主高效协作”

，Team Skills让团队

协作能力“会沉淀、可复制”

。

Team Skills长什么样

你可能用过Anthropic提出的Agent Skills，比如给单个Agent写一份“技能说明书”，让它知道遇到某类任务该怎么做。

Team Skills在这个基础上往上走了一步：

单Agent Skill解决的是“一个Agent怎么做事”，Team Skill解决的是“一个Agent团队怎么配合做事”。

一个Team Skill，本质上就是一个

文件夹目录结构

：

<

team-skill-name

>

/

├── SKILL.md              ← 这个团队叫什么、干什么、成员有谁

├── roles/                ← 每个成员角色各自负责什么

│   ├──

<

role-a

>

.md

│   └──

<

role-b

>

.md

├── workflow.md           ← 大家怎么配合、执行顺序是什么

├── bind.md               ← 遇到问题怎么处理、边界在哪里

├── dependencies.yaml     ← 依赖哪些外部工具

└── examples/ | templates/ | assets/ ...  ← 自由扩展

Team Skill的文件结构

非常简单

。

最简单的情况，一个

SKILL.md

加上

roles/

里几个角色定义，就能组起一支可用的团队。

简单任务两三个文件就够，复杂任务再按需要逐步补充，让结构随着任务演进自然展开，

几乎没有门槛

。

Team Skills怎么创建

JiuwenClaw不但提出了Team Skills标准，同时发布了配套创建技能“团队技能自动生成专家（teamskill-creator）”和共享平台Team Skills Hub。

在Team Skills Hub平台上，其提供了可以用来自由创建团队技能的Skill——

团队技能自动生成专家（teamskill-creator）

，同时支持将现有

单Agent Skill转化为Team SKill

，或者

修改已有的Team Skill

，如增减角色、调整执行流程。

按照如下步骤，可创建”多学科自动分诊的医疗专家团队“技能：

1.

在

Team

Skill

Hub

（团队技能市场）上下载

`团队技能自动生成专家（teamskill-creator）`

2.

在

JiuwenClaw

上安装该技能

3.

在

JiuwenClaw

页面输入

"帮我创建一个医疗专家会诊的团队技能，要求科目齐全，能根据用户的病情描述按需加载"

即可创建团队技能

最终，其生成了具备23位AI医学专科专家的团队技能，该技能可根据病情动态创建多个不同专科专家团进行会诊。

Team Skills实战验证

基于JiuwenClaw的多学科医疗专家团队联合会诊

以飞书频道为例，用户可在飞书上使用

/mode team

切换到集群模式，输入请求即可使用多智能体协作了。

若想停止任务或开启新会话，可使用

/new_session

命令。

若想切换其他模式，可使用

/mode agent.plan

切换规划模式，

/mode agent.fast

切换性能模式。

用户输入：“我最近浑身有点酸痛，能不能用团队技能帮我诊断一下”。

视频里可以看到，系统不会先让Leader手动决定“该找哪些专家”，而是先由分诊角色读取用户的年龄、性别、症状持续时间和关键症状表现等，判断可能涉及哪些科室方向，再

按需动态创建对应的专科专家成员

，并为每位专家分配明确的分析重点。

在这个案例里，分诊完成后，对应的专科专家会被即时创建，同时展开并行分析；

随后由主任医生统一汇总各方意见，输出一份完整的会诊报告。

整个过程不仅能看到建议方案，还能实时看到专家是如何被选中和创建的、哪些环节已完成、哪些角色正在并行工作、下一步由谁接力。

整条协作过程可见、可追踪、可复盘

。

这正是Team Skills真正能拉开差距的地方，它提供的不是“多几个Agent一起干活”，而是把复杂协作中

最关键、最昂贵、也最容易出错的协调决策，沉淀成一套可直接执行的团队工作流。

谁先分诊、该创建哪些专家、创建几个、各自负责什么、哪些环节并行、何时汇总、冲突怎么处理……

这些原本高度依赖Leader临场判断的事情，现在都能稳定复用。

Leader只需要选择合适的Team Skill，后续流程就自动运行。

这带来的不是一点点提效，而是把每次从零开始的临时编排，变成了可复制、可迭代的团队能力。

Team Skills的跨框架兼容性验证

同时，通过使用团队技能自动生成专家（teamskill-creator），可以创建一个“研究与PPT撰写”团队技能，并在Claude Code上进行验证，对Team Skill能完全遵从。

Team Skills扩展的是Agent Skills开放标准，不依赖特定平台框架，完全可以在Claude Code、Cursor等支持多智能体协同的平台上零适配运行。

这意味着，凡是支持Agent Skills标准的平台，都可以直接复用Team Skills的能力。

Team Skills如何共建

openJiuwen提供了

Team Skills Hub平台

，支持上传、检索、下载、维护团队技能。

当前已内置了一批开箱即用的Team Skills，包含

开发编程、办公与生产力、内容创作、多模态与媒体、数据与科研、合规与法律、生活与健康、金融与理财

八大类别。

大家可以体验使用“团队技能自动生成专家（teamskill-creator）”生成Team Skills，并上传至Team Skills Hub平台共享。

地址：https://teamskills.openjiuwen.com/

结语

JiuwenClaw Team Skills实现了多Agent协作经验的标准化、可复用、可分发与跨框架通用，进一步完善了Coordination Engineering的架构体系。

从

Agent Team

到

Team Skills

，JiuwenClaw持续打通“单智能体好用—多智能体协同—团队能力沉淀”的完整闭环，让Agent团队协作从“一次性组队”走向“团队化作战”。

当前，Team Skills Hub已经沉淀了开发编程、办公生产力提效、内容创作等多个场景的团队高效协作技能，大家可以即刻去体验。

同时也可以使用“团队技能自动生成专家（teamskill-creator）”创建Team Skills，并上传到Team Skills Hub，共享你的协作经验，共同构建Team Skills生态，让Agent协作更智能、更高效！

项目地址：

Team Skills Hub：

https://teamskills.openjiuwen.com/

JiuwenClaw快速上手：

https://gitcode.com/openJiuwen/jiuwenclaw/blob/develop/docs/zh/Quickstart.md

JiuwenClaw AtomGit：

https://gitcode.com/openJiuwen/jiuwenclaw

jiuwenClaw GitHub：

https://github.com/openJiuwen-ai/jiuwenclaw

openJiuwen AtomGit：

https://gitcode.com/openJiuwen/

openJiuwen GitHub：

https://github.com/openJiuwen-ai/

*本文系量子位获授权刊载，观点仅为原作者所有。

一键三连

「点赞」「转发」「小心心」

欢迎在评论区留下你的想法！

—

完

—

🌟 点亮星标 🌟

科技前沿进展每日见