---
publish_time: 1787795940
link: https://mp.weixin.qq.com/s/DcWsDYykew5jG7WHjd1K8g
source: 量子位
status: confirmed
category: 国内
is_model_related: true
digest: |
  阿里在 Qwen4 新架构中引入 DeepSeek 提出的 Engram 稀疏记忆机制。新架构以 125B 参数 MoE、仅 6B 激活参数预览，并宣称单张 RTX 4090 即可运行、无需量化。Engram 通过结构化外部记忆缓解长上下文与知识遗忘问题，使模型在有限激活算力下保持长程一致性。该权重以 Qwen3.8-Flash-Next 名义开源，被视为 Qwen4 架构的早期预览。
title: Qwen 4用上DeepSeek的Engram！125B MoE一张4090能跑不用量化
---

# Qwen 4用上DeepSeek的Engram！125B MoE一张4090能跑不用量化

来源：量子位
原文链接：https://mp.weixin.qq.com/s/DcWsDYykew5jG7WHjd1K8g

梦晨 发自 凹非寺
量子位 | 公众号 QbitAI
Qwen4还没出，架构先开源了。
阿里发布Qwen3.8-Flash-Next的全部权重， 同时也是
Qwen4新架构的早期预览版
。
这个新架构它确实够新。
除了常规的125B参数MoE模型配6B激活参数，
关键是还附加了51B的N-gram Embedding参数
。
这是个啥呢？
发布公告明确写着，
受DeepSeek的Engram启发，进一步扩展了这种设计。
它的主要优势在于，它可以添加大量参数，而每个token几乎不需要额外的计算。
Qwen3.8-Flash-Next 大幅降低了训练和推理成本，训练时间仅为原来的九分之一，却在代码和办公任务方面表现出色。
Qwen3.8-Flash-Next的跑分可以总结在
小模型里超过DeepSeek V4 Flash正式版，向上多项测试可以挑战Claude-Opus-4.6（Max）
。
模型权重公开后，也确实有人在
24GB显存的4090+128G内存上成功部署
，而且不用量化。
虽然之前发布的密集模型Qwen3.8-27B在消费硬件上体验更好。
但这一次，Qwen3.8-Flash-Next证明了在消费级硬件上跑满血版MOE模型也是完全可行的。
DeepSeek Engram更复杂，Qwen更精简
传统Transformer只有一个词嵌入层，每个token对应一个向量。
而Qwen的N-gram Embedding和DeepSeek的Engram都是利用当前token及其前面若干token组成的局部上下文作为key，通过确定性的哈希函数在一张巨大的嵌入表中查到对应的向量，时间复杂度为O(1)。
DeepSeek的Engram论文首次将这一思路形式化为“条件记忆”（conditional memory），并将其定位为与MoE的“条件计算”（conditional computation）平行的第二种稀疏方式。
Engram论文通过Sparsity Allocation实验发现了一条U形缩放定律：在总参数和FLOPs固定的前提下，把大约20%–25%的稀疏参数预算从MoE专家重新分配给Engram嵌入表，能获得比纯MoE更低的验证损失。这一分配比例在5.7B和9.9B两个规模上保持稳定，最优点均落在75%–80%分配给MoE的区间。
Qwen3.8-Flash-Next在技术报告中直接引用了Engram论文和Gemma 3n的Per-Layer Embedding作为灵感来源，并在最终模型中配置了51B的N-gram嵌入参数，附加在125B主模型之上。
Engram的设计有四个关键组件。
第一是Tokenizer Compression，通过NFKC归一化和小写映射把128k词表压缩23%，消除”Apple”和”apple”这类语义等价但ID不同的冗余。
第二是Multi-Head Hashing，对每个N-gram阶数使用K个独立哈希头映射到素数大小的嵌入表中以缓解冲突，最终把所有检索到的向量拼接成一个记忆向量。
第三是Context-aware Gating，用当前层的隐藏状态作为Query、检索到的记忆作为Key和Value，通过RMSNorm归一化后的缩放点积计算出一个标量门控值，决定是否采纳这条记忆——如果记忆与当前上下文矛盾，门控趋近于零自动抑制噪声。
第四是一个核大小为4、膨胀率等于最大N-gram阶数的深度可分离因果卷积，用于扩展感受野并增加非线性。此外，Engram还专门设计了与多分支架构的集成方案：多个分支共享一张嵌入表和一个Value投影矩阵，但各自拥有独立的Key投影以实现分支级别的差异化门控。
Qwen3.8-Flash-Next的N-gram Embedding在公开博客中没有披露同等细节深度的设计说明，但从已公布信息可以看出几点差异。
Qwen最终只使用了一个N-gram Embedding层，而Engram在27B模型中部署于第2层和第15层两个位置。
DeepSeek的Engram论文在严格的等参数、等FLOPs条件下完成了对照实验。在26.7B总参数规模上，Engram-27B相比纯MoE-27B基线在知识任务上提升了MMLU +3.0、CMMLU +4.0，在推理任务上提升了BBH +5.0、ARC-Challenge +3.7，在代码数学上提升了HumanEval +3.0、MATH +2.4。
Engram论文还通过LogitLens和CKA分析揭示了增益来源：Engram让模型的第5层表示在功能上等价于纯MoE基线的第12层，相当于在不增加实际层数的情况下增加了网络的有效深度。
Qwen的51B嵌入参数远超Engram论文中验证过的最大规模（Engram-40B的嵌入参数为18.5B），这意味着Qwen在实践中把Engram论文中观察到的“嵌入槽数量与验证损失呈对数线性关系”这一结论推到了更大的尺度。
不过由于Qwen3.8-Flash-Next同时引入了QSA稀疏注意力、Gated Residual和Muon优化器等多项改动，N-gram Embedding的单独贡献无法从最终结果中精确隔离。
四项架构升级，从注意力到优化器全换了
除了嵌入层外，Qwen3.8-Flash-Next还在注意力、残差、和优化三个维度上做了系统性升级。
注意力层面，模型延续了Qwen3-Next以来“GDN+注意力”的混合设计。
48层网络中，每4层有3层使用门控DeltaNet将历史信息压缩进固定大小的状态，剩余1层负责全局精确检索。
但这次全局注意力从之前的Gated Attention升级为全新的Qwen Sparse Attention（QSA）。
QSA的做法是先用一个轻量索引器把序列聚合成”微块”，在块级别估计上下文重要性，再只对最相关的区域做注意力计算。这不仅降低了注意力本身的开销，连索引过程的计算量也一并压了下去。
在100万token的长上下文场景下，QSA的注意力内核在预填充和解码阶段分别实现了7.6倍和4.9倍的加速。在90%前缀缓存命中率的在线服务场景中，Qwen3.8-Flash-Next在100万token上下文长度下的预填充吞吐量达到了Qwen3.7-Plus的8.6倍。
残差连接方面，引入了Gated Residual（GR），把传统Transformer的单条残差流扩展为4条并行分支，通过动态门控机制控制每一层对各分支的读写。这样做的效果是加强了跨层信息流动和训练稳定性，同时残差状态还支持FP8存储以降低显存带宽开销。
优化器方面，用Muon替代AdamW作为主优化器，并围绕正交化精度、Muon与AdamW的分工以及融合参数的拆分做了改进。
Qwen还公布了一个新发现：大规模训练中常见的Batch Size Warmup在新架构上不再必要，直接用目标Batch Size开训的效果一样，反而省掉了18.8%的优化器步数。
百万token上下文，每百万输入token定价0.16美元
Qwen3.8-Flash-Next原生支持262144 token上下文，通过YaRN可扩展至100万token。模型权重已在HuggingFace和ModelScope开放下载。
在QwenCloud上，这个模型以”qwen3.8-flash”提供API服务，也是加入了100万上下文默认支持和官方内置工具的版本，输入定价为每百万token 0.16美元，输出为每百万token 0.47美元。
作为参照，同门旗舰Qwen3.8-Max的输入和输出定价分别是2.00和6.00美元，Flash-Next的成本约为旗舰的十二分之一。
部署生态方面，通义千问这次直接兼容了Anthropic和OpenAI两套API协议，可以直接插入Claude Code、OpenAI Codex等主流编程助手使用。
团队还同步推出了Qoder CLI和Qwen Code两个自研编程工具，以及与OpenClaw的集成。
阿里AI办公平台QwenWork也已将Qwen3.8-Flash-Next集成为其”Standard”模式的底层模型。
至于未来的Qwen4本体，只能说，还会更强。
参考链接：
[1]https://qwen.ai/blog?id=qwen3.8-flash-next
[2]https://x.com/analogalok/status/2092697021790708148
一键三连
「点赞」「转发」「小心心」
欢迎在评论区留下你的想法！
—
完
—
🌟 点亮星标 🌟
科技前沿进展每日见
