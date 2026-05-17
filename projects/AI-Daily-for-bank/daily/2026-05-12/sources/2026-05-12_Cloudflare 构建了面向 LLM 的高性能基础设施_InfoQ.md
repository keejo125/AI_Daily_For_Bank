---
publish_time: 1778571070
---

# Cloudflare 构建了面向 LLM 的高性能基础设施

> 原文链接：https://mp.weixin.qq.com/s/fF1GtsLxbly_5PKlRHpckA
> 公众号：InfoQ

作者 ｜ Renato Losio

译者 ｜ 张卫滨

Cloudflare 最近发布了全新的 基础设施，可以在其全球边缘网络上运行大型的 AI 大语言模型。由于这类模型依赖昂贵的硬件，并且需要处理海量的输入和输出文本数据，Cloudflare 将模型输入处理与输出生成拆分到不同的专用优化系统中，并自研推理引擎实现 GPU 资源的更高效调度。

Cloudflare 团队表示，其中的一个核心优化是把模型推理拆分为两个阶段，由不同服务器分别进行处理，一个阶段负责读取并预处理输入文本，另一阶段专注生成输出内容。Cloudflare 首席产品经理 Michelle Chen、高级工程经理 Kevin Flansburg 和首席系统工程师 Vlad Krasnov 撰文指出：

我们用来提升性能与资源效率的硬件架构叫做解耦预填充（disaggregated prefill）。LLM 请求处理分为两个阶段，预填充阶段处理输入 Token 并填充 KV 缓存，解码阶段逐一生成输出 Token。预填充通常属于计算密集型负载，而解码则是内存密集型负载。

Cloudflare 还自研了名为 Infire 的 AI 推理引擎。该引擎在 2025 年 Cloudflare 周年庆活动期间正式发布，它可以跨多 GPU 更高效地运行大语言模型，降低内存占用、缩短模型启动时间，最终实现更低的响应延迟。

像 Kimi K2.5 这类大语言模型体量极其庞大（参数规模超万亿、模型大小约 560GB），必须拆分部署到多块 GPU 上，仅加载模型到内存就至少需要 8 块 H100 显卡，这还未计入推理过程额外占用的内存开销。当谈及 Infire 引擎与硬件优化为何能高效支撑超大规模的模型、并为用户提供更快的响应时，Chen、Flansburg 和 Krasnov 补充说：

在流水线并行方面，Infire 会对流水线所有阶段做合理的负载均衡，避免某一阶段 GPU 空闲等待而其他阶段满载执行的资源饥饿问题。在张量（tensor）并行方面，Infire 以减少 GPU 间通信开销为优化目标，尽可能提升通信效率。对绝大多数模型而言，流水线并行与张量并行结合使用，就能在吞吐量和延迟之间取得最优平衡。

Cloudflare 此前曾发文介绍如何在自己的 AI 推理平台部署开源模型，率先在 Workers AI 上线了 Moonshot AI 的 Kimi K2.5 模型，并透露团队正在采用多样化的硬件配置，适配各类大模型的最优运行需求。

图片来源：Cloudflare 的博客文章

Cloudflare 表示，团队进一步对 Infire 做了内存优化，缩减内部流程的 GPU 内存开销，如今仅需 2 块 H200 GPU 即可运行 Llama 4 Scout，并且仍留有充足容量支撑上下文 Token，8 块 H100GPU 便可运行 Kimi K2.5，同时预留出足够内存用于 KV 缓存。

Cloudflare 近期还推出了 Unweight 模型压缩系统，官方称可在无损精度的前提下，将大语言模型权重压缩了 15%–22%，减少推理时 GPU 加载与传输的数据量，让模型运行更快、资源效率更高。

并不是只有 Cloudflare 在关注大模型生产落地方面的基础设施挑战。Cockroach Labs 最新“AI 基础设施现状”报告 指出，随着企业将 AI 系统投入日常业务，大量企业发现现有基础设施无法承载 AI 负载所需的规模与可靠性要求：

传统基础设施围绕间歇性的人机交互而设计，无法承受 AI 这种高压力的负载。想要适配 AI 业务的高并发与不可预测性，企业不能只做性能升级，更需要从系统架构层面进行根本性的重构。

Cloudflare 还分享了他们在 提示词缓存（prompt caching）层面的效率优化方案。

原文链接：

Cloudflare Builds High-Performance Infrastructure for Running LLMs(https://www.infoq.com/news/2026/05/cloudflare-llm-infrastructure/)

声明：本文由 InfoQ 翻译，未经许可禁止转载。

点击底部

阅读原文

访问 InfoQ 官网，获取更多精彩内容！

今日好文推荐

Anthropic 的 Harness 没管住 Claude Code？不遵守 CLAUDE.md、烧光 credits，开发者怒喊退钱

Chrome 开了一个危险的头：偷偷给数亿电脑塞 4GB Gemini 模型，占硬盘、耗算力、删了自动重下

智能体=新型攻击入口？模型上线前，OpenAI内部到底审什么？董事会成员首次详解

Manus交易失败了，但创始人依然在谈成功学