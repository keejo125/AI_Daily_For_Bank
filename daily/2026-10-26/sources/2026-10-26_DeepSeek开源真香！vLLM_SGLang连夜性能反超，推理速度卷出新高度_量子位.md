---
publish_time: 1793010600
link: https://mp.weixin.qq.com/s/fK3mkAFImswHu_ETHI2N1g
source: 量子位
status: confirmed
category: 国内
is_model_related: false
digest: |
  DeepSeek 开源推理引擎 DeepInfer 不到一周，社区接连交出作业：vLLM 集成其内核并对预填充/解码大量优化，在 GB200 上吞吐与 DeepInfer 差距仅 6%，扩展到 GB300 NVL72 机架每卡吞吐达 95.4 万 tokens/s（7.9 倍）；SGLang 在预填充最高超出约 4%，并补齐 KV 缓存、分离架构与负载均衡等组件。开源推理竞速进入白热化。
title: DeepSeek开源真香！vLLM/SGLang连夜性能反超，推理速度卷出新高度
---

# DeepSeek开源真香！vLLM/SGLang连夜性能反超，推理速度卷出新高度

来源：量子位
原文链接：https://mp.weixin.qq.com/s/fK3mkAFImswHu_ETHI2N1g

鹭羽 发自 凹非寺
量子位 | 公众号 QbitAI
还得是
「源神」
D老师，善呐！
自家推理引擎
DeepInfer
掏出来还不到一周，开源社区就纷纷交上了作业。
真乃一鲸“落”万物生，第一波开源效果已经新鲜出炉：
立志学习DeepSeek、成为DeepSeek、超越DeepSeek。
（bushi）
vLLM、SGLang这些成熟的推理框架率先迎来T0升级包——
在各自披露的测试配置下，性能已经
接近甚至部分超过DeepInfer
。
不戳不戳！DeepInfer最初基于vLLM构建，设计上也借鉴了SGLang的思路。
如今DeepSeek把打磨后的实现公开，两家又接着吸收、继续优化。
哥几个才是把
开源
玩出了花。
还有些受DeepInfer灵感启发的开发者个人项目陆续上线，从硬件适配、推理加速到部署优化，画风各不相同。
但效果倒是出奇一致：
都更能打了！
这下DeepInfer一开源，社区都热闹了起来。
推理竞速进入白热化，It’s showtime～
开源社区玩转DeepInfer
先看
vLLM
。
这回交出的成绩，已经从「追平DeepInfer」一路延伸到了整机架部署。
通过
集成DeepSeek的开源内核
，并对预填充和解码阶段进行大量优化，vLLM现在的性能曲线已经可以与DeepInfer持平。
在相同解码配置
（131K上下文、每轮3个草稿token）
下，vLLM使用GB200测得的吞吐量，在批大小为8到256的范围内，与DeepInfer差距仅为
6%
。
预填充这边，新增token的吞吐量也提升了35.6%～43.9%。
再把部署规模拉到NVIDIA GB300 NVL72机架。
配合预填充与解码分离、扩大专家并行，vLLM在SemiAnalysis AgentX测试中的每卡吞吐高达95.4万tokens/s，是此前单节点结果的
7.9倍
。
同一个DeepSeek，还真被他们继续挤出了速度。。。
要说这些提升怎么来的？团队几乎做到了每一个细节都不放过。
比如处理输入时，稀疏注意力需要从一批候选中筛出值得关注的内容，这就涉及top-k选择。
此前的一条路径，会先把DeepGEMM输出的BF16分数转换成FP32，再进行筛选。
新的实现则直接让
DeepSelect
处理BF16数据，把中间那次转换省掉。
少启动一道计算，看起来只是一个小改动，但在对应的算子测试中，这部分top-k处理速度能达到原来的
约3.7倍
。
vLLM团队还自己另外改了一套CPU通信方式，采用递归倍增等方式交换信息，减少同步所需的轮次。
对应Agent常用的小批量解码，vLLM也选择单独支持
DSpark草稿生成
，并使用完整CUDA Graph执行专用解码路径。
SGLang
紧接着交出的答卷，则走得更远，把输入、输出两个阶段都覆盖到了。
SGLang分别在4张B300、4张GB300上测试预填充，最高吞吐比DeepInfer高出
约4%
。
解码测试时，同样使用64张GB300。
每卡256个请求时，DeepInfer每步耗时31.19毫秒，SGLang为28.88毫秒，单步时间缩短约7.4%；每卡8个请求时，两者则基本持平。
具体操作中，SGLang先是将Mega内核
（MegaMoE、MegaAttention、Mega-mHC、MegaGate）
、SWA有界重放以及Engram优化通通集成。
达到对标DeepInfer的性能后，再继续迭代，引入更多内核融合方案。
随后通过支持
可拆分CUDA图
，实现高效预填充。
最终对比DeepInfer的开源版本，
SGLang更为完整
，额外补充了关键的服务组件，包括KV缓存系统、预填充/解码分离架构以及负载均衡模块。
值得一提的是，SGLang为了更严谨地对比，还在GB300和B300上，将DeepInfer重新跑了一遍。
结果不跑不知道，DeepInfer部分配置的吞吐，比原先公布的成绩
还高
。。。
好家伙！原来D老师真是老实人，测试成绩相当实在！
推理加速循环
开发者Eric Zhang又把玩法往前推了一格。
此前他一直在开发一套用于搭建大模型推理引擎的实验性积木库——
Resin
。
它把多个模型都会用到的部分做成
公共底座
，比如调度器、KV缓存管理等。再由用户自行补上特定模型、特定硬件需要的计算实现，就能组合出一个独立引擎。
Eric自述，最近一周他
受DeepInfer启发
，成功让不少功能和并行机制跑了起来。
根据测试结果，在DeepSeek-V4.1-Flash上，Resin的性能与DeepInfer相差约
5%～10%
，同时具备HTTP服务、前缀缓存和指标等功能。
接着，他又给这个底座配了个Skill。
任务是教会AI如何基于Resin实现模型，再把Codex放上去通宵干。
据他披露，Agent完成了支持MTP的
GLM-5.3-Flash
引擎；在B200、EP4配置下，输入吞吐最高达到6万tokens/s，输出吞吐最高达到1.6万tokens/s。
而且！Resin依旧开源。
泪目了，大肥鱼，这开源盛世如你所愿。
DeepInfer从开源来，又回归开源。成熟框架接着继续集成和优化，个人开发者也得以吸收其中的设计，接力开源。
So，大肥鱼才是真正领悟了
可持续开源
的真谛～
参考链接：
[1]https://vllm.ai/blog/2026-10-23-deepseek-v41-flash-pd-wide-ep
[2]https://gist.github.com/sglang-bot/f03d7d0dd268b0386177eb2ef09f8b3b
[3]https://x.com/BanghuaZ/status/2114083299102691751
[4]https://x.com/vllm_project/status/2112480719952138301
[5]https://x.com/ekzhang1/status/2114516258188153215
一键三连
「点赞」「转发」「小心心」
欢迎在评论区留下你的想法！
—
完
—
🌟 点亮星标 🌟
科技前沿进展每日见
