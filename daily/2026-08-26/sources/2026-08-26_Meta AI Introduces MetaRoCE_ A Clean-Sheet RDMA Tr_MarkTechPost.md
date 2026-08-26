---
publish_time: 1787678736
link: https://www.marktechpost.com/2026/08/25/meta-ai-introduces-metaroce-a-clean-sheet-rdma-transport-built-for-ai-scale-ethernet/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Meta 发布 MetaRoCE，一套为 AI 规模以太网从头设计的 RDMA 传输协议。与标准 RoCE 假设网络有序交付不同，MetaRoCE 把网络视为有损，将排序、路径选择与恢复下沉到网卡（NIC），打破对 PFC 与包喷洒的限制，适配多平面大规模网络。Meta 同步开源规范、参考软件实现与合规测试套件，目标降低集合通信（all-reduce/all-to-all）中的网络摩擦与算力空转。
---

# Meta 发布 MetaRoCE：面向 AI 规模以太网的干净 RDMA 传输协议

> 原文链接：https://www.marktechpost.com/2026/08/25/meta-ai-introduces-metaroce-a-clean-sheet-rdma-transport-built-for-ai-scale-ethernet/
> 来源：MarkTechPost

Training and serving frontier models is now a networking problem as much as a compute problem. Collective operations like all-reduce and all-to-all synchronize thousands of accelerators during training, and the slowest transfer sets the pace for the entire job. Even small amounts of network friction directly strand significant compute capacity. 

This week, Meta introduced MetaRoCE. It is described as a clean-sheet RDMA transport protocol purpose-built for AI workloads on commodity Ethernet. The design breaks with standard RoCE on its central assumption. Standard RoCE expects the network to deliver every frame in order, leveraging PFC and discouraging the packet spraying that provides performance in multiplane and large-scale networks. MetaRoCE instead treats the fabric as lossy and pushes ordering, path selection, and recovery into the NIC. Meta is releasing the specification, a reference software implementation, and a compliance test suite through the Open Compute Project (OCP)

Is it deployable?

Not yet, the artifacts possibly ships in October, 2026. Meta may release the MetaRoCE specification, a DPDK-optimized software reference implementation, and its production compliance framework at the 2026 OCP Global Summit. Hardware support is early: Meta proved it on AMD Pensando programmable NICs, with additional implementations underway from other vendors. For now this is a fabric-architecture decision, not a procurement one

The problem: the fabric sees packets, the NIC sees intent

Meta has scaled clusters to hundreds of thousands of GPUs across multiple data centers and regions. At that size the network sits in the critical path of every training step. Collective operations like all-reduce and all-to-all synchronize thousands of accelerators, and the slowest transfer sets the pace for the entire job. 

Standard RoCE is the constraint. It expects the network to deliver every frame in order, leans on PFC, and discourages the packet spraying that provides performance in multiplane and large-scale networks. MetaRoCE inverts that: intelligence moves to the endpoint, and the network decomposes into many fine-grained logical paths, each with its own real-time telemetry — per-path RTT, ECN state, and utilization. 

This builds directly on Meta&#8217;s 2024 RoCE-at-scale work and its broader infrastructure evolution.

Six design decisions that matter

Out-of-order delivery is the default: Packets are sprayed across many paths and arrive out of order by design. Every packet carries its own destination, so data is written straight to its final memory location as it lands — no reorder buffer, no head-of-line blocking. Sends carry the match to a posted receive buffer, so a Send lands correctly even when messages ahead of it have not arrived. 

Multipathing is native: Each path carries a distinct UDP source port as its ECMP entropy, which the NIC can change at any time to move traffic off a bad route. Because each path keeps its own window and round-trip estimate, the transport can tell congestion from failure and rebalance explicitly.

Loss tolerance replaces losslessness: MetaRoCE treats the fabric as lossy — no PFC, no pause frames. A gap in a path&#8217;s 256-bit selective acknowledgment bitvector is evidence of loss rather than reordering, so it triggers retransmission of exactly the missing packet, on the path that lost it.

Congestion control runs from both ends: Sender-driven ECN-based AIMD is combined with receiver-driven fair-share rate hints. In every acknowledgment the receiver returns the share of inbound bandwidth it allocated to that sender, so senders approach the right speed directly rather than searching for it. Incast resolves in one or two round trips.

Topology independence: MetaRoCE asks the fabric for two things every switch already has: ECN marking and ECMP. It does not require packet trimming, in-network telemetry, credit-based flow control, or switch-side spraying — which means it also runs over vendor clouds whose configuration you don&#8217;t control. 

Connection state stops exploding: Traditional RDMA gets more ordering or bandwidth by opening more queue pairs — dozens per node pair — each with a congestion window blind to the rest. MetaRoCE separates the two: one connection carries many independent ordered streams above and many paths below, under one congestion controller.

The numbers

Meta implemented MetaRoCE on AMD Pensando programmable NICs. On a 64-node AMD GPU cluster running RCCL collectives, it was compared directly against RoCEv2 across all-reduce and all-to-all, delivering higher throughput and lower flow completion times. 

The resilience result is the core statement: MetaRoCE maintains ~86% throughput at 1% packet loss and continues delivering useful bandwidth even at 10% loss rates, converging gracefully rather than collapsing. Multiplane validation across 4-plane and 8-plane topologies with up to 4,000 concurrent connections confirmed throughput scales linearly with plane count, and simulated plane failures showed traffic redistributing without application involvement or operator intervention. 

Open by design

MetaRoCE extends the multi-vendor philosophy that OCP&#8217;s Ethernet Scalable Unified Network (ESUN) initiative established for the fabric into the transport layer. Three artifacts ship: the full spec via OCP, a compliance suite that lets vendors prove their implementations match, and libsoftmetaroce as the authoritative behavioral model for silicon development. Meta has proven it on AMD Pensando hardware, with additional implementations underway from other vendors. 

Explainer embed

&

Key Takeaways

MetaRoCE is a clean-sheet RDMA transport that treats Ethernet as lossy — no PFC, no pause frames.

Packets spray across paths and write straight to memory; no reorder buffer, no head-of-line blocking.

Holds ~86% throughput at 1% loss on a 64-node AMD GPU cluster running RCCL.

Needs only ECN and ECMP from switches, so it runs on fabrics you don&#8217;t control.

Spec, compliance suite, and libsoftmetaroce land at the OCP Global Summit in October.

Check out the TECHNICAL DETAILS here.

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

The post Meta AI Introduces MetaRoCE: A Clean-Sheet RDMA Transport Built for AI-Scale Ethernet appeared first on MarkTechPost.