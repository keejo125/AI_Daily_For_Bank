---
publish_time: 1787913060
link: https://mp.weixin.qq.com/s/FbCnWDuw_E6Wt6YqX6J7Cg
source: 量子位
status: confirmed
category: 国内
is_model_related: true
digest: |
  阿里千问发布并开源Qwen 3.8 Flash-Next，采用125B MoE架构、每Token激活约6B参数，原生支持26万token上下文、可扩展至1M，价格低至每百万输入0.8元、输出2.7元，为DeepSeek-V4-Flash的约1/3。实测可在消费级4090显卡运行，并在相机文案、会议纪要与方案生成等办公任务中表现强悍，被视为Qwen4新架构预演。
title: 实测比DeepSeek便宜的Qwen 3.8 Flash，卷飞了
---

# 实测比DeepSeek便宜的Qwen 3.8 Flash，卷飞了

来源：量子位
原文链接：https://mp.weixin.qq.com/s/FbCnWDuw_E6Wt6YqX6J7Cg

文婷 发自 凹非寺
量子位 | 公众号 QbitAI
阿里千问新模型，又卷出了新水平。
他们发布并开源的Qwen 3.8 Flash-Next，不仅
价格直接秒杀了DeepSeek-V4-Flash
，而且
刚发布便摘得了Huggingface榜首！
推上网友们也沸腾了，甚至还有工程师甩出实测视频直呼牛逼：
Qwen 3.8 Flash踏平了VRAM的门槛，
数据中心级的长文本大模型，在消费级4090显卡上也能跑了！
还有人已经兴冲冲地把它用到了工作中。
不到8分钟，它就跑完了涵盖Python编程、多表分析和研究报告生成的一整套工作流
：
宝塔特效也不在话下：
哇奥，真有这么炫？我们当然也得上手试试。
每百万Tokens输入仅0.8元
Qwen3.8-Flash采用了
125B MoE架构
，每Token仅激活约
6B参数
，原生可支持
262144token上下文
，并
可通过YaRN扩展至1M token
。
同时，它也
是Qwen4新架构的提前预演
。
相比于Qwen 3.7 Plus，Qwen 3.8 Flash不光
把激活参数砍到了1/3
，
训练成本也仅为其1/9
，且通用、数学推理、编程等能力都更加强悍了。
更狠的是价格，Qwen 3.8 Flash
每百万Tokens输入仅0.8元
，
输出2.7元
，
缓存命中0.1元
，价格最低至DeepSeek-V4-Flash的
1/3
。
真是比拼多多砍一刀力度大多了（bushi
好吧好吧，既然价格已经卷到了这个份上，那咱也不客气了，直接上强度，用两个实测来探探Qwen 3.8 Flash在办公场景实际的干活能力吧。
实测一：为相机产品设计四种适配不同风格平台的文案
我们设计了一场“赛博文案挑战赛”，让Qwen 3.8 Flash在1元的额度内，将一份近万字的相机产品资料改写成小红书、微博、抖音和朋友圈文案，看看它究竟能完成多少项任务。
提示词如下：
发完提示词之后，我就去公司茶水间打了个水，
全程不到2分钟
。
回来一看，四份不同平台的文案都已经全部写好了，并且@对了品牌、风格、话题词条拿捏得准准的（除了我不会那么发那么长的朋友圈之外hhh）：
不到2分钟肝完四份文案，“赛博打工人”的手速算是过关了。
但职场里真正让人头疼的，往往不是写文案，而是
开完会之后谁来把一地鸡毛整理清楚。
于是，我们给它安排了第二份工作，考验它的实战办公能力。
实测二：把一场产品周会变成可执行方案
我们以
“智能客服Agent V2.0 需求与技术评审会”为主题
，原汁原味复刻了一份大家刚开完周会后可能会拿到的、同音错字多且穿插着琐碎闲聊的万字原始会议实录材料，并
让Qwen3.8-Flash一次性完成了提取总结、整理表格和会后通知邮件三项工作。
△
图片由AI生成，“token”听成“偷啃”真是太有生活了
提示词如下：
默认模式下，
不到4分钟，Qwen3.8-Flash就圆满完成了所有任务
，且五条核心结论总结、表格分工内容均准确无误，邮件格式规范，收件人也与会议内容一一对应。
△
部分测试结果图
甚至没有要求它，它也会自行贴心地给我们梳理出了会议中尚未讨论出结果的事项
、方便我们下次开会继续讨论，be like：
而且到这一步，我的额度还没烧完哦！
啊哈哈这种不受限的感觉真是太爽了。
现在，
Qwen 3.8 Flash已经在“千问办公”平台首发上线，API接口也已同步开放
，大家可以去试试啦！
One More Thing
国产大模型价格战打得更猛了。
就在Qwen 3.8 Flash开源的几乎同一时间，智谱也开源了GLM-5系列首个原生多模态模型
GLM-5.3-Flash
，也就是之前在网上爆火的“牛来”大模型
Ox Alpha。
测评中，该模型的
性能比肩Claude Opus 4.8，价格却砍到了GLM-5.3的1/10。
而且GLM-5.3-Flash还慷慨地开放了
为期两周的半价活动
，这意味着，
活动期内的GLM-5.3-Flash的价格仅为GLM-5.3的1/20，为Opus4.8的1/40。
此外，Qwen 3.8 Flash和GLM-5.3-Flash还有一个
共同点
，那就是他们这次都以超低的价格杀了DeepSeek-V4-Flash个措手不及（DeepSeek骂骂咧咧地走开了）：
△
DeepSeek-V4-Flash、Qwen 3.8 Flash、GLM-5.3-Flash价格对比图
没得说，太卷了。
参考链接：
[1]https://qwen.ai/blog?id=qwen3.8-flash-next
[2]https://huggingface.co/models?inference_provider=all&sort=trending
[3]
https://www.qianwenai.com/?source_channel=hy_qwen&utm_content=g_1000415132
[4]https://x.com/Alibaba_Qwen/status/2092591393424515114
[5]
https://mp.weixin.qq.com/s/O7RCVME1Kut-Z2oFYhgrkw
一键三连
「点赞」「转发」「小心心」
欢迎在评论区留下你的想法！
—
完
—
🌟 点亮星标 🌟
科技前沿进展每日见
