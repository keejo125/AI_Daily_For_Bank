---
publish_time: 1793069127
link: https://www.marktechpost.com/2026/10/26/openai-gpt-6-1-terra/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  OpenAI 推出 GPT-6.1 Terra，将 GPT-6.1 Sol 的 API 价格腰斩，主打更快、更强且更低成本的电脑操控与办公自动化能力。
---

# OpenAI Launches GPT-6.1 Terra, Halving GPT-6.1 Sol’s API Price for Agent Work

> 原文链接：https://www.marktechpost.com/2026/10/26/openai-gpt-6-1-terra/
> 来源：MarkTechPost

OpenAI has released GPT-6.1 Terra, a fast model for visual reasoning, computer use and writing. It replaces GPT-5.6 Terra and is live in the API as gpt-6.1-terra. Standard pricing is $1 per million input tokens and $5 per million output tokens. For teams automating screens, forms and documents at volume, GPT-6.1 Terra changes the cost math.

TL;DR

Size: 1.05M-token context, 128K max output.

Runs on: OpenAI-hosted only (API, ChatGPT Work, Codex). Closed weights.

Performance: Near GPT-6.1 Sol and GPT-6 Astra on vision and computer use, at lower cost.

Best: 85.5% on MMMU-Pro (Vision) at max effort, 1.2 points behind GPT-6 Astra.

Worst: 50.3% on Terminal-Bench 4.0, behind GPT-6.1 Sol (55.9%) and Claude Sonnet 5.5 (70.6%).

What is GPT-6.1 Terra?

GPT-6.1 Terra is an OpenAI reasoning model built for high-volume visual and computer-use work. It accepts text and image input and returns text. The context window is 1,050,000 tokens, with up to 128,000 output tokens. Its knowledge cutoff is June 1, 2026.

Reasoning effort runs from none to max, with medium as the default. Tool calling requires the Responses API. Supported tools include computer use, hosted shell, code interpreter, web search, file search and MCP. OpenAI&#8217;s listed use cases include matching product photos to catalog entries and interpreting technical drawings.

How does GPT-6.1 Terra perform on computer use?

OpenAI&#8217;s main influential test is Agents&#8217; Last Exam v1, a set of professional computer tasks. One task turns architectural drawings into a 3D model.

At medium effort, Terra scores 57.6% at $0.29 per task. GPT-5.6 Terra scored 42.6% at $0.84 on the same setting. GPT-6 Astra also scores 57.6% at medium, but costs $4.82 per task.

At max effort, Terra reaches 60.0% at $1.01 per task. Claude Opus 5.5 scores 63.2% at $8.82 per task on the same chart. OpenAI says Terra completes tasks over 3 times faster than GPT-6 Astra and GPT-6.1 Sol.

On the OSWorld 2.1 offline set, Terra scores 66.7% at medium and 74.2% at max. GPT-5.6 Terra peaked at 57.1%. GPT-6.1 Sol reaches 78.0%, GPT-6 Astra 80.9% and Claude Sonnet 5.5 83.9%.

How strong is its visual reasoning?

On MMMU-Pro (Vision), Terra scores 85.5% at max effort. GPT-6.1 Sol scores 86.3% and GPT-6 Astra 86.7%. GPT-5.6 Terra topped out at 81.7%. Terra&#8217;s max-effort run costs $0.012 per task, against $0.065 for Astra.

&

Did factuality and coding improve?

On OpenAI&#8217;s internal set of error-inducing prompts, the low-effort error rate fell from 53.6% to 16.7%. At max effort, it fell 18 points to 4.3%. The set is adversarial by design, so production error rates will differ.

On Terminal-Bench 4.0, Terra solves 50.3% at max effort, up from 21.5% for GPT-5.6 Terra. It still trails GPT-6.1 Sol (55.9%), GPT-6 Astra (58.2%) and Claude Sonnet 5.5 (70.6%). OpenAI itself recommends Sol or Astra for the most complex coding tasks.

On Terminal-Bench-Science 0.1, Terra scores 58.3% at $4.15 per task. That beats GPT-6.1 Sol&#8217;s 57.0% at $5.47. Claude Opus 5.5 with fallbacks scores 63.3% at $23.21.

How much does GPT-6.1 Terra cost, and where is it available?

Standard API pricing is $1 input, $0.05 cached input and $5 output per million tokens. Batch and Flex are 50% cheaper. Fast mode costs 2x Standard. Prompts above 272K input tokens bill at 2x input and 1.5x output.

That is half of GPT-6.1 Sol&#8217;s $2/$10 and one-tenth of GPT-6 Astra&#8217;s $10/$50. Claude Opus 5.5 lists at $4/$20.

In ChatGPT, Terra is live for Plus, Pro, Enterprise and Edu users in ChatGPT Work and Codex.

GPT-6.1 Terra vs competitors

FeatureGPT-6.1 TerraGPT-6.1 SolGPT-6 AstraClaude Opus 5.5Claude Sonnet 5.5ParametersNot disclosedNot disclosedNot disclosedNot disclosedNot disclosedContext window1.05M1.05M1.05M1M1MMax output128K128K128K128K128KKnowledge cutoffJun 1, 2026Apr 30, 2026Apr 30, 2026Jun 2026Jun 2026API price (in/out per 1M)$1 / $5$2 / $10$10 / $50$4 / $20$2 / $10WeightsClosedClosedClosedClosedClosedAgents&#8217; Last Exam v1 (max)60.0% ($1.01/task)58.6% ($2.00/task)59.3% ($7.24/task)63.2% ($8.82/task)Not shownMMMU-Pro Vision (max)85.5%86.3%86.7%Not shownNot shownOSWorld 2.1 offline (max)74.2%78.0%80.9%Not shown83.9%Terminal-Bench 4.0 (max)50.3%55.9%58.2%Not shown70.6%Terminal-Bench-Science 0.1 (max)58.3%57.0%68.1%63.3% (with fallbacks)Not shown

Benchmark scores and per-task costs are read from OpenAI&#8217;s launch charts and are self-reported. Specs and prices come from each vendor&#8217;s model page. Claude prices: Anthropic pricing.

Key Takeaways

GPT-6.1 Terra costs $1/$5 per million tokens, half of GPT-6.1 Sol.

It matches GPT-6 Astra&#8217;s 57.6% on Agents&#8217; Last Exam at $0.29 per task.

MMMU-Pro hits 85.5%, within 1.2 points of Astra.

Coding still lags: 50.3% on Terminal-Bench 4.0 vs Sonnet 5.5&#8217;s 70.6%.

All scores are OpenAI-reported; parameters and hardware are undisclosed.

Check out the OpenAI announcement, the API model page and the system card addendum. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post OpenAI Launches GPT-6.1 Terra, Halving GPT-6.1 Sol’s API Price for Agent Work appeared first on MarkTechPost.