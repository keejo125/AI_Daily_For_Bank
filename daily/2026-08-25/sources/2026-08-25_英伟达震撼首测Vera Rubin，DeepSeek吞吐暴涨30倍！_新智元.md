---
publish_time: 1787613328
link: https://mp.weixin.qq.com/s/TOz7SHlyAvX5P7PIXFpm4w
source: 新智元
status: confirmed
category: 国际
is_model_related: false
digest: |
  英伟达首测下一代机柜Vera Rubin NVL72：在AgentX基准（回放真实代码编写会话）下跑DeepSeek-V4-Pro，每兆瓦吞吐较GB300最高提升30倍、每百万Token成本最高降35倍。
  配套量产的Groq 3 LPX推理加速器达3400 Token/秒；专为Agent打造的Vera CPU（88核Olympus）已由SpaceXAI规模化部署并计划送上天。文章称Agent时代基准与算力格局被重写，老黄卖的是「AI工厂」。
title: '英伟达震撼首测Vera Rubin，DeepSeek吞吐暴涨30倍！'
---

# 英伟达震撼首测Vera Rubin，DeepSeek吞吐暴涨30倍！

来源：新智元

新智元报道
太炸裂了。
就在刚刚，英伟达史上首次公布了下一代旗舰级机柜 Vera Rubin NVL72 的首次片上实测数据。
而且，这次实测直接拉来了DeepSeek-V4-Pro，跑最真实的「智能体编码」任务！
结果令人吃惊：对比当前的主力机皇GB300 NVL72，Vera Rubin的每兆瓦吞吐量最高飙升了30倍、Token成本最高暴降了35倍！
有人惊呼：「我连骗投资人的 PPT 都不敢这么写！」
还有网友神评：「以前嫌 H200 三万美元一张贵，现在回头一看，H200 居然连丐版都算不上了。」
让我们来仔细盘一盘。
从H200到GB300，真实Agent工作负载的吞吐量提升了最高30倍，成本大致翻倍。
从GB300到Vera Rubin，吞吐量再次飙升最高30倍，整机架价格大致再翻倍。
按照老黄的摩尔定律，合着这两年英伟达最大的技术突破不是GPU本身，而是让价格贵了4倍，却换来了整整900倍的速度飞跃！
这次，英伟达向所有人宣布了一个反常识的真相：LLM时代结束，Agent时代降临，以前的AI跑分基准，全部作废！
与此同时，专为智能体打造的Vera CPU，已被马斯克的SpaceXAI连夜装机，甚至准备直接打上太空.
同在今天，英伟达Groq 3 LPX也全面量产。
Gemma 4 31B在上面跑，速度简直绝了，直接干到每秒3400个Token。万亿参数模型吞吐，狂飙35倍。
这些新纪录，直接让Agent生态的商业格局，从今夜开始重写！
为什么英伟达必须推出Vera Rubin？
OpenRouter的最新数据给出了答案：在真实世界里，一个Agent AI任务消耗的Token数量，是普通聊天对话的15倍！
比如，如果让一个Agent为投资决策去研究一家公司，在这个过程中，智能体和子智能体会不断推理，累积的Token成为下一步的输入，长上下文处理，就成为限制智能体AI的最关键要素。
智能体交互次数越多，吞吐量越大——智能体数量多了10倍，工具调用多了2倍，算力和算法的矛盾催生了新的需求。
别拿聊天当智能体，旧基准全废了！
这时候，传统的AI基准测试（如固定长度的8K/1K序列测试）就彻底无效了。
英伟达官方挑明：性能测量必须进化！不能再测单一的推理请求，必须捕捉完整的Agent工作流。
为此，他们使用了SemiAnalysis 旗下的 AgentX 基准测试。
这个测试不再是死板的问答，而是回放真实的、具有上下文增长、工具调用和子智能体生成的「代码编写会话」。
这就是为什么H200在新的Agent战场上显得力不从心，Vera Rubin注定要称王。
Vera Rubin NVL72 × DeepSeek-V4-Pro：
算力怪物来了
为了证明Vera Rubin NVL72的实力，英伟达直接使用开源王者——DeepSeek-V4-Pro (1.6T) 进行片上实测。
数据一出，结果惊人——
在AgentX工作负载下，Vera Rubin NVL72的每兆瓦吞吐量，比GB300 NVL72最高提升了整整30倍！
请注意，这里对比的不是老旧的H200，而是炙手可热的主力GB300。
GB300在同样的DeepSeek-V4-Pro测试中，每兆瓦吞吐量已经比H200提升了15倍。
然而Vera Rubin却在GB300的肩膀上，又拔高了30倍，在整个帕累托曲线上又提高了！
这意味着什么？
对于受制于电力供应的「AI工厂」来说，这直接拓展了物理法则边界。
在同样的电力预算下，Vera Rubin能干30倍的智能体活儿。
对于兆瓦级甚至吉瓦级的数据中心来说，这相当于凭空变出了30倍的算力资产。
而且，NVIDIA DSX MaxLPS 技术可以在 GPU、机架和工作负载层面进行电源管理，能在相同的兆瓦预算内多配置高达 40% 的 GPU，让AI工厂进一步提升了每兆瓦吞吐量！
Token成本暴降35倍！Agent行业的「账本」彻底重写
每兆瓦吞吐量，直接影响的就是每个生成 token 的成本。性能的飙升，带来的最直接后果就是商业模式的核爆。
英伟达宣布，Vera Rubin NVL72 生产每百万Token的成本，比 GB300 NVL72 最高降低了 35 倍！
当推理成本呈断崖式下跌35倍时，24小时无休的数字员工将成为现实，ToC端超级应用将迎来大爆发。
老黄这一刀，直接切开了Agent应用的时代大门。
极致协同设计：老黄是怎么做到的？
你可能会问：凭什么能提速30倍？靠的是单颗芯片的工艺吗？
显然不是。
Vera Rubin NVL72惊人的性能提升，靠的是「极致协同设计」。
比如分离式服务，分布式KV缓存，KV感知路由，MegaMoE等等。
另外，NVFP4 量化直接将模型权重压缩到 4 位精度，在不牺牲输出质量的情况下，大幅缩减内存占用，让吞吐量原地起飞。
而第六代 NVLink 与大模型MoE，提供了比现成以太网快10倍、延迟低3倍的互联网络，让像DeepSeek这种基于MoE架构的大模型，可以在72个GPU之间行云流水地调用不同的「专家」子网络。
这早已不是在卖显卡，老黄卖的是一整套「AI发电厂」。
英伟达Groq 3 LPX 全面量产：
3400 Token/秒，代码Agent变天！
这次Hot Chips 2026 大会上，英伟达还抛出一个震撼消息：Groq 3 LPX 开始全面量产！
Groq 3 LPX，是Vera Rubin NVL72 数据中心平台的专属扩展。
它是专为这个系统「量身定制」，主打就是一个低延迟推理加速。
这项黑科技，是去年12月英伟达豪掷200亿美元从初创公司 Groq 手中买来的。
AI智能体会遇到解码延迟的问题，为了终结这一痛点，Groq 3 LPX 巧妙地将庞大的上下文处理与 Token 生成彻底分离。
英伟达的解法是，让Rubin GPU处理大规模上下文，把极速生成Token的任务交给Groq 3 LPX。
一个管「读」，一个管「写」，各干各最擅长的。
在一个完整的机架级部署中，多达 256 个 LP30 加速器可以通过超高带宽互连与 GPU 协同作战，构造出企业级规模的推理引擎。
由此，Groq 3 LPX直接达到了破纪录的输出速度。
在 Artificial Analysis 的基准测试中，Groq 3 LPX 在 10 万 Token 超长上下文窗口下运行Gemma 4 31B，输出速度达到惊人的3,400 Token/秒！
这使得它在延迟极度敏感的工作负载中，响应速度比竞品快了4倍。
过去几个小时才能完成的多步智能体任务，现在几分钟内就能完成！
Groq 3 LPX在生成5000 Token，所用时间从50秒将至1.5秒，34倍差距。
而且在编码任务中，Groq 3 LPX最大输出速度6981 token/s。
黄仁勋直言，通过 LPX 推进超高速 Token 生成，在 AI 吞吐量和响应能力上实现了「又一次巨大飞跃」。
Nebius已经在Nebius Token Factory 中部署该芯片，让智能体循环的每一步都能获得即时响应的极致体验。
紧随其后的，还有Groq自己。
首款Agent专属CPU发布，
马斯克连夜「打上太空」！
这次官宣中，最具野心的一步棋，就是 Vera CPU了。
为了Agent，英伟达专门造了一颗CPU。
Vera这颗CPU，就是专门喂饱智能体的，
它配备了88个自研的Olympus核心，高带宽的LPDDR5X内存，带宽直接干到1.2TB/s。
为什么大模型时代需要全新的CPU？
Hot Chips现场，英伟达Vera CPU高管直言，「Agentic AI是史上最复杂的计算任务」。
一次任务，Agent背后要跑上百步：调用工具、执行Python代码、翻上下文、处理海量数据....
这些跑腿调度的活儿，全都压在CPU身上硬扛。因此，英伟达必须给Agent单独造颗CPU。
正是看中了这一点，马斯克的 SpaceXAI 连夜宣布，正式规模化部署英伟达 Vera CPU！
早在今年5月，英伟达就把第一批Vera样片，悄悄送到了A社、OpenAI、SpaceXAI先「试水」。
仅仅3个月后，SpaceXAI 就迫不及待地将其转入全面部署。
更疯狂的是，SpaceXAI 正在基于Vera Rubin 平台建设吉瓦级算力工厂，用来驱动Grok。
不仅如此，这套算力，还要被直接送上太空。
马斯克表示，「两家强强联手，设计了一款优化版的Vera Rubin NVL72，将在2028年大规模部署」。
SpaceXAI的第一代「Starmind」AI卫星，就计划采用Vera Rubin NVL72 机架级系统。
从一块GPU，到整座Agent工厂
同一天，两大芯片Vera CPU和Groq 3 LPX，全面量产。
这对英伟达来说，意义重大。
大模型时代，英伟达靠GPU拿下训练和推理。
Agent时代，它的版图已经延伸到CPU、推理加速器、NVLink等等。
老黄卖的，早已不只是一块GPU。
他要卖的，是一座可以不断生产Token的AI工厂。
老黄这一次，是要给整个「Agent时代」重新铺一遍地基。
参考资料：
https://x.com/MinLiBuilds/status/2091915873661686204
https://developer.nvidia.com/blog/nvidia-vera-rubin-and-blackwell-set-a-new-standard-for-agentic-ai-performance-per-watt/
https://developer.nvidia.com/blog/inside-nvidia-groq-3-lpx-the-low-latency-inference-accelerator-for-the-nvidia-vera-rubin-platform/
https://developer.nvidia.com/blog/maximizing-ai-factory-performance-per-watt-with-nvidia-dsx-maxlps/
编辑：编辑部
秒追ASI
⭐
点赞、转发、在看一键三连
⭐
点亮星标，锁定新智元极速推送！
