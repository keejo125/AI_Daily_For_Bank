---
publish_time: 1783156569
---

# Arm CEO：CPU需求已「爆表」！

> 原文链接：https://mp.weixin.qq.com/s/QS3xSOwlmq2sGgPCqKmTIg
> 公众号：机器之心

机器之心编辑部

过去两年，AI 基础设施的主角可谓一直是 GPU，尤其是英伟达（NVIDIA）的 GPU 。从大模型训练，到推理集群，再到 HBM、先进封装、液冷机柜，行业讨论算力，默认就是在讨论 GPU，讨论谁能拿到更多的卡。

似乎，相较 GPU，AI 时代的

CPU 只是个干杂活的「配角」。

但现在情况好像不同了。CPU 或将从长期处于 AI 叙事边缘走向牌桌更为中心的位置。

近日，科技记者 Tae Kim 采访了 Arm CEO Rene Haas（雷内・哈斯），后者直言，

当前市场对高级 AI CPU 的需求正处于「爆表」（Off the Charts）状态……

文章链接：https://taekim.substack.com/p/an-interview-with-arm-ceo-rene-haas

Arm CEO Rene Haas

资料显示，自从今年 3 月下旬，Arm 在旧金山的一场产品活动上发布全新的 AGI CPU 以来，公司股价已经上涨超过一倍。当时，Rene Haas 就曾预测，

随着 Agent 时代的到来，每 1 吉瓦数据中心容量将需要 1.2 亿个 CPU 核心，而去年这一数字是 3000 万个。

过去，外界对 Arm 的认知是更像是一家「卖架构」的公司。苹果、NVIDIA、亚马逊、微软、谷歌等客户使用 Arm 架构设计芯片，Arm 通过授权费和版税赚钱。但随着 AGI CPU 的出现，让 Arm 开始直接站到 AI 数据中心 CPU 市场前台。

一个直观的佐证是，今年 2 月英特尔因转型滞后而财务承压，而同期 Arm 公布的财报显示其季度营收大涨 26%，第四季度指引远超预期……

接下来，我们一起来看看 Rene Haas 在采访中谈及的重点内容。

AI 时代的 CPU 需求「爆表」

Rene Haas 坦言，

大约一年半前，当人们开始构建基于 Arm 的 SoC 时，他们就意识到这一趋势：AI 时代的 CPU 需求将「爆表」。

「当时我们觉得 128 核可能已经是天花板了。但我们看到客户开始问：『能不能做到 160 核以上？能不能做到 192 核？』于是我们开始想，是什么在推动这么高的核心数需求？」

经过一番研究后，

Arm 发现，是 Agent。

在这些 Agent 工作流中，核心越多越好，因为可以直接启动一个 Agent 去运行一个虚拟任务。

紧接着，Arm 又去观察其他相关趋势，然后意识到：

CPU 需求真的会因为 Agent 的编排、调度和管理而「起飞」。

因为这些负载无法简单交给 GPU 完成，CPU 才是支撑 Agent 系统持续运行的关键底座。

「这些都是纯粹的 CPU 型工作。」

从「卖图纸」向「卖更完整的计算平台」延伸

随着趋势的变化，Arm 的商业模型也因此发生变化。

Tae Kim 认为，从本质上来说，Arm 既在提供芯片技术，也在 CPU 领域与合作伙伴竞争，比如 Nvidia、亚马逊的 Graviton 和微软。那这样的话，Arm 将如何进入市场？未来会不会出现 Arm CPU 机架和 Vera Rubin 机架并排放在一起的情况？

Rene Haas 坦言

「完全可能。」

Arm 的看法是，在 x86 世界里，用户有两个选择，不过世界可能会很欢迎第三种、第四种选择，因为归根结底，市场需要很多不同的 CPU 机架配置。「我们的 AGI CPU 也是如此。」

资料显示，Arm 把 AGI CPU 定位成 Agentic AI 数据中心的「编排层」，Arm AGI CPU 最高 136 个 Neoverse V3 核心，采用 TSMC 3nm 工艺，TDP 300W，支持 DDR5-8800、96 条 PCIe Gen6、CXL 3.0，并宣称相比 x86 平台可实现超过 2 倍的 rack-level performance。

在 Rene Haas 看来，未来，Arm 100% 有可能和 Graviton 出现在同一个数据中心机房里，也 100% 有可能会和 Vera Rubin 出现在同一个数据中心机房。

Rene Haas 举了 Vera Rubin 为例来阐述原因。

NVIDIA 的 Vera CPU 机架是在一个液冷机架中集成 256 颗 Vera CPU。一个数据中心中，可能这一区域部分全部采用液冷，而在另一个区域部分使用的可能全是风冷机架，那么那里有存储，有网络，也就可能正好放着 Arm AGI CPU，它们都是 OCP 标准机架。

「所以从采购角度看，就像我购买存储、购买网络一样，我只是购买计算资源。」

因此，Rene Haas 强调，Arm 构建 AGI CPU，并不意味着会放弃 IP 业务。亚马逊会继续做 Graviton 吗？100% 会。那他们会买 Arm AGI CPU 吗？很有可能，但如果他们不买，也没关系。

「我们有很多客户没有芯片设计能力，他们会购买这颗芯片。也有一些客户会自己设计芯片，可能不会购买它。还有一些客户两者都会做，他们很可能两种都买。这是一个巨大的市场扩展机会。」

写在最后

总的来说，Rene Haas 的这次采访透露了当前 AI 火热趋势下的另一个切面：

AI 的终局不仅是 GPU 的比拼，更是能效比和 CPU 调度能力的博弈。

不过值得注意的是，虽然 Rene Haas 直白给出「爆论」：CPU 需求已「爆表」。但其实，关于 CPU 回潮，Arm 并不是唯一一家把 CPU 重新放回 AI 中心的公司，各大巨头早已开始布局。

今年 3 月，NVIDIA 于在 GTC 2026 大会上正式发布了 Vera CPU，这是其首款自研 Arm 架构处理器，称其为「the CPU for Agents」，面向 Agentic AI、强化学习、数据处理等工作负载，能够服务代码执行、工具使用、沙盒、数据流水线和编排等模型之外的 CPU 工作。

Intel 也在同一方向发力，在 2026 年 Computex 上发布基于 Intel 18A 制程的至强 6+（Xeon 6+）处理器，明确将 CPU 重新定位为 Agentic AI 系统的核心控制单元，以应对推理负载取代训练负载带来的架构变革 。

而 AMD 的表述也很直接，把 Agentic AI 视为端到端工作流，并强调 CPU 基础设施应以机架级能力来规划，而不是孤立地比较单个组件。

这无疑是在说明，一个新的行业共识正在形成：

AI 基础设施不能再只围绕 GPU 来理解。

模型之外的系统执行、数据调度、工具调用、并发编排，会成为下一阶段 AI 工厂效率的关键变量。

当 AI 还是聊天机器人，CPU 很容易被看作 GPU 旁边的配套组件；当 AI 变成 Agent，CPU 就成了调度、执行和编排的核心环节。

或许，AI 基础设施的下一轮争夺，

已经从「谁有更多 GPU」扩展到「谁能支撑更多 Agent」。

参考链接：

https://x.com/firstadopter/status/2072827611579851067

https://taekim.substack.com/p/an-interview-with-arm-ceo-rene-haas

https://newsroom.intel.com/data-center/intel-puts-agentic-ai-xeon-6-networking-ai-systems

https://nvidianews.nvidia.com/news/nvidia-unveils-vera-the-cpu-for-agents

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com