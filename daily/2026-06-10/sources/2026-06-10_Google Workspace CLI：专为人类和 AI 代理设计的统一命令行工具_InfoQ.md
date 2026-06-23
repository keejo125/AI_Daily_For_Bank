---
publish_time: 1781055590
---

# Google Workspace CLI：专为人类和 AI 代理设计的统一命令行工具

> 原文链接：https://mp.weixin.qq.com/s/9yCoeZSN0BmUwMC9Oauyjw
> 公众号：InfoQ

作者 ｜ Daniel Curtis

译者 ｜ 平川

Google Workspace CLI 发布，为 Drive、Gmail、日历、表格、文档、聊天、管理控制台以及所有其他 Google Workspace API 提供了一个统一的接口。该 CLI 采用 Rust 语言编写，遵循 Apache 2.0 许可协议，旨在同时支持人工操作者和 AI 代理的工作流程，并提供结构化的 JSON 输出以及 100 多种内置的代理技能。

与提供静态命令列表的传统 CLI 工具不同，gws 会在运行时读取谷歌自有的 Discovery Service，并动态构建其完整的命令集。当谷歌添加或更新 API 端点时，CLI 会自动检测到这些变化，不需要发布新版本。该工具还包含一组以 + 为前缀的辅助命令，用于处理发送电子邮件、整理收件箱以及生成每日站会报告等常见工作流。

该工具需要 Node.js 18 或更高版本（或来自 GitHub Releases 的预编译二进制文件）、一个用于 OAuth 凭据的 Google Cloud 项目，以及一个具有 Workspace 访问权限的谷歌账户。安装可以通过 npm、Homebrew、Cargo 或 Nix 进行：

npm install -

g

@googleworkspace

/cli

安装完成后，初始设置和身份验证可通过以下两条命令完成：

gws

auth setup

gws auth login

然后，与 Workspace 服务的交互遵循一致的模式。例如，列出最近的 Drive 文件只需一次调用：

gws

drive files list --params &#x27;{

"pageSize"

:

10

}&#x27;

代理技能生态系统是其核心功能之一。各项技能以 SKILL.md 文件的形式打包，涵盖了所有受支持的 API。该 CLI 还包含一个 MCP 服务器选项，用于连接 Claude Code 和 Gemini CLI 等工具。Google Cloud 总监 Addy Osmani 将该 CLI 描述 为“专为人类和代理而打造”。该代码库在 GitHub 上已获得超过 26500 个星标。

社区反响褒贬不一。在 Hacker News 上，多位用户称赞了动态命令生成功能，以及向“命令行优先”工具体系的整体转变。

一位评论者指出：

企业终于开始为那些早在几年前就该配备 API 的功能提供 API 了。

另一人则提醒道：

这并非谷歌官方支持的产品。

这一点在 GitHub Readme 中已经以注释的形式做了说明，并警告说，该项目正处于积极开发阶段，预计会出现破坏性变更。

一位 Hacker News 用户 表示，他花了 45 分钟时间按照默认设置流程进行操作，结果却遇到了配额限制和验证错误：

我在配置过程中遇到了各种错误和问题，现在我正在进行 gws auth login，并尝试选择 OAuth 权限范围。我直接接受了默认设置并选择了 recommended 选项，结果却收到了警告，说权限范围过多可能会导致错误（那为什么这还是推荐设置呢？），果然，在浏览器中尝试身份验证时就报错了。

在 Reddit 上，讨论更为热烈。一位用户将 gws 与 Claude Code 连接起来，让该代理阅读、总结并处理电子邮件。据他说，这种体验比之前的脚本方法“简单得多”。这款由社区驱动的 Microsoft 365 命令行工具（CLI） 为微软生态系统提供了类似的交互界面，当前版本为 11.7.0，支持 SharePoint、Teams、Entra ID 和 Power Platform。虽然受益于成熟的插件架构和更直观的身份验证流程，但与 gws 不同，它通过 npm 提供静态命令集，而非动态生成命令。

存储库的 README 文件 中提供了完整的设置说明、身份验证选项和故障排除指南。

原文链接：

https://www.infoq.com/news/2026/06/google-workspace-cli/

声明：本文由 InfoQ 翻译，未经许可禁止转载。

点击底部

阅读原文

访问 InfoQ 官网，获取更多精彩内容！

今日好文推荐

大人，AI编程又变天了！Claude Code之父、龙虾创始人同时力捧新范式，杀死提示词工程？

WWDC 2026，硅谷历史上最昂贵的认输：1.2 万亿参数 Siri 来自 Gemini，但你的手机跑不了

Notion 全面禁用Anthropic，并用模型降智把 Opus 4.8 送上热搜！12小时后紧急澄清系笔误

“英伟达也缺算力！”顶尖 AI 研究员转投 xAI 内幕：谁 GPU 管够，就去哪里