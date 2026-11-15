---
publish_time: 1790837870
link: https://www.marktechpost.com/2026/09/30/nvidia-releases-kumo-tabular/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  英伟达发布表格基础模型 Kumo Tabular（Small/Medium/Large，约 2800 万至 2.15 亿参数），面向分类与回归：以标注行作上下文，单次前向即可预测新行，无需训练、调参或特征工程。模型基于表结构 Transformer（列/行/上下文注意力），完全在合成表格（结构因果模型采样）上预训练，通过 GPU 原生 SDM 库（Apache-2.0）运行，权重采用 OpenMDW-1.1 许可可商用。官方称在 TabArena 综合第一（Elo 1950），单卡较 LimiX-2 快 17 倍；与 TabPFN-3、LimiX-2、TabFM 的非商用权重相比，其商用许可是主要差异点。
---

# 英伟达发布 Kumo Tabular 表格基础模型：单次前向即可预测新行

> 原文链接：https://www.marktechpost.com/2026/09/30/nvidia-releases-kumo-tabular/
> 来源：MarkTechPost

NVIDIA has released Kumo Tabular, a new family of tabular foundation models (TFMs) for classification and regression. If you have followed TabPFN or TabICL, the setup will look familiar. The model takes labeled rows as context and predicts new rows in one forward pass. There is no training, no hyperparameter tuning, and no feature engineering.

Kumo Tabular comes in Small, Medium, and Large versions, spanning about 28M to 215M parameters. It runs through NVIDIA&#8217;s open-source structured-data-models (SDM) library.

Is it deployable? Yes. Weights ship under the OpenMDW-1.1 license, which permits commercial use. The SDM code is Apache-2.0, and it needs Python 3.11+ and PyTorch 2.7+, with examples targeting a CUDA GPU.

What the SDM Library Adds

SDM is a GPU-native library for structured-data foundation models and preprocessing. Besides Kumo Tabular, it ships TabICLv2, Google&#8217;s TabFM, and KumoRelational for multi-table data. All models share one in-context learning interface built on a TableTensor container. The library also handles preprocessing, ensembling, and many-class prediction.

How Kumo Tabular Works

Kumo Tabular is a Transformer built around the structure of a table. It uses column, row, and in-context attention, as introduced in TabICL and TabPFN. The pipeline has 3 stages:

Cell embedding: Numerical and categorical values pass through learned Fourier features, with separate weights per type. Missing values need no imputation.

Row embedding: Column attention uses induced self-attention, so cost grows linearly with rows. Row attention, with rotary positions, learns feature interactions. 4 learnable [CLS] tokens compress each row.

In-context learning: A final Transformer runs over row embeddings. Context rows attend to each other, while query rows attend only to context rows.

Because the context never sees the queries, its keys and values are computed once and reused. The head outputs class probabilities, or 999 quantiles for regression. That gives a point prediction plus an uncertainty estimate.

One more detail matters at scale. Softmax attention spreads thin as the number of keys grows. Kumo Tabular scales each query by a temperature that grows with the log of the key count. The coefficient is learned per attention head, so attention stays sharp on larger tables.

&&

Trained Only on Artificial Tables

Kumo Tabular is pretrained entirely on synthetic tables sampled from Structural Causal Models (SCMs). A random causal graph links hidden variables through linear maps, small neural networks, trees, or Gaussian processes. The generator also injects messy, real-world patterns: missing values, high-cardinality categories, heavy-tailed targets, and conflicting duplicate rows.

Training ran in 3 stages, similar to TabICLv2. Context grew from 1,024 rows to 60,000 rows, with up to 100 columns. Small, Medium, and Large saw about 35M, 71M, and 137M artificial tables. Classification and regression are trained as separate models. NVIDIA says the training recipe and data generators will be released soon.

Benchmarks

With default settings, Kumo Tabular ranks first overall on TabArena with an Elo of 1950. NVIDIA team reports it runs 17x faster than LimiX-2 on a single RTX 6000 Pro. All 3 sizes sit on the accuracy and inference-time Pareto front.

BeyondArena: First place, with an Elo of 1418 and an Improvability score of 7.78%.

TALENT: Top overall ranking, with average ranks of 6.67 (accuracy), 3.98 (log-loss), and 4.22 (RMSE).

ScoringBench: Large and Medium rank first and second on average rank.

Kumo Tabular vs Its Closest Competitors

FeatureKumo TabularTabICLv2TabPFN-3LimiX-2TabFMDeveloperNVIDIAInria SODAPrior LabsStable AIGoogle ResearchParameters~28M to 215M (3 sizes)27.55M (cls), 28.54M (reg)Not listed in docs400M~1.64BTasksClassification, regressionClassification, regressionClassification, regressionClassification, regression, imputationClassification, regressionNative classes per pass10 (ECOC for more)10 (hierarchical for more)160Not specified10 (hard limit)Weights licenseOpenMDW-1.1BSD-3-ClauseTABPFN-3 License v1.0StableAI LimiX Non-CommercialTabFM Non-Commercial v1.0Commercial use of weightsYesYesPaid license requiredNoNoRuns in NVIDIA SDMYesYesNoNoYes

Sources: NVIDIA blog, SDM model docs, Prior Labs docs, LimiX GitHub, TabICLv2 paper. Checked September 30, 2026.

The license row is the real differentiator. TabPFN-3, LimiX-2, and TabFM weights carry non-commercial terms. Kumo Tabular and TabICLv2 are the permissive options, and Kumo Tabular leads the benchmarks NVIDIA reports.

Getting Started

Install the library and pass a DataFrame through TableTensor, following the model card:

Copy CodeCopiedUse a different Browser

# pip install structured-data-models
from sklearn.datasets import load_breast_cancer
import sdm

df = load_breast_cancer(as_frame=True).frame
table = sdm.TableTensor.from_pandas(
    df=df,
    stypes=sdm.infer_stypes(df, overrides={"target": "categorical"}),
    device="cuda",
)
model = sdm.models.KumoTabular(task="classification", device="cuda")
probs = model(
    x_context=table[:300].drop_columns("target"),
    y_context=table[:300, "target"],
    x_query=table[300:].drop_columns("target"),
    num_estimators=8,
)

The size argument accepts "small", "medium", or "large", and defaults to large.

Key Takeaways

NVIDIA&#8217;s Kumo Tabular predicts new table rows in 1 forward pass, with no training.

3 sizes span about 28M to 215M parameters, pretrained only on synthetic tables.

NVIDIA reports first place on TabArena (Elo 1950), BeyondArena, TALENT, and ScoringBench.

OpenMDW-1.1 weights allow commercial use, unlike TabPFN-3, LimiX-2, and TabFM.

It runs through NVIDIA&#8217;s GPU-native SDM library alongside TabICLv2, TabFM, and KumoRelational.

Check out the Model on HF, GitHub Repo and Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Releases Kumo Tabular: Open Tabular Foundation Models That Predict New Rows in a Single Forward Pass appeared first on MarkTechPost.