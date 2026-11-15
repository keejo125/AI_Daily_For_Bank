---
publish_time: 1791689228
link: https://www.qbitai.com/2026/10/502544.html
source: 量子位
status: confirmed
category: 国内
is_model_related: false
digest: |
  民间开发者基于DeepSeek Harness（DSH）推出“DeepSeek-Bot”——一套多Bot团队界面，上线不到一天即获250+星。每个Bot拥有独立身份、角色、模型与持久化长期记忆；可设“Main Bot”主管，在群聊中默认由其回复并调度其他Bot，既降低多Agent管理复杂度，也减少群聊场景的token消耗。技术上每个Bot对应一个DSH Session，超长对话以压缩、交接摘要与本地搜索管理上下文，记忆以Markdown文件存储并支持团队共享，每轮对话结束自动做记忆审查。项目采用Apache 2.0许可，DSH桌面端与Web端均可安装，延续DSH“一切皆插件”理念。
---

# DeepSeek Bot来了！民间版，DSH装个插件就能用

> 原文链接：https://www.qbitai.com/2026/10/502544.html
> 来源：量子位

DeepSeek Bot来了！民间版，DSH装个插件就能用
鱼羊
量子位
Grok Bot我养不起，ds bot不得高低尝尝咸淡？
鱼羊 发自 凹非寺
量子位 | 公众号QbitAI
DeepSeek官方Muse还没来，民间高手们已经迫不及待了。
刚刚新鲜上桌的是「DeepSeek-Bot」：
基于DeepSeek Harness的机器人团队
。
△图源：作者@Fei2411
跟Grok Bot一样，ds bot基于DeepSeek Harness做了一套多Bot团队界面。
每个Bot都可以拥有自己的名字、角色、模型，更重要的是「持久化」——能够积累长期记忆。
另外，为了节省token，你还可以给Bot们安排一个主管，有事先找主管，再让它去协同Bot们就行。
作者FeiZ还给划了重点：
你可以为ds bot接入任何你想接入的模型。未来甚至可以接入本地Agent。
ds bot继承了dsh的「一切皆插件」理念，以保持可拓展性。
虽然非官方，不过似乎这才是蓝色大肥鱼的正统风味（bushi）？
上线不到一天，大肥鱼爱好者们已经给这个项目点了250+星。
Grok Bot我养不起，ds bot那不得高低尝尝咸淡？
基于DSH的bot插件
一切皆插件，ds bot同样是插件的形式。
主要功能如下。
有问题，先找Bot主管
在ds bot里，每个Bot都有独立身份，可以设置名称、职责说明、指令、形象，以及背后调用的模型。
Bot们具有持久化的运行状态，拥有长期记忆。
还可以设置Main Bot。这个Bot主管拥有高权限，能帮你管理、配置其他Bot和群聊，既能降低管理多个Agent的复杂度，也能在群聊这种狂烧token的环境里，降低token消耗。
这方面，ds bot是专门做了优化的：在一个群聊里设置管理员，你的消息默认会由管理员回复，它会帮你调用其他bot。
当然，你也可以直接@需要单独沟通的bot，来进行一对一。
△图源：作者@Fei2411
总之，作者强烈建议，直接通过和Bot对话来配置其他Bot和群聊。
BTW，作者还提到，Bot的模型可以随时切换。不过：
我仍然建议你长期使用同一个模型，仅在真正需要时才进行切换。
长期记忆
长期记忆是ds bot的一个重点。记忆可以在详情页中管理，也可以直接对话管理。
从技术上来说，每个Bot在底层对应一个DeepSeek Harness Session，拥有自己的工作上下文。
遇到超出上下文窗口的长对话，ds bot会使用压缩、交接摘要和本地搜索等机制管理上下文。
ds bot还为每个Bot设置了基于Markdown文件的记忆存储，同时设计了团队共享记忆。
另外，每轮对话结束后，模型都会进行自动记忆审查，判断哪些信息需要保存、更新或删除。
其他的技术特点还包括：
使用量统计：在Settings → Usage中，可以查看按时间、Bot和模型分类的Token使用情况。
数据本地化：所有数据都保存在你电脑DSH主文件夹目录下的bot/ 和sessions/ 文件夹中。卸载插件不会删除这些数据。
开源与许可：项目采用Apache License 2.0许可。
安装与使用
DSH的桌面端和Web端都能使用ds bot。
桌面端，在侧边栏选择「插件」→「添加插件」，输入「ds-bot」即可安装。
Web端，需要Node.js 22.19或更高版本，以及pnpm。然后通过以下命令来添加插件：
npx @deepseek-ai/dsh@0.2.1-alpha.1 plugin –profile web add ds-bot
npx @deepseek-ai/dsh@0.2.1-alpha.1 web
更多细节，可以参见项目主页。
那么，如果你感兴趣，就可以耍起来了，欢迎回到评论区留下你的使用反馈呀~
项目地址：
https://github.com/FeiZhuLulu/DeepSeek-Bot/tree/main
— 完 —
版权所有，未经授权不得以任何形式转载及使用，违者必究。
Deepseek
鱼羊
马斯克睡进工地！为AI基建拼了
李飞飞发布：全球首个多模态世界模型
ResNet作者任少卿机器人创业！公司注册就独角兽了
突发，Jeff Dean离职创业！谷歌股价应声蒸发1.34万亿
扫码分享至朋友圈
相关阅读
新研究揭示DeepSeek弱点：频繁切换思路欠思考，最短答案往往就对
国内外两支团队同时发现
梦晨
Deepseek
推理大模型
DeepSeek新论文公开Agent训练！梁文锋署名
每秒能产生5000+个沙盒
克雷西
Deepseek
DeepSeek一句话让国产芯片集体暴涨！背后的UE8M0 FP8到底是个啥
国产AI正在走向软硬协同阶段
克雷西
Deepseek
芯片
DeepSeek V3.1更新「最终版」！下一次是V4/R2了？？？
修复「极你太美」Bug
鱼羊
Deepseek
华为昇腾推理DeepSeek-R1，性能比肩高端GPU，API免费无限量
同步推出云镜像服务
明敏
Deepseek
华为昇腾
DeepSeek识图模式是个新模型？！一手实测在此（没错我被灰度到了）
非思考模式快到飞起
鱼羊
Deepseek
多模态