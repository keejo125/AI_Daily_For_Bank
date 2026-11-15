---
publish_time: 1791898836
link: https://mp.weixin.qq.com/s/S-UiuIV1HMND7WF0-7F7cA
source: 阿里云基础设施
status: confirmed
category: 国内
is_model_related: false
digest: |
  阿里云基础设施讲解开源 RL 后训练框架 VeRL（支持 PPO、GRPO）。随模型能力升级，RL 从单次文本生成扩展到多轮决策的 Agent RL，典型如 coding agent：读问题、改代码、跑测试、按结果修正，由测试通过给奖励。环境从训练系统外部设施变为训练过程一部分，Agent Sandbox 打通「环境执行层」，让多轮交互的奖励可在真实环境验证。
title: VeRL后训练实战： Agent Sandbox如何打通Coding Agent的“环境执行层”？
---

# VeRL后训练实战： Agent Sandbox如何打通Coding Agent的“环境执行层”？

来源：阿里云基础设施
原文链接：https://mp.weixin.qq.com/s/S-UiuIV1HMND7WF0-7F7cA

1 背景与概述
强化学习（Reinforcement Learning，RL）是一类通过与环境交互来学习决策的机器学习方法。在该范式中，智能体（agent）观察环境状态并执行动作，环境根据动作返回新的观察结果与奖励，训练目标是学习一个策略，使其在长期交互中获得的累计奖励最大化。与监督学习不同，强化学习的监督信号不来自人工标注的标准答案，而来自环境对动作结果的反馈，环境本身因此构成训练数据的来源。
在大语言模型的后训练阶段，强化学习首先以基于人类反馈的强化学习（RLHF）的形式被广泛采用：训练系统对模型生成的回答进行评分，再通过 PPO、GRPO 等算法更新模型参数。对于数学、代码等结果可自动验证的任务，奖励可以直接来自程序化校验，例如单元测试是否通过，这类方法通常称为可验证奖励强化学习（RLVR）。VeRL 是面向这一阶段的开源强化学习训练框架，支持 PPO、GRPO 等算法，并可组合多种训练与推理引擎。
随着模型能力的提升，强化学习的应用对象从单次文本生成扩展到多轮决策任务，即 Agent 强化学习。在这类任务中，模型的动作不再局限于生成文本，还包括调用工具、执行命令、读写文件等；环境返回的执行结果作为观察结果进入模型上下文，模型据此规划下一步动作，形成模型、工具与环境之间的多轮交互循环。coding agent 是其中的典型场景：模型需要在代码仓库中阅读问题、修改代码、运行测试，并根据测试结果继续修正，最终由测试是否通过给出奖励。
这一变化使环境从训练系统的外部设施转变为训练过程的一部分：奖励计算需要在真实环境中执行验证，多轮交互则要求环境贯穿整个生成过程。训练系统中承担环境创建、动作执行与结果返回职责的部分，称为环境执行层。以 coding agent 为例，环境执行层提供隔离的沙箱实例，模型生成的命令（读写文件、运行测试等）在实例内执行，执行结果（标准输出、错误输出、文件内容等）再由其返回训练系统。环境执行层位于训练框架与底层算力之间：对上，它向训练循环提供统一的环境操作接口；对下，它调度隔离的算力资源承载真实的代码执行。
以多轮交互路径为例，环境执行层与训练框架的交互流程如下图所示。
如图所示，一次完整的环境交互可分为三个阶段：一是环境供给，训练框架经环境执行层申请并创建沙箱实例；二是多轮交互，模型生成的动作经环境执行层在沙箱内执行，观察结果沿原路返回，模型据此生成下一步动作，如此循环直至任务完成；三是验证与释放，在沙箱内应用补丁并运行测试得到奖励，随后销毁沙箱、回收资源。奖励计算路径（见第 3 节）可视为该流程的特例：省略其中的多轮交互阶段，仅在最终答案生成后执行一次验证。
由于训练系统需要持续提供隔离、可快速供给、可并发执行的沙箱环境，环境执行层以何种方式接入训练框架，直接影响训练信号的形态与可训练的任务类型。
具体而言，对于 coding agent 的训练，环境执行层存在两个可行的接入位置：奖励（reward）计算环节与生成（rollout）环节。接入位置决定了训练信号的形态，也决定了最终能够训练出的 agent 能力。
本文以阿里云智能体沙箱 Agent Sandbox 容器版 作为环境执行层，分析其接入 VeRL 后训练的两条路径：仅参与奖励计算的路径，以及参与生成过程的路径（AgentLoop）。文中给出 AgentLoop 路径下沙箱的两种供给方式（通过 ACS 预热池申请、在集群内直接创建）、轨迹数据的回流方案，以及 GPU 训练集群与沙箱弹性算力的隔离方案。本文内容不限于接入示例，还包括完整的生产环境操作手册，覆盖 ACK 组件安装、预热池创建、RayCluster 部署、训练启动与分阶段验证，对应我们在 VeRL 三个 recipe、Harbor 定制分支与 Rollout Server 上的工程实现。
本文使用以下术语：
rollout
：模型根据 prompt 生成回答或动作的过程。在普通 RLHF 中通常指一次文本生成；在 Agent 强化学习中则包含多轮工具调用与环境交互。
reward
：训练系统对模型输出的评分。在代码任务中，奖励通常来自真实执行结果，例如补丁能否应用、测试能否通过。
AgentLoop
：模型、工具与环境进行多轮交互的循环。模型输出动作，环境返回观察结果，模型据此继续下一步动作。
沙箱接入 VeRL 的两条路径训练的是两种不同的能力，工程复杂度也不相同。第一条路径仅参与奖励计算：模型一次性生成最终答案，由奖励函数创建沙箱执行测试，沙箱不参与生成过程。第二条路径让沙箱参与生成过程：模型在 rollout 中反复操作沙箱，环境返回的观察结果进入模型上下文，但这些观察 token 不参与策略损失计算。第二条路径是本文的重点。
AgentLoop 路径的落地需要三个环节协同配合：一是沙箱供给，即环境层从何处获得隔离的执行环境；二是 Agent 编排，即由哪个组件驱动模型与环境的多轮交互；三是轨迹回流，即 token 级数据如何回到训练器。其中第三个环节最容易被低估：response_mask 的赋值正确性直接决定策略梯度，无论将环境 token 误标为参与损失，还是将模型 token 误标为不参与损失，都不会触发任何报错，训练照常进行，而梯度已经失真。
本文采用的方案是：沙箱供给下沉到 Harbor 环境层，通过 E2B 协议从 ACS 预热池申请沙箱，或者通过 Kubernetes CRD 在集群内直接创建沙箱；轨迹数据经一台旁路录制的 LLM Proxy 回流；外部 Agent 无需任何代码改动（见第 4 节）。
2 Agent Sandbox 容器版简介
阿里云智能体沙箱 Agent Sandbox 容器版是面向 AI Agent 推出的沙箱产品，其能力与 Agent 强化学习的负载特征相匹配：
Serverless 容器算力
：以 Pod 为粒度秒级供给，使用方无需为沙箱单独维护节点池；大规模并发创建与快速销毁是产品原生能力。
SandboxSet 预热池
：预先创建一组沙箱副本，申请后即可立即使用，消除了拉取镜像与安装依赖带来的分钟级冷启动；副本被分配后，预热池自动补充。
双协议接入
：同时兼容 E2B SDK（Sandbox.create()、run_code、files、commands 等 HTTP 接口）与 Kubernetes CRD（OpenKruise 的 Sandbox、SandboxSet、SandboxClaim）。前者适合应用侧集成，后者适合平台侧编排。
申请时替换镜像
：申请沙箱时可通过 e2b.agents.kruise.io/image 元数据将主容器镜像替换为任务镜像，同一个预热池因此可以服务任意多个使用不同镜像的任务。
安全隔离
：提供专用沙箱算力类（alibabacloud.com/compute-class: agent-sandbox）、网络策略，并默认关闭服务账号令牌挂载（automountServiceAccountToken: false），适用于执行不可信代码的场景。
组件形态上，该产品由两部分组成：ack-agent-sandbox-controller 负责 Sandbox 生命周期管理；ack-sandbox-manager 是兼容 E2B 协议的沙箱管理 API Server，部署在 sandbox-system 命名空间。
3
接入路径一：沙箱仅参与奖励计算
该路径对训练框架的侵入最小。模型在 rollout 阶段一次性生成答案，沙箱仅出现在评分阶段，负责验证最终输出，不参与生成过程。
VeRL 的自定义奖励函数放在独立文件中，通过 reward.custom_reward_function.path 与 reward.custom_reward_function.name 两个配置项指定；函数参数包括 data_source、solution_str、ground_truth 与 extra_info。接入 ACS 沙箱之后，评分过程依次为：通过 E2B SDK 创建沙箱（模板指定预热池，元数据指定任务镜像）；将补丁或代码写入沙箱；在沙箱内执行测试；返回分数与结构化的执行信息。
# custom_reward.py —— 仅评分路径示意
from
e2b_code_interpreter
import
Sandbox
def
compute_score
(
data_source, solution_str, ground_truth, extra_info=
None
):
sbx = Sandbox.create(
template=extra_info[
"sandbox_set"
],
# ACS 预热池
metadata={
"e2b.agents.kruise.io/image"
: extra_info[
"docker_image"
]},
timeout=
900
,
)
try
:
sbx.files.write(
"/testbed/patch.diff"
, solution_str)
r = sbx.commands.run(extra_info.get(
"test_cmd"
,
"python -m pytest -x"
), timeout=
600
)
passed = r.exit_code ==
0
return
1.0
if
passed
else
0.0
, {
"test_exit"
: r.exit_code,
"stderr_tail"
: r.stderr[-
2000
:]}
finally
:
sbx.kill()
# 清理逻辑必须使用 finally 语义
该路径的优点是侵入小：VeRL 对代码环境无感知，真实执行完全由奖励函数自行封装。代价是模型在生成最终补丁之前无法获得 pytest 输出、文件内容与命令反馈，因此学到的策略更接近一次性解题，而不是对仓库进行探索。
4 接入路径二：沙箱参与生成过程（AgentLoop）
要训练能够自主读文件、执行测试、根据报错继续修改的 agent，沙箱必须参与 rollout，而不能仅出现在最终评分环节。
4.1
response_mask 赋值规则
该路径的核心约束是 AgentLoopOutput 中 response_mask 的赋值规则（见 verl/experimental/agent_loop/agent_loop.py 第 90 至 108 行）。模型生成的动作 token（例如 bash 命令、编辑操作与最终回答）赋值为 1；沙箱返回的观察 token（例如标准输出、错误输出、文件内容与测试日志）赋值为 0。两类 token 都会进入 response_ids、input_ids、attention_mask 与 position_ids，但只有赋值为 1 的 token 参与 actor 损失计算。换言之，环境反馈进入轨迹，但不参与策略梯度。
4.2
整体架构与数据流
AgentLoop 路径的落地需要三个环节协同：沙箱供给由 Harbor 环境层对接 阿里云智能体沙箱 Agent Sandbox 容器版；Agent 编排由 Harbor Trial 承担；轨迹回流由一台旁路录制的 LLM Proxy 完成。外部 Agent 无需任何代码改动。
整体架构如下。训练循环（PPO 或 GRPO trainer）以异步方式驱动 rollout。RemoteAgentLoop 是与 Agent 框架无关的核心组件，通过 agent_loop 注册表接入，负责会话生命周期管理、轨迹重建与 tokenization。Harbor Trial 运行在 RemoteAgentLoop 内部，作为其任务执行单元，负责驱动外部 Agent 并编排环境。RemoteAgentLoop 同时与一台兼容 OpenAI 接口的 LLM Proxy（以 Ray actor 形式运行）交互： LLM Proxy 将 Agent 的模型调用转发至 VeRL 的 SGLang rollout 引擎，并以旁路方式记录每次调用的 token_ids 与 logprobs。Harbor Trial 通过环境层获取沙箱，环境层提供两条通道：E2BEnvironment 经 HTTP 访问 ack-sandbox-manager，从 ACS 预热池申请沙箱；ACKEnvironment 经 Kubernetes API 使用 OpenKruise CRD 直接创建 Sandbox Pod。
一次 rollout 的完整数据流分为以下五步：
RemoteAgentLoop 向 LLM Proxy 注册以 trial_id 为键的会话。
Harbor Trial 驱动外部 Agent（例如 SWE-Agent，无需修改任何代码），Agent 的 LLM 客户端地址被指向 LLM Proxy，地址格式为 http:////v1。
环境层从 ACS 预热池申请沙箱，或在集群内直接创建 Sandbox Pod；Agent 在沙箱内阅读 Issue、修改代码、运行测试。
Agent 的每一次 LLM 调用都经 LLM Proxy 转发至 VeRL 的 rollout 引擎，同时被旁路记录 token_ids 与 logprobs。
Agent 运行结束后，RemoteAgentLoop 从录制数据重建 AgentLoopOutput，交回训练循环。
上述步骤对应的组件交互时序如下图所示。与第 1 节的概念性流程相比，该图体现了 RemoteAgentLoop 方案的实际组件划分：Harbor Trial 运行在 RemoteAgentLoop 内部，模型调用统一经 LLM Proxy 转发并旁路录制，沙箱供给由环境层的两条通道完成。
4.3
沙箱供给的两条通道
通道一：E2B 协议加 ACS 预热池（E2BEnvironment，推荐）。
该通道经 ack-sandbox-manager 的 E2B 兼容 HTTP API 从 SandboxSet 预热池申请沙箱。申请请求携带 e2b.agents.kruise.io/image 元数据，由 ACK 的 E2B 网关将主容器镜像替换为任务镜像（task.toml 中的 docker_image）。借助这一机制，同一预热池可以服务任意多个任务镜像，无需逐任务预热模板。沙箱就绪后，Agent 的命令与文件操作经 sandbox-gateway 数据通道进入沙箱执行；Trial 结束后沙箱即释放，SandboxSet 自动补充预热副本。该通道适用于任务镜像可预先构建（见第 6 节的 upload-images 命令）、并发较高的训练场景，是本文操作手册采用的主要方式。
通道二：Kubernetes CRD 直接创建（ACKEnvironment）。
该通道经 Kubernetes SDK 直接创建 Sandbox Pod，支持任意任务 Dockerfile 在集群内构建（使用远程 BuildKit）；pod_overrides 用于注入节点亲和性、容忍与资源覆盖；memory_limit_multiplier 按 task.toml 的声明放大内存。该通道适用于各任务镜像差异较大、任务频繁变化、无预热需求的场景。
需要说明 Agent 进程的运行位置：Agent 运行在训练集群的 Ray worker（TaskRunner actor）内，通过 Harbor Trial 的环境接口远程操作沙箱。阅读 Issue、修改代码、运行测试全部发生在沙箱中，训练节点不执行任务代码。
4.4
轨迹回流：旁路录制的 LLM Proxy
LLM Proxy 位于 Agent 与训练引擎之间。Agent 结束后，RemoteAgentLoop 从录制数据重建 AgentLoopOutput：LLM 生成的补全片段赋值为 1，轮次之间的工具消息与用户消息赋值为 0。边界判定的依据是 LLM Proxy 转发时的录制事实，即哪一段 token 由本次 LLM 调用生成，而不是对最终消息流的重新解析。
这一设计是相对于在框架内组装轨迹的常规做法而言的。以 ToolAgentLoop 为例，其状态机在调用工具、拼接上下文的同时，由框架代码为每段 token 追加 mask；这种方式下 mask 的追加同样是自动的，但每接入一个新的 Agent 框架，该边界逻辑就需要重新实现并验证一次，而 mask 赋值错误没有任何显式症状，策略梯度会在无告警的情况下失真。旁路录制将边界逻辑集中到 LLM Proxy 与 RemoteAgentLoop 一处实现，对任意 Agent 框架均可复用。
LLM Proxy 的录制设计还决定了两个工程行为。第一，采用失败开放（fail-open）策略：单个 rollout 失败（沙箱崩溃、Agent 超时）不会让 run() 抛出异常，而是返回一个仅含结束符的合法输出，单条失败样本不会中断整个批次。第二，token 级数据有保证：logprobs 直接来自 rollout 引擎的录制，无需事后使用参考模型重新计算，避免引入离策略（off-policy）偏差。
需要指出的是，旁路录制降低了但并未完全消除 response_mask 与 tokenization 的风险。录制侧自身可能出错的位置包括：工具调用解析（hermes 等格式）、重试时的会话重置与去重、Agent 侧对话模板与录制 token 边界的一致性。这些错误同样没有显式症状。相应的对策有两点：其一，重建逻辑集中在 LLM Proxy 与 RemoteAgentLoop 一处实现，对任意 Agent 框架只需实现一次；其二，以 rollout 侧与训练侧 log-prob 的一致性作为静默错位的检测手段，remote_megatron_sglang 的端到端验证即采用这一判据，两侧 log-prob 的 Pearson 相关系数约为 0.999。
4.5
两条路径的对比
路径
模型能否获得环境反馈
适用任务
主要风险
仅参与奖励计算
不能，模型仅在生成最终答案后获得评分
一次性补丁生成、代码题、SQL 输出
生成阶段无法获得环境反馈，单次生成中的错误不可恢复
参与生成过程（本文重点）
可以，标准输出、错误输出与文件内容均进入上下文
多轮 coding agent、SWE-bench 类任务
轨迹更长、token 消耗成倍增加：轨迹级奖励的信用分配（credit assignment）方差更大、轨迹长度长尾更明显；response_mask 与 tokenization 易错（旁路录制可降低该类风险，见 4.4 节）
两条路径的奖励均为轨迹末端的稀疏标量（测试是否通过），除非引入轮次级奖励或过程奖励。AgentLoop 路径的收益不在于训练信号的密度，而在于生成过程的可迭代性：环境反馈进入上下文，推理阶段的错误可以在后续轮次中得到修正。其代价是同一个末端奖励需要分配到更长、更稀疏的动作序列上（大量观察 token 不参与损失，动作 token 分散在长上下文中），优势值（advantage）估计的难度高于仅评分路径。
两条路径可以组合使用：AgentLoop 负责多轮探索，最终评分仍在干净的沙箱中应用补丁并执行测试。
5 GPU 训练集群与沙箱算力的隔离
VeRL 的 actor、critic、reference 与 rollout 引擎以 GPU 资源为主要瓶颈；沙箱负载以 CPU、内存、磁盘 IO 与网络为主。两类负载同节点部署会相互干扰，因此本方案将二者隔离部署。训练侧组件以 KubeRay RayCluster 形式部署在 ACK 集群的 GPU 节点池中，包括：PPO/GRPO trainer（运行于 head 节点，不占用 GPU）、SGLang 或 vLLM rollout 引擎（运行于 GPU worker）、RemoteAgentLoop 与 LLM Proxy（Ray actor）、Harbor Trial（环境编排）。沙箱以 SandboxSet 预热池形式运行在 ACS Serverless 算力之上，申请时按任务替换镜像，到期自动回收并自动补充，E2B 协议与 Kubernetes CRD 两条通道均可使用。
容量规划因此分为两条相互独立的基线：
GPU 侧
：token 吞吐、rollout 延迟、actor 更新时间、权重同步耗时。
沙箱侧
：kubectl get sbs 显示的可用副本数、申请 QPS 与申请超时率、沙箱平均存活时长、镜像替换耗时。
奖励由 Harbor verifier 在沙箱内执行测试得到，其开销计入沙箱侧，不构成独立基线。
此外还有一组训练质量侧的观测指标（不属于容量基线）：成功率、超时率，以及补丁应用失败、测试失败、基础设施失败的分类计数，用于失败归因。更进一步的隔离见 7.3 节：通过 Rollout Server 可将沙箱执行从训练集群彻底剥离。
6
任务数据组织方式
coding agent 的样本除 prompt 与 answer 之外，还需要声明环境启动方式、仓库位置、测试命令、网络策略与超时时间。本方案采用 Harbor 任务目录作为数据约定（Harbor 是开源的 agent 试验框架，负责环境、Agent、Verifier 三者的编排），目录结构如下：
/swebench/train/
django__django-16379/
task.toml
# 任务配置：镜像、资源、metadata（写入 extra_info.task_metadata）
instruction.md
# 作为 user prompt
environment/
# 可选：任务 Dockerfile（ACK 后端可在集群内构建）
tests/
# 可选：测试资产
数据集记录由 recipe 从任务目录自动生成 parquet 文件，关键字段如下：
{
"data_source"
:
"harbor"
,
"prompt"
:
[{
"role"
:
"user"
,
"content"
:
""
}],
"reward_model"
:
{
"style"
:
"rule"
,
"ground_truth"
:
""
},
"extra_info"
:
{
"task_id"
:
"django__django-16379"
,
"task_metadata"
:
{
"environment"
:
{
"docker_image"
:
"registry/swebench/django-django-16379:v1"
}}
}
}
其中 docker_image 是任务初始环境的引用。工程实践上，建议将仓库检出与依赖安装固化到任务镜像中，使用 harbor admin upload-images 命令一次性完成增量构建。该命令通过任务目录内容哈希与远端镜像摘要进行双重校验，--skip-unchanged 参数用于跳过已同步的任务，--diff-only 参数用于 CI 中的漂移检测。如此，训练阶段只需执行申请沙箱、执行动作、评分、释放四个步骤。
7 工程实现
7.1
VeRL 侧：三个 recipe 与一个抽象层
VeRL 内置的 AgentLoop 不支持第三方 Agent 集成、token 级捕获与分布式沙箱，我们以 recipe 形式补齐这些能力，全部可以在未经修改的上游 VeRL main 分支上运行。
Recipe
定位
关键能力
recipe/agentic
生产环境全功能版本
LLM Proxy 支持 Ray actor 与独立 Kubernetes 服务两种部署形态；提供 RemoteAgentLoop；与 Harbor/ACK 深度集成（SandboxClaim 预热池、BuildKit 构建）；支持训练推理分离部署、按训练步耗时统计、任务提交 SDK
recipe/remote_agent
面向上游的解耦版本
Agent 框架通过 runner 注册表接入，Harbor 仅为其中一种 runner；纯 YAML 配置；通过兼容层（shim）与 sitecustomize 机制实现不修改 VeRL 主仓库代码，已在 0.9.0.dev 与 0.10.0.dev 版本验证；附带完整的集群操作手册
recipe/remote_megatron_sglang
存算分离编排
训练（Megatron，PyTorchJob）与推理（SGLang，RoleBasedGroup）均运行于 Ray 之外，VeRL 仅承担编排角色、不参与 GPU 计算；权重同步方式可插拔（nccl_http 方式同步 290 个 tensor 约 0.8 秒每步，另有 store、mooncake 方式）；已在 ACK 2×8×H20 环境完成端到端验证，rollout 与训练侧 log-prob 的 Pearson 相关系数约为 0.999
第三个 recipe 建立在从上游 PR
#6422
移植的 verl/remote_backend/ 抽象之上：RemoteBackend 抽象基类仅约束生命周期（from_config、reconnect_handle、destroy）、权重同步与 checkpoint、单 forwarder 并行契约，计算与更新的签名留给具体后端实现，训练引擎与采样引擎因此可以异构组合。该抽象处理的是引擎的部署位置，与本文重点讨论的环境供给问题相互独立；训练集群虚拟化之后，沙箱层的弹性即成为吞吐的主要杠杆。
7.2
Harbor 侧：ACK 上的环境管理
基于 Harbor 0.21.0 的定制分支（release-dev-e5e46809 与 release-dev-e5e46809-rollout-server）包含以下四项改动：
新增 ACKEnvironment：通过 Kubernetes SDK 直接创建 Sandbox Pod，支持镜像拉取密钥（image_pull_secret）、按 task.toml 声明放大内存（memory_limit_multiplier）、灵骏节点的容忍（tolerations）配置、通过 pod_overrides 注入节点亲和性与资源覆盖以将 Pod 固定到指定节点池、通过远程 BuildKit 构建镜像，以及通过 OpenKruise SandboxClaim 从预热池申请沙箱。
E2B 预热池支持按任务替换镜像：E2BEnvironment 新增 sandbox_set_name 与 override_claim_image 参数，申请请求携带 e2b.agents.kruise.io/image 元数据，由 ACK 的 E2B 网关将主容器镜像替换为任务镜像。借助该机制，一个预热池可以服务几百个 SWE-bench 实例各自不同的镜像，无需逐任务预热模板，这是 ACS 预热池支撑强化学习负载的关键机制。
新增 harbor admin upload-images 命令，实现镜像批量构建的增量治理（见第 6 节）。
凭证隔离：E2B 与 ACK 的凭证作为环境构造参数（ambient_env）注入，而非使用全局环境变量，同一 worker 进程内多个 trial 并发时凭证互不干扰。
7.3
Rollout Server：
rollout 执行与训练集群分离
Rollout Server 是运行在 Kubernetes 上的试验执行服务：接收任务打包，在服务端构建环境、运行 Agent、执行 Verifier、存储完整的 TrialResult。Harbor 定制分支内置了该服务的客户端（harbor/rollout/），用法如下：
harbor
run --path ./my-task -a swe-agent -m 
\
--rollout-server http://rollout.example.com:
8080
\
--rollout-token 
\
--rollout-queue default
\
--rollout-llm-proxy http:////v1
其价值随训练规模递进：
训练集群不再需要沙箱相关依赖
：
本地仅打包 task.tar.gz 提交、轮询状态、取回结果，GPU 节点不再需要 Docker、沙箱凭证与 Agent 依赖，回归纯训练角色。
配额与优先级
：
通过类似 Spark 的配额队列管理多个训练任务共享沙箱资源池时的并发与速率；配额占满时返回 HTTP 429 并附带 retry_after_hint 提示，客户端在预算内退避重试。
服务端重试与断点续跑
：
业务失败由服务端按 --rollout-retries 指定的次数重试；本地进程崩溃后重新执行同一命令，可经 trial 目录中的 rollout.json 标记文件重新连接原有运行，而非重复提交；--rollout-detach 参数支持提交后即退出、事后收集结果，这是数十小时长时训练下的必要能力。
强化学习适配
：
--rollout-llm-proxy 将 VeRL LLM Proxy 的地址透传给服务端的 Agent，token 与 logprob 的捕获链路在远程执行模式下保持不变。
能力协商
：
GET /api/v1/capabilities/environments 接口暴露服务端支持的环境后端；ACK 后端接受任意任务 Dockerfile 在集群内构建，E2B 后端原本要求镜像与池模板一致，镜像替换能力放宽了这一限制。
概括而言， LLM Proxy 解耦的是 Agent 与训练框架之间的数据通道，Rollout Server 解耦的是 rollout 执行与训练集群之间的部署关系。
8 部署与运行操作手册
本节以 recipe/remote_agent（上游 VeRL + Harbor + SWE-Agent + ACS 预热池）为例说明部署流程；如需生产环境的全功能版本（独立部署的 LLM Proxy、训练推理分离、按步耗时统计），可改用 recipe/agentic，两者的环境准备工作一致。文中所有  需替换为实际值。
8.1
前置条件
已创建 ACK Pro 集群（包含 GPU 节点，本文示例使用单节点 8×H20），并已安装 KubeRay Operator。
已开通 阿里云智能体沙箱 Agent Sandbox 容器版：acs-virtual-node 组件版本不低于 v2.17.0，Kube Scheduler 已升级至集群版本对应的规格。
训练镜像已按照 remote_agent/docker/Dockerfile 构建，包含 VeRL、recipe、Harbor 定制分支、TransferQueue 0.1.8 以及 5.6.0 以下版本的 transformers。
已准备模型 PVC（只读，挂载路径 /mnt/models）与数据 PVC（支持多节点读写，挂载路径 /mnt/data）。
8.2
安装 Agent Sandbox 组件
在控制台的组件管理页面依次安装以下组件：
Ingress Controller（例如 ALB），用于从集群外访问 sandbox-manager；如仅在集群内访问，可使用 Headless Service sandbox-manager.sandbox-system.svc.cluster.local。
ack-agent-sandbox-controller，版本不低于 v0.5.14-release.1；首次安装需授权 AliyunCSManagedAgentSandboxRole。
ack-sandbox-manager，版本不低于 v0.6.0；需配置 className、E2B 的 domain 与 adminApiKey。
安装完成后，sandbox-system 命名空间下会出现 sandbox-manager 的路由。
8.3
创建 SandboxSet 预热池
apiVersion: agents.kruise.io/v1alpha1
kind: SandboxSet
metadata:
name: swe-warm-pool
# 训练脚本中 SANDBOX_SET 使用该名称
namespace: default
spec:
replicas: 32
# 预热副本数不小于单步 rollout 并发数
template:
metadata:
labels:
alibabacloud.com/acs:
"true"
alibabacloud.com/compute-class: agent-sandbox
alibabacloud.com/compute-qos: default
spec:
automountServiceAccountToken:
false
containers:
- name: sandbox
image: 
# 仅为启动占位，申请时按任务替换
resources:
requests: { cpu:
"2"
, memory: 8Gi }
limits:   { cpu:
"2"
, memory: 8Gi }
配置时需注意以下三点。第一，replicas 按 train_batch_size 乘以 rollout.n 估算；预热池被申请后会自动补充，但补充速率有限，池容量过小会出现申请超时（ReadTimeout）。第二，配合 override_claim_image 使用时，池内镜像仅为启动占位，可通过 ops.alibabacloud.com/update-with-image-cache: "true" 注解加速镜像替换。第三，如不同任务需要差异化资源，可开启原地资源调整（scaling.alibabacloud.com/enable-inplace-resource-resize: "true"），并在申请时通过 e2b.agents.kruise.io/cpu-request 与 e2b.agents.kruise.io/cpu-limit 元数据声明规格。
创建完成后执行 kubectl get sbs 验证，可用副本数应等于 replicas。
8.4
准备任务数据与镜像
harbor
datasets download swebench-verified --output /mnt/data/swe-bench-verified
mkdir
-p /mnt/data/swebench/{train,val}    # 按
400
/
100
分发任务子目录
# 增量构建沙箱镜像（一次性执行），buildkitd 为集群内 BuildKit 服务
harbor
admin upload-images
\
--tasks-dir /mnt/data/swe-bench-verified
\
--registry /swebench
\
--remote-buildkit tcp://buildkitd:
1234
\
--sanitize-image-names
\
--update-config --skip-unchanged --parallel
8
8.5
部署 RayCluster
RayCluster 的完整配置较长，可参见 recipe 仓库中的模板，此处说明三处最易出错的配置：
PYTHONPATH 必须包含 /workspace，使 remote_agent/compat/sitecustomize.py 能够在每个 Python 进程（包括 Ray worker）启动时自动加载，完成兼容配置的注入与 agent loop 的注册。
head 节点的 num-cpus 需设置为 "0"。 LLM Proxy 与 TaskRunner actor 均以 num_cpus=0 申请资源，该设置保证它们在 head 节点零 CPU 配额的情况下仍可调度。
数据 PVC 需同时挂载到 worker 节点。V1 版本的 TaskRunner actor 运行在 worker 节点上，因此 data.harbor_cache_dir 必须指向共享 PVC（例如 /mnt/data/.harbor_cache）。
此外需注意两点：E2B 相关的三个环境变量（E2B_API_KEY、E2B_API_URL、E2B_SANDBOX_URL）需在 head 与 worker 上同时配置，因为 V1 TaskRunner actor 在 worker 上执行沙箱交互；E2B 模式通过 HTTP API 访问沙箱，无需 Pod 操作权限，而 ACK 直接创建模式（SANDBOX_MODE=ack）需额外配置 pods、pods/exec、pods/log 等资源的 RBAC 权限。
8.6 启动训练
在 head pod 内执行以下命令：
export
MODEL_PATH=/mnt/models/Qwen2.
5
-
7
B-Instruct
export
TRAIN_TASKS=/mnt/data/swebench/train
export
VAL_TASKS=/mnt/data/swebench/val
export
SANDBOX_MODE=e2b
export
SANDBOX_SET=swe-warm-pool
bash
remote_agent/scripts/train_harbor_sweagent.sh
\
trainer.n_gpus_per_node=
8
\
actor_rollout_ref.rollout.tensor_model_parallel_size=
8
\
data.train_batch_size=
32
\
actor_rollout_ref.rollout.n=
4
\
data.max_prompt_length=
8192
\
data.max_response_length=
1024
\
trainer.total_training_steps=
100
\
trainer.logger='[console]'
脚本自动完成三项处理：将 advertised_host 设为本节点 IP 并经 Hydra 传入配置（Ray worker 从序列化配置中继承）；为模型名添加 openai/ 前缀（swe-agent 通过 litellm 调用模型，需要该前缀才能路由到 LLM Proxy）；注入 sandbox_set_name 与 override_claim_image=true 参数。
如使用 ACK 直接创建模式（不经预热池，支持任意 Dockerfile 集群内构建），按以下方式设置环境变量：
export
SANDBOX_MODE=ack
export
SANDBOX_NAMESPACE=
export
SANDBOX_IMAGE_PULL_SECRET=
export
SANDBOX_MEMORY_LIMIT_MULT=4
bash remote_agent/scripts/train_harbor_sweagent.sh ...
8.7
验证数据流
阶段
日志特征
含义
数据集物化
materialized dataset: train=...parquet
Harbor runner 已从任务目录生成 parquet
权重加载
Loading weights: 100%
actor 模型已加载到 GPU
推理引擎就绪
SGLang http server / Capturing num tokens
rollout 引擎初始化完成
LLM Proxy 启动
Proxy server actor created at http://:
LLM Proxy 就绪（TaskRunner actor 内）
rollout 开始
Training Progress: 0%
首步 rollout 启动
LLM 流量
[GENERATE] prompt_ids length=
SWE-Agent 正在调用 LLM Proxy，真实生成已发生
轨迹重建
Successfully converted trajectory to ATIF format
Agent 轨迹已转换为训练格式
训练步完成
Training Progress: 100%
优势值估计与 actor 更新完成
沙箱侧可同步观察：kubectl get sandboxes 应显示与并发数一致的 Running 实例；训练多步后奖励统计中出现非零值，说明补丁已通过测试。
9 方案选型参考
需求场景
推荐方案
一次性代码评分，需要快速起步
仅评分路径，通过 ACS E2B SDK 接入（第 3 节）
多轮 coding agent 的生产环境训练
AgentLoop 路径，使用 recipe/agentic（独立 LLM Proxy、训练推理分离、按步耗时统计）
多轮 coding agent，要求不修改上游代码或接入自定义 Agent 框架
AgentLoop 路径，使用 recipe/remote_agent（runner 可插拔，无需修改 VeRL 主仓库）
多个训练任务共享沙箱资源池，需要配额管理，训练侧不依赖沙箱
在以上任一方案上叠加 Rollout Server（7.3 节）
训练与推理引擎需移出 Ray 集群（存算分离）
recipe/remote_megatron_sglang（VeRL 仅承担编排，对接外部 Megatron 与 SGLang）
各任务镜像差异较大、任务频繁变化、无预热需求
SANDBOX_MODE=ack 直接创建模式（支持任意 Dockerfile 集群内构建）
高并发场景且任务镜像可预先构建
SANDBOX_MODE=e2b 预热池模式（秒级申请并按任务替换镜像）
10 总结
阿里云智能体沙箱 Agent Sandbox 容器板接入 VeRL 后的端到端数据流可概括如下。Harbor 任务目录通过 task.toml 中的 docker_image 字段声明任务的初始环境镜像；沙箱由 SandboxSet 预热池或 ACK 直接创建提供，其申请、到期回收与补充由平台自动完成；RemoteAgentLoop 与 LLM Proxy 完成 rollout 过程，并以旁路方式录制 token_ids 与 logprobs；response_mask 依据录制事实完成 0/1 赋值；Harbor verifier 输出结构化奖励与三种结束状态，用于失败归因；数据最终以 DataProto、rm_scores 与 reward_extra_keys 的形式进入优势值估计与 actor 更新。
对于一次性代码评分需求，可从仅评分路径起步，该路径实现简单、风险较低。对于多轮 coding agent 训练，则必须采用 AgentLoop 路径，并系统性地处理沙箱供给、轨迹回流、上下文长度、环境并发与失败归因五个方面。本方案中，ACS 预热池负责沙箱供给（E2B 申请与镜像替换），旁路录制负责轨迹回流（response_mask 判定统一收敛到录制事实，潜在错误点集中于一处实现），Rollout Server 使执行层具备独立伸缩能力。
模型开始执行动作之后，环境本身即成为训练数据流的一部分。本方案中，VeRL 的三个 recipe 负责训练框架接入，Harbor 定制分支负责环境生命周期管理，Rollout Server 负责规模化后的执行层独立部署，三者共同构成 coding agent 强化学习在云上的完整执行栈。
