---
publish_time: 1789896590
link: https://mp.weixin.qq.com/s/xqGxH3dbtGfcgOSx51z8dw
source: Qoder
status: confirmed
category: 国内
is_model_related: false
digest: |
  Qoder推出QCA（Qoder Cloud Agents）Realtime，将实时语音与云端Agent执行连接起来：用户用语音提出需求，Agent调用工具处理任务，再把进展与结果实时反馈。以销售数据分析为例，为Agent模板配置好数据文件、Python运行环境与工具后，可直接口述“分析这份销售数据，找出收入下滑最明显的渠道并画图”，Agent便在云端沙箱中读取数据、运行脚本、生成图表与报告，执行进度实时显示在对话中。它把“说句话就让Agent干活”变成可操作的云工作流。
title: QCA Realtime：说句话，让 Agent 开始干活
---

# QCA Realtime：说句话，让 Agent 开始干活

来源：Qoder
原文链接：https://mp.weixin.qq.com/s/xqGxH3dbtGfcgOSx51z8dw

现在可以直接说出你的需求，让 Agent 查资料、读代码、跑脚本。
QCA（Qoder Cloud Agents） Realtime
将实时语音与云端 Agent 执行连在一起。
你用语音交代需求，Agent 调用工具处理任务，再把进展和结果实时反馈给你。
读数据、跑代码、出报告，都能聊着来
以销售数据分析为例。为 Agent 模板（Template）配置好 CSV 文件、Python 运行环境和所需工具后，就可以直接说：
分析这份销售数据，找出收入下滑最明显的渠道，画一张趋势图，再整理成分析报告。
文件名、时间范围和筛选条件，可以用文字补充。Agent 在云端沙箱中读取数据、运行分析脚本，生成图表和报告，执行进度会显示在对话中。
拿到结果后，可以让它先讲重点：“用一分钟说清楚，哪些渠道的收入下滑最明显？”你边听结论，边看图表。
听到需要进一步分析的地方，可以打断讲解，接着问：“把这个渠道按周拆开，看看从哪一周开始下滑。”Agent 随后继续分析、更新图表。
从提出问题、查看结果到进一步追问，分析可以在同一场对话中逐步展开。
技术设计：两个 Agent 如何协作
实时交流需要及时回应，数据分析、代码执行等任务则可能持续更久。QCA Realtime 通过语音 Agent 与任务 Agent 分工协作，衔接这两种不同的工作节奏。
交流与执行分工，任务独立推进
当需求涉及查资料、处理文件或运行代码时，语音 Agent 将任务交给基于 Template 创建的执行会话。任务 Agent 在云端处理工作，语音 Agent 根据返回的进展与结果继续交流。用户也可以在执行期间询问进度。
会话和任务状态由服务端保存，与语音连接分别管理。因此，通话断开不会直接取消已受理的任务。重新连接同一会话后，系统加载近期对话和活动任务信息，接着反馈进展与结果。任务仍受原有超时、权限和运行环境约束。
复用已有 Template，分别适配语音与执行
语音 Agent 沿用模板与用户配置中生效的角色设定和业务指令，并加入口语表达、打断、任务委派和结果讲解等交互规则。任务 Agent 则复用 Template 的技能、工具和运行环境。开发者配置好的业务能力，可以直接用于语音发起的任务。
平台支持为语音场景配置独立的执行模型策略，在创建任务会话时调整模型与推理档位，无需修改原 Template。策略会先校验目标模型的可用性；没有匹配规则或目标不可用时，保留原模型。新的模型策略仅影响后续创建的会话。
在控制台快速体验
已有可用 Template，开启 Voice 即可在控制台体验，无需重新搭建 Agent 或编写接入代码。
使用具备相应权限的账号登录 Qoder Cloud Agents 控制台：
切换到 Forward Mode，创建或选择一个可用的 Template。
进入 Template 的 Voice 标签，开启语音配置。
点击体验面板中的麦克风，允许浏览器使用麦克风，连接就绪后开始说话。
可以先说“你好，介绍一下你自己”，体验语音回复和字幕；再用已配好文件、环境与工具的 Template，尝试前面的数据分析任务。
也可以运行 Quickstart，在本地体验并查看接入实现。在线 Demo 暂不支持语音。
接入自己的应用
将同样的语音交互接入应用，可以分为四步：
准备 Template。
配置任务所需的模型、技能、工具和运行环境，确认 Agent 能完成目标任务，再开启 Voice。
创建语音会话。
关联应用用户与 Template，调用接口创建 Conversation，并保存会话 ID，用于后续交互与重连。
接通实时交互。
按接入示例连接已创建的会话，收到就绪通知后，即可发送语音或文字。
呈现反馈与结果。
根据返回事件播放音频、更新字幕，展示任务进度和产物，并处理打断、重连与结束通话等交互。
接入示例参考 Quickstart Demo，完整接口说明见 Realtime API 文档。
https://github.com/QoderAI/forward-quickstart
https://docs.qoder.cn/cloud-agents/forward-realtime-create-conversation
QCA Realtime 目前处于 Beta， Realtime 模型免费体验。
