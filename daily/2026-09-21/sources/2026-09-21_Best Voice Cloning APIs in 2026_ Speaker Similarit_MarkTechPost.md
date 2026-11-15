---
publish_time: 1789975578
link: https://www.marktechpost.com/2026/09/21/best-voice-cloning-apis-in-2026-speaker-similarity-consent-checks-and-price-per-1m-characters/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  本文盘点2026年主流语音克隆API，从克隆保真度、实时延迟、多语种支持、价格与合规等维度对比ElevenLabs、Cartesia、Resemble AI等厂商。文章指出语音克隆已进入低延迟、高相似度的实用阶段，但深度伪造与授权合规仍是落地门槛，企业应在声纹确权与防滥用上前置设计。
---

# 2026年最佳语音克隆API盘点

> 原文链接：https://www.marktechpost.com/2026/09/21/best-voice-cloning-apis-in-2026-speaker-similarity-consent-checks-and-price-per-1m-characters/
> 来源：MarkTechPost

A stock voice only needs to sound good. A cloned voice must sound like one specific person. That is a harder test, and the 7 Voice cloning providers here handle it very differently.

We recorded one 10-second reference clip and cloned it on every platform. The results sit side by side below, unlabeled, so you can judge before seeing names. We then compare 4 axes that decide deployments: reference audio needed, consent verification, commercial license, and languages.

How the 10-second test works

The reference is 10 seconds of one speaker in a quiet room, saved as WAV. Every platform reads the same 2 sentences. One is conversational; the other packs numbers and a proper name. We use each vendor&#8217;s instant cloning path with default settings.

Two vendors bend the rule. Hume documents 15 seconds as its floor, so its clone uses the same speaker extended to 15 seconds. ElevenLabs recommends 1 to 2 minutes for Instant Voice Cloning, so its 10-second clone runs below vendor guidance.

&&

Comparison at a glance

ProviderReference audio (instant / pro)Consent verificationCommercial license fromLanguagesList price per 1M charsElevenLabs1 to 2 min recommended / 30 min minimumRights attestation for IVC; Voice Captcha for PVCStarter, $6/mo70+ (Eleven v3)$50 (Flash) to $100 (v3)Cartesia10 s, up to 60 s on Sonic 3.6+ / 30 minPermission required by termsPro, $5/mo44About $37 to $50Inworld3 to 30 s / 10 min minimum (beta, English only)Rights confirmationFree On-Demand tier200+ languages and locales$12.50 to $25 (TTS-2)Gradium10 s / 30 min, 2 h recommendedOwner consent required by policyXS, $13/mo5About $36 to $58Fish AudioAbout 10 s / 10 to 180 minLive ownership check for pro clonesPlus, $15/mo83$15 per 1M UTF-8 bytesResemble AI10 s / 10 to 25+ minVerifiable consent for Professional CloneBusiness plan for cloning API23About $30 (estimate)Hume15 s / not documentedUpload from a consenting speakerCreator, $14/mo11$50 to $150 by plan

Credit-plan rates equal plan price divided by included characters. Resemble AI&#8217;s pricing page lists no TTS rate; trackers report $0.0005 per second in mid-2026, converted here at about 1,000 characters per minute. Prices were checked September 20, 2026.

Speaker similarity: what public data shows

Hume published its Voice Replication Leaderboard on September 10, 2026. It tested 11 models on 25 reference voices with 7 prompts. 3 blind raters scored each clip from 1 to 5 on sounding like the reference.

Among vendors here, Fish Audio s2-pro led at 4.03. Cartesia sonic-3.5 scored 3.70, and ElevenLabs Multilingual v2 scored 3.68. Cartesia sonic-3.6-beta scored 3.63, and Inworld TTS-2 scored 3.62. ElevenLabs Eleven v3 ranked last of 11 at 2.91.

The board also shows why one number misleads. Cartesia sonic-3.6-beta topped naturalness at 4.36 yet ranked 8th on identity. Inworld TTS-2 topped audio quality at 4.61. Full per-category data sits on the Hugging Face leaderboard.

Provider breakdown

ElevenLabs

ElevenLabs offers Instant Voice Cloning (IVC) and Professional Voice Cloning (PVC). IVC docs recommend 1 to 2 minutes of clean audio. PVC needs at least 30 minutes, ideally 2 to 3 hours, on the Creator plan or above. It also has the strictest gate here: the voice owner reads on-screen text aloud through Voice Captcha. API rates are $0.10 per 1K characters on Eleven v3 and Multilingual v2. Flash, Turbo, and v3 Conversational cost $0.05. Eleven v3 supports 70+ languages.

Cartesia

Cartesia clones from 10 seconds of audio. Sonic 3.6 and newer use up to 60 seconds to hold accents better. Pro Voice Clones train on 30+ minutes and start on the $49 Startup plan. Sonic bills 1 credit per character. Plans run from $5 for 100K credits to $299 for 8M. Sonic lists 44 languages.

Inworld

Inworld instant clones work from 3 seconds, and samples up to 30 seconds improve similarity. Cloning itself is free. Realtime TTS-2 lists $25 per 1M characters on demand. That falls to $15 at $300 a month and $12.50 at $1,500. TTS-2 Flash starts at $15 and falls to $7. Professional cloning is in beta, needs 10 minutes of audio, and supports English only. Inworld supports 200+ languages and locales, with 15 in its top quality tier.

Gradium

Gradium, founded by Kyutai co-founders, clones from 10 seconds. The free tier includes 5 clones for non-commercial use. Paid plans start at $13 for 225K credits, billed at 1 credit per character. Pro Voice Clone needs 30 minutes minimum and starts on the $340 M plan. Coverage is narrow: English, French, German, Spanish, and Portuguese.

Fish Audio

Fish Audio bills its API at $15 per 1M UTF-8 bytes. English text runs about 1 byte per character. Chinese, Japanese, and Korean run about 3, which roughly triples the effective price. S2.1 Pro covers 83 languages. Instant clones work from about 10 seconds. Professional clones take 10 to 180 minutes and require live ownership verification. Commercial use starts on the $15 Plus plan and covers verified voices you own.

Resemble AI

Resemble AI Rapid Clone needs 10 seconds and finishes in under a minute. Professional Clone needs 10 to 25+ minutes and about 40 minutes of training. It requires explicit, verifiable consent from the voice talent. PerTh watermarking is available on every output. Chatterbox Multilingual covers 23 languages. The catch: Resemble now leads with deepfake detection. Its Voice Cloning API requires a Business plan or higher. Its pricing page no longer lists TTS rates.

Hume

Hume Octave clones from as little as 15 seconds, recorded live or uploaded from a consenting speaker. Octave 2 covers 11 languages. Commercial use starts on Creator at $14 a month; Free and Starter are non-commercial. Hume&#8217;s pricing page lists API access to voice cloning only on Enterprise; other tiers create clones in the platform. Extra characters cost $0.15 per 1K on Creator, down to $0.05 on Business.

Which API fits which job

Budget voice agents at scale: Inworld or Fish Audio.

Low latency with broad language coverage: Cartesia.

Brand voices with strict consent: ElevenLabs PVC.

European languages with a free test tier: Gradium.

Cloning plus watermarking and deepfake detection: Resemble AI.

Emotion-directed delivery: Hume.

Key Takeaways

ElevenLabs is the category default, but its models trail on Hume&#8217;s new same-speaker leaderboard.

Only ElevenLabs, Fish Audio, and Resemble AI document technical consent checks, and only for pro clones.

Inworld and Fish Audio list $25 or less per 1M characters; ElevenLabs v3 lists $100.

Hume needs 15 seconds of audio, so a 10-second clip falls short.

Languages range from 5 (Gradium) to 200+ languages and locales (Inworld).

FAQ

What is the best voice cloning API in 2026? No vendor wins every axis. On Hume&#8217;s September 2026 board, Fish Audio led the vendors here on same-speaker similarity. ElevenLabs offers the strongest consent gate for professional clones.

How much audio does voice cloning need? Instant clones need 3 to 30 seconds on most platforms. Professional clones need 10 to 30 minutes minimum, and 2 hours is often recommended.

Which voice cloning APIs verify consent? ElevenLabs, Fish Audio, and Resemble AI document technical checks for professional clones. The rest rely on attestation and terms of service.

What is the cheapest voice cloning API per 1M characters? Among self-serve list prices, Inworld TTS-2 Flash falls to $7 on higher plans. Fish Audio charges a flat $15 per 1M UTF-8 bytes for S2.1 Pro.

The post Best Voice Cloning APIs in 2026: Speaker Similarity, Consent Checks, and Price per 1M Characters appeared first on MarkTechPost.