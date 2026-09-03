---
publish_time: 1788422400
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/QJENmVesXzRG0wKR6pwRCw
source: CSDN
title: “你用AI取代我？我就用AI取代你！”被CEO用AI裁掉后，他们反手造了个“AI CEO”：已狂揽3.5k+Star
---

# “你用AI取代我？我就用AI取代你！”被CEO用AI裁掉后，他们反手造了个“AI CEO”：已狂揽3.5k+Star

来源：CSDN
原文链接：https://mp.weixin.qq.com/s/QJENmVesXzRG0wKR6pwRCw

整理 | 郑丽媛
出品 | CSDN（ID：CSDNnews）
如果
某
一天，你被公司裁员，HR
告诉你：“不是你的能力有问题，只是公司正在进行 AI 转型。”
——
你会怎么做？
有人可能选择重新找工作，有人可能转行，还有人……
决定直接造一个 AI CEO
来“报仇”
。
最近，一个名为 OpenExecutive 的开源项目在开发者社区引发关注。
一位 Reddit 用户
表示，自己的几位朋友正是在公司所谓的“AI 转型”中被裁掉的。于是，这群开发者干脆聚到一起，做出了一个
反击
项目：
既然 AI 可以替代开发者，那为什么不能反过来用 AI 替代 CEO 和其他高管？
更有意思的是，这并不只是一个玩梗 Demo，而是一个真正可以运行、部署和二次开发的多 Agent AI 系统
，
目前已
狂揽
3.
5
k
+
Star
。
8
个
AI Agent，拼出一套“虚拟高管团队”
根据
GitHub 页面介绍，
OpenExecutive 并不是简单地给 Claude 套一个“CEO Prompt”。它是
把一家公司的高管团队拆成 8 个专业角色
，再由一个统一的 Agent 负责调度。
这 8 个角色分别是：
●
CSO（首席战略官）：竞争分析、并购、市场定位、OKR；
●
CFO（首席财务官）：财务建模、融资、单位经济模型、现金流；
●
CHRO（首席人力资源官）：招聘、薪酬、绩效、企业文化；
●
General Counsel（总法律顾问）：合同、知识产权、劳动法和合规；
●
COO（首席运营官）：流程、供应商管理、业务规模化；
●
CMO（首席营销官）：GTM、品牌、传播和公关；
●
CPO（首席产品官）：产品路线图、优先级和产品战略；
●
Board Communications Director（董事会沟通负责人）：董事会材料、投资者关系和公司治理。
用户并不会直接和这 8 个 Agent 打交道。
所有问题首先交给 Executive Orchestrator
（执行
协调员，
相当于整个系统的“大脑中枢”
）
，由它判断需要哪些“高管”参与。如果问题涉及多个领域，就可以并行调用多个 Agent，最后把结果重新汇总成一个统一的回答。
所以
，
从用户视角来看，你面对的始终只有一个“CEO”。
例如，你问：“公司现在现金流紧张，但我们又想进入一个新市场，应该怎么办？”
AI 可能同时让 CFO 分析现金流，让 CSO 判断市场机会，再让 COO 评估执行成本
，最后综合这些意见给出方案。
当然，
如果只是让大模型回答几个商业问题，这个项目
也
没有太特别
——
真正让 OpenExecutive 更像“
人类
高管”的，是它
加入了企业知识库、情景记忆和主动任务调度。
公司
可以上传 Pitch Deck、财务模型、战略文档等资料
，
系统会把这些内容切分后存进 ChromaDB，回答问题时通过 RAG 检索相关内容。每次对话结束后，系统还会提取重要的决策、项目和建议，并保存到 SQLite。
这样
下一次会话启动时，它
就
能回忆此前提出过什么建议。
不仅如此，
项目还内置了 Scheduler，
能
主动发现到期任务并提醒后续行动。不过目前调度器要求 API 以单实例运行
，否则同一个任务可能被重复触发。
提示词缓存也被精心设计
过
，会把
Executive
人设、公司概况、知识索引分别缓存
。
据
官方 README 称，在前几轮交互之后，缓存命中率最高可达约 85%。
开源程度相当高，连新增“高管”都留好了接口
如果用户觉得 8 个
“
AI
高管
”
还不够，Op
enExecutive 也提供了添加新 Specialist Agent
（专员）
的完整流程：
（1）
创建一个继承自 BaseAgent 的新 Agent；
（2
）
在 domain_prompts.py 中添加对应的系统提示词；
（3
）
在 Router 中注册新的 Specialist
Agent
；
（4
）
在知识检索模块中添加领域别名；
（5）
为新领域增加内置知识文档；
（6
）
至少增加两个 Eval 场景；
（7
）
提交 Pull Request。
项目甚至
还
内置了完整的评测系统。目前 evals/ 中包含 29 个评测场景，覆盖全部 8 个专业领域。每个场景都会定义用户问题、模拟企业背景、预期讨论主题、应该调用的 Specialist
Agent
以及针对具体领域的评分标准。
系统会从五个维度进行 1～5 分评价：
人设
一致性、领域准确性、上下文利用程度、路由质量、可执行性
。
CI 的要求是平均分至少达到 3.5/5；如果任何一个维度相较之前下降超过 10%，Pull Request 就会失败。
换句话说，这并不
只
是简单地“把几个 Prompt 拼在一起”，而是
要
把一个
“
AI CEO
”
系统做成可持续测试、迭代和扩展
的工程项目。
不止于网页，
“AI CEO
”
还
可以直接进群
所谓“
AI CEO
”，必然不能
只存在于一个网页里
。
目前
，
OpenExecutive 支持 Web UI、Slack、Email、Telegram、Google Chat、Discord 和 CLI。用户
可直接通过 Web UI 与 AI 高管交流，也可以在 Slack、Telegram 或 Discord 中直接提及它。
以 Discord 为例，项目
就
提供了完整的 Bot 支持。用户可以私聊机器人，也可以在频道中 @ 它，还支持 /ask、/today 等斜杠命令。与此同时，OpenExecutive 还支持通过邮件接收和处理信息。
因此
从技术设计来看，
OpenExecutive
是
想
把 AI 高管嵌入企业原本使用的沟通渠道
，而不是让员工每天专门打开一个 AI 网站
去
“问老板”。
不想用 Claude？还能换成本地模型
目前
，
这套架构主要基于 Anthropic Claude API，默认使用
C
laude
S
onnet
4.
6，而战略、财务、法律和董事会等需要更强推理能力的任务，则可以使用
C
laude
O
pus
4.7
。
不过，OpenExecutive 也没有把自己完全绑定在 Anthropic 身上。项目支持 OpenAI-compatible 的本地模型服务，因此可以通过 Ollama、LM Studio、vLLM 或 llama.cpp 接入本地模型。
例如，用户可以直接运行：
ollama
pull llama3.
3
然后
配置：
LOCAL_MODELS_ENABLED
=
true
LOCAL_BASE_URL
=http://localhost:
11434
/v1
LOCAL_MODELS
=llama3.
3
甚至可以完全不提供 Anthropic API Key，让本地模型承担 Executive、推理和路由任务。
当然，
本地模型也存在一些限制
。例如服务器端 Web Search、Anthropic 的提示词缓存和扩展思考等能力，在本地模型模式下无法直接使用。
另外，由于这个项目高度依赖工具调用和多 Agent 路由，小模型可能无法很好地完成任务。因此，
官方
建议选择工具调用能力较强的模型，例如 Llama 3.3 70B、Qwen2.5 等。
网友热议：AI CEO
到底靠不靠谱？
OpenExecutive 开源后
引发了
不少关注，但网友
讨论很快从“技术上能不能做”变成了一个更现实的问题：
AI 真能当 CEO 吗？
有人指出，CEO 和普通知识型岗位最大的区别之一，是 CEO 往往承担着现实世界中的受托责任和法律责任
：“
如果 AI 做出的决策导致公司重大损失，甚至触犯法律，那
谁来负责？”
更
有人直击痛点：“
AI
都
没法签署公司注册文件，所以最终责任还是得由人类来扛。
”
不过，也有网友
反驳道
，这些 C 字打头的高管，确实应该被取代：“
既然 AI 能替代开发者，那为什么 CEO、CFO、CMO 就
不会被取代
？
把他们的
工作拆开来看，其中同样存在大量信息分析、报告生成、方案比较、流程跟进和决策支持工作。
”
对此，由反对者表示：“
你们把 CEO 想得太简单了。
”
“
CEO 真正有价值的地方，本来就不是‘决策支持’，而在于其愿景和人脉
。一个优秀 CEO 能想出创新的产品、服务和商业模式新点子，在行业里能有广泛的人脉，包括记者、研究人员、投资人和其他合作伙伴——在这些方面，AI 几乎完全无能为力。”
诚然，
至少目前
AI 距离真正承担 CEO 的责任还很远
。
但
OpenExecutive
这个项目的
出现本身就很值得玩味
：
当“AI
取代人类”从一个抽象的概念变成具体的裁员理由时，被取代的人开始用同样的逻辑威胁
那些
所谓
“不可替代”的位置。
就像
文章开头那位 Reddit 用户
说的那句话：“
希望
这种
‘以牙还牙’的做法
，能让那些动不动就想用
AI
取代员工
的老板们多长个心眼。
”
参考链接：
https://github.com/SenteLabsAI/OpenExecutive
https://www.reddit.com/r/artificial/comments/1vyegah/ceo_fired_developers_to_make_room_for_ai/
官宣！Ruby on Rails之父DHH将出席GOSIM Shenzhen 2026
Agent 自进化、AI Coding、世界模型、Agent Infra……2026 奇点智能技术大会首批议题公布
700GB数据被Claude“一键清空”！CTO傻眼了：本想让AI清垃圾，结果一周工作成果都没了……
文末福利｜AI 开学季硬核资料免费领
2026 奇点智能技术大会限时送出两份技术礼包：
Łukasz Kaiser 历届演讲视频 + PPT
Transformer 八子之一、OpenAI 资深研究科学家，带你理解推理模型与大模型第一性原理。
Agent 实战训练营录播课
覆盖 Agent 架构、基座模型、Skill、Agentic Infra 等核心技术，从理论到企业级落地。
扫码免费领取，两套硬核资料一次带走。
📅 11 月 20—21 日
📍 北京万达文华酒店
2026 奇点智能技术大会，现场见。
