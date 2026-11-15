---
publish_time: 1793367831
link: https://www.solidot.org/story?sid=85756
source: Solidot
status: confirmed
category: 国际
is_model_related: false
digest: |
  安全研究人员在Cursor扩展市场的Claude Code for VS Code官方扩展（Anthropic.claude-code 2.1.313）中发现后门，该恶意版本上线约11小时、影响约5000名用户，会尝试植入持久SSH后门并收集主机与Git信息、建立反向隧道。攻击者已关闭服务器，Cursor发布安全公告，Anthropic尚未公开回应，受影响用户需检查系统。
---

# Claude Code for VS Code 官方扩展被植入后门

> 原文链接：https://www.solidot.org/story?sid=85756
> 来源：Solidot

安全研究人员在 Cursor Marketplace 的 Claude Code for VS Code 官方扩展中发现了后门，该恶意版本已经撤下，攻击者也关闭了其服务器。Cursor 已发布安全公告，但 Claude Code 开发商 Anthropic 尚未做出任何声明。受影响的版本是 Anthropic.claude-code 2.1.313，共上线了大约 11 小时，受影响用户估计有 5,000 名，该扩展会试图植入一个持久 SSH 后门。恶意扩展会：收集主机和用户信息：主机名、用户名、操作系统、架构、主目录路径、环境变量名称、工作目录、已配置的 Git 邮箱以及公网 IP。尝试将攻击者控制的 SSH 键添加到 authorized_keys，启用本地 SSH 服务，并建立反向 SSH 隧道。由于恶意代码存在 bug，除非 Cursor 是以管理员权限启动的 (这种情况极为罕见) ，否则这一步会失败。尝试通过 LaunchAgent (macOS) 或计划任务 (Windows，该任务会尝试以 SYSTEM 身份运行，并以启动脚本作为回退) 使反向 SSH 隧道长期生效。后台脚本大约每 60 秒重试一次建立隧道。通过 HTTP POST 将主机详情和后门状态上报至 8099 端口上的 /beacon。如果用户是在 2026 年 10 月 29 日太平洋时间凌晨 2:27 至下午 1:35 之间，从 Cursor VS Code 扩展市场安装了 Anthropic.claude-code 2.1.313 或更新到该版本，那么需要检查下系统。