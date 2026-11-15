---
publish_time: 1792236992
link: https://mp.weixin.qq.com/s/czw36Fdn5Z58qhMcAkbpBw
source: 智东西
status: confirmed
category: 国内
is_model_related: true
digest: |
  智东西详细报道 DeepSeek V4.1-Flash 更新至 1017 版本：模型权重已在 HuggingFace 与 ModelScope 开放，并开放自研 Search 与 Fetch API（均定价 5 元/千次）。在 DeepSWE、Automation-Bench、Agents Last Exam、Apex Bench 四项测试领先 Kimi K3、GLM 5.3、GPT-5.6 Sol、Claude Opus 5；有海外开发者称其推理速度达每秒 244 Token，比 GPT-6.1 Sol 超快模式更快且智能接近 GPT-5.6 Sol。
title: 梁圣又掀桌了！DeepSeek新模型斩杀GPT-6，许愿式编程时代降临
---

# 梁圣又掀桌了！DeepSeek新模型斩杀GPT-6，许愿式编程时代降临

来源：智东西
原文链接：https://mp.weixin.qq.com/s/czw36Fdn5Z58qhMcAkbpBw

开发者喊它改名“V4.2-Pro”，DeepSeek这次更新有多猛？
作者 |
杨京丽
编辑 |
李水青
智东西10月17日报道，刚刚，DeepSeek V4.1 Flash更新至
V4.1-Flash-1017版本
，官方网页端、App与API已同步更新至新模型，模型权重也已在HuggingFace和ModelScope开放下载。DeepSeek还向公众开放自研搜索引擎的
Search（搜索）与Fetch（抓取）API
，两个接口均定价为
5元/千次
。
此次更新距离该模型发布仅过去一个多月。9月10日，
DeepSeek正式推出V4.1-Flash
，在性能上超越了DeepSeek-V4-Pro。
开源地址：
HuggingFace:
https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017
ModelScope:
https://modelscope.cn/models/deepseek-ai/DeepSeek-V4.1-Flash-1017
模型更新主要围绕
性能、任务执行效率和完整项目开发能力
展开。DeepSeek称，相比上一版本，新模型在多项基准测试中取得提升，同时缩短了任务运行时间与输出长度，让用户以更低成本、更快速度完成任务。
在衡量软件工程能力的DeepSWE、业务自动化能力的Automation-Bench、复杂任务执行能力的Agents' Last Exam，以及专业知识工作能力的Apex Bench四项测试中，新模型展现出较大优势，领先Kimi K3、GLM 5.3、GPT-5.6 Sol和Claude Opus 5等模型。
在DeepSWE v1.1测试中，新模型max档位的单次任务通过率达到77.0%，得分超
GPT-6 Astra、GPT-6.1 Sol、Gemini 3.8 Flash、Claude Opus 5
等模型，较V4.1-Flash上一版本提高2.8个百分点，每项任务平均费用则从约3.3元降至约1.3元，下降约六成。新模型在多个Harness下达到了
新的性能-费用帕累托最优
，即以更低成本取得更好的任务表现。
就在模型更新前两天，10月15日，DeepSeek曾发生
近5小时的API服务中断
。服务恢复后，DeepSeek致歉并公布补偿方案，将用户10月8日至14日的消耗金额以赠金形式全额返还，自动到账。
服务中断时，就有网友猜测是不是要发新模型了。如今，V4.1-Flash-1017正式上线，满足了大家的心愿。评论区中，大家讨论DeepSeek在“背着我们偷偷进步”。还有用户分享使用感受称：“模型突然变强了，几分钟就完成了自己的大作业。”
一位海外开发者称，DeepSeek-V4.1-Flash-1017的运算速度达到了每秒244个Token，这太不可思议了！它甚至比GPT-6.1 Sol的超快模式还要快，同时还拥有与GPT-5.6 Sol相当的智能；并真诚发问：开发出如此高效又便宜的模型有什么秘诀？
有的开发者甚至觉得：“这个模型都可以改名叫DeepSeek-V4.2-Pro。”
本次更新还针对DeepSeek Harness、腾讯CodeBuddy和WorkBuddy等平台框架进行了优化。DeepSeek Harness同步更新至0.2.1版本以适配新模型，官方建议用户升级至0.2.1-rc.1及以上版本。
符合活动条件的用户首次登录使用DeepSeek Harness，可获6元赠金，无需充值即可体验。赠金限量发放，到账后7天内有效。
在编程方面，新模型通过基于自反馈的强化学习（RL）训练，增强了从零构建完整项目的能力，覆盖游戏开发、3D建模等场景。
DeepSeek称，新模型支持用自然语言描述需求的“许愿式”编程请求。用户仅需较少提示词与参考素材，即可在较少交互轮次下完成项目。
▲官方案例1：故宫 3D 建模展示效果（图源：DeepSeek）
▲官方案例2：网页版赛车游戏开发效果（图源：DeepSeek）
模型更新后，有网友用新模型制作了“鹈鹕骑自行车”作品。画面采用复古旅行海报风格，以墨绿、浅绿与暖黄色搭配，将骑车的鹈鹕与海岸公路、灯塔等元素融合，整体构图完整、配色协调。但局部结构仍有瑕疵：自行车坐垫与鹈鹕身体的边界不清，似乎融为一体，脚部与脚踏的衔接也不够自然。
此外，搜索服务也是此次更新的另一重点。DeepSeek称，DeepSeek搜索已索引全球千亿级网页，每天处理数亿次搜索请求，支持多语言搜索，并针对SEO作弊、GEO操纵和低质AI生成内容进行过滤。
本次新版本发布DeepSeek API新增对Search（搜索）与
Fetch（抓取）
接口的支持，相关能力正式向公众开放。两个接口价格均为5元/千次。需要注意的是，目前用户在DeepSeek Harness、Claude Code和Codex中使用DeepSeek API时，通过服务端工具调用访问的Search/Fetch接口暂未计费，这部分调用将于北京时间11月1日00:00起按次收费。
