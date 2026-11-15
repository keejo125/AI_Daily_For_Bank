---
publish_time: 1789720837
link: https://www.marktechpost.com/2026/09/18/alibaba-qwen-releases-qwen3-8-omni-flash/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  阿里 Qwen 团队发布 Qwen3.8-Omni-Flash，自称首个围绕智能体能力构建的全模态模型，接受文本、图像、音频、视频输入并返回文本，将音视频理解、推理与工具调用统一在同一模型内。其工作流为“理解内容→规划任务→调用工具执行→交付结果”。模型已作为托管 API 上线 QwenCloud、阿里云百炼与 Qwen Studio，支持 1M 上下文；发布时未宣布开放权重，暂不支持私有化部署。该模型延续 Qwen 系列在多模态与智能体方向的推进，强调 agentic audio-video understanding 与 tool use。
---

# 阿里 Qwen 发布 Qwen3.8-Omni-Flash：百万上下文全模态模型，主攻智能体音视频理解与工具调用

> 原文链接：https://www.marktechpost.com/2026/09/18/alibaba-qwen-releases-qwen3-8-omni-flash/
> 来源：MarkTechPost

Alibaba&#8217;s Qwen team has released Qwen3.8-Omni-Flash. They called it its first omni-modal model built around agentic capabilities. It accepts text, images, audio, and video, and it returns text. Audio-video understanding, reasoning, and tool use sit inside one model. The stated workflow is simple: understand the content, plan the task, execute with tools, deliver the result.

Is it deployable? Yes, as a hosted API today. It is live on QwenCloud, Alibaba Cloud Model Studio, and Qwen Studio. No open weights were announced at launch, so self-hosting is not an option.

What is Qwen3.8-Omni-Flash

The Qwen3.8-Omni-Flash is built on the Qwen3.8-Flash-Next architecture. That base model shipped with open weights in August 2026. 

The context window is 1M tokens. QwenCloud lists 991K max input and 131K max output. Max reasoning length is 262K tokens.

Output is text only. The Model Studio docs point developers to Qwen3.5-Omni when they need generated speech. Thinking is on by default, with reasoning_effort set to xhigh. Setting it to none disables thinking.

The API follows both the DashScope and OpenAI protocols. It works with Chat Completions and the Responses API. Function calling, web search, structured outputs, context caching, and batch calls are supported.

Agentic Perception for Long Video

Most video models read a long file from start to finish. That holds even when the answer sits in 3 minutes of footage.

Qwen research team describes a different path. The agent starts from the question. It decides what to watch and hear. It then gathers evidence over several coarse-to-fine rounds. Compute and tokens go to the segments that matter.

The research team reports the result on OmniVideoBench. Accuracy rises from 63.4 to 67.8. Token use drops from 145,736 to 79,117. That is about 45.7% fewer tokens. 

Reported Benchmarks

All figures here come from Qwen. Independent results were not available at publication.

Across 29 evaluations, the average score improves more than 25% over Qwen3.5-Omni-Plus.

WildClawBench-MM improves by 36.5 points. AgenticVBench improves by 22.3 points.

UniClawBench reaches 69.6.

LongAudioSpan gains 8.3 points. OmniVideoBench gains 9.6 points.

OmniCap-IF CSR and ISR improve by 8.5 and 14.1 points.

The research team states that audio-visual performance is close to Gemini 3.8 Flash. It also claims overall audio performance above Gemini 3.8 Flash. The X post summarizes the agent gains as +19.5 points on average across WildClawBench-MM and UniClawBench.

 Meet Qwen3.8-Omni-Flash, Qwen's first omni-modal model built around agentic capabilities!

Native audio-video understanding, reasoning, and tool use come together in one model: understand the content, plan the task, execute with tools, and deliver the result.

Highlights: 
-… pic.twitter.com/iJypeohw7y
&mdash; Qwen (@Alibaba_Qwen) September 18, 2026

Pricing and Input Limits

QwenCloud lists $0.15 per 1M input tokens and $0.47 per 1M output tokens. Implicit cache hits cost $0.016 per 1M tokens.

The research team reports large cost cuts against Qwen3.5-Omni-Plus. Audio input costs over 98% less per hour. Audio-visual input costs over 93% less per hour. The X post puts the video input reduction at about 89%.

Key limits from the Model Studio docs:

Video files up to 2 hours and 2 GB by URL.

Audio files up to 3 hours.

Audio input in 113 languages and dialects.

Stable results with video sampled at up to 15 fps.

Two-channel stereo and four-channel FOA spatial audio through use_multichannel.

Availability in 6 regions: Beijing, Singapore, Hong Kong, Tokyo, Frankfurt, and Virginia.

Calling it takes a few lines with the OpenAI SDK:

Copy CodeCopiedUse a different Browser

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["DASHSCOPE_BASE_URL"],
)
completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[{"role": "user", "content": [
        {"type": "video_url", "video_url": {"url": os.environ["VIDEO_URL"]}},
        {"type": "text", "text": "List the key moments with timestamps."},
    ]}],
    modalities=["text"],
    stream=True,
)
for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

Open-Source Tooling: Qwen-MM-Plugins and Qwen-Live Harness

The model returns text, so tools do the media work. Qwen team is open-sourcing 2 projects to support that.

Qwen-MM-Plugins is live under Apache-2.0. Its tagline is &#8216;Make any agent harness multimodal-native.&#8217; Each capability installs as a Skill plus an optional MCP server. The guided installer supports Claude Code, CodeBuddy, Codex, Qoder, OpenClaw, Qwen Code, and Gemini CLI.

The Omni capabilities map to the launch demos:

omni-memory builds an audio-visual memory of a long video.

omni-video2note converts a tutorial video into an illustrated PDF.

omni-chatcut covers Music-to-MV, movie commentary, and speaker-preserving video translation.

A core plugin lets the main model read local images and video frames natively. The README notes one current gap. Most harnesses cannot feed audio to the main model natively yet. Audio is routed through the API for now.

Interactive Explainer

&&&

Key Takeaways

Qwen3.8-Omni-Flash takes text, image, audio, and video in, and returns text.

It offers a 1M-token context, function calling, web search, and default-on thinking.

Agentic perception lifts OmniVideoBench from 63.4 to 67.8 with about 45.7% fewer tokens.

QwenCloud pricing is $0.15 input and $0.47 output per 1M tokens.

It is API-only at launch, with Apache-2.0 Qwen-MM-Plugins for agent harnesses.

Check out the Technical details, QwenCloud model page, API docs, and GitHub repo. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Alibaba Qwen Releases Qwen3.8-Omni-Flash: A 1M-Context Omni-Modal Model Built Around Agentic Audio-Video Understanding and Tool Use appeared first on MarkTechPost.