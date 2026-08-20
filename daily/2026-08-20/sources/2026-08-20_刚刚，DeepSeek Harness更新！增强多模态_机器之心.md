---
publish_time: 1787179094
status: pending
category:
is_model_related: false
link: https://mp.weixin.qq.com/s/D-kkE__o9yt8QVzQLUlvOw
source: 机器之心
title: 刚刚，DeepSeek Harness更新！增强多模态
---

# 刚刚，DeepSeek Harness更新！增强多模态

> 原文链接：https://mp.weixin.qq.com/s/D-kkE__o9yt8QVzQLUlvOw
> 来源：机器之心

机器之心编辑部
深夜，DeepSeek Harness 迎来一波大更新，RC.8 版本已经放出。
距离 RC.7 发布才过去两天，DeepSeek 又给这个开源 Agent 框架补上了一批关键能力。此次更新覆盖多模态输入、子代理、工具调用、Windows 终端以及底层存储等多个方向。
地址：https://github.com/deepseek-ai/deepseek-harness/releases
#en
-v0.1.0-rc.8
其中最值得关注的有两点。
第一，DeepSeek Harness 的多模态能力进一步补齐。
根据更新文档来看：DeepSeek 模型适配器现在可以直接开启原生图片请求，/goal、/plan 等核心命令也已经支持图文混合输入。与此同时，@ 菜单新增了文件和历史会话引用，用户可以直接把本地文件、此前的对话上下文一起交给 Agent 处理。
另一个值得关注的变化，是 Claude Code 和 Codex 被进一步纳入 DeepSeek Harness 的 Agent 编排体系。这可能也是 RC.8 最值得关注的变化。
RC.8 中，两者都可以作为 Profile Bundle 按需安装，并作为子代理被 Harness 调用。其中 Codex 还新增了非交互权限模式，并支持同时运行多个命名实例。
这表明，DeepSeek Harness 正在越来越像一个 Agent 的统一调度层：上层负责拆任务和编排工作流，底层可以根据任务需要，把不同 Coding Agent 拉进来干活。
事实上，这条路线在 RC.7 中已经初现雏形。
8 月 17 日发布的 RC.7，首次让 Codex 与 Claude Code 的子代理任务接入 Job Panel。用户可以直接在 Harness 的任务面板中管理这两类 Agent 的执行过程。到了 RC.8，这项能力又往前走了一步：Claude Code 和 Codex 对应的 provider 可以做成独立 Profile Bundle，需要时再安装。
工具调用也有一轮明显加强。
web_search 现在支持并发查询；子代理完成任务后，reportDelivery 可以及时反馈结果并主动唤醒父任务。对于需要同时搜索多个信息源、再交给主 Agent 汇总的长链任务，这类改动会直接影响整个工作流的执行效率。
Windows 用户也迎来一个实用更新。PTY 终端现在支持持久化 PowerShell 会话，并且在 Minimal 预设中默认开启。安装和启动流程也进一步简化，包括缩小依赖下载体积，以及本地运行 dsh web 时自动打开浏览器。
此外，RC.8 还集中修掉了一批实际使用中的问题，包括：
修复图片尺寸过大或历史图片累计载荷过高导致模型请求失败的问题
修正取消流式生成后已展示的回复前缀未带入后续提问和分叉会话
修复部分自定义 OpenAI 兼容网关因请求格式差异无法调用，以及推理内容回传可能缺失问题
在 SDK 方面，Python SDK 依赖配置覆盖 4 个内置 Agent 预设，并包含 rg /glob 搜索和 MCP stdio 工具所需依赖。
以上就是更新的一些内容，可以看出 RC.8 最值得关注的地方，可能还真不是某一个新增功能。DeepSeek Harness 正在慢慢把 Claude Code、Codex 这样的顶级 Coding Agent，都变成自己工作流里可以随时调来的「队友」。
© THE END
转载请联系本公众号获得授权
投稿或寻求报道：liyazhou@jiqizhixin.com
