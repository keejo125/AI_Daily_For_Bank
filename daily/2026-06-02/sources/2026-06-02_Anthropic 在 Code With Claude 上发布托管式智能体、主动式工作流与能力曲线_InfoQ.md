---
publish_time: 1780379050
---

# Anthropic 在 Code With Claude 上发布托管式智能体、主动式工作流与能力曲线

> 原文链接：https://mp.weixin.qq.com/s/56JDja7dvxJKO_gMDE6jdQ
> 公众号：InfoQ

作者 | Andrew Hoblitzell

译者 | 张卫滨

Anthropic 于 5 月 6 日在旧金山举办了 Code with Claude 2026 会议，并将直播内容发布到了 YouTube。相关分享覆盖了 Claude Code、Claude Developer Platform，以及在 GitHub、Vercel、Datadog、Bun 和多家 AI 原生创业公司中的合作部署案例。贯穿全天的主线话题是：模型能力的阶段性跃迁，会如何影响产品架构、组织设计与基础设施经济性。

Anthropic Claude Code 团队的 Dickson Tsai 展示了 Claude Code 的最新更新。在开发者体验方面，远程控制功能允许会话在一台机器上开始、随后在手机上继续；重新设计的桌面 GUI 则加入了分栏视图、将助手消息固定为章节并自动生成目录的能力，以及内联 diff 评论。在自主能力方面，Auto 模式把权限决策交给分类器，由其筛查破坏性操作和提示词注入；worktrees 则为 Claude 提供进入与退出工具，使其能够自行创建和销毁隔离分支。Tsai 还演示了 routines，这一能力可基于 cron 计划、GitHub webhook 或 API 端点触发提示词的执行。

随后，GitHub 首席产品官 Mario Rodriguez 与 Anthropic 的 Brad Abrams 共同进行了分享。Rodriguez 将缓存命中率视为任何向平台发送数十亿条消息的团队都必须关注的基础指标。他表示：“这有点像高频交易，哪怕只提升 1% 的效率，整体上都意味着数百万的价值。”GitHub 的目标是将缓存命中率维持在 94% 以上，而一旦跌到 70% 左右，通常就意味着提示词组装环节出现了缺陷。Rodriguez 还列举了 GitHub 在工程实践中必须应对的 3 类缓存失效的原因。

Abrams 借此介绍了一种 advisor 策略，也就是，由较小的执行模型（比如，Haiku）仅在遇到困难场景时才调用更大的 advisor 模型（比如，Opus）。Abrams 表示：“我们能以远低于 Opus 级别的全面调用成本，获得接近 Opus 级别的智能，因为我们对 advisor 实际发送的 token 非常克制。”Rodriguez 还提到，GitHub 内部配合使用了一个 critic 模块，内部昵称为 Rubber Duck，它会在规划之后、复杂实现完成之后，以及测试编写完成但尚未运行之前进行检查。

Anthropic Managed Agents 的产品经理 Jess Yan 和 Anthropic 的技术团队成员 Lance Martin 在午间时段演示了 Claude Managed Agents，并认为当前生产级智能体的瓶颈已经不再是智能本身，而是基础设施。他们重点介绍了沙箱代码执行、检查点和凭据作用域控制等底层原语。

下午 1 点，Anthropic 联合创始人兼 CEO Dario Amodei 以及联合创始人兼总裁 Daniela Amodei 登上主舞台。Daniela Amodei 表示，开发者“是 Claude 最重要的用户”，并介绍了 Anthropic 内部的一项文化价值观：同时掌控光明与阴暗面（hold light and shade），用以指导公司如何在交付强大模型的同时配套安全护栏。Dario Amodei 则透露，以年化口径计算，Anthropic 在 2026 年第一季度的收入和使用量增长达到了 80 倍，而不是原计划的 10 倍；他认为，这正是近期算力压力的根本原因，而公司当天早些时候宣布的 与 SpaceX 的合作 则在一定程度上缓解了这一问题。

他再次重申了此前的预测：2026 年将出现一家“一个人就能创造十亿美元价值”的公司，并指出，借助 AI 构建的两人公司实际上已经突破了十亿美元估值。他认为，下一个拐点将是智能体团队以组织而非个人的层级开展工作。当前真正拖慢进展的，是软件工程中那些不可验证的部分，例如设计质量与安全审查，而 Anthropic 如今正专注于训练模型来处理这些环节。

Anthropic Claude Code 负责人 Boris Cherny 与 Bun 创建者 Jarred Sumner 通过一场现场编程展示了 Bun 如何借助 Robobun 机器人实现自维护：它会复现每一个 issue，只有当自动生成的回归测试在旧版 Bun 上失败、而在修复分支上通过时，才会创建 pull request。Datadog 工程副总裁 Sesh Nalla 则介绍了一种叫做机器工具的概念，即让智能体输出“对意图和问题域的精确规格说明”，而不是为每个局部需求临时创造出彼此割裂的工具。

随后，Vercel CEO Guillermo Rauch 与 Anthropic 平台产品负责人 Angela Jiang 进行了对谈。Rauch 表示，Opus token 大约占 Vercel AI Gateway 使用量的百分之二十几，但却占到了超过 70% 的支出；此外，自 Anthropic 最近一次升级以来，V0 上的信用花费已经翻倍。他表示，更聪明的模型让 Vercel 得以简化 harness；模型“品味”的提升，也让 V0 能够吸收 Vercel 十年来积累的设计判断，而不是与之对抗。与此同时，由于模型能够在沙箱中编写中间代码，而不再依赖预定义的子智能体，工具的范围也在收缩。Rauch 表示：“我们现在更多是在围绕工具批准（tool approval）做工程设计，本质上是在构建正确的安全护栏。”

在由 Anthropic 创业合作负责人 Beth Robertson 主持的一场圆桌中，Cognition 联合创始人 Walden Yan、Gamma AI 产品负责人 Deeni Fatiha 以及 Harvey 应用研究负责人 Niko Grupen 共同探讨了在模型指数级进步下的产品架构。Cognition 开发的是可自主编程、能够操作自己计算机的 Devin；Gamma 是一款拥有超过 7000 万用户的 AI 原生演示文档工具；Harvey 则面向法律和专业服务领域提供生成式 AI 平台。每位嘉宾都提到，自己都曾因为模型能力拐点而不得不重写产品架构。

Brad Abrams 在当天稍晚时候再次登台，单独介绍了 Claude Platform，重点讨论了提示词缓存、结构化输出以及在大规模工作负载客户中观察到的工具设计模式。Anthropic 开发者关系负责人 Alex Albert 则在收官环节提到，一年前 Claude 配合 Sonnet 3.7 在 SWE-bench Verified 上的成绩是 62%，而如今使用 Opus 4.7 已达到 87%；他还借助能力曲线，对未来的一年给出了预期。

Anthropic 的营收增速也在迅猛攀升。截至 4 月初，在公司 调整了定价模式，改为按照企业客户实际使用的 AI 量收费，而非仅收取固定费用之后，其年化销售额已达到 300 亿美元。与此同时，ServiceNow、Uber 等公司也报告称，它们在年初几个月内就已用满全年的 token 预算。

有兴趣进一步了解的开发者，可以前往 Anthropic 的 YouTube 频道观看完整会议录像，浏览 claude.com 上的 Code with Claude 专题页面，或报名参加 5 月 19 日的伦敦场 和 6 月 10 日的东京场 活动。

查看英文原文：

Anthropic&#x27;s Code With Claude Announces Managed Agents, Proactive Workflows, Capability Curve

(https://www.infoq.com/news/2026/05/code-with-claude/)

声明：本文由 InfoQ 翻译，未经许可禁止转载。

点击底部

阅读原文

访问 InfoQ 官网，获取更多精彩内容！

今日好文推荐

不会写代码的“鲸鱼哥”，被 DeepSeek 改写人生 | 专访 Hunter Bown

港股上市5个月市值翻四倍，人均95后的MiniMax再冲A股！

半数华人、3位亿万富翁：这张十年前的量化实习生合照，藏着 AI 时代的新贵版图

Opus 4.8 刚发布，被DHH和Redis之父当场拆台：跑分赢了GPT-5.5，但编码王座不稳了