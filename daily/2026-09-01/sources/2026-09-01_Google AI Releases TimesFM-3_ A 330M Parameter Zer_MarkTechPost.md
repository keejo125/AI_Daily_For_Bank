---
publish_time: 1788211216
link: https://www.marktechpost.com/2026/08/31/google-ai-releases-timesfm-3-a-330m-parameter-zero-shot-foundation-model-for-multivariate-time-series-forecasting/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google Research 发布时序预测基础模型 TimesFM-3（3.3 亿参数），原生支持多变量预测，在单次前向传播中同时预测多个相关序列。此前 TimesFM 2.5 及以前均为单变量。TimesFM-3 在超 1 万亿时间点预训练，接受多目标、历史协变量与未来已知协变量输入，无需任务微调；采用连续分块掩码，一次前向生成整段预测并给出每步 9 个分位数。在 GIFT-Eval、fev-bench 与 TIME 榜单上均居预训练基础模型平均排名第一，权重仅限非商业非生产使用。
---

# 谷歌发布时序预测基础模型 TimesFM-3（3.3亿参数）

> 原文链接：https://www.marktechpost.com/2026/08/31/google-ai-releases-timesfm-3-a-330m-parameter-zero-shot-foundation-model-for-multivariate-time-series-forecasting/
> 来源：MarkTechPost

Google Research has released TimesFM-3, a 330 million parameter time series foundation model that forecasts multiple related series in a single forward pass. Every TimesFM checkpoint through 2.5 was univariate: one series, its own history, nothing else. TimesFM-3 is pretrained natively for multivariate forecasting on more than 1 trillion time points, and accepts multiple targets, past covariates, and past-future covariates with no task-specific fine-tuning. It takes the top average rank among pretrained foundation models on GIFT-Eval, fev-bench, and the TIME leaderboard, on both point and probabilistic metrics. 

https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/

Is it deployable?

Partial, the TimesFM repository code is Apache-2.0, but the TimesFM 3.0 weights ship under timesfm-non-commercial-license-v1.0. They are restricted to non-commercial, non-production use. You can benchmark it today. You cannot ship it behind a production forecast API.

What changed

Every TimesFM release through 2.5 was univariate. It forecast one series from its own history. Most real forecasting problems are not shaped that way. Google&#8217;s example is ice cream sales, where related product sales, foot traffic, weather, promotions, and holidays all move the target.

TimesFM-3 is pretrained natively for multivariate forecasting. It carries 330 million parameters and was pretrained on more than 1 trillion time points of real and synthetic series. Three input types work zero-shot, with no task-specific fine-tuning:

Multiple targets forecast jointly, with point and quantile outputs for each.

Past covariates, known only historically, such as past foot traffic.

Past-future covariates, whose future values are known, such as a promotion calendar.

Architecture: patches, then two kinds of attention

The backbone stays a decoder-only transformer. Contiguous points are grouped into patches of 32 steps, then normalized per series so that wildly different scales do not dominate. Target and past-covariate tokens come from a single patch. Past-future covariate tokens use a lookahead trick: the current patch is concatenated with future patches, so the model sees scheduled events before they occur.

Tokens then enter a 2D grid and pass through two alternating attention mechanisms:

Causal temporal attention runs horizontally. It is strictly causal and confined to earlier tokens inside the same series, which blocks leakage.

Full variate attention runs vertically. At a given time step, a token reads every other series at that step, learning cross-series correlations.

One forward pass instead of many

Earlier TimesFM versions decoded one patch at a time. That adds latency, compute cost, and compounding error. TimesFM-3 uses Contiguous Patch Masking, the training-time masking strategy introduced with TiRex. Masked placeholder tokens are appended for the whole horizon. Targets and past covariates are masked there. Past-future covariates stay visible, so known future signals still reach the model. The alternating attention layers fill every masked horizon patch simultaneously. Each target receives 9 quantiles, the 10th through 90th percentile, at every horizon step.

Benchmarks

Google evaluated on GIFT-Eval, fev-bench, and the TIME leaderboard, against Chronos-2, the Toto 2.0 family, and TimesFM-2.5. Among pretrained foundation models, TimesFM-3 takes the top average rank on all three, for both point and probabilistic metrics. The package release notes record rank #1 overall on fev-bench across 100 real-world tasks, rank #1 overall on TIME across 50 domain datasets and 98 evaluation tasks, and rank #1 among foundation models on GIFT-Eval.

Interactive explainer

&&

Key Takeaways

TimesFM-3 is a 330M parameter, natively multivariate time series foundation model, pretrained on 1T+ time points.

Alternating causal temporal and full variate attention lets it model cross-series dependencies zero-shot.

Contiguous Patch Masking produces the entire horizon in one forward pass, with 9 quantiles per step.

It ranks #1 among foundation models on GIFT-Eval, fev-bench, and TIME, in univariate and multivariate modes.

The weights are non-commercial and non-production only; TimesFM 2.5 remains the Apache-2.0 option for shipping.

Check out the Technical details, Model weights on Hugging Face, and the GitHub repo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google AI Releases TimesFM-3: A 330M Parameter Zero-Shot Foundation Model For Multivariate Time Series Forecasting appeared first on MarkTechPost.