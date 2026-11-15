---
publish_time: 1789025461
link: https://www.marktechpost.com/2026/09/10/deepseek-ai-released-deepseek-v4-1-flash-with-1m-context-fp4-kv-cache-and-cross-layer-attention-reuse/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  DeepSeek-V4.1-Flash 发布：支持 1M 上下文，采用 FP4 KV Cache 与跨层注意力复用（Cross-Layer Attention Reuse）以降低长上下文 Agent 场景的 HBM/SSD 压力，面向输入密集型负载优化推理成本。
---

# DeepSeek 发布 V4.1-Flash：1M 上下文、FP4 KV Cache 与跨层注意力复用

> 原文链接：https://www.marktechpost.com/2026/09/10/deepseek-ai-released-deepseek-v4-1-flash-with-1m-context-fp4-kv-cache-and-cross-layer-attention-reuse/
> 来源：MarkTechPost

Long-horizon agents have turned LLM serving into an input-heavy workload. Repeated prefills and million-token contexts leave KV caches that strain HBM, SSD capacity, and bandwidth. DeepSeek AI built its newest release around that exact bottleneck. DeepSeek-V4.1-Flash is a multimodal Mixture-of-Experts model with 552B backbone parameters, 196B additional Engram parameters, and a 1M-token context window. It activates 8B parameters per token during prefill and 16B during decode. The main number is a global KV cache footprint of 890 bytes per token, about 1/4 of DeepSeek-V4-Flash and roughly 437x smaller than DeepSeek-V1.

Is it deployable? Yes. Open weights ship under an MIT license with vLLM, SGLang, and Transformers paths on Hugging Face, and the research team describes a public API with low, high, and max reasoning tiers.

Causal Encoder-Decoder: Half the Prefill

The 40-layer backbone is split into a 20-layer causal encoder and a 20-layer decoder. Inspired by YOCO, the decoder does not compute its own global KV. Instead, per-layer projection weights derive it from the final encoder hidden state. Prompt tokens therefore stop at the encoder, which nearly halves prefill compute. Sliding-window attention (SWA) with a 128-token window still runs in every layer, so decoder SWA states are rebuilt by replaying only the last 128 prompt tokens. The research team calls this Decoder SWA Bounded Replay.

Compressed Sparse Attention 2 (CSA2)

DeepSeek-V4 mixed CSA with Heavily Compressed Attention. V4.1-Flash uses pure CSA2 and attacks cache size along the layer axis. Each CSA2 layer is statically assigned one of 3 modes:

Full: computes its own main KV, projects indexer K from it, and selects fresh Top-512 indices.

Reindex: reuses main KV and indexer K from the last Full layer but rescores them with its own indexer Q.

Reuse: reuses both the main KV and the latest Top-K indices, skipping the indexer entirely.

Every layer keeps its own main Q and SWA KV. The 18 CSA2 encoder layers use a compression ratio of 2 in 3 groups of 6 (1 Full, 5 Reuse). The 20 decoder layers use ratio 1 in 5 groups of 4: the first is Full plus 3 Reuse, the rest Reindex plus 3 Reuse. A Hierarchical Sparse Indexer in the decoder lets the Full layer build a candidate pool of up to 16,384 positions (2,048 blocks of 8), so later Reindex layers score a bounded set instead of the entire context.

FP4 KV, Bounded Replay, and Other Extensions

The main KV cache is quantized to E2M1 with one E4M3 scale per 16 channels, following NVFP4 without its global scale. This is introduced through quantization-aware training in post-training and nearly halves storage against V4&#8217;s FP8 cache.

At the deployment level, SWA KV is no longer persisted to SSD. It lives in a distributed pool carved from 10% of host DRAM with a TTL of minutes, while global KV keeps a guaranteed 72-hour lifetime. On a miss, Encoder SWA Bounded Replay recomputes only 128 tokens instead of layers times window.

Other changes include Single-Pass mHC, which shifts input-mixing coefficients by one block so a fused Mega-mHC kernel can halve activation memory traffic, the Engram conditional memory module at layers 1 and 14, DSpark speculative decoding trained after pre-training with the backbone frozen, and head-wise Muon. Single-token decode FLOPs rise by only 1/4 when context grows from 4K to 1M.

Training and Results

Pre-training covers 45T multimodal tokens at a 7:1 text-to-multimodal ratio. Sparse attention is trained from scratch at 64K sequence length with no dense warmup, and context is extended to 1M at 34T tokens. The base model matches DeepSeek-V4-Pro-Base on world knowledge and coding while using 1/3 of the total and 1/4 of the activated parameters.

Post-training introduces no new algorithms. Gains come from large-scale synthesis of verifiable agent tasks, RL across heterogeneous scaffolds (Claude Code, Codex, OpenCode, Pi, mini-SWE, DeepSeek Harness), and on-policy distillation from over 40 teachers. Selected max-effort results:

BenchmarkDS-V4.1-FlashDS-V4-FlashOpus-5GPT-5.6 SolTerminal-Bench 2.190.682.789.188.8DeepSWE v1.174.254.474.073.0Terminal-Bench 4.031.27.051.839.9Automation-Bench54.837.750.345.8GPQA Diamond90.989.993.494.1Codeforces (rating)34713289n/an/a

Interactive Explainer

&

Key Takeaways

Global KV cache falls to 890 bytes per token, about 1/4 of V4-Flash and 437x below V1.

CED runs only 20 encoder layers in prefill, activating 8B parameters against 16B in decode.

CSA2 shares main KV, indexer K, and Top-K indices across layers in Full, Reindex, and Reuse modes.

FP4 main KV plus SWA Bounded Replay cut persistent cache to about 1/8 of V4-Flash.

Beats Opus-5 and GPT-5.6 Sol on Terminal-Bench 2.1 and DeepSWE v1.1 with MIT weights.

Check out the Model on Hugging Face and the Technical Report. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post DeepSeek AI Released DeepSeek-V4.1-Flash with 1M Context, FP4 KV Cache, and Cross-Layer Attention Reuse appeared first on MarkTechPost.