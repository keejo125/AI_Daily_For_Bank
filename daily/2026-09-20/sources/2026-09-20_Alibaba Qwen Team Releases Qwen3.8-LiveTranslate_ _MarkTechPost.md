---
publish_time: 1789886768
link: https://www.marktechpost.com/2026/09/19/alibaba-qwen-team-releases-qwen3-8-livetranslate/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  阿里通义千问团队发布Qwen3.8-LiveTranslate，新一代实时同声传译模型。它能够监听实时语音（可选结合视频帧），返回翻译文本与对应字幕，覆盖60种语言，平均延迟降至2.3秒。该模型面向会议、直播、跨国协作等需要低延迟多语种翻译的场景，延续了Qwen系列在多模态与语音方向的布局。作为通义千问家族的新成员，Qwen3.8-LiveTranslate进一步把大模型能力延伸到实时跨语言沟通这一高频刚需场景。
---

# 阿里通义千问团队发布 Qwen3.8-LiveTranslate：覆盖60语言的实时同传模型，平均延迟降至2.3秒

> 原文链接：https://www.marktechpost.com/2026/09/19/alibaba-qwen-team-releases-qwen3-8-livetranslate/
> 来源：MarkTechPost

Qwen has released Qwen3.8-LiveTranslate, its next-generation real-time simultaneous interpretation model. It listens to live speech, with optional video frames, and returns translated text and speech while the speaker is still talking. The core change is a new Interleave architecture. Qwen reports gains in faithfulness, fluency, and conciseness, with average lagging (LAAL) dropping from 2.8 seconds to 2.3 seconds. The release also adds real-time speaker diarization, synchronized bilingual display, and long-context disambiguation.

Deployable? Yes, as a hosted API. It is live on Alibaba Cloud Model Studio and QwenCloud as qwen3.8-livetranslate-flash-realtime over WebSocket. 

What Changed Under the Hood

Simultaneous interpretation is a tradeoff. Waiting longer gives the model more context. Speaking sooner cuts delay for the listener. Qwen3.8-LiveTranslate rebuilds this loop with an Interleave architecture.

The latency metric here is LAAL, or Length-Adaptive Average Lagging. It measures how far the translation trails the source speech on average. It also avoids rewarding systems that over-generate output. A drop from 2.8 seconds to 2.3 seconds is roughly an 18% cut in average lag.

QwenCloud team describes the model as the real-time version of Qwen3.8-LiveTranslate-Flash. It builds on the Qwen-Omni stack, large-scale multimodal data, cross-language and cross-modal alignment, and visual enhancement. The Flash model also supports offline audio and video translation.

Three New Capabilities

Real-time speaker diarization: The model distinguishes speakers in multi-party speech. It also preserves each speaker&#8217;s voice through more stable voice cloning. The API exposes cloning modes, including an always mode that re-clones before each response for multi-speaker sessions.

Synchronized bilingual display: Source text and translation appear on screen together. In the API, source transcription streams as its own events next to the translation stream.

Long-context disambiguation: The model uses conversation history to resolve names and terminology. A name introduced early in a meeting stays consistent later in the translation.

Try the explainer below. It walks through the interleaved stream, speaker tagging, context disambiguation, language coverage, and session cost.

Languages, Inputs, and Vision

The model understands 60 languages. It can speak 29 of them, returning audio plus text. The remaining 31 return text only. Speech output covers Chinese, English, Arabic, German, French, Spanish, Japanese, Korean, Hindi, and others.

Inputs are audio and optional images. Outputs are text and audio. Visual cues such as lip movements, gestures, and on-screen text help in noisy rooms and with ambiguous words. The docs recommend sending no more than 2 images per second.

Teams can also set hotwords. These map source terms to fixed target translations. The docs recommend configuring no more than 1,000 hotwords.

API, Pricing, and Limits

Developers connect through the WebSocket Realtime API with the model ID qwen3.8-livetranslate-flash-realtime. The default turn detection type is speaker_detection. Clients stream audio continuously and receive server-generated responses.

Default audio is 16 kHz PCM in and 24 kHz PCM out. The default voice is Tina. Set session.output_modalities to text only, or text and audio. Always send session.finish before closing, or the final segment is lost.

Singapore list pricing per 1M tokens:

Audio input: $7.50

Image input: $0.55

Text output: $20

Audio output: $30

Beijing pricing is lower, at $5.653, $0.466, $14.133, and $22.613 in USD. Audio input consumes 7 tokens per second. Audio output consumes 12.5 tokens per second. One hour of speech in and speech out costs about $1.54 in Singapore, before text and image tokens.

The context window is 53,248 tokens, with 49,152 for input and 4,096 for output. Default rate limits are 10 requests and 100,000 tokens per minute. Model Studio lists function calling, structured outputs, batch inference, and fine-tuning as unsupported.

Key Takeaways

Qwen3.8-LiveTranslate cuts average lag (LAAL) from 2.8s to 2.3s.

A new Interleave architecture improves faithfulness, fluency, and conciseness.

It adds speaker diarization, bilingual display, and long-context disambiguation.

It understands 60 languages and speaks 29.

Access is API-only via Alibaba Cloud Model Studio and QwenCloud.

Check out the Technical Details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Alibaba Qwen Team Releases Qwen3.8-LiveTranslate: A Real-Time Interpretation Model That Cuts Average Lag to 2.3 Seconds Across 60 Languages appeared first on MarkTechPost.