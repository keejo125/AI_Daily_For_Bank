---
publish_time: 1791449614
link: https://www.marktechpost.com/2026/10/08/architect-launches-liquid-inference-a-real-time-auction-for-llm-inference/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Architect Financial Technologies 推出 Liquid Inference，一个面向 LLM 推理的实时拍卖路由系统。它让不同的推理供应商在实时竞价中承接请求，按价格与延迟动态分配流量，旨在为应用方降低推理成本、提升供给弹性。该方案属于推理基础设施层面的调度优化，反映 LLM 服务市场向更具价格发现机制的形态演进。
---

# Architect 推出 Liquid Inference：LLM 推理的实时拍卖路由

> 原文链接：https://www.marktechpost.com/2026/10/08/architect-launches-liquid-inference-a-real-time-auction-for-llm-inference/
> 来源：MarkTechPost

Architect Financial Technologies has launched Liquid Inference, an LLM router that runs a live auction for every request. Liquid Inference is an LLM inference marketplace from Architect where providers bid to serve each prompt. The buyer pays the lowest offer that meets its rules.  For developers, it is quite simple message: swap a base URL, keep your code, and let providers compete on price.

What is Liquid Inference?

Liquid Inference is an exchange-style router for LLM inference. According to Architect, providers post offers to serve specific models. Each request is auctioned across every provider quoting the named model. The lowest-priced offer that meets the buyer&#8217;s rules wins.

The product comes from a trading firm, not an AI lab. Architect runs the AX perpetual futures exchange. In May 2026 it acquired a US Designated Contract Market to list GPU compute futures, pending regulatory review. The team used its experience building financial exchanges to create two-sided price discovery for inference.

How does the inference auction work?

The flow has 4 steps:

Request: A client sends a standard OpenAI or Anthropic API call.

Rules: The buyer&#8217;s constraints filter eligible offers.

Auction: Providers quoting that model compete. The lowest qualifying offer wins.

Receipt: The max price is locked before generation. Billing covers metered usage only.

Buyers can set per-job cost caps, time to first token limits and minimum throughput. They can also require approved regions, zero data retention and provider or model allow lists. An Auto mode can pick the model for a given unit of work. Harrison&#8217;s LinkedIn post adds routing rule presets and full multi-modal support.

Account holders can view live order books, per-provider and per-model quotes, and cleared transactions. That level of market data is unusual for an LLM API.

What do buyers get?

Drop-in compatibility with agentic coding tools. The post lists Claude Code, Codex, OpenCode, Cursor, Pi and Cline.

Free email signup. The first 500 users get $20 of free inference, per Harrison.

A referral program: 20% of referred fees as free inference, plus 10% on second-level referrals.

What do inference providers get?

Providers onboard through the Liquid Inference app. Harrison says new providers are verified &#8220;in minutes, not weeks.&#8221; All prompts use the OpenAI API standard. A REST and WebSocket API registers models and quotes.

Providers can update quotes based on their own costs. That lets them sell spare GPU capacity only when they want. Payouts run through Stripe, with itemized records of every job.

How does Liquid Inference compare with OpenRouter and Hugging Face?

FeatureLiquid InferenceOpenRouterHugging Face Inference ProvidersRouting modelPer-request auction across quoting providers Price-weighted load balancing, inverse square of price Fastest provider by default; :cheapest suffix optional Model / provider count&#8220;Hundreds&#8221; of models; providers not disclosed500+ models, 80+ providers 18 listed partners API compatibilityOpenAI and Anthropic-compatibleOpenAI-compatibleOpenAI-compatible, chat only Price capMax price locked before first tokenmax_price parameter Not disclosedData controlsZDR, regions, allow listszdr, data_collection, only/ignore Provider preference orderPlatform feeNot disclosed5.5% card credit fee, $0.80 minimum No markup Free credits$20 for first 500 users Not disclosed$0.10/month free, $2.00 PRO Public market dataLive order books and cleared tradesNot disclosedNot disclosed

&

Key Takeaways

Liquid Inference auctions every LLM request across competing providers.

Max price is locked before the first token, with a per-job receipt.

Works with OpenAI and Anthropic clients, including Claude Code and Cursor.

First 500 users get $20 free; referrals earn 20% of fees.

Fees, provider list and latency data are not yet public.

Check out the Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Architect Launches Liquid Inference, a Real-Time Auction for LLM Inference appeared first on MarkTechPost.