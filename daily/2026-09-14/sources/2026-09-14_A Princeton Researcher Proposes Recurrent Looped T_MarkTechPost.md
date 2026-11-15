---
publish_time: 1789318946
link: https://www.marktechpost.com/2026/09/13/a-princeton-researcher-proposes-recurrent-looped-transformer-rlt/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  普林斯顿研究者 Yifan Zhang 的技术报告提出循环回路 Transformer（Recurrent Looped Transformer, RLT），尝试闭合大多数 decoder-only 模型中被打断的状态传递：将解码器最终隐状态与逐层滑动窗口注意力（SWA）缓存跨令牌、跨提示与回复边界持续携带，不重置。RLT 以因果编码器配对循环解码器，完整状态含最终输出与各级 SWA 键值，门控融合编码器表示与历史输出。报告明确为架构设计规范，定义了执行调度与 RL 回放契约，但明示未给出效率、推理质量或扩展性的实测结果。
---

# 普林斯顿提出循环回路Transformer（RLT）：跨令牌传递解码器状态，实现无界时间深度

> 原文链接：https://www.marktechpost.com/2026/09/13/a-princeton-researcher-proposes-recurrent-looped-transformer-rlt/
> 来源：MarkTechPost

In most decoder-only LLMs, nothing computed at the last layer of token t feeds the first layer of token t+1; positions communicate only through attention over cached keys and values. A Princeton researcher&#8217;s (Yifan Zhang) technical report, Recurrent Looped Transformer (RLT), proposes closing that loop. The decoder&#8217;s final hidden state and its layerwise sliding-window attention (SWA) cache are carried into the next token, across both prompt and response, with no reset at the boundary. The proposed research is a design specification. It defines the architecture, execution schedules, and RL replay contract, and it explicitly reports no measured efficiency, reasoning quality, or scaling results.

How RLT is Built

Recurrent Looped Transformer (RLT) pairs a causal encoder with a recurrent decoder. The encoder processes tokens in parallel under a causal mask and produces representations e_t, from which key-value memory M≤t is projected; memory groups can be shared across decoder layers (G = 1) or kept layer-specific (G = L_D).

The decoder holds the recurrence. Its complete state is Ht = (st, CtD), where st is the final decoder output and CtD holds the retained SWA keys and values at every decoder layer. For each token, a gated merge combines et with the previous output s{t-1}, then each decoder block runs causal SWA over decoder activations, cross-attention to encoder memory, and an FFN. The window W includes the current token, so at most W &#8211; 1 historical entries per layer are retained. The next-token distribution is read from st, and initialization happens once before BOS with a learned start state s* and an empty cache.

The reference tied configuration uses 48 encoder and 48 decoder layers with compatible attention and FFN weights shared between them. Each token therefore executes 96 logical blocks, though decoder blocks add cross-attention, so per-block FLOPs are not equal. Zhang calls this parameter reuse, not activation copying.

The 3 Design Principles

Latent reasoning with unbounded temporal depth: After t processed tokens, the state path from s0 traverses t·LD decoder blocks, or 48t in the reference configuration. Per-token work stays fixed while the path&#8217;s structural depth grows with the sequence. The research report warns that gates and contraction may suppress long paths; structural depth is not a reasoning guarantee.

Model-hardware co-design: Encoder features and memory projections for known tokens use token-parallel kernels. Decoder transitions stay sequential within a sequence, but ready updates from independent sequences can share one batched kernel. The report states plainly that no exact parallel scan is assumed for the nonlinear decoder, no reduced-prefill speedup is claimed, and a standard parallel SWA decoder pass is not equivalent to the recurrence. Batching, kernel fusion, and checkpointing are listed as implementation targets, not completed kernels.

Model-RL algorithm co-design: Pretraining, SFT, sampling, and RL replay share one state transition. For RL, the sampler records each action&#8217;s behavior log-probability under its actual sampling distribution, including temperature and truncation. The trainer rebuilds encoder memory, the recurrent output, and every SWA cache from the sequence start under current parameters before scoring each action; old rollout states are never reused. Proposition 3.1 formalizes the payoff: moving the prompt-response split leaves the conditional distribution unchanged for a fixed token history.

Training and Serving

Pretraining is full-sequence next-token prediction with full backpropagation through time. SFT masks the loss to assistant targets but never masks state updates, so assistant losses backpropagate through user and tool tokens. Appendix B shows why partial detaching is risky: the state-to-state Jacobian has cross terms through decoder KV, so detaching only st leaves gradient paths through the cache; any truncated-BPTT scheme must name every detached tensor.

For multi-turn serving, an exact prefix snapshot includes encoder cache and memory, the complete decoder state, position metadata, the window convention, and model version. A fixed-weight snapshot can be reused because the state is independent of the serving split; weight updates invalidate old states, and editing a prefix forces recomputation from an earlier checkpoint. External tokens in multi-turn RL update the state but get no importance-ratio factors.

How It Relates to Prior Work

Encoder-derived memory follows YOCO, which caches KV once for a cross-decoder, and DeepSeek-V4.1-Flash, which projects decoder global KV from final encoder states; RLT keeps the memory but drops prompt-wide decoder skipping. Temporal feedback builds on Feedback Transformer and Recurrent Transformer; RLT instead feeds the previous final decoder output into the next decoder input and runs recurrence over the prompt too. Depth-wise reuse connects to Universal Transformers and recurrent-depth latent reasoning; the replay argument extends Zhang&#8217;s prefill-decode kernel mismatch note.

Interactive Explainer

&&&

Key Takeaways

RLT carries the full decoder state (final output plus layerwise SWA cache) across every prompt and response token with no boundary reset.

Reference config: 48 tied encoder and decoder layers, 96 logical blocks per token, state path of 48t blocks after t tokens.

Hardware opportunities: encoder parallelism and batching across sequences; no parallel scan or reduced-prefill speedup is claimed.

RL replay rebuilds all states under current parameters while keeping recorded behavior log-probabilities as ratio denominators.

No measured results: reasoning quality, efficiency, and RL scaling remain open validation targets.

Check out the Technical Report, GitHub repository, and Project Page. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post A Princeton Researcher Proposes Recurrent Looped Transformer (RLT) that Carries Decoder State across Every Token, Fixing 96 Blocks per Token with Unbounded Temporal Depth appeared first on MarkTechPost.