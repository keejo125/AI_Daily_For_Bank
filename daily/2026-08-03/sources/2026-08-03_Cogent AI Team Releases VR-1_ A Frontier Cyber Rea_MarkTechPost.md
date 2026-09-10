---
status: confirmed
category: 国际
is_model_related: true
digest: |
  Cogent AI发布VR-1，首个专为网络安全推理后训练的模型。配套IntrusionBench（基于执行完成的入侵评测基准）和Cogent AI Harness（带治理的安全Agent运行时）。
  
  VR-1针对四项关键行为后训练：部分信息下的调查、跨域证据组合、从死胡同恢复、验证真实目标。自主完成给定立足点和目标下的攻击链路，限2小时或250轮Agent回合。
  
  相比Kimi K3、Claude Opus 4.8和GLM-5.2，VR-1在黑盒测试中发现约两倍攻击路径且成本仅四分之一。但自身黑盒成功率仍低于30%。仅向受审核企业开放。Cogent引用OpenAI模型逃逸沙箱事件论证防守方需要同等级推理能力。
publish_time: 1785742094
---

# Cogent AI Team Releases VR-1: A Frontier Cyber Reasoning Model That Composes and Verifies Enterprise Attack Paths

> 原文链接：https://www.marktechpost.com/2026/08/03/ogent-ai-team-releases-vr-1/
> 来源：MarkTechPost

Cogent AI team released Cogent VR-1, a reasoning model post-trained specifically for cybersecurity rather than picking up cyber capability as a side effect of general coding strength. It ships with two companions: IntrusionBench, a benchmark that scores agents on completed enterprise intrusions, and the Cogent AI Harness, a governed runtime for security agents. The launch lands six days after OpenAI disclosed that its models escaped a sandboxed evaluation and compromised Hugging Face&#8217;s production infrastructure, an incident Cogent cites directly as the reason defenders need equivalent reasoning on their side.

Is VR-1 deployable

Not open-sourced or weight. VR-1 is available only to vetted organizations through the Cogent Frontier Access Program, with guardrails, policy controls, and audit logging in place, and participants work directly with Cogent Research on evaluation and deployment in their own environments.

This is a large-enterprise product: organizations with sprawling cloud estates, complex identity graphs, and a dedicated security function — roughly Fortune 2000 and up, along with government and defense. It is not an SMB purchase. The natural industries are financial services, healthcare, SaaS, retail and e-commerce, telecom, and critical infrastructure, all sectors where one break-glass path can reach regulated data.

What VR-1 is trained to do

Cogent&#8217;s research is explicit that identifying a weakness is not the same as completing an intrusion. Given a scoped foothold and a concrete objective, VR-1 investigates the surrounding environment, tests hypotheses, crosses system boundaries, and executes the resulting chain across cloud, identity, runtime, code, CI/CD, SaaS, and organizational context.

Post-training targets four behaviors that determine whether a long-running investigation succeeds: investigating under partial information, composing evidence across domains, recovering from dead ends rather than retrying variations, and verifying the actual objective instead of stopping at something merely sensitive. Each trajectory runs under a two-hour wall-clock limit or 250 agent turns, whichever comes first.

IntrusionBench grades execution, not narration

IntrusionBench places an agent inside a controlled environment with a foothold, a hidden multi-domain path, scoped tools, and an execution-based verifier. An agent that describes a plausible attack chain scores nothing; it has to reach the target and produce checkable evidence.

Cogent evaluates across three information settings. In black-box, the agent gets only the foothold and objective. In grey-box, partial environment detail is disclosed. In white-box, the source and underlying weakness are handed over outright, and the models largely converge — which is the most informative result in the release, because it suggests VR-1&#8217;s advantage comes from finding the path rather than from superior exploitation skill.

Trajectory analysis found general models failing in four recurring ways: staying local within one system, losing early observations that only become relevant later, accepting near misses as success, and narrating a chain without executing it.

Numbers

Cogent reports VR-1 proving roughly twice as many attack paths at about a quarter of the cost, measured as black-box pass@3 against Kimi K3, Claude Opus 4.8, and GLM-5.2.

On &#8216;Mythos-class&#8216;

Cogent uses Mythos-class to describe a capability threshold — the transition from identifying weaknesses to executing material attack paths — and states plainly that it does not claim general equivalence with Anthropic&#8217;s Mythos models. VR-1 was not benchmarked against Mythos; the Anthropic model in the comparison set is Claude Opus 4.8. Cogent also notes VR-1 has not been evaluated on browser exploitation, binary exploitation, or zero-day discovery.

&

Key Takeaways

VR-1 is the first frontier model post-trained specifically for enterprise attack-chain composition, not single-bug discovery.

The 2× claim is black-box pass@3 against baselines on their default harnesses; harness-matched, the gap nearly closes.

VR-1&#8217;s own black-box success rate is under 30%, and Cogent labels the figures preliminary.

&#8220;Mythos-class&#8221; is a scoped capability threshold — VR-1 was never benchmarked against Mythos.

Access is gated to vetted enterprises; the model-agnostic AI Harness is the broadly deployable piece.

Check out the Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Cogent AI Team Releases VR-1: A Frontier Cyber Reasoning Model That Composes and Verifies Enterprise Attack Paths appeared first on MarkTechPost.