---
publish_time: 1788146674
link: https://www.qbitai.com/2026/08/481759.html
source: 量子位
status: confirmed
category: 国际
is_model_related: true
digest: |
  量子位援引 Information 消息，OpenAI 已采购数万台 Mac mini 与 Mac Studio 专用于强化学习，训练能自主操作电脑的 computer-use agent；Anthropic 亦通过 AWS 租用 Mac mini 做类似任务。Mac 在 RL 场景被大规模采购靠统一内存架构（CPU/GPU 共享池）与专门散热，避免英伟达 GPU 显存与系统内存分离的数据传输瓶颈，带动 Mac 营收同比增近29%。
---

# OpenAI买几万台Mac搞强化训练！英伟达的活被苹果抢了

> 原文链接：https://www.qbitai.com/2026/08/481759.html
> 来源：量子位

OpenAI买几万台Mac搞强化训练！英伟达的活被苹果抢了
梦晨
量子位
什么样的AI业务，英伟达GPU和谷歌TPU搞不定，非得用Mac
梦晨 发自 凹非寺
量子位 | 公众号 QbitAI
OpenAI被曝疯狂扫货Mac，
一买就是几万台
。
一不小心给买断货了，还要想尽办法搞到更多。
Macbook笔记本不要，专买没有屏幕、没有键盘的
Mac mini和Mac Studio
。
那么问题来了：什么样的AI业务，英伟达GPU和谷歌TPU搞不定，非得用Mac？
几万台Mac搞强化学习，A\也干了
据Information消息，OpenAI已经购买了数以万计的Mac mini和Mac Studio，专门用于强化学习。
不只是OpenAI，
Anthropic也在通过亚马逊云服务AWS租用Mac mini
来做类似的任务。
这些Mac被用来训练”计算机使用智能体”（computer-use agent），也就是能自主操作电脑、完成编辑测试代码、自动整理邮箱、总结文档等多步骤任务的AI系统。
这股热潮直接反映在了苹果财报上。
最近一个季度，
Mac销售额同比增长近29%，达到103亿美元，增速超过了iPhone、iPad等苹果旗下所有其他产品线，Mac成了苹果增长最快的业务
。
6月23日，苹果总部Apple Park举办了一场名为”Business at the Park”的活动。这在苹果历史上并不常见，苹果向来专注消费者市场，极少专门面向企业客户办活动。
这场活动迪士尼和福特的高管到了，Anthropic联合创始人Jared Kaplan也到了，苹果即将卸任的CEO Tim Cook和即将接任的John Ternus都在。
据一位参会者透露，
苹果在活动上反复强调其硬件非常适合在本地处理AI任务，Mac mini是整场活动的焦点
。
AI训练长期以来由英伟达GPU主导，但Mac能在强化学习这个细分场景中被大规模采购，靠的是统一内存。
英伟达GPU的显存和系统内存是分开的，数据在两者之间传输会产生瓶颈。苹果M系列芯片则采用单一共享内存池，CPU和GPU直接访问同一块内存，在处理AI工作负载时具备性能优势。
另外，与轻薄的MacBook不同，Mac mini和Mac Studio配备了专门的散热系统，长时间运行复杂AI任务不会因为过热而降频。这对需要持续数小时甚至数天的强化学习训练来说至关重要。
苹果还在推广EXO Labs开源软件项目，可以将多台Mac组成集群，在本地运行万亿参数级别的AI模型。
苹果刚刚发布的新款Mac Studio也特别强调了集群能力，多台Mac Studio可以串联组成更强大的系统来运行前沿模型。
这次新品发布的时间也不寻常。苹果通常在每年10月或11月进行年末更新Mac产品线，这次提前到了8月。
英伟达盯上了，苹果仓促应对
Mac在本地AI领域的崛起已经引起了英伟达的注意。
据一位与英伟达高管讨论过竞争形势的知情人士透露，英伟达将苹果视为本地AI领域最大的竞争对手。
去年底，英伟达发布了DGX Spark，一款与Mac mini设计风格相似的AI桌面电脑，直接瞄准这个市场。
苹果这边面临供应跟不上的现实问题。
AI数据中心对内存芯片的巨大需求导致了历史性的全行业短缺，苹果也未能幸免。
对AI开发者最有吸引力的高配版Mac mini和Mac Studio已经断货数月。
苹果前AI产品企业营销经理Todd Dailey透露，过去一年由于Mac供应受限，一些企业已经开始寻找替代方案，英伟达DGX Spark是被频繁提及的选项，而且现在有现货。
Dailey今年4月从苹果离职，目前是独立AI顾问。他还透露Mac在企业AI市场的火爆完全是意外，而非苹果的主动规划。苹果没有专门面向企业客户的工程团队，也没有任何专注于开发者关系的员工。
苹果上一次出售服务器产品还是2011年就停产的Xserve。基于Mac的服务器操作系统也已于2022年停止开发。
不过已经有人嗅到了机会。
前OpenAI计算基础设施员工Peter Voell创办了Mount Thor，一家基于苹果硬件的云计算公司，目前仍处于隐身模式，官网将产品描述为“基于苹果硬件的AI执行环境”。
苹果也在寄希望于Mount Thor和webAI这样的合作伙伴，把Mac推进更深的企业市场。
苹果最近终于开始使用Mac芯片构建自己的服务器。不过，这些服务器仅供内部使用，用于私有云计算（Private Cloud Compute）服务，处理超出iPhone或Mac处理能力的AI任务。
一些企业客户曾询问苹果是否可以出售这些服务器的使用权，但苹果目前为止都拒绝了。
参考链接：
[1]
https://www.theinformation.com/articles/apple-stumbled-ai-hardware-success-mac
[2]
https://www.apple.com/newsroom/2026/07/apple-reports-third-quarter-results/
版权所有，未经授权不得以任何形式转载及使用，违者必究。
OpenAI
梦晨
不是Demo！优必选把客户产线1:1搬进WRC，解锁具身智能真落地路径
写2000字提示词，不如先生成3D白模！AI视频创作进入“预演时代”
Eon用LIF“上传”果蝇脑，中国团队直接上精细神经元和跨身体平台
今日起，阿里“千问办公”接入企业微信
扫码分享至朋友圈
相关阅读
苹果Mac用户狂喜！ChatGPT深度集成应用，最后再藏AGI彩蛋
VSCode、Notion等第一波上桌
一水
OpenAI
o1完整思维链成OpenAI头号禁忌！问多了等着封号吧
o1并非GPT-5，奥特曼暗示下一代“猎户座”在路上
克雷西
ChatGPT
OpenAI
突发！OpenAI开除Ilya盟友，理由：涉嫌信息泄漏
神秘Q*再次引发热议
西风
OpenAI
开除员工
ChatGPT支持个人定制！告别大段提示词，只需先和它做好自我介绍
自定义指令功能上线
明敏
ChatGPT
OpenAI
月入过万只需用ChatGPT建个网站？AI创业博主在线教学
不仅不用投广告，就连更新都免了
十三
ChatGPT
OpenAI
人工智能
奥特曼的ChatGPT育儿大法，捅了马蜂窝
这就有些尴尬了。
Jay
OpenAI