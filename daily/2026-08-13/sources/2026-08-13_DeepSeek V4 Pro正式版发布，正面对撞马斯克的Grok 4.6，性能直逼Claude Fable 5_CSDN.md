---
publish_time: 1786600209
status: pending
category: 
is_model_related: true
digest: |
link: https://mp.weixin.qq.com/s/NhDraVIppustqs4FIUdWhQ
source: CSDN
title: DeepSeek V4 Pro正式版发布，正面对撞马斯克的Grok 4.6，性能直逼Claude Fable 5
---

# DeepSeek V4 Pro正式版发布，正面对撞马斯克的Grok 4.6，性能直逼Claude Fable 5

来源：CSDN
原文链接：https://mp.weixin.qq.com/s/NhDraVIppustqs4FIUdWhQ

整理 | 屠敏
出品 | CSDN（ID：CSDNnews）
DeepSeek 又在深夜“放大招”了。
8 月 12 日深夜，DeepSeek 悄无声息地把此前一直处于预览状态的 V4 Pro 更新成了正式版，模型版本号变为 DeepSeek-V4-Pro-0813。
没有发布博客文章，也没有一条正式的社交媒体公告。
最先让外界发现 Deepseek 有更新动作的是在 DeepSeek API 的模型与价格页面上：原本的 deepseek-v4-pro 对应的型号版本被悄悄替换成了 DeepSeek-V4-Pro-0813。
目前，通过 OpenRouter 已经可以直接查看这
一版本
（
https://openrouter.ai/deepseek/deepseek-v4-pro-0813
）
，页面显示该模型支持 100 万 Token 上下文，输入价格为每百万 Token 0.435 美元，输出价格为 0.87 美元。
更有意思的是，DeepSeek 这次更新并没有提高价格，但这可能只是暂时的。
因为就在几天前，DeepSeek 已经在用户后台发布公告，宣布计划于近期整体上调 Deepseek API 服务的定价，预计涨幅较大，让用户合理安排自身的使用。不过，截至目前，
新的具体价格和生效时间尚未公布。
当然价格只是一方面，真正让外界兴奋的，是 V4 Pro 0813 的性能。
从“预览版”到正式版，V4 Pro 到底升级了多少？
DeepSeek V4 Pro 最初是在今年 4 月 24 日以预览版身份发布的。
当时，DeepSeek 给 V4 Pro 配备了 1.6 万亿总参数、490 亿激活参数，并首次将 100 万 Token 上下文作为 V4 系列的标准配置。
DeepSeek 当时就把 V4 Pro 的定位放得非常高：强调其 Agent、世界知识、代码和推理能力，目标是与全球顶级闭源模型竞争。
但问题在于，此前外界测到的各种成绩，其实都是 V4 Pro Preview 的成绩。这意味着，过去几个月大家拿来和 Claude、GPT 等模型比较的，很可能还是一个“半成品”。
如今正式版终于来了，DeepSeek 自己给出的对比数据，也开始变得相当有意思。
从 Deepseek 官方群发布的覆盖 10 项智能体基准测试的横向对比结果来看，在 Claude Fable 5 或其他模型占优的 8 项测试里，
DeepSeek-V4-Pro-0813 与之相比
性能差距都十分微小。
综合所有测试，Fable 5 平均领先幅度为 5.3%。如果剔除「无工具版人类终极考试」这一极端样本（DeepSeek 得分 42.7，Fable 5 为 53.3，存在 10.6% 的差距，大幅拉高整体差值），剩余项目平均差距仅 2.8%。
更值得关注的，是在
专门考察 AI 编程 Agent 长周期软件工程能力的基准测试
DeepSWE 中，
DeepSeek-V4-Pro 正式版的表现有了很大的跃升，其得分从预览版的 12.8 直接提升至 62.7，暴涨近 5 倍。
与传统代码生成测试不同，这一基准测试要求模型真正进入一个复杂的开源代码仓库，自主理解代码、修改多个文件、运行测试并不断修正，最终完成一个完整的软件工程任务。
这个变化反映的并不只是模型“写代码更快了”，而是它处理复杂软件工程任务、连续调用工具并自主完成多轮修改的能力出现了明显提升。
此外，
在聚焦 AI 网络安全攻防能力的 CyberGym 和面向 AI Agent 自动化能力的 AutomationBench（Public）两项基准测试中，
DeepSeek-V4-Pro-0813
反超 Fable 5。
价格
如果性能只是接近，那么价格可能才是 V4 Pro 0813 最值得关注的地方。
正如上文所述，目前 DeepSeek API 给 V4 Pro 的价格是：
输入：0.435 美元 / 百万 Token
输出：0.87 美元 / 百万 Token
缓存命中输入甚至只有 0.003625 美元 / 百万 Token。
相较之下，Anthropic Fable 5 输入每百万 token 10 美元，输出 50 美元。
综合折算均价：
Fable 5 约 30 美元，V4 Pro 约 0.65 美元，前者成本大约是后者 46 倍。
对于规模化使用 AI 工具的企业而言，这样的成本差距至关重要。
此外，据外媒 The Decrypt 分析，由于 Fable 5 推理耗时更长、生成文本更多，因此其
完成单次任务的实际成本差距更大
。据
Artificial Analysis 早期时候
测算，基准测试中单任务成本 Fable 5 达到 3.15 美元，而 V4-Flash 仅 3 美分，价差约 105 倍。Hugging Face CEO Clem 估算，
测试的各型号每项任务的成本差异高达 800 倍：Claude Fable 5 在基准测试中领先，但平均每项任务的成本超过 31 美元，而 DeepSeek V4 Flash (max) 的成本仅为 0.04 美元。
不过目前还没有 0813 新版 V4 Pro 的单任务成本数据。
整体而言，拥有能够逼近最顶级的闭源模型的性能，同时把成本压到后者的零头，
开源的 Deepseek 优势不言而喻。
马斯克的 Grok 4.6 同期发布
值得一提的，也就是在今天，马斯克为自家新模型站台，官宣 Grok 4.6 发布，并称其为“智能、快速且性价比极高的产品。”
Grok 4.6 同样将重点放在了 AI Agent 和复杂任务上。根据 SpaceXAI 最新收购的 Cursor 官方介绍，新模型基于 Grok 4.5 打造，重点强化了长时间运行的 Agent，以及更复杂的交互和视觉任务，能够处理研究、信息分析、跨代码库开发等需要多步骤完成的工作。
在性能方面，Cursor 表示，Grok 4.6 在多项 Agent 编程和知识工作基准测试中达到前沿水平，在 Artificial Analysis Intelligence Index 上与 GPT-5.6 Sol 持平。与此同时，Grok 4.6 已经登陆 Cursor、Grok Build，并可通过 API 以及 OpenRouter、Vercel、Cloudflare 等平台调用，价格为每百万输入 Token 2 美元、每百万输出 Token 6 美元。
这也让 DeepSeek V4 Pro 和 Grok 4.6 的“同日登场”显得颇有意思：一个把价格压到了极低水平，一个则试图用更强的 Agent 能力冲击前沿模型。
开发者已经开始“实测”了
让人颇为关注的是，随后有开发者也开始把这两个模型直接放在一起进行实际编程测试。
在 HN 讨论区，一位名为
jklmnopqrstuvw 的网友
直接把 V4 Pro 0813 和 Grok 4.6 放进 Codex CLI，对同一个新功能进行开发测试。
结果是：
V4 Pro 0813 花了 12 分 02 秒，成本 0.12 美元，但出现 Bug；
Grok 4.6 花了 3 分 18 秒，成本 1.41 美元，没有出现 Bug。
这个结果其实比“某个 Benchmark 超过了多少”更有意思。因为它恰恰说明，真实的软件开发中，模型能力并不是一个简单的分数。
当然，也有人提醒，不应该拿一次实验就给模型下结论。毕竟 Agent 本身具有很强的随机性，一次成功或者失败，并不能代表模型的整体水平。
而面对
DeepSeek-V4-Pro-0813 的到来，
独立 AI 分析师、前 Hugging Face  研究员
Tiezhen Wang 发帖
直言：
你可能还没有意识到这意味着什么。
如果这是真的，而且 DS-V4-Pro 还是开源模型，那 Opus 甚至 Fable 都要“GG”了 😅。
这意味着，得益于 DeepSeek V4 极小的稀疏 KV Cache，DeepSeek 有能力以只有 Fable API 价格 1/50 的成本，提供与 Fable 同级别的模型，同时还能获得远高于 Anthropic 的缓存命中率。
最终的总成本甚至可能低 100 倍，而模型能力基本处于同一水平。
这对存储行业来说是个利好，因为 SSD KV Cache 可能会成为标准配置。对整个 AI 行业也是好消息——AI 变得更加便宜，意味着会有更多人开始使用 AI，而这又会进一步加快需求增长。
现在我是真的想问一句：
接下来会发生什么？
我们准备好迎接一个 Fable 开源后的世界了吗？
回看从 2025 年的 R1 到今年的 V4，其实 DeepSeek 一直在做一件很类似的事情：不是简单追求“我要做一个比所有模型都强的 AI”，而是不断把前沿模型的能力往更低的成本区间里压。
V4 Pro 0813 的意义，可能也不只是“又一个国产大模型发布”。
如果 DeepSeek 自己公布的测试结果最终能够得到第三方验证，那么这一次真正值得关注的，将是一个越来越明显的变化：顶级闭源模型与高性价比开源模型之间的性能差距，可能正在进一步缩小。
参考：
https://openrouter.ai/deepseek/deepseek-v4-pro-0813
https://x.com/Xianbao_QIAN
https://news.ycombinator.com/item?id=49274600
https://decrypt.co/375507/china-deepseek-upgrades-v4-pro-claude-fable
“写代码从来都不是难点”？25年开发者怒写3000字反驳：这句话是对所有程序员的一种侮辱！
每周 120 万个 App 诞生，每位开发者都是智能体管理者
——
Google 在上海画出了一张全栈 AI 出海路线图
openJiuwen协同昇腾打造智能体「算力亲和」技术，首 token 时延砍半，推理存储占用下降25%
11.20-21 日，2026 奇点智能大会·北京站。
OpenAI 资深研究科学家 Łukasz Kaiser 确认进行主题分享。
他是 Transformer 八子中唯一还在科研前线的人，GPT-4/5、o1、o3、ChatGPT 的核心开发者。
2021 年，他在这个大会上分享了三个方向：多模态、更大更好的 Transformer、模型即服务。五年后，多模态爆发，ChatGPT 席卷全球，前沿观点全部成了现实。
去年，他讲的是推理模型的进化：从"记忆"到"策略"再到"研究器"——模型开始学会自己思考。
欢迎大家扫码领取 Łukasz Kaiser 历年在奇点智能大会上的分享 PPT 和视频
