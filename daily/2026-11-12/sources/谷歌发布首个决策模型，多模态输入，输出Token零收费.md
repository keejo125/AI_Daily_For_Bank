---
publish_time: 1794450225
link: https://mp.weixin.qq.com/s/iSPXt9A3em4pCqUFPO-_AQ
source: 夕小瑶科技说
status: confirmed
category: 国际
is_model_related: true
digest: |
  夕小瑶科技说梳理决策模型赛道：继TypeSafe Jev、OpenAI Decisions API后，谷歌携Gemini Decision 1入局，支持文本、图片、音频、视频、PDF输入，单次最多1000个问题；独立榜单Decision Index v2.1总分66，与Jev 1.14同档。
title: 谷歌发布首个决策模型，多模态输入，输出Token零收费
---

# 谷歌发布首个决策模型，多模态输入，输出Token零收费

来源：夕小瑶科技说
原文链接：https://mp.weixin.qq.com/s/iSPXt9A3em4pCqUFPO-_AQ

决策模型这条赛道，谷歌也来加入了。
今天，谷歌 CEO 桑达尔·皮查伊发帖宣布：
Gemini Decisions API 正式上线，配套的新模型叫 Gemini Decision 1。
在此之前，这个赛道已经热闹了一阵。
9 月 15 日，创业公司 TypeSafe 发布了 Jev。主要任务是根据给定的信息做判断：比如判断是或否、从几个选项中选答案，或者按照标准打分。
Jev 上线 仅仅 24 小时，就有将近 13% 的付费团队用上了。
两周后的 9 月 29 日，OpenAI 在开发者日宣布了自己的 Decisions API，底层用 GPT-6 Luna，同样做分类、选择和评分。
现在，谷歌带着 Gemini Decision 1 入局。
它不仅能处理文字和图片，还能听音频、看视频、读 PDF；面对同一份材料，一次最多可以回答 1000 个独立问题。
◈
能听音频、看视频，一次回答 1000 个问题
Gemini Decision 1 的用法跟 Jev 几乎一样，可以理解成回答三类题。
第一种是
判断题
：某个条件是否成立？
第二种是
选择题
：在给定选项中，哪个最合适？一次可以提供 2 到 255 个选项。
第三种是
评分题
：按照预先写好的标准，给内容打分。
通常开发者只需要把材料、问题和选项交给它，模型会返回选择、分数以及相应的概率或置信度，程序再根据结果决定下一步怎么做。
前面两个决策模型中，Jev 主要输入是文字和 JSON，OpenAI 的Decisions API 能看文字还有图片。
Gemini Decision 1 则是处理的材料更丰富：
包括文字、图片、音频、视频和 PDF 都可以作为输入，还能在同一次请求中组合使用。
谷歌举的例子，是把一张茶水间台面的照片和一句文字说明放进同一次请求。文字写的是：早上 9 点客户会前来之前，检查这张台面。
以前这两样是分开的：
只看照片，不知道 9 点有会；只看这句话，又看不见台面上现在有没有水。
放在一次请求里，模型要同时回答三道题：台面上有没有没擦掉的液体？接下来是用旁边的抹布擦、叫保洁，还是已经可以开会？按“干净、只有一小片、洒得很开或有安全隐患”这三档，脏到哪一档？
同一份材料上，这种问题一次最多可以交 1000 道，不用每问一句就把照片和说明再交一遍。
目前 OpenAI 的 Decisions API 一次最多 400 道。Jev 没有公布固定的题数上限。
◈
谷歌自测领先，独立榜单和 Jev 接近
发布新模型，谷歌也晒出了跑分。
在官方测试中，谷歌把 Gemini Decision 1 和 Jev 1.14、OpenAI Decisions API 使用的 GPT-6 Luna 等模型放在一起比较。
先看
JevBench
。这是一个评估模型处理多种决策任务能力的测试：
Gemini Decision 1拿了92.2%，
Luna 是 90.9%，Jev 是 90.0%
但继续往下看，它也不是每一项都领先。
在考察网页操作判断的 Mind2Web Multimodal 上，Jev 1.14 得分 86.8%，略高于 Gemini 的 86.2%。
在考察何时应该调用工具的 When2Call 测试中，Jev 的得分是 82.0%，Gemini 为 79.9%。
谷歌还比较了模型的置信度校准误差，可以简单理解为：模型说自己“有多确定”，和它在一组问题上的实际表现是否相符。这个误差越低越好。
在谷歌的共同测试中，Gemini Decision 1 的校准误差为 0.0250，低于 Jev 的 0.0494 和 GPT-6 Luna 的 0.0721。
从成绩单看，
Gemini 在多项任务中表现不错，Jev 则在部分任务上仍然领先。
发布几分钟后，独立评测机构 Artificial Analysis 也把 Gemini Decision 1 纳入了 Decision Index。
这个榜单会综合考察文档判断、工具选择、知识、推理，以及问题换一种说法后答案是否一致等方面。
Decision Index v2.1 总分 66，跟 Elephant 9B、Jev 1.14 一档，比并列第一的 Drex Max v1.1 和 GLiDE v1.2 低 7 分。
在这套测试中，
Gemini 和 Jev 的综合成绩相当接近。
◈
谷歌已经拿它做了什么？
谷歌展示了一个包裹检查演示。
面对配送照片，Gemini Decision 1 需要回答：包裹是否破损？是不是放在门廊下？配送质量该打几分？是否需要进入后续的理赔审核流程？
在这次演示中，模型用
4.5 秒处理了 100 张配送照片
，每张照片完成 16 项检查；在这个特定任务中，速度接近 Gemini 3.5 Flash-Lite 的 4 倍。
除了演示，谷歌也介绍了它在自家产品中的应用。
其中一个用途是
给模型分流
。
Gemini Notebook 会用 Decisions API 判断用户请求适合哪一档模型、需要多少思考强度。简单问题交给更轻的路径处理，复杂问题再交给更擅长深度推理的模型。
而且在这个场景中，日常请求的延迟最高降低了
40%
。
另一个应用来自设计工具
Stitch
。在 Stitch 的快速画布实验中，Decisions API 被用于支持快速生成可交互的产品流程，以及通过语音或点击近实时调整。用户确定方向后，还可以把画面交给完整的 Stitch 流程继续细化。
此外，Google Labs 的 CC 用它从 200 多个选项中挑选表情反应；Google Search 也将它用于 MCP 工具相关的安全检查。
◈
输入每百万 token 0.10 美元，输出不收费
最后是开发者很关心的两个问题：快不快，贵不贵。
速度上，谷歌给出的
Gemini Decision 1 端到端延迟是 150～250 毫秒
。
而且在最长 16K token 的上下文条件下，一次请求从 1 个问题增加到 100 个问题时，延迟变化不大。
价格方面，Gemini Decision 1 的输入价格为
每 100 万 token 0.10 美元
，输出 token 不收费。
开发者可以通过 Google AI Studio 的 Gemini API 使用，谷歌也提供免费层用于试用。
但是如果和 Jev 比，Jev 的输入标价仍然更低：
Jev：每 100 万输入 token 0.042 美元
Gemini Decision 1：每 100 万输入 token 0.10 美元
OpenAI Decisions API：非缓存输入每 100 万 token 0.10 美元
三者都不收输出 token 费用。
不过，实际完成一项任务要花多少钱，还和材料长度、问题数量、缓存以及具体调用方式有关，不能只看单价。
三个月前，“决策模型”这个说法还没有。现在，Artificial Analysis 的榜单上已经排了 18 个。
目前在独立榜单上排前面的，是 Nace、Fastino 这些专门做决策模型的小公司；
论价格，Jev 和 Drex 也比两家大厂便宜一截。
这样看，下一轮比的未必是谁家表格好看，而是谁能在开发者自己的数据上判得又准又便宜。
参考文献
[1]
Gemini Decisions API:
https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/
