---
publish_time: 1785651686
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA NeMo团队发布Molt，一个PyTorch原生的Agent强化学习框架。其核心设计目标极为独特：代码库仅约8600行（对比verl的6.2万行、slime的2.5万行），精简到研究者可将整个框架装进大脑、AI编程助手能完整阅读和理解。Molt由Ray负责资源调度、vLLM负责rollout、NVIDIA AutoModel+FSDP2负责训练，三个组件均未fork上游，可直接获取最新改进。默认配置需2节点×8 H100 GPU（8训练+8rollout），适用于多轮工具调用Agent、代码执行Agent、视觉语言环境和LLM-as-judge奖励循环等场景。采用Apache 2.0开源协议。
---


# NVIDIA AI Releases Molt: A PyTorch-Native Agentic Reinforcement Learning Framework

> 原文链接：https://www.marktechpost.com/2026/08/01/nvidia-ai-releases-molt-a-pytorch-native-agentic-reinforcement-learning-framework/
> 来源：MarkTechPost

Agentic reinforcement learning research is constant algorithm modification. New estimators, new pipeline stages, new rollout schemes. In mainstream frameworks each change threads through layers of trainer, distributed backend, and rollout glue. That cost lands on the researcher at every iteration.

Molt, from NVIDIA&#8217;s NeMo team, targets that cost directly. Its a PyTorch-native agentic RL framework with an unusual design target. The codebase should be compact enough for a researcher to hold in their head, and for an AI coding assistant to read and reason about in its entirety. The stated footprint is roughly 8.6K lines of RL code, measured by tracing the import graph from each framework&#8217;s RL entry point. The same method counts about 62K lines for verl, 25K for slime, and 7.2K for OpenRLHF.

Is it deployable?

Yes. Molt ships under Apache 2.0 with launch codes, Slurm scripts, and a prebuilt container. But the research paper positions it as research infrastructure, not a production training service, and hardware is the real gate. The shipped recipes assume 2 nodes of 8 H100 GPUs, split 8 for training and 8 for rollout.

That puts Molt in reach of frontier and frontier-adjacent labs, well-funded AI startups doing post-training, enterprise AI research groups in finance, healthcare, and robotics that train agents against proprietary environments, and academic labs with multi-node H100/H200 access. Applications include multi-turn tool-use agents, code-execution agents, vision-language environments (the shipped geo3k recipe), LLM-as-judge reward loops, and on-policy distillation onto a smaller student.

Three components, one loop

Molt composes Ray for placement and asynchronous queues, vLLM for rollout, and NVIDIA AutoModel with FSDP2 for training. None of the three is forked, so upstream improvements arrive as a container pin rather than a rebase.

The runtime is an agent pool, a set of vLLM engines behind a request router, and a single trainable policy actor. A streaming pool keeps prompt groups in flight so engines never drain while the actor trains. Partial rollout pauses the engines, broadcasts actor shards over NCCL directly to each engine, and resumes retained requests instead of discarding them.

The agent is an ordinary program

An RL run names one Python module that exports an AgentRunner. Everything else is ordinary code, including the reward.

Two forms are supported. With Env, the framework owns the LLM loop in a Gymnasium-aligned step(). With ChatAgent, the user owns the loop through a stock OpenAI or Anthropic SDK. Molt launches a loopback server that speaks both wire protocols, and every request decodes server-side into one token-exact accumulation. When a long-horizon agent compacts its context and rewrites the prefix, the server seals the current segment and opens a fresh one automatically.

Never train on a token you did not generate

Three correctness invariants organize the design. Token identity: sampled token ids define the trajectory, not a retokenized transcript. Policy-version semantics: trainable tokens keep their behavior-policy log-probabilities, and asynchronous use is corrected per token behind a sequence-level gate. Forward consistency: rollout and actor must agree on model semantics.

For mixture-of-experts policies, the last invariant matters most. The rollout and training routers select experts independently, and small numerical differences can flip top-k choices. Molt applies rollout routing replay, where vLLM returns its per-token expert ids and the training forward replays them.

Interactive explainer

Key Takeaways

Molt is an Apache-2.0 agentic RL framework in about 8.6K lines of RL code, roughly 7× smaller than verl.

Ray, vLLM, and NVIDIA AutoModel are composed, never forked, so upstream releases arrive as a container pin.

Agents are plain Python; a stock OpenAI or Anthropic SDK trains as-is through a token-exact loopback server.

Throughput is statistically comparable to a Megatron-based stack, with the MoE-mismatch caveat disclosed.

Scale is a flag: the same loop runs a dense 4B model and a 700B MoE at --fsdp.ep_size 256.

Check out the Paper and Repo here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA AI Releases Molt: A PyTorch-Native Agentic Reinforcement Learning Framework appeared first on MarkTechPost.