---
publish_time: 1789843293
link: https://www.marktechpost.com/2026/09/19/typesafe-ai-releases-jev/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  TypeSafe AI发布Jev——一个基于Transformer但并非大语言模型的“System One模型”。与生成自由文本不同，Jev返回的是类型化、经过校准的结构化决策结果，而非自然语言。其设计目标是让AI直接“与软件对话”而非“与人对话”，适用于需要确定性输出的系统控制与自动化场景。文章指出，2022年ChatGPT让AI学会与人交流，而Jev试图开启AI与软件交互的新范式，是模型形态从生成式走向决策式的一次探索。
---

# TypeSafe AI 发布 Jev：返回类型化校准决策的 System One 模型

> 原文链接：https://www.marktechpost.com/2026/09/19/typesafe-ai-releases-jev/
> 来源：MarkTechPost

The ChatGPT moment in 2022 taught AI to talk to people. One of its builders now bets the next moment is AI that talks to software, not people. TypeSafe AI released Jev. Jev is transformer-based, but it is not a large language model. It does not generate text. You send a state and typed questions. It returns typed decisions with probabilities that code can branch on.

Is it deployable? Yes, as a hosted API in early access behind a waitlist. TypeSafe has not published weights, a parameter count, or a self-hosting option.

What is a System One Model?

The name borrows from Daniel Kahneman&#8217;s split between fast intuition and slow reasoning. TypeSafe team argues RLHF tuned models for human preference. That produced chat, and overconfidence and mode dropping. Those flaws keep a human in the loop.

Jev uses a new stack: a new architecture, a parallel sampler, and Reinforcement Learning for Calibrated Decisions (RLCD). TypeSafe has not disclosed the architecture. 

How the Jev API Works

One endpoint handles everything: POST https://api.typesafe.ai/v1/systemone. The body carries state, model, and a map of questions. The docs define 3 question types.

PrimitiveAsksReturnsChoicePick 1 option from a listchoice, probabilities, confidenceScoreRate against ordered levelsscore, probabilities, confidenceNoulIs this statement true?noul, a probability from 0 to 1

Questions run in parallel and in isolation against the same state. TypeSafe says adding questions barely changes response time. A Choice supports up to 255 options.

Copy CodeCopiedUse a different Browser

from typesafe_sdk import Choice, Noul, TypeSafeClient

client = TypeSafeClient()  # reads TYPESAFE_API_KEY
r = client.system_one(
    state=ticket,
    questions={
        "department": Choice(
            instructions="Which team should handle this",
            criteria={"billing": "Payment issues", "technical": "Bugs"},
        ),
        "is_urgent": Noul(instructions="The message conveys urgency"),
    },
)
print(r.answers["department"].choice, r.answers["is_urgent"].noul)

Install with pip install typesafe-sdk (Python 3.10 or later). A JavaScript SDK ships as @typesafe-ai/sdk. The quickstart also covers cURL and an agent skill for Claude Code.

Confidence is the Product

Every Choice and Score answer carries a confidence value from 0 to 1. TypeSafe derives it from the shape of the probability distribution. In the docs example, billing wins at 0.84. Confidence is only 0.596, because technical still holds 0.159.

The docs suggest 3 paths. Act on high confidence. Review the middle. Send low confidence to a human. Thresholds should scale with the cost of a wrong action.

Pricing, Speed, and the Benchmark Fine Print

Jev costs $42 per billion input tokens. TypeSafe quotes existing LLMs at $0.20 to $10 per 1M input tokens. In its recorded demo, Jev finished in 0.114s for $0.000081. GPT-5.6 Terra took 8.566s for $0.013880.

The TypeSafe team claims it to be 193.6x faster and 444.6x cheaper. Those figures come from TypeSafe&#8217;s own workflow evals. But hold on here are some things to keep in mind:

The reference answer is the average of GPT-6 Astra and Fable 5.1.

TypeSafe&#8217;s capabilities team wrote the workflows.

TypeSafe expects these gains to sit at the high end of real use.

TypeSafe says it cannot prove the price is unsubsidized.

&#8216;Zero hallucinations&#8217; means schema matching is guaranteed. The 0% figure is not empirical. Answers can still be wrong.

What Developers are Building with Jev

Community projects appeared within days of launch. Here are some examples:

Command safety: Vercel CEO Guillermo Rauch reported Jev up to 18x faster at p95 than GPT Luna, and more accurate. His post said the fx reviewer still ran on Luna. Engineer Pranit Sharma shared the benchmark.

Email triage:Bryo AI CTO Nikhil Mudholkar found Gemini slightly more accurate, but 10 to 20 times more expensive.

Browser agents: Browser Use&#8217;s jev-ultrafast ran a Zürich to London Google Flights search in 7.1 seconds (video).

Phone agents: Droidrun&#8217;s mobile-jev drove Uber on a real Android phone: 9 actions in about 21 seconds (video). No booking was completed.

Video scoring: jevmeter scores every sentence of a debate for about $0.05 (demo on X).

Live typing: Steve Krouse&#8217;s Typewriter updates 16 judgments as you type (try it).

Games: Jev completed StarCraft&#8217;s first combat mission (video). It also runs the guards in heist-one (video).

Agent guardrails: jev-guard rates each tool call as deny, ask, or allow (78-second video).

Data and homes: pg-jev adds plain-language filters to Postgres. HA-Jev turns answers into Home Assistant entities.

Interactive Explainer

&&&

Key Takeaways

Jev outputs typed decisions with probabilities, not strings.

3 primitives (Choice, Score, Noul) can share 1 request.

Input costs $0.042 per 1M tokens. Output tokens are free.

TypeSafe reports 70ms to 500ms end-to-end response times.

The main benchmarks are vendor-run. Test on your own data.

Check out the launch post, docs, and TypeSafe&#8217;s GitHub. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post TypeSafe AI Releases Jev: A System One Model That Returns Typed, Calibrated Decisions Instead of Text appeared first on MarkTechPost.