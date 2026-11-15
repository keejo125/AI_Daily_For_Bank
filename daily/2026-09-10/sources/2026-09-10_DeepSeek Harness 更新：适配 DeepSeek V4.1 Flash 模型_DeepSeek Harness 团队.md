---
publish_time: 1789017808
link: https://mp.weixin.qq.com/s/lt6fT1iYCJIfEdAGlJEktg
source: DeepSeek Harness 团队
status: confirmed
category: 国内
is_model_related: false
digest: |
  DeepSeek Harness v0.1.5 发布，深度适配新发布的 DeepSeek V4.1 Flash 模型：该模型在标准、程序化工具调用（PTC）与极简三种模式下均经专项训练与优化。新版同时为插件作者开放更多标准化 UI 扩展入口，新增文件上传、侧边栏文件预览等能力，并优化交互性能，持续增加与模型前沿结合的实验性功能。
title: DeepSeek Harness 更新：适配 DeepSeek V4.1 Flash 模型
---

# DeepSeek Harness 更新：适配 DeepSeek V4.1 Flash 模型

来源：DeepSeek Harness 团队
原文链接：https://mp.weixin.qq.com/s/lt6fT1iYCJIfEdAGlJEktg

DeepSeek Harness v0.1.5 版本现已发布。新版本与 DeepSeek V4.1 Flash 模型训练深度结合，模型在 DeepSeek Harness  的不同配置中都进行了专项训练和优化。同时，新版 DeepSeek Harness 为插件作者提供了更多标准化的 UI 扩展入口，新增了文件上传、侧边栏文件预览等功能，优化了 UI 的性能与交互，并持续增加与模型研究前沿深度结合的实验性功能。
主要更新
面向 DeepSeek V4.1 Flash 模型的适配
DeepSeek V4.1 Flash 模型针对 DeepSeek Harness 进行了专项训练和优化，覆盖标准模式、程序化工具调用（PTC）模式和极简模式。
在使用 DeepSeek V4.1 Flash 模型时，DeepSeek Harness 新版本还支持在保留已有 KV Cache 的情况下更新系统提示词。
针对 DeepSeek 模型和 Harness 的反馈可以使用 UI 中的点赞、点踩功能以及 /feedback 命令提交给 DeepSeek 团队。
文件处理与预览方式进一步丰富
Web 界面现已支持上传包括图片、PDF 等多种类型的文件，模型可通过文件工具按需读取。右侧 Sidebar 支持浏览工作区文件树，并可直接预览 Markdown、HTML、PDF、常见代码和图片格式的文件；模型产出的文件既可以在 Sidebar 中查看，也可以通过系统默认应用打开，或在文件管理器中定位。
面向插件作者的标准化 Web UI 扩展入口
Web 界面已在左右两侧建立标准化的插件扩展入口。插件可以在左侧 Sidebar 的“新会话”和“工作区”之间注册全局入口，并与中央内容面板联动；右侧 Sidebar 则支持插件注册新的 Tab 类型和内容页面，并通过多标签、分栏与全屏等方式展示预览内容或工具界面。
至此，插件在主界面左右两侧都有了明确的接入位置，为后续的插件管理功能和更多插件扩展入口的加入打下了基础。
长会话性能与使用体验持续优化
新版本优化了长会话的加载、恢复与持续对话性能，降低内存占用，优化存储格式。会话过程内容折叠、完整历史轮次导航，以及正文宽度、字号和运行统计等交互也得到完善。
子 Agent 通信与任务控制更加灵活
父 Agent 与可继续对话的子 Agent 支持双向通信，可在执行过程中补充信息、调整任务方向；用户也可排队发送消息、编辑或删除待处理消息，以及插话或停止任务；主 Agent 可为子 Agent 选择模型和推理强度。
实验性功能 Agent Teams
Agent Teams 允许主 Agent 创建多个团队成员，通过共享任务列表拆分、分配和跟踪工作。成员之间可互发消息；主 Agent 可查看进度、等待结果或中断任务，最后统一汇总。Web 端可查看团队成员和共享任务，也能进入任一成员的子会话继续沟通。
该功能以实验性插件方式提供，默认关闭，开发者需在命令行中将相关的实验性插件加入 Profile 中使用，使用会产生额外 Token 消耗。
用户实践
近期，社区开发者使用 DeepSeek V4.1 Flash 模型与 DeepSeek Harness 做出了一些有意思的作品和插件，我们选取了其中一部分与大家分享。
上下滑动查看更多
安装使用
快速体验
在已安装 Node.js 开发工具链的系统中，可以使用 npx 命令快速启动 DeepSeek Harness 的 Web UI：
npx @deepseek-ai/dsh web
源码安装
获取完整项目源码，并按照仓库说明完成安装：
git
clone
https://github.com/deepseek-ai/deepseek-harness
“一切皆插件”的下一步
在后续版本中，我们计划新增内置插件管理面板，让开发者和用户更方便地管理插件、相关配置及其 UI 入口展示。同时，计划面向插件开发者提供更多插件扩展入口，支持插件代码以更灵活、可靠的方式嵌入和调用内置功能，以及将插件 UI 嵌入界面的更多位置。
DeepSeek Harness 团队仍在开放招聘中，欢迎加入我们，一起打造 “一切皆插件” 的下一步，一起探索模型与 Harness 共同进化的 Agent 智能上限。
