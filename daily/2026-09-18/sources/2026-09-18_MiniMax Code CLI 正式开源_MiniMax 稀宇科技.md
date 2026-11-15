---
publish_time: 1789734313
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/aZTOlQUnULqptBgGGKZXEg
source: MiniMax 稀宇科技
title: MiniMax Code CLI 正式开源
---

# MiniMax Code CLI 正式开源

来源：MiniMax 稀宇科技
原文链接：https://mp.weixin.qq.com/s/aZTOlQUnULqptBgGGKZXEg

今天，MiniMax Code CLI 的 v0.4.12 版本面向全球开发者正式开放，并且以 MIT 协议正式开放源代码。
MiniMax Code CLI 是 MiniMax Code 客户端的核心组件。在基于 FrontierHarness Eval 的本轮评测中，取得了 76.7% 的任务通过率，成功任务耗时中位数为 4 分 33 秒，两项指标均优于报告所列公开基线。我们希望通过优秀的 harness 设计，持续释放模型能力，缩短任务等待时间。
*1
我们希望通过开源，让开发者能够审视工具调用和权限处理，构建可靠的企业级应用。也让社区参与发现问题、贡献修复。让使用更放心，让安全机制在实际使用和审查中持续完善。
快速体验：
curl -fsSL https://filecdn.minimax.chat/public/install.sh | bash
Github 源码：
https://gi
thub.com/MiniMax-AI/minimax-code
客户端下载：
https://ag
ent.minimax.cn/download
MiniMax Code 仍然在高速迭代中，我们愿和社区共建安全、可靠、高性能的 harness，持续释放模型的智能水平。
Intelligence with Everyone.
备注：
FrontierHarness Eval：https://github.com/frontier-harness-eval/eval
本轮使用 MiniMax Code 0.3.2 与 FrontierHarness Eval 默认的 Kimi K3 模型，共评测 30 道任务，其中 23 道通过、4 道未通过、3 道超时未评分；通过率按全部 30 道计算。结果为第三方评测，供应商、checkpoint 方式及部分任务时限口径与公开基线存在差异，仅作数值比较，不代表官方榜单排名
评测结果：https://github.com/frontier-harness-eval/eval/pull/13
运行轨迹：https://file.cdn.minimax.io/public/FrontierHarness-Eval-mcode.zip
适配配置：https://github.com/frontier-harness-eval/eval/pull/14
