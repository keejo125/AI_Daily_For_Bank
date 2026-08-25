---
publish_time: 1787652000
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/L1MD4XJIFFqEKOBWimsHIA
source: 阿里云基础设施
title: 'AgenticFS 重磅发布：专为 AI Agent 打造的全新文件存储'
---

# AgenticFS 重磅发布：专为 AI Agent 打造的全新文件存储

来源：阿里云基础设施

阿里云正式发布文件存储全新规格 AgenticFS，这是一款面向 AI Agent 场景设计的 Agent
Nativ
e 的文件存储。单个 AgenticFS 文件系统可管理百万级 Agent 工作空间（AgenticSpace），并为每个工作空间提供独立的权限、配额与性能隔离，支持 10 万 QPS 挂卸载能力。
AI Agent 应用已从单纯的模型调用，演进为具备工具调用、任务执行和环境交互能力的自主系统，而文件系统是 Agent 的主要交互界面。AI Agent 正在越来越多地走向规模化、场景化落地, 从服务于人类用户转变为服务于 Agent。这一转变对存储提出了新的挑战：
规模跃升
：每个 Agent 都需要独立工作目录，单文件系统的租户规模从千级迈向百万级，挂载点数、配额数、挂载卸载 QPS 随之扩大几个
数量级
；共享的 Skills 目录需要支撑
数十万 Agent 并发访问。
目录级安全隔离
：
Agent 执行路径由大模型动态生成，容易被诱导走向破坏性路径，越权访问一旦发生就是数据安全事故。个别 Agent 的异常行为会消耗大量存储资源，进而影响同一平台上其他 Agent 的性能。因此要求每 Agent 工作目录具备独立的权限控制、配额管理和 QoS 能力。
AgenticFS 重新定义 Agent Native 文件存储
为了满足 AI Agent 场景需求，AgenticFS 为平台上的每个 Agent 或每个终端用户分配独立的 Agent 工作空间，即 AgenticSpace，用于存储会话记录、记忆数据、MarkDown 文件、Skill 等持久化数据；同一 Agent 的多次会话对应 AgenticSpace 下的不同子目录。基于 AgenticSpace 支持
访问隔离、配额管理、性能隔离
。
大规模与弹性挂卸载
：
基于跨集群、跨可用区的
分布式编排架构
：单个 AgenticFS 文件系统
支持百万规模
AgenticSpace 的动态创建，10 万 QPS 挂卸载；未来可扩展至
亿级
AgenticSpace 与
亿级
元数据 QPS；单个 AgenticFS 支持
百 PiB
容量，
5 万亿
文件数
。
零信任安全隔离
：
为每个 AgenticSpace 配置独立的接入点（Access Point）与访问策略
；
独立安全凭证
杜绝跨 Agent 泄露，
临时凭证
攻击窗口收敛至最小。
弹
性共享与按需伸
缩
：
支持共享挂载，容量按需
弹性伸缩
，
支持
计算资源弹性伸缩至零
。
企业级特性
：
后续将发布
生命周期管理
降低存储成本，
回收站与备份
防御误删风险，
云监控和审计日志
使 Agent 行为可观测、可分析。
如何开始使用
在
控制台
创建 AgenticFS 文件系统；新 Agent 注册流程：创建 Sandbox → 通过 OpenAPI 创建 AgenticSpace → 为其创建 AccessPoint → 设置容量与文件数配额 → 挂载 AgenticSpace；动态挂载时延约 1~3 秒。Agent 唤醒时只需 Sandbox 唤醒 → 查询 AccessPoint → 重新挂载。
AgenticFS 默认按量付费，0KiB 起步，按实际使用量付费，中国大陆地域参考价 0.85 元/GiB/月。
AgenticFS 解决了百万级 Agent 并发下的性能瓶颈、安全隔离和资源管理难题，为 AI Agent 规模化落地提供了基础设施基石。
了解更多，戳文末
「阅读原文」
获取 AgenticFS 详细产品规格与最佳实践。
