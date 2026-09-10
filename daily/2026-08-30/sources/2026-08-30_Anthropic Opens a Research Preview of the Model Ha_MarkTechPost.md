---
publish_time: 1788070341
link: https://www.marktechpost.com/2026/08/29/anthropic-opens-a-research-preview-of-the-model-hardware-standard-mhs-a-shared-specification-for-ai-agents-to-safely-operate-physical-devices/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Anthropic 开放了模型硬件标准 MHS（Model Hardware Standard）的研究预览，这是一套让 AI 智能体发现并安全操作物理设备的统一规范。实验室或产线由互不兼容的仪器拼凑而成，过去每对设备都要专家手写专用转译层，搭建常需数周至数月，MHS 将其压缩到数小时甚至分钟级。MHS 标准化了操作系统与设备之间的驱动层，暴露 read/write/discovery 等原语，并通过 MCP、CLI 与代码文件三种方式控制，且模型无关。合作方实测：Genentech 用其自动化蛋白检测，QuEra 将激光重锁成功率从约 58% 提升至 99.3%（700 次中 695 次），CMU 把剂量-响应实验提速约三倍。安全限制内置于驱动而非提示词中。
---

# Anthropic 开放模型硬件标准 MHS：让 AI 智能体安全操控物理设备的统一规范

> 原文链接：https://www.marktechpost.com/2026/08/29/anthropic-opens-a-research-preview-of-the-model-hardware-standard-mhs-a-shared-specification-for-ai-agents-to-safely-operate-physical-devices/
> 来源：MarkTechPost

Anthropic has opened a research preview of the Model Hardware Standard (MHS), a shared specification that lets AI agents discover and operate physical devices. The problem it targets is plumbing. A lab bench or factory cell is assembled from vendors that never planned to interoperate, so every instrument ships its own interface and specialists hand-write bespoke translators between each pair. According to Anthropic team, the setup normally takes weeks to months, and that MHS cuts it to hours or minutes. 

The Integration Tax

Each instrument ships its own programming interface, so specialists hand-write bespoke translators between every pair. Even once wired together, there is no common way for devices to hand state to an agent or be operated safely by one. Anthropic says setup typically runs weeks to months; MHS reduces it to hours or minutes.

How it works

MHS standardizes the driver — the layer between an OS and a device. It exposes a small primitive set: read (get temperature), write (set temperature), plus discovery, so devices and agents find each other across a network without a translator in between.

It also carries knowledge code alone does not encode — the weight of a robot arm, for instance. Driver tags let a user write that in natural language, or have an agent interview them about the setup. The driver compiles those tags into a reference file: what a device measures, what can be adjusted, which safety limits are enforced.

Control runs through three mechanisms: the Model Context Protocol, a CLI, and code files. MHS is model-agnostic — any agent harness can reach it via standard protocols.

Interactive explainer &middot; Figures verified against Anthropic&rsquo;s MHS announcement &middot; &copy; Marktechpost

&&

What partners measured

Genentech automated the BCA protein assay across a liquid handler, robotic arm, and plate reader. Claude ran trial transfers of dyed liquid, read absorbance, scored itself against an expert&#8217;s plate using RMSE, and converged on ~140 µL/s for water (0.016 RMSE) and 10 µL/s for viscous BSA (0.181 RMSE) — parameters its automation experts confirmed as reasonable.

QuEra Computing is the sharpest number. A bespoke laser-relock script, built over months by a four-person team, worked about 58% of the time at ~150 seconds per attempt. Handed the same problem through MHS, a four-role agent loop ran unattended overnight and produced a deterministic Python script that recovered the lock 695 times out of 700 — 99.3%, hardest cases in 10–14 seconds against 5–10 minutes for a human. Claude also cut the servo&#8217;s residual error from a specialist&#8217;s 15.7 mV to 1.55 mV; over a 19-hour run its tune never lost lock, while the expert tune unlocked about 1.6 times an hour (QuEra blog).

Carnegie Mellon ran dose-response experiments roughly three times faster, orchestrating a liquid handler, plate reader, robotic arm, and cameras across three computers with incompatible interfaces — one with no programmatic interface at all. Driver-writing through to a completed curve, including an autonomous rerun after the agent rejected an R² < 0.9 fit, took about eight hours against the several weeks a vendor setup takes. Six induced fault conditions were all blocked before any device moved.

At the University of Washington, a PhD student in the Baker and Pinglay labs connected six instruments in under a week, driver-writing included. Tetsuwan Scientific paired MHS with its ResearchOS platform for qPCR pollution profiling. At Janelia, one microscopy rig went from seven programs launched in a fixed order to a single dashboard click.

Key Takeaways

A shared driver spec letting AI agents discover and operate any device with a programmable interface.

Integration drops from weeks to hours: CMU hit a finished dose-response curve in eight.

QuEra&#8217;s laser relock: 58% at ~150s, to 99.3% across 700 trials, as a deterministic script.

Model-agnostic and MCP-compatible; safety limits live in the driver, not the prompt.

Still gated, and still needs supervision — Claude&#8217;s physical reasoning has real gaps.

Check out the full announcement and apply for the preview. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Anthropic Opens a Research Preview of the Model Hardware Standard (MHS): A Shared Specification for  AI Agents to Safely Operate Physical Devices appeared first on MarkTechPost.