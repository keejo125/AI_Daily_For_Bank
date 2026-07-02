## Java微服务本地化改造:AI Coding的最后一公里

### 问题的本质:微服务架构天然不AI友好

Java微服务项目重度依赖HSF/TDDL/OSS/Diamond/MetaQ等云端基础设施。本地`mvn spring-boot:run`直接启动失败,AI写完代码没有任何办法验证自己写的东西能不能跑。经典循环:我把代码推到预发,等5分钟部署完成,手动触发一次调用,发现NPE,截图贴回给AI,AI改了两行,我再推预发,再等5分钟......三轮下来半小时过去了,改的只是一个参数注入顺序的问题。同样的模型、同样的Prompt,差距不在AI能力,在如何构建AI友好的工程环境。

**改造前工作流**:本地Vibe Coding → 推预发部署 → 人工验证 → 反馈给AI → AI继续改 → 再次推预发 → 再次人工验证......人在每个环节都是阻塞点。

### 三条改造原则

**1. 依赖倒置,接口先行**

上层逻辑依赖抽象接口,不依赖具体实现。云端和本地只是接口的不同实现。抽一个`StorageAdapter`接口,线上的OSS实现加一行`implements StorageAdapter`,本地新写一个`LocalStorageAdapter`用`java.nio.file`映射到本地路径。工厂类检测参数自动选择,切换运行环境就是换一个接口实现,上层代码完全不用改。

```
StorageAdapter (接口)
 ├── OssStorageAdapter (线上,走OSS SDK)
 └── LocalStorageAdapter (本地,走java.nio.file)

CommandExecutor (接口)
 ├── SandboxCommandExecutor (线上,调远程沙箱API)
 └── LocalCommandExecutor (本地,ProcessBuilder + bash -c)
```

**2. 零侵入,Profile隔离**

本地改造不能让线上代码路径多走一行额外的代码。Spring Profile隔离:本地专属Bean通过`@Profile("local")`装配,线上专属的通过`@Profile("!local")`守卫。`@Nullable`参数注入:可选依赖标`@Nullable`,不存在时Spring注入null。条件守卫:`localFsBasePath`不为空就走本地,`ossClient`不为空就走线上。最终效果:删掉所有本地相关代码后,线上行为完全不变。

**3. 工具AI化:CLI优先**

AI Agent的能力边界 = 它能调用的工具的边界。GUI对AI不可见,CLI才是AI能用的东西。通过`mw-cli`查询Diamond运行时配置、通过`mw hsf address`查询HSF服务地址。团队使用的运维工具是否有CLI入口?配置管理是否可通过命令行查询?是否有MCP Server或Skill将内部系统能力暴露给AI Agent?

**工具AI化优先级**:CLI直接可用(mw-cli、mvn、git、arthas)> MCP Server协议适配 > Skill/Tool自定义封装 > GUI不可用。

### 改造效果

| 对比项 | 改造前 | 改造后 |
|--------|--------|--------|
| 文件操作验证 | 推预发,通过OSS控制台查看 | 本地直接`ls`查看 |
| Bash执行验证 | 推预发,登录沙箱查看 | 本地Terminal直接看 |
| AI自主验证 | 做不到 | ReadFile → 验证WriteFile结果 |
| 单次迭代耗时 | 5-10分钟(含部署等待) | 秒级 |
| AI自主修复轮数 | 0(每轮都要人工介入) | 平均3-5轮后自行收敛 |

完整bug fix流程:改造前需要3-4轮人工推预发验证、总耗时30分钟以上;改造后AI在本地自主迭代,通常2分钟内收敛,人只需要最后review结果。

### 配套Harness工程

**CLAUDE.md**:给AI一张地图。项目根目录放一份,告诉AI这个项目是什么、怎么构建、怎么测试、本地环境怎么启动。100行以内,重点是让AI能快速定位该看哪些代码、该跑什么命令。

**验证脚本**:`scripts/verify-local.sh`让AI自己检查:编译→单元测试→本地启动检查→文件系统闭环检查。AI改完代码跑一次`bash scripts/verify-local.sh`,不需要人工介入就能知道本地环境是否正常。

### 对我行的启示

1. **本地Harness是基础中的基础**:CLAUDE.md写得再好,AI连代码能不能编译通过都验证不了,后面一切都是空谈。我行Java项目占比高,本地环境改造需求更迫切
2. **接口抽象是关键杠杆**:依赖倒置不只是设计原则,更是让AI跑起来的必要条件--不抽接口,本地化无从谈起
3. **Profile隔离保证安全**:零侵入原则确保本地改造不引入线上风险,这对金融系统尤为重要
4. **CLI化是AI化的前提**:行内Diamond/HSF/Switch等管理平台GUI化程度高,需要先CLI桥接才能让AI调用
5. **渐进式改造可行**:不需要一次性改造完所有依赖,找到核心链路(请求→LLM→Tool→返回)所需最小依赖集合,先让这条链路本地跑通

---

## Agent核心技术范式演变

### 核心观点

从宏观架构看,今日的Agent仍由Prompt、Planning、Memory、Tools、Workflow、Environment等经典模块组成,与Lilian Weng早期提出的理论框架无本质差异。"形"未变,但"神"已大不同--这不是简单的技术升级,而是一场深刻的内核重构。

### Agent发展四阶段

| 阶段 | 时期 | 核心特征 |
|------|------|----------|
| 早期Agent(ReAct) | 2023 | 被动式响应,单步Reasoning+Action,依赖用户明确指令,缺乏长期规划 |
| 工作流Agent | 2024 | Agentic Workflow,工程化约束弥补模型不确定性,Harness雏形 |
| 自主Agent | 2025 | 复杂Planning+长程任务,Manus/Claude Code/Codex,AI Coding爆发 |
| 自进化Agent | 2026+ | 自我沉淀Skill/知识库,RL训练提升能力,从消耗品到可积累资产 |

### 六个核心技术维度的演进

**Prompt:单体 → 解耦+渐进式加载**

早期:一个任务创建一个Agent,每个Agent对应一段精心调试的独立System Prompt(人设+目标+约束+示例),维护成本极高。

当前:System Prompt只保留最底层、最通用的系统级指令和基本行为规范(极度"稳定"部分);动态内容(任务要求、领域知识、人设规范)剥离到外部文件系统,通过渐进式披露(Progressive Disclosure)动态加载。

具体方式:
- **Skill层面**:执行某项任务的方法论、步骤要求、领域约束,沉淀为独立Markdown文件(如SKILL.md),Agent执行特定任务时动态加载对应Skill
- **配置文件层面**:USER.md、SOUL.md、AGENTS.md等,通过文件系统渐进式加载

本质:**动静分离**--System Prompt稳定,动态业务逻辑灵活挂载。

**Planning:线性CoT → 复杂长程任务拆解**

早期:依赖模型原生的思维链(CoT)能力,如"Let's think step by step",处理简单任务尚可,复杂场景易陷入逻辑断层或死循环。

当前(基座模型推理能力显著增强后):
1. **结构化分解**:将宏大模糊目标拆解为多个可执行的子任务,生成结构化Todo List
2. **多步协同**:按步骤有序执行,动态调整计划,保持长上下文依赖的逻辑一致性和连贯性
3. **动态子Agent构建**:根据子任务需求,动态实例化或调用特定子Agent专项解决

核心驱动力:**底层基座模型推理能力升级**,从"提示词技巧"演变为真正的"智能决策中枢"。

**Memory:向量检索主导 → 文件系统化+向量检索混合**

短期记忆(Short-term Memory):Context Window有限且成本敏感,从简单堆砌历史对话 → 多种压缩策略:
- 阈值控制:基于固定token数或动态语义密度阈值触发压缩
- 结构化摘要:对中间过程对话进行Summary提炼,保留头尾关键指令和最终结论
- 重点提取:从冗长对话流中提取关键事实或状态变化,剔除无关噪音

长期记忆(Long-term Memory):从"向量数据库主导"向"文件系统主导"回归:
- **事项型记忆(Episodic Memory)**:用户偏好、历史行为、每日待办等动态事实 → 文件系统记录(如MEMORY.md或每日Memory日志文件),比向量检索更可控、更易读、更适合Agent直接读取理解时间序列状态变化
- **知识型记忆(Semantic Memory)**:Karpathy等提出的LLM-Wiki、GBrain等本地化知识库理念 → 本地文件系统+Obsidian等笔记工具,grep类关键词检索 + 搭配QMD或SQLite等轻量向量检索机制

本质:**文件系统化的沉淀+向量检索混合管理**,追求更高的记忆效果、可读性和效率均衡。

**Tools:Function Call → CLI原生+Script脚本化**

早期痛点:Function Call需要针对具体业务场景将系统能力封装成标准API并注册为模型可调用函数,开发维护成本极高,且大量系统没有现成API可供调用。

MCP(Model Context Protocol):协议层面优化了工具注册与发现机制,实现"一次注册,自动暴露",但本质仍停留在接口标准化层面。

真正的范式转移:**CLI原生化 + Script脚本化**:

- **CLI的核心优势**:
  - 零样本学习:大模型预训练数据中海量Linux/Unix命令属于"先天知识",无需额外定义API Schema,节省巨大token空间和调试成本
  - 可扩展性与自解释性:只要遵循标准Linux/Unix规范(如支持--help),模型就能即时查询帮助文档、自主理解参数用法并执行调用
  - Skill集成:第三方CLI工具可通过Skill包装,Skill描述文件中提供安装指南和使用示例,使模型快速掌握新工具

- **Script脚本化**:Python或其他语言的工具逻辑封装为独立脚本文件
  - 本地与远程统一:直接执行本地命令(文件操作、环境配置),或内部封装对远程API调用
  - 协议黑盒化:API鉴权、参数拼接等细节隐藏在脚本内部,Agent只需关注"调用哪个脚本"+"传入什么核心参数"

本质:**从"人为适配模型"到"利用模型原生能力"**,不再为每个操作编写专用API,充分利用模型预训练阶段积累的通用计算机操作知识(CLI)和代码执行能力(Script)。

**Workflow:刚性编排 → 动态Skill封装+混合架构**

早期:依赖显式、硬编码的Workflow(状态机/流水线Pipline),强制按部就班执行,确保Agent不"跑偏"。问题是过于"机械化",无法根据实际情况动态调整。

当前演进:从"刚性的流程编排"转向"动态的Skill封装与混合架构":
- **逻辑内聚化**:原本分散在Workflow引擎中的步骤定义、约束条件、核心判断逻辑,直接写入Skill的Markdown描述文件(如SKILL.md),模型通过阅读Skills文档理解完整任务链路
- **执行脚本化**:需要精确控制的环节,通过Skill关联的Resources的Script脚本进行代码级编排和控制,打包成独立可复用Skills

混合架构策略(当前最佳实践):
- 成熟、标准化的子任务封装为Skills,通过Markdown维护逻辑,利用其灵活性和易用性
- 对稳定性要求极高的主干流程仍保留为Workflow,或将特定Workflow封装为特殊Tool供Agent调用
- **"Skill为主,Workflow为辅/兜底"**--既利用新技术红利,又保留一定确定性

**Environment:无状态 → 有状态隔离Runtime**

早期:Agent对工具调用、子Agent调用几乎无状态,不需要"运行环境"。

当前(引入文件系统操作、代码执行等能力后):Agent必须拥有专属Workspace,需要持久化存储、文件读写和状态管理,成为真正的"数字员工"。

两种主要形态:
- **本地个人电脑(Local Desktop)**:极高便利性和灵活性,OpenClaw最早就是基于个人电脑操作而"火"的。但缺乏严格隔离,Agent操作失误可能导致数据丢失或系统配置混乱,需要更严格的用户确认机制或权限控制
- **沙箱环境(Sandbox/Cloud Server)**:企业级生产环境主流选择。Docker/Kubernetes等容器化技术构建隔离沙箱,所有操作限制在特定虚拟文件系统内,提供必要的安全边界和资源管控,确保Agent在不可预测行为下保持系统整体稳定性

### 核心结论

Agent正在从"魔法调优"到"系统工程"的转变--用工程化手段构建确定性,承载模型的不确定性。理解演进背后的逻辑,比掌握具体某个工具更为重要。因为Agent还在持续发展,模型会继续升级、工具会继续变化,框架会持续更新,但**"通过工程化手段构建确定性,以承载模型不确定性"**的核心思想,将是未来很长一段时间内构建高质量Agent的基石。

---

## 文章引用列表

| # | 标题 | 来源 | 核心要点 |
|---|------|------|----------|
| [1] | Harness Engineering(驾驭工程) | 微信公众号 | R.E.S.T框架、PPAF循环、REPL容器、六原则、四层沙箱 |
| [2] | 从 Prompt Engineering 到 Harness Engineering | 阿里妹 | 三次范式跃迁、四根支柱、四种失败模式、十阶段流程、AI代码率25%→90% |
| [3] | 终端沙箱:Agent Harness 的基础设施 | Qoder/通义灵码 | 终端沙箱三层防护、三平台实现、性能开销、对银行启示 |
| [4] | 一个 AI 还是不够 | MiniMax 稀宇科技 | Agent Team 架构、Leader-Worker-Verifier、四场景落地、成本验证 |
| [5] | OpenClacky Harness 工程7个决策 | AI Maker Summit(李亚飞) | 两代失败教训、双Cache标记、System Prompt字节冻结、Skill子Agent、固定16工具、压缩策略、工具自进化、内置浏览器接管 |
| [6] | Java微服务本地化改造:AI Coding的最后一公里 | 内部技术实践 | 依赖倒置/零侵入Profile/CLI优先三条原则,本地Harness让AI自主验证,单次迭代从10分钟降到秒级 |
| [7] | Agent核心技术概念与范式发生了哪些演变以及背后的思考 | 阿里云开发者（飞樰） | Agent发展四阶段、六个核心技术维度演进：Prompt解耦、Planning长程、Memory混合、Tools脚本化、Skill封装、环境隔离；核心洞察：从"魔法调优"到"系统工程"的转变 |
| [8] | Anthropic与OpenAI同周预警：AI开始自己造自己 | 51CTO技术栈 | RSI递归自我改进实证、80%代码Claude所写、52倍提速能力、Karpathy加入Anthropic做RSI、未来三种剧本 |

---

### RSI：AI正在加速自己（Anthropic实证）

RSI（递归自我改进）= AI不再只是被人类改进，开始自己改进自己。[8]

**外部证据**：
- 外部证据：AI独立可靠完成的任务时长约每4个月翻一番（此前趋势是每7个月）
- CORE-Bench测试：2024年成功率约20%，15个月后饱和；METR测试Claude Mythos Preview至少连续运行16小时，达到METR可衡量的上限
- 趋势推演：2024年Claude Opus 3处理4分钟任务→2025年Claude Sonnet 3.7处理1.5小时任务→2026年Claude Opus 4.6处理12小时任务

**内部证据**（Anthropic自家）：
- Anthropic代码库中**超80%代码出自Claude**
- Claude代码质量持续提升：高难度开放式任务成功率6个月从约26%提升至76%（+50个百分点）
- Claude提速能力：2025年5月平均提速3倍→2026年4月提速**52倍**
- Claude首次完整运行开放式研究项目（自主研究实验）
- Claude在引导研究会议方面越来越强：Mythos Preview在64%情况下优于人类选择

**关键人物**：Andrej Karpathy加入Anthropic，据报道就是做RSI相关工作

**未来剧本**（Anthropic预设）：
1. 发展趋势停滞，但能力已广泛普及（可能性不大）
2. **实验室效率持续提升**（很可能）：AI开发高度自动化，人类负责设定研究方向和评判结果。100人公司或可完成1万~10万人组织的工作量
3. 完全递归自我改进：AI发展速度完全取决于计算资源，人类角色转为监督/验证/确认

---

_最后更新：2026-06-05_
_版本：v1.7_

---

## PawBench：通用智能体评测基准（Harness × 模型联合评测）

### 定位

PawBench（通义实验室）将"底座模型 + 运行框架（Harness）"纳入同一评测体系，给通用智能体一把可度量的尺。

**评测矩阵**：9模型 × 3 Harness × 150任务 = 4050测试单元  
Harness：Hermes、OpenClaw、QwenPaw  
全部任务在Docker沙箱中运行，轨迹/产物/快照均可保留复盘。

### 关键发现

**发现一：Harness间存在稳定分差**

| Harness | 得分 |
|---------|------|
| QwenPaw | 76.4 |
| OpenClaw | 75.4 |
| Hermes | 70.4 |

极差6.4分，堪比一次重大模型版本升级。

**好Harness能让模型"以下克上"**：GLM 5.1在Hermes下68.2分；Qwen3.6-35b-a3b在QwenPaw下70.4分（差2.2分）。

**同一模型换Harness差距达11.5分**（qwen3.6-35b-a3b）。

根因分析：
- **缺乏产物级硬校验**：模型过早宣布完成，Workspace产物未真正落盘
- **路径感知与约束宽松**：模型"自以为"写入成功，评测程序扫描不到产物
- **工具表体量过大**：Hermes约65个、OpenClaw约30个、QwenPaw约15个。过多工具Schema挤占上下文、增加小模型首轮决策负担

**发现二：Skill主动发现是Harness能力短板**

17道Skill任务三家都吃力：
- OpenClaw**唯一**能主动加载workspace中的Skills
- 其他两家只扫描全局预装Skill，漏掉项目专属Skills

**发现三：Web搜索任务依赖默认可用性**

- Hermes：核心工具(web_search/web_extract)被锁死，需配置外部API Key才可用
- OpenClaw：web_search支持DuckDuckGo免密服务，web_fetch内置HTTP抓取，零配置直连
- QwenPaw：通过browser_use结合模型知识也能完成基础Web访问

### Harness设计四条原则

| 原则 | 含义 |
|------|------|
| **Inform Fully（充分告知）** | 模型看不见的东西=不存在。明确告知cwd/workspace路径/输出目录/Skill位置 |
| **Equip on Demand（按需装备）** | 关键工具默认可用（keyless搜索、内置fetch、Skill helper）；工具数量匹配模型上下文预算 |
| **Monitor Actively（主动监控）** | 检查产物是否真正落地：文件是否存在/非空/含必填字段；产物级校验>一句"我完成了" |
| **Recover Gracefully（弹性恢复）** | 异常时不直接失败，给一次信息量更足的续推机会（注入当前状态+说明缺少什么），设置合理的retry budget |

### 对我行启示

1. **Harness比模型本身更关键**：好Harness能让弱模型超越强模型，选型时应Harness+模型联合评测
2. **OpenClaw的Skill主动发现能力是优势**：我行已在用OpenClaw，Skill机制值得深挖
3. **产物级校验是必备能力**：文件写入/代码修改/报告生成类任务，必须验证产物真正落盘
4. **工具"默认可用"决定零配置体验**：我行推广时，内网工具应做到拉下来就跑

---

_最后更新：2026-06-05_
_版本：v1.8_
