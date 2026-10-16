---
publish_time: 1792041534
link: https://www.marktechpost.com/2026/10/14/meet-grok-voice-3-0-spacexai-voice-agent-model-ranks-1-on-artificial-analysis/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  SpaceXAI发布Grok Voice 3.0，一个语音到语音模型，可听、推理、调用工具并说话，以86.9分登顶Artificial Analysis语音到语音指数（第1）。端点、事件与每分钟0.08美元价格沿用Grok Voice 2.0，仅提供托管API，无开放权重。
---

# SpaceXAI 发布 Grok Voice 3.0：语音到语音模型登顶 Artificial Analysis 语音指数

> 原文链接：https://www.marktechpost.com/2026/10/14/meet-grok-voice-3-0-spacexai-voice-agent-model-ranks-1-on-artificial-analysis/
> 来源：MarkTechPost

SpaceXAI just released Grok Voice 3.0. Grok Voice 3.0 is a SpaceXAI speech-to-speech model that listens, reasons, calls tools and speaks. It now ranks first on the Artificial Analysis Speech-to-Speech Index with a score of 86.9. For developers, the endpoint, events and $0.08 per minute price are unchanged from Grok Voice 2.0.

TL;DR

Runs on: SpaceXAI&#8217;s hosted Voice Agent API only. No open weights, no local or quantized variants.

Performance: Highest Index score of any model Artificial Analysis currently ranks.

Best: 86.9 on the AA Speech-to-Speech Index, ranked #1.

Worst: 71.6% on τ-Voice, behind GPT-Live-1 (Astra, medium) at 74.5%.

Bottom line: 

Best: top composite score at 0.81 s time to first audio. 

Worst: not the leader on agentic task resolution or raw speech reasoning.

What is Grok Voice 3.0?

Grok Voice 3.0 is SpaceXAI&#8217;s flagship realtime voice model, exposed as grok-voice-3.0 on the /v1/realtime WebSocket endpoint. The grok-voice-latest alias already points to it, so existing agents switched automatically.

SpaceXAI has not published parameter counts or architecture details. Reasoning is on by default (reasoning.effort: "high") and can be set to "none" for faster turns. Server-side voice activity detection handles barge-in. Tools run inside the session: collections search, web search, X search, remote MCP servers and custom functions.

How does Grok Voice 3.0 perform on benchmarks?

The AA Speech-to-Speech Index is an equal-weighted average of 4 components. Those are Big Bench Audio reasoning, τ-Voice agentic performance, Speech Agent Arena preference and task success rate.

Grok Voice 3.0 scores 86.9. GPT-Live-1 (Astra, medium) scores 83.2, Gemini 3.8 Live Extended Thinking 82.6. Grok Voice 2.0 scored 81.3.

Component results are strong, not uniformly first:

Big Bench Audio: 98.5%, ranked 4th. StepAudio 3 Realtime leads at 99.7%.

Full Duplex Bench: 97.0%, ranked 4th. StepAudio 3 Realtime leads at 98.9%.

Task success rate: 94.8%, up from 94.6% for Grok Voice 2.0.

Speech Agent Arena Elo: 1070, the highest among the 4 models compared here.

τ-Voice: 71.6%, up from 56.5%, but below GPT-Live-1 (Astra, medium) at 74.5%.

ServiceNow&#8217;s EVA-Bench scores enterprise voice agents on accuracy and experience. SpaceXAI reports a top accuracy score of 74%.

Is Grok Voice 3.0 fast and cheap?

Artificial Analysis measures 0.81 s time to first audio. GPT-Live-1 (Astra, medium) measures 1.34 s, so SpaceXAI&#8217;s &#8220;40% lower latency&#8221; claim checks out. Grok Voice 2.0 was faster, though, at 0.70 s.

On cost, SpaceXAI cites Artificial Analysis cost per Big Bench Audio task. Grok Voice 3.0 costs $0.025 per task, versus $0.030 for GPT-Live-1 (Astra, medium) and $0.055 for GPT-Realtime-2.1 (High). On AA&#8217;s cost per hour of input audio, Gemini 3.8 Live Extended Thinking is cheaper: $3.50 versus $4.80.

List prices are not directly comparable. GPT-Live-1 costs $0.05 per minute, but backend model and tool usage is billed separately. Gemini 3.8 Live bills audio per minute plus text tokens.

How does Grok Voice 3.0 compare to GPT-Live-1 and Gemini 3.8 Live?

FeatureGrok Voice 3.0Grok Voice 2.0GPT-Live-1 (Astra, medium)Gemini 3.8 Live Extended ThinkingDeveloperSpaceXAISpaceXAIOpenAIGoogleParametersNot disclosedNot disclosedNot disclosedNot disclosedContext lengthNot disclosedNot disclosedNot disclosedNot disclosedWeightsClosed, API onlyClosed, deprecatedClosed, API onlyClosed, API onlyInput / outputAudio, text / audio, textAudio, text / audio, textAudio, text / audio, textText, image, video, audio / audio, textAA Speech-to-Speech Index86.981.383.282.6Big Bench Audio98.5%97.2%90.1%97.7%τ-Voice71.6%56.5%74.5%68.6%Full Duplex Bench97.0%95.1%94.9%91.9%Task success rate94.8%94.6%87.4%89.1%Arena Elo (AA live)107010111056993Time to first audio0.81 s0.70 s1.34 s1.35 sAA cost per hour input audio$4.80$4.80$5.83$3.50List price$0.08/min$0.08/min$0.05/min plus backend usage$0.005/min audio in, $0.018/min audio out, plus text tokens

Benchmark data: Artificial Analysis, accessed October 14, 2026. SpaceXAI&#8217;s blog lists frozen Arena Elo values of 1048 (GPT-Live-1) and 990 (Gemini).

How do developers deploy Grok Voice 3.0?

The API is compatible with the OpenAI Realtime API, so migration mostly means a new URL and key.

Transports: WebSocket, WebRTC demo apps, and SIP for phone and contact-center calls.

Audio: PCM at 8 to 48 kHz, G.711 μ-law and A-law, and Opus.

Voices: 28 built-in voices, plus custom voices cloned from a reference clip of up to 120 s.

Languages: 20 listed locales with automatic language detection.

Extensions: force_message for scripted lines, pronunciation replace maps, and 30-minute session resumption.

Compliance: SOC 2 Type II, HIPAA eligible with a BAA, and GDPR. SpaceXAI says audio is not stored or used for training.

Production teams should pin grok-voice-3.0 rather than the alias. Grok Voice 2.0 is now deprecated.

Key Takeaways

Grok Voice 3.0 ranks #1 on the AA Speech-to-Speech Index at 86.9.

It answers in 0.81 s, 40% lower latency than GPT-Live-1 (Astra, medium).

τ-Voice jumped to 71.6%, but GPT-Live-1 still leads at 74.5%.

Price stays at $0.08 per minute, and grok-voice-latest upgraded automatically.

It is API only: no weights, no disclosed size.

Check out the official announcement, the Speech to Speech docs and the Artificial Analysis leaderboard. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Meet Grok Voice 3.0: SpaceXAI Voice Agent Model Ranks #1 on Artificial Analysis appeared first on MarkTechPost.