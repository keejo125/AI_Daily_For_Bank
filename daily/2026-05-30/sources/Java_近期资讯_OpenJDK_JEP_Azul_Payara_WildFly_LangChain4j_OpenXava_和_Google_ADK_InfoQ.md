---
publish_time: 1780106400
---

# Java 近期资讯：OpenJDK JEP、Azul Payara、WildFly、LangChain4j、OpenXava 和 Google ADK

> 原文链接：https://mp.weixin.qq.com/s/NdyUYL4Nm4J8JIvq43oz3g
> 公众号：InfoQ

作者 ｜ Michael Redlich
译者 ｜ 张卫滨
OpenJDK
JEP 523：在所有环境中将 G1 设为默认垃圾回收器（Make G1 the Default Garbage Collector in All Environments），已经从
Candidate
状态提升为 JDK 27 的
Proposed to Target
状态（参见公告）。该 JEP 提议将 Garbage-First 垃圾收集器（G1 GC）设为“所有环境下的默认选项，而不仅是服务端环境”。如果命令行未显式指定垃圾回收器，HotSpot JVM 将始终选择 G1 GC。评审会于 2026 年 5 月 19 日结束。
JEP 534：默认启用紧凑对象头（Compact Object Headers by Default），也已经从
Candidate
状态提升为 JDK 27 的
Proposed to Target
状态（参见公告）。该 JEP 提议把 JDK 25 交付的 JEP 519：紧凑对象头（Compact Object Headers）设为 HotSpot JVM 默认的对象头布局。关于该特性的更多背景可参考 InfoQ 此前的报道：Java 24 中的紧凑对象头。评审会于 2026 年 5 月 19 日结束。
JEP 537：Vector API（第 12 轮孵化），先由
JEP Draft 8381663
升级为
Candidate
，后又升级为 JDK 27 的
Proposed to Target
（公告参见此处和此处）。该 JEP 提议进行第 12 轮孵化，在 JDK 16 到 JDK 26 完成 11 轮孵化后，与 JDK 25 相比在实现层面没有重大变化。该特性引入了一个 API，用于“表达可在运行时可靠编译为受支持 CPU 架构上最优向量指令的向量计算，从而获得优于等价标量计算的性能”。Vector API 将继续孵化，直到Valhalla 项目的必要特性以预览形式可用。届时团队将适配 Vector API 及其实现，并将其从
孵化（Incubation）推进到预览（Preview）状态
。评审会于 2026 年 5 月 19 日结束。
JEP 538：密码对象的 PEM 编码（PEM Encodings of Cryptographic Objects）已经从
JEP Draft 8376991
提升为
Candidate
状态（参见公告）。该 JEP 提议在 JDK 25 与 JDK 26 两轮预览之后，将该特性经修改后正式定稿。该特性提供“用于将表示加密密钥、证书和证书吊销列表的对象编码为广泛使用的 Privacy-Enhanced Mail（PEM）传输格式，以及从该格式解码回对象的 API”。该 JEP 将支持 PEM 文本与PKCS
#8
、X.509二进制格式密码对象之间的转换。变更包括，将 PEM record 类重新定义为常规类，以便提供可接受 Base64 编码字节数组内容的构造器；将
DEREncodable
接口重命名为
BinaryEncodable
，以更准确描述 PEM 文本中存储的二进制数据。
甲骨文宣布，随着苹果逐步停止对 x64 架构的支持，macOS/x64 移植版本的维护将在 JDK 27 发布后结束。不过，如果有开发者愿意继续维护该移植版本，团队表示欢迎，但也提醒这将需要显著的时间与投入。
JDK 27
JDK 27早期访问构建版本的Build 22发布，包含对 Build 21 的更新，并修复了多项问题。更多细节可参见发布说明。
针对JDK27，开发者可通过Java Bug Database提交缺陷报告。
Azul Payara
在Azul 收购 Payara五个月后，团队推出了
Azul Payara Community
作为 Payara Platform Community 的新名称。开发者仍可选择使用
Azul Payara Server Community
或
Azul Payara Micro Community
构建应用。官方 Logo 也已随之更新。
在该博客中，Azul 的 Payara Community、Jakarta EE 与 Foojay.io 高级开发者布道师Dominika Tasarz-Sochacka表示，此次品牌更新对 Java 社区意味着：
这次品牌调整是将 Azul Payara Community 正式纳入 Azul 产品组合的一部分，与 Azul Zulu（OpenJDK）、Azul Prime、Intelligence Cloud 以及 Azul Payara 商业版本并列。它仍是同一个开源项目，只是进入了更大的 Azul 生态中。
团队还发布了 2026 年 5 月版的 Azul Payara 7，包含缺陷修复、安全修复、依赖升级及多项改进，例如，更新
JaccProviderCompatibilityStartup
类，将遗留的 Payara 6 JAAC 提供者与策略配置工厂（policy configuration factory）分别迁移到 Eclipse Exousia 的
DefaultPolicy
和
DefaultPolicyConfigurationFactory
；新增 Payara 部署描述符，以反映对 Jakarta EE 11 支持的更新，并移除此前错误实现的托管执行器（managed executors）、托管调度执行器（managed scheduled executors）、托管线程工厂（managed thread factories）和上下文服务（context services）的定义能力。更多信息可见以下版本说明：Community Edition 7.2026.5、Enterprise Edition 6.38.0、Enterprise Edition 5.87.0。
Micronaut
Micronaut 基金会发布了Micronaut Framework 4.10.14 版本（基于Micronaut Core 4.10.23），包含了缺陷修复、对Micronaut Data的补丁更新，并将依赖升级到Netty 4.2.13。该 Netty 版本修复了十余个 CVE 问题。更多信息参见发布说明。
WildFly
WildFly 团队推出了新的开源命令行工具wado，用于在 domain 模式和 standalone 模式下构建并运行不同版本的 WildFly 容器。wado 由 Rust 编写，其名称是 WildFly admin containers 的缩写，允许开发者基于合理的默认值快速启动容器，包括命名、端口和凭据。
LangChain4j
LangChain4j 1.15.0 正式版（连同第 25 个 Beta 版）发布，带来缺陷修复、依赖升级和新特性，例如，集成Docling文档解析器；在
@P
注解中新增
defaultValue()
属性，使工具开发者可以在 LLM 未提供参数时指定运行时的兜底值。更多信息参见发布说明。
OpenXava
OpenXava 7.7.2发布，带来缺陷修复、文档改进、依赖升级及功能增强，例如，优化
AGENTS.md
文件以改进编写新动作时的 AI 代码生成效果；支持通过简单提示词添加仪表盘。更多细节参见发布说明。
Google Agent Development Kit
Java 版 Agent Development Kit（ADK） 1.3.0 发布，包含缺陷修复和新特性，例如，新增
ChatCompletionsHTTPClient
类，提供支持 Google Cloud Apigee API 的聊天补全接口；新增
SkillSource
接口，支持从多种来源加载 ADK skill。更多信息参见发布说明。
查看英文原文：
Java News Roundup: OpenJDK JEPs, Azul Payara, WildFly, LangChain4j, OpenXava, Google ADK（
https://www.infoq.com/news/2026/05/java-news-roundup-may11-2026/
）
声明：本文由 InfoQ 翻译，未经许可禁止转载。
点击底部
阅读原文
访问 InfoQ 官网，获取更多精彩内容！
今日好文推荐
米哈游一夜烧掉200万元Token，大厂高管也开始质疑：Token烧不出价值，但养肥了谁？
Opus 4.8 刚发布，被DHH和Redis之父当场拆台：跑分赢了GPT-5.5，但编码王座不稳了
前 CEO 被学生嘘“别吹AI”，现 CEO 被追问“会不会被AI取代”：谷歌两代掌门人的AI信仰，同时被质疑
中国首次提出半导体演进新原则：华为“韬定律”5 年内冲刺等效1.4nm制程，麒麟、昇腾将先后落地量产