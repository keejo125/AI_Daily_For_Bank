---
publish_time: 1790564830
link: https://www.marktechpost.com/2026/09/27/20-agentic-use-cases-of-typesafe-ais-jev/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  TypeSafe AI 上周发布其首个 System One 模型 Jev，创始人 Diogo Almeida 曾任职 OpenAI 主导 ChatGPT 背后的指令跟随研究。Jev 不做对话、写代码或摘要，而是接收非结构化状态并返回带校准概率的类型化决策，天然适配 Agent 循环内成千上万次的微小判断——调用哪个模型、命令是否安全、段落是否相关、任务是否真的完成。其接口定义 Choice（从列表中选一并返回概率）、Score（按有序量规打分）、Noul（判断陈述为真的概率）三种原语，单次请求内并行评估同一状态的所有问题，并以强化学习校准决策（RLCD）训练，使高置信度对应高准确率。文章列举了 20 个 Agentic 落地场景。
---

# TypeSafe AI 的 Jev：20 个智能体应用案例

> 原文链接：https://www.marktechpost.com/2026/09/27/20-agentic-use-cases-of-typesafe-ais-jev/
> 来源：MarkTechPost

Last week, TypeSafe AI released Jev, its first System One model. Founder Diogo Almeida previously worked at OpenAI on the instruction-following research behind ChatGPT. 

Jev does not chat, write code or summarize. It takes unstructured state and returns typed decisions with calibrated probabilities. That makes it a natural fit for the thousands of small judgments inside an agent loop: which model to call, whether a command is safe, which passage is relevant, whether the agent is actually done.

How Jev Works

Every call sends a state (text or JSON) plus a dictionary of typed questions. TypeSafe&#8217;s docs define 3 primitives:

Choice picks one option from a list and returns a probability per option plus confidence.

Score rates the state on ordered rubric levels and returns probabilities plus confidence.

Noul returns the probability (0 to 1) that a statement is true.

All questions are evaluated in parallel against the same state in one request. TypeSafe trains Jev with Reinforcement Learning for Calibrated Decisions (RLCD), so higher confidence should track higher accuracy. Choice supports up to 255 options.

The main claims, 193.6x faster and 444.6x cheaper, come from TypeSafe&#8217;s own workflow evals. The launch post says these figures sit on the higher end of real-world gains and use GPT-6 Astra and Fable 5.1 as the reference answer.

Interactive Explainer

Race a token-by-token LLM against Jev&#8217;s single pass, move a confidence threshold to see how code gates each decision, estimate monthly cost, and browse all 20 use cases.

20 Agentic Use Cases for Jev

Routing and orchestration

Model routing: Score request difficulty, then send it to a fast or strong model. LangChain ships this as ModelRouterMiddleware; jev-router does it per turn for Claude Code and Codex.

Skill selection: TypeSafe&#8217;s skill suggestion cookbook picks at most one skill from 182 in Nous Research&#8217;s Hermes catalog using 2 requests.

Typed function calling: The function calling cookbook maps natural-language trading requests to function names and closed-set arguments, gated by confidence.

Ticket triage and intent routing: One call returns department, frustration and urgency. The intent routing pattern sends each request to deterministic logic, a specialist LLM or a human.

Safety and guardrails

Tool-call risk gating: pi-warden asks whether a pending bash, write or edit is irreversible or off-task. It tells db:reset after &#8220;reset the database&#8221; apart from db:reset after &#8220;add a column&#8221;. LangChain&#8217;s AutoModeMiddleware returns an error for risky calls.

Read-only auto-approval: jev-auto-approve is a Claude Code hook that auto-approves only at p ≥ 0.95 and approved 0 of 8 state-changing commands in its published calibration.

Secret-leak guard: jev-secret-guard sends masked strings to Jev and blocked 6 of 6 secrets and 0 of 6 benign strings in its calibration.

Prompt-injection screening: In TypeSafe&#8217;s RAG passages cookbook, cosine similarity ranked a planted injection first at 0.584. Jev scored it 0.99 and dropped it.

LLM input and output guardrails: The guardrails cookbook thresholds hazard probabilities to pass, review, block or route every message.

Retrieval and grounding

Reranking: On 40 CLERC legal queries, the reranking cookbook lifted top-1 accuracy from 5% to 18% and top-10 from 38% to 62%.

Citation verification: The citation check cookbook uses one Choice to decide whether a source section supports, contradicts or says nothing about a claim.

Computer, browser and real-time control

Browser agents: Browser Use&#8217;s Jev Ultrafast picks an operation and DOM element in one request and finished a Google Flights search in about 7.1 seconds.

Desktop computer use: typesafe-computer-use OCRs the macOS screen and lets Jev classify the next action for about $0.0002 per step.

Mobile agents: Mobile Jev decides each Android tap, reaching an Uber payment screen in about 21 seconds and 9 actions.

Real-time game agents: TypeSafe&#8217;s Doom demo runs about 10 queries per second, roughly $7 per hour, on structured game state.

Agent quality and memory

Loop stagnation detection: ProgressGate judges the trajectory, and code returns CONTINUE, WARN, REPLAN or HALT.

&#8220;Done&#8221; claim verification: jev-belay checks the transcript for evidence before trusting a Claude Code agent&#8217;s &#8220;done&#8221; claim.

Context compaction: fast-jev-compaction scores tool calls and drops stale ones instead of summarizing context.

Trace mining for memory: Beacon by Asymptote Labs uses Jev to find which runs across Claude Code, Codex, Cursor and OpenCode are worth turning into reusable skills.

Semantic linting: jev-lint flags team-rule violations at edit time for Claude Code and Codex.

Jev vs Closest Competitors

FeatureJev 1.13 (TypeSafe)Laya (open)kev (open)Claude Opus 5 (LLM)Model typeSystem One decision modelEncoder decision model (ModernBERT-large)LoRA + readout head on Qwen2.5-0.5BGenerative LLMWeights / licenseClosed, hosted APIApache 2.0, 421M and 322M paramsApache-2.0 (base uses Qwen license)Closed, hosted APIChoice / Score / NoulYesYesYesVia structured prompting/v1/systemone compatible NativeYesYesNoOutput guaranteeSchema-bound, no type errorsTyped answers over declared optionsTyped answers over declared options0 of 3,080 invalid in OpenRouter testCalibrationRLCD-trained confidenceConfidence returnedHeld-out ECE 0.065Prompted estimates, not guaranteed calibratedMax Choice options255Degrades past 50255n/aLatency70 to 500 ms (vendor); 175 ms median (OpenRouter)32.8 ms single question, local (self-reported)~160 ms, 6 questions, local (self-reported)2,266 ms median (OpenRouter)Banking77 accuracy81.0% (OpenRouter)Not comparable (0.425 at defaults, own harness)0.860 on 77-way (own held-out set)84.4% (OpenRouter)Price$0.042/MTok input, output freeFree, self-hostedFree, self-hosted$2.42 per 1,000 requests vs $0.11 for Jev (OpenRouter)DeploymentTypeSafe, Vercel AI Gateway, OpenRouterpip, local CPU or GPULocal serverAPI

Open-model figures are self-reported by each project on its own harness, so treat them as directional. OpenRouter&#8217;s Banking77 test is the cleanest head-to-head: Jev was 3.3 points less accurate than Claude Opus 5, 13x faster at the median, and about 1/22 the cost.

Key Takeaways

Jev returns typed Choice, Score and Noul answers with probabilities, never free text.

TypeSafe lists $0.042 per million input tokens, free output, and 70 to 500 ms latency.

Best agent fits: routing, tool-call gating, reranking, citation checks and injection screening.

On Banking77, Jev scored 81.0% vs 84.4% for Claude Opus 5, at 13x lower median latency.

Schema-safe does not mean correct: calibrate thresholds on your own traffic first.

FAQ

What is Jev? Jev is TypeSafe AI&#8217;s first System One model. It returns typed Choice, Score and Noul answers with probabilities instead of generated text.

Is Jev an LLM replacement? No. It sits beside an LLM. The LLM plans and writes; Jev handles bounded decisions such as routing, gating and verification.

How much does Jev cost? TypeSafe lists $0.042 per million input tokens, with output tokens free.

Can I run Jev locally? Not TypeSafe&#8217;s model. Open projects like Laya and kev implement the same /v1/systemone interface on your own hardware.

The post 20 Agentic Use Cases of TypeSafe AI&#8217;s Jev appeared first on MarkTechPost.