---
publish_time: 1792486494
link: https://mp.weixin.qq.com/s/5MEu2eeqNfBWXlkCKTd6sg
source: DeepSeek
status: confirmed
category: 国内
is_model_related: false
digest: |
  DeepSeek 宣布将内部推理框架 DeepInfer 全面开源，并配套开源生产级 Token 编解码组件 deepseek-recipe。文章指出，推理框架是"让模型为人所用"的中间层，直接决定大规模 AI 服务的算力成本与能耗；DeepSeek 希望分享内部部署经验，帮助开发者与企业优化大规模推理的吞吐与延迟，降低算力成本与能源消耗，让智能以更低价格触达更广人群。
title: DeepSeek 开源推理框架：走向真正普惠的未来
---

# DeepSeek 开源推理框架：走向真正普惠的未来

来源：DeepSeek
原文链接：https://mp.weixin.qq.com/s/5MEu2eeqNfBWXlkCKTd6sg

大模型的能力边界由模型本身划定，但如何以合理成本提供超大规模的模型服务，还取决于一个长期未被公众了解的中间层：
推理框架
。
训练使模型学有所成，推理则让模型为人所用。面对如今海量的用户调用，推理框架负责统筹调度庞大的算力集群，其效率直接决定了 AI 服务的算力成本与电力消耗。
DeepSeek 长期致力于将推理性能推向极致。在此前开源一系列大模型、TileLang 编译工具及推理算子库的基础上，我们决定进一步
将内部推理框架 DeepInfer 全面开源
。
「为善与众行之，为巧与众能之。」
我们希望通过分享内部的部署经验，帮助开发者与企业组织优化大规模推理的吞吐与延迟，从而高效构建私有化及公有云部署，降低算力成本、减少能源消耗，让智能以更低的价格触达更广泛的人群，实现真正的大模型普惠。我们也将继续支持社区进行大规模部署优化，欢迎加入我们的开源行列。
DeepInfer
基于
DeepInfer
，我们已实现 DeepSeek V4.1 Flash 高吞吐、低延迟的大规模推理服务。未来，DeepSeek 新模型的推理代码及后续优化也将在此持续更新。
DeepInfer 推理框架
：集成高性能算子与深度优化的推理引擎，支持分布式推理、推测解码、SWA Bounded Replay、结构化输出等能力，兼容英伟达与华为昇腾平台。
deepseek-recipe 编解码组件
：同步开源的生产级 Token 编解码组件，与 DeepSeek 官方 API 处理逻辑完整对齐，确保社区获得与官方部署一致的 API 体验。
开源仓库
DeepInfer
:
https://github.com/deepseek-ai/DeepInfer
deepseek-recipe
:
https://github.com/
deepseek-ai/deepseek-recipe
复制链接进入浏览器打开或点击“阅读原文”查看 DeepSeek 知乎技术报告：
https://zhuanlan.zhihu.com/p/2095560295930508953
未来展望
借助全面开源的模型、算子库与推理框架，我们期待着在不远的未来，能够看到全球 AI 服务的范围与质量获得前所未有的扩展与提升，变得更加公平、透明、可信赖，进而实现在全社会范围内加快技术迭代、减少能源浪费，让有限的资源以更高的效率在基础设施与用户终端之间流转，以每个人都能够负担的成本传递更加强大的智能，以及伴随着智能的善意和无限可能性。
DeepSeek 将与各位一同携手，为实现这样的未来图景而不懈努力。
