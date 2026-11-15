---
publish_time: 1790402816
link: https://www.solidot.org/story?sid=85479
source: Solidot
status: confirmed
category: 国内
is_model_related: false
digest: |
  开源社区 HardenedLinux 发布用现代 C++ 开发的 CosyVoice 推理程序 Velum，编译为单一可执行文件，便于部署。CosyVoice 是当前较优秀的 TTS 模型，但其 Python 推理体系老旧、依赖体积大，不利于 Agent 大量部署；Velum 运行时无需任何 Python 依赖，更新即拷贝。作者表示该项目由人类做架构规划、DeepSeek-v4-pro 完成代码，体现了 DeepSeek 在该类工程上的能力。
---

# Velum：方便部署的CosyVoice推理程序

> 原文链接：https://www.solidot.org/story?sid=85479
> 来源：Solidot

Nala Ginrut 写道：
HardenedLinux 最近发布了可用于推理CosyVoice的Velum，它用modern C++开发，编译成一个单一的可执行文件，方便部署。

CosyVoice是目前比较优秀的一款 TTS 模型，但其推理程序使用的Python体系比较老旧，需要在部署的时候做一些处理，而且Python依赖占用空间较大，不利于大量能力情况下的Agent部署。要是每个agent能力都要一堆Python十几G的依赖，每一堆还有版本冲突，那就不要卖产品了，不如回家卖红薯。
Velum编译之后只有一个可执行文件，所谓部署更新就是拷贝。一些预处理的模型相关的东西虽然需要用Python生成，但运行时是不需要任何Python的东西。

Velum同时也是一个例证，它是由人类做架构规划，DeepSeek-v4-pro完成的项目，也就是说，DeepSeek足以做这种程度的Vibe。在目前Claude只需要两轮配额就烧干的今天，稍微复杂点的程序，如果不能用DeepSeek做，最后还是要回家卖红薯。

希望以后Codex和Claude也能增强自己的竞争力，把价格向DeepSeek靠拢，让天下无红薯可卖，也未尝不是一件美事。