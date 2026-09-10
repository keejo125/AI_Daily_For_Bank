---
publish_time: 1780798246
---

# 重写《给阿嬷的情书》结局：哈工大张民团队联合阿里开源全流程AI多智能体导演框架VideoClaw

> 原文链接：https://mp.weixin.qq.com/s/3NpB4iDCpGO21wFendiQcQ
> 公众号：机器之心

2026 年，国产视频生成模型频频出圈，在视频生成模型快速迭代的今天，生成一个 5 秒至 15 秒视频让人惊艳的画面片段已经不再新鲜。然而，

能不能从一句简单想法出发，自动生成剧情流畅完整、主体和场景一致的长视频？

受视频大模型生成时长限制，现有 AI 长视频生成需分段独立创作，因缺失跨片段的约束机制，导致生成视频存在人物、场景及叙事跨片段不一致的问题；同时依赖人工微调提示词，存在生成效率低、成本消耗大的核心瓶颈。因此，

如何构建长程、统一的跨片段时空约束机制，实现连贯一致的长视频生成，是亟待解决的关键科学、

技术和工程

难题。

早在 2023 年大模型快速发展期，哈工大张民教授立知大模型团队已开展多模态大模型驱动的视频内容创作智能体研究，并全球首发开源了电影制作智能体 FilmAgent

与动画片生成智能体 Anim-Director，

受到国内外智能体研究者与文艺创作者的广泛关注。

FilmAgent 项目链接：https://github.com/HITsz-TMG/VideoClaw/tree/main/FilmAgent

Anim-Director 项目链接：

https://github.com/HITsz-TMG/Anim-Director)

三年来，哈工大张民团队与阿里巴巴深入合作，在大模型视频创作领域稳步迭代，已发表 3 篇 SIGGRAPH、3 篇 ACL 等学术成果，多款开源工具陆续落地。

第一代技术方案是基于

大模型与工具深度交互

范式，并开源了 ComfyUI-Copilot、FilmAgent、Anim-Director 等视频生成框架，覆盖 3D 虚拟环境、工作流辅助、动画片创作等场景，主打视频创作流程自动化与效率提升。

视频内容创作智能体技术演进脉络

近几日，哈工大团队联合阿里巴巴正式推出

第二代多智能体高效协作视频生成框架

，全面突破能力和效率边界，Pixelle-Video 实现基于 ComfyUI 平台的全自动短视频生成；全新长视频创作框架 VideoClaw 支持短剧制作与剧情无限续写，解锁无限长视频创作能力。面向长视频生成的 AI 视频创作系统

VideoClaw

致力于将复杂的视频生成任务拆解为

可观察、可干预、可迭代的视频生产线

。

VideoClaw (1.3K⭐): https://github.com/HITsz-TMG/VideoClaw

ComfyUI-Copilot (5.2K⭐): https://github.com/AIDC-AI/ComfyUI-Copilot

Pixelle-Video (20.8K⭐): https://github.com/AIDC-AI/Pixelle-Video

多智能体协作：从创意到可执行的影视流水线

VideoClaw 将长视频生成拆解为一套

多智能体协作流程

：用户只需要输入一句灵感或故事梗概，系统便会调度由大模型驱动的 “数字化剧组”，依次完成剧本扩写、角色与场景设定、分镜规划、关键帧构图、视频分段生成、音频合成与后期拼接等任务。

VideoClaw 框架图

相比传统黑盒式视频生成，VideoClaw 将复杂任务拆成多个

可见、可控、可回溯

的生产环节，每完成剧本、角色场景、分镜等阶段，系统默认暂停并展示阶段性产物，让创作者能在关键节点介入修改。除了提供功能完备的

WebUI

供创作者进行精细化调整外，VideoClaw 支持集成至

微信、飞书

等日常通讯软件来调用。

场记库与长程上下文：

支撑连贯叙事和视觉一致

长视频生成困难的地方并不只是时长，而是如何让剧情、人物、道具和场景在多个镜头之间保持一致。因此，VideoClaw 引入了多阶段上下文管理机制，构建类似

「场记」的状态库

，将角色关系、空间位置、场景分镜和版本信息等沉淀为可复用的结构化资产，为后续生成提供参考约束。

场记状态库示意图

借助这种显式状态管理，VideoClaw 能够

支持故事

的无限续写

，让视频一段接一段地延展，剧情冲突自然升级，人物互动基于已有情节继续推进。

VLM 闭环质检：迭代质量优化机制

VideoClaw 将视觉语言模型（VLM）嵌入视频生成的关键流程中，在图片、关键帧和视频片段等中间产物生成后启动

审查

：一方面比对画面内容是否符合剧本设定和分镜要求，另一方面检查人物、场景和叙事逻辑是否出现偏移。

迭代质量优化机制示例

在具体执行中，系统可为同一创作任务并行生成多个候选版本，并由 VLM 进行

多维度综合评估

，筛选出最符合要求的结果。若所有候选版本都未达到预设质量阈值，VLM 会进一步输出具体的诊断报告，例如人物或场景不一致，并据此

触发回溯与重新生成

。

VideoClaw 生成视频案例

VideoClaw 支持多种安装方式，满足不同开发者和用户的需求，覆盖 Linux/Mac/Windows 快速安装、前端页面支持、OpenClaw 自动配置、以及 ClawHub 安装。

案例 1：影视二创

为《给阿嬷的情书》电影二创完美结局：在另一个时空，木生归乡，与淑柔相守一生，终得圆满。

视频以蒙太奇串联半生岁月：木生带信归家与淑柔、孩子相拥，一家三口乘车合影；骑车画面随蒙太奇岁月流转，二人暮年收到南枝寄来的家书与腊肉。镜头切换，南枝异地写信渐老，最后归来相聚院中晒木棉。

案例 2：写实短剧

输入剧情描述：程序员男主之前天天被老板 PUA，最后惨遭裁员。后来用 OpenClaw 创建一人公司，翻身收购原老板公司。

根据上述描述生成了 6 集的短剧，此处展示第一集，后续集数逐渐满足描述中的剧情。此后，VideoClaw 额外续写两集内容，生成的剧情聚焦 OpenClaw 衍生的网络安全隐患与行业规范管控问题。

案例 3：科幻漫剧

输入文件为刘慈欣《乡村教师》小说。根据该小说生成了 5 集漫剧，此处展示第一集。

总结与展望

VideoClaw 是一套流程可控、支持迭代的多智能体长视频创作框架。从团队初代工作流提效工具 ComfyUI-Copilot，到第二代日常短视频制作工具 Pixelle-Video 和长视频一键创作工具 VideoClaw，该系列方案不仅验证了智能体驱动影视创作的落地路径，也实现了从流程辅助提效到全链路智能化生成的升级。该系列开源项目的发布，为行业带来了一套开箱即用的视频生产智能体框架，期望助力 AI 视频生成与多模态创作领域的研究与应用发展。

参考文献

[SIGGRAPH Asia 2024] Zhenran Xu, Longyue Wang, Jifang Wang, Zhouyi Li, Senbao Shi, Xue Yang, Yiyu Wang, Baotian Hu, Jun Yu, Min Zhang. FilmAgent: Automating Virtual Film Production Through a Multi-Agent Collaborative Framework.

[SIGGRAPH Asia 2024] Yunxin Li, Haoyuan Shi, Baotian Hu, Longyue Wang, Jiashun Zhu, Jinyi Xu, Zhen Zhao, Min Zhang. Anim-Director: A Large Multimodal Model Powered Agent for Controllable Animation Video Generation.

[ACL 2025] Zhenran Xu, Xue Yang, Yiyu Wang, Qingli Hu, Zijiao Wu, Longyue Wang, Weihua Luo, Kaifu Zhang, Baotian Hu, Min Zhang. ComfyUI-Copilot: An Intelligent Assistant for Automated Workflow Development.

[SIGGRAPH Asia 2025] Haoyuan Shi, Yunxin Li, Xinyu Chen, Longyue Wang, Baotian Hu, Min Zhang. AniMaker: Multi-Agent Animated Storytelling with MCTS-Driven Clip Generation.

[ACL 2026] Zhenran Xu, Yiyu Wang, Yunxin Li, Muyang Ye, Xue Yang, Kai Chen, Longyue Wang, Weihua Luo, Baotian Hu, Min Zhang. ComfyFlow: Benchmarking LLMs for AIGC Workflow Generation.

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com