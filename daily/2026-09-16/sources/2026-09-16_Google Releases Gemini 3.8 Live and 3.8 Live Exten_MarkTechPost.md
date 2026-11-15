---
publish_time: 1789505589
link: https://www.marktechpost.com/2026/09/15/google-releases-gemini-3-8-live-and-3-8-live-extended-thinking-for-production-grade-voice-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MarkTechPost 同步报道：Google 发布 Gemini 3.8 Live 与 3.8 Live Extended Thinking，为原生语音到语音模型，专为实时语音智能体打造，延续 Gemini Audio 系列。报道指出其瞄准语音 Agent 场景的特定能力缺口。
---

# Google 发布 Gemini 3.8 Live 与 3.8 Live 扩展思考，面向生产级语音智能体

> 原文链接：https://www.marktechpost.com/2026/09/15/google-releases-gemini-3-8-live-and-3-8-live-extended-thinking-for-production-grade-voice-agents/
> 来源：MarkTechPost

Google has introduced Gemini 3.8 Live and Gemini 3.8 Live Extended Thinking, its most advanced live dialogue models to date. Both are native speech to speech models built for real time voice agents. They extend the Gemini Audio family that Google expanded last month with Gemini 3.5 Transcribe. The release targets a specific gap: voice agents that can reason and execute tools without breaking conversational flow.

Is it deployable? Yes, for API based production use. Both models are live today in the Gemini Live API and Google AI Studio. They are hosted models, not open weights, so there is no self hosted option.

&

What Google Released

The launch covers 2 models with distinct roles. Gemini 3.8 Live is built for scale and cost efficiency. It combines conversational intelligence with fluid dialogue and visual grounding. Gemini 3.8 Live Extended Thinking is built for high complexity tasks. It adds increased intelligence and multi step reasoning while it speaks. Google positions both as a streamlined alternative to cascaded speech pipelines that chain ASR, an LLM, and TTS.

Benchmark Results

Gemini 3.8 Live Extended Thinking takes the #1 overall spot on Artificial Analysis&#8217; Speech to Speech Quality Index with a score of 82.6. It leads agentic task completion with 68.6% on τ-Voice and 35.1% on Sierra&#8217;s τ-Voice-banking benchmark. It also scores 97.7% on Big Bench Audio, a reasoning benchmark for audio models. Gemini 3.8 Live secured second place in the Speech Agent Arena, a human preference evaluation. On ServiceNow&#8217;s EVA-Bench, Google reports that the models push the Pareto Frontier for complex workflows. They balance task accuracy with conversational quality, measured on the Live API on Gemini Enterprise Agent Platform.

Capabilities for Developers

The Live API exposes 5 core capabilities in the new models:

Asynchronous function calling: The model executes API and tool calls in the background. Audio responses keep streaming to the user while tasks finish.

Visual context: The model processes live visual inputs in near real time, so agents can understand what users say and see.

Alphanumeric precision: It accurately parses confirmation codes, claim numbers, and technical data, a common failure point in voice systems.

Multilingual support: It automatically detects and transitions between 97 supported languages mid conversation, with accent consistency.

Incremental content updates: It merges real time audio with structured data to return context aware responses.

Extended Thinking adds configurable thinking for multi step reasoning in the background. It reasons and speaks simultaneously, using early verbal cues such as &#8220;Let me check that&#8221; to acknowledge prompts. It then narrates progress step by step while long running tasks execute. Google&#8217;s demos show the model converting sketches plus voice feedback into working React components and coordinating multi step bookings.

Pricing and Ecosystem

Both models are priced at $0.005/min for audio input and $0.018/min for audio output. Google states this estimate is based on $3/1M input tokens and $12/1M output tokens. Developers can also build through Live API integration partners that handle real time media streaming infrastructure. These include Agora, Fishjam, LangChain, LiveKit, Pipecat, Vercel, and Vision Agents. Google is also partnering with Salesforce, Genspark, and Lumeris, which cite the models&#8217; latency, fluidity, and tool calling. Example apps are available on GitHub.

Key Takeaways

Gemini 3.8 Live Extended Thinking ranks #1 on Artificial Analysis&#8217; Speech to Speech Quality Index with 82.6.

It scores 68.6% on τ-Voice, 35.1% on Sierra&#8217;s τ-Voice-banking, and 97.7% on Big Bench Audio.

Gemini 3.8 Live runs tools and API calls in the background while continuing the conversation.

Pricing is $0.005/min for audio input and $0.018/min for audio output via the Live API.

All generated audio carries Google DeepMind&#8217;s imperceptible SynthID watermark.

Check out the technical details and the developer post. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google Releases Gemini 3.8 Live and 3.8 Live Extended Thinking for Production Grade Voice Agents appeared first on MarkTechPost.