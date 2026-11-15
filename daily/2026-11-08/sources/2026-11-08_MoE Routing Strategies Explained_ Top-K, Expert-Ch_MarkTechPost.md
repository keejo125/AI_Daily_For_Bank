---
publish_time: 1794118713
link: https://www.marktechpost.com/2026/11/07/moe-routing-strategies-explained/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  每个 MoE 模型对每个 token 都要做一次路由决策：哪些专家处理它。本文详解生产中使用的 7 种路由策略，专家数从 Mixtral 的 8 个到 DeepSeek-V4-Pro 的 384 个，每 token 激活 1 至 8 个。要点：Softmax Top-K（Mixtral、Qwen3 等）、Top-1 开关路由（Switch、Llama 4）、共享+路由专家（DeepSeekMoE、Kimi K2、GLM-4.5）。2026 年主流方案是 Sigmoid 评分配无辅助损失偏置均衡，在 1B 规模将 MaxVio 从 0.72 降到 0.04 且困惑度更低；但专家选择在因果模型中会泄露未来 token。
---

# MoE 路由策略详解：Top-K、专家选择、Sigmoid 门控与动态路由（2026 指南）

> 原文链接：https://www.marktechpost.com/2026/11/07/moe-routing-strategies-explained/
> 来源：MarkTechPost

Every Mixture-of-Experts (MoE) model repeats one decision for every token: which experts should process it. That decision belongs to the router. MoE routing strategies shape quality, load balance and serving cost in every major open model. This guide explains the 7 routing strategies used in production, and the models that use each one.

TL;DR

Size: Routers choose from 8 experts (Mixtral) to 384 (DeepSeek-V4-Pro), activating 1 to 8 per token.

Runs on: Routing cost shows up in multi-GPU expert parallelism, where each choice becomes all-to-all network traffic.

Performance: Sigmoid scoring with aux-loss-free bias balancing is the dominant 2026 recipe for frontier open MoE models.

Best: Loss-free balancing cut MaxVio from 0.72 to 0.04 at 1B, with lower perplexity.

Worst: Expert choice leaks future tokens in causal models; one test showed a roughly 10% abnormal loss drop.

Bottom line: Best thing: bias-based balancing adds no interfering gradients. Worst thing: no router removes the need for serving-time load fixes.

What is MoE routing?

MoE routing is the mechanism that sends each token to a small subset of expert networks. A router scores every expert, keeps the top candidates and weights their outputs. Only the selected experts run. Mixtral 8x7B, for example, gives each token access to 47B parameters but uses 13B active parameters.

video created by marktechpost.com

The 7 MoE routing strategies used in production

1. Softmax top-k token choice

Each token scores all experts with a linear layer and keeps the k highest. A softmax over those k scores sets the mixing weights. Mixtral picks 2 of 8 experts. gpt-oss-120b picks 4 of 128. Qwen3-235B-A22B picks 8 of 128. An auxiliary loss usually keeps expert load even.

Used by: Mixtral, gpt-oss, Qwen3.

2. Top-1 switch routing with a capacity factor

Switch Transformer showed that routing each token to 1 expert preserves quality and cuts router compute. Each expert gets a fixed buffer: tokens per batch divided by experts, times a capacity factor. Overflow tokens skip the layer through the residual connection. Llama 4 Maverick also sends each token to 1 routed expert, plus a shared expert.

Used by: Switch Transformer, Llama 4 Maverick (with a shared expert).

3. Shared plus routed experts

DeepSeekMoE splits each layer into always-on shared experts and sparsely routed experts. The shared expert captures common knowledge, so routed experts can specialize. DeepSeek-V3 uses 1 shared and 256 routed experts, activating 8. Kimi K2, GLM-4.5 and Qwen3.6-35B-A3B follow the same pattern. Qwen3 went the other way and removed shared experts.

Used by: DeepSeek-V3 and V4, Kimi K2, GLM-4.5, Qwen3.6, Llama 4.

4. Sigmoid gating with aux-loss-free bias

DeepSeek-V3 scores experts with a sigmoid instead of a softmax. It adds a per-expert bias only when choosing the top-k. After each step, the bias drops for overloaded experts and rises for idle ones. Mixing weights still come from the raw scores. GLM-4.5 uses loss-free balance routing with sigmoid gates. DeepSeek-V4 switches the score to sqrtsoftplus but keeps bias balancing.

Used by: DeepSeek-V3, DeepSeek-V4, GLM-4.5, Kimi K2.

5. Group-limited and node-limited routing

Sending one token to experts on many nodes is expensive. DeepSeek-V3 caps each token at 4 nodes, chosen by their highest affinity scores. Its config splits experts into 8 groups and keeps 4 before the final top-8 pick. DeepSeek says this cap lets training nearly fully overlap computation and communication. Kimi K2 drops grouping entirely, with n_group set to 1.

Used by: DeepSeek-V2 and V3.

6. Expert choice routing

Google&#8217;s expert choice routing flips the direction. Each expert picks its top-k tokens, so every expert gets a fixed bucket size. Tokens can receive a variable number of experts. The paper reports more than 2x faster training convergence. The catch is causality: a token&#8217;s expert can depend on later tokens. DeepSeek researchers measured an abnormal loss drop of about 10% from this leakage.

Used by: Research and non-causal settings. None of the 10 models in our companion table uses it.

7. Hash routing and dynamic top-k

Hash routing assigns experts from the token ID, with no learned router. DeepSeek-V4 uses hash routing in its first 3 MoE layers. Dynamic top-k lets the number of active experts vary per token. SMIDT built it into SGLang and improved P99 time-to-first-token by 1.21 to 1.26x.

Used by: DeepSeek-V4 (hash routing), research serving systems (dynamic top-k).

MoE routing strategies compared

StrategyWho choosesHow load is balancedMain riskUsed bySoftmax top-kToken picks k expertsAuxiliary lossLoss trades off qualityMixtral, gpt-oss, Qwen3Top-1 switchToken picks 1 expertAux loss + capacity factorDropped overflow tokensSwitch, Llama 4 MaverickShared + routedToken picks routed; shared always runsInherits routed methodExtra always-on computeDeepSeek, Kimi K2, GLM-4.5, Qwen3.6Sigmoid + biasToken picks via biased scorePer-expert bias, no loss gradientImbalance inside one sequenceDeepSeek-V3/V4, GLM-4.5, Kimi K2Node-limitedToken picks within capped nodesInherits routed methodRestricts expert choiceDeepSeek-V2/V3Expert choiceExpert picks k tokensFixed by constructionFuture-token leakageResearch modelsHash / dynamicToken ID or variable kFixed mapping or adaptive kLess learned specializationDeepSeek-V4, SMIDT

&&

Which MoE routing strategy should you use?

Most teams do not pick a router. They inherit one when they choose a checkpoint. Before serving, read 4 fields in config.json: expert count, experts per token, shared experts and topk_method. Changing top-k at inference changes the model itself, so treat it as a quality experiment. For new pretraining runs, sigmoid scoring with bias balancing is the current open default.

Key Takeaways

Top-k token choice is the baseline; k ranges from 1 (Llama 4) to 8 (DeepSeek-V3, Qwen3).

Shared experts are standard in DeepSeek, Kimi, GLM and Qwen3.6; Qwen3 dropped them.

Sigmoid plus bias balancing is the 2026 default for frontier open MoE models.

Expert choice balances perfectly but leaks future tokens in causal LLMs.

DeepSeek-V4 adds hash routing to its first 3 MoE layers.

Check out the primary sources: Switch Transformer, Expert Choice, Loss-Free Balancing, DeepSeek-V3 report and the DeepSeek-V4 model card. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post MoE Routing Strategies Explained: Top-K, Expert-Choice, Sigmoid Gating and Dynamic Routing (2026 Guide) appeared first on MarkTechPost.