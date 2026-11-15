---
publish_time: 1792391845
link: https://www.solidot.org/story?sid=85645
source: Solidot
status: confirmed
category: 国内
is_model_related: false
digest: |
  SonicBoom 是由 HardenedLinux 社区主导的全新 AI 运行时框架，采用 GPLv3 许可，提供语言无关的 C API，可用任意语言绑定实现高性能 AI 研发（官方支持 GNU Guile）。它利用 Guile 的 delimited continuation 实现应用层“死计算消除”，运行时含 LLVM MLIR，将计算图再次优化并依硬件生成 kernel，免去手工按硬件调优。研究侧兼具 PyTorch 灵活性与超越 llama.cpp 的单点推理性能；部署侧可直接加载模型高效推理，且研究与生产共用同一运行时图编译优化栈。
---

# SonicBoom发布：AI框架告别手工调优

> 原文链接：https://www.solidot.org/story?sid=85645
> 来源：Solidot

Nala Ginrut 写道：

SonicBoom是全新的AI运行时框架[0]，采用 GPLv3 许可证，由 HardenedLinux 社区主导开发。它提供语言无关的C API接口，这意味着你可以用任意语言绑定这个库，从而实现任何编程语言都能进行高性能AI研发。目前 GNU Guile 是官方支持的语言，同时利用 Guile 的 delimited continuation 实现了应用层的“死计算消除”，只有真正有效的计算才会进入运行时。

而运行时包含 LLVM MLIR，它将会把计算图再次优化，进一步去掉无效的计算图，并利用 LLVM 根据硬件具体生成 kernel，而不是手工根据硬件去优化 kernel。

对于 AI 研究而言，应用层绑定的动态语言将提供 pytorch 的灵活性，以及超越 llama.cpp 的单点推理性能。其实际运行的时候会自动将计算图进行编译优化，这样同时实现了 pytorch 的动态图弹性，以及 tensorflow 的静态图性能。

对于推理部署而言，无需应用层动态语言的支持，可以直接加载模型进行高效推理。但研究和生产部署使用的是完全相同的运行时图编译器优化栈，这意味着你研发完就能直接部署到产品。部署成本压缩到一个三百多MB的 .so 文件。没有几十个G的 python 全家桶。

llama.cpp 依靠非常有经验的工程师进行 kernel 调优，已经将性能优化到极致。而 SonicBoom 直接利用 llama.cpp 已有的 kernel，在 kernel 优化不变的情况下，依靠图编译器的优化，将原始性能提升20%（rtx3050 8G)，并且还在持续增加中。

目前 SonicBoom 社区版仅提供单点推理的能力，分布式推理能力计划于企业版提供。SonicBoom 的野心并不局限于 LLM 推理，它对标 pytorch，将在之后将更高的性能推向 image, video, tts 计算。

目前 SonicBoom 仅支持 CPI 和 CUDA，之后计划支持 Vulkan，为 non-nvidia 和纯自由软件爱好者提供更好的选择。我们目前缺乏足够多样的 GPU 评测数据用于优化，所以在 rtx 3050 之外可能测试数据会发生波动，您的评测数据能帮助我们把优化扩散到更多 GPU。

目前 v0.0.3 正在邀请社区贡献者参与不同 Nvidia 平台的评测，我们准备了非常简单那的脚本一行就能完成，不过测试时间可能比较长，请安排好自己的时间再参与，每位测评贡献者都会出现在贡献者名单中。[1]

如果您暂时没有硬件条件或者时间参与贡献，欢迎star，或者转发让更多有兴趣的朋友一起来玩。