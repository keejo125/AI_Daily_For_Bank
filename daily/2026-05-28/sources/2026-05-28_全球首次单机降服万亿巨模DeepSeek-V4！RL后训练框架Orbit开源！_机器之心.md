---
publish_time: 1779938207
---

# 全球首次单机降服万亿巨模DeepSeek-V4！RL后训练框架Orbit开源！

> 原文链接：https://mp.weixin.qq.com/s/M3Q4AnhMa2ymj1JHO1W5ag
> 公众号：机器之心

从数学、代码、复杂推理，到多轮工具调用，大模型的很多能力的提升都离不开 RL 后训练。但当模型规模进入 MoE 万亿参数级别之后，RL 不再只是一个算法问题，同时更加是一个系统问题。

训练侧需要容纳庞大的模型权重、梯度和优化器状态；rollout 侧需要持续生成样本，并保持足够高的吞吐；reference policy 又会进一步放大显存和调度压力。同时，很多 RL 系统在训练时使用较高精度模型，而真正 rollout 或部署时使用低精度 serving 模型。这些精度差异，最终会体现在部署效果与 RL 效果的不一致上。

通过将 base model 固定在部署时使用的低精度表示，并只更新 adapter，Orbit 将 Kimi-K2.6、DeepSeek V4 级别的 1T 模型 RL 后训练压缩到单台 8×B200 上完成。同时，训练和 rollout 使用同一条低精度 base + adapter 路径，从系统层面消除了训练模型与 rollout / 部署模型之间的精度不一致。

Orbit 做到

「让万亿模型进入单节点 RL 区间」

这件事的意义在于：

避免了「训练精度」和「部署精度」不一致带来的偏差，从而带来更稳定更高效的 RL 后训练；

单节点 RL 可以显著降低多节点训练时的通信时延与故障率；

在同样的 HBM 预算下，模型会获得更宽的训练空间，过去需要多卡才能训的模型，有机会被压缩到单卡。

官方博客：https://spherelab.ai/orbit/

Github：https://github.com/Sphere-AI-Lab/orbit

Orbit：支持万亿参数模型 RL 微调的高效框架

显存控制：

如下图 1 所示的估算中，单节点 8×B200 的 HBM 预算约为 1536GB。对 1T 级模型而言，传统全参微调的 weight + grad 显存下界会远超单机预算；而 Orbit  路径由于冻结低精度 base，只训练 adapter，可以把 1T 级模型的 RL 后训练放进单节点预算内。

图 1 不同框架下大参数模型的单节点显存需求估算

训推精度对齐：

在很多 RL 系统里，训练侧可能使用 BF16 或 FP8 等高精度 ，而推理侧使用 INT4、FP4 等低精度。对于监督微调来说，这种差异有时可以被视作推理优化的一部分；但在 RL 中，policy log-prob 本身就是训练信号的一部分，训练侧和推理侧之间的误差 log-prob diff 会直接影响稳定性。

Orbit 将这一问题

前置到了系统设计中：

训练和推理使用相同的低精度 base ，并在其上加载同一个 BF16 adapter，从而保持训推精度一致。

Adapter-first 的系统设计：

Orbit 围绕 adapter 对 RL 训练、推理、同步、reference policy 和低精度 MoE 做了一套整体设计。base 始终冻结，每次训练更新后，只需要将 MB 级 adapter （不需将 GB 级的 base）从训练引擎推送到推理引擎。

这不仅减少了权重同步的体积，也避免了频繁重建推理引擎的开销。

单节点 Kimi-K2.6 结果

在这组实验中，模型运行在单台 8×B200 上，训练精度为 INT4 base + BF16 adapter，rollout 精度使用相同的 INT4 base + BF16 adapter。也就是说，训练和 rollout 走的是同一条低精度 base + adapter 路径。

在约 200 step 的 RL 过程中，Orbit 观察到了几个同时成立的信号：

reward 上升；

eval accuracy 上升；

pass@k 上升；

train-rollout log-prob diff 保持稳定。

图 2 Kimi-2.6 在 Orbit 下单机 RL 后训练信号

图 3 Kimi-2.6 在 Orbit 下单机 RL 后训练的显存记录

图 2 显示，Kimi-K2.6 的 rollout raw reward、eval accuracy 和 pass@k 曲线随训练推进而稳定上升。同时，train-rollout log-prob diff 稳定维持在一个区间。

对于一个对 log-prob 差异非常敏感的训练范式来说，这些信号实际地证明了 Orbit 的 RL 后训练闭环不仅在单机上把 1T 的模型上稳定能跑，同时跑对了且在测试任务上有效果。

单节点 DeepSeek V4 Flash 结果

在这组实验中，DeepSeek V4 Flash 同样运行在单台 8×B200 上。训练精度为 FP4 base + BF16 adapter，rollout 精度也使用相同的 FP4 base + BF16 adapter。

图 4 DeepSeek V4 Flash 在 Orbit 下单机 RL 后训练信号

图 5 DeepSeek V4 Flash 在 Orbit 下单机 RL 后训练的显存记录

从结果看，DeepSeek V4 Flash 在 100 step 以上的 RL 过程中同样保持稳定：reward、eval、pass@k 整体上升，train-rollout log-prob diff 保持在稳定区间。这些趋势跟在 Kimi-K2.6 上的实验结果类似。

单节点 1.6T DeepSeek V4 Pro 初步验证

除了 Kimi-K2.6 和 DeepSeek V4 Flash 两组稳定有效的训练结果，Orbit 还在 DeepSeek V4 Pro 1.6T 上完成初步验证。

由于 DeepSeek V4 Pro base model 本身很强，实验中用的 RL 训练数据不能让它涨点，因此该实验更多是证明 Orbit 的系统路径可以扩展到更大的 1.6T 级 MoE 模型。

图 6 DeepSeek V4 Pro 在 Orbit 下单机 RL 后训练信号和显存记录

在 1.6T DeepSeek V4 Pro 上，Orbit 完成了单节点 8×B200 的实验，展示了稳定的 train-rollout log-prob diff 和可控稳定的 GPU 显存。

这组结果证明

Orbit 的系统上限可在单节点 8×B200 达到 1.6T 级别，展示了其设计有机会覆盖更大的 MoE 模型区间。

从单节点万亿模型，到单卡更大模型

单节点跑通万亿模型 RL 反过来也说明了同样的硬件预算就可以覆盖更大的模型区间。

对万亿模型来说，这意味着

原本可能需要多机协同的 RL 后训练，可以被压缩到单节点完成。

对中小模型来说在 Orbit 的 adapter-first 框架下，单卡也有机会 RL 微调过去需要多卡才能支持的模型，或者在相同模型规模下支持更长 response、更大 batch、更高 rollout throughput 和更频繁的更新。

因此，Orbit 的价值

并不只在于「让大模型变得可训练」，也在于让小模型的 RL 后训练变得更容易。

技术细节

Active-expert-chunked dequantization:

对于 MoE 模型来说，每个词元只会激活部分 experts。Orbit 动态地将 router 选中的 experts 分组成固定大小的 batch，临时反量化后执行 grouped GEMM，并在计算结束后释放高精度权重。这样既能利用 grouped matrix multiplication 的吞吐，又能将临时显存峰值限制在较小 chunk 内，避免大规模低精度 MoE 训练中的 OOM。

Adapter-native async with double-buffered rollout:

系统会为 adapter 维护版本号，并将新版本 adapter 流式写入 inactive slot；当前 active slot 继续服务 in-flight 请求，待新版本准备好后再原子切换。这样可以减少 rollout bubble。在 Qwen3-4B + OFT、8×B200、TP=2 设置下，该设计带来了 1.42 倍的单步时间优化和 44% 更高的 rollout throughput，同时 eval accuracy 保持不变。

DeepSeek V4 相关优化：

Orbit 支持 Full-CUDA graph decoding、DeepGEMM、DeepEP V2，并使用 tilelang / Triton / CUDA 实现高效 attention backward 和 fusion kernels。根据 adapter 训练的特点，Orbit 还设计了 bypass-base-weight-grad 的高效 GEMM backward 算子，避免为冻结 base 计算不必要的梯度。

结语

过去，大模型 RL 后训练往往意味着更复杂的多机系统：更多节点、更重的权重同步和更复杂的系统协同。

Orbit 提供了另一条路径：

冻结低精度 base，只训 adapter，让训练、rollout 和部署对齐，并把整模同步换成 adapter 同步。这让万亿模型可以进入单节点训练区间，更小模型也能在单卡或更有限的硬件上跑得更远。

从 Kimi-K2.6 到 DeepSeek V4 Flash，再到 DeepSeek V4 Pro 1.6T，Orbit 展示和提供了一套面向大模型后训练的高效框架。

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com