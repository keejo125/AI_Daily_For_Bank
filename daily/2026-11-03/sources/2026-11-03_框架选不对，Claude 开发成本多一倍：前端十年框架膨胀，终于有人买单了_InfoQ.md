---
publish_time: 1793673484
link: https://www.infoq.cn/article/M6Q9I3DFrozJOREx9ztL
source: InfoQ
status: confirmed
category: 国际
is_model_related: false
digest: |
  资深 Web 开发者 Nolan Lawson 让 AI Agent 用 12 种 JavaScript 框架构建同一 Pokémon 应用并比较成本：最便宜的 Hono+htmx 中位成本 2.67 美元，Angular 达 4.97 美元、接近两倍；Token 消耗上 Angular 976 万、Hono+htmx 426 万，差约 2.3 倍。文章提出，当开发者不再逐行写代码，过去围绕开发体验的框架选型是否还应原样保留，值得行业重新审视。
---

# 框架选不对，Claude 开发成本多一倍：前端十年框架膨胀，终于有人买单了

> 原文链接：https://www.infoq.cn/article/M6Q9I3DFrozJOREx9ztL
> 来源：InfoQ

过去十几年，JavaScript 框架之间的竞争，主要围绕开发体验、运行性能和工程效率展开。React、Angular、Vue 等框架各自形成了庞大的开发者生态，框架选择往往与团队技术积累、开发习惯甚至技术偏好密切相关。

但当 AI Agent 开始承担越来越多的代码编写工作，这套评价标准可能正在发生变化：越来越多开发者开始关注哪种框架更适合AI Agent编程，能让模型更快完成任务、少消耗Token，同时生成更容易维护的代码？

近日，前Microsoft Edge浏览器性能项目经理、资深Web 开发者 Nolan Lawson 让 AI Agent 分别使用 12 种 JavaScript 框架构建同一个 Pokémon 应用，并从开发成本、Token 消耗、开发时间、最终产品性能和代码维护规模等维度进行了比较。

结果显示，同样的应用开发任务，最便宜的 Hono+htmx 中位成本为 2.67 美元，而 Angular 达到 4.97 美元，接近前者的两倍。Token 消耗方面，Angular 达到 976 万，Hono+htmx 为 426 万，相差约 2.3 倍。与此同时，不同框架生成的应用在 JavaScript 体积、浏览器主线程阻塞时间和代码规模方面也呈现出明显差异。

Lawson 借此提出一个值得整个行业重新思考的问题：当开发者不再亲手编写每一行代码，过去那些围绕开发体验形成的技术选型，是否还应该原样保留？

同一应用，Angular成本近翻倍，Token消耗超两倍

参与这次测试的有 12 个框架：Angular、Astro、Gracile+Lit、Hono+htmx、Next.js、Nuxt、Qwik、React Router、SolidStart、SvelteKit、TanStack Start，以及不使用 UI 框架、仅采用 Vanilla JavaScript/TypeScript 和 Vite 的方案。

实验统一使用 Claude Opus 5.5，并设置 High 推理强度，要求 Agent 使用对应框架的最新版本。每个框架原则上运行 5 次，每次都在独立沙箱中完成开发。作者没有提前告诉 Agent 应用将接受 Lighthouse 性能和可访问性测试，也没有指定必须使用 SSR 还是 CSR，更没有要求 Agent 必须采用特定的性能优化方案。

为了尽可能公平，Lawson 为各框架安装了官方提供的 MCP、Skills 或 Claude Code 插件（如果有），但没有强制 Agent 必须调用这些工具。CSS 方面，他没有限定具体方法，只要求不要使用 Tailwind、Bootstrap 或其他组件框架，并通过统一的设计规范保持视觉一致性。

为了尽可能控制变量，Lawson没有让Agent随意开发不同类型的项目，而是要求所有框架完成同一个基于PokéAPI的宝可梦图鉴应用。应用包含宝可梦列表、属性、技能和游戏版本数据，并支持搜索、筛选等功能。

需要说明的是，Angular有两次测试出现了特殊情况：Agent虽然生成了SSR应用，但应用拒绝来自localhost以外的访问，不符合测试要求。Lawson将其视为未按规范完成任务，没有重新运行。因此，代码规模和性能指标仅采用3次有效测试结果，而成本统计仍保留全部5次结果。

首先是最直观的开发成本。结果显示，Hono+htmx、Astro和Nuxt在AI构建成本方面表现突出：Hono+htmx以2.67美元排名第一，Astro为2.76美元，Nuxt为2.82美元；而Angular、Gracile+Lit和SvelteKit的成本相对较高。其中，Angular单次构建的估算成本达到4.97美元，接近Hono+htmx的1.86倍。

这些价格是Claude Code按照API价格计算的Token成本估算，并非 Lawson实际支付的独立账单。Lawson使用的是每月100美元的Claude Max套餐，因此测试本身属于订阅额度内的使用。

成本差异背后，Token 消耗和开发时间也呈现出相似趋势。

开发时间方面，Astro表现最好，单次构建中位数为8.2分钟，Hono+htmx为8.6分钟，Nuxt为9分钟。Angular则需要17.2分钟，是Astro的两倍还多。

Token消耗也呈现出类似趋势。Nuxt单次构建消耗约385万Token，Astro约413万，Hono+htmx约426万；Angular则达到976万Token，是Nuxt的约2.5倍。TanStack Start、SolidStart和React Router的Token消耗也相对较高，分别达到707万、713万和758万。

这意味着，即使使用同一个模型、相同的任务要求，选择不同的框架，Agent完成工作的成本和时间也可能出现明显差异。

不过，Lawson 也提醒，成本和 Token 数据存在较大波动。例如 React Router 的中位成本比 Hono+htmx 高约1美元，但前者最便宜的一次测试只花费2.82美元，仍低于后者最贵的一次3.19美元。因此，不能把单次测试的差异直接理解为框架之间必然存在固定的成本差距。

整体来看，SvelteKit、Gracile+Lit 和 Angular 的开发成本相对较高。其中，SvelteKit 的一个可能原因是版本较新，Agent 在每次测试中都会阅读 SvelteKit v3 迁移指南，可能是因为 Opus 5.5 的训练数据中缺乏足够的新版本信息。

Gracile 的情况更加明显，由于 Agent 对该框架不熟悉，有时会直接克隆整个代码仓库，甚至阅读 node_modules 中的编译后源码。Angular 的高成本则更多与最终生成的代码规模有关。

这也暴露出一个此前容易被忽略的问题：框架是否容易被模型理解，正在成为技术选型的新变量。

MCP、Skills没想象中好用，Agent甚至经常不看

为了避免某些框架因为缺乏 AI 工具支持而在测试中吃亏，Lawson 尽可能为各框架安装了官方 MCP、Skills 或 Claude Code 插件。但实验结果显示，Agent 对这些工具的实际使用情况并不稳定。

Lawson 认为，这种情况恰恰符合真实的 AI Coding 使用场景。普通开发者并不会每次都用大写命令反复要求 Agent 调用 MCP 或读取 Skills，很多人甚至根本不会主动配置这些工具。

此外，Lawson 还解释了部分测试方案的选择原因。Hono+htmx 是为了让 htmx 进入对比，同时将 Hono 作为一种 JavaScript 版的 Rails/Django 式方案；Gracile+Lit 则是为了代表 Web Components 生态。

对于 Vanilla，Lawson 要求 Agent 使用不带 UI 框架的原生 JavaScript 或 TypeScript，并通过 Vite 构建。结果却显示，原生方案的表现并没有优于所有框架，甚至在成本和 Token 消耗方面不如部分框架。

生成的应用也有性能差异

前面回答了“AI 写代码需要花多少钱”的成本问题，最终生成的应用性能则回答了：花了这些 Token，最后交付的产品质量究竟如何？

Lawson 使用 Lighthouse 对生成的应用进行了性能和可访问性测试。他认为，软件开发不能只追求低成本，还需要关注最终产品是否足够高效、易用。

首先，从 Lighthouse 的整体评分来看，12种框架的差距并不大。除了 Vanilla 的 CLS（累计布局偏移）为0.111、性能得分为97分，Angular 性能得分为98分、TanStack Start 为99分外，其余方案基本都达到了100分的性能和可访问性评分，CLS 也普遍为0。

由于整体评分已经非常接近满分，Lawson 进一步比较了 JavaScript 传输体积、总阻塞时间（TBT）和最大内容绘制时间（LCP）等具体指标。

在 JavaScript 传输体积方面，Astro 最轻，仅为0KiB（测试范围0—1KiB）；Vanilla 为7KiB，Gracile+Lit 为8KiB，Hono+htmx 为18KiB。相比之下，Next.js 达到142KiB，TanStack Start 为118KiB，React Router 为115KiB。

更值得注意的是 TBT。总阻塞时间衡量浏览器主线程被长任务阻塞的时间，数值越高，意味着页面在加载过程中主线程被占用的时间越长，可能影响用户的交互响应。

实验中，Astro、Gracile+Lit、Hono+htmx、SvelteKit 和 Vanilla 的 TBT 中位数均为0ms；TanStack Start 为1ms，Qwik 为3ms，SolidStart 为11ms，React Router 为17ms，Nuxt 为40ms。Next.js 达到71ms，Angular 则达到103ms。

Lawson 特别指出，TBT 并不完全取决于 JavaScript 传输体积。例如，Angular 的 JavaScript 传输体积为93KiB，低于 Next.js 的142KiB，但它的 TBT 反而更高。这说明，浏览器主线程的实际执行负担不仅与代码下载量有关，还受到代码解析、执行以及框架运行机制等因素影响。

在 LCP（最大内容绘制）方面，Astro 以810ms 位居第一，Gracile+Lit 为956ms，Hono+htmx 为978ms，Qwik 为979ms。Next.js 达到2090ms，TanStack Start 为2028ms，Angular 为1954ms。

LCP 的波动明显高于其他指标。Lawson发现，Next.js 的一次测试没有使用图片懒加载，而另外四次使用了懒加载，这直接造成了结果差异。Astro 和 Vanilla 也出现了类似波动，可能与资源优先级和 LCP 对最大元素的识别变化有关。

总体而言，LCP 测试更倾向于奖励能够快速返回 HTML 的 MPA（多页面应用），而不是需要等待客户端 JavaScript 执行、甚至还需要多次网络请求获取数据的 SPA（单页面应用）。从这次实验来看，LCP 在很大程度上与 JavaScript Bundle 体积相关。不过，Qwik 是一个例外：它采用客户端路由，技术上属于 SPA，但最终得分接近 MPA 方案。

不过，Lawson指出，Lighthouse 和 Core Web Vitals 本身就存在对 SPA 不够友好的倾向，因此不能直接将这组结果理解为 SPA 在所有应用场景下都不如 MPA。

代码越少，AI维护也可能越便宜

除了开发成本和最终产品性能，Lawson 还比较了各框架生成代码的规模，并将其作为衡量可维护性的一个简单指标。

他没有采用复杂的圈复杂度等指标，而是直接统计非空源代码行数。结果显示，Hono+htmx 只生成1370行代码，是所有方案中最少的；Nuxt 为1415行，Astro 为1461行，Next.js 为1539行。Angular 则达到2009行，是所有方案中最多的。

这组结果让Lawson 特别关注。他引用了 Svelte 创始人 Rich Harris 的一句话：“框架不是组织代码的工具，而是组织思想的工具。”

在 Lawson 看来，框架的意义本来就是减少需要维护的代码。但在 Agent 时代，这个问题变得更加重要，因为代码规模最终会影响 Token 消耗，不仅是最初生成代码时的成本，也包括未来每次修改、调试和重构时的成本。

在这次实验中，Hono+htmx 使用约1370行代码，就完成了与 Angular 约2009行代码相同的应用功能，代码量约为后者的68%，同时开发成本更低、速度也更快。

Lawson 也强调，简洁并不是框架唯一值得追求的价值，但在 AI Agent 成为主要代码生产者的背景下，框架能否减少代码规模，显然值得重新纳入技术选型标准。

以后怎么选框架？开发者吵起来了

Lawson在文章中提出，Web开发社区长期存在一个问题：技术选型经常依赖主观感受，而不是可靠的测试数据。某个框架被宣传为速度更快、开发效率更高，另一个工具则被认为更适合AI Agent，但这些结论往往缺乏足够的实验证据。

他认为，随着AI Agent逐渐取代开发者完成大量具体编码工作，过去围绕开发者体验建立的技术选型逻辑也需要重新审视。如果开发者不再亲自逐行编写代码，那么选择框架时，就应该更加关注Agent能否稳定理解文档、完成任务，以及最终生成的应用是否足够高效、易于维护。

Lawson 的实验发布后，立刻引发了社区的争论。有人要回归原生，有人认为框架反而更重要了。

一部分开发者认为，AI正在削弱传统框架存在的必要性。过去，框架最大的价值之一是帮助人类开发者组织代码、管理复杂状态和提高协作效率，但这些工作如今可以交给AI完成。对于内容展示、信息检索等交互相对简单的网站，直接使用HTML、CSS和原生JavaScript，可能比引入React等大型框架更加经济。有人甚至直言，既然AI已经能够写代码，就没有必要继续沿用过去为了方便人类开发者而建立的复杂技术体系。

另一派开发者则认为，框架在AI时代不仅没有过时，反而可能更加重要。有开发者分享，自己尝试让大模型使用原生JavaScript开发后，代码缺陷逐渐增加，最终重新选择React。React稳定的API和相对成熟的编程模式，更容易被模型理解，也有利于减少实现过程中的混乱。还有人认为，框架为长期项目提供了必要的工程约束，能够减少Agent在复杂代码中反复踩坑的概率。

讨论还延伸到了企业的软件工程管理。一名开发者认为，他分享了所在团队在不到5年内，从Backbone、Angular、React、Ember、Next.js、Vue、Svelte，最终又回到Angular和React的经历。频繁重构让管理者获得了新的项目成果，却可能留下仓促交付的代码和不断增加的技术债。过去十多年JavaScript框架频繁更迭，部分原因并不是业务真的需要，而是企业招聘、技术选型和管理层追逐流行技术共同推动的结果。

也有开发者反驳称，框架并不只是技术潮流的产物。对于商业软件和大型应用，框架背后还有持续维护的开源社区、成熟的组件生态和经过验证的工程实践。如果企业完全抛弃现有框架，转而自行构建状态管理、响应式更新和组件体系，最终可能只是重新发明一套维护成本更高的框架。AI虽然能够加速代码维护，却并不意味着软件维护本身已经消失。

不过，这项实验并不是一份可以直接用于所有项目的框架排行榜。测试只覆盖一个以内容展示为主、交互相对简单的宝可梦应用，并不能代表复杂仪表盘、邮件系统、设计工具或大型企业应用。Lawson 希望通过这次实验说明，在AI编程时代，技术选型依然可以通过数据和Benchmark来验证，而不是继续依靠社区口碑和主观判断。

对于已经高度依赖AI Agent的软件团队而言，这项实验提出了一个值得重新考虑的问题：过去开发者选择框架，是为了让自己写代码更舒服；未来选择框架，可能还需要考虑让AI写代码更省Token、开发更快、生成的代码更少，并且让后续维护成本更低。

有开发者分享，自己使用AI开发HTMX项目时，简单页面效果不错，但遇到复杂表单和状态管理后，Agent经常出现页面加载缓慢、状态丢失等问题。他认为，如果改用React，Agent可能一次就能完成。不过，他最终通过增加测试约束，让Agent逐步解决了这些问题，保留了HTMX方案，而且最终性能甚至超过了他认为React能够达到的水平。

相反，也有人认为，React的流行程度和大量现成代码示例，让模型更容易掌握其开发模式。技术栈是否适合AI，不仅取决于框架本身，还取决于模型训练数据、文档质量、工具支持和实际任务复杂度。

这场讨论没有统一答案，但一个变化已经比较明确：AI正在迫使开发者重新审视过去的技术选型标准。框架不再只是帮助人类更方便地编写代码，也需要证明自己能够帮助Agent更准确地理解项目、更少地生成错误，并降低后续维护成本。

参考链接：
https://nolanlawson.com/2026/10/28/the-ai-cost-of-javascript-frameworks/"
https://news.ycombinator.com/item?id=50323088"
https://github.com/nolanlawson"