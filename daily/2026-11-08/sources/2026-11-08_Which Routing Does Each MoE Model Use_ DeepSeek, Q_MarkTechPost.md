---
publish_time: 1794133647
link: https://www.marktechpost.com/2026/11/08/moe-model-routing-comparison/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  本文横向对比 10 个开源 MoE 模型的路由细节：总/激活参数从 Qwen3.6-35B-A3B（35B/3B）到 DeepSeek-V4-Pro（1.6T/49B），专家数 8 到 384，Top-k 1 到 8，部分模型保留常驻共享专家。DeepSeek 系列用 Sigmoid 评分加无辅助损失偏置，Kimi K2、GLM-4.5 同属此类；Mixtral、gpt-oss、Qwen3 用 Softmax Top-k。数据均取自各模型 Hugging Face config.json 与技术报告（2026-11-07 核验）。结论：config 让路由完全可审计，但“17B 激活”这类名字掩盖了截然不同的路由器。
---

# 各 MoE 模型用哪种路由？DeepSeek、Qwen、Mixtral、Llama 4、gpt-oss 对比

> 原文链接：https://www.marktechpost.com/2026/11/08/moe-model-routing-comparison/
> 来源：MarkTechPost

Open Mixture-of-Experts (MoE) models share one idea but disagree on almost every routing detail. Expert counts range from 8 to 384. Top-k ranges from 1 to 8. Some models keep an always-on shared expert; others drop it. 

TL;DR

Size: 10 models, from Qwen3.6-35B-A3B (35B total, 3B active) to DeepSeek-V4-Pro (1.6T total, 49B active).

Runs on: gpt-oss-120b fits one 80 GB GPU with MXFP4; DeepSeek-V4-Pro and Kimi K2 need multi-GPU expert parallelism.

Performance: Routed sparsity spans 4x in Mixtral (8 experts, top-2) to 128x in Llama 4 Maverick (128, top-1).

Best: Kimi K2 found sparsity 48 needed 1.69x fewer FLOPs than sparsity 8 at equal validation loss.

Worst: Llama 4 Maverick and gpt-oss do not publish their gating or balancing method in config.json.

Bottom line: Best thing: configs make routing fully auditable. Worst thing: names like &#8220;17B active&#8221; hide very different routers.

How do open MoE models route tokens?

Every model below uses token-choice routing: each token selects its own experts. They differ on 5 knobs. These are expert count, experts per token, shared experts, the scoring function and the load-balancing method. The table lists each knob per model.

MoE routing comparison table (November 2026)

ModelTotal / active paramsRouted expertsTop-kShared expertsGatingLoad balancingMixtral 8x7B47B / 13B820Softmax over top-kAux loss, coef 0.02 (config)gpt-oss-120b117B / 5.1B12840Softmax over selectedNot disclosedQwen3-235B-A22B235B / 22B12880Softmax, top-k normalizedGlobal-batch aux loss, coef 0.001Qwen3.6-35B-A3B35B / 3B25681Not disclosedAux loss, coef 0.001 (config)Llama 4 Maverick400B / 17B12811Not disclosedNot disclosedDeepSeek-V3671B / 37B25681SigmoidAux-loss-free bias (noaux_tc)DeepSeek-V4-Pro1.6T / 49B38461sqrtsoftplusnoaux_tc; hash routing in 3 layersDeepSeek-V4-Flash284B / 13B25661sqrtsoftplusnoaux_tc; hash routing in 3 layersKimi K21.04T / 32B38481Sigmoidnoaux_tc + sequence aux, alpha 0.001GLM-4.5355B / 32B16081SigmoidLoss-free balance routing

Sources: each model&#8217;s Hugging Face config.json, model card or technical report, verified November 7, 2026. Configs and cards for Qwen3.6 and Llama 4 omit gating. gpt-oss and Llama 4 omit the balancing method. 

&&

How does DeepSeek-V3 routing work?

DeepSeek-V3 scores 256 routed experts with a sigmoid, then normalizes the selected scores. A per-expert bias steers the top-8 selection without touching the mixing weights. Experts sit in 8 groups, and the router keeps 4 groups first. Each token reaches at most 4 nodes, according to the technical report. One shared expert runs for every token.

What changed in DeepSeek-V4 routing?

DeepSeek-V4 raises Pro to 384 routed experts but lowers top-k from 8 to 6. The score function becomes sqrtsoftplus. The first 3 MoE layers use hash routing, a fixed token-to-expert map. Bias-based noaux_tc balancing stays.

How many experts does Qwen3 MoE use?

Both original Qwen3 MoE models use 128 experts and route each token to 8. Qwen3 dropped the shared experts of Qwen2.5-MoE and adopted a global-batch balancing loss. Qwen3.6-35B-A3B changes course: 256 experts, 8 routed plus 1 shared, per its model card.

How does Llama 4 Maverick routing differ?

Llama 4 Maverick alternates dense and MoE layers. In each MoE layer, a token goes to 1 shared expert and 1 of 128 routed experts. That top-1 design echoes the Switch Transformer. It keeps 17B active parameters despite 400B in total.

How does gpt-oss route tokens?

gpt-oss-120b uses a linear router over 128 experts and keeps the top 4. Its config lists no shared expert. Its MoE weights ship in MXFP4, which lets the 117B model fit on a single 80 GB GPU.

Why do Kimi K2 and GLM-4.5 look like DeepSeek-V3?

Kimi K2 ships with the DeepseekV3ForCausalLM architecture class and the noaux_tc router. It raises routed experts to 384 at the same top-8. The Kimi K2 report found that higher sparsity lowered loss at fixed active compute. GLM-4.5 chose 160 experts and more layers instead, favoring depth over width.

What the trend means for serving

More experts per layer means more weights resident in memory and more all-to-all traffic. Lower top-k, as in DeepSeek-V4, trims per-token compute and communication. Shared experts add a dense path that every token pays for. Check these fields before sizing GPUs for any MoE deployment.

Key Takeaways

Expert counts grew from 8 (Mixtral) to 384 (Kimi K2, DeepSeek-V4-Pro).

Top-k now spans 1 (Llama 4) to 8 (DeepSeek-V3, Qwen3, Kimi K2, GLM-4.5).

7 of 10 models keep 1 shared expert; Mixtral, gpt-oss and Qwen3 do not.

Sigmoid or sqrtsoftplus with bias balancing is the DeepSeek-family standard.

Llama 4 and gpt-oss leave gating or balancing details unpublished.

Model sources: DeepSeek-V4-Pro, DeepSeek-V3 report, Qwen3 report, Kimi K2 report, GLM-4.5 report, Mixtral paper. Also see gpt-oss-120b and the Llama 4 announcement. 

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Which Routing Does Each MoE Model Use? DeepSeek, Qwen, Mixtral, Llama 4, gpt-oss Compared appeared first on MarkTechPost.