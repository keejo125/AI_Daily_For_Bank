---
publish_time: 1793248884
link: https://www.marktechpost.com/2026/10/28/nvidia-nemotron-3-5-transcribe-open-speech-llm/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  NVIDIA发布开源语音LLM Nemotron 3.5 Transcribe（34B总参、约4.3B激活、65K上下文），单模型覆盖40种语言、最长1小时录音，以文本指令选择逐字/书面/说话人归属/上下文/翻译等输出风格，可替代ASR、说话人分离与对齐工具。英文与多语Open ASR榜最佳开源模型（9项英文WER均4.71%），离线运行，普通话远场会议较弱（cpCER 34.95%）。
---

# 英伟达开源 Nemotron 3.5 Transcribe：支持 40 种语言的开源语音大模型

> 原文链接：https://www.marktechpost.com/2026/10/28/nvidia-nemotron-3-5-transcribe-open-speech-llm/
> 来源：MarkTechPost

NVIDIA has released Nemotron 3.5 Transcribe, an open-weights speech LLM built for transcription. One model handles 40 languages and recordings up to 1 hour. A text instruction picks the output style for each request. Options include verbatim, written form, speaker-attributed, contextual and translated output. For developers, it can replace separate ASR, diarization and alignment tools.

TL;DR

Size: 34B total and about 4.3B active parameters; 65,536-token context; audio up to 1 hour.

Runs on: 1x H100 80 GB in BF16. FP8 (about 35 GB) and NVFP4 (about 21 GB) checkpoints exist; NVFP4 runs on an RTX 5090. GGUF files target NeMo-Speech.cpp.

Performance: Best open-weights model on the English and multilingual Open ASR Leaderboards; top commercial APIs still lead.

Best: 4.71% mean WER on the 9 public English Open ASR sets (next open model: 4.94%).

Worst: 34.95% cpCER on AliMeeting Mandarin far-field meetings.

Bottom line: Best thing: 1 open model covers transcripts, speaker labels, timestamps and translation. Worst thing: offline only, with weak Mandarin meeting accuracy.

What is Nemotron 3.5 Transcribe?

Nemotron 3.5 Transcribe is a speech-augmented language model (SALM) from NVIDIA that turns audio and instructions into text. An audio encoder feeds embeddings into an LLM decoder, which makes transcription promptable. NVIDIA&#8217;s technical research report argues there is no single correct transcript. Numbers, fillers and domain terms depend on who reads the output. NVIDIA positions the model as a transcription specialist, not a general-purpose assistant.

How does the architecture work?

It has three parts:

Parallel Expert Encoder: a trainable 0.6B Transformer ASR encoder runs beside a frozen Nemotron 3 Diarization model. The diarizer tracks up to 8 speakers. Its speaker activity is added to the ASR features every 80 ms. The LLM therefore sees who spoke when, without architecture changes.

LLM backbone: Nemotron 3.5 Lightning 30B-A3B, a hybrid Mamba-Transformer MoE. It has 52 layers: 23 Mamba-2, 23 MoE and only 6 attention layers. Each MoE layer routes to 6 of 128 experts plus 1 shared expert. Few attention layers keep the KV cache small for hour-long audio.

Add-ons: a shared multi-token prediction (MTP) layer drafts tokens for speculative decoding. A 50M-parameter CTC adapter aligns the finished transcript to audio for word timestamps.

The model name says 30B-A4B, but the checkpoint holds about 34B parameters. The extra weight comes from the 1.3B MTP module and the audio components.

Training used 1 supervised fine-tuning stage on 256 H100 GPUs for 28,500 steps. A short RL stage followed: 400 GSPO updates with a reward of 1 minus WER. The model saw about 1.72M unique hours of audio, or 6.5M hours with repeats.

How does it score on benchmarks?

All numbers below are self-reported by NVIDIA in the technical report.

English Open ASR (9 public sets): 4.71% mean WER. The next open model, Qwen3-ASR-1.7B, scores 4.94%. Seven commercial systems still lead, topped by OtterAI speech-v3.1 at 3.88%.

Multilingual Open ASR (7 languages): 4.62% mean WER, versus 6.49% for Qwen3-ASR-1.7B. ElevenLabs Scribe v2 reaches 3.56%.

Long-form ASR: 10.98% mean WER, versus 13.37% for Parakeet-TDT-0.6B-v3.

Multi-speaker, full sessions: 15.80% mean cpWER, versus 16.83% for DiCoW v3.3 with DiariZen. NVIDIA says it is the first SALM to beat cascaded systems here.

Contextual ASR: an entity list cuts named-entity WER on ContextASR-Bench from 12.21% to 2.20%.

 -->

How do you deploy Nemotron 3.5 Transcribe?

Weights ship in BF16, FP8, NVFP4 and GGUF. A DFlash2 draft model is optional. The OpenMDW-1.1 license allows commercial use.

Runtimes include vLLM 0.32.0 with the NeMo Speech plugin, Transformers and SGLang-Omni 0.2.0. vLLM exposes an OpenAI-compatible API.

NVIDIA model&#8217;s main speed comes from its Nemotron Transcribe NIM. With NVFP4 and DFlash2, 1 RTX PRO 6000 Blackwell Server Edition transcribes 2,238 seconds of audio per second. It returns a 30-second clip in 0.13 seconds. There is a catch: those serving optimizations are not open source yet. NVIDIA expects the release-day vLLM path to be roughly 2x slower. On 1 H100 in BF16 with MTP2, NVIDIA estimates about 410 RTFx.

For fine-tuning, NVIDIA tested 17 tasks. Each took about 0.5 to 2.3 GPU-hours on a single GB300.

How does it compare with other open ASR models?

FeatureNemotron 3.5 TranscribeQwen3-ASR-1.7BCanary-Qwen-2.5BWhisper-large-v3Parameters34B total, ~4.3B active1.7B2.5B1.55BLanguages4030 + 22 Chinese dialectsEnglish only99 (HF tag)Max audio per request1 hourNot disclosed40 s in training30 s window, chunked long-formSpeaker attributionBuilt in, up to 8 speakersNot listedNot listedNot listedWord timestampsBuilt in (CTC adapter)Via separate ForcedAligner-0.6BNot listedYes, word-levelLicenseOpenMDW-1.1Apache-2.0CC-BY-4.0Apache-2.0English Open ASR, 9 public sets (mean WER, lower is better)4.71%4.94%*5.38%*6.66%*Open ASR mean WER on own model card (earlier leaderboard set)Not reported5.76%5.63%7.44%Multilingual Open ASR, 7 languages (mean WER)4.62%6.49%*Not applicable (English only)7.94%*Reference hardware1x H100 80 GB (BF16)Not disclosedTested on A6000, A100, RTX 5090Not disclosed

*Competitor scores on the current 9-set leaderboard come from NVIDIA&#8217;s report, citing Hugging Face leaderboard results from October 2026. The leaderboard set changed since the competitors published their own cards, so the 2 WER rows are not interchangeable.

Key Takeaways

One open model handles transcripts, speakers, timestamps and translation across 40 languages.

4.71% English WER is the best open-weights score; commercial APIs still lead.

About 4.3B active parameters; BF16 fits 1 H100, NVFP4 fits an RTX 5090.

An entity list cuts named-entity WER from 12.21% to 2.20%.

Offline only; Mandarin meetings and code-switching remain weak spots.

Check out the technical report, model weights, project page and live demo. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Releases Nemotron 3.5 Transcribe: An Open 30B MoE Model for 40-Language Transcription with ~4B Active Parameters appeared first on MarkTechPost.