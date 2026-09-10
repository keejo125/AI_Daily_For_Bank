---
publish_time: 1786525320
status: confirmed
category: 国内
is_model_related: false
digest: |
  Qoder CLI 手机遥控有两种玩法：远程控制模式，任务中途离开时用 /remote-control 把当前任务同步到手机远程遥控；守护进程模式，先在终端敲 qodercn remote-control 让整台电脑待命，随时从手机端发起新任务。

  连接方式支持手机扫码、复制 URL 浏览器打开、或 Qoder 移动端 App（同账号登录）三种。App 还支持实时活动与灵动岛，需审批操作时通知即时推送。CN 版命令为 qodercn，国际版将 qodercn 换成 qoder，其余一致。
link: https://mp.weixin.qq.com/s/vF-5G7PNkEnYeUsdwA51jQ
source: Qoder
title: 简单两个命令，用手机遥控 Qoder CLI 干活儿
---

# 简单两个命令，用手机遥控 Qoder CLI 干活儿

来源：Qoder
原文链接：https://mp.weixin.qq.com/s/vF-5G7PNkEnYeUsdwA51jQ

上周我在 Qoder CLI 里布置了一个任务，跑到一半，饭点到了。
以前这种时候，要么我盯着它跑完，要么人虽然走了，心还挂着。
这次我开了 Qoder CLI 的手机遥控,直接下楼吃饭去了,拿着手机实时看进展。
Qoder CLI 手机遥控有两种玩法：
远程控制模式：
任务中途临时离开，把手头这个任务用 /remote-control 同步到手机上远程遥控。
守护进程模式：
先在终端敲 qodercn remote-control 让整台电脑待命，随时从手机端发起新任务。
注意：本文以 Qoder CN 为例，如果你用的是国际版，把 qodercn 换成 qoder，其余一致。
临时离开 远程控制模式
跑任务中途需要离开电脑，任务不用暂停。
在
Qoder CLI 里输入 /remote-control。
随后，终端会给出两种连接手机的方式。
方式一：用手机扫码，或复制 URL 在浏览器中打开即可连接。
好处是不需要下载任何APP
方式二：使用 Qoder 移动端打开
如果你手机上装了 Qoder 移动端，并用 CLI 的同一个账号登录，打开 App 就能看到电脑上正在跑的任务，点进去就能远程遥控它。
App 还支持实时活动（Live Activity）和灵动岛，需要你批操作时，通知会立刻推过来，手机自动锁屏也不怕。
任务收尾，在 CLI 里敲 /remote-control stop 就能断开。
Qoder 移动端安装注意：
如果你用的是 Qoder CLI 的中国版（带CN标识），在应用市场搜索「Qoder CN」下载安装即可
如果你用的是 Qoder CLI 的国际版，需要去海外区 App Store 或 Google Play 下载国际版 App「Qoder」。
Qoder 国内版和国际版的账号互不相通，电脑上用哪套 CLI，手机就得装对应的那个版本。例如我用的是 Qoder CN CLI，手机上装的就是 Qoder CN。
电脑待命 守护进程模式
出门不想带电脑，又想让电脑继续干活。
在终端 cd 到你要干活的项目目录，敲一句 qodercn remote-control
（1.1.18 之前的老版本敲 qoderclicn remote-control）
这时候打开 App 就能看到已经连接上电脑了。
点左下角加号新建任务，输入框上方能选这个任务交给谁跑，默认是云端，你把它切成「Qoder CN CLI」，任务就派到你出门前待命的那台电脑上了。还可以多个任务并行。
产出的成果手机 App 或者浏览器打开就能看，而且所有生成的文件都会保存在运行 CLI 的电脑上。
回到电脑前不需要手机遥控了，终端里按 Ctrl+C 退出就行。
两种模式的区别：
前一种把某一个正在跑的会话遥控权交给手机。
后一种把整台电脑设成待命的接活口，手机想派几个派几个。
但它们都有个共同前提是电脑得醒着，一旦合盖休眠，手机这头就断了。
写在最后
这么用过一次，最明显的变化是我不用守在电脑前了。Agent 在电脑上一直干活，我在路上，它需要一个决定的时候我再出现一下。
已经在用 Qoder CLI 的，现在在会话里敲一下 /remote-control 就能试。
还没上手的，去 Qoder 官网 用一行命令装好 CLI，再下载好 Qoder CN 移动端，同一个账号登录就能使用。
