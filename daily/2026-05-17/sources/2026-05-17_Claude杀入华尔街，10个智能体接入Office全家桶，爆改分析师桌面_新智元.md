---
publish_time: 1779003000
---

# Claude杀入华尔街，10个智能体接入Office全家桶，爆改分析师桌面

> 原文链接：https://mp.weixin.qq.com/s/fJreDeRTh2LpJjA35tgKhw
> 公众号：新智元

新智元报道

编辑：元宇

【新智元导读】

Anthropic一口气甩出10个金融智能体模板，穆迪6亿家公司数据通过MCP打通，Office全家桶全线就位：这不是模型升级，是一次工作流入口的抢占。

华尔街的工作流，被Claude重写了一遍。

5月5日，纽约。

Anthropic CEO Dario Amodei与JPMorgan CEO Jamie Dimon同台亮相，这一幕预示着Anthropic已经进入华尔街核心圈。

Anthropic CEO Dario Amodei（右）与JPMorgan CEO Jamie Dimon（左）在纽约同台亮相

就在同一天，Anthropic发布了面向金融服务的智能体套件：10个可部署的工作流参考架构、Moody&#x27;s MCP应用（覆盖6亿家公司）、8个新数据连接器。

同时，Excel、PowerPoint、Word插件正式上线，Outlook插件即将跟进。

https://www.anthropic.com/news/finance-agents

10个金融agent模板，覆盖从路演准备到合规筛查的完整工作链路：

搭路演材料、准备客户会前简报、读财报更新模型、做行业研究、审估值逻辑、跑总账对账、完成月末关账、核查财报一致性。

这些任务是金融机构每个季度都要反复跑的核心工作流。

同一天，Vals AI的金融基准Finance Agent v1.1上，Claude Opus 4.7以64.37%的准确率位列榜首。

https://www.vals.ai/benchmarks/finance_agent

据Anthropic披露：金融已经成为其第二大行业收入来源，仅次于科技；前50大客户里有40%来自金融机构。

Anthropic一次甩出10张底牌

覆盖前台到后台

这次发布的10个agent，每一个都不只是条提示词，Anthropic把每个模板的结构拆成三件套：

skills（任务指令与领域知识）

connectors（实时接入外部数据的授权通道）

subagents（为特定子任务单独召唤的辅助模型）

以路演搭建模板为例，理论上的工作流是这样的：

你递给它一份目标客户名单，它能跑出一张同类可比公司表格，在Excel里搭出财务模型，在PowerPoint里起草好演示文稿，还能在Outlook里备好一封覆盖函，等你回来审阅。

整个链条不需要你中途接手解释背景，上下文在应用之间自动贯通，像极了一个永远不下班的后台系统。

它的部署方式有两种。

一种是作为Cowork或Claude Code的插件，跟着分析师在桌面上跑，人仍然在场，随时可以接手。

另一种是作为托管智能体在Claude Platform上自主运行，能扛住跨越数小时的deal close、跑通一夜的关账。

Managed Agents自带了金融机构原本要工程团队搭半年才能搭起来的东西：长会话、按工具粒度的权限、托管的凭证库，以及在Claude Console中完整保留的审计日志。

10个模板加上两种部署形态，意味着金融机构原本需要数月工程化才能落地的agent 工作流，现在能在几天内上线。

但Anthropic在GitHub仓库提醒道：

这些智能体不执行交易，不批准客户入驻，不过账，也不作投资建议。所有输出，都需要专业人员复核之后才能使用。

https://github.com/anthropics/financial-services?utm_source=chatgpt.com

Claude长进了Excel、PowerPoint、Word

分析师桌面被改写

第二条线打的是应用层入口：Microsoft 365。

Excel/PowerPoint/Word add-ins 全量可用，Outlook add-in即将上线。

每个应用Claude各自能做什么，Anthropic都给了具体定义。

在Excel里，Claude能从监管申报文件和实时数据流中建财务模型，跨链接工作簿审查公式，并运行敏感性分析。

PowerPoint里，Claude起草deck，底层数字一变，slide自动跟着更新。

Word里，Claude按公司自有模板改信用备忘录。

Outlook里，Claude充当chief of staff，分诊收件箱、安排会议、按你的语气起草回复。

四件套之外，更关键的是上下文在四个应用之间自动接力。

分析师在Excel里建好的模型挪到PowerPoint，不用重新解释一遍；knowledge和context 跟着任务走，而不是被锁在某一个软件里。

这条接力把金融工作流的颗粒度从「应用」切成了「任务」。

原本一份完整的客户分析要在Excel算、PowerPoint画、Word写、Outlook发，每跳一次软件就要重新组织一次上下文。

现在Claude把四个软件「粘成」了一条流水线。

Claude Cowork这边还多了一个功能叫Dispatch。

分析师可以通过文字或语音，从任何地方给Claude派活。Claude在分析师离开工位时继续处理本地文件，等分析师回到工位，结果已经备好待审。

这条接入的意义比功能本身更重要。

Microsoft 365 是华尔街金融机构最常见的生产力栈之一。

把agent接进Office四件套，意味着金融机构不必等IT团队跨年级别的迁移就能落地：agent不要求你换工作台，而是它自己长进现有工作台。

对分析师来说，过去那种打开浏览器、贴一段提示词、再把结果粘回Excel的工作方式，即将成为过去式。

6亿公司数据塞进 Claude

金融数据生态被打通

第三条线打的是数据层入口。

就在同一天，Moody&#x27;s宣布通过MCP应用把自己的信用评级和合规数据流接进了Claude的工作环境。

这个数据流的规模是这样的：超过6亿家公众和私人公司的信息，20亿条所有权关系。

这意味着什么？

一个做信用分析的智能体，现在理论上可以查询其信用/风险数据、股权穿透关系，以及合规相关风险标记，全部来自Moody数据库，全部不需要离开Claude的界面。

这次新增的连接器有Dun&Bradstreet、IBISWorld、Third Bridge和Guidepoint。

更早之前，FactSet、PitchBook、LSEG、Morningstar、S&P Capital IQ已经接进来了。

金融数据平台，正在从「终端订阅费生意」，变成智能体的工具层。

AI智能体的能力取决于其可访问的数据和上下文，接入Claude生态的金融数据平台，包括FactSet、PitchBook、LSEG、Morningstar及新加入的Moody&#x27;s、Dun & Bradstreet等。

Moody’s的MCP app/server基于开放的Model Context Protocol标准，并非独家绑定Claude。

金融数据生态原来分散在数十个终端、数十个API上，每一家用一套登录、一套权限模型、一套查询语法。

MCP这种开放协议，正在把分散的数据层整合进一个统一的智能体工具层。终端层、API层之上，第三层智能体工具层（agent tool layer）正在成型。

这也是Anthropic正在押注的逻辑：谁先让这一层成为标配，谁就拿到下个十年的金融数据入口。

Anthropic闯入的

是一片红海

华尔街的AI赛道，早已不是一片空地。

JPMorgan、Goldman Sachs、Morgan Stanley，三家大行都已经在内部跑着AI助手，覆盖了从研究摘要到代码生成的各类工作。

Rogo，一家由前投行人创立的AI金融创业公司，估值已经到了20亿美元，服务超过250家机构客户，照样能做路演材料、研究报告和财务模型。

Hebbia在大规模数据集上跑并行查询，同一时间处理几百份文件的交叉比对。

Rogo的总裁Rahul Rekhi在发布当天表示：

我们的工具不绑定特定模型，基础模型越强，我们能做的事就越多，竞争对我们是利好。

Rekhi将Anthropic的进场定性为加速剂，而非对手。

但这里有个微妙的地方。

Anthropic在这次发布里每隔几段就强调一次：人在回路、审计日志、权限控制、专业人员复核。

金融行业一些环节，比如签字，这背后的确认和责任，在相应监管法规完善之前，AI还需要人类决策辅助。

EY Americas金融科技咨询负责人Scott Keipper向Business Insider称，未来的差异化竞争将集中在「领域数据、工作流设计和控制层」，产品能不能嵌进现有的风控架构，比模型跑分更重要。

从

工作流模板、数据连接器，到

Office嵌入，Anthropic这次卖的不是模型，而是一整套落地包，打包交付给金融机构的IT和合规团队，拆开就能用。

对于金融机构来说，原本只有头部大行能负担的agent工作流，现在中小机构和买方也能用上同一套基础设施：能力的获取门槛被拉平了。

对于AI公司来说，基础模型层之上的工作流层、控制层、合规层是下一个增长点：模型卷不动了，工作流的战场刚开始。

对于从业者来说，一些新角色的轮廓正在浮现：负责审核智能体输出的监督岗、设计工作流的架构师，以及合规审计、模型治理方向的岗位需求正在上升。

从更长的时间尺度看，懂agent怎么调度的分析师，会比只懂Excel的分析师值钱。

参考资料：

https://www.anthropic.com/news/finance-agents

秒追ASI

⭐点赞、转发、在看一键三连⭐

点亮星标，锁定新智元极速推送！