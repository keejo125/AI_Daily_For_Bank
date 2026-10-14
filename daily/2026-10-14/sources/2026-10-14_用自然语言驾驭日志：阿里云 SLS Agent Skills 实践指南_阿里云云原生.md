---
publish_time: 1791973935
link: https://mp.weixin.qq.com/s/QaZI6LClAqfPF4DaHF0jBg
source: 阿里云云原生
status: confirmed
category: 国内
is_model_related: false
digest: |
  阿里云日志服务SLS已提供8个Agent Skill，覆盖日志从采集、索引、查询分析、告警到可视化与根因分析全生命周期，支持渐进式上下文披露。文章以Codex用量监控为例，展示用自然语言让Agent自动完成Token采集上报、创建logstore与索引、搭建仪表盘、配置额度重置邮件告警，把运维配置从手写命令转为对话式编排。
title: 用自然语言驾驭日志：阿里云 SLS Agent Skills 实践指南
---

# 用自然语言驾驭日志：阿里云 SLS Agent Skills 实践指南

来源：阿里云云原生
原文链接：https://mp.weixin.qq.com/s/QaZI6LClAqfPF4DaHF0jBg

过去一年，阿里云日志服务 SLS 持续完善 CLI 与 Agent Skills，将日志采集、分析和监控等能力逐步接入 Agent 工作流。用户可以用自然语言描述业务目标，由 Agent 协同完成日志接入、监控搭建与故障排查，减少手动配置、命令编写和反复查询的工作。
目前，SLS 已提供 8 个技能，覆盖日志从产生到使用的完整生命周期：从 SDK 接入、日志采集，到日志库创建、索引配置，再到查询分析、告警、可视化和根因分析。各技能支持按需安装，并采用渐进式上下文披露，按任务需要加载相关说明，减少不必要的上下文开销。
本文将结合实际场景，介绍这些技能的功能、使用方法与最佳实践。
技能与能力总览
Cloud Native
场景示例：一句话完成 Codex 用量监控
Cloud Native
以 Codex 用量监控为例，我们希望了解 Token 消耗在哪里、周额度还剩多少，并在额度重置时收到通知。我们可以把需求概括成如下的提示词交给 Agent：
帮我写脚本采集本机 Codex 的 Token 消耗（包括
input
、output、cached 等详细信息）和当前消耗额度（定时上报），使用 aliyun cli 上报到 SLS 的 xxxx Project，创建好相应的 logstore、索引配置，然后创建一个仪表盘，包含每日、每周的 token 消耗统计、额度消耗曲线、各个维度的 token 消耗统计，最后配置一个告警， codex  周额度重置时通过邮件通知到 xxxx
@example
.com 邮箱内。
Agent 会自动完成几个相互衔接的步骤：
1. 采集与上报
：
将 Token 用量和额度快照写入 token-usage 日志库，持续记录消耗、剩余额度和重置时间。
2. 创建 logstore 与配置索引
：
创建对应的 logstore， 为 Token 数量、额度百分比和时间等字段配置索引与统计能力，让这些数据可以直接查询和分析。
3. 搭建仪表盘
：
按模型、项目和会话查看 Token 消耗，观察用量趋势，了解额度花在了哪些任务上。
4. 配置告警邮件提醒
：
定期查询周额度记录，识别额度重置，在满足条件时发送邮件。
推荐配合 browser use、browser act、chrome use、playwright、agent browser 等能够控制浏览器的技能或者工具使用， 让 agent 能够使用浏览器验证、调整仪表盘显示细节，实现更佳的显示效果。
下面是 Agent 创建的仪表盘示意图：
下面是 Codex 重置时邮箱收到的告警截图：
通过这个例子，我们可以看到，采集、索引、查询、可视化和告警能够围绕一个业务目标协同工作。我们描述“了解用量，并在额度恢复时收到提醒”的需求，Agent 就可以将它转化为可以持续运行的监控流程。
安装与使用
Cloud Native
使用 npx 安装技能需要 Node.js。
▍
1. alibabacloud-sls-query
在线查询和分析 SLS 日志，支持 SLS 查询语法、SQL 和 SPL，生成和优化查询语句。可按字段检索日志，统计错误数量、接口排名和延迟变化。
安装命令：
npx -
y
skills add aliyun/alibabacloud-aiops-skills
--skill
alibabacloud-sls-query -
y
--full-depth
场景一：统计错误接口 Top 10
查询 cn-hangzhou 的 prod-web/nginx-access，统计过去一小时各 request_uri 的
500 请求数，列出错误最多的 10 个接口，并给出查询语句和统计结果。
场景二：对比延迟趋势
分析 prod-web/nginx-access 最近一小时与昨天同期的平均延迟变化，按分钟统计。
参见
Query 使用文档
[
9]
。
▍
2. alibabacloud-loongcollector-ops
在 ECS、Linux 主机、ACK 或自建 Kubernetes 上安装、升级 Logtail/LoongCollector；
管理采集配置、机器组和绑定关系；
排查采集无数据和机器组心跳异常。
支持主机日志采集接入、采集配置调整和基础故障排查。
安装命令：
npx -
y
skills add aliyun/alibabacloud-aiops-skills
--skill
alibabacloud-loongcollector-ops -
y
--full-depth
场景一：接入主机日志
在 cn-hangzhou 的 ECS i-example 上安装 LoongCollector，将 /var/log/nginx/access.log
采集到 prod-web/nginx-access，配置机器组和绑定，并验证 SLS 中能查到日志。
场景二：排查采集无数据
cn-hangzhou 的 prod-web/nginx-access 最近没有新日志。
请检查关联采集配置、机器组绑定和成员心跳，说明异常位置及处理建议。
▍
3. alibabacloud-sls-agent-workflow
根据任务选择并组合技能，完成资源创建、日志采集、查询分析和告警配置。支持从日志库与索引创建到日志写入、查询验证的组合任务。
安装命令：
npx -
y
skills add aliyun/alibabacloud-aiops-skills
--skill
alibabacloud-sls-agent-workflow -
y
--full-depth
场景示例：完成日志写入与查询
在 cn-hangzhou 创建 Project=demo-sls 和 Logstore=app-logs，
为 level、service、message 配置索引，写入几条测试日志，
再查询 ERROR 日志并按 service 统计数量，验证写入和查询结果。
▍
4. alibabacloud-sls-alerting
创建和调整告警规则，管理通知渠道、接收人和策略，支持启停、静默和告警降噪。结合告警历史与源日志定位触发原因，分析告警频率和持续时间。
安装命令：
npx -
y
skills add aliyun/alibabacloud-aiops-skills
--skill
alibabacloud-sls-alerting -
y
--full-depth
场景一：创建日志告警
在 cn-hangzhou 的 prod-web 创建 web-
500
-alert，数据源是 nginx-access。
每
1
分钟检查过去
5
分钟的日志，status=
500
的请求数不少于
100
时告警，
邮件发送给已有通知人 web-ops
@example
.
com
。
场景二：分析历史告警
分析 cn-hangzhou 的 prod-web/web-500-alert 在北京时间
2026-10-08 09:00 到 10:00 的告警，核对触发原因、频率和持续时间，
并结合源日志找出错误集中的接口，给出查询证据。
“每 1 分钟”是检查频率，“过去 5 分钟”是查询窗口。规则配置、执行和通知送达需分别验证。参见
Alerting 使用文档
[
10]
。
▍
5. alibabacloud-sls-dashboard
创建和修改仪表盘、图表及筛选控件，排查显示问题，管理仪表盘订阅。支持将查询结果配置为监控看板，展示请求量、错误率、延迟等指标。
安装命令：
npx -
y
skills add aliyun/alibabacloud-aiops-skills
--skill
alibabacloud-sls-dashboard -
y
--full-depth
场景一：创建请求监控看板
为 cn-hangzhou 的 prod-web/nginx-access 创建请求监控仪表盘。
展示每分钟请求量、5xx 数量和平均 request_time（单位为秒），
增加 service 筛选控件，先验证查询，再发布到 prod-web。
场景二：调整已有仪表盘
读取 cn-hangzhou 的 prod-web 中仪表盘 web-overview，
新增按 request_uri 统计的错误数
Top
10
图表，保留其他图表和筛选控件，
更新后核验配置。
▍
6. alibabacloud-sls-data-agent
调用 SLS Data Agent，通过数字员工完成取数、处理、分析和可视化，辅助异常排查与根因分析，支持保留分析会话、多轮追问和日志下钻。
该技能依赖 StarOps 数字员工能力，使用前需准备可用的 StarOps 数字员工和目标 Project。
安装命令：
npx -
y
skills add aliyun/alibabacloud-aiops-skills
--skill
alibabacloud-sls-data-agent -
y
--full-depth
场景示例：分析异常并继续下钻
使用
SLS
Data
Agent 和数字员工 apsara
-ops
，分析 cn
-hangzhou
的
prod
-web
/nginx
-access
最近一小时的请求量、错误率和延迟，
找出异常时间段，给出图表和分析结论。
可以在同一会话中继续追问：
继续分析刚才的异常时间段，按接口比较错误率，找出变化最大的接口。
▍
7. alibabacloud-sls-index-config-management
管理 Logstore 索引，根据日志样本生成配置，按查询需求调整字段类型和统计配置。支持索引的查看、创建、修改和删除，以及写入吞吐和存储成本优化。
安装命令：
npx -
y
skills add aliyun/alibabacloud-aiops-skills
--skill
alibabacloud-sls-index-config-management -
y
--full-depth
场景一：根据日志样本生成索引
为下面的日志样本生成索引配置，需要按 status 过滤、按 service 分组，
并统计 latency_ms 的平均值。先给出配置
JSON
和字段说明，不执行更新。
{
"status"
:
500
,
"service"
:
"order"
,
"latency_ms"
:
238.5
,
"message"
:
"timeout"
}
场景二：补充分析字段
读取 cn-hangzhou 的 prod-web/app-logs 索引，为 latency_ms 配置 double 类型
并开启统计，支持平均值分析；保留其他字段配置，给出变更内容。
▍
8. alibabacloud-sls-sdk-guidance
根据编程语言和业务场景自动选择 SLS SDK，提供依赖安装、初始化和代码示例。支持日志写入、消费、查询，以及 Log4j2、Logback 等日志框架接入。
安装命令：
npx -
y
skills add aliyun/alibabacloud-aiops-skills
--skill
alibabacloud-sls-sdk-guidance -
y
--full-depth
场景一：选择写入和消费 SDK
为 Java
17
项目选择
SLS
SDK。日志需要异步批量写入，消费端需要
Consumer
Group
、checkpoint 和多实例负载均衡。
请给出选型理由、Maven 依赖和最小接入示例。
场景二：通过 Log4j2 接入
Java 项目已有 Log4j2，希望通过 Appender 将日志发送到 cn-hangzhou 的
prod-web/app-logs。请给出 Maven 依赖和 log4j2.xml 配置。
参见
SDK 集成文档
[
11]
。
配置凭证
Cloud Native
SLS 技能主要依赖于 Aliyun CLI 和 SLS 插件。除静态 AccessKey 外，也支持 OAuth、EcsRamRole 等无需配置长期 AccessKey 的方式。支持所有凭证类型和配置方法参见
阿里云 CLI：配置与管理身份凭证
[
12]
。认证后仍需具备对应资源的 RAM 权限。
aliyun cli 支持将凭证信息与地域信息保存在 profile 内，来实现不同身份、地域、凭证类型的快速切换，默认的 profile 名字是
default
。使用下列命令可以列出现有的 profile：
aliyun
configure list
这里介绍几种常用的凭证类型的配置方式，其他凭证类型和配置方法参见
阿里云 CLI：配置与管理身份凭证
。
▍
静态 AccessKey
使用静态 AccessKey 配置 profile：
aliyun
configure
# 配置默认 profile
aliyun configure --profile 
# 配置指定名称的 profile，不存在时会自动化创建
▍
OAuth 登录授权
对于可以使用浏览器登录阿里云账号的环境（例如处于办公网的本地 mac 电脑），使用 OAuth 接入比较简单。OAuth 首次登录需要给账号
授权
[
28]
。
之后可使用 OAuth 配置指定 profile，会自动打开浏览器进行登录授权:
aliyun configure
--mode
OAuth
--profile

管理跨地域 Project 资源
Cloud Native
alibabacloud-sls-query 内置了 Project 跨地域发现能力。当默认地域找不到 Project，或用户不确定 Project 所属地域时，Agent 会在全局查找该 Project，获取其 Region 和 Endpoint，并使用发现的 Endpoint 继续执行查询，免去人工查找和设置 Region 或 Endpoint。
也可以通过以下方式手动查询（需要指定 endpoint 固定为
cn-zhangjiakou.log.aliyuncs.com
）。
aliyun sls get-project
--project

--cross-region
true
--endpoint
cn-zhangjiakou
.log.aliyuncs.com
常见问题
Cloud Native
▍
需要提前安装 CLI 和 SLS 插件吗？
执行云端操作时需要安装。Agent 会检查 CLI 和 SLS 插件，并在缺失或版本不满足要求时提供安装、升级指引。仅解释配置或生成代码示例时无需访问云资源。参见
Query 文档
和
Alerting 文档
。
▍
能使用内网、传输加速或自定义 Endpoint 吗？
支持。在需求中指定 Endpoint，例如
cn-hangzhou-intranet.log.aliyuncs.com
，并确保运行环境能够访问。参见
Query FAQ
[
29]
。
▍
推荐安装哪些技能？
alibabacloud-sls-query
是最推荐安装的技能，建议直接安装，对日志查询分析、生成 SQL/SPL 都有很大帮助。其他技能可根据实际需求安装。
▍
对于诺曼底托管的日志资源如何接入？
目前 aliyun cli 暂不支持诺曼底的鉴权方式，推荐安装并使用
normandy-cli
[
30]
技能，配合
alibabacloud-sls-query
技能一起使用。
总结
Cloud Native
通过官方 CLI 和 8 个 Agent Skills，SLS 已将日志采集、SDK 接入、资源与索引管理、查询分析、告警、可视化和根因分析等能力连接起来，覆盖日志的完整生命周期。配合多种鉴权方式和跨地域资源发现，用户可以围绕业务目标组织任务，减少环境配置、命令编写和工具切换的工作。
目前，CLI 日均请求量已超过 110 万次，Skills 日均请求量已超过 50 万次。其中，CLI 日均请求量约为 2026 年 2 月的 700 倍，CLI 和 Skills 正在成为开发和运维人员使用 SLS 的日常入口。
后续，我们会进一步完善技能场景的覆盖，提升多技能协同和复杂问题分析能力，将更多经过验证的操作流程与排查经验沉淀到技能中。在提高执行准确性和可靠性的同时，持续将 SLS 打造为 AI First、Agent Native 的可观测平台，让数据、工具与产品能力能够被 Agent 自然调用和组合，充分释放 Agent 在数据分析、系统诊断和自动化运维中的潜力。
相关链接：
[1] alibabacloud-sls-query
https://skills.aliyun.com/skills/alibabacloud-sls-query
[2] alibabacloud-loongcollector-ops
https://skills.aliyun.com/skills/alibabacloud-loongcollector-ops
[3] alibabacloud-sls-agent-workflow
https://skills.aliyun.com/skills/alibabacloud-sls-agent-workflow
[4] alibabacloud-sls-alerting
https://skills.aliyun.com/skills/alibabacloud-sls-alerting
[5] alibabacloud-sls-dashboard
https://skills.aliyun.com/skills/alibabacloud-sls-dashboard
[6] alibabacloud-sls-data-agent
https://skills.aliyun.com/skills/alibabacloud-sls-data-agent
[7] alibabacloud-sls-index-config-management
https://skills.aliyun.com/skills/alibabacloud-sls-index-config-management
[8] alibabacloud-sls-sdk-guidance
https://skills.aliyun.com/skills/alibabacloud-sls-sdk-guidance
[9]
Query 使用文档
https://help.aliyun.com/zh/sls/sls-query-skill-intelligent-log-query-and-analysis
[10]
Alerting 使用文档
https://help.aliyun.com/zh/sls/intelligently-manage-and-diagnose-alerts-using-the-sls-alerting-skill
[11]
SDK 集成文档
https://help.aliyun.com/zh/sls/developer-reference/quickly-integrate-the-sls-sdk-using-agent-skill
[12]
阿里云 CLI：配置与管理身份凭证
https://help.aliyun.com/zh/cli/configure-credentials
[13] AccessKey 最佳实践
https://help.aliyun.com/zh/ram/product-overview/best-practices-for-identity-and-access-control
#8ca79a7ca278m
[14] 配置 AK 凭证
https://help.aliyun.com/zh/cli/ak-credential
[15] 配置 OAuth 凭证
https://help.aliyun.com/zh/cli/oauth-credentials
[16] 配置 EcsRamRole 凭证
https://help.aliyun.com/zh/cli/ecs-ram-role
[17] 扮演 RAM 角色
https://help.aliyun.com/zh/ram/user-guide/ram-role-overview
#ce9ce27a75hqi
[18] 配置 RAM 角色凭证
https://help.aliyun.com/zh/cli/ram-role-credentials
#h2
-arn-01
[19] 角色链
https://help.aliyun.com/zh/ram/user-guide/ram-role-overview
#13c5fcecb645c
[20] 配置 RAM 角色链凭证
https://help.aliyun.com/zh/cli/ram-role-credentials
#h2
-chain-01
[21] RRSA
https://help.aliyun.com/zh/cs/user-guide/use-rrsa-to-configure-ram-permissions-for-serviceaccount-to-implement
[22] 配置 OIDC 凭证
https://help.aliyun.com/zh/cli/other-credentials-oidc-cloudsso-external-credentialsuri-bearertoken
#1f9791c531qdo
[23] 配置 CloudSSO 凭证
https://help.aliyun.com/zh/cli/other-credentials-oidc-cloudsso-external-credentialsuri-bearertoken
#219bcad7728bv
[24] 配置 External 凭证
https://help.aliyun.com/zh/cli/other-credentials-oidc-cloudsso-external-credentialsuri-bearertoken
#f1ed28ef9e3lw
[25] 配置 CredentialsURI 凭证
https://help.aliyun.com/zh/cli/other-credentials-oidc-cloudsso-external-credentialsuri-bearertoken
#67896b8dd1vvt
[26] 配置 StsToken 凭证
https://help.aliyun.com/zh/cli/temporary-security-credentials-sts-token
[27] 配置 BearerToken 凭证
https://help.aliyun.com/zh/cli/other-credentials-oidc-cloudsso-external-credentialsuri-bearertoken
[28]
授权
https://help.aliyun.com/zh/cli/oauth-credentials?spm=a2c4g.11186623.0.0.212c388fqLtWZ3
#s
-admin-ops-k7l8m9n0
[29]
Query FAQ
https://help.aliyun.com/zh/sls/sls-query-skill-intelligent-log-query-and-analysis
[30]
normandy-cli
https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation
