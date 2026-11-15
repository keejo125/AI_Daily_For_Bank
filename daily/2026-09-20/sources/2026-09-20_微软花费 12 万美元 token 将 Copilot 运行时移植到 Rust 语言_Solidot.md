---
publish_time: 1789916999
link: https://www.solidot.org/story?sid=85433
source: Solidot
status: confirmed
category: 国际
is_model_related: false
digest: |
  微软利用AI智能体，借助GPT-5.6 Sol与Claude Opus 4.8，历时14.5周、花费约12万美元token，将Copilot运行时从TypeScript移植到Rust语言。项目采用逐个更新运行时模块的方式推进，共进行了135次发布，平均每天约1.3个Pull Request。这一案例展示了大模型智能体在大型遗留代码库语言迁移中的实际工程价值：以可控的token成本完成系统性重构，也为“AI辅助大规模代码改造”提供了可参考的节奏与成本基准。
---

# 微软花费 12 万美元 token 将 Copilot 运行时移植到 Rust 语言
> 原文链接：https://www.solidot.org/story?sid=85433
> 来源：Solidot

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
本文已被查看 1200 次
微软花费 12 万美元 token 将 Copilot 运行时移植到 Rust 语言
Edwards
(42866)发表于 2026年09月20日 23时09分 星期日
新浪微博分享
来自白玫瑰
微软利用使用 GPT-5.6 Sol 和 Claude Opus 4.8 的 AI 智能体、历时  14.5 周，花费 12 万美元 token 将 Copilot 运行时从 TypeScript 语言移植到 Rust 语言。该项目采用逐个更新运行时模块的方式执行，共进行了 135 次发布，平均每天提交约 1.3 个 Pull Request，最终将 43 万行 TypeScript 代码转换为 80 万行可用于生产的 Rust 代码。测试显示，原 TypeScript 代码每秒能完成 7.55 个生命周期（one-turn session lifecycles），而 Rust 代码每秒 120 个——意味着在特定工作负载下速度提升了 15.9 倍。包含 10 个客户端的智能体在 TypeScript 语言下消耗了 1383 MB 内存，而 Rust 语言版本仅消耗了 126 MB。Rust 版本将任务保持在进程内执行，无需像 TypeScript 版本那样启动外部后台进程完成任务。
https://www.theregister.com/devops/2026/09/18/microsoft-agentically-ports-copilot-runtime-to-rust-for-120k/5297549
回复
﻿
具有新想法的人在其想法实现之前是个怪人。
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