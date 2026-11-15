---
publish_time: 1793443094
link: https://www.marktechpost.com/2026/10/31/factory-droid-1-0-frontier-harness/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Factory 发布 Droid 1.0，是其 Coding Agent harness 迄今最大更新，核心是默认开启的“编程式工具调用”（programmatic tool calling）：模型写一段在沙箱中运行的程序来驱动工具，一次模型请求可触发数百次工具调用。基础提示词从 20,887 token 降至 13,055（降 37%），默认只加载 2 个工具定义。在同一模型下，Droid 1.0 在 Terminal-Bench 4 取得最高通过率（Claude Opus 5.5 上 65.2%），单次通过成本 4.73 美元。
---

# Factory 发布 Droid 1.0：模型无关的编程智能体脚手架

> 原文链接：https://www.marktechpost.com/2026/10/31/factory-droid-1-0-frontier-harness/
> 来源：MarkTechPost

Factory has released Droid 1.0, the largest update yet to the Factory Droid agent harness. The main change is programmatic tool calling, now on by default. The model writes a program that runs its tools. One model request can now drive hundreds of tool calls.

TL;DR

Size: Base prompt is 13,055 input tokens, down 37% from 20,887. Only 2 tool definitions ship up front, down from 11.

Runs on: macOS and Windows desktop app, a terminal UI, and the Node SDK @factory/droid-sdk. Works with any supported model, including your own API keys.

Performance: Highest pass rate of every harness Factory tested, on the same model, at lower cost.

Best: 65.2% on Terminal-Bench 4 with Claude Opus 5.5, at $4.73 per passed task (self-reported).

Worst: With GPT-6.1 Sol, Droid takes 10% longer per passed task than Codex.

What is Droid 1.0?

Droid 1.0 is a model-independent coding agent harness from Factory. Factory defines a harness as everything around the model. That means the prompts, the tools, how tool results return, and the loop. Users pick a model or let Factory Router choose a cost-efficient mix.

How does programmatic tool calling work?

In a standard loop, every tool output lands in the model&#8217;s context. With programmatic tool calling (PTC), the model writes a program instead. Droid implements this as a Script tool. The model writes JavaScript that runs in a sandbox. The sandbox has no file, network, or system access of its own.

Raw files, search results, and logs stay inside the program. Only printed output returns to the model. Independent calls run concurrently.

The idea builds on CodeAct (Wang et al., 2024). Factory reports these results from its own sessions:

Unit test fix: 15 tool calls took 5 model calls instead of 10. The task finished in 41.6 s instead of 56.8 s.

Linear cleanup: 151 issues moved and verified in 312 tool calls. The Script used 2 requests and about 61,000 tokens. Factory models direct calls at 36 requests and about 3.1M tokens.

CI sweep: 5,384 jobs across 547 runs, in 2 requests. Under 0.1% of tool results reached the model&#8217;s context.

On Claude Opus 5.5, Script mode cuts Droid&#8217;s cost by 15% versus direct tool calling. It is on by default for 10 models, including GPT-6.1 Sol and Kimi K3.

How does Droid 1.0 score on Terminal-Bench 4?

Factory ran each harness against Droid on the same model. Each harness ran 3 trials per task, from October 23 to 28, 2026. Only tasks both harnesses passed in all 3 trials count toward cost and time.

Claude Opus 5.5: Droid scores 65.2%. Cursor and OpenCode score 62.1%, Devin 59.6%, Claude Code 57.6%. Droid costs up to 24% less.

GPT-6.1 Sol: Droid scores 57.6% at $0.79 per passed task. Codex scores 54.0%, OpenCode 51.0%, Devin 45.0%.

Speed: On Opus 5.5, Droid takes 16% to 26% less time per passed task. Against Claude Code, it also uses 17% fewer tokens.

What else changed in the harness?

Most changes came from an internal Agent Factory loop. Agents read failures and propose changes, tested on every affected model family. Engineers review and merge.

Prompt cache: Newly loaded tools are appended to the request end. The typical production request reads 98% of input from cache.

Leaner first request: Tool definitions fell 46%. Rarely used tools now load on demand.

Bounded autonomy: 3 identical tool calls trigger a nudge, and 6 stop the loop. Compaction summaries now hold 16,000 tokens, up from 8,000.

App latency: First paint fell from 1,839 ms to 488 ms. Each extra session now adds about 20 MB, not 350 MB.

Comparison: Droid 1.0 vs other coding agent harnesses

FeatureDroid 1.0 (Factory)Codex CLIClaude CodeOpenCodeDeveloperFactoryOpenAIAnthropicAnomalyModel supportModel-independent, BYOK, Factory RouterChatGPT plan or API keyNative harness for Claude (Factory)75+ LLM providers, local modelsLicenseNot disclosed (SDK is Apache 2.0)Apache-2.0Anthropic Commercial TermsMITProgrammatic tool callingDefault (Script tool)Yes, per FactoryNot disclosedNot disclosedTB4, Claude Opus 5.5*65.2%Not tested57.6%62.1%TB4, GPT-6.1 Sol*57.6%54.0%Not tested51.0%Time per passed task vs Droid*BaselineDroid 10% slower (Sol)Droid 26% faster (Opus)Droid 4% to 24% fasterPricingFrom $20/moChatGPT plan or APINot disclosedFree, open source

*Terminal-Bench 4 figures are Factory&#8217;s own runs, from its methodology section.

How can developers try it?

Droid 1.0 ships as a desktop app and terminal UI. The Droid SDK runs the same harness from Node, with sessions, streaming and MCP tools. Paid plans start at $20 per month.

Key Takeaways

Droid 1.0 makes programmatic tool calling the default.

1 Script can run hundreds of tool calls per model request.

65.2% on Terminal-Bench 4 with Opus 5.5, self-reported.

Base prompt shrank 37%, to 13,055 tokens.

Codex still wins on speed with GPT-6.1 Sol.

Check out the full Factory research post, the Droid SDK on GitHub and the Droid docs. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet Factory Droid 1.0: A Model-Independent Coding Agent Harness Built on Script Mode appeared first on MarkTechPost.