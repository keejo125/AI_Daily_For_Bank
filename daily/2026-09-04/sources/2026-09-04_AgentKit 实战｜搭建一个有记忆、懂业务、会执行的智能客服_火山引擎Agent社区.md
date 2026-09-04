---
publish_time: 1788517610
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/3tt3JjdoC9T5__DuhGvcmQ
source: 火山引擎Agent社区
title: AgentKit 实战｜搭建一个有记忆、懂业务、会执行的智能客服
---

# AgentKit 实战｜搭建一个有记忆、懂业务、会执行的智能客服

来源：火山引擎Agent社区
原文链接：https://mp.weixin.qq.com/s/3tt3JjdoC9T5__DuhGvcmQ

点击上方
👆
蓝字
关注我们！
当前，很多企业已具备快速构建 Agent Demo 的能力，但真正的挑战在于，如何让 Agent 真正进入生产环境，稳定服务真实用户。
从 Demo 到生产环境，需要解决记忆持久化、知识索引与版本管理、工具调用的权限与容错，以及运行状态的监控和问题追溯。而作为火山引擎推出的企业级 AI Agent 基础设施平台，AgentKit 提供 Agent 开发、运行与治理的端到端能力，通过安全隔离的 Sandbox、统一身份与权限、运行治理及企业系统集成，让 Agent 在安全、可控、可观测的环境中持续运行，并真正融入企业业务流程。
下面以
智能售后客服为例
，基于 AgentKit 接入 VikingDB、Mem0 和 CRM，构建具备知识检索、长期记忆与业务系统操作能力的 Agent，并将其部署至云端 Runtime。
原理解读
智能售后客服 = 大脑 (AgentKit 引擎) + 知识 (知识库) + 记忆 (Memory) + 接口 (CRM 工具集成)
大脑：
基于火山引擎大模型，理解用户意图，进行逻辑判断，并为Agent提供运行环境。
知识：
存储在 Viking 向量数据库中的产品手册和维修政策，为回答提供业务依据。
记忆：
记录用户的对话历史和个人信息，保证服务连贯性。
接口：
通过 API 连接 CRM 系统，执行查订单、开工单等实际操作。
前期准备
1. 本地环境要求：
本地操作系统要求：
建议使用 MacOS/Linux 操作系统。
Windows 用户建议使用 wsl 完成当前实验。
本地 Python 版本：
需要 Python 3.12 或更高版本。
2. 在火山引擎控制台准备好以下资源：
AK/SK：
前往
API 访问密钥 (
https://mic.anruicloud.com/url/20260904keymanage
)
页面，"创建 Access Key"，并申请以下权限 AgentKitFullAccess、CRFullAccess、VikingdbFullAccess、Mem0FullAccess、VPCFullAccess、ArkFullAccess、AIDAPFullAccess。
私有网络：
在
VPC 控制台 (
https://mic.anruicloud.com/url/20260904vpc
)
创建私有网络和子网，记录 VPC ID 与子网 ID
开通模型：
在
火山方舟-开通管理 (
https://mic.anruicloud.com/url/20260904openmanagement
)
开通语言模型，开通 doubao-seed-evolving
TOS Bucket：
在
对象存储 TOS (
https://mic.anruicloud.com/url/20260904tos
)
准备一个对象存储桶，用于存放构建产物和知识库文档。桶名规则为
agentkit-platform-<你的火山引擎账号ID>
，地域
cn-beijing
。
3. 获取智能售后客服代码
本次实验所需要的代码位于 Agentkit 官方的示例代码仓库中。
agentkit-samples：
https://github.com/bytedance/agentkit-samples.git
Clone 或下载项目代码，在下面的路径中找到智能售后客服的代码：
python/02-use-cases/customer_support
在代码目录下开启一个终端，后续的命令行交互过程都在
customer_support
目录下进行。
4. 安装 Agentkit 二进制命令
在本地终端安装 agentkit 二进制命令，后续与 Agentkit 平台上各类资源的互动（创建、删除）都借助这个命令实现。
# 安装命令
wget
-qO- https://agentkit-cli.tos-cn-beijing.volces.com/install.sh | sh
# 验证
ak --version
# 预期返回 agenkit-cli 版本，如 0.46.7
5. 声明环境变量
所有的系统配置，后续都会以环境变量的形式注入，故而需要后续所有的操作都在同一个终端下进行。到这一步，需要声明的环境变量如下：
# 声明AK/SK：用于本地 CLI 创建和管理云端资源
export
VOLCENGINE_ACCESS_KEY=<your_ak>
export
VOLCENGINE_SECRET_KEY=<your_sk>
# 声明网络信息
export
VPC_ID=<vpc_id>
export
SUBNET_ID=<subnet_id>
# 声明模型接入点相关信息
export
MODEL_AGENT_API_KEY=<ark_api_key>
export
MODEL_AGENT_NAME=doubao-seed-evolving
# 推荐使用当前最新版本的 Seed 模型
# 实验名称（自定义，会作为知识库/记忆库/智能体的命名前缀）
export
EXP_NAME=
"agentkit_customer_xxx"
# TOS 桶（注意把 xxx 换成你的账号 ID）
export
DATABASE_TOS_BUCKET=
"agentkit-platform-xxx"
构建“知识大脑” — 创建售后知识库
一个优秀的客服必须熟读产品手册。在这一步，我们将创建出知识库，便于后续将售后知识灌输给智能体。
在终端输入以下代码：
创建
# 执行创建命令，注意 **自定义** 知识库名称
ak
knowledge create --name
"knowledge_${EXP_NAME}"
\
--provider-type viking
\
--description
"用于AgentKit端到端验证的知识库-knowledge_${EXP_NAME}"
\
--region cn-beijing
验证
# 列出账号下的所有知识库，确认实例的状态 STATUS = Ready，并记录 KNOWLEDGE ID
ak
knowledge list
声明引用知识库所需的环境变量
# 变量的值来自于自定义的知识库名称
export
DATABASE_VIKING_COLLECTION=
"knowledge_
${EXP_NAME}
"
# 变量的值来自于 ak knowledge list 的返回
export
KNOWLEDGE_ID=<KNOWLEDGE ID>
赋予“记忆能力” — 创建 Viking 记忆库
VikingDB 负责存储产品和政策，Mem0（长期记忆库）负责存储与具体用户相关的信息，包含设备型号、购买时间、已确认的故障现象、做过的排查动作和工单状态等数据。
在终端输入下面这组代码，创建长期记忆库：
ak
memory create
\
--name
"mem_${EXP_NAME}"
\
--description
"用于 AgentKit 验证的长期记忆库"
\
--provider-type MEM0
\
--region cn-beijing
\
--json '{
"VpcConfig"
:{
"VpcId"
:
"'"
${VPC_ID}
"'"
,
"SubnetIds"
:[
"'"
${SUBNET_ID}
"'"
]},
"LongTermConfiguration"
:{
"Strategies"
:[{
"Name"
:
"default"
,
"Type"
:
"Summary"
}]}}'
查询并记录 MEMORY ID：
ak
memory list
# 确认 STATUS = Ready，记录 mem-xxxx 形式的 MEMORY ID
然后前往
记忆库 Mem0 控制台 (
https://mic.anruicloud.com/url/20260904mem0
)
，点击刚才创建的记忆项目：
在「连接管理」里复制
私网连接地址
；
在「API Keys」里创建并复制
API Key
。
声明环境变量：
export
DATABASE_MEM0_BASE_URL=<Mem0 私网连接地址>
export
DATABASE_MEM0_API_KEY=<Mem0 API Key>
export
MEMORY_ID=<mem-xxxx>
打造与顾客“接口” — 模拟 CRM 系统搭建
为了让 AI 能够真正处理业务（如回答客户问题，查询订单等），我们需要一个模拟的业务系统。此处我们使用
python/02-use-cases/customer_support/tools/crm_mock.py
来模拟这个业务系统，并通过自定义工具的方式传递给智能体。
把智能体发布到云端
现在，组件都已准备就绪，让我们在 AgentKit 中将智能体部署起来。
通过 agentkit-cli 进行云端部署之前，需要先创建出部署所需要的配置文件与 Dockerfile。
ak
config --init
\
--agent_name
"${EXP_NAME}"
\
--entry_point main.py
\
--knowledge_id
"${KNOWLEDGE_ID}"
\
--runtime_network_mode hybrid
\
--runtime_enable_shared_internet_access
\
--runtime-vpc-id
"${VPC_ID}"
\
--runtime-subnet-id
"${SUBNET_ID}"
\
--tos_bucket
"${DATABASE_TOS_BUCKET}"
\
--runtime_envs DATABASE_MEM0_BASE_URL=
"${DATABASE_MEM0_BASE_URL}"
\
--runtime_envs DATABASE_MEM0_API_KEY=
"${DATABASE_MEM0_API_KEY}"
\
--runtime_envs MEMORY_ID=
"${MEMORY_ID}"
\
--runtime_envs DATABASE_VIKING_COLLECTION=
"knowledge_${EXP_NAME}"
\
--runtime_envs DATABASE_TOS_BUCKET=
"${DATABASE_TOS_BUCKET}"
\
--runtime_envs DATABASE_TOS_REGION=
"cn-beijing"
\
--runtime_envs DATABASE_TOS_ENDPOINT=
"tos-cn-beijing.volces.com"
✅
成功标志：当前目录生成
`agentkit.yaml
`。
确认入口文件可加载、网络和环境变量无误后，发布：
ak
launch
✅
成功标志：终端显示 `Launch completed successfully!`
，并给出 Runtime Endpoint。
发布成功后，可以登录火山引擎 AgentKit 控制台，点击智能体运行时查看部署的智能体。
发布成功！测试你的智能客服 Agent
测试场景一
你好，我之前买的电视坏了。
我的邮箱是
user
@example
.com，电视序列号是 SN20240001。
我需要帮助排查电视故障：无法开机。
测试场景二
我想买一款客厅用的智能电视,主要用来打游戏,预算 3000 元以内
到这里，这个客服 Agent 已经能查资料、记得住上次的进度、也能把工单落进业务系统。
下一步，你可以尝试：
接入更多渠道：
将你的智能体对接到飞书机器人进行交互，参考：
https://docs.volcengine.com/docs/86681/2222895?lang=zh
丰富工具集：
增加“物流查询”或“退款申请”的 API 能力。
个性化定制：
调整 Prompt，让客服的语气更加活泼或更加专业。
自定义知识库：
上传自己的知识库，打造一个完完全全属于你的专属客服！
点击
阅读原文
，进入 AgentKit 官网，了解更多！
