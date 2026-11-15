---
publish_time: 1793258916
link: https://www.marktechpost.com/2026/10/29/assemblyai-tts-1-text-to-speech-api-voice-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  AssemblyAI发布首款文本转语音模型AssemblyAI-TTS-1并正式可用，面向实时电话语音智能体，延迟与发音决定caller留存。定价每百万字符15美元、无年约无并发档。其以连续音频表征（而非离散token）提升真实感与首字延迟，在AssemblyAI自测中实体准确率持平ElevenLabs v4而价格不到1/5；独立基准中位流式延迟159ms（19款中第8）。暂不支持SSML与情感标签。
---

# AssemblyAI 推出 TTS-1 文本转语音模型：每百万字符 15 美元的语音智能体 API

> 原文链接：https://www.marktechpost.com/2026/10/29/assemblyai-tts-1-text-to-speech-api-voice-agents/
> 来源：MarkTechPost

AssemblyAI has released AssemblyAI-TTS-1, its first text-to-speech model, now generally available. The AssemblyAI-TTS-1 text-to-speech API targets voice agents running on live phone calls. In that setting, latency and pronunciation decide whether a caller stays on the line. Pricing is $15 per 1M characters, with no annual contract and no concurrency tier to buy. For developers already using AssemblyAI speech-to-text, it closes the voice loop with one vendor.

TL;DR

Size: It is a hosted API model.

Runs on: AssemblyAI&#8217;s cloud only, in the US (us-east-1) or EU (eu-north-1). No open weights or on-prem option. Any client with HTTP or WebSocket works.

Performance: Ties ElevenLabs v4 on entity accuracy in AssemblyAI&#8217;s tests, at under 1/5 of its price.

Best: 47 ms median time to first byte across 6 models in AssemblyAI&#8217;s API test (self-reported).

Worst: 159 ms median streaming latency on Cekura&#8217;s independent benchmark, 8th of 19 timed models.

Bottom line: 

Best: $15 per 1M characters with unlimited concurrency. 

Worst: no SSML, speed control, pronunciation dictionaries or emotion tags yet.

What is AssemblyAI-TTS-1?

AssemblyAI-TTS-1 is a streaming text-to-speech model from AssemblyAI that turns agent replies into speech for live calls. It was trained on millions of hours of audio, including real conversational data. Most TTS models represent audio as discrete tokens. AssemblyAI says TTS-1 operates on continuous audio representations instead. The AssemblyAI claims this improves realism and cuts time to first spoken audio.

The launch includes a library of 4,000+ voices and instant voice cloning. A clone needs a short recording and a confirmation of the speaker&#8217;s permission. The clone in the launch post used 24 seconds of audio. Six languages are supported at launch: English, Spanish, French, German, Italian and Portuguese.

How do developers integrate AssemblyAI-TTS-1?

There are 3 interfaces: an HTTP API, a WebSocket API and an OpenAI-compatible route. The WebSocket session keeps one connection per conversation and accepts a cancel message for barge-in. Output is mono PCM, mu-law or A-law, at 8 kHz to 48 kHz. 24 kHz PCM is the native format; telephony stacks can request 8 kHz mu-law directly. Word timestamps are included. AssemblyAI also published LiveKit and Pipecat reference agents.

How does AssemblyAI-TTS-1 perform on benchmarks?

AssemblyAI tested TTS-1 against 5 models on 4 English sets, using 50 matched cloned voices. All figures below are self-reported, from an eval dated October 28, 2026.

Entity accuracy (580 hard targets such as phone numbers and codes): 93.7%, vs ElevenLabs v4 93.6%, Cartesia Sonic 3.6 82.5%, ElevenLabs Flash v2.5 68.0%.

Word accuracy: 99.0% on Seed-TTS and LibriSpeech sentences.

Predicted MOS: 3.85, behind Inworld TTS-2 Flash at 3.88 and ahead of Sonic 3.6 at 3.82.

Median time to first byte: 47 ms. Flash v2.5 took 119 ms, Sonic 3.6 143 ms, Inworld TTS-2 Flash 244 ms.

Other: 85.5 TTSDS prosody score and 0.64 speaker similarity for cloned audio.

Independent results are more mixed. On Cekura&#8217;s benchmark of 27 models, TTS-1 scored 81.5% reading accuracy and 4.50 naturalness. Its median streaming latency, timed from the last word sent, was 159 ms. Inworld TTS-2 Flash posted 45 ms and 93.2% accuracy there, at the same $15 price. AssemblyAI also cites a 1.7% word error rate on Coval&#8217;s leaderboard. It reports a top-10 debut in Artificial Analysis&#8217; controlled-voice arena.

How does AssemblyAI-TTS-1 compare with ElevenLabs, Cartesia and Inworld?

FeatureAssemblyAI-TTS-1Inworld TTS-2 FlashElevenLabs Flash v2.5Cartesia Sonic 3.6Model sizeNot disclosedNot disclosedNot disclosedNot disclosedArchitectureContinuous audio representationsNot disclosedNot disclosedState space model (SSM)AccessHosted API (US, EU)Hosted APIHosted APIHosted API; on-prem and VPC on enterpriseLanguages6200+3244Vendor latency claimAbout 90 ms to first audioUnder 25 ms P99 server-side TTFBAbout 75 msUnder 90 msMedian TTFB, AssemblyAI test47 ms244 ms119 ms143 msMedian streaming latency, Cekura159 ms45 ms177 ms270 msEntity accuracy, AssemblyAI set93.7%Not reported68.0%82.5%Reading accuracy, Cekura81.5%93.2%64.4%74.9%Naturalness, Cekura (UTMOS)4.504.464.334.41List price per 1M characters$15$15 on demand, $7 on Growth plan$40$37.38 to $50 via plan creditsSelf-serve concurrencyUnlimited on pay-as-you-go5 to 500 requests by planNot disclosed2 to 15 requests by planVoice cloningInstant onlyInstant and professionalYesInstant and professional

Cartesia&#8217;s range divides each plan price by its credits, at 1 credit per character.

What does AssemblyAI-TTS-1 cost?

Pricing is per input character, including spaces and punctuation, at $15 per 1M. Every voice, cloning, word timestamps and EU processing come at that same rate. There are no per-voice fees, concurrency fees or minimums. AssemblyAI calls it the lowest-priced frontier TTS model for voice agents. However, Inworld TTS-2 Flash also lists $15 per 1M on demand, falling to $7 on paid plans. The sharper difference is concurrency: Inworld&#8217;s on-demand tier allows 5 concurrent requests.

Key Takeaways

AssemblyAI-TTS-1 is AssemblyAI&#8217;s first text-to-speech model, built for live voice agents.

It costs $15 per 1M characters, with unlimited concurrency and no contract.

Self-reported: 93.7% entity accuracy and 47 ms median time to first byte.

Cekura measured 159 ms streaming latency and 81.5% reading accuracy.

Missing at launch: SSML, speed control, pronunciation dictionaries and emotion tags.

Check out the launch post, docs, pricing, and the LiveKit and Pipecat reference agents. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post AssemblyAI Ships AssemblyAI-TTS-1: A $15 per 1M Character Text-to-Speech API for Voice Agents appeared first on MarkTechPost.