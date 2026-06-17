---
publish_time: 1781155800
---

# OpenAI 为 Codex 智能体打造安全的 Windows 沙盒

> 原文链接：https://mp.weixin.qq.com/s/E9ZHbc4b50eugJKqvjQCGQ
> 公众号：InfoQ

作者 | Leela Kumili

译者 | 明知山

OpenAI 发布了旗下 Codex 编码智能体所使用的 Windows 沙盒架构 的详细技术细节，重点阐述了在微软操作系统上为兼顾安全性、可用性与开发者效率所做出的工程权衡。OpenAI 解释称，在发现现有的 Windows 隔离机制无法完全满足自主编码智能体的需求后，他们构建了一套自定义的沙盒方案。正如 OpenAI 提到，Windows 系统本身并没有一个能够直接与智能体工作负载安全执行环境映射的原生组件。

Codex 是 OpenAI 旗下的编码智能体，可通过命令行界面、IDE 扩展和桌面应用程序在开发者的本地机器上运行。由于该智能体可以执行命令、读取文件、修改源代码并执行开发任务，OpenAI 需要一种机制来限制其访问权限，同时尽量减少对开发者工作流程的干扰。据 OpenAI 技术团队成员 David Wiesen 介绍，用户此前面临着一个两难选择：要么需要逐一批准智能体的每一个操作，要么通过完全访问模式授予其不受限制的系统权限。

OpenAI 在 LinkedIn 的发布 帖子 中写道：

这套方案让运行在 Windows 系统上的 Codex 兼顾性能与安全性，开发者也能更放心地在实际工作场景中使用这款编码智能体。

OpenAI 评估了多种现有的 Windows 安全技术，包括 Windows Sandbox 和 强制完整性控制（Mandatory Integrity Control，MIC）。虽然 Windows Sandbox 通过一次性虚拟机提供了强大的隔离性，但 OpenAI 认为它并不适用，因为 Codex 需要直接访问开发者的工作环境、工具和代码仓库。此外，Windows Sandbox 并非所有 Windows 版本都支持，从而限制了它的使用场景。

第一个实现方案在内部被称为“非提升权限沙盒”（Unelevated Sandbox），它结合了 Windows 安全标识符（SID）、访问控制列表（ACL）和写入限制令牌。OpenAI 引入了一个合成安全标识符

sandbox-write

，仅授予对指定目录（如当前工作区和手动配置的写入位置）的写入权限。敏感路径（包括 Git 元数据目录）则通过 ACL 强制执行保持受保护状态。

OpenAI 随后将系统重新设计成“提升权限沙盒”（Elevated Sandbox）。在部署过程中，沙盒会创建专术的本地 Windows 账户，包括

CodexSandboxOffline

和

CodexSandboxOnline

。相关命令会在这些隔离账户下通过受限令牌运行。网络访问可以通过防火墙规则进行控制，从而在保留常用开发者工作流兼容性的同时严格划定文件系统和网络边界。

完整的沙盒架构（来源：OpenAI 博客文章）

该公告也引发了开发者对编码智能体安全影响的讨论。Marcus 在 X 平台上 评论 道：

这个沙盒架构简直就是幕后英雄。其他编码智能体都会随意读写你的文件系统，而运行在 Windows 上的 Codex 实现了环境隔离，你大可放心让它运行，无需时刻提防。

随着编码智能体越来越能够代表用户执行操作，供应商必须在严格的安全约束与流畅的自动化体验之间找到平衡。与传统应用程序不同，自主编码智能体需要访问源代码、开发工具和操作系统资源，又要维持有效的隔离边界。OpenAI 的方案也说明，现有操作系统原生功能需要整合与适配，才能适配这类新兴工作场景，兼顾可用性、兼容性与安全管控。

查看英文原文：

https://www.infoq.com/news/2026/06/codex-windows-sandbox-design/

今日好文推荐

Anthropic 祭出双旗舰模型 Fable、Mythos，屠榜所有基测！网友：除了贵没毛病

人形机器人价格大跳水，比iPhone还便宜：一场关于生产力而非形态的产业竞速

大人，AI编程又变天了！Claude Code之父、龙虾创始人同时力捧新范式，杀死提示词工程？

WWDC 2026，硅谷历史上最昂贵的认输：1.2 万亿参数 Siri 来自 Gemini，但你的手机跑不了