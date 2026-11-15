---
publish_time: 1792398733
link: https://mp.weixin.qq.com/s/EEoOYzQ9fodD4bNP62zNpQ
source: 智东西
status: confirmed
category: 国际
is_model_related: false
digest: |
  成立 8 个月的美国 AI Agent 创企 Conway Research 发布首款个人 AI 助手 Underdog，并官宣获 Anthropic 旗下投资联合体、a16z 以及来自谷歌、OpenAI、Hugging Face 的 AI 大牛等个人与机构投资。Underdog 被称作“迄今隐私性最强的 Muse 竞品”：继 Meta 9 月发布 Muse（10 天登顶美区 App Store）后，OpenAI 推 Dot、马斯克推 Grok Bot、Manus 推 2.0，字节、腾讯、蚂蚁、阿里等也被曝在研类似“always-on 个人 agent”产品。
title: 华人00后做“本地Muse”，被硅谷AI圈疯抢，a16z和Anthropic都投了
---

# 华人00后做“本地Muse”，被硅谷AI圈疯抢，a16z和Anthropic都投了

来源：智东西
原文链接：https://mp.weixin.qq.com/s/EEoOYzQ9fodD4bNP62zNpQ

创始人大学肄业、自学成才。
作者 |
程茜
编辑 |
李水青
智东西10月19日报道，近日，一家刚成立8个月的美国AI Agent创企Conway Research
‌
，亮出
首款个人AI助手Underdog
，同时官宣获得
Anthropic旗下投资联合体
、硅谷知名风投公司a16z，以及来自
谷歌、OpenAI、Hugging Face的AI大牛
等个人及机构的投资
。
▲Conway Research‌创始人Sigil Wen官宣融资的推文（图源：X）
该公司将Underdog称作“
迄今为止隐私性最强的Muse竞品
”。
9月8日，Meta发布个人AI助手Muse，上线仅10天就超过ChatGPT登顶美国App Store免费应用总榜。Muse可自主拆解用户目标、执行任务，覆盖办公、生活、消费等多场景，每名用户拥有云端独立虚拟机，可后台持续执行任务。
这股热潮迅速扩散，OpenAI发布新一代智能体产品Dot、马斯克发布Grok Bot、Manus推出2.0，还有国内字节、腾讯、蚂蚁、阿里也被曝正进行研发类似产品。
Underdog与Muse这类产品的功能类似，都是帮助用户处理日常生活、工作的任务，最大不同之处在于，
Underdog完全运行在用户的设备上，且离线也能跑
。
▲Underdog自动添加日程演示（图源：Conway Research‌）
Conway Research
‌
成立于今年2月，其核心研究方向是能自主运行的AI Agent框架。目前，Conway发布的这款产品仍处于邀测阶段，尚未公开发布。
该公司创始人为
大学肄业、自学成才的00后硅谷AI天才少年Sigil Wen
，他出生于多伦多，17岁刚搬到硅谷就与一众日后知名的AI创始人朝夕相伴了11个月，包括AI大牛Andrej Karpathy，还有Midjourney、Anthropic的联创。他还在2021年就体验了Midjourney、Claude的原型产品。
▲Sigil Wen（图源：TechCrunch）
Sigil Wen此前凭借在Apple Watch跑通GPT-2，发布首个能自我生存、自我进化且无需人类干预即可复制的AI Automaton（自动机）在社交平台X上名声大噪。
那么，这家新秀AI公司靠什么收获硅谷顶尖从业者的押注，其给出的Agent解法又有什么不同？我们试图找到这些问题的答案。
01
.
完全本地运行
能帮你查邮件、生图、处理会议记录
Underdog的核心特点是能完全运行在用户的设备上。这意味着数据只在本地保存，即使在离线状态下也能帮助用户做出决策。
该产品目前已经推出支持Mac、Windows电脑的测试版，未来会有Linux、iOS、安卓版本推出。其可以直接在Mac上运行，并连接用户的邮件和日历，处理如查看电子邮件、日程安排、会议记录、语音输入、在线跑腿、私人iMessage等任务。
从推出至今，Underdog的功能正在陆续更新，包括
本地图像生成和编辑功能、联合Stripe推出的本地智能体支付、一键导入会议记录
等功能。
10月12日，其本地免费的图像生成与编辑功能上线，基于Qwen-Image Flash、Qwen-Image-2.1-Turbo打造。
根据其官方演示，Underdog Images可以根据用户输入的自然语言需求出图，还支持参考图生成，进行局部修改、换背景等。
同一天，Underdog发布其支持一键导入会议记录的功能，并且相关内容不会上传至任何服务器，通话结束后可即时生成摘要、决策事项和行动项。
10月14日，Underdog和Stripe合作，推出了首个设备端智能体支付功能。在本地浏览器中，Underdog能获取对应精确金额的一次性Link卡，并等待用户授权支付。
此外，该公司宣布，还在研究让Agent直接替用户购物等能力，其希望将这类本地AI逐步做成长期掌握个人上下文、直接替用户办事的个人Agent。
02
.
基于Qwen3.8 27B微调模型
专属推理引擎比MLX快4.5倍
根据官方披露，Underdog的性能优势得益于两大关键支撑：更轻量、聪明的模型及专属推理引擎Husky。
先来看模型，Underdog背后的模型有速度更快的Woof 4B、更聪明的Saluki 27B。Saluki 27B已开源。
其中的
Saluki 27B是基于Qwen3.8 27B打造
，官方数据显示，该模型的权重体积是全精度版本的1/7，同时保留96%的性能，在工具调用方面优于Qwen模型。
Sigil Wen在接受外媒TechCrunch采访时透露，该模型能够完成人们期望AI助手完成的日常任务，比如购物调研或解答数学作业题。他称因为成本极低，所以无需收取订阅费来运营Underdog。
第二大支撑是其
为Underdog构建的推理引擎Husky
，这也是支撑该应用能在本地设备跑的关键。
官方数据显示，在MacBook上，启用Husky Flash后，Woof 4B每秒最多可处理730个token，速度比苹果的开源机器学习框架
‌
MLX快
4.5倍
，在相同权重下，响应速度提升
5倍
。
其团队在16类提示词场景下对比了Husky和MLX，结果显示Husky在全部测试中速度都更有优势。
这是因为在执行图像编辑时，Husky每一步并行校验8个token，开销为单个token的1.5倍，而且大部分回复内容已经包含在提示词上下文里；文本生成速度的优势来自流水线调度，在当前步骤执行的同时，就对下一步做编码与提交，让GPU不必空等主机。
Sigil Wen称，与同类设备端引擎相比，该引擎在计算机主芯片与图形芯片之间传输的数据量更少。
除了技术优势，Underdog的早期商业化模式也较为特殊。
Sigil Wen透露，Underdog初期免费，且永远不会投放广告。其中一种收入方式是，他们将从AI助手经由Stripe安全支付基础设施完成的每一笔交易中
抽取少量分成
，模式类似银行卡交换费。这套商业模式下，AI助手无需采集、挖掘用户数据。
这种做法与其他个人AI助手提供商有很大区别，一般企业会允许收集用户数据，然后将这些数据出售给广告商或用来训练其他模型。
03
.
00后大学肄业、自学成才
闯进核心AI大牛朋友圈
虽然未公布具体金额，但Conway Research
‌
的投资人阵容堪称豪华。
除硅谷头部风投a16z、Anthropic与Menlo Ventures组成的投资联合体Anthology之外，还有一众AI领域标杆人物。
包括Stripe联合创始人Patrick Collison、Vercel创始人Guillermo Rauch、有着“AI推理之父”之称的OpenAI研究员Noam Brown、OpenAI知名
研究员Ro
on、Hugging Face联合创始人Thom Wolf，以及谷歌DeepMind高级产品经理Logan Kilpatrick等。
并且在Sigil Wen的评论区，能看到a16z联合创始人、Vercel创始人、Brown等纷纷发来祝贺。
这样的豪华支持，或与其创始人Sigil Wen自身的特殊背景息息相关。
Sigil Wen的个人主页显示，他出生于2003年，是宾夕法尼亚大学管理与技术双学位项目肄业生。
他17岁只身搬到硅谷后，就与当下一众明星AI独角兽的缔造者朝夕相交，并抢先体验了Midjourney、Claude等产品的原型。
他在硅谷创客之家住了11个月，当时和他在公寓同住的包括
OpenAI联合创始人、AI大牛Andrej Karpathy，Midjourney创始人David Holz，Anthropic联合创始人Ben Mann，以及Stable Diffusion、OpenAI、Perplexity等公司的研究人员
。
到2023年之后，Sigil Wen实操的多个AI项目频频刷屏X。
2023年9月，Sigil Wen在
Apple Watch上跑通了GPT-2
，直接在手表上完成文本生成。不过，该模型在生成30个token之后就内存溢出了。之后他还在Airchat公司将OpenAI的语音识别模型Whisper部署到了iPhone上。
Conway Research
‌
的首次亮相就是在今年2月，Sigil Wen称该团队打造出首个能自我生存、自我进化且无需人类干预即可复制的AI
Automaton
。当时他宣告，Web 4.0超级智能生命自此诞生。
Automaton会自主研发并推出产品、交易预测市场、注册域名、在服务器上部署应用和服务、制作病毒式社交媒体内容来推广产品、给供应商发邮件搭建电商渠道、致电企业为其搭建网站。只要还能负担运营成本，Automaton就会一直运作下去。
不过这款产品上线后评价两极分化。一方面它收获了大量关注。产品刚推出时，Sigil Wen就在X平台发文称，Conway Automaton注册智能体数量已经突破1.8万个；时至今日，Automaton的GitHub开源项目累计收获7300星。
另一方面质疑声也不少。以太坊创始人Vitalik Buterin曾公开表态，认为所谓Web4的发展方向存在偏差。在他看来，拉长人类与AI之间的反馈链路，对整个世界而言并非好事。Softswiss首席信息官Denis Romanovskiy当时也提出，AI智能体能否实现真正的经济自主，取决于大模型在成熟度、记忆、规划以及工具调用上的能力；而在这些维度上，现有技术尚不稳定，不足以支撑可靠的无人值守运行。
04
.
结语：性能不及Muse、Dot
个人Agent跑在终端仍处早期探索阶段
这一轮个人智能体竞赛，主流思路仍是搭建云端虚拟机，让AI在厂商的服务器里持续执行任务。但Agent一旦开始高频循环、反复读写个人文件，持续的Token开销与数据上传风险就会凸显，这也让本地离线方案找到了差异化空间。
不过本地设备的算力会限制模型规模与复杂任务表现。Underdog这类产品的探索，试图让Agent的记忆、权限、任务闭环留在本地。虽然目前来看，其产品性能无法超过Muse、Dot等能力，但这也进一步证明了Agent在本地部署的可行性。
来源：Conway Research、X、TechCrunch
