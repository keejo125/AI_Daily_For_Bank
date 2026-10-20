---
publish_time: 1792493258
link: https://mp.weixin.qq.com/s/7p-Wq_qD_0lU1ndjR97X4g
source: 智东西
status: confirmed
category: 国内
is_model_related: false
digest: |
  智东西报道，DeepSeek 开源内部使用的云服务推理框架 DeepInfer 与生产级 Token 编解码组件 deepseek-recipe。DeepInfer 集成高性能算子与深度优化推理引擎，支持分布式推理、推测解码、SWA Bounded Replay、结构化输出，可在英伟达与华为昇腾平台运行。据团队公布，DeepSeek V4.1 Flash 的高吞吐、低延迟大规模推理服务即基于该框架，单集群吞吐达 155 万亿 Token/天，按谷价每卡每小时约 38 美元。
title: 梁圣大气！DeepSeek推理框架全开源，公布日均吞吐和毛利，真正的OpenAI来了
---

# 梁圣大气！DeepSeek推理框架全开源，公布日均吞吐和毛利，真正的OpenAI来了

来源：智东西
原文链接：https://mp.weixin.qq.com/s/7p-Wq_qD_0lU1ndjR97X4g

DeepSeek V4.1 Flash高吞吐、低延迟的背后，竟然是它？！
作者 |
王涵
编辑 |
心缘
梁圣又来送福利了！
智东西10月20日报道，刚刚，DeepSeek开源了其内部使用的、
大规模云服务推理框架DeepInfer
和
生产级token编解码组件deepseek-recipe
。
DeepInfer框架
集成了
高性能算子和深度优化的推理引擎
，支持分布式推理、推测解码、SWA Bounded Replay、结构化输出等能力，
可在英伟达与华为昇腾平台上运行
。
据DeepSeek团队公布，DeepSeek V4.1 Flash的高吞吐、低延迟大规模推理服务就是基于该框架实现的。目前，其单一集群的服务吞吐是
155万亿Tokens/天
，整体收入按照谷价计算是
每卡每小时38美金（约合人民币253.81元）
。
这个数字是什么概念？按这个数字粗略计算，一张卡24小时满负荷运行，
每天收入为6091.38元
；一个月按照30天计算，那
月收入就有185711.4元
。
生产级Token编解码组件deepseek-recipe
则支持
主流大模型API协议与模型Tokens之间的编解码
，处理逻辑与DeepSeek官方API完整对齐，可以确保第三方部署能获得与官方部署一致的API体验。
同时，DeepSeek在知乎发布了更加详细的技术报告，介绍了DeepSeek V4.1 Flash推理系统的整体架构与关键实现，以及今天开源的两部分的设计细节。
技术报告篇幅很长，我们用最新发布的
DeepSeek-V4.1-Flash-1017
模型总结了要点：
吞吐线：把GPU空转压到最低
1、节点内MoE专家并行（EP）：增大batch size，提高GPU矩阵乘效率。
2、并行度取值相反：Prefill用EP2～8/DP2～8（8卡机，显存够就取小）；Decode用EP64～128/DP64～128 Wide-EP（64～128卡超节点，卡够就取大）。
3、四类负载均衡器：
Prefill：四级调度共用一张代价模型，所有决策最终落到compute-quota；moe_lb 1.0320（EP2/DP2）、1.0618（EP4/DP4）。
Decode：两维均衡，moe_lb 1.090。
Vision Encoder：按patch粒度分配，一般单卡部署。
EP：冗余专家参数+动态重排。
DSpark 变长验证：低秩logit bias校正草稿模型偏差，Confidence Head 按置信度决定验证长度，替代固定验证5token，吞吐+6%。
4、异步调度：用CPU侧逻辑填满decode各步之间的GPU空档，做流水线重叠。
5、容错：不靠加快重启，靠多留机器、请求重路由、降级重启。
成本线：把重复prefill降到最低
1、KVCache长期留存：设计目标72小时以上；线上TTL为agent 3天、chatbot 7天（3天TTL会让chatbot命中率下降0.5%–1%）。
2、Block KVCache不进本机内存：按128token切块、4层mainKV，落独立3FS集群——约100PiB SSD，读10TiB/s、写约850 GiB/s（面向约112 KiB block粒度随机读写）。
换来的是「任意prefill机器可命中任意前缀」，代价是放弃前缀亲和路由。
3、SWA：20层×134的ring，只留本机内存、不持久化，TTL约180秒，命中率98%以上；未命中由Bounded Replay重算。
4、SWA Bounded Replay：V4把SWA落盘，占掉持久VCache近一半容量却换不到命中收益；V4.1改为只重算最近128 token，Decoder侧总prefill计算量近乎减半。
5、硬件成本：常见硬件组网（8卡机+超节点），兼容多厂商芯片，可在英伟达与华为昇腾运行。
延迟线：TTFT与TBT分别优化
1、编码器/Prefill/Decode分离部署：解耦资源分配，Prefill侧优化TTFT，Decode侧优化TBT。
2、chunk size按时间预算反解：由目标时延倒推每个chunk的大小。
3、分词不拖TTFT：分词从线性改为分段并行——special token之间的普通文本独立编码，再按序拼接；核心路径用Rust实现。
4、边生成边返回：跨chunk状态机缓冲不完整UTF-8码点，按思考/正文/工具参数分阶段维护状态，KMP增量匹配分隔标记，不回溯已确定文本。
5、工具参数不整体构造：按DSML边界直接输出JSON片段，字符串逐段转义，缩短首个参数片段的等待时间。
6、投机解码同时压延迟：Confidence Head按接受率分配验证算力，避免固定长度验证带来的无效等待。
技术报告地址：
https://zhuanlan.zhihu.com/p/2095560295930508953
开源地址：
DeepInfer:
https://github.com/deepseek-ai/DeepInfer
deepseek-recipe:
https://github.com/deepseek-ai/deepseek-recipe
DeepSeek团队补充说明称，由于推理系统中的KVCache管理与负载均衡组件因与内部基础设施耦合较深，相关代码目前尚未完整开源。未来，DeepSeek新模型的推理代码及后续性能优化也将在DeepInfer中持续开源。
