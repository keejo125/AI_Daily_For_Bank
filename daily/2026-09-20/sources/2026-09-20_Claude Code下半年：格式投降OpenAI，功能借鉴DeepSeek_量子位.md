---
publish_time: 1789879800
link: https://mp.weixin.qq.com/s/Z0a9aSn1ncJDRFDgBHYB1g
source: 量子位
status: confirmed
category: 国际
is_model_related: false
digest: |
  量子位报道，Claude Code自9月19日起原生支持AGENTS.md，向OpenAI在2025年8月推出的项目指令文件格式“投降”——此前Claude Code一直只读自己的CLAUDE.md。抽样显示，6.2%的GitHub活跃仓库已包含AGENTS.md，略高于CLAUDE.md的5.4%，大量开发者不得不同时维护两个文件。与此同时，Claude Code在功能上借鉴了DeepSeek等产品的思路。文章认为，Agent编码工具正从各自为政走向格式互通，但也暴露出多文件维护的负担。
title: Claude Code下半年：格式投降OpenAI，功能借鉴DeepSeek
---

# Claude Code下半年：格式投降OpenAI，功能借鉴DeepSeek

来源：量子位
原文链接：https://mp.weixin.qq.com/s/Z0a9aSn1ncJDRFDgBHYB1g

梦晨 发自 凹非寺
量子位 | 公众号 QbitAI
Claude向OpenAI格式投降了。
Claude Code从9月19日起
原生支持AGENTS.md
。
这是OpenAI在2025年8月推出的一种项目指令文件格式，此前Claude Code一直坚持只读自己的CLAUDE.md。
现在兼容了，隔壁OpenAI加的Tibo也来围观支持。
大概在5月，Agents.md的使用数量就已经超越了Claude.md。
就在更新这一天，有人搞了个抽样调查，
6.2%的GitHub活跃仓库
包含AGENTS.md（活跃仓库标准是90天内有push、非fork、非archived），
CLAUDE.md的比例是5.4%。
也就是说，大量项目的开发者不得不同时维护两个文件。
尽管从格式到内容，两者几乎没什么区别。
没什么区别，但是折磨开发者一年
OpenAI为自家的Codex设计了AGENTS.md，给AI编程助手一个标准化的方式来读取项目的编码规范、构建步骤和测试要求。它本质上就是一个放在代码仓库根目录的Markdown文件，相当于写给AI的README。
OpenAI从一开始就没有把它叫做OpenAI.md或者Codex.md。
这个开放格式迅速获得了行业认可，到2025年12月，OpenAI把AGENTS.md捐赠给了Linux基金会下新成立的Agentic AI Foundation（AAIF）。
奇怪的是
Anthropic也是这个基金会的联合创始方之一
，捐出了自家的MCP协议，Block则贡献了goose框架。AWS、Google、Microsoft、Bloomberg、Cloudflare全部以白金会员身份加入。
Codex、GitHub Copilot、Cursor、Windsurf、Gemini CLI、Aider、Zed、Jules、JetBrains Junie先后宣布原生支持Agents.md。
在所有主流AI编程工具中，Claude Code是最后一个。
Claude Code只认CLAUDE.md这件事，已经困扰开发者很久了。
同一个项目里，Codex读AGENTS.md，Cursor读AGENTS.md，只有Claude Code要求一份单独的CLAUDE.md。两份文件内容90%重合，却必须分开维护。
一旦一边更新另一边忘了改，不同AI agent就会给出矛盾的建议。
社区被迫发明了各种变通方案。这些变通方案能用，但都有各自的问题。
最常见的是在项目根目录执行
ln -s AGENTS.md CLAUDE.md
，用文件系统的符号链接让两个文件名指向同一份内容。
但这在Windows上需要管理员权限或开发者模式，
Git在Windows上默认也不保留符号链接
，没有正确配置的情况下克隆仓库，CLAUDE.md会变成只包含「AGENTS.md」这几个字母的空壳文件，Agent读进去完全无效，而且也不会报错，很容易发现不了。
也有人在CLAUDE.md第一行写@AGENTS.md利用导入语法间接读取。
对于新加入团队的成员来说，看到一个只有一行内容、指向另一个不同名Markdown文件的指令文件，很难理解发生了什么。
用多个AI编程工具协作的团队受影响最大。
同一个代码仓库要同时维护CLAUDE.md和AGENTS.md，内容高度重复，但又不完全相同，CLAUDE.md可能包含Claude特有的指令，AGENTS.md则是工具无关的。
两个文件一旦漂移不同步，排查问题会非常头疼。
Claude Code的下一步：Mod
Claude Code 2.1.277的实现方式是回退机制，而不是全面替换。
默认模式叫「claude-md-or-agents-md」：只有当项目中不存在任何CLAUDE.md的时候，才会去查找并加载AGENTS.md。如果项目已经有了CLAUDE.md，哪怕只是一个空文件，AGENTS.md就不会被读取。
除了默认模式之外，开发者还可以在/config中选择另外三种模式：只读CLAUDE.md、同时读取两种文件、或者只加载组织级别的托管指令文件，整个功能作为一个内置插件（Mod）实现。
Claude Code的Mod系统9月刚刚发布，本质上是一套插件系统
，允许开发者在Claude Code的运行流程中插入自定义逻辑。
每个mod可以监听特定的生命周期事件，比如会话启动、上下文构建、工具调用、子agent派生等，在这些关键节点上拦截、修改或补充Claude Code的默认行为。
通过Mod，你甚至可以在Claude Code里玩俄罗斯方块。
不过从Agents.md的支持上也可以看出Claude Code插件体系还有一些不完善。
文档中列出了一系列「仍然与CLAUDE.md存在差异」的条目：
AGENTS.md的嵌套文件只在文本类型的Read操作中触发，不覆盖IDE中打开的文件、notebook和图片等场景；
/memory命令和#快捷键不识别AGENTS.md文件；
--add-dir添加的额外目录不会加载其中的AGENTS.md；
AGENTS.md中引用外部路径的@导入需要借用CLAUDE.md的授权对话框才能生效，自身不会触发授权提示。
这些限制来自于当前插件事件体系尚未覆盖到这些场景。
所以总结这一波，Claude Code在格式上更像OpenAI了，在功能上更像DeepSeek了。
参考链接：
[1]https://x.com/trq212/status/2101009392611278961?s=20
[2]https://github.com/anthropics/claude-code/tree/main/mods/agents-md
一键三连
「点赞」「转发」「小心心」
欢迎在评论区留下你的想法！
—
完
—
🌟 点亮星标 🌟
科技前沿进展每日见
