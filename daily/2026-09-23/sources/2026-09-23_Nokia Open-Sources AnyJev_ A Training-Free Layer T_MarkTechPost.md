---
publish_time: 1790147378
link: https://www.marktechpost.com/2026/09/23/nokia-open-sources-anyjev-a-training-free-layer-that-turns-any-open-llm-into-a-calibrated-decision-model/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  诺基亚应用研究团队开源 AnyJev，一个把开源 LLM 变成决策模型的 Python 库，无需训练。它借用了 TypeSafe AI 的 Jev 接口，给定类型化问题即可返回带阈值概率的决策，概率直接从模型 next-token 分布读取。支持选择、评分、比较三类问题，已上 PyPI、采用 Apache-2.0 许可。
---

# 诺基亚开源 AnyJev：无需训练即可将任意开源 LLM 转为决策模型

> 原文链接：https://www.marktechpost.com/2026/09/23/nokia-open-sources-anyjev-a-training-free-layer-that-turns-any-open-llm-into-a-calibrated-decision-model/
> 来源：MarkTechPost

Nokia&#8217;s applied research team has open-sourced AnyJev, a Python library that turns an open LLM into a decision model. It needs no training. It targets a common production job: picking one answer from a fixed set instead of writing a sentence. 

Is it deployable? Yes, it installs from PyPI, ships under Apache-2.0, and has transformers and vLLM backends with shared-prefix scoring. 

What is AnyJev?

AnyJev borrows its interface from Jev. Jev is the System One decision model that TypeSafe AI launched in September 2026 (our coverage). You give AnyJev a typed question and get back a decision with a probability you can threshold. That probability is read from the model&#8217;s next-token distribution. Nothing is generated, parsed, or trained.

The library supports 3 question types:

A choice question picks one of K options. 

A noul question is yes or no. 

A score question places the answer in one of several ordered bins.

The Problem With Reading Logits Directly

Many open projects already restrict the next token to the option labels and read the scores. The Nokia research team flags 2 flaws in that shortcut. First, the answer can change when the options are reordered. Second, the probabilities are not calibrated.

The levels doc names 2 causes: 

The first is prior bias: the model favors some labels, such as &#8220;Yes&#8221; over &#8220;No&#8221;, whatever the input. 

The second is position bias: the model favors certain slots in the option list.

How AnyJev Works: L0 and L1

Every decision carries a level field.

L0 (zero labels, on by default) applies 2 fixes:

Cyclic shifts. For a question with K options, the list is shown in K rotations, so every option appears in every position once. The results are combined in log space as a geometric mean. If the position bias is additive in logit space, this removes it exactly.

Prior correction. By default, AnyJev uses batch calibration. It keeps a running mean of the predicted distributions on real inputs and divides it out at strength 0.75. The correction starts after 8 items.

L0 costs K prefills per decision, batched over a shared prefix. That is about 0.25 s per decision at batch 32 on one H100, with K = 20.

L1 (100 to 500 labels per question) adds temperature scaling on top of L0. The fitted values are saved as a small JSON artifact. L1 reshapes confidence but does not change the ranking of answers.

Benchmark Results

On Qwen3-8B with BANKING77 (20-way, 300 test items), the numbers look like this:

MetricRaw logitsAnyJev L0AnyJev L1Labels required00100 to 500Flip rate when options reversed0.2300.0730.077Accuracy0.7470.8030.807Calibration error (ECE)0.2400.1840.095Auto-decidable at 5% error7.7%46.3%52.0%

A few other results from the repo:

L0 reduced order flips on all 9 model and task rows tested.

On a typed-decisions set, Qwen3-32B with L1 reached an ECE of 0.036, compared with 0.144 published for Jev. On accuracy, the fine-tuned Laya still leads.

The full ablation table covers Qwen, OLMo, Granite, Phi and Mistral models.

Wu says the team tried AnyJev on an internal Nokia routing problem and saw promising results.

How to Use AnyJev

Copy CodeCopiedUse a different Browser

# pip install "anyjev[hf]"
from anyjev import Decider, Question
from anyjev.backends.hf import HFBackend

d = Decider(HFBackend("Qwen/Qwen3-8B"))
route = Question.choice("Which team should handle this?",
                        ["billing", "technical", "sales", "other"], name="route")
r = d.decide({"conversation": [...]}, [route])
r["route"].distribution   # probabilities per option

For serving, you start vLLM with prefix caching and point a VLLMBackend at it.

&&&

Key Takeaways

AnyJev turns open LLMs into Jev-style typed decision models with no training.

L0 uses cyclic shifts and a batch prior to remove position and label bias.

On Qwen3-8B BANKING77, the order-flip rate falls from 0.230 to 0.073.

Auto-decidable traffic at 5% error rises from 7.7% to 52.0% with L1.

It is Apache-2.0 on PyPI, with Hugging Face and vLLM backends.

Check out the GitHub Repo. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Nokia Open-Sources AnyJev: A Training-Free Layer That Turns Any Open LLM Into a Calibrated Decision Model appeared first on MarkTechPost.