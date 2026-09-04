---
publish_time: 1788488202
link: https://www.infoq.cn/article/M792kCZ4FIzk7YHe4WhT
source: InfoQ
status: confirmed
category: 国际
is_model_related: true
digest: |
  InfoQ 报道，Gemini 近期在中文互联网被戏称为"美国大豆包"，但新版本在输出速度上碾压同类、智能水平重回第一梯队。文章分析 Gemini 在工程优化（如推理提速）与多模态能力上的改进，认为其凭借性价比与速度重新获得开发者青睐。
---

# “美国大豆包”Gemini翻身：输出速度碾压同行、智能水平重回第一梯队

> 原文链接：https://www.infoq.cn/article/M792kCZ4FIzk7YHe4WhT
> 来源：InfoQ

过去几个月，Gemini 在中文互联网上多了一个颇具杀伤力的外号：“美国大豆包”。

这个称呼吐槽的，是 Gemini 身上长期存在的反差：发布会上基准成绩漂亮、上下文窗口巨大、免费额度充足，真正用起来却偶尔理解跑偏，一本正经地给出错误答案。被用户指出问题后，它还可能先送上一大段夸奖和道歉，情绪价值给得很足，事情却没有办好。

在 Gemini 3.5 Flash 发布后，这种调侃一度升级为：“这是最快告诉你错误答案的 AI。”

如今，Google 带着 Gemini 3.8 Flash 回来了。这是其六周内推出的第三款 Flash，也是不到四个月内的第四次 Flash 更新。新模型在 Artificial Analysis Intelligence Index 上获得 59 分，与 xhigh 档位下的 GPT-5.6 Sol 和 medium 档位下的 Grok 4.6 持平；在 DeepSWE v1.1 上，它甚至超过大多数体量更大的前沿模型，登上长程软件工程榜首。

更关键的是，Gemini 3.8 Flash 仍能保持每秒约 300 Token 的输出速度，约为许多主流模型的4—6倍。

“美国大豆包”这次似乎真的变聪明了。Google没有直接把Flash做成一款缩小版Pro，而是让模型思考更多、反复调用工具、执行更多轮次，并为此消耗更多Token。

一款模型可以拥有极高的Token输出速度，每项评测任务的加权生成时间却比上一代更长。理解这组看似矛盾的数据，才是理解 Gemini 3.8 Flash 的关键。

Flash冲进第一梯队

自 2026 年初以来，Google 一直没有发布前沿级别的 Gemini Pro 模型。

原本承诺在今年 6 月推出的 Gemini 3.5 Pro 至今没有出现，据称原因之一是它的编程能力未能达到 Google 的预期。8 月初，Google DeepMind 的管理层也发生变化。Demis Hassabis 卸任 CEO、转任董事长，Koray Kavukcuoglu 接过管理工作，职衔则变成了高级副总裁。Google CEO Sundar Pichai 随后试图安抚外界，但这并没有完全消除市场的疑虑：Google 是否还准备继续争夺前沿模型的最高位置？

与此同时，Flash 系列进入了高速迭代。Gemini 3.5 Flash、3.6 Flash、3.7 Flash 和如今的 3.8 Flash 接连发布，Google 更新低价模型的速度，已经超过其他实验室迭代同类产品的速度。

Flash 原本是 Google 模型家族里的经济型产品线，主打低成本和高速度，能力通常低于 Pro 系列。到了 Gemini 3.8 Flash，这条边界已经开始模糊。

开启高推理档位后，Gemini 3.8 Flash 在 Artificial Analysis Intelligence Index 上获得 59 分，比上一代提高3分。它与 xhigh 档位下的 GPT-5.6 Sol、medium 档位下的 Grok 4.6 持平，距离最高档位下的 GLM-5.3 和 Kimi K3 只有1分，距离最高档位下的 GPT-5.6 Sol 和高档位下的 Grok 4.6 也只有2分。

再往上，Claude Opus 5 获得63分，Claude Fable 5.1以66分位居榜首。Gemini 3.8 Flash没有拿下绝对最高分，却已经进入当前第一梯队。

Google 暂时没有依靠 Pro 重返模型能力的最前沿，却让 Flash 回到了帕累托前沿：在当前市场上，很难找到一款智能水平比它更高、成本又比它更低的模型。

Token单价没涨，完成任务却贵了40%

今年年底前，Gemini 3.8 Flash 将沿用上一代的 API 推广价格：每百万输入 Token 0.75美元，每百万输出 Token 3.75美元，缓存输入则按正常输入价格的10%计费。优惠期结束后，价格将翻倍，恢复至每百万输入 Token 1.50美元、每百万输出 Token 7.50美元。

按照Artificial Analysis的测算，高推理档位下的Gemini 3.8 Flash完成一项Intelligence Index评测任务，平均成本为0.58美元，是该机构测得的同等智能水平中最便宜的模型。

作为对比，Anthropic最新的通用旗舰模型Claude Fable 5.1完成同类任务约需3.76美元，成本是Gemini 3.8 Flash的6倍以上。最高推理档位下的GPT-5.6 Terra，单任务成本为0.53美元，与Gemini 3.8 Flash接近，但智能水平得分为57分，比后者低2分。

Gemini 3.8 Flash的Token单价没有上涨，单任务成本却比Gemini 3.7 Flash高出约40%，从0.40美元增至0.58美元。在Artificial Analysis的Intelligence Index评测中，新模型每项任务的加权平均输出Token增长30%，达到约4.8万个，同时在智能体评测中执行了更多轮次。

Google将这种变化形容为“3.8 Flash works harder”。面对复杂任务时，它会增加推理步骤、反复调用工具，并可能在较高推理档位下消耗更多Token，以换取更好的最终结果。

它消化这些额外计算的关键，正是速度。Artificial Analysis测得，Gemini 3.8 Flash在高推理档位下平均每秒输出约305个Token，是榜单第二名 Meta Muse Spark 1.2 的两倍左右，后者为每秒 154 个 Token。

GPT-5.6 Luna 以每秒 126 个 Token 位居其后，Nemotron 3 Ultra 和 DeepSeek V4 Pro 0813 分别为每秒 112 个和 80 个 Token。相比之下，Claude 系列模型在榜单上的位置明显靠后：启用 fallback 的 Claude Fable 5.1 每秒输出 66 个 Token，Claude Opus 5 则为每秒 56 个 Token，还不到 Gemini 3.8 Flash 的五分之一。

由于输出Token增加了30%，Gemini 3.8 Flash在这套评测中的单任务加权生成时间仍从2.2分钟升至2.5分钟，增幅约14%。这项指标只统计模型生成输出所需的时间，不包含首Token延迟和其他系统开销，不能直接等同于Agent完成整项工作的真实耗时。

换句话说，3.8 Flash吐Token更快，却也生成了更多Token。300 TPS抵消了部分额外Token带来的时间开销，但没有让加权生成时间继续缩短。

这也说明，评价Agent模型只看Token单价已经不够。模型为了完成任务会生成多少Token、执行多少轮，以及能以多快的速度消化这些Token，共同决定了最终的成本与等待时间。

提高的3分，主要来自Agent能力
Gemini 3.8 Flash在Intelligence Index上提高的3分，主要来自智能体评测。Artificial Analysis认为，贡献最大的项目包括衡量工具使用能力的τ³-Banking、衡量编程能力的Terminal-Bench v2.1，以及测试现实世界高经济价值任务的GDPval-AA v2。其中，τ³-Banking提高12个百分点，达到45%。

在Artificial Analysis自建的AA-Briefcase知识工作评测中，Gemini 3.8 Flash获得1213的Elo评分，比上一代提高79分。这部分进步主要来自更高的任务要求达成度和更强的分析质量，输出呈现方式没有明显变化。

Google公布的结果也显示，Gemini 3.8 Flash在长程软件工程评测DeepSWE v1.1中超过大多数体量更大的前沿模型。在DeepSWE当前公布的结果中，它与Claude Opus 5均为74%，并列第一；平均任务成本为2.36美元，约为Claude Opus 5的五分之一。

这一结果也与Google所说的“更加努力”相呼应：面对复杂任务时，模型会增加推理步骤、反复调用工具，并在必要时使用更多Token。

不过，它在计算机操作上的提升相对有限。Gemini 3.8 Flash在OSWorld-2.0上的成绩虽然超过3.7 Flash，与Claude Opus仍有较大差距。

“美国大豆包”真的翻身了吗？
Gemini 3.8 Flash 拥有100万 Token 的上下文窗口，支持文本、图像、视频和语音输入，输出目前仍限于文本。开发者可以通过 Google Antigravity、Google AI Studio 和 Android Studio 中的 Gemini API，以及界面设计服务 Stitch 使用它；企业客户可以通过 Gemini Enterprise 接入；Google AI Pro 和 Ultra 订阅用户则可以在 Gemini 应用、Google 搜索的 AI Mode 和 Google Sheets 中调用该模型。

Google 还同步推出了 Gemini 3.8 Flash Cyber，一个专门针对软件漏洞发现与修复进行调优的版本。它目前只向受信任的测试者、政府机构、关键基础设施组织和部分软件维护者开放。
Google 称，Gemini 3.8 Flash Cyber 能够发现更多漏洞，生成有效补丁的成功率也更高。Chrome 安全团队使用新模型后，补丁准确率提升至原来的2.6倍；Google Cloud 团队则表示，新模型只用了两个小时便发现了一个严重漏洞。

从通用 Agent、长程软件工程到网络安全，Flash 已经逐渐从 Google 模型家族中的经济型选项，变成了真正承担生产任务的主力。

至于“美国大豆包”是否已经翻身，基准测试只能回答一半。59分证明它进入了第一梯队，DeepSWE 榜首证明它的编程和 Agent 能力取得了实质进步，0.58美元的单任务成本则让它重新站上了性价比前沿。

剩下的一半仍要交给真实使用。Google 需要证明，Gemini 3.8 Flash 增加的 Token 和工具调用真正提高了任务成功率，而不是用更长的过程制造更昂贵的错误。

但至少这一次，“最快告诉你错误答案的 AI”已经开始把速度用在更有价值的地方。Gemini 3.8 Flash 每秒依然能够输出约300个 Token，只是它不再满足于最快给出一个答案，而是试图成为最快把任务做完的模型之一。

参考链接：
https://www.theregister.com/ai-and-ml/2026/09/02/with-gemini-38-flash-google-reminds-everyone-its-still-in-the-race/5294049"
https://artificialanalysis.ai/articles/gemini-3-8-flash"
https://arstechnica.com/ai/2026/09/google-releases-gemini-3-8-flash-its-third-flash-model-in-six-weeks/"