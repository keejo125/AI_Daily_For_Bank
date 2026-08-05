---
publish_time: 1785535419
status: pending
---

# DeepSeek Upgrades DeepSeek-V4-Flash-0731 with Major Agentic and Coding Gains

> 原文链接：https://www.marktechpost.com/2026/07/31/deepseek-upgrades-deepseek-v4-flash-0731-with-major-agentic-and-coding-gains/
> 来源：MarkTechPost

DeepSeek published DeepSeek-V4-Flash-0731 on Hugging Face and moved the official V4-Flash API into public beta on July 31, 2026. The model card is explicit that this is the official release superseding the preview, and that the architecture and size are unchanged. The gains come from re-post-training, not a new design.

The checkpoint ships with the DSpark speculative decoding module attached, matching the structure of DeepSeek-V4-Flash-DSpark. Hugging Face reports 304B parameters for the repo, which includes that draft module on top of the 284B base.

On the API side, deepseek-v4-flash now natively supports the Responses API format and is adapted for Codex. The V4-Pro API and the app and web models were not updated.

Is it deployable?

Yes, in two very different ways.

Via API, it is deployable by almost anyone: DeepSeek&#8217;s pricing page lists deepseek-v4-flash at $0.14 per 1M input tokens on a cache miss, $0.0028 on a cache hit, and $0.28 per 1M output tokens, with a 2,500 concurrency limit. That is roughly a third of deepseek-v4-pro output pricing ($0.87). Seed-stage startups, indie developers, and internal platform teams can run agent loops at this price without a GPU budget.

Via self-hosting, the bar is much higher: The weights are MIT-licensed and ungated, but every expert stays resident in memory even though only 13B activate per token. DeepSeek&#8217;s vLLM example serves it on a single 4×GB300 node. Unsloth&#8217;s dynamic GGUFs put the lossless 8-bit build at 162 GB and a 3-bit build at 103 GB, needing roughly 110 GB of combined RAM plus VRAM. Self-hosting suits mid-size and large enterprises with a serving cluster, or one well-specced workstation at aggressive quantization.

Architecture

Per the DeepSeek-V4 technical report, V4-Flash is a 284B-parameter MoE with 13B activated per token and a 1M-token context window. Each MoE layer holds 1 shared expert and 256 routed experts with an intermediate dimension of 2048, and 6 routed experts fire per token. The first three MoE layers use hash routing. Multi-token prediction depth is 1.

Attention is hybrid, combining Compressed Sparse Attention (CSA) and Heavily Compressed Attention (HCA). Manifold-Constrained Hyper-Connections (mHC) replace conventional residual connections, with expansion factor 4 and 20 Sinkhorn-Knopp iterations. Pre-training used more than 32T tokens and the Muon optimizer. The paper&#8217;s headline efficiency figure — 27% of single-token inference FLOPs and 10% of KV cache versus DeepSeek-V3.2 at 1M context — is stated for V4-Pro, not Flash. 

<!&#8211; EMBED HERE: paste wordpress-embed.html into a Custom HTML block &#8211;>

&&&

Benchmarks

All figures below are DeepSeek-reported, from the 0731 model card.

BenchmarkV4-Flash-0731V4-Flash (Preview)V4-Pro (Preview)GLM-5.2Opus-4.8Terminal Bench 2.182.761.872.181.085.0NL2Repo54.239.438.548.969.7Cybergym76.738.752.7—83.1DeepSWE54.47.312.846.258.0Toolathlon-Verified70.349.755.959.976.2Agents&#8217; Last Exam25.215.816.523.825.7AutomationBench Public25.110.812.812.927.2

Two important things to note: 

Code Agent tasks were run with the minimal mode of DeepSeek Harness, which has not been released. 

DSBench-FullStack (68.7) and DSBench-Hard (59.6) are internal test sets. Agent scores are harness-sensitive, so independent runs may diverge.

Serving it

DSpark is enabled with one vLLM flag: --speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}'. The DSpark paper reports 60–85% faster per-user generation on V4-Flash versus the MTP-1 baseline at matched aggregate throughput.

There is no Jinja chat template. DeepSeek ships an encoding/ folder with encode_messages and parse_message_from_completion_text instead. reasoning_effort takes low, high, or max. DeepSeek recommends temperature = 1.0, top_p = 0.95 for agentic use and 1.0 otherwise, with up to 384K output tokens at high and max.

Key Takeaways

Same 284B/13B architecture as the April preview: the jump is post-training only.

Beats V4-Pro (Preview) on every agentic benchmark DeepSeek published, at a third of the output price.

MIT-licensed and ungated, so on-premise commercial deployment is unblocked.

Self-hosting needs ~110 GB memory at 3-bit, or a 4×GB300 node for full-precision serving.

All benchmark numbers are vendor-reported on an unreleased harness — run your own evals first.

Check out the Model Update on HF. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post DeepSeek Upgrades DeepSeek-V4-Flash-0731 with Major Agentic and Coding Gains appeared first on MarkTechPost.