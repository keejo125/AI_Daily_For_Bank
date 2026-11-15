---
publish_time: 1792101600
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/Ouw9Bq6O9ZaGz4L716FcLg
source: AI寒武纪
title: 刚刚，Meta推出美国最强开源模型：8160亿参数，两台Mac Studio就能满血跑
---

# 刚刚，Meta推出美国最强开源模型：8160亿参数，两台Mac Studio就能满血跑

来源：AI寒武纪
原文链接：https://mp.weixin.qq.com/s/Ouw9Bq6O9ZaGz4L716FcLg

↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新
Meta推出美国迄今最强开源权重模型 Muse Spark Open
原生多模态。
总参数量 816B，单次激活参数 42B。
原生支持 100 万 token 的上下文窗口。
模型专门针对长周期任务、复杂软件工程和多步推理进行构建，核心专长就是写代码和执行复杂的 Agent 任务。
跑分：
核心的编程能力落后于几个月前的kimi k3和glm 5.3
最引人关注的突破在硬件部署门槛上。
借助最新的 MLX 框架，只要两台搭载 M5 Ultra 芯片的 Mac Studio，就能在本地桌面完整运行。
这是同级别模型第一次实现桌面端运行。
实现方式完全依靠硬件层面的吞吐。
M5 Ultra 的统一内存架构允许集成的 GPU 在单台机器上调动最多 512 GB 内存。
两台机器拼在一起，就变成了一台拥有 1 TB 统一内存的桌面超级计算机。
配合每台机器 1.2 TB/s 的内存带宽，读取每个 token 所需的参数切片速度完全足够。
官方进行了全本地环境的 Agent 工作流测试。
在完全依靠本地设备计算的情况下，Muse Spark Open 驱动的编程应用完成了对开源 Mastodon 客户端 Ice Cubes 的实际开发工作。
模型在本地独立完成了修复系统错误、编写新增功能以及最终的代码打包构建。
在另一项测试中，模型端到端接管了视频剪辑软件 DaVinci Resolve。
它逐帧审查素材，自动挑选出表现力最强的镜头片段，并将其统一裁切调整为竖屏视频。
除了苹果生态，模型在常规服务器硬件上也做了深度优化。
开源版本的权重内置了面向 SGLang 的自定义自动调优 Helion GPU 内核。
在英伟达和 AMD GPU 上，内核级别提速达到了 1.03 到 3.95 倍。
在 AMD MI350 芯片上，实现了 3% 的端到端提速。
模型对主流推理引擎提供了全面适配：
支持 SGLang、vLLM、TensorRT-LLM、Hugging Face Transformers、Apple MLX、llama.cpp 以及 Unsloth。
硬件底层覆盖了 AMD、Apple、Intel 和 NVIDIA 的芯片架构。
开发者如果需要定制训练，可以使用 PyTorch 旗下的 TorchTitan 工具进行后续调整。
目前模型的权重已经正式上线。
开发者可以在 Hugging Face、亚马逊 SageMaker AI、谷歌云 Model Garden 以及微软 Foundry Models 下载完整权重。
在 API 调用方面，Baseten、Fireworks AI、Groq、Modal、Nebius、OpenRouter 和 Together AI 已经同步支持。
开源协议方面，官方采用的是 Muse Model License，包含有限的商业条款，面向绝大多数开发者免费开放使用。
最后说一句
作为美国本土首个具备接近顶尖 Agent 能力的开源权重模型，基准测试的数据还没在实际落地中得到验证，小扎同学封闭开源同时开打，花几十亿美金挖人看来真不是白挖的。
--end--
最后记得⭐️我，每天都在更新：如果觉得文章还不错的话可以点赞转发推荐评论
/...@作者：你说的完全正确（YAR师）
