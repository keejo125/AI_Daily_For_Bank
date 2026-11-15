---
publish_time: 1789534787
link: https://www.marktechpost.com/2026/09/15/nums-ai-releases-causilo-a-tabular-foundation-model-that-tops-tabarena-among-single-models/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Nums AI 发布表格基础模型 Causilo，面向分类与回归的预训练模型，提供 scikit-learn 接口、Apache-2.0 代码与 Hugging Face 预训练权重。在 TabArena 上，其分类与回归的单模型 Elo 均居首。该模型面向研究与评估可部署，瞄准结构化数据这一传统机器学习长期主导、大模型尚未完全接管的应用场景。
---

# Nums AI 发布表格基础模型 Causilo，单模型登顶 TabArena

> 原文链接：https://www.marktechpost.com/2026/09/15/nums-ai-releases-causilo-a-tabular-foundation-model-that-tops-tabarena-among-single-models/
> 来源：MarkTechPost

Nums AI has released Causilo, a pretrained tabular foundation model for classification and regression. Causilo comes with a scikit-learn interface, Apache-2.0 code and pretrained weights on Hugging Face. On TabArena, it has the highest Elo among single models for both classification and regression.

Is it deployable? Yes, for research and evaluation today, on CUDA or CPU. Commercial, production and hosted API use need a separate license from Nums AI.

What Causilo Does

Causilo is an in-context learning model. Calling fit does not update the pretrained weights. It stores the training rows as context and predicts query rows in one forward pass. According to its TabArena submission, Nums AI pretrained Causilo only on synthetic data, with no TabArena datasets.

Inputs can be NumPy arrays or pandas DataFrames, including categorical features and missing values. Classification supports up to 10 classes. Regression returns mean predictions by default. Version 1.0.1 adds median and quantile outputs, based on 999 native quantiles.

Architecture: Refinement, Compression, In-Context Learning

Nums AI splits the network into 3 phases: refinement, compression and in-context learning. The released code and configs show how each phase works.

Features are grouped in sets of 3. Each value is embedded with 16 learned sine and cosine frequencies. Missing values get their own learned vector.

2 column stages summarize each feature group. In each, 128 latent slots read only the training rows and pass that summary to every row. Between the 2 column stages, a row stage lets feature groups interact through 4 latent tokens. It uses cross-attention instead of full self-attention, which Nums AI says keeps cost linear in feature count.

A pooling block then compresses each row into a fixed 512-dimensional vector. Labels are added to the training rows. A 12-layer prediction block lets query rows attend to those labeled rows. Query rows cannot change the training context or each other.

By default, 8 ensemble members share the same weights. Each one cycles through none, rank2gaussian, robust or power normalization, with seeded feature and class permutations.

TabArena Results

Nums AI used the official TabArena pipeline: 51 datasets and 816 Full splits, with 8 estimators and seed 42. A TabArena maintainer re-ran the full evaluation and got the same overall Elo of 1794.

TaskCausilo EloNext best single modelCausilo improvabilityOverall1792.9TabFM, 1764.40.0684Classification1771.8EXAONE Tabular, 1758.80.0875Regression2032.6TabFM, 1992.80.0125

The field includes Google Research&#8217;s TabFM, LG AI Research&#8217;s EXAONE Tabular and Prior Labs&#8217; TabPFN-3 (1636.2 overall).

A few points help when reading these numbers:

The #1 positions exclude system entries. With systems included, the maintainer re-run placed Causilo 3rd of 88 overall.

On improvability, TabFM still leads overall and on classification. Causilo leads on regression.

The Elo confidence intervals at the top overlap, so the lead over TabFM and EXAONE Tabular is narrow.

Nums AI also lists Xiaomi-TabLDM and Amazon&#8217;s Mitra-v2 behind Causilo. Neither model appears in the benchmark files in Causilo&#8217;s repo.

ScoringBench Results

ScoringBench scores regression models with proper scoring rules such as CRPS, alongside RMSE and R². Nums AI submitted Causilo 1.0.1 on 101 datasets, 5 folds each, capped at 3,000 samples. Nums AI reports that Causilo ranks 1st by CRPS, R² and RMSE. The ScoringBench maintainer independently checked the results before committing them.

Speed and Memory

Nums AI also reran 3 models on 1 H100 80 GB GPU, with 8 CPU cores per job.

ModelFit (s per 1k rows)Predict (s per 1k rows)GPU memory (GiB)Causilo2.5040.2518.15TabICLv23.4490.3038.37TabPFN-34.180.6860.88

In this test, Causilo is fastest on both fit and predict. TabPFN-3 uses far less GPU memory. Setting use_kv_cache=True moves context work into fit, using more memory to speed up repeated predictions.

Getting Started

Causilo needs Python 3.10 to 3.12 and PyTorch 2.13 or newer. The first fit downloads the checkpoint automatically.

Copy CodeCopiedUse a different Browser

# pip install causilo
from causilo import CausiloClassifier, CausiloRegressor

clf = CausiloClassifier(n_estimators=8, random_state=42)
clf.fit(X_train, y_train)
proba = clf.predict_proba(X_test)

reg = CausiloRegressor()
reg.fit(X_train, y_train)
bands = reg.predict(X_test, output_type="quantiles", quantiles=[0.05, 0.5, 0.95])

You can also try the Hugging Face demo Space.

&&&

Key Takeaways

Causilo has the top TabArena Elo among single models, overall and per task.

With system ensembles included, a maintainer re-run places it 3rd of 88.

Row mixing goes through 4 latent tokens, keeping cost linear in feature count.

The code is Apache-2.0; the weights are research-only without a commercial license.

Version 1.0.1 adds quantile outputs, so regression intervals work out of the box.

Check out the Repo on GitHub and Model on HF. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Nums AI Releases Causilo: A Tabular Foundation Model That Tops TabArena Among Single Models appeared first on MarkTechPost.