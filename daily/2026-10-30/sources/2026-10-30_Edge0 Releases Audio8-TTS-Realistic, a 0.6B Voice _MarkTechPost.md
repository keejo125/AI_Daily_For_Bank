---
publish_time: 1793336572
link: https://www.marktechpost.com/2026/10/29/edge0-audio8-tts-realistic-0-6b-voice-cloning/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Edge0发布开源权重的文本转语音模型Audio8-TTS-Realistic，参数规模0.6B，可用1条参考音频与文本克隆声音，支持23种语言（较前代多12种），权重与代码以Apache 2.0发布。在9种语言的CV3评测中平均错误率4.86%，优于Qwen3-TTS-1.7B的7.73%；采用DualAR双自回归架构，已在Hugging Face提供。
---

# Edge0发布Audio8-TTS-Realistic：0.6B语音克隆TTS模型

> 原文链接：https://www.marktechpost.com/2026/10/29/edge0-audio8-tts-realistic-0-6b-voice-cloning/
> 来源：MarkTechPost

Edge0 has released Audio8-TTS-Realistic, an open-weight text-to-speech model for zero-shot voice cloning. Audio8-TTS-Realistic is a 0.6B-parameter model that clones a voice from 1 reference clip and transcript. It supports 23 languages, 12 more than its predecessor. The weights and code ship under Apache 2.0. For developers, the catch is competitive multilingual accuracy at a size that is cheap to fine-tune and serve.

TL;DR

Size: 601M main-model parameters (codec excluded); up to 2,048 packed text/audio positions of context.

Runs on: a CUDA GPU is recommended; smoke-tested on NVIDIA H20 in BF16. The paper reports 1.1 to 1.2 GiB peak memory on an Apple M2 CPU (INT4 ONNX). No Realistic ONNX export is public yet.

Performance: ahead of larger open models on CV3, behind 4B-class models on MiniMax.

Best: 4.86% average CV3 error across 9 languages, versus 7.73% for Qwen3-TTS-1.7B.

Worst: 48.57% WER on Thai (CV3) and 31.35% CER on Cantonese (MiniMax).

What is Audio8-TTS-Realistic?

It is the second 0.6B release in Edge0&#8217;s Audio8 TTS family. It builds on Audio8-TTS-Preview-0.6b and keeps the same Transformers inference interface. The repository bundles the checkpoint, a 44.1 kHz neural audio codec, tokenizer, processor and custom code. It can also generate speech without a reference voice.

New languages are Arabic, Finnish, Hindi, Indonesian, Malay, Norwegian, Portuguese, Russian, Swedish, Thai, Turkish and Vietnamese.

How does the architecture work?

The model uses a dual-autoregressive (DualAR) design inspired by Fish Audio S2 Pro. According to the technical research report, the slow branch is built on Qwen2.5 0.5B. It has 24 layers at width 896 and runs at about 21.5 frames per second. Each step predicts text tokens plus the first audio codebook.

A shallow 4-layer fast branch then predicts the remaining 9 codebooks in parallel. Sequential compute therefore happens only at the frame level.

How does Edge0 train for realism?

The team argues that word error rate (WER) and speaker similarity (SIM) miss rhythm, pauses and timing. A model can score well on both and still sound synthetic.

Training runs in 3 stages:

Multilingual supervised fine-tuning (SFT).

GRPO with a combined reward: 0.7 weight on WER, 0.3 on SIM.

GRPO guided by a learned realism critic.

The critic scores each output against a matched human recording of the same sentence. It was trained on a quality ladder built from 6 open-source TTS systems. These were ranked in a private blind listening study, with human recordings at the top. Synthetic pause compression adds finer rungs to the ladder.

An identity-erasure loss stops the critic from rewarding generator fingerprints. The critic head has about 3M parameters on top of a frozen WavLM-large encoder. A duration penalty also kicks in beyond 1.35x the reference length. This blocks the policy from gaming the critic with slower speech.

The final stage used only Chinese and English prompts. It still improved both aggregate metrics on the 13 lower-resource languages. Their error fell from 22.53% to 20.77%, and SIM rose from 0.637 to 0.679.

How does it perform on benchmarks?

All numbers below are self-reported error rates, where lower is better.

Seed-TTS (English/Chinese): 1.25% average error, SIM 0.704.

CV3 (9 languages): 4.86% average error, SIM 0.661.

MiniMax (24 languages): 5.89% average error, SIM 0.754.

On CV3, Audio8 beats VoxCPM2 (5.35%), CosyVoice3-1.5B (6.89%) and Qwen3-TTS-1.7B (7.73%). On MiniMax, Qwen3-TTS-1.7B scores 27.41%, but it officially supports only 10 of the 24 test languages.

Larger models still lead elsewhere. Higgs TTS 3 reports 4.41% on CV3 and 2.74% on MiniMax. Qwen3-TTS-1.7B averages 1.01% on Seed-TTS. Edge0 itself calls its table a reference comparison, since evaluation pipelines and text normalization differ.

How does it compare with other open TTS models?

FeatureAudio8-TTS-RealisticQwen3-TTS-12Hz-1.7B-BaseVoxCPM2Higgs TTS 3Size0.6B (excl. codec)1.7B2B~4B backboneLicenseApache 2.0Apache 2.0Apache 2.0Research and non-commercialLanguages231030100+Output sample rate44.1 kHzNot disclosed48 kHz24 kHzSeed-TTS EN WER1.46%1.24%1.84%Not disclosedSeed-TTS ZH CER1.03%0.77%0.97%Not disclosedCV3 avg error (9 langs)4.86%7.73% (Boson AI eval)5.35%4.41%MiniMax avg error (24 langs)5.89%27.41% (Boson AI eval)Not disclosed2.74%Hardware notedCUDA GPU; INT4 M2 CPU in paperGPU, FlashAttention 2~8 GB VRAM1x H100 serving tests

VoxCPM2&#8217;s CV3 average is computed from its per-language table.

How do you deploy it?

Install PyTorch 2.5+ and Transformers 4.57+, then load with trust_remote_code=True. Voice cloning needs a clean reference clip and its exact transcript. The GitHub repo adds a CLI, batching and supervised fine-tuning scripts.

For GPU serving, an SGLang Omni adapter provides paged attention, dynamic batching and an OpenAI-compatible /v1/audio/speech API. Edge0 notes throughput and streaming were not benchmarked. A free Playground runs on Hugging Face ZeroGPU.

Key Takeaways

601M parameters, 23 languages, Apache 2.0 weights.

A learned realism critic drives the final GRPO stage.

4.86% CV3 error beats Qwen3-TTS-1.7B and VoxCPM2.

4B-class Higgs TTS 3 still leads on CV3 and MiniMax.

Lower-resource languages remain weak, with Thai near 49% WER.

Check out the Paper, Model Weights, Repo and Samples. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Edge0 Releases Audio8-TTS-Realistic, a 0.6B Voice Cloning TTS Model appeared first on MarkTechPost.