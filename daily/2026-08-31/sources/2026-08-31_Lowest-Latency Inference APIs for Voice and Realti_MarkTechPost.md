---
publish_time: 1788125078
link: https://www.marktechpost.com/2026/08/30/lowest-latency-inference-apis-for-voice-and-realtime-agents-a-time-to-first-token-ttft-first-benchmark/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  MarkTechPost 评测语音与实时智能体场景的各层推理 API 延迟，指出 TTFT（首 token 时延）是选型常用但易误导的指标：它只标记生成起点，而语音智能体要等整句生成、经 TTS 后才能「说话」。文章逐层基准 LLM、语音识别、语音合成与语音到语音，强调真实对话体验取决于全栈时延预算而非单一 TTFT。
---

# 语音与实时智能体最低延迟推理 API：以首 token 延迟（TTFT）为核心的基准评测

> 原文链接：https://www.marktechpost.com/2026/08/30/lowest-latency-inference-apis-for-voice-and-realtime-agents-a-time-to-first-token-ttft-first-benchmark/
> 来源：MarkTechPost

Time to first token (TTFT) is the metric teams use to pick an inference API for voice. It is also the metric that misleads them. TTFT marks when generation starts; a text-to-speech model cannot speak until a full clause arrives. Between those two points sits the difference between an agent that feels conversational and one that gets interrupted. This piece benchmarks every layer of the voice stack including LLM, speech-to-text, text-to-speech, and speech-to-speech.

Why TTFT Is the Right Entry Point and the Wrong Finish Line

A voice agent is a latency budget with a language model inside it. Every stage spends milliseconds the user can hear.

Time to first token (TTFT) is the interval between sending an inference request and receiving the first token back. IBM&#8217;s definition frames it as the moment a system transitions from idle to visibly active.

For chat, TTFT is close to the whole story. For voice, it is one term in a sum.

The reason is mechanical. A text-to-speech model cannot synthesize half a word. It needs a complete clause or sentence before it produces audio. LiveKit calls the resulting metric time-to-first-sentence (TTFS), and argues in its Gemma 4 deployment post that TTFS is what users actually feel.

That gives you two knobs rather than one. TTFT controls when generation starts. Tokens per second controls how fast the first sentence completes. A provider that wins one and loses the other will not feel fast.

The Latency Budget: What One Voice Turn Actually Costs

LiveKit&#8217;s voice agents overview breaks a turn into STT at roughly 100–200ms, LLM at 300–500ms with streaming, TTS at 100–200ms, and network at 50–150ms over WebRTC. It puts the practical end-to-end target at 700ms to 1.2s.

Kwindla Hultman Kramer, co-creator of Pipecat, has advised targeting 800ms median voice-to-voice latency, with a looser 1,500ms acceptable for a proof of concept. His rough arithmetic splits that four ways at roughly 200ms each: transport and media processing, STT plus phrase endpointing, LLM inference, and TTS.

Daily&#8217;s earlier work on the fastest voice bot supplies the human baseline. Typical human response time in conversation is around 500ms. Pauses beyond 800ms start to feel unnatural.

Daily&#8217;s February 2026 voice-agent LLM benchmark translates that into an LLM requirement directly. Natural conversation needs voice-to-voice under 1,500ms, which works out to roughly 700ms of TTFT budget for a text-mode LLM inside a transcription-to-LLM-to-voice harness.

That 700ms number is the bar to hold every provider against.

How to Read a TTFT Benchmark Without Being Misled

Before the tables, five methodology facts that change what the numbers mean:

1. Workload shape dominates: Artificial Analysis changed its default workload in March 2026. The site now reports 10k input token prompts rather than 1k. Longer prompts raise both TTFT and output speed. LiveKit argues this is closer to reality for voice, because production agents front-load policy, persona, escalation rules, retrieved data, and tool schemas.

2. Server location is baked in: Artificial Analysis tests from a virtual machine in Google Cloud&#8217;s us-central1-a zone. It states plainly that TTFT includes network latency and may advantage or disadvantage providers based on where they serve.

3. Reasoning tokens count: In the Artificial Analysis definition, TTFT for a reasoning model is the first reasoning token, not the first answer token. Those are separate columns.

4. Measure from the receiving side: Daily notes that model providers sometimes quote TTFT internal to their inference stacks. Daily measures from request send to first usable token off the API.

5. Runs are not repeatable: Daily is blunt about this: TTFT varies substantially between benchmark runs, and providers change inference stacks and sometimes weights without changing model names.

Layer 1: LLM Time to First Token

Figures below are from the Artificial Analysis API providers leaderboard, retrieved August 30, 2026. The &#8220;first chunk&#8221; column is TTFT. Workload is 10k input tokens, single prompt, median over 72 hours.

Lowest measured first-chunk latency

ProviderModelTTFTOutput speedBasetengpt-oss-120b (high)0.23s266 tok/sBasetengpt-oss-120b (low)0.24s271 tok/sDeepInfraNemotron 3 Ultra0.28s371 tok/sCohereNorth Mini Code0.32s104 tok/sCohereCommand A+0.40s239 tok/sBasetenInkling Small0.42s337 tok/sModularGemma 4 31B (NVFP4)0.44s243 tok/sNebiusGLM-5.3-Flash0.46s206 tok/sFireworksNemotron 3.5 Lightning0.46s501 tok/sTogether AIKimi K2.7 Code0.47s245 tok/sCerebrasgpt-oss-120b (high)0.49s1,697 tok/s

The throughput trap

Silicon vendors optimize for a different metric than voice agents need.

ProviderModelTTFTOutput speedCerebrasgpt-oss-120b (high)0.49s1,697 tok/sCelerisCeleris-10.62s1,612 tok/sCerebrasGemma 4 31B0.53s1,351 tok/sGroqgpt-oss-20b (high)0.82s957 tok/sSambaNovagpt-oss-120b (high)0.92s706 tok/sGroqgpt-oss-120b (low)0.69s473 tok/sInceptionMercury 23.07s770 tok/s

Mercury 2 is the clearest illustration. It is a diffusion-based language model, and it generates 770 tokens per second. Its first chunk arrives at 3.07s. That is four times the entire LLM budget for a natural conversation.

Cerebras and Groq are a different case. Their TTFT is respectable and their throughput is exceptional. For TTFS specifically, that combination is strong, because the sentence completes almost immediately after the first token lands.

Frontier and proprietary endpoints

ProviderModelTTFTOutput speedAmazon BedrockGPT-5.6 Luna (non-reasoning)0.59s181 tok/sAmazon BedrockGPT-5.6 Terra (non-reasoning)0.72s103 tok/sOpenAIGPT-5.6 Luna (non-reasoning)0.74s113 tok/sGoogleGemini 3.7 Flash (low), AI Studio0.84s315 tok/sAnthropicClaude 4.5 Haiku (non-reasoning)0.84s82 tok/sAmazon BedrockNova Micro0.86s264 tok/sGoogleGemini 3.5 Flash (minimal), AI Studio0.90s202 tok/sOpenAIGPT-5.6 Sol (non-reasoning)1.06s71 tok/s

Note the same model on different hosts. GPT-5.6 Luna non-reasoning measures 0.59s on Amazon Bedrock and 0.74s on OpenAI&#8217;s own API. Hosting and routing matter as much as the weights.

The vendor-measured outlier

LiveKit publishes TTFT figures for its own inference product. Gemma 4 31B on LiveKit Inference measured 192ms, against Gemini 2.5 Flash at 911ms, GPT-5.5 at 966ms, GPT-4.1 at 1,006ms, and the same Gemma 4 31B via OpenRouter at 1,876ms.

LiveKit is transparent about the mechanism, which makes the claim more credible than most. It runs Gemma behind SGLang with speculative decoding, and deliberately under-packs each GPU so queueing delay stays low. A warm request, it says, starts returning tokens in around 100ms. The tradeoff is cost, at $1.20 per 1M output tokens.

The same post reports TTFS across full conversations: 354ms for Gemma 4 31B on LiveKit, 1,034ms for Gemini 2.5 Flash, 1,088ms for GPT-4.1, 1,267ms for Gemini 3.0 Flash, and 1,404ms for GPT-5.5.

Capability numbers accompany it. On IFBench, independently scored by Artificial Analysis, Gemma 4 31B scores 75.6% against GPT-5.5 at 75.9%, GPT-4.1 at 43%, and Gemini 2.5 Flash at 39%. On τ²-bench, GPT-5.5 leads at 93.9% with Gemma 4 31B at 76.9%.

Layer 2: Speech-to-Text and Turn Detection

For voice, STT latency is not transcription speed. It is how long after the user stops talking the pipeline knows the user stopped talking.

Artificial Analysis measures two things on its streaming STT leaderboard, both starting from a SileroVAD-detected end of speech: time to first partial transcript, and time to final transcript. Its AA-WER Streaming index draws on roughly 8 hours of audio, weighted AA-AgentTalk 50%, VoxPopuli 25%, Earnings-22 25%.

Vendor-published latency figures:

ModelClaimSource typeDeepgram Flux~260ms p50 end-of-turn detection at defaultsVendor docsDeepgram Nova-3Sub-300ms streaming latencyVendor docsAssemblyAI Universal-Streaming~300ms immutable word emissionVendorCartesia Ink-2100ms transcript latencyVendorSpeechmatics Voice SDK0.451 ± 0.022s end-of-speech to finalsVendor internal tool

Deepgram Flux is the most architecturally interesting entry. It folds end-of-turn detection into the recognition model rather than bolting a VAD on top. Deepgram states this can cut agent response latency by 200–600ms versus a traditional STT-plus-VAD pipeline. It exposes eot_threshold (0.5–0.9), eager_eot_threshold (0.3–0.9), and an EagerEndOfTurn event that lets you start the LLM early.

That last capability matters more than the raw number. If you can begin generation on an eager signal, you move LLM TTFT off the critical path entirely when the prediction is right.

AssemblyAI Universal-Streaming inverts the usual partials-then-finals model by emitting immutable transcripts. AssemblyAI reported 307ms median word emission against 516ms for Deepgram Nova-3 in its own 2025 measurement. Its docs also recommend using unformatted transcripts for voice agents, since formatting arrives later and rarely changes LLM behavior.

Accuracy claims here are contested and vendor-published. AssemblyAI reports Universal-3.5 Pro Realtime at 6.99% WER on the open Pipecat voice-agent benchmark, ahead of Google Chirp3 at 9.04%, ElevenLabs Scribe v2 at 9.76%, and Deepgram Flux at 15.58%. Run it yourself before treating it as settled.

LiveKit also documents preemptive generation, which starts the LLM on a partial transcript. The caveat is real: if the reply has to be regenerated after the final transcript, you burn tokens and save nothing.

Layer 3: Text-to-Speech Time to First Audio

This is where vendor numbers diverge most sharply from what users experience.

ElevenLabs states Flash v2.5 delivers approximately 75ms. Its own docs qualify that carefully: 75ms refers to model inference time only. The company&#8217;s latency concepts page goes further, listing network round-trip at typically 20–200ms depending on geography, and noting that most audio players buffer before playback, with 500ms buffering being common. It also states that Eleven v3 is not built for real-time, and recommends Flash v2.5, Flash v2, or Multilingual v2 for its Agents Platform.

Cartesia states sub-90ms TTS and 100ms transcript latency for Sonic-3.6 and Ink-2. Marktechpost&#8217;s coverage of the Sonic-3.6 release flagged both as vendor-stated model latency, not measured end-to-end round trips. Cartesia previously claimed 82ms end-to-end time-to-first-audio for Sonic 3.5. Sonic runs on state space models rather than transformers, which scale linearly rather than quadratically with sequence length.

On quality, the Artificial Analysis Provider Voice arena is blind-listener Elo, retrieved August 30, 2026:

ModelEloPrice per 1M charsCartesia Sonic 3.61,288$49.00SpeechifyAI Simba 3.21,243$10.00Alibaba Qwen-Audio-3.0-TTS-Plus1,243$27.60Inworld Realtime TTS-2 Flash (preview)1,228$10.40BreezeBlue Breeze TTS 2 (open weights)1,220$34.00ElevenLabs v3 Conversational1,215$50.00Google Gemini 3.1 Flash TTS1,210$18.30ElevenLabs Flash v2.51,083$50.00

The gap between Sonic 3.6 at 1,288 and Flash v2.5 at 1,083 is the quality cost of the low-latency tier that most agents actually run on.

Layer 4: Speech-to-Speech Time to First Audio

Speech-to-speech models collapse STT, LLM, and TTS into one pass. Fewer round trips should mean lower latency.

LiveKit is careful here, noting that realtime models are not guaranteed to be faster in every case, and that a well-tuned pipeline can be highly competitive.

The data supports that caution. From the Artificial Analysis speech-to-speech leaderboard, TTFA measured on Big Bench Audio, retrieved August 30, 2026:

ModelTTFASpeech reasoningTask successS2S IndexDeepslate Opal0.44s85%——Gemini 2.5 Flash Native Audio Dialog0.63s69%——Grok Voice Think Fast 2.0 High0.70s97%94.7%79.0%Grok Voice Fast 1.00.78s93%——Qwen3.5 Omni Flash Realtime0.79s59%29.1%—OpenAI GPT-Realtime-1.50.81s81%85.1%70.3%OpenAI GPT Realtime Mini (Oct &#8217;25)0.81s64%79.6%56.8%OpenAI GPT-Realtime-2.1 Mini Minimal0.85s63%76.7%52.8%Google Gemini 3.1 Flash Live Minimal0.96s71%74.6%63.9%OpenAI GPT-Realtime-2.1 Minimal0.97s87%89.4%70.3%Amazon Nova 2.0 Sonic (Mar 2026)1.14s88%57.1%—OpenAI GPT-Realtime-2 (High)1.14s97%89.8%73.6%OpenAI GPT-Realtime-2.1 High1.21s96%91.5%73.9%Google Gemini 3.1 Flash Live High2.99s97%71.8%71.5%OpenAI GPT-Realtime-2.1 Mini High4.28s75%——

Grok Voice Think Fast 2.0 High is the standout on this board: 0.70s TTFA with 97% speech reasoning and 94.7% task success.

The reasoning-effort penalty is visible within single model families. Gemini 3.1 Flash Live moves from 0.96s to 2.99s between Minimal and High. OpenAI&#8217;s GPT-Realtime-2.1 moves from 0.97s to 1.21s, buying 2.1 percentage points of task success.

OpenAI shipped gpt-realtime-2.1 and gpt-realtime-2.1-mini in early July 2026, and stated that improved caching cut p95 latency by at least 25% across its Realtime voice models. Tail latency is what makes a phone agent feel broken, so that is a more useful claim than a median improvement would be.

The capability gap

Daily&#8217;s benchmark quantifies why most production agents still use cascaded pipelines. On its aiwf_medium_context test, GPT Realtime scored 86.7% against GPT-4.1 at 94.9%. Ultravox 0.7 was, in Daily&#8217;s assessment, the first speech-to-speech model to perform well on long multi-turn conversations, and it is open weights.

Artificial Analysis also benchmarks four vendor &#8220;default cascaded systems,&#8221; which is useful context for what the platforms actually ship: Deepgram Voice Agent (Nova-3 + GPT-4o Mini + Aura-2), ElevenLabs Agents (Scribe v2 Realtime + Gemini 2.5 Flash + Eleven Flash v2), Cartesia Line (Ink + Gemini 2.5 Flash + Sonic), and Inworld Realtime (Inworld STT 1 + Gemini 2.5 Flash + Inworld TTS 1.5 Mini).

Three of the four run Gemini 2.5 Flash. That is a revealing consensus.

Reference Budgets

Assembled from the verified component figures above. These are planning estimates, not measurements of a running system.

Aggressive cascaded pipeline, US-hosted, colocated:

StageBudgetTransport and media (WebRTC)50–150msSTT + end-of-turn (Flux at defaults)~260msLLM first chunk (sub-0.5s tier)230–500msSentence completion at 250+ tok/s~100msTTS first audio + network150–300msTotal~790ms–1.3s

That lands at or slightly above the 800ms target, which matches Kwindla&#8217;s framing that 800ms is tight but achievable.

Speech-to-speech, single model:

StageBudgetTransport and media50–150msModel TTFA (minimal reasoning tier)700ms–1.0sTotal~750ms–1.15s

Comparable, with less observability and, per Daily&#8217;s benchmark, a measurable capability gap on tool calling and instruction following.

What to Do With This

Pick the metric your architecture is bounded by. If a TTS model sits downstream, optimize TTFS, not TTFT. That means TTFT and tokens per second together.

Colocate before you optimize models. LiveKit rates agent-model colocation as very high impact, above model choice. If you use SIP, keep the trunk geographically close too.

Cap reasoning effort explicitly. It is the largest single lever in the tables above, and it is a configuration flag on most modern endpoints.

Budget for tool calls. Kwindla notes that any turn with a tool call roughly doubles LLM latency. LiveKit recommends limiting max_tool_steps, consolidating external API calls, and playing a thinking sound so silence is not the user&#8217;s only feedback.

Instrument before you tune. The LiveKit Agents SDK exposes e2e_latency, LLM time to first token, and TTS time to first byte per turn. Pipecat exposes the equivalent through enable_metrics and observers. Store the logs externally and watch for regression.

Measure p95, not just p50. OpenAI&#8217;s own main improvement in July 2026 was a tail-latency reduction, because that is where voice agents break.

Watch for infrastructure footguns. LiveKit documents that self-hosted agents on AWS burstable instance types such as t3 or t4g can hit severe latency and turn-detection timeouts even at apparently low CPU usage.

Key Takeaways

Fastest independently measured first chunk on a 10k-token workload: Baseten serving gpt-oss-120b at 0.23s, per Artificial Analysis.

Throughput and TTFT are different products: Cerebras hits 1,697 tok/s but 0.49s TTFT; Inception&#8217;s Mercury 2 hits 770 tok/s at 3.07s.

Vendor latency claims like ElevenLabs&#8217; 75ms and Cartesia&#8217;s sub-90ms are model inference time only, excluding network.

Reasoning effort is the single largest TTFT lever: Gemini 3.1 Flash Live goes 0.96s to 2.99s between Minimal and High.

TTFT alone does not predict how an agent feels. Time-to-first-sentence does, because speech synthesis needs a full clause.

Sources

Artificial Analysis: LLM API Providers Leaderboard

Artificial Analysis: Performance Benchmarking Methodology

Artificial Analysis: Speech to Speech Leaderboard

Artificial Analysis: Streaming Speech to Text Leaderboard

Artificial Analysis: Text to Speech Provider Voice Leaderboard

LiveKit: Understand and Improve Voice Agent Latency

LiveKit: Latency Optimized Inference, Gemma 4

LiveKit: Voice Agents

Daily: Benchmarking LLMs for Voice Agent Use Cases

Daily: Advice on Building Voice AI

Deepgram: Migrating from Nova-3 to Flux

Deepgram: Measuring STT Latency

AssemblyAI: Introducing Universal-Streaming

ElevenLabs: Understanding Latency

ElevenLabs: Latency Optimization

Cartesia: Sonic-3.6 and Ink-2

OpenAI: Realtime and Audio Guide

aiewf-eval benchmark source

The post Lowest-Latency Inference APIs for Voice and Realtime Agents: A Time to First Token TTFT-First Benchmark appeared first on MarkTechPost.