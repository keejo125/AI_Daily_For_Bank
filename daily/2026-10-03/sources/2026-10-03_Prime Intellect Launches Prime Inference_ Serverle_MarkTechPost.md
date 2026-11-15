---
publish_time: 1790935200
link: https://www.marktechpost.com/2026/10/02/prime-intellect-launches-prime-inference-serverless-and-reserved-serving-for-frontier-open-models/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Prime Intellect 推出 Prime Inference，一个面向前沿开源模型的推理服务平台，提供 serverless 弹性端点与自有 GPU（多数据中心）预留算力，正式发布前日处理近一万亿 token。它补齐了公司开放训练栈（prime-rl/verifier/sandbox）的“服务层”：部署模型产出的生产轨迹可回灌训练形成闭环。平台兼容 OpenAI API，组合 NVIDIA Dynamo、vLLM、Mooncake、FlashInfer，采用 prefill/decode 分离，p90 词间延迟降低近 40%，并支持数据中心间自动故障转移。
title: Prime Intellect 推出 Prime Inference 开放模型推理服务平台
---

# Prime Intellect 推出 Prime Inference 开放模型推理服务平台

来源：MarkTechPost
原文链接：https://www.marktechpost.com/2026/10/02/prime-intellect-launches-prime-inference-serverless-and-reserved-serving-for-frontier-open-models/

Prime Intellect 推出 Prime Inference，一个面向前沿开源模型的推理服务平台，提供 serverless 端点和在自有 GPU（多数据中心）上的预留算力。正式发布前，它每天在内部处理近一万亿 token，流量来自 RL rollout、合成数据生成、评测和长时 coding agent。

Prime Inference 是 Prime Intellect 开放训练栈的"服务层"：公司已提供 prime-rl、verifier、sandbox 等后训练工具，补齐服务环节后形成闭环——部署的模型产出生产轨迹，可回灌训练。平台兼容 OpenAI API（api.pinference.ai/api/v1），支持 serverless（弹性需求）与 reserved（持续负载）两种模式，数据中心间自动故障转移。硬件当前为 NVIDIA Blackwell，Vera Rubin 在路线图中。

其服务栈组合 NVIDIA Dynamo、vLLM、Mooncake、FlashInfer，采用 prefill/decode 分离：Dynamo 负责路由，vLLM 跑模型，KV 经 NIXL 传输，p90 词间延迟降低近 40%；Dynamo 的 KV 感知路由按前缀重叠与排队权衡，会话保持在同解码器上，Mooncake 增加主机 DRAM 二级 KV。GLM-5.3 在 GB200 NVL72 上以 1:4 prefill/decode 比例、每 prefill 组服务 66 个会话、每用户 101 tok/s；NVFP4 KV 压缩使单解码器缓存容量从 109 万升至 163 万 token。团队还向 Dynamo 贡献结构化标签构建器、并用 xgrammar 屏蔽违规工具调用 token，修复工具调用解析 bug，提升 agent 工具调用可靠性。
