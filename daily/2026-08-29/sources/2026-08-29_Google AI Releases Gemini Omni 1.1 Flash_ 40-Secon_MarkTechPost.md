---
publish_time: 1788013844
link: https://www.marktechpost.com/2026/08/29/google-ai-releases-gemini-omni-1-1-flash-40-second-scene-extension-first-last-frame-control-and-4k-upscaling/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  谷歌发布 Gemini Omni 1.1 Flash，将原生多模态视频生成/编辑模型从「能生成」推向「可导演」：场景延展可读取长达 10 秒前文（原为末帧 1 秒），以 10 秒为步累至 40 秒；支持钉住首/尾帧控制运镜，并以 <VIDEO_REF_N> 等标签保证角色一致性；360p 草稿速度较 720p 快 60%、成本仅三分之一，正片超分至 4K。通过 Gemini API 与 Enterprise Agent Platform 开放，Adobe、Figma、Runway 等已用于生产，所有生成视频带 SynthID 水印。
---

# 谷歌发布 Gemini Omni 1.1 Flash：40秒场景延展、首尾帧控制与4K超分

> 原文链接：https://www.marktechpost.com/2026/08/29/google-ai-releases-gemini-omni-1-1-flash-40-second-scene-extension-first-last-frame-control-and-4k-upscaling/
> 来源：MarkTechPost

Google has released Gemini Omni 1.1 Flash (gemini-omni-1.1-flash), a production update to its native multimodal video generation and editing model. The release moves Omni from a capable generator to a directable one: scene extension now reads up to 10 seconds of prior context instead of a single final frame, first and last frames can be pinned to control camera movement, drafts render in 360p at a third of 720p cost, finals upscale to 4K, and video clips can be passed as references for character consistency. 

Gemini Omni Flash is built on three properties Google distinguishes from prior video models: native multimodality (text, image, audio, and video processed together), conversational editing through the Interactions API, and world knowledge inherited from Gemini. Editing is stateful — you pass previous_interaction_id and the model applies your change while preserving what you did not mention, without re-uploading the prior video.

Is it deployable?

It is available through the Gemini API in Google AI Studio and the Gemini Enterprise Agent Platform, with Adobe, Figma Weave, GMI Cloud, and Runway already named as production users.

&&

Scene Extension is the Main Change

Omni 1.1 analyzes up to 10 seconds of prior context when continuing a clip. Google states that previous models referenced only the final second. Extensions run in 10-second increments to a cumulative 40 seconds, and the model generates a 3–10 second continuation per call. Some final frames of the input are edited to make the seam continuous.

The constraints are specific. Extension appends to the end of a clip only — no prepending, no mid-clip insertion. Uploaded input videos must be 10 seconds or shorter, unless you are extending a model-generated video in multi-turn. You cannot add new dialogue when extending an uploaded video where someone is speaking; spoken dialogue is supported in multi-turn extension via previous_interaction_id.

Keyframes and Video References

You can now supply a first and last frame and have the model generate the continuous video between them, which is the mechanism behind orbits, dolly-zooms, and seamless loops. Prompts bind media to roles with tags: <FIRST_FRAME>, <LAST_FRAME>, <IMAGE_REF_N>, and <VIDEO_REF_N>.

Video references accept a maximum of three clips, up to three seconds each, and work best for likenesses. Audio inside a video reference is ignored. Reasoning across multiple videos is not supported and may degrade output.

Cost Control: Draft in 360p, Ship in 4K

The resolution parameter in response_format takes 360p, 720p (default), 1080p, and 4k, with the top two upscaled. Google reports 360p previews generate up to 60% faster and at a third of the cost of 720p, based on system throughput of 360p versus 720p. That makes the draft-then-upscale loop the intended production pattern: iterate cheaply, render once.

Pricing, provenance, and limits

Input is $1.50 per 1M tokens (text, image, video, audio). Output is $9.00 per 1M text tokens and $17.50 per 1M video tokens. Video billing runs at 5,792 tokens per second of 720p, an effective ~$0.10 per second under standard pricing.

Every generated video carries SynthID watermarking — invisible to viewers, programmatically detectable for provenance. Notable gaps: no system instructions, temperature, top_p, stop sequences, or negative prompts (negatives go in the prompt text); voice editing is unsupported; audio references are unsupported; YouTube URLs cannot be used as a source. English is fully supported; other languages are unevaluated. For outputs above 4MB, use delivery="uri" and poll the Files API until the file is ACTIVE.

Google names Adobe (Firefly), Figma Weave, GMI Cloud, and Runway as customers already running Omni Flash in production. The model is also live in Google Flow for AI Plus, Pro, and Ultra subscribers, with scene extension in the Gemini app.

Comparison

&&

Key Takeaways

Scene extension now reads 10s of prior context, up from one final second, and stacks to 40s total.

First/last frame interpolation plus <VIDEO_REF_N> tags give shot-level camera and character control.

360p drafts run up to 60% faster at a third of 720p cost; 1080p and 4K are upscaled outputs.

Paid tier only — ~$0.10 per second of 720p video, no free tier, no provisioned throughput.

Check out the Google blog announcement, Gemini API Omni documentation, Gemini API pricing, and Omni quickstart cookbook. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google AI Releases Gemini Omni 1.1 Flash: 40-Second Scene Extension, First/Last Frame Control, and 4K Upscaling appeared first on MarkTechPost.