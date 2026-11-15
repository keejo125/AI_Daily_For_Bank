---
publish_time: 1790459783
link: https://www.marktechpost.com/2026/09/26/sarvam-ai-releases-saaras-v4-a-speech-to-text-model-for-all-22-indian-languages-and-global-english/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Sarvam AI 发布其语音识别模型 Saaras V4，覆盖印度 22 种官方语言并加入全球英语口音，官方称在全部 22 种语言上达到 SOTA 精度。模型采用编码器—解码器架构：音频编码器将波形转为承载音素与声学细节的嵌入，时序下采样适配器压缩序列并投影进语言模型空间；解码器为自研 3B 参数混合状态空间语言模型 Sarvam-3B，按文本提示自回归输出转写结果。评测上，英文在 7 个数据集上取得所比模型最低平均词错率（WER），印度语在 Vistaar 上以 WER 与 LLM-WER 双指标报告，噪声场景下错误率据称不到 Deepgram Nova-3 与 GPT-4o Transcribe 的一半。同一模型通过 mode 参数可输出 5 种表示。需注意的是，上述数字均为厂商自报，尚未有独立复现。
---

# Sarvam 发布 Saaras V4 语音识别模型，覆盖 22 种印度语言与全球英语

> 原文链接：https://www.marktechpost.com/2026/09/26/sarvam-ai-releases-saaras-v4-a-speech-to-text-model-for-all-22-indian-languages-and-global-english/
> 来源：MarkTechPost

Sarvam AI has released Saaras V4, the newest generation of its speech recognition model. It covers all 22 scheduled Indian languages plus English, now including global English accents. Sarvam reports state-of-the-art accuracy across all 22 languages. 

Is it deployable? Yes, through Sarvam&#8217;s API today, using model="saaras:v4". Weights are not public, and Sarvam&#8217;s SageMaker self-hosting docs currently cover Saaras v3 only.

What is Inside Saaras V4

Saaras V4 is an encoder-decoder system. An audio encoder converts the waveform into embeddings that carry phonetic and acoustic detail. A temporal-downsampling adapter then shortens that sequence and projects it into the language model&#8217;s embedding space. This keeps long recordings inside the decoder&#8217;s context budget.

The decoder is Sarvam-3B, a 3B-parameter hybrid state-space language model trained from scratch in-house. It reads the audio features alongside a text prompt. It then emits the transcript autoregressively, feeding each token back as input for the next.

Benchmark Results

English: Sarvam evaluated 7 English datasets. Six come from Hugging Face&#8217;s Open ASR Leaderboard: AMI, GigaSpeech, LibriSpeech clean, LibriSpeech other, SPGISpeech and VoxPopuli. The seventh is AI4Bharat&#8217;s Indian-accented Svarah. Scoring follows the leaderboard&#8217;s normalization code. Saaras V4 posts the lowest average WER among the models Sarvam benchmarked.

Indic: On Vistaar, Sarvam reports results across 10 Indian languages using both WER and LLM-WER. LLM-WER adds a semantic check. It separates real meaning errors from harmless spelling or formatting variants common in Indic scripts.

Noisy audio: On Kathbath Noisy, measured with LLM-WER, Sarvam says Saaras V4&#8217;s error rate is under half that of Deepgram Nova-3 and GPT-4o Transcribe. The set includes compressed, clipped and background-heavy recordings.

Language ID: On verified IndicVoices utterances, language identification error is 2.9% across the top 10 Indian languages. It is 5.22% across all 22.

It is important to note that all numbers above are vendor-reported. Independent reproduction has not been published yet.

5 Output Modes From 1 Model

The same audio can return 5 representations, selected through the mode parameter:

transcribe (default): native script with numbers and dates normalized.

verbatim: every word as spoken, fillers and spoken numbers kept.

codemix: native script, with English words left in English.

translit: the full utterance in Latin script.

translate: an English translation with numbers normalized.

Sarvam&#8217;s argument is simple. Handling these inside the model removes post-processing steps that can compound errors.

Keyterm Prompting

Keyterm prompting is new in V4 and works only with saaras:v4. You pass a JSON list under keyterms, with up to 50 terms of 64 characters each. Keyterms bias recognition; they do not guarantee output. Use codemix mode when a brand such as PhonePe must stay in Latin script.

On IndicContextEval (paper, Interspeech 2026), Saaras V4 reports 16.03% WER in the L5 keyword-prompting setting. Sarvam says that is the lowest score on the benchmark.

Streaming, Long Audio and Pricing

Streaming: WebSocket with partial results and time to first token below 150 ms.

REST: synchronous transcription for clips up to 30 seconds.

Batch: asynchronous jobs up to 2 hours per file, with optional speaker diarization.

SDKs: Python 3.9+ and Node.js 18+, plus LiveKit Agents, Pipecat and Vercel AI SDK integrations.

Price: Sarvam lists speech-to-text at ₹30 per hour for real-time, streaming and batch, and ₹45 per hour with diarization.

Saaras v3 stays the default model. V4 uses the same request shape, so switching is a 1-line change.

&

Saaras V4 vs Closest Competitors

These are the 3 systems Sarvam benchmarked against. Figures come from each vendor&#8217;s public docs and pricing pages, checked on September 26, 2026.

FeatureSarvam Saaras V4Deepgram Nova-3ElevenLabs Scribe v2OpenAI GPT-4o TranscribeIndian scheduled languages (of 22)221114Not listed per languageTotal languages23 (22 Indian + English)45+90+MultilingualKeyterm biasingUp to 50 termsYes, paid add-onUp to 1,000 (batch), 50 (realtime), paid add-onFree-text promptBuilt-in output modes5 (transcribe, verbatim, codemix, translit, translate)Transcript plus Smart FormattingVerbatim or no_verbatimTranscriptReal-time streamingWebSocket, under 150 ms TTFT (vendor claim)Yes (WebSocket)Scribe v2 Realtime, about 150 msFile streaming; live via Realtime APISpeaker diarizationBatch APIYesUp to 32 speakersSeparate gpt-4o-transcribe-diarize modelList price₹30/hour$0.0052/min (multilingual, pre-recorded)$0.22/hour (batch)~$0.006/minSelf-hostingNot for V4 yet (v3 on SageMaker)YesCloud APICloud API

Key Takeaways

Saaras V4 covers all 22 Indian languages plus global English in 1 model.

A 3B hybrid state-space decoder, trained from scratch, sits behind an audio encoder.

Keyterm prompting accepts up to 50 terms and scored 16.03% WER on IndicContextEval L5.

5 output modes and sub-150 ms streaming TTFT come from the same model.

API-only today at ₹30 per hour; self-hosting docs still cover v3.

Check out the Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Sarvam AI Releases Saaras V4: A Speech-to-Text Model for All 22 Indian Languages and Global English appeared first on MarkTechPost.