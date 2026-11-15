---
publish_time: 1791004193
link: https://www.marktechpost.com/2026/10/02/microsoft-ai-releases-mai-transcribe-2-streaming-1-real-time-speech-to-text-model-on-artificial-analysis/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  微软 AI 发布首款流式语音转写模型 MAI-Transcribe-2-Streaming，并同步推出 MAI-Voice-2.1 与 Flash 两款语音合成模型。该模型支持 60 种语言、连续语言检测，音频流入即流式回传文本，首字假设延迟约 100ms 并随上下文修正。Artificial Analysis 在 38 款模型中将其终稿与首字准确率均评为第一（终稿 WER 2.5% @ 0.13s）。其目标场景为语音 Agent、实时字幕与听写，让 Agent 能在用户说话中途就开始推理与调用工具。
---

# 微软发布 MAI-Transcribe-2-Streaming 实时语音转写模型，Artificial Analysis 评测居首

> 原文链接：https://www.marktechpost.com/2026/10/02/microsoft-ai-releases-mai-transcribe-2-streaming-1-real-time-speech-to-text-model-on-artificial-analysis/
> 来源：MarkTechPost

Microsoft AI has released MAI-Transcribe-2-Streaming, its first streaming speech-to-text (STT) model. It launched on October 1, 2026, alongside 2 text-to-speech models, MAI-Voice-2.1 and MAI-Voice-2.1-Flash. Artificial Analysis ranks it #1 of 38 models for final and first partial transcript accuracy. The model targets voice agents, live captions and dictation, where latency decides the experience.

What Microsoft Shipped

MAI-Transcribe-2-Streaming is the real-time sibling of the batch MAI-Transcribe-2, released in September. It transcribes 60 languages with automatic, continuous language detection. Audio streams in continuously, and text streams back while the speaker is still talking.

The model emits its first hypotheses, called partials, just over 100ms after receiving audio. It revises those partials as context arrives, then commits a stable final transcript. An agent can therefore start reasoning or calling tools mid-sentence. Microsoft team states its internal tests show words appearing 2x faster than its closest competitor. 

What Artificial Analysis Measured

The AA-WER Streaming index uses about 8 hours of audio. The mix is AA-AgentTalk (50%), VoxPopuli (25%) and Earnings22 (25%). Latency is timed from the end of speech, as detected by SileroVAD.

Final transcript: 2.5% WER at 0.13s after end of speech, #1 of 38 models.

First partial transcript: 2.5% WER at 0.12s after end of speech, also #1.

Runners-up: Grok Voice Transcribe 2.0 at 2.7% and 0.49s. Muse Voice Transcribe at 3.1% and 0.16s.

Not the fastest: Cartesia Ink-2 (external endpoints) returns finals in 0.07s, but at 4.0% WER.

The first partial is as accurate as the final transcript. That matters for agents that act before the speaker finishes. Microsoft also places the model on the accuracy versus latency Pareto frontier.

&

Pricing

MAI-Transcribe-2-Streaming costs $0.54 per hour of audio. This is an introductory price through the end of 2026. Artificial Analysis normalizes it to $9.00 per 1,000 minutes. Batch MAI-Transcribe-2 costs $0.10 per hour. On streaming, Microsoft charges more than xAI and Meta, and roughly matches Google&#8217;s estimated rate.

How Developers Integrate It

Microsoft documents 2 integration paths. The Realtime API suits apps already using an OpenAI Realtime-compatible WebSocket. The Azure Speech SDK handles connection management, retries and audio streaming. Both return intermediate and final results.

The model is also available in the MAI Playground, through Vercel and Azure Voice Live. LiveKit support is listed as coming soon.

Microsoft pairs it with MAI-Voice-2.1-Flash for full voice loops. Flash generates 45s of audio at 150ms end-to-end latency for $15 per 1M characters. MAI-Voice-2.1 covers 23 languages and 26 locales at $22 per 1M characters.

Comparison: MAI-Transcribe-2-Streaming vs Closest Streaming Competitors

FeatureMAI-Transcribe-2-StreamingGrok Voice Transcribe 2.0Muse Voice TranscribeGemini 3.5 Transcribe LiveDeveloperMicrosoft AIxAIMeta Superintelligence LabsGoogleReleasedOct 1, 2026Sep 18, 2026Sep 1, 2026Aug 26, 2026AA-WER Streaming (final)2.5%2.7%3.1%4.0%Time to final0.13s0.49s0.16sNot reported by AA source citedStreaming price / hour$0.54 (intro)$0.20$0.18~$0.54 (token-billed estimate)Languages60, continuous auto-detectDozens, auto-detect, mid-recording switch70+ trained, 25 verified85+, auto-detectSpeaker diarization in streamNot statedIncluded in API (streaming not confirmed)Yes, 20+ speakersNot supported in Live modeInterfaceRealtime API (WebSocket) + Azure Speech SDKWebSocketWebSocket + file endpointLive API (WebSocket)Open weightsNoNoNoNo

Sources: Artificial Analysis, 9to5Mac (Muse pricing), DataCamp (Grok pricing), The Batch (Gemini pricing). Verified October 2, 2026.

Key Takeaways

#1 of 38 on AA-WER Streaming: 2.5% WER at 0.13s to final.

First partials score the same 2.5% WER, at 0.12s.

60 languages with continuous automatic language detection.

$0.54 per hour introductory price, higher than xAI and Meta.

Public preview with no SLA and no open weights.

Check out the Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Microsoft AI Releases MAI-Transcribe-2-Streaming: #1 Real-Time Speech-to-Text Model on Artificial Analysis appeared first on MarkTechPost.