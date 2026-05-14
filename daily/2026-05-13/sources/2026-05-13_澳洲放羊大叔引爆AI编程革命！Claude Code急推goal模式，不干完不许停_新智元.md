---
publish_time: 1778666400
---

# 澳洲放羊大叔引爆AI编程革命！Claude Code急推goal模式，不干完不许停

> 原文链接：https://mp.weixin.qq.com/s/VwsCC3WNHatLbGBPDw7VOw
> 公众号：新智元

新智元报道

编辑：好困 KingZH

【新智元导读】

澳洲牧羊大叔随手写的三行bash，11天内被OpenAI、Anthropic和Hermes集体收编了。

一觉醒来，Claude Code又更新！

为了让Claude 持续工作直到任务完成，Claude Code最近推出的新功能：/goal 。

你只要设定条件，Claude不完成任务它绝不罢休！

用过AI编程工具的人都懂，这到底多重要！

你给Agent下了一个任务，它跑了三个回合，改了两个文件，突然停下来问你「接下来需要我做什么？」

不是，bug你这还没修完呢啊！

Agent越来越聪明，写代码越来越快，但「从头到尾把一件事干完」这件事，到2026年初都没有一家能做到。

然后，

一位来自澳大利亚的牧羊大叔Geoffrey Huntley，用三行bash解决了。

while

:;

do

cat

PROMPT.md | claude-code --

continue

done

他把它命名为

Ralph Loop

，致敬《辛普森一家》里那个永远搞不清状况但从不放弃的小孩Ralph Wiggum。

逻辑极其粗暴，无限循环，反复把同一个prompt喂给Agent。进度写在文件系统和Git历史里，上下文满了就开新实例，读文件接着干。

原始，不优雅，但十分有效。

有效到OpenAI看见了，Nous Research看见了，Anthropic也看见了。

11天，三家顶级AI实验室，不约而同地把这三行bash写进了官方产品。

这一刻，所有人都明白了一件事——

通用人工智能的临门一脚，可能不是更聪明的模型，而是「把事做完」的模型。

换句话说，AI编程的核心战场正在从「生成代码」转向「闭环交付」。

11天，三条线，同一个终点

4月30日，OpenAI的Codex率先上线

/goal

。

Greg Brockman在X上只丢了一句，「Codex现已内置Ralph loop++」。

一周后，Hermes Agent跟上。又过4天，Claude Code也上了。

11天。三家。同一个命令。同一个功能。

但实现路径，差了十万八千里。

Codex「不忘事」，Hermes「不烂尾」，Claude Code「不自欺」。

Codex：

把目标存成一条数据库记录

OpenAI是三家里最先出手的，方案也最简洁。

在Codex里，

/goal

是一个持久化的工作流对象，存在本地的app-server状态层里。

关掉终端、合上笔记本、甚至重启系统，目标都不会丢。下次打开Codex，自动接上。

模型通过结构化的

update_goal

工具汇报进度状态，token预算耗尽时触发「软着陆」而非硬停。

有人用这个功能连续跑了14个小时，中间暂停5小时去睡觉，回来Codex从断点续跑，把一个设备驱动项目做完了。

工程化，干净，但克制。

Hermes Agent：

一个人干不完，那就上一个团队

Hermes Agent的野心最大。

在这里，/goal

只是冰山一角。真正的重头戏是多智能体看板系统，Hermes把「让AI把活干完」从单Agent问题升级成了团队协作问题。

看板的底层是本地SQLite，持久化存储，跨重启不丢。

你在上面创建一个任务卡片，Hermes会直接把它拆成多个子任务，分配给不同的Agent worker。每个worker是一个独立的OS进程，有自己的身份、模型配置和工作目录。

看板和

/goal

是两套互补的系统。/goal管的是单个Agent的目标锁定（Ralph loop），看板管的是多个Agent之间的任务调度。一个纵向深入，一个横向铺开。

最后，是五层防烂尾机制。

第一层，心跳检测。

每个worker定期向看板报到，证明自己还活着。

第二层，僵尸回收。

worker超时没响应？系统自动判定死亡，回收它手上的任务重新分配。macOS上还有专门的达尔文僵尸检测逻辑。

第三层，退出拦截。

worker没完成任务就退出了？系统自动把它标记为blocked，不让它再接新活，防止「摸鱼型Agent」反复领任务又不做。

第四层，幻觉拦截。

这是最狠的一层。AI说「我做完了」不算数，系统会验证它实际产出的代码是否真的落盘了。Agent说自己创建了一个文件但实际上没有？抓住，回滚，重来。

第五层，重试预算。

每个任务有独立的

max_retries

，最多重试N次，超过就上报人类。绝对不会无限循环到死机。

Claude Code：

做事的人和验收的人，不能是同一个

Anthropic是三家里最后出手的，但方案最巧妙。

本质上，Claude Code的

/goal

是一个session级别的Stop Hook。

你设定一个完成条件（比如「test/auth目录下所有测试通过且lint无报错」），Claude就开始干活。

关键设计在验收环节。每干完一轮，系统不让Claude自己判断「我做完了没有」。

它把对话记录和你的完成条件一起发给一个独立的小模型（默认是Haiku），让这个小模型来裁判。

小模型如果觉得没完成，就需要返回一个具体理由（比如「test_login.py还有2个failure」）。然后这个理由会被注入Claude下一轮的上下文，指导它接着干。

如果小模型认为完成了，目标就会自动清除，任务结束。

值得一提的是，这个裁判模型不调用任何工具，不读文件，不跑命令。它只看Claude在对话里产出的内容。

所以，你的完成条件必须是Claude在对话中能证明的东西。

它最长支持4000字符，因此你可以写得很细。

甚至，还可以在条件里加约束，比如「不修改其他测试文件」「20轮内完成否则停止」等等。

决赛进行时：工作流入口

把视角拉远一步。

Claude Code背后站着Anthropic，

Codex背后站着OpenAI，

Hermes Agent接入了两边的模型，同时也是DeepSeek V4等模型的主力分发渠道。

三条路径，恰好覆盖了ASI决赛的三个生态入口。

而他们

争的，也是同一样东西——工作流。

谁的Agent先让开发者养成「设完目标就走开」的习惯，谁就锁死了工作流入口。

因为习惯一旦形成，迁移成本是指数级的。

你不会轻易离开一个已经跑通了看板调度、断点续传、checkpoint回滚的Agent基础设施。

一个看似很小的/goal命令，背后卡的是整条Agent工作流的护城河。

参考资料：

https://code.claude.com/docs/en/goal

https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.7

https://github.com/anthropics/claude-code/releases/tag/v2.1.139

https://developers.openai.com/codex/changelog

秒追ASI

⭐点赞、转发、在看一键三连⭐

点亮星标，锁定新智元极速推送！