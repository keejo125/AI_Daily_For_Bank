---
publish_time: 1786519800
status: confirmed
category: 国际
is_model_related: false
digest: |
  Oracle 针对 OpenJDK 贡献者发布《OpenJDK 关于生成式 AI 的临时政策》，明确规定社区贡献不得包含任何由 LLM、扩散模型等深度学习系统部分或全部生成的内容，范围涵盖源码、文本、图像、Pull Request、邮件、Wiki 页面与 JBS Issue。

  开发者可私下用 AI 工具理解、调试、审查 OpenJDK 代码或开展相关研究，但不得将 AI 生成内容贡献到社区。这一「外松内紧」的规则与 Oracle 自身积极拥抱 AI 编程的态度形成反差，引发对 AI 生成代码进入核心基础设施边界的讨论。
link: https://mp.weixin.qq.com/s/QqofSV9bmjxHBx0cJ3CC0Q
source: CSDN
title: OpenJDK“封杀”AI生成代码，Oracle发新规！
---

# OpenJDK“封杀”AI生成代码，Oracle发新规！

来源：CSDN
原文链接：https://mp.weixin.qq.com/s/QqofSV9bmjxHBx0cJ3CC0Q

编译 | 苏宓
出品 | CSDN（ID：CSDNnews）
近日，Oracle 针对 OpenJDK 贡献者发布了一项新规：
禁止提交由 AI 生成的代码。
这并非一项建议，而是一条硬性要求。作为 Java 的参考实现、并支撑着全球大量企业级软件的核心基础设施，OpenJDK 的这一决定迅速引发了外界对 AI 生成代码的讨论。
除此之外，更令人疑惑的是，制定这项规则的 Oracle，自己却在积极拥抱 AI 编程，并公开强调 AI 正在改变软件开发方式。一边是对 AI 编程的积极拥抱，另一边却对 AI 生成代码设下限制，这种看似矛盾的态度，也难免引发众人关注。
这项政策到底说了什么？
在这份名为《OpenJDK 关于生成式 AI 的临时政策》声明中，Oracle 说的非常直白：
OpenJDK 社区中的贡献不得包含任何由大型语言模型（LLM）、扩散模型或类似深度学习系统部分或全部生成的内容。这里所说的“内容”包括但不限于：OpenJDK Git 仓库中的源代码、文本和图像，以及 GitHub Pull Request、电子邮件、Wiki 页面和 JBS Issue 中的相关内容。
不过，Oracle 并不是完全禁止开发者使用 AI 工具。
Oracle 指出，OpenJDK 社区的贡献者可以私下使用生成式 AI 工具，帮助理解、调试和审查 OpenJDK 代码及其他内容，也可以利用这些工具开展与 OpenJDK 项目相关的研究，
但前提是不得将这些工具生成的内容贡献到 OpenJDK 社区。
对此，有开
发者
Kanishk Singh
整理了这套规则下的贡献流程：
贡献者
必须勾选确认提交内容合规，合并请求才会进入人工审核流程。
Contributor&#x27;s local workflow          OpenJDK contribution pipeline
┌───────────────────────┐            ┌─────────────────────────┐
│ AI used privately to  │            │ Pull request opened     │
│ explain,debug,research│  ───────►  │   │                     │
└───────────────────────┘            │   ▼                     │
│Skara compliance checkbox│
Human writes and owns the  ─────────►│ (
&quot;not AI-generated&quot;
)    │
actual submitted code                │   │                     │
│   ▼                     │
│ Human reviewer          │
│   │                     │
│   ▼                     │
│ Merge                   │
└─────────────────────────┘
之所以这么做，Oracle 给出的理由包括，如果直接使用 AI 生成的代码会增加代码审核负担、安全风险，以及 AI 生成内容尚未解决的知识产权归属问题
。
Oracle 着重强调：OpenJDK 支撑着全球大量关键业务系统。在这种情况下，看起来正确但隐藏细微错误的代码，会带来另一种风险——尤其是在代码审查者往往无法可靠判断某次修改究竟来自人类，还是 AI 自动生成时。
关于 AI 使用，Oracle 自己内部并没有统一答案
让这件事变得耐人寻味的地方在于，同一时期，Oracle 旗下另一个开源项目采取了完全不同的态度。
其中，由 Oracle Labs 推动的 GraalVM 项目，此前发布的 Coding Assistants 政策明确允许 AI 辅助贡献。
但它设置的门槛并非一刀切禁止，而是设立责任制度：无论是否借助 AI，贡献者必须能够解释、论证、长期维护自己提交的所有代码；这一政策鼓励主动披露 AI 参与情况，但不作强制要求。
也就是说，同一家企业内部，两个开源项目面对同一类潜在风险，制定了截然相反的规则：OpenJDK 选择全面禁止 AI 生成代码；GraalVM 选择 “可以自由使用 AI，但贡献者全权负责”。
两种方案从工程角度都具备合理性，但放在一起，很难让人认为 Oracle 对 AI 代码已经形成统一、成熟的立场。
这种矛盾，在 Oracle 管理层过去公开表达的观点衬托下更加明显。
在 2025 年 Oracle AI World 大会上，Oracle 联合创始人兼 CTO Larry Ellison 曾表示，Oracle 内部的软件开发已经不再真正意义上是“写代码”。工程师只需要描述他们希望程序实现什么功能，而模型会生成具体的实现步骤。
Oracle 联席 CEO 也曾多次强调，公司正在快速采用 AI 编程工具，并将其视为保持竞争力的必要手段，而不是需要回避的风险。
为什么这项政策引发关注？
严格来说，Oracle 对 OpenJDK 实施 AI 代码禁令，并不是毫无道理。代码审查能力、安全问题，以及 AI 输出的知识产权来源不明确，确实是所有大型开源项目都需要面对的问题。
许多其他重要开源项目，也都在讨论类似问题。但真正引发争议的是这项政策背后隐藏的信息：一家最积极推动 AI 编写生产级代码的公司，却决定对于自己最重要的基础设施项目，仍然要求每一行代码背后必须有人承担责任。
这与 Oracle 目前大举押注 AI 的做法，多少有些矛盾。如今，Oracle 正投入数百亿美元建设 AI 数据中心基础设施，但这笔巨额投资能否带来预期回报仍存在不确定性，公司也因此面临信用评级压力。今年早些时候，Oracle 还曾将 AI 的快速发展，作为调整员工结构的因素之一。
对于那些正在开发 AI 编程工具的团队来说，这或许才是这项政策最值得关注的地方：Oracle 并不是反对 AI 编程，而是说明了一件事——即使是一家正在大力押注 AI 的公司，也不认为 AI 生成的代码可以在没有人工审核和负责人的情况下，直接进入关键软件项目。
来源：
https://openjdk.org/legal/ai
https://medium.com/@kanishks772/oracle-just-banned-ai-code-from-openjdk-the-reason-is-going-to-upset-ai-developers-bc577ee7c73d
“写代码从来都不是难点”？25年开发者怒写3000字反驳：这句话是对所有程序员的一种侮辱！
一人干满 27 人活却带不动组织？360 廖百成拆解 AI-Native 时代的“黑灯公司”
OpenAI资深研究科学家、Transformer联合作者Lukasz Kaiser领衔，2026 奇点智能大会·北京站正式官宣
📢
最后，说一件事
2026 奇点智能大会
，终于要和大家见面了。
11 月 20-21 日·北京，奇点智能研究院联合 CSDN，把两场技术大会放在了同一个时空里：
奇点智能技术大会（始于 2016）——聊大模型、AI Native、企业级 AI 落地、多模态与世界模型；
C++ 及系统软件技术大会（始于 2005）——聊现代 C++ 演进、AI 算力与推理优化、高性能低时延系统。
为什么要放在一起？因为我们越来越相信——上层 AI 应用的爆发，离不开底层系统软件的支撑；而底层技术的演进方向，也正在被 AI 重新定义。
这次大会汇聚 70+ 位技术专家、18 个主题、1000+ 同行到场。
如果你也在这些方向上做研究、做产品、做工程，别错过。
if like:
click(&quot;分享🔗&quot;, &quot;点赞👍&quot;, &quot;在看🌸&quot;)
