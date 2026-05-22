---
publish_time: 1779355800
---

# 断供OpenAI！Anthropic买下全球1/4开发者都在用的工具商

> 原文链接：https://mp.weixin.qq.com/s/fnYPL0TTroRiBCt0wCCwTw
> 公众号：新智元

新智元报道

【新智元导读】

刚刚，Anthropic买下了SDK工具公司Stainless，从开源MCP到收购Stainless，Anthropic的智能体棋盘已集齐模型、接口、连接三件套。

你也许没听过Stainless，但如果你用过Claude、OpenAI或Cloudflare的一些官方SDK，很可能已经间接用过它生成的代码。

除了OpenAI、Anthropic之外，Stainless的客户还包括Meta、Groq、Runway、Cerebras等，客户名单几乎覆盖了AI基础设施的全部头部玩家。

它就像是大模型和开发者之间的「翻译官」：把晦涩的API规范，转成开发者能直接上手的代码库。

现在，Anthropic将Stainless收入囊中，两家公司均已发布公告，确认收购完成。

Stainless创始团队将加入Anthropic，Stainless也将开始关停包括SDK generator在内的托管产品。

这不是一笔简单的工具公司收购。

Anthropic在收购Stainless的官方博客中提到，智能体的能力上限，取决于它能连接多少外部系统：收购Stainless，是在给智能体补强接口。

https://www.anthropic.com/news/anthropic-acquires-stainless

AI前沿正从仅能回答问题的模型，转向能够主动执行任务的智能体——而智能体的能力取决于它们所能触达的系统。收购Stainless，正是为了进一步拓展这一触达能力。

如果把这次收购与Anthropic过去 18 个月的动作链放在一起，智能体三件套已全部落子：Claude是模型，Stainless是接口，MCP是连接。

给多家AI巨头写SDK的那家公司

Anthropic买走了

2022年，Stainless成立于纽约，创始人Alex Rattray来自Stripe，在那里主导重做了API文档，并亲手搭建了Stripe的SDK代码生成系统。

他在做用户调研时发现，开发者从来不直接调用API端点：对他们来说，SDK就是API本身。

这个洞察，直接驱动他后来创立了Stainless，把这套能力做成了一个产品。

Stainless创始人Alex Rattray

开发者把OpenAPI规范丢给它，它输出Python、TypeScript、Go、Java、Ruby等多种语言的官方SDK。

模型公司自己只要维护一份API描述，剩下的所有语言版本、错误处理、重试逻辑、文档生成，Stainless全包了。

OpenAI、Anthropic、Meta、Cloudflare、DocuSign、Square，这些AI巨头或软件厂商都是Stainless的客户。

打开OpenAI官方Python SDK的GitHub仓库，README写着：「由Stainless基于OpenAPI规范生成」。

同样，Anthropic SDK的任意一个源码文件，文件头也标着：「由Stainless根据OpenAPI规范自动生成」。

也就是说，过去几年里，OpenAI和Anthropic这对宿敌，在官方SDK生成这一层，长期使用了同一家开发者工具平台。

被收购之后，

Stainless创始人

Alex Rattray对现有客户表示，此前生成的所有SDK完整所有权归客户所有，可自行修改和扩展，但Stainless不再提供后续支持。

Stainless团队将以Anthropic内部组织的身份继续工作，专注于Claude Platform能力建设及智能体与API的连接。

https://www.stainless.com/blog/stainless-is-joining-anthropic/

这家工具公司的产品，间接触达了全球约四分之一的专业软件开发者。加入Anthropic的第一天，就对整个行业关上了门：从共享基础设施，变成了Anthropic的一个内部部门。

智能体三件套集齐

模型、接口、连接

这次收购并非孤立事件。

把Stainless这笔收购放回Anthropic过去18个月的战略主线上看，三件套已经成型。

最底层的是模型。

从Claude 3.5 Sonnet一路打到Claude 4.7，编程和智能体能力是Anthropic一贯的差异化重点。Claude Code这一年也成了开发者圈子里最受欢迎的编程智能体之一。

中间是接口。

Stainless提供的SDK自动生成能力，让agent用统一规范调用各种API成为可能。这一层过去是外包，现在收归Anthropic内部。

最上面是连接。

2024年11月，Anthropic开源了MCP（Model Context Protocol，模型上下文协议），把模型与外部数据源、工具、文件系统的连接方式标准化了，让智能体不用为每一个外部服务单独写适配。

MCP开源之后，OpenAI、Google DeepMind、Cursor、Replit陆续宣布支持，MCP正在向智能体连接标准演进。

而Stainless恰好能把API规范直接生成MCP server。模型是大脑，接口是神经末梢，连接标准是把两端打通的协议。三件套合起来，才是一台能干活的智能体机器。

Anthropic负责平台工程的负责人Katelyn Lesse直言：「智能体有多大用，取决于它能连接什么。」

Stainless创始人兼CEO Alex Rattray说，Anthropic是最早押注Stainless的团队之一，「把两支团队放在一起，是一个容易做出的决定。」

这次收购，是一盘下了18个月的棋局里，最后一步落子。

一个「SDK翻译公司」凭什么3亿美元？

据The Information此前报道，这笔收购的谈判金额至少3亿美元。Anthropic官方未披露具体数字，但光是这个量级，就足以让人重新审视SDK这一层的价值。

在过去，SDK是个不起眼的工程问题。

API是模型公司的事，SDK只是把API翻译成各种编程语言的「包装层」。模型公司自己写也可以，外包给Stainless也可以，没人在意。

但智能体时代不一样了。当Claude或者GPT作为智能体去调用第三方服务的时候，SDK不再是「写给人看的工具」，而是「写给智能体用的接口」。

一个智能体任务能不能成功，很大程度上取决于它调用的每一个API的SDK是否健壮：错误处理是否完整、重试逻辑是否合理、参数定义是否严格、类型是否可推断。

任何一个不规范的SDK，都会让智能体在中途被卡死。

如果3亿美元级别的谈判金额属实，Anthropic看中的显然不只是一个SDK生成器，而是API到智能体之间那层开发者接口基础设施。

更微妙的一点：OpenAI、Meta、Cloudflare这些公司的官方SDK，过去都由Stainless生成。

收购完成、Stainless对外关门的第一天，这些公司就得面对一个现实问题：接下来的SDK维护，自己接手，还是另找供应商？

目前没有任何一方回应这一问题。

OpenAI卷模型

Anthropic 抢底座

回到ASI决赛双雄的格局里看，OpenAI和Anthropic的战略主线各不相同。

OpenAI的重心在模型代际和算力投入。

从GPT-5、GPT-5.4到GPT-5.5逐步更新，Stargate项目千亿级算力采购落地，ChatGPT周活跃用户从一年前的4亿涨到9亿，将资源重心放在C端入口和模型本身。

Anthropic走的是另一条路：企业端智能体基础设施。Claude Code做强开发者工具，MCP把连接协议标准化，Stainless则是把SDK层收编进来。

这两条路的底层逻辑完全不同。

模型层是代际颠覆的逻辑：下一代出来，上一代的优势可能瞬间清零。每一代之间的差距越来越小，窗口越来越短，只能靠算力和数据堆出来。

基础设施层的逻辑相反。一旦做成事实标准，复利就是长期的。MCP现在被全行业采用，每多一个采用者就增加一份切换成本。SDK这一层一旦内化进Anthropic，整个智能体生态对Anthropic的接口规范就可能形成路径依赖。

据Digital Applied统计，MCP公开服务器数量从2025年一季度的1200个增长到2026年4月的9400个以上，78%的企业AI团队已在生产环境中部署至少一个MCP智能体。

模型能力的差距，越来越容易追上。

连接层这个入口，一旦被锁住，就很难绕开了。

参考资料：

https://www.anthropic.com/news/anthropic-acquires-stainless%20

https://www.stainless.com/blog/stainless-is-joining-anthropic/%20

https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol

编辑：元宇

Moses

秒追ASI

⭐

点赞、转发、在看一键三连

⭐

点亮星标，锁定新智元极速推送！