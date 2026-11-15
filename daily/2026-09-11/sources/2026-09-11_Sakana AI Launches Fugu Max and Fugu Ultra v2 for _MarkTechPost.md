---
publish_time: 1789108479
link: https://www.marktechpost.com/2026/09/10/sakana-ai-launches-fugu-max-and-fugu-ultra-v2-for-cheaper-stronger-multi-agent-orchestration/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Sakana AI 发布 Fugu 系列两款新模型 Fugu Max 与 Fugu Ultra v2。Fugu 并非单一基座模型，而是一个「学习型编排器」：在单一 API 后跨多个模型路由任务。Fugu Max 追求每美元最优输出，Fugu Ultra v2 面向困难多步任务的最高能力。Sakana 以帕累托前沿框架说明——简单查询不应派给万亿参数大模型，应按任务成本与质量动态选路。两款均以托管 API 形式提供（无开放权重，不在欧盟提供）。
---

# Sakana AI 发布 Fugu Max 与 Fugu Ultra v2：更省更强的多智能体编排

> 原文链接：https://www.marktechpost.com/2026/09/10/sakana-ai-launches-fugu-max-and-fugu-ultra-v2-for-cheaper-stronger-multi-agent-orchestration/
> 来源：MarkTechPost

Sakana AI has released Fugu Max and Fugu Ultra v2, 2 new models in its Sakana Fugu family. Fugu is not a single foundation model. It is a learned orchestrator that routes work across a pool of other models behind 1 API. The new release tunes that architecture for 2 missions. Fugu Max targets the best output per dollar. Fugu Ultra v2 targets the highest capability on hard, multi-step tasks.

Is it deployable? Yes, as a hosted API. Both models are live today through Sakana&#8217;s OpenAI-compatible API. There are no open weights to self-host, and Sakana does not offer the service in the EU/EEA.

Why Sakana Frames This as a 2-Axis Problem

Sakana&#8217;s argument is direct. Real workloads are judged on capability and cost together. Sending a simple data lookup to a multi-trillion-parameter model wastes money. A better system picks the cheapest machinery that can still solve the task.

Sakana team describes this with the Pareto frontier. On that frontier, gaining quality costs more, and cutting cost loses quality. Fugu Max and Fugu Ultra v2 share 1 core orchestration architecture. Only the optimization target differs.

The release follows a fast cadence. Fugu entered beta in April, reached general availability in June, and added Fugu-Cyber and a Claude Code interface in July.

How Fugu Orchestration Works

The Sakana Fugu&#8217;s Technical Report describes Fugu models as language models in their own right. They read a query and build an agentic scaffold for it on the fly. Training combines large-scale fine-tuning, evolutionary algorithms, and reinforcement learning.

The system builds on 2 ICLR 2026 papers. TRINITY uses a lightweight evolved coordinator that assigns Thinker, Worker, or Verifier roles across turns. The Conductor is trained with reinforcement learning to discover natural-language coordination strategies and focused prompts.

Fugu Max: More Models, Less Cost

Fugu Max widens the pool of models Fugu can orchestrate. It adds a large set of open-weights and specialized models. That includes the NVIDIA Nemotron family, through Sakana&#8217;s collaboration with NVIDIA. Fugu Max routes each task to the leanest model capable of solving it.

Sakana team reports the following:

Pricing: $2 per 1M input tokens and $6 per 1M output tokens.

Output price: 40% to 60% lower than Sonnet 5, GPT 5.6 Terra, and Kimi K3.

Performance: Best overall score on 6 benchmarks: Terminal Bench 2.1, GPQA Diamond, AA-LCR, GDP.pdf, AutomationBench, and SWEFish.

Efficiency: Expands the cost-performance Pareto frontier on 7 of 10 benchmarks.

Sakana places Fugu Max within striking distance of elite models at 2x to 6x lower cost. SWEFish is an internal Sakana benchmark built from its own coding challenges. Treat that result as a vendor signal.

Fugu Ultra v2: Raising the Ceiling

Fugu Ultra v2 targets complex reasoning, autonomous research, and full-stack software development. Its largest gains appear on sustained reasoning over visual and structured data.

Chartography (visual reasoning and data interpretation): 48.3, versus 27.3 for Opus 5 and 29.5 for Fable 5.

DeepSWE (real-world software engineering): 74.3, ahead of models priced 3x to 5x higher per token.

Breadth: Best or joint-best on 5 of 8 benchmarks: GDP.pdf, Chartography, SWEFish, DeepSWE, and Toolathon.

Consistency: Top 2 on 7 of 8 benchmarks.

Fable 5, Fable 5.1, and GPT-6-Astra are not in Fugu Ultra v2&#8217;s agent pool. The model&#8217;s training cutoff is August 28, 2026. Sakana&#8217;s main message is frontier output without dependence on any 1 proprietary model. The research team states that this reduces exposure to vendor lock-in, API revocations, and sudden service cutoffs.

Interactive Explainer

&

Key Takeaways

Fugu Max costs $2/$6 per 1M input/output tokens and targets output per dollar.

Fugu Max posts the best overall score on 6 benchmarks and expands the frontier on 7 of 10.

Fugu Ultra v2 scores 48.3 on Chartography and 74.3 on DeepSWE.

Ultra v2 reaches these scores without Fable 5, Fable 5.1, or GPT-6-Astra in its pool.

Both ship today via an OpenAI-compatible API, with a 1-line switch for existing users.

Check out the Technical details and Project page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Sakana AI Launches Fugu Max and Fugu Ultra v2 for Cheaper, Stronger Multi-Agent Orchestration appeared first on MarkTechPost.