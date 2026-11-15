---
publish_time: 1791669738
link: https://www.marktechpost.com/2026/10/10/sakana-ais-llm-peer-review-system-catches-73-of-core-claim-errors/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Sakana AI在TMLR发表《Beyond Imitation》，提出以“错误检测”为核心的LLM辅助同行评审。大多数AI评审以模仿人类评审为评判标准，该工作转问更难的“AI能否发现植入的错误”。团队发布两部分：矛盾基准（在5个会议257篇论文中植入1164处矛盾）与多层评审系统（MLR）。MLR由3个基于Claude Sonnet 4 / Haiku 3.5的Agent组成（附录Agent、文献综述Agent、主评审Agent），最多读10页正文，单篇成本约0.47美元。实测以4次评审捕获73.43%的核心论断错误，远超最佳基线14.81%，但对真实撤稿论文的精确匹配仅16.11%，且仍会落入隐藏提示注入。
---

# Sakana AI 推出 LLM 同行评审系统，捕获 73% 核心论断错误

> 原文链接：https://www.marktechpost.com/2026/10/10/sakana-ais-llm-peer-review-system-catches-73-of-core-claim-errors/
> 来源：MarkTechPost

Sakana AI has published Beyond Imitation, a TMLR research paper on LLM-assisted peer review built around error detection. Most AI reviewers are graded on how closely they copy human reviews. This work asks a harder question: can an AI reviewer find a planted mistake? The research team ships two pieces: a Contradiction Benchmark and a Multi-Layered Review (MLR) system. For developers building research agents, the lesson is practical. Both system design and model choice move error detection.

TL;DR

Size: 1,164 inserted contradictions across 257 papers from 5 venues. MLR reads up to 10 pages of main text.

Runs on: Off-the-shelf API models (Claude Sonnet 4, Claude Haiku 3.5). No GPU, no fine-tuning. About $0.47 per review.

Performance: Highest error detection of all 4 systems tested, with human-aligned scores.

Best: Caught 73.43% of core-claim errors with 4 reviews, versus 14.81% for the best baseline.

Worst: Only 16.11% exact matches on real retracted arXiv papers.

Bottom line: 

Best: reads before judging, and finds far more serious errors. 

Worst: still falls for hidden prompt injection.

What is Multi-Layered Review?

Multi-Layered Review is an agentic AI review system from Sakana AI that understands a research paper before critiquing it. It uses 3 agents on off-the-shelf Claude models:

Appendix Agent (Claude Haiku 3.5): summarizes experiments and implementation details from the appendix.

Literature Review Agent (Claude Sonnet 4): uses web search to place the paper in prior work. It is optional.

Review Agent (Claude Sonnet 4): runs a 3-pass prompt chain inspired by Keshav&#8217;s Three-Pass Approach.

Pass 1 writes a high-level outline. Pass 2 reads in detail and flags weaknesses, assumptions and gaps. Pass 3 merges all agent outputs into Strengths, Weaknesses, Questions, Recommendation, Score and a To-Do list. The PDF is passed directly, so figures and equations survive.

How does the Contradiction Benchmark work?

The benchmark plants errors into real papers and checks whether reviewers catch them. The research team collected 257 CC-licensed papers from ACL, AISTATS, CVPR and ICML 2025, plus NeurIPS 2024.

Gemini 2.5 Pro builds a knowledge graph of each paper&#8217;s claims, evidence and methods. Node distance from a &#8220;main claim&#8221; sets severity. Distance 0 hits a core claim; larger distances hit details. GPT-4.1 then rewrites 1 node per distance into a contradiction, yielding 1,164 data points.

An o3 judge scores each review 10 times. On clean papers it reached 99.9% accuracy. It showed 86.8% sensitivity on manually confirmed catches, so reported scores may be conservative.

How well does MLR detect errors?

MLR led every baseline on the benchmark. With 4 reviews, it caught 73.43% of distance-0 contradictions and 40.95% overall. The best baseline, AgentReview, caught 14.81% at distance 0. A single MLR review still caught 60.79%.

An ablation separates model from design. Swapping GPT-4.1 for Claude Sonnet 4 inside LLM-Review lifted distance-0 detection from 14.56% to 35.40%. MLR&#8217;s design added about 25 more points on a single review. Accuracy falls as node distance grows, which supports the severity scoring.

On real retracted papers from WithdrarXiv-Check (211 papers), gains shrink. MLR scored 26.07% on &#8216;similar&#8217; matches and 16.11% on &#8216;exact&#8217; matches. The strongest baselines scored 18.48% and 9.00%.

&&&

Does MLR agree with human reviewers?

On scores, mostly yes. On ICLR 2025 submissions, MLR&#8217;s predicted scores reached a Pearson correlation of 0.586 with human scores. The human-to-human reference was 0.742. On ICML 2025, the AI Reviewer edged it, 0.439 versus 0.429.

On focus, no. MLR stresses validity and experiments, while humans weigh clarity and novelty more. The authors frame this as a complementary perspective, not a replacement.

What does it cost to run?

MLR costs about $0.47 per review, excluding the optional literature agent. It uses 189,062 input tokens, about half of the AI Reviewer&#8217;s 403,654. A single-prompt variant cut cost by about two-thirds. Its detection dropped about 3.5 points on a subset of the benchmark.

How does MLR compare with other AI reviewers?

FeatureMLR (Sakana AI)LLM-ReviewAI ReviewerAgentReviewLLM used in this studyClaude Sonnet 4 + Haiku 3.5GPT-4.1o4-miniGPT-4oDesign3 agents, 3-pass chainSingle prompt, text truncated5-review ensemble, meta-review, reflectionReviewer, author, area chair rolesContradiction Benchmark, full40.95% (4 reviews)6.39%6.50%5.95%Core-claim errors (distance 0)73.43%14.56%11.17%14.81%WithdrarXiv-Check, similar / exact26.07% / 16.11%5.21% / 2.37%13.74% / 9.00%18.48% / 5.69%ICLR 2025 Pearson vs human0.586-0.0130.5380.195Input tokens per review189,0626,517403,654310,964Cost per review~$0.47~$0.01~$0.49~$0.81Open codeOn requestYesYesYes

All benchmark, correlation, token and cost figures come from the Beyond Imitation paper.

Key Takeaways

Sakana AI scores AI reviewers on catching errors, not copying humans.

MLR caught 73.43% of core-claim errors, about 5x the best baseline.

Model swap and 3-pass design each add large detection gains.

Real retracted-paper errors remain hard: 16.11% exact matches.

Hidden prompt injection still sways every AI reviewer tested.

Check out the Paper here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Sakana AI’s LLM Peer Review System Catches 73% of Core-Claim Errors appeared first on MarkTechPost.