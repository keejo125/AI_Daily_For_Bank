---
publish_time: 1787306416
link: https://mp.weixin.qq.com/s/FTs3pJGGfKqG_ewim5SkKw
source: CSDN
status: confirmed
category: 国内
is_model_related: true
digest: |
  DeepSeek官方宣布实验性质的多模态视觉理解模型DeepSeek-V4-Flash-Vision-Exp正式上线API平台，与此前以文本为主的V4-Flash形成互补，补齐视觉理解拼图。
---

# 刚刚！DeepSeek多模态视觉理解模型上线

来源：CSDN
原文链接：https://mp.weixin.qq.com/s/FTs3pJGGfKqG_ewim5SkKw

刚刚，DeepSeek 又给 V4 系列补上了一块重要拼图。其官方宣布，
实验性质的多模态视觉理解模型 DeepSeek-V4-Flash-Vision-Exp 正式上线 API 平台。
与此前主要处理文本的 V4-Flash 不同，新模型可以直接接收图片，并将视觉理解能力接入 Agent 工作流。
这也意味着，DeepSeek 的多模态能力开始从模型展示进一步走向 API 服务。
来源：https://api-docs.deepseek.com/updates/
文本能力基本不变，视觉 Agent 能力明显提升
从官方公布的测试结果来看，V4-Flash-Vision-Exp 并不是简单地在文本模型之外“加上看图能力”。
在 Agent、推理、世界知识等纯文本任务上，V4-Flash-Vision-Exp 与正式版 V4-Flash 基本持平。而在需要处理视觉信息的 Agent Benchmark 中，新模型相比 V4-Flash 出现了明显提升。
DeepSeek 特别提到，在 ApexBench、Agents’ Last Exam 等测试中，纯文本版 V4-Flash 会忽略其中包含的多模态元素，因此无法充分完成相关任务。
而加入视觉能力之后，V4-Flash-Vision-Exp 在这些场景中的表现大幅跃升，
官方称其多模态 Agent 能力已经接近 Opus-4.8。
多模态能力正式进入 API
对于开发者来说，这次更新更重要的部分还是 API。
据官方介绍，开发者可以通过设置
model='deepseek-v4-flash-vision-exp'
调用新模型。API 支持 Chat Completions、Messages 和 Responses 三种调用格式，可以直接接入现有 Agent 框架。
在输入方式上，模型支持图文混合输入，图片可以通过三种方式传入：
Base64 内联
外部 URL
Files API
图片在 API 服务中会转换成 Token 进行计费，单张图片最多占用 384 Tokens，价格则与 V4-Flash 保持一致。
这意味着开发者不需要为多模态能力单独适配一套完全不同的调用方式，现有的 Agent 工作流也可以比较方便地加入视觉输入。
Files API 同步上线
与多模态 API 一起开放的，还有 DeepSeek 的 Files API。它主要解决的是图片重复上传的问题。
开发者可以先把图片上传到 DeepSeek 平台，之后在请求中直接通过 file_id 引用。这样一来，同一张图片需要被多次调用时，就不必每次都重新上传，也能减少请求过程中的带宽消耗。
目前 Files API 不收取费用。
从这次更新来看，DeepSeek 正在把视觉能力与 Agent 工具调用进一步结合起来，而不是仅仅增加一个“图片输入”的模型接口。
当然，V4-Flash-Vision-Exp 目前仍然带有 Exp（Experimental） 标识，意味着它本质上还是实验性质的模型。实际效果、稳定性以及后续是否进入正式版本，仍需要更多开发者使用和测试。
但至少从 API 开放这一点来看，DeepSeek V4 系列已经开始从纯文本 Agent，向能够同时处理文字、图片和工具的多模态 Agent 继续迈进。
来源：
V4-Flash-Vision-Exp 上线，开启多模态 API 服务
GitHub宕机7小时47分钟，究竟发生了什么？官方发布复盘报告
杀进“羊圈”的AI Coding？从大厂辞职11年后，他又把代码“捡”了回来：一个人用AI干了3个月，仅花5万元给1万只羊写了套系统
曾经号称比Python快9万倍，Mojo如今彻底开源了！
📢
最后，说一件事
2026 奇点智能技术大会与C++及系统软件技术大会
终于要和大家见面了。
11 月 20-21 日·北京，奇点智能研究院联合 CSDN，把两场技术大会放在了同一个时空里：
奇点智能技术大会（始于 2016）——聊大模型、AI Native、企业级 AI 落地、多模态与世界模型；
C++ 及系统软件技术大会（始于 2005）——聊现代 C++ 演进、AI 算力与推理优化、高性能低时延系统。
为什么要放在一起？因为我们越来越相信——上层 AI
应用的爆发，离不开底层系统软件的支撑；而底层技术的演进方向，也正在被 AI 重新定义。
这次大会汇聚 70+ 位技术专家、18 个主题、1000+ 同行到场。
如果你也在这些方向上做研究、做产品、做工程，别错过。
