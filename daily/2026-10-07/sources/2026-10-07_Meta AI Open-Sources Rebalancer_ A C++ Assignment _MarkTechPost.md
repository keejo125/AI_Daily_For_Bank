---
publish_time: 1791354554
link: https://www.marktechpost.com/2026/10/06/meta-ai-open-sources-rebalancer-a-c-assignment-solver-that-runs-about-40-million-placement-problems-a-day/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Meta 开源 Rebalancer——一个带 Python 接口的 C++ 分配问题求解库（Apache 2.0），用于在高可用与可扩展约束下决定“对象放哪个桶”。其设计将问题规格与求解分离：规格编译为表达式图，再由局部搜索（并行、每秒数百万次评估）或 MIP 求解器（FICO Xpress / Gurobi / HiGHS）求解。Meta 内部已运行 9 年，日均处理约 4000 万分配问题、30+ 种 formulation，P99 在 26.5 万对象 / 3200 桶上为 12 秒；并提供 Docker 化调试 UI Rebalancer Explorer。对标 Google OR-Tools，其优势是一套分配规格同时跑局部搜索与 MIP。
---

# Meta 开源 Rebalancer：日均处理约 4000 万分配问题的 C++ 求解器

> 原文链接：https://www.marktechpost.com/2026/10/06/meta-ai-open-sources-rebalancer-a-c-assignment-solver-that-runs-about-40-million-placement-problems-a-day/
> 来源：MarkTechPost

Meta has open-sourced Rebalancer, a C++ library with a Python interface for solving assignment problems. It decides which objects go into which bins under constraints and objectives. According to the Engineering at Meta&#8217;s post, Rebalancer has handled resource allocation across Meta for over 9 years. The release ships under Apache 2.0 with documentation, a PyPI package and a debugging UI called Rebalancer Explorer.

Is it deployable? Yes. pip install rebalancer installs v1.0.4 for Python 3.12+, with prebuilt wheels for Linux x86-64 and macOS 14+ ARM64. .deb, .rpm and Homebrew packages also exist. PyPI still classifies the project as Alpha.

What Problem Does Rebalancer Solve?

Assignment problems show up across Meta&#8217;s stack. Racks go into datacenters, servers go to services, tasks go to servers, and user traffic goes to datacenters. Meta names 2 blockers: usability and scalability. Engineers struggle to turn policies into precise formulas, and many problems are NP-hard and too large for commercial solvers.

Rebalancer&#8217;s answer is to separate how a problem is specified from how it is solved. The design is detailed in the OSDI 2024 paper, Optimizing Resource Allocation in Hyperscale Datacenters.

How the Specification Layer Works

The spec language has 3 layers:

Modeling constructs: dimensions (attributes such as CPU or storage), partitions (groups of objects), scopes (groups of bins) and utilization.

Expression API: aggregate utilization with SUM or MAX, or transform it with operations such as SQUARE.

Spec API: dozens of predefined objectives and constraints, listed in the docs.

Meta&#8217;s example models tasks as objects, servers as bins and racks as a scope. A CapacitySpec caps CPU and storage per server. A GroupCountSpec keeps 1 job type per rack. A BalanceSpec balances each server&#8217;s utilization across both dimensions.

One Expression Graph, Two Solvers

Rebalancer compiles the spec into a directed acyclic expression graph. Leaf nodes hold utilization values; aggregation and transformation nodes sit above them. Users supply an initial assignment and a stopping condition. Constraints that the initial assignment already violates become high-priority goals.

Optimal solver: The graph is translated into a mixed integer program for FICO Xpress, Gurobi or HiGHS. Variable aggregation and symmetry breaking shrink models. The worst-case model size is still O(objects × bins). Meta&#8217;s largest problems are too big for any MIP solver.

Local search: This solver works directly on the expression graph. It explores moves of objects to other bins, with a worst-case neighborhood of O(objects + bins). It then applies the best candidate that breaks no constraint. Evaluation is parallelized, reaching millions of evaluations per second, and the search space is pruned.

Meta uses local search for almost all large problems and MIP for small to mid-size ones, often prototyping with MIP first.

Production Numbers at Meta

About 40 million assignment problems solved per day, across 30+ unique formulations.

P99 solve time of 12 seconds on 265k objects and 3.2k bins.

Problems above 1 million objects and 5k bins average 171 seconds, across 3.4k+ runs.

Best Use Cases for Rebalancer

Placing shards, tasks or containers on a cluster: Assign work to servers under CPU and memory caps while spreading replicas across racks. Meta&#8217;s Shard Manager and RAS run this pattern.

Balancing traffic and workloads across regions: Route user traffic or jobs to datacenters, trading latency against load. Taiji does this for edge traffic, and Meta balances ML training by priority.

Operational assignment outside infrastructure: Map support tickets to engineers, meetings to rooms or desks to people under capacity rules. Meta has done all 3.

Debugging With Rebalancer Explorer

Modelers at Meta spent most of their time debugging solver behavior. Rebalancer Explorer is a Dockerized web UI built for this. It shows binding constraints, relaxation effects, and why an object landed in a bin.

Interactive Explainer

Rebalancer vs Closest Open Source Alternatives

FeatureMeta RebalancerGoogle OR-ToolsTimefold Solver (Community)LicenseApache 2.0Apache 2.0Apache 2.0 (Enterprise edition is commercial)Core languageC++C++JavaAPIsC++, PythonC++, Python, Java, C#Java, KotlinFocusGeneric assignment (objects to bins)Broad suite: CP-SAT, LP, MIP wrappers, routing, packing, assignmentPlanning: routing, rostering, scheduling, task assignmentLocal searchYes, parallel, on expression graphYes, in routing solver (guided local search, simulated annealing, tabu)Yes, core engine (tabu, simulated annealing, late acceptance)MIP backendsFICO Xpress, Gurobi, HiGHSWrappers for commercial and open source MIP solversNot usedDebugging UIRebalancer Explorer (Docker)Not listed in READMEBenchmarker; score analysis in commercial editionsInstallpip install rebalancerpip install ortoolsMaven, JDK 21+

OR-Tools covers more problem classes, and Timefold targets JVM scheduling and routing. Rebalancer&#8217;s edge is one assignment spec that runs on both local search and MIP.

Key Takeaways

Rebalancer models any assignment problem as objects, bins, constraints and objectives.

Specs compile into an expression graph solved by local search or a MIP solver.

MIP backends include FICO Xpress, Gurobi and open source HiGHS.

Meta runs about 40M problems a day; P99 is 12s on 265k objects and 3.2k bins.

Apache 2.0, C++ and Python APIs, installable from PyPI today.

Check out the Paper, GitHub Repo and Technical details. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

[Sponsored] The web is the one API most agents are missing. Databases, calendars and repos have APIs. The open web mostly doesn’t. The TinyFish MCP server gives any MCP client four tools: TinySearch, TinyFetch (full pages as markdown, JavaScript included), TinyBrowser for logins and forms, and TinyAgent for multi-step jobs. Search and Fetch are free.

The post Meta AI Open-Sources Rebalancer: A C++ Assignment Solver That Runs About 40 Million Placement Problems a Day appeared first on MarkTechPost.