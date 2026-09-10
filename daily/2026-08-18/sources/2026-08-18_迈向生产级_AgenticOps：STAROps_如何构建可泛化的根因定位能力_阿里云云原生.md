---
publish_time: 1787049000
status: confirmed
category: 国内
is_model_related: false
digest: |
  STAROps 是阿里云打造的下一代 AI 原生全域智能运维平台，文章聚焦其将“根因定位（RCA）”作为 AgenticOps 核心能力。关键设计：UModel（统一对象关系地图，避免同名对象被误判）、动态调查拓扑（记录调查过程与证据）、RCA-Bench/RCA-100（103个故障用例、6大类28种类型，约82%综合分由确定性规则计算，LLM只辅助判断方向）、线上 Bad Case 回归。评测用 RCA-100 的30个分层案例与 OpenClaw+DeepSeek-V4-Pro 对比，STAROps 综合分75.23 vs 51.02，根因实体90 vs 52.8，故障类型58 vs 33.3。两个典型案例（Node CPU高、inventory慢SQL）显示通用 ReAct/OpenClaw 易停在传播链中间，STAROps 因沿关系取证、多候选同置时间线收敛而得分94/84。结论：AgenticOps 能力差距将集中在判断质量（建立证据链、区分根因与伴随现象、证据不足时停下）。
link: https://mp.weixin.qq.com/s/KqwB4Kyn7Y1NgVHYa3faDA
source: 阿里云云原生
title: 迈向生产级 AgenticOps：STAROps 如何构建可泛化的根因定位能力

---

# 迈向生产级 AgenticOps：STAROps 如何构建可泛化的根因定位能力

