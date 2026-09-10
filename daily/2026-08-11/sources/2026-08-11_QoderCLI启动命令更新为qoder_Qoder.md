---
publish_time: 1786420890
status: deleted
reason: 纯产品版本更新公告，非技术内容
category: 国内
digest: |
link: https://mp.weixin.qq.com/s/61xDGLkdk3vXht2rNH_lQg
source: Qoder
title: Qoder CLI 启动命令更新为 qoder
---

# Qoder CLI 启动命令更新为 qoder

来源：Qoder
原文链接：https://mp.weixin.qq.com/s/61xDGLkdk3vXht2rNH_lQg

为了优化产品使用体验，从V1.1.18版本开始，在终端直接输入 qoder 即可启动 Qoder CLI，原有的 qodercli 命令仍可使用。本次更新同样适用于 Qoder CN，输入 qodercn 即可启动 Qoder CN CLI，原有的 qoderclicn 命令继续保留。本次修改仅涉及启动命令，不会影响具体功能。
命令使用说明
注意事项：
对于运行 qodercli update 升级的用户：升级完成后，需再启动一次 qodercli，配置方可完成。如果 qoder 命令仍不可用，可运行 qodercli configure-path 修复。
常见问题
输入 qoder，打开的是 IDE 而不是 CLI。
见于同时安装了 IDE、且升级后尚未启动过新版 qodercli 的情况。解决方法：启动一次 qodercli 并退出，新开终端窗口即可恢复；若仍未生效，运行 qodercli configure-path 修复。
只安装了 CLI，没有安装 IDE。
运行 qoder desktop 时会提示 IDE 未安装，并给出下载地址。CLI 功能不受影响。
只安装了 IDE，没有安装 CLI。
qoder 命令的行为保持不变，仍打开 IDE；安装 CLI 之后，qoder 默认进入 CLI。
如在使用中遇到问题，欢迎通过 /feedback 向我们反馈。
关于 Qoder CLI
Qoder CLI 是支撑整个 Qoder 产品家族的内核，同时也是一个可以在终端里工作的 AI 编程智能体：把任务交给它，它会自己读代码、改文件、执行命令、验证结果，直到任务完成。
此外，这一套Agent Harness 能力，不只在终端可用：它可以以非交互模式（headless）接入 CI/CD 流水线，也可通过 SDK 供企业集成、开发自己的 Agent 应用。目前，Qoder Agent SDK 国内版与国际版均已上线，开发文档（点击阅读原文）👉：SDK 文档。
