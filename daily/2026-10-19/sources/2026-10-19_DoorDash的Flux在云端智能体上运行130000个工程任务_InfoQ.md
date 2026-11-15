---
publish_time: 1792395720
link: https://www.infoq.cn/article/4IPptJpXQqX5Lr77uBFZ
source: InfoQ
status: confirmed
category: 国际
is_model_related: false
digest: |
  外卖平台 DoorDash 已将工程智能体工作负载从开发者笔记本迁移至自研 Flux 云平台，2026 年单月自动化完成 13 万个工程任务，每周支撑超 2.5 万次自动化代码审查，拥有 300 多个 Playbook、每周超 1 万次触发调用，支持工作流无人值守并行运行。Flux 基于云端 Sandbox、MCP 网关、可复用 Playbook 与触发方式四类原语构建；本地执行受算力、在线时长与安全限制，迁移后工程师可从 Slack、GitHub 或定时任务触发智能体，并保留完整企业安全护栏。
---

# DoorDash的Flux在云端智能体上运行130000个工程任务

> 原文链接：https://www.infoq.cn/article/4IPptJpXQqX5Lr77uBFZ
> 来源：InfoQ

DoorDash已经将工程智能体工作负载从开发者的笔记本迁移到其Flux云平台"上，该平台在2026年单月自动化完成了130000个工程任务。该平台每周支持超过25000次的自动化代码审查，拥有超过300个Playbook和每周超过10000次的触发调用，允许工作流无人值守并行运行。

DoorDash在其智能体工作负载在单台笔记本上运行时遇到限制后开发了Flux。本地执行受限于可用的CPU与内存，依赖开发者设备保持在线，并可能让自治智能体访问开发者已拥有的凭据与内部系统。DoorDash还表示，本地执行使得监控智能体的运行位置、它们访问的系统以及它们代表谁操作变得更难。

安全架构师Radoslav Krehlik"在LinkedIn上就Flux发布了一条帖子"，这样写到：

它是在基于笔记本的智能体遇到算力、正常运行时间和安全限制后构建的。工程师可以从Slack、GitHub或定时任务触发智能体，而DoorDash保持了完整的企业安全护栏。

Flux是基于四个平台原语构建的，分别是云端Sandbox、MCP网关、可复用Playbook和触发方式（invocation surface）。Playbook定义工作内容，Sandbox提供隔离的执行环境，网关控制对内部系统的访问，触发方式则允许通过Slack、GitHub、Cron、命令行或会话接口启动工作流。

这些Sandbox使用Firecracker微虚拟机（Firecracker micro virtual machines）" 来隔离智能体工作负载。每个环境都预配置了任务所需的仓库、开发工具、密钥以及运行时依赖。根据DoorDash的报告，端到端Sandbox的搭建（包括启动microVM、克隆仓库、安装构建工具和配置编码智能体harness）的第95百分位目标在五秒以内。

智能体通过Agent Gateway访问DoorDash的内部系统，Agent Gateway是一个内部的MCP网关，提供有范围限制的权限并记录智能体的活动以供审计和策略执行。基于YAML定义的Playbook会指定任务、所需工具、权限、校验和安全边界。它们可以将智能体驱动的步骤与确定性代码结合，并在需要可预测执行或校验的地方使用它们。

TOP GROUP Vietnam的联合创始人Duy Nguyễn"在LinkedIn上就Flux发布了一条帖子"，他写到：

一旦智能体处理后台工作、代码审查、内部工具和并发执行，那么困难就会从模型选择转向控制：身份、权限、沙箱、审计日志、配额以及真正的终止开关。

这一做法是编程智能体向基于云端的执行模式迈进的更广泛趋势的一部分。GitHub为Copilot提供了本地和云端两种Sandbox环境，并允许开发者对文件系统、网络及系统访问权限进行控制。其云端Sandbox为智能体提供了隔离的执行环境，使其能够在运行编码任务时不占用本地开发者的计算资源。关于其基于云端的执行模型，GitHub的官方文档"提供了更多详细信息。

DoorDash最初使用Flux进行自动代码审查，该公司将这一环节描述为一种高频且效果可衡量的工作流。随后，该公司将该平台的应用范围扩展到了CI分流、值班任务、日常维护工作流以及由工单（Ticket）驱动的开发任务中。此外，DoorDash还将其Slack的集成方式从私密频道改为了公开讨论链（Public threads），以便工程师们能够观察智能体的执行过程、审查执行结果，并了解其他团队是如何分配和委派任务的。

查看英文原文：DoorDash’s Flux Runs 130,000 Engineering Tasks Through Cloud-Based Agents"