---
publish_time: 1794388999
link: https://www.infoq.cn/article/7wd1IyRiffi1vPz6goHS
source: 蚂蚁数科
status: confirmed
category: 国内
is_model_related: true
digest: |
  蚂蚁数科决策模型 LingDT-Decision 对 System One 协议扩展，首发信息抽取能力，可从句工单等上下文中抽取金额、日期等要素综合决策。该模型通过 mid-train 与强化学习适配产业侧精度与效率需求，信息抽取性能超过同尺寸乃至更大尺寸生成式模型，已在 DTMaaS 平台开放。
---

# 面向产业决策的升级：蚂蚁数科LingDT-Decision 首发信息抽取能力

> 原文链接：https://www.infoq.cn/article/7wd1IyRiffi1vPz6goHS
> 来源：InfoQ

以Jev为代表的决策模型仅能够处理单选、判断等问题类型， 然而产业决策过程中除了做选择判断，还需要从上下文中抽取部分信息来综合决策，例如金额，日期等，当前的决策模型暂时无法提供此类问题的解决方案。

针对此类问题， 蚂蚁数科决策模型LingDT-Decision对System One协议进行拓展，首发信息抽取能力。该模型通过mid-train、强化学习等技术深度适配产业侧对决策精度和效率的双重需求。

目前，LingDT-Decision模型的信息抽取性能已经超过同尺寸甚至更大尺寸生成式模型的效果，并且兼具速度优势和推理可靠性。LingDT Decision模型目前已在蚂蚁数科 DTMaaS"平台开放，Slotting功能可参考 DTMaaS 公开调用示例"进行免费体验。

以Jev为例：决策模型的能力边界

客服后台进来一条新工单：

订单 A123 多扣了 199 元，退款等了一周还没到。

系统需要判断工单派给谁，用Jev等决策模型处理上述工单，大致流程： 把客户原话放进 state，再在 questions 里问「这条工单该交给谁」，给出账单、物流、账号三个选项，然后调用请求：

{
"state": "订单 A123 多扣了 199 元，退款等了一周还没到。",
"questions": {
"department": {
"type": "choice",
"instructions": "这条工单最适合交给哪个团队处理？",
 "criteria": {
 "billing": "扣款、账单或退款问题",
 "shipping": "物流、包裹或配送问题",
 "account": "登录或账号设置问题"
      }
    }
  }
}

对应的响应如下所示，概率和置信度为示意值。

{
"answers": {
"department": {
"type": "choice",
"choice": "billing",
"probabilities": { "billing": 0.94, "shipping": 0.04, "account": 0.02 },
"confidence": 0.91
  }
 }
}

后台读到 answers.department.choice 是 billing，就可以把工单送进账单队列。

客服点开工单，得先找到客户说的「199 元」，再和扣款记录核对，但退款金额是一个开口的数值类型，难以使用选择、判断或者评分功能来提取。

System One模型从设计上来看，目前难以处理这种信息抽取类问题。

针对当前System One模型的缺陷，LingDT-Decision 在 System One 协议上新增了信息抽取功能，原生支持 extract 题型来处理信息抽取。应用指定要找「多扣金额」，模型可以返回对应的原文片段和位置，客服就能在工单里看到「199 元」被划出来。

不同System One模型支持的问题类型 

从jev的开源实现出发：答案究竟怎样被读出来？

思考一个问题，上述Jev响应里的三个概率是怎么来的？以Jev的开源实现Kev来看，整个过程可以拆成几步：

拼接输入 → 基座 Prefill → 取特定Token的向量 → 计算目标token的概率 → 返回结果，如下图所示：

先把请求拼成一条序列

 后面接工单原话， 后面接题目；每个候选的名字和描述用 、 包起来，最后放一个 。注：这里用便于阅读的标签表示特殊 token，实际看不同基座选取不同token。

订单 A123 多扣了 199 元，退款等了一周还没到。
这条工单最适合交给哪个团队处理？
billing: 扣款、账单或退款问题
shipping: 物流、包裹或配送问题
account: 登录或账号设置问题

Prefill 之后，选取特定位置Token的向量表示计算

基座模型对编码后的序列做一次前向计算，得到每个 token 位置的隐藏向量。针对Choice、Score、Noul问题取三个 和最后一个  位置的向量进行概率计算。首先把决策位 的向量经线性投影得到 q，三个候选结束位向量经同一个候选投影层得到 k₁、k₂、k₃。打分头用 q 和每个 kᵢ 做缩放点积，得到三个分数，然后基于任务的不同，计算每个选项的概率值。

从选择答案，到定位答案：信息抽取 怎样接上这套思路

还是以上述工单为例，问题从「交给哪个部门」换成了「多扣了用户多少钱」。前者有三个预设选项，而后者的答案就在客户原话里。LingDT-Decision 沿用了拼接输入 → 基座 Prefill → 取特定Token的向量 → 计算目标token的概率这条路径，解决信息抽取的问题，如下图所示：

请求怎么拼接？

如下所示，  放待抽取的文本，随指令一起送入的工单原文， 定义要找的字段。

 此处放历史上下文信息
从下面正文中抽取预定义的实体类型
订单 A123 多扣了 199 元，退款等了一周还没到。
overcharge_amount：这笔订单中多扣的金额，保留原文单位。

取哪些位置的token向量？

Prefill 之后，除了 和 ， 还需要抽标签内部的每个token的向量表示，用于后续的概率计算。

概率怎么算？

抽取头为原文的每个 token 给出三个分数：B 是片段的开头，I 是片段的延续，O 表示不属于这个片段。在同一个 token 的 B、I、O 三个分数之间利用softmax计算标签概率。与 Choice 给每个选项分配概率不同，这里概率是针对标签下的原文的每个位置进行计算的。

LingDT-Decision 的效果

LingDT-Decision整体性能

相比于其他决策模型，LingDT-Decision目前额外支持信息抽取和多选两种原生能力，并通过mid-train、强化学习、OPD等技术实现企业真实应用场景的深度对齐。在23项开源评测基准中，LingDT-Decision模型的综合评分超过了Microsoft-Decision-1、Jev 1.13等热门决策模型，其中27B的版本在同参数规模的模型中取得最高准确率。

（图注：LingDT Decision 的4B/27B 版本的优势区域，覆盖了相关尺寸包括Jev、MS Decision、GLiDE等决策模型，表现出极强的综合性价比）

信息抽取效果

选取信息抽取10个典型的bench进行评测，结果显示，目前LingDT-Decision模型的整体性能已经超过同尺寸甚至更大尺寸生成式模型的效果，并且兼具速度优势和推理可靠性。

（图注：图中均分为各数据集的macro F1）

单选和多选效果

覆盖23项主流开源评测基准的测试结果显示，LingDT-Decision的27B版本综合评分（90%x单选评分+10%x多选评分）位居第一，准确率超过Microsoft-Decision-1、Jev 1.13.0、Fastino/GLiDE等热门决策模型。

其中，在多选任务上，LingDT-Decision的4B和27B版本的准确率表现超过Microsoft-Decision-1、Jev 1.13.0、Star-lux等16个决策模型，体现出原生多选能力在多标签与组合判定任务中的优势，在单选任务上，位居第一梯队。

LingDT-Decision 的体验

请求和返回 

以前述工单案例为例，使用 LingDT-Decision解决抽取类问题，可按下列请求体提交请求：

{
 "state": ".....",
 "questions": {
  "overcharge": {
   "type": "extract",
   "instructions": "抽取这条工单中多扣的金额。",
   "criteria": {
   "overcharge_amount": "这笔订单中多扣的金额，保留原文单位。"
   },
   "context": "订单 A123 多扣了 199 元，退款等了一周还没到。"
    }
  }
}

返回结果如下所示：

{
 "answers": {
  "overcharge": {
  "type": "extract",
  "spans": [
   { "type": "overcharge_amount", "text": "199 元", "start": 12, "end": 17 }
   ]
  }
 }
}

LingDT Decision模型目前已在蚂蚁数科 DTMaaS"平台开放，Slotting功能可参考 DTMaaS 公开调用示例"进行免费体验。