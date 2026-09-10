---
publish_time: 1787850289
link: https://www.marktechpost.com/2026/08/27/best-agent-sandboxes-2026-cold-start-pricing-network-policy/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  MarkTechPost对比了E2B、Daytona、Modal、Cloudflare、Vercel等主流智能体代码运行沙箱，指出该类产品的四个关键架构属性：并发下的冷启动、多轮间文件系统持久化、出口网络策略以及空闲计费。文章认为厂商宣传的冷启动数据难以横向比较，团队选型时应重点关注这些真实影响架构的属性而非功能矩阵。
---

# 2026年最佳智能体沙箱对比：冷启动、按秒计费与网络策略

> 原文链接：https://www.marktechpost.com/2026/08/27/best-agent-sandboxes-2026-cold-start-pricing-network-policy/
> 来源：MarkTechPost

Every agent that writes code needs somewhere to run it. That &#8220;somewhere&#8221; is now a product category with at least a dozen vendors, four incompatible billing models, and marketing pages that quote cold starts measured under conditions nobody publishes.

This comparison fixes the units. It covers the five platforms most teams shortlist — E2B, Daytona, Modal Sandboxes, Cloudflare Sandbox SDK, and Vercel Sandbox — along with Runloop, Fly.io Sprites, and Northflank where they change the answer.

The four questions that actually decide this

Feature matrices for this category are mostly noise. Four properties change architecture, and everything else is a preference:

Cold start under concurrency: An agent loop that creates a sandbox per tool call pays this tax thousands of times a day.

Filesystem persistence between turns: Does turn 2 see the pip install from turn 1, or does the agent rebuild its world?

Egress policy: Can the sandbox reach the internet, can you turn that off, and can you change your mind mid-session?

Idle billing: Agents spend most of their wall-clock waiting on a model. Somebody is paying for those seconds.

1. Cold start: what the numbers actually say

The vendor claims are not comparable to each other. Daytona&#8217;s pricing page advertises sub-90ms sandbox creation. E2B is commonly cited at roughly 150ms. Modal advertises sub-second cold starts for pre-cached containers. None of these state concurrency, region, image size, or whether the clock stops at API acknowledgment or at first executed command.

The most useful public dataset is ComputeSDK&#8217;s sandbox leaderboard, which is open source and runs on a schedule. It measures Time to Interactive (TTI): elapsed time from create() to the first successful command inside the sandbox, 100 iterations per provider, launched concurrently in a single burst, from a 4 vCPU host in Northern Virginia.

Results from the August 21, 2026 run:

ProviderMedian TTIP95P99Success rateVercel Sandbox0.67s1.04s1.12s100%Modal0.88s1.00s1.08s100%Runloop0.89s3.27s3.50s100%E2B1.61s1.77s1.81s100%Cloudflare5.06s6.04s6.48s100%Daytona0.27s0.43s0.44s37%

Three things in that table matter more than the ranking.

Burst is not the same test as sequential: Daytona&#8217;s fastest published median is real, and on an earlier provider-page run it created sandboxes at a 0.10s median when launched one at a time. On the August burst run it posted the fastest median in the field and completed 37 of 100 attempts. A median you only reach on a third of your calls is not a latency number, it is a capacity number. Retry logic is not optional on any of these platforms.

Tail latency is the number to design against: Runloop&#8217;s median and Modal&#8217;s median are 10ms apart. Runloop&#8217;s P95 is 3.3x Modal&#8217;s. If your agent&#8217;s UX budget is one second, the median tells you almost nothing.

Cloudflare is measuring a different product: Sandbox SDK sits on Cloudflare Containers, which schedules a container instance and boots an image. That is architecturally a heavier operation than resuming a pre-warmed Firecracker VM, and 5s medians reflect it. Cloudflare&#8217;s own GA post is candid about the shape of the problem: booting a sandbox, cloning a repo, and running npm install takes about 30 seconds, while restoring the same environment from a backup takes about two.

Reproducing this yourself

The task worth measuring is the one your agent runs, not echo hello. A useful harness runs the same unit of work everywhere: install pandas, read a CSV, plot it, return a PNG. Time four checkpoints separately.

Copy CodeCopiedUse a different Browser

# checkpoints: t_create -> t_ready -> t_deps -> t_result
# run 100 iterations sequential, then 100 concurrent, report median/P95/P99
import time, statistics

def one_run(provider):
    t0 = time.perf_counter()
    sbx = provider.create()              # API acknowledged
    t1 = time.perf_counter()
    sbx.exec("python -c 'print(1)'")     # first command returns: TTI
    t2 = time.perf_counter()
    sbx.exec("pip install pandas matplotlib")
    t3 = time.perf_counter()
    sbx.exec("python /work/plot.py")     # writes /work/out.png
    png = sbx.read_file("/work/out.png")
    t4 = time.perf_counter()
    sbx.kill()
    return dict(create=t1-t0, tti=t2-t0, deps=t3-t2, task=t4-t3, bytes=len(png))

Report tti and task separately. Vendors optimize the first and readers care about the second. Pin the region, pin the image, and publish both the sequential and the concurrent series, because they answer different questions.

2. Per-second pricing, normalized

Published rates as of August 27, 2026, converted to a common unit. Modal prices per physical core, which it defines as 2 vCPU, so the vCPU-equivalent is shown for comparison.

PlatformCPUMemoryBilling basisPlan floorE2B$0.0504 / vCPU-hr$0.0162 / GiB-hrWall-clock, per secondFree Hobby; $150/mo ProDaytona$0.0504 / vCPU-hr$0.0162 / GiB-hrWall-clock, per secondNone; $200 creditModal Sandbox$0.1419 / core-hr (~$0.0710 / vCPU-hr)$0.0240 / GiB-hrmax(request, actual), per secondFree Starter; $250/mo TeamVercel Sandbox$0.128 / vCPU-hr active CPU only$0.0212 / GB-hr provisionedSplit: CPU active, memory wall-clockHobby allotment; Pro creditCloudflare Sandbox$0.072 / vCPU-hr active CPU only$0.009 / GiB-hr provisionedActive CPU + provisioned memory/disk$5/mo Workers PaidFly.io Sprites$0.07 / CPU-hr$0.04375 / GB-hrActive use only; sleeps when idleSubscription tiersRunloop$0.108 / CPU-hr$0.0252 / GB-hrRunning state; suspended is storage-onlyFree Basic; $250/mo ProNorthflank$0.01667 / vCPU-hr$0.00833 / GB-hrAllocated resources, per secondFree Sandbox tier

Two footnotes that people get wrong.

Modal&#8217;s sandbox tier is roughly 3x its standard Function rate ($0.00003942 vs $0.0000131 per core-second), and region selection adds 1.5–1.75x on top. Sandbox pricing is not Modal&#8217;s headline compute pricing.

Daytona&#8217;s GPU rates are widely reproduced at $3.95/hr for an H100. Its live pricing page lists on-demand H100 at $2.27/hr and H200 at $2.61/hr. Third-party comparison tables in this category go stale within a quarter.

3. Cost per 1,000 executions

Rates are not costs. The model below fixes the workload and runs it through each rate card.

Assumptions: 2 vCPU / 4 GiB sandbox, 1,000 executions, no plan floor included, no egress, default region (Vercel iad1, Cloudflare standard-3 at 2 vCPU / 8 GiB / 16 GB disk since instance sizes are fixed).

Scenario A: short burst — 90s alive, 50% average CPU

PlatformCost / 1,000CompositionNorthflank$1.67$0.83 CPU + $0.83 memoryCloudflare$3.70$1.80 CPU + $1.80 memory + $0.10 diskE2B / Daytona$4.14$2.52 CPU + $1.62 memoryVercel$5.32$3.20 active CPU + $2.12 memoryModal$5.95$3.55 CPU + $2.40 memoryFly Sprites$7.88$3.50 CPU + $4.38 memoryRunloop$7.92$5.40 CPU + $2.52 memory

Scenario B: idle-heavy — 10 min alive, 5% average CPU

This is what a real agent loop looks like. The sandbox is open, the model is thinking, nothing is running.

PlatformCost / 1,000Change vs ANorthflank$11.116.7xCloudflare$13.873.7xVercel$16.273.1xE2B / Daytona$27.606.7xModal$39.666.7xFly Sprites (kept awake)$52.506.7xRunloop (kept running)$52.806.7x

Vercel moves from 4th-cheapest to 3rd, and its CPU line drops from $3.20 to $2.13 while everyone else&#8217;s scales linearly. Cloudflare&#8217;s active-CPU line falls to $1.20. That is the entire argument for active-CPU billing, and it is worth roughly 2x on this workload.

Scenario B with suspend

The platforms that lose Scenario B can win it back, if your orchestration suspends between turns instead of holding the box open. Same workload, 30s awake per execution:

PlatformCost / 1,000MechanismE2B (auto-pause)~$2.16Pause costs ~4s per GiB of RAM, resume ~1s (docs)Fly Sprites$2.62Idle monitor sleeps the sprite within secondsRunloop$2.64Suspend stops compute billing; storage continues

E2B&#8217;s number includes ~17s of pause and resume overhead for a 4 GiB sandbox. That overhead is the deciding variable: pausing is only economical when the gap between turns is meaningfully longer than the pause itself.

Fly&#8217;s idle detector is specific about what counts as activity: an in-flight HTTP or API request, output to a session&#8217;s stdout, an open TCP connection, or an active task (sprites.dev). An agent that holds a connection open while it waits is an agent that is billed. Redirecting output to a file does not count, which is a real lever.

4. Filesystem persistence between turns

This is where the platforms diverge most, and where the wrong choice shows up as a rebuilt node_modules on every turn.

PlatformDefault on stop/idleMemory stateMechanismE2BonTimeout defaults to killPause preserves RAM and running processespause() / connect(), paused boxes kept indefinitelyDaytonaPersistent by default; auto-stop 15 min (containers), auto-pause 60 min (VMs)VM sandboxes only, via pause/resumeStop, archive, pause, fork, volumesModalTerminated at timeout (default 5 min, max 24h)Memory snapshots, 7-day expiryFilesystem snapshots are Images, 30-day default TTLCloudflareSleeps after 10 min; disk resets to imageNocreateBackup() / restoreBackup(), R2 mounts, snapshots rolling outVercelPersistent sandboxes snapshot the filesystem on stopNoSnapshots, 30-day default expiry, $0.08/GB-moRunloopSuspend preserves stateYes, via suspend/resumeSuspend/resume and snapshot branching; Pro plan onlyFly Sprites100 GB root filesystem persists indefinitelyCheckpoint/restoreObject-storage-backed disk, no container image

Three details worth internalizing:

E2B&#8217;s default kills your work: onTimeout is kill unless you set lifecycle: { onTimeout: 'pause' } at creation. The killed state is terminal, and the docs describe no shutdown signal before termination. Treat unsaved work as lost.

Cloudflare&#8217;s disk is ephemeral across sleep: Container docs state plainly that a sleeping instance restarts with a fresh disk from its image. Backup and restore to R2 works today; the automatic persistAcrossSessions disk snapshot announced at GA was still rolling out at the time of writing.

Daytona splits persistence by sandbox class: Container sandboxes preserve the filesystem across stop/start but do not support pause, so memory is cleared every time. Linux VM sandboxes support both. GPU sandboxes are ephemeral and are deleted on stop; results have to be written to a volume.

5. Egress policy

Every platform in this comparison can now run a sandbox with no internet access. The differences are in precedence, granularity, and whether policy can change without a restart.

PlatformDefaultBlock allAllowlistChange at runtimeE2BOpen egressallowInternetAccess: falseDomains, IPs, CIDRs; wildcardsYes, updateNetwork() replaces the whole policyDaytonaTier-dependentnetworkBlockAlldomainAllowList (20 max), networkAllowList (10 CIDRs, IPv4 only)Yes, Tier 3/4 onlyModalOpen egress, no inboundblock_network=Trueoutbound_cidr_allowlist, outbound_domain_allowlist (beta)Alpha, and only if allowlists were set at createCloudflareOpen egressenableInternet = falseallowedHosts / deniedHosts, glob patternsYes, handlers and host rules apply liveVercelallow-alldeny-all, including DNSDomains via SNI, plus IP/CIDR fallbackYes, without restartingRunloopNetwork policies per devboxYesYesDocumented per devbox

The precedence trap

E2B and Vercel resolve conflicts in opposite directions. In E2B, allow rules take precedence over deny rules: an IP in both lists is allowed. In Vercel Sandbox, denied ranges override allowed ranges. A policy ported from one to the other without rewriting it does not mean the same thing.

The failure-mode trap

E2B documents that blocked TCP connections can look successful from inside the sandbox. The firewall accepts the connection before deciding whether the destination is allowed, so a socket opens and no packets arrive. Verify egress with an application-level response — an HTTP status, a TLS handshake — not with a successful connect(). Any test suite that asserts &#8220;network is blocked&#8221; by checking for a connection error will pass against an unblocked sandbox.

Credential injection is the real differentiator

Blocking egress is table stakes. Letting a sandbox make an authenticated call without ever holding the credential is not.

Cloudflare runs outbound handlers in the Workers runtime, outside the sandbox, with access to Workers bindings. The sandbox issues a plain request, the handler attaches the secret, and ctx.containerId scopes credentials per instance (docs). Vercel brokers credentials on egress with matchers scoped by path, method, query string, or headers, and states the firewall runs on the host outside the microVM where sandbox code cannot disable it (Vercel). E2B ships per-host request transforms in public beta that inject headers at the egress proxy, including workload-identity tokens the sandbox never sees. Runloop offers a Credential Gateway with opaque token injection.

For agents processing untrusted input, this design matters more than cold start. A prompt-injected agent with a GitHub token in its environment is a different incident from one that can only reach GitHub through a proxy holding the token.

6. Isolation, limits, and the fine print

PlatformIsolationMax sessionConcurrencyGPU in sandboxSelf-host / BYOCE2BFirecracker microVM1h Hobby, 24h Pro; resets after pause20 Hobby, 100 Pro, up to 1,100NoApache-2.0 infra repo, Terraform + Nomad + ConsulDaytonaContainers, plus VM and Windows classesConfigurable, wall-clock TTL optionalTier-basedYes (ephemeral)BYOC, enterpriseModalgVisor5 min default, 24h max100 Starter, 5,000 TeamYes, full rate cardNoCloudflareContainers on WorkersSleeps at 10 min idle, keepAlive available15,000 lite, 1,000+ standard-2NoNoVercelFirecracker microVM45 min Hobby, 24h Pro10 Hobby, 10,000 ProNoAWS BYOC in private betaRunloopmicroVMSuspend/resume10,000 demonstratedNoVPC deploymentFly SpritesFirecracker microVMPersistentSubscription tiersNoNoNorthflankmicroVM (Kata, Firecracker, gVisor)Persistent or ephemeralPlatform-levelYesSelf-serve BYOC

7. How to choose

Pick Vercel Sandbox if your agent waits on models more than it computes, and you want the cheapest measured burst cold start in this set. Active-CPU billing is worth roughly 2x on idle-heavy loops, the egress firewall with credential brokering is now available on every plan, and the 0.67s median with a 1.12s P99 was the tightest distribution in the August run.

Pick E2B if you need per-session kernel isolation for adversarial code, want memory-state persistence across turns, or need a self-host path. Set onTimeout: 'pause' on day one. Budget for the $150/mo Pro floor as soon as you exceed 20 concurrent sandboxes or 1-hour sessions.

Pick Daytona if persistence is the product and you can absorb capacity variance. The stop/archive/pause/fork lifecycle is the most developed in the category, forking a live VM with memory intact has no clean equivalent elsewhere, and the compute rate matches E2B without a subscription floor.

Pick Modal if any part of the agent&#8217;s work touches a GPU. It is the only platform here with a full GPU rate card inside the sandbox, T4 through B300. Price the 3x sandbox multiplier and regional multipliers before you commit.

Pick Cloudflare Sandbox if your app already lives on Workers and your egress security model matters more than your cold start. Programmable egress handlers running outside the sandbox with binding access are genuinely differentiated. Five-second burst medians are not, so hold sandboxes open per session rather than creating one per tool call, and plan for disk that resets on sleep.

Pick Runloop if you are building a coding agent and need SWE-Bench-style evaluation in the same platform. Note that suspend/resume, the feature that fixes its idle economics, is gated behind the $250/mo Pro plan.

Pick Fly Sprites if you want a persistent computer per user rather than a disposable one per call, and Northflank if you need the lowest published rate, GPU support, and self-serve BYOC in one platform.

Key Takeaways

Measured burst cold start spreads 7x across providers: Vercel 0.67s, Modal 0.88s, E2B 1.61s, Cloudflare 5.06s.

Vendor "sub-90ms" and "~150ms" claims describe sequential creates, not the concurrent bursts agents actually generate.

Billing model beats headline rate: the cheapest provider flips depending on how long your sandbox sits idle.

Only Vercel and Cloudflare bill CPU on active use; E2B, Daytona, Modal and Runloop bill wall-clock while the box is alive.

Every platform here can now deny egress by default, but allow/deny precedence and TCP failure behavior differ in ways that break assumptions.

Sources: E2B pricing, E2B persistence, E2B internet access, Daytona pricing, Daytona persistence, Daytona network limits, Daytona billing, Modal pricing, Modal sandbox networking, Modal sandbox resources, Modal sandbox snapshots, Cloudflare Containers pricing, Cloudflare outbound traffic, Cloudflare Sandboxes GA, Vercel Sandbox pricing, Vercel Sandbox firewall, Runloop pricing, Sprites and Northflank pricing

The post Best Agent Sandboxes in 2026: Cold Start, Per-Second Pricing, and Network Policy Across E2B, Daytona, Modal, Cloudflare, and Vercel appeared first on MarkTechPost.