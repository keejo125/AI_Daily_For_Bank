---
publish_time: 1790053483
link: https://www.marktechpost.com/2026/09/21/nvidia-researchers-have-released-sol-pi/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA、NTU 与 MIT 研究者发布 SoL-Pi，一套面向开源 Pi 编码智能体的 4 项效率机制。这些机制由 AI 在 harness 层运行自动研究循环自行发现，在 51 任务的 EdgeBench 评测上，较 Pi 基线将记录的 Token 流量降低 44.7%~49.0%，为长时运行编码智能体的成本与上下文膨胀问题提供缓解方案。
---

# NVIDIA 推出 SoL-Pi：自动研究循环使编码智能体 Token 流量最高降 49%

> 原文链接：https://www.marktechpost.com/2026/09/21/nvidia-researchers-have-released-sol-pi/
> 来源：MarkTechPost

Coding agents now run for hours, not minutes. Every edit, test run and log read goes back into the model&#8217;s context. A team of researchers from NVIDIA, NTU and MIT have released SoL-Pi, a set of 4 efficiency mechanisms for the open-source Pi coding agent. An AI found these mechanisms by running auto-research loops at the harness layer. On the 51-task EdgeBench evaluation, SoL-Pi cuts recorded token traffic by 44.7% to 49.0% versus Pi and cuts API cost by roughly 33%. Its scores stay close to Pi on both GPT-5.6 Sol and Opus 5.

Is it deployable? Yes. SoL-Pi ships on GitHub under NVlabs as an MIT-licensed extension that runs on an unmodified Pi release. It is tested with Pi 0.85.1 and Node.js 22.19 or newer. 

Why Target the Harness

Most efficiency work lowers the cost per token through faster kernels, quantization or cheaper models. SoL-Pi instead reduces how many tokens a task consumes. The harness is the layer that handles tool calls, context, observations and delegation.

Tuning a harness by hand is slow, and its parts are coupled: a fix in one place can push cost into later steps. Meta-Harness and similar systems automate this work. However, a recent study found that evolved harnesses can overfit their search tasks and give only marginal gains on unseen ones.

How the Search Works

A research AI observes execution traces from a separate agent running base Pi. It then proposes harness changes and tests them. The search covered:

152 proposed directions across 6 families: context, progress, tools, delegation, prompt and policy, and improvement and evaluation

535 executable environments: 495 built from GitHub issue-pull request pairs and 40 synthetic tasks with executable verifiers

More than 3,000 runs and 60,000+ agent-environment interactions

Each search is a disposable, isolated loop. It follows the autoresearch cycle, extended with a Ralph Loop implementation step and an independent reviewer.

Acceptance rules are fixed before the search starts, and the optimizer cannot change them. Every capability metric must stay within a predeclared tolerance. The candidate must also improve at least 1 efficiency metric. EdgeBench stays held out. Of its 51 public tasks, 11 are used for one-way acceptance of frozen candidates and 40 for final evaluation. Held-out results never feed back into the search.

The 4 Mechanisms That Survived

Action Fusion: Base Pi often edits a file and then issues a separate command to test, build or run it. Action Fusion merges both into 1 tool request and returns both outcomes in 1 observation. This removes a model round trip.

Online Context Compact: Plan steps are tracked through update_plan. When a step completes, the harness estimates how many requests remain. It then compares the projected input savings with the extra cost of rewriting the prompt cache. It invokes Pi&#8217;s native compaction when this gate passes or when context nears the window limit.

ObservationPack: Tool outputs above 10 KiB are archived locally and sent in full for the next 2 provider requests. From the 3rd request onward, the model sees a stable handle, the original size and a short excerpt of head and tail lines. Exact pages stay retrievable through the handle.

Evidence-Preserving Reducer: Build and test logs of at least 4 KiB go to a cheaper model, GPT-5.6 Luna at high, which writes a compact receipt. A deterministic verifier checks the receipt&#8217;s schema, source hash, exit status, exact quotes and size. The harness falls back to the original log in 3 cases: verification fails, credentials are suspected, or the receipt is not smaller.

&&

Results on EdgeBench

BackendHarnessTokens (B)API CostAvg. ScoreGPT-5.6 SolCodex3.05$1,78734.7GPT-5.6 SolPi2.15$1,33944.8GPT-5.6 SolSoL-Pi [Efficiency]1.10$89442.0GPT-5.6 SolSoL-Pi [Performance]2.02$1,27147.2Opus 5Claude Code2.00$2,53543.7Opus 5Pi2.37$1,74144.8Opus 5SoL-Pi [Efficiency]1.31$1,15842.2Opus 5SoL-Pi [Performance]2.10$1,60550.5

The full stack was built on GPT-5.6 Sol and moved to Opus 5 without further search. On Opus 5, it keeps 94.3% of Pi&#8217;s score while cutting token traffic by 44.7% and API cost by 33.5%. On GPT-5.6 Sol, it keeps 93.7% of Pi&#8217;s score with 49.0% fewer tokens and 33.2% lower cost.

The Performance point uses the best single mechanism for each backend: ObservationPack on GPT-5.6 Sol and Action Fusion on Opus 5. It lifts scores 5.3% and 12.8% above Pi.

On GPT-5.6 Sol, the full stack increases cache-write traffic from 0.0141 B to 0.0316 B tokens. Total cost still falls, from $1,339 to $894. The paper estimates hourly savings of $8.75 to $13.50 versus the native Codex and Claude Code harnesses, and $4.36 to $5.71 versus Pi.

Beyond EdgeBench

Terminal-Bench 4 (63 CPU-only tasks): SoL-Pi solves 15 tasks versus 18 for both Codex and Pi. It lowers total cost by 26.3% versus Pi ($211.12 vs $286.45).

IMO 2026, Lean 4-verified: SoL-Pi passes 3 of 6 problems, matching Pi, at the lowest cost per passed problem ($20.90). Codex passes 5.

Agent swarm: A Codex coordinator with 20 SoL-Pi workers reaches 1,127 cycles at $60.11. With 20 Pi workers, it reaches 1,366 cycles at $82.12. A single Codex agent is still the cheapest option at $39.20 and reaches 1,333 cycles.

The research team calls the cross-model transfer preliminary. The mechanisms trigger less often on Opus 5, possibly because the search used only GPT-5.6 Sol trajectories.

Key Takeaways

SoL-Pi cuts EdgeBench token traffic by 44.7% to 49.0% versus Pi.

API cost drops about 33% while keeping about 94% of Pi&#8217;s average score.

The 4 mechanisms survived a search over 152 directions and 535 environments.

SoL-Pi is an MIT-licensed, opt-in Pi extension on GitHub.

Check out the Paper, GitHub Repo and Technical Blog. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Introduces SoL-Pi: Auto-Research Loops That Cut Coding Agent Token Traffic by Up to 49% appeared first on MarkTechPost.