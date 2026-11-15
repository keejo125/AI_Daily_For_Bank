---
publish_time: 1791421440
link: https://www.qbitai.com/2026/10/501832.html
source: 量子位
status: confirmed
category: 国际
is_model_related: true
digest: |
  Anthropic 发布 Claude Haiku 5.5，小模型迎来“大逆袭”：官方跑分逐项超越 DeepSeek V4.1 Flash 与 GLM-5.3-Flash 等前代“斩杀线”模型，被定位为新的小模型守门员。其成本较前代 Haiku 4.5 显著降低（智东西称平均低约 75%），面向高吞吐、成本敏感任务，直接对标 OpenAI 的 GPT-6 Luna 轻量档。
---

# Claude 新模型发布：跑分暴击 GPT-6 Luna，价格比竞品更便宜

> 原文链接：https://www.qbitai.com/2026/10/501832.html
> 来源：量子位

Claude新模型发布！跑分暴击GPT-6 Luna，价格比梁文谷还便宜，OpenAI只能送重置卡挽尊
梦晨
量子位
小模型新守门员
梦晨 发自 凹非寺
量子位 | 公众号 QbitAI
Claude Haiku 5.5发布，小模型大逆袭！
单论跑分，直接超越两大前“斩杀线”DeepSeek V4.1Flash和GLM-5.3-Flash，成为新的小模型守门员。
一看官方跑分，好嘛，这就是冲着GPT-6 Luna来的，逐项赢过Luna。
由于鹈鹕骑自行车测试已经基本饱和了，最新干到战场的是奔跑斑马测试。
Haiku 5.5甚至价格也完全对标GPT-6 Luna。
上代Haiku 4.5还是刚好一年前出的，价格是5.5的10倍。
不过Haiku5.5的价格还有条件，提示词在10万token以内的请求（占Haiku 4.5请求量的90%），输入输出价格直接砍90%；超过10万token的部分，只砍50%。
这样一来，除了缓存命中的输入这一项，Haiku 5.5的价格也比DeepSeek-V4.1 Flash便宜了。
至此Opus 5.5管复杂推理、Sonnet 5.5管通用执行、Haiku 5.5管跑量和速度，群贤毕至，只差Fable了。
只能说隔壁OpenAI要是不努把力，Claude也没必要把Fable 5.5这管大牙膏挤出来。
仿佛回到了英特尔和AMD比拼CPU的日子。
换了tokenizer，耗费token更多
Haiku 5.5是第一个支持effort调节的Haiku模型，继承了系列从low到max的五档配置。
上一代Haiku 4.5在计算机操作和编码方面基本交白卷，这一代直接进化。
看OSWorld 2.1（测agent操作真实电脑完成多步任务）：Low档42.0%准确率、单次成本$0.07；Max档72.4%、$0.61。Haiku 4.5只有Max档15.7%、$1.45，
也就是说，5.5的Low档比4.5的Max档准，还便宜一半。
GDPval-AA v2.1（测44个职业的真实专业工作）也是类似曲线：Low档Elo 1125、$0.01；Max档1620、$0.87。4.5的Max档只有735、$0.24。
不过Haiku 5.5换了tokenizer（和Sonnet 5.5、Opus 5.5同款），同样任务会多耗费token，所以实际省的钱比标价折扣少亿点点。
特别是代码、表格、
非英语内容
的膨胀可能更高。
在AA测评中，Haiku 5.5虽然API价格便宜了，但“完成任务的平均成本”并没有到达理想区间。
替不了Sonnet
很多人对Haiku5.5的期待是能在部分任务替代Sonnet 5.5，进一步压低成本。
但这次并没有出现奇迹，小杯还是小杯。
Terminal-Bench 4.0上Haiku 5.5拿39.2%，Sonnet 5.5拿70.6%。复杂多步编码、跨文件重构、长周期自主规划方面差距非常清楚。
Anthropic自己也建议了，复杂agent编码优先用Sonnet 5.5或Opus 5.5。
Haiku 5.5的价值在执行层。任务已经拆好、验收标准明确、可以并行跑的任务。
比如Cognition的Devin用Opus 5.5做主模型、Haiku 5.5做子智能体，FrontierCode组合跑到了66.2%，比两个模型各自单跑都高。
如果你以前的业务用Haiku 4.5，这次不是换个模型名就能上线的。
budget_tokens手动思考配置直接报错，必须改成自适应思考加effort参数。
temperature、top_p、top_k全部锁定默认值，依赖采样参数做创意控制或多样化生成的应用要改逻辑。
assistant消息预填充被取消了，以前靠预填充强制JSON开头的写法得换工具调用或结构化输出接口。
计算机操作工具版本也更新了，从computer_20250124换成computer_toolset_20260801，接口格式和返回结构可能都不同。
另外自适应思考默认开启，响应第一个内容块可能是思考块而不是正文，解析逻辑要按type字段过滤。
五处变动，每一处都可能让请求直接报错或返回非预期结构。
Anthropic提供了迁移指南，建议切之前对着过一遍。
顺带两条福利
Sonnet 5.5的缓存读取从$0.20/M降到$0.10/M，Anthropic称大多数agent任务因此成本降约20%。
Max和Team订阅用户本周起可以领取API额度，Max 5x每月$100，Max 20x每月$200，Team最多$500/月在团队内共享。
这些额度可以用来实验调API建工具、应用、agent，所有模型通用。
神马？你说A社把我的买Coding Plan钱还给我，让我还可以在API上再用一次？
那么OpenAI在干嘛呢？OpenAI又送了一张重置卡。
参考链接：
[1]
https://www.anthropic.com/claude-haiku-5-5
[2]
https://x.com/AI_Screening/status/2107906044915749274?s=20
版权所有，未经授权不得以任何形式转载及使用，违者必究。
Claude
梦晨
Jev估值100亿美元！创始人Diogo Almeida回答一切
openJiuwen X-Router自演进模型路由技术首发，昇腾亲和，Agent越跑越省，实测减少50+%Token消耗
丘成桐新论文致谢了GPT和Claude
李飞飞创业公司被苏姿丰550亿收购！世界模型最大交易落地
扫码分享至朋友圈
相关阅读
新版Claude曝光：“极限推理”成最大亮点
预计未来几周发布
十三
Anthropic
Claude
AI“读书”合法了：美法院最新裁定，无需作者同意，已购书籍可用于训练AI
数据来源合法性>使用目的合法性
不圆
Anthropic
Claude
侵权
180万刀，连亚马逊都烧不起Claude了
Claude不是我说你，钱真不能这么花
程浅
Claude
亚马逊
两个AI关小黑屋：Llama3.1把Claude Opus聊自闭了
Claude能经受住心理阴暗面的诱惑吗？
西风
Claude
LLaMA
OpenAI和Anthropic罕见互评模型：Claude幻觉明显要低
网友：以后就这么搞！
十三
Anthropic
Claude
GPT-4
OpenAI
最强编码模型Claude 4！7小时不间断写代码，连玩24小时宝可梦，GitHub已选为Copilot底层模型
网友一次性用它写完俄罗斯方块
衡宇
AI编程
Claude