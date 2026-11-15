---
publish_time: 1794352581
link: https://mp.weixin.qq.com/s/sch617r-tqG_UOlzOmwg9Q
source: 机器之心
status: confirmed
category: 国际
is_model_related: true
digest: |
  谷歌 Gemini 4 Carbon 全球全量开放，文章重点介绍其 4 周内用 650 万行数学证明验证“Signal 安全”等能力，并对比 Fable 5.2 等竞品。
title: 刚刚，Gemini 4 Carbon全球全量开放，4周、650万行数学证明验证「Signal安全」
---

# 刚刚，Gemini 4 Carbon全球全量开放，4周、650万行数学证明验证「Signal安全」

来源：机器之心
原文链接：https://mp.weixin.qq.com/s/sch617r-tqG_UOlzOmwg9Q

机器之心编辑部
刚刚，
Google DeepMind 宣告 Gemini 4 Carbon 今天正式开放，
号称为「Google 目前能力最强的模型」，专门面向复杂、长周期任务，能够投入更多推理资源，深入探索问题，并通过持续的执行、检查和修正，完成软件工程、网络安全、知识工作和科学研究中的复杂任务。
与此前的 Gemini 4 Argon 相比，Carbon 的定位更加明确：
它不满足于快速给出一个答案，而是愿意花更多时间和计算资源，把一件复杂的事情真正做完。
Demis Hassabis 给出了一个直观案例，「Carbon 对我最初开发的《Theme Park》游戏二进制文件进行了逆向工程，在游戏中新增了一项以 DeepMind 为主题的游乐设施，并一次性将整个游戏移植到了 Web 端。」
而下面他还附上了去年同时期用 Gemini 3 做的视频对比，并感慨：
「不到一年的时间，Gemini 就从 3 进化到 4，进步实在惊人……
亲眼看到这一切，真的有种不可思议的感觉！」
而这样的强大能力，如今，全球用户都可以用到了！官方表示，目前从今天起，Gemini 4 Carbon 将通过以下渠道开放：
消费者：
Google AI Ultra 订阅用户可以通过 Gemini App 和 Google 搜索中的 AI Mode 使用。
开发者与企业：
可以通过 Google AI Studio 和 Android Studio 中的 API 进行开发；Google AI Ultra 订阅用户还可以通过 Google Antigravity 使用，企业用户则可以通过 Gemini for Business 使用。
科学家与研究人员：
可以通过 Google Antigravity 申请，有机会获得为期 6 个月的免费使用资格。
网络安全防御人员：
可以申请加入 Fairwind 计划，获得 Carbon 在网络安全领域的使用权限。
此外，为了证明 Gemini 4 Carbon 在处理科学研究中复杂任务的能力，就在刚刚模型正式发布后，Google DeepMind 给出了一个颇具代表性的案例，公布了一项
名为 AlphaProof Code 的研究：
研究人员利用 Gemini 4 Carbon 驱动的 AI Agent，对 Signal 加密协议的底层代码进行了形式化验证，最终生成了超过 650 万行经过机器检查的数学证明代码。
这项原本可能需要专家团队耗费数年完成的工作，最终只用了四周。
更重要的是，这意味着 AI 开始从「写出代码」，走向「用数学证明代码是安全的」。
从长周期推理，到真正完成复杂工作
Google 对 Gemini 4 Carbon 的定位，是
目前最适合处理高难度、多步骤任务的模型。
在软件工程中，它可以面对复杂代码库，进行跨模块问题排查、架构调整和多轮调试；在科学研究中，它能够围绕开放问题持续探索假设、分析证据并验证结果；在知识工作中，它也可以处理大量复杂文档、数据和结构化信息。
这背后有一个重要设计：
Extended Verification Loops（扩展验证循环）。
面对复杂任务，Carbon 会投入更多 Thinking Tokens，探索不同的解决路径，并在执行过程中反复检查结果。发现问题后，它可以继续修改、测试，直到得到更可靠的结果。
在 Google 公布的独立工作流基准测试中，Carbon 在 CursorBench 4.0、Perplexity WANDR 和 Zapier AutomationBench 上均排名第一。Google 还表示，在这些测试中，其单项任务成本比表现最好的下一款外部模型低两倍以上。
与此同时，
Google 正在 Google Antigravity 中预览 /swarm 功能：
用户只需给出一个任务，就可以让多个 Agent 组成协作团队，分别承担架构设计、任务协调、代码实现和审查等工作。
Carbon 可以负责其中最需要深度推理的环节，其他更轻量的模型则并行处理具体任务。
从模型能力到多 Agent 协作，Google 希望让 AI 承担的工作变得更复杂，也更接近真实的专业工作流程。
650 万行数学证明，AI Agent 给 Signal 做了一次「安全体检」
如果说 Gemini 4 Carbon 展示的是能力上限，那么 AlphaProof Code 就是一次非常具体的能力验证。
这项研究瞄准的是一个长期困扰软件安全领域的难题：
如何证明一套真实运行的软件，确实满足设计者要求的安全属性？
以 Signal 为例。
作为广泛使用的加密通信协议，Signal 的安全性建立在一系列复杂的密码学机制之上。过去，密码学专家可以从数学层面分析协议设计是否安全，也可以通过代码审查和测试寻找漏洞。
但这里始终存在一道鸿沟：理论上安全的协议，不代表最终运行在用户设备上的代码一定安全。
从协议设计到实际运行，中间还要经历代码实现、编译和优化。一个微小的实现错误，就可能让原本严密的安全设计失效。
传统的形式化验证（Formal Verification）试图用数学证明解决这个问题：把软件需要满足的安全条件写成严格的数学命题，再证明实际代码确实满足这些条件。
问题在于，这项工作极其复杂，往往需要专家投入大量时间。
Google DeepMind 这次推出的 AlphaProof Code，就是希望借助 AI Agent 降低这道门槛。
研究团队首先与模型合作，将 Signal 的安全目标转化为 Lean 语言能够理解的数学规格，并由人类专家逐一审核。随后，Gemini 4 Carbon 驱动的多个 Agent 开始自动构造证明，尝试证明实际代码满足这些安全要求。
这里的关键是，研究并没有停留在协议设计或源代码层面，而是进一步深入到最终编译后的设备代码。
研究人员建立了 AArch64 指令集的形式化语义，将编译后的机器码纳入验证范围。这意味着，他们试图证明的是真正运行在设备上的代码，而不只是理论上的算法描述。
最终，AlphaProof Code 为 Signal 的核心实现生成了约
650 万行 Lean 证明代码，
建立在约 2.6 万行经过审核的形式化规格和机器码语义基础之上。
整个验证过程只用了四周。AI Agent 还会自动标记需要人类进一步检查的部分，最终只有约 1% 的代码库需要额外人工关注，其余证明均交由 Lean 的可信内核进行机器检查。
更重要的是，这套系统并非只会给正确代码生成证明。
研究团队还故意将两个过去真实存在、后来已经修复的漏洞重新植入隔离版本的 Signal 代码。结果，AlphaProof Code 都成功生成了机器检查通过的反例证明，识别出这些代码不满足原先的安全要求。
这说明它不仅能帮助验证正确实现，也具备识别特定错误实现的能力。
AI 编程的下一步，是让代码变得可信？
这项研究的意义，远不止帮 Signal 做了一次安全验证。
过去，形式化验证一直是软件工程中成本最高的安全保障手段之一。即使对于非常重要的系统，想要证明其代码满足严格的安全属性，也往往需要专家团队耗费数年。
现在，AI Agent 开始接手其中大量繁重的工作：
编写形式化规格、探索证明路径、生成 Lean 代码，再由独立的证明内核进行检查。
当然，这不意味着 AI 已经能够独立证明任何软件绝对安全。人类专家仍然需要定义和审核安全规格，证明系统也只能保证代码满足已经明确表达出来的属性。
但这条路线已经展示出一种新的可能：当 Agent 能够持续推理、调用工具、构造复杂中间结果，并通过外部验证机制反复检查，AI 就有机会承担过去需要专家团队长期完成的工作。
Google DeepMind 也表示，未来希望将这套技术扩展到医疗设备固件、电网软件等关键基础设施，并与自动化漏洞修复工具 CodeMender 结合，让软件从发现漏洞、修复问题到形式化验证形成更完整的安全闭环。
从 Gemini 4 Carbon 的发布，到 AlphaProof Code 对 Signal 的验证，Google 展示的是同一个方向：模型的价值正在从回答问题，延伸到承担复杂工作。
而当 AI 不仅能写出代码，还能帮助人类用数学证明代码满足安全要求，Agent 能力的边界也就被推向了一个新的领域。
那么你呢，如何看待如今的大模型已经不止于打榜比分，而是去探索更复杂的数学、密码难题？欢迎在评论区留言交流！
参考链接：
https://x.com/GoogleDeepMind/status/2120219371473617099
https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/?utm_source=x&utm_medium=social&utm_campaign=&utm_content=
https://x.com/sundarpichai/status/2120207062655549933
https://deepmind.google/blog/introducing-alphaproof-code/
© THE END
转载请联系本公众号获得授权
投稿或寻求报道：liyazhou@jiqizhixin.com
