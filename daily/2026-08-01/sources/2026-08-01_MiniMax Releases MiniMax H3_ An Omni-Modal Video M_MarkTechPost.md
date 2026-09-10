---
publish_time: 1785572887
status: pending
---

# MiniMax Releases MiniMax H3: An Omni-Modal Video Model That Generates 15-Second 2K Clips With Native Stereo Audio

> 原文链接：https://www.marktechpost.com/2026/08/01/minimax-releases-minimax-h3-an-omni-modal-video-model-that-generates-15-second-2k-clips-with-native-stereo-audio/
> 来源：MarkTechPost

MiniMax releases MiniMax H3, a general-purpose multimodal generation model. MiniMax H3 is not a text-to-video model with add-ons. MiniMax describes it as a general-purpose multimodal generation model that reads text, images, video, and audio as one unified context and returns video with native stereo sound. The mains specs include: 2K output, 4–15 seconds, integer durations only.

Previous video stacks split into text-to-video, image-to-video, first-and-last-frame, subject reference, motion reference, and video editing,  each often a separate expert model. MiniMax H3 folds those into one pretraining paradigm where reference and editing relationships are expressed in natural language. MiniMax&#8217;s example prompt makes the point: reference the camera movement from Video 1, have the character in Image 2 sing, match the vocals to Audio 3.

Is it deployable? 

Today: yes, through the API and no, on your own hardware. MiniMax launched H3 on July 31, 2026 with the model live in the platform API under the model ID MiniMax-H3 and in the consumer Hailuo AI app. 

Industries: MiniMax positions MiniMax H3 for advertising, branding, e-commerce, product design, UI/UX, and gaming along with film pre-visualization and retail catalog media.

Applications: Ad variant generation, product and listing videos, animated posters, film title sequences, website hero loops, character-consistent game cinematics, and video-to-video motion transfer.

The API surface

The video generation guide documents three entry modes: text-to-video, first/last-frame image-to-video, and reference generation. Behind one endpoint and an asynchronous three-step flow: create a task, poll task_id, download content.url.

Input limits worth designing around:

Reference images: up to 9. Reference videos: up to 3 clips, 2–15 s each, ≤15 s total. Reference audio: up to 3 clips, and audio cannot be sent without an accompanying image or video.

Mixed input caps at 12 files total. Prompt length ≤7,000 characters; request body ≤64 MB, with URL input recommended for large assets.

File sizes: video ≤50 MB, image ≤30 MB, audio ≤15 MB, per asset.

Formats: H.264/H.265 video, JPG/PNG/WEBP/HEIC/HEIF images, WAV/MP3 audio.

Four technical pieces doing the work

Contextual Omni Representation: MiniMax rebuilt captioning so it describes the relationship between context and target video, not just the target. Most source material requires roughly 100K tokens of inference, distilled to about 4K tokens on average. Language is the bridge that turns a fixed task set into an open, descriptive one.

H3-VAE: A full tokenizer overhaul. Its high compression ratio delivers a stated 4× gain in effective sequence length, cutting training and inference cost and it is the enabling technology for native 2K.

H3-Omni Transformer: MiniMax explicitly set aside the Hailuo-02 architecture here. Multimodal context tripled sequence-length variance, so the training architecture separates understanding and generation workloads and tunes hardware utilization for each. Reported result: end-to-end training throughput up nearly 30%.

In-Context Regeneration: Instead of a bolt-on super-resolution module, the base model regenerates its own low-resolution output in-context, re-reading the original multimodal context. That is what recovers small text and fine detail that conventional upscalers guess at — directly relevant to brand and product rendering.

&

Price and standing

MiniMax&#8217;s own claim: at 2K, H3&#8217;s per-second price is less than a third of mainstream models; at 768p, less than half the price of mainstream 720p. The company amplified both the launch and the pricing framing on X (1, 2). Third-party trackers and launch coverage put the 2K pay-as-you-go rate at $0.13 per second, about $1.95 for a 15-second clip, but MiniMax&#8217;s pay-as-you-go page still listed only Hailuo 2.3 tiers at the time of writing, so treat that figure as reported, not primary.

On placement: SCMP reports, citing Artificial Analysis, that H3 leads in video editing while trailing Google&#8217;s Gemini Omni Flash in text-to-video and sitting behind both Seedance 2.0 and Gemini Omni Flash in image-to-video. 

Key Takeaways

H3 unifies text, image, video, and audio into one generation model — 2K, 4–15s, native stereo.

Open weights are promised &#8220;in the coming days,&#8221; not shipped; the API is the only path today.

H3-VAE&#8217;s 4× effective sequence-length gain is what makes native 2K economically viable.

In-context regeneration replaces super-resolution, preserving small text and brand marks.

Artificial Analysis ranks H3 first in video editing, behind rivals in text-to-video and image-to-video.

Sentimental Analysis

&

Check out the Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post MiniMax Releases MiniMax H3: An Omni-Modal Video Model That Generates 15-Second 2K Clips With Native Stereo Audio appeared first on MarkTechPost.