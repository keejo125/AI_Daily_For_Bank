---
publish_time: 1794212420
link: https://www.marktechpost.com/2026/11/09/reason-machines-aspen-open-source-git-server-ai-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Reason Machines 发布开源 Git 服务器 Aspen，专门承接成百上千智能体并发推送的代码仓库流量，独立实现了 OpenAI 此前描述的设计。它针对“多 Agent 协作写代码”场景下传统 Git 服务的并发与权限瓶颈，为无人值守的代码工厂提供底层版本控制支撑。
---

# Reason Machines 开源 Aspen：面向 AI 智能体的 Git 服务器

> 原文链接：https://www.marktechpost.com/2026/11/09/reason-machines-aspen-open-source-git-server-ai-agents/
> 来源：MarkTechPost

Reason Machines has released Aspen, an open-source Git server for AI agent traffic. It targets repositories that hundreds of agents push to at once. Aspen independently implements the design OpenAI described for Pando. 

TL;DR

Size: One Rust binary. Branches live in PostgreSQL (or SQLite), packs live in object storage.

Runs on: A laptop (aspen dev), one host via Docker Compose, or Helm and Terraform clouds.

Performance: Pushes to different branches never wait on each other, and fetches reuse stored packs.

Best: 567 pushes per second sustained for 5 minutes on one 8-core server (self-reported).

Worst: Landing on main runs at about 4 per second, and the project is pre-alpha.

Bottom line: Best: per-branch writes remove the per-repository push ceiling. Worst: no releases, no web UI, and the 24-hour durability gate is not met.

What is Aspen?

Aspen is a self-hostable Git server from Reason Machines that scales writes per branch, not per repository. It speaks plain Git over HTTPS and SSH. Packs go to S3-compatible object storage; branch history goes to PostgreSQL.

Why do classic Git servers struggle with AI agents?

An agent pushes every few minutes, and CI fetches after each push. Per Reason Machines, a classic server queues every push to a repository together. It also builds a fresh pack for every fetch. Server work grows with clients, not with new code.

OpenAI hit this wall and built Pando. It cut median push latency by nearly 5x and serves nearly a petabyte daily.

How does Aspen work?

Aspen follows Pando and drops 2 claims most Git servers keep.

Per-branch compare-and-swap

Each branch is a chain of versions in one Postgres row. A push uploads its pack, then moves the branch with one compare-and-swap. Pushes to different branches never wait for each other. If 2 pushes race on one branch, one wins. The other gets Git&#8217;s usual &#8220;fetch first&#8221; error. The cost: branches may be read at slightly different moments.

Stored packs instead of per-client packs

Aspen never unpacks a push. It checks the pack, completes missing bases and stores it as-is. A fetch streams stored packs the client lacks, recompressing nothing. Signed URLs can serve packs from a CDN.

Trunk-only advertisement and compaction

A push sees only the trunk branch, so negotiation stays small with a million branches. Background compaction merges packs 16 at a time, in levels like a log-structured merge tree. A client far behind gets a few dozen packs, not thousands. Depth-1 CI fetches get a tip pack built once and served to every job.

How fast is Aspen?

The test used one 8-core server, S3 Standard and a 4-core Postgres. The target was a copy of git.git, about 4,500 files and 75,000 commits. Aspen sustained 567 pushes per second for 5 minutes with no errors. Each push reached S3 and Postgres before Git printed &#8220;ok.&#8221;

Median push latency: 208 ms; 99th percentile: 314 ms.

Another client saw each push 30 ms after acknowledgement, at the median.

Depth-1 fetch storm: 1.029x the bytes of stock git upload-pack on git.git.

Cursor reports up to 120 pushes per second for Origin on S3 Standard. On S3 Express One Zone it exceeds 300. That is a replicated cluster on Cursor&#8217;s monorepo, so setups differ. The README calls Aspen&#8217;s figures indicative, not performance claims.

How does Aspen compare with other agent-scale Git backends?

FeatureAspenCursor OriginOpenAI PandoGitHub SpokesAvailabilityOpen source, self-hostedCommercial Cursor platformInternal to OpenAIInternal to GitHubLicenseApache 2.0Not disclosedNot disclosedNot disclosedPush orderingPer branch (compare-and-swap)Per repository (write-ahead log in S3)Per branchThree-phase commit across replicasRef storagePostgreSQL or SQLiteWAL index in S3, no relational DBMetadata storeGit repos on NVMeFetch servingStored packs, stitched or via URIsLocal Git repo cache on NVMeReused stored packsGit repo replicasPublished push rate567/s, S3 Standard, 1 server (self-reported)120/s S3 Standard; 300+/s S3 ExpressNot disclosedNot disclosedOther published resultp99 push 314 msLinear read scaling to 100 replicasMedian push latency cut nearly 5xNot disclosed

How do you deploy Aspen?

You build from source with Rust. aspen dev runs everything with SQLite and a local directory. Teams get Docker Compose with PostgreSQL and MinIO, plus a Helm chart. Terraform covers AWS, Google Cloud, Azure and Hetzner. Mirror mode fronts GitHub or GitLab, so you can trial it without migrating.

The live demo is a 64 x 64 pixel canvas where each click is one pushed commit. Per the company, one Reason agent built Aspen from first commit to public in 4 days. That took 151 merged PRs.

Key Takeaways

Aspen is an Apache 2.0 Git server built for agent-scale push traffic.

It is an independent, open implementation of OpenAI&#8217;s Pando design.

Self-reported: 567 pushes per second on one 8-core server, p99 314 ms.

Clients need no changes; stock git works over HTTPS and SSH.

Check out the GitHub repo and the launch post. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Reason Machines Open-Sources Aspen, a Git Server Built for AI Agents appeared first on MarkTechPost.