---
publish_time: 1786773181
status: confirmed
category: 国内
is_model_related: false
digest: |
  DeepSeek Harness开源后GitHub上dsh-plugin标签公开仓库已超700个，社区玩法爆发。实用类：dsh-agent-teams（对话拉起多Agent团队）、DSH Better Sidebar（侧边栏变迷你IDE）、dsh-at-file（@文件）、dsh-memory-evolve（跨会话长期记忆+感知Git分支）、dsh-plugin-claude-bridge/claude-move（迁移Claude Code记忆与会话）、ModLens（外挂视觉引擎）。
  趣味类：dsh-TUI（Claude Code风格终端）、dsh-web-ui（电子宠物）、dsh-ads（2005风格广告）、dsh-minigames（18款小游戏）、deepseek-manners（自动补“谢谢你，鲸鱼大人”）。整体体现“Everything is a Plugin”生态。
link: https://www.qbitai.com/2026/08/473597.html
source: 量子位
title: 
---

# DeepSeek Harness插件一夜燃爆GitHub：长期记忆、电子宠物、4399小游戏全来了

> 原文链接：https://www.qbitai.com/2026/08/473597.html
> 来源：量子位

DeepSeek Harness插件一夜燃爆GitHub：长期记忆、电子宠物、4399小游戏全来了
梦瑶
量子位
大家已经给DeepSeek装上了啥
梦瑶 发自 凹非寺
量子位 | 公众号 QbitAI
忒忒忒忒火爆！！
DeepSeek Harness这下真快被网友「插成万物」了。
小黑鲸上线还没多久，单单在GitHub上打着dsh-plugin标签的公开仓库，就已经冲到了
700+
个？？？
有人给它装
浏览器、长期记忆、数据库和任务管理
；有人嫌DeepSeek不会看图，现场接了个视觉模型进去。
再往下翻，画风直接开始放飞——
电子宠物、像素鲸鱼、18款小游戏
，网友大神统统给小鲸鱼安排上，真·赛博装修队连夜进场啊我说？
更神的还在后面。
2005年
中文网站风格广告UI
，这玩意儿居然也有人专门做了插件？？
DeepSeek前脚喊出：Everything is a Plugin！
网友后脚的理解大概就是：懂咧，那我可什么都往里塞了哈～
行，那既然都玩成这样了——
咱就瞅瞅这波社区开发者到底把DeepSeek Harness《盘》成啥样了。。。
700+个仓库，大家已经给DeepSeek装上了啥
常言道，就论给官方产品搞衍生玩法这件事儿，开发者从来没让人失望过。
DeepSeek Harness本身是一套开源Agent Harness，它整个架构最核心的一句话就是：
Everything is a Plugin.（万物皆插件）
这句Slogan，属实生逢其时。
前脚DeepSeek Harness一发布，后脚网友就开始大测特测，那边GitHub也跟开闸了一样，各种插件哗哗往外冒。。。
我也小小扫了一圈，目前各社区维护的Awesome DeepSeek Harness Plugins精选目录，就已经收录了无数个插件。
开发工具、Agent编排、效率协作、数据研究、DevOps、AI设计与媒体，全都有人做。
真·德智体美劳，甭管跟干活效率搭边不搭边，先给小黑鲸安排上再说……
先看一个很实用的插件——
dsh-agent-teams
。
这东西能帮咱直接在Harness里现场拉起一支多Agent团队。
比如你说一句「用AgentTeams调研一下XX」。
当前会话里的Agent能立马原地升职当队长，再拉几个子Agent进组，拆任务、设依赖、互相发消息，成员之间还能直接沟通。
而且Web界面右上角还能实时围观整个团队：谁在干活、谁空闲、谁摸鱼，真·上帝视角了。
赛博钉钉，这不就建起来了！
再往下看，还有一个给侧边栏疯狂增肥的插件——
DSH Better Sidebar。
文件管理、代码编辑、终端、Git面板、后台任务、子Agent，全被它塞进了同一块侧边栏。
换句话说，装完插件之后侧边栏也逐渐长成了一个迷你IDE工作台。
所以它最明显的价值，就是可以让我们少！切！窗！口！
比如以前我们可能得在Harness、VS Code、终端、Git之间来回横跳，现在不少操作直接在侧边栏里就能完成，文件能看能改，终端是真Shell，Git还能看diff、暂存和提交。
（Alt+Tab：挺好，终于能少挨几下毒打了。）
接下来这个插件就更简单粗暴了——
dsh-at-file
。
是的，友友们，我们可以在DeepSeek Harness里直接@文件了。
它给DSH补上了类似Codex的@file能力，可以直接在输入框里搜索工作区文件，然后把指定文件内容一起塞进Prompt。
比如你想让Agent参考现有登录模块，把支付页也照着同一套逻辑改一遍。
以前可能得自己找文件、复制代码、粘进去。
现在——@login.ts，改。
完事儿。
还有一个很符合当下Agent潮流的插件：
dsh-memory-evolve
。
它给DeepSeek Harness补上了一套跨会话长期记忆。
项目约定、架构决策、踩过的坑、当前进度，它都可以持续记下来，甚至还能感知Git分支，并在后台做Skill演化。
对于长期项目而言这个插件就很实用了，比如你今天告诉它：“这个项目部署端口是8080。”
确认之后，它会把这件事写进项目记忆，过几天你重新开个会话，再问部署配置，它还能直接接上，不用你又从项目背景开始讲。
而且记忆太多也能归档，需要时再调出来，相当于把AI从每次开聊都失忆，变成一个能长期跟项目的助手：
此外，Claude用户要是想数据资料搬家，那下面这俩插件没准能帮上亿点点小忙。
首先是能把Claude Code的记忆、Skill和配置搬进DSH的
「dsh-plugin-claude-bridge」。
像现在好多友友已经在Claude Code里积了一堆CLAUDE.md、Skills和历史配置，那这插件就是直接架桥，把这些东西带进DeepSeek Harness。
然后就是
「dsh-claude-move」
，这玩意儿搬的更彻底，连Claude Code旧会话都能整体迁过来。。。
Session、Memory、Skills、CLAUDE.md都能导，甚至可以直接在DSH里接着之前的会话往下聊，真·赛博大迁徙超实用工具了也是。
再比如ModLens。
装进DeepSeek Harness之后，我们可以直接往聊天框里粘图片。
ModLens会先调用外挂视觉引擎，把图片里的文字、布局、实体和语义信息整理成结构化证据，再交给DeepSeek继续推理，非常实用的还是：
其他一些偏实用类的DeepSeek Harness插件就不一一展开说了，再简单介绍几个我自认为蛮实用的工具：
dsh-github-connector：
直接让Agent在对话里管GitHub
context-vista：
直接看上下文Token都被谁吃了
dsh-undo：
Agent改崩了，可以直接回滚上下文
dsh-record-replay：
你演示一遍操作，Agent以后能照着复现
dsh-obsidian-export：
把Harness对话一键沉淀进Obsidian
dsh-share：
一键分享Harness里的完整对话
……
太多了，实用的插件太多了，友友们直接在GitHub上贪婪地大搜特搜，大装特装叭！
缺啥补啥，网友把Harness玩成了赛博改装车？？
如果说前面的插件还属于「为了让Agent更好干活」。
那么继续往下翻GitHub，开发者的精神状态就开始逐渐抽象化了。
因为整个DeepSeek Harness在GitHub上，也越来越像一台刚提回家的素车——
有人换发动机，有人装中控，有人贴痛车膜，还有人在后排塞了一台游戏机。
如果你嫌界面太正经……
那如果我说，Claude Code风格在Harness的全屏终端界面也能实现呢？
在
dsh-TUI
插件里，素鲸鱼顶栏、实时工作状态、思考流展开、双击Esc回滚、上下文进度条、TPS仪表这些全都有。
神了。
还有
dsh-web-ui
插件，连二次元电子宠物都安排上了。
任务看板、Git图谱、右侧面板、移动端远程、实时Token统计、皮肤中心全塞进去了。
不知道为什么，有种梦回千禧年贴吧和QQ空间的感觉啊我说！！！
然后更抽象的来了——
dsh-ads
。
朋友们，这个插件存在的唯一意义，我猜可能就是给DSH Web UI添加2005年中文互联网风格广告。
侧栏广告、对话内信息流、角落弹窗全有，开屏广告内味儿立刻出来了。
请问这个插件的受众是？？？（bushi
然后，还有一个看起来很不务正业、但又莫名很合理的插件：
dsh-minigames。
干嘛用？等模型回复、等Agent跑任务、等Bug修复的时候——
玩游戏。
而且绝对不是随手塞两个小游戏意思一下，足！足！18款！
俄罗斯方块、坦克大战、消消乐、华容道、贪吃蛇、2048、扫雷、五子棋、黑白棋、数独、吃豆人全都有。
一眼望过去，我恍惚间以为自己点开了4399，我只能说，这个开发者是懂Agent用户的。。。
One More Thing
然后。
就在我沉浸在这个黑鲸生态圈无法自拔的时候，又被一个项目震慑住了。
它叫
deepseek-manners
。
功能非常单纯，甚至单纯到让人肃然起敬。
每次AI回复结束后，自动补一句：
谢谢你，鲸鱼大人。
没了，对。整个插件就干这一个事儿。
泪目了。
在这个实用主义盛行的Everything is a Plugin时代。
还有大神想得起来礼貌也得「插件」化——
Everything is a plugin,including politeness.
参考链接：
[1]https://github.com/topics/dsh-plugin
[2]https://github.com/Dominic789654/awesome-deepseek-harness
[3]https://github.com/omdsh-dev
[4]https://github.com/Alex-Yanggg/awesome-DSH-plugin
版权所有，未经授权不得以任何形式转载及使用，违者必究。
Deepseek
梦瑶
源神启动！一张消费级显卡跑“Opus级”Agent，Qwen3.8-27B多项榜单反超Claude
国产具身智能创全球新纪录！以30%成本跑赢 Figure AI 45%效率，聪明的具身大脑成关键
苹果开测长鑫存储！百度、千问也一起挤进苹果供应链
等等，MiniMax H3不是刚发布吗？怎么就卷到几分钱的价格了……
扫码分享至朋友圈
相关阅读
不用跟着挤DeepSeek官方了！这个神器让你零门槛拥有私人助手
免费使用，无额度限制
白交
Deepseek
支付宝
智能体
DeepSeek突然拥抱国产GPU语言!对标CUDA替代Triton,华为Day0适配
DeepSeek v3.2隐藏菜单
梦晨
Deepseek
DeepSeek-V3.2-Exp第一时间上线华为云
目前可访问华为云官网，体验DeepSeek-V3.2-Exp模型的卓越能力
明敏
Deepseek
华为云
刚刚，DeepSeek V4 Pro正式版发布，多项对标Fable 5
现在调用V4 Pro，能直接用上完全体
Jay
Deepseek
国产之光DeepSeek把AI大佬全炸出来了！671B大模型训练只需此前算力1/10，细节全公开
"有限算力下的美妙工程”
一水
Deepseek
DeepSeek新模型霸榜，代码能力与OpenAI o1相当且确认开源，网友：今年编程只剩Tab键
团队还给基准测试挑出了bug
西风
Deepseek
DeepSeek-R1-Preview