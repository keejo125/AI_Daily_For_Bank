---
publish_time: 1788154260
link: https://www.infoq.cn/article/grb2X7v7fr6kUNuuRkvt
source: InfoQ
status: confirmed
category: 国际
is_model_related: false
digest: |
  InfoQ 报道，Kubeflow 发布多项更新迈向 CNCF 毕业：Kale 2.0 可将标注 Jupyter notebook 转生产管道且支持 Kubeflow Pipelines v2；Kubeflow Trainer 与 Flux Framework 集成，统一 MPI 协调的大规模 HPC 模拟与 AI 训练；SDK 加入原生 Spark 支持与微调 LLM 蓝图；即将发布声明式 CRD 驱动的 Kubeflow Notebooks v2。
---

# Kubeflow扩展了AI功能，项目临近CNCF毕业

> 原文链接：https://www.infoq.cn/article/grb2X7v7fr6kUNuuRkvt
> 来源：InfoQ

Kubeflow"项目发布了多项技术更新，以增强Kubernetes上的分布式AI和高性能计算能力。这些进展包括Kale 2.0，这是一个具有原生Spark支持的现代化SDK，以及Kubeflow Trainer功能的扩展。这些发展标志着该项目正向云原生计算基金会（Cloud Native Computing Foundation，CNCF）毕业阶段迈进。

一个重大的更新是Kale 2.0的发布"。这个工具可以将标注的Jupyter notebooks转换为生产就绪的管道，而无需编写任何KFP SDK代码。更新版本现在支持Kubeflow Pipelines v2架构。这使数据科学家能够避免手动创作管道，更快地从实验转向生产。

Kubeflow项目正在迅速推进在CNCF毕业，强调其演进为成熟的、生产就绪的ML生态系统。CNCF博客"

该项目也即将发布Kubeflow Notebooks v2"。这是一个从头开始的重新设计，采用声明式CRD驱动的架构。它为平台团队提供了对交互式环境（比如，Kubernetes上的JupyterLab和VS Code）的模板化控制。Alpha版本现已可用，帮助用户在正式发布前测试这些新功能。

Kubeflow SDK"的技术更新引入了原生Spark支持。这使用户能够在Kubernetes上运行Spark，而无需编写基础设施配置。SDK为数据处理和管道编排以及分布式训练和超参数调优提供了统一的Python接口。它还包括用于微调大语言模型的内置蓝图。计划的更新内容包括添加OpenTelemetry检测和MLflow跟踪，以改进AI生命周期的可观测性。

新的Kubeflow Trainer"旨在通过MPI支持统一的分布式AI训练和高性能的计算工作负载。Andrey Velichkevich在LinkedIn上写到"，该训练器现在正式与Flux Framework进行集成。这允许用户在单个Kubernetes环境中使用Process Management Interface Exascale进行协调，同时运行大规模HPC模拟和AI训练job。

这是在云原生基础设施中采用HPC技术的巨大一步，这对现代GenAI工作负载至关重要。Andrey Velichkevich"

Luca Berton在LinkedIn上指出"，Kubernetes和云原生技术正成为生产环境AI的基础层。他指出，Subaru Corporation最近通过使用Kubernetes和Argo CD在CNCF案例研究竞赛中获胜，将大于30 GB的AI容器镜像的拉取时间从三小时减少到仅三分钟。

核心平台组件也有更新。Model Registry已更名为Hub，以反映它现在包括Model Catalog和MCP Catalog的更广泛范围。这使得用户能够使用OCI作为模型存储的标准来搜索和部署MCP服务器。KServe引入了LLMInferenceService CRD，使大语言模型服务成为一等的平台原语（platform primitive）。此更新支持跨多个节点的分布式推理，并提供与OpenAI兼容的API。

Kubeflow Community Distribution 26.03版本专注于可扩展性和安全性。它已被正式验证支持Kubernetes 1.34及更高版本。本次更新加强了多租户默认设置，并实现了与Pod Security Standards Restricted策略的兼容性，以确保更严格的安全合规性。这些变更帮助组织以更好的可靠性运行大规模的Kubeflow。

通过新的外联项目（Outreach Program ）"和ML体验工作组（ML Experience Working Group），社区参与度也在增加。这些举措旨在通过改进用户界面和为贡献者提供指导来降低参与门槛。

查看英文原文：Kubeflow Expands AI Capabilities as CNCF Graduation Nears"