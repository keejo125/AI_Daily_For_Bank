---
publish_time: 1788278054
link: https://www.marktechpost.com/2026/09/01/aqua-a-two-part-agentic-framework-for-autonomous-factor-discovery/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  普林斯顿、蚂蚁集团与斯坦福联合提出 AQuA——一个用于量化金融中自主因子发现与模型开发的双部分智能体框架。研究指出，自行编写实验的量化研究 Agent 可能污染其后续学习的证据：表现良好的「泄漏特征」会被存为成功先例并不断传播。AQuA 通过提示级指令与评审 Agent 等机制缓解证据污染，提升量化研究中智能体实验的可靠性，展示 Agent 在金融建模中的自主化潜力。
---

# 普林斯顿、蚂蚁集团与斯坦福联合提出 AQuA：量化金融自主因子发现与建模智能体框架

> 原文链接：https://www.marktechpost.com/2026/09/01/aqua-a-two-part-agentic-framework-for-autonomous-factor-discovery/
> 来源：MarkTechPost

Quantitative research agents that write their own experiments can corrupt the evidence they later learn from. A leaky feature that scores well gets stored as a successful precedent and propagated through later iterations. Prompt-level instructions and reviewer agents do not close this, because author and reviewer share the same blind spots. A team of researchers from Princeton University, Ant Group and Stanford University propose AQuA. AQuA is a pair of language-model-driven research systems that improve their own research process across iterations while the thing judging them stays frozen. One discovers symbolic alpha factors on crypto; the other develops time-series models on US equities. They share no agents, memories, candidate spaces or research state.

The failure mode AQuA is built around

Quantitative research breaks on small methodological errors that produce convincing but non-reproducible backtests, documented since Bailey et al.. An agent writing its own experiments makes this worse: a leaky feature that scores well gets stored as precedent, and recursion amplifies an undetected bug as readily as a real discovery.

Prompt-level instructions and model review are not an integrity boundary. Repeated access to a fixed holdout causes adaptive overfitting, and LLM agents have been observed exploiting misspecified objectives and evaluators. AQuA instead makes leakage-inducing actions unavailable. Each part fixes its splits, feature and label definitions and evaluator before any iteration starts, and the agent emits only a constrained factor expression or a single config diff. The research team call this asymmetric freedom: the agent explores freely inside its DSL, but the evaluator sits outside the adaptive surface. What improves is the research process.

Interactive explainer

&&

Part I: Manager-Mediated Factor Discovery

Part I is a six-agent pipeline: Data Steward, Visual Analyst, Idea Miner, Factor Evaluator, Backtest Engineer and Research Librarian — orchestrated by an AI Manager. Agents never call one another; every handoff goes through the Manager, keeping runs auditable.

A factor enters as a falsifiable proposal, not an expression: hypothesis, mechanism, predicted direction, and refutation conditions. Only then is it assembled from the standard formulaic-alpha operator registry. Because every time-series operator reads only a trailing window and every cross-sectional operator reads only the current timestamp, causality is closed under composition. Three feedback loops run: direction calibration inside a backtest, falsification-driven belief update inside a run, and cross-run memory that steers the next search.

On a crypto five-minute universe the combined validation Spearman IC climbs across 20 research epochs to approximately 0.190, against 0.171 for an adapted AlphaMemo, 0.151 for an adapted AlphaGen, 0.137 for LSTM, 0.106 for LightGBM and 0.075 for an Alpha158-style baseline. Individual mechanisms stay weak — single-factor ICs of 0.026 to 0.037. The claim is about the harness, not one expression.

Part II: Config-Driven Model Development

Part II predicts each stock&#8217;s forward return over the next thirty minutes on intraday US equities. Training runs on 2010–2019, 2020 is an embargo gap nothing touches, and 2021–2025 is untouched test data. Selection uses an inner-validation slice from the end of the training window only.

A hypothesis here is one config diff — architecture, loss, sampler or optimizer — and one diff produces exactly one variant, keeping variants comparable. The predictor is a hybrid: a multi-scale 1-D convolutional front-end, a configurable backbone spanning LSTM, Mamba and attention (attention in the reported run), a cross-sectional stage that mixes across the panel, gated fusion and a pooled per-stock readout.

No single price-volume feature carries the signal: the strongest is a 5-minute return at −0.031, and a ridge combination reaches only +0.025. Across model families on identical data and the same evaluator, per-stock raw IC runs +0.0251 (ridge), +0.0397 (LGB), +0.0434 (xLSTM), +0.0535 (LSTM), +0.0613 (GRU) and +0.0843 for the hybrid — +0.0230 absolute over the best baseline, 37.5% relative. The two parts&#8217; ICs use different conventions and the paper states plainly they should not be compared.

From Signal to Strategy

The per-stock score becomes a dollar-neutral threshold long/short book at a two-leg cost of 2 bps. Sector-neutralizing raises the held-out Sharpe to +2.15, with training and held-out values nearly equal. A causal volatility-targeting overlay lifts it to +2.50, and a fully causal walk-forward choosing every parameter from past data alone still reaches +2.00. Per-stock R² is 1.20%. Sharpe by year runs +1.7, +3.5, +1.9, +1.8 and +2.7 for 2021 through 2025 — positive in every year, including the 2022 drawdown.

Key Takeaways

Two independent research loops: factor discovery and model development, share no agents, memory or state.

Freedom is asymmetric: the agent explores inside a DSL, but splits, features, labels and evaluator are sealed.

Part I hits ~0.190 combined IC on crypto; Part II hits +0.0843 per-stock IC versus +0.0613 for a GRU.

The equity book holds a +2.50 Sharpe at 2 bps and is positive in all five years, 2021–2025.

Check out the Paper. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

Note:Thanks to the Ant Research team for the thought leadership/ Resources for this article. Ant Research team has supported this content/article for promotion.

The post Researchers from Princeton, Ant Group and Stanford Introduce AQuA: A Two-Part Agentic Framework for Autonomous Factor Discovery and Model Development in Quantitative Finance appeared first on MarkTechPost.