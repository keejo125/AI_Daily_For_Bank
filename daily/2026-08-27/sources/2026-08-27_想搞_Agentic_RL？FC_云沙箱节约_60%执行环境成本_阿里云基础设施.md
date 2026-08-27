---
publish_time: 1787826963
status: pending
category: 
is_model_related: false
digest: |
link: https://mp.weixin.qq.com/s/C1WR5-SJWDl98-bvwGWRNw
source: 阿里云基础设施
title: 想搞 Agentic RL？FC 云沙箱节约 60%执行环境成本
---

# 想搞 Agentic RL？FC 云沙箱节约 60%执行环境成本

来源：阿里云基础设施
原文链接：https://mp.weixin.qq.com/s/C1WR5-SJWDl98-bvwGWRNw

Agentic RL 正在把模型训练和评测从“生成答案”推向“在环境中完成任务”。当 Agent 开始操作 Browser、Filesystem、Desktop 和真实应用，一条 Rollout 往往要持续几十甚至上百步：每次 Action 都会改变环境，下一次 Observation 又依赖这些变化，最终还要由 Verifier 检查 Agent 留下的结果。执行环境因此不再只是模型调用的配套资源，而开始直接影响 Rollout 的正确性、稳定性和执行效率。
OSWorld 是这种 workload 的一个典型代表。Agent 需要根据 Screenshot、Accessibility Tree 等 Observation，在完整桌面和应用中持续执行 Mouse、Keyboard、Command、File 等操作，并在任务结束后由 Verifier 检查最终状态。单个 Trial 已经要求 Environment 保持状态连续、Observation 与 Action 一致；到了全量评测，又进一步涉及数百条独立 Trial 的隔离、复用和并发调度。
这次我们把 OSWorld 接入 Harbor，并使用阿里云函数计算 FC 云沙箱承载每条 Trial 的执行环境，完成了 OSWorld 全量评测和规模化运行。这篇文章想讨论的也不只是“如何给 Harbor 换一个 沙箱后端”，而是一个更基础的问题：
当 Rollout 开始持续改变外部世界，Agentic RL 到底需要什么样的执行环境？
一、从 Agentic RL Rollout 到 OSWorld：执行环境需要解决什么
在 Agentic RL 中，一条 Rollout 不再只是若干次模型调用。Agent 每执行一次 Action，都会改变 Environment；下一次 Observation 又来自已经变化后的状态。这样的交互持续几十甚至上百步，直到任务结束，再由 Verifier 根据最终状态产生 Reward。
一条典型 Rollout 可以抽象成：
这里和普通模型调用最大的区别，是 Environment 本身也在保存状态。Context 可以记录 Agent 刚才做过什么，但不能代替 Action 真正留下的结果。文件是否已经保存、浏览器是否保持登录、应用当前处于什么状态，都真实存在于 Environment 中。只要这些状态在 Rollout 中途丢失，后续 Observation 和最终 Reward 的依据都会发生变化。
OSWorld 把这种要求体现得尤其完整：Agent 需要在真实桌面和应用中，根据 Screenshot、Accessibility Tree 等 Observation 持续执行鼠标、键盘、命令和文件操作；任务结束后，Verifier 还要检查文件、应用或系统最终留下的状态。它需要的并不是"一台能够远程操作的桌面"，而是一个真正能够承载 Rollout 的 Environment，同时具备以下四项能力：
① Agent 造成的状态变化，要一路保留到 Verifier 检查完成；
② Observation 和 Action，要持续围绕同一份状态形成闭环；
③ 反复创建的环境，要共享一套稳定的公共基线；
④
而每一次创建出来的状态，又要有自己独立的归属，不能和别的 Trial 混在一起。
这四项要求首先保证的是一条 Trial 的语义正确性。但到了全量评测，Environment 还要面对另一个问题：同一套 Baseline 能不能被反复创建，并让大量完整 Trial 在有限并发下持续完成准备、执行、判分和回收。问题由此从“一个 Environment 是否正确”，进一步变成了“这样的 Environment 能否被规模化复制和调度”。
二、一个 GUI Agent Environment 到底要保证什么
2.1
Trial 必须面对同一个持续变化的世界
在 Harbor 中，一次评测被组织为一条 Trial。Environment Setup、Agent 执行、Verifier 判分和 Result 回收共同构成它的完整生命周期。
这个流程真正保证的是状态连续性。Environment Setup 把任务素材放进环境并完成任务级初始化；Agent 在此基础上启动应用、操作桌面、修改文件；Agent 结束后，Verifier 继续进入同一个环境，读取刚刚形成的最终状态并生成 Reward。
在当前实现中，
tests/
会在 Agent 执行结束后才注入 Sandbox，避免 Agent 在操作阶段接触判分逻辑。更关键的是，从 Agent execution 到 Verifier execution 不能更换沙箱实例：即使两个 Sandbox 从同一个 Image 启动，安装的软件和执行的 Task 都完全一样，它们也只是起点相同——Agent 在前一个 Sandbox 里改过的文件、应用状态和桌面现场，如果没有继续保留给 Verifier，Verifier 看到的就不是这条 Trial 真正执行完后的环境。
所以
GUI Benchmark
所需的不是配置一致，而是状态连续。
2.2
Observation 和 Action 必须围绕同一个状态闭环
一个 GUI Environment 同时存在两条方向相反的数据路径：Environment 向 Agent 提供 Observation，Agent 再通过 Action 改变 Environment。
在 OSWorld 中，这些路径具体涉及 Command、File、Screenshot、Accessibility Tree、Mouse 和 Keyboard。把每个 API 单独调通只是第一步，Environment 还必须保证这些接口共同指向同一个状态空间。
例如，Command 写入的文件需要能被桌面应用打开；Mouse 或 Keyboard 改变的窗口需要出现在下一张 Screenshot 中；GUI 应用保存的内容需要能被 File 接口和 Verifier 读取。否则每个接口都可能返回成功，但整条 Rollout 的因果关系仍然不成立。
这里有一个很容易被单个接口掩盖的问题：Screenshot 请求成功，只能证明返回了一张合法图片，并不能证明它反映的是 Agent 刚刚操作过的最新状态；同样，GUI Action 返回成功，也不能证明动作作用在 Agent 当前观察的那个桌面上。对 Rollout 来说，真正需要验证的是 Observation 和 Action 是否围绕同一个 Display 和同一份 Environment State 形成因果闭环。
2.3
公共 Environment 和每条 Trial 的状态必须分开
如果每个 Trial 都从头安装桌面、应用和 Verifier 依赖，固定准备成本会在几百条任务中重复发生；如果把具体任务的状态也固化到公共环境里，不同 Trial 又会失去隔离。
因此，一个可复用的 GUI Environment 需要拆成公共的 Environment Baseline，以及仅属于当前任务的 Trial State。
Baseline 保存所有 Trial 共同需要的内容：
● OS、systemd、X Server 和 GNOME Desktop
● Chrome、LibreOffice、GIMP、VLC、Thunderbird、VS Code 等应用
● envd 和 OSWorld Service
● 公共 Verifier 运行依赖
Trial State 则只属于当前任务：
● environment/
中的任务素材
● solution/
中供 Oracle 使用的参考解法
● Agent 对文件、应用和桌面造成的变化
● Agent 结束后注入的
tests/
● 日志和其他运行产物
这条边界首先影响效率。公共依赖可以提前构建和预热，Trial 启动时只注入任务相关内容，不必重复准备完整桌面。
但它同样影响实验解释。如果不同 Trial 的应用版本、桌面配置和公共依赖发生变化，那么 Reward 的差异究竟来自 Agent，还是来自 Environment，就很难判断。Baseline 因此不只是为了加快启动，它还决定了不同 Trial 能否在一致的环境条件下进行比较。Dataset、模型和 Agent 配置需要版本化，Environment Baseline 同样需要。
2.4
一条 Trial 必须拥有自己的外部状态
隔离的核心不是把任务文件放到不同目录，而是让一条 Rollout 产生的副作用具有唯一归属。对于只执行命令的任务，独立工作目录有时可以覆盖大部分状态。但 GUI Agent 会改变更多系统级和会话级状态：browser session、window focus、clipboard、应用偏好、home directory、background processes、desktop session 和 authentication state 都不天然受一个任务目录约束。Task A 打开的窗口、登录的账号或遗留的后台进程，仍然可能影响 Task B 的 Observation 和 Action。
在 Harbor + FC 云沙箱的实现中，这个状态所有权边界具体落成：
One Trial, One沙箱实例
每个 Trial 从独立 Sandbox 开始，Agent 与 Verifier 共同使用该实例，日志和结果回收后再将实例释放。公共 Template 可以复用，但任何可变状态不跨 Trial 复用。
三、Harbor + FC 云沙箱如何
把 Environment 变成可运行的基础设施
3.1
Harbor 评测体系的核心概念
在讨论 Harbor 与 FC 云沙箱如何衔接之前，需要先说明 Harbor 如何组织一次评测。Harbor 将评测过程拆成 Task、Trial Runner、Environment、Agent、Verifier 和 Result。它们之间的关系如下：
一个
Task
由独立的任务目录描述：
<task-dir>/
├── instruction.md     #
任务描述
├── task.toml          #
超时、资源、工作目录等配置
├── environment/       #
任务素材和环境初始化内容
├── tests/             # Verifier
使用的判分内容
└── solution/          #
参考解法，仅
Oracle
路径使用
Trial Runner
负责一次 Trial 的执行顺序和阶段状态管理。一次
harbor run
可以加载多个 Task，并按配置并发执行多个 Trial。
Environment
提供任务执行所需的生命周期、命令和文件能力。对 Harbor 来说，它是一组稳定接口；至于这些接口背后由本地容器、虚拟机还是远程 Sandbox 承载，不属于上层 Trial 的职责。
Agent
接收 instruction 和 Environment，在环境中执行任务。Harbor 约定 Agent 的调用接口，但不规定它使用什么模型，也不干预内部如何生成 Action。
Verifier
在 Agent 执行结束后检查 Environment 的最终状态，并据此生成 Reward。
Result
记录 Reward、日志和异常，也记录 environment setup、agent setup、agent execution、verifier 等阶段的状态与耗时。
Trial Runner 通过统一接口调用 Environment 和 Agent，不直接处理底层沙箱的SDK。正是这层边界，使 Harbor 原有的 Task、Trial 和 Verifier 流程可以保留，而执行环境能够替换成 FC 云沙箱。
3.2
系统三层架构：从抽象到落地
基于上述评测抽象，整套实现可以分成三个层次：Harbor 评测编排、Environment Adapter，以及 FC 云沙箱基础设施。
Harbor 管理的是 Task 和 Trial。它加载任务，调用 Agent 与 Verifier，处理阶段超时和并发，最后归集 Reward、日志与异常。FC 云沙箱承载的则是每条 Trial 对应的外部世界：具体沙箱实例的创建、持续访问和回收，以及实例内 command、file 和 GUI interaction 所需的数据路径。
Environment Adapter 位于两者之间。它实现 Harbor 的
BaseEnvironment
，把
start()
、
stop()
映射到 Sandbox 生命周期，把
exec()
、文件上传和下载映射到当前实例的数据面。上层 Trial Runner 因而不需要直接依赖 沙箱的SDK，底层执行环境也不需要理解 Harbor 的完整评测流程。
但 Adapter 最重要的工作是对齐两套系统对结果的理解。以 Verifier 执行命令为例。Harbor 需要得到 stdout、stderr 和 return code；沙箱的SDK 在部分非零退出场景下可能抛出带
exit_code
的异常。对评测来说，这里至少有两类完全不同的失败：Verifier 返回非零退出码，表示 Task 没有通过判分；连接失败、协议错误或执行超时，则表示 Environment 没有正常完成操作。前者是评测语义，后者是基础设施语义。Adapter 检查异常中是否存在
exit_code
：如果进程已经执行并结束，就把退出码转换成 Harbor 可以记录的
ExecResult
；如果没有退出码，则继续把连接或协议异常向上抛出。换句话说，任务失败与环境失败不是同一种状态。
FC 云沙箱承载的正是接口背后的东西：每条 Trial 对应的独立沙箱实例，包括它的生命周期，以及实例内部命令、文件和 GUI 交互的数据路径。
3.3
为什么生命周期管理和 Rollout 交互要分开
一条 100-step Trial 对 Sandbox 的操作并不均匀。生命周期相关的 create、get 和 kill 通常只有少数几次；Screenshot、Accessibility Tree、Mouse、Keyboard、Command 和 File 等实例内交互则会反复发生。前者回答“这个 Environment 是否存在”，后者回答“在它存在期间，Agent 怎样持续观察并改变它”。两类调用的频率、延迟特征和失败语义不同，因此 FC 云沙箱把它们分为 Control Plane 与 Data Plane。
Control Plane 管理沙箱实例的创建、查询、挂起、恢复与回收。Data Plane 面向已经创建的实例，处理命令和文件访问。OSWorld Service 不直接暴露公网地址，而是监听 Sandbox 内部的 loopback；Agent 先通过数据面进入 envd，再由 envd 访问 OSWorld Service，获取 Screenshot、Accessibility Tree 或执行 GUI Action。
Control Plane
Data Plane
管理对象
Sandbox Instance
的生命周期
已创建实例中的命令、文件和服务
典型操作
create
、
get
、
pause
、
resume
、
kill
exec
、
files.read
、
files.write
、
GUI interaction
主要阶段
创建、状态查询、恢复、回收
环境准备、
Agent
执行、
Verifier
执行、日志回收
这条数据路径还有一个直接结果：Harbor 的普通命令、Agent 的 GUI 交互和 Verifier 的判分请求最终都落在同一个沙箱实例，只是调用了实例内不同的服务。它们因此能够读写同一份 Trial State。
对 Agent workload 来说，Sandbox 不只是一个能启动实例的控制面产品。实例内部持续几十分钟、发生数百次往返的数据面，才是真正承载 Rollout 的执行路径。
3.4
一个 OCI Image 为什么还不是一个可复用的Environment
普通 OCI Image 能描述基础系统和应用文件，但它并不自动具备 Sandbox 数据面、桌面会话和可交互就绪语义。把它变成可批量运行的 GUI Environment，需要依次补齐 Runtime 约定、构建可复用 Template，并最终创建承载单次 Trial 状态的沙箱实例。
Image 回答“环境里有什么”：操作系统、桌面、应用和依赖都以文件的形式进入镜像。
Runtime 回答“环境怎样被稳定控制和访问”：镜像需要补充 envd、启动配置等 Runtime 约定，图形栈、GNOME Session 和 OSWorld Service 也必须在同一显示环境中运行。
Template 回答“哪些与具体 Task 无关的能力应该提前固化”。Runtime 适配、镜像转换、公共依赖和预热等固定工作在这里完成，后续 Trial 直接从同一 Baseline 创建实例，不进入重复构建路径。
Sandbox Instance 则回答“这一次 Trial 真正改变的世界在哪里”。每个实例从相同 Template 出发，接收自己的任务素材，并独立保存 Agent 留下的文件、桌面、应用和进程状态。
重点并不是某个图形后端本身，而是一个更一般的要求：Agent 看到的世界，必须是它实际操作的世界。镜像能启动桌面，只能说明里面具备相关软件；Observation、Action 和最终状态能够闭环，才说明它已经成为可驱动的 Environment。
3.5
从单个 Trial 到批量 Rollout
对 Harbor 来说，并发的基本单位不是一次模型请求，也不是一次 Sandbox API 调用，而是一条完整的 Trial。每条 Trial 都要依次经历 Sandbox 创建、Trial State 注入、Agent 执行、Verifier 判分、结果回收和实例释放。一个 Trial 结束以后，并发槽位才会被下一条 Task 继续使用。
因此，Harbor 中的
concurrency
实际控制的是
同时有多少条完整的 Environment 生命周期在向前推进
。例如
30 concurrency
，表示最多有 30 条 Trial 同时处于创建、准备、Agent 执行或 Verifier 阶段，而不是简单地同时发出 30 个请求。
这也带来一个直接的问题：Sandbox “创建成功”，并不等于这条 Trial 已经可以开始执行。
一个实例从资源分配完成，到真正能够承载 GUI Agent，中间还要经过桌面会话和相关服务的初始化。Command 和 File 可能已经可用，但 Screenshot 还拿不到有效画面，Mouse 和 Keyboard 也未必已经能够作用到 Agent 实际观察的桌面。对于 Coding Agent，这时可能已经足够开始工作；对于 OSWorld 这样的 GUI workload，则还不够。
因此，我们最终关心的不是单纯的
Resource Ready
，而是
Workload Ready
：当前 Agent 所依赖的 Observation、Action 和运行服务已经真正可用。在当前实现中，Harbor 不会用固定
sleep
去估计这个时间，而是通过实际的 health、screenshot 等能力判断 Environment 是否已经达到 GUI workload 所需的可交互状态。只有这一步成立，Trial 才进入后续 Agent执行。
这个区别在单条 Trial 中可能只是几秒钟的启动等待，但放到数百条任务和有限并发槽位里，就会直接影响 Environment 的周转效率：实例能否稳定进入 Workload Ready，决定了并发槽位是在真正执行 Rollout，还是大量时间耗在等待环境准备上。
因此，从单个 Trial 扩展到批量 Rollout，需要验证的不只是“Environment 能不能创建”，而是两件更具体的事：
同一套 Baseline 能不能反复进入可交互状态，以及大量完整 Trial 能不能在有限并发下持续周转。
四、从“能跑”到“能规模化”：用 OSWorld 验证 Environment
4.1
先验证完整性：这套
Environment 能不能跑完整个 Trial
完整性实验采用 OSWorld Verified 361 个任务，并使用较长的 100-step 配置：
配置项
配置
Benchmark
OSWorld Verified
Tasks
361
Model
Qwen3.6-Plus
Thinking
No Thinking
Observation
Screenshot + Accessibility Tree
max_steps
100
Concurrency
50
Sandbox Spec
4 vCPU / 8 GiB
Retry
0
两轮完整运行的结果如下：
指标
Run A
Run B
Tasks
361
361
完成判分
361 / 361
360 / 361
Mean Reward
0.383
0.397
Reward = 1.0
136
137
Trial Exception
0
1
这里列出 Reward，是为了完整交代实验结果，但这一轮首先验证的不是模型能力高低。更直接的问题是：前面定义的 Environment 生命周期，能否覆盖不同应用、不同任务和不同 Verifier，并在最长 100 步的交互后仍然把 Agent 留下的状态交给判分阶段。
Run A 的 361 条 Trial 全部完成判分；Run B 完成 360 条，出现 1 条 Trial Exception。两轮实验覆盖 OSWorld Verified 的全部任务域，说明 Harbor 调度、Sandbox 生命周期、GUI Observation / Action 和 Verifier 已经能够组成一条完整链路。它不是只能完成单个经过挑选的 Demo，而是能承载一套异构任务集合。
4.2
再验证可复制性：新 Environment 能不能稳定达到交互状态
第二层验证关注从 Template 创建的新 Sandbox，能否重复进入相同的可用状态。这里刻意拆开两个指标：
Sandbox.create()
返回，以及从发起创建到 Desktop Ready。测试不包含具体 Task 素材上传、Agent 推理和 Verifier。
Concurrency
Samples
Create P90
Create → Desktop Ready P90
1
10
1.25s
18.19s
10
10
1.15s
17.99s
20
20
1.27s
17.94s
Create P90
约为 1.2 秒，只说明 Sandbox provisioning 已经完成，并且 envd 很快可以提供命令与文件能力。
Create → Desktop Ready P90
约为 18 秒，才表示桌面会话、OSWorld Service、Screenshot 和 GUI Action 达到当前 workload 所需的交互状态，该启动时间数字为空载探针口径。
在本次 1、10、20 并发的测试范围内，两项 P90 都没有随并发提高而明显增长，且所有样本成功完成。这说明相同 Template 不只是可以创建多个实例，也能让这些实例重复进入相近的 GUI 可交互状态。
这说明从同一套 Baseline 出发，新 Environment 可以重复达到当前 workload 所要求的 GUI 可交互状态。复制的不只是计算资源，也包括这套 workload 正常开始执行所需要的运行能力。
4.3
最后验证规模化：数百条 Trial 能不能持续向前推进
最后一轮实验把关注点从单个 Environment 转到完整 Job。为了与 UI-Evol 公开实验的任务数量、最大步数和并发规模形成参照，本轮执行了
369 个 OSWorld Task
（相比于常见361题的版本，其中包含 8 道 Google Drive 任务，主要用于尽量对齐 UI-Evol 公开实验的任务规模和运行配置）
、15 steps、30 并发
的完整性能实验，每个 Sandbox 使用
4 vCPU / 8 GiB
。
本轮整体运行情况如下：
指标
结果
Tasks
369
Concurrency
30
Sandbox Spec
4C / 8GiB
Max Steps
15
Wall Clock
2h25m52s
Sandbox
总存活时间
246,033s
Sandbox-hours
68.34h
单
Trial Lifetime P50
629s
Mean Lifetime
667s
Max Lifetime
1991s
并发填充率
93.7%
68.34 sandbox-hours 相对于 30 个并发槽位和 2h25m52s 的完整 Job 墙钟，对应约
93.7% 的并发填充率
。也就是说，在本轮绝大部分运行时间内，并发槽位都由实际 Trial 占用，没有长时间停在 Environment 创建、等待就绪或任务切换阶段。
369 个 Task 均完成调度，其中
356 个完成判分，13 个在 Verifier 阶段发生
VerifierTimeoutError
。由于这一轮主要用于观察规模化 workload 的端到端执行和资源周转，因此这里以完整 Job 墙钟、Sandbox 资源使用量和并发利用率作为主要指标，不使用这一轮的 Reward 评价前面 100-step 配置下的 Agent 能力。
UI-Evol 公开实验同样采用
369 个 OSWorld Task、15 steps、30 个并发实例
，完整运行时间约为
2.5 小时
。两组运行规模对比如下：
项目
FC
云沙箱
UI-Evol / Azure
Tasks
369
369
Max Steps
15
15
Concurrency
30
30
Wall Clock
2h25m52s
约
2.5h
在任务数量、最大步数和并发规模三个主要参数对齐后，FC 云沙箱的完整 Job 墙钟约为
2.43 小时
，与 UI-Evol 公开的 Azure 运行时间处于同一量级。
需要说明的是，两组实验的 Agent、模型和具体执行实现并不完全一致，因此这里不把它作为严格的平台 A/B Benchmark，也不据此计算性能提升百分比。这个对照主要用于说明：FC 云沙箱已经能够承载与公开工作同规模的 OSWorld GUI Agent workload，并在约
2.5 小时量级
完成整轮执行。
Compute-only成本
除了 Job 能不能持续跑完，规模化运行还直接对应资源成本。
本轮所有 Sandbox 的累计使用时长为
68.34 sandbox-hours
。对于 4 vCPU / 8 GiB 的 FC 云沙箱Eco，按公开活跃态计算价格：
4 × ¥0.060 + 8 × ¥0.030 = ¥0.48 / h
因此，369 个 Task 本轮的 compute-only 成本约为：
68.34 × ¥0.48 = ¥32.80 / 轮
即约
¥0.089 / Trial
。
这里的成本只计算 CPU 和内存，不包含磁盘、模型 API、网络和其他外围资源，也不代表内部账号的实际账单。
为了给这个数字一个同规格的公开价格参考，UI-Evol 没有公开实际使用的 Azure VM SKU，因此无法直接还原其真实账单。这里选取 Azure Machine Learning 公开价格中的
F4s v2：4 vCPU / 8 GiB
作为同规格参考。
其 Linux Pay-as-you-go 公开价格约为
$123.37 / 月
。按 730 小时 / 月折算，约为：
$0.169 / 4C8G·h
按写作时汇率折算约为：
¥1.14 / 4C8G·h
因此，在相同 4C8G、compute-only、公开按量价格口径下：
平台
4C8G Compute
单价
Azure ML F4s v2
约
¥1.14/h
FC
云沙箱
Eco
¥0.48/h
按这一公开价格口径，FC 云沙箱Eco 的同规格计算单价约低
57.9%
。
进一步按整轮运行规模估算，UI-Evol 公开的
30 instances × 2.5h
对应约
75 VM-hours
。如果按上述 F4s v2 公开价格折算，对应约：
75 × ¥1.14 ≈ ¥85.50
FC 本轮实际累计使用
68.34 sandbox-hours
，按 Eco 活跃态公开价格估算约为：
68.34 × ¥0.48 ≈ ¥32.80
两者汇总如下：
项目
FC
云沙箱
Azure
同规格公开参考
Compute Spec
4C / 8GiB
F4s v2 4C / 8GiB
Resource Time
68.34h
75h
Compute Cost
¥32.80
约
¥85.50
按这一公开参考口径，FC 本轮 compute-only 成本约低
61.6%
。
需要说明的是，Azure 的
¥85.50
来自同规格 F4s v2 公开价格与 UI-Evol 公开运行规模的组合估算，并不代表 UI-Evol 的实际 Azure 账单。两边的数据集版本、Agent、Observation 配置也并不完全一致，因此这里不把成本差异解释为严格的平台性能或性价比加速比，只作为同规格公开价格和资源使用规模的参考。
把 Rollout 所需要的外部世界，变成基础设施
从一次模型调用走向持续交互的 Rollout，Agentic RL 对执行环境的要求也在发生变化。对于 OSWorld 这样的 GUI workload，Environment 已经不只是一台能够启动、远程操作的桌面，而要持续承载 Agent 对文件、应用和桌面造成的状态变化，并把这份状态一路保留到最终的 Verifier。
这次 Harbor on FC 云沙箱的实践，从 OSWorld 全量评测、GUI Environment 的重复创建，到数百条 Trial 的并发运行，验证了这样一套 Environment 可以从“跑通一个任务”，进一步变成可复用、可隔离、可批量调度的执行基础设施。随着 Agent 从 Coding 走向 Browser、Desktop 和更复杂的真实应用，
如何稳定地为每条 Rollout 提供一个独立、持续、可验证的外部世界，会成为 Agent Infra 越来越基础的一层能力。
