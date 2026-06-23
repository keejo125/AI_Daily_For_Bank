---
publish_time: 1780560843
---

# 「这可能是人类写的最后一篇论文」Stanford、Michigan、CMU 等 37 位学者联手：把论文从 PDF 改写成 AI 能直接执行的研究包

> 原文链接：https://mp.weixin.qq.com/s/3Nt_S1xweNOs4YlOzf1LRA
> 公众号：机器之心

作者：Jiachen Liu、Jiaxin Pei、Jintao Huang、Chenglei Si 等 37 人

重新思考为人类认知带宽设计的科研生态：

现在应该以AI科学家为中心。

我们今天以 PDF 写论文的方式，已经持续了三百多年。然而论文其实是把一段混乱反复、充满试错的真实研究，讲成一个干净利落、足以服人的完美故事。

如果未来大多数 CS 论文是 AI 写的、又是 AI 读的，我们还需要 PDF 吗？

最近，由 前 Meta 超级人工智能实验室 研究科学家 Jiachen Liu 牵头，联合 MIT、CMU、Michigan、Stanford 等机构、共计 37 位作者 的一篇新论文给出了一个相当激进的回答：不需要。

这篇名为 The Last Human-Written Paper: Agent-Native Research Artifacts（arXiv:2604.24658）的论文里，作者们抛出了一个让整个学术圈都得停下来想一想的问题 —— 当作者和读者都不再是人，沿用了三百年的论文范式还成立吗？

作者团队的署名相当「重」，里面包括了 MIT 的 Alex Pentland、CMU 的 Beidi Chen、Michigan 的 Mosharaf Chowdhury，以及 Stanford 在 AI co-scientist 方向上颇活跃的 Chenglei Si 等一众熟面孔。论文一上 arXiv，就在 X 和小红书上引起了不小的争论。

论文标题：

The Last Human-Written Paper: Agent-Native Research Artifacts

论文链接：https://arxiv.org/abs/2604.24658

Github 链接: github.com/AmberLJC/Agent-Native-Research-Artifact

让我们看看他们具体是怎么说的。

论文格式的两笔「隐形税」

把科研过程塞进一篇 PDF 论文里，本身就要交两笔「隐形税」。这两笔税，人类同行在复现别人的工作时其实一直在交，只是到了带宽近乎无限的 agent 面前，它们才彻底无处可藏。

叙

事

税 (Storytelling Tax)。

真实的研究是一棵分叉的树，会有几十次尝试、撞墙、推倒重来，但 PDF 只汇报最后跑通的那条主干，把失败实验、被驳回的假设、临时拐弯的决定全部丢弃。这种压缩对人类读者是一种必要的服务，毕竟没人有时间读完一整棵搜索树；可对带宽近乎无限的 agent 来说，它就是纯粹的信息损失。那些 pivot、dead end 和负面结果没有进入任何文档，对下一个想做类似研究的人 (或 AI 智能体) 来说，这部分知识等于从未存在过。

工

程税 (Engineering Tax)。

论文里方法描述的精度，只够让审稿人相信；能不能让别人跑起来，从来不是论文的责任。超参数缺失、warmup schedule 只存在于某个作者的脑子里、数值稳定性的小 trick 在哪份文档里都找不到。这就是 "足以说服" 与 "足以执行" 之间的鸿沟。

作者用 PaperBench 上 8921 条专家标注的复现要求，做了一次量化分析。结果触目惊心：PDF 中完整说明的只占 45.4%, 缺失超参数的占 26.2%, 描述含糊的占 21.9%, 仅靠交叉引用的占 13.4%, 缺少代码或 baseline 细节的占 21.7%。换句话说，AI 智能体复现一篇论文所需的信息，有一半以上根本不在 PDF 里。

这些信息当然存在过，只是停留在某本实验记录、某个 Slack 对话、原作者的肌肉记忆里，始终没有沉淀成一种可被检索、可被继承的形式。于是每一次复现尝试，都得把同样的代价重新支付一遍。

解决方案：四层互锁的「研究包」

那研究的载体究竟该长什么样，才能把这些被压缩掉的颗粒度原样留住？作者的答案是 ARA (Agent-Native Research Artifact): 把整段研究以机器可执行的形式原样保留下来，跳过叙事压缩这一步。一个 ARA 由四层组成。

认知层

，描述这个研究在干什么：可证伪的论断、形式化的概念、声明式的实验设计。

物理层

，描述怎么把它跑起来：一份让 agent 即开即用的代码加环境清单。

探索图

，描述研究是怎么走到这一步的：把被叙事税抹掉的死路、pivot 和踩过的坑，用一张 DAG 完整保留。

证据层

，回答 "凭什么相信你": 每一个论断都直接挂在原始实验输出上，不再隔着一层人工写就的 "我们观察到 X"。

四层互相印证，把论文从一个 compiled view 变回了一份持续演化、有结构的研究知识。

三个让生态跑起来的机制

光有结构还不够。作者配套设计了三个机制，让 ARA 不需要研究者额外加班就能产出。

Live Research Manager。

这是整个体系的关键一环。研究者不必事后回忆、手工打包；这个组件在 AI 与人协同做研究的过程中静默捕获轨迹：哪一步是 decision、哪一步是 dead_end、哪一步是 heuristic、哪次实验产生了多少 loss。整个 artifact 在后台自己长出来。

ARA Compiler。

几百万篇存量 PDF 不可能一夜废弃。作者为此做了一个把 "legacy PDF + 代码仓库" 自动翻译成 ARA 的 compiler, 让历史文献也能被 agent 直接消费。

ARA-native Review System。

既然 ARA 本身是结构化的，那么大量 "这个超参数有没有报告"" 这个 claim 有没有 evidence 支撑 " 之类的客观检查就可以完全自动化。人类审稿人则能把精力留给只有人才能判断的事：重要性、新颖性、品味。

实验结果

作者想验证的问题很具体：对一个接手任务的 AI agent 来说，一份 ARA 是不是真的能比今天最常见的科研载体，也就是 "论文 PDF + 配套 GitHub 仓库", 更好地支撑它去理解、复现、并在此基础上扩展一项研究？他们在 PaperBench 和 RE-Bench 两个基准上，把这三件事拆开来量化对比。

理解 (Understanding):+21.3pp。

在跨越两个 benchmark、共 450 道问题的设定下，读 ARA 的 agent 回答准确率达到 93.7%, 而读 PDF + GitHub 的对照组只有 72.4%。所有子类别上，ARA 都占优。

复现 (Reproduction):+7.0pp。

在 PaperBench 的 15 篇论文、150 个子任务上，复现成功率从 PDF + 仓库的 57.4% 提升到 ARA 的 64.4%。一个值得注意的发现是：任务越难，ARA 的优势越大。简单任务上两者差距很小，但在难任务上，ARA 的领先非常明显。

扩展 (Extension):3 / 5 任务获胜。

在 RE-Bench 的 5 个开放式扩展任务上，ARA 在 3 个任务上拿到了最佳分数，其余 2 个基本持平；并且在全部 5 个任务上，它都能让 agent 更早做出第一步有用的动作。

不过扩展维度上还有一个反向发现值得单独拎出来：当 agent 本身已经足够强时，被保留下来的 dead_end 反而会把它框死在原作者走过的路径里，让它不容易跳出 prior-run 的框架去做真正大胆的探索。这是 ARA 设计上的一个深层张力：保留多少是 "站在巨人肩膀上", 保留多少是 "替巨人套上枷锁"。目前的答案是：对中等能力的 agent, 保留是巨大助力；对最强的 agent, 则需要一套更精细的 "忘记机制"。

三个维度合在一起，得到的是同一个结论：在 AI agent 已经是核心读者的前提下，把论文和代码各自打包好，远不如把它们按 ARA 的结构合并后交出去。

感兴趣的读者可以阅读论文原文，了解更多研究细节。

关于一作

刘嘉晨 (Amber Liu), 本文一作，密歇根大学 CS 博士 (师从 Mosharaf Chowdhury), 前 Meta 超级智能实验室研究科学家，本科毕业于上海交通大学。研究方向为 AI for Science 与机器学习系统 (LLM 预训练 & 后训练系统), 曾在 Apple、MIT CSAIL 从事研究工作。2023 年入选 MLSys Rising Stars。

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com