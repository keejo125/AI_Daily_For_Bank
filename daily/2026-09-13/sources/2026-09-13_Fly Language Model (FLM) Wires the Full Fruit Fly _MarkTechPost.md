---
publish_time: 1789239084
link: https://www.marktechpost.com/2026/09/12/fly-language-model-flm-wires-the-full-fruit-fly-connectome-into-a-frozen-1-2b-llm-and-its-own-controls-show-the-wiring-does-not-help/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  开发者发布 Fly Language Model（FLM），号称世界首个『果蝇语言模型』：将完整雄性果蝇脑连接组（MaleCNS v1.0，166,700 节点、25,582,938 条有向边）耦合到冻结的 LiquidAI LFM2.5-1.2B-Instruct 骨干，架构名为 GPF（Generative Pre-trained Fly）。系统本质是在语言模型上嫁接一个储层计算机：图、骨干与随机投影全部固定，仅训练约 27.8 万参数的读出层（占骨干 0.024%）。作者坦言，去掉果蝇连接组的参数匹配对照模型表现反而略好，并明确否认自己是首个连接组语言模型。项目以 MIT 许可开源，可本地运行（macOS/Linux，MPS/CUDA/CPU，无需 API key）。
---

# 果蝇语言模型 FLM：将完整果蝇连接组接入 1.2B 冻结 LLM

> 原文链接：https://www.marktechpost.com/2026/09/12/fly-language-model-flm-wires-the-full-fruit-fly-connectome-into-a-frozen-1-2b-llm-and-its-own-controls-show-the-wiring-does-not-help/
> 来源：MarkTechPost

The Fly Language Model (FLM) is a public chatbot that couples the complete retained MaleCNS v1.0 fruit fly connectome to a frozen LiquidAI LFM2.5-1.2B-Instruct backbone. The developer who created the FLM calls it the world&#8217;s first Fly Language Model, built on an architecture called GPF (Generative Pre-trained Fly). It does not use the GPF label, explicitly disclaims being the first connectome language model, and reports that a parameter-matched control without the fly graph performs slightly better.

Deployable: Yes, locally. The nftechie/flm repo is MIT-licensed and runs on Python 3.12 (macOS or Linux, MPS, CUDA, or CPU) with no API key. 

What was actually built

The system is a reservoir computer bolted onto a language model. All 166,700 retained nodes and 25,582,938 directed edges of the MaleCNS graph participate. The graph, the backbone, and the random input and output projections are all fixed. Only a 278,528-parameter readout is trained, which is about 0.0238% of the 1,170,340,608 backbone parameters.

At each token, a fixed Gaussian projection compresses the 2,048-dimensional token embedding to 128 channels. Each reservoir node receives one channel with a random sign. The whole graph then updates with x = tanh(W(0.6x + 0.4Bc)), where W holds incoming-normalized anatomical contact counts. States are pooled into 128 bins, passed through two trained bias-free matrices (U at 128 by 128, V at 2,048 by 128), and projected through the frozen vocabulary head as a bounded residual added to the backbone logits. The residual is capped at an RMS of 0.25 across vocabulary coordinates.

The results

On a freshly frozen set of 32 SmolTalk everyday-conversation dialogues (1,236 target tokens), three fit seeds gave:

ConditionNLL (nats/token)Frozen backbone1.381995Fly readout1.359816 ± 0.000110Direct-input readout1.359328 ± 0.000108Relabeled, no refit1.381265 ± 0.000802No edges1.381995

The fly readout improved on the backbone by 0.0222 nats per token (perplexity 3.98 to 3.90). But a direct-input control, which feeds the same 128-channel token projection straight into an identical readout with no graph, did better in all 3 seeds by 0.000488 nats per token. The paired bootstrap interval (+0.00000502 to +0.00104) does not support a fly-specific gain.

Two other controls matter. Setting W to zero removes the residual exactly, reproducing the backbone&#8217;s per-token losses, so the graph verifiably participates. Relabeling node identities without retraining returns NLL near baseline, which shows the readout depends on its learned interface alignment, not that fly topology beats random wiring.

The research report also proves the recurrence contracts initial-state differences by at most 0.6 per token. After 10 tokens that bound is 0.00605; after 20 it is 0.0000366. Piling in 166,700 cells does not buy long memory. Context still comes from the backbone.

Prior work and the &#8216;first&#8217; claim

The research report cites ngxson/fly-hf, an earlier prototype that used a 49,393-cell central-brain subset of MaleCNS as a reservoir trained on TinyStories without a pretrained backbone, and states plainly that it makes no claim to be the first connectome-based language model. FLM&#8217;s distinction is scale (the full retained graph) and the frozen-backbone design that keeps the source of language competence identifiable.

Interactive explainer

&&

Key Takeaways

Full 166,700-node fly connectome drives a frozen LFM2.5-1.2B; only 278,528 parameters train.

Fly readout cuts NLL by 0.0222 nats/token, but a no-graph control beats it in every seed.

Disconnection zeroes the residual exactly; relabeling breaks it. The graph participates, it does not win.

State forgets at 0.6 per token, so the connectome adds no long-range memory.

MIT code runs locally on Python 3.12; study artifacts stay private, so results are not independently reproducible yet.

Check out the Paper, GitHub repo, and live demo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Fly Language Model (FLM) Wires the Full Fruit Fly Connectome Into a Frozen 1.2B LLM, and Its Own Controls Show the Wiring Does Not Help appeared first on MarkTechPost.