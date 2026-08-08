# 腾讯云Team Memory来了！

> 来源：微信公众号 | 2026-08-07

Memory支持团队记忆了！
腾讯云Agent Memory
2.0.0大版本已上线，全新升级
Team Memory
，将长期记忆能力从个人扩展到团队协作场景。
以后，团队与Agent协作过程中产生的
代码知识、项目文档、历史对话和工作方法
，都可以沉淀为团队长期记忆，在不同Agent之间共享，再根据Agent角色和具体任务按需装配，不用每次都重新介绍项目背景。
如果你已经有GitHub代码仓库、项目文档或历史Agent Session，也不用重新开始。Team Memory支持直接导入这些已有资产，并自动生成对应的
Wiki、CodeGraph、Chat Memory和Skill
，让Agent和团队成员快速接手已有项目。
今年5月
开源
以来，TencentDB Agent Memory已经获得不少开发者关注。项目开源80天，
GitHub Star数突破1
5,
000，并多次登上GitHub Trending日榜第一。
这次的Team Memory，也吸收了不少社区开发者的反馈和贡献。感谢每一位提Issue、提PR、参与讨论的朋友
。
//
支持统一管理
对话、文档、代码库、Skill四类
资产
以前的记忆基本只存对话，Team Memory把它扩成四类
👇
历史Agent Session整理成Chat Memory，记住聊过什么、定过什么。
项目文档生成Wiki，设计文档和运维手册变成能查的结构化页面。
代码仓库自动生成CodeGraph，让Agent看懂代码结构和调用关系，改一个函数会牵连到哪儿，动手前先算清楚。
一次干成的排障或代码评审，则沉淀为Skill，下次同类任务直接调用。
四类记忆能在团队内共享，也能分别装配给不同角色的Agent。修Bug的Agent优先使用CodeGraph、排障经验和相关Skill，做需求分析的Agent则加载Wiki、业务背景和历史讨论，不用把整个项目重新读一遍。
这些记忆资产与具体模型和Agent框架相互独立。团队以后更换模型或工具，已经积累的知识和经验仍然可以继续使用。
刚接手的项目也能用。已有的GitHub仓库、项目文档和历史Session可以直接导入，自动生成对应记忆，让新Agent从现有项目经验开始工作。
//Memory Hub：每条记忆都有Owner和版本
为了方便查看和管理记忆，这次全新版本还同步上线了Memory Hub控制台。
用户可以在里面创建
Team、Agent和Task
，把散在各处的记忆收到一处，生成、审核、授权、分享和装配都在这里完成。每条记忆归谁、更新到哪个版本、被哪些Agent用过，也可以直接查看。
实际使用时，用户先在Memory Hub中创建一个Team，再设置负责开发、评审或需求分析的不同Agent，并为它们配置需要使用的Wiki、CodeGraph、Chat Memory和Skill。
随后，Agent工具可以通过Proxy接入Team Memory。每次开启新会话时，用户选择本次会话所属的Team、使用的Agent和具体Task，系统就会自动把相关记忆和知识注入上下文。
例如，选择
“开发Agent+修复登录问题”
后，系统可以优先加载相关代码关系、历史排障记录和Skill；切换到
“需求分析Agent”
时，则加载项目Wiki和历史讨论。
新建的Chat Memory和Skill默认只有创建者可见，需要共享时由Owner主动发起，还可以按用户、角色和Agent分别设置权限。
//
OPC+多Agent、团队多成员都能用
这套能力不只服务多人团队。现在不少
开发者
处在
OPC
的状态：自己一个，加几个Agent 和AI工具，调研的、写代码的、找bug的
各自负责不同模块。
在Memory Hub里，可以把这些知识集中管起来，再分别装配。调研的Agent 拿业务背景和Wiki，写代码的拿CodeGraph，挑毛病的拿排障记录和评审Skill。各取所需，不用每开一个工具就把同一份背景交代一遍。
换成多人团队，同一套机制用来在成员之间共享和分发。一个人怎么用，一群人也怎么用。
T
eam Memory
更多新增特性，欢迎安装下载体验，也欢迎来主页点个Star或者提issue。
👉
Memory安装部署指南
👉
Memory项目主页
也欢迎来我们另一个破万星标的Agent infra项目CubeSandbox来逛逛
👉
Cube项目主页
-面向Agent，腾讯云全面加速中-