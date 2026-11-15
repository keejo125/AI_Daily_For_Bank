---
publish_time: 1792660115
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/mvQI4D64t0J4UDg8XCBUvA
source: 量子位
title: 4个月RSI从0训练！田渊栋创业首个模型来了：MacBook Pro可跑，已开源
---

# 4个月RSI从0训练！田渊栋创业首个模型来了：MacBook Pro可跑，已开源

来源：量子位
原文链接：https://mp.weixin.qq.com/s/mvQI4D64t0J4UDg8XCBUvA

鹭羽 发自 凹非寺
量子位 | 公众号 QbitAI
40B的MoE“程序员”，MacBook Pro就能带走了！
田渊栋
离职Meta后，强势回归——
携其创业的Recursive，刚刚开源首个模型
Flint
：
主打本地Agent编程，总参数400亿，单个token生成只激活25亿。
而且！速度还比同类产品快
2倍
。
搭配优化后的推理引擎，Flint在MacBook Pro上能跑至少125 tokens/s，RTX Spark上则超过150 tokens/s。
这也是自Recursive成立以来，借助
自动化AI研究系统
，交出的首份模型答卷。
更牛的是，模型从零开始训练，只花费了区区4个月时间。
不得不说，田渊栋他们是真会玩。
这套
「AI手搓AI」
的RSI打法，又被往前推了一大步。
只不过今天这一步，率先落在了开发者的笔记本上。
MacBook Pro能跑
Flint先要解决的，是本地模型一个相当实际的问题：
能装下还不够，还得
跑得够快、干得了活
。
它采用
MoE
混合专家架构，具体到每个MoE层有256个路由专家，每个token选中6个，此外还有一个始终工作的共享专家。
这样总参数够用，每步计算涉及的激活参数也能稳稳控制在25亿上。
以及模型最高支持512k token的上下文窗口，数据可保存在本地上离线使用。
与此同时，Recursive还开源了推理引擎
rec
，专门优化Flint在苹果芯片上的运行。
官方测试中，同一个Flint模型使用rec，相比llama.cpp，在对应上下文长度的token吞吐中能提升约1.4～2.6倍。
它的最终速度要比同等级
（参数量为250亿～400亿）
的稠密模型快5倍，即使是短上下文，也有将近2倍的优势。
其中就包括老东家Meta的
Muse Glimmer
。
编码成绩也很亮眼：
Flint在SWE-bench Verified上得分74.2%，SWE-bench Pro v2为89.7%，Terminal-Bench 2.1为54.9%，都是
同等级最佳
。
毫不夸张的说，Flint在本地编码方面是突破了
帕累托前沿
，推理速度快还代码能力强。
至于怎么跑起来的，Recursive也把配置过程尽量收短。
只需在支持的Mac安装rec后，一条
「rec launch pi」
指令就能自动下载模型、启动服务并连接编程工具，另外OpenCode也有对应入口。
目前rec支持M4 Pro、M5 Pro和M5 Max，要求至少48GB统一内存，以及约30GB空闲磁盘空间。
换言之，对于想把部分日常编程搬到本地的开发者，Flint的确是一个不错的选项。
让AI自己训练自己
回到
Recursive
身上，这家公司五月份才初公开亮相。
一露面，就拿到了6.5亿美元
（折合人民币44亿元）
的早期融资，估值高达46.5亿美元
（约316亿元）
。
谷歌GV、Greycroft联合领投，英伟达、AMD等巨头也参与其中。
一则押的是人。
八位联创
个个来头不小，除了田渊栋，还有吴恩达弟子Richard Socher、清华姚班施天麟、Vision Transformer的作者之一Alexey Dosovitskiy等。
二来押的是路线。
Recursive从创立之初，就明确研究路线为
RSI
，即递归式自我改进。
背后的逻辑也很直接：AI本身由代码构成，而AI现在已经能写代码，那么它能否再进一步参与改进AI？
Eureka Machine
就是Recursive对这个问题的初步尝试。
该系统会先针对目标提出想法，再把想法实现，通过运行实验、检查结果，决定下一步。多条研究路线可以同时推进，之前有效的经验也能被保留组合。
此前Recursive公开的第一批实验成果，就来源于此。
落在NanoChat Autoresearch、NanoGPT Speedrun和英伟达SOL-ExecBench上，分别拿下了整体和各单项测试的
SOTA
。
这三个基准测试也依次对应训练质量、训练速度和GPU内核效率。
到了Flint，问题变得更大。
团队把这些不同环节的改进，组合在一起，构成了一个最终能交付的模型。
这也解释了为什么Recursive要把
首款模型
选在本地编程这个方向，因为本地代码任务容易收获反馈，自动化研究找到的收益，也更容易被逐项检查。
显然，进展不错。
所以对于田渊栋和Recursive来说，下一步就很明确了——
这套自动化AI研究系统，能否让
下一款模型
用更少的研发成本，交出更好的实际能力。
咱们且拭目以待。
参考链接：
[1]https://x.com/RichardSocher/status/2112944385415426249
[2]https://recursive.com/updates/introducing-recursive-flint
[3]https://x.com/NVIDIARTXSpark/status/2112963691469787433
[4]https://x.com/tydsh/status/2112952791480357331
[5]https://docs.recursive.com/edge/rec
一键三连
「点赞」「转发」「小心心」
欢迎在评论区留下你的想法！
—
完
—
🌟 点亮星标 🌟
科技前沿进展每日见
