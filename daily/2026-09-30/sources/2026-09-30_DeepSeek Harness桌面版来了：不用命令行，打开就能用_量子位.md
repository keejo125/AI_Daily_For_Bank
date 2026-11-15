---
publish_time: 1790697660
link: https://mp.weixin.qq.com/s/YBaKK_SkjnhvR_xdGBjGyA
source: 量子位
status: confirmed
category: 国内
is_model_related: false
digest: |
  DeepSeek Harness发布v0.2预览版，上线macOS与Windows桌面端，用户可直接下载安装、登录即用，无需再经命令行启动。桌面版与网页版界面一致，用Electron将Web UI及Agent、工具、插件运行逻辑封装进桌面应用，与CLI、Web版共用同一份.dsh数据，原有工作区与历史会话可延续。近期DSH密集更新：会话置顶归档、Agent工作过程可控展示、Office文档预览、文件Diff、Subagent、Agent Team、后台与定时任务，并新增账号与余额可直接查看用量与充值。
title: DeepSeek Harness桌面版来了：不用命令行，打开就能用
---

# DeepSeek Harness桌面版来了：不用命令行，打开就能用

来源：量子位
原文链接：https://mp.weixin.qq.com/s/YBaKK_SkjnhvR_xdGBjGyA

程浅 发自 凹非寺
量子位 | 公众号 QbitAI
刚刚，
DeepSeek Harness更新v0.2预览版，终于把桌面版端上来了。
访问官网deepseek.com/harness，
Mac和Windows用户现在都可以直接下载安装。
相比此前需要用命令行启动，现在的流程简单了不少。
不仅如此，桌面版上线的同时，Harness本身也刚经历了一轮
密集更新。
我翻了一下DeepSeek Harness最近十多天的Release——终端、Office文档预览、文件Diff、Subagent、Agent Team、后台任务、定时任务……该有的全都有了。
现在看来，DeepSeek Harness越来越像一款真正的产品了。
Harness桌面版长啥样？
外观上，桌面版和网页版长得不能说是毫无关系，只能说是一模一样。
而且装下来我感觉，最直接的变化其实就一个：
不用先过终端了
。
过去想用DeepSeek Harness，得先装好Node.js，再在终端里敲命令启动服务，最后打开浏览器使用。
对开发者来说，这几步当然算不上什么，但对不熟悉命令行的人来说，往往就是
“能不能开始用”
的区别。
现在装好之后，先登录，然后开袋即食，拎包入住。
还有一个比较大的变化就是，设置里多了一个“账号与余额”，可以直接在账户里查看余额和用量、直接充值。
此外，DeepSeek自己的账号体系也被直接接进了Harness。
登录后，模型列表里会多出一组“DeepSeek账号”模型，可以直接消耗账户余额跑任务，
不需要再单独去开放平台申请API Key。
技术实现上，Harness桌面版用Electron把原本的Web UI，以及Agent、工具、插件等运行逻辑一起装进了桌面应用。
桌面端和此前的CLI/Web版本共用同一份.dsh数据。因此
原来的工作区、历史会话和模型配置，打开客户端还能接着用。
最近几次DSH更新了什么？
我翻了一下DeepSeek Harness最近几次密集的Release。
从9月22日发布的0.1.7-alpha.1到最新v0.2预览版，
大量用户侧体验开始被补齐。
这一版更新中，会话可以置顶、归档，也支持搜索恢复；
新用户进入后会自动生成默认工作区，不必上来先选一个文件夹；
Agent的工作过程也开始可以控制展示程度，用户可以决定自己到底只想看结果，还是想多看一些中间过程。
与此同时，一些更接近“工作台”的能力也被补了进来。
长任务可以丢到后台继续跑，执行过程还能实时查看；
Excel、CSV、TSV等文件可以直接预览；
原本分散的模型配置，也被统一收进“模型提供商”入口。
以及大量的关于“用户怎么管理任务、文件和会话”的内容。
一天之后，0.1.7-rc.1上线。
这一版的重点主要是往Harness里塞了更完整的Agent能力。
首先是执行环境越来越完整：Web侧边栏直接加入终端；Headless模式可以从标准输入接收任务、继续已有会话；DSH还能本地运行Agent、通过SSH操作远端工作区。
其次是浏览器和Computer Use。
这一轮加入了实验性的Playwright MCP、Chrome DevTools MCP、Stagehand浏览器后端，以及Computer Use，可以通过驱动直接操作本机并获取截图。
第三块则是多Agent和插件系统。
Subagent可以直接在侧边栏打开；Agent Team面板能实时展示成员和任务。插件管理页也已经可以安装、配置、启停，甚至运行时卸载插件。
又过了一天，0.1.7-rc.2来了。
这次更新的重点，已经非常地“桌面软件”了。
首次打开Harness时，会出现完整的使用引导，可以选择自己更偏向“办公创作”还是“代码开发”，也可以决定想看到多少Agent的工作过程。
快捷键可以自己改，后台任务继续完善，还加入了定时任务。
现在就算重启应用，之前的任务状态仍然可以保留，把桌面窗口关掉之后，后台任务也能继续跑了。
此外，一些很产品经理的细节也出现了。
包括账号余额刷新、充值提示、登录失效、Windows自动更新、macOS窗口拖动、插件报错、语言切换……
总结来看，DeepSeek Harness最近这轮更新大概可以概括成两个方向。
一个是，Agent正在从“一次任务”变成“持续工作”。
加入了非常多关于多任务管理的功能，比如后台任务、任务恢复、定时执行、窗口关闭后继续运行。
另一个变化是，Harness正在从“工具”变成一个“产品”。
毕竟以前更新日志里高频出现的基本都是MCP、Tool、Runtime、Profile这些词。
现在越来越多的是首次启动引导、默认工作区、Office预览、快捷键、账号登录、后台任务等等。
这意味也是不言而喻了。
One More Thing
Harness这边刚有新动静，DeepSeek下一款模型V4.1 Pro也冒出了更多痕迹。
最近，第三方平台上已经出现了 deepseek-v4.1-pro 的模型条目。
不过上下文、输出长度、发布日期统统未知，Token使用量和用户数都是0。
据The Information报道，前几天，梁文锋在一场闭门投资者会议上透露，DeepSeek目前正在训练一个2万亿参数的大模型，未来甚至还计划继续做到8万亿参数。
为了防止内容再次外泄，这场会还要上交手机、电子设备和提包，只留纸和笔做记录。
也不知道这个2T模型是不是V4.1 Pro呢……
下载地址：https://www.deepseek.com/harness/
文档：
https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/desktop/README.zh.md
一键三连
「点赞」「转发」「小心心」
欢迎在评论区留下你的想法！
—
完
—
🌟 点亮星标 🌟
科技前沿进展每日见
