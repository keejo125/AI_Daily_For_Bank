---
publish_time: 2026-08-02
source: InfoQ
title: "GitHub AI Agent翻车：攻击者只写一句话就能窃取数据"
link: https://mp.weixin.qq.com/s/Cq-em2gvtSrNtk0oSKD2gQ
category: 国际
is_model_related: false
status: confirmed
digest: |
  Noma Security发现GitHub新推出的Agentic Workflows存在提示注入漏洞GitLost。攻击者无需编程技能，只需在公开仓库创建Issue嵌入隐藏指令，即可诱骗AI Agent泄露私有仓库数据。漏洞利用关键词"Additionally"绕过了GitHub部署的防护机制——它将攻击载荷从"新指令"重新归类为"当前任务的延续"。研究人员指出，Agentic系统中信任边界部分依赖模型行为，提示注入正在变成AI时代的SQL注入。建议：用户控制的内容绝不应视为可信指令输入，Agent权限应严格限制在最小必要范围。社区评论："私有仓库从来不是安全边界——当读取代码的不再是你雇佣的人类时，它只是组织边界。"
---
# GitHub AI Agent翻车：攻击者只写一句话就能窃取数据

来源：InfoQ

原文链接：https://mp.weixin.qq.com/s/Cq-em2gvtSrNtk0oSKD2gQ

