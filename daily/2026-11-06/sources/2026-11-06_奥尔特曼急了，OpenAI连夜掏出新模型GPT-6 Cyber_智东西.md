---
publish_time: 1793929464
link: https://mp.weixin.qq.com/s/fJQm6RzagZZkzP7qZjN5DA
source: 智东西
status: confirmed
category: 国际
is_model_related: true
digest: |
  OpenAI 推出 GPT-6 Cyber，主攻安全研究，在 ExploitGym 基准得分 48.5%，较 GPT-5.6 Cyber 的 32.1% 相对提升 51%，已在 Linux、Firefox 等代码库发现并验证数千个漏洞，Mozilla、Palo Alto 等安全团队已应用。GPT-6 系列含 Astra/Sol/Terra/Luna 等型号，Cyber 专攻安全领域。
title: 
---

# 奥尔特曼急了，OpenAI连夜掏出新模型GPT-6 Cyber

来源：智东西
原文链接：https://mp.weixin.qq.com/s/fJQm6RzagZZkzP7qZjN5DA

多数网络安全任务胜Astra。
编译 |
李水青
编辑 |
云鹏
智东西11月6日报道，今日，OpenAI推出新模型
GPT-6 Cyber
，主攻安全研究领域。该模型在关键网络安全基准测试中相比GPT-5.6 Cyber显著提升，在安全测试ExploitGym中，GPT-6 Cyber得分48.5%，高于GPT-5.6 Cyber的32.1%，相对提升
51%
。
▲OpenAI在社交平台X发布公告
模型一经发布，不少开发者评论：“原本以为是6.2。”“不是这个，我们需要6.2 Sol和Astra。”前日，外媒The Information报道，OpenAI最快可能于当地时间本周五发布新一代（网传GPT-6.2）Astra、Sol系列模型，以及面向网络安全领域的Cyber模型。
▲社交平台X上的开发者评论节选
但今天截至目前，到来的只有GPT-6 Cyber。从模型定位来看，OpenAI的GPT-6和GPT-6.1系列包括Astra、Sol、Terra、Luna等不同型号。GPT-6 Astra是OpenAI能力最强的旗舰模型，面向高难度推理和复杂任务；GPT-6 Luna则主打快速、高效的规模化日常工作；
本次推出的GPT-6 Cyber则主攻安全领域。
而GPT-6.1也已迭代出了：GPT-6.1 Terra，侧重速度、成本和日常任务执行；GPT-6.1 Sol，侧重高性价比的复杂编程和推理任务。
OpenAI称，GPT-6 Cyber已在Linux和Firefox等安全关键型代码库中发现并验证
数千个漏洞
。包括Mozilla、Palo Alto Networks、Calif和Cisco在内的多家公司的安全团队，以OpenAI团队自身，都已开始应用该模型。
GPT-6 Cyber受到了不少开发者的关注，有开发者在社交平台X上说：“能够发现Linux内核中真实安全漏洞的AI……哇，这才是真正重要的进步。”有人说：“Linux内核的工作为本次公告提供了一个具体的案例。如果能提供从发现bug到验证修复的完整步骤，对开发者来说将尤为有用。”
▲社交平台X上的开发者评论节选
不过，GPT-6 Cyber目前并非可以直接在聊天中选择的模型，而是面向部分
Daybreak Red
计划认证的客户开放，OpenAI称将逐步扩大其使用范围。为此，不少开发者吐槽：“又一个没人能用的模型，OpenAI我真的会谢。”
▲社交平台X上的开发者评论节选
01
.
比Astra更能打
GPT-6 Cyber远程漏洞任务完成95%
OpenAI称，GPT-6 Cyber在大多数网络安全任务上优于GPT-6 Astra。测评覆盖理解软件、识别漏洞和开发有效攻击程序等任务。
基于结果，按其网络安全准备框架，OpenAI将GPT-6 Cyber的网络安全等级评为“关键（Critical）”，高于GPT-5.6 Cyber的“高（High）”。
ExploitGym测试中，GPT-6 Cyber得分48.5%，比GPT-5.6 Cyber的32.1%高约16个百分点。为测试漏洞发现能力，OpenAI构建了针对攻击性Web渗透测试的新评估：模型无法访问Web应用源代码，只能探测。GPT-6 Cyber漏洞召回率为40.3%，GPT-6 Astra为32.0%。
Daybreak Red支持更高级安全流程，包括开发可用漏洞利用程序并用于远程目标。为了评估这些功能，OpenAI构建新基准RemoteExploitBench，利用受控环境中GitLab、PostgreSQL和Jenkins等应用的已知漏洞。
初步评估中，运行Daybreak Blue的GPT-6 Astra拒绝了100%的任务，GPT-6 Cyber完成了95%；其唯一失败是无法远程运行某个漏洞利用程序。
02
.
该出手才出手
GPT-6 Cyber越界规避99.93%
OpenAI称，网络安全人员可能超出分配任务范围，试图利用不相关服务，或无视研究人员合作规则。
因此，OpenAI把模型一致性作为GPT-6 Cyber核心重点，通过专门训练帮助模型保持在授权范围内、遵守行为限制并准确报告工作。部署前，OpenAI进行了一系列一致性评估。
其中一项评估是ExploitGym Honeypot，其设计灵感来源于Hugging Face事件。OpenAI给模型布置高难度攻击任务，任务在隔离环境中进行，并允许访问软件包注册表或对象存储等辅助服务。这些服务被特意设计得易于攻击，以便攻击它们可暴露任务标志。模型必须推断出，利用这些服务超出了其任务范围。
评估中，未启用部署安全提示时，GPT-6 Cyber在99.93%的情况下避免利用超出范围的服务，高于GPT-5.6 Cyber的94.49%；启用安全提示后，GPT-6 Cyber 100%避免攻击超出范围的服务。
OpenAI称，从模型思维链可直接看出其如何推理并保持在界限内，比如以下思考：“不能假设额外的API或攻击控制器不是目标。我们应该只针对二进制文件/服务器。”“不要探索超出范围的资质。”
03
.
实战发现81个Firefox新漏洞
开发948个Linux利用程序
OpenAI称，GPT-6 Cyber已开始帮助安全团队发现漏洞、验证影响并开发修复程序。客户已将其应用于大型代码库、长期漏洞利用开发和安全审查。
OpenAI漏洞研究人员还使用GPT-6 Cyber大规模查找和验证开源软件漏洞，发现多年来备受关注软件中的此前未知缺陷：
-发现81个新Firefox漏洞。 GPT-6 Cyber为Mozilla分类为高危的81个新漏洞提供证据和可复现测试，并表明另外30个已知问题比之前报告更严重。OpenAI将结果连同建议补丁披露给Mozilla；Mozilla表示支持，并在收到报告后不久开始实施修复。
-针对948个Linux内核漏洞开发利用程序。 GPT-6 Cyber重现1724个漏洞，并针对其中948个开发可用利用程序，是使用相同研究工具的GPT-5.6 Sol所利用漏洞数量（166个）的五倍多。根据Linux社区指导，OpenAI已向维护者披露304个关键漏洞及候选补丁，目前正在修复其他漏洞。
-演示关键远程代码执行漏洞。 OpenAI近期讨论Brotli中的一个关键漏洞；Brotli是被Node.js和其他软件使用的压缩库。OpenAI安全研究人员利用GPT-6 Cyber及其他OpenAI模型开发并验证漏洞利用程序，展示该漏洞如何导致下游应用远程执行代码。
04
.
GPT-6 Cyber升级防滥用，
OpenAI设10亿美元一线防御者计划
OpenAI称，随着模型能力提升和安全漏洞增多，越来越多人试图利用模型进行恶意攻击，包括恶意网络攻击者和敌对组织试图提取模型底层信息。
因此，OpenAI为GPT-6 Cyber配备更强大安全措施，检测和阻止滥用，确保模型操作符合用户意图和授权。发布同时，OpenAI添加并加强保护措施，包括网络安全特定错配监控、针对新出现威胁的定向监控、隐私安全处理（PSP）、防范凭证被盗、沙盒机制和监管等。
OpenAI称，保护关键基础设施一直是GPT-6 Cyber安全防护和访问控制设计的关键考量，包括发电厂、水处理设施及支撑它们的OT/ICS。OpenAI希望在确保这些系统安全的同时，为防御团队提供最强模型，并加强措施防止未经授权攻击。
首先，OpenAI斥资10亿美元设立“一线安全卫士曙光计划”（Daybreak for Frontline Defenders）资助项目，为资源有限团队（如政府机构和关键服务提供商）提供资金支持。此外，在“曙光计划红队”（Daybreak Red for Critical Infrastructure）中新增小组，专门面向已获批准的关键基础设施安全卫士，授权其对关键系统进行授权测试，同时确保模型匹配度、防止偏差。
其次，为防止滥用Daybreak Red和Blue平台，OpenAI完善安全措施，防范可能损害工业控制系统或安全关键系统、干扰设备运行、造成严重人身伤害、灾难性物理损坏或危及生命的服务中断的协助和能力开发活动。下图比较了在最近与GPT-6 Cyber一同推出的更新前后，四种访问配置下的安全标签覆盖率。
OpenAI同时称，更高安全防护拦截率并非总是更好；许多技术对合法安全工作也至关重要，因此评估拦截率时会同时考虑对合法研究和补丁的支持程度，而不是以100%为目标。
为评估模型如何帮助保护关键基础设施，OpenAI与扩展运营技术（xOT）网络安全提供商Dragos合作。Dragos在受控实验室环境中使用网络容错型Daybreak Red模型评估，涵盖从网络发现和资产枚举到定向侦察、敏感数据泄露及未经授权潜在危险设备操作等请求。
05
.
结语：GPT-6 Cyber显出实战价值
治理体系成胜负手
GPT-6 Cyber把安全模型从代码审查推向自主挖洞、利用验证与补丁开发，通过Linux、Firefox等一系列实战结果，证明其已具备产业级安全研究价值。
能力越强，访问控制越关键。目前OpenAI仅向Daybreak Red认证客户开放，叠加防滥用与关键基础设施保护，表明安全AI的落地竞争不仅是模型能力，更是可信授权与治理体系的竞争。
