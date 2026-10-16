---
publish_time: 1792070625
link: https://www.marktechpost.com/2026/10/15/openkylin-outlines-its-vision-for-reimagining-linux-in-the-ai-era-at-open-source-summit-europe-2026/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: false
digest: |
  在OSS EU 2026上，openKylin执行主任刘敏发表主旨演讲，提出以KART统一AI运行时与系统级智能体执行环境重构Linux；社区成员李建峰亦分享基于RISC-V打造AI-Ready Linux桌面的实践，展现开源社区在AI时代操作系统演进上的路线。
---

# openKylin 在 OSS EU 2026 阐述 AI 时代 Linux 重构愿景：KART 统一 AI 运行时与系统级智能体

> 原文链接：https://www.marktechpost.com/2026/10/15/openkylin-outlines-its-vision-for-reimagining-linux-in-the-ai-era-at-open-source-summit-europe-2026/
> 来源：MarkTechPost

Open Source Summit Europe 2026 (OSS EU 2026) took place in Prague, Czechia, from October 7 to 9. On October 8, Min Liu, Executive Director of openKylin, delivered a main-stage keynote titled “From AI Runtime to System Agents: Reimagining Linux for the AI Era with openKylin,” introducing KART, a unified AI runtime, along with a system-level agent execution environment. Jianfeng Li, a member of the community’s Technical Committee, also delivered a lightning talk titled “Building an AI-Ready Linux Desktop on RISC-V.”

openKylin is an open-source operating system community originating in China, dedicated to developing an AI-integrated OS for global users. Through presentations, demonstrations, and developer exchanges, the project showcased its latest work on AI and operating system integration.

Why Operating Systems Need to Evolve for the AI Era

The rapid adoption of open frameworks and open-weight models is creating a stronger foundation for AI innovation. PyTorch, vLLM, and llama.cpp provide reusable engineering components; open-weight models such as those from DeepSeek lower the barriers to model adaptation; and open-source communities continue to expand opportunities for upstream collaboration. 

openKylin believes the key challenge is no longer model capability alone, but the system infrastructure needed to connect AI with everyday computing. Model capabilities remain disconnected from desktop tasks, AI stacks are fragmented, and hardware–software integration remains highly complex. openKylin views this as a shared challenge for operating systems transitioning into the AI era, rather than one specific to any single community or company.

openKylin’s Vision: Moving from Resource Management to Intent Management

To bridge this gap, openKylin proposes a shift in the operating system management paradigm—from “resource management” to “intent management.” Traditional operating systems focus on managing CPUs, memory, and files. Operating systems in the AI era, by contrast, need to understand user goals and break them down into system actions that can be coordinated and observed, forming a closed loop of understanding, planning, execution, and observation.

The architecture comprises three layers:

● Runtime layer: KART, the unified AI runtime, and the kytensor local inference engine provide shared inference services.

● Agent execution layer: An agent execution environment supports KylinBot, Kylin-CUA, and third-party agents.

● Capability layer: API tools and desktop GUI skills make existing Linux capabilities accessible, with permission boundaries and execution monitoring governing their use.

openKylin 3.0 Brings AI Capabilities to the Desktop

In openKylin 3.0, these capabilities are reflected in three core desktop features:

● AI Assistant: Interaction shifts from “finding features” to “expressing intent.”

● Global Intelligent Search: Search moves from location-based lookup to semantic discovery.

● Intelligent Space: Information is organized around tasks rather than folders.

Expanding the AI Stack to RISC-V and Open Hardware Ecosystems

Focusing on key areas including hardware enablement, RISC-V Vector (RVV) extension optimization, AI runtimes, and heterogeneous computing, openKylin highlights the following:

● Inference acceleration: RVV kernel optimizations deliver a 2–5× speedup in FP32 inference with ONNX Runtime.

● Large-model support: The AI stack supports CPU inference with vLLM on SpacemiT K3.

● Multiple distribution formats: Delivery options include .deb packages, Python wheels, Conda, and Docker.

openKylin says this work is being advanced through open contributions, with plans to contribute both RVV kernel optimizations and inference framework enablement work upstream.

Demonstrations and Community Engagement

During the summit, AI PCs and other devices running openKylin 3.0 were showcased at the openKylin booth, where many attendees tried the systems and spoke with the technical team. Haihe Laboratory presented an interactive VR experience; SpacemiT exhibited a K3 laptop with openKylin 3.0 preinstalled; and Singapore-based Nanyang Singtech showcased its SingNova series of AI edge computing products.

Key Takeaways

The infrastructure gap: openKylin identifies system infrastructure, rather than model capabilities, as the key gap in the AI era. Model capabilities remain disconnected from desktop tasks, and AI stacks are fragmented.

openKylin’s architectural direction: A three-layer architecture comprising the KART unified AI runtime, an agent execution environment, and a capability layer enables the system to understand user goals and translate them into a closed loop of coordinated, observable actions.

Implementation in openKylin 3.0: AI Assistant, Global Intelligent Search, and Intelligent Space have been integrated into openKylin 3.0, shifting interaction from “finding features” to “expressing intent” and search from location-based lookup to semantic discovery.

RISC-V ecosystem expansion: RVV kernel optimizations deliver a 2–5× speedup in ONNX Runtime FP32 inference. Both the RVV kernel optimizations and inference framework enablement work are planned for upstream contribution.

About openKylin

openKylin is an open-source operating system community based in China, dedicated to developing an AI-integrated OS for global users. The community contributes to Linux and RISC-V ecosystems, with more than one million lines of core code contributed. Its UKUI desktop environment is included in the official repositories of 12 Linux distributions, including Debian, Ubuntu, and Fedora. As of October 2026, openKylin reports approximately 27 million deployments, 2.9 million active users, and more than 29,000 contributors worldwide.

The community has also established a network of international user groups across more than 30 countries. Looking ahead, the community plans to continue investing in three key areas: strengthening the runtime foundation to make AI easier to build; enhancing security and control to ensure actions are controllable and observable; and fostering a thriving open ecosystem to enable more efficient collaboration among hardware, models, and applications.

Official website: https://www.openkylin.top/index-en.html

Download openKylin: https://www.openkylin.top/downloads/os-en.html

openKylin on GitHub: https://github.com/openkylin

openKylin on AtomGit: https://atomgit.com/openkylin

openKylin on Gitee: https://gitee.com/openkylin

openKylin on DistroWatch: https://distrowatch.com/table.php?distribution=openKylin

This article is supported and promoted by openKylin

The post openKylin Outlines Its Vision for Reimagining Linux in the AI Era at Open Source Summit Europe 2026 appeared first on MarkTechPost.