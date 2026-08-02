---
publish_time: 2026-08-02
source: InfoQ
title: "MCP迎来最大更新：砍掉握手和会话，重回上古HTTP时代"
link: https://mp.weixin.qq.com/s/2oofgGKGIDDGhq68CquiKQ
category: 国际
is_model_related: false
status: confirmed
digest: |
  MCP（Model Context Protocol）发布自诞生以来最大更新：移除会话与初始化握手，彻底实现无状态化。每个请求独立携带完整上下文，远程MCP服务器可像传统HTTP服务一样用轮询调度，无需会话亲和性。核心变化包括：协议版本和客户端能力通过_meta每次传递；新增server/discover方法支持按需能力查询；TTL缓存机制提升提示词缓存命中率。代价是：基于实验性Tasks API构建的系统需迁移，采样和日志机制被弃用。维护者设置了十周验证期和12个月弃用过渡期，新旧协议将共存。开发者评价两极：有人认为解决了长期痛点，也有人批评"把好不容易从SSE迈向WebSocket的协议又拽回了上古世界观"。
---
# MCP迎来最大更新：砍掉握手和会话，重回上古HTTP时代

来源：InfoQ

原文链接：https://mp.weixin.qq.com/s/2oofgGKGIDDGhq68CquiKQ

