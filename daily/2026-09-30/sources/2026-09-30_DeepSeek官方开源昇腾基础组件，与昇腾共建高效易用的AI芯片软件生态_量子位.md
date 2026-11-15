---
publish_time: 1790736797
link: https://www.qbitai.com/2026/09/499263.html
source: 量子位
status: confirmed
category: 国内
is_model_related: false
digest: |
  9月30日，DeepSeek正式开源面向昇腾算力平台的基础设施组件，涵盖TileLang高级语言编译工具、高性能计算库与分布式通信库，与此前面向GPU平台开源的组件一一对应。华为向DeepSeek团队提供联合定义的昇腾超节点SuperPoD Flex与UBL128组网方案，可实现128卡3.2Tbps单层交换Scale-up网络；DeepSeek开发高性能DeepEP通信库，互联带宽实测Dispatch 375 GB/s、Combine 347 GB/s接近硬件上限。双方将联合创新成果在CANN社区开源，支持基于昇腾950及超节点集群部署DeepSeek模型。
---

# DeepSeek官方开源昇腾基础组件，与昇腾共建高效易用的AI芯片软件生态

> 原文链接：https://www.qbitai.com/2026/09/499263.html
> 来源：量子位

DeepSeek官方开源昇腾基础组件，与昇腾共建高效易用的AI芯片软件生态
量子位的朋友们
量子位
9月30日，DeepSeek 正式开源面向昇腾算力平台的基础设施组件，涵盖 TileLang 高级语言编译工具、高性能计算库与分布式通信库，与此前面向GPU平台开源的组件一一对应。
Deepseek团队面向华为昇腾平台开源发布基础设施加速库，对中国 AI 软件生态具有里程碑意义，为算力平台提供了新的选择。
本次开源，DeepSeek发布了DeepGEMM、FlashMLA、TileKernel、DeepSelect等高性能昇腾算子库组件和DeepEP分布式通信库。昇腾提供了稳定、开放的Ascend C API接口，使能用户对访存路径及计算流水线进行深度调优，完成高性能算子开发。同时依托开放 Ascend C 编程接口与 PTO ISA 底层指令体系，支持了DeepSeek的TileLang编程开源工作。昇腾生态兼顾不同开发范式，既支持资深开发者进行精细的手工调优，也支持 TileLang 等高级语言的编译对接。
华为向DeepSeek团队提供了联合定义的昇腾超节点SuperPoD Flex 和UBL128组网方案，
可实现128卡3.2Tbps单层交换Scale-up网络和256K卡两层交换Scale-out网络，可以支持超低时延推理和前沿基座模型的大规模训练的需求
。基于全互联的UBL128超节点，昇腾提供了 ASC-COMM 高性能自定义通信编程库，支撑用户通信算子与通算融合算子高性能编程。Deepseek团队开发了高性能 DeepEP 通信库，涵盖EP / CP / PP / FSDP 等模式下的通信算子，为更大模型向更大集群扩展提供支持，互联带宽实测达到 Dispatch
375 GB/s
、Combine
347 GB/s
的通信性能，接近硬件上限。
为支持广泛的开发者基于昇腾 950 及超节点集群部署 DeepSeek模型，华为将此次联合创新的成果在CANN社区开源，包括大EP低延时推理部署、单卡/单机部署、大规模训练、超长文本KVcache池化与 Agentic RL。其中面向大规模推理场景，基于EP32部署策略，offline推理模式下DeepSeek-V4.1-Flash不带框架纯模型性能可实现
TPOT=5ms，每卡输出吞吐2469 tokens/s；TPOT=10ms，每卡输出吞吐5102 tokens/s。
（注：Benchmark数据均基于Offline推理模式采集，不包含Serving调度和框架负载均衡影响。ContextLength = 128K，Dspark 投机接受率 0.85，profiling链接详见附录：DeepSeek-V4.1-Flash超节点部署推理优化实践）
基承其本，算展其用。
华为昇腾平台将与Deepseek等前沿模型团队，持续深耕芯模协同，联合创新。以AI算力底座承载模型能力，深度适配，双向奔赴，打通推理到训练的全链路，携手打造开放、高效、易用的AI软件生态。
附开源参考实践和技术报告链接：
通信编程体系：基于UB memory和URMA通信编程接口的通算并行算子开发实践：
https://gitcode.com/cann/cann-recipes-infer/tree/master/docs/models/deepseek_v4_1/deepseek_v4.1_asc_comm_tech_report.md
基于Agent-Friendly算子编程范式CANNBot-DSL的高性能融合算子开发实践：
https://gitcode.com/cann/cann-recipes-infer/blob/master/docs/models/deepseek_v4_1/deepseek_v4.1_cannbotdsl_operator_guide.md
DeepSeek-V4.1-Flash超节点部署推理优化实践：
https://gitcode.com/cann/cann-recipes-infer/tree/master/docs/models/deepseek_v4_1/deepseek_v4.1_flash_cann_tech_report.md
DeepSeek-V4.1-Flash单机部署低时延推理优化实践：
https://gitcode.com/cann/cann-recipes-infer/tree/master/docs/models/deepseek_v4_1/deepseek_v4.1_low_latency_tp_guide.md
DeepSeek-V4.1-Flash 单卡部署推理优化实践：https://gitcode.com/cann/cann-recipes-infer/blob/master/docs/models/deepseek_v4_1/dsv41-flash-950-single-card.md
基于PyTorch原生框架的DeepSeek-V4.1-Flash模型预训练实践：
https://gitcode.com/cann/cann-recipes-train/blob/master/docs/llm_pretrain/ascend950_superpod_moe_pretrain_system_reference.md
DeepSeek-V4.1-Flash模型低精度量化训练实践：https://gitcode.com/cann/cann-recipes-train/tree/master/docs/llm_pretrain/ascend950/low_precision_training.md
DeepSeek-V4 DSpark草稿模型昇腾训练实践：https://gitcode.com/cann/cann-recipes-train/tree/master/llm_sft/DeepSpec
DeepSeek-V4 单机LoRA 微调实践：https://gitcode.com/cann/torchtitan-npu/blob/master/docs/feature_guides/deepseek_v4_lora.md
基于鲲鹏CPU、昇腾950、灵衢协同的Agentic RL训练实践：https://gitcode.com/cann/cann-recipes-train/tree/master/docs/llm_rl/kunpeng_ascend_agentic_rl_infrastructure.md
鲲鹏CPU对AgentENV的适配与优化实践：
https://gitcode.com/KunpengSDK/agentENV/blob/main/agentenv-kunpeng-optimization-practice.md
推理模型优化Agent 部署调优实践
https://gitcode.com/cann/cann-recipes-infer/blob/master/docs/agent/DeepSeekV4.1-Flash-Model-Agent.md
AMCT 低精度量化Agent量化实践：
https://gitcode.com/cann/amct/tree/master/examples/models/deepseekv4.1/DeepSeekV4.1-Flash-Quantization-Agent.md
TileLang 算子Agent开发和优化实践：
https://gitcode.com/cann/cannbot-skills/tree/master/plugins-official/tilelang-op-orchestrator
本文由华为提供，量子位获授权转载，观点归原作者所有。
版权所有，未经授权不得以任何形式转载及使用，违者必究。
华为
量子位的朋友们
正行创新联合创始人杨宇欣正式亮相：出任总裁，负责全球业务拓展
DeepSeek知乎独家发文，首次公开V4.1 Agent训练“大本营”DSec
成立一年完成5轮融资，诺因智能再获数亿元，累计超10亿元
从真机到世界模型，具身智能正在补一条看不见的数据产线
扫码分享至朋友圈
相关阅读
这就是华为速度：2.69分钟完成BERT训练！新发CANN 5.0加持，还公开了背后技术
打通软硬件的爽，华为最知道！
十三
CANN5.0
华为
昇腾
DeepSeek V4芯模协同背后，国产算力生态开始飞轮加速
国产算力是潮流，先用起来。
henry
CANN
华为
未来智慧城市长啥样？华为云让我们到深圳看一看
未来城市初具雏形。
晓查
云计算
华为
MindCon | 5天啦，你有领取MSG城市专属徽章吗？
智能车参考
Mindcon
MindSpore
华为
华为发布全新一代OceanStor存储Pacific系列 释放海量数据价值
近日华为面向全球发布全新一代海量数据存储OceanStor存储Pacific系列，通过打破架构、服务和性能的边界，以多协议无损互通、下一代弹性EC算法和系列化硬件，灵活应对AI、HPC、视频等海量数据场景的多样化需求及效率、成本和可靠性挑战，帮助企业释放海量数据价值。
晶少
OceanStor
华为
数据价值
Coordination Engineering关键一环，JiuwenClaw再发布Team Skills技能新范式
业界首个面向多Agent协作的标准化能力包规范
邓思邈
JiuwenClaw
openJiuwen社区
Team Skills
华为