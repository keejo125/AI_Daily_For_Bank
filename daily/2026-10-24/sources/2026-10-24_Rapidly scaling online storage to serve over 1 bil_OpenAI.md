---
publish_time: 1792774800
link: https://openai.com/index/scaling-storage-one-billion-users-part-two
source: OpenAI
status: confirmed
category: 国际
is_model_related: false
digest: |
  OpenAI 工程博客介绍其如何扩展 Habitat 存储系统，以可靠的多租户、全局缓存与 Azure Cosmos DB 为 ChatGPT 提供支撑，使读取速度提升 12 倍、服务超 10 亿用户。文章聚焦大规模消费级 AI 产品的存储架构：通过多租户隔离与跨区域全局缓存降低延迟、用 Cosmos DB 承载元数据与状态，在海量并发下保持读路径稳定。对 AI 研发组织而言，该实践揭示了“模型能力”之外、支撑十亿级 AI 应用的工程底座同样关键——推理服务、会话状态与缓存治理正成为大模型落地的隐形瓶颈。
---

# OpenAI 扩展 Habitat 存储：多租户+全局缓存为 ChatGPT 提速 12 倍

> 原文链接：https://openai.com/index/scaling-storage-one-billion-users-part-two
> 来源：OpenAI

Learn how OpenAI scaled Habitat with reliable multi-tenancy, global caching, and Azure Cosmos DB to deliver 12× faster reads for ChatGPT.