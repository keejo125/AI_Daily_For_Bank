---
publish_time: 1791294698
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/AdqzqJmluYJ5LMlgfRXXsQ
source: 赛博禅心
title: Mistral Large 4 发布：1T 参数、49B 激活，aka「大胖猫」
---

# Mistral Large 4 发布：1T 参数、49B 激活，aka「大胖猫」

来源：赛博禅心
原文链接：https://mp.weixin.qq.com/s/AdqzqJmluYJ5LMlgfRXXsQ

今天早些时候，
美国那边开源了个 glm5.2 级别的模型
而刚刚，欧洲的希望  Mistral 发布了 Mistral Large 4，aka Le Chonk 大胖猫
Mistral 官方推文
总参数
1.05T
，每次只激活
49B
，另带一个 1.6B 的视觉编码器
它用的是细粒度的混合专家（MoE）结构：模型拆成很多个“专家”，每处理一个词只叫醒其中一小部分。所以 1T 的模型，每算一个词的开销接近一个 49B 的模型
原生多模态：能读文字和图片，输出文字；上下文 1M
从零训练，用了两个月、
4000
张英伟达 Grace Blackwell，全在 Mistral 自己的欧洲机房里。上一代 Large 3 是 675B 总参数、41B 激活，用 3000 张 H200 训出来
官方说，按综合跑分，它是美国和欧洲最强的开源权重模型
Chonk 在网络俚语里指圆滚滚的胖猫。今年 6 月，网友虚构过一个叫 Le Chaton Fat 的“肥猫模型”
现在， Mistral 端出了真正的 1T 胖猫，今天起 API 可用，权重 10 月 27 日放出
写代码、对账、审合同
DeepSWE 让模型做真实的长链条软件工程任务，Large 4 预览版拿到 62%
DeepSWE v1.1，官方预览成绩
同一张图里，智谱 GLM-5.3 是 61%，DeepSeek-V4-Pro 57%，Qwen 3.8 Max 51%，Reflection 前一天刚发的 Beam 44%
Finch（FinWorkBench）考的是企业财务流程：在乱糟糟的表格、文档里查数、建模、出报告。Large 4 拿到 67%，和 DeepSeek-V4-Pro 打平，GLM-5.3 是 65%
左边两根橙色柱子都是 Mistral 自家
自家上一代的 Medium 3.5 则只有 37%，翻了个倍差
对于 Harvey 的法律 Agent 测试，也就是让 Agent 独立完成整件法律工作，按任务通过率算。Large 4 是 15%，Kimi K3 13%，GPT-6 Astra 5%
法律题，全场都没及格
这些都是预览版成绩。官方说，强化学习还在跑，提升还没见顶，权重放出前分数还会变
看图找东西
视觉定位（grounding）则是让模型在图里的某个东西框出来。DIOR-RSVG 用的是遥感航拍图，Large 4 拿到 73%，GPT-6 Astra 68%；Dense200 两者都是 42%
左：Dense200；右：DIOR-RSVG 遥感图
官方说，在视觉定位上，它超过了闭源的前沿模型
；对 Anthropic 的 Fable 5.1 也说赢了，不过没给出这组数字
Mistral 举的用法：保险公司看航拍图评估风暴损失，电力公司巡检输电线，农场盯庄稼长势。它还能把技术图纸转成 CAD 模型，官方说它在半导体相关测试上成绩也靠前，芯片设计也在官方列的场景里
为什么要放权重
据 CNBC，今年早些时候，Hugging Face 遭到失控的 OpenAI Agent 入侵，先找美国的闭源模型帮忙防守，结果护栏把它的操作当成了攻击，拦了下来，最后用的是智谱的 GLM 5.2
官方推文列的重点场景里，网络防御排在第一个。联合创始人兼首席科学家 Guillaume Lample 说：“网络防御能力能让企业和政府，去防住那些越狱闭源模型来发动攻击的人”
Mistral 的理由是：安全团队每天都要扫自家系统找新漏洞，量很大；闭源模型的安全策略，可能把正当的防御请求也拒掉。权重下载到自己机器上，扫多少、怎么扫，不用再问谁
这三周预览期里，开发者、网安公司和政府机构拿到的是一个限制更少、网安功能更多的版本，公开 API 上没有。官方还说，它在网安任务上超过 Kimi、DeepSeek 和 Meta 最好的开源模型，这组数字也还没公布
Mistral 还说，客户要两样保证：不会被哪个外国政府断供，模型怎么训出来的有据可查。可以部署在自家服务器上，也可以调 Mistral 的 API 并选部署区域，包括受欧盟法律保护的欧洲区；训练语言超过 160 种，覆盖欧盟全部官方语言
Lample 对 VentureBeat 说，客户要的早就不止模型本身，部署、基础设施、定制、围着越来越复杂的 AI 流程做工程支持，都是生意。Mistral 现在服务 125 家以上的大企业，包括空客、ASML 和汇丰，其中一些客户用 Mistral 卖的 Forge 平台参与了 Large 4 的训练
9 月，Mistral 刚完成
30 亿欧元
的 D 轮，投后估值超过 210 亿欧元，自称欧洲科技公司史上最大的一笔股权融资。Large 4 是这笔钱之后的第一个模型，新买的算力 2027 年上半年陆续到位
9 月 D 轮的官宣动图，截了一帧
怎么用、多少钱
模型名
mistral-large-4
，在 Mistral Studio 和 API 上已经能调，文档标的是公开预览版
文档右上角，趴着一只像素猫
每百万 token：输入 0.68 美元，缓存输入 0.07 美元，输出 2.09 美元。文档上，原价 1.36、0.14、4.18 都被划掉了，现价是一半
权重 10 月 27 日放出，预计用 Mistral 自定的许可证。在那之前，官方会陆续公布架构细节、更多跑分、后训练方法和安全测试
之后，Large 4 会成为一整个系列专用模型的底座
一点背景：大胖猫
首先，这个和国内的胖猫没啥关系
今年 6 月，一个根本不存在的 Mistral 模型 Le Chaton Fat（法语，肥猫咪）在 X 和 Reddit 上火了：有假跑分图，有越编越离谱的规格，有的版本号称 30 万亿参数，有的宣传“每秒 1000 声喵”
Mistral CEO Arthur Mensch 也下场了，在 X 上纠正：“其实是 le gros chaton（大猫咪）”。投资人 Marc Andreessen 也跟着转发了这个梗
发布前一天晚上，Mensch 发了 2014 年欧洲田径锦标赛女子 4×400 米接力决赛的视频：法国队最后一棒 Floria Gueï 进最后直道时还排第四，连超三人，拿了金牌
发布前一晚，Mensch 只发了一个词
评论区里，有人催他一定要让市场部把 Large 4 叫 Le Chaton Fat，不然就是“史上最大的失误”。Hugging Face CEO Clément Delangue 回了一句：“那也许吧！”
官方推文下，大家只关心体重
Lample 接受 VentureBeat 采访时说，团队很喜欢这个梗，Large 4 可以算这个想法的第一版，后面还会有更大的模型
