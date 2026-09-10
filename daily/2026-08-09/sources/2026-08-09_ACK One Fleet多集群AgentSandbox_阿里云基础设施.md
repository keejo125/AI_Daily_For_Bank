---
publish_time: 1786278178
link: https://mp.weixin.qq.com/s/JqnNmnNMlB6KDO0rSqoZ6A
source: 阿里云基础设施
status: confirmed
category: 国内
is_model_related: false
digest: |
  阿里云ACK One Fleet发布多集群Agent Sandbox方案，解决单集群容量天花板和故障域集中问题。方案支持E2B SDK与Kubernetes CR双协议链路，全局控制面与数据面分离，仅代理控制面流量、数据面由子集群自行完成。核心调度能力包括：全局水位视图+实时资源路由+跨集群故障转移+削峰填谷+预热池亲和调度。Sandbox本身提供MicroVM级隔离、内存级休眠唤醒和Checkpoint克隆，最高每分钟15K弹性扩展。对业务方而言，将单集群的容量和可用性上限一举打开，实现大规模多地域高可用部署，同时提升资源利用率和启动速度。
---

# ACK One Fleet：让Agent Sandbox从"单集群"走向"多集群"

来源：阿里云基础设施
原文链接：https://mp.weixin.qq.com/s/JqnNmnNMlB6KDO0rSqoZ6A

从"能聊天"迈向"能干活"，每一个执行任务的AI Agent，背后都需要一个安全、隔离、随起随停的运行环境 —— Agent Sandbox（智能体沙箱）。而随着Agent大规模落地及规模持续增长，单Kubernetes集群很容易遇到以下问题：

容量瓶颈：Sandbox本质上仍然是消耗计算、网络和存储资源，单集群承载能力有上限。故障风险集中：单集群是一个故障域。在K8s集群管控面故障/Sandbox管控面故障时，无法再为客户提供服务。

而如果客户自己管理多个集群，又可能会面临调度效率不足等问题：缺乏全局水位视图、无法按实时资源路由、缺少集群健康感知与故障转移、利用率低且运维重。

所以ACK One Fleet的多集群Agent Sandbox目标很明确：提升总Sandbox规模，高可用，故障failover，并且利用多集群调度能力提升资源利用率和Sandbox启动效率。

ACK One Fleet是阿里云面向多集群、多地域Kubernetes场景的统一管理平面。它纳管自建的、其他云的、以及分布在不同Region的ACK集群。在此基础上，Fleet针对Agent Sandbox场景做了专门的调度增强，把"单集群K8s能做的事"升级成了"多集群协同能做的事"。用户只需集中到一个入口，几乎不用改动就可以像使用单集群时一样使用多集群Agent Sandbox。

架构与核心能力：E2B与K8s CR两条链路。E2B SDK链路实现了控制面与数据面分离，仅代理控制面流量（Agent Sandbox的生命周期管理），数据面流量由子集群自行完成。此外还具有：单集群容量控制、水位均衡调度、多集群故障转移、预热池感知与亲和调度等全局调度能力。K8s CR链路则适合深度使用Kubernetes的企业团队，提供声明式管理，并额外支持集群级的优先级调度。

总结来看，ACK One Fleet的多集群Agent Sandbox把单集群的容量、故障域天花板一举打开，对业务方收益可概括为：大规模（多管控面分摊压力）、多地域高可用、资源利用更充分、启动更快。未来还会围绕Agent业务持续增强多集群调度能力。
