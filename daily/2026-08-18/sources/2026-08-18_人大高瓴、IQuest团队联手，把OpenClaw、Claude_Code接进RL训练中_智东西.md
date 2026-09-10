---
publish_time: 1787047405
status: confirmed
category: 国内
is_model_related: false
digest: |
  中国人民大学高瓴人工智能学院、至知创新研究院（IQuest）团队提出面向复杂 Agent Harness 的黑盒强化学习框架 ClawGym II，并已开源。与 Part I 用 Harness 交互数据训练模型不同，ClawGym II 直接将 Claude Code、OpenClaw 等真实 Harness 纳入 RL 闭环——无需改动其内部实现，仅通过模型服务边界（Serving Proxy）捕获调用、结合 Verifier 奖励优化底层策略。核心技术：①Sandbox 隔离执行与优化解耦；②基于前缀树的轨迹重建（合并公共前缀、保留分叉分支、过滤 dead leaves）；③GRPO/PPO 适配一对多树状轨迹 + Token-in-Token-out 与 importance-sampling 修正 off-policy 偏差；④Mix-Harness Training 让多异构 Harness 的 rollout 联合训练同一共享策略。以 Qwen3-30B-A3B 为骨干，在 ClawGym-Bench 上 OpenClaw/Claude Code 分别提升9.98/14.81分，PinchBench 提升11.71/17.28分，并迁移到 JobBench、OfficeQA。
link: https://mp.weixin.qq.com/s/ZrJ8jCs3VX0ngLROxUmJdw
source: 智东西
title: 人大高瓴、IQuest团队联手，把OpenClaw、Claude Code接进RL训练中

---

# 人大高瓴、IQuest团队联手，把OpenClaw、Claude Code接进RL训练中

