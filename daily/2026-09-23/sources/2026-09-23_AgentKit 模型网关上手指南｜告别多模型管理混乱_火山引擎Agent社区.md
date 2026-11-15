---
publish_time: 1790157600
link: https://mp.weixin.qq.com/s/THbeUTZ1gvnU9tyCAwfxsA
source: 火山引擎Agent社区
status: confirmed
category: 国内
is_model_related: false
digest: |
  文章以 DeepSeek Harness 为例，手把手演示火山引擎 AgentKit 模型网关的接入与验证全流程。AgentKit 把模型接入、密钥托管、故障兜底与用量观测收拢到单一入口，业务侧只需指向网关、换掉密钥即可接入，并以 DeepSeek Harness 场景说明多模型统一治理的落地方式。
title: AgentKit 模型网关上手指南｜告别多模型管理混乱
---

# AgentKit 模型网关上手指南｜告别多模型管理混乱

来源：火山引擎Agent社区
原文链接：https://mp.weixin.qq.com/s/THbeUTZ1gvnU9tyCAwfxsA

点击上方
👆
蓝字
关注我们！
企业在使用 Agent 时，大模型管理是最为关键的环节之一。从 "能调通模型" 到 "能稳定、可控地用好模型"，中间隔着接入入口、访问凭证、权限控制和成本管理几道坎。
火山引擎 AgentKit
是面向企业的 AI Agent 基础设施平台，提供 Agent 所需的运行时、身份权限、工具、记忆、知识和观测等能力。其中
AgentKit 模型网关
把模型接入、密钥托管、故障兜底和用量观测收到一个入口，业务侧只要指向网关、换掉密钥即可接入。
本文以 DeepSeek Harness 为例，完成从配置到验证的全流程实战。
01
前期准备
（1）开通 AgentKit 服务
若未开通，请登录 AgentKit 控制台：
https://console.volcengine.com/AgentKit
，根据系统引导开通产品。
（2） 模型准备
本期内容以火山方舟模型广场为例，需在平台获取 Base URL、API Key、模型 ID，详细步骤见：
https://ark.volcengine.com/region:cn-beijing/docs/82379/2272060?lang=zh
（3）私有网络
创建私有网络，为保持高可用性，至少创建 2 个子网，详细步骤见：
https://docs.volcengine.com/docs/6401/69467?lang=zh
至少创建 2 个子网
（4）日志服务
创建日志项目，这里以”agentkitgateway“为例，详细步骤见：
https://docs.volcengine.com/docs/6470/112663?lang=zh
以“agentkitgateway”为例
02
创建网关实例
在【AgentKit - 网关 - 网关实例】页面（直达链接：
https://console.volcengine.com/agentkit/region:agentkit+cn-shanghai/gateway/instance
），点击【创建网关】。
选择【模型网关】，在【网络设置】中选择此前准备好的【私有网络】和【子网】，在【日志项目】中选择前期准备好的 agentkitgateway 日志项目，点击【立即购买】即可完成实例创建。
03
创建模型网关
在【AgentKit - 网关 - 模型服务】中点击【创建模型服务】，选择对应的网关实例。
点击【创建模型服务】
选择【网关实例】
配置模型资源
以【火山方舟 - 模型广场】为例，填写以下信息：
配置项
说明
示例值
Base URL
模型服务接入地址
https://ark.cn-beijing.volces.com/api/v3
API Key
供应商 API 密钥
ark-xxxxxxx
模型限额
针对不同模型配置每分钟 Token 上限，控成本
按需配置
备用模型
主模型故障时自动切换，提高可用性
按需配置
点击【模型配置】-【添加】
针对不同模型 Token 限额
点击确认，完成模型网关配置。
04
创建 Proxy API Key
在【AgentKit - 模型服务 - 供应商与模型管理】中获取网关地址，作为后续调用的 Base URL。
在【AgentKit - 模型服务 - Proxy API Key 管理】中创建 Proxy API Key，作为业务侧实际使用的 API Key，保障原始 API Key 不泄露。
1. 填写【输入名称】：这里以 Gatewaymodeltest 为例。
2. 设置【自定义范围】：可针对模型配置速率限制及每日 / 每周 / 每月额度，控制模型使用量与成本。
3. 点击【确认】：Proxy API Key 完成创建，查看 Proxy Key。
在【模型服务 - 调用示例】中可查看 AgentKit Runtime、OpenAI SDK（Python）、cURL 等多种调用方式示例。
AgentKit Runtime 调用示例
OpenAI SDK（Python）调用示例
cURL 调用示例
05
调用示例
（1）以 cURL 为例
复制以下代码到终端，替换网关地址和 Proxy Key 后即可成功调用：
curl
"你的网关地址url"
\
--request POST \
--header
"Content-Type: application/json"
\
--header
"Authorization: Bearer 你的Proxykey"
\
--data '{
"model"
:
"doubao-seed-2-1-pro-260915"
,
"messages"
: [
{
"role"
:
"user"
,
"content"
:
"你好，请介绍一下自己。"
}
]
}'
（2）DeepSeek Harness 调用
终端安装 DeepSeek Harness：
npx
@deepseek
-ai/dsh web
打开 DeepSeek Harness，点击【设置 - 模型 - 添加自定义提供方】，填写以下信息：
1. API地址：填写网关地址：
https://xxxxxx.apigateway-cn-shanghai.volceapi.com/ark
。（
非火山方舟 URL
）
2. API Key：填写 Proxy API Key：sk-xxx。（
非火山方舟以”ark-xxxx“开头的 API Key，保护原始API Key不泄露
）
滑动查看更多
回到对话框，选择对应模型，输入问题，成功调用。
06
查看模型使用量
在【AgentKit - 模型服务 - 日志】中可查看运行日志，定位调用异常。
在【AgentKit - 模型服务 - 监控】中可按照 Provider、Proxy API Key 等维度查看 Token 消耗详情，掌握用量与成本。
以上就是 AgentKit 模型网关的完整接入流程。从创建网关实例、配置模型资源，到分配 Proxy API Key、验证调用、查看用量，整条链路只需在网关侧完成配置，业务代码无需改动。
AgentKit 模型网关把多模型接入、密钥安全、故障兜底和成本观测收敛到一个统一入口。
对业务侧而言
，换模型、加兜底、控成本都不再需要改代码或发版。
对管理者而言
，每一次调用的来源、耗时和花费都清晰可查。模型调用，从此从“能调通”走向“可管理、可优化”。
想试用 AgentKit 模型网关，点击「
阅读原文
」咨询了解。
