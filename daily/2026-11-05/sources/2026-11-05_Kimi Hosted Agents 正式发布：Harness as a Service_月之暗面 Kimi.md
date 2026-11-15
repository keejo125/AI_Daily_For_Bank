---
publish_time: 1793852196
link: https://mp.weixin.qq.com/s/anUer3njbiUh4KOYfORncA
source: 月之暗面 Kimi
status: confirmed
category: 国内
is_model_related: false
digest: |
  月之暗面发布 Kimi Hosted Agents（托管智能体），把支撑 Agent 运行的 Harness 作为云端服务提供，企业无需自建和维护运行框架即可获得 7×24 小时托管环境与长程任务、多智能体协作能力。平台支持面向内部业务（监控、运维）与面向产品用户（投研、客服助手）两类应用，并提供独立沙箱保障安全可控。
title: Kimi Hosted Agents 正式发布：Harness as a Service
---

# Kimi Hosted Agents 正式发布：Harness as a Service

来源：月之暗面 Kimi
原文链接：https://mp.weixin.qq.com/s/anUer3njbiUh4KOYfORncA

今天，我们发布 Kimi Hosted Agents（托管智能体），将支撑 Agent 运行的 Harness 作为云端服务提供给企业和开发者，企业无需自行搭建和维护运行框架，即可获得 7×24 小时的托管环境，支持长程任务执行与多智能体高效协作。
开始使用：
platform.kimi.com/docs/hosted-agents/quickstart
企业可以按需配置 Agent，快速构建两类业务应用：
面向内部业务
：集成到企业内部系统，提供业务监控、运维响应等任务。
面向产品用户
：嵌入企业对外提供的产品，提供 App 内的投研助手、客服助手等 Agent 服务。
为保障 Agent 安全可控地运行，Kimi Hosted Agents 提供独立沙箱、网络访问权限控制，企业可设定操作边界，并在必要时随时中止会话；执行过程留痕可查，支持审计导出；清晰的计费规则与用量报表，也让企业能够掌握各个 Agent 项目资源消耗与费用。
注册登录 platform.kimi.com
即可体验
告别自建 Harness，专注业务应用开发
让 Agent 投入生产，企业需要投入几个月构建一套可靠的 Harness 底座 —— 搭建代码执行环境，实现上下文与会话管理、工具调用、权限控制、任务中断恢复等能力。在 Agent 上线后，企业仍需花费大量时间和成本持续维护这套 Harness 系统。
现在，依托 Kimi Hosted Agents 提供的 Harness 框架与托管环境，企业可以快速定义任务、接入工具，缩短从原型验证到应用上线的开发周期。底层运行环境的维护与升级由 Kimi 负责，团队无需反复投入基础设施适配与运维，可以更快响应业务需求、迭代应用功能。
自建 Harness vs 使用 Kimi 托管智能体
调
用官方 Skills 与插件，加速业务功能开发
Kimi Hosted Agents 提供 140+ Skills 与 30+ 插件，覆盖联网检索、专业数据查询、办公文档处理和内容生成等任务，开发者可按需调用，减少逐项接入工具的开发工作。企业也可接入自有工具和数据源，让智能体适配具体业务流程。
数据源和插件库仍在持续拓展中
接入 Kimi Inference Hook，让 Agent 在企业安全规则下运行
Kimi Hosted Agents 可结合开放平台的
独立安全组件
Kimi
Inference Hook，对接企业自建或采购的安全服务，
在每次模型推理前检查任务输入与工具返回内容，将隐私和敏感数据拦截在推理之前。
安全检查规则由企业定义，放行或拒绝由
Kimi
Inference Hook 执行
：只有通过企业安全检查的内容才会进入模型推理。
注： Kimi Inference Hook 目前仅针对企业认证用户定向开放，如有业务需求，请联系我们 platform.kimi.com/contact-sales
官方模板开箱即用，快速构建业务智能体
Kimi 开放平台文档站同步提供配套的 Agent 架构设计思路、配置教程、运行成本估算；企业可将 Agent 模板复制到自己的项目空间，接入内部业务系统、私有数据库等资源，按需调整任务流程，快速构建适合自身业务的智能体。
首批提供 8 个金融 Agent 模板，覆盖投研建模、深度研究、晨报生成、IPO 跟踪、持仓监控等任务，支持在托管环境中持续运行。企业可以将 Agent 模板复制到自己的项目空间，接入内部研报、私有数据库等资源，适配实际业务流程。
下面以投研建模、监管例报和基金对账为例，展示 Agent 如何拆解任务、调用工具并完成处理。
→ 右滑查看 Agent 设计与配置架构图
相关文档
使用指南：Kimi Hosted Agents 快速开始
platform.kimi.com/docs/hosted-agents/quickstart
定价说明：Kimi Hosted Agents 定价
platform.kimi.com/docs/pricing/hosted-agents
API 说明：Kimi Hosted Agents API 参考
platform.kimi.com/docs/api-reference
如需更多
Kimi
托管智能体产品支持，请联系我们，并备注「
KHA」：
扫描二维码联系我们
