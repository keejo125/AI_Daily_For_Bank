---
publish_time: 1788413899
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/kv1YsmetgCs3QJxyy3KWKQ
source: 智东西
title: Meta旗舰模型翻身！比DeepSeek还便宜，华裔掌门人骑脸Gemini
---

# Meta旗舰模型翻身！比DeepSeek还便宜，华裔掌门人骑脸Gemini

来源：智东西
原文链接：https://mp.weixin.qq.com/s/kv1YsmetgCs3QJxyy3KWKQ

5个月迭代4款模型，下一步还要开源。
编译 |
程茜
编辑 |
心缘
智东西9月3日消息，今日，Meta发布新一代最强旗舰模型
Muse Spark 1.3
。在Artificial Analysis的AI分析指数榜上，新模型分数
仅次于Claude Fable 5.1、Claude Opus 5
。
Meta联合创始人、CEO马克·扎克伯格（Mark Zuckerberg）在社交平台X上称，Muse Spark 1.3的性能
超乎想象
。
Meta超级智能实验室负责人、首席AI官汪滔（Alexander Wang）称，该模型
成本低到几乎可以忽略不计
，智能体、编程能力以及易用性大幅提升。并且
Muse Spark 1.3搭配Muse Code
，评测表现可与Claude Code + Opus 5、Claude Code + Fable 5媲美。
有开发者使用Muse Spark 1.3制作了《我的世界》游戏，成本仅
10美分（约合人民币0.67元）
。
就在Meta新模型发布的4个小时前，谷歌发布了自家
迄今为止最强的推理与编程模型
Gemini 3.8的Gemini 3.8 Flash和Gemini 3.8 Flash Cyber版本
。但随后在Artificial Analysis榜单上被Meta反超。目前在AI分析指数榜上，Muse Spark 1.3得分为62分，仅次于66分的Claude Fable 5.1和63分的Claude Opus 5，Gemini 3.8 Flash为59分。
谷歌在Artificial Analysis指数上仅领先了几个小时，就被Meta反超，汪滔还在社交平台上对谷歌贴脸开大：“gemini who？”，还说“Gemini现在取消（上线）还不算晚”。
过去5个月，Meta接连推出四款Muse Spark模型：4月首发Muse Spark，7月更新Muse Spark 1.1、8月上线Muse Spark 1.2，再加上最新的Muse Spark 1.3，其迭代节奏愈发密集。
从Meta放出的基准测试图可以看出，
Muse Spark 1.3拿下5项第一
，在长上下文、编程的绝大部分测试都优于GPT‑5.6 Sol、Claude Opus 5，仅Terminal‑Bench终端操作Agent测试与GPT‑5.6 Sol打平。其相对薄弱的是Agent能力，在联网搜索类Agent、通用知识任务GDPVal‑AA v2中分数较低。
价格方面，Muse Spark 1.3的‌API定价
与前代1.2保持一致
，每百万token输入（缓存未命中）1.25美元（约合人民币8.4元），每百万token输入（缓存命中）0.15美元（约合人民币1元），每百万token输出为4.25美元（约合人民币28.55元）。Muse Spark 1.3的价格略高于Gemini 3.8 Flash，比DeepSeek-V4-Pro的高峰期价格还便宜。
▲部分大模型价格对比（智东西制表）
Muse Spark 1.3已在Muse Code与Meta Model API中逐步推送上线，此前已支持的推理模式现已可用；max‑reasoning（极致推理模式）将在完成额外安全测试后很快开放。
Meta称，其已规划好令人期待的产品路线图，包含更大参数规模模型、Muse Spark开源权重版本发布以及更多更新。
01
.
开发者实测：速度快、成本低
但生成效果一般
在社交平台X上，不少开发者晒出了自己实测Muse Spark 1.3的案例，大部分人的评价是速度快、成本低，但生成效果并不惊艳。
一位开发者对比了Muse Spark 1.1到1.3对同一栋建筑仅基于照片进行3D模拟的效果，其在几何形状、结构以及视觉效果上都有明显提升，总成本都保持在0.6美元（约合人民币4.03元）不变。
还有一位开发者晒出了Muse Spark 1.3 Ultra Contributor（开启Ultra超高算力模式）版本和Claude Fable 5.1 xHigh的对比效果，使用相同提示词，双方均运行约2小时。提示词内置了一套自我迭代优化规则：如果独立评审模型给输出结果打分低于9.5/10，模型就必须持续优化、重新尝试。
令他震惊的是，Muse Spark一直在迭代，一共跑了20轮自我优化循环，每轮会启动3个智能体；两小时内累计执行60次以上智能体任务，但成本不到1美元（约合人民币6.7元）。
有一位网友在评论区质疑，这是不是说明Muse Spark 1.3一直没有完成任务，只花费1美元（约合人民币6.7元）就停止了。
开源的3D空间推理基准测试MineBench中，对比Gemini 3.8 Flash和Muse Spark 1.3的实测显示，Gemini 3.8 Flash总测试成本1.18美元（约合人民币7.93元），平均推理耗时1分51秒，首测Elo评分为1888分；Muse Spark 1.3总测试成本6.57美元（约合人民币44.14元），平均推理耗时5分36秒，首测得分1787分，其生成输出质量距离顶尖前沿模型仍存在一定差距。
另一位开发者对比了Muse Spark 1.3、Qwen 3.8 Max、GLM 5.3、GPT-5.6 Sol的效果，他的综合感受是Muse Spark 1.3在成本与速度方面可以与Qwen 3.8 Max相媲美，GLM 5.3在性能、成本、速度以及token使用量方面的综合表现堪称最佳。
虽然Muse Spark 1.3的价格非常低廉且运行速度快，但表现只能算不错。Qwen 3.8 Max输出的成果质量最好、完成度最高，但耗时大约一个半小时，Muse Spark只需要约2分钟。
02
.
长周期任务不跑偏
编程token量减少25%
Meta的博客提到，Muse Spark 1.3的优势在于支撑长周期任务以及编程。
Muse Spark 1.3能够与用户协同，在单条长对话会话中并行处理多条工作流。面对开放式目标时，它会调用工具，从杂乱、相互矛盾的信息源中自主构建上下文，然后主动修正方案漏洞，并基于已获取的信息输出完整交付成果。
同时，Meta的研究人员基于多套多样化评测框架完成模型训练，使其能够适配各类智能体运行环境。
例如下图中，Muse Spark 1.3获得的提示词非常复杂，其需要在不同的位置找到活动详情、文案、图片，然后编辑组合在广告管理平台中创建并发布。
相比之前的Muse Spark模型，Muse Spark 1.3能在多步骤任务中，更好保留细节要求，不会遗漏约束条件，也不会偏离既定工作流程。
Meta还改进了Meta的多任务处理能力，例如即便是在信息杂乱的单会话上下文里，无论用户是接续过往任务，还是中途打断任务，模型都能把新输入提示匹配到对应的任务上。
Muse Spark 1.3能了解自己能做什么、不能做什么，知道什么、不知道什么，以及在遇到障碍时该如何应对，而不是产生错误的预测结果。
例如，当提示词为“你是一家小型航空企业的机械工程师，正在为下一代飞行器设计一款实验型 X 型机翼组件。为配合设计评审，请基于附件材料撰写一份流体仿真报告初稿：（1）初步CFD仿真结果；（2）用于本次仿真的机翼组件CAD模型STEP文件。”Muse Spark 1.3就会生成对应的文件：
编程方面，与Muse Spark 1.2相比，Muse Spark 1.3需要的操作步骤更少，表述也更简洁，整体编码风格也更为清晰。根据Meta工程师的测试结果显示，它的工具调用次数减少了20%，使用的token数量减少了25%。
▲Muse Spark 1.3生成的超能力风暴游戏
此外，研究人员围绕智能体与代码能力相关的多个维度完成了安全能力升级。Muse Spark 1.3的对抗鲁棒性有所增强，对对抗输入与提示注入攻击的抵御能力得到提升；处理复杂智能体任务时，模型对不可逆操作具备风险判断，并据此审慎执行动作。
03
.
结语：5个月迭代4版
Meta的大模型要起飞了？
5个月迭代4个Muse Spark模型版本，这样密集的发布节奏，或标志Meta的AI研发进程发生明显转变。并且从模型能力上看，Muse Spark 1.3没有追求全维度通杀，而是把资源集中砸向长上下文、编程等方面，在DeepSWE、OSWorld等面向真实工程任务的基准上实现对前沿模型的反超。
这种取舍或许也证明，未来开发者、企业选型不会再追求“一个模型搞定全部”，多模型路由，根据任务类型调度不同专长模型，可能会成为企业落地Agent的主流方案。
来源：Meta、X
