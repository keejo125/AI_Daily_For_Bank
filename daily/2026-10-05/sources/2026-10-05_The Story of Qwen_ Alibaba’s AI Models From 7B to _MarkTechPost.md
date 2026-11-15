---
publish_time: 1791173434
link: https://www.marktechpost.com/2026/10/04/the-story-of-qwen-alibabas-ai-models-from-7b-to-2-4t/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  本文系统梳理阿里巴巴通义千问（Qwen）从2023年4月通义千问亮相，到2026年开放权重达2.4万亿参数的演进之路。2023年8月开源Qwen-7B直接对标Llama 2；2024年Qwen1.5、Qwen2（首推MoE旗舰）、Qwen2.5（一次性开源超100个模型、预训练数据扩至18万亿token、Apache 2.0许可）形成开源机器；同年11月推出Qwen2.5-Coder与首个推理模型QwQ。三年半间，Qwen从对话机器人成长为横跨语言、视觉、音频、代码与推理的开源模型家族，已成为全球开发者默认选择之一，Hugging Face衍生模型超5万个。
---

# 通义千问进化史：从 7B 到 2.4T 参数

> 原文链接：https://www.marktechpost.com/2026/10/04/the-story-of-qwen-alibabas-ai-models-from-7b-to-2-4t/
> 来源：MarkTechPost

In April 2023, Alibaba Cloud demoed a chatbot whose name roughly means &#8216;truth from a thousand questions.&#8217; Three and a half years later, its descendant ships open weights with 2.4 trillion parameters. This is the story of how Qwen got there, release by release.

&&&

Chapter 1 — 2023: a thousand questions

Alibaba moved after ChatGPT, but not by much. On April 7, 2023, Alibaba Cloud began handing invitation codes to corporate customers for a model called Tongyi Qianwen. The name draws partly on the philosopher Mencius.

Four days later, at the Alibaba Cloud Summit in Beijing, then-CEO Daniel Zhang unveiled it publicly. Alibaba said it would roll the model into every business, starting with DingTalk and the Tmall Genie voice assistant (China Daily).

The real turn came in August. On August 3, 2023, Alibaba open-sourced Qwen-7B and Qwen-7B-Chat, a direct answer to Meta&#8217;s Llama 2. Qwen-7B was pretrained on over 2.2 trillion tokens with a 2,048-token context. Its license was free for commercial use below 100 million monthly users.

Vision followed within weeks. Qwen-VL, the first vision-language branch, launched in late August 2023.

On September 13, 2023, Tongyi Qianwen opened to the general public, a sign of Chinese regulatory approval. The same month, the team published the Qwen Technical Report on arXiv.

The year closed with scale. Alibaba released its 72B and 1.8B models for download around December 1, 2023. Qwen now spanned laptop-sized to frontier-sized open weights.

Chapter 2 — 2024: the open-weight machine

2024 is the year Qwen became a default choice for developers. The team shipped 3 generations in 8 months.

Qwen1.5 (February): On February 5, 2024, the team released Qwen1.5, framed as a beta of Qwen2. It covered 0.5B to 72B dense models with stable 32K context at every size. A 14B MoE with 2.7B active parameters followed. So did a 110B dense model, the family&#8217;s first above 100B.

Qwen2 (June): The team announced Qwen2 in early June 2024 in 5 sizes, from 0.5B to 72B. That lineup included Qwen2-57B-A14B, its first open mixture-of-experts flagship. Training data added 27 languages beyond English and Chinese. The 7B and 72B instruct models handled up to 128K tokens. The licensing shift mattered most: every size except 72B moved to Apache 2.0.

Specialists arrived over the summer. Qwen2-Math launched in August, along with Qwen2-Audio. Qwen2-VL followed at the end of August, able to analyze videos over 20 minutes long.

Qwen2.5 (September): At the Apsara Conference on September 19, 2024, Alibaba released over 100 open-source models at once. The Qwen2.5 Technical Report says pretraining data grew from 7 trillion to 18 trillion tokens. Sizes ran 0.5B to 72B, with 128K context and 8K-token generation.

Adoption was already real. Alibaba said Qwen models had passed 40 million downloads and inspired over 50,000 derivative models on Hugging Face.

Coding and reasoning (November–December): Qwen2.5-Coder shipped its full family on November 11, 2024. Then came the first reasoning model. QwQ-32B-Preview arrived in late November under Apache 2.0, as an open challenger to OpenAI&#8217;s o1. QVQ-72B-Preview, an experimental visual reasoning model, closed the year on December 24.

Chapter 3 — Early 2025: answering DeepSeek

January 2025 belonged to DeepSeek-R1. Qwen&#8217;s response came in weeks, not months.

On January 26, the team shipped Qwen2.5-VL in 3B, 7B and 72B sizes. TechCrunch noted it could control PCs and phones. Three days later, on the first day of Lunar New Year, Alibaba launched Qwen2.5-Max, a large-scale MoE model. Reuters reported Alibaba&#8217;s claim that it surpassed DeepSeek-V3.

The bigger statement came on March 6. QwQ-32B, built on Qwen2.5-32B and trained with reinforcement learning, shipped under Apache 2.0. Qwen claimed performance comparable to DeepSeek-R1, a 671B model. VentureBeat put the hardware gap at about 24 GB of VRAM versus over 1,500 GB. Alibaba&#8217;s Hong Kong shares rose more than 7% that day.

Multimodality kept pace. Qwen2.5-Omni-7B arrived on March 26 under Apache 2.0. It took text, images, audio and video as input, and answered in text or speech. CNBC framed it as a model for cost-effective AI agents.

Chapter 4 — 2025: Qwen3 and the trillion-parameter line

Qwen3 (April): On April 29, 2025 (Beijing time), the team released Qwen3: 6 dense models from 0.6B to 32B and 2 MoE models. The flagship was Qwen3-235B-A22B, with 22B active parameters. Every model shipped under Apache 2.0.

The key feature was hybrid thinking. One model could reason step by step or answer instantly, toggled by the user. The Qwen3 Technical Report lists pretraining on about 36 trillion tokens. Language coverage jumped from 29 to 119 languages and dialects. TechCrunch called it a family of &#8220;hybrid&#8221; reasoning models.

The 2507 refresh (July): On July 21, 2025, Qwen split hybrid thinking back apart. Qwen3-235B-A22B-Instruct-2507 shipped as a non-thinking model with a 262K native context. Separate Thinking-2507 checkpoints followed (Hugging Face collection).

Agents and images (July–August): Qwen3-Coder-480B-A35B launched on July 22, 2025 for agentic coding. Alibaba paired it with Qwen Code, an open-source terminal coding agent (Computerworld). On August 4, the team open-sourced Qwen-Image, a 20B MMDiT model built for text rendering inside images.

An editing variant, Qwen-Image-Edit, was open-sourced on August 18, 2025.

The September sprint: Qwen3-Max-Preview, the first Qwen model over 1 trillion parameters, appeared on September 5. Unlike past flagships, it shipped API-only.

Days later came Qwen3-Next-80B-A3B, an architecture bet. It mixed Gated DeltaNet linear attention with gated attention in a 3:1 layout. The model card claims 10% of Qwen3-32B&#8217;s training cost and 10x inference throughput past 32K tokens.

On September 22, Qwen3-Omni and Qwen3-VL followed. At Apsara on September 24, Alibaba formally launched Qwen3-Max. CEO Eddie Wu said spending would exceed the RMB 380 billion (US$53 billion) three-year AI and cloud plan.

By year&#8217;s end, Qwen was national infrastructure for others. In November 2025, AI Singapore said its Sea-Lion model would switch from Llama to Qwen as its base.

Qwen also became a consumer brand. The Qwen App entered public beta on November 17, 2025. Alibaba said it passed 10 million downloads in its first week.

Chapter 5 — 2026: 4 generations in 6 months

A fast start (January–February): On January 26, 2026, Qwen released Qwen3-Max-Thinking, a closed reasoning model. Qwen said it was comparable to GPT-5.2-Thinking, Claude Opus 4.5 and Gemini 3 Pro across 19 benchmarks (TestingCatalog). Qwen3-Coder-Next, a small hybrid model for agentic coding, followed on February 2. Qwen-Image-2.0 merged generation and editing into one model on February 10.

Qwen3.5 (February): On February 16, 2026, Lunar New Year&#8217;s Eve, Alibaba unveiled Qwen3.5 for what it called the agentic AI era. The open Qwen3.5-397B-A17B activates 17B of 397B parameters. It runs on the hybrid linear-attention design that Qwen3-Next had previewed. A hosted Qwen3.5-Plus added a 1M-token context.

A medium series followed on February 24. Qwen said its Qwen3.5-35B-A3B beat the older Qwen3-235B-A22B-2507. Small on-device models arrived on March 2.

A leadership break (March): On March 3, tech lead Junyang Lin posted that he was stepping down. Reuters reported he was the third senior Qwen figure to leave in 2026. Post-training head Yu Bowen also left, and coding lead Hui Binyuan had joined Meta in January (Yicai).

The trigger, per 36Kr, was a plan to split Qwen into horizontal pre-training, post-training and modality teams. On March 16, Alibaba put its AI units under a new group led by CEO Eddie Wu. By then, Alibaba had released more than 400 open Qwen models, downloaded over 1 billion times.

Qwen3.6 (April): The cadence did not slow. Qwen3.6-Plus launched on April 2 as a proprietary, hosted model. That fit a wider shift: SCMP reported Chinese AI giants pivoting toward proprietary models for revenue. The open side kept moving. Qwen3.6-35B-A3B shipped under Apache 2.0 on April 16, aimed at agentic coding.

Two more followed within a week. Qwen3.6-Max-Preview, a closed flagship preview, arrived on April 20. On April 22, the dense Qwen3.6-27B shipped under Apache 2.0. Qwen said it beat Qwen3.5-397B-A17B on major coding benchmarks.

Qwen3.7 (May–June): At the Alibaba Cloud Summit on May 20, Alibaba unveiled Qwen3.7-Max, built for long-horizon agent tasks. Alibaba said Artificial Analysis ranked it fifth globally and first among Chinese models. Qwen3.7-Plus followed in early June at $0.4/$1.6 per 1M tokens. Both stayed closed.

In July, CNBC reported Qwen would be integrated into Apple Intelligence in China.

Qwen3.8 (July–August): Bloomberg reported a preview of the new flagship on July 19. The hosted Qwen3.8-Max launched in early August. On August 12, Alibaba open-sourced its base as Qwen3.8-2.4T-A95B: 2.4 trillion parameters, 95B active (Gigazine).

The license had a new catch. Providers earning over US$50 million in 12 months need a commercial license. Two days later, Qwen3.8-27B shipped under plain Apache 2.0. On August 26, Reuters covered Qwen3.8-Flash. Its open sibling, Qwen3.8-Flash-Next, was billed as an early preview of the Qwen4 architecture.

September: On September 20, Qwen-Image-2.1 arrived as a 7B generator. Unlike earlier open Qwen image models, it is research-only.

Two days later, at Apsara 2026, Alibaba said Qwen 4 is &#8220;currently in training&#8221;. It projected Qwen 4.5 and Qwen 5 at 5 to 10 trillion parameters. No date, sizes or license were given for Qwen 4.

Chapter 6 — The ecosystem and the license arc

Qwen&#8217;s reach grew faster than its parameter counts. In September 2024, Alibaba reported 40 million downloads and 50,000+ derivative models. By March 2026, Reuters put it at more than 400 open models and over 1 billion downloads. The same report said the Qwen app hit 203 million monthly active users in February 2026.

At the Qwen3-Max-Thinking launch in January 2026, Alibaba also said Qwen had become the first open model family with over 200,000 derivative models on Hugging Face.

The licenses tell a quieter story. Qwen has moved from restrictive, to open, to a deliberate two-tier split.

PeriodWhat changedExampleAug 2023Custom license, free below 100M monthly usersQwen-7BJun 2024Most sizes move to Apache 2.0; 72B keeps Qianwen licenseQwen2Apr 2025Every open model under Apache 2.0Qwen3Sep 2025Flagship goes API-onlyQwen3-MaxApr–Jun 2026Plus and Max tiers proprietary; mid-size openQwen3.6, Qwen3.7-PlusAug 20262.4T weights open, with a US$50M revenue thresholdQwen3.8-2.4T-A95BSep 2026Image model under research-only licenseQwen-Image-2.1

The pattern is consistent. Small and mid-size models stay permissive to keep developers building on Qwen. The frontier tier earns revenue through Alibaba Cloud.

Timeline

Every date below is linked in the chapters above. Newest first.

Key Takeaways

Qwen began as Tongyi Qianwen, an invite-only enterprise beta announced on April 11, 2023.

Open weights came fast: Qwen-7B in August 2023, Qwen-72B by the end of that year.

Qwen3 (April 2025) added hybrid thinking, 36T training tokens and 119 languages under Apache 2.0.

2026 brought 4 generations in 6 months (Qwen3.5 to Qwen3.8) and a split open/proprietary strategy.

Qwen 4 is in training; Alibaba&#8217;s roadmap puts Qwen 4.5 and Qwen 5 at 5 to 10 trillion parameters.

Resources:

Qwen blog and QwenLM on GitHub

Qwen on Hugging Face

Qwen Technical Report (arXiv 2309.16609)

Qwen2.5 Technical Report (arXiv 2412.15115)

Qwen3 Technical Report (arXiv 2505.09388)

Alibaba Cloud: 2026 Apsara Conference roadmap

Alibaba Group: Apsara Conference 2025

The post The Story of Qwen: Alibaba&#8217;s AI Models From 7B to 2.4T appeared first on MarkTechPost.