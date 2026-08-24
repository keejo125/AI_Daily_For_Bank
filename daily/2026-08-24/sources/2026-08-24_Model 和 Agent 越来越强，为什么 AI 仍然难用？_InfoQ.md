---
publish_time: 1787550338
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/2OphdcBb4YGGkv773S8VJA
source: InfoQ
title: Model 和 Agent 越来越强，为什么 AI 仍然难用？
---

# Model 和 Agent 越来越强，为什么 AI 仍然难用？

来源：InfoQ
原文链接：https://mp.weixin.qq.com/s/2OphdcBb4YGGkv773S8VJA

作者 | 可可
核心观点：Model 提供智能，Agent 提供行动，Product 负责把记忆、流程与界面组织起来，让普通用户无需理解 Prompt、上下文和工具编排，也能直接使用 AI 完成持续的工作。相关实践 Kition：https://github.com/KitionAI/kition
AI 行业当下存在一个误判：将"Agent 完成任务"
直接等同于
"用户完成工作"。
Agent 已经能够分析信息、调用工具并交付结果，但真实工作通常跨越多轮、多人和多个系统：结果需要核对，异常需要处理，进展需要保存，方法需要复用。几天或几周后，人和 Agent 还要能从上一次的状态继续，而不是重新解释一切。
当 Coding Agent 和通用 Agent 逐步解决了"AI 如何执行任务"之后，下一个关键问题随之浮现：
如何把执行能力转化为普通人能够长期使用的产品？
这中间横亘着一道"Agent 能力—用户可用性鸿沟"（Agent Capability–Usability Gap）。跨越它，不能只依靠更强的模型或更复杂的 Agent，而要由 Product 承担实现复杂度——记住事实与进展，保存验证过的方法，并让用户通过熟悉的工作对象查看、修改、审核和接管。
1
Agent 能执行，但普通人用不起来
开发者是最早感受到 Agent 价值的人群，因为软件开发天然提供了一套适合 Agent 工作的环境——文件、目录、版本历史、命令、测试和相对清晰的完成条件。Agent 修改文件后可以运行测试，测试失败后可以读取错误并继续调整；人和 Agent 操作的是同一批对象。
与此同时，WorkBuddy 等办公 Agent 通过多 Agent、Skills、MCP 和自主规划完成更复杂的任务。不同路线共同指向一个结论：
Agent Layer 已经具备执行真实任务的生产能力。
但开发者与普通用户之间存在一个关键差异：**开发者的执行环境由仓库、文件和工具构成；普通人的工作入口通常是文档、记录、状态和流程。**开发者可以把仓库、路径、脚本、权限、MCP、日志和 Diff 当作灵活的工作材料；而大多数人开始一项工作时，面对的是一篇需要修改的文档、一批等待处理的票据、一张客户表、一组营销素材，或者一套每周都要重复的流程。
如果产品只提供一个对话框，用户就必须先把熟悉的工作翻译成 Agent 能理解的 Prompt、文件、工具和执行步骤。这个**"翻译成本"**，正是 Agent 能力难以向普通用户普及的重要原因。
大模型出现以后，自然语言让用户可以直接描述自己想要什么，大幅降低了表达意图的门槛。但表达意图与构建一套可持续运行的应用，是两项不同的工作——后者还需要定义数据结构、验证系统行为、处理异常并长期维护结果。《Why Johnny Can't Prompt》对非 AI 专家设计 LLM Prompt 的过程观察发现：参与者多采用机会式尝试，较少系统评估不同 Prompt，还会把人与人之间发出指令的经验过度迁移到模型上，同时受到 Prompt 行为脆弱性的影响。[1]
换言之，自然语言并没有消除**"编程式工作"**，只是把一部分复杂度从代码转移到了 Prompt、上下文和工具编排。当用户反复定义字段、选择工具、维护提示词、检查中间结果时，他实际上是在用新的语言搭建一个小型应用。
真正的产品不应继续教育每个用户成为 Prompt 工程师，而应把目录、脚本、Skills、MCP、权限和错误处理收进系统，把文档、表格、状态、按钮和流程留给用户。简而言之：
Agent 保留灵活性，Product 承担复杂性。
2
上下文不等于产品记忆
更长的上下文窗口和聊天历史，能够帮助 Agent 理解当前任务，却不能替代产品中的持久记忆。真实工作依赖的不只是"说过什么"，还包括对象之间的关系、当前状态、责任归属和历史变化——这些信息不仅帮助模型记住过去，也决定下一步能够做什么。
分布式认知研究为此提供了理论支撑。Hollan、Hutchins 与 Kirsh 将研究视角从单个用户和单台计算机扩展到完整环境，观察人、工具和信息材料如何共同完成活动。[4] 在实际工作中，一篇文档、一张表格、一个状态字段、一组附件和一张流程图，同时承担着信息容器、外部记忆、协调机制和判断依据等多重角色。
例如，"待审核"不是一句聊天记录，而是一个能够被筛选、统计并触发后续动作的状态；生成图片与产品 Brief 的关联，也不应只存在于某轮对话的上下文里，而应保存在可追溯的工作对象中。
两者的区别可以概括为：
•
上下文
是模型当前可以读取的信息；
•
产品记忆
保存的是用户与 Agent 之后还要持续操作的事实、关系、状态和历史。
由此可见，文档、表格、状态和历史记录并非单纯的输出格式，而是不同形态的产品记忆：文档保存叙事与判断，表格保存事实与关系，状态保存进展，历史记录保存变化，而 Workflow 则保存"这件事应该怎样做"。
因此，真正支撑持续协作的不是无限延长的聊天记录，而是建立一组人和 Agent 都能看到、理解、修改并继续使用的
共享对象与显式流程
。
3
Product 的基础：记忆、流程与界面
如果说产品记忆回答"工作进行到了哪里"，流程回答"下一步怎样推进"，那么界面则决定用户能否理解和控制这一切。三者需要落在具体的工作对象上，而不是停留在聊天记录中。
文档：保存叙事、判断与上下文
文档适合承载方案、分析、规范等叙事性工作。它在项目中拥有稳定位置，人可以阅读、编辑、链接、搜索和导出；Agent 可以基于当前内容继续工作，用户也能清楚地检查它增加、删除和改写了什么。
文档不再只是一次性输出，而是人与 Agent 持续完成同一项工作的共享界面。
DataTable：保存事实、关系与状态
DataTable 适合承载票据、客户、素材等结构化工作。业务任务不仅需要单元格，还需要字段类型、附件、公式、筛选、分组、视图、记录状态，以及绑定到具体字段的 AI 操作。
例如，在同一条票据记录中，一个字段保存原始图片，一个字段提取商户，一个字段识别金额，另一个字段完成分类。生成结果始终与原始资料和当前记录保持关联。
生成的 Spreadsheet 是一次输出；原生 DataTable 是一个持续运行的应用。
这样，DataTable 可以同时承担输入界面、批处理队列、运营数据库和人工审核页面。产品中持续存在的数据结构，也让后续任务可以直接在同一结构上继续。
这也延续了 End-User Computing 的重要传统：表格之所以成为最成功的最终用户计算环境之一，正是因为人可以通过可见的单元格、公式和数据关系直接构建行为。[12]
Workflow：保存方法与下一步
Workflow 适合把已经验证的方法沉淀下来。Agent 可以执行脚本、调用 Skill 或定时运行 Prompt，但进入业务的流程还必须让负责人理解和接管：触发条件、执行动作、配置状态、测试结果、失败节点、运行历史和启用状态，都应该被直接呈现。
Scheduled Agent Task 重复执行一条指令；可视化 Workflow 保存并呈现一套明确的流程。
至此，文档保存叙事，DataTable 保存事实与状态，Workflow 保存方法——三者共同构成持续工作的基础。而界面的任务，就是让人能够直接理解和操作它们。
Product 的核心不是替代 UI，而是让 Agent 与 UI 协同
Product 不应在 Prompt 与传统 UI 之间二选一。Ben Shneiderman 在 Direct Manipulation 研究中强调持续可见的对象、增量操作、快速反馈和可逆性[3]；Eric Horvitz 在 Mixed-Initiative User Interfaces 研究中进一步提出，把自动化服务与人的直接操作结合起来，可以形成更有价值的设计空间。[7]
Prompt 擅长表达目标和处理未知路径，UI 擅长呈现对象、结构、状态和反馈。两者不是替代关系，而是互补关系。
在这样的协同关系中，人应该可以直接编辑文档和记录，也可以把路径未知的任务交给 Agent；Agent 完成修改后，人能够检查、纠正或撤销；已经验证的方法则可以进一步转化为 Workflow。
Jeffrey Heer 提出的"Agency plus Automation"，同样强调通过共享表示让人和算法发挥互补能力，同时保留人的主动性。[6]
从这些研究出发，一个面向普通用户的 AI Product 需要形成一条完整链路：
从熟悉的对象进入，让人和 Agent 在同一对象上协作，使执行过程可控，再把验证过的方法沉淀为可演进的流程。
第一，从用户熟悉的工作对象开始
用户应该可以从编写文档、添加记录、上传图片、选择字段类型，或者连接一个触发器与动作开始——这些都是他们熟悉的工作入口。
这些对象本身就在表达任务结构，用户无需先理解 Agent 的内部机制，便可以自然进入工作。
第二，让人和 Agent 操作同一批对象
日期应该继续是日期，附件应该与记录保持关联，状态应该能够筛选，生成素材也应该保留自己与源字段的关系——而不是在生成后就变成孤立的文件。
自然语言负责表达意图，原生对象负责保存工作中有价值的结构、关系和状态。
当人和 Agent 操作同一批对象时，结果会直接进入现有工作结构，后续的核对、修改、协作和自动化也能沿着同一条链路自然延续。
第三，让执行可见、可改、可恢复
当 Agent 开始修改真实工作对象时，审核的重要性也随之提升——用户需要知道 Agent 做了什么、为什么这样做，以及如何撤回。
Amershi 等人总结的 Human-AI Interaction Guidelines 对此给出了明确方向：系统应明确自己能做什么、展示当前任务相关的上下文、支持高效纠错、在不确定时缩小服务范围、解释行为原因，并为用户提供控制能力。[8]
因此，Diff、字段编辑、失败节点、运行历史、撤销与重试不是附加功能，而是长期人机协作的基础设施。
自动化研究对此提供了更具警示性的视角。Bainbridge 在《Ironies of Automation》中指出，自动化会把人从正常执行转向系统监控和异常接管[9]；当过程参与和上下文减少时，故障处理反而会变得更困难。
Parasuraman、Sheridan 与 Wickens 也指出，自动化会重塑人的活动并产生新的协调要求，信息获取、分析、决策和行动执行可以采用不同程度的自动化。[10]
这意味着产品需要为不同环节选择合适的自动化程度，明确用户何时介入、检查什么，以及如何从异常中恢复。
第四，让探索沉淀为流程，并允许流程继续演进
当路径未知时，Agent 最有价值——它可以研究、比较、规划并动态选择工具。
而当一种方法得到验证后，明确的 Workflow 可以保存这条路径，提升后续执行的稳定性。
Agent 探索未知，Workflow 保存已知。
但 Workflow 不应因此变成僵化的脚本，它还需要保持可演进性。
Feldman 与 Pentland 对组织惯例的研究区分了惯例的显式结构与每一次具体执行，并指出两者会持续相互修改。[11] Workflow 提供可指认的流程结构，而 Agent 与人的每次真实执行则可能暴露新的例外和改进机会。
完整的循环因此是：
Agent 探索方法，Workflow 固化方法，真实运行暴露例外，人和 Agent 再共同修正 Workflow
。
4
AI 产品需要从围绕对话，转向围绕工作
第一代生成式 AI 产品围绕答案组织，当前一代产品开始围绕 Agent 和 Task 组织。下一阶段，产品需要围绕持续发生的工作来组织：既保留 Agent 探索未知路径的能力，也让结果进入稳定的对象、状态和流程。
这意味着产品重心需要完成四个转变：
• 从聊天历史转向共享工作对象；
• 从生成文件转向原生文档与结构化数据；
• 从孤立 Task 转向可持续的工作状态；
• 从隐藏编排转向可理解、可接管的流程。
模型和 Agent 的能力还会继续提升，但执行能力不会自动转化为用户价值。真正的产品机会，在于完成最后一段转换：用文档、DataTable 和 Workflow 承载工作记忆，用 Agent 处理不确定性，用 UI 保证可见、可改和可接管。
Model 让 AI 变聪明，Agent 让 AI 能行动，Product 让工作能够持续。
5
用 Kition 实践 Product Layer
Product Layer 目前仍处于早期探索阶段，它更像一个需要通过真实产品不断验证和修正的假设。
Kition 正是基于这一思路构建的一次实践：将 Markdown 文档、DataTable、Agent 与可视化 Workflow 放在同一个工作环境中，让 Agent 不再只存在于对话框里，而是能够直接参与真实工作对象的创建、修改与流转。
在 Kition 中，文档承载持续演进的内容与判断，DataTable 保存结构化事实、关系与状态，Workflow 沉淀已经验证的方法，而 Agent 则负责处理其中仍然不确定、需要探索和推理的部分。用户可以从自己熟悉的文档、记录和流程开始工作，而不必先理解 Prompt、上下文管理、Skills 或工具编排。
Kition 想验证的并不是“如何再做一个更强的 Agent”，而是另一个问题：当 Agent 已经足够强之后，Product 应该如何组织记忆、流程与界面，才能让这些能力真正进入普通人的持续工作。
如果你想看看这种 Product Layer 被实际做出来是什么样子，可以在这里找到项目：
Kition：
https://github.com/KitionAI/kition
参考资料
Zamfirescu-Pereira, J.D., Wong, R.Y., Hartmann, B., and Yang, Q. “Why Johnny Can’t Prompt: How Non-AI Experts Try (and Fail) to Design LLM Prompts.”
CHI 2023
, pp. 1–21.
https://doi.org/10.1145/3544548.3581388
Lieberman, H., Paternò, F., and Wulf, V., eds.
End User Development
. Springer, 2006.
https://doi.org/10.1007/1-4020-5386-X
Shneiderman, B. “Direct Manipulation: A Step Beyond Programming Languages.”
Computer
16(8), 1983, pp. 57–69.
https://doi.org/10.1109/MC.1983.1654471
Hollan, J., Hutchins, E., and Kirsh, D. “Distributed Cognition: Toward a New Foundation for Human-Computer Interaction Research.”
ACM Transactions on Computer-Human Interaction
7(2), 2000, pp. 174–196.
https://doi.org/10.1145/353485.353487
Carroll, J.M., and Rosson, M.B. “Getting Around the Task-Artifact Cycle.”
ACM Transactions on Information Systems
10(2), 1992, pp. 181–212.
https://doi.org/10.1145/146802.146834
Heer, J. “Agency Plus Automation: Designing Artificial Intelligence into Interactive Systems.”
PNAS
116(6), 2019, pp. 1844–1850.
https://doi.org/10.1073/pnas.1807184115
Horvitz, E. “Principles of Mixed-Initiative User Interfaces.”
CHI 1999
, pp. 159–166.
https://doi.org/10.1145/302979.303030
Amershi, S., Weld, D., Vorvoreanu, M., et al. “Guidelines for Human-AI Interaction.”
CHI 2019
, pp. 1–13.
https://doi.org/10.1145/3290605.3300233
Bainbridge, L. “Ironies of Automation.”
Automatica
19(6), 1983, pp. 775–779.
https://doi.org/10.1016/0005-1098(83)90046-8
Parasuraman, R., Sheridan, T.B., and Wickens, C.D. “A Model for Types and Levels of Human Interaction with Automation.”
IEEE Transactions on Systems, Man, and Cybernetics - Part A
30(3), 2000, pp. 286–297.
https://doi.org/10.1109/3468.844354
Feldman, M.S., and Pentland, B.T. “Reconceptualizing Organizational Routines as a Source of Flexibility and Change.”
Administrative Science Quarterly
48(1), 2003, pp. 94–118.
https://doi.org/10.2307/3556620
Nardi, B.A.
A Small Matter of Programming: Perspectives on End User Computing
. MIT Press, 1993. ISBN 978-0-262-14053-9.
OpenAI Codex and ChatGPT desktop documentation:
https://learn.chatgpt.com/docs/glossary
,
https://learn.chatgpt.com/codex/app
, and
https://learn.chatgpt.com/docs/artifacts-viewer
WorkBuddy official product page:
https://www.codebuddy.cn/work/
今日好文推荐
完全相信AI代码的Uncle Bob，坦诚这条路还没走通
“烂代码”转正？Bun稳定版终落地：跳票一个半月，2900个问题清零
“Anthropic不再是AI圈的信仰”
撞名Anthropic的“外挂”刷屏：让“DeepSeek V4‑Pro碾压 Fable 5”但无人能复现，Token开销反而翻倍
