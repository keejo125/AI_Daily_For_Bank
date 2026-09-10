---
publish_time: 1788327432
link: https://www.marktechpost.com/2026/09/01/meta-superintelligence-labs-releases-muse-voice-transcribe-one-real-time-model-for-streaming-asr-diarization-and-endpointing/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Meta Superintelligence Labs 发布 Muse Voice Transcribe，被称为其首个实时音频感知模型，将流式语音识别（ASR）、20+ 说话人分离（diarization）与端点检测合并为单一自回归多模态模型，无需后处理。音频以 80ms 分块输入，模型在「继续听」与「写文本」间逐块二选一；说话人归属通过特殊 token 实现。经强化学习在词错率与延迟间权衡，登上速度-精度 Pareto 前沿。已作为托管 API（muse-voice-transcribe-1.0）上线，按每千音频分钟 3 美元计费，暂无权重开放。
---

# Meta 超级智能实验室发布 Muse Voice Transcribe：集流式语音识别、说话人分离与端点检测于一体的实时模型

> 原文链接：https://www.marktechpost.com/2026/09/01/meta-superintelligence-labs-releases-muse-voice-transcribe-one-real-time-model-for-streaming-asr-diarization-and-endpointing/
> 来源：MarkTechPost

Most production voice stacks are three systems stitched together. One model transcribes, a second separates speakers, and a detector decides when the user stopped talking. Each hand-off adds latency and a new failure mode.

Muse Voice Transcribe, announced by Meta Superintelligence Labs this week, collapses those three jobs into a single autoregressive model. Meta calls it its first real-time audio perception model. It performs streaming ASR, speaker diarization for 20+ speakers, and endpointing in one pass, with no required post-processing.

Is it deployable? Yes, but only as a hosted API. It is live on the Meta Model API as muse-voice-transcribe-1.0 at $3.00 per 1,000 audio minutes ($0.18 per hour), and it already powers dictation in Meta AI for Mac and Muse Code. No weights have been released, so there is no self-hosted path.

Streaming ASR as the foundation

Muse Voice Transcribe is an autoregressive multimodal model from the Muse Spark family. Audio arrives in 80ms chunks at 12.5 Hz. Each chunk is transformed into a single soft token.

After every chunk the model makes one binary choice. It either predicts a <|next_audio|> token and keeps listening, or it emits a text token. When the model predicts <|next_audio|>, that token is replaced by the actual next audio chunk in the input. When the stream ends, an <|empty_audio|> token is inserted, and the model flushes all remaining text without requesting more audio.

Listening and writing share one decoder loop, so there is no separate alignment stage to drift.

Adaptive delay, trained with RL

Because the model controls when it listens, it also controls how much audio context sits behind each word. Meta calls that gap &#8216;delay.&#8217; Longer delay means a more accurate transcript and higher latency.

Instead of fixing that trade-off, Meta trains it. Reinforcement learning combines a word error rate reward and a delay reward multiplicatively, producing a policy that varies delay per word by difficulty. Meta reports this puts the model on the Pareto front for speed against accuracy, measured by time to final transcription, ahead of the previous frontier formed by Soniox, Cartesia, and ElevenLabs systems.

Diarization and endpointing are more tokens

Meta did not add a second model for speaker attribution. It added special tokens to the same stream.

For diarization, a <|start_of_turn|> token marks a potential speaker switch, and a <|speaker_{A-Z}|> tag identifies the speaker. The turn token fires as soon as a switch is possible, while the speaker tag is delayed to the end of the chunk. Audio from one speaker can be split across several segments that all resolve to the same tag.

For endpointing, <|speech_onset|> marks the start of speech and <|speech_endpoint|> marks the point where the user finished. Both tasks are trained jointly with streaming ASR, using extra rewards layered on top of the ASR reward.

Capabilities

The model was trained on 70+ languages, of which 25 are extensively verified and recommended at launch. Code-switching is native, both within a sentence and between sentences, which matters for bilingual speakers who mix languages mid-clause. Accuracy can be improved further with language, keyword, and context biasing.

Long-context handling is a practical differentiator. Meta states the model natively supports audio input exceeding one hour and 20+ speakers, with no required post-processing step.

Benchmarks

Meta reports first place on Artificial Analysis for streaming speech-to-text and on public diarization benchmarks, as of September 1, 2026.

On Artificial Analysis AA-WER Streaming, Muse Voice Transcribe records 3.1% final-transcript WER at 0.16s after end of speech. Cartesia Ink-2 with semantic endpoints is 3.4% at 0.43s. ElevenLabs Scribe v2 Realtime is 3.6% at 0.14s. Cartesia Ink-2 with external endpoints is fastest at 0.07s but least accurate at 4.0%. On first partial transcript, Muse Voice Transcribe records 3.6% WER at 0.13s.

On diarization, Meta reports a 17.5% average diarization error rate across AMI-IHM, AMI-SDM, and VoxConverse. Five other systems in the same chart range from 21.1% to 28.6%.

Price is the other axis. At $3.00 per 1,000 minutes, it undercuts Cartesia Ink-2 at $4.00 and is less than half the $6.50 for ElevenLabs Scribe v2 Realtime and Deepgram Flux.

Interactive explainer

&

Key Takeaways

Single model does streaming ASR, diarization for 20+ speakers, and endpointing.

3.1% final-transcript WER at 0.16s on Artificial Analysis AA-WER Streaming.

Reinforcement learning teaches the model a per-word "adaptive delay" policy.

Trained on 70+ languages, 25 extensively verified, with native code-switching.

API-only at $0.18 per audio hour. No open weights.

Check out Meta AI Research blog, AI at Meta on X, Artificial Analysis and Meta Model API model page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meta Superintelligence Labs Releases Muse Voice Transcribe: One Real-Time Model for Streaming ASR, Diarization, and Endpointing appeared first on MarkTechPost.