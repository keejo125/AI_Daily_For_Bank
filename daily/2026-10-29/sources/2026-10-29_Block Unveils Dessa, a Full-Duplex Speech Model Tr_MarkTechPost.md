---
publish_time: 1793260239
link: https://www.marktechpost.com/2026/10/29/block-dessa-full-duplex-speech-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Block AI实验室发布研究预览Dessa——一个仅以人类对话训练的全双工语音模型，听与说同时进行，无需文本或预训练模型，可在MacBook Pro M4 Max本地实时运行。其直接处理情绪、讽刺与笑声等信号，演示展现插话、mid-sentence大笑等自然中断。目前仅演示、零公开基准，训练用了1台NVIDIA GB200 NVL72（72 GPU），Moshi曾用1016块H100。
---

# Block 发布 Dessa：仅用人类对话训练的全双工语音模型

> 原文链接：https://www.marktechpost.com/2026/10/29/block-dessa-full-duplex-speech-model/
> 来源：MarkTechPost

Block&#8217;s AI research lab has released Dessa, a full-duplex speech model trained only on human conversation. Block announced it on October 23, 2026 as a research preview. Dessa is a speech-to-speech model from Block that listens and talks at the same time. Block says it used no text and no pretrained models. That is a different design from the text-first stacks behind most voice agents today.

TL;DR

Runs on: A MacBook Pro M4 Max or better, locally, faster than real time. 

Performance: Demo-only so far. Live recordings show backchannels, mid-sentence laughs and natural interruptions.

Best: Trained on 1 NVIDIA GB200 NVL72 rack (72 GPUs). Moshi used 1,016 H100 GPUs.

Worst: 0 published benchmark scores. No weights, paper, API or price.

What is Block&#8217;s Dessa?

Dessa is a true speech-to-speech model: audio in, audio out. According to Block&#8217;s project page, everything it knows came from human speech.

It is full-duplex, so it listens while it talks. Block says it learned from real conversation when to cut in. It also learned when to backchannel with short cues like &#8220;yeah&#8221; or &#8220;got it&#8221;.

Block&#8217;s demo clips show Dessa laughing mid-sentence and getting louder when asked to speak up. One clip shows it talking with OpenAI&#8217;s GPT-Live-1. Block says nobody steered any clip.

How does speech-only training work?

Most voice systems chain 3 parts: speech recognition, a text model, then speech synthesis. Block team argues that chain throws away emotion, sarcasm, laughter and sighs. Dessa hears and produces those signals directly.

Block has not published the architecture. Here is what it has disclosed:

Training data: human conversation audio only. No text and no pretrained models.

Compute: 1 NVIDIA GB200 NVL72, which links 72 Blackwell GPUs and 36 Grace CPUs.

Data efficiency: Block says Dessa learned language from hundreds of times fewer words than LLMs need.

Inference: faster than real time, on a MacBook Pro M4 Max or better.

The lab also explains why this is hard. Speech never repeats exactly. A spoken word takes thousands of times more bytes than the same word in text.

Kyutai&#8217;s Moshi, the best-known open full-duplex model, takes another route. Moshi starts from a text language model backbone and predicts time-aligned text tokens before audio tokens. Its model card lists 7 million hours of pretraining audio and 1,016 H100 GPUs.

&

How does Dessa compare with Moshi, PersonaPlex and GPT-Live-1?

FeatureDessa (Block)Moshi (Kyutai)PersonaPlex-7B-v1 (NVIDIA)GPT-Live-1 (OpenAI)Starting pointSpeech only, no text, no pretrained modelHelium text LM backbone plus audioFine-tuned from Moshi (Moshiko) weightsNot disclosed; delegates reasoning to a backend agentParametersNot disclosed8B (Hugging Face listing)7B (model card)Not disclosedTraining compute1 GB200 NVL72 (72 GPUs)1,016 H100 GPUsNot disclosedNot disclosedTraining audioNot disclosed7M h unsupervised, 2,000 h Fisher, 20,000 h syntheticFisher English, under 10,000 hNot disclosedLatencyNot disclosed (&#8220;faster than real time&#8221;)200 ms in practice, 160 ms theoretical0.170 s turn-taking, 0.240 s interruption (FullDuplexBench)Not disclosed on model pageWeights and licenseNot releasedOpen, CC-BY 4.0Open, NVIDIA Open Model LicenseClosedRuns onMacBook Pro M4 Max or betterGPU; MLX, Candle and PyTorch checkpointsNVIDIA A100 / H100, LinuxOpenAI cloudAccess and priceResearch preview, waitlistFree downloadFree download (gated)API, $0.05 per minute voice layer

Key Takeaways

Dessa is full-duplex and speech-to-speech, trained only on human conversation audio.

Block trained it on 1 GB200 NVL72 rack; Moshi used 1,016 H100s.

It runs locally on a MacBook Pro M4 Max, faster than real time.

Block published 0 benchmarks, no parameter count and no weights.

Access is a waitlist.

Check out the Dessa project page. Compare it with the Moshi paper, the PersonaPlex model card and the GPT-Live-1 docs. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Block Unveils Dessa, a Full-Duplex Speech Model Trained Only on Speech appeared first on MarkTechPost.