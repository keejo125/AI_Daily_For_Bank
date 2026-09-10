---
publish_time: 1786427545
status: confirmed
category: 国内
is_model_related: false
digest: |
  智谱发布ZCode重大升级，新增Goal、Subagents、Remote Control和闲时任务四大功能。ZCode是针对GLM深度优化的国产Coding Harness，已成为百万开发者用GLM写代码的首选入口。智谱内部自研的Z.ai Code Bench评测显示，GLM+ZCode相比GLM+Claude Code在任务通过率上高出2.39%。

  文章强调"模型决定能力上限，Harness负责发挥"的核心理念——Harness管理上下文、工具调用、任务调度、缓存和结果校验，同一模型在不同Harness中表现可差很多。Z.ai Code Bench围绕真实用户需求场景，通过回归测试、前端模拟交互等多维度评估复杂长程编程能力，避免公开榜单的数据污染。GLM Coding Plan全体用户额度已于当日统一重置作为百万用户回馈。
link: https://mp.weixin.qq.com/s/NwVPQ8zsyIp8BC0Z1dN90g
source: 智谱
title: ZCode全面升级，GLM最佳Harness，让复杂任务自主交付
---

# ZCode全面升级，GLM最佳Harness，让复杂任务自主交付

来源：智谱
原文链接：https://mp.weixin.qq.com/s/NwVPQ8zsyIp8BC0Z1dN90g

ZCode是一款针对GLM深度优化的国产Coding Harness，已成为百万开发者用GLM写代码的首选入口。今天，ZCode迎来重大升级，Goal、Subagents、Remote Control与闲时任务四大功能正式上线。
作为百万用户里程碑的特别回馈，
GLM Coding Plan
全体用户
额度已
于今天13:00统一重置，
届时全员额度全部回满。
Z
Co
de，GLM的最佳拍档
模型决定能力上限，Harness负责上下文管理、工具调用、任务调度、缓存和结果校验，决定模型能力能发挥出多少。同一个模型放在不同的Coding Agent里，实际表现可能差很多。
在ZCode里使用GLM可以获得更好的任务表现。
智谱内部自研的Z.ai Code Bench围绕真实用户需求场景，基于Full Stack、Bug Fix、Feature Implementation等细分类别构造任务，模拟复杂的本地编程环境，通过回归测试、新功能测试、前端模拟交互、代码质量评估等维度对于模型的复杂长程编程能力进行全面评估，避免公开榜单可能存在的数据污染，力求还原用户真实体感。
在Z.ai Code Bench中，我们使用GLM-5.2，分别搭配ZCode、Claude Code进行测试。结果显示，GLM+ZCode相较于GLM+Claude Code，在任务整体通过率上高2.39%；在检查项通过率上，ZCode
低1.22%
。
ZCode的优势更集中在需要跨文件、跨环节协作并完成最终验收的复杂任务上
，能够更好地帮助模型把任务完整交付。
GLM用量接近翻倍
ZCode
对上下文缓存复用进行了
专门优化。根据我们对多款Coding Agent的测试，
GLM在ZCode中缓存命中率超过98%
，让更多重复上下文命中缓存，以更低的积分系数抵扣，从而让GLM Coding Plan有效Token量提升约30%。
即日起至2026年8月31日，在
ZCode中使用GLM Coding Plan还可获得1.5倍限时额度加成。两项效果叠加后，
整体使用量接近常规额度的1.8倍
。
此外，ZCode上线闲时任务功能，GLM Coding Plan用户提交闲时任务后，ZCode会
在低峰时段自动执行
，在闲时任务权益范围内，不扣减用户的GLM Coding Plan积分，适合不着急但耗时较长的任务。
ZCode让复杂任务自主交付
这次升级最重要的变化
，是让Agent可以自己把复杂任务跑完。
过去使用Coding Agent，开发者往往需要守在旁边不断推动：提出需求后等Agent回复，再让它继续修改；测试失败了要追问，发现遗漏还得重新补充上下文。
Goal模式改变了这一流程。
现在，只要给ZCode设定一个明确、可验收的目标，例
如：把首屏加载时间控制在2秒以内，并确保现有测试全部通过。
接下来，ZCode会自动拆解任务、修改代码、运行命令和执行测试，再根据文件、命令输出和测试结果判断目标是否完成。没有达标就继续下一轮，直到完成任务。每轮进度
、耗时和执行结果都能在Goal面板中一目了然。
Goal搭配使用Subagent，可以让一个 Agent 变成一支能够并行协作的开发团队。ZCode内置了两类子智能体：General-purpose可以修改代码、修复问题和运行命令；Explore主要负责只读探索，适合定位代码、分析调用链，以及在改动前收集证据。
用户也可以创建自
己的子智能体，配置模
型、权限范围和提示词，并在聊天框中通过“/”直接调用。
对于全栈功能开发、跨文件重构和复杂Bug定位，这种方式比让一个Agent从头做到尾更高效，也能减轻长任务对主对话上下文的占用。
把ZCode装进手机
Remote Control将当前ZCode桌面窗口临时开放给手机访问。
长任务在电脑上运行时，开发者可以通过手机查看进度、继续输入指令、创建新任务，或者重新连接断开的工作区。
除了扫码和浏览器链接
，ZCode支持微信、飞书、Lark，可以直接从微信或飞书会话中打开自己的工作区，跟踪 Agent 执行进度。手机只作为控制界面，代码和命令仍在桌面端原有环境中运行，不会将项目同步到
手机，也不会额外创建云端环境。本地、SSH、WSL和Docker工作区均可使用。
下载体验
ZCode最新版本下载：
https://zcode.z.ai/cn
完成安装并登录后，即可开
始使用，无需额外配置。
本次重置已生效，诚邀大家体验上述功能。使用过程中如有疑问或建议，欢迎加入ZCode用户交流群与我们交流，我们将第一时间为大家提供帮助。
