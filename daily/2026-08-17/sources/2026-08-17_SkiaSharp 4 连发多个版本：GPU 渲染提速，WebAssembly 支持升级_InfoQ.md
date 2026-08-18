---
publish_time: 1786945200
status: pending
link: https://mp.weixin.qq.com/s/KUNcDsAJ-K8uMxAWyxobuw
source: InfoQ
title: SkiaSharp 4 连发多个版本：GPU 渲染提速，WebAssembly 支持升级
---
# SkiaSharp 4 连发多个版本：GPU 渲染提速，WebAssembly 支持升级

来源：InfoQ
原文链接：https://mp.weixin.qq.com/s/KUNcDsAJ-K8uMxAWyxobuw

作者 | Edin Kapić
译者 | 田橙
Microsoft 和 Uno Platform 发布了 SkiaSharp 4 系列的首批稳定版本，首先是 SkiaSharp 4.148.0，随后不久又发布了 4.150.0。4.151.0 预发布版本线也已推出，这体现了该项目将软件包版本和发布节奏与上游 Skia 里程碑保持一致的新方法。
SkiaSharp 为 谷歌的 Skia 2D 图形引擎 提供 .NET 绑定，覆盖移动、桌面、Web 和服务器应用。此前的稳定分支 SkiaSharp 3.119 已落后上游 Skia 数个里程碑。版本 4 对引擎进行了现代化改造，移除了较旧的 API，并引入了一种更可预测的模式，使稳定版和预览版软件包能够跟进 Chrome 各发布渠道所使用的 Skia 版本。
首个稳定版本 SkiaSharp 4.148.0 将内置引擎升级至 Skia m148。它增加了对 OpenType 可变字体轴的控制、彩色字体调色板选择、通过
SKWebpEncoder
进行动态 WebP 编码，以及零拷贝流和文本塑形 API。该项目还重新设计了共享原生对象的生命周期，以减少因原生操作期间托管包装器被终结而引发的释放后使用故障。
Microsoft 报告称，在针对以阴影和分层表面为主的 GPU 渲染界面进行的初步 OpenGL 测试中，性能最高提升了 24%。在该公司的测试中，基于 CPU 的 Perlin 噪声着色器速度提高了约六倍。不过，Microsoft 指出，结果取决于硬件和驱动程序，而以文本、图表或矢量地图为主的场景几乎没有变化。
SkiaSharp 4.150.0 于 7 月 7 日紧随其后发布， 将引擎更新至 Skia m150，并增加了多项图形诊断和滤镜 API。
SKPaint.GetFastBounds()
提供了一个用于可见性剔除的保守边界，而
SKImageFilter.CreateCrop()
和
CreateEmpty()
则支持滤镜链中的裁剪和透明空操作阶段。该版本还增加了
SKColorFilter.CreateOverdraw()
，用于可视化渲染热点，并缓存了
SKSurface.Canvas
包装器，以避免在渲染循环中重复进行托管分配。
4.151.0 版本 升级至 Skia m151，并主要聚焦于托管代码性能。颜色转换、预乘、标签解析和相关热点路径现在使用托管整数运算，而不是重复调用 P/Invoke。HarfBuzz UTF-8 编码使用池化缓冲区，而
SKShaper
则通过零拷贝 Span 公开字形结果。该版本还为十六进制颜色解析增加了无分配的
ReadOnlySpan
重载。
此外，4.151.0 版本还包含 Emscripten 5.0.6 库，用于让 SkiaSharp 配合 .NET 11 WebAssembly 的
exnref
异常处理模型运行。它修复了
SKImage.FromEncodedData
的一个裁剪图像重载中的原生句柄泄漏、在升级至 m151 期间引入的 CPU 光栅化回归，以及影响某些 WebAssembly 构建的宏冲突。与之前的版本不同，4.151.0 版本线未列出任何新的破坏性 API 变更。
从版本 3 升级至 SkiaSharp 4 仍属于破坏性升级。已过时的
SKPaint
文本和字体成员现在会导致编译错误，应用程序必须改用
SKFont
。无参数的
SKFont
也会使用
SKTypeface.Empty
，这意味着在开发者显式指定字体之前，文本不会被测量或渲染。此外，版本 4.150.0 还移除了该项目的 .NET Interactive 和 Polyglot Notebooks 集成包。
从 m148 快速推进至 m150 和 m151 表明，与里程碑保持一致不只是路线图中的承诺。稳定版软件包旨在跟进 Chrome Stable 和 Extended Stable 所使用的 Skia 里程碑，而预发布版本则跟进 Chrome Beta。
开发者可以 在 NuGet 上找到这些软件包，并查阅官方 发布说明、交互式画廊 和 GitHub 仓库，以获取示例和迁移详情。
原文链接：
https://www.infoq.com/news/2026/08/skia-sharp-4-release/
声明：本文为 InfoQ 翻译，未经许可禁止转载。
点击底部
阅读原文
访问 InfoQ 官网，获取更多精彩内容！
今日好文推荐
梁神变牢梁的原因找到了！疑似 DeepSeek 发错模型，HF配置和API后台紧急切换
编程能力提高50%！GLM-5.3 满分通过了GPT-5.6给的Coding 测试
Gemini 3.7 Flash 突袭！谷歌AI紧急换帅后的首个大动作，“内斗”真相浮出水面
DeepSeek 把 Harness 开源了：模型、工具、Agent Loop 全是插件
