# 智能研发业界对标调研报告

**报告周期：2026年4月1日 — 4月30日**
**版本：V2（2026年5月2日修订）**

---

## 第一章 概述

2026年4月，智能研发领域从"单点工具迭代"进入"范式重构"阶段。本月最核心的变化不是某个模型分数又涨了几分，而是三条路径同时发生了**模式级转变**：编码环节从"AI辅助人类"转向"Agent自主完成全流程"，算力基础设施从"英伟达依赖"转向"国产全栈替代"，金融行业从"概念验证"转向"生产级大模型私有化部署"。

### 一、国际动态

**岗位智能体方面**，本月最大的模式变化是AI编程从辅助工具跃迁为全流程自主执行者。谷歌宣布75%代码由AI生成并全面转向智能体工作流，Anthropic的Claude Mythos核心架构开源将Agent从"对话模式"推入"自主执行模式"。Parasoft发布的AI智能体实现单元测试全流程无人化，Meta的Just-in-Time测试将测试环节左移至代码评审阶段——测试不再是独立环节，而是融入编码流程。3月31日泄露的Claude Code完整源码（51.2万行TypeScript代码，1906个文件，44个功能标志，20余个未发布特性）引发了社区对其工程架构的广泛分析，成为了解顶级AI Agent内部设计的最佳参考案例。

**支撑能力方面**，Agent记忆系统出现方向性突破。Codex发布终身记忆功能，AI Agent可跨会话持久化项目上下文和历史决策，从"每次从零开始"转变为"越用越懂业务"。Claude Code发布上下文预加载功能，项目级上下文自动缓存，减少70%重复查询。GitLab发布AI Pipeline智能体，CI/CD从人工触发转向Agent自主完成构建-测试-部署全流程。

**底座能力方面**，谷歌发布第八代TPU，采用训推双芯片架构，专为Agent时代优化推理性能，标志着算力架构从"训练优先"转向"训推并重"。OpenAI发布GPT-6 Symphony，200万Token上下文窗口将长文本处理能力推至新量级，使单次会话可处理整个代码仓库。OpenAI与微软正式结束七年独家合作，向所有云厂商开放，行业格局从"寡头绑定"转向"开放竞争"。

### 二、国内动态

**岗位智能体方面**，国内厂商在Agent编码的工程化落地速度上全球领先。Kimi K2.6实现300个Agent并行协作、连续13小时长程自主编码，将"多Agent协同"从实验室推入生产环境。灵码企业版支持Kimi K2.6长程编码，验证了银行级大代码库场景下的可行性。通义灵码推出专家模式，允许将团队编码规范封装为专属智能体，实现了编码知识从"人传人"到"Agent固化"的模式转变。

**支撑能力方面**，国内在Agent生态基础设施上的投入呈现爆发态势。腾讯云开源AI Agent底座（与OpenAI、Manus同架构），为Agent开发提供标准化基础设施。openJiuwen社区发布Team Skills与Coordination Engineering框架，开创多智能体团队级技能共享新范式。上海交通大学开源SkVM技能虚拟机，实现Skill"一次编写、处处执行"，解决Agent技能跨平台可移植性问题。M-Flow记忆引擎和NUS&NTU的Pask框架分别在记忆持久化和流式意图检测上实现了架构级创新。工信部与国家数据局启动2026"模数共振"行动，提出打造智能体工厂，标志着国家层面对Agent生态的系统性布局。

**底座能力方面**，本月国产算力实现三个里程碑式突破：DeepSeek-V4全面适配华为昇腾950PR，完成从CUDA到CANN的全栈迁移；美团LongCat-2.0用5-6万张国产算力卡完成万亿参数模型训练，是迄今最大规模国产算力训练实践；国产E级超算"灵晟"点亮，纯国产CPU架构、无GPU加速卡，持续性能超2EFlops。这三件事共同证明国产算力已具备支撑前沿大模型训练与推理的能力，对工行等有国产化替代需求的金融机构具有战略意义。大模型方面，DeepSeek-V4以1.6万亿参数开源、百万Token上下文标配，GPT-5.5发布后迅速登顶全榜。

### 三、同业动态

**岗位智能体方面**，中国银联于4月24日依托昇腾算力率先完成DeepSeek-V4私有化部署，是金融行业首个公开确认的DeepSeek-V4私有化部署案例，标志着金融大模型从"公有云调用"进入"自主可控私有化"阶段。招商银行2025年报披露日均Token吞吐量达260亿（同比增长10.1倍），研发人员超1.1万人，AI渗透已具规模。

**支撑能力方面**，工商银行参与八大机构（工行、农行、中行、建行、邮储等）协同攻关数据分类分级大模型，推动银行业数据治理标准化。南京银行AI+产业大脑融入对公业务全流程，宁波银行探索AI四类场景应用，区域性银行在AI应用上的追赶态势明显。

**底座能力方面**，六大行科技投入合计超1300亿元，AI成为转型核心引擎。农业银行发布绿色金融AI智能体，实现绿色项目数据自动加工、交叉验证和尽调报告智能生成。2026年金融AI智能体开发聚焦风控、投研、合规三大核心场景。国务院4月21日政策首次明确提出"支持采购大模型、智能体服务"，为银行AI投入提供了政策依据。

---

## 第二章 详细内容

### 2.1 维度一：岗位智能体建设

#### 2.1.1 需求阶段

**【国际】AI赋能需求全流程**

4月21日，社区报道AI赋能需求全流程实践，涵盖PRD自动生成、内容补全、规范检查、冲突检测、遗漏检测等环节。4月26日，AI Agents PRD→任务拆解五阶段流程发布，覆盖需求澄清→PRD生成→技术评审→任务拆解→开发执行全链路，另有AI生成PRD分步引导方法，强调AI初稿+人工精修的人机协作模式。

> **对工行影响：** 可引入AI需求评审工具，PRD编写时间预计减少50%，需求缺陷检出率提升40%，尤其适合标准化的银行产品需求场景。

**【国内】AI需求评审实践**

4月23日，开发者分享intv_ai_mk11实战经验，AI完成产品需求评审并输出质疑点，辅助产品经理识别需求漏洞和逻辑矛盾。

> **对工行影响：** 银行产品需求文档量大且标准化程度高，AI辅助评审可有效减少需求返工，建议在关键业务系统需求评审中试点。

#### 2.1.2 设计阶段

**【国际】AI架构评审进入实用阶段**

4月28日，华为云发布架构评审智能体，支持云原生、微服务、智能体协同架构等多场景评审，评审效率提升70%，缺陷检出率提升4倍。谷歌第八代TPU配套发布智能体架构设计指南，推动架构设计从模块拆分转向Agent交互协议与任务编排设计。

**【国内】数据模型与接口设计AI化**

4月25日，腾讯云发布数据模型智能设计工具，可从需求文档自动提取实体关系，生成ER图与DDL，数据模型设计周期从天级压缩至小时级。4月23日，阿里云发布API网关AI增强版，支持智能接口路由与自适应限流，接口设计效率提升50%以上。

> **对工行影响：** 银行核心系统架构评审复杂度高、人工成本大，AI辅助评审可将评审周期缩短70%；数据模型自动化设计工具有望降低数据治理人力投入。

#### 2.1.3 编码阶段

**【国际·变革性】Claude Mythos核心架构开源：从"说到"到"动手"**

4月21日，Anthropic开源Claude Mythos核心架构，Agent从对话辅助模式转向自主执行模式，可独立完成复杂编码任务。Claude Code源码泄露事件（3月31日，51.2万行代码、1906个文件因构建配置失误意外公开）引发了社区对Claude Code工程架构的深度分析，暴露了其完整的MCP集成、Hooks自动化、子代理、Skills系统等设计，为行业理解顶级AI Agent内部架构提供了前所未有的参考。

**【国际·变革性】谷歌75%代码AI生成，全面转向智能体工作流**

4月26日，谷歌宣布内部75%代码由AI生成，全面转向智能体工作流，从代码提交到部署全链路自动化，交付周期缩短60%。这标志着头部科技公司已从"AI辅助编码"进入"Agent主导交付"的新阶段。同期GitLab发布AI Pipeline智能体，可自主完成代码构建-测试-部署全流程，部署频率从每周2次提升至每天10次。

**【国际·持续性】Claude Opus 4.7与GPT-5.5：编程能力持续攀升**

4月，Claude Opus 4.7编程能力较前代提升11%，SWE-bench达87.6%，支持2K像素UI设计稿直接转代码。GPT-5.5在多项基准测试中全面登顶，GPT-5.5 Pro视觉智商达145，Token消耗减少45.6%。GPT-6 Symphony（4月17日）支持200万Token上下文，LongBench比GPT-5提升40%。

**【国内·变革性】Kimi K2.6：300 Agent并行，13小时长程自主编码**

4月24日，月之暗面发布Kimi K2.6，支持300个Agent并行协作，连续运行13小时完成复杂编码任务无需人工干预，复杂任务完成率88%。灵码企业版同步接入，验证了长程自主编码在工业场景的可行性。这标志着AI编码从"单次对话辅助"进入"多Agent长时间自主执行"的新模式。

**【国内·变革性】DeepSeek-V4开源，百万上下文成为标配**

4月24日，DeepSeek发布V4模型，总参数1.6万亿（MoE架构），百万Token上下文标配，百万上下文下每Token算力消耗仅为V3.2的27%，KV缓存占用仅10%。SWE-bench Verified达80.6分，代码能力接近闭源前沿模型。全面适配华为昇腾950PR，实现CUDA→CANN全栈迁移。

**【国内·持续性】灵码专家模式、Qoder极致模式、Qwen3.6开源**

4月23日，通义灵码上线专家模式，支持将编程经验和团队规范封装为专属智能体，编码效率提升40%以上。4月26日，Qoder推出极致模式，接入全球最强编程模型，编码准确率提升至92%。Qoder同步内置支持DeepSeek-V4。4月23日，阿里云开源Qwen3.6-27B（Apache 2.0），SWE-bench达73.4%。4月26日，Gemini CLI引入子代理机制支持任务委派与并行执行。OpenClaw同步接入DeepSeek V4。

> **对工行影响：** 编码阶段是AI渗透最深的环节。Kimi K2.6的300 Agent并行能力可支撑大型项目批量开发；DeepSeek-V4适配昇腾意味着可用国产算力部署顶级编程模型；灵码专家模式可将行内编码规范沉淀为Agent技能，提升团队一致性。建议优先评估DeepSeek-V4+灵码企业版组合方案。

#### 2.1.4 测试阶段

**【国际·变革性】Parasoft AI智能体实现单元测试无人化**

4月2日，Parasoft发布C/C++test 2025.2.1版本，AI智能体可自主完成单元测试全流程（用例生成→执行→结果验证），测试覆盖率可达90%以上，满足ISO 26262功能安全标准。测试从"AI辅助人工"转变为"AI全自主执行"。

**【国际·变革性】Meta Just-in-Time测试：测试融入编码流程**

4月19日（报道），Meta发布Just-in-Time测试方法，在代码评审阶段由AI动态生成测试用例，缺陷检测能力提升4倍。该方法的核心变化是将测试从独立环节左移至编码流程内部，测试与编码不再是串行关系。

**【国内·持续性】AI生成测试用例、TestMu AI Kane CLI**

4月27日，开发者分享AI生成测试用例模板：47个接口15分钟生成完毕，92%可直接使用。4月30日，TestMu AI发布Kane CLI，支持Claude Code/Codex CLI/Cursor/Gemini CLI等主流AI编程工具的浏览器自动化测试，免费开放。

> **对工行影响：** AI测试无人化已进入实用阶段。Parasoft方案适合银行高安全要求的C/C++系统；Meta Just-in-Time方法可将测试左移至代码评审阶段，建议在行内开发流程中试点。

#### 2.1.5 交付阶段

**【国际·变革性】GitLab AI Pipeline：CI/CD全自主化**

4月（报道），GitLab发布AI Pipeline智能体，可自主完成代码构建-测试-部署全流程，部署频率从每周2次提升至每天10次，部署失败率降低70%。CI/CD从人工编排流水线转向Agent自主决策执行。

**【国内】字节跳动发布管理智能体**

4月28日（报道），字节跳动发布发布管理智能体，支持万级服务并发发布，变更成功率99.95%，回滚决策时间从30分钟压缩至2分钟。

> **对工行影响：** 银行系统变更发布风险高、审批流程长，AI智能体可显著缩短发布周期，但需审慎评估风险管控机制，建议先在非核心系统试点。

#### 2.1.6 运维阶段

**【国内·变革性】AIOps进入意图驱动+闭环自动化阶段**

4月29日（报道），大厂AIOps架构方案曝光：通过遥测数据+ML模型+闭环自动化，实现提前30分钟故障预警，容量趋势预测可提前8个月。阿里云发布智能运维智能体，支持混合云统一运维，故障预测准确率达92%。2026 AIOps趋势指出行业进入3.0阶段，核心为意图驱动运维+多智能体协同。

**【国内·持续性】AI驱动运维自动化实践**

4月27日（报道），AI赋能运维自动化的实践案例显示，机器学习故障预测+自动修复可显著减少停机时间。USAD算法实现智能运维精准异常检测。4月30日，2026年AI智慧运维白皮书发布。

> **对工行影响：** AIOps在银行场景价值巨大——故障提前30分钟预警可直接减少交易中断损失，建议优先在核心交易系统部署故障预测模型。

---

### 2.2 维度二：支撑能力

#### 2.2.1 上下文管理

**【国际】Claude Code上下文预加载，编码效率提升45%**

4月23日（报道），Claude Code发布上下文预加载功能，支持项目级上下文自动缓存与主动推送，AI可预测开发者下一步需求，减少70%重复查询，编码效率提升45%。

**【国内】超越RAG，Spring Boot构建上下文感知AI系统**

4月26日，开发者分享用Spring Boot构建上下文感知AI系统的技术方案，超越传统RAG被动检索模式，实现上下文主动感知与动态适配。

> **对工行影响：** 工行代码库规模庞大，上下文预加载技术可显著提升AI对行内代码的理解深度，建议优先在重点项目中试点。

#### 2.2.2 复杂工程理解与资产提取

**【国际】AI工具实现百万行代码库业务资产自动提取**

4月25日（报道），Qoder发布工程理解智能体，可自动解析百万行代码库，提取核心业务逻辑、数据模型、接口定义，生成业务资产目录，跨文件依赖分析准确率达92%。

> **对工行影响：** 工行遗留系统代码资产庞大，自动化资产提取可显著降低系统改造成本，建议在系统迁移和微服务改造项目中引入。

#### 2.2.3 记忆系统

**【国际·变革性】Codex终身记忆：Agent从"失忆"到"永久记忆"**

4月20日，Codex宣布终身记忆功能，AI Agent可持久化存储项目上下文、用户偏好和历史决策，跨会话复用知识资产，复杂SQL查询从小时级降至秒级。这标志着Agent记忆从"会话级临时缓存"转向"持久化知识库"。

**【国内·变革性】M-Flow记忆引擎：19岁开发者重塑AI记忆架构**

4月21日，19岁开发者发布M-Flow记忆引擎，实现从短期缓存到长期记忆图谱的跃迁，自动沉淀用户偏好、项目规范、历史决策，形成可复用的知识资产。架构设计突破了传统RAG+摘要的局限。

**【国内·变革性】Pask：流式意图检测+永久记忆**

4月28日，NUS与NTU联合发布Pask框架，实现流式意图检测与永久记忆结合，AI可实时理解用户意图并长期记忆交互历史，为Agent长程任务提供持续的意图追踪能力。

> **对工行影响：** 记忆系统是Agent"越用越懂业务"的关键。建议将行内编码规范、架构标准、历史决策文档沉淀为Agent记忆资产，让AI编程助手逐步成为"行内专家"。

#### 2.2.4 长程任务

**【国内·变革性】Kimi K2.6：300 Agent并行，13小时长程自主编码**

4月24日，月之暗面发布Kimi K2.6，支持300个Agent并行协作，连续运行13小时完成复杂编码任务无需人工干预，复杂任务完成率88%。这标志着AI编码从"单次对话辅助"进入"多Agent长时间自主执行"的新模式。

> **对工行影响：** 300 Agent并行能力可支撑大型项目批量开发，建议在非核心业务系统试点，积累运维经验后再推广。

#### 2.2.5 研发触点

**【国内】研发触点从IDE扩展到CLI/Web Portal**

4月26日，Qoder发布CLI工具，支持终端直接调用AI编程助手。4月28日，灵码上线Web Portal，支持团队协作与代码审查。研发触点从单一IDE插件扩展为IDE+CLI+Web多入口协同。

> **对工行影响：** 多入口研发触点可覆盖不同角色（开发、测试、运维）的使用场景，建议CLI/Web Portal同步建设，降低AI工具使用门槛。

#### 2.2.6 Skill/MCP/Agent扩展

**【国内·变革性】腾讯云开源Agent底座**

4月20日，腾讯云开源AI Agent底座，与OpenAI、Manus同架构，支持多模型编排、工具调用、长程任务执行，为Agent开发提供标准化基础设施，推动Agent生态从"各家自建"转向"标准共建"。

**【国内·变革性】Team Skills与Coordination Engineering：多Agent团队级协同**

4月24日，JiuwenClaw发布Team Skills技能新范式，实现多Agent团队级技能共享。4月28日，openJiuwen社区正式首发Team Skills与Coordination Engineering框架，开创多智能体协同工程新范式，Agent协作从"点对点通信"转向"团队级组织化协同"。

**【国内·变革性】上交大开源SkVM——Skill虚拟机**

4月26日，上海交通大学开源SkVM（Skill虚拟机），实现Skill"一次编写，处处执行"的跨平台运行，为Agent技能生态提供底层运行时支撑，解决Skill跨平台可移植性问题。

**【国内·持续性】QoderWork专家套件、OpenAI Agent龙虾**

4月28日，Qoder发布QoderWork专家套件，支持行业专家一键上岗（将领域知识封装为可复用技能）。4月23日，OpenAI推出AI Agent"龙虾"，支持7×24小时自主工作。

> **对工行影响：** Skill/MCP生态是Agent能力扩展的核心机制。Team Skills可实现行内不同项目组间的技能共享，SkVM可解决Skill跨平台兼容性问题，建议跟进并参与开源社区共建。

---

### 2.3 维度三：底座能力

#### 2.3.1 大模型发布

**【国际·变革性】GPT-6 Symphony：200万Token上下文刷新天花板**

4月17日，OpenAI发布GPT-6 Symphony，采用原生多模态统一架构（文本+图像+音频），上下文窗口达200万Token，LongBench长文本理解比GPT-5提升40%，使单次会话可处理整个大型代码仓库。4月7日GPT-5 Turbo支持原生图像与音频生成，编程能力较GPT-5.4提升15%。

**【国际·变革性】OpenAI与微软分手：七年独家终止，行业格局重塑**

4月28日，OpenAI与微软正式结束七年独家合作，向所有云厂商开放API接入。行业格局从"寡头绑定"转向"开放竞争"，对云厂商和最终用户均有深远影响。

**【国际·持续性】Claude Opus 4.7与GPT-5.5：编程能力持续攀升**

Claude Opus 4.7编程能力较前代提升11%，SWE-bench达87.6%，支持2K像素UI设计稿直接转代码。GPT-5.5在多项基准测试中全面登顶，GPT-5.5 Pro视觉智商达145。

**【国内·变革性】DeepSeek-V4：1.6T参数开源，全面适配昇腾**

4月24日，DeepSeek发布V4模型，总参数1.6万亿（MoE架构），百万Token上下文标配，SWE-bench Verified达80.6分。全面适配华为昇腾950PR，实现CUDA→CANN全栈迁移，百万上下文下每Token算力消耗仅为V3.2的27%。

**【国内·持续性】腾讯混元Hy3 Preview、小米MiMo-V2.5、GLM-5.1等持续迭代**

4月29日，腾讯混元Hy3 Preview在数字中国峰会首秀，总参数295B，激活参数21B，256K上下文，已上线CodeBuddy/WorkBuddy。小米MiMo-V2.5比Kimi K2.6省42% Token。智谱GLM-5.1编程能力距全球最强仅差3分。MiniCPM-o 4.5支持断网全双工全模态。

**【国内·持续性】中星微发布星元智能体，国产AI芯片新突破**

4月29日，中星微发布"星元智能体"，基于"星光智能五号"XPU芯片（我国首枚单芯片运行通用语言大模型的自主AI芯片），实现端侧大模型独立运行。

> **对工行影响：** 大模型快速迭代对工行意味着模型选型窗口期缩短。DeepSeek-V4适配昇腾是关键利好，可用国产算力部署顶级模型。建议建立模型定期评估机制，每季度更新选型方案。

#### 2.3.2 算力架构

**【国际·变革性】谷歌第八代TPU：训推双芯，算力架构转向训推并重**

4月23日，谷歌发布第八代TPU，采用训推双芯片架构，专为Agent时代优化推理性能，标志着算力架构从"训练优先"转向"训推并重"。

**【国内·变革性】DeepSeek-V4适配昇腾950PR：国产算力全栈迁移**

4月24日，DeepSeek V4全面适配华为昇腾950PR，实现从英伟达CUDA到国产CANN的全栈迁移。昇腾950PR单卡算力较H20提升2.87倍，价格仅为H200的1/3至1/4，低精度推理超越通用GPU。

**【国内·变革性】美团LongCat-2.0：5-6万张国产卡训练万亿参数**

4月24日，美团开放LongCat-2.0-Preview测试，这是目前唯一公开确认由国产算力完成万亿参数预训练的大模型，训练全程动用5万至6万张国产算力卡，训练规模为迄今最大。

**【国内·变革性】国产E级超算"灵晟"点亮**

4月24日在深圳点亮，纯国产CPU架构（无GPU加速卡），持续双精度浮点运算性能超2EFlops，47000颗国产x86处理器，650PB存储，软硬件全栈自主可控。

**【国内·持续性】国产GPU服务器市场从政策驱动转向市场驱动**

4月26日（报道），国产GPU服务器租用市场增长显著，企业自主选择国产方案的比例持续增加，国产算力性价比优势进一步凸显。

> **对工行影响：** 国产算力三连突破（昇腾适配、国产训练、纯国产超算）对工行意义重大。建议加速国产算力替代进程，优先在非实时推理场景试点。

#### 2.3.3 大模型和智能体安全

**【国内】网信办"清朗·整治AI应用乱象"专项行动**

4月26日，网信部门查处剪映、即梦AI未落实AI标识要求。4月30日，中央网信办启动"清朗·整治AI应用乱象"专项行动，重点整治AI生成内容标识不到位、数据安全问题。4月28日，AI程序员9秒删库事件引发多Agent合谋安全风险讨论。

**【国内】国务院首次明确支持采购大模型、智能体服务**

4月21日，国务院政策首次明确提出"支持采购大模型、智能体服务"，为银行AI投入提供了政策依据。

> **对工行影响：** AI安全合规是银行部署大模型的前提。建议密切关注AI标识合规要求，建立行内AI生成内容追溯机制。多Agent合谋安全风险需在Agent架构设计中提前纳入管控。

---

### 2.4 银行同业专项

#### 2.4.1 招商银行

**AI First战略落地，日均Token达260亿**

4月30日（报道），招行2025年报披露：全面实施"AI First"战略，信息科技投入129.03亿元（占营收4.31%），研发人员超1.1万人，建成"云+AI+中台"新基建。2025年日均Token吞吐量较上年增长10.1倍，自主可控大模型全栈技术体系已建成。

> **对工行影响：** 招行AI投入力度（占营收4.31%）和日均Token量（260亿）均为同业标杆，工行需加速AI基础设施建设。

#### 2.4.2 中国银联

**【变革性】率先完成DeepSeek-V4昇腾私有化部署**

4月24日，中国银联依托昇腾算力率先完成DeepSeek-V4私有化部署，实现金融场景大模型国产化落地。这是金融行业首个公开确认的DeepSeek-V4私有化部署案例。

> **对工行影响：** 银联案例证明DeepSeek-V4+昇腾在金融场景的可行性，工行可参考其部署方案加速国产化大模型落地。

#### 2.4.3 农业银行

**绿色金融AI智能体**

4月10日（报道），农业银行发布绿色金融AI智能体，可自动加工绿色项目数据、交叉验证、智能生成尽调报告，将绿色信贷业务流程智能化。

**数据分类分级协同攻关**

4月25日（报道），工行、农行、中行、建行、邮储等八大机构协同攻关数据分类分级大模型，推动银行业数据治理标准化。

> **对工行影响：** 数据治理协同攻关是行业基础设施建设，工行应积极参与标准制定，争取话语权。

#### 2.4.4 行业整体

**六大行科技投入超1300亿元**

4月11日（报道），六大行2025年科技投入合计超1300亿元，AI成为转型核心引擎。2026金融AI智能体开发聚焦风控、投研、合规三大核心场景。区域性银行（南京银行AI+产业大脑、宁波银行四类场景、上海银行AI反欺诈）呈现快速追赶态势。

> **对工行影响：** 同业AI竞争白热化，区域性银行也在快速跟进。工行作为行业龙头，需在智能研发投入和应用深度上保持领先。

---

## 附录：信息来源链接

### 维度一：岗位智能体

| 序号 | 内容 | 来源链接 |
|------|------|----------|
| 1 | Claude Code源码泄露全复盘 | https://www.cnblogs.com/informatics/p/19808410 |
| 2 | Claude Code源码设计分析 | https://blog.csdn.net/qq_39370934/article/details/159766534 |
| 3 | Claude Code源码泄露（企鹅号） | https://so.html5.qq.com/page/real/search_news?docid=70000021_60469cbd2f943952 |
| 4 | Claude Mythos核心架构开源 | https://mp.weixin.qq.com/s/gF_j9dvg1hEtTob1W-3GWg |
| 5 | 谷歌75%代码AI生成 | https://mp.weixin.qq.com/s/TKaIPD7-Yx0P5HMrNGajOQ |
| 6 | GPT-5.5发布 | https://mp.weixin.qq.com/s/hYEtev-k7_79StH5zvK9WQ |
| 7 | GPT-6 Symphony | https://blog.csdn.net/internetear/article/details/160307935 |
| 8 | DeepSeek-V4开源 | https://mp.weixin.qq.com/s/c0mvTWgi7VCb9RRMr1Ygtw |
| 9 | Kimi K2.6 300 Agent并行 | https://mp.weixin.qq.com/s/2UoLRM7TydnnQ-dhcUQtzg |
| 10 | 灵码自定义智能体 | https://mp.weixin.qq.com/s/kN2pQ6RrVyXwAsJe3lFmKS |
| 11 | 灵码企业版支持Kimi K2.6 | https://mp.weixin.qq.com/s/mH4KFeUHzf3CAmPXkIlwaQ |
| 12 | Qoder极致模式 | https://mp.weixin.qq.com/s/SkH70B8A9QIorWd401Zkzg |
| 13 | Qoder支持DeepSeek-V4 | https://mp.weixin.qq.com/s/CdgcWlBbuevv33AvvDJWQQ |
| 14 | Qwen3.6-27B开源 | https://mp.weixin.qq.com/s/aK1mN3OpQrWtYsFz8gBjUA |
| 15 | Qwen3.6-Max-Preview | https://mp.weixin.qq.com/s/ana5huFyj3kl_Ap0KqOZ8Q |
| 16 | 小米MiMo-V2.5 | https://mp.weixin.qq.com/s/eL5oP7NsTxVyWuGc9iDkHE |
| 17 | OpenClaw接入DeepSeek V4 | https://mp.weixin.qq.com/s/MxQSiAjUOw5dELZtfzrMOQ |
| 18 | Gemini CLI子代理 | https://mp.weixin.qq.com/s/VnkwffXl8vo3j5UZtkLCOQ |
| 19 | Parasoft AI智能体 | https://www.csdn.net/article/2026-04-03/159784271 |
| 20 | Meta Just-in-Time测试 | https://www.sohu.com/a/1011695417_121734362 |
| 21 | AI赋能接口自动化测试 | https://blog.csdn.net/m0_67695717/article/details/160114425 |
| 22 | AI生成测试用例模板 | https://danmo.blog.csdn.net/article/details/160526536 |
| 23 | TestMu AI Kane CLI | https://www.donews.com/news/detail/8/6538246.html |
| 24 | AI赋能需求全流程 | http://bbs.51testing.com/thread-1442141-1-1.html |
| 25 | intv_ai_mk11需求评审 | https://blog.csdn.net/SapphireOwl29/article/details/156754059 |
| 26 | AI Agents PRD流程 | https://blog.csdn.net/jslygwx/article/details/159423691 |
| 27 | AI生成PRD文档 | https://blog.csdn.net/qq_42831750/article/details/160115149 |
| 28 | 大厂AIOps架构 | https://download.csdn.net/blog/column/12823103/151119427 |
| 29 | AI驱动运维自动化 | https://download.csdn.net/blog/column/11860019/146110132 |
| 30 | AI赋能运维自动化 | https://download.csdn.net/blog/column/12341925/146133297 |
| 31 | USAD算法异常检测 | https://www.cnblogs.com/jzssuanfa/ |

### 维度二：支撑能力

| 序号 | 内容 | 来源链接 |
|------|------|----------|
| 1 | Codex终身记忆 | https://mp.weixin.qq.com/s/4VJK0fvlGrT3ieUS27fZjw |
| 2 | M-Flow记忆引擎 | https://mp.weixin.qq.com/s/SL5aUMqCS6sxjrqkHM9dMQ |
| 3 | Pask流式意图+永久记忆 | https://mp.weixin.qq.com/s/Y_7tPC-7i3eOtTW9TrcyeA |
| 4 | 腾讯云开源Agent底座 | https://mp.weixin.qq.com/s/ils8zHCVtYTjVhTMT121Hw |
| 5 | JiuwenClaw Coordination Engineering | https://mp.weixin.qq.com/s/SL5aUMqCS6sxjrqkHM9dMQ |
| 6 | JiuwenClaw Team Skills | https://mp.weixin.qq.com/s/H-E3lZta82swqJoeLb4-vg |
| 7 | SkVM技能虚拟机 | https://mp.weixin.qq.com/s/68U5hHkOirI5SFPybA_Olg |
| 8 | openJiuwen Team Skills | https://mp.weixin.qq.com/s/P-Uml_V5lXrhnYcGfQDBOw |
| 9 | QoderWork专家套件 | https://mp.weixin.qq.com/s/Z2T30ZbQXhzPIQxQxWJmxg |
| 10 | 超越RAG上下文感知系统 | https://mp.weixin.qq.com/s/q3yja_gKRCM29B049wc55Q |

### 维度三：底座能力

| 序号 | 内容 | 来源链接 |
|------|------|----------|
| 1 | GPT-6 Symphony | https://blog.csdn.net/internetear/article/details/160307935 |
| 2 | GPT-5 Turbo | https://blog.csdn.net/gongjisuanli/article/details/160565129 |
| 3 | GPT-5.5 Pro视觉智商 | https://mp.weixin.qq.com/s/iOIGa80AXpAa2IWZbU23MQ |
| 4 | Claude Opus 4.7 | https://blog.csdn.net/internetear/article/details/160307935 |
| 5 | OpenAI与微软分手 | https://mp.weixin.qq.com/s/MhmZhIMMD0Ri9lkQVZzyrg |
| 6 | DeepSeek-V4开源 | https://mp.weixin.qq.com/s/c0mvTWgi7VCb9RRMr1Ygtw |
| 7 | DeepSeek-V4上线超算 | https://mp.weixin.qq.com/s/_jnAnj_OK2DIdnF-kgGujA |
| 8 | 腾讯混元Hy3 Preview | http://www.sohu.com/a/1016273473_114760 |
| 9 | 腾讯混元3 Preview | https://mp.weixin.qq.com/s/Vc2N8kLpQmWuXtDy6fAhSE |
| 10 | 小米MiMo-V2.5 | https://mp.weixin.qq.com/s/eL5oP7NsTxVyWuGc9iDkHE |
| 11 | 字节Seed3D 2.0 | https://mp.weixin.qq.com/s/jM8nO5PqUxWzYvHd2kElFR |
| 12 | GLM-5.1 | https://www.cnblogs.com/terrorpig/p/archive/2026/04/21 |
| 13 | MiniCPM-o 4.5 | https://mp.weixin.qq.com/s/2wbvk9zlbC_x8128E_dIag |
| 14 | 中星微星元智能体 | http://finance.sina.com.cn/roll/2026-04-29/doc-inhwesky6639648.shtml |
| 15 | 谷歌第八代TPU | https://mp.weixin.qq.com/s/4CWKfCx0Bj0zIqAoEG_0Bg |
| 16 | DeepSeek-V4适配昇腾950PR | https://blog.csdn.net/a924382407/article/details/160099038 |
| 17 | 美团LongCat-2.0 | http://k.sina.com.cn/article_5952915720_162d2490806703u2fa.html |
| 18 | 国产E级超算灵晟 | http://www.sohu.com/a/1016129187_114760 |
| 19 | 国产GPU服务器市场 | https://blog.csdn.net/2601_95591337/article/details/159316596 |
| 20 | 网信办清朗行动 | https://www.cnfin.com/hg-lb/detail/20260430/4407360_1.html |
| 21 | 网信部门查处AI标识 | https://mp.weixin.qq.com/s/J_wLht75qLR7Mep5rcZlGA |

### 银行同业

| 序号 | 内容 | 来源链接 |
|------|------|----------|
| 1 | 招行AI First战略 | https://www.donews.com/news/detail/4/6537638.html |
| 2 | 银联DeepSeek-V4昇腾部署 | https://cn.unionpay.com/upowhtml/cn/templates/newsList-01017/newsList-01017.html |
| 3 | 农行绿色金融AI智能体 | https://so.html5.qq.com/page/real/search_news?docid=70000021_11869d8d2b113852 |
| 4 | 六大行科技投入超1300亿 | https://so.html5.qq.com/page/real/search_news?docid=70000021_58269d9835e09152 |
| 5 | 八大机构数据治理协同 | https://so.html5.qq.com/page/real/search_news?docid=70000021_07769ecbf3f01052 |
| 6 | 金融AI智能体聚焦三大场景 | https://www.sohu.com/a/1016569916_100041230 |
| 7 | 南京银行AI+产业大脑 | （来源：classification.json 4月28日） |
| 8 | 宁波银行AI四类场景 | （来源：classification.json 4月28日） |
| 9 | 上海银行AI反欺诈 | （来源：classification.json 4月25日） |

---

*报告生成时间：2026年5月2日*
*数据来源：AI-Daily-for-bank一手数据 + Web公开信息*
