---
publish_time: 1787450400
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/chjUVB0-uXGBvQF4K5VMmA
source: 阿里云云原生
title: GPU 利用率低却难定位根因？试试这款零侵入 AI Profiling 工具
---

# GPU 利用率低却难定位根因？试试这款零侵入 AI Profiling 工具

来源：阿里云云原生
原文链接：https://mp.weixin.qq.com/s/chjUVB0-uXGBvQF4K5VMmA

说明：
本文中 SysOM 为阿里云操作系统控制台运维组件。AI Profiling 作为 SysOM 中智算运维功能之一，主要聚焦 AI 作业的性能分析场景。该能力也是
SysOM 与阿里云可观测
在智算/AI Infra 方向上的协同探索，结合
阿里云可观测在指标、链路、日志、告警等方向的基础能力，
以及 SysOM AI Profiling 在 AI 作业级深度诊断上的能力，共同帮助用户定位 GPU 利用率低、显存异常、通信长尾等问题。
你是否遇到过这些困扰：训练任务跑了几小时才发现 GPU 利用率不到 30%，推理服务上线后显存莫名增长直到 OOM，千卡集群中某几张卡的通信延迟拖慢整体训练速度，却无从下手定位？
SysOM AI Profiling
（下文简称为 AI Profiling
）
就是为解决这些问题而生的。它是一款专为 AI 应用设计的全生命周期性能观测与诊断工具——从训练到推理，从单卡到千卡集群，从 Python 层到 GPU Kernel 层，帮你看清每一微秒发生了什么。
现有工具为什么不够用
Cloud Native
在 AI Profiling 出现之前，大规模集群下的性能观测主要依赖业界已有的多类工具：有的能在 GPU 层面细粒度抓取 CUDA Stream、Kernel 及相关算子的执行情况，并以 Trace 格式输出；有的面向 Kubernetes Pod 与 GPU 维度做监控数据上报；有的借助 eBPF 从内核层面采集 CPU、内存、系统调用等追踪数据；也有的能较丰富地抓取框架层（如 Torch）与 Kernel 层的数据。这些工具各有所长，但在应对复杂 AI 作业时普遍存在一些共性局限——侵入性偏强、更适合短时间离线分析、难以做迭代级采集、与运行环境或框架版本强关联，且多数只覆盖单一维度、难以跨厂商兼容，最终导致维度信息不全、数据难以联动、诊断效率不高。
因此，新一代智能分析工具需要具备
零侵入、全生命周期覆盖、跨厂商兼容
的特点，以便更有效地优化资源利用和提升系统稳定性。这正是 AI Profiling 要解决的问题。
AI Profiling 核心功能
Cloud Native
▍
一
键 Profiling，分钟级拿到分析结果
只需在输入实例 ID、GPU进程，AI Profiling 就会自动完成采集、回传、分析全流程。不用改一行代码，不用重启进程，不用手动拷贝 trace 文件到 Chrome Tracing——系统自带 TimeLine 视图，结果直接在前端呈现。
▍
多维度深入观测
AI Profiling 支持同时采集 Python 调用栈、CPU、GPU 算子、Torch 层调用、显存、FLOPS、RDMA 通信、TCP 网络等多维度数据，既能查看宏观的整体耗时分布，也能下钻到 GPU Kernel 级别的细粒度信息。
具体来说，你能看到多进程聚合与单进程两种视图：
多进程聚合视图：
基础概览
—— 本次采集的进程列表、使用的卡编号、显存占用、卡显存总量以及单进程报告视角入口。
核函数热力图
—— 本次采集的所有涉及的 GPU 核函数在 GPU 上调用的热力图。
多进程 GPU Kernel 具体分析 timeline
—— 本次采集的所有进程的 GPU 核函数聚合在一张 timeline 图上，能观察多进程之间 GPU 的执行情况。
单进程视图：
整体性能概览
——设备与显存概况、GPU 利用率、各阶段时间占比等关键指标一览。
图 / “CPU/GPU Summary”面板
GPU 算子分析
—— 展示 GPU 运算/通信/显存/空闲等时间占比，帮助快速判断作业的算力利用情况。
GPU 核函数详细信息统计
—— 按核函数维度统计调用次数、耗时分布与资源占用等指标，便于定位热点核函数。
图 / “GPU Kernel 分析”面板
图 / “Top内核函数”面板
迭代时间与损失精度统计
——按迭代维度统计各阶段耗时占比与损失精度，训练与推理作业均可自动切分迭代，并支持自定义迭代入口。
图 / “迭代统计与差分分析”面板
TimeLine 原始数据展示
—— 无需再打开 Perfetto/Chrome Tracing。
图/多源异构数据融合 TimeLine 示意图
▍
显存快照分析
活跃显存分配释放时序图（Active Memory Timeline）
从微观角度展示采样时间段内所有显存块（block）的大小、分配/释放与生命周期，直观呈现显存随时间的变化趋势。
当锁定某个迭代或某个可疑的 block 时，可进一步查看其调用堆栈，辅助定位显存异常的来源。
图 / “显存时序图”面板
▍
基于迭代锚点的差异分析
在大规模 AI 训练/推理场景中，AI Profiling 采集的 Timeline 数据通常具有极高的复杂度与体量
（通常可达数 GB）
，使得性能分析和异常定位极具挑战。尤其在进行性能对比或异常根因分析时，传统方法难以高效识别关键差异。
AI Profiling 通过在训练/推理流程中嵌入迭代标记，将整个执行过程精准划分为若干独立的迭代单元，并对每个迭代分别统计其损失值、计算耗时、存储开销及通信延迟等关键指标。进一步地，将这些指标以柱状图等形式进行可视化呈现，使用户能够“一眼识别
”
离群迭代——例如梯度爆炸导致的损失突变，或某次迭代中通信占比显著偏高等离群行为。
图 / 基于迭代统计示意图
你能从中获得什么
Cloud Native
零侵入，对业务无感
—— 采用无侵入式 Profiling 技术，无需用户对容器做任何变更、重启。
跨厂商兼容
—— 支持 Nvidia、PPU、AMD 等设备类型，不必为不同硬件平台切换观测工具。
极低开销
—— 业界现有 Profiling工具在采集后，作业性能通常难以恢复到采集前水平；AI Profiling 在
采
集结束后能让业务性能快速恢复到采集前状态，对生产作业的持续影响可控。
丰富性
—— 支持按需采集 Python 调用栈、CPU 信息、GPU 算子、Torch、显存、FLOPS、RDMA、TCP 等指标。GPU/CPU 监控指标也支持按需采集。
全流程自动化
—— 全流程分钟级自动完成。只需要在前端配置实例 ID，就能够自动触发 AI Profiling，采集完成会自动回传中心端，分析完成会生成报告在前端显示；自带 TimeLine 视图，无需重新拷贝到 Chrome Tracing/Perfetto 等组件。
多进程聚合分析
—— 支持多进程采集，并支持多进程 GPU Kernel 合并观测分析。
多维度采集
—— 支持按时间采集与按迭代采集两种采集维度。同时支持自定义迭代入口与跳过前 n 迭代等高级配置。
对比业内工具优势
—— 除了 GPU Kernel 和 Torch 层数据，还覆盖 RDMA 通信、系统调用、DCGM 监控和 NVTX 标记；同时支持 Python 与 C++ 应用进程的数据采集，并可对非 GPU 相关进程进行统一监控。
真实案例
Cloud Native
▍
案例一：vLLM 推理服务显存泄漏定位
问题背景：
用户使用 vLLM 部署大模型推理服务时，在预设占用显存的情况下，运行过程中出现了显存 OOM（Out of Memory）错误，并观测到显存有明显增长。
图 / 通过 dcgm-exporter 监控观察到有显存增长
图 / 观测 vLLM 日志发现 KV-Cache 利用率并未打满
使用 AI Profiling 显存分配追踪
1. 进入阿里云操作系统控制台
-
-
>GPU 性能与诊断-
-
>AI Profiling。
2. 输入目标实例 ID， 对正在运行的 vLLM 推理服务进行 AI Profiling，配置 Profiling 采集项与分析模式点击开始分析。
3. 系统自动完成采集、数据回传和中心端分析，全程无需人工干预，采集完成后，在前端查看自动生成的分析报告。
通过 AI Profiling 报告中的 GPU Kernel Timeline，可以观察到显存增长的峰值出现在显存申请（cudaMalloc）操作中；在 Timeline 上定位到对应时间点后，进一步下钻到 Python 调用栈，最终定位到推理请求处理过程中框架的上下文管理逻辑动态预留了额外显存。尽管 vLLM 在服务启动时已预分配显存，但推理过程中的这部分动态预留仍使整体占用超出预期阈值，最终触发 OOM。
图 / 显存峰值增长定位
图 / 在 TimeLine 上标注所定位的 cudaMalloc 的时间部分
图 / 通过 Python 调用栈逐层下钻，定位到触发额外显存申请的具体方法
结合 PyTorch 显存缓存机制分析， PyTorch 的显存管理采用分块
（block）
机制，会缓存已释放的内存块以减少频繁的 CUDA 内存分配开销。然而，这些缓存块的大小和数量会随模型推理复杂度动态变化。当显存使用率接近阈值时，缓存块的累积可能导致显存占用超出预期。例如，
nvidia-smi
显示的显存占用包含
reserved_memory
（缓存块）
和
allocated_memory
（实际使用）
，两者之和可能远超初始预留值。
解决方案与优化建议：
1. 避免显存碎片化：
当出现显存剩余量足够却无法分配连续的显存时，可以通过环境变量
CUDA_PYTORCH_CUDA_ALLOC_CONF
将
max_split_size_mb
调小，来减少显存碎片化的影响；
2. 尝试其他优化策略：
除了调整
max_split_size_mb
外，还可以考虑其他优化策略来减少显存碎片化，如使用显存清理工具（如
torch.cuda.empty_cache()
）或调整模型和数据加载策略。
▍
案例二：客户使用 AI Profiling 对比 SGLang 与 vLLM 性能差异
同样如案例一的方式，进入阿里云操作系统控制台->GPU性能与诊断->AI Profiling，发起 AI Profiling 分析，得到分析报告。
SGLang 推理：
根据 GPU/CPU Tracing 分析的 Timeline 图，可以发现其显著特征是：
1.
图像编码未做 batch 处理，多个请求会看到多次独立的图像编码，单次编码耗时相对较高；
2.
文本解码有 batch，在观测的参数配置下 batch 大小对单次 Decode 执行时间影响不大；
3.
GPU 空闲主要由每个阶段开始时 GPU 算子下发不充分造成，并观察到部分毫秒级 GPU 空隙，疑与操作系统活动相关；
4.
文本 decode 阶段的 GPU 空隙主要来自 Cuda Graph 处理的开销。
图/SGLang Python 函数调用栈分析
vLLM pipeline：
根据 GPU/CPU Tracing 分析的 Timeline 图，可以发现 vLLM pipeline 的特征如下：
图像编码：单次耗时略高于 SGLang 单请求的图像编码；
文本解码：单次耗时与 SGLang 基本相当，略高一些。
图 / vLLM Python 函数调用栈分析
AI Profiling 入口链接（复制链接至浏览器打开）：
https://alinux.console.aliyun.com/sysom-ai/ai-infra-observation
写在最后
Cloud Native
从训练到推理、从单卡到千卡集群、从 Python 层到 GPU Kernel 层，AI Profiling 以零侵入、低开销、跨厂商兼容的方式，把过去难以看清的性能问题一一呈现出来——一键采集、分钟级出结果，多维度深入观测，配合显存快照与基于迭代锚点的差分分析，让 GPU 利用率不高、显存异常增长、集群通信长尾等问题都变得有迹可循，并已在真实的 vLLM 显存泄漏定位、SGLang 与 vLLM 性能对比等场景中得到验证。
▍
Profiling Agent：从“看见问题”到“理解问题”
在 AI Profiling 提供全生命周期采集与观测能力的基础上，我们进一步构建了 Profiling Agent
（也称性能剖析 Agent）
，目标是打造源码级的问题分析与解决能力，实现“感知 → 诊断 → 分析 → 修复建议
”
的闭环。
前文展现的是 AI Profiling 在采集与观测层面“看得清、看得全”的能力；而 Profiling Agent 要解决的，是让机器自动读懂这些数据、定位根因并给出修复建议，把观测延伸为端到端的智能闭环。目前，Profiling Agent 已发布，后续会专门介绍以及讲解如何使用，欢迎关注。
