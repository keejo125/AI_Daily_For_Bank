---
publish_time: 1786319914
link: https://www.marktechpost.com/2026/08/09/nvidia-releases-nemotronlabs-voicechat-11b-an-open-full-duplex-speech-to-speech-model-with-450-ms-turn-taking-and-live-tool-calling/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  英伟达发布NemotronLabs VoiceChat 11B，一个开源的端到端语音到语音模型，采用混合Mamba/Transformer架构实现全双工实时对话。模型将ASR、LLM和TTS统一为单一网络，端到端延迟约448毫秒，支持用户打断（480毫秒内接管率达100%）。独特之处在于支持边对话边工具调用，通过独立输出通道发送TOOLCALL脚本，并自动生成占位语填充API执行间隙。目前仅提供研究用途，需要80GB以上显存GPU（A100/H100），存在2分钟音频上下文上限和长对话后产生乱码等已知限制。
---
# NVIDIA Releases NemotronLabs VoiceChat 11B: An Open Full-Duplex Speech-to-Speech Model with ~450 ms Turn-Taking and Live Tool Calling

> 原文链接：https://www.marktechpost.com/2026/08/09/nvidia-releases-nemotronlabs-voicechat-11b-an-open-full-duplex-speech-to-speech-model-with-450-ms-turn-taking-and-live-tool-calling/
> 来源：MarkTechPost

NVIDIA has released NemotronLabs VoiceChat 11B, an open 11B end-to-end speech-to-speech model for real-time, full-duplex conversation. Instead of chaining ASR, an LLM, and TTS, it performs streaming speech understanding and speech generation in one unified network. That removes the multi-model orchestration and API handoffs a cascaded stack requires, and cuts end-to-end latency: measured smooth turn-taking latency is 448 ms on Full-Duplex-Bench 1.0. The model listens while it speaks, so a user can barge in mid-turn and the agent yields, with a take-over rate of 1.00 at 480 ms. It is also first open full-duplex model to support tool calling while conversation keeps flowing, using a separate output channel for <TOOLCALL> scripts along with operator-defined &#8220;on-hold&#8221; lines that fill the gap while an API runs. 

Is it deployable?

PARTIAL — deployable today for pilots, not for production. Weights and container are both public, and the license is permissive. But NVIDIA team states the checkpoint is &#8216;ready for research purposes only,&#8217; and the repo documents real failure modes: a two-minute audio context ceiling, degradation into non-recoverable gibberish after several turns, runaway self-talk after a turn ends, and dropped words in user transcription. 

Which companies: any team that can allocate one GPU with at least 80 GB of VRAM — A100, H100, RTX 6000 Pro, or B200 on x86_64 Linux. That covers AI-native startups, funded scaleups, enterprise R&D and innovation labs, GPU cloud providers, and university speech groups. There is no hosted API and no inference provider currently serves the model, so teams without GPU access may not evaluate it.

Industries: contact centers and CX platforms, automotive in-cabin assistants, retail and drive-thru ordering, telecom IVR modernization, games and NPC dialogue, and accessibility tooling.

Applications: barge-in-capable voice agents, voice front-ends over internal APIs, live-lookup assistants (weather, pricing, order status), and duplex latency benchmarking harnesses.

Architecture

The model is a hybrid Mamba/Transformer, assembled from three existing NVIDIA components along with one new output path:

A Fast Conformer speech encoder from Nemotron-Speech-Streaming-En-0.6b, which encodes the incoming 16 kHz stream continuously.

The NVIDIA Nemotron Nano v2 LLM backbone, which consumes audio tokens and predicts text tokens.

An NVIDIA TTS decoder and codec that predicts audio codes, rendered as 22.05 kHz agent speech.

A separate output channel dedicated to tool-calling scripts.

Outputs include agent audio, agent text, and a running user transcription. Training used roughly 550k hours of audio across real and synthetic corpora, building on SALM-Duplex and Audio Flamingo 3.

Tool calling without dead air

Tool calls are emitted on the side channel as a <TOOLCALL> block; your code returns results in a <TOOL_RESPONSE> block. The notable piece is the on-hold message: per tool, an operator defines a line the agent speaks the moment the model generates the text triggering the call, so the conversation does not fall silent while an API runs.

Constraints are explicit. NVIDIA recommends a maximum of five tools per session, the model cannot reliably call multiple tools simultaneously, and the user cannot interrupt the agent during tool execution. System prompts and tool responses must be ASCII-only and TTS-friendly.

Performance

On Full-Duplex-Bench 1.0: smooth turn-taking TOR 0.82 at 448 ms, user-interruption TOR 1.00 at 480 ms, and pause-handling TOR of 0.153 (synthetic) and 0.255 (Candor), where lower is better.

On AU Harness BFCL-v3 spoken tool calling: 58.5% simple, 62.5% multiple, 42.5% parallel, 27.5% parallel-multiple, 89.6% irrelevance, 56.1% average. On Full-Duplex-Bench v3: 82.5% tool selection, 44.2% argument accuracy, 33% pass@1.

NVIDIA reports the model ranks #2 among open full-duplex models on VoiceBench and #2 among open models on Full-Duplex-Bench 1.0.

Interactive explainer

&&&

Key Takeaways

One 11B model replaces the ASR → LLM → TTS chain, at 448 ms measured turn-taking latency.

First open full-duplex model with tool calling, using a side channel plus operator-defined on-hold messages.

Weights are OpenMDW-1.1 permissive, but NVIDIA labels the checkpoint research-only.

Requires one 80 GB GPU; no hosted API exists today.

Check out the Hugging Face model card, GitHub (NeMo Speech) and NGC container. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Releases NemotronLabs VoiceChat 11B: An Open Full-Duplex Speech-to-Speech Model with ~450 ms Turn-Taking and Live Tool Calling appeared first on MarkTechPost.