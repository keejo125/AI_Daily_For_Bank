---
publish_time: 1789790400
status: confirmed
category: 国际
is_model_related: false
digest: |
  Claude Code 自 2.1.277 版本起支持 AGENTS.md：项目无 CLAUDE.md 时回退读取 AGENTS.md，并开源 agents-md mod。此举使 Claude Code 首次加入跨厂商"Agent README"标准，OpenAI Codex 负责人亦公开祝贺。此前 Shopify CEO 曾因配置入口不统一（CLAUDE.md 与 AGENTS.md 分叉）考虑禁用 Claude Code。分析认为项目指令文件正从工具偏好演变为代码库基础设施，主流 harness 围绕统一"Agent README"收敛，跨工具迁移成本将持续降低。
link: https://mp.weixin.qq.com/s/u3oTtbEFuTUAPWsEYZSXkw
source: 机器之心
title: Anthropic接受OpenAI标准，智能体从此共用一份AGENTS.md
---

# Anthropic接受OpenAI标准，智能体从此共用一份AGENTS.md

来源：机器之心
原文链接：https://mp.weixin.qq.com/s/u3oTtbEFuTUAPWsEYZSXkw

编辑｜泽南、杨文
Anthropic 要 Open 起来了？
刚刚，Claude Code 成员 Thariq Shihipar（@trq212）发帖称，Claude Code 开始支持 AGENTS.md 文件了。
从 2.1.277 版本开始，如果项目目录中没有 CLAUDE.md，Claude Code 会检查并使用 AGENTS.md。用户可以通过 /config 切换这项行为。
这项能力建立在 Claude Code 的 mods 机制上。Anthropic 已将 agents-md 做成内置 mod，并公开了相关源码。
相关源码链接：https://github.com/anthropics/claude-code/tree/main/mods/agents-md
Thariq 表示，未来开发者也可以围绕项目指令构建自定义版本。
AGENTS.md 就像是项目写给 AI Agent 看的说明书，里面的内容旨在告诉 Agent 项目的结构、怎么安装依赖、运行哪些测试、代码规范是什么等等。官方 AGENTS.md 网站也明确把它称为「README for agents」。Claude Code 的这次改动第一次让这个热门的 harness 加入了跨厂商的项目指令标准之中。
消息一出，网友喜大普奔，评论区迅速被「终于统一了」、「Thanks」刷屏。
甚至连 OpenAI Codex 负责人 Tibo 也跑来祝贺：「太好了！这就对了。欢迎来到光明的一边。」
要知道，AGENTS.md 最初就是源自 OpenAI 的 Codex。表面上水火不容的 Anthropic 和 OpenAI，在竞争激烈的 Agent 赛道上现在倒是走到了一块。
Claude Code 开始兼容 AGENTS.md
在默认模式下，Claude Code 会沿项目目录树查找 AGENTS.md，只要项目路径上没有项目级 CLAUDE.md，找到的文件就会作为项目指令加载。
当 Agent 读取项目子目录中的文件时，mod 还会按目录层级补充对应的 AGENTS.md。如果同级目录存在 CLAUDE.md，则遵循原有的 CLAUDE.md 规则。
相关设置位于 /config 的 Project instructions 中。用户可以选择仅使用 CLAUDE.md，在没有 CLAUDE.md 时回退到 AGENTS.md，也可以同时加载两类文件。具体采用哪种方式，可以根据项目的协作模式进行调整。
这意味着，Claude Code 不必再完全依赖自身的文件命名约定，对于已经使用 AGENTS.md 管理项目规则的团队，接入成本明显降低。
Shopify 曾把兼容问题摆上台面
前段时间，机器之心就报道过，
Shopify CEO Tobi Lütke 曾考虑在公司内部禁用 Claude Code
，直到它支持读取 AGENTS.md、.agents/skills 等文件。
当团队成员同时使用 Codex、Cursor 和 Claude Code 时，同一个仓库可能出现不同的配置入口。使用 Codex 的开发者读取 AGENTS.md，使用 Claude Code 的开发者读取 CLAUDE.md。如果两份文件存在差异，不同 Agent 获得的项目规则也会不同。
这些文件通常记录项目结构、编码规范、测试要求、开发流程，以及 Agent 可以调用的技能。它们已经成为 AI coding Agent 理解代码库的重要上下文。
开发者此前给出的解决办法包括建立软链接，或者在 CLAUDE.md 中写入 @AGENTS.md。小型项目比较容易采用这些方案，到了大型 monorepo，配置文件会沿目录树递归生效，维护成本也会迅速上升。
Lütke 认为，团队不应该长期承担这类同步工作。他把这种额外负担称为「复杂性税」。
Anthropic 为何坚持 CLAUDE.md ？
Anthropic 此前也有自己的产品考虑。
Thariq 曾解释，不同模型家族具有不同的行为特点，system prompt 会显著影响模型表现。Claude 模型对 skills、system prompt 和 CLAUDE.md 的组织方式有特定偏好，Claude Code 也会针对不同模型调整 system prompt。
这套思路与 Anthropic 关于 context engineering 的讨论相呼应。项目说明、技能文件和 system prompt，共同构成 Agent 完成任务所需的上下文。
这种模型专属设计有助于优化 Claude Code 体验，也会增加跨工具协作的维护成本。
支持 AGENTS.md 只是第一步
这次更新首先解决了文件读取入口的问题，对于已经使用 AGENTS.md 的团队，Claude Code 不再需要额外的软链接或引用配置。
不过，兼容并不等于完全统一。在默认模式下，只有项目路径上没有 CLAUDE.md 时，Claude Code 才会回退读取 AGENTS.md。如果团队希望同时加载两类文件，还需要在 /config 中调整设置。
此外，.agents/skills 和 .claude/skills 仍是两套独立目录。团队依然需要决定哪些规则属于跨工具的共同内容，哪些内容只服务于 Claude Code。
随着 AI coding Agent 进入日常开发流程，项目指令文件正在从工具偏好变成代码库基础设施。Claude Code 此次加入 AGENTS.md，说明跨工具共享项目上下文已经成为开发团队的现实需求。
此前 Claude Code 是这个标准最大的缺席者之一，Claude Code 加入以后，主流 AI Coding 工具围绕「Agent README」收敛的趋势就明显得多了。未来可以预见的是，不同 Harness 之间的迁移成本将会越来越低。
那么问题来了，现在哪家 Harness 更好用呢？
参考链接：
https://x.com/trq212/status/2101009392611278961?s=20
https://github.com/anthropics/claude-code/tree/main/mods/agents-md
© THE END
转载请联系本公众号获得授权
投稿或寻求报道：liyazhou@jiqizhixin.com
