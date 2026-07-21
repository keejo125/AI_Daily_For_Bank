---
publish_time: 1784620800
---

# 我用 Qoder CLI + 49k star 的tldraw，让 AI 直接在画板上做动画

> 原文链接：https://mp.weixin.qq.com/s/DBUNrNUu5q3sdyOOmWRpbg
> 公众号：Qoder

本周最值得关注的 AI 工具，是 tldraw offline —— 一款对 AI 极度友好的绘图工具。

它是一款以本地文件为核心、完全离线运行、并支持 AI 脚本扩展的桌面端无限画板应用。

核心特性：

完全本地优先：无需账户系统，所有数据保存在本地 .tldraw 文件中，整个应用离线可用，零网络依赖。

文件即作品：每个文件自包含画布图形、嵌入的图片、视频及自定义脚本，可自由备份、私有保存或分享。

关键机制与AI集成：

脚本执行需授权：文档可嵌入脚本为画布添加动态行为，但运行前会明确征求用户同意，确保安全可控。

AI 协作基础：脚本嵌入机制使「回写」（writeback）成为可能——AI 的交互逻辑保存在画板文件中，并随文件一同传播。

兼容多种 AI 代理：支持 Qoder 等 AI 代理「查看」文档，直接在编辑器中修改，并编写可复用脚本扩展画布功能。

本文以 Qoder CLI 为例，演示用Qoder CLI 在tldraw offline 生成动画的完整流程。

安装 Qoder CLI 和 tldraw offline

访问 https://qoder.com/zh/cli ，根据操作系统选择对应版本安装 Qoder CLI。

访问 https://offline.tldraw.com/ ，下载对应系统的 tldraw offline 安装包并安装，也可以直接让 Qoder CLI 帮你完成。

安装 tldraw-offline SKILL

让 qoder cli 帮你安装 tldraw-offline SKILL，它返回了详细的步骤。

按照 Qoder CLI 的指引，先在 tldraw offline 新建一个文件，点击「Develop」菜单，选择 Install Agent Skills 即可。

接下来需要在 Qoder CLI 中安装 tldraw-offline SKILL，建议直接让 Qoder CLI 帮你完成。

也可以使用如下命令安装：

mkdir

-p

$HOME

/.qoder/skills

cp

-r

$HOME

/skills/tldraw-offline

$HOME

/.qoder/skills

创建第一个tldraw动画

回到命令行，创建新目录（如 tldraw-demo）或使用已有项目目录，按 Shift+Tab 切换到 Qoder CLI 的 YOLO 模式。由于 tldraw offline 涉及大量 shell 脚本交互，切换到 YOLO 模式可跳过所有确认提示，提升效率。

输入：

使用 tldraw-offline skill 创建一个 "Java G1GC的工作原理动画"

。等待 3-5 分钟，Qoder CLI 与 tldraw offline 完成交互后，动画创作即告完成。最终效果如下：

当然，真实样例是带有动画效果的，这里仅展示截屏。

上图使用的模型为 Ultra 极致模式，所有 Qoder 注册用户730前均可免费领取 200 次极致调用额度。你也可以直接用 Qwen 3.8-Max-Preview 生成，效果与 Ultra 相差无几。在与 tldraw offline 交互的过程中涉及大量命令行操作，可以看出 Qwen 3.8 在指令遵循方面表现非常出色。

多说一句，Qwen 3.8-Max-Preview 现在使用起来非常便宜，白天1折，夜间0.2折，真的是量大管饱！

日常工作中涉及线框图、示意图、基础动画等场景时，Qoder CLI +tldraw offline + 是一个值得尝试的组合。打开 tldraw 时思路尚未成型，也可以快速唤出 Qoder CLI 协助构思图示，效率很高。