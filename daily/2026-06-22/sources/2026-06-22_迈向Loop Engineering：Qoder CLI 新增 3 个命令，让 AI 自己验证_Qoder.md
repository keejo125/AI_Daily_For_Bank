---
publish_time: 1782115200
---

# 迈向Loop Engineering：Qoder CLI 新增 3 个命令，让 AI 自己验证

> 原文链接：https://mp.weixin.qq.com/s/LXsftoveJ5QXimlzxzWWng
> 公众号：Qoder

最近社区在聊 Loop Engineering。核心意思很简单：别再一条一条手动写 prompt 了，你应该设计一个循环，让 agent 在里面自动跑起来。写代码、验证、修复、再验证，整个流程自驱动。

道理大家都懂。但实际用 cli 写代码的人都知道，这个 loop 总是到"验证"这一步就断了。

AI写代码很爽，你说需求，它改文件跑命令，一轮对话功能就有了。但是验收阶段总是最头疼的，你得切出去，手动把服务起起来，肉眼确认没问题，再切回来继续。

当然你也可以在对话里让 agent 帮忙验："帮我跑一下看看 /api/users 返回什么"。进一步可以把启动方式写进 AGENTS.md 或者搞成 skill。

这些都是对的，用 Loop Engineering 的话说，这就是把项目知识固化下来，减少和agent的重复沟通。

这次我们把这件事做进Qoder CLI 了。三个内置命令，分别解决 loop 里的三个问题：知识录制、快速观察、闭环验证。

/run-skill-generator — 录制启动 Skill

Loop Engineering 里有一个核心模块叫 Skills：把项目知识写下来，让 agent 不用每次都靠猜。

以前自己干这件事，你需要自己在 README 里写步骤，或者写prompt给Agent让它自己沉淀。现在可以通过下面一个命令让agent自动的扫描仓库，产出一个专属于项目的启动技能和driver脚本：

>

/run-skill-generator

以一个工作中常用的小工具TODO管理器为例，它是个有前后端的小应用，想把它跑起来验证功能，需要装依赖、起服务、用 curl 打到真实接口上看返回。

执行了上面的命令后，Agent会自主的探索整个仓库，将仓库项目的启动方法和环境配置摸清楚，随后把它们录下来：一份简短的 SKILL.md 指令，加一个 driver 脚本（shell、Node 或 Python，看项目用什么栈）。

它交付的是代码加文档。SKILL.md 是指令的 main page，driver 脚本才是下次 agent 能一键跑起来的东西。后面的run和verify命令可以直接复用。

其中driver的内容会按项目类型而不同：

Web 服务 / API：后台起服务，curl 打健康检查或关键接口，看 status code 和返回体

CLI 工具：跑代表性命令，检查退出码和 stdout

库 / SDK：写一段调公开 API 的 smoke 脚本，看输出是否符合预期

生成的文件在

.qoder/skills/run-<unit>

/ 下面，跟代码一起 git 提交，团队 clone 下来就能用。启动方式变了重新跑一次，自动覆盖。

生成的SKILL.md开头如下：

生成的driver脚本开头如下：

/run — Loop 里的快速观察

Loop Engineering 讲的循环是：写代码 → 执行观察 → 发现问题 → 修复 → 再观察。中间"执行观察"这一步，以前是你手动做的。现在你可以：

>

/run 启动项目和功能

cli 首先去

.qoder/skills/

下找有没有已经录好的启动配方。有的话严格按配方执行，没有的话按项目类型推断，以我们的简单的TODO管理工具为例，我们已经生成好了启动技能和脚本，本次run会直接使用它。

执行结果如下：

/run 会一直执行到能看见结果：启动服务，枚举case，调用接口，产生报告。尽量模仿人在验证过程中的动作。除此之外，你还可以根据自己的需要让它 run 各种各样的项目能力：

>

/run 试试 --output=json

>

/run 调一下 UserService.GetProfile

这样一来，你不用切窗口，不用记端口号，改完就让ai自己看，不对接着改。loop engineering 的节奏就是这样：ai自己改一下看一下，人在外面观察。

当然，如果没有执行过 skill generator。run每次都会重新调研项目如何启动，如果推断启动的过程中需要额外安装依赖、配环境变量，/run 会在报告里建议你跑一次

/run-skill-generator

把这些步骤录下来，下次就不用重来。

/verify — Loop 的闭合验证

/run 是写代码过程中随手看一眼。/verify 是提交前正经做一轮端到端验证。

>

/verify 验证一个有改动的功能

它做的事情跟 /run 完全不同。/verify 有一套完整的验证协议：

先确定范围

——用 git diff 系列命令搞清楚这次动了什么。

定位交互面

——变更怎么才能测试到？例如CLI项目在终端验，Server变更要查接口等等。

驱动执行

——找最短路径让修改的代码被触发，通过真实接口端到端走一遍。

边界验证

——确认正常路径之后，开始验证。新 flag 传空值试试、handler 发语法错误 body 、错误路径、接口幂等性是否满足 等等操作。

最后给报告：

PASS / FAIL / BLOCKED / SKIP。

还是以TODO管理器小工具为例，假设新增了todo的写入接口，可以使用verify命令验证他是否正常工作：

执行结果如下：

这样一来，每次变更都可以让agent自己通过verify来先做一边验证，将这个步骤嵌入到你的agent工作路径中，可以减少非常多人工验证的成本。

迈向 loop engineering

以前 cli 帮你写完代码，得切出去验证：起服务、看输出、回来告诉它哪里不对、改完再来一遍。一个小改动来回切两三次窗口很正常。

现在你可以直接让agent自己 /run，/verify，都做好了再向你汇报，将测试验证反馈循环不断地自动化解放人力。再进一步，还可以和其他各种命令配合使用，比如搭配 /goal 让循环自己跑，设一个目标让模型实现直到/verify 输出 PASS——cli 写代码、跑 /run /verify、发现不对自己改，循环到达标为止。

用起来

更新到最新的QoderCLI，进项目目录：

/run-skill-generator    ← 录制项目启动 skill + driver，跑一次就行

/run 看看首页           ← 改完快速观察，必须驱动不能仅启动

/verify 确认XX功能正常  ← 提交前闭环验证，含边界探测

Node.js、Python、Rust、Go、Java，Docker Compose 的项目都能用！