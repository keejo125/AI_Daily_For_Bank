---
publish_time: 1787224200
status: confirmed
category: 国内
is_model_related: false
digest: |
  阿里云 Workbench CLI 已上架 Qoder IDE 插件市场及官网能力市场，让开发者在 Qoder 中用自然语言直接操作 ECS，无需公网 IP、SSH 或记忆运维命令。文章介绍该工具面向 Agent 设计：返回结构化 JSON、透传远程命令 exit code、无状态执行、命令语义直观（list/connect/exec/upload/download）。
  文中以 5 分钟部署 WordPress、本地项目打包部署到 ECS 并调试、查看网站访问日志三个场景演示 Agent 如何自动调用 workbench 命令完成全流程。为兼顾安全，工具要求破坏性命令（rm -rf、shutdown 等）与文件覆盖前须经用户明确确认，官方 Skill 也约束 Agent 先 ls 检查再上传，做到"危险动作仍由人把关"。
link: https://mp.weixin.qq.com/s/nMNFhxVkvfurHCrtAgx4Uw
source: Qoder
title: 阿里云 Workbench CLI 上架 Qoder 插件市场，不用 SSH 也能操作 ECS
---

# 阿里云 Workbench CLI 上架 Qoder 插件市场，不用 SSH 也能操作 ECS

> 原文链接：https://mp.weixin.qq.com/s/nMNFhxVkvfurHCrtAgx4Uw
> 来源：Qoder

Agent 写代码挺顺，但是一提"帮我连到那台 ECS ,排查下线上报错"，它就懵了。要么让你开公网 IP、配 SSH 密钥，要么给你一段命令但根本跑不通。最后还得你自己切到终端，手动登录、执行、复制结果，再贴回对话框。
今天这个环节可以省掉了，阿里云 Workbench CLI 已上架到 Qoder IDE 内的插件市场及 官网的能力市场内。
装上之后，你在 Qoder 里用自然语言就能让 Agent 直接操作 ECS：查实例、执行命令、传文件、看日志、部署服务——不用公网 IP，不用 SSH，不用记运维命令。
适合谁
想用自然语言操作 ECS 的开发者
不想给每台机器开公网 IP 和 SSH 端口的运维和安全团队
需要 Agent 自动部署、巡检、排查问题的 DevOps 场景
刚接触云、不想先学一堆 CLI 命令的新手
为什么需要 Workbench CLI
传统 SSH 对人不难，对 Agent 却不友好：输出是文本、状态会延续、失败不好判断、权限还难收敛。
阿里云 Workbench CLI 是面向 Agent 设计的 ECS 连接工具，几个特性正好解决这些问题：
免公网 IP 连接
：内网实例也能直接操作，安全组由 CLI 自动处理。
--output json
：所有命令返回结构化数据，Agent 不用写正则解析。
退出码透传
：workbench exec 把远程命令的 exit code 原样返回，Agent 能判断成功失败。
无状态执行
：每次命令独立运行，没有 cd 或 export 污染上下文。
命令语义直观
：list、connect、exec、upload、download，Agent 一看就懂。
简单说：它让 ECS 对 Agent 来说，就像本地终端一样好用。
快速上手 Workbench CLI
第 1 步：登录 Qoder IDE ，打开 Quest ，在左下角的插件市场安装 AlibabCloud Workbench 插件
第 2 步：安装完成后，在 Qoder 对话框里直接自然语言对话就行。
例如："帮我看一下杭州地域有哪些运行中的 ECS 实例"
Agent 会自动调用 workbench list --region cn-hangzhou --output json，并汇总成表格给你。
几个真实场景，看看它多顺手
场景一：5 分钟部署一个 WordPress
"在实例 i-bp1hgw33lt0yyfudbh9e 上帮我部署 WordPress"
Agent 会依次完成：
用 workbench exec 安装 Apache、MariaDB、PHP；
启动数据库和 Web 服务；
用 workbench exec 创建 WordPress 数据库和用户；
下载 WordPress 并解压到 /var/www/html；
配置 wp-config.php 并重启 Apache。
你不需要知道 dnf 怎么写、PHP-FPM 怎么配、数据库字符集怎么设。只要说一句，Agent 全包。
场景二：把本地项目打包部署到 ECS 并调试
"帮我把当前这个 Spring Boot 项目打包，部署到实例 i-bp1hgw33lt0yyfudbh9e 上跑起来"
Agent 会依次完成：
在本地执行 mvn clean package，拿到 target/app.jar；
用 workbench upload 把 jar 传到实例，传输前自动 ls 检查路径，避免覆盖已有文件；
用 workbench exec 在后台启动服务；
用 workbench exec 发起 curl 健康检查，读 exit_code 判断是否起来了；
若启动失败，自动 tail 日志定位是端口占用、依赖缺失还是配置写错。
你不需要在本地打包、scp 传包、SSH 登录启动之间来回切终端。只要说一句，从编译到部署再到调试，Agent 一条龙搞定。
场景三：查看网站访问日志
"帮我看看这个网站最近的访问日志"
Agent 会自动执行：
workbench exec -
i
i
-bp1hgw33lt0yyfudbh9e \
-c "sudo tail -
50
/
var
/log/httpd/access_log"
--output
json
然后自动汇总：最近访问来自哪个 IP、有没有错误、用户在浏览哪些页面。
你不需要记得日志路径，也不需要翻 less 和 grep，Agent 直接给你结论。
Workbench CLI 为什么比 SSH 更适合 Agent
看一个 workbench exec 的 JSON 输出就明白了：
{
"output"
:
"Filesystem      Size  Used Avail Use% Mounted on
\n
/dev/vda1        40G   15G   25G  38% /
\n
"
,
"stderr"
:
""
,
"exit_code"
:
0
}
Agent 读 exit_code 判断成败，读 output 提取字段，读 stderr 处理异常——全是结构化数据，不用再写正则从文本里扒结果。
这就是 Agent 用云和人有云最大的区别：人不介意看文本，Agent 需要能解析的结构。
两个让 Agent 更安全的设计
把服务器交给 Agent 操作，很多人会担心"它会不会误删数据"。Workbench CLI 在设计上已经做了两道保险：
1. 无状态执行，避免上下文污染
每次 workbench exec 都是一次独立的命令执行。这意味着 Agent 不会因为"上一句命令切了目录"导致下一句命令跑错地方，也不会因为环境变量残留引发意外行为。
2. 破坏性操作和文件覆盖都有保护
官方 Skill 明确要求：执行 rm -rf、shutdown、reboot、mkfs、dd、停止核心服务等破坏性命令前，Agent 必须先向用户说明目标实例、操作内容和潜在影响，获得明确批准后才能执行。
文件传输也一样：workbench upload 默认会检测远程文件是否已存在，存在时提示确认，防止自动覆盖重要文件。在 Agent 自动化流程中，Skill 要求 Agent 先 ls 检查目标路径，再告知用户是否会覆盖。
简单说：
Agent 能干的活变多了，但危险动作仍然由人把关。
快去 Qoder 里安装 Workbench 插件
，然后对 Qoder 说：
"帮我部署一个 WordPress"
，看看 Agent 能不能在 5 分钟内把网站跑起来。
