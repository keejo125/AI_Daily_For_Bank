---
publish_time: 1784541217
---

# 谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同

> 原文链接：https://mp.weixin.qq.com/s/BYiSAp3I8W4YunklU_FraQ
> 公众号：InfoQ

作者 | Steef-Jan Wiggers

译者 | 明知山

最近，谷歌 Genkit（谷歌用于构建全栈式 AI 应用的开源框架）发布预览版 Agents API。该 API 将消息历史、工具执行循环、流式传输、状态持久化以及前端协议全部封装在一个

chat()

接口背后，无论智能体是在进程内运行还是部署在 HTTP 端点之后，该接口的工作方式完全一致。预览版现已支持 TypeScript 和 Go，Python 和 Dart 的支持也在计划之中。

其核心设计原则是：一个抽象层即可实现扩容，无需更换底层基础组件。同一个智能体对象可处理一次性应答、流式多轮对话、等待人工确认的暂停工具调用，以及独立运行的长耗时任务。当产品功能从简易聊天机器人迭代为多智能体协同工作流时，开发团队无需切换框架内其他组件。

Genkit 对两种大多数框架会混淆的智能体数据进行了区分。自定义状态：驱动下一轮对话的强类型应用数据，例如工作流状态、任务列表或已选择的实体。产物（Artifact）：可供用户单独查看、下载或版本管理的生成输出，例如报告、代码补丁或旅行行程。工具可通过当前会话更新任意一类数据，且 Genkit 会实时将数据变更流式推送至客户端。

状态持久化提供两种实现方案。服务端管理：配置会话存储后，消息、自定义状态和产物会以快照形式持久化保存，客户端通过会话 ID 重新连接。Genkit 内置了 Firestore（生产多实例）、内存（开发环境）和文件（本地测试）三种存储，并支持通过可插拔接口实现自定义存储。客户端管理：未配置存储时，服务端返回完整状态，客户端在每次对话轮次将其回传。

AI 工程师 Ebenezer Don 强调了这一架构选择在合规层面的意义：

若要为 AI 智能体增设记忆能力，核心难点在于维持上下文的稳定可靠。

关于客户端管理状态，Don 特别指出了服务端管理方案无法提供的数据驻留优势：

这种方式非常适合临时会话或有严格数据驻留约束的应用——服务端不应持久化用户数据。代价是会话增长后网络负载会增加。

在各类智能体框架层出不穷的当下，该框架有两项核心能力尤为突出。

分离式交互轮次支持客户端发起智能体任务后断开连接，后续再轮询获取结果。此外，智能体会在服务端持续运行，将进度写入快照，任意客户端均可读取这些快照数据：

const

chat = reportAgent.chat({ sessionId:

&#x27;report-123&#x27;

});

const

task =

await

chat.detach(

&#x27;Write the quarterly market report.&#x27;

);

savePendingSnapshot(task.snapshotId);

for

await

(

const

snapshot of task.poll({ intervalMs:

1000

}

))

{

renderStatus(snapshot.status);

if

(snapshot.status ===

&#x27;completed&#x27;

) renderMessages(snapshot.state.messages);

}

借助分离式运行能力，开发者可以创建长时间运行的研究任务、多步骤规划以及重度依赖工具的工作流——无需 WebSocket、独立的任务队列或保持连接持续打开。

另一项核心能力是可中断工具，它提供带防伪造保护的人机协同控制能力。当工具被标记为可中断时，智能体会在执行中途暂停，将待执行操作返回客户端，仅在用户批准或驳回后才恢复运行。运行时会结合会话历史校验恢复请求载荷，防止工具被伪造输入诱导执行。以下为 Go 语言示例：

runShell := genkitx.DefineInterruptibleTool(g,

"run_shell"

,

"Run a shell command after a safety check."

,

func

(ctx context.Context, input ShellInput, confirm *Confirmation)

(ShellOutput,

error

) {

if

isRisky(input.Command) {

if

confirm ==

nil

{

return

ShellOutput{}, tool.Interrupt(ShellInterrupt{

Command: input.Command, Reason:

"The command can modify files."

,

})

}

else

if

!confirm.Approved {

return

ShellOutput{}, errors.New(

"user rejected shell command execution"

)

}

}

return

execute(input.Command)

},

)

针对多智能体编排场景，的 中间件系统（已于五月份发布）会为每一个子智能体注入委派调用工具，编排主模型便可将请求拆分，分派给各专业子智能体处理。子智能体既可以本地运行，也能通过 HTTP 接口对外部署，二者共用同一个

chat()

接口。该中间件层还提供可组合的钩子函数，支持带指数退避策略的重试机制、跨提供商的模型降级、工具人工审核门控，以及技能体系 —— 该体系可读取

SKILL.md

文件并将内容注入系统提示词。

Genkit 通过其插件架构实现了模型无关性。官方插件支持谷歌 AI（Gemini）、Vertex AI、Anthropic、OpenAI 和 Ollama。Vercel AI SDK 适配器 让团队能够将 Genkit 智能体集成到 Next.js 应用中。所有智能体原生支持对外提供服务，路由辅助工具仅需少量代码即可在标准 HTTP 多路复用器上配置交互轮次、快照读取、任务终止三类接口。

目前同类智能体开发赛道竞争十分激烈。LangChain、CrewAI、Semantic Kernel、AutoGen、Mastra、Pydantic AI 等框架解决的业务场景高度重合。谷歌自身同时搭建了两层智能体基础设施：面向自建部署智能体应用的 Genkit，以及 Gemini API 托管智能体服务 —— 后者由谷歌托管运行环境，后台任务执行、远程 MCP 服务、沙箱代码运行等能力全部由服务端统一处理。放眼整个行业，Genkit 的核心差异化优势在于其全栈式开发方案：包含服务端智能体逻辑、适配网页与移动端的强类型客户端 SDK、内置流式传输协议，同时支持部署至 Firebase、Cloud Run，或是任意可运行 Node.js、Go 的环境。而短板在于 Genkit 面世时间较短，社区第三方集成生态的规模不及 LangChain。

Agents API 目前处于 预览阶段。中间件系统已面向 TypeScript、Go 和 Dart 语言正式发布可用版本。Genkit 在 GitHub 上基于 Apache 2.0 许可协议开源。

查看英文原文：

https://www.infoq.com/news/2026/07/genkit-agents-api-preview/

声明：本文由 InfoQ 翻译，未经许可禁止转载。

点击底部

阅读原文

访问 InfoQ 官网，获取更多精彩内容！

今日好文推荐

WAIC 进行时 | 图灵奖得主萨顿重磅演讲：大模型不具备原生智能，AI 正迈入“经验时代”

暂不跟进视频生成！Kimi K3 力压 Fable 5、登顶 Arena 榜单，提价近4倍对标Sonnet 5

马斯克连夜开源Grok Build，但84万行代码里还留着上传用户整个代码库的痕迹

微软用Go语言卷智能体了，谷歌也已入局，只剩OpenAI和Anthropic了