---
publish_time: 1786801951
status: confirmed
category: 国际
is_model_related: false
digest: |
  Cloudflare发布开源运行时Cloudflare Computer，为AI智能体提供接近真实“计算机”的持久化运行环境，而非临时容器。其@cloudflare/computer包由平台决定代码在isolate、容器沙箱或浏览器中运行，目标仅不到10%工作需容器，编码、音视频处理、文档创建均可由isolate完成，以支撑数亿至数十亿并发智能体。
  架构核心是基于SQLite的共享文件系统，isolate与容器均可访问、任务可无缝转移；提供容器项目、isolate shell、isolate JavaScript三种后端，并能持久保存智能体状态、不运行时休眠。目前处早期预览，仅适合实验与原型。
link: https://www.infoq.cn/article/RaKIH7E4lA9uQ4Iasltb
source: InfoQ
title: 
---

# Cloudflare Computer 发布：让 AI 智能体拥有持久化运行环境

> 原文链接：https://www.infoq.cn/article/RaKIH7E4lA9uQ4Iasltb
> 来源：InfoQ

Cloudflare 推出了 Cloudflare Computer"。这是一个新的开源运行时，旨在为 AI 智能体提供更接近真实“计算机”的环境，而不只是临时容器。据该公司称，它利用 Cloudflare isolates 实现快速的无服务器执行，使智能体成本更低、速度更快，也更容易扩展。

Cloudflare Computer 试图解决 AI 智能体部署面临的一项重大挑战。该公司认为，依赖容器运行智能体无法扩展到“数亿乃至数十亿个并发智能体”，因为全球根本没有足够的计算能力。

为解决这一问题，@cloudflare/computer" 软件包引入了一种智能体运行时，由平台决定代码是在 isolate、容器沙箱还是 Web 浏览器中运行。在这种模式下，“每个智能体都会获得一台计算机，而运行时会针对效率和可扩展性进行优化”。

我们对 @cloudflare/computer 的目标是，为智能体提供这样一种运行时：只有不到 10% 的工作需要容器，编码任务、音视频处理和文档创建都可以由 isolates 完成。

Cloudflare 表示，随 Cloudflare Workers" 一同推出的 isolates 可以“无限横向扩展”，并且能够极快地启动和关闭。此外，它们可以持久保存智能体状态，在智能体不运行时进入休眠状态，并在需要时启动自己的容器沙箱。Cloudflare 认为，isolate 与容器沙箱的这种组合非常有效，因为它兼顾了横向和纵向扩展能力：

Cloudflare 的架构被设计为在 isolate（一个 Durable Object）中运行智能体运行框架，并将按需连接的容器作为工具调用。这使你能够只在必要时使用更重量级的计算原语，从而优化性能和成本。

该架构的一个核心组成部分是基于 SQLite 的共享文件系统，isolate 和容器都可以访问它。这样，任务便能在两者之间无缝转移，共享文件系统则允许它们处理相同的文件。Cloudflare Computer 文件系统可以与 Git 仓库、存储桶或任意文件配合使用，同时确保所有操作都受到管控、经过审计并处于可观测状态。

目前，Cloudflare Computer 提供三种后端：容器项目，将 SQLite 状态以真正挂载到 FUSE 文件系统的形式暴露给沙箱容器；isolate shell，在 Dynamic Worker 中运行 just-bash 环境；以及 isolate JavaScript，在一个全新的 Dynamic Worker 中运行 ECMAScript 模块。

Cloudflare 表示，Cloudflare Computer 仍处于早期预览阶段，只适合用于实验、探索和原型开发。

原文链接：
https://www.infoq.com/news/2026/08/cloudflare-computer-agents/"