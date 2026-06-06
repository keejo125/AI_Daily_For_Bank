---
publish_time: 1780561565
---

# 超越TurboQuant：Together AI把2-bit KV Cache推向真实服务

> 原文链接：https://mp.weixin.qq.com/s/gDnXSTdlEMKgvEXhs6VCGA
> 公众号：量子位

允中 整理自

凹非寺

量子位 | 公众号 QbitAI

长上下文模型越来越能“记”，但真正让它们跑到线上时，最先顶不住的往往不是算力，而是

KV Cache

。

每生成一个新token，模型都要回读越来越长的历史Key和Value。上下文越长、batch越大，KV Cache对显存容量和显存带宽的消耗就越明显。

这也是为什么KV Cache量化成了长上下文serving的核心问题：压得不够，显存撑不住；压得太狠，推理质量又容易崩。

Together AI、悉尼大学和UIUC的研究团队，为此提出了一种面向真实serving的2-bit KV Cache量化方案——

OSCAR

。

模型不再只是把K/V张量压小，而是围绕attention真正会使用的方向来做旋转、裁剪和分组，让量化误差尽量避开模型最敏感的部分。

在约2.28 effective bits per KV element的预算下，OSCAR仍能

接近BF16

；在Qwen3-4B-Thinking上，相比全层3-bit K/V TurboQuant，最高

提升40.1分

。

这意味着，KV Cache压缩不再只是“少占显存”，而是开始进入真实长上下文服务系统的设计核心。

不是更会“压缩向量”，而是开始保护attention

过去很多KV Cache量化方法，关注的是如何更好地还原K/V向量本身。

但在低比特场景里，这个目标并不总是等价于更好的生成质量。

原因很直接：

attention真正消费的是Key和Query之间的匹配关系，以及Value被注意力权重加权后的输出。

K/V 重建误差看起来不大，并不代表attention logits、attention block output和后续hidden state不会被放大偏移。

2-bit INT只有4个离散等级，而KV activation中又常常存在少数幅值很大的outlier channel。

如果量化尺度被这些极端通道牵着走，大部分正常值会被挤到很窄的区间里，attention分布也会跟着偏。

普通Hadamard旋转可以把outlier打散，却不知道哪些方向对attention更关键。

OSCAR的核心变化就在这里：

它不再只问“怎么把K/V向量还原得更像”，而是问“怎么让attention读到的关键信息尽量不变”。

△

只用K/V重建误差，容易低估真实误差传播

OSCAR把旋转对准attention

OSCAR的方法可以概括成一句话：

用attention-aware covariance来决定K/V应该怎么旋转。

具体到

Key

，量化误差会通过QKᵀ进入attention logits，因此OSCAR使用query covariance，也就是QᵀQ，来决定Key的旋转方向。

具体到

Value

，误差会先被attention score加权，再进入attention 输出，因此OSCAR使用score-weighted value covariance，也就是VᵀSᵀSV，来决定Value的旋转方向。

离线校准阶段，系统用少量样本估计每一层、每一个head的这些covariance，并生成固定的旋转矩阵和clipping阈值。

推理阶段，这些参数直接复用，不需要任务级微调，也不需要在线学习。

最终旋转可以写成：

R=U·Hadamard·bit-reversal

其中，U负责对齐attention相关方向，Hadamard用来摊平outlier能量，bit-reversal让INT2分组更均衡，避免某个group被少数异常通道主导。

也就是说，OSCAR不是简单“加一个旋转”，而是把旋转、裁剪和分组都放进attention质量这个目标里。

△

从离线校准到在线推理的pipeline

OSCAR的另一个关键点，是

它没有停留在离线量化评测里

。

它已经接入SGLang的服务路径，在运行时维护一个三段式token pool：

BF16 sink（64 tokens）｜INT2 history｜BF16 recent（256 tokens）

开头的attention sink token和最近窗口token继续用BF16保存，用来保护attention sink与最近上下文。

中间最长、占比最大的历史KV，则保存为旋转和裁剪后的INT2。

新token会先写入recent window。随着解码推进，最老的recent token会被融合Triton kernel处理，完成rotate、clip、quantize和pack，然后降级进入INT2 history。

存储上，每4个2-bit数值被打包进1个byte。

decode阶段，OSCAR在GPU上分别处理BF16段和INT2段：

INT2 kernel负责unpack、scale/zero point反量化以及浮点累加；BF16 kernel处理 sink/recent；最后再通过online softmax merge合并两部分结果。

由于它兼容paged KV、radix prefix cache和SGLang的fused kernel pipeline，OSCAR面向的是可部署的长上下文workload，

而不是只展示漂亮的离线准确率

。

小模型也能守住高难推理

论文在Qwen3-4B-Thinking、Qwen3-8B、Qwen3-32B和GLM-4.7-FP8上做了评估。

任务覆盖GPQA、HumanEval、LiveCodeBench v6、AIME25和MATH500，最长生成长度达到32K，并且每个配置运行5次取平均。

结果显示，在约2.28BPE下，OSCAR的精度仍然

非常接近BF16

。

以

Qwen3-4B-Thinking

为例：

TurboQuant mean为31.74，QuaRot-INT2只有1.40，Naive INT2为0.00；OSCAR达到71.86，距离BF16只差3.78，并且比TurboQuant高40.1分。

在Qwen3-8B上，OSCAR mean为69.42，BF16为70.84，TurboQuant为56.88。

到了Qwen3-32B和GLM-4.7-FP8，OSCAR与BF16基本持平。

这组结果背后的含义，比单个榜单数字更重要：

当任务真正依赖长链推理、代码生成和数学推导时，低比特KV Cache的核心瓶颈不是“能不能压”，而是

压缩误差会不会破坏attention的关键路径

。

OSCAR的优势，正是让接近2-bit的预算仍然守住推理质量。

论文还专门看了

AIME25

这个高难数学推理任务，并加入KIVI-KV2、Kitty和OSCAR的对比。由于KIVI和Kitty没有可直接用于long context run的framework支持，论文选取了它们唯一在32K下汇报的AIME25结果。

在Qwen3-8B上，OSCAR以2.38 BPE达到66.67，几乎追平BF16的66.00，并明显高于KIVI-KV2与Kitty。

在Qwen3-32B上，OSCAR达到74.00，略高于BF16的72.59，也超过Kitty的69.26。

这说明，OSCAR的优势不只体现在与TurboQuant的比较中。在现有KV Cache量化方法里，它也能以接近2-bit的预算守住

困难数学推理能力

。

但对serving系统来说，精度只是第一关。真正上线时，还要看显存、带宽、batch、prefix cache，以及端到端吞吐。

OSCAR在

系统层面的收益

也很直接：

相比BF16 history storage，OSCAR可以把KV Cache memory降低约8倍。

在100k context、batch-size-1、full prefix-cache hit的设置下，decode最高约3倍加速。

在大batch且显存预算固定时，job-level throughput最高约7倍。

这背后的逻辑很直白：当历史KV footprint变小，系统就能在同样显存预算下容纳更长上下文、更大batch，或者更多并发请求。

prefix cache命中率越高，KV Cache压缩带来的收益越容易转化为吞吐提升。

对于共享系统提示、多轮Agent、工具调用链路这类长前缀高复用场景，这一点尤其重要。

其实如果把OSCAR放在KV Cache量化的发展脉络里看，最重要的不是它又把bit数压低了一点。

更关键的是，它把2-bit KV Cache的问题从“向量压缩”推进到了

“attention质量”

和

“serving系统”

共同设计。

很多低比特方法为了保分，会把第一层、最后一层或若干敏感层保留在更高bit。这当然能减少精度损失，但也会抬高平均bit数，并让kernel和cache layout更复杂。

OSCAR的设定

更接近真实服务

：历史KV主体统一使用INT2，只在sink和recent两个很小窗口保留BF16。

这让它更容易接进paged cache、prefix cache和批量调度。

为什么这对长上下文Agent很重要

真实Agent往往包含很长的系统提示、工具说明、历史对话和检索内容。不同请求之间，还会存在大量共享前缀。

如果KV Cache全部使用BF16，显存很快会成为天花板。如果直接上朴素INT2，推理链条又可能失真。

OSCAR给出了一种更系统的折中：

长历史用INT2降容量和带宽；关键sink/recent用BF16保稳定；再让prefix cache复用共享前缀。

这也解释了为什么attention-aware rotation值得被单独提出。

它不是一个更花哨的旋转技巧，而是在重新定义低比特KV Cache的优化目标：

压缩不是目的

，

让模型在压缩后仍然能正确使用注意力机制，才是目的。

诚然，TurboQuant仍是很强的通用online vector quantization方法，OSCAR则更专注于attention-aware的2-bit KV serving。

两者并不一定只能二选一。

OSCAR目前code repo中已经把attention-aware rotation与更强的Lloyd Max codebook结合，把压缩率继续往极限推。

OSCAR带来的关键启发是：2-bit KV Cache如果要真正上线，旋转不能只追求“有”，而要

对准attention

。

同时，它也必须被放进真实serving系统里一起设计。

不过虽然目前OSCAR已经覆盖多个模型规模和多类推理任务，但真实线上workload更复杂。未来仍需要在更多模型架构、硬件环境、prefix cache命中模式、多租户请求和尾延迟场景中继续验证。

此外，OSCAR重点解决的是attention-aware rotation与2-bit KV serving。

后续如果能结合更强的动态窗口策略、更多硬件后端和统一serving框架，低比特KV Cache的边界还可能继续向前推进。

P.S.作者Zhongzhu Zhou是Together AI的Senior Research Scientist，悉尼大学博士，研究方向包括高效机器学习系统、模型训练与推理的算法系统协同设计，以及 LLM 压缩与量化。

团队成员分别来自Together AI、悉尼大学和伊利诺伊大学厄巴纳-香槟分校。

Together AI创立于2022年6月，联合创始人包括苹果前高管Vipul Ved Prakash、斯坦福大模型研究中心主任Percy Liang、芝加哥大学副教授Ce Zhang，以及FlashAttention作者Tri Dao。

论文链接：https://arxiv.org/abs/2605.17757

项目主页：https://oscar-quantize.github.io/

代码链接：https://github.com/FutureMLS-Lab/OSCAR

ModelScope链接：https://modelscope.cn/models/togethercomputer/OSCAR-RotationZoo

HuggingFace链接：https://huggingface.co/Zhongzhu/OSCAR-RotationZoo

一键三连

「点赞」「转发」「小心心」

欢迎在评论区留下你的想法！

—

完

—

我们正在招聘一名眼疾手快、关注AI的

学术编辑实习生

🎓

感兴趣的小伙伴欢迎关注 👉

了解详情

🌟 点亮星标 🌟

科技前沿进展每日见