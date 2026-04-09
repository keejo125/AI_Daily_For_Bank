# Hermes Agent：开源自进化Agent平台

**来源**: 微信公众号「新智元」  
**发布时间**: 2026年4月9日  
**原文链接**: https://mp.weixin.qq.com/s/NrK1fbzqHTmqbz84IeZ9gQ

---

## 产品定位

Nous Research 2026年2月推出的开源Agent神器，被称为「会跟着你成长的Agent」。

- GitHub：4万+ stars，迭代到v0.8.0
- 更新速度：平均不到一周一个大版本
- 社区：240+贡献者，1400+合并PR

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 自主Agent | 运行在你自己的服务器上，每月5美元VPS即可 |
| 多平台接入 | Telegram、Discord、Slack、WhatsApp、Signal、SMS、飞书、企业微信 |
| 内置学习闭环 | 记忆→技能→训练数据三层闭环 |
| 定时自动化 | 类似cron的自然语言指令，后台无人值守执行 |
| 委派与并行 | 支持跨框架Agent联邦通信（Hermes ↔ OpenClaw） |
| 沙盒隔离 | 安全执行环境 |
| 全网页控制 | 浏览器自动化 |

---

## 三层学习闭环

### 第一层：记忆
- MEMORY.md：环境信息和历史教训
- USER.md：用户偏好和工作习惯
- 基于FTS5的跨会话检索 + LLM摘要

### 第二层：技能
- 完成复杂任务（5+工具调用）自动创建skill
- 包含操作步骤、常见陷阱、验证方法
- 使用中发现更好做法自动更新

### 第三层：训练数据
- 批量轨迹生成
- Atropos强化学习环境
- 工具调用记录直接用于训练下一代模型

---

## 典型应用场景

1. **自动化情报监控**
   - 自然语言cron指令：「每天早上8点扫描GitHub仓库新release，摘要发Telegram」
   - 已有用户搭建横跨Reddit和X的AI趋势日报

2. **带记忆的编程**
   - 记住代码库结构、命名习惯、部署流程
   - 6种终端后端，云端VM持续干活

3. **多平台无缝切换**
   - 手机Telegram发起对话，电脑终端无缝接续
   - 语音备忘录自动转写处理

---

## 版本演进路线

| 版本 | 发布日期 | 主题 | 重点 |
|------|----------|------|------|
| v0.5.0 | 2026-03-28 | hardening release | 50+安全修复、供应链审计 |
| v0.7.0 | 2026-04-03 | resilience release | 可插拔记忆架构、凭证池轮换、168个PR |
| v0.8.0 | 最新 | intelligence release | 后台任务自动通知、模型实时切换、MCP OAuth 2.1 |

**核心判断**：长期运行才是Agent真正的工程挑战（不是「不够聪明」，而是「跑着跑着崩了」）

---

## 模型支持

- Nous Portal、OpenRouter、OpenAI、Anthropic、Google Gemini、xAI、z.ai、Kimi、MiniMax
- 本地Ollama及任何OpenAI兼容端点
- `hermes model` 随时切换，不锁定厂商

---

## 快速上手

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 初始化
hermes setup          # 选择LLM提供商、填API Key
hermes gateway setup  # 接入消息平台
hermes gateway install # 注册系统服务（24小时在线）

# OpenClaw迁移
hermes claw migrate   # 一键导入设置、记忆、技能
```

---

## 生态体系

| 项目 | 说明 |
|------|------|
| agentskills.io | 开放技能标准，跨项目/社区共享 |
| Skills Hub | 官方技能市场 |
| HermesHub | 带安全扫描的第三方技能市场 |
| hermes-workspace | 网页端GUI |
| mission-control | 多Agent管理面板 |

---

## 背后的团队

**Nous Research**
- 2023年成立，约20人
- 累计融资6500万美元（Paradigm领投A轮5000万）
- 创始人：Jeffrey Quesnelle、Karan Malhotra、Teknium、Shivani Mitra
- 原工作：训练大模型（Hermes、Nomos、Psyche三个开源模型家族，下载量5000万+）

**关键洞察**：训模型的人亲自做Agent，Agent产生的数据又能回流训练——这是设计而非巧合。

---

## 对我行的价值

1. **私有化部署**：数据留在用户手里，符合银行安全合规要求
2. **技能沉淀机制**：自动从经验中提取可复用技能，降低人员流动影响
3. **训练数据闭环**：Agent使用数据可用于模型训练，形成自进化系统
4. **多平台接入**：飞书、企业微信等国内平台支持
5. **开源可控**：4万+ stars社区活跃，可定制改造

**关键启示**：智能研发助手不应只是「一次性调用接口」，而应该是「私有、常驻、会积累、能反哺训练」的系统。

---

_存入知识库时间：2026-04-10_
