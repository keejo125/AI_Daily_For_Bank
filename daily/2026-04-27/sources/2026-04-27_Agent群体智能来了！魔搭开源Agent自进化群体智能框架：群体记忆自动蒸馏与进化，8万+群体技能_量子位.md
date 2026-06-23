---
publish_time: 1777286214
---

# Agent群体智能来了！魔搭开源Agent自进化群体智能框架：群体记忆自动蒸馏与进化，8万+群体技能即取即用，智能体画像一键复用

> 原文链接：https://mp.weixin.qq.com/s/cCzTNq0LpWgv-fM_EKFMQQ
> 公众号：量子位

Ultron 团队 投稿

量子位 | 公众号 QbitAI

目前个人团队或团队在自行部署和使用智能体的过程中，普遍面临三大痛点，导致使用成本极高

：

状态易失（换会话就失忆）

单次任务的经验随会话结束而清空，无法沉淀为可复用的长期记忆，更谈不上持续进化。

重复试错（同一坑全队踩）

缺乏经验共享与自动蒸馏机制，A踩过的坑无法进化为团队技能，B还会重新排查一遍（例如文中提到的MySQL 8.0字符集问题）。

迁移困难（专家画像烂本机）

调教好的Agent（包含提示词、记忆、技能）与特定框架或设备深度绑定，经验积累无法跨环境流转，难以在团队间共享或向其他框架平稳迁移。

而这些问题，正在被一套面向通用智能体的自进化群体智能系统逐步解决。

ModelScope团队最近开源了

Ultron

。它不是在重复造一个Agent，而是补上了Agent体系里长期缺失的一层——

群体协作基础设施

。

目标很直接，让经验自动沉淀并持续进化为可复用的高阶技能，让已经调好的智能体画像可以被团队共享。

Ultron主要在解决三件事：

一次会话结束后，经验很容易随上下文一起消失。

同样的问题会被不同智能体反复踩一遍。

调好的专家型智能体很难共享，也很难在不同框架之间平稳复用。

这些问题在单个Demo里通常不明显，但一旦进入多智能体、多会话和多团队协作场景，成本会迅速上升。同一个错误要重复排查，同一种工作流要重复搭建，同一套高质量画像既难分享，也难在不同Agent框架间稳定迁移。

一群智能体一起进化

Ultron实现了从“单点智能”到“群体智能”的跃升，核心亮点在于：

经验沉淀为群体资产 (Memory Hub)

：从真实轨迹中提炼出1746条结构化记忆，并按HOT/WARM/COLD分层，支持相似场景下直接检索召回。

经验结晶为为技能并持续进化 (Skill Hub)

：反复验证的高频记忆通过语义聚类自动结晶为工作流技能（已形成182个）；新证据积累后触发再结晶持续进化，溯源验证与结构分数门控确保只升不降。同时打通了魔搭社区8万+外部技能，即取即用。

画像蓝图一键分发 (Harness Hub)

：将角色设定（如内置的201个预置角色）、记忆背景、技能组合和工具配置打包成标准化蓝图。其他框架（如OpenClaw、Nanobot）可以像下载软件一样一键导入成熟的专家智能体（例如文中提到的FinanceBot）。

具体来说, Ultron围绕三个核心模块展开：

1. Memory Hub

把智能体在真实任务中积累的踩坑记录、修复方法和模式总结，沉淀为可检索的群体记忆。

这些记忆并不是简单堆叠，而是按HOT、WARM、COLD分层管理，并支持语义检索、命中统计、摘要压缩和去重合并。

这带来的直接变化是，某个智能体刚解决过的问题，另一个智能体在相似场景下可以直接召回，不用再从零开始分析。

2. Skill Hub

当一类经验被反复命中、反复验证时，它就不该只停留在“记忆”层，而应该结晶为可直接调用的“技能”。在Ultron中，高频记忆通过语义聚类自动结晶为工作流技能；技能上线后并非固化——新证据积累会触发再结晶持续进化，溯源验证与结构分数门控确保只升不，无需人工整理或编写复杂的Skill文件。

同时，Ultron还打通了ModelScope Skill Hub，可统一检索80000多个外部技能。这意味着，系统既能复用团队内部沉淀的经验，也能无缝接入外部生态能力。

3. Harness Hub

这一部分更像一个

“智能体画像分发中心”

。一个真正调好的智能体，往往不只是Prompt写得好，而是

角色设定、记忆背景、技能组合和工具配置

共同打磨出来的结果。

Ultron支持把这些要素打包成可分享的蓝图，其他实例可以一键导入并快速复用。换句话说，以前团队里那个“只在某个人本机上最好用的专家智能体”，现在终于可以被稳定地分享出去。

如何使用

连接你的智能体

无需安装或阅读Ultron源码。在已运行的Ultron实例上，按交互式快速入门操作，数分钟内即可完成接入（以 Nanobot 为例）：

#1

.获取技能包

#已部署的

Ultron 会将 `ultron-1.0.0` 打成 zip，可通过下面地址下载并解压到助手工作区的 `skills/` 目录（压缩包内路径为 `ultron-1.0.0/...`）：

mkdir -p ~/.nanobot/workspace/skills

wget -O /tmp/ultron

-1.0

.0

.zip

"https://writtingforfun-ultron.ms.show/dashboard/agent-skill-package"

wget -O /tmp/ultron

-1.0

.0

.zip

"https://writtingforfun-ultron.ms.show/dashboard/agent-skill-package"

unzip -o /tmp/ultron

-1.0

.0

.zip -d ~/.nanobot/workspace/skills/

#2

.设置 Ultron 服务地址

export ULTRON_API_URL=https://writtingforfun-ultron.ms.show

#3

.让助手自动配置

#向助手发送消息

：

Set up Ultron using setup.md

#助手会自动读取

`skills/ultron-1.0.0/setup.md`，完成以下配置：

# - 生成 `ULTRON_AGENT_ID`（UUID，用于 ingest 进度隔离）

#4

.验证

cd ~/.nanobot/workspace

python3 skills/ultron

-1.0

.0

/scripts/ultron_client.py

&#x27;{"action":"get_stats"}&#x27;

# 预期响应中含 `"status": "ok"`。

#技能包内容

skills/ultron

-1.0

.0

/

├── SKILL.md

# 主入口（actions 表、调用优先级）

├── setup.md

# 安装指南（助手读取并执行）

├── operations.md

# 记忆操作与上传模板

├── boundaries.md

# 安全边界

└── scripts/

├── ultron_client.py

# API 客户端

└── memory_sync.py

# 记忆同步脚本

已沉淀的“群体智能”

Ultron当前已经具备一套相当完整的基础数据和能力框架：

1.从真实智能体任务轨迹中提炼出

1746

条结构化记忆。覆盖

pattern、error、security、life、correction

5类知识。

2.高频记忆自动结晶为182个内部技能，按项目文档已归入9大类、39个分类体系，并随新证据积累持续再结晶进化。

3.接入ModelScope Skill Hub，统一检索

80000+

外部技能。

4.提供201个预置角色(soul preset)，可组合角色、MBTI、星座等画像能力。

使用案例

场景：开发者让智能体排查使用

mode="session"

调用

sessions_spawn

创建子智能体时的错误。此前另一智能体已踩过同一坑，解法已沉淀为群体记忆。

❌ 未接入Ultron

用户：我想用

sessions_spawn

创建一个子 agent 来并行处理任务，用

mode=session

，但一直报错，怎么回事？

Agent：根据我的工具定义，创建子agent应该使用

spawn

工具，而不是

sessions_spawn。

Agent不认识

sessions_spawn

，给出了完全错误的方向。

✅ 接入Ultron

用户：我想用

sessions_spawn

创建一个子agent来并行处理任务，用

mode=session

，但一直报错，怎么回事？

Agent：根据召回的群体记忆，找到了问题所在！

召回记忆：

sessions_spawn

的

mode="session"

必须配合

thread=true

，且需要

channel

插件注册

subagent_spawning hooks

。缺少

hooks

时无论参数是否正确都会失败。

1轮对话，直接命中根因并给出分场景方案。

维度

未接入Ultron

接入Ultron

工具识别

不认识

sessions_spawn

，误导为

spawn

准确识别工具及其参数约束

根因定位

完全偏离

直达根因：缺少

thread=true

或 channel hooks

解决方案

无效

分场景给出两种方案

知识来源

智能体从零猜测

召回群体记忆中已验证的踩坑经验

适用于更多场景

通过Ultron，许多过去「这次运气好碰对了、下次换个人又翻车」的问题，可以变成可复用的具体资产：

共享避坑（Memory Hub）：智能体A遇到「MySQL 8.0默认字符集导致emoji写入失败」，修复沉淀到Memory Hub。数周后智能体B建新库时自动命中同一条记忆，跳过陷阱，无需重复排查。

运维技能包（Skill Hub）：SRE 将「K8s OOMKilled→定位泄漏→调整limits→灰度验证」打成可复用技能，其他团队的智能体按相同步骤执行，而不是各自重写流程。

领域专家智能体（Harness Hub）：DevOps工程师花数周把OpenClaw调成Kubernetes专家（记忆、技能、人设齐备），将画像发布到Harness Hub，其他开发者可实现一键导入OpenClaw/Nanobot/Hermers Agent等智能体。

把智能体真正放到开发、运维、研究或内容生产场景里，最难的往往不是模型不够聪明，而是这份“聪明”很难被继承。比如，一个开发智能体已经踩过某个工具调用陷阱，也验证过修复路径。没有群体智能时，下一个智能体遇到同类问题，通常还是要重新搜索、重新判断、重新试错。

有了Ultron，这段经验可以先沉淀为记忆，并在后续任务中通过语义检索被召回。若同类问题反复出现，这些经验还会继续蒸馏成技能，直接变成可复用的标准化能力。从“这次解决了”到“以后大家都会了”，背后是两套完全不同的系统能力。

分发专家型智能体功能的具体应用

Ultron还提供了一个很有代表性的Showcase：FinanceBot。

它不是一个空白Agent，而是一个已经调好的金融领域智能体。这个案例里，Ultron把角色设定成Data Engineer，给它配上ISTJ的决策风格和Capricorn的长期主义底色，同时接入Finnhub Pro技能，用于实时行情、财务报表、公司新闻和IPO日历等金融数据处理任务。更重要的是，它还继承了5条精选金融实战记忆。也就是说，导入的不是一个“会聊天的金融助手”，而是一个带着角色、技能和过往经验一起到岗的专家型Agent。

这其实展示了Harness Hub最直观的价值：智能体不再只是“一个模型入口”，而是可以像软件模板、工作流模板一样，被封装、分享和复用。

一键导入Ultron调配的FinanceBot：

# Nanobot

curl -fsSL

"https://writtingforfun-ultron.ms.show/i/at3ZEe?product=nanobot"

| bash

# OpenClaw

curl -fsSL

"https://writtingforfun-ultron.ms.show/i/at3ZEe?product=openclaw"

| bash

# Hermes Agent

curl -fsSL

"https://writtingforfun-ultron.ms.show/i/at3ZEe?product=hermes"

| bash

Agent的下一步，可能不是更长的Prompt，而是更强的群体协作

过去大家做Agent，更多关注模型能力、工具调用和工作流编排。但当Agent真正进入生产环境，一个更现实的问题会浮现出来：怎样让团队里的智能体越用越好，而不是每次都从头开始。从这个角度看，Ultron补上的正是一层关键基础设施，

让经验沉淀下来，让技能持续生长，让画像稳定传递。

这也意味着，Ultron关注的已经不只是某一个Agent框架本身，而是更上层的群体智能协作能力。像

Hermes Agent

这样的自进化Agent可以接入 Ultron，持续贡献新经验和新技能。像

darwin-skill

这类围绕Skill进行评估、改进、测试与保留的演进系统，也能与Ultron形成互补。

在多源协同下，Skill不再只是静态说明文档，而是可以在任务中生成、在反馈中迭代、在不同团队与运行时之间持续复用的能力单元。

如果说单个Agent解决的是“能不能做”，那么群体智能系统解决的就是

“做过的东西能不能持续复用、持续演化、持续扩散”

。从这个意义上看，Ultron面向的也不只是某一套固定框架，而是所有希望把经验沉淀、技能演进和画像复用纳入日常工作流的主流Agent生态。

这或许正是Agent从“能用”走向“好用”，从“单点能力”走向“组织能力”的关键分水岭。

GitHub：

https://github.com/modelscope/ultron

FinanceBot Showcase：https://github.com/modelscope/ultron/blob/main/docs/zh/Showcase/financebot.md

体验页面：

https://writtingforfun-ultron.ms.show

快速接入：

https://writtingforfun-ultron.ms.show/quickstart

一键三连

「点赞」「转发」「小心心」

欢迎在评论区留下你的想法！

—

完

—

我们正在招聘一名眼疾手快、关注AI的

学术编辑实习生

🎓

感兴趣的小伙伴欢迎关注 👉

了解详情

🌟 点亮星标 🌟

科技前沿进展每日见