---
publish_time: 1788233945
link: https://www.marktechpost.com/2026/08/31/gradium-ai-releases-new-default-tts-model-81-0-hard-case-pass-rate-at-216-ms-time-to-first-audio/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Gradium AI 发布新默认 TTS 语音模型并设为全线默认，主打语音智能体最易出错的「硬案例」：订单号、回拨数字、邮箱等关键信息。新模型硬案例通过率达 81.0%，首音频延迟（Time-to-First-Audio）仅 216 毫秒，在准确率与响应速度间取得平衡，适用于客服、外呼等实时语音场景。该模型面向语音 Agent 落地中的可靠性痛点，降低关键信息念错率，提升通话体验。
---

# Gradium AI 发布默认 TTS 语音模型：硬案例通过率81%、首音频延迟216毫秒

> 原文链接：https://www.marktechpost.com/2026/08/31/gradium-ai-releases-new-default-tts-model-81-0-hard-case-pass-rate-at-216-ms-time-to-first-audio/
> 来源：MarkTechPost

Voice agents fail on exactly the parts of a call that matter most: the order number, the callback digits, the email address the caller has to write down. Gradium AI has released a new text-to-speech model and made it the default across its API and Studio. The company reports an 81.0% human-rated pass rate on a 500-sentence hard-case set spanning five languages, ahead of Cartesia Sonic 3.6 at 75.1% and ElevenLabs v3 Conversational at 65.4%. Time to first audio is 216 ms at P50 on Coval, 170 ms faster than the model it replaces. 

Is it deployable?

Yes, today, with no migration. Gradium switched the model on as the default across its API and Studio on August 31, 2026. Existing voices, including custom clones, keep working unchanged.

&&&

The accuracy number

Gradium built a 500-sentence evaluation set and open-sourced it on Hugging Face under CC BY 4.0: 100 items across 10 criteria in five languages (EN, DE, FR, ES, PT). Seven atomic criteria cover spelling, acronyms, alphanumeric tokens, dates, regular numbers, large and floating numbers, and email. Three composite criteria (Orders, IT Ticket, Claims) stack several of those into one realistic agent turn.

Scoring is human and strict. A sentence passes only if an independent native-speaker rater hears every element pronounced correctly and completely; one dropped digit fails the sentence. Audio was loudness-normalized, order randomized, and raters capped at 40 comparisons with an enforced break.

Pooled across the ten criteria and averaged over the five languages with equal weight: Gradium TTS 81.0%, Cartesia Sonic 3.6 75.1%, ElevenLabs v3 Conversational 65.4%, Fish Audio S2.1 Pro 49.5%, Inworld TTS 1.5 Max 46.5%. All generated in August 2026 with default settings.

The latency number

On Coval&#8217;s TTS benchmark, Gradium reports a 216 ms P50 time to first audio, 170 ms faster than the model it replaces. The more useful figure is the spread: a 30 ms p75-p25 interquartile range across 480 runs, the tightest of the five models tested. Cartesia Sonic 3.6 sits at 454 ms median with a 165 ms spread, 36% of its own median, and callers experience tail turns rather than medians.

Gradium is not the fastest model on that chart. Inworld TTS 2 posts a 166 ms median; Fish Audio S2.1 Pro (291 ms) and ElevenLabs v3 Conversational (329 ms) trail Gradium. The claim being made is about joint position: the lowest hard-case failure rate at sub-250 ms first audio, with very little variance.

Getting started

Existing users need do nothing. New teams install the Python SDK, point at the WebSocket TTS endpoint, and reuse existing voice IDs. Gradium is offering 1M credits for complete hard-case failure reports on its Discord.

Key Takeaways

New Gradium TTS model is live and default as of August 31, 2026; no migration needed.

81.0% human-rated pass rate on 500 hard sentences, ahead of Cartesia, ElevenLabs, Fish Audio and Inworld.

216 ms P50 time to first audio on Coval, with a 30 ms interquartile spread over 480 runs.

Reads phone numbers, emails, IBANs and reference codes with no text normalization required.

Vendor-run benchmark, but the 500-sentence evaluation set is open on Hugging Face under CC BY 4.0.

Check out the release post and the dataset. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Gradium AI Releases New Default TTS Model: 81.0% Hard-Case Pass Rate at 216 ms Time-to-First-Audio appeared first on MarkTechPost.