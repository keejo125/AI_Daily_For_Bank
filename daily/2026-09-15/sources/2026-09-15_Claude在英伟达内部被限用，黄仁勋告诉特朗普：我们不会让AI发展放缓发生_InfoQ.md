---
publish_time: 1789459301
link: https://www.infoq.cn/article/g9eJhszhJa3JcZsgZwmj
source: InfoQ
status: confirmed
category: 其他
is_model_related: false
digest: |
  据 The Information，Palantir、英伟达、Booz Allen 等科技与防务公司可能限制甚至停用先进 AI 模型，除非 Anthropic、OpenAI 保证不不当使用其知识产权。英伟达将 Claude 限制在低敏感任务、内部依赖自家 Nemotron；Booz Allen 禁止在涉专有信息的网安工作用商业 Claude；微软借隔离云与自研产品争取客户。Anthropic 的 30 天日志保留等数据条款正遭遇企业客户明显阻力，反映企业 AI 采购中的知识产权与数据主权顾虑。
---

# Claude在英伟达内部被限用，黄仁勋告诉特朗普：我们不会让AI发展放缓发生

> 原文链接：https://www.infoq.cn/article/g9eJhszhJa3JcZsgZwmj
> 来源：InfoQ

根据The Information报道，包括 Palantir Technologies、英伟达和 Booz Allen Hamilton 在内的大型科技公司，可能会限制甚至停止使用先进人工智能模型，除非 Anthropic 和 OpenAI 能够保证不会不当使用这些公司的知识产权。

与此同时，微软正利用企业客户的这类担忧，通过推介隔离式云环境以及自有人工智能产品来争取客户。

“霸道”的数据条款

今年6月，Anthropic 修改了 Fable 模型的相关政策，赋予公司将使用日志保留30天的权利，以防范所谓“复杂且新型的攻击”。此后，Anthropic 遭到了客户的抵制。报道称，OpenAI 也面临类似审查。此前有指控称，OpenAI 可能曾使用用户数据训练模型，以帮助解决一道数学问题。

Palantir、Nvidia、Booz Allen、Anthropic 和 OpenAI 均未立即作出回应。

Anthropic数据政策

报道称，一名了解相关讨论的知情人士表示，在允许 Anthropic 的模型通过 Palantir 软件提供给客户之前，Palantir 一直要求 Anthropic 提供不可撤销的“零数据保留（Zero Data Retention，ZDR）”保证；英伟达则将 Anthropic 模型的使用范围限制在敏感程度较低的任务中，而在内部工作中则依赖自家的 Nemotron 模型；与此同时，Booz Allen 已禁止员工在涉及公司专有信息的网络安全工作中使用 Anthropic 的商业模型。

两家 AI 实验室都表示，除非企业客户主动选择加入，否则默认情况下不会使用客户数据训练模型。不过，两家公司都会收集匿名化的元数据，用于改进产品。

特别地，Anthropic围绕Claude高能力模型的数据保留政策，正在面临越来越明显的企业客户阻力。

根据Anthropic隐私中心公布的规则，部分“受管辖模型”默认要求至少保留30天的Prompt和输出内容。即便客户此前已经与Anthropic签署ZDR协议，只要使用这类模型，同样会受到新的数据保留要求影响。

Anthropic在API文档中进一步明确，Fable 5、Fable 5.1、Mythos 5和Mythos 5.1默认都要求保留30天数据。除非Anthropic明确授权，这些模型不能使用ZDR。如果一个组织已经开启ZDR，但没有为上述模型单独启用数据保留，请求甚至会直接返回错误。也就是说，针对这批高能力模型，Anthropic实际上把“安全监控所需的数据留存”置于原有ZDR安排之上。

微软在6月将Claude Fable 5接入Microsoft 365 Copilot时，就专门提醒企业管理员，Fable 5受到Anthropic数据保留政策约束，组织应在启用前把这一因素纳入内部合规和数据治理决策。出于这一原因，Fable 5在企业环境中并不是默认开启，而需要管理员主动启用。

GitHub Copilot企业管理员同样需要主动开启Fable 5。GitHub在相关说明中明确指出，Anthropic会保留用户输入的Prompt和模型输出最多30天，用于安全分类和滥用检测；相比之下，其他Claude模型仍然可以维持ZDR。

这说明，在同一个企业AI产品体系中，不同Claude模型实际上可能对应完全不同的数据治理规则。对于一般开发任务，这种差异影响有限；但一旦涉及源代码、客户信息、内部战略文档、法律材料或者其他专有数据，是否保留Prompt和输出，就会直接进入企业法务、安全和合规团队的审查范围。

事实上，The Information早在6月就曾报道，微软一度没有立即向内部员工开放Fable，原因之一正是其法务团队仍在评估Anthropic的数据保留政策是否符合微软自身的数据保护要求。

与此同时，一些AI法律服务公司也对类似政策表达担忧，因为如果律师将客户材料输入模型，而这些数据又被模型供应商保留，可能触及律师—客户保密特权等更敏感的法律问题。

从企业客户的角度看，只要数据离开自己的基础设施，并在第三方系统中保留一定时间，本身就意味着额外的合规、审计和泄露风险。Anthropic随后明显开始调整这一矛盾，并在9月推出Enterprise Frontier Safeguards（EFS）。

EFS的核心思路是，安全监控机制继续运行，但相关数据不再由Anthropic集中持有，而是保存在客户自己的云基础设施中。这样一来，Anthropic仍然可以提供针对高风险模型的安全能力，同时又能让企业获得接近ZDR的控制效果。

Anthropic表示，EFS并不是单独为某一家企业定制，而是与超过100家来自金融、医疗、制造、电信、法律、零售和公共部门的客户共同设计。这也从侧面说明，数据保留问题已经不是少数客户的特殊诉求，而正在成为前沿模型进入大型企业的普遍门槛。

但目前看，这一策略依然不够。

黄仁勋告诉特朗普：不会让AI放缓发生

Anthropic CEO Dario Amodei 上周呼吁人工智能公司放缓前沿模型的开发速度。他警告称，AI 能力的发展速度已经超过研究人员理解或控制这些能力的速度。OpenAI CEO Sam Altman 和马斯克随后很快对此立场表示支持。

当地时间周一，在洛杉矶举行的 All-In Summit 上，Nvidia CEO 黄仁勋公开反对放缓前沿 AI 能力发展的主张。就在他讨论这一话题时，美国总统 Donald Trump 突然来电，并在电话中明确表示，美国不会允许 AI 产业因相关担忧而停滞。

当时，黄仁勋正在与播客《All-In》的几位嘉宾进行现场交流，包括科技投资人 Chamath Palihapitiya、Jason Calacanis，以及 David Friedberg 和白宫 AI 与加密事务负责人 David Sacks。

接到特朗普电话后，黄仁勋直接将通话接入现场扩音系统。

“我现在正在台上，和几位好朋友在一起。”黄仁勋对特朗普表示。在工作人员帮助黄仁勋将电话声音接入现场时，特朗普还开玩笑称：“人生有趣的地方就在这儿。Jensen 能设计出世界上最复杂的计算机芯片，但他却搞不明白怎么把你切到免提。”

这通电话出现前，黄仁勋几人正在讨论 Anthropic CEO Dario Amodei 最近提出的观点。Amodei 呼吁 AI 公司放慢前沿模型能力提升的速度，认为 AI 能力正在以超过研究人员理解和控制能力的速度发展，这一观点随后获得马斯克和 Altman 的公开支持。

特朗普在电话中对此表示，他们这么做正好中了很多不希望看到这件事发生的人的下怀。“我们不会允许这种事情发生。这就是一个骗局。”

黄仁勋随即回应：“您说得对，先生。我们不会让这种事情发生。”现场随后响起掌声。

特朗普及其部分盟友此前一直对美国国内反对数据中心和 AI 基础设施扩张的声音持批评态度。包括 Y Combinator CEO Garry Tan 在内的一些科技行业人士认为，围绕数据中心建设的反对情绪可能削弱美国在 AI 基础设施领域的扩张速度和全球竞争力。

不过，美国公众对于数据中心扩张的担忧更多集中在能源、环境和生活成本等现实问题上。

Gallup 最新民调显示，约七成美国受访者反对在自己居住的地区建设数据中心。超过一半受访者担心数据中心会消耗大量环境资源，约20%的受访者则担心其推高生活成本并影响当地生活质量。

特朗普在电话中也承认，AI 基础设施扩张需要兼顾相关风险。“我们确实需要稍微谨慎一点。我们要做这些事情，也必须以审慎的方式推进，但这并不意味着我们要叫停整个行业。”特朗普对黄仁勋表示。

他随后补充称：“所以我完全支持你。我之前甚至都不知道你在这件事上的立场，我只是希望你的想法和我一样。我们会保持领先。”

这场临时加入峰会现场的总统电话，也使近期围绕“是否应该主动放慢前沿 AI 发展”的争论进一步公开化。

一方面，Anthropic、OpenAI 等前沿模型公司越来越频繁地讨论超级智能、安全和失控风险，部分行业领袖开始主张降低模型能力扩张速度；另一方面，以英伟达为代表的 AI 基础设施企业以及美国政府内部部分人士则担心，主动减速可能削弱美国在全球 AI 竞争中的领先优势。

黄仁勋此次表态显示，在 AI 安全讨论持续升温的同时，美国科技行业内部对于“减速”还是“继续加速”的分歧正在进一步扩大。

参考链接：
https://www.theinformation.com/articles/anthropic-data-fears-prompt-nvidia-palantir-booz-allen-restrict-model-use?utm_campaign=Editorial&utm_content=Nebius%2CTITV%2Ctitv_gxijn&utm_medium=organic_social&utm_source=facebook%2Cthreads%2Ctwitter"
https://www.reuters.com/business/palantir-nvidia-curb-ai-model-use-over-data-fears-information-reports-2026-09-14/?utm_source=chatgpt.com"
https://techcrunch.com/2026/09/14/nvidia-ceo-jensen-huang-tells-trump-were-not-going-to-let-an-ai-slowdown-happen/"