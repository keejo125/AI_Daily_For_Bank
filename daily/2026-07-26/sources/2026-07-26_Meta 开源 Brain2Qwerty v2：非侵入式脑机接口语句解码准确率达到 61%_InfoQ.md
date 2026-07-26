---
publish_time: 1785032851
---

# Meta 开源 Brain2Qwerty v2：非侵入式脑机接口语句解码准确率达到 61%

> 原文链接：https://mp.weixin.qq.com/s/5NpTmetb8n1K2aWRD9Q7gQ
> 公众号：InfoQ

作者 ｜ Anthony Alford

译者 ｜ 马可薇

Meta 近日开源了 Brain2Qwerty v2。这是一套非侵入式脑机接口（BCI）系统，可利用脑电图（EEG）或脑磁图（MEG）采集的脑信号，将人脑中的想法解码为完整语句。在评测中，Brain2Qwerty v2 的平均单词识别准确率达到 61%，相比之下，其他非侵入式方案仅为 8%。

Brain2Qwerty 采用 三阶段深度学习模型，根据脑信号预测输入字符。在数据采集过程中，研究人员首先向参与者展示一句话，要求其记住内容，然后再通过键盘输入。Meta 发现，MEG 信号的表现明显优于 EEG：平均字符错误率（CER）分别为 29% 和 65%。与基线 模型 EEGNet 相比，Brain2Qwerty 的字符错误率降低了约 2.5 倍。为了推动开放脑科学研究，Meta 已将模型代码和训练数据全部公开。Meta 表示：

我们相信，这项研究有望为数百万因脑部损伤而失去沟通能力的人带来真正的帮助。我们还发现，随着数据规模不断扩大，解码准确率会呈对数线性增长。这意味着，仅通过持续扩大数据规模，就有望进一步缩小非侵入式方案与植入式方案之间的性能差距。

我们正通过 Digital Brain Project 设立的 500 万美元基金，与研究社区密切合作，推动开放数据集的发展。我们希望，这项开放开展的研究能够加速神经科学的发展，更快推动神经系统疾病的发现、诊断和治疗，而不是让相关研究局限于各自封闭的体系之中。

Meta 指出，以往非侵入式脑机接口的发展主要受限于脑信号中的高噪声和复杂性。相比之下，皮层脑电图（ECoG）等侵入式方案能够获得更加可靠的信号，但由于需要手术植入，因此“难以大规模推广”。Meta 曾于 2025 年发布 Brain2Qwerty v1，而 新版模型 的单词错误率（WER）相比上一代几乎降低了一半，进一步缩小了与侵入式脑机接口之间的性能差距。

Brain2Qwerty v2 由三个核心模块组成：Encoder 负责接收脑信号并预测字符；Aligner 将字符组合成单词；最后由 LLM 根据对齐后的结果生成最终输出。这一架构还带来了一个意外收获：即使用户在输入时拼写错误，系统也能够自动纠正这些类似“打字错误”的问题。

在 X 平台讨论此次发布时，io.net 联合创始人 Tory Green 将 Brain2Qwerty v2 与上一代 进行了比较：

看起来，从 v1 到 v2 的性能提升几乎完全源自训练数据的十倍涨幅，而非模型架构上的突破。这种结果其实很振奋人心，因为这就意味着，目前真正的瓶颈是能够采集到、并完成标注的 MEG 数据，而不是这个问题本身已经接近理论极限。数据量这类限制往往会比人们预想的更快得到解决。

Brain2Qwerty v2 的代码 已发布在 GitHub，训练数据 也可从 Hugging Face 下载。Brain2Qwerty 属于 Meta Digital Brain 项目的一部分，该项目旨在以开源方式推进脑活动建模，服务于科学研究和医学应用。Digital Brain 项目的其他开源成果还包括 NeuralSet——一个用于处理 MEG、EEG 等神经信号的 Python 工具包，以及 NeuralBench——一个用于评测脑活动 AI 模型的统一基准框架。

原文链接：

Meta&#x27;s Noninvasive Brain–Computer Interface Brain2Qwerty Achieves 61% Accuracy（

https://www.infoq.com/news/2026/07/meta-brain-interface/

）

声明：本文由 InfoQ 翻译，未经许可禁止转载。

点击底部

阅读原文

访问 InfoQ 官网，获取更多精彩内容！

今日好文推荐

半价“背刺”Fable 5，Opus 5登场！A社高管：Kimi K3更便宜，但复杂项目表现待观察

Cursor 用一群Agent重造SQLite：仅凭 835 页手册，无源码、无测试、不联网

“围攻” Ralph Loop 之父？一场关于 Loops 的激辩：代码照样垃圾，只会失败得更加难看

1800亿美金逼出来的杀手锏：谷歌Frozen v2把Gemini烧进硬件，每瓦Token翻10倍，股价先涨3.3%