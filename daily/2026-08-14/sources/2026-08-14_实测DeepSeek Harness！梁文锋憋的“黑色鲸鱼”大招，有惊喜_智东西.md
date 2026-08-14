---
publish_time: 1786637587
status: pending
category: 
is_model_related: true
digest: |
  智东西实测DeepSeek Harness：上手体验梁文锋团队最新Agent架构'黑色鲸鱼'大招，实测其在任务拆解、工具调用与自主闭环上的表现，总体'有惊喜'，给出一手使用评测与能力边界。
link: https://mp.weixin.qq.com/s/xSS-d5Pr36o7x7Cp25fPKQ
source: 智东西
title: 实测DeepSeek Harness！梁文锋憋的“黑色鲸鱼”大招，有惊喜
---
# 实测DeepSeek Harness！梁文锋憋的“黑色鲸鱼”大招，有惊喜

来源：智东西
原文链接：https://mp.weixin.qq.com/s/xSS-d5Pr36o7x7Cp25fPKQ

DeepSeek Harness发布。
作者 |
毕伟豪
编辑 |
漠影
智东西8月14日报道，昨夜，
DeepSeek Harness的开发者预览版（v0.1版本）正式公测，并同步开源
。
DeepSeek Harness团队负责人崔添翼在社交媒体上表示，这是一个预览版本，可能存在很多粗糙之处，希望大家多提意见。消息一出，
半小时DeepSeek Harness的GitHub仓库星数就超过了一万
，
截至发稿已经超过了3万
。
而就在宣布公测两小时前，DeepSeek官方才宣布了DeepSeek-V4-Pro正式版上线以及价格即将大幅上涨的消息，这套闪电二连击引爆了社交媒体。
国内外社交媒体上很多内测成员纷纷发表“解密感言”，还晒出了内测成员大合影，但也有开发者认为这更像是一个开发框架，而非Coding Agent。
原因在于，与社区先前猜测不同的是，DeepSeek Harness并没有采用Pi Agent架构，也没有套用DeepSeek模型缓存命中率超高的Reasonix。
据DeepSeek Harness团队称，DeepSeek Harness采用“一切皆插件”的设计思路，模型、工具、技能、会话、沙箱、存储、循环、调度、UI等所有Agent能力，都由插件组合而成，可自由替换、灵活重组。
底层是Cordis插件系统，这个元框架只负责插件的加载、卸载和依赖关系，Agent Harness的所有具体组件都是不同的Cordis插件，元框架的理念来自北京大学和DeepSeek联合署名的一篇论文《A Programming Paradigm for Spatiotemporal Composability》。
仓库地址：
https://github.com/deepseek-ai/deepseek-harness
论文地址：
https://github.com/cordiverse/paper/blob/main/paper.pdf
看到消息的第一时间，智东西就拉取源码安装了DeepSeek Harness，用上了这个期待许久的Agent底层框架。
01
.
一切皆插件，内置四种模式
默认加载不同插件集
安装其实也非常简单，如果你有常用的Agent，直接把下面这段代码丢给它即可：
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
安装完成后，打开本地网关，可以看到这样的界面，输入DeepSeek的API Key即可进入DeepSeek Harness。
映入眼帘的是一个非常干净，但又有点熟悉的界面，不得不说和网页版DeepSeek还是挺像的，不太一样的地方在于
DeepSeek Harness
的鲸鱼是黑色的。
页面左侧是新建对话的菜单栏，右侧是输入框和模式选择区域，设置中可以选择一些内置的插件，其他就什么都没有了。
如开头所说，DeepSeek Harness采用“一切皆插件”的设计思路，而这种设计思路反映在Agent上，演化成了标准、极简、创造和PTC（程序化工具调用）四种模式，每种模式默认加载不同插件集合，开发者可以根据不同使用场景自由选择。
标准模式
提供完整工具组合；
PTC模式
由模型生成一段代码组合多轮工具调用；
极简模式
只留一个shell工具和一个文件编辑工具，专门给最小环境下的模型基准测试使用；
创造模式
可以检查当前运行时、在内存中试验 Cordis 插件，并据此组合和创作新的模式。
DeepSeek Harness团队强调“每一次运行都有迹可循”，这个有迹可循体现在一个非常有意思的设计上——轨迹。
模型看到的一切都会写入仅追加（append-only）设计的会话日志，包括系统提示词、思维链、工具调用与结果、子Agent调度，以及每一次上下文注入。在轨迹视图中可以按来源查看这些信息，恢复、分叉、检索与回放也都共享这一事件流。
下方的每一个彩色读条都对应着一个运行节点，鼠标选中读条即可查看对应部分的具体运行过程。
02
.
体验：88页论文翻译耗时22分钟
做贪吃蛇游戏只要50秒
智东西也是在标准模式下，给了DeepSeek Harness一个非常简单的任务，翻译PDF文件，源文件是前文提到的Cordis元框架那篇论文，DeepSeek Harness确实是一穷二白，首次执行任务PDF提取工具也需要先安装一下。
很快DeepSeek Harness提取了PDF文件，但它识别出我桌面上存在一个对该论文的翻译文件，只不过创建时间有点不太对，它推荐我在原文件的基础上进行补充。
其实DeepSeek Harness的任务执行过程还是很顺畅的，而且整体流程很透明，任务拆分比较合理，在补齐论文的过程中派发了10个子代理，对我原本的翻译文件进行了复制、修正以及补齐。
最后得到了一份格式比较完整、内容严谨的翻译文件。
从数据上看，DeepSeek Harness的任务执行速度尚可，88页论文翻译任务耗时22分钟，首Token启动速度平均在1.4秒，缓存命中率98%，输入6.6M，输出72.7k。
任务完成后再打开轨迹页面，可以看到密密麻麻的一片进度条，所有的工具调用、子代理派发都一览无余，所有过程都可以在这里面查看，报错信息亦然，对于开发者来说非常便利。
此外，我还分别使用极简模式和PTC模式写了贪吃蛇游戏，极简模式下，DeepSeek Harness仅用50多秒就完成了任务，而PTC用时一分零五秒，但极简模式中的游戏并没有写成HTML的格式，需要在python中运行。
可以看到的是，极简模式是专门为模型测试准备的，完全不会去做多余动作。
03
.
结语：一款与用户期待不太一样的产品
初次体验下来，DeepSeek Harness似乎真的不是一款面向C端用户的产品，就像崔添翼所说，面向全球开发者进行测试。
DeepSeek Harness所提供的功能非常简洁，极简模式、创造模式包括这个插件系统的架构，都是为开发者自主创造而设计的。
但这并不意味着DeepSeek Harness不是一款好产品，相反，它对于喜欢Agent的人来说，就像一款乐高玩具，你可以随自己的心意将它组装成任何样子。
的确，它现在不管是从生态，还是从功能上都算不上“顶尖”，但它是开源的，是可塑的，能够随着使用的过程不断进化为用户想要的样子。
闭源为用户提供现在，开源让用户自己掌握未来。
9月20-21日，智东西主办的
2026全球AI芯片峰会
将在上海举行，设有开幕式，
大模型AI芯片、Agent推理芯片、具身智能芯片
3场高峰论坛
，以及
Token工厂异构混训混推、超节点、AI芯片架构创新、新型存储器、大模型KV Cache
5场技术研讨会
。
