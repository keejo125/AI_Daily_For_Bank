---
publish_time: 1789744670
link: https://www.solidot.org/story?sid=85421
source: Solidot
status: confirmed
category: 国际
is_model_related: false
digest: |
  安全团队 Hacktron 组合利用 OpenAI 的 SSO 配置错误，及其社区论坛所用 Discourse 软件的 libheif 堆缓冲区溢出漏洞，控制了多名 OpenAI 员工的 ChatGPT 账户，进而访问内部代码库等关联服务，并向 OpenAI 报告漏洞、获 6500 美元赏金。过程中他们用 Anthropic 的 Claude（先 Opus 4.8、后 Opus 5.5）辅助发现 bug 并实现远程代码执行（RCE）。整个 AI 辅助的 bug 发现与攻击消耗 token 不到 3000 美元、耗时数天，而人工仅投入数小时，凸显 AI 时代攻击成本的低廉与安全边界的脆弱。
---

# 安全研究人员利用 Claude 成功入侵 OpenAI
> 原文链接：https://www.solidot.org/story?sid=85421
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
本文已被查看 1597 次
安全研究人员利用 Claude 成功入侵 OpenAI
Edwards
(42866)发表于 2026年09月18日 23时17分 星期五
新浪微博分享
来自我是6号
Hacktron 安全团队组合利用 OpenAI 的 SSO（单点登录）配置错误以及其社区论坛使用的 Discourse 软件 libheif 软件包堆缓冲区溢出漏洞，成功控制了多名 OpenAI 员工的 ChatGPT 账户。利用这些账户安全研究人员能访问 OpenAI 内部代码库，以及其他关联服务。他们向 OpenAI 和 Discourse 报告了 bug，从 OpenAI 获得了  6500 美元的赏金。安全研究人员利用了 OpenAI 竞争对手 Anthropic 的 Claude AI 工具去辅助发现 bug，以及实现远程代码执行 RCE。他们一开始使用的是较旧的模型 Opus 4.8，之后使用了新发布的 Opus 5.5。整个 AI 辅助 bug 发现和辅助攻击消耗的 token 支出不到 3000 美元，AI 智能体花费了数天时间，而研究人员投入的人工时间仅仅数小时，凸显了 AI 时代黑客攻击成本的低廉。
https://www.hacktron.ai/blog/hacking-openai
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