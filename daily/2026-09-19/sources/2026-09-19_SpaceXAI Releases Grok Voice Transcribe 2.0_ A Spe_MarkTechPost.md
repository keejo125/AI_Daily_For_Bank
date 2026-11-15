---
publish_time: 1789789344
link: https://www.marktechpost.com/2026/09/18/spacexai-releases-grok-voice-transcribe-2-0/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  SpaceXAI 发布语音转文字模型 Grok Voice Transcribe 2.0，团队称在相同价格下准确率为 1.0 版本的两倍，面向嘈杂电话线、重叠人声、地方口音与口头敏感信息等难采音频，支持批量与实时流式两种模式，经 Speech to Text API 调用。该模型基于 Grok Voice 的音频基座，据称每天已处理数万通客服电话、转录数百万小时视频旁白，并驱动特斯拉车内的 Grok 助手；目前以 grok-voice-transcribe-2.0 上线为托管 API，未开放权重，无法自托管。
---

# SpaceXAI 发布 Grok Voice Transcribe 2.0：语音转文字 API（准确率翻倍）

> 原文链接：https://www.marktechpost.com/2026/09/18/spacexai-releases-grok-voice-transcribe-2-0/
> 来源：MarkTechPost

SpaceXAI has released Grok Voice Transcribe 2.0, its newest speech-to-text (STT) model. The development team claims it to be twice as accurate as Grok Voice Transcribe 1.0 at the same price. The model targets hard audio: noisy phone lines, competing voices, local accents, and spoken credentials. It runs in batch and real-time streaming modes through the Speech to Text API.

Is it deployable? Yes, as a hosted API. It is live today under the model ID grok-voice-transcribe-2.0. SpaceXAI has not announced open weights, so self-hosting is not an option.

What is Grok Voice Transcribe 2.0?

Grok Voice Transcribe 2.0 is built on the audio foundation model behind Grok Voice. SpaceXAI team states that Grok Voice already handles tens of thousands of customer-support calls a day. It also transcribes millions of hours of video narration and runs the Grok assistant in Tesla vehicles. 

The training data is live, noisy, multilingual audio recorded across diverse environments. SpaceXAI then refined the model with post-training.

Benchmarks: What SpaceXAI Reports

SpaceXAI reports a first-place accuracy rank among 32 streaming models on the public Artificial Analysis leaderboard. That benchmark, AA-WER Streaming, uses about 8 hours of audio. It weights AA-AgentTalk at 50%, VoxPopuli at 25%, and Earnings22 at 25%. See the methodology for details.

SpaceXAI also measures word error rate (WER) on 4 internal sets drawn from production traffic:

Telephony (8 kHz): English customer support calls

Conversational: English conversations with Grok

Credentials: phone numbers, emails, and addresses in English

Short phrases: voice-assistant utterances in 19 languages

Version 2.0 improves on 1.0 across all 4 sets. On telephony, SpaceXAI says it leads every model the company tested. These internal results are vendor-reported and not independently reproduced.

Multilingual Transcription and Language Switching

The model transcribes dozens of languages and detects the language automatically. It also follows mid-recording language switches in a single pass. SpaceXAI team calls multilingual accuracy the largest improvement over 1.0.

Short phrases, such as in-car commands, give a model little context to identify the language. On that set, WER drops from 20.6% to 6.8%. That works out to roughly 67% fewer word errors.

The docs list 25 languages for written-form formatting of numbers, currencies, and units.

&

Key Features for Developers

Every feature below ships in the same API:

Batch and streaming: transcribe files and URLs, or stream audio over WebSocket at wss://api.x.ai/v1/stt

Word-level timestamps: start and end times plus confidence scores for each word

Speaker diarization: speaker labels at no additional cost

Multichannel transcription: up to 8 channels transcribed independently

Key term biasing: up to 100 domain terms per request, each up to 50 characters

Text formatting: numbers, dates, currencies, phone numbers, and emails returned in written form

Filler word removal: &#8220;um&#8221; and &#8220;uh&#8221; are removed by default

Smart turn detection: an ML model predicts end of turn for voice agents

The batch endpoint accepts files up to 500 MB across 12 audio formats. Streaming also accepts Opus at roughly 4 KB/s, versus 48 KB/s for raw PCM at 24 kHz.

Pricing

Pricing is identical to version 1.0. Batch transcription costs $0.10 per hour of audio. Streaming costs $0.20 per hour. Diarization, timestamps, and key terms are included. That equals about $1.67 and $3.33 per 1,000 minutes.

How to Call It

Copy CodeCopiedUse a different Browser

curl -X POST https://api.x.ai/v1/stt \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -F model=grok-voice-transcribe-2.0 \
  -F format=true \
  -F language=en \
  -F file=@audio.mp3

Atlassian Loom Adopts Grok Voice Transcribe 2.0

Atlassian Loom now uses Grok Voice Transcribe 2.0 to transcribe every video. Atlassian found it more accurate than its existing solution.

The workflow SpaceXAI describes is record, transcribe, then code. A user records an action plan in Loom. The transcript is piped into Cursor, which makes the code updates. Sanchan Saxena, SVP of Teamwork Collection at Atlassian, described it as &#8216;closing the loop from context to code.&#8217;

Key Takeaways

Grok Voice Transcribe 2.0 claims 2x the accuracy of 1.0 at unchanged pricing.

Batch costs $0.10 per audio hour and streaming costs $0.20.

SpaceXAI reports rank 1 among 32 streaming models on Artificial Analysis.

Short-phrase WER across 19 languages fell from 20.6% to 6.8%.

It is API-only, so set model=grok-voice-transcribe-2.0 explicitly for now.

Check out the technical details and the API docs. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post SpaceXAI Releases Grok Voice Transcribe 2.0: A Speech-to-Text API Claiming 2x Accuracy Over 1.0 at $0.10 per Hour appeared first on MarkTechPost.