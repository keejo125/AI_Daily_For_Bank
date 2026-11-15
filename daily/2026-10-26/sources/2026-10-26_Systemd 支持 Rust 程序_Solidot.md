---
publish_time: 1793001743
link: https://www.solidot.org/story?sid=85710
source: Solidot
status: pending
---

# Systemd 支持 Rust 程序
> 原文链接：https://www.solidot.org/story?sid=85710
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
本文已被查看 2049 次
Systemd 支持 Rust 程序
Edwards
(42866)发表于 2026年10月26日 16时02分 星期一
新浪微博分享
来自白玫瑰
Systemd 支持用 Rust 语言开发程序。核心 systemd 代码如 systemd 库目前尚不支持 Rust 代码，但对于systemd 程序/末端组件已支持使用 Rust 语言。Systemd 开发者并不计划将现有的 C 代码移植到 Rust，所有 Rust 代码都是通过 Meson 构建的（不使用 Cargo），仅强制要求使用 C 语言链接。Systemd 的 Rust 组件体积比 C 语言略大，一个测试程序的体积为 32KB，而其 C 语言对应程序的体积为 20KB。目前 systemd 的 Rust 支持是可选的。
https://www.phoronix.com/news/systemd-Merges-Rust-Programs
回复
﻿
我注意过，即便是那些声称一切都是命中注定的而且我们无力改变的人，在过马路之前都会左右看。--史提芬·霍金
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