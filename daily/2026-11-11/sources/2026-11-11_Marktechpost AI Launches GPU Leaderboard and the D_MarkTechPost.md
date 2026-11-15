---
publish_time: 1794412274
link: https://www.marktechpost.com/2026/11/11/marktechpost-gpu-leaderboard-chrome-extension-launch/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Marktechpost 发布 GPU Leaderboard，一个免费的云 GPU 推理价格比对工具，读取各供应商官网的按需与竞价价格，按每 GPU 小时价格排序，并配套 Chrome 插件 Deploy It，帮助推理团队一站式回答“需要什么 GPU、哪里最便宜”。
---

# Marktechpost AI 推出 GPU Leaderboard 与 Deploy It 浏览器插件

> 原文链接：https://www.marktechpost.com/2026/11/11/marktechpost-gpu-leaderboard-chrome-extension-launch/
> 来源：MarkTechPost

Marktechpost has launched GPU Leaderboard, a free cloud GPU price comparison for AI inference. It also shipped GPU Leaderboard: Deploy It, a Chrome extension for the same data. The site reads on-demand and spot prices from each provider&#8217;s own pricing page. The goal is simple: answer &#8220;what GPU do I need, and where is it cheapest?&#8221; in one place.

What is GPU Leaderboard?

GPU Leaderboard is a pricing dashboard that ranks rentable cloud GPUs by price per GPU-hour. It is built for teams running inference. 

The v1 application has 4 views:

Inference pricing: a cost calculator for a full run, not a single hourly rate.

Leaderboard: every offer ranked by $/GPU-hr, filterable by GPU, tier, region and availability.

Cheapest Inference: the lowest on-demand floor for each tracked GPU.

Providers: a directory with instance counts, regions, status-page incidents and price-check history.

How does the GPU inference cost calculator work?

You pick an accelerator, GPU count, duration and utilization. The calculator then prices that exact run at every provider. An optional model field narrows the list.

The default example is 8×H100 for 72 hours at 90% utilization. That bills 576 GPU-hours. The cheapest result is $967.68 at Latitude, at $1.68 per GPU-hour. The median across 15 providers is $1,716.48. The most expensive is $3,545.28 at CoreWeave.

The calculator also shows a &#8220;real&#8221; cost per used GPU-hour. Idle time is still billed, so $1.68 at 90% utilization becomes $1.87. This is the number most budget sheets miss.

&&

What does the Deploy It Chrome extension do?

GPU Leaderboard: Deploy It brings the price data to where developers pick models. Per its store listing, it works in 3 places:

Hugging Face model pages: detects model size and estimates VRAM at FP16, INT8 and INT4. It then shows the cheapest hourly GPUs that fit.

GitHub repos: detects model references and gives a hardware estimate in place.

Toolbar lookup: search any model or GPU from the browser toolbar.

Key Takeaways

GPU Leaderboard ranks 201 live GPU offers from 24 providers by $/GPU-hr.

Its calculator prices a full run, including idle time at your utilization.

Deploy It shows VRAM needs and cheapest GPUs on Hugging Face and GitHub.

An 8×H100, 72-hour run spans $967.68 to $3,545.28 across multiple providers.

Coverage and daily refresh are the main gaps versus older trackers.

Try it at gpuleaderboard.com and install the Deploy It extension from the Chrome Web Store.

The post Marktechpost AI Launches GPU Leaderboard and the Deploy It Chrome Extension appeared first on MarkTechPost.