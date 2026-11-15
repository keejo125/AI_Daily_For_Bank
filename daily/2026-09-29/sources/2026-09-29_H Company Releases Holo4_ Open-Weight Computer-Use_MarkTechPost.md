---
publish_time: 1790667493
link: https://www.marktechpost.com/2026/09/29/h-company-releases-holo4-open-weight-computer-use-models-that-click-code-and-call-tools-across-desktop-web-android-and-apis/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  H公司发布通用计算机操作模型族Holo4，含27B稠密与35B-A3B MoE（激活3B）两档，均提供256K上下文，27B稠密基于Qwen3.8-27B微调、35B-A3B MoE基于Qwen3.6-35B-A3B微调，可点击屏幕、输入、写代码、调用MCP或API工具。35B-A3B以Apache 2.0开源可商用自托管，27B权重为CC BY-NC（商用走H Models API），是面向桌面/网页/安卓/API的开放权重计算机操作模型。
---

# H 公司发布 Holo4：可点击、编码、调用工具的开放式计算机操作模型

> 原文链接：https://www.marktechpost.com/2026/09/29/h-company-releases-holo4-open-weight-computer-use-models-that-click-code-and-call-tools-across-desktop-web-android-and-apis/
> 来源：MarkTechPost

H Company has released Holo4, a family of generalist computer-use models for AI agents. One set of weights clicks and types on screens. It also writes code and calls MCP or API tools. Holo4 ships in 2 sizes: Holo4 27B (dense) and Holo4 35B-A3B (Mixture of Experts, 3B active). Both serve a 256K context on the H Models API.

Is it deployable? Yes. Holo4 35B-A3B ships Apache 2.0 weights for commercial self-hosting. Holo4 27B weights are CC BY-NC 4.0, so commercial use of 27B runs through the H Models API.

What is Holo4

Holo4 is a vision-language model for computer use. Holo4 27B is fine-tuned from Qwen3.8-27B. Holo4 35B-A3B is built on Qwen3.6-35B-A3B. Both pair with H&#8217;s open hai-agents harness. The harness sends screenshots and tool results to the model. It then executes the requested clicks, typing, code and tool calls.

H company targets a known gap. GUI-only agents fail without a screen. Tool-calling agents stall when an application has no API. Holo4 runs on desktop, web, Android, code sandboxes and business APIs. It is the same model, called the same way, on every platform.

Benchmarks: Close to the Frontier, at a Fraction of the Cost

Per H Company&#8217;s benchmark table, Holo4 27B scores 85.2% on OSWorld at $0.08 per task. Its Qwen3.8 27B base scores 84.3% at $0.22. On AndroidWorld, Holo4 27B reaches 85.1%.

Long workflows show the remaining gap. On OSWorld 2.0, Holo4 27B scores 61.7% at $1.22 per task. Claude Opus 5.5 scores 81.8% at $8.48, per H&#8217;s figures. On AutomationBench, Holo4 27B scores 45.4% at $0.05 per task.

It is important to note that frontier scores come from different harnesses and effort levels. Also, 480 of AutomationBench&#8217;s 600 public tasks sit in the split H Company collected training data from. On the 120 held-out tasks, Holo4 27B scores 49.3%. H Company publishes every trajectory at trajectories.hcompany.ai and on Hugging Face.

How H Company Built Holo4

Agentic Task Factory: H&#8217;s internal pipelines build environments and verifiable tasks from documentation, screenshots and real software. The factory has produced about 10,000 tasks: 4k web apps, 3k MCP servers, 3k desktop and OS. A task survives only if its verifier rejects near misses. An agent must also solve it through the real interface.

Supervised fine-tuning: The SFT set holds 127B tokens. About three quarters are successful agentic trajectories: desktop 45%, web 14%, MCP and API 12%, mobile 3%.

2 RL experts, 1 merge: Asynchronous online RL trains 2 LoRA experts. One handles desktop and web. The other handles terminal, MCP and API. Both merge back with equal weight and no further training.

Harness: H Company rebuilt its agent loop using OSWorld 2.0 failure analysis. The largest changes were reliable memory across hundreds of steps and a shell on the desktop machine.

Holotron4 Nano

H Company also released Holotron4 Nano, built on NVIDIA&#8217;s Nemotron 3 Nano Omni through the Nemotron Coalition. The same combination lifts OSWorld from 21.0% to 76.3% over the base model.

Pricing and Deployment

Holo4 27B costs $0.40 input and $3.00 output per 1M tokens. Holo4 35B-A3B costs $0.30 and $2.00. The API is OpenAI-compatible at https://api.hcompany.ai/v1; see the quickstart. Weights on the Hugging Face collection come in BF16, FP8, NVFP4 and 4-bit GGUF. H Company documents local inference with vLLM and llama.cpp. H says DSpark drafter checkpoints for faster inference arrive in the coming days.

Interactive Explainer: How Holo4 Works

&&

Holo4 vs. Closest Competitors

FeatureHolo4 27BHolo4 35B-A3BQwen3.8-27B (base)Claude Opus 5.5GPT-6 AstraArchitecture27B dense35B MoE, 3B active27B denseProprietaryProprietaryWeights and licenseOpen, CC BY-NC 4.0Open, Apache 2.0Open, Apache 2.0ClosedClosedContext window256K256K262K native, up to 1M1M1.05MAPI price (input / output per 1M)$0.40 / $3.00$0.30 / $2.00Varies by provider$4 / $20$10 / $50InterfacesGUI, code, MCP, APIsGUI, code, MCP, APIsGUI, tools, codeComputer use, toolsComputer and browser use, toolsOSWorld 2.0 score*61.7%30.9%48.0%81.8%73.5%OSWorld 2.0 cost per task*$1.22$0.61$3.49$8.48$9.07Self-hostableNon-commercial onlyYesYesNoNoSourceModel cardModel cardModel cardAnthropic docsOpenAI, OpenRouter

*OSWorld 2.0 figures from H Company&#8217;s newsroom table. Opus 5.5 ran at max effort in Anthropic&#8217;s harness. GPT-6 Astra ran at max effort on the 82-task offline subset. Harnesses differ, so treat cross-vendor rows as directional.

Key Takeaways

Holo4 uses 1 model for GUI clicks, code, MCP and API calls.

Holo4 27B scores 85.2% on OSWorld at $0.08 per task.

35B-A3B is Apache 2.0; 27B weights are non-commercial only.

Opus 5.5 still leads OSWorld 2.0: 81.8% vs 61.7%.

API pricing starts at $0.30 input and $2.00 output per 1M tokens.

Check out the Technical details, H Company&#8217;s HuggingFace Collection and Model API. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post H Company Releases Holo4: Open-Weight Computer-Use Models That Click, Code and Call Tools Across Desktop, Web, Android and APIs appeared first on MarkTechPost.