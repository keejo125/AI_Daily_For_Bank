---
publish_time: 1792372697
link: https://www.marktechpost.com/2026/10/18/mistral-timestral-time-series-foundation-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Mistral AI 发布 Timestral，其首个时间序列基础模型家族，包含 5M 至 209M 参数的 4 个零样本预测模型。最大检查点在 GIFT-Eval、TIME 与 fev-bench 等基准上，于预训练零样本模型中排名第一，且推理无需 GPU。对开发者而言，Timestral 把时间序列预测从“需训练专属模型”变为“开箱即用的基础模型”，可应用于需求预测、运维监测等场景，降低时序预测门槛。这是大模型厂商向纵向专业基础模型（forecast foundation model）拓展的又一动作。
---

# Mistral 发布 Timestral：209M 参数时序预测基础模型家族

> 原文链接：https://www.marktechpost.com/2026/10/18/mistral-timestral-time-series-foundation-model/
> 来源：MarkTechPost

Mistral AI has released Timestral, its first family of time series foundation models. Timestral is a set of 4 zero-shot forecasting models from Mistral AI, sized from 5M to 209M parameters. The largest checkpoint ranks first among pretrained, zero-shot models on GIFT-Eval, TIME and fev-bench. It does this without a GPU at inference. For developers, this Timestral time series foundation model means probabilistic forecasts on standard server CPUs, with open weights and inference code.

TL;DR

Size: 4 models: 5M, 28M, 123M, 209M parameters (dense). Context up to 32,768 time steps.

Runs on: Standard server CPU, no GPU needed. 209M weights are 837 MB in fp32. GPU optional.

Performance: #1 among zero-shot pretrained models on GIFT-Eval, TIME and fev-bench (Mistral-reported).

Best: fev-bench SQL skill score of 50.39, ahead of TimesFM-3 at 48.99.

Worst: GIFT-Eval MASE of 0.658 leads t0-gamma (0.661) by only 0.003.

What is Timestral?

Timestral is a time series foundation model (TSFM). It is pretrained on a large, diverse corpus, then forecasts zero-shot on data it has never seen. Classical tools like ARIMA fit one series at a time. Deep models like PatchTST usually train from scratch on each dataset. Timestral transfers patterns across domains instead.

Each model outputs 21 quantiles per time step. It forecasts multivariate targets jointly. It accepts past-only, known-future and categorical covariates.

How does Timestral work?

Timestral is a causal, patch-based transformer with time attention and variate attention. The 209M model uses 24 layers and an embedding dimension of 768. Each patch covers 32 time steps. A single forward pass forecasts up to 1,024 steps. Longer horizons run block by block, feeding each block&#8217;s median back as context.

Mistral lists 4 technical contributions:

Decoupled Horizon Forecasting (DHF): Learned forecast tokens read the full history. Observed values stay in context instead of being masked, unlike contiguous patch masking in Toto 2.0 and TimesFM-3.

Covariate-aware attention: Each series is a target, past-only covariate or known-future covariate. Information flows only from covariates to targets, preventing future leakage.

Synthetic-first data: Most training data is synthetic, with trends, seasonality, noise and nonlinear cross-series dependencies.

Two-stage training: Pretraining on synthetic data at context 8,192, then post-training on mixed data with 4x longer context. The loss is pinball loss over 21 quantiles.

&&

How does Timestral perform on benchmarks?

All scores below are zero-shot, from a single checkpoint without ensembling. They come from the Timestral-209M model card.

GIFT-Eval: MASE 0.658, CRPS 0.446 (lower is better).

TIME: MASE 0.626, CRPS 0.522 (lower is better).

fev-bench: SQL skill score 50.39, MASE skill score 39.49 (higher is better).

The size scaling is flat at the top. Timestral-123M scores 0.659 MASE on GIFT-Eval, against 0.658 for 209M. Mistral team states that the 28M model beats Chronos-2 on GIFT-Eval and TIME. Chronos-2 is about 4 times larger.

How fast is Timestral on CPU?

Mistral team tested a standard server CPU with 8 threads. The task: forecast 1 day ahead from 3 weeks of 15-minute history. The 5M model took 10 ms and the 209M model took 140 ms. The 28M model is 5 times faster than 209M. The 123M model lands within 0.2% of the 209M score at three quarters of its latency.

How does Timestral compare with TimesFM-3, Chronos-2 and Toto 2.0?

FeatureTimestral-209MTimesFM-3Chronos-2Toto-2.0-2.5BDeveloperMistral AIGoogle ResearchAmazonDatadogParameters209M330M120M2.5BArchitectureCausal patch transformer, DHFDecoder-only, contiguous patch maskingEncoder-only, group attentionDecoder-only, contiguous patch maskingMax context32,768 stepsNot disclosed8,192 stepsNot disclosedSingle-pass horizon1,024 stepsNot disclosed1,024 steps (max)Not disclosedQuantiles219Not disclosed9Weights licenceModified MITNon-commercial v1.0Apache 2.0Apache 2.0Weights (fp32)837 MBNot disclosedNot disclosed9.1 GBGIFT-Eval MASE / CRPS0.658 / 0.4460.667 / 0.456*0.698 / 0.485*0.696 / 0.476TIME MASE / CRPS0.626 / 0.5220.640 / 0.536*0.662 / 0.556*0.640 / 0.532**fev-bench SQL skill50.3948.99*47.28*44.42*

* As listed on the Timestral-209M model card. Google and Amazon do not publish matching figures on their own model pages. ** From Datadog&#8217;s model card. Mistral&#8217;s card lists 0.642 / 0.539.

How can developers deploy Timestral?

Install the package with pip install git+https://github.com/mistralai/timestral.git. It needs Python 3.10+ and torch 2.4+. Dependencies are PyTorch, NumPy, safetensors and huggingface_hub. Weights download from Hugging Face: 21 MB for 5M, 111 MB for 28M, 490 MB for 123M.

Mistral&#8217;s docs list Timestral 1.0 209M as Public Preview. Fine-tuning on proprietary data runs through Mistral Forge. The pipeline can deploy on-prem, in a VPC or air-gapped.

Key Takeaways

4 sizes, 5M to 209M, all on the accuracy-vs-size Pareto front.

209M leads GIFT-Eval, TIME and fev-bench among zero-shot models.

CPU-only inference: 10 ms (5M) to 140 ms (209M).

32,768-step context, 21 quantiles, native covariate support.

Modified MIT weights, unlike TimesFM-3&#8217;s non-commercial licence.

Check out the blog post, GitHub repo and model weights on Hugging Face. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Mistral AI Releases Timestral: A 209M Forecasting Model Family That Outperforms Google’s TimesFM-3 appeared first on MarkTechPost.