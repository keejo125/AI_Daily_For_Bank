---
publish_time: 1792652456
link: https://www.marktechpost.com/2026/10/22/ibm-granite-speech-5-0-2b-release/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  IBM 发布 Granite Speech 5.0 2B，一个 2B 参数的稠密开源语音语言模型（Apache 2.0），支持 6 种语言语音转文字与翻译。模型由 16 个 Conformer 块组成的语音编码器、2 层窗口 q-former 与经 YaRN 扩展至 16k 的 granite-4.0-1b-base LLM 组成，训练用了 39 万小时公开与合成音频，在 8 张 H100 上训练 40 天。
  
  在 Open ASR Leaderboard 上平均英文 WER 5.68%，位列开源权重模型第 2（仅次于 Qwen3-ASR-1.7B 的 5.40%）；LibriSpeech Clean 上 WER 仅 0.99%。新特性包括语言 ID 提示、最多 2000 词的关键词偏置、标点与大小写生成。同期更新的 Turbo CTC 吞吐达 19870 RTFx、支持 7 种语言，4.1 2B Plus 也做了权重级改进。
---

# IBM AI 发布 Granite Speech 5.0 2B，用于多语种转录与翻译

> 原文链接：https://www.marktechpost.com/2026/10/22/ibm-granite-speech-5-0-2b-release/
> 来源：MarkTechPost

IBM has released Granite Speech 5.0 2B, a new open speech-language model for transcription and translation. Granite Speech 5.0 2B is a 2B-parameter model from IBM that turns speech into text in 6 languages. It ships under Apache 2.0. IBM also updated 2 existing models: the edge-focused Turbo CTC and the diarization-focused 4.1 2B Plus. For developers, the release covers accurate transcription, fast on-device transcription and speaker-attributed transcripts.

TL;DR

Size: 2B parameters, dense. LLM backbone uses YaRN extension to 16k positions. IBM recommends audio segments of up to about 2 minutes.

Runs on: GPU via Transformers or vLLM, Apple Silicon via mlx-audio, local CPU/Mac via llama.cpp GGUF (Q8_0 recommended).

Performance: #2 open-weight model on the Open ASR Leaderboard, 5.68% average English WER.

Best: 0.99% WER on LibriSpeech Clean.

Worst: 13.79% WER on the leaderboard&#8217;s private conversational set.

How does Granite Speech 5.0 2B work?

The model has 3 parts, per the model card. A speech encoder of 16 Conformer blocks is trained with CTC. It uses block attention over 4-second audio blocks.

A 2-layer window q-former then projects and downsamples the acoustic embeddings. Total downsampling is 10x, so the LLM sees embeddings at 10 Hz.

The LLM is an intermediate checkpoint of granite-4.0-1b-base. IBM extended it to 16k positions with YaRN and fine-tuned it with LoRA adapters.

Training used 390,000 hours of public audio plus synthetic data. The synthetic sets target Japanese ASR, keyword biasing and translation. Training took 40 days on 8 H100 GPUs.

What is new versus Granite Speech 4.1 2B?

Language ID prompting: name the input language in the prompt to steer transcription.

Keyword lists up to 2,000 terms: bias output toward product names, people and acronyms.

Punctuation and capitalization on request: capitalization F1 runs from 90.16 to 99.51 across test sets.

Robustness: better handling of noise, reverberation and distant microphones.

How does Granite Speech 5.0 2B perform on benchmarks?

On the Open ASR Leaderboard, IBM&#8217;s chart shows a 5.68% average English WER. That average covers 9 public and 2 private test sets, as of October 21, 2026. Only Qwen3-ASR-1.7B scores better, at 5.40%.

Note a source conflict. IBM&#8217;s blog reports 5.06% instead. That figure is unofficial, dated October 15, and averages public short-form sets only.

Per-set results range widely. The model scores 0.99% on LibriSpeech Clean and 2.21% on LibriSpeech Other. It scores 13.79% on the private conversational set.

On the noisy FFASR leaderboard, it ranks #4 of 42 at 14.80% average WER. Qwen3-ASR-1.7B scores 13.41% there.

Multilingual CommonVoice WER is 2.60% for Portuguese and 3.50% for Spanish. Japanese is the weakest language at 10.74%.

For translation, X-to-English CoVoST BLEU reaches 53.6 for Portuguese and 40.1 for German. English-to-Mandarin was not evaluated.

Keyword biasing shows the clearest gain. On Earnings-22, keyword F1 rises from 67.2 to 90.1 with correct keyword lists. With 2,000-term lists mixing correct and wrong terms, it still reaches 82.8.

&

How does it compare with other open ASR models?

FeatureGranite Speech 5.0 2BQwen3-ASR-1.7BCohere Transcribe 03-2026Canary-Qwen-2.5BSize2B2.35B (Hub count)2.07B (Hub count)2.5BLicenseApache 2.0Apache 2.0Apache 2.0 (gated)CC-BY-4.0ASR languages630 + 22 Chinese dialects14English onlySpeech translationYesNot disclosedNot disclosedNoOpen ASR avg WER (Oct 21, 2026)*5.68%5.40%5.77%5.94%FFASR avg WER (Oct 18, 2026)*14.80%13.41%15.03%Not disclosedKeyword biasingUp to 2,000 termsNot disclosedNot disclosedNot disclosedLong audio~2 min segmentsLong audio supportedNot disclosed40 s max in training

*Leaderboard averages as charted in IBM&#8217;s model card from the Open ASR and FFASR leaderboards.

What changed in Turbo CTC and 4.1 2B Plus?

Granite Speech 5.0 Turbo CTC keeps its 470M footprint. It now transcribes 7 languages with native punctuation and capitalization. IBM compiled one Conformer block and reused its graph across the stack. That lifted throughput to 19,870 RTFx, up from about 12,600 at launch.

The updated Granite Speech 4.1 2B Plus is a drop-in weight update. Average timestamp shift falls from 210.86 to 98.54. Long-form WER drops from 13.53 to 10.22. Biased-keyword WER falls from 11.79 to 6.48.

How can developers deploy it?

Granite Speech 5.0 2B runs in Transformers, vLLM, llama.cpp and mlx-audio. For GGUF, IBM recommends Q8_0. Lower-bit quantizations lose accuracy on audio longer than about 1 minute. 

Key Takeaways

#2 open-weight model on the Open ASR Leaderboard at 5.68% WER.

2B parameters, Apache 2.0, runs on GPU, Mac and local CPU.

2,000-term keyword biasing across all supported languages.

Turbo CTC reaches 19,870 RTFx and now covers 7 languages.

Qwen3-ASR-1.7B still leads on accuracy and noisy audio.

Check out the model card, IBM blog and Granite Speech paper. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post IBM AI Releases Granite Speech 5.0 2B for Multilingual Transcription and Translation appeared first on MarkTechPost.