---
publish_time: 1790145198
link: https://www.marktechpost.com/2026/09/22/kyutai-releases-voice-of-reason-a-speech-native-model-that-solves-spoken-math-with-reinforcement-learning/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  法国 AI 实验室 Kyutai 发布 Voice of Reason，两款开放权重的语音到语音模型可“出声”解题。两者均从 GLM-4-Voice-9B 出发，经 SFT 与强化学习训练，无需转录步骤、循环中也无独立文本 LLM。在口语 GSM8K 上准确率从基座的 27.3% 提升至 77.1%，可单张 H100 自托管。
---

# Kyutai 发布 Voice of Reason：语音原生数学推理模型

> 原文链接：https://www.marktechpost.com/2026/09/22/kyutai-releases-voice-of-reason-a-speech-native-model-that-solves-spoken-math-with-reinforcement-learning/
> 来源：MarkTechPost

Kyutai has released Voice of Reason, 2 open-weight speech-to-speech models that solve math problems out loud. Both start from GLM-4-Voice-9B and add supervised fine-tuning (SFT) and reinforcement learning (RL). There is no transcription step and no separate text LLM in the loop. On spoken GSM8K, accuracy climbs from 27.3% for the base model to 77.1%.

Is it deployable? Yes, for self-hosting. Kyutai ran both BF16 checkpoints on a single H100. You also need the GLM-4-Voice repo for its speech tokenizer and decoder. Weights inherit the GLM-4-Voice license, and no Hugging Face inference provider hosts them yet.

Why Speech Models Lag on Math

Cascaded pipelines (speech-to-text, text LLM, text-to-speech) still lead on reasoning. However, each stage adds latency, and the pipeline loses paralinguistic cues like tone. Speech-native models must emit audio at regular intervals to stay interactive. That limits how many hidden reasoning tokens they can afford.

Base GLM-4-Voice scores 27.3% on GSM8K. The earlier STITCH method raised that to 58.7% by adding reasoning chunks. The research team call their work the first application of RL to math reasoning in speech-native models.

How the Training Works

GLM-4-Voice interleaves its output: 13 text tokens, then 26 audio tokens, repeating.

Stage-1 SFT: Training uses 150,616 problems from Orca-Math. Qwen3-235B rewrote each problem for speech. Kyutai&#8217;s DSM TTS then voiced them in many voices. SFT alone lifts GLM-4-Voice from 27.3% to 61.7%.

Stage-2 RL: For each spoken question, the model samples 4 replies at temperature 0.9. A judge, Qwen3-235B-A22B-2507, scores the decoded text with a binary reward. The judge never sees the reference answer. On 100 hand-checked cases, it agreed with humans 88% of the time.

Rewards are centered within each group, forming a group-relative REINFORCE objective. It is related to GRPO but drops PPO clipping and KL regularization. Training ran on 16 H100 GPUs, with 1,500 RL updates.

2 design choices matter most:

Temperature correction: Logits are divided by the sampling temperature before the log-softmax in the loss. Without it, GSM8K collapsed from 65.5% to 12.3%.

Audio-token merging: At each audio position, all audio-vocabulary probabilities are summed into 1 abstract token. The loss asks only whether audio came next, not which audio token. The paper proves this estimator is unbiased and lower-variance under a value-invariance assumption.

Interactive Explainer

&&&

The 2 Released Checkpoints

glm-4-voice-of-reason-9b answers directly, with no extra reasoning tokens. Any step-by-step working is spoken aloud.

glm-4-voice-of-reason-stitch-9b writes silent 100-token reasoning chunks between spoken blocks. Kyutai says later chunks are generated while earlier speech plays, so thinking adds no extra latency. In the STITCH-R layout used here, the first reasoning chunk precedes the first spoken block.

Results

ModelParamsGSM8K (%)PersonaPlex (full-duplex)8B3.2GLM-4-Voice9B27.3STITCH (Chiang et al.)9B58.7Voice of Reason9B65.5 ± 1.1 (70.3 released)Voice of Reason (Stitch)9B74.8 ± 1.1 (77.1 released)Qwen2.5-Omni (text output)7B84.7Qwen3-Omni (text output)30B94.6Cascaded ASR-LLM-TTS-ASR31B LLM95.7

Paper scores use top-k 50 decoding, averaged over 3 seeds. Removing top-k gives 70.3% and 77.1%. The released checkpoints correspond to these runs. The omni and cascaded systems are larger top lines, not matched comparisons.

Other findings:

Gains survive in real speech: Transcribed with Qwen3-ASR-1.7B, the Stitch model scores 72.0 ± 1.9%.

Naturalness holds: UTMOSv2 moved from 4.067 to 4.069 (direct) and 4.174 to 4.164 (Stitch) after RL.

Gains do not come from longer answers: RL cut the direct model&#8217;s average reply from 41.9 to 36.4 seconds. Stitch reasoning tokens rose only from 167 to 176.

RL helps most with little data: With 10% of SFT data, a longer RL run reached 58.5%. SFT alone scored 43.9%.

General knowledge dips: Spoken TriviaQA fell from 40.6% to 34.0% for the direct model. The authors attribute this mainly to full-data SFT, not RL.

Contamination check: The team dropped AddSub, MultiArith, SingleEQ and SVAMP from evaluation. Of 678 checked questions, 54.0% overlapped with Orca-Math at the paraphrase level.

Evaluation audio came from GPT-4o-mini-TTS, a different TTS system than the training audio. GPT-4o served as the evaluation judge.

Key Takeaways

Kyutai&#8217;s RL recipe lifts GLM-4-Voice from 27.3% to 77.1% on spoken GSM8K.

The direct model reaches 70.3% without reasoning tokens, beating STITCH&#8217;s 58.7%.

Temperature correction is critical: removing it crashed accuracy to 12.3%.

Speech naturalness holds after RL; TriviaQA drops, mostly from SFT.

Both 9B checkpoints are open on Hugging Face and run on 1 H100.

Check out the Paper, the direct model and the Stitch model. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Kyutai Releases Voice of Reason: A Speech-Native Model that Solves Spoken Math with Reinforcement Learning appeared first on MarkTechPost.