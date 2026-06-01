---
publish_time: 1780193700
---

# Zod 作者推出 Pullfrog：一个跑在 GitHub Actions 里的开源 AI 编程 Agent

> 原文链接：https://mp.weixin.qq.com/s/XF5Aa2J4uCnI8NZByJDMBQ
> 公众号：InfoQ

作者 ｜ Daniel Curtis

译者 ｜ 田橙

Pullfrog 是由 Colin McDonnell 创建的一款开源 AI 驱动的 GitHub bot，目前处于 beta 阶段。它将自己定位为 CodeRabbit 的模型无关替代方案，并且完全运行在 GitHub Actions 内部。

McDonnell 最广为人知的身份，是 Zod 的创建者。Zod 是一个 TypeScript 优先的 schema 验证库，在 GitHub 上拥有超过 42,000 个 star。他于 2026 年 5 月 12 日 发布 了 Pullfrog。该工具被设计为 GitHub 内部异步开发的编排层，可以监听 webhook，并根据可配置事件触发 AI agent 运行，例如新的 pull request、issue、CI 失败以及 review 提交。

与 CodeRabbit 不同，后者是一个托管式 SaaS 平台，并使用自己的 AI 模型；Pullfrog 采用的是自带密钥（bring-your-own-key，BYOK）的方式。开发者可以连接任意 LLM 提供商，包括 Anthropic、OpenAI、Google、Mistral、DeepSeek 和 OpenRouter，并且只需修改一项配置，就可以在不同模型之间切换。所有 API key 都通过 GitHub 的 secret 管理系统存储，agent 运行则通过一个专用的 pullfrog.yml workflow 文件，在仓库自己的 GitHub Actions 环境中执行。

开始使用 Pullfrog，需要先安装 Pullfrog GitHub App，并向仓库中添加 workflow 文件。

之后，开发者可以在任何 issue、pull request 或评论中标记 @pullfrog 来触发一次 agent 运行，也可以在 Pullfrog 控制台 中配置自动化触发器。完整的安装指南可以在 官方文档中 查看。

该 agent 自带一个专门构建的 MCP server，用于执行 git 和 GitHub 操作，例如创建 pull request、留下 review、读取 CI 日志以及管理 issue。Shell 命令会在隔离的子进程中运行，无法访问敏感环境变量。它还内置了一个无头浏览器工具，使 agent 无需额外配置，就可以运行端到端测试、截图，并对 UI 进行迭代。

近几个月，AI 代码审查领域的竞争格局已经明显扩大。自 2023 年以来，CodeRabbit 一直是专门代码审查工具中的既有领导者；而 GitHub Copilot 的代码审查能力于 2025 年 4 月 推出，并凭借原生平台集成实现了快速采用。Greptile 和 Bito 等其他工具也在这一领域展开竞争。

Pullfrog 的差异化之处在于，它采用开源许可证，具备模型无关性，并且覆盖范围更广，不止于代码审查，还扩展到 issue 分流、CI 自动修复、合并冲突解决和计划生成。

该发布在社区中引发了超过 50 条回复和超过 1,000 个点赞。一位用户问道：

它能不能在本地运行，用于那些还没推送到 GitHub 或云端 Agent 的 Agentic 工作流？

对此，McDonnell 回复道：

Pullfrog 是构建在 OpenCode 和 Claude Code 之上的一层运行框架，主要面向 CI 场景。

如果是本地开发，你可以直接使用 OpenCode 或 Claude Code，并让它们访问 git 和 gh CLI。我们很快会推出一个 CLI，用来快速启动运行在 GitHub Actions 里的云端 Agent。不过，我们并不打算把 Pullfrog 做成一个本地开发时使用的 Agent。

Pullfrog 是由 Colin McDonnell 创建的一款开源 AI 驱动的 GitHub bot，McDonnell 最知名的身份是 Zod 的作者。它为 pull request review、issue 分流和 CI 修复提供模型无关、基于 agent 的自动化能力，并且完全运行在 GitHub Actions 中，而不需要依赖托管式第三方服务。自 2025 年底首次预览以来，该项目的源代码已经获得了超过 400 个 star。

原文连接：

https://www.infoq.com/news/2026/05/pullfrog-ai-github/

声明：本文由 InfoQ 翻译，未经许可禁止转载。

点击底部

阅读原文

访问 InfoQ 官网，获取更多精彩内容！

今日好文推荐

港股上市5个月市值翻四倍，人均95后的MiniMax再冲A股！

半数华人、3位亿万富翁：这张十年前的量化实习生合照，藏着 AI 时代的新贵版图

Opus 4.8 刚发布，被DHH和Redis之父当场拆台：跑分赢了GPT-5.5，但编码王座不稳了

前 CEO 被学生嘘“别吹AI”，现 CEO 被追问“会不会被AI取代”：谷歌两代掌门人的AI信仰，同时被质疑