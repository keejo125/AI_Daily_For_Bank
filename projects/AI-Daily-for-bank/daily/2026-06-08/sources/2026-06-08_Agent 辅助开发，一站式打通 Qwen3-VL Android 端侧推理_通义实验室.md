---
publish_time: 1780912416
---

# Agent 辅助开发，一站式打通 Qwen3-VL Android 端侧推理

> 原文链接：https://mp.weixin.qq.com/s/VhxGZp9FNCLbi3e_aoBRzg
> 公众号：通义实验室

在上一期

《让手机拥有视觉感知能力》

中，我们探讨了如何通过 MCP 架构和端侧语义提取，让大模型安全地“看懂”物理世界。

但

在实际动手时我们会发现：

做端侧 AI App 会伴随一长串的工程问题：

Android 环境怎么配？

模型怎么下？

MNN是什么，跟App的关系是啥？

1.4GB 模型怎么推到手机？

输出截断、ADB 多设备、手机拒绝安装这些坑怎么排？

第二期教程我们将换一种玩法：不用手动敲命令，把繁琐的工程任务交给 Agent，你负责思考目标与业务逻辑，Agent 负责检查环境、写代码、跑构建、排 Bug。

本文将带你一步步跑通：Android Native C++ 工程、MNN runtime 编译、Qwen3-VL 模型部署、JNI 桥接，最终在手机上实现真正的

端侧图文推理！

提示

在真实开发里，每个人的路径、环境、代理、设备状态都不一样（当前教程均在Mac环境下）。所以这篇教程换个方式写：

明确任务目标 ➔ 提供直接可用的 Prompt ➔ 说明 Agent 应该帮你确认的结果

。

第一步：下载 Android Studio，并检查 Android 环境

安装 Android Studio

先安装 Android Studio，下载的地址如下：

https://developer.android.com/studio?pkg=studio

，Android Studio 是构建 Android 应用的基础平台，是不可或缺项。

补全其他环境

装完 Android Studio 还没结束，还需要补齐这些环境组件：

JDK（电脑端 Java 构建环境，用来运行 Gradle 和 Android 构建工具）

Android SDK（提供 Android 平台 API、构建工具和 adb 等基础开发组件）

NDK（让 App 能编译和运行 C/C++ 原生代码）

CMake

（负责把 C/C++ 代码组织成可被 Android 加载的原生库）

adb / platform-tools（连接 Android 设备、安装 APK、推送模型文件）

Git（下载 MNN 源码或管理项目代码）

Python / uvx / ModelScope

CLI

（下载 ModelScope 模型）

推荐用版本如下：

JDK

21

Android SDK：本项目使用 compileSdk

35

、targetSdk

35

、minSdk

29

NDK

27

CMake

3.18.1

adb / platform-tools：使用 Android SDK 自带版本

Git：系统可用即可

Python / uvx：能运行 ModelScope

CLI

即可

一台 arm64-v8a 的真实手机（任意

4

GB 以上 Android 手机均可）

你可以

直接复制以下 Prompt 发给 Agent (如 Qoder)：

请检查当前机器的

Android

端侧开发环境是否完整，如果不完整请帮我下载补全

。

重点检查：

JDK

、

Android

SDK

、

NDK

、

CMake

、

adb

、

Git

、

Python

/uvx/

ModelScope

CLI等

本项目用于集成

MNN

+

Qwen3

-

VL，推荐使用：JDK

21

、

NDK

27

、

CMake

3.18

.

1

第二步：创建 Native C++ Android 工程

由于项目需要 JNI（Java Native Interface）作为

Android/Kotlin

代码调用 C/C++ 原生代码的桥梁，我们直接使用 Android Studio 的 Native C++ 模板来创建项目。

项目配置

打开 Android Studio，按下图配置项目：

你也可以

直接复制以下 Prompt 让

Qoder

创建项目：

请在当前目录创建一个新的 Android Native C++ 项目，用于集成 MNN + Qwen3-VL 端侧推理。

项目要求：

1.

项目名：PhotoTaggerMNN

2.

包名：com.local.phototaggermnn

3.

使用 Kotlin。

4.

使用 Android Native C++ 模板，确保包含 CMakeLists.txt 和 native-lib.cpp。

5.

minSdk 设置为 29。

6.

compileSdk / targetSdk 使用当前 Android SDK 已安装的稳定版本，优先使用 35。

7.

只构建 arm64-v8a。

8.

NDK 使用 27。

9.

CMake 使用 3.18.1。

10.

C++ 标准使用 C++17。

11.

启用 ViewBinding。

12.

创建完成后运行，确认基础工程可以构建。

如果当前目录已经是 Android 项目，请不要重新创建项目，而是检查并修正现有项目配置，使它满足以上要求。

这里重点是只保留

arm64-v8a

，因为后面我们编译的

libMNN.so

也是这个架构！

第三步：下载 Qwen3-VL 的 MNN 模型

Qwen3-VL 的 MNN 版本模型已经在魔搭上准备好了

MNN/Qwen3-VL-2B-Instruct-MNN

。无需自己手敲下载命令，直接让 Qoder 做，或者直接到魔搭下载模型：

https://modelscope.cn/models/MNN/Qwen3-VL-2B-Instruct-MNN

或者对 Qoder说：

请在当前 Android 项目根目录下，使用 ModelScope CLI 下载 Qwen3-VL 的 MNN 版本模型。

请执行：

modelscope download \

--model

MNN/Qwen3-VL-

2

B-Instruct-MNN \

--local_dir

models/MNN/Qwen3-VL-

2

B-Instruct-MNN

如果当前环境没有安装 modelscope 命令，请用 uvx 或 pip 搜索安装：python3 -m pip install -U modelscope

下载完成后，请检查目录大小，并确认模型相关关键文件存在

Qoder 下载完成后，应给你类似结果：

模型目录约 1.4GB

关键文件全部存在

注意：

1.4GB

的模型

绝对

不要

打包进 APK 中

，否则安装、调试、传输都会非常痛苦。我们后续会将其推送到手机私有目录。

第四步：让 Agent 编译支持 Qwen3-VL 的 libMNN.so

MNN 默认编译出来的库不一定包含 LLM 和视觉能力。我们需要定制编译一个专属的

libMNN.so

（

具体也可以参见

第一篇

教程

）。这一步非常适合交给 Agent，因为它会根据本机的 NDK 路径、CMake 版本自动调整命令。

对 Qoder 说：

请下载或准备 MNN 源码，并为 Android arm64-v8a 编译一个支持 Qwen3-VL 的 libMNN.so。

要求：

1.

使用当前 Android SDK 里的 NDK 27。

2.

开启 MNN

_BUILD_

LLM。

3.

开启 LLM

_SUPPORT_

VISION。

4.

开启 MNN

_IMGCODECS 和 MNN_

BUILD

_OPENCV。

5. 使用 MNN_SEP

_BUILD=OFF，确保 LLM、视觉等能力进入同一个 libMNN.so。

6. 关闭测试和 benchmark，避免无关目标导致构建失败。

7. 编译完成后，把 libMNN.so 复制到 app/src/main/jniLibs/arm64-v8a/libMNN.so。

8. 最后检查 so 文件大小，并运行 Gradle 构建验证 APK。

我们实际编译后得到：

app/src/main/jniLibs/arm64-v8a/libMNN.so

APK 内也确认包含：

lib/arm64-v8a/libMNN.so

lib/arm64-v8a/libphototaggermnn.so

第五步：把 MNN 接进 Android 工程，并构建App

编译出 libMNN.so 只是第一步，Android 工程还要知道怎么链接它。

接复制以下 Prompt 发给

Qoder：

请把 MNN 接入当前 Android Native C++ 工程。要求：1. CMake 导入 app/src/main/jniLibs/arm64-v8a/libMNN.so。2. CMake include MNN/include。3. CMake include transformers/llm/engine/include。4. target_link_libraries 链接 MNN、android、

log

、jnigraphics。5. Kotlin 启动时先 System.loadLibrary(

"MNN"

)，再加载本项目 JNI 库。6. 新增 nativeRuntimeInfo 方法，在 App 页面显示 MNN 版本和 ABI。7. 运行 assembleDebug 验证 APK 能构建。

这里的目标是先让 App 成功带着 libMNN.so 跑起来。

现在我们先构建一个最小的 Android App，App 内需要做一个最小的页面，确认 MNN runtime 和模型目录都没问题。

对 Qoder 说：

构建App，并请在 App 首页做一个 MNN 和模型文件检查页面。要求：

1

. 显示 MNN runtime 版本。

2

. 显示当前 ABI。

3

. 检查模型目录下 config

.json

、llm

.mnn

、llm

.mnn.weight

、visual

.mnn

、visual

.mnn.weight

、tokenizer

.txt

是否存在。

4

. 每个文件显示 ok 或 missing。

5

. 如果全部存在，显示 Ready forLlm::

createLLM

(config.json)。

6

. 构建完成后运行 assembleDebug 验证。

以上都运行结束后，我们的 App 就运行好了，现在我们需要把App安装到手机上。

第七步：连接手机

底座没问题了，接下来上真机！

在手机上打开调试模型，将手机用 USB 或 Type-C 线链接至你的电脑，并且打开手机上的调试模式（搜索调试模式即可）

如图所示，打开系统的开发者选项，并打开 USB 调试

这样我们的 Android Studio 就可以安装 App 到手机上了，如需检查连接并安装App，可以对 Qoder 说：

请检查当前是否有 Android 真机连接。如果 adb devices 里有多个设备，请找出在线的真机序列号。后续所有 adb 命令都请自动带上 -s

<

真机序列号

>

。然后请把当前构建的APK 安装到这台真机上。如果设备是 unauthorized、offline 或安装失败，请告诉我手机端应该检查哪些设置。

按照以上的命令，我们就可以成功的将App安装到我们已经连接的手机上了！

第八步：推送模型到 App 私有目录

App 安装成功后，再推模型。

对 Qoder 说：

请写并执行一个 scripts

/push_qwen3_vl_2b_to_device.sh 脚本，把本地模型目录：models/

MNN

/Qwen3-VL-2B-Instruct-MNN推送到 Android App 私有目录：/

data

/data/

com.local.phototaggermnn

/files/

mnn_models

/

qwen3

-

vl

-

2b要求：

1

. 自动查找 adb

。

2

. 如果有多个设备，优先使用

ANDROID_SERIAL

。

3

. 如果没有

ANDROID_SERIAL，则自动选择唯一在线的

device

。

4

. 忽略 offline 模拟器

。

5

. 先 adb push 到

/data/

local

/tmp/

qwen3

-

vl

-

2b

。

6

. 再用 run

-

as

com.local.phototaggermnn 拷贝到 files

/mnn_models/

qwen3

-

vl

-

2b

。

7

. 脚本失败时给出清晰错误

。

8

. 推送完成后，重新打开

App，确认模型文件检查页面全部显示

ok

。

这里要强调一句：推送模型依赖于App 已经安装，所以模型推送必须发生在安装 App 之后。

模型推完后，重新打开 App。

正常应该看到：

MNN

loaded:

3

.

5

.

0

ABI: arm64-v8a[ok] config.json[ok] llm.mnn[ok] llm.mnn.json[ok] llm.mnn.weight[ok] llm_config.json[ok] tokenizer.txt[ok] visual.mnn[ok] visual.mnn.weightReady forLlm::createLLM(config.json).

看到这个，说明在推理前的所有准备工作都已经完成了：

libMNN.so

成功加载模型成功推到手机JNI

能访问模型文件

这一步跑通后，再做真正推理会稳很多。

第九步：构建真正的、可以推理的App

当我们确认底座没问题后，再加推理能力。

对 Qoder 说（以下是最简单的内容，可以按照自己的想法随意调整）：

请在当前 App 里做一个最小调试页面，并实现对应 JNI 推理桥，用于测试本地 Qwen3-VL 图文推理能力。页面需要包含：

1.

选择本地图片按钮。

2.

图片预览。

3.

Prompt 输入框。

4.

Max new tokens 输入框，默认 512。

5.

加载模型按钮。

6.

开始推理按钮。

7.

Output 输出区。

8.

Logs 日志区。

Native 层要求：

1.

nativeLoadModel(configPath, cachePath)：调用 Llm::createLLM(configPath)，设置 runtime config，并执行 load。

2.

nativeGenerate(prompt, bitmap, maxNewTokens)：如果 bitmap 不为空，把 Android Bitmap 转成 MNN Tensor，然后构造 MultimodalPrompt。

3.

图片 prompt 使用

<

img

>

image

_0

</

img

>

占位，并把 image_

0 映射到 PromptImagePart。

4.

如果没有图片，则走纯文本 response。

5.

nativeReleaseModel 用于释放全局 Llm 实例。

6.

所有阶段都输出页面日志和 Logcat。

7.

返回内容末尾追加 metrics，包括 finish

_status、current_

token、prompt

_len、decode_

len、output

_chars、vision_

ms、prefill

_ms、decode_

ms、total。

8.

推理不能阻塞主线程。

9.

构建完成后运行 assembleDebug 验证。

按照以上的方法调整后，我们就可以获得了一个可以分析理解，运行端侧模型的最小App，我们可以进行一下简单测试。

这套流程最终跑通了什么？

Android Native C++ 工程

MNN Android runtime 编译

Qwen3-VL MNN 模型下载

模型部署到手机私有目录

JNI 桥接

Bitmap 转 MNN Tensor

MultimodalPrompt 构造

端侧图文推理

到这里，我们已经完成了最关键的一步：让 Android 手机真正具备了本地图文理解能力。

这篇文章做的不是一个最终产品，而是先把最难的底座打通：Android 工程、MNN runtime、Qwen3-VL 模型、JNI 桥接、本地图片输入和端侧推理链路。后面就可以继续往上构建更复杂的 App 能力。

接下来，我们会基于这个本地 VL 模型继续扩展更多场景，如：本地相册自动打标和检索、拍照后自动生成结构化描述、端侧 OCR 和物体识别等，大家敬请期待～

推荐阅读

PawBench：给通用智能体一把可度量的尺

Qwen3.7-Plus：把多模态AI变成“实干家”