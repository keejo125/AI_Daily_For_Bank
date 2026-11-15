---
publish_time: 1794348600
link: https://mp.weixin.qq.com/s/9b1_lBtr62ZaQUurGKl5DA
source: 量子位
status: confirmed
category: 国际
is_model_related: true
digest: |
  谷歌 Gemini 4 Carbon 正式 API 上线并向 Ultra 用户开放，在 CursorBench 4.0、WANDR、AutomationBench 均排名第一，单任务成本比 Fable 5.2 低 50% 以上，并展现 3D 重建与网络安全能力。
title: Gemini 4 Carbon连夜上桌！力压Fable 5.2花费仅一半，还挖出了PHP同级漏洞…
---

# Gemini 4 Carbon连夜上桌！力压Fable 5.2花费仅一半，还挖出了PHP同级漏洞…

来源：量子位
原文链接：https://mp.weixin.qq.com/s/9b1_lBtr62ZaQUurGKl5DA

鱼羊 发自 凹非寺
量子位 | 公众号 QbitAI
A社Fable 5.2一发，谷歌Gemini 4 Carbon终于是憋不住了。
刚刚，谷歌这个誓要重回牌桌，拳打Claude Opus 5.5、脚踩GPT-6 Astra的大饼总算是
API上线
了，同时，
面向Ultra订阅用户开放
。
嗯，100刀一个月那个Ultra。
emmm…但至少，这回可以眼见为实了，咱先来看效果：
谷歌用Carbon分析了阿波罗登月舱的图片资料和技术图纸，然后，Carbon就自己个儿重建了3D模型，并制作了这么一个视频。
此番正式上线，谷歌也更新了一波Gemini 4 Carbon的测试成绩。
在CursorBench 4.0、Perplexity的WANDR和Zapier的AutomationBench中，Carbon均排名第一，
并且每项任务成本都比排名第二的模型低50%以上
——
说的就是你，Fable 5.2。
此外，Gemini推特带盐人Logan也没忘又暗示了一把RSI：
Argon发布仅仅几周，Carbon就根据Argon的诸多反馈取得了显著进展，并在网络安全、知识和代码领域开辟了新天地！
行行行，你们御三家就这么卷吧，让我们看看2026年最后不到两个月，「新天地」还能被重新定义几次。
首批实测
什么编码推理能力提升、网络安全性能突破、3D/UI设计改进，谷歌都已经早早剧透，详情戳
这里
，就不多赘述了。
模型正式上线，我们还是从官方和非官方实测中，见见真章。
最近模拟人类发声结构的语音合成器Chimera不是挺火嘛，谷歌直接用Carbon搞了个鸟声模拟器。
从研究这套结构到编程实现交互式3D模拟，实时合成6种鸟类的声音，都由Carbon一手包办。
再来看最近流行的新测试基准：游戏。
△
作者：X@kimmonismus
Po出这一实测的博主Chubby说，Carbon打造的这个弹珠游戏具有真实的物理特性，不过在照明效果和启动状态上，还有需要进一步调教完善的地方。
Carbon还可以用3js重建真实的视频片段。
△
作者：X@emollick
给产品拍宣传图的任务也完成得挺惊艳
（调用了nano banana）
。
谷歌还披露，Carbon近期刚刚发现了某热门开源软件中的两个超级漏洞，其严重程度跟PHP那个不相上下。。。谷歌没具体说是什么漏洞，不过补丁已发，公告也会在完成合规披露流程后发出。
一条指令叫来一队Agent
还有个有意思的。
跟模型一起亮相的，还有Google Antigravity里的一项新功能 /swarm。
简单来说，该功能可以一条指令叫来一队Agent给你打工，还能实时看到它们干到了哪一步。
功能的核心，是让Carbon担当架构师，负责架构设计、协调和审查需要深度推理的活，同时让速度更快的轻量模型在各自的工作区里并行执行，验证Agent则专门检查每一项改动。
用起来是酱婶的：
投喂7份市政规划PDF，输入一条提示词，Carbon团队就把谷歌自家办公楼搬进了浏览器。
Agent团队在夜间跑了10轮迭代，最终交付了一个约
90.6万个三角面
的交互式Three.js模型。
比Argon更费Token
价格方面，Carbon首发阶段有半价折扣，
输入2美元/百万Token、输出10美元/百万Token
，优惠期截止至11月30日。
开发者可以通过Gemini API接入，企业用户可通过Gemini for business、Antigravity或CodeMender使用，Ultra会员可在Gemini App、搜索AI Mode和Antigravity使用。
哦对了，嫌Argon烧Token烧得猛的朋友们注意了，Carbon更是一头吞Token巨兽。。。
官方明确说明，Carbon会消耗更多推理Token，来探索不同路径、延长验证循环，以应对复杂多步编程、调试和开放式科研。
如果是面向日常工作，谷歌还是建议把Argon当成主力模型。
这个取舍，在第三方评测里已经能看到。
Zapier的AutomationBench考的是Agent能否在多个办公应用之间把一件事从头做到尾。Carbon高推理档拿到
53.88%
，排在榜首。Claude Fable 5.2 Max
（启用默认回退）
是51.45%，Argon高档是51.29%。按榜单的标准标价口径，三者平均每道任务分别花
2.12美元、4.64美元和1.70美元
。
大致的情况就是这样了。谷歌紧赶着Fable 5.2端上的这盘热饼，诸位觉得味道还行不？
但反正只给Ultra用户开放这事儿吧……
已经被喷上了。
参考链接：
[1]https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/
[2]https://x.com/koraykv/status/2120186714358702187
一键三连
「点赞」「转发」「小心心」
欢迎在评论区留下你的想法！
—
完
—
🌟 点亮星标 🌟
科技前沿进展每日见
