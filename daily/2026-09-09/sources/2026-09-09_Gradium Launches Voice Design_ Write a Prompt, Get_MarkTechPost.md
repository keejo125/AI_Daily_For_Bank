---
publish_time: 1788938953
link: https://www.marktechpost.com/2026/09/09/gradium-launches-voice-design-write-a-prompt-get-a-brand-new-synthetic-voice-in-seconds/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  巴黎语音 AI 公司 Gradium（脱胎于 Kyutai 实验室）推出 Voice Design：输入一段文字描述即可在数秒内生成全新合成音色，无需参考音频、无需授权清算。该能力已上线 Gradium API 与 Studio，免费层可用，生成音色运行在与目录音色相同的流式 TTS 端点上，延迟与格式一致。对语音 Agent 团队而言，“选角 brief”即是 API，用描述替代传统录音克隆，规避了 sourcing、consent 与 license 等合规负担。
---

# Gradium Voice Design 发布：文字描述即可生成全新合成音色

> 原文链接：https://www.marktechpost.com/2026/09/09/gradium-launches-voice-design-write-a-prompt-get-a-brand-new-synthetic-voice-in-seconds/
> 来源：MarkTechPost

Voice agent teams keep hitting the same wall. The catalog holds 400 voices and the brief asks for the one that is not in it: a Quebecoise receptionist for a Montreal dealership, a narrator in his sixties with lecture hall authority. Briefs outnumber any catalog, and cloning closes the gap one speaker at a time, each carrying sourcing, consent and a licence.

Gradium, the Paris-based voice AI company spun out of the Kyutai research lab, has shipped a different answer. Voice Design reads a written description and returns complete new voices in a few seconds. No reference audio, no speaker, no rights to clear.

Is it deployable? Yes, Voice Design is live in the Gradium API and in Studio, free on every plan including the free tier, and a kept voice runs on the same streaming Text-to-Speech endpoint as any catalog voice, at the same latency and output formats.

The casting brief is the API

The description is the only input the model gets. Gradium&#8217;s documentation lists the attributes it responds to, and they read like a casting call: gender, age band, accent or origin, pitch, pace, energy, timbre and resonance, register and manner, and the job the voice is doing. Descriptions run 1 to 500 characters in English, French, Spanish, Portuguese or German. Gradium advises ending with the intended use, because it steers delivery and register rather than only the colour of the voice.

One request returns 1 to 5 candidates, typically ready in 3 to 5 seconds. They are variations on a single character, so a different character means a different description, not more samples.

From candidate to production voice

The flow is four calls. POST /voice-generator/generate mints candidate ids with ready: false. GET /voice-generator/embeddings polls until they flip. Each candidate auditions through the ordinary TTS endpoint, using the candidate id as voice_id. POST /voices/from-embedding promotes the one you keep.

Candidates carry three restrictions converted voices do not: audition text is capped at 100 characters, they are REST only, and the TTS WebSocket and Speech-to-Speech reject them. Unconverted candidates are deleted after 30 days. Converting is free, clears the expiry, and uses one custom voice slot shared with clones. The free tier holds 5, paid plans 1,000.

Sampling is deliberately non-deterministic. Gradium team expands the description first, and that expansion varies per request, so the same prompt with a fixed seed still yields a different voice. 

The benchmark, and how to read it

Gradium ran a blind pairwise listening test on accent prompts across six voice design systems reachable through public APIs and five languages. Native speakers heard two unlabelled clips and picked the closer match, or a tie. Across 7,627 comparisons, Gradium reports a 72.6% win rate against the field, 13.6 points ahead of ElevenLabs eleven_ttv_v3 at 59.0%, followed by Inworld at 44.8%, Fish Audio at 36.7% and MiniMax at 31.7%. Win rate is wins plus half of ties, so 50% is par. Gradium placed first in all five languages. The widest margins came on regional accents that most catalogs flatten: Quebecois French at 97%, Rioplatense Spanish at 86%, Bavarian German at 85%, Colombian Spanish and African Portuguese at 83%.

A model judge over the same prompt set agreed. Gemini 3.1 Pro rated single unlabelled clips from 1 to 5 and produced the same ranking: Gradium 4.06, ElevenLabs 3.86, Inworld 3.64, Fish Audio 3.51. Separately, the product page claims 83.4% prompt adherence on the English split of InstructTTSEval, the academic benchmark for instruction following in TTS. (Note: All of these numbers are vendor designed and vendor run.)

Key Takeaways

Voice Design turns a 500 character description into up to 5 new voices in seconds, no reference audio required.

It is live and free on every Gradium plan, in the API and Studio, across 5 languages.

Vendor run blind tests put it at a 72.6% win rate over 7,627 comparisons, first in all 5 languages.

Kept voices become a normal voice_id on REST, WebSocket and Speech-to-Speech.

Sampling is non-deterministic, so an unsaved candidate is gone for good after 30 days.

Check out the Technical details and Docs. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Gradium Launches Voice Design: Write a Prompt, Get a Brand New Synthetic Voice in Seconds appeared first on MarkTechPost.