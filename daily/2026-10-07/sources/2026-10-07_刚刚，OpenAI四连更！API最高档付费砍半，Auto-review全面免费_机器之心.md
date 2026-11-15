---
publish_time: 1791327808
link: https://mp.weixin.qq.com/s/KSuZPCh333T4xdQfA7j5Aw
source: 机器之心
status: confirmed
category: 国际
is_model_related: false
digest: |
  OpenAI 的 Tibo 开启“28 天每日一更”挑战，第二天连发四项更新：① Auto-review 对所有 ChatGPT 登录用户免费，引入第二个 Agent 专查主 Agent 的高风险操作，缓解长任务中频繁人工确认的负担；② API 付费等级由五档简化为三档（Build / Launch / Grow），最高档累计付费门槛由 1000 美元降至 500 美元；③ Meetings 插件进入 ChatGPT，可记录会议并存入 Space 生成总结与待办；④ Decisions API 进入 public beta，由 GPT-6 Luna 驱动，输出 Predicates / Choices / Scores 三类低延迟决策（比 Responses API 快约 10 倍），用于路由、工具选择与风险判断。
title: 刚刚，OpenAI四连更！API最高档付费砍半，Auto-review全面免费
---

# 刚刚，OpenAI四连更！API最高档付费砍半，Auto-review全面免费

来源：机器之心
原文链接：https://mp.weixin.qq.com/s/KSuZPCh333T4xdQfA7j5Aw

机器之心编辑部
10 月初，OpenAI 的 Tibo 给自己立了一个颇有压力的 Flag。未来连续 28 天，每一天，OpenAI 都要给 Codex / Work 用户带来一项足够明确的改进。如果当天没有更新，就直接来一次完整的用量重置。
第一天的更新很直接：GPT-6 Astra 和 GPT-6.1 Sol 在订阅体系下的默认速度提升约 50%。
到了第二天，节奏突然加快。Tibo 没有只交出一个更新，一口气放出四项更新：
Auto-review 免费、API 用量等级简化、Meetings 插件接入会议记录，以及 Decisions API 面向更多开发者开放
。
四项更新横跨 Codex、ChatGPT 和 API。
单独看，每一项都算不上 DevDay 级别的新品发布；放在一起，它们指向的却是同一件事：OpenAI 正在集中处理那些真正进入日常工作后，最容易让 Agent 卡住的细节。
Day 2.1
让第二个 Agent 替你盯着第一个 Agent
第二天最先动刀的是
权限确认
。
OpenAI 宣布，Auto-review 现在对所有通过 ChatGPT 账号登录的用户免费开放，不会再消耗用户套餐中的使用额度。Auto-review 对应的就是权限菜单里的「Approve for me」。
在默认的沙箱权限模式下，当 Agent 准备执行一些可能产生外部影响的操作时，用户往往需要手动确认。任务很短时，这套机制问题不大。一旦 Agent 开始连续工作几十分钟甚至更久，频繁点击批准本身就会成为负担。
Auto-review 给出的解决方案，是再引入一个 Agent。主 Agent 继续执行任务，另一个 Agent 专门检查它准备采取的操作。它的职责很窄，主要关注高风险行为，以及明显偏离用户原始意图的动作。Tibo 同时确认，Auto-review 就是此前的「Approve for me」模式。
这里真正值得关注的，其实不是「免费」两个字。
当 Agent 从几分钟的代码生成逐渐进入长时间运行的真实任务，权限管理会越来越难依赖用户逐步点击确认。完全放开权限又会带来明显风险。Auto-review 相当于在两者之间增加了一层自动审查，让 Agent 可以继续运行，同时保留一道针对高风险行为的检查。
它无法等同于绝对安全，但对于长任务来说，这种权限模式更接近实际可用的 Agent 工作流。
Day 2.2
API 五档变三档，最高等级门槛直接减半
这一次针对开发者。
OpenAI 将此前五个付费 API Usage Tier 简化成三个：Build、Launch 和 Grow。其中，
Build 的累计付费门槛为 5 美元，Launch 为 100 美元，最高等级 Grow 为 500 美元
。
此前进入最高付费等级需要累计支付 1000 美元，现在门槛直接降了一半
。达到条件后，组织会自动升级，无需手动申请。
这次调整本身并没有改变模型能力，也不能简单理解成 API 降价。它解决的是扩容过程中的摩擦。
对于正在把应用从测试推向正式生产的开发者来说，API Rate Limit 很容易从一个后台参数变成实际瓶颈。请求量一旦迅速增长，能否及时获得更高的 RPM、TPM 和整体使用额度，会直接影响服务能否继续扩展。
把五层压缩成三层，同时降低最高等级的进入门槛，相当于缩短了开发者从小规模试验走向较大规模调用的路径。
相比继续增加新的等级和规则，OpenAI 这次选择了把规则本身变简单。
Day 2.3
会议结束，ChatGPT 拿到上下文
Day 2.3 则回到了一个更加日常的工作场景：开会。
OpenAI 正式把 Meetings 插件带进 ChatGPT
。它可以在会议过程中记录内容，随后将个性化总结和待办事项保存到 ChatGPT Space。用户可以把记录保持私有，也可以分享给团队，再让 ChatGPT 基于这些内容继续更新项目计划、整理行动项或者起草会后跟进。
目前，Meetings 已在 macOS 版 ChatGPT 桌面应用中向 Pro 和 Business 用户开放 Beta。Enterprise 尚未普遍开放。OpenAI 的帮助文档显示，目前仅有一小部分 Enterprise 客户参与 Alpha 测试。
这项功能有意思的地方，在于它进一步缩短了「工作发生」和「AI 获得上下文」之间的距离。
过去把会议内容交给 AI，往往需要录音、转写，再上传文件或者复制会议纪要。现在会议本身成为 ChatGPT 的上下文入口。更重要的是，会议记录没有停留在「总结一下刚才说了什么」。
会议结束后产生的决定、任务和背景，可以继续进入 Space，随后成为项目计划、文档以及下一轮任务的输入。这样一来，会议记录开始和后续执行连在一起。
这也是 ChatGPT Space 推出之后，OpenAI 正在逐渐补齐的一块拼图：让 Agent 获取工作上下文的过程越来越自动。
Day 2.4
让模型少写点答案，直接做决定
第二天最后一项更新，则落在 Decisions API。
这个 API 最早在 9 月 29 日的 OpenAI DevDay 2026 上亮相。当时还处于 limited preview。现在，按照 OpenAI 最新公布的信息，
Decisions API 已进入 public beta，面向开发者开放
。
它解决的问题和普通生成式 API 有些不同。
很多应用调用大模型，并不是为了得到一段长文本。比如，一条请求应该交给哪个模型，一个任务应该使用哪个工具，某个 Agent 下一步应该采取什么动作，一次工具调用是否存在风险。这些问题最终往往只需要一个明确判断。
Decisions API 就是为这类任务设计的。它由 GPT-6 Luna 驱动，接受文本和图片输入，目前支持三类输出形式。Predicates 用于判断某个陈述为真的概率；Choices 从预先定义的选项中进行选择，并返回置信度；Scores 则把输入映射到一个数值区间。
OpenAI 给出的数据是，Decisions API 做出决策的速度最高可以达到通过 Responses API 调用 GPT-6 Luna 的约 10 倍。此前 DevDay 展示的数据大约是 150 毫秒对 1.6 秒，不过这一数字来自 OpenAI 自己的演示，实际延迟仍会受到具体任务和输入规模影响。
它已经可以被用于请求路由、模型和工具选择、内容分类、图片比较，以及 Agent 工具调用前的风险判断。这也是 Decisions API 值得继续观察的原因。
随着 Agent 工作流越来越复杂，大量模型调用实际上承担的是「判断下一步做什么」。过去，开发者通常会让通用模型生成结构化结果，再解析 JSON，或者通过 Prompt 限制模型从几个选项中作答。现在 OpenAI 开始把这类任务单独抽出来，变成一个低延迟的决策接口。
如果这种接口能够在稳定性、成本和置信度校准上进一步成熟，Agent 系统里「负责生成」和「负责判断」的模型调用可能会变得更加清晰。
从 Auto-review 到 Decisions API，第二天的四项更新跨度很大。但它们有一个明显的共同点：都没有继续追逐单纯的模型能力指标。
Agent 已经可以写代码、调用工具、操作电脑和连续执行任务。真正进入长时间、高频率的工作环境以后，新的问题随之出现：人需要不断批准操作，API 扩容规则太复杂，工作上下文需要反复搬运，大量简单判断又没有必要调用完整的生成流程。Tibo Day 2 做的事情，基本都落在这些环节。
第一天，OpenAI 把模型跑得更快。第二天，它开始清理模型真正进入工作之后留下的一系列摩擦。
参考链接：
https://x.com/thsottiaux/status/2107575657014468879
© THE END
转载请联系本公众号获得授权
投稿或寻求报道：liyazhou@jiqizhixin.com
