---
publish_time: 1792899179
link: https://www.marktechpost.com/2026/10/24/microsoft-agensh-multi-agent-harness-1024-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  微软研究院开源 Agensh，一个面向大规模编码智能体团队的去中心化 harness，移除了多数框架依赖的中央编排器：每个 worker 自行领取子任务、共享发现并合并代码到公共 Git 仓库。在 ProgramBench 上，团队将规模从 1 个智能体扩展到 1024 个；每个 worker 拥有 27.2 万 token 输入、12.8 万 token 输出上限与 64 GiB 内存上限，1024 智能体运行用 16 节点、每节点 64 个。论文以 Claude Code agent teams、Codex 子智能体、Copilot fleet、Kimi Agent Swarm 为例指出编排器瓶颈，让 worker 自行协调。实测更多智能体提升全部 5 个最难任务得分并更快达成；32 智能体在 GPT-6.1-sol 上 pandoc 通过率 79.59%，1024 智能体在 GPT-5.6-sol 上 55.06%。
---

# 微软开源 Agensh：支撑千级智能体的去中心化多智能体框架

> 原文链接：https://www.marktechpost.com/2026/10/24/microsoft-agensh-multi-agent-harness-1024-agents/
> 来源：MarkTechPost

Microsoft Research has open-sourced Agensh, a decentralized harness for large teams of coding agents. The Agensh multi-agent harness removes the central orchestrator that most agent frameworks depend on. Every worker picks its own sub-task, shares findings and merges code into a common Git repo. On ProgramBench, the team scaled the setup from 1 agent to 1,024 agents. 

TL;DR

A Harness: Tested from 1 to 1,024 agents. Each worker gets a 272,000-token input and 128,000-token output limit.

Runs on: Linux with Docker Compose. Single node by default (8 workers). The 1,024-agent run used 16 nodes, 64 agents each. Workers have a 64 GiB memory ceiling.

Performance: more agents raised scores on all 5 hardest ProgramBench tasks, and reached them sooner.

Best: 79.59% pandoc pass rate with 32 agents on GPT-6.1-sol. GPT-5.6-sol hit 55.06% with 1,024 agents.

Worst: the 5-task mean reached only 28.78% at 128 agents. Going from 1 to 8 agents added 1.37 points.

What is Agensh?

Agensh is a multi-agent harness from Microsoft Research that coordinates many LLM agents without a lead agent. 

The target problem is the orchestrator ceiling. In orchestrator-worker designs, a lead agent plans, assigns and merges all work. The research paper cites Claude Code agent teams, Codex sub-agents, Copilot fleet and Kimi Agent Swarm as examples. Agensh lets the workers do that coordination themselves.

How does the Agensh cooperation loop work?

Each worker runs the same 5-step loop, concurrently and asynchronously:

Gather context: read the goal, peer progress, messages and findings.

Claim a sub-task: post a CLAIM, then settle overlaps by direct message.

Take action: work locally with tools and post useful findings early.

Verify results: check the work against the sub-task&#8217;s acceptance criteria.

Merge progress: merge into the shared repo, post an update, then repeat.

Three services connect the workers. Gitea hosts the shared workspace, with branches, PRs and merge conflicts. Mattermost carries a team channel plus direct messages for urgent collisions. A shared context board, adapted from DeLM, stores typed notes: OBSERVED, FACT, FAIL, CLAIM and PATCH_SUMMARY.

The loop lives in the prompt, not in runtime code. Every worker gets the same prompt except its ID. Agensh sits on top of a single-agent harness. The experiments used GitHub Copilot CLI. The research paper states thin adapters can connect other harnesses, such as Claude Code.

&&&

How well does Agensh scale on ProgramBench?

Microsoft team tested the 5 hardest ProgramBench tasks: FFmpeg, gromacs, pandoc, PHP-src and ctags. Agents rebuild each program from its observed behavior. They work offline, within 6 hours. Reference repos range from 2,767 files (pandoc) to 26,266 files (PHP-src).

With GPT-5.6-sol at high reasoning effort, the mean final test-pass rate moved as follows:

1 agent: 19.31%

8 agents: 20.68%

32 agents: 26.52%

128 agents: 28.78%

That is a 9.47-point gain, about 49% relative. On pandoc alone, scores were 33.89% (1), 41.75% (8), 43.11% (32), 50.94% (128) and 55.06% (1,024).

Speed improved too: on pandoc, 128 agents passed 30% at the 30-minute checkpoint. 32 and 8 agents needed 60 and 90 minutes.

The README adds a newer model. With GPT-6.1-sol, pandoc rose from 56.19% (1 agent) to 79.59% (32 agents). That is a 41.64% relative gain. These GPT-6.1-sol figures are not in the v1 paper.

What behaviors emerged as the team grew?

The research team traced worker trajectories at each scale:

8 agents: peers agreed on interfaces and resolved overlapping claims themselves.

32 agents: peers reviewed shared work; one approval was withdrawn after a counterexample.

128 agents: workers reused trusted reviewers and standardized an integration protocol.

1,024 agents: several workers acted as integrators, and peers recovered failed work.

None of these roles was hard-coded.

How does Agensh compare with other multi-agent harnesses?

FeatureAgenshClaude Code agent teamsKimi Agent SwarmCopilot CLI /fleetCoordinationNo orchestrator; peers self-claim workFixed lead session coordinates teammatesOrchestrator decomposes tasksCopilot assigns parts to subagentsAgents shown1,024 testedNo hard limit; 3 to 5 recommendedUp to 100 sub-agentsNot disclosedShared stateGitea repo + shared context boardShared task list with file lockingNot disclosedPlan from plan modeMessagingMattermost channel + direct messagesMailbox messages between teammatesNot disclosedNot disclosedModelsModel agnostic; tested GPT-5.6-sol, GPT-6.1-solClaude modelsKimi K2.5Not disclosedSpeed claim30% on pandoc at 30 min (128 agents)Not disclosed4.5x faster than sequential (self-reported)Not disclosedAvailabilityOpen source, MITIn Claude Code; experimental, off by defaultTop-tier subscribers, research previewIn Copilot CLI

How do you run Agensh?

The release includes a single-node Docker Compose team and a single-agent baseline. Both use native Copilot ACP sessions. You need Linux with Docker Engine, Compose v2, systemd, cgroup v2 and Python 3.11+. Defaults are 8 workers, 6 hours per task and gpt-5.6-sol at high effort. You also need ProgramBench (v1.2.5 was validated) and a model API token. Full steps sit in the reproduction guide.

Key Takeaways

Agensh coordinates up to 1,024 agents with no central orchestrator.

Workers self-claim tasks via Gitea, Mattermost and a shared findings board.

128 agents lifted the 5-task ProgramBench mean from 19.31% to 28.78%.

GPT-6.1-sol with 32 agents hit 79.59% on pandoc.

Code is MIT licensed, but token cost is not disclosed.

Check out the Paper, GitHub Repo and Project Page. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Microsoft Open-Sources Agensh: A Multi-Agent Harness for 1,024 Agents appeared first on MarkTechPost.