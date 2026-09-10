---
publish_time: 1788808687
link: https://www.marktechpost.com/2026/09/07/openbmb-releases-minicpm5-2b-a-2-52b-dense-model-averaging-53-9-across-34-benchmarks-and-built-to-run-on-device/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  OpenBMB 发布 MiniCPM5-2B，MiniCPM5 系列第二 checkpoint，2.52B 稠密因果语言模型，42 层、GQA、原生 13 万 token 上下文，架构为标准 LlamaForCausalLM，主流引擎无需定制内核即可加载，面向端侧部署。
---

# OpenBMB 发布 MiniCPM5-2B 端侧稠密模型

> 原文链接：https://www.marktechpost.com/2026/09/07/openbmb-releases-minicpm5-2b-a-2-52b-dense-model-averaging-53-9-across-34-benchmarks-and-built-to-run-on-device/
> 来源：MarkTechPost

OpenBMB has released MiniCPM5-2B, the second checkpoint in the MiniCPM5 series and the follow-up to MiniCPM5-1B. It is a dense causal language model with 2,516,756,480 parameters, of which 1,981,982,720 sit outside the embeddings. It uses 42 layers, grouped-query attention with 16 query heads and 2 key/value heads, and a native context window of 131,072 tokens. The architecture is standard LlamaForCausalLM, so mainstream engines load it with no custom kernels and no model-code fork.

Is it deployable? Yes. The weights are Apache 2.0 and run through vLLM, SGLang, Transformers, llama.cpp, Ollama, LM Studio, MLX and FlagOS. 

What the benchmark table actually shows

OpenBMB compares MiniCPM5-2B against LFM2.5-2.6B, Qwen3.5-2B and Gemma-4-E2B-it in the same size class, and lists Qwen3.5-4B, granite-4.2-3B, Nemotron-3-Nano-4B, Gemma-4-E4B-it and LFM2.5-8B-A1B for reference. Across 34 benchmark rows it averages 53.9. The best baseline in that set is Qwen3.5-4B at 51.1, then granite-4.2-3B at 42.7 and LFM2.5-2.6B at 33.2.

On code reasoning MiniCPM5-2B posts 69.1 on LiveCodeBench v6 against 56.4, and 46.4 on SWE-bench Verified against 33.6. Tool use is the widest margin: 97.1 on τ²-Bench Telecom, 66.6 on BFCL v4, and 20.8 on τ³-Bench Banking against 6.8. Long context is split, with 68.1 on NoLiMa against 43.5, but 59.0 on AA-LCR against 61.0 and 43.7 on LongBench v2 against 47.3. General knowledge is where the size gap shows: 70.8 on MMLU-Pro against 78.0, and 8.9 on Humanity&#8217;s Last Exam against 9.9. OpenBMB marks rows sourced from Artificial Analysis separately from internally reproduced ones.

Training recipe: SFT, then RL, then on-policy distillation

Training follows the UltraData tiered data management method described in original research. Base training runs stable and decay phases, then mid-training adapts the model to the target data distribution. Post-training starts with 400B tokens of deep-thinking SFT, then trains specialised RL teachers for math, code, agentic tasks and writing using the critic-based JustRL II algorithm.

The final step is on-policy distillation. OPD merges 16 RL experts, five of them agentic, into a single shipped model. At each response position it computes full-vocabulary reverse KL divergence between student and teacher logits as the advantage estimate, replacing the verification-based advantage. It reuses the RL prompts as distillation data, so no new corpus is built. OpenBMB measures the RL plus OPD stage at 10.96 average points on reasoning and general benchmarks and 6.96 points on agentic ones.

The data is open too

Alongside the weights, OpenBMB released Ultra-FineWeb, Ultra-FineWeb-L3, UltraX, UltraData-Code, UltraData-Math, UltraData-SFT-2605, UltraData-SFT-Agent-2609 with 500K agent samples, and UltraData-RL-2609 with more than 80K RL samples. Intermediate checkpoints are published as well, covering Base, Midtrain and SFT-only, so the contribution of each stage can be measured directly.

Summary

MiniCPM5-2B is a credible on-device option for agentic and tool-calling workloads, not a general knowledge model. Its advantage is clearest on tool use, coding agents and NoLiMa-style long-context retrieval, and it trails larger models on MMLU-Pro, GPQA-Diamond and MATH-500. The open data and intermediate checkpoints make the RL plus OPD claim checkable, which matters more than the headline average.

Key Takeaways

2.52B dense model, 131,072 token context, Apache 2.0, standard Llama architecture.

Averages 53.9 across 34 benchmarks, ahead of Qwen3.5-4B at 51.1.

Strongest on tool use, coding agents and long-context retrieval; weakest on knowledge.

Post-training pairs 400B SFT tokens with RL teachers and on-policy distillation.

Pre-training, SFT and RL datasets ship alongside the weights.

Check out the HF, GitHub repo and Web. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post OpenBMB Releases MiniCPM5-2B: A 2.52B Dense Model Averaging 53.9 Across 34 Benchmarks and Built to Run On Device appeared first on MarkTechPost.