# Qoder Hooks 核心用法及8个实战案例

**来源**: 微信公众号「Qoder」  
**发布时间**: 2026年4月9日  
**原文链接**: https://mp.weixin.qq.com/s/Y9Wz88D-jjCM9cmh9-zXwQ

---

## 核心概念

Qoder Hooks 是 Agent 提供的**事件驱动扩展机制**，在 Agent 执行的关键节点注入自定义脚本逻辑。

**一句话理解**：hooks = Git hooks 的 AI 编程版，但触发时机更丰富，上下文更完整。

### 解决的核心问题

AI Agent 三大痛点：
- **不可控**：无法阻止危险操作，安全策略全靠个人自觉
- **不可观测**：不知道 Agent 做了什么，无法量化评估
- **不可进化**：经验散落在对话历史里，每次都是一次性对话

---

## 工作原理

```
Agent 执行关键操作 → 触发事件（Event） → 匹配规则（Matcher） → 执行脚本（Handler） → 放行/阻断/注入上下文
```

### 关键机制

| 机制 | 说明 |
|------|------|
| 放行与阻断 | exit 0 = 放行，exit 2 = 阻断（仅可阻断事件生效） |
| 上下文注入 | stdout 输出 JSON 向 Agent 注入额外信息 |
| 容错设计 | 脚本异常不会阻断 Agent，确保主流程不受影响 |
| 三级配置 | ~/.qoder/settings.json（全局）、.qoder/settings.json（项目级Git共享）、.qoder/settings.local.json（本地最高优先级） |

---

## 5种事件类型

| 事件 | 触发时机 | 可阻断 |
|------|----------|--------|
| UserPromptSubmit | 用户 Prompt 提交时 | ✅ |
| PreToolUse | 工具调用前 | ✅ |
| PostToolUse | 工具调用后 | ❌ |
| Stop | Agent 完成响应时 | ✅ |
| SessionStart | 会话开始时（规划中） | ❌ |

其中 **UserPromptSubmit、PreToolUse、Stop** 三种可阻断事件是安全管控和质量守护的核心能力。

---

## 8个实战案例

### 场景一：Prompt 增强 — 自动使用特定 Skill
- **痛点**：每次对话需要手动指定 Skill
- **方案**：UserPromptSubmit hooks 自动注入提示语，引导 Agent 优先使用特定 Skill
- **关键**：通过 session_id + 临时文件实现会话级去重

### 场景二：敏感 Prompt 禁止
- **痛点**：用户可能在 Prompt 中包含密码、密钥、内部 IP 等敏感信息
- **方案**：UserPromptSubmit hooks 做正则匹配检测，命中则 exit 2 阻断
- **关键**：建议将敏感词规则抽取到独立配置文件便于维护

### 场景三：Rule/Skill 使用情况分析
- **痛点**：配置了很多 Rule 和 Skill，不知道实际使用率
- **方案**：Stop hooks + Transcript 系统分析会话中 Rule/Skill 触发情况
- **关键**：Transcript 自动记录 session_meta(rules)、slash_command 等元信息

### 场景四：文件编辑情况分析
- **痛点**：不清楚 Agent 修改了哪些文件、修改了多少次
- **方案**：PostToolUse hooks 匹配 Edit|Write|search_replace|create_file
- **关键**：可对接代码统计系统，追踪 AI 辅助编码的变更量

### 场景五：使用情况全局分析
- **痛点**：缺乏 Agent 整体使用情况的量化数据
- **方案**：多事件组合 hooks（UserPromptSubmit + PostToolUse + Stop）
- **关键**：Stop 事件通过 Transcript 获取完整会话历史（模型回复、工具调用分布、成功/失败率）

### 场景六：安全管控 — 危险命令拦截
- **痛点**：Agent 可能执行 rm -rf、git push --force 等
- **方案**：PreToolUse hooks 匹配 Bash|run_in_terminal，正则黑名单拦截
- **关键**：Agent 收到阻断后会尝试替代方案

### 场景七：Agent 完成前质量检查
- **痛点**：Agent 声称完成任务，但测试未通过
- **方案**：Stop hooks（可阻断）执行编译、测试等质量门禁
- **关键**：stop_hooks_active 字段防止无限循环

### 场景八：Harness 自进化 — 资产沉淀自循环
- **痛点**：每次任务完成后的经验散落在对话历史中
- **方案**：Stop hooks 自动触发沉淀流程，分析对话产生可复用经验
- **关键**：可记录 pending-review.jsonl 供批量复盘，可与 /retro Skill 联动

---

## Transcript 文件格式

Qoder 自动生成的会话记录文件，位于 `transcript_path` 指向路径。每行一个独立 JSON 对象，按时间顺序追加。

### 记录类型

| 类型 | 说明 |
|------|------|
| session_meta | 会话开始时记录模式/类型/rules/slash_command |
| user (string) | 用户提问 |
| assistant (text) | 模型文本回复 |
| assistant (tool_use) | 模型工具调用 |
| user (tool_result) | 工具返回结果 |
| progress | hooks 触发记录 |

### 常用 jq 提取命令

```bash
# 提取所有用户提问
jq -r 'select(.type == "user" and (.message.content | type == "string")) | .message.content' "$TRANSCRIPT"

# 提取所有模型文本回复
jq -r 'select(.type == "assistant") | .message.content[ ]? | select(.type == "text") | .text' "$TRANSCRIPT"

# 统计工具调用分布
jq -r 'select(.type == "assistant") | .message.content[ ]? | select(.type == "tool_use") | .name' "$TRANSCRIPT" | sort | uniq -c | sort -rn

# 提取失败的工具调用
jq -c 'select(.type == "user") | .message.content[ ]? | select(.type == "tool_result" and .is_error == true)' "$TRANSCRIPT"

# 获取 hooks 触发记录
jq -c 'select(.type == "progress" and .data.type == "hooks_progress") | {event: .data.hooksEvent, command: .data.command}' "$TRANSCRIPT"
```

---

## 脚本输入参考

所有 hooks 脚本通过 stdin 接收 JSON 输入：

```bash
INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // empty')
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')
EMAIL=$(printf '%s' "$INPUT" | jq -r '.extra.email // empty')
```

### 环境变量

- `QODER_TOOL_INPUT_FILE_PATH`：工具操作的文件路径（PostToolUse 时可用）

### Matcher 工具名兼容

配置 matcher 时支持 Qoder 工具名和 Claude Code 工具名两种写法。

---

## 对我行的价值

Hooks 机制是智能研发助手从"工具"升级为"可管控的基础设施"的关键能力：

1. **安全合规**：敏感信息拦截、危险命令阻断，满足银行安全要求
2. **使用度量**：全链路数据采集，量化评估 AI 辅助研发效能
3. **质量守护**：自动化质量门禁，确保 Agent 输出质量
4. **经验沉淀**：资产自进化机制，降低人员流动影响
5. **团队管控**：项目级配置 Git 共享，统一团队标准

---

_存入知识库时间：2026-04-09_
