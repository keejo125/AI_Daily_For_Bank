---
publish_time: 1778040000
---

# DeepSeek版Claude Code登顶热榜：8700星，鲸鱼哥火了

> 原文链接：https://mp.weixin.qq.com/s/A7ATOoYGBWwf1dpV9GIevw
> 公众号：机器之心

编辑｜泽南

感谢鲸鱼兄弟开源。

DeepSeek V4 才推出一个星期，DeepSeek 版的 Claude Code 就登顶了 GitHub 热榜。大家缺的就是这么一个工具。

目前已经有了超过 8700 的 Star 量，数字还在以肉眼可见的速度增长。

这还只是个开始。

DeepSeek TUI 是一个完全运行在本地终端里的 AI 编程智能体，由自称「鲸鱼兄弟」的 Hunter Bown 用 Rust 语言开发。它专门为 DeepSeek（尤其是最新发布的 DeepSeek V4 大模型）打造，能提供终端原生、长上下文、推理过程可视化的使用体验与效果。

它用开放工具链和极低的成本，打响了替代主流高价 AI 编码助手的第一枪。

GitHub 链接：https://github.com/Hmbown/DeepSeek-TUI/tree/main

基于 DeepSeek TUI，开发人员能够直接从终端与 DeepSeek 模型进行聊天、编辑文件、运行 shell 命令、管理任务，甚至协调代码库中的子智能体。所有这些都具有可配置的审批门控，使其功能与更成熟的商业工具相媲美。

简单来说就是可以用 DeepSeek 的那一套完全代替 Claude Code。

把 DeepSeek 的

「

脑回路

」

搬进终端

这款工具与普通封装工具的不同之处在于它与 DeepSeek 的推理功能深度集成。当开发者发出复杂命令时，该工具会进入「思考模式」来分析代码库。

在你使用 DeepSeek TUI 的过程中，

DeepSeek 标志性的思维链会实时流式输出到终端

，你能实时看到模型是怎么分析代码问题的、走了哪条解决路径、甚至中途是否自我纠错或改变主意。整个「脑回路」对开发者完全透明。

针对 DeepSeek V4 带来的

100 万 Token 超大上下文窗口，DeepSeek TUI 默认用满

，还有上下文压缩机制，让你在跑复杂项目或者重构整个代码库时，不用担心 AI 中途出现「记忆断档」。

此外，DeepSeek TUI 还有一个 RLM（Recursive Language Model）模式，这种并行任务处理机制利用 DeepSeek 便宜的特性搞并发调度，

能同时驱动最多 16 个 V4 Flash 子任务跑批量分析

，能实现高效率、低成本的复杂编程任务处理。

由于 Flash 模型的输出价格仅为 Pro 模型的约三分之一。RLM 模式将大部分扇形子任务交给 Flash 处理，能显著降低整体项目的 API 费用。

DeepSeek TUI 的操作模式分三档：

分别是只读的 Plan 模式，用于输出任务拆解计划，梳理修改思路。

默认的 Agent 模式，拥有完整的工具链权限，但每当它准备执行关键操作时需要你手动确认。

全自动的 YOLO 模式，所有的手动审批弹窗都会被关闭。AI 拥有完全的自主决策权和执行权。

目前在终端原生编码智能体上，虽然像 Claude Code 这样的专有系统已几乎成为标准，但它们通常需要付费 API 访问权限，并且运行在封闭的生态系统中。DeepSeek-TUI 则打破了这种局面，它依托 DeepSeek 的低成本模型堆栈，以极低的成本提供类似的工作流程。

作者半路出家，用魔法打败魔法

说到这个项目的开发者 —— 这个基于开源的 DeepSeek 打造的开源工具 DeepSeek TUI，是一个美国极客打造的。

随着该项目的走红，5 月 3 日，Hunter Bown 已经在感谢鲸鱼兄弟了：「这是我人生中最疯狂的两天。」

一月份做出来的项目，到五一随着 DeepSeek V4 的发布热度直接来了个直角上升。

更有趣的是，Hunter Bown 是个「半路出家」的程序员。他在学校学习的是乐队指挥、法学，现在是

南卫理公会大学（SMU）专利法专业的二年级学生。

他自建了名为 Shannon Labs 的工作室，定位是 AGI 时代的下一个贝尔实验室。

不过人家说了，以前学的也没白学，指挥乐队和管理开源项目是相通的。

他打造 DeepSeek TUI 使用的是 AI 辅助编程，「工作流完美闭环」的过程，这可以说已是 AI 自我迭代的雏形了。

既然 DeepSeek 来自中国，Hunter Bown 正在积极寻求与国内开发者交流，他已答应大家，一定好好学中文。

不过就算没学好问题也不大，实在不行，现在有 DeepSeek 翻译。

参考内容：

https://shannonlabs.dev/

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com