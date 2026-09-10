---
publish_time: 1777691414
---

# 苹果官方APP惊现Claude.md，24小时秒删！4万亿帝国AI底裤被扒光

> 原文链接：https://mp.weixin.qq.com/s/XZzW8exX38IoJ3de0l0LVw
> 公众号：新智元

新智元报道

编辑：好困 桃子

【新智元导读】

尴尬了！苹果Support App更新发生重大技术乌龙，工程师竟忘了删除CLAUDE.md文件，直接坐实了苹果内部AI架构竟是绕着Anthropic转的。

苹果自家工程师，也用上Claude了？

4月30日，Apple Support App推送了一个看似平平无奇的v5.13版本更新。

开发者Aaron Perris拆包后愣住了，App里赫然躺着两个不该出现的文件——CLAUDE.md。

从泄露的文件可以看出，苹果正在用Claude Code构建一套完整的AI系统，具体内容比「苹果在用AI」劲爆得多。

苹果发现后立即更新了App，但截图已经传开了。

这才真的是Claude无处不在。

一个.md文件

撕开了苹果的AI底裤

分析师Perris在X上贴出截图后，整个开发者社区炸了。

截图显示的内容，远不止「苹果在用Claude」这么简单。

第一个文件描述了一个聊天模块的完整架构——Juno AI。

三个角色分工明确，client（用户）、agent（真人客服）、assistant（AI助手）。

消息路由、异步流式传输、会话持久化，一套完整的AI客服系统设计图被摊在阳光下。

文件里还出现了几个关键词，「Juno AI」、「SupportAssistantAPIProvider」、「ChatKit」。

Juno AI，是苹果内部大模型平台的代号。

SupportAssistantAPIProvider，连接聊天界面和苹果AI后端的接口。

ChatKit，处理真人客服交互的内部平台。

条件编译标志JUNO_ENABLED和DEV_BUILD也赫然在列，甚至还引用了苹果内部Bug追踪系统的条目。

如此之高的架构完成度，大概只有苹果自己知道背后打磨了多久。

一次技术乌龙，坐实了一件事，4万亿美元帝国也离不开Claude。

三个月前就曝了

苹果靠Anthropic运转

有趣的是，早在今年1月曝出要与谷歌Gemini进行合作时，苹果内部的运转实际上全靠Anthropic——

无论是在产品开发，还是各种内部工具上，甚至内部服务器上，还跑着定制版的Claude。

在TBNP的采访中，

Mark Gurman

一句话道破，「现阶段，苹果就是靠Anthropic运转的」。

他们本来根本没打算用谷歌，苹果其实原本计划围绕Claude来重构Siri。

没谈成的原因是，Anthropic有点狮子大开口。

他们想要一大笔钱，一年就要几十亿美金，而且在接下来的三年里，价格每年还要再翻一倍。

最终，苹果以每年大约10亿美元的价格和Google Gemini签了Siri合作协议。

不过，虽然嘴上选了便宜的，手上却离不开贵的。

这一次没删掉的CLAUDE.md，直接把窗户纸捅破了。

写代码用Claude Code，搭AI客服系统也用Claude Code，去年9月Xcode就加了Claude Sonnet 4支持，今年的Xcode 26.3更是集成了原生Claude Agent SDK。

Claude Code在苹果内部早就不是什么「外部工具」了。

它像.gitignore一样自然，自然到没人觉得需要在打包前专门清理它。

599美元Mac mini没了

都怪AI太火

同一周，苹果做了一件过去十年几乎没做过的事，涨价。

Mac mini起售价从599美元一步跳到799美元，涨幅超过33%。

苹果的操作方式很苹果，直接砍掉搭载M4芯片和256GB存储的入门款，连涨价的姿势都省了。

想买Mac mini？最低配就是512GB起步，799美元，不接受还价。

库克在5月1日的财报电话会上给出了解释。

产能瓶颈主要受限于生产我们SoC芯片的先进工艺节点供不应求。

但这只是供给侧的故事。需求侧的故事更有意思。

Mac mini和Mac Studio是运行AI和AI Agent工具的绝佳平台，消费者对此的认知速度超出了我们的预期，因此我们看到了比预期更旺盛的需求。

库克说的「AI Agent工具」，具体是什么？

答案几乎可以锁定一个名字，OpenClaw。

今年1月，OpenClaw病毒式爆红后，开发者们突然发现，Mac mini是部署7×24小时AI Agent的完美硬件。

原因很简单。

Mac mini待机功耗只有15瓦，满载AI推理也就30瓦，一年电费不到15美元，完全静音。

部上本地模型，再把OpenClaw连上社交平台，它就是一台全天候在线的私人AI Agent工厂。

买一次，此后每月推理成本趋近于零。

如今，这台小方盒子承载的已经远远超出了苹果的产品定义。

它是OpenClaw的宿主、Ollama的推理引擎、Claude Code的开发终端、LM Studio的模型管理器。

开发者们把它塞进书架、数据柜、甚至衣橱里，让它安静地替自己工作。

在如此庞大的AI需求下，它早已不再只是一台电脑。

参考资料：

https://x.com/aaronp613/status/2049986504617820551

https://x.com/aaronp613/status/2050154318934712525

https://news.ycombinator.com/item?id=47973378

https://www.bloomberg.com/news/articles/2026-05-01/apple-raises-mac-mini-s-starting-price-to-799-after-ai-frenzy-drains-supply

秒追ASI

⭐点赞、转发、在看一键三连⭐

点亮星标，锁定新智元极速推送！