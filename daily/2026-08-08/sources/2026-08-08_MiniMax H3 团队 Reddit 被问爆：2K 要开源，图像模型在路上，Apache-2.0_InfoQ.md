---
publish_time: 1786147200
status: pending
---

# MiniMax H3 团队 Reddit 被问爆：2K 要开源，图像模型在路上，Apache-2.0 也在考虑了

> 原文链接：https://www.infoq.cn/article/9C3eK9tJqDXbabbBy3aj
> 来源：InfoQ

MiniMax H3 开放权重之后，开发者最关心的几个问题，终于有了官方回应。

8 月 7 日晚上 10 点，MiniMax H3 团队来到 Reddit 的 r/StableDiffusion 社区举行 AMA（Ask Me Anything）。

MiniMax H3 团队公开回应一切

参与此次交流的包括 H3 研究负责人 dacongya，研究员 Luigi、Nero、Kiro，系统工程师 Reynor，以及 MiniMax 开发者关系负责人 Ryanlee。团队表示，讨论范围将涵盖模型架构与训练、视频生成、图生视频与参考生成、推理优化以及未来计划。

这场讨论受到相当高的关注。

截至发稿时，帖子已经积累超过 300 条评论，目前已经在 Reddit 页面被标记为“Finished”。

而从整个讨论看，社区关注的重心已经从 H3 在某个 Benchmark 上超过了谁，换成了一些更实际的问题，比如 2K 能不能本地跑？Sparse Attention 什么时候开放？有没有 4 步版本？为什么 Ref2Vid 比 I2V 糊？能不能拿它直接生成图片？Context-IR 怎么在本地复现？MiniMax 以后还会不会继续开放模型？

这些问题，也恰好指向一个开放模型发布之后真正困难的部分——开放权重只是第一步，围绕训练、推理、工具链和模型能力边界的东西，到底能开放到什么程度，才真正决定一个模型最终能形成多大的开发者生态。

H3 是 MiniMax 7 月 31 日正式发布的全模态视频生成模型，可以同时理解文本、图像、视频和声音组成的上下文，并生成最长 15 秒、最高 2K 分辨率、带原生双声道的视频。MiniMax 当时表示，会在符合法律法规的前提下开放模型权重。

而在这次 AMA 中，MiniMax 第一次比较具体地回应了开放之后的下一步。

InfoQ 整理了 Reddit 社区中讨论热度比较高的提问和H3团队的回答，以飨读者。

一些关键问题

用于最终 2K 输出的模型会不会发布？

社区最集中的问题，首先指向 H3 的 2K 能力。

H3 发布时，MiniMax 将 2K 输出背后的方案称为 In-context Regeneration。按照官方此前的解释，它没有走传统视频模型常见的独立超分路线，而是让模型结合原有的多模态上下文，对低分辨率结果再次生成高分辨率版本。这样做的目的，是让模型重新“生成”文字、纹理等信息，而不仅仅依赖超分算法从低分辨率像素中猜测细节。

但开放权重后，社区拿到的版本还无法完整复现线上 2K 能力。

于是有开发者直接询问：用于最终 2K 输出的模型会不会发布？

MiniMax 开发者关系负责人 Ryanlee 先给出了一个非常简短的肯定答复：“会，而且不会太久。”

随后，H3 研究员 Kiro 给出了更完整的技术解释。

他表示，H3-Regenerate-2K 本质上是第二阶段的条件生成过程，但并不是简单地把目前发布的 H3 Base Checkpoint 再运行一遍，更不是传统意义上的 Upscaler。

这个阶段实际上使用了一个专门面向更高目标分辨率的 latent-space DiT regeneration checkpoint。基础模型此前生成的内容会作为额外上下文输入，同时部分参考输入也会以更高分辨率提供给模型。

H3 是否直接沿用了 M3 上的 MSA？

第二个高频问题是速度和显存。

H3 在训练后期已经使用稀疏注意力，但目前开放版本仍然以 Full Attention 推理。随着视频分辨率和时长提高，Attention 的计算和显存开销会快速膨胀，因此 Sparse Attention 被不少开发者视为 H3 后续最重要的本地推理优化之一。

有人询问：H3 是否直接沿用了 MiniMax M3 大模型上的 MSA，也就是 MiniMax Sparse Attention？

Kiro 给出了明确答案：H3 没有使用 MSA。

H3 的方案更接近 MoBA-style block selection。其基本思路是利用相邻视觉 Token 高度相关的特征，将一组 Token 进行 mean pooling 得到 Block Representation，再利用这些表示判断哪些 Block 更重要，从而减少不必要的 Attention 计算，同时不需要额外训练一个 learned indexer。

目前，这套方案只针对视频 Token 做了三维稀疏化，图片和文本 Token 尚未进入同样的稀疏路径，不过团队正在研究进一步扩展。

MiniMax 表示，计划近期给社区提供一个相对保守的 Sparse Attention 参考实现，第一目标不是追求一个夸张的加速数字，而是做到没有可感知的质量损失。真正针对不同 GPU 获得最大加速，还需要进一步的硬件适配和社区参与。

如果这一实现最终如期开放，那么现在社区基于 Full Attention 测得的 H3 本地运行成本，很可能还不是它最终能够达到的效率水平。

会不会推出官方 4-step 或 8-step 版本？

比 Sparse Attention 更直接的问题是：能不能少跑几步？

H3 开放后，第三方 Turbo LoRA 很快就出现了，因此网友直接询问 MiniMax，会不会推出官方 4-step 或 8-step 版本。

Kiro 首先解释，目前发布的 H3 Checkpoint 本身已经包含 CFG Distillation，最终训练阶段也采用了一种特殊策略，因此模型本身已经具有一定低步数推理能力。

但它并不是一个专门针对极低步数蒸馏出来的模型。

在最初的回答中，Kiro表示团队仍在研究进一步的 Step Distillation，但没有正式公布固定的 4/8-step 目标；随后在回答另一名网友关于 Turbo 版本的问题时，团队把路线图说得更具体了一些：MiniMax 正在积极考虑 4-NFE 或 8-NFE 这样的低步数版本。

但团队仍然强调，暂时无法承诺近期提供。默认目标首先是降低推理成本，同时尽量不产生用户能够明显感知的质量下降。

这与社区现在正在进行的尝试形成了有意思的反差。

目前第三方 H3 Turbo LoRA 已经迅速出现，LightX2V 甚至发布了 4-step Turbo LoRA 预览版本。

但社区测试同样发现，激进减少步数之后，人体结构、运动质量甚至音频都可能明显受损。有用户测试 Turbo 版本后直接评价，运动和 Anatomy 出现了明显退化；LightX2V 4-step 版本的早期测试中，也有人遇到音频质量严重下降。

所以 MiniMax 暂时不急着宣布一个“4 步 H3”，背后的问题并不是做不到，而是如何把加速和质量损失之间的账算清楚。

如何生成完美无像素化的片段，现在H3 在这方面有 Bug 吗？

还有Reddit 用户提到，生成的画面中，远处的角色总是会出现像素化和变形，无论是图生视频、文生视频还是参考图生视频都是如此。即便他使用了2K分辨率和25步采样，问题依然存在。他问道，要生成完美无像素化的片段，推荐的步数（Steps）、采样器（Sampler）、调度器（Scheduler）和分辨率（Resolution）是什么？还是说，这纯粹是 Minimax H3 的一个bug？

Kiro 表示，他们团队也观察到了这个问题，尤其是在主体较小或距离较远时尤为明显。这将是团队后续重点改进的问题之一。

根据其内部实验，这个问题不能简单地归因于视觉VAE的压缩比，也不单是某个训练阶段造成的。它是一个复杂的系统级问题，涉及模型和训练流程中的多个环节。团队正在持续调研主要的影响因素，并会在未来的更新中努力加以改善。

MiniMax 正在做一个专门的图像模型吗？

这场 AMA 后半程出现了一个此前没有披露的重要信息——图像生成。

很多开发者发现，H3 本身已经隐约展现出了图像生成和编辑能力。

社区甚至摸索出了一个有些取巧的办法：让 H3 只生成 5 帧视频，再把第一帧拿出来，当作 Text-to-Image 或 Image-to-Image 使用。

因此网友直接问：是否会基于此发布一个类似图生图或文生图模型？

Kiro透露，团队正在从 H3 模型谱系中的共同祖先模型出发，派生一个专门的图像生成模型，目前团队正在完善和优化其训练后阶段。

这个图像模型会沿用 H3 的 VAE Encoder 架构。由于 H3 的 Temporal Encoder 是 Causal 的，团队可以通过 Weight Slicing 获得一个二维 VAE Encoder，与此同时，MiniMax 还计划为图片生成提供一个专门设计的 VAE Decoder。

这其实是一个颇值得注意的方向变化。

H3 今天首先被视作一个视频生成模型，但 MiniMax 显然希望这套多模态生成架构继续向静态图像扩展。

不过，团队也明确解释了一个能力边界：H3 并不是 Streaming Video Generation Model。
因此它无法像一些开发者设想的那样，先生成一张“预览首帧”，用户确认后，再在同一次生成过程中无缝继续扩展成视频。

MiniMax 认为更合理的工作流是：先使用即将到来的图像模型生成首帧，再把这张图片交给 H3 的 I2VA 模式完成视频生成。

Ref2Vid 为什么 比 I2V 更容易糊？

另一个引发热议的问题是Ref2Vid 为什么 比 I2V 更容易糊？

MiniMax给出的回答是，和后训练策略有关。

Reddit 用户 eggplantpot 表示，他大量使用 Reference Workflow 后发现，Ref2Vid 的输出画质明显比 I2V 更容易退化，尤其使用 Driving Video 作为动作参考时，同样的分辨率和步数下，Ref2VA 往往没有 FL2VA 清晰。

这个问题得到不少用户附议。

MiniMax 这次没有把原因简单归结为 Prompt。团队确认：他们已经意识到了这一问题。

MiniMax解释，目前 FL2VA 和 Ref2VA 两个 Checkpoint 在视觉质量上的表现倾向确实存在明显差异，其中一个原因来自二者采用的不同 Post-training Strategy。团队正在主动改善 Ref2VA 的视觉质量。

官方目前给出的一个实际建议是：尽可能提供最高质量的 Reference Input，因为 Ref2VA 对参考条件本身的质量相对敏感。

这条回答很重要，因为此前社区存在两种解释。

一部分用户认为 Ref2VA 效果不好主要是没有严格按照官方 Reference Prompt Guide 编写 Prompt。

但原始提问者强调，他遇到的不是 Prompt Adherence，而是输出本身“发糊”和缺少 Definition。

MiniMax 现在的回答相当于确认：至少其中一部分问题，的确来自模型自身，而不仅仅是“用户不会写 Prompt”。

为什么 H3 特别“听话”？

H3 开放后，另一个被大量用户提到的特点，是它似乎比过去很多开放视频模型更能“听懂人话”。那么，为什么 H3 特别“听话”？在训练方案或模型架构中，哪一方面的贡献对实现这一结果最为关键？

MiniMax给出的答案：不是某一个架构技巧。本质上，最重要的因素是构建足够广泛且多样的数据集和任务，使用通用架构进行训练，并避免选择那些无法有效扩展的架构设计。

有开发者举例称，即使要求模型生成老式卡车、复杂打斗场面，H3 仍然能够比较准确地理解要求，而且不需要反复抽卡。

他因此追问：是不是 H3 使用了某种非常特殊的架构？训练数据到底有多大？

MiniMax没有披露具体数据集规模。

团队给出的解释反而相当朴素：这种能力很难归因于某一个单独的 Architecture Choice 或 Training Technique。

H3 从最开始的设计目标，就是让一个模型能够在尽可能广泛的任务之间泛化，并理解由文本、图像、视频和音频任意组合形成的多模态上下文。

为了实现这一点，MiniMax表示，团队同时在数据构建、任务设计、模型架构和训练策略上投入，而所有选择还有一个共同前提：能够继续 Scale。

另一条回答将这一逻辑概括得更加直接：最重要的是构造足够广泛、多样的数据和任务，用一个 General-purpose Architecture 进行训练，同时避免采用那些无法有效扩展的架构设计。

也就是说，MiniMax并没有把 H3 的 Prompt Adherence 描述成一个神奇模块，而更像是整个预训练任务分布最终涌现出的结果。

在开发 H3 的过程中，哪一个实验最改变团队对“视频模型究竟在学习什么”的认识？

这场 AMA 中最有研究意味的一个问题是：在开发 H3 的过程中，哪一个实验最改变团队对“视频模型究竟在学习什么”的认识？

一名团队成员给出的答案，是一个看起来相当简单的实验。

他们曾经训练一个模型，只完成这样一个任务：给它第一帧和一句 Caption，让它预测最后一帧。

按理说，这只是一个非常有限的时序预测任务。

但团队意外发现，这个模型在没有进行任何专门 Image Editing Post-training 的情况下，在多个图像编辑 Benchmark 上已经表现出了很强的 Zero-shot 能力。

这让研究人员更加相信一件事：由自然语言指令驱动的 Native In-context Learning，本身就可能在不同生成任务之间产生很强的泛化能力，而扩大这类预训练任务的规模，是一个值得继续下注的方向。

这也从另一个角度解释了为什么 H3 开放之后，社区很快开始尝试把它用于视频编辑、图像编辑、Reference Composition，甚至一些 MiniMax 原本没有单独定义出来的工作流。

一个足够通用的多模态生成模型，最终能做什么，可能并不会完全由发布时的功能列表决定。

Context-IR 暂时没有开放，本地用户该怎么办？

H3 完整产品链路还有一个关键组件：H3-Context-IR。

它负责先理解用户提供的复杂文本、图片、视频和音频条件，再把它们整理成 H3 更容易理解的结构化上下文。

这意味着，单纯下载 H3 Base 权重，本地生成时并没有自动获得 MiniMax 在线服务里的完整 Prompt Processing Pipeline。

网友因此询问：即使 Context-IR 本身无法开放，MiniMax 能不能至少发布 Prompt Template 或结构化输入格式，让本地用户尽量接近 API 端的效果？

团队的回答是，目前已经提供了两套官方 Prompt Guide，分别针对 Base 工作流和 Reference 工作流，其中包含 Prompt Expansion 和 Input Template 示例。

除此之外，MiniMax还把两份指南整合成了一个 H3 Prompt Writing Skill，并表示后续还会持续更新。

但团队同时明确：如果用户希望得到完整、原生的 Context-IR 效果，目前推荐的方式依旧是调用官方 API。

这里也反映出了 H3 当前“开放程度”的边界。

模型核心权重已经可以本地部署，2K Regenerate 也明确准备开放，但完整在线产品背后的所有组件，目前并没有同时变成开放实现。

远景人物为什么容易“融化”？

画质仍然是本次 AMA 中最尖锐的问题之一。

有用户表示，无论使用 T2V、I2V 还是 Ref2V，只要人物距离镜头较远，就很容易出现像素化、脸部畸变和高频细节丢失，即使提高到 2K、增加 Steps 也无法彻底解决。

MiniMax承认团队内部已经观察到同样的问题，尤其是在 Small/Distant Subjects 上，并表示这会成为接下来重点改善的问题之一。

但官方否定了一个非常直接的解释——这并不能简单归因于 H3 Visual VAE 的高压缩率，也无法归因于某一个单独的训练阶段。

MiniMax目前将其判断为一个System-level Issue，涉及模型多个组件以及整个训练 Pipeline 之间的相互作用，团队仍在继续隔离主要因素。

MiniMax 以后还开放模型吗？

对于开放策略，社区显然非常敏感。

有人直接问：“Future MiniMax models also be open source?”

团队给出的回复只有一句：

“Yep, Keep open until AGI arrived.”（希望一直开放到 AGI 到来）。

当然，这更像是 AMA 场合下的一句轻松表态，而不是具有约束力的正式产品路线图，但至少体现出 MiniMax 当前希望继续维持开放模型策略的态度。

更值得注意的是 License。

目前 H3 并不是采用传统的 Apache-2.0 或 MIT 许可证，因此有网友直接大写追问：“LICENCE APACHE 2 OR MIT WHEN……”

Ryanlee 给出的最新回应是，随着版权相关文件逐步处理完成，以及法律环境进一步清晰，MiniMax 会考虑采用 Apache-2.0 License。

但对于开放模型社区而言，这仍然是这场 AMA 中相当重要的一次表态。

因为从“开放权重”向标准宽松开源许可证进一步移动，影响的已经不只是普通玩家能不能下载模型，而是企业、开发者能以多低的法律成本进行二次开发和商业部署。

还有一些问题，MiniMax 没有回答

需要特别说一句的是，InfoQ 留意到，Reddit 虽然已经将这场活动标记为“AMA Finished”，但并不意味着所有问题都得到了回复。

例如那条获得大量支持的七连问中，Kiro回答了 H3-Regenerate-2K、Sparse Attention、Low-step Inference 和 High-frequency Detail，Luigi 则回答了 Context-IR，但截至发稿前，关于 FL2VA/Ref2VA 两个 Checkpoint 在推理服务器上究竟如何共享或切换 Backbone，以及官方 Fine-tuning/LoRA Training Script 是否会发布，并没有看到团队给出明确回复。

此外，社区还提出了原生更长视频、Alpha Channel、小显存版本、Mac M3 Ultra 支持、Lip-sync、Diffusion Cache 与 Sigma Schedule、NSFW/Uncensor、官方架构论文和更详细训练数据等问题，目前也没有看到对应的完整官方答案。

这也让这次 AMA 最后留下了一个很有意思的状态。

MiniMax已经明确要把 2K Regenerate 和 Sparse Attention 继续交给社区，低步数模型开始进入路线图，专门的图像模型也已经在开发中；另一边，Context-IR 仍主要留在 API，官方 LoRA 训练体系没有明确时间表，Apache-2.0 也仍停留在“考虑”。

所以，H3 真正值得观察的，可能已经不只是它是不是目前最强的开放视频模型之一。
更值得观察的是：一家中国 AI 公司在开放一个前沿多模态生成模型之后，究竟愿意把整套训练、推理和工具链打开到哪里。

权重发布只是 H3 故事的开始。

而从这场 Reddit AMA 看，社区已经开始追着 MiniMax 问下一步了。

参考链接：
https://www.reddit.com/r/StableDiffusion/comments/1vh9rtw/ama_minimax_h3_team_ask_us_anything_about_our/"