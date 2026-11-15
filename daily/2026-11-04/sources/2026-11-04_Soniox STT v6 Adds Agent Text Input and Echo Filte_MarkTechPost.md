---
publish_time: 1793737102
link: https://www.marktechpost.com/2026/11/03/soniox-stt-v6-agent-text-input-echo-cancellation/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Soniox发布语音转文本API STT v6，新增文本输入通道与回声过滤，面向语音智能体场景。
---

# Soniox 发布 STT v6：为语音智能体加入文本输入与回声过滤

> 原文链接：https://www.marktechpost.com/2026/11/03/soniox-stt-v6-agent-text-input-echo-cancellation/
> 来源：MarkTechPost

Soniox has released Soniox STT v6, the latest generation of its speech-to-text API. Soniox STT v6 is a speech-to-text model that reads what a voice agent says while hearing the caller. It uses that text to recognize short replies and to drop the agent&#8217;s own voice. The release ships as stt-rt-v6 for streaming and stt-async-v6 for files, across 60+ languages.

TL;DR

Size: Soniox STT v6 is a proprietary hosted model, no parameter count published.

Runs on: Soniox cloud API only (WebSocket streaming and async REST). No self-hosted or on-device option disclosed.

Performance: Soniox calls it &#8220;significantly&#8221; more accurate than v5, but publishes no v6 numbers yet.

Best: Price. $0.12/hour streaming and $0.10/hour async, with diarization and language ID bundled.

Worst: Zero independent v6 results. Its v5 predecessor scored 1.34% semantic WER on Pipecat, behind v4&#8217;s 1.25%.

What problem does Soniox STT v6 solve?

In a cascaded voice agent, STT usually hears only the caller. It never sees the question being answered.

Short answers suffer most. In Soniox&#8217;s docs, &#8220;River Roast&#8221; becomes &#8220;River Road&#8221; and &#8220;a tow&#8221; becomes &#8220;a tour.&#8221;

The second problem is echo. Agent audio leaks back through speakerphones and laptops, gets transcribed as user speech, and the agent interrupts itself.

How does agent text input work?

You enable it with one flag in the start request: "enable_agent_text_input": true. It is only available on stt-rt-v6, not the async model.

While the agent speaks, you stream its words on the same WebSocket as the caller&#8217;s audio. Each message is a small JSON frame: {"type": "agent_text", "text": "...", "end_of_segment": true}.

Timing matters. Messages carry no timestamps, so the model places text where it arrives in the audio stream. Soniox recommends sending each piece 500 ms to 1 second before playback, paced by TTS timestamps.

On barge-in, you flush what was already played, send end_of_segment: true, and drop the unplayed rest. The agent&#8217;s text never appears in the returned transcript.

How does agent voice echo cancellation work?

With agent text input on, v6 knows what the agent is saying. It uses that to separate leftover agent audio from caller speech and filter it out.

It keeps listening during playback, so callers can still interrupt. It does not replace acoustic echo cancellation. It handles what your existing AEC leaves behind, so keep AEC on.

What else changed in v6?

Better voice typing: numbers, currencies, units, dates, IDs, names and specialized terms.

Spoken commands like &#8220;period&#8221; or &#8220;new line&#8221; are written as words, so your app applies them.

Improved meeting transcription and speaker diarization, live or recorded.

Stronger accents, code-switching and language switching within a sentence.

There is one formatting change to test before upgrading. v6 writes &#8220;15 dollars and 20 cents&#8221; as spoken, not &#8220;$15.20&#8221;. Hyphens in codes appear only when spoken.

&&

How does Soniox compare on benchmarks?

Soniox has not published v6 accuracy or latency numbers. Its benchmarks page still reports v5 on the open-source Pipecat STT benchmark. It uses 1,000 real-world samples and measures semantic WER plus time to final segment (TTFS).

On it, stt-rt-v5 scores 1.34% semantic WER, 83.3% perfect transcripts and 260 ms median TTFS. Its P95 latency is 305 ms. Azure posts the lowest WER mean at 1.21%, but at 1,016 ms median latency.

FeatureSoniox stt-rt-v6AssemblyAI Universal-3.5 Pro RealtimeDeepgram Nova-3ElevenLabs Scribe v2 RealtimeModel sizeNot disclosedNot disclosedNot disclosedNot disclosedStreaming languages60+1860+ (Nova models)90+Streaming price / hour$0.12$0.45$0.46 mono, $0.55 multi$0.39Agent-side text contextYes, timed agent_textYes, agent_contextNot disclosedNot disclosedModel-level agent echo filteringYesNot disclosedNot disclosedNot disclosedDiarization costIncludedNot disclosed+$0.0020/minNot disclosedPipecat semantic WER mean1.34% (v5; v6 untested)1.44%1.71% (nova-3-general)3.16%Pipecat perfect transcripts83.3% (v5)84.7%76.5%81.3%Pipecat TTFS median260 ms (v5)282 ms247 ms281 ms

Pipecat figures from the Pipecat STT benchmark README. Soniox numbers are for v5, since v6 has not been benchmarked yet.

Is Soniox really the first?

Soniox calls v6 the first model that knows what your voice agent is saying. That claim needs a qualifier.

AssemblyAI shipped agent context in Universal-3.5 Pro Realtime in July 2026. It also feeds the agent&#8217;s replies into streaming STT.

The clearer difference is echo. Soniox&#8217;s docs describe filtering leaked agent audio using that text. AssemblyAI&#8217;s context docs describe no such filtering.

Deployment, pricing and migration

v6 is a drop-in swap: change the model name to stt-rt-v6 or stt-async-v6.

The v5 models are deprecated and will be removed on December 15, 2026. After that, v5 requests route to v6 automatically.

Pricing is token-based. Soniox lists about $0.12/hour streaming and $0.10/hour async. Agent text is billed as input text tokens, at $4.00 per 1M on real-time.

Key Takeaways

Soniox STT v6 reads the agent&#8217;s text to transcribe caller replies.

Echo filtering removes leaked agent voice, on top of normal AEC.

Streaming costs $0.12/hour, with diarization included.

No v6 benchmark numbers exist yet; v5 scored 1.34% on Pipecat.

v5 models retire December 15, 2026, with automatic routing to v6.

Check out the Soniox STT v6 announcement, the agent text input docs and the v6 changelog. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Soniox STT v6 Adds Agent Text Input and Echo Filtering for Voice Agents appeared first on MarkTechPost.