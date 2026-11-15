---
publish_time: 1794389400
link: https://mp.weixin.qq.com/s/qYoa4_nZO8RY8kv-SfzdvA
source: CSDN
status: confirmed
category: 国际
is_model_related: false
digest: |
  安全公司 Apiiro 发现大量公开 GitHub 仓库含 Claude Code 配置文件，部分竟包含数据库密码、API Key 乃至超级管理员凭证。根因在于用户选择“Yes, and don't ask again”后，Claude Code 将含敏感信息的授权命令持久化保存，导致凭据随仓库外泄；Anthropic 已回应。
title: 点一下「以后不再询问」，密码、API Key全被上传！Claude Code配置文件泄露数千条敏感信息，Anthropic回应
---

# 点一下「以后不再询问」，密码、API Key全被上传！Claude Code配置文件泄露数千条敏感信息，Anthropic回应

来源：CSDN
原文链接：https://mp.weixin.qq.com/s/qYoa4_nZO8RY8kv-SfzdvA

整理 | 屠敏
出品 | CSDN（ID：CSDNnews）
只是为了让 AI 少问自己几次，没想到却把家底都交出去了。
近日，安全公司 Apiiro 的研究人员发现，公开的 GitHub 仓库中出现了大量 Claude Code 配置文件，其中不少文件竟然包含数据库密码、API Key，甚至超级管理员登录凭证。
进一步调查后，研究人员指出，这场泄露风波竟然与 Claude Code 中一个看似不起眼的选项有关：「Yes, and don’t ask again」（是的，以后不再询问）。
一个「不再询问」，怎么就把密码给存下来了？
要理解这次问题，还得从 Claude Code 的权限管理机制说起。
在使用 Claude Code 时，如果 AI 需要执行一些涉及系统操作的命令，通常会先向用户请求授权。
例如，开发者让 Claude Code 查询数据库，AI 可能会生成一条类似这样的命令：
PGPASSWORD
=your_password psql -h db.example.com -U admin
如果用户选择允许执行，Claude Code 就会运行这条命令。
但如果用户进一步选择「Yes, and don’t ask again」
（是的，以后不再询问）
，情况就有所不同了。
为了避免下次执行相同操作时再次询问，Claude Code 会将这条命令保存为一条长期生效的权限规则，写入项目目录下的：
.claude/settings.local.json
这本身是一个为了提高开发效率而设计的功能。
问题在于，Claude Code 保存的可能不是经过脱敏处理的命令模板，而是完整命令。
也就是说，上面那条命令中的 your_password，可能会原封不动地出现在配置文件里。
类似的情况还可能出现在其他命令中。例如，开发者让 Claude Code 使用 curl 请求某个 API，如果请求头中包含 Authorization Token，那么这条命令被保存为权限规则时，Token 也可能跟着一起进入配置文件。
于是，一个原本用于记录「哪些操作可以免去重复授权」的文件，意外变成了敏感信息的集中存放地。
问题出在 Git 忽略规则上
可能有人会问：既然这是一个本地配置文件，为什么会被上传到 GitHub？
事实上，Anthropic 并非完全没有考虑过这个问题。
根据 Claude Code 官方文档，.claude/settings.local.json 本来就被设计为个人使用的本地配置文件，不应该提交到 Git 仓库。
正常情况下，Claude Code 第一次创建这个文件时，会自动将其添加到 Git 的全局忽略规则（global gitignore）中。
但这里存在一个容易被忽略的区别：全局 Git 忽略规则，并不等于项目自身的 .gitignore 文件。
举个例子：
开发者 A 在自己的电脑上使用 Claude Code，系统自动将 settings.local.json 添加到了本机的 Git 忽略规则中。
此时，这个文件不会被正常提交到 Git 仓库。
但如果开发者将项目复制到另一台电脑，或者在一个原本没有 Git 仓库的目录中创建 Git 仓库，那么新环境未必拥有原来的全局忽略规则。
如果文件已经被 Git 跟踪，或者开发者手动创建了这个配置文件，而没有将其添加到忽略列表中，它就有可能被一起提交。
更麻烦的是，安全研究公司 Apiiro 的研究人员还发现，在一些情况下，Claude Code 自己也会参与提交包含这些敏感信息的配置文件。
换句话说，问题并不在于配置文件本身不应该存在，而在于它缺少一层足够可靠的保护。
安全公司调查：数千条密码、Token 已经暴露
那么，这个问题究竟影响了多少开发者？
11 月 5 日，安全公司 Apiiro 发布了一份相关调查报告。
研究人员在公开 GitHub 仓库中检查了 104,185 个 .claude/settings.local.json 文件，最终发现其中有 1,122 个文件包含真实的敏感凭证，共计 1,379 条。
这些信息涉及 63 家不同组织，包括服务 API Token、数据库密码、AI 模型 API Key、Supabase 服务角色密钥、Google API Key、SSH 登录凭证、GitHub、GitLab 和 npm Token，AWS 密钥以及私钥等。
其中，数据库密码和 Supabase 服务角色密钥合计达到 501 条，占全部 1,379 条凭证的 36.3%。
更令人担忧的是，研究人员还发现了 43 条用于登录公网服务器的 SSH 凭证，其中一些甚至涉及 Root 账户密码。
当然，这还不是全部。
11 月 9 日，另一家安全公司 GitGuardian 公布了更大规模的调查结果。
在 2025 年 1 月至 2026 年 11 月 7 日期间，GitGuardian 在公开 GitHub 上发现了 23,276 个仓库中的 .claude/settings.local.json 文件，累计识别出 31,088 条不同的敏感凭证。
其中，5,343 条在检测时仍然有效。
有一点已经相当明确：这不是几个开发者偶然犯下的低级错误，而是一个值得整个开发者社区警惕的问题。
Anthropic 团队回应：正在研究解决办法
事实上，这并不是一个刚刚出现的问题。
早在 2025 年 8 月，就有开发者在 Claude Code 的 GitHub Issue 中报告过类似情况：当用户批准包含凭证的命令时，敏感信息会以明文形式写入配置文件。
此后，社区还陆续出现了其他相关反馈。
但这些问题报告最终都因长时间没有更新而被自动关闭，并未得到实质性处理。
直到这次安全研究公开，问题才再次引起广泛关注。
在 Hacker News 的相关讨论中，Claude Code 团队负责人 Boris Cherny 也亲自作出了回应。
他承认，Claude Code 历史上并没有内置敏感信息清理机制，团队正在研究如何避免此类问题。
对于配置文件泄露，他解释称，.claude/settings.local.json 本来就不应该被提交到版本控制系统中，Claude Code 在自己创建文件时也会自动将其加入 Git 忽略规则。
他同时建议开发者使用 Claude Code 的 Auto Mode，而不是继续手动维护复杂的允许和拒绝规则。
按照他的说法，Auto Mode 可以通过分类器自动处理常规权限请求，减少开发者反复维护权限规则的麻烦。
不过，当有用户指出，即使使用 Auto Mode，涉及敏感命令的授权操作仍可能将相关内容写入配置文件时，Cherny 也认可了这一反馈，并表示团队正在考虑如何改进。
此外，他还提到，团队正在考虑将基础的 Secret Scanning（敏感信息扫描）能力直接集成到 Claude Code 中，目前正在研究和原型验证阶段。
但值得注意的是，Apiiro 的研究还发现，常见的两个敏感信息扫描工具 gitleaks 和 TruffleHog，即使结合使用，也漏掉了 215 个包含敏感凭证的文件，占相关文件总数的 19.2%。这说明，仅仅依赖现有扫描工具，也未必能完全解决问题。
开发者现在应该做什么？
对于已经使用 Claude Code 的开发者来说，这次事件最值得注意的，并不是简单地把某个文件加入 .gitignore 就万事大吉。
首先，可以检查项目中的 .claude/settings.local.json，看看其中是否存在包含密码、Token 或其他凭证的命令。
其次，应该在项目自己的 .gitignore 中明确添加：.claude/settings.local.json
如果项目还会被打包成 Docker 镜像，也应该在 .dockerignore 中排除：.claude/
如果已经发现敏感凭证被提交到公开仓库，仅仅删除文件并不够。Git 历史记录、Fork 仓库以及已经发布的 Docker 镜像，都可能继续保留这些信息。
因此，更重要的是立即撤销并轮换已经暴露的 API Key、数据库密码和其他凭证，再处理仓库历史记录及其他公开副本。
另外，对于需要在命令中使用的敏感信息，尽量通过环境变量引用，而不是直接把密码或 Token 写进命令参数中。
毕竟，AI 编程工具本来是为了让开发者少操心一些琐事。如果连自己电脑里的密码都需要额外担心会不会被它顺手打包上传，那这份便利显然还有不少需要完善的地方。
来源：
https://arstechnica.com/ai/2026/11/claude-code-settings-files-expose-thousands-of-secrets-on-github/
https://news.ycombinator.com/item?id=50408126
“AI正在毁掉我的计算机学位！”一名大学生吐槽：作业量暴涨3倍，老师用AI出题，学生却成了“小白鼠”
“AI正在逼我们还清40年的技术债！”一个两年没人修的老Bug，几天被AI挖成了「致命漏洞」：差点放倒全球近70%的网站
上千个Agent 8天写操作系统、还能从零设计硬件！Anthropic重磅发布Claude Fable 5.2、Mythos 5.2
🤖 AI 训练越来越烧钱，瓶颈真的只是算力不够吗？
⏰
11月11日（周三）19:30-21:00，CSDN「AI进化论」直播，聚焦 Agent 后训练的基础设施挑战！
🔹 七成算力花在推理上，训练和推理还要分开吗？
🔹 千万个沙箱同时运行，卡住训练的究竟是什么？
🔹 不靠万卡集群，普通硬件能否撑起大模型后训练？
🎁
直播专属福利
扫码免费领取「
2026 Agent 核心技术演进与实战资料包
」！
📚 现在报名，更有机会获得 AI 技术好书！
📲
扫描海报二维码，立即预约直播！
