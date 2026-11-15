---
publish_time: 1792562592
link: https://www.marktechpost.com/2026/10/20/mistral-voxtral-3-speech-models-voice-agent-sdk/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Mistral AI 发布 Voxtral 3 语音模型家族及基于 LiveKit 的语音智能体 SDK，包含 3 个转录模型、1 个 TTS 模型与 1 套 SDK，均处于 Mistral API 公开预览。转录模型支持说话人分离（diarization）与上下文偏置，批处理覆盖 50 种语言；Small Transcribe 3 在 Artificial Analysis 上达 2.1% AA-WER（排名第 3），说话人分离 cpWER 18.4% 领先 Pyannote 与 MAI；实时转写以延迟换精度（240ms 下 FLEURS 35 WER 7.4%，落后于 Gemini 3.5 Realtime 的 4.2%）。TTS（Voxtral Speech 3）每百万字符 13 美元，支持情绪/节奏/重音控制与约 90ms 首音频延迟。语音智能体 SDK 将“听—推理—说话”合为一条流式管线，每轮低于 1 秒。批处理转录约 0.0035–0.004 美元/分钟，未发布开源权重。
---

# Mistral 发布 Voxtral 3：语音识别、语音合成与语音智能体 SDK

> 原文链接：https://www.marktechpost.com/2026/10/20/mistral-voxtral-3-speech-models-voice-agent-sdk/
> 来源：MarkTechPost

Mistral AI just released Voxtral 3. Mistral Voxtral 3 is a speech model family paired with a voice agent SDK. It ships 3 transcription models, 1 text-to-speech model and an SDK built on LiveKit. One place for listening, reasoning, tool calls and speaking. All 4 models are in public preview on the Mistral API.

TL;DR

Size: Voxtral Mini Transcribe 3 has 4B parameters. Small Transcribe 3 size: not disclosed. Both batch models list a 32k context.

Runs on: Mistral API (EU, US and global endpoints) or your own infrastructure via Mistral sales. GPU and VRAM needs: not disclosed. Mistral says Mini suits resource-constrained environments.

Performance: Top 3 on independent speech-to-text rankings, strongest on diarization and multilingual batch transcription.

Best: 2.1% AA-WER for Small Transcribe 3, #3 on Artificial Analysis.

Worst: Realtime at 240 ms: 7.4% WER on FLEURS 35, vs 4.2% for Gemini 3.5 Realtime.

What is in the Voxtral 3 family?

Mistral lists 4 models and 1 SDK:

Voxtral Small Transcribe 3: flagship batch transcription and diarization. Docs also list translation, speech Q&A, summarization and function calling.

Voxtral Mini Transcribe 3: a 4B model for cheaper, faster batch jobs.

Voxtral Mini Transcribe Realtime 3: streaming ASR over WebSocket with end-of-turn detection.

Voxtral Speech 3: text-to-speech, also called Voxtral Mini TTS 3 in the post.

All transcription models support diarization and context biasing. Context biasing takes key terms or free text to improve recall. Batch transcription covers 50 languages, including 24 official EU languages.

How does the Voxtral voice agent SDK work?

The SDK is built on LiveKit and runs 3 stages as 1 streaming pipeline. Realtime Transcribe 3 listens and detects when the caller stops speaking. A general LLM, such as Mistral Small 4, reasons and calls tools. Voxtral Speech 3 replies in the tone of the conversation so far.

Each turn completes in under 1 second. The agent stops talking when the caller cuts in. It handles phone calls over SIP and browser or app sessions over WebRTC. Because each stage is a separate model, teams can swap the LLM, voice or language. 

&&

How accurate is Voxtral Transcribe 3?

These numbers are self-reported by Mistral:

FLEURS 45 (WER, forced / inferred language): Small 4.1% / 4.0%. MAI-Transcribe-2 ties at 4.1% / 4.0%. Mini 4.6% / 4.5%. Whisper large-v3 16.0% / 14.9%.

Diarization (cpWER, 5 public sets): Small 18.4% and Mini 18.6%. Pyannote scores 19.0% and MAI-Transcribe-2 20.3%.

Keyphrase recall (Earnings 22): Small 94.6% with context, 81.4% without. Scribe v2 posts 94.3% and 84.0%.

On Artificial Analysis, Small scores 2.1% AA-WER and Mini 2.2%. Only Fun-Realtime-ASR-preview (1.7%) and MAI-Transcribe-2 (2.0%) rank higher. Speed is the gap: Small&#8217;s speed factor is 65.8x, against 307.5x for MAI-Transcribe-2.

How do realtime transcription and TTS compare?

On FLEURS 35, the realtime model trades latency for accuracy. It scores 5.7% WER at 2,400 ms and 6.4% at 480 ms. At 240 ms, WER rises to 7.4%. Gemini 3.5 Realtime Transcribe scores 4.2% and MAI-Transcribe-2 Streaming 5.8%. GPT Live Transcribe (8.4%) and Scribe v2 Realtime (8.7%) trail every Voxtral setting.

Voxtral Speech 3 costs $13 per 1M characters. Mistral says that undercuts OpenAI TTS-1, Deepgram, ElevenLabs Flash and Gemini Flash. Explicit controls cover emotion, pacing and emphasis. The model page lists ~90 ms time-to-first-audio and 34 emotion tags. Pro Voice adapts a speaker&#8217;s style from 30 minutes of audio. Artificial Analysis places it in the top 12 of both TTS arenas.

Voxtral 3 vs MAI-Transcribe-2, Scribe v2 and Gemini 3.5 Transcribe

Voxtral Small Transcribe 3MAI-Transcribe-2ElevenLabs Scribe v2Gemini 3.5 TranscribeDeveloperMistral AIMicrosoft AIElevenLabsGoogleParametersNot disclosed (Mini: 4B)Not disclosedNot disclosedNot disclosedLanguages506090+85+FLEURS 45 WER, forced / inferred (Mistral)4.1% / 4.0%4.1% / 4.0%4.9% / 4.9%6.1% / 4.5%Diarization cpWER (Mistral)18.4%20.3%23.0%38.4%AA-WER (Artificial Analysis)2.1%2.0%2.2%2.6%AA speed factor (Artificial Analysis)65.8x307.5x65.4x89.5xPrice per 1,000 min (Artificial Analysis)$4.00$1.67$3.67$5.00Vendor list price$0.004/min$0.10/hour, limited-time offer$0.22/hourToken-billed, see Google pricing

How much does Voxtral 3 cost, and where can you run it?

Per Mistral&#8217;s price table:

Voxtral Mini Transcribe 3 (batch): $0.0035/min

Voxtral Small Transcribe 3: $0.004/min

Voxtral Mini Transcribe Realtime 3: $0.008/min

Voxtral Speech 3 (batch and realtime): $13 per 1M characters

Voice agent API: $0.04/min with Mistral Small 4, $0.08/min with any other reasoning model

The models run on Mistral&#8217;s European, US and global endpoints. OpenRouter also lists all 3 new models with EU-hosted, zero-data-retention endpoints. 

Key Takeaways

Voxtral 3 bundles 3 ASR models, 1 TTS model and a LiveKit voice agent SDK.

Small Transcribe 3 hits 2.1% AA-WER, #3 on Artificial Analysis.

Best-in-chart diarization: 18.4% cpWER, ahead of Pyannote and MAI-Transcribe-2.

Batch transcription costs $0.0035 to $0.004 per minute; TTS costs $13 per 1M characters.

Realtime accuracy trails Gemini 3.5 Realtime, and no open weights were announced.

Check out the Voxtral 3 announcement, the audio docs and the model pages. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Mistral AI Releases Voxtral 3: Speech-to-Text, TTS and a Voice Agent SDK appeared first on MarkTechPost.