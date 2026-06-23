---
publish_time: 1778148517
---

# 灵码 Hooks：让 AI 按你的规矩办事

> 原文链接：https://mp.weixin.qq.com/s/1LebNSQKdfn5LsMriop62Q
> 公众号：灵码Lingma

用 AI 写代码越来越爽，但你有没有这种感觉——

Agent 帮你写完代码直接就"收工"了，不跑测试、不做检查，每次都得自己追一句"跑一下单测"；提示里不小心粘了一段 access_key，这次注意到了，下次呢？Agent 生成

rm -rf /data/

，手一滑点了确认，几个 G 的数据说没就没。

你开始意识到：

AI Agent 越强大，就越需要"规矩"。

传统开发有 Git hooks、CI/CD、代码审查来管控流程。AI 编程同样需要一套机制——在 Agent 执行的关键节点注入自定义逻辑，让它按照你的方式干活。

这就是

灵码 Hooks。

01

什么是灵码 Hooks？

Hooks 是灵码 Agent 提供的

事件驱动扩展机制

，让你可以在 Agent 执行的关键节点——如用户提交提示、工具调用前后、Agent 完成响应等——

注入自定义的 Shell 脚本逻辑。

一句话理解：

Hooks = Git hooks 的 AI 编程版

，但触发时机更丰富，上下文信息更完整。

具体来说，灵码 Hooks 可以做到：

安全防线：

拦截危险命令、屏蔽敏感信息泄露

质量守护：

Agent 完成任务前自动跑测试、做检查

效率倍增：

自动注入项目规范、加载上下文，减少重复沟通

行为可观测：

记录 Agent 的每一次操作，量化 AI 辅助开发效果

02

工作原理

灵码 Hooks 的执行流程非常直观：

Agent

执行关键操作 → 触发事件（Event） → 匹配规则（Matcher） → 执行脚本（Handler） → 放行 / 阻断 / 注入上下文

五种事件类型，

覆盖 Agent 执行的全生命周期：

事件

触发时机

可阻断

UserPromptSubmit

用户提交提示时

✅

PreToolUse

Agent 调用工具前

✅

PostToolUse

工具调用完成后

❌

PostToolUseFailure

工具调用失败后

❌

Stop

Agent 完成响应时

✅

其中 3 种

可阻断事件

（UserPromptSubmit、PreToolUse、Stop）是安全管控和质量守护的核心。脚本返回

exit 0

表示放行，

exit 2

表示阻断——就这么简单。

03

三个实战案例

案例一：危险命令拦截——给 Agent 装上安全护栏

痛点：

Agent 可能执行

rm -rf

、

git push --force

等危险命令，一旦误操作后果不堪设想。

解法：

通过 PreToolUse Hook 匹配 Shell 执行工具，

在命令执行前自动拦截。

配置示例

{

"hooks"

:

{

"PreToolUse"

:

[

{

"matcher"

:

"Bash|run_in_terminal"

,

"hooks"

:

[

{

"type"

:

"command"

,

"command"

:

".lingma/hooks/block-dangerous-commands.sh"

}

]

}

]

}

}

脚本逻辑

#!/bin/sh

INPUT=$(

cat

)

COMMAND=$(

printf

&#x27;%s&#x27;

"

$INPUT

"

| jq -r

&#x27;.tool_input.command // empty&#x27;

)

# 危险命令黑名单

DANGEROUS=

"rm -rf|git push --force|git push -f|DROP TABLE|DROP DATABASE"

if

echo

"

$COMMAND

"

| grep -qiE

"

$DANGEROUS

"

;

then

echo

"⚠️ 检测到危险命令:

$COMMAND

"

>&2

exit

2

# 阻断执行

fi

exit

0

效果：

Agent 被阻断后会收到反馈原因，并自动尝试更安全的替代方案。从此不再担心"手滑"的代价。

案例二：完成前质量门禁——Agent 说"完成了"不算，测试通过才算

痛点：

Agent 声称任务完成，但跑一下测试就报错，每次都得手动返工。

解法：

通过 Stop Hook 在 Agent 完成响应前

自动执行质量检查

，不通过就让 Agent 继续干。

配置示例

{

"hooks": {

"

Stop

": [

{

"hooks": [

{

"type":

"command"

,

"command"

:

".lingma/hooks/quality-gate.sh"

,

"timeout"

:

120

}

]

}

]

}

}

脚本逻辑

#!/bin/sh

INPUT=$(

cat

)

# 防止无限循环

STOP_HOOKS_ACTIVE=$(

printf

&#x27;%s&#x27;

"

$INPUT

"

| jq -r

&#x27;.stop_hooks_active // false&#x27;

)

if

[

"

$STOP_HOOKS_ACTIVE

"

=

"true"

];

then

exit

0

fi

# 执行测试

if

! npm

test

2>/dev/null;

then

cat

<<

EOF

{"decision":"block","reason":"测试未通过，请修复失败的用例后再完成。"}

EOF

exit

2

fi

exit

0

效果：

Agent 不再"虎头蛇尾"。每次交付都经过质量门禁验证，相当于给 AI 编程配了一位自动化 QA。

案例三：提示增强——让 Agent 自动理解项目规范

痛点

：

每次对话都要重复提醒 Agent 使用某种技能、遵守编码规范，低效且容易遗漏。

解法：

通过 UserPromptSubmit Hook

自动注入项目上下文

，让 Agent 天然了解你的项目规范。

配置示例

{

"hooks"

:

{

"UserPromptSubmit"

:

[

{

"hooks"

:

[

{

"type"

:

"command"

,

"command"

:

".lingma/hooks/inject-context.sh"

}

]

}

]

}

}

脚本逻辑

#!/bin/sh

INPUT=$(

cat

)

# 会话级去重：同一 session 只注入一次

SESSION_ID=$(

printf

&#x27;%s&#x27;

"

$INPUT

"

| jq -r

&#x27;.session_id // empty&#x27;

)

DEDUP_DIR=

"/tmp/hooks-dedup"

mkdir

-p

"

$DEDUP_DIR

"

if

[ -n

"

$SESSION_ID

"

] && [ -f

"

$DEDUP_DIR

/context-

$SESSION_ID

"

];

then

exit

0

fi

# 注入项目规范提示

CONTEXT=

"本项目使用 TypeScript + React，测试框架为 Jest，请遵循 ESLint 规范。提交代码前请确保所有测试通过。"

[ -n

"

$SESSION_ID

"

] &&

touch

"

$DEDUP_DIR

/context-

$SESSION_ID

"

cat

<<

EOF

{"hookspecificOutput":{"additionalContext":"$CONTEXT"}}

EOF

exit

0

效果：

项目规范自动加载，Agent 从第一轮对话就"懂规矩"。团队统一配置后，每位成员的 Agent 都遵循同一套标准。

04

如何开始使用？

三步上手你的第一个 Hook

：

① 创建脚本目录

mkdir

-p .lingma/hooks

② 编写 Hook 脚本

（参考上面的案例，选一个你最需要的场景）

chmod

+x .lingma/hooks/your-hook-script.sh

③ 配置触

发规则

在项目配置文件中声明 Hook 绑定关系即可生效。灵码支持三级配置优先级：

全局配置：

适用所有项目的通用规则

项目级配置：

提交到 Git，团队共享

本地配置：

个人差异化覆盖，不入库

写在最后

灵码 Hooks 的设计哲学很简单——

AI Agent 越自主，就越需要可编程的边界。

它不是限制 Agent 的能力，而是让 Agent 在你设定的轨道上跑得更快、更安全。无论是个人开发者想要保护自己的代码安全，还是团队负责人想要统一 AI 辅助开发的质量标准，Hooks 都给了你一个优雅的答案。

现在就动手配置你的第一个 Hook，让灵码真正成为懂你规矩的编程伙伴。

关注灵码，获取更多 AI 编程最佳实践

。