---
publish_time: 1789725600
link: https://mp.weixin.qq.com/s/nV7AVvbOMGMPccGbTxz9vQ
source: 火山引擎Agent社区
status: confirmed
category: 国内
is_model_related: false
digest: |
  火山引擎 AgentKit 是面向企业的 AI Agent 基础设施平台，提供运行时、身份权限、工具、记忆、知识与观测等能力；其 MCP 网关可集中纳管企业存量系统与内部 API，无需改造即可生成标准 MCP 服务，多个工具可编排为 MCP 工具集按语义匹配调用以降低 Token 消耗。本文以实操指南形式，演示三种接入方式：HTTP 转 MCP（存量 API 一键转标准服务）、导入已有 MCP 服务、部署自研/公开 MCP 服务并支持 Local→Remote 转换，完整走通从服务创建、工具集编排到 Agent 验证调用的流程。
title: AgentKit MCP 网关上手指南｜让企业存量服务快速接入 AI
---

# AgentKit MCP 网关上手指南｜让企业存量服务快速接入 AI

来源：火山引擎Agent社区
原文链接：https://mp.weixin.qq.com/s/nV7AVvbOMGMPccGbTxz9vQ

点击上方
👆
蓝字
关注我们！
企业积累了大量业务系统和内部 API，Agent 时代需要快速调用这些存量能力，但逐个改造周期长、成本高。
火山引擎推出的 AgentKit 是面向企业的 AI Agent 基础设施平台，提供运行时、身份权限、工具、记忆、知识和观测等能力。
其中 MCP 网关可集中纳管企业存量系统与内部 API，无需改造即可生成标准 MCP 服务。多个工具可编排为
MCP 工具集，可按语义匹配调用，降低 Token 消耗。
当前支持以下接入方式：
（1）HTTP 转 MCP：
将存量系统 API 一键转换为 MCP 服务。
（2）导入 MCP 服务：
导入已有 MCP 服务便于智能体统一对接，支持固定域名、容器服务、云服务器、函数服务方式导入。
（3）部署 MCP 服务：
支持部署自研或公开的 MCP 服务并提供对外访问，同时支持将 Local MCP 自动转换为 Remote MCP。
本期以
（1）、（2）两种方式为例
，完成从服务创建到工具集编排、再到 Agent 验证调用的全流程。
01
前期准备
（1）
开通 AgentKit 服务
。
若未开通，请登录 AgentKit 控制台：
https://console.volcengine.com/AgentKit
，按指引开通。
（2）由
存量系统 API 接口
转化而来的的 Swagger 或 OpenAPI Schema json 文件，及对应
后端服务域名
，
用于 HTTP 转 MCP 实操。
存量 API 文件可用 Trae 等 AI工具快速格式转化，MCP 服务 API 文件规范与示例请见：
https://docs.volcengine.com/docs/86681/2227893?lang=zh
（3）
已有 MCP 服务
域名及对应 API Key，
用于导入已有 MCP 服务实操。
本文以 GitHub MCP 为例，可前往 GitHub → Settings → Developer settings → Personal access tokens，获取 Key 值。
02
创建 HTTP 转 MCP 服务
在【AgentKit - 网关 - MCP】页面中点击【创建 MCP】服务，选择【共享网关】：
（1）共享网关，适用于 POC 或低流量验证。
（2）专属网关，适用于生产环境，此处若选择该网关，需在【AgentKit - 网关 - 网关实例 - 创建网关】提前创建，详细步骤见：
https://docs.volcengine.com/docs/86681/2650647?lang=zh
基本信息配置
，选择接入方式【HTTP 转 MCP】，上传根据企业存量 API 接口转化的 Swagger 或 OpenAPI Schema json 文件：
认证信息配置
，入站身份认证将用来控制谁可以访问此 MCP 服务。AgentKit 目前支持 API Key 及 OAuth JWT 方式。若使用 OAuth 授权模式，需提前创建用户池和客户端（详情见：
https://docs.volcengine.com/docs/86681/1873447?lang=zh
#Gzz7rgDs
）。
本次使用 API Key。
后端配置
，配置存量服务域名（支持函数服务、云服务器、固定域名）。
点击【创建】即可完成。
注：首次选择共享网关模式创建 MCP 服务时，系统将自动为您下单一个共享网关。
以上就完成 HTTP转 MCP 服务的创建，接下来我们获取调用代码，并在 Trae 进行验证调用：
注：Trae 配置 MCP服务地址：设置 - MCP -添加 - 手动配置。
在【AgentKit - 网关 - MCP】，选择刚创建的 MCP 服务，点击【监控】即可查看调用信息：
03
导入已有 MCP 服务
本文以导入 GitHub MCP 为例。
在【AgentKit - 网关 - MCP】页面中点击【创建 MCP】服务，选择【共享模型】，接入方式选择”导入 MCP 服务“，访问路径填“/mcp”。
后端配置：
选择”固定域名“，输入 GitHub MCP 服务域名
api.githubcopilot.com
。
“出站凭据”设置：
选择 API Key，点击【添加】，填入 API Key 名称（此处以 GitHub MCP 为例），填入 API Key（填入准备好的 GitHub 平台获取的 Key 值）。
“API Key 传递方式”设置：
参数位置选择“Header”，参数名称填写“Authorization”，Prefix 填写“Bearer”。
回到创建 MCP 服务页面，此时出站凭据可选择上一步创建的“GitHubMCP”，点击【创建】即可完成。
以上就完成了已有 MCP 服务的导入，同样获取调用代码并在 Trae 验证：
04
创建 MCP 工具集
这一步将多个 MCP 服务编排为一个工具集，灵活组合不同服务中的工具，并配置调用模式。
在【AgentKit - 网关 - MCP - MCP工具集】点击【创建 MCP 工具集】，选择【共享模式】，在【工具管理】中 AgentKit 支持 3 种调用模式：
（1）全量返回：直接返回内部所有 MCP 工具。
（2）语义检索：基于调用意图与工具描述进行语义匹配。
（3）标签检索：基于工具标签精准筛选所需工具。
本文我们以【语义检索】为例：
在【工具管理-工具】选择该 MCP 工具集包含的工具，【确认】后，点击【创建】，即可完成。
在【AgentKit - 网关 - MCP - MCP 工具集】，点击【调用示例】，可参照上述步骤将服务配置到 Trae 等工具中。
进入 MCP工具集，选择【调试】，可在线调试，本次我们使用
语义检索
模式，在“在线调试”中验证语义检索效果。
在自建效果检测工具中，相同条件下，相比全量返回所有MCP，MCP 工具集
按渐进式拉取工具使用
，Token 消耗从 31883 降至 10763（降幅超 60%），工具拉取耗时从 6680ms 降至 26ms（降幅超 99%）。
注：实际效果受大模型、网络等因素影响可能存在波动，以实际运行结果为准。
到这里，MCP 网关的整条链路就跑通了：HTTP 接口一键转标准工具、外部 MCP 统一纳管、多个服务编成工具集、语义检索精准匹配、调用监控一目了然。
AgentKit MCP 网关把“改造存量系统”变成了“接入存量系统”，周期从周级压到小时级。存量系统越复杂、工具数量越多，MCP 网关的价值就越明显。
如需详细了解 AgentKit MCP 网关，可点击「
阅读原文
」咨询。
