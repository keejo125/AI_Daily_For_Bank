---
publish_time: 1787737468
link: https://www.infoq.cn/article/3F8I0zcLfC5wcENtLASD
source: InfoQ
status: confirmed
category: 国际
is_model_related: false
digest: |
  英伟达在 Hot Chips 披露 Vera Rubin 平台多项进展：面向低延迟推理的 Groq 3 LPX 量产，在 10 万 Token 上下文、Gemma 4 31B 下达每秒 3400 输出 Token，提速智能体等长链路负载；Spectrum-X 多平面以太网在不加第三层网络下扩展至 51.2 万 GPU；BlueField-4 的 Scale-In 接管 AI 工厂安全、存储与运维；NVLink Fusion 接入云厂自研 XPU/CPU。
---

# 英伟达公布 Vera Rubin 最新进展：推理、网络和定制芯片全面升级

> 原文链接：https://www.infoq.cn/article/3F8I0zcLfC5wcENtLASD
> 来源：InfoQ

当地时间8月24日，在Hot Chips大会期间，英伟达集中披露了新一代AI基础设施的多项进展。

面向低延迟推理的NVIDIA Groq 3 LPX已经进入全面量产，Nebius将成为首家采用者；

Spectrum-X以太网引入多平面架构，目标是在不增加第三层网络的情况下扩展至51.2万颗GPU；由BlueField-4和DOCA支持的Scale-In，则开始接管AI工厂的安全、存储访问和运维任务；NVLink Fusion进一步把云厂商自研的XPU和CPU接入英伟达机架体系。

这些并非彼此独立的产品。英伟达正在围绕Vera Rubin构建一套更完整的“AI工厂”：GPU负责训练和通用推理，Groq 3 LPX提高Token生成速度，NVLink完成机架内互连，Spectrum-X连接大规模集群，Scale-In处理基础设施服务。

Groq 3 LPX量产，专门加速Token生成

Groq 3 LPX被英伟达定义为“交互式AI推理加速器”。它并非用于替代Vera Rubin GPU，而是作为Vera Rubin平台的扩展，专门提高推理生成阶段的Token输出速度。

代码智能体等应用不会在一次推理后结束任务，而是需要反复读取文件、编写和测试代码、调用工具、检查结果。在数百甚至数千个执行步骤中，单次生成延迟会不断累积，最终影响一个任务需要几分钟还是几小时完成。

英伟达称，Groq 3 LPX在Artificial Analysis使用Gemma 4 31B开放模型进行的测试中，在10万Token上下文条件下达到每秒3400个输出Token，并将其描述为该模型目前有记录以来的最快成绩。

据介绍，在智能体和其他延迟敏感型负载上，其响应速度可达到最接近替代平台的4倍。

首批部署将来自AI云服务商。Nebius计划把Groq 3 LPX接入生产级推理平台Nebius Token Factory，开发者可以继续使用原有API，无需迁移软件栈。继Nebius之后，Groq也计划成为早期采用者之一。

Spectrum-X多平面：不增加第三层网络

Groq 3 LPX解决Token生成速度，Spectrum-X多平面则负责扩大集群。

传统两层以太网集群达到一定规模后，往往需要增加第三层网络，随之而来的是更多交换跳数、延迟、抖动，以及交换机、光模块和布线成本。

Spectrum-X多平面采用另一种方式：将每台服务器的网络连接拆分成多个独立“平面”，每个平面运行一套两层网络。多个网络平面组合后，整体最高可扩展至51.2万颗GPU，而应用看到的仍然是一条完整连接。

流量分配由ConnectX SuperNIC内置的硬件引擎完成。一个网络平面发生故障时，SuperNIC会将流量重新分配至其他平面。

在八平面拓扑中，一个平面失效后，系统仍可保留约90%的总带宽。英伟达称，其基于硬件恢复速度比基于软件多平面负载均衡的恢复速度快了11倍，并可使AI工厂产出提高1.6倍。

Spectrum-X SN6000系列交换机采用102.4Tb/s Spectrum-6以太网ASIC，配合ConnectX-9 SuperNIC，可为每颗GPU提供最高1600Gb/s的带宽。Spectrum-XGS则把网络扩展到多个数据中心，英伟达称其可将多站点NCCL集合通信性能提高1.9倍。

Scale-In接管安全、存储和运维

GPU集群扩大后，需要处理的不只是模型数据。用户访问、存储请求、身份验证、安全检测和监控流量同样会消耗计算资源。

为此，英伟达推出了Scale-In，并将其称为AI网络体系的“第五大支柱”。

Scale-In由BlueField-4处理器和DOCA软件平台支持，通过Spectrum-X以太网连接。它将多租户网络、存储访问、安全、资源配置和实时可观测性从主机侧分离出来，放入独立的硬件加速域，避免这些任务持续占用CPU和GPU。

如果说NVLink解决机架内部的Scale-Up，Spectrum-X解决跨机架的Scale-Out，那么Scale-In处理的是用户、数据、存储和基础设施服务如何进入AI工厂。

这也意味着，英伟达定义的AI工厂已经不只是一个GPU集群，而是开始覆盖计算任务进入、运行、存储和管理的完整过程。

另外一侧，NVLink Fusion解决的则是另一个问题：当云厂商开始开发自己的AI芯片，如何将这些定制XPU部署到成熟的机架系统中。

过去，NVLink主要用于英伟达GPU之间的高速互连。NVLink Fusion将这一能力延伸到第三方XPU和CPU，使超大规模云厂商能够把自研芯片接入NVLink、NVLink Switch和MGX机架架构。

NVLink Fusion包括第六代NVLink、NVLink Switch和用于连接XPU与CPU的NVLink-C2C。NVLink Fusion将XPU引入NVIDIA NVLink纵向扩展互连域。

第六代NVLink提供领先的高带宽、低延迟网络实现72个XPU的互连域。与基于通用以太网的替代解决方案相比，XPU到XPU传输的端到端延迟降低至三分之一，数据包速率提高10倍。NVIDIA NVLink-C2C技术，可将XPU连接到NVIDIA Vera CPU或其他生态系统CPU，能效最高可达PCIe接口的6倍，显著减少代理式AI系统在控制和计算之间的性能瓶颈。

采用者还可以沿用MGX机架，以及相应的供电、液冷、网络、管理软件和制造供应链。这使云厂商能够在相似的基础设施中部署英伟达GPU或自研XPU，并根据供应情况和工作负载调整芯片组合。

英伟达将这一策略概括为“纵向整合、横向开放”。这里的开放不是将NVLink变成完全独立的通用标准，而是允许第三方芯片进入英伟达定义的机架级体系。

英伟达要定义的不只是一颗GPU

将此次公布的产品放在一起，英伟达的路线已经较为清晰：Groq 3 LPX负责低延迟Token生成、NVLink和NVLink Fusion负责机架内部互连、Spectrum-X多平面负责跨机架扩展、Spectrum-XGS连接多个数据中心加上Scale-In负责安全、存储和运维服务。

这套架构背后的判断是，未来AI系统的性能不会由某一颗芯片单独决定。

计算速度、Token生成延迟、网络、存储、安全和运维必须被共同设计。

对英伟达而言，这也意味着竞争边界正在从GPU扩大到整座AI工厂。因此，此次Hot Chips披露的更像是一张完整的技术路线图。

真正需要等待验证的是，这套覆盖计算、网络和运维的架构，能否将基准测试中的性能提升转化为客户可以衡量的成本、稳定性与产出。