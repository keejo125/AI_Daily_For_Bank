---
publish_time: 1786208679
link: https://www.marktechpost.com/2026/08/08/pokee-ai-releases-pokee-isaac-28b-a-10m-token-context-agentic-model-built-to-run-inside-the-customer-boundary/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Pokee AI发布Pokee-Isaac 28B，一款1000万token超长上下文智能体模型。最大亮点：模型设计为在客户边界内本地运行，无需将数据发送到第三方API，满足企业数据主权和合规需求。支持10M token上下文窗口，适合长期对话、大型代码库分析、多轮Agent工作流等场景。
---

# Pokee AI Releases Pokee-Isaac 28B: A 10M-Token Context Agentic Model Built to Run Inside the Customer Boundary

> 原文链接：https://www.marktechpost.com/2026/08/08/pokee-ai-releases-pokee-isaac-28b-a-10m-token-context-agentic-model-built-to-run-inside-the-customer-boundary/
> 来源：MarkTechPost

Long-horizon agents accumulate context faster than they resolve tasks. Every tool output, observation, and intermediate reasoning step stays in the window, and the two capabilities that matter — holding that context and staying coherent across it — have so far been available almost exclusively from cloud endpoints. That excludes regulated industries, public-sector institutions, and on-device applications, where the data is not permitted to leave the boundary at all. Pokee AI released Pokee-Isaac 28B, a 28B text-only foundation model with a 10M-token context window, designed to run inside that boundary. The Pokee research team claims 93.3% on RULER at 10M tokens, parity with the strongest cost-optimized cloud baselines on agentic benchmarks, and a serving profile that fits a single GPU.

Is it deployable

Yes — but licensed, not open-weight. Pokee AI serves Isaac through an OpenAI-compatible developer API, and licenses it for deployment inside a VPC, on-premises, or on-device. The launch announcement advertises Day-0 support for vLLM and SGLang, and single-GPU serving starting from an RTX 4090 or equivalent. The research team publishes measurements only from a single B200-class GPU, so treat the consumer-GPU claim as vendor guidance rather than a reported result.

Company level: This fits organizations that already own their inference stack — mid-size and enterprise teams with a platform group, plus device OEMs. A solo practitioner without on-prem hardware should use the hosted API instead; the boundary argument only pays off if you have a boundary.

Industries: Healthcare and payors, financial services and insurance, defense and public sector, legal and e-discovery, and pharma or semiconductor R&D. The common trait is a rule that the data cannot cross an external API boundary, not a preference for privacy.

Applications: Whole-repository code review, multi-year contract and claims analysis, incident forensics over full log archives, and long-running tool agents that never need summarization or context pruning. The research paper makes this second point explicitly: when enough usable context is available in-boundary, memory hierarchies and compression become optional rather than required.

Long-context results

On RULER, Isaac stays above 93.3% at every tested length, ending at 93.3% at 10M. GPT-5.6 Luna and Gemini 3.5 Flash Lite track it to 512K, then hit context-overflow at 1M. 

On MRCR v2 with 8 needles, Isaac scores 0.607, 0.743, and 0.500 at 256K, 512K, and 1M. Its margin over Gemini widens from 0.133 to 0.295 across that sweep. 

Agentic and security results

Isaac leads BFCL v4 at 70.94 against Luna&#8217;s 70.61. The report calls that parity rather than a lead, which is the correct read. On τ³-bench it averages 0.662 across four domains, ahead of Gemini&#8217;s 0.631, with banking at 0.186 for everyone&#8217;s difficulty. On MCP-Atlas it places third at 74.59% coverage, but uses 9.10 turns per task against Gemini&#8217;s 14.99. On Terminal-Bench 2.1 it resolves 56 of 86 text-compatible tasks (65.1%), behind Luna&#8217;s 60. That is the one benchmark a cloud baseline wins, and the report states it plainly.

On DTAP red-teaming, Isaac records the lowest direct (36.0), indirect (35.2), and combined (35.6) attack success rates, with 82.5 benign success. One condition differs: baselines ran under the stock runner, Isaac under the Pokee harness.

Efficiency, pricing, and portability

Under the RULER workload on one B200-class GPU, TTFT is 23.6s at 1M and 72.9s at 10M. Prefill throughput rises with context, from 42,400 to 137,200 tokens/s, so a ten-fold longer prompt costs roughly three times the TTFT. List pricing is $0.15/$1.00 per million input/output tokens, marked provisional. Isaac also runs fully on-device on Intel Arc Pro B70 and Core Ultra Series 3 (Panther Lake), and on Qualcomm Snapdragon X2 Elite. 

Key Takeaways

Pokee-Isaac 28B scores 93.3% on RULER at 10M tokens; every baseline in its panel returns 0.0 beyond 2M.

Prefill reaches 137,200 tokens/s at 10M context on one B200; decode holds flat near 335 tokens/s.

It leads BFCL v4 (70.94) and τ³-bench (0.662 avg), places second on Terminal-Bench 2.1, third on MCP-Atlas.

Lowest combined attack success rate on DTAP (35.6) while keeping 82.5 benign task success.

Weights are not published; deployment is licensed into VPC, on-premises, or on-device.

Check out the Blog and Paper. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Pokee AI Releases Pokee-Isaac 28B: A 10M-Token Context Agentic Model Built to Run Inside the Customer Boundary appeared first on MarkTechPost.