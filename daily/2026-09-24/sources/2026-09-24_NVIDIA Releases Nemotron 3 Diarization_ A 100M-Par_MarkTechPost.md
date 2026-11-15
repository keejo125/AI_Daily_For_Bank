---
publish_time: 1790187434
link: https://www.marktechpost.com/2026/09/23/nvidia-releases-nemotron-3-diarization/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MarkTechPost 报道英伟达开源 Nemotron 3 Diarization，一个约 1 亿参数的开放权重模型，可实时区分多达 8 名说话人，适用于会议转写、客服质检等场景。文章强调其轻量、低延迟与可商用，是语音理解与多说话人处理的高效底座。
---

# 英伟达开源 Nemotron 3 Diarization：1 亿参数实时 8 说话人分离模型

> 原文链接：https://www.marktechpost.com/2026/09/23/nvidia-releases-nemotron-3-diarization/
> 来源：MarkTechPost

NVIDIA has released Nemotron 3 Diarization, an open-weight speaker diarization model on Hugging Face. It answers one question about any conversation: who spoke when. The 100M-parameter model tracks up to 8 speakers, including when voices overlap. One checkpoint handles both offline recordings and real-time streaming.

Is it deployable? Yes. The weights are released under the OpenMDW License 1.1, which permits commercial use. It runs on Linux through NVIDIA NeMo, using Ampere, Ada Lovelace, Hopper, or Blackwell GPUs.

Why Speaker Diarization?

Automatic speech recognition (ASR) gives you the words. It does not tell you who said them. Without attribution, a summarizer cannot tell who made a commitment or who raised an objection.

Diarization outputs the time intervals where each speaker is active. Those timestamps combine with ASR output to produce a speaker-attributed transcript. Meeting tools, call analytics, podcast pipelines, and voice-agent memory all depend on this step.

What Changed From Streaming Sortformer

NVIDIA&#8217;s earlier Streaming Sortformer checkpoint, diar_streaming_sortformer_4spk-v2.1, supported 4 speakers. Nemotron 3 Diarization doubles that limit to 8. According to NVIDIA&#8217;s announcement, the target is messy multi-party audio where people talk at once.

How the Architecture Works

The model accepts 16 kHz, single-channel audio in .wav, .flac, .opus, or .mp3 format. It converts the audio into Mel-spectrogram features with a 10 ms step. The features are stacked by a factor of 8, which produces 80 ms encoder frames.

A 31-layer Transformer encoder with rotary positional embeddings (RoPE) processes those frames. A Conv1D layer then upsamples the predictions back to 10 ms resolution. The output is a [T, 8] tensor of per-speaker activity probabilities.

This design handles overlap directly. If 2 people talk at the same time, 2 channels activate in the same frame.

The model follows the Sortformer approach of ordering speakers by arrival time. The first new voice takes channel 1, the next takes channel 2, and so on. This keeps labels stable across streaming chunks, so the model does not have to re-match speakers to channels for every chunk.

Streaming uses 2 memory mechanisms. The Arrival-Order Speaker Cache (AOSC) keeps speaker information from earlier chunks. A FIFO queue supplies recent frame context. The labels are anonymous, and mapping them to real identities is left to downstream applications.

4 Latency Operating Points

Input-buffer latency equals (chunk + right context) × 80 ms. The table uses DIHARD III full-set DER and batch-32 compiled throughput from the model card.

ConfigurationBuffer latencyDIHARD III DERRTFx (batch 32, compiled)Offline style30.4 s12.73%15,113×Low latency1.04 s13.18%865×Very low latency0.64 s13.28%579×Ultra-low latency0.32 s13.55%292×

This latency excludes compute, networking, and ASR time. The model can technically run with an 80 ms buffer, but 0.32 s is the lowest recommended setting.

Benchmark Results

In Voice Arena&#8217;s initial Diarization-Bench results, the model ranked first among 12 systems and 17 configurations. The test covered 139 English conversations totaling about 22 hours. It scored 14.72% DER against 19.3% for the next-ranked system, roughly a 24% relative reduction. NVIDIA notes these results may change once Voice Arena completes its Version 1 evaluation.

Against the 4-speaker baseline at 1.04 s latency, DER dropped on all 8 evaluation conditions. Relative reductions ranged from 9.0% on CALLHOME-Part2 to 65.2% on NOTSOFAR1 MHM. The unweighted mean across the 8 conditions was 41.0%.

There is one regression. On 2-speaker CALLHOME at 30.4 s, DER rose from 5.68% to 5.98%. Full-set CALLHOME-Part2 still improved from 10.32% to 9.10%.

Throughput also jumped. At 30.4 s, the model reached 15,113× RTFx versus 2,619× for the baseline. The tests used BF16 on an NVIDIA RTX PRO 5000 with torch.compile(). These are batched numbers, not single-stream application latency.

Training Data

Training combined about 10,000 hours of real conversations with 82,611 hours of simulated multi-talker mixtures. The mix included real-world multi-speaker audio licensed from David AI. Adding the David AI data cut compound DER from 11.19% to 10.42%. The licensed source audio for the simulated mixtures spans 21 languages.

Getting Started

Install NVIDIA NeMo Speech with Python 3.12 or later:

Copy CodeCopiedUse a different Browser

uv pip install 'nemo-toolkit[asr]'

Copy CodeCopiedUse a different Browser

from nemo.collections.asr.models import SortformerEncLabelModel
diar_model = SortformerEncLabelModel.from_pretrained("nvidia/Nemotron-3-Diarization")
diar_model.eval()
segments = diar_model.diarize(audio=["conversation.wav"], batch_size=1)

Output segments take the form start end speaker_id. To get the words as well, pair the model with Parakeet TDT 0.6B v3 using the ASR integration guide.

The live demo Space offers synthetic conversations, a live mic, a multilingual live mic, and audio upload. For production, NVIDIA lists Baseten and DigitalOcean. On-device support is available through Argmax Pro SDK 3. The model is not yet available through Hugging Face Inference Providers.

The model has limits. Recordings with more than 8 speakers can produce missed or misassigned speech. Heavy noise, reverberation, and far-field capture can also raise error rates.

Interactive Explainer

&&

Key Takeaways

100M-parameter open-weight model tracks up to 8 overlapping speakers.

One checkpoint covers everything from offline (30.4 s) to ultra-low 0.32 s streaming.

Ranked #1 on Voice Arena&#8217;s initial Diarization-Bench at 14.72% DER.

Averages a 41.0% relative DER reduction versus Streaming Sortformer at 1.04 s.

The OpenMDW-1.1 license permits commercial use; the model runs on NVIDIA GPUs through NeMo.

Check out the Model Weights, Technical Blog, and Demo. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Releases Nemotron 3 Diarization: A 100M-Parameter Open-Weight Model That Tracks 8 Speakers in Real Time appeared first on MarkTechPost.