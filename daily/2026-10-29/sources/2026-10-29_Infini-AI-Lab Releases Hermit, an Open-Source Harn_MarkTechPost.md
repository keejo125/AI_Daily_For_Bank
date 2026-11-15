---
publish_time: 1793262292
link: https://www.marktechpost.com/2026/10/29/infini-ai-lab-hermit-harness-adapter-framework/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Infini-AI-Lab（CMU博士后Haizhong Zheng宣布）开源harness适配器框架Hermit v0.1.0（Apache-2.0），在不微调、不fork底层harness的前提下，训练一个可插拔的外部“harness适配器”来适配Codex或Claude Code至新任务。适配器可承载指令、技能、记忆、工具与协调逻辑。在GLM 5.3 Flash上，MWM适配器于CL-Bench达0.795（基线0.580）。
---

# Infini-AI-Lab 开源 Hermit：可插拔的智能体 harness 适配器框架

> 原文链接：https://www.marktechpost.com/2026/10/29/infini-ai-lab-hermit-harness-adapter-framework/
> 来源：MarkTechPost

Infini-AI-Lab has released Hermit, an open-source harness adapter framework for AI agents. Hermit is a framework from Infini-AI-Lab that trains an external &#8216;harness adapter&#8217; while the agent&#8217;s model and harness stay frozen. The first release, v0.1.0, shipped on October 25, 2026. CMU postdoc Haizhong Zheng announced it on X on October 27. For developers, the pitch is simple: adapt Codex or Claude Code agents to new tasks without fine-tuning or forking the harness.

TL;DR

Footprint: A Python framework. No parameters of its own. Apache-2.0, pip install hermit-harness.

Runs on: The offline Quick Start needs no GPU, model account or dataset. Real runs use any API backend or a local vLLM, SGLang or Ollama server.

Performance: Reported gains over no-adapter baselines on OfficeQA, CL-Bench and ServeLearnBench, all with GLM 5.3 Flash.

Best: MWM adapter hits 0.795 accuracy on CL-Bench database exploration, vs 0.580 for the in-context baseline.

Worst: The prompt-only adapter scores 0.470 on the same venue, below that 0.580 baseline.

Bottom line: Best: one training loop for 5 harness evolution methods. Worst: most results are single runs, self-reported.

What is a harness adapter?

A harness adapter is a trainable external harness. It works like a plugin with training support built in. A model adapter, such as LoRA, adapts a model. A harness adapter adapts an existing agent instead.

The adapter can hold instructions, skills, memory, tools, executable code and agent coordination logic. It can even be a whole repository. Its specification says which parts are learnable and how updates get checked. The base model and harness never change.

The team gives 3 reasons for this design. Many harnesses are closed-source. Editing open ones can break carefully tuned component interactions. And a learned adapter can move between compatible models and harnesses.

How does Hermit train an adapter?

Hermit uses an RL-style training loop. A Trainer runs a batch of tasks through the acting agent with the current adapter. A judge scores the outputs. An Evolver reads the trajectories and feedback, then proposes a new adapter. The Trainer checks it against the template and commits it as the next version.

Every adapter version lives in a git tree. You can inspect, roll back or ship any version. Learner programs can run sandboxed, which requires Linux with bubblewrap.

Five evolution methods ship today: GEPA, SkillOpt, MetaWorld Model (MWM), Harness² and Continual Harness. ACE and ReHarness are listed as coming soon. You can also write your own Evolver.

What are the benchmark results?

All runs below use GLM 5.3 Flash as the acting model. The numbers come from the repo&#8217;s example READMEs and are self-reported.

OfficeQA (recipe) asks 172 test questions about U.S. Treasury Bulletins, scored by exact match:

MethodAccuracyNo adapter0.541Initial skill0.576GEPA0.580SkillOpt0.600Continual Harness0.634Harness²0.651

GEPA and SkillOpt train on 50 questions and are tested frozen. Continual Harness and Harness² instead learn while streaming the test set once. The team reports a +7.6 point gain for Harness² over its reference run, with a 95% interval of +1.7 to +13.4.

CL-Bench (database, poker) tests stateful environments from the Continual Learning Bench paper. On database exploration, MWM reaches 0.795 accuracy. The benchmark&#8217;s in-context baseline scores 0.580. On exploitable poker, MWM wins 3.08 big blinds per hand, vs 2.51 for in-context learning.

ServeLearnBench (recipe) streams 624 retail support requests under a hidden, shifting policy. MWM scores 45.3 on hidden-policy tests. The best learning method on the leaderboard, CH, scores 28.7. An oracle given the policy scores 89.2.

How does Hermit compare with other agent optimizers?

FeatureHermitGEPAACEAgent LightningWhat it trainsExternal harness adapterAny text parameter (prompts, code)Context playbookPrompts and model weightsChanges model weightsNoNoNot disclosedYes, via RL or SFTMethods5 built in, custom EvolversReflective evolution, Pareto selectionGenerator, Reflector, CuratorRL, prompt optimization, SFTDeploy targetsCodex, Claude Code, Pi; plugin exportDSPy (dspy.GEPA)Not disclosedLangChain, OpenAI Agents SDK, AutoGen, CrewAI and moreLicenseApache-2.0MITApache-2.0MITKey result0.795 on CL-Bench database (self-reported)AIME 2025: 46.6% to 56.6% (GPT-4.1 Mini)+10.6% on AppWorldNot disclosed

How do you install and deploy it?

Install from PyPI with pip install hermit-harness, or clone the repo for examples. The CLI covers check, train, eval, deploy and convert. Models are referenced as <backend>/<model id>. Supported backends include Fireworks, OpenAI, Anthropic, DeepSeek, vLLM, SGLang and Ollama.

hermit deploy writes a workspace for Codex, Claude Code or Pi. hermit convert exports a trained adapter as a native plugin for Codex, Claude Code, Pi or Hermes. A finished Lean collaboration adapter coordinates 5 Codex agents proving one theorem together.

Key Takeaways

Hermit trains an external adapter; model and harness stay frozen.

5 methods ship: GEPA, SkillOpt, MWM, Harness², Continual Harness.

MWM reaches 0.795 on CL-Bench database vs 0.580 in-context.

Adapters deploy to Codex, Claude Code and Pi, or export as plugins.

Results are self-reported, mostly single runs, with GLM 5.3 Flash.

Check out the GitHub repo, project page and docs. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Infini-AI-Lab Releases Hermit, an Open-Source Harness Adapter Framework for AI Agents appeared first on MarkTechPost.