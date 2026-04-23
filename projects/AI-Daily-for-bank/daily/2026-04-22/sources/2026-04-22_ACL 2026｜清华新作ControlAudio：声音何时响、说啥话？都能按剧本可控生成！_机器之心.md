# ACL 2026｜清华新作ControlAudio：声音何时响、说啥话？都能按剧本可控生成！

> 原文链接：https://mp.weixin.qq.com/s/n8sjvwE5TOAVIa8d9A1-sQ
> 公众号：机器之心

---

本文第一作者是江宇轩，清华大学博士生，研究方向为生成模型、文生音频和多模态学习，指导老师为朱军教授与窦维蓓教授。

文本到音频（Text-to-Audio, TTA）生成技术近年来取得了显著进展，从早期的简单声效合成逐步发展到基于扩散模型的高保真音频生成，能够较好地还原复杂的自然语言描述，为影视配音、游戏音效及多媒体内容创作提供了重要的技术支撑。

然而，现有 TTA 技术在精细化控制方面仍面临挑战：

一方面，模型难以实现对声音事件发生时间的精确控制；另一方面，生成的语音内容往往不够清晰，缺乏可理解性。

针对这一问题，

清华大学研究团队提出了 ControlAudio，

一种基于渐进式扩散建模的文生音频方法。该方法通过系统性的数据构建流程与渐进式建模策略，在统一框架下实现了对时间结构与语音内容的联合建模。

目前，该工作已被 ACL 2026 Main Conference 接收，并拟推荐为口头报告。

论文地址：https://arxiv.org/abs/2510.08878

效果试听：https://control-audio.github.io/Control-Audio

研究背景

文生音频系统旨在合成与自然语言描述一致的音频内容（如「鸟儿正在鸣叫」），在高保真生成方面已取得显著进展，但在精细化控制维度仍存在明显不足：

精确的时间控制：

如「鸟儿在 2 至 5 秒间鸣叫」；

可理解语音生成：

如「鸟儿在鸣叫，同时一名男子在说：

『

今天天气真好』」。

然而，由于带有精确时间标注和语音转录的信息难以大规模获取，可控 TTA 系统在规模化训练与生成能力上仍受到限制。同时，现有方法通常仅关注单一控制维度，尚未在统一框架下同时实现时间控制与可理解语音生成。

核心方法

本文提出 ControlAudio，一种渐进式扩散建模方法，通过逐步建模文本、时间与音素等不同粒度的条件信息，实现可控的 TTA 生成。整体方法包含三个核心部分：

数据构造与表征：

通过人工标注与仿真生成相结合的方式构建多层级数据，并设计结构化提示词（Structured Prompt），使预训练文本编码器能够统一编码文本、时间与音素信息；

模型训练：

采用渐进式训练策略。首先在大规模文本 - 音频数据上预训练扩散模型，随后逐步引入时间与语音内容信息进行建模，使模型逐步具备更细粒度的控制能力；

引导采样：

针对扩散模型「由粗到细」的生成特性，设计渐进式引导采样策略，在推理过程中先生成整体时间结构，再逐步细化语音内容。

渐进式扩散建模

ControlAudio 将多条件建模拆解为一个由粗到细的渐进过程。

在训练阶段，模型分三步逐步引入控制信号：首先在大规模文本 - 音频数据上预训练，学习基础的文本到音频生成能力；随后在包含时间标注的数据上进行微调，使模型能够控制声音事件的时间结构；最后进一步引入音素信息进行联合训练，实现对语音内容的建模。

在这一过程中，通过使用 Text、Text + Timing 以及 Text + Timing + Phoneme 等不同条件组合，逐步提升模型对细粒度控制信号的建模能力。

在推理阶段，方法提出了

渐进式引导采样策略：

在扩散早期，仅使用文本与时间条件进行引导，先生成整体的时间结构；在后期阶段，再引入音素信息并提高引导强度，用于细化语音内容。该设计与扩散模型由粗到细的生成过程一致，从而在时间对齐与语音清晰度上取得更好的效果。

数据集构建

针对可控 TTA 所需的时间标注与语音内容数据稀缺问题，ControlAudio 构建了一个

多来源的数据体系，将真实标注与仿真数据相结合。

首先，在真实数据方面，基于具有时间标注的 AudioSet-SL，筛选包含语音的片段，并通过分离与转写流程，获得带有时间戳与语音内容的信息，将原始的 ⟨text, audio⟩ 扩展为 ⟨text, timing, phoneme, audio⟩ 的细粒度数据。在此基础上，进一步构建大规模仿真数据。

方法从真实数据中统计语音活动分布，并据此合成单人或多人语音片段，按照合理的时间结构进行排列，并与背景音频混合生成复杂音频场景。该流程额外扩展了

超过 17 万条训练样本，

提升了数据规模与多样性。

此外，在结构化提示词的构建过程中，ControlAudio 引入

基于链式推理（Chain-of-Thought, CoT）的自动生成流程，

将自然语言描述解析为「事件 — 时间 — 语音内容」的结构化表示，为模型提供更加清晰的条件输入。

实验结果

为了验证 ControlAudio 的有效性，团队首先在时间可控音频生成的 AudioCondition 测试集上进行评估。相比现有方法，

在事件时间对齐指标上取得显著提升，同时在 FAD、CLAP 等音频质量指标上保持竞争力甚至更优表现。

在包含语音生成的评测任务中，ControlAudio 同样展现出更强的语音可理解性与整体音频质量，验证了其

在统一框架下同时建模时间结构与语音内容的能力。

在文生音频任务中，ControlAudio 同样取得了与当前主流方法相当甚至更优的生成质量，在引入时间与语音控制能力的同时，并未降低基础的文本到音频生成性能。

总结与展望

ControlAudio 从数据构建、模型训练到采样策略三个层面系统性地解决了文生音频中的精细化控制问题，在统一框架下实现了文本、时间与语音内容的协同建模，并在多项任务上取得了优于现有方法的表现。

相比以往仅关注单一控制维度的工作，ControlAudio 展现了

更强的通用性与扩展潜力。

随着音频与多模态生成模型的发展，越来越多系统开始探索 Speech、Audio、Music 的统一建模范式。研究团队希望

ControlAudio 所提出的「多粒度条件统一建模 + 渐进式生成」思路，能够为通用音频生成提供一种可扩展的技术路径，推动模型从单一任务走向更复杂、多维度可控的内容生成。

样本展示

Text Prompt:

Music plays, followed by mechanisms, typing, beeps, and an alarm.

Timing Prompt:

Music : 0.00s - 10.00s; Beeps : 1.00s - 1.20s 3.00s - 3.20s 4.90s - 5.10s 6.90s - 7.10s; Typing : 1.20s - 7.80s; Alarm : 7.85s - 8.50s.

Structured prompt:

Music plays, followed by mechanisms, typing, beeps, and an alarm. @{Music. & <0.00,10.00>}@{Beeps. & <1.00,1.20><3.00,3.20><4.90,5.10><6.90,7.10>}@{Typing. & <1.20,7.80>}@{Alarm. & <7.85,8.50>}

Text Prompt:

A man speaking over an intercom as a crowd of people talk followed by a dog barking.

Content Prompt:

and contain them until that person can be taken into custody effectively and safely on the part of the other team of police sheriffs.

Structured prompt:

A man speaking over an intercom as a crowd of people talk followed by a dog barking. @{Crowd talking ambience & <0.00,10.00>}@{Male speech, man speaking & <0.46,5.14>"And contain them until that person can be taken into custody effectively and safely."<5.64,8.22>"On the part of the other team of police sheriffs."}@{Dog barking & <9.26,9.46>}

Text Prompt:

Females voice narrating a scene as music is playing and rain drops are falling.

Content Prompt:

Daniel came out of the airport. He raised one arm to hail a taxi.

Structured prompt:

Females voice narrating a scene as music is playing and rain drops are falling. @{Music & <0.00,10.00>}@{Female speech, woman narrating & <2.62,4.65>"Daniel came out of the airport."<5.37,8.26>"He raised one arm to hail a taxi."}@{Rain falling & <8.26,10.00>}

Text Prompt:

Splashing water followed by a girl speaking then scraping and spitting.

Content Prompt:

This is the last time you did that first thing. Same thing.

Structured prompt:

Splashing water followed by a girl speaking then scraping and spitting. @{Splashing water & <0.00,1.38>}@{Female speech, girl speaking & <1.57,4.52>"This is the last time you did that first thing. Same thing."}@{Scraping & <4.66,6.81><7.10,8.00>}@{Spitting & <8.10,8.48>}

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

insertaudio (166:40)
[Play Audio / Click to Listen]

insertaudio (166:40)
[Play Audio / Click to Listen]

insertaudio (166:40)
[Play Audio / Click to Listen]

insertaudio (166:40)
[Play Audio / Click to Listen]