---
publish_time: 1780718400
---

# 大晓机器人联合南洋理工打通Physical AI全链路！PhysX-Omni补齐物理AI基建

> 原文链接：https://mp.weixin.qq.com/s/5rspbiAQ8YWoVIgI97w8Cw
> 公众号：机器之心

PhysX-Omni：统一刚体、可形变与关节物体的物理 3D 生成

该论文第一作者为曹子昂，研究方向主要聚焦于 3D AIGC、Physical AI 与具身智能。论文主要合作者包括来自南洋理工大学的李海天、姚润茂、洪方舟、陈昭熹，以及大晓机器人的刘英豪和潘亮。通讯作者为南洋理工大学刘子纬教授。

此前，大晓机器人曾发布 ACE 具身研发范式 ——“环境式数据采集 — 世界模型 —— 泛化大脑模组”，新研究成果和研发范式或将为其打造能真正理解并交互物理世界的机器人的最强大脑提供核心数据基建。

论文标题：

PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects

论文链接：

https://arxiv.org/abs/2605.21572

项目主页：hthttps://physx-omni.github.io/

GitHub 代码：https://github.com/physx-omni/PhysX-Omni

近年来，随着大语言模型（LLM）、视觉语言模型（VLM）以及具身智能（Embodied AI）的快速发展，人工智能正从 “感知世界” 迈向 “理解并交互世界”。然而，现有大多数 3D 生成方法仍主要关注外观与几何结构，缺乏真实世界所需的物理属性与运动能力，难以直接应用于机器人与物理仿真场景。同时，simulation-ready physical 3D generation 领域也长期面临数据稀缺与缺乏统一评测标准的问题。

为了解决这些挑战，研究团队提出了全新的统一生成框架 PhysX-Omni，首次实现对刚体、可形变物体以及关节物体的统一建模，能够直接生成具备丰富物理属性、可用于真实仿真环境的高质量 3D 资产，并进一步构建了更大规模的数据集与统一 benchmark，为 Physical AI 与 Embodied AI 研究提供了新的基础。

1 引言

与传统 3D AIGC 方法不同，PhysX-Omni 不仅关注几何结构与视觉质量，更进一步建模物体的绝对尺度（Absolute Scale）、材料属性（Material）、运动学参数（Kinematics）、交互能力（Affordance）以及语义描述（Description）等关键物理信息，从而真正实现 “可交互、可运动、可仿真” 的 Physical AI 资产生成。

PhysX-Omni 的核心创新之一，是提出了一种专门面向 VLM 的全新几何表征方式，可以直接显式建模高分辨率三维结构，同时无需引入额外 special token。通过避免 segmentation 带来的误差累积。

此外，为了解决 simulation-ready physical 3D 数据稀缺的问题，研究团队进一步构建了首个通用 simulation-ready physical 3D dataset，PhysXVerse。该数据集包含超过 8K 个高质量 physical 3D assets，覆盖 2K+ 室内与室外类别。为了更加全面地评估 simulation-ready 3D generation，团队还提出了首个物理 3D generation benchmark——PhysX-Bench。首次从六个核心维度对生成结果进行综合评估，包括：几何结构、绝对尺度、材料属性、可供性、运动学、语义描述。

2 方法介绍

2.1 物理几何表征

为了实现高质量生成，PhysX-Omni 提出了一种全新的几何表征。受经典二维 Run-Length Encoding（RLE）启发，该方法设计了一种 template-based RLE representation，用于显式、高效地建模高分辨率三维结构。

具体而言，系统首先将 3D 资产体素化（voxelization），并根据对象的部件层级结构划分为 part-level voxels。随后，每个部件级体素会沿 z-axis 切分为一系列二维二值 mask，并对每一层采用紧凑的二维 RLE 编码，将占据区域高效转换为文本 token 表示。不同于传统二维 RLE，三维结构在相邻切片之间通常具有较强的空间冗余性，尤其是在平滑区域或重复结构中。

为进一步提升压缩效率，PhysX-Omni 提出了 template layers 的概念：多个结构相似的切片可以共享同一个模板，仅记录它们相对于模板的残差变化，而无需对每一层进行独立编码。通过复用跨层结构模式，该方法在保留精细几何信息的同时，大幅减少了 token 数目。

此外，这种 template-based representation 在整个生成过程中始终保持显式三维结构信息，因此相比传统 autoregressive geometry generation 方法具有更强的鲁棒性，能够有效降低预测误差累积问题，并更加适用于复杂高分辨率三维结构建模。

2.2 PhysXVerse 数据集

为了缓解 simulation-ready physical 3D 数据稀缺的问题，PhysX-Omni 构建了首个通用物理化 3D 数据集，PhysXVerse。为了获得高质量的 simulation-ready assets，研究团队基于 PartVerse 提供的人类验证部件分割结果，并进一步结合此前提出的 human-in-the-loop physical annotation pipeline，对物理属性进行精细标注。

最终，PhysXVerse 包含超过 8.7K 个高质量 simulation-ready physical 3D assets，覆盖 2.9K+ 类别，包括室内家具、无人机、机器人、车辆以及大型场景组件等多种复杂对象。相比现有 simulation-ready datasets，PhysXVerse 在类别多样性与物理属性覆盖范围上都有显著提升。

2.3 P

hysX-

Bench

为了全面评估 simulation-ready physical 3D generation，研究团队提出了首个统一 benchmark——PhysX-Bench。该 benchmark 基于开源 Vision-Language Model（Qwen3.5）与 physics-based simulation，对生成结果进行真实场景下的综合评估。为了降低复杂物理属性与三维结构理解难度，PhysX-Bench 不直接输入物理参数，而是通过渲染图像与仿真视频进行评测，从而更加贴近真实人类感知与机器人应用场景。

PhysX-Bench 从六个核心维度对生成结果进行评价，包括 Geometry、Absolute Scale、Material、Affordance、Kinematics 与 Description。

其中，Geometry 用于评估三维结构一致性与视觉质量，包括 CLIP alignment、multi-view 3D consistency 以及 visual quality 等指标；Absolute Scale 用于衡量生成结果在真实世界中的尺寸合理性；Description 则评估对象及部件级别的语义理解能力。

在物理属性评估方面，Material 通过自由落体、水中下落等物理模拟视频，对密度、杨氏模量以及泊松比等材料属性进行间接评测；Affordance 则基于人类常识，对对象的交互合理性与功能区域进行评估；Kinematics 通过运动视频分析关节运动的一致性、合理性以及整体运动协调性，从而衡量生成结果是否具备真实可信的物理行为。

通过结合物理仿真与强大的 VLM 推理能力，PhysX-Bench 能够更加真实、全面地评估 simulation-ready physical 3D assets 的生成质量与实际可用性，为后续 Physical AI 与 Embodied AI 研究提供了统一评测标准。

3 实验

3.1 在传统评估指标上的结果

研究团队将 PhysX-Omni 与 PhysXGen、Articulate-Anything、MonoArt 以及 PhysX-Anything 等最新 simulation-ready 3D generation 方法进行了系统对比，并在 PhysXVerse 与 PhysX-Mobility 数据集上进行了大量实验。结果表明，PhysX-Omni 在几乎所有几何与物理属性指标上都取得了最佳性能，展现出了统一 simulation-ready physical generation framework 的显著优势。

PhysX-Omni 在物理属性预测上实现了大幅提升。特别是在 Absolute Scale 评估中，其误差相比 PhysXGen 与 PhysX-Anything 降低了两个数量级，说明模型对真实世界尺寸与物理先验具备更强理解能力。在 Material、Affordance、Description 以及 Kinematics 等维度上，PhysX-Omni 也均取得了最优结果。其中，运动学（Kinematics）提升尤为显著，证明该框架能够更加准确地推理关节结构、运动类型以及运动约束，从而生成具备真实物理行为的 articulated assets。

3.2 PhysX-Bench 上的结果

为了更加全面地评估不同方法在真实场景中的泛化能力，研究团队进一步在新提出的 benchmark——PhysX-Bench 上进行了系统实验。不同于传统依赖 ground-truth 标注的评测方式，PhysX-Bench 更强调真实场景下的 ground-truth-free evaluation，其测试图像同时包含真实世界照片与渲染生成图像，覆盖大量复杂类别与 challenging in-the-wild cases。Benchmark 从 Geometry、Absolute Scale、Material、Affordance、Kinematics 与 Description 六个维度，对 simulation-ready physical 3D generation 进行综合评估。

实验结果表明，PhysX-Omni 在绝大多数 physical attributes 上均取得了最佳性能，尤其在 Absolute Scale、Material、Affordance、Kinematics 与 Description 等维度表现尤为突出。同时，在 Affordance 与 Description 等任务上，PhysX-Omni 也展现出了更强的物理推理与语义理解能力。此外，论文还进一步展示了大量可视化结果。实验表明，PhysX-Omni 在复杂结构、精细几何以及 challenging articulated objects 上都展现出了更强鲁棒性。

3.3 相关应用

为了验证生成结果在真实仿真环境中的可用性，研究团队进一步将 PhysX-Omni 生成的 simulation-ready 3D assets 直接部署到物理模拟器中，用于机器人交互与策略学习。实验证明了为未来大规模 embodied AI 数据构建提供了新的可能性。

除了 object-level generation，研究团队还进一步探索了 PhysX-Omni 在 scene-level simulation-ready generation 中的潜力。这些结果进一步证明，PhysX-Omni 不仅能够生成高质量 simulation-ready assets，还为未来 scene-level physical world generation、机器人训练环境构建以及 embodied AI world modeling 提供了重要基础。

4 总结

PhysX-Omni 提出了首个统一的 simulation-ready physical 3D generation framework，实现了对刚体、可形变物体以及关节物体的统一建模。相比传统仅关注外观与几何的 3D 生成方法，PhysX-Omni 能够同时生成几何结构、材料属性、运动学参数、交互能力等丰富物理信息，从而直接构建可用于真实仿真环境的 simulation-ready 3D assets。

为解决数据与评测缺失问题，研究团队进一步构建了通用数据集 PhysXVerse 与统一 benchmark PhysX-Bench。大量实验结果表明，PhysX-Omni 在几何质量、物理一致性以及运动建模上均显著优于现有方法，并能够直接应用于机器人策略学习、场景生成以及 embodied AI 等下游任务，为未来 Physical AI 与物理世界生成提供了新的研究方向。

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com