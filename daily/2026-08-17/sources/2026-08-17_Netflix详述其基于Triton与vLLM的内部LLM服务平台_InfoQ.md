---
publish_time: 1786931784
link: https://www.infoq.cn/article/J9Zi9LELcpxFRe23PHdY
source: InfoQ
status: confirmed
category: 国际
is_model_related: false
digest: |
  Netflix 公开其将 LLM 推理纳入内部服务平台的生产经验，讨论如何支撑不同模型规模、硬件与快速演进的推理引擎。平台基于现有 JVM 服务层构建（负责路由、特征获取、后处理与日志），小模型在 CPU 进程内运行，大模型请求委托给 MSS，由 Triton 负责模型加载、批处理与 GPU 调度，vLLM 执行推理并提供扩展点。Netflix 强调需固定兼容的 Triton 与 vLLM 版本以防加载失败，并以 Red-Black/Versioned 策略做部署隔离。文章还详解受约束解码的状态同步难题——vLLM 暂停 GPU 资源后恢复请求时，需重建解码状态以强制输出合法 JSON。通用服务接口并未消除底层差异，打包、兼容性、约束解码与部署隔离仍需逐层工程实现。
---
# Netflix 详述其基于 Triton 与 vLLM 的内部 LLM 服务平台

> 原文链接：https://www.infoq.cn/article/J9Zi9LELcpxFRe23PHdY
> 来源：InfoQ

## 核心要点

- 平台基于 Netflix 现有 JVM 服务层构建，负责路由、特征获取、候选生成、后处理与日志；小模型在 CPU 进程内运行，大模型请求委托给 MSS（由 Triton 负责模型加载、批处理、GPU 调度与多框架服务）。
- GPU 路径选择 vLLM 满足运营适配性与扩展性，同时保留 Triton 的模型管理与调度职责；二者版本需固定兼容，否则部署无法加载。
- 对比 Triton 的 Python backend 与 vLLM backend：vLLM-backend 使模型与前端更独立演进，影响耦合强度而非执行引擎。
- 受约束解码（强制合法 JSON）需在全请求过程维护状态；vLLM 为管理 GPU 资源暂停后恢复时，状态可能与 token 历史不同步，Netflix 增加检测变化并重建状态的逻辑。
- 部署采用 Red-Black 与 Versioned 策略隔离模型级变更。Uber 的 GenAI 网关思路类似（兼容 OpenAI 接口 + 集中认证/缓存/可观测），但实现不同；通用服务接口并未消除底层引擎差异。
