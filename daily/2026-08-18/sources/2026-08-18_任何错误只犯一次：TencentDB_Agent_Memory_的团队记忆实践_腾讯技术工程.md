---
publish_time: 1787045760
status: confirmed
category: 国内
is_model_related: false
digest: |
  文章介绍 TencentDB Agent Memory 的团队记忆工程实践，核心是用“协作带宽”（单位时间内在正确权限边界下被相关人/Agent 正确理解并直接用于任务的有效上下文）替代单纯消息量。产品将记忆分为四类资产：Chat Memory（L0原始对话→L1原子事实→L2场景→L3画像/Persona 分层）、Wiki、CodeGraph、Skill，按“身份与作用域→固定绑定→浮动召回(BM25+向量RRF融合)→上下文装配”逐层缩小边界后生成 Memory Pack，框架中立、资产跟 Team 走。内部数据：分析2600个 Session、5081个 Task、2203个卡点（逻辑返工1350最多）；访谈7位研发。评测上，SWE-bench 相关 Case 加入团队记忆后完成率从60%提升到80%（+20pp），Top50超长难任务成本降19%同时成功率提升。结论是团队记忆本质是一套带版本/权限/冲突/生命周期治理的系统。
link: https://mp.weixin.qq.com/s/-ghlUNmB8HvzX9cFYXlDKg
source: 腾讯技术工程
title: 任何错误只犯一次：TencentDB Agent Memory 的团队记忆实践

---

# 任何错误只犯一次：TencentDB Agent Memory 的团队记忆实践

