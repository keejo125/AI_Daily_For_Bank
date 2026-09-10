---
publish_time: 1786411855
status: confirmed
category: 国内
is_model_related: false
digest: |
  Bun创建者Jarred Sumner利用并行Claude智能体，仅用11天将Bun从Zig移植到Rust，耗资约16.5万美元，展示了AI完成大规模软件重构的可行性。Zig创始人Andrew Kelley随即发文回应，将问题归咎于Sumner不规范的编程实践而非语言差异。

  Kelley指出争议核心在于"两个项目截然不同的价值观体系"，而非语言功能或AI使用本身。事件背景包括：Bun被Anthropic收购后大量使用AI维护代码（RoboBun Bot已是合并PR数量最多的贡献者），以及Anthropic 3月发生的51.2万行代码泄露事件被追溯至Bun的源映射漏洞。该争议引发了关于AI生成代码质量管控与工程规范的广泛讨论。
link: https://mp.weixin.qq.com/s/g5_U5DhVICANoboyAbFAhA
source: InfoQ
title: Zig 创始人直言，Bun 靠 Claude 生成的 Rust 重构版是“没人把关的烂代码”
---

# Zig 创始人直言，Bun 靠 Claude 生成的 Rust 重构版是“没人把关的烂代码”

来源：InfoQ
原文链接：https://mp.weixin.qq.com/s/g5_U5DhVICANoboyAbFAhA

作者 | Joab Jackson
译者 | 平川
策划 | Tina
一款广受欢迎的、隶属于 Anthropic 公司的 JavaScript 运行时及工具链在利用 AI 重写后，因其执行速度之快而广受赞誉，但也因其项目背后糟糕的编码实践而遭到批评。
上周，Bun 的创建者 Jarred Sumner 宣布，他利用一批并行运行的 Claude 智能体，仅用 11 天就将 Bun 从 Zig 编程语言移植到了 Rust 语言。按 API 定价计算，这项工作耗资约 16.5 万美元。这表明，此前被认为规模过大而无法实施的软件重构，如今借助 AI 技术已经变得可行。
Sumner 表示，鉴于 Bun 用户发现的漏洞数量日益增多，这次移植势在必行，其中包括一个与近期 Claude 源代码泄露事件有关的漏洞。
但 Zig 语言的创建者 Andrew Kelley 不希望自己的项目被视为 Bun 困境的罪魁祸首，他将问题归咎于 Sumner 不规范的编程实践。
Kelley 在文中写道，对他而言，转向 Rust 并非关乎两种语言的功能差异，甚至与 AI 的使用也无关，而是源于“两个项目截然不同的价值观体系”。
Bun 的孕育
Bun 是一套 JavaScript 工具集，包含运行时、包管理器、打包工具和测试运行器。一些开发者青睐它，是因为它是一个与 Node.js 配合良好的快速一站式解决方案。
为了 提升 Bun 的运行速度，Sumner 采用了苹果公司内存占用低、启动速度快的 WebKit JavaScriptCore（JSC）引擎，而非谷歌的默认引擎 V8 。他选择了当时正崭露头角的 Zig 语言，因为看中了其性能和底层控制能力。
Anthropic 于 2025 年 12 月 收购 了 Bun。该公司基于 Bun 构建了其核心状态机。
到那时，Sumner 也逐渐认识到 AI 的编程能力，并在 Bun 的维护工作中大量运用了 AI。 在收购发生时，一个名为 RoboBun 的 Claude Bot 已经在 Bun 代码库中承担了大量繁重的工作。它是所有贡献者中合并 PR 数量最多的，负责修复 Bug 并解决测试失败的问题。
但随着 Bun 用户群的扩大，代码中开始出现越来越多的漏洞。用户在软件各处发现了问题。Anthropic 3 月份发生的 51.2 万行代码泄露事件？据 NodeSource 报道，这其实是 Bun 的过错，因为 Bundler 中存在一个漏洞，即使被明确禁止，它仍然会在构建过程中生成源映射文件。
Sumner 在上周 详细介绍 此次迁移的博文中解释说，所有这些漏洞都不是 Zig 的过错。Bun 的架构混合了垃圾回收和应用程序驱动的内存管理。Sumner 承认，Zig 原本就不是为此类任务而设计的。Rust 在自动化内存管理方面确实更胜一筹。
Bun 的 Rust 化
如果手动将 50 万行 Zig 代码用另一种语言重写，那将是一项浩大的工程。Sumner 写道，“用另一种语言重写代码，一个小型工程师团队需要整整一年的时间。这意味着在此期间， Bug 修复、安全修复或功能开发都将暂停”。
因此，Sumner 选择了 Claude。他启动了约 50 个动态 Claude Code 工作流，峰值时每分钟可生成约 1300 行代码，最终生成了 超过 100 万行的 Rust 代码。这项工作耗时 11 天，按 API 定价计算成本约为 16.5 万美元。其中，Claude Fable 承担了大部分繁重的工作。
随后，基于 Rust 的 Bun 项目接受了 Bun 自身包含的超过 100 万条断言的测试套件的全面检验。据 Sumner 称，该项目在所有受支持平台上 100% 通过了 测试，而且未跳过或删除任何测试项。
HashiCorp 联合创始人 Mitchell Hashimoto 大为震撼。他 在 X 平台上指出，“以那样的薪资水平，工程师绝对不可能在 11 天内达成 Claude 所完成的里程碑”。
Zig 与 Bun 的摇摆往事
但 Bun 的快速开发速度是否违背了优质软件开发的核心原则？
Zig 公司的 Kelley 对此并不买账。在一篇题为“我对 Bun 用 Rust 重写的看法”的博文中，他慷慨激昂地表达了自己的疑虑。
Kelley 写道，甚至在 Anthropic 收购之前，“我们对在 Bun 代码库中看到的编程实践感到越来越震惊”。Bun 是使用 Zig 语言开发的规模最大、知名度最高的项目之一，在被 Anthropic 收购之前，它一直是 Zig 软件基金会的定期捐助者。
在 Kelley 看来，该项目激进地发布新功能，导致 Bug 堆积如山、错误处理代码拙劣，并积累了大量的技术债务。
Kelley 打趣道：“早在获得大语言模型（LLM）访问权限之前，Sumner 就已经在写一团糟糕的代码了。”他推测，Sumner 可能面临着必须达成商业目标而非技术目标的压力，而这种压力在被 Anthropic 收购后愈发加剧。
事实上，在 Kelley 看来，Bun 的代码库已经变得如此令人怀疑，以至于 Bun 与 Zig 分道扬镳反而是个好消息。他写道：“这个曾被公众视为 Zig 编程语言典范的项目，实际上已经不再是‘如何不编写 Zig 代码’的典型案例。”
Bun 团队还曾尝试将部分 AI 辅助开发成果回馈给 Zig 项目，但未果。正如 Reg 杂志眼尖的记者 Tim Anderson 今年 5 月披露 的那样，在重写 Bun 之前，该团队维护着一个 Zig 分支，据称其调试编译速度提高了四倍。但 Zig 项目以“不接受基于 AI 的贡献”这一政策为由，拒绝了 Bun 的改动。
Zig 此前一直涌入大量由大语言模型（LLM）生成的提交代码，其中大部分质量堪忧。Kelley 认为，对 AI 生成的代码缺乏工程监督，将来会导致无数的问题。
Kelley 指出，如果 Bun 的测试在 Zig 代码中都未能发现这些 Bug，那么在未经监督的 Rust 代码中又如何能发现它们呢？
他写道，“支持发布这 100 万行未经审核代码的论点是，测试套件足够完善，能够发现所有问题。它连 Zig 代码中的 Bug 都无法完全发现，却足以发现 100 万行未经审核的粗制滥造的代码中的 Bug 吗？”
原文链接：
https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743
声明：本文为 InfoQ 翻译，未经许可禁止转载。
今日好文推荐
“写代码从来都不是难点”，这是对全世界所有程序员的严重侮辱
Rust 给 AI 编程立新规：能帮你看，不能替你写，用多了还会“熔断”
MiniMax H3 团队 Reddit 上回应一切：2K 要开源，图像模型在路上，Apache 2.0 也在考虑了
涨价30倍仍是最便宜的模型，DeepSeek可能有这个底气
