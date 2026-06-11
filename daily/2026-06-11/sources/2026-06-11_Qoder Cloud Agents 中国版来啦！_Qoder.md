---
publish_time: 1781169660
---

# Qoder Cloud Agents 中国版来啦！

> 原文链接：https://mp.weixin.qq.com/s/CsqGhztbt_A7kuQYlK8q0w
> 公众号：Qoder

1 images

今天，我们正式上线 Qoder Cloud Agents 中国版。

Qoder Cloud Agents 是一个全托管的 AI Agent 云服务，开发者只需通过 REST API 调用，就能快速构建持续运行、自主进化的 Agent 应用——不必自建基础设施，不必维护沙箱，不必担心模型升级。

中国版内置的全部是中国SOTA模型，部署在中国区，如果你的企业对数据出境方面有强管控，又希望能快速构建 Agent 应用，Qoder Cloud Agents 中国版是您的不错选择。

1、声明式 Agent，一次定义、长期演进

通过 Agent API 声明式创建和管理 Agent——配置模型、工具、系统指令、MCP 集成。支持版本管理与回滚，平台升级模型与编排策略时，已接入的应用零代码变更自动变强。

2、长程任务，跑得稳、续得上

长会话持续运行：跨小时到跨天的连续执行，支持断点恢复、事件流跨轮次持久化。会话事件实时流支持网络抖动后自动重连并从断点续传，全程无需刷新。

3、托管的执行环境，开箱即用的工具集

平台提供安全隔离的 Sandbox 执行环境，可配置网络策略，无需自建基础设施。内置 8 种开箱即用工具：bash、read、write、edit、glob、grep、web_fetch、web_search。需要更多能力时，可以接入外部 MCP Server 获得无限扩展。

4、全程可观测，每一步都看得见

通过 SSE 实时事件流，Agent 的每一步思考、每一次工具调用都会实时推送，方便观测、审计和回放。

5、完整的资源管理 API

- 文件上传与挂载（Files API）：向 Session 提供文件上下文，Agent 产物也可通过 API 下载

- 用户凭证（Vaults API）：安全托管访问凭证，Session 运行时按需注入

- Agent Skills（Skills API）：为 Agent 附加领域专业知识，让通用 Agent 在特定任务上表现得更专业

- 持久化记忆（Memory Stores API）：让 Agent 的学习成果与产出跨 Session 持久保留

6、一个Skill，即可轻松调用

我们把整个API对接的流程做成了skill, 直接调用cloud agents skill ，即可快速打造AI-Native应用。

了解更多，欢迎加入Qoder Cloud Agents 用户交流钉钉群:183685011067