---
publish_time: 1789201800
link: https://mp.weixin.qq.com/s/4c9x7AjLWSD8ZunmhA0b_g
source: 量子位
status: confirmed
category: 国内
is_model_related: false
digest: |
  浙江大学 ZJU-REAL 团队开源 ageval（agent eval）评测底座，将待测 Agent 与运行环境通过插件彻底解耦：改一行配置即可让同一 dataset 在不同环境、不同 Agent 间切换。配套 CLI 与 skills，支持 coding agent 自主编写 benchmark、迁移测试集、自动化评测；本地 ageval view 可逐轮回放交互轨迹（环境准备/任务循环/评分耗时、工具调用明细），并提供 Hub 协作与结果共享，解决换 Agent/换环境重写胶水代码、分数不可追溯的痛点。
title: 配套CLI与Skills，浙大开源可插拔Agent评测底座
---

# 配套CLI与Skills，浙大开源可插拔Agent评测底座

来源：量子位
原文链接：https://mp.weixin.qq.com/s/4c9x7AjLWSD8ZunmhA0b_g

ZJU-REAL 团队 投稿
量子位 | 公众号 QbitAI
同一套模型，换一个coding agent运行时，测试得分和实际消耗往往大相径庭。
而在本地、Docker与各类云沙箱之间来回适配，又容易陷入写不完胶水代码的泥潭。
针对这一问题，
浙江大学ZJU-REAL团队
开源了
ageval
（agent eval）。它的核心思路是将待测Agent与运行环境通过插件彻底解耦：在配置文件中修改一行，同一份dataset就能在不同环境、不同Agent间自由切换运行。
配合专用的CLI与skills，ageval还能让coding agent自主编写benchmark、迁移已有测试集并执行自动化评测。
△
演示视频：配置一次评测，任意切换运行
功能一览：从本地调试到Hub协作
做Agent评测，开发者常遇到两个痛点：一是换个Agent或换套环境就得重写一遍适配脚手架；二是跑完只给出一个笼统的分数，中间卡在哪一步完全无法追溯。
ageval
覆盖了从本地复盘调试到云端结果共享的完整工作流。
本地轻量复盘：逐轮交互轨迹回放
评测未通过时，定位问题最需要看清Agent的实际执行轨迹。
在终端执行
ageval view
，即可在本地启动轻量Web轨迹查看器，按照
Jobs→Tasks
层级完整复盘每一次运行：
阶段耗时清晰可见：
明确展示环境准备（environment）、任务循环（run）与评分（evaluate）各个阶段的精确耗时；
交互事件逐轮展开：
完整对照Agent输入、工具调用（Tool Calls）、终端输出与模型回复，无需再在终端漫无目的地翻看滚屏日志；
单任务直接复现：
每个失败task均附带完整的重跑命令，方便在终端针对单一用例单独复现和单步调试。
△
本地Viewer中的一次运行轨迹与事件明细
插件中心：自由组合环境与Agent运行时
ageval将运行环境与Agent运行时均封装为标准插件，免去重复编写适配胶水代码的成本：
环境插件（Environment）：
支持Docker、E2B、Daytona以及Local本地宿主环境；
Agent运行时插件（Executor）：
默认支持通过ACP接入通用coding agent（如pi、Codex、Claude Code、OpenCode等），同时也原生收录了各类特化执行栈（如DeepSeek官方dsh、NVIDIA nooa、SWE-agent miniswe）。
如果需要切换执行环境或待测Agent，只需在配置文件profiles.yaml中修改对应声明，原有的dataset无需任何改动即可直接运行。
△
插件市场：浏览与接入环境插件和Agent运行时插件
插件详情页：依赖契约与运行参数一览
点击进入任意插件详情页，可以直观查看该插件对外export的服务、所依赖的环境capabilities，以及安装命令与参数配置示例：
△
dsh插件详情页：查看DeepSeek官方harness的插件配置与能力说明
△
nooa插件详情页：NVIDIA官方Agent运行时插件详情
公开榜单（Leaderboard）：环境与配置严格对齐的对比
许多公开benchmark往往只公布模型名称与得分，既没有说明使用的是哪套Harness，也没有标明沙箱环境版本与Prompt模版，外界往往难以真正复现。
在ageval Hub的公开榜单上：
每一项成绩都明确绑定了具体的Agent运行时版本与执行环境
（如Docker、E2B）
；
无论是更换底层沙箱还是调整工具调用策略，得分与资源消耗的变化都可以在榜单中横向对照；
每次提交均附带不可变的lock.json与完整轨迹文件，其他开发者可以直接拉取配置一键复现。
△
Hub Leaderboard榜单：查看不同环境与Agent组合下的真实评测成绩
Agents市场：沉淀与复用Agent资产
在实际业务中，调优出一套好用的Agent
（包括Prompt模版、工具链编排与执行逻辑）
通常需要投入大量的工程精力。
在ageval Hub上，团队可以直接将调优好的方案打包发布为Agent包：
完整包含Prompt模版、Tool定义以及底层插件依赖声明；
其他成员在运行评测时，只需指定--
agent<org/name@version>，即可直接拉取并在任意dataset上开箱即用。
△
Agents Hub：浏览、发布与复用已配置好的Agent包
点击进入单个Agent主页，可以进一步查看该Agent的配置详情、参与测评的模型列表与dataset历史记录。
△
dsh-agent详情页：查看Agent架构、配置参数与历史评测记录
Models视图：模型画像与横向PK
在针对业务场景进行模型选型时，团队通常关注两个核心问题：
该模型在不同的评测任务和不同的Agent架构下的整体表现如何？
在固定当前自研Agent架构的前提下，换用哪个模型能在成功率与调用成本之间取得最优平衡？
Models Hub：以模型为维度的综合画像
在
Models
Tab中，可以按照模型维度查看其在各类dataset与Agent组合下的解题成功率和调用成本：
△
Models Hub：以模型为主维度的全景观测面板
点击具体模型进入详情页，可以进一步查看该模型在不同dataset和不同Agent下的表现明细：
△
Model详情页：查看模型在各个dataset和不同Agent下的表现明细
固定Agent架构，横向对比不同模型
在Agent详情页中，可以固定同一套Agent运行时
（保持相同的Prompt策略与工具调度链）
，横向对比不同模型在同一个dataset下的代码生成质量与解题通过率：
△
在Agent Hub中比较Model表现：固定同一套Agent运行时，横向比对不同模型的解题效果
自动化评测：让coding agent驱动整个流程（Skills&CLI）
在本地开发环境中，只需为coding agent安装ageval CLI和配套skills：
uv tool install ageval-cli
npx skills add
ZJU
-
REAL
/ageval
安装完成后，你的coding agent就能理解ageval的CLI指令与数据结构规范。你可以直接吩咐它完成原本繁琐的工程操作：
自主编写新的benchmark，自动生成各task所需的run.py与evaluator.py；
将团队现有的评测脚本迁移为标准的ageval dataset；
自动拉起测试环境跑完指定评测矩阵，并汇总输出不同配置的对比分析报告。
△
Agent借助skills自动化运行评测
运行机制：为什么能做到自由插拔？
要既能无缝适配多种执行环境
（本机、Docker、云沙箱）
，又能兼容完全不同的Agent运行时，关键在于底层两项核心设计：
一次运行的五个标准阶段以及基于服务契约的插件机制。
一次运行的五个阶段
ageval的执行底座是一条确定性的单向流水线：
lock→environment→run→evaluate→record
无论运行过程是成功、失败、超时还是被外部中断，cleanup钩子都会在finally阶段可靠执行，彻底清理容器实例、注销网络并擦除临时凭证。
△
一次运行的生命周期：从静态lock、gold隔离、run任务循环到独立评分与evidence封存
ageval lock：在执行前静态拦截配置问题：
在实际拉起运行环境之前，系统会静态解析出依赖图
（ExtensionGraph）
。比对环境是否满足Agent插件声明的capabilities要求，并检查宿主Docker守护进程与API Key凭证。一旦校验未通过，在lock阶段就会直接报错终止，避免运行到半途才因环境缺失而崩溃。
独立评分与参考答案隔离（gold延迟上传）：
评分逻辑统一收敛在evaluator.py中，支持程序化断言测试、产物diff校验或LLM-as-a-judge。参考答案
（gold）
存放在tasks//evaluation/目录中，在Agent执行阶段环境内完全不可见；直到evaluate阶段才会挂载上传至打分环境。同时打分容器可以配置为network: none断开外网连接，彻底防止模型提前泄题或作弊。
不可变证据链归档（Evidence）：
运行结束后，执行配置与拓扑快照lock.json、评分细节result.json、完整交互事件轨迹trajectory.jsonl会被一体化封存归档，确保每一次评测结果都有据可查、可精确复现。
插件机制：基于export与inject的服务契约
框架内部没有面向特定环境或特定Agent的硬编码if/else分支，所有组件均通过声明式的服务契约实现解耦：
△
插件机制与依赖图：通过export与inject服务契约解耦环境与Agent，由ExtensionGraph驱动调度
服务声明（export与inject）：
环境插件（如docker、e2b、local）：
对外
export
提供environment服务，并声明自身支持的基础capabilities（如命令执行exec、文件上传upload、终端交互attach_stdio）；
Agent插件（如acp、dsh、nooa）：
通过
inject
声明自身需要的服务与capabilities（例如dsh声明需要环境提供exec与upload）。
在lock阶段校验并编排依赖拓扑：
静态检查requires⊆capabilities契约是否成立；
检查通过后生成调度拓扑，运行时基座严格依照拓扑关系分发调用，从而实现“基座代码完全不变，环境与Agent自由插拔替换”。
实战：零侵入接入DeepSeek官方harness
以DeepSeek开源的deepseek-harness（dsh）为例。接入dsh
不需要改动ageval框架的一行源码
，只需要提供一份简明直观的插件声明：
plugins/dsh/plugin.
yaml
——
Agent
插件声明（节选）
plugin_id
: dsh
slots
:
exclusive
:
-
id
: executor
#注册为
Agent
执行器
inject
:
-
service
: environment
#声明依赖环境服务
capabilities
: [exec, upload]
#要求环境提供命令执行和文件上传能力
对于使用者而言，调用dsh与运行普通Agent完全一致。原有的dataset保持原样不动，切换对应的配置文件即可直接执行：
#
1.
安装带dsh支持的extras
uv tool install
'ageval-cli[dsh]'
#
2.
dataset保持不动，指定dsh配置开跑
ageval run <dataset> --task <task-id> --profiles profiles.
dsh
.
yaml
快速开始
ageval现已正式开源。你可以通过pip/uv安装CLI，也可以直接从源码编译体验。
方式一：直接安装CLI（推荐）
#全局安装
CLI
uv tool install ageval-cli
#或一次性安装全部插件扩展
（含e2b,dsh,daytona等）
uv tool install
'ageval-cli[all]'
#检查安装
ageval -V
#为本机codingagent安装skills
npx skills add
ZJU
-
REAL
/ageval
直接运行公开的dataset，或本地dataset目录：
#查看公开可见的dataset
ageval registry list
#运行评测
ageval run <org>/<name>@<version> --task <task-id>
#本地启动复盘查看器
ageval view <org>/<name>@<version>
方式二：从源码体验最小示例
#克隆仓库
git clone
https
:
//github.com/ZJU-REAL/ageval.git
cd ageval
#安装项目依赖
uv sync --frozen --all-packages
#运行仓库自带的最小示例
uv run ageval run examples/datasets/minimal-demo --task terminal-jsonl-agg
#本地启动复盘查看器
uv run ageval view examples/datasets/minimal-demo
GitHub仓库：https://github.com/ZJU-REAL/ageval
项目主页：https://zju-real.github.io/ageval
文档与插件指南：https://zju-real.github.io/ageval/docs/
一键三连
「点赞」「转发」「小心心」
欢迎在评论区留下你的想法！
—
完
—
【学术投稿】请在工作日发送邮件至：
ai@qbitai.com
，标题注明【投稿】，并告诉我们：
你是谁
，
从哪来
，
投稿内容
附上
项目/主页链接
，以及
联系方式
。
🎓
我们会 (尽量) 及时回复你 :)
🌟 点亮星标 🌟
科技前沿进展每日见
