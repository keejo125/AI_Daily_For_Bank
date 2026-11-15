---
publish_time: 1790194812
link: https://www.marktechpost.com/2026/09/23/google-releases-gemini-3-8-flash-tts-and-flash-lite-tts-with-prompt-based-voice-design/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MarkTechPost 报道谷歌发布 Gemini 3.8 Flash TTS 与 Flash-Lite TTS，支持基于提示词的音色设计，可用自然语言描述说话人风格并即时生成语音，且在延迟与成本上更优。文章强调其多语言、情感可控与批量合成能力，适用于有声内容、客服与无障碍场景，是谷歌在语音合成赛道的升级。
---

# 谷歌发布 Gemini 3.8 Flash TTS 与 Flash-Lite TTS：支持提示词定制音色

> 原文链接：https://www.marktechpost.com/2026/09/23/google-releases-gemini-3-8-flash-tts-and-flash-lite-tts-with-prompt-based-voice-design/
> 来源：MarkTechPost

Google has released Gemini 3.8 Flash TTS and Gemini 3.8 Flash-Lite TTS, 2 new text-to-speech models in its Gemini Audio family. Google calls them its most expressive audio generation models yet. Flash TTS targets creative direction and character voices. Flash-Lite TTS targets high-volume, cost-efficient production. Both let developers direct delivery line by line using natural language.

Is it deployable? Yes, both models are rolling out now through the Gemini API and Google AI Studio. Access is API-only, with no open weights for self-hosting. Enterprise API access via Gemini Enterprise is listed as coming soon.

What Google Shipped

The release splits TTS into 2 tiers with shared direction controls:

Gemini 3.8 Flash TTS is built for deep creative direction and character design. Target uses include gaming, immersive audiobooks, podcasts and interactive media. It offers granular control over acting cues, pacing, dialect shifts and backchanneling.

Gemini 3.8 Flash-Lite TTS is built for high-volume, cost-efficient scale. Google positions it for dubbing, audio content creation and expressive voice agents. It offers fine-grained control over tone, pacing and expressive nuance.

In AI Studio, the playground links use the model identifiers gemini-3.8-flash-tts and gemini-3.8-flash-lite-tts.

Voice Design From a Text Prompt

Previous Gemini TTS offered 30 original voices. The 3.8 release moves to a much larger voice system.

Generative voice design: Flash TTS creates new voices from prompts describing role, accent and voice characteristics. This works across more than 100 languages and dialects. Google&#8217;s demos include a Melbourne DJ, a monotone robot and a Japanese dragon.

Voice library: Developers get 2,000+ production-ready voices. Coverage includes regional varieties like Mexican Spanish, Quebec French and Scots English.

Save and scale: Custom voices can be saved and reused, with minimal drift across projects.

Voice remixing (coming soon): Users will adjust a library voice&#8217;s timbre, pitch, pace and accent through prompts.

Directing the Performance

Both models accept stage directions written in the script. Gemini can also steer delivery from natural script cues.

Long-form generation: Voice quality, pacing and timbre hold across hours of continuous audio.

Native 2-speaker staging: A single script drives a multi-turn conversation with distinct, separated voices.

Vocal bursts: Non-verbal cues like <laughs>, <sigh> and <gasp> add conversational texture.

Backchanneling: Active-listening interjections like |mhm| and |yeah| control reaction beats and comedic timing.

Voice Replication and Safety Controls

Voice replication builds a consistent vocal profile from a 30-second audio sample. The sample must be your voice or one you have rights to use. Replication requires a verbal consent recording from the voice owner, matched against the reference speaker.

Every clip from Gemini Audio models carries a SynthID watermark. This imperceptible mark is embedded directly in the audio output. Replicated voices also carry C2PA content credentials. Google points to the Gemini 3.8 Audio model card for its broader safety approach.

Benchmark Results

Google reports these results for the new models:

Hume AI Voice Design Benchmark: Flash TTS ranks #1 overall with a score of 71.4, per Hume AI.

Accent modeling: Flash TTS leads with a score of 60.8.

Hume AI Overall Quality Index: Flash TTS ranks #1 and Flash-Lite TTS ranks #2.

Voice Arena blind preference: Both models take top positions in Japanese, Brazilian Portuguese, Vietnamese, Modern Standard Arabic, Mexican Spanish and Hindi.

&

Key Takeaways

Google launched Gemini 3.8 Flash TTS for creative work and Flash-Lite TTS for scale.

Flash TTS designs new voices from prompts across 100+ languages and dialects.

Developers get 2,000+ production voices, up from 30 originals.

Voice replication needs a 30-second sample plus a matching consent recording.

Flash TTS ranks #1 on Hume AI&#8217;s Voice Design Benchmark with 71.4.

FAQ

What is Gemini 3.8 Flash TTS? It is Google&#8217;s text-to-speech model for creative voice design and line-by-line performance direction. It is available through the Gemini API and Google AI Studio.

How is Flash-Lite TTS different? Flash-Lite TTS is optimized for high-volume, cost-efficient workloads like dubbing and voice agents. It ranks #2 on Hume AI&#8217;s Overall Quality Index.

Can I clone my own voice? Yes, with a 30-second sample and a verbal consent recording. It is unavailable in AI Studio in several regions, including the UK, EEA and India.

Check out the Technical Blog. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google Releases Gemini 3.8 Flash TTS and Flash-Lite TTS With Prompt-Based Voice Design appeared first on MarkTechPost.