---
publish_time: 1794306600
link: https://mp.weixin.qq.com/s/44vxpEPwrlo9Y3egWqsc4Q
source: 智东西
status: confirmed
category: 国际
is_model_related: true
digest: |
  智东西报道 Meta 发布 Muse Ember：最小最高效模型，100 万上下文、原生多模态，专为 Agent 全天高频、高 Token 消耗任务打造。AA 测评最高档 35.8 分持平 Haiku 5.5（36.2），但单任务成本约 0.14 美元、仅为其三分之一；定价每百万输入 0.10、输出 0.50 美元，已通过 Meta Model API 与 Muse Code 开放。
title: 便宜得离谱！Meta甩出“最省钱模型”，1/3成本追平Claude Haiku 5.5
---

# 便宜得离谱！Meta甩出“最省钱模型”，1/3成本追平Claude Haiku 5.5

来源：智东西
原文链接：https://mp.weixin.qq.com/s/44vxpEPwrlo9Y3egWqsc4Q

单项任务成本约为Claude Haiku 5.5的三分之一。
编译 |
黄菲
编辑 |
江宇
智东西11月10日消息，今日，Meta正式发布最新模型Muse Ember，
主打复杂推理和智能体任务
。Meta称，这是其迄今体量
最小、效率最高
的模型，能够跨应用执行工作流、连续调用工具、运行测试并修复代码。Muse Ember
持100万Token上下文窗口
，具备对文本、图像、音频和视频的原生理解能力，
可处理大规模文档和多模态输入
。
Meta创始人兼CEO马克·扎克伯格（Mark Zuckerberg）也在社交平台X上宣布了这一消息，他谈道：“Muse Ember是Meta目前最小的模型，在同类模型中能够以更低的成本提供更强的算力，专为Agent全天反复执行、消耗大量Token的工作打造。”
该模型也是
首款使用Muse Wonder Full训练的模型
。Muse Wonder Full于今年10月12日发布，时隔近一个月，Meta便基于这一模型开发出Muse Ember，进一步利用Wonder系列模型训练专用模型。
在第三方Artificial Analysis测评中，
最高推理强度下Muse Ember得分为35.8分，与Claude Haiku 5.5（36.2）基本持平
，
但其完成
单项任务的成本仅约0.14美元（约合人民币0.94元）
，约为Claude Haiku 5.5的三分之一。同日发布的Anthropic新模型Claude Fable 5.2则取得65分，高出Muse Ember 29分。
价格方面，Muse Ember定价为
每百万输入Token 0.10美元（约合人民币0.67元）、每百万缓存输入Token 0.004美元（约合人民币0.03元）、每百万输出Token 0.50美元（约合人民币3.36元）
。
目前，Muse Ember已通过Meta Model API和Muse Code开放使用，并支持Responses API。
01
.
网页生成实测表现亮眼
20多个网站平均2分钟完成
Muse Ember发布后，不少用户和开发者在社交平台X上分享了对模型本身及实际使用体验的看法。
有用户称，Muse Ember以轻量化的模型体量支持原生多模态输入和100万Token上下文窗口，却不会给GPU带来过重负担，这正是本地开发工具运行真实Agent工作流所需要的能力。
另一用户则认为，相比每Token的价格，“单项任务成本”才是更值得关注的指标。他举例称，一个便宜但需要重试三次才能完成任务的模型，实际成本可能高于一个价格更贵、但一次就能正确完成任务的模型。他还提到，如果Muse Ember在真实Agent工作负载中确实能将成本降至同类模型的三分之一，这才会真正推动用户采用。
第三方评测机构Vals AI称，Muse Ember是其Vals Index中单项测试成本最低的模型，
每项测试仅需0.15美元（约合人民币1.01元）
。该模型在测试中取得
60.5%
的成绩，
超过Claude Haiku 5.5和GPT-6 Luna
。Muse Ember完成测试约需
15分钟
，是榜单前12名模型中速度最快的。
在实际网页开发测试中，Arena.ai将Muse Ember接入Code Arena: WebDev，并让模型一次性生成20多个网站和动画。Arena.ai称，Muse Ember是
目前该平台上表现最好的小模型
，能够以较快速度、较低成本生成高质量网页。在其计时的多轮生成任务中，模型平均
每次生成耗时约2分钟
。
从其展示的画面中，可以看到Muse Ember生成了一个名为NOCTIS的香水品牌网站，包含产品展示、香水分类、香调介绍、产品对比和试香盒组合等功能。
除了网页生成，Muse Ember还被用于3D模型设计测试。一名开发者称，在一项生成树木模型的任务中，Muse Ember仅用33秒便完成了5种不同树木模型的生成，
速度比对比模型快25倍
。生成结果还为每棵树分别添加了标签，并提供树木高度、多边形数量等细节信息，以及线框视图。
另一名开发者则分享了Muse Ember在其近期发布的批发业务基准测试ORO SMB Bench中的表现。他称，Muse Ember在这项测试中的
表现与GLM 5.3、Grok 4.7和Muse Spark 1.3相当
。不过，Muse Wonder 1.0的表现仍然是其中最差的。他还提到，团队正在补充GPT-6 Luna和Claude Haiku 5.5的测试，以便进行真正的横向比较。
有用户也直接评价称：“Muse Ember真的非常快。”其分享的截图显示，通过OpenRouter调用Muse Ember时，一次运行完成了18个步骤，界面显示生成速度达到
3565 Token/秒，缓存命中率为75%
。
不过，另一名用户对Meta AI的产品体验提出批评，他称，Meta AI的安全限制过多，自己已经取消订阅。他谈道，自己甚至无法让Meta AI准确回答当前运行的是哪个模型，期间得到的回答前后不一，一开始声称运行的是Muse，后来又突然称自己运行的是Muse Wonder。
02
.
单项任务成本低至0.14美元
Agent测试比肩Claude Haiku 5.5
Muse Ember主要面向AI Agent执行过程中大量重复发生的任务。Meta称，Agent在完成复杂工作时，需要反复调用工具、读取文件、运行代码、提取信息和修改结果。这些任务单次并不复杂，但在长工作流中会持续消耗Token和算力。
Muse Ember正是为这类高频任务设计，可承担工具调用、运行测试和有针对性的代码修复等工作。Meta称，在不同推理强度设置下，
Muse Ember的单位成本智能水平基本高于Claude Haiku 5.5和GPT-6 Luna
。
在考察模型综合智能水平的Artificial Analysis Intelligence Index v5中，在最高推理强度下，Muse Ember与表现最好的模型Claude Haiku 5.5
得分仅相差0.4分
。
Muse Ember得分为35.8分，低于Claude Haiku 5.5的36.2分，但Muse Ember完成单项任务的成本仅为0.136美元（约合人民币0.91元），是后者单项任务成本的三分之一（约为0.411美元，约合人民币2.74元）。
与Meta自家的Muse Spark 1.3相比，Muse Ember的成本优势也较为明显。
同样在测评集Artificial Analysis Intelligence Index v5中，
Muse Ember的得分为36分，Muse Spark 1.3为37分
。
这两款模型完成单项任务的成本分别约为0.14美元（约合人民币0.94元）和2.39美元（约合人民币15.94元），
Muse Ember的单项任务成本不到Muse Spark 1.3的5.9%
。
在Agent任务测试中，
Muse Ember在AutomationBench-AA、Agents' Last Exam等多项评测中均取得第一
。
在测试模型能否完成端到端业务流程的测评集AutomationBench-AA中，
Muse Ember得分为
37.8%
，高于GPT-6 Luna的
20.2%
和Claude Haiku 5.5的
13.9%
。
在测试模型能否完成复杂工作任务的测评集Agents' Last Exam中，
Muse Ember得分为
61.6%
，高于GPT-6 Luna的
57.1%
和Claude Haiku 5.5的
57.0%
。
在测试模型综合智能指数的测评集Personal Superintelligence Index中，
Muse Ember得分为
46.8%
，高于GPT-6 Luna的
37.0%
和Claude Haiku 5.5的
36.1%
。
编码能力方面，Muse Ember在多项测试中也表现出竞争力，但在真实工程任务上仍有差距，
三项测试中两项取得第一成绩
。
在测试模型在真实Agent框架中完成编码任务能力的测评集Coding Agent Index中，
Muse Ember得分为46分
，高于Claude Haiku 5.5的
37分
和GPT-6 Luna的
31分
。
在考察模型通过终端环境完成Agent式编程任务能力的测试集Terminal-Bench 4.0中，Muse Ember得分为40.9%，略高于Claude Haiku 5.5的39.2%，领先GPT-6 Luna的16.4%。
在考察模型能否完成真实工程任务的测试集Artificial Analysis的FrontierCode 2.0-AA中，Muse Ember并不占优，该模型在这一项上仍
落后于Claude Haiku 5.5
。Claude Haiku 5.5得分最高，为34.9%；Muse Ember落后，为27.2%；GPT-6 Luna最低，为25.2%。
在多模态和电脑操作方面，
Muse Ember表现与GPT-6 Luna、Claude Haiku持平或更高
。Meta称，该模型还能根据截图直接操作电脑，并识别画面中的细节。
在考察模型长文档能力的测试集GDP.pdf-AA中，
Muse Ember与GPT-6 Luna均得分22.8%
，高于Claude Haiku 5.5的
20.8%
。
Meta还通过测试集OSWorld 2.1，考察模型在真实桌面应用环境中操作电脑的能力。
Muse Ember得分为69.5%
，略高于Claude Haiku 5.5的
68.9%
，领先GPT-6 Luna的
50.5%
。
在考察模型对图像中细节信息的识别与理解能力的Meta内部测试PerceptionBench中，
Muse Ember得分为80.6%
，高于Claude Haiku 5.5的
78.6%
和GPT-6 Luna的
62.8%
。
03
.
企业合作伙伴反馈积极
Muse Ember主打执行任务
在企业应用方面，Meta邀请网络安全服务商Cloudflare和AI搜索平台You.com等合作伙伴参与早期测试。
Cloudflare首席技术官戴恩·克内希特（Dane Knecht）称，在该公司的测试中，Muse Ember能够将部分任务的
尾部延迟降低最多30%
。
You.com推理负责人查克·波蒂纳（Chak Pothina）则谈道，Muse Ember完成了其测试中的全部编码任务，
P95延迟为2.2秒
，速度约为部分
领先开源模型的
4至13倍
，
输出Token数量减少36%至48%
。
按照Meta的定位，Muse Wonder主要处理难度最高的问题，Muse Spark面向编程和Agent工作流，Muse Ember则负责大规模、重复性的编码和Agent任务。Meta称：“Muse Wonder负责规划，Muse Ember负责处理大量执行任务。”
Muse Ember还是
首款使用Muse Wonder Full训练的模型
。Meta此前称，将利用Muse Wonder系列模型开发更专门化的模型，再将这些能力带给更多用户。Muse Ember正是这一思路下推出的产品。
在安全方面，Meta称，Muse Ember发布前已按照Meta超级智能扩展框架（Superintelligence Scaling Framework）进行评估，覆盖化学与生物安全、网络安全和失控风险等类别。在已评估的风险类别中，该模型均未达到框架设定的高风险阈值。
04
.
结语：大模型造小模型
Meta探索Agent时代的模型分工
从Muse Ember的产品定位来看，Meta正进一步细化不同规模模型在Agent工作流中的分工，让Muse Wonder Full等大模型承担复杂任务，并通过更轻量化的小模型处理高频调用和重复执行任务。
基于Muse Wonder Full训练的Muse Ember，在部分测试集中已能取得优于通用大模型的成绩，同时兼顾执行速度与调用成本。
对于需要持续调用模型的开发者和企业而言，Muse Ember为高频Agent任务提供了成本更低的选择，也让小模型成为大模型能力的重要补充。
来源：Meta
