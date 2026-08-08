---
publish_time: 1786070308
status: pending

link: https://www.infoq.cn/article/sQW5F63ZP4QMyhlWAzQi---

# HBM 不够用了，AI SSD 迎来爆发前夜

> 原文链接：https://www.infoq.cn/article/sQW5F63ZP4QMyhlWAzQi
> 来源：InfoQ

HBM 装不下、数据搬不动，SSD 开始进入实时路径

大语言模型推理正在同时撞上两堵墙：一堵是容量墙，另一堵是 I/O 墙。模型参数持续扩大，长上下文、多轮对话和智能体任务又让 KV Cache 快速膨胀；MoE 模型虽然降低了单次计算的激活参数量，却需要保存远大于显存或内存容量的专家权重。在云侧算力中心，昂贵的 HBM 被模型权重和 KV Cache 长期占用，GPU 有效利用率受制于数据搬运；在边缘侧和端侧，有限的 DRAM 或统一内存则直接限制了本地可运行模型的规模。

当显存和内存越来越难以独自承接推理负载，SSD 开始从模型文件的静态存放设备进入大模型推理的实时数据路径，成为 HBM、VRAM 和 DRAM 之后的一层正式存储层级。

这一变化最早在推理基础设施和集群架构中得到清晰体现。月之暗面的 Mooncake 采用以 KV Cache 为中心的分离式推理架构，将 GPU 集群中原本未被充分利用的 CPU、DRAM 和 SSD 组织为分布式缓存资源[1]；Mooncake Store 进一步支持由 DRAM 与 SSD/NVMe 构成的多级缓存，使冷数据能够在容量更大、成本更低的闪存层长期保留[2]。

2026 年，英伟达推出 CMX 上下文内存存储平台，在 Vera Rubin 基础设施中增加一个面向 KV Cache 优化、通过以太网连接的闪存层级，由 BlueField-4 负责 NVMe SSD 管理、数据保护和网络传输。英伟达将其定义为介于 GPU 内存与共享存储之间的 pod 级上下文层[3]。产业信号已经很明确：SSD 正在成为推理系统需要直接调度的资源，而不再只是模型加载前后的外围设备。

问题是，推理系统开始调用 SSD，并不等于传统 SSD 已经适合承担常驻推理任务。

传统 SSD 面向文件和块数据存储设计，性能指标主要围绕顺序带宽、随机 IOPS、数据可靠性与单位容量成本展开；LLM 推理需要的却是具有严格时序约束的数据供应。KV Cache 会在prefill 阶段集中生成并持续写入，在后续请求中按会话、模型层和 Token 位置反复读取；MoE 推理则需要根据路由结果，在每一层计算前及时取得特定专家权重。一次读取未能赶上计算窗口，就可能让 GPU、NPU 或 CPU 进入等待状态，而 SSD 在高队列深度下取得的峰值 IOPS，并不等同于低队列深度、细粒度访问时的稳定延迟。

这种矛盾还延伸至 SSD 内部。NAND Flash 以页为单位读取、以块为单位擦除，FTL 需要执行地址映射、垃圾回收和磨损均衡，容易产生写放大与尾延迟；持续写入 KV Cache 还会对闪存寿命提出远高于普通消费负载的要求。

传统 LBA 排布并不了解模型层、MoE 专家、KV 块及其访问顺序之间的语义关系，相互关联的数据可能被分散到不同物理位置，难以形成可预测的并行读取。文件系统、块设备和 NVMe 软件栈中的排队、中断、数据复制与页缓存，也会增加端到端延迟。如果缺少面向模型执行顺序的地址布局、缓存划分、优先级调度、异步预取和寿命管理，SSD 虽然拥有 TB 级容量，却仍难以像 DRAM 或 VRAM 一样稳定参与每一个 Token 的生成。

AI SSD 分成两条路线：强化 I/O，还是直接参与推理调度？

于是，市场上出现了多种被称为“AI SSD”的产品。但到目前为止，“AI SSD”仍没有统一的技术定义，主流方案大致可以分为两类。

第一类可以称为“AI 负载强化型企业级 SSD”，如图 1 所示。这类产品仍以块存储设备为基本形态，但其设计指标开始围绕 AI 集群的数据路径重新排序。英韧科技的洞庭 N3X 系列是这一方向的代表之一。

图1：AI 负载强化型企业级 SSD 的代表性产品：英韧科技洞庭 N3X 与华为 OceanDisk LC 560。

该系列针对训练、微调和推理中的高频缓存数据访问，采用 XL-Flash、SLC NAND 等低时延、高耐久介质，重点服务 KV Cache 卸载和高并发临时数据读写。据公开材料披露，与传统 TLC SSD 相比，相关方案的访问时延可降低至约三分之一，写入吞吐量提高至约三倍，DWPD 则提高约 17-33 倍；其价值不只是提高峰值性能，更在于减少持续写入、垃圾回收和高队列深度下的性能波动。英韧还规划向 PCIe 6.0 以及 NVMe/CXL 双协议产品演进，并提出从千万级 IOPS 继续向更高随机访问能力发展的路线，希望使 SSD 能够承接更多原本驻留在高成本内存中的热数据[4]。

华为 OceanDisk 则采用系列化产品组合覆盖不同 AI 负载。OceanDisk EX 560 强调极高随机写入性能、微秒级写入时延和高写入耐久性，主要面向模型微调、检查点保存及高频缓存写入；SP 560 在性能、耐久性和成本之间进行平衡，针对 AI 一体机和集群推理中的 KV Cache、长上下文及多并发访问；LC 560 则将重点放在容量密度和顺序读取带宽上，单盘容量最高达到 245TB，用于承载训练语料、多模态数据、向量库和大规模模型文件。华为还通过 DiskBooster 等驱动软件推动 SSD 与 HBM、DDR 形成分层协同，使高性能企业级 SSD 进一步进入内存扩展和缓存卸载路径[5]。

这说明 AI 负载强化型企业级 SSD 并非单一规格，而是正在分化为极致性能盘、高性价比推理盘和超大容量盘等不同产品线。

第二类 AI SSD 更进一步，试图改变 SSD 在计算机中的运行逻辑：通过主控、固件、中间件以及 OS 或主板层协同，建立近似于“NAND Flash 与 DRAM/VRAM 联合虚拟化”的多级存储体系，使部分模型权重、MoE 专家和 KV Cache 在推理运行期间驻留于 SSD，并按照计算进度动态换入内存。它兼容传统 SSD 的数据存储功能，同时增加面向 LLM 的数据感知、调度和预取能力，因此既可以形成企业级产品，也可以进入 AI PC、工作站和边缘计算设备。

在这一类别中，群联（Phison）和江波龙目前主要从存储侧展开探索，如图2 所示。两家厂商都试图把 NAND 从模型文件的静态存放位置，转变为 DRAM 或 VRAM 之外的高容量运行时数据层，但在产品组织方式、软件入口和目标市场上形成了不同侧重。

图 2：存储侧推理参与型 AI SSD 探索：群联 aiDAPTIV 缓存 SSD、江波龙 SPU＋iSA 方案以及寅谱-联芸 AI SSD 方案。

群联的 aiDAPTIV 方案由 aiDAPTIVCache 专用缓存 SSD、内存管理中间件和配套工具链组成。其核心机制是将超过 VRAM 容量的模型权重切分为多个数据块，根据模型执行过程在 VRAM 与 SSD 之间进行流式传输：当前需要参与计算的权重优先保留在 VRAM 中，暂时不活跃的权重则下沉至 SSD，从而在不继续增加 GPU 数量的情况下扩展可加载模型的规模。对于推理场景，aiDAPTIV 还会保存原本可能被逐出的 KV Cache，并在后续上下文复用时从 SSD 回取，减少重新执行 Prefill 和重建缓存的开销。其专用缓存 SSD 强调低时延和高耐久性，群联公开资料给出的产品耐久性最高达到 100 DWPD，多个缓存 SSD 可提供 TB 级的扩展内存空间[6]。

群联的商业化思路并不是单独销售一块普通 SSD，而是将高耐久缓存盘、中间件、安装工具和经过验证的计算机配置组合成可部署方案，并通过整机厂商和渠道合作伙伴进入教育、科研、政府、企业私有化部署以及本地模型微调市场。

江波龙选择了“SPU 硬件执行＋iSA 软件决策”的路线。其 WM8500 SPU 不再被定义为只负责数据搬运的传统 SSD 控制器，而是集成存储控制、压缩、缓存和数据调度能力，并由 iSA 感知推理负载、制定数据分层和预取策略。根据江波龙公开材料，SPU 采用 5nm 工艺，支持存内无损压缩、HLC 高级缓存和混合 NAND 调度；其中，存内压缩用于提高有效容量和带宽利用率，HLC 允许 SSD 承接原本驻留在 DRAM 中的温数据和冷数据，混合 NAND 机制则根据冷热程度在不同介质区域之间调度数据。相关设计使 SPU 既可以用于消费级 AI SSD，也可以向高容量企业级 SSD、工作站和端侧智能设备扩展[7]。

与群联更强调 VRAM 扩展和模型权重流送不同，江波龙将压缩、冷热识别、缓存分区和预取调度进一步集成到 SPU 与 iSA 体系中，试图把 SSD 主控从数据通道升级为存储侧智能调度节点。

另一条路线由联芸（Maxio）与寅谱（Infplane）组成的技术联盟推进，如图 2 所示。寅谱（Infplane）在大模型推理芯片，以及计算机 OS 和主板侧的处理器、内存与存储协同控制方面具有较多技术积累。双方合作形成 AI SSD 的过程，并非简单地在传统 SSD 上叠加一层推理软件，而是将寅谱原本用于推理芯片的部分技术栈——尤其是其中关于多级缓存、数据调度、并行搬运和预测式预取的技术——抽取出来，与联芸对 NAND Flash、SSD 主控和固件的控制能力结合，形成一套跨越计算侧与存储侧的 AI SSD 架构。

具体而言，该方案围绕 MoE 专家、KV Cache 和数值精度三个维度开展数据切分、冷热分层、并行搬运与预测式预取：一方面根据模型执行过程调度不同专家权重和 KV Cache，另一方面将模型文件的数值精度分为较热的低精度位和较冷的高精度位进行特殊的读写和存放。按照联盟披露的技术方向，该方案将模型和推理框架兼容性作为核心设计目标，力图在不修改模型文件、不侵入主流推理框架的条件下适配不同处理器平台，并降低对特定 SSD 模组形态的限制。

其潜在价值在于，同时改善本地设备可承载的 MoE 模型容量、prefill 数据复用效率和 decode 阶段的数据供应；相应代价是需要贯通 middleware、firmware与controller，软硬件协同范围更深，研发成本和工程验证难度也明显更高。联芸已经公开提出，AI 推理正在推动 SSD 主控从传统数据通道走向面向 Token 成本的智能调度[8]；其横跨消费级、工业级和企业级市场的主控产品基础，也为相关技术进入不同 SSD 模组和整机形态提供了较大的产业化空间[9]。

从完整的推理数据路径看，不同 AI SSD 方案覆盖的技术层级并不相同：部分产品主要强化 SSD 介质与 I/O 能力，部分方案进一步参与模型权重、KV Cache 和 MoE 专家的运行时调度，而寅谱—联芸方案则试图贯通计算侧缓存体系、middleware、firmware、controller与NAND介质管理。

各路线在模型加载、prefill、decode 和长上下文复用中的作用如图 3 所示。

图 3：AI SSD 在 LLM 推理数据路径中的作用，以及主要厂商技术路线与推理环节的对应关系。

从单盘性能到系统协同，产业竞争才刚开始

从计算机制造商和智算基础设施厂商披露的信息看，群联与寅谱—联芸的方案都已不止于概念展示，正进入产品验证和商业化尝试阶段。其中，寅谱—联芸方案的验证范围已经不再局限于单一主控、单一模组或少数原型机，而是在消费级 AI PC、Mini 工作站、高性能本地推理设备、边缘计算平台和企业级推理节点等多类产品中同步推进，并覆盖不同 CPU、GPU、NPU 及内存架构组合。与此同时，群联也在通过服务器、工作站和边缘 AI 合作伙伴扩大 aiDAPTIV 的落地范围，江波龙则已围绕 AMD 锐龙 AI Max+ 395 完成较深入的端侧 AI 存储适配[6][7]。

相关技术路线尚未完全收敛，但先发企业正在持续积累主控、固件、运行时、模型生态、模组生产和整机验证数据，由此形成初步的生态壁垒与产业壁垒。对于后来者而言，竞争门槛已经不再只是开发一款高带宽、高 IOPS 的 SSD，而是能否建立从 NAND 控制、推理调度到整机适配的完整协作体系。

可以预期，AI SSD 不会取代 HBM、VRAM 或 DRAM，而是通过容量、性能和成本的重新分层，成为更多云侧、边缘侧和端侧设备中的 Token 生成基础设施。当产业评价指标从单纯追求峰值算力转向每 Token 成本、单位功耗吞吐和有效算力利用率时，SSD 的价值也将被重新衡量：它不再只是长期被 LLM 产业低估的外围组件，很可能成为 Token 经济学中的关键变量。

参考文献：
[1] R. Qin et al., “Mooncake: A KVCache-centric Architecture for Serving LLM Chatbot,” 23rd USENIX Conference on File and Storage Technologies (FAST ’25), 2025.
https://www.usenix.org/conference/fast25/presentation/qin"
[2] Mooncake Project, “Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving,” GitHub Repository.
https://github.com/kvcache-ai/Mooncake"
[3] NVIDIA, “Introducing NVIDIA BlueField-4-Powered CMX Context Memory Storage Platform for the Next Frontier of AI,” 2026.
https://developer.nvidia.com/blog/introducing-nvidia-bluefield-4-powered-inference-context-memory-storage-platform-for-the-next-frontier-of-ai/"
[4] 英韧科技，“从N3X到Gen6：英韧科技如何用三大要素打造国产AI SSD”，2026。
https://www.yingren.cn/news/%E4%BB%8En3x%E5%88%B0gen6%EF%BC%9A%E8%8B%B1%E9%9F%A7%E7%A7%91%E6%8A%80%E5%A6%82%E4%BD%95%E7%94%A8%E4%B8%89%E5%A4%A7%E8%A6%81%E7%B4%A0%E6%89%93%E9%80%A0%E5%9B%BD%E4%BA%A7ai-ssd/"
[5] Huawei, “Huawei OceanDisk LC 560 SSD Data Sheet,” 2025.
https://e.huawei.com/en/documents/products/storage/97dc7a1dc98f4d3d90b268db03235cf7"
[6] Phison Electronics, “How aiDAPTIV+ Works.”
https://phisonaidaptiv.com/zh-tw/how-aidaptiv-works/"
[7] 江波龙，“SPU与iSA”，2026。
https://cn.longsys.com/about/news/13353.html"
[8] 联芸科技，“CFMS 2026｜联芸科技：AI推理时代，存储主控芯片价值跃迁”，2026。
https://www.maxio-tech.com/news/11645/13048.html"
[9] 联芸科技，“PCIe接口SSD控制芯片”。
https://www.maxio-tech.com/product/11628/11631/"