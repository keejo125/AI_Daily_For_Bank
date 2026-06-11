---
publish_time: 1781160551
---

# Anthropic宣告「递归自我提升」时代到来，LLM如何实现自我进化？全景综述带你一探究竟

> 原文链接：https://mp.weixin.qq.com/s/N_qd_beuSQ4zMcJAActTaQ
> 公众号：机器之心

近日，Anthropic 发布了一篇引发广泛关注的文章

《When AI builds itself》

。文中披露了极其惊人的内部数据：

截至 2026 年 5 月，Anthropic 超过 80% 的合并代码已由 Claude 编写，工程师的日常代码产出飙升了 8 倍；

更令人瞩目的是，AI 智能体已经可以自主提出假设、执行长达数百小时的强化安全实验。

这说明 AI 已开始展现自主参与下一代模型设计与训练的潜力，而这种自我提升能力（Self-Improvement），正在成为下一代 AI 发展的关键驱动力。

图 1：大语言模型自我提升 (LLM Self-improvement) 的构想：人类只需启动系统，模型便能够持续改进自身能力。

过去，探讨大语言模型（LLMs）的下一步发展时，焦点往往局限于更大的参数规模、海量的数据喂养和极限的算力堆叠。

然而，传统依赖人类监督的训练范式正逐渐面临瓶颈：高质量人工标注极其昂贵，专家反馈难以规模化；更致命的是，随着模型能力的指数级攀升，在高等数学、复杂代码生成和前沿科研推理等任务中，人类的认知边界，反而成了限制模型进化的天花板。与此同时，随着智能体技术的成熟，模型已展现出自主生成数据、调用工具和执行代码的强大自动化能力。

这表明，当前的大语言模型已具备主动参与自身迭代的能力，无需再完全依赖人类的监督。这一趋势标志着一种深刻的范式转移：

大语言模型的发展正从被动接受人类微调与修正转向自主探索与持续进化。

为了解构大语言模型自我提升的底层逻辑，填补系统性研究的空白，来自

纽约州立大学石溪分校 Zesearch NLP Lab 的 Haoyan Yang、Jiawei Zhou 等人

经过将近一年的努力，最近发布了一篇 113 页、涵盖 500 余篇前沿文献的关于大模型自我提升的全景综述：

论文链接: https://arxiv.org/pdf/2603.25681

GitHub Repo: https://github.com/Zesearch/self-improvement-llm

项目网站: https://zesearch.github.io/self-improvement-llm-website/

图 2：LLM 自我提升系统 (LLM Self-improvement system) 的闭环框架：数据获取、数据筛选、模型优化、推理细化与贯穿全程的自动评估。

论文提出了

「LLM 自我提升系统」（LLM Self-Improvement System）

这一概念。

相比已有关于自我演化智能体 (Self-Evovling Agents) 的研究，这篇论文更加从模型自身能力出发，关注模型如何凭借内在能力驱动系统持续演化，并将过去分散在数据、训练、推理和评估中的方法，整合为一个由模型能力驱动的系统级闭环生命周期。

在这个框架中，

自我提升不再是单一算法，而是一套可持续运转的智能系统。

论文围绕一个核心问题展开：

如何在不同阶段利用模型自身能力，推动持续且自主的改进？

论文将自我提升系统概括为四个核心环节：数据获取（Data Acquisition）→ 数据筛选（Data Selection）→ 模型优化（Model Optimization）→ 推理细化（Inference Refinement），并由自动评估（Autonomous Evaluation）作为贯穿全程的控制层。每个环节都以模型的自动化能力为核心，使模型能够主动获取数据、筛选样本、优化自身，并在推理中反思改进。

数据获取（Data Acquisition）

图 3：数据获取 (Data Acquisition) 的三种主要路径：静态筛选、环境交互与合成生成。

自我提升首先需要源源不断的学习数据。论文将数据获取分为三类：静态筛选 （Static Curation）、环境交互（Environment Interaction）和合成生成（Synthetic Generation）。

静态筛选是从已有语料中挖掘可学习样本；环境交互让模型通过与外部环境交互来主动获取数据；合成生成则进一步让模型自己构造新的训练数据。随着这三类方式递进，模型从使用已有数据走向主动探索甚至是自主创造数据。

数据筛选（Data Selection）

图 4：数据筛选（Data Selection）的两类核心机制：模型引导评分与自适应选择。

在数据获取之后，问题转向数据筛选：重点变成当已经获取到足够的数据后，判断哪些数据真正有价值。 低质量、重复或错误的数据可能放大偏差，甚至导致模型坍塌。因此，系统需要筛选出更有效的数据，进入下一步训练。

论文将数据筛选方法分为两类：

第一类是模型引导评分（Model-Guided Scoring），

即利用模型产生的信号对数据进行打分和过滤，例如置信度、困惑度、梯度或损失函数；

第二类是自适应选择（Adaptive Selection），

即把数据筛选变成一个可学习的策略，根据模型能力和反馈动态更新，选择当前最有价值的数据。

模型优化（Model Optimization）

图 5：模型优化 (Model Optimization) 的 GRO 框架，通过生成、奖励与优化循环推动模型能力持续提升。

在数据经过获取和筛选之后，模型优化阶段负责将这些数据真正转化为模型能力。

作者将这一过程总结为

GRO 框架，即生成 — 奖励 — 优化（Generation–Reward–Optimization）：

模型首先基于已有数据生成反映当前能力的输出，再利用奖励信号判断其质量，并通过训练更新自身参数，使模型在循环迭代中持续提升能力。

在这个 GRO 循环中，

生成（Generation）

是起点：模型基于当前能力产生答案、推理链等。论文将生成方式分为三类：

自我探索（Self-Exploratory Generation）

让模型尝试生成多种可能解；

精炼生成（Refined Generation）

让模型在初始输出上反思和修改；

交互式生成（Interactive Generation）

则通过工具、环境或外部反馈不断调整生成过程。

随后是

奖励（Reward） 阶段：

系统对生成结果进行自动评估，判断哪些输出值得学习。奖励信号主要包括三类：启发式奖励（Heuristic Reward） 依赖规则或简单指标，模型奖励（Model-based Reward） 由模型或奖励模型进行打分，可验证奖励（Verifiable Reward） 则通过代码执行、答案匹配或形式化检查等方式提供更可靠的反馈。

最后是

优化（Optimization） 阶段：

模型利用这些反馈更新自身参数。优化方法可以分为三类：监督微调（Supervised Fine-Tuning, SFT） 把高质量输出作为训练数据，强化学习（Reinforcement Learning, RL） 根据奖励信号直接优化模型行为，混合优化（Hybrid Optimization） 则结合 SFT 和 RL：先用高质量数据进行监督学习，再通过奖励信号进一步强化模型表现。

此外，作者还总结了三种常见的模型优化范式，它们可以看作 GRO 框架在具体方法中的不同实例：

迭代拒绝采样（Iterative Rejection Sampling）、自我验证与精炼（Self-Verification and Self-Refinement），以及自我对弈（Self-Play）。

在迭代拒绝采样中，模型先生成多个候选答案，再通过规则或模型打分筛选高质量样本，最后将这些样本用于监督微调。自我验证与精炼则先生成初始答案，再进行自我检查与修改，最后利用改进后的答案进行监督微调，或将修改前后的答案构造成偏好对进行偏好优化，从而提升模型能力。自我对弈通过模型自身或多个模型之间的竞争与协作生成更具挑战性的样本，并借助胜负、偏好或验证信号更新模型。

推理细化（Inference Refinement）

图 6：推理细化 (Inference Refinement) 的四类方法：解码策略、推理式增强、智能体系统增强与测试时训练。

在模型优化之后，自我提升系统还需要考虑另一个问题：模型能力如何在实际推理过程中被进一步提升。

模型优化关注的是通过训练更新参数，而推理细化（Inference Refinement）关注的是：在参数不一定永久改变的情况下，如何让模型在回答问题时更好地搜索、反思、调用工具并修正自身输出。

论文将推理细化归纳为四类方法。

第一类是解码策略（Decoding Strategies），

通过采样、树搜索、logit 调整和效率优化等方式，引导模型生成更可靠的答案。

第二类是推理式增强（Reasoning-based Improvement），

让模型在生成过程中加入执行、反馈、反思和协作推理，从而不断修正中间步骤。

第三类是智能体系统增强（Agentic System-based Improvement），

通过提示词、工具、记忆模块和工作流，把模型放入更完整的任务系统中提升表现。

第四类是测试时训练（Test-Time Training），

即模型在面对具体问题时，利用当前任务产生的反馈进行临时更新，再生成最终答案。

这部分的核心意义在于，它把自我提升扩展到推理过程，使系统不仅依赖训练后的参数更新，也能在具体任务中实现动态改进。

这也是当前「自我演化智能体」研究最关注的方向之一：智能体如何在运行时通过规划、反思、工具调用和环境交互，不断调整自身行为并提升任务完成能力。

自动评估（Autonomous Evaluation）

图 7：自动评估（Autonomous Evaluation）通过动态基准和交互环境评估，持续监控自我提升系统的真实进步。

除了上述四个环节，自我提升系统还需要一个贯穿全程的控制层：自动评估（Autonomous Evaluation）。如果缺少评估，系统就无法判断自身改进是否真实有效。作者认为，评估过程不应只依赖人工检查或固定测试集，而应能够随着模型迭代自动更新并提供反馈。

为此，论文强调两类方法：

动态基准（Dynamic Benchmarking）

可以持续生成或更新测试任务，避免静态基准失效；

交互环境评估（Interactive Environment Evaluation）

则让模型在真实或模拟环境中完成任务，并根据环境反馈自动判断表现。

通过这种方式，评估不再是闭环末端的一次性打分，而是持续指导系统改进的反馈机制。

风险、应用与未来（Application, Challenge and Future Outlook）

图 8：自我提升系统的六大挑战：数据自噬、反馈信号缺陷、优化驱动失败、无效自我精炼、评估瓶颈和监督瓶颈。

自我提升系统具有巨大潜力，但也面临一系列挑战。作者一共总结了六个关键问题：模型反复学习自身生成的数据，可能带来

数据自噬（Data Autophagy）；

错误或有偏的反馈会造成

反馈信号缺陷（Flawed Feedback Signals）；

训练和优化过程可能出现

优化驱动失败（Optimization-Driven Failures）；

推理阶段的自我精炼有时只是表面修改，形成

无效自我精炼（Ineffective Self-Refinement）；

此外，

评估瓶颈（Evaluation Bottlenecks）和监督瓶颈（Supervision Bottlenecks）

也会限制系统的可靠发展。

图 9：自我提升系统的六大应用场景：代码、数学、医疗、金融、算法发现和科学研究。

与此同时，作者总结了自我提升系统的六大应用场景，包括

代码（Code）、数学（Math）、医疗（Medicine）、金融（Finance）、算法发现（Algorithm）和科学研究（Science）。

这些领域中已经出现了不少自我提升的应用案例，展现着这一方向的实际价值。

面向未来，作者提出了自我提升研究的四大方向：

第一，从模型级优化走向端到端自我提升系统（End-to-End Self-Improving Systems）；

第二，发展面向应用的专用自我提升模型（Application-Centric Self-Improved Models）；

第三，建立统一基准与自主评估（Unified Benchmarks and Autonomous Evaluation），

衡量模型是否真的在持续进步；

第四，在自动化与人类监督之间取得平衡（Balancing Automation and Human Oversight），

确保系统既能自主进化，又保持安全和可控。

总体来看，这篇论文把自我提升从一组分散的技术方法，提升为一个以模型为主体的系统级闭环框架，通过数据、训练、推理和评估等环节的协同，使大模型从一次性训练的产物，逐步走向能够持续成长的闭环智能系统。

当人类不再总能继续教模型时，谁来推动模型进步？答案或许是模型自己。

作者介绍

第一作者： Haoyan Yang，

纽约州立大学石溪分校计算机科学博士生。

个人主页：

https://joyyang158.github.io/haoyan-yang/

其他作者：

Mario Xerri、Solha Park、Huajian Zhang、Yiyang Feng、Sai Akhil Kogilathota，

来自纽约州立大学石溪分校计算机科学系以及数据科学项目

通讯作者： Jiawei Zhou，

纽约州立大学石溪分校计算机科学系、数据科学项目、应用数学与统计系助理教授。

个人主页：https://joezhouai.com

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com