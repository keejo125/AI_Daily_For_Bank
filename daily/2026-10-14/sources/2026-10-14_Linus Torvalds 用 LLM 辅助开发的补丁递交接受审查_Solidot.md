---
publish_time: 1791990888
link: https://www.solidot.org/story?sid=85612
source: Solidot
status: confirmed
category: 国际
is_model_related: false
digest: |
  Linux作者Linus Torvalds在维护者峰会上透露，他在大模型帮助下开发了一组解决长期问题的补丁，共10个已递交审查。补丁增强folio查找机制：标记热数据folio延迟释放至RCU周期结束，在RCU保护下完成查找与数据访问，测试中性能实现数量级提升，但已发现竞态条件需完善。
---

# Linus Torvalds 用 LLM 辅助开发的补丁递交接受审查
> 原文链接：https://www.solidot.org/story?sid=85612
> 来源：Solidot

至顶科技：
至顶网
科技行者
Solidot
登录
注册
文章
往日文章
往日投票
皮肤
蓝色
橙色
绿色
浅绿色
关注我们：
solidot新版网站常见问题，请点击
这里
查看。
消息
本文已被查看 1261 次
Linus Torvalds 用 LLM 辅助开发的补丁递交接受审查
Edwards
(42866)发表于 2026年10月14日 23时14分 星期三
新浪微博分享
来自异形：悲伤之海
Linux 作者 Linus Torvalds 在维护者峰会上透露他在大模型帮助下开发了一系列补丁解决一个长期存在的问题。现在这组 10 个补丁已递交接受审查。这些补丁主要增强 folio 的查找机制：通过识别处于热数据状态的 folio，设置一个“延迟释放该 folio 直至 RCU 周期结束”的标志。随后利用 RCU 延迟在 RCU 保护下进行常规的 folio 查找，同时在 RCU 保护下直接进行实际的 folio 数据访问...补丁在测试中性能实现了数量级的提升，但已发现存在竞态条件，因此需要进一步完善。
https://lwn.net/Articles/1100449/
回复
﻿
只有两种编程语言：一种是天天挨骂的，另一种是没人用--Bjarne Stroustrup
首页
至顶网
往日文章
过去的投票
编辑介绍
隐私政策
使用条款
网站介绍
RSS
本站提到的所有注册商标属于他们各自的所有人所有，评论属于其发表者所有，其余内容版权属于 solidot.org(2009-
) 所有 。
京ICP证161336号
京ICP备15039648号-15
北京市公安局海淀分局备案号：11010802021500
举报电话：010-62641205　涉未成年人举报专线：010-62641208 举报邮箱：jubao@zhiding.cn　网上有害信息举报专区：
https://www.12377.cn