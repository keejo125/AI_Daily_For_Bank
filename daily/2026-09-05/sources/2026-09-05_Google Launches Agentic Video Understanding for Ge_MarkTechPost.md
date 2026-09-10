---
publish_time: 1788583045
link: https://www.marktechpost.com/2026/09/04/google-agentic-video-understanding-gemini-flash-models/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google本周为Gemini Flash系列推出智能体式视频理解能力。传统做法以固定1帧/秒一次性摄入整段视频，无论问题是“总结”还是“演讲何时切到报价页”都付出全时间线成本。新方案下Gemini主动“导航”时间线，自行决定看什么、以何种帧率、经何种模态处理。Google称视频token最多减少88%、成本最多降66%、标准视频基准准确率最高提升7%。该能力仅作为托管API特性提供（AI Studio与Gemini企业智能体平台），无开源权重、不可自托管。
---

# Gemini Flash 智能体式视频理解上线，视频 Token 最多降 88%

> 原文链接：https://www.marktechpost.com/2026/09/04/google-agentic-video-understanding-gemini-flash-models/
> 来源：MarkTechPost

Video has been the most expensive modality to reason over. A Gemini model handed a 90-minute lecture has, until now, ingested the whole thing at a fixed one frame per second, whether the question was &#8216;summarize this&#8217; or &#8216;what time does the speaker switch to the pricing slide?&#8217; That single-pass design forces a bad trade: pay for the full timeline in context, or pre-chunk the video and risk dropping the detail that mattered.

This week, Google launched agentic video understanding across its Flash models. Instead of ingesting the timeline, Gemini navigates it deciding what to watch, at what frame rate, and through which modality. Google reports up to 88% fewer tokens, up to 66% lower cost, and up to 7% higher accuracy on standard video benchmarks.

Is it deployable? Yes, but only as a hosted API feature. There are no open weights and nothing to self-host. It ships through the Gemini API in Google AI Studio and the Gemini Enterprise Agent Platform, works with both file uploads and public YouTube URLs, and bills at standard Gemini API token pricing with no additional feature fee.

What actually changed

Static processing, still the default on every Gemini model, extracts frames at 1 FPS in a single pass, processes audio at 1 Kbps single channel, and inserts timestamps every second. Agentic processing replaces that with a loop. The model pairs its own reasoning with native video tools to search, scan, and inspect target segments across frames, audio, and transcripts, loading only what the prompt requires. Developers could already assemble this by hand; the change is that Gemini runs the loop internally, which is where the development overhead disappears.

Across Google&#8217;s evaluations, Gemini 3.7 Flash with agentic understanding lands on the accuracy-to-cost Pareto frontier for video analysis among the models tested. The efficiency gains concentrate on long-form content, from 10-minute how-to guides to multi-hour recordings.

&&&

What the API returns

Agentic processing adds two step types to the response steps array: a processing_call when the model requests a segment or transcript, and a matching processing_result when that load completes. They interleave with thought steps and precede model_output, so they can drive a live progress trace in your UI. Their presence is also how you verify agentic mode actually ran.

Token accounting splits accordingly. Navigation reasoning bills as thought tokens (total_thought_tokens); frames, audio, and transcripts loaded on demand bill as tool-use tokens (total_tool_use_tokens).

Enabling it is one field on the video part:

Copy CodeCopiedUse a different Browser

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "video",
            "uri": "https://youtu.be/7Z5Vy9JBANs",
            "processing": "agentic"
        },
        {
            "type": "text",
            "text": "What are the 3 most important announcements in this keynote?",
        },
    ],
)

You can also mix modes per video inside a single request, agentic on the long lecture, static on the short clip.

Key Takeaways

Agentic mode lets Gemini navigate a video timeline instead of ingesting it at a fixed 1 FPS.

Google reports up to 88% fewer tokens, 66% lower cost, and 7% higher accuracy on video benchmarks.

Supported on Gemini 3.8, 3.7, 3.6 Flash and 3.5 Flash-Lite; enabled by one processing field.

Static remains better for clips under five minutes and for frame-by-frame precision work.

Standard API pricing applies, but navigation reasoning is billed as thought tokens.

Check out the Google blog, Gemini API video understanding docs, Developer guide in AI Studio and Agentic vision announcement. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google Launches Agentic Video Understanding for Gemini Flash Models, Cutting Video Tokens by Up to 88% appeared first on MarkTechPost.