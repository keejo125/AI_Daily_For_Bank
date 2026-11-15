---
publish_time: 1794372233
link: https://www.marktechpost.com/2026/11/10/fish-audio-live-3-full-duplex-voice-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Fish Audio 发布 Live 3，一款面向实时语音智能体的全双工语音模型，在说话时保持聆听， caller 可停顿、附和或改口而不中断通话，将轮次切换从手工编排的规则移入语音模型本身。提供托管 Fish Agent Platform、Fish Audio API 及企业本地部署。
---

# Fish Audio 发布 Live 3 全双工语音模型，响应延迟 186 毫秒

> 原文链接：https://www.marktechpost.com/2026/11/10/fish-audio-live-3-full-duplex-voice-model/
> 来源：MarkTechPost

Fish Audio has released Live 3, a full-duplex voice model built for real-time voice agents. The Fish Audio Live 3 full-duplex voice model keeps listening while it speaks. That lets a caller pause, say &#8220;mm-hmm,&#8221; or change their mind without breaking the call. For developers, the pitch is simple. Turn-taking moves out of hand-tuned pipeline rules and into the speech model.

TL;DR

Product: A full-duplex voice model built for real-time voice agents

Runs on: Hosted Fish Agent Platform and Fish Audio API; on-premises for enterprises. 

Performance: Fish Audio shows behavior demos, but publishes no benchmark scores.

Best: Can decide to respond in as little as 186 ms for short reactions like &#8220;mm-hmm.&#8221;

What is Fish Audio Live 3?

Live 3 is a full-duplex voice model from Fish Audio that listens and speaks at the same time. 

The core argument is that speed and timing are different problems. An agent can reply fast and still speak at the wrong moment. A pause after &#8220;What time do you open?&#8221; usually ends a turn. A pause in the middle of a phone number does not.

How does Live 3 handle turn-taking?

Most voice agents split recognition, reasoning, speech generation and turn-taking across separate pipeline stages. Fish Audio team states that Live 3 moves conversational timing into the speech model. It was trained on real human conversations to learn when to acknowledge, wait, respond or stop.

They framed the old approach as piling on &#8220;more rules and more thresholds.&#8221; Fish Audio instead wants the model to learn timing from data. A separate reasoning layer still holds the agent&#8217;s instructions and tools.

The Fish Audio team walks through 3 behaviors:

Acknowledging without taking over. A caller reads &#8220;415… 555… 0132.&#8221; Live 3 may say &#8220;okay, 415&#8221; between chunks, then wait.

Telling a backchannel from an interruption. A caller saying &#8220;yeah&#8221; lets the agent continue. &#8220;Wait, actually, I just need Thursday&#8221; makes it stop.

Waiting through corrections. For &#8220;two pizzas… no, three,&#8221; Live 3 waits instead of logging the wrong order.

How fast is Live 3?

Fish Audio states Live 3 can decide to respond in as little as 186 ms. That figure covers short reactions such as &#8220;mm-hmm,&#8221; &#8220;okay&#8221; and quick confirmations. The full answer is prepared in parallel.

This is a floor for small reactions, not time-to-first-audio for a complete reply. Fish Audio has not published a latency distribution. Third-party tracker OrcaRouter also reports no Artificial Analysis score for Live 3 as of November 11.

&

How do developers deploy Live 3?

Live 3 is available on the Fish Agent Platform, through the Fish Audio API, and on-premises for enterprises. The Agents platform is in public beta.

Agents expose a REST surface under /v1/agent/*. Browser sessions run through @fishaudio/agent-client or @fishaudio/agent-react. Agents can answer phone numbers, connect over WebRTC, or sit in a website widget. The Live 3 page lists 2,000,000+ library voices, including cloned voices.

A pending docs pull request shows Live 3 enabled with voice.engine: "live3". With it on, speech recognition is fixed to fish_audio:transcribe-stream-1. Fish Audio&#8217;s current docs say that model also classifies overlaps as interruptions or acknowledgements.

How much does Live 3 cost?

The Live 3 page lists $0.035 per minute, down 50% from $0.07, until December 31, 2026. It says the plan includes Live 3. The pricing docs say the $0.07 list rate covers STT, TTS, basic LLMs, knowledge retrieval and tool calls.

Phone calls add $0.01 per minute. A number costs $1.20 per month. New accounts get a $5 trial balance.

How does Live 3 compare with other full-duplex voice models?

MetricsFish Audio Live 3OpenAI GPT-Live-1Eleven Realtime v1 MaxGemini 3.8 LiveDesignFull duplex, timing learned in the speech modelFull duplex, delegates reasoning to a backend modelCascaded, tuned end to endLive dialogue model, runs tools in the backgroundLanguagesEnglish onlyNot disclosed90+97Published timing186 ms minimum (short reactions)Not disclosed in post text0.57 s avg time to first audioNot disclosedTurn-taking scoreNot published+30 pp Full Duplex Bench vs GPT-Realtime-2.1 (self-reported)94.1% Full-Duplex-BenchNot disclosedReasoning / agent scoreNot published#1 on Tau3 with GPT-6 Astra (medium)98.8% Big Bench Audio; 87.1% tool tasksExtended Thinking: 97.7% Big Bench Audio; 68.6% τ-VoicePrice$0.035/min promo, $0.07 list (incl. STT, basic LLM, TTS)$0.05/min voice layer + backend tokensSession time + tokensNot disclosed in launch postDeploymentAgent Platform, API, on-premAPI, telephonyElevenAgents, Realtime APIGemini API, AI Studio, Gemini Enterprise (preview)

ElevenLabs scores come from Artificial Analysis, as reported by ElevenLabs. OpenAI and Google figures are self-reported.

Key Takeaways

Live 3 is Fish Audio&#8217;s full-duplex voice model for phone and web agents.

It learns turn-taking from real conversations instead of silence thresholds.

Short reactions can start in as little as 186 ms.

Agents cost $0.035 per minute until December 31, 2026, then $0.07.

English only, with no published benchmark scores yet.

Check out the launch post, try it at fish.audio/live3, and see the Agents docs. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Fish Audio Releases Live 3, a Full-Duplex Voice Model That Reacts in 186 ms appeared first on MarkTechPost.