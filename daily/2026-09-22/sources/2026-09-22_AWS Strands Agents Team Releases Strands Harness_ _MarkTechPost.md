---
publish_time: 1790026934
link: https://www.marktechpost.com/2026/09/21/aws-strands-agents-team-releases-strands-harness/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  AWS Strands 团队发布 Strands Harness，一个开箱即用的通用智能体框架，面向“在 Claude Code/Codex 中可行、自建循环却难落地”的痛点。它支持本地或云端部署，以 Apache 2.0 提供 Python 与 TypeScript 版本，一行代码即可启动。团队称在同等精度下可降低约 28% 的 Token 成本，帮助开发者跳过从零搭建 agent loop 的环节。
---

# AWS Strands 团队发布 Strands Harness：开源智能体框架，同等精度 Token 成本降 28%

> 原文链接：https://www.marktechpost.com/2026/09/21/aws-strands-agents-team-releases-strands-harness/
> 来源：MarkTechPost

Many developers find that an agent idea works inside Claude Code or Codex, then struggles once they rebuild it with their own loop. The Strands Agents team at AWS is targeting that gap with Strands harness, a fully assembled, general-purpose agent harness. It runs locally or deploys to a cloud provider, ships for Python and TypeScript under Apache 2.0, and starts with one line of code. The team reports 28% lower cost than other harnesses running the same Claude or GPT models across 6 benchmarks, with near-equal accuracy.

Is it deployable? Yes. It runs locally, and a bundled skills file helps your coding agent generate deployment config for AWS, GCP, Azure, Cloudflare, and Modal.

What is Strands Harness

A harness is the system around the model: the loop, tools, context handling, memory, and recovery. Strands already exposed those building blocks through the Strands Harness SDK. Strands harness packages them into working defaults. It is built as a general-purpose agent, not a coding agent.

Out of the box, create_harness() returns an agent that:

Runs on a current reasoning model through Amazon Bedrock, Anthropic, OpenAI, Google, Ollama, or LiteLLM.

Ships shell, file (read, write, edit), and web tools, instead of a bespoke tool per task.

Offloads bulky tool results to files and caches reused parts of each request.

Keeps long-term memory across runs and resumes a conversation from a session ID.

Delegates open-ended subtasks to a built-in helper agent and tracks multi-step work with a checklist.

Loads Agent Skills when it finds them.

Benchmark Setup and the 28% Figure

The Strands Agents team ran distributed benchmarking on Amazon EC2 with Harbor, the evaluation framework from the Terminal-Bench creators. The score is the average across 6 benchmarks: ALFWorld, ContextBench, GAIA, WebShop, τ²-bench, and Terminal-Bench 2.1. Cost is the average dollars per task. Rivals on the chart are Claude Code, Codex, oh-my-pi, OpenCode, and DeepSeek Harness.

One important thing to note. DeepSeek Harness was the most token-efficient harness overall, running about 14% cheaper than Strands harness. It also scored lower on every benchmark. The chart footnote states that including it brought the overall savings figure down to 28%. The highest-scoring point on the chart is Claude Opus 5 on Strands harness, near 85%.

Terminal-Bench 2.1: Same Model, 5 Harnesses

The clearest head-to-head uses Claude Fable 5 on Terminal-Bench 2.1, with 89 trials per harness.

HarnessRun costAccuracyStrands harness$56.2969.7Oh-my-pi$86.8369.7OpenCode$73.4266.3Claude Code$248.0561.8DeepSeek Harness$40.3059.5

Against Claude Code, Strands harness cost 77% less and scored 7.9 points higher. Oh-my-pi matched its 69.7 accuracy at 54% higher cost. DeepSeek Harness was cheaper still, but trailed by 10.2 points. The team also noted that 2 other open-source harnesses performed well on cost and accuracy against Claude Code.

&&

What Drives the Efficiency

Strands harness ships defaults for prompt caching and context management. The team says context management largely drove both token efficiency and accuracy. 3 rules do the work:

Tool results over about 1,500 tokens get truncated.

Summarization (compaction) triggers when context usage passes 85%.

Context recovery runs inside the loop if the window overflows.

This matches recent independent research. The HarnessTax study compared Claude Code, Codex CLI, and Pi across 7 models. It found harness choice barely moved success rates, while the same model reached similar success at up to 5x the cost. The Strands researchers say a follow-up paper on their benchmarks is coming.

Getting Started

Install with pip install strands-harness or npm install @strands-agents/harness. Pick a model by name, or point the harness at a local Ollama model:

Copy CodeCopiedUse a different Browser

from strands_harness import create_harness

agent = create_harness(model="litellm/openai/gpt-5.6-sol")
agent("Research the top three vector databases and compare their pricing")

The Strands CLI (npm install @strands-agents/strands-cli) lets you prototype an agent in plain English. In the team&#8217;s demo, the agent was asked to add the Playwright MCP server and measure video load latency on a blog post. Running /export then produced the harness code, with the Playwright MCP included, as a Python or TypeScript zip.

The CLI itself is built on Strands harness. Strands engineer Gautam Sirdeshmukh also used it to build a desktop app that starts Strands harness runs remotely.

Customization goes deep. You can override any default, swap models, add tools, or replace components down to the Strands Harness SDK. Because the harness is a library dependency, the agent prototyped on a laptop is the same one embedded in production.

Key Takeaways

Strands harness packages AWS&#8217;s Strands primitives into a general-purpose, Apache 2.0 agent.

It reports 28% lower cost than rival harnesses across 6 benchmarks at comparable accuracy.

With Fable 5 on Terminal-Bench 2.1, it cost 77% less than Claude Code and scored higher.

Context defaults drive the gains: 1,500-token truncation, 85% compaction, in-loop recovery.

One create_harness() call targets Bedrock, Anthropic, OpenAI, Google, Ollama, or LiteLLM.

Check out the Technical details, GitHub repo, PyPI package, and Strands Agents docs.

The post AWS Strands Agents Team Releases Strands Harness: An Open-Source Agent Harness With 28% Lower Token Cost at Comparable Accuracy appeared first on MarkTechPost.