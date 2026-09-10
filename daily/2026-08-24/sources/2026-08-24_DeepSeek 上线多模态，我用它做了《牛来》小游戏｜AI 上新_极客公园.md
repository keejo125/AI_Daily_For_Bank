---
publish_time: 1787555656
link: http://www.geekpark.net/news/369278
source: 极客公园
status: confirmed
category: 国内
is_model_related: true
digest: |
  8 月 21 日 DeepSeek 正式上线多模态视觉理解模型 DeepSeek-V4-Flash-Vision-Exp（API：deepseek-v4-flash-vision-exp），支持图片内联/URL/Files API 三种传入，单图最多 384 token（约为 GPT/Claude 同等图一半），纯文本能力不降级、多模态 Agent 能力「接近 Opus-4.8」。极客公园实测：喂《牛来》截图生成 SVG 卡通牛（35 秒、384 token）、做跑酷小游戏（36 秒）、看设计稿出可运行 HTML（26 秒）。踩坑提示：默认 thinking 模式推理 token 会吞光输出预算，需设 reasoning_effort:none。DeepSeek 选择在 Flash 而非 Pro 试水视觉，配合 Harness RC.8 打通多模态 Agent 管道。
---

# DeepSeek 上线多模态，我用它做了《牛来》小游戏｜AI 上新

> 原文链接：http://www.geekpark.net/news/369278
> 来源：极客公园

作者｜Wildcard

编辑｜靖宇

多模态也是「梁心」地板价。

「鲸鱼睁眼了！」

非常突然的，8 月 21 日 DeepSeek 官方正式宣布，V4-Flash-Vision-Exp 上线，开启多模态 API 服务。

等了这么久，DeepSeek 模型终于补上了多模态能力，欢喜的人们甚至差点忘了 DeepSeek 刚刚开始根据使用时间涨价的事儿。

梁文锋滑动变阻器，旋钮向着「梁圣」方向前进一格。

极客公园按耐不住，马上测试了起来。

栏目作者召集
极客公园的新栏目「AI 上新」，将带大家体验最新的 AI 应用和硬件，让你成为 AI 时代「最靓的仔」！

现在，我们也向所有喜欢尝鲜和体验 AI 的同学发出召集，只要你发现并体验了新的 AI 应用或者功能，按照格式（参考案例： 实测正式版 DeepSeek V4 Pro，补齐 Agent 能力｜AI 上新 ）向栏目投稿，在极客公园公众号发布，不仅能获得相应稿费，且会为你「报销」AI 应用的订阅费用。

同时，优秀作者还有机会进入极客公园 AI 体验群，获得最新 AI 应用和工具的内测资格，参加极客公园专属相关 AI 活动，和 AI 应用创始人一对一沟通。

AGI 太久，只争朝夕，让一部分人先 AI 起来吧！投稿、进群请扫描下方二维码添加极客小助手微信👇

01
能力接近 Opus4.8

DeepSeek 在微信公众号发布公告，全新的多模态视觉理解模型DeepSeek-V4-Flash-Vision-Exp 正式上线 API 平台。开发者可以通过设置 model='deepseek-v4-flash-vision-exp' 直接调用，支持 base64 内联、外部 URL、Files API 三种图片传入方式。

但名字里带着「Exp」三个字母，说明故事才刚开始。

从官方公告来看，V4-Flash-Vision-Exp 有几个关键参数值得注意。

DeepSeek 官方给出的数据｜图片来源：DeepSeek

定价与 V4-Flash 一致。一张图片最多占 384 个 token，按 token 计费，没有额外的视觉处理溢价。做个对比&mdash;&mdash;GPT 和 Claude 处理同等分辨率的图片通常消耗 800 到 1100 个 token。同一张图，DeepSeek 的 token 开销不到竞品的一半。这个数字背后是 DeepSeek 此前公布的「Thinking with Visual Primitives」框架在起作用，它将视觉元素压缩成空间坐标式的原语，而不是把整张图拆成密密麻麻的图像 patch。

纯文本能力没有降级。官方强调，在 Agent、推理、世界知识等纯文本基准上，Vision-Exp 与 V4-Flash 正式版持平。这意味着它不是一个「为了看图牺牲了文本能力」的特化模型，而是在 Flash 基础上叠加了视觉理解。

多模态 Agent 能力「已接近 Opus-4.8」。这是官方公告里最大胆的一句话。在需要视觉理解的 Agent Benchmark 上，Vision-Exp 相比纯文本的 V4-Flash 实现了大幅跃升。

同步上线的还有Files API&mdash;&mdash;这个接口本身不收费，开发者可以先把图片上传到平台拿到 file_id，之后在请求中直接引用，同一张图多次调用不用重复传输。对于需要反复分析同一批图片的 Agent 工作流来说，这是一个很实际的优化。

02
给《牛来》做个 AI 重制版

规格说完了，上手测。

2026 年暑假最火的梗是什么？《牛来》。这部母子手搓 5 年、3D 建模粗糙到被网友称为「连 AI 都生成不出来」的动画电影，票房从 7169 元逆袭到 3000 万，成了全网最大的行为艺术。

我们决定用它来做第一个测试&mdash;&mdash;把《牛来》那个经典的「妈妈」特写截图喂给 DeepSeek Vision，让它看懂画面后用纯代码画一个「AI 重制版」。

对比图_牛来重制.png&mdash;&mdash; 左边原片截图，右边 AI 重制版｜图片来源：极客公园

DeepSeek 的表现多少有点一言难尽。

但至少它准确识别了牛的橙色配色、皱着的眉毛、厚嘴唇和「既凶又委屈」的表情，还保留了画面底部的「妈妈」字幕。输出的 SVG + CSS 代码渲染出来，是一头有渐变光泽、圆润线条的卡通牛&mdash;&mdash;从「恐怖谷」直接跳到了「萌系」。

整个过程只用了 35 秒，图片仅消耗 384 个 token。网友说「AI 都比原片更像电影」，现在有了实锤（不是。

我们还做了一个更有趣的测试&mdash;&mdash;给 DeepSeek 看了《牛来》两头牛面对面的截图，让它根据画面中牛的形象，直接写一个可交互的跑酷小游戏。

牛来跑酷游戏｜图片来源：极客公园

DeepSeek 从截图中提取了牛的配色和基本形态，用 CSS 绘制了一个像素风的奔跑牛角色，搭配了天空、草地、障碍物和计分系统。从看到图片到输出可玩的完整 HTML 游戏，一共花了 36 秒。

这个 demo 本身可能没有生产力价值，但它展示了一件更重要的事&mdash;&mdash;视觉理解和代码生成能力叠加在一起时，AI 能做的事情比单独拥有任何一项要多得多。

03
看截图写代码，一步到位

第二个测试更贴近真实的工作场景。

我们制作了一张支付产品的 Landing Page 设计稿&mdash;&mdash;深色渐变背景、导航栏、大标题、代码区域的语法高亮、双按钮、三个 feature 卡片&mdash;&mdash;然后截图喂给 DeepSeek Vision，要求它直接输出可运行的 HTML。

对比图_看图写代码.png&mdash;&mdash; 左边设计稿，右边 AI 生成的 HTML 页面｜图片来源：极客公园

26 秒后，DeepSeek 输出了一份完整的响应式 HTML 页面。渐变背景色、导航栏布局、按钮样式、代码区域的语法高亮颜色&mdash;&mdash;全部精确匹配。它甚至自主添加了 hover 动效和入场动画。

这个能力直接指向 Agent 的核心场景。当你的 AI Agent 需要操作浏览器、理解一个网页界面的结构，或者把设计师的视觉稿快速变成前端代码，视觉理解就不再是「锦上添花」，而是「能不能干活」的前提。

但测试中也遇到了一个熟悉的问题。

在开启默认的 thinking 模式时，模型的推理 token 会疯狂膨胀，吞掉全部输出预算。我们在场景理解测试中观察到，2001 个 completion token 里，2001 个全是 reasoning token&mdash;&mdash;实际输出为零。模型想了半天，一个字都没说出来。

解决方法跟上次一样粗暴&mdash;&mdash;设置 reasoning_effort: "none" 关掉思考模式。关掉后，同一个测试从 23 秒缩短到 7.9 秒，输出完整且质量上乘。

这已经是连续两个版本复现的同一个问题了。V4 Pro 正式版发布时，我们发现 thinking 模式会消耗 82% 以上的输出预算；现在 Flash Vision 又出现了 100% 被推理吃光的情况。对于开发者来说，这意味着一个实操层面的硬规则&mdash;&mdash;在视觉任务中，请务必关闭 thinking 模式或设置足够大的 max_tokens，否则大概率拿到空响应。

这条经验，我们已经替你踩过两次了。

04
为什么是 Flash

一个值得思考的产品决策是，DeepSeek 选择先在 Flash 上试水视觉能力，而不是旗舰 Pro。

从成本来看，Flash 是 284B 参数的 MoE 模型，推理成本远低于 1.6T 参数的 Pro。每张图片至少占 384 个 token 的输入预算，如果叠加在 Pro 的定价上，成本会迅速膨胀。Flash 的低价基底让多模态调用在经济上可行。

从节奏看，就在前一天，DeepSeek Harness 框架刚发布了 RC.8 版本，新增了原生图片请求的支持。

Harness 在框架层打通了多模态 Agent 的管道，Flash Vision 在模型层补上了视觉理解的引擎&mdash;&mdash;两手同时落子，指向的是同一个目标：

让 DeepSeek 生态里的 Agent 真正「看得见」。

回看这四个月的多模态补课时间线&mdash;&mdash;4 月底灰度识图模式，5 月大范围开放网页端，6 月全量上线 App，8 月 Harness 框架支持多模态，同一天 Flash Vision API 开放&mdash;&mdash;每一步都精确地踩在前一步的基础上。只是它没有开发布会，而是用一个带着「Exp」后缀的模型名，悄悄把门推开。

对于一直在等多模态 API 的开发者来说，等待结束了&mdash;&mdash;虽然结尾写的是「Exp」而不是「GA」。对于正在构建多模态 Agent 的团队来说，一个 token 消耗不到竞品一半、纯文本能力没有降级的视觉模型，可能是当下性价比最高的选项。

只是，别忘了关掉 thinking 模式。

*头图来源：AI 生成

本文为极客公园原创文章，转载请联系极客君微信 geekparkGO