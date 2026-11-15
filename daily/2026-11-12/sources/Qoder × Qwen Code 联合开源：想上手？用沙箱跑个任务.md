---
publish_time: 1794476592
link: https://mp.weixin.qq.com/s/ETOYura8U4cHfCzKcJQGqg
source: 阿里云基础设施
status: confirmed
category: 国内
is_model_related: false
digest: |
  阿里云智能体沙箱Agent Sandbox上线Qwen Code沙箱模板：开发者无需在本机安装Node.js与CLI，即可在隔离云端环境中让Qoder与Qwen Code读代码、改文件、跑命令，环境按需创建、用完释放。文章给出从模板市场复制、SDK创建沙箱到接入自有应用的实操路径，降低编码Agent上手与运维门槛。
title: Qoder × Qwen Code 联合开源：想上手？用沙箱跑个任务
---

# Qoder × Qwen Code 联合开源：想上手？用沙箱跑个任务

来源：阿里云基础设施
原文链接：https://mp.weixin.qq.com/s/ETOYura8U4cHfCzKcJQGqg

Qoder 与 Qwen Code 的 Harness 融合开源，为开发者提供了可嵌入自身产品的 Agent 运行基础。想把 Qwen Code 跑起来，不必先在自己的电脑上安装 Node.js、配置 CLI。
阿里云智能体沙箱 Agent Sandbox 的模版市场上线了 Qwen Code 沙箱模板，配置好模型服务即可开始：Agent 读代码、改文件、跑命令，都在与本机隔离的云端环境中进行，避免影响本机文件和依赖；环境按需创建，用完释放，无需长期维护一套专用环境。
本文先带你在控制台跑通第一个编码任务，再通过 SDK 创建沙箱、执行任务，将这套流程接入自己的应用。
开始之前，只需要准备一样东西
Qwen Code 自己不带模型，它要连一个模型服务。本文用阿里云百炼，走 OpenAI 兼容协议，在百炼控制台创建一个 API Key 就够了，形如
sk-
开头的一串。
顺手记一下你打算用的地域，本文截图用的是
华南1（深圳）
。后面复制模板、创建沙箱、代码里的接入地址，都要跟它对齐。
第一条路：在控制台点一点
第一步：从模板市场复制一个模板
打开 Agent Sandbox 控制台，左侧进「模板市场」，往下翻到
Qwen Code Sandbox
，点「复制模板」。
市场里的模板是公共的、只读的。复制一份到你自己的 Team 下，才能拿它创建沙箱。
弹窗里只有两件事要填：模板名称和所属 Team。名称用英文字母开头，后面可以带数字、下划线和短横线，比如
qwen-code-demo
；还没有 Team 的话，点右边「创建 Team」现建一个。然后点「创建」。
第二步：等模板变成「就绪」
复制完会来到「极速版 → 沙箱模板」列表。刚建好的模板要先把镜像准备好，构建状态变成绿色的「就绪」就能用了。这一步通常很快，点一下右上角刷新即可。
就绪之后，点这一行右边的「创建沙箱实例」。
第三步：创建实例，重点是那三个环境变量
基本信息里，Team 和沙箱模板已经自动带过来了，不用改。
「超时时间」默认 300 秒，意思是沙箱活 300 秒，到点自动释放。跑个 Hello World 够用；想慢慢跟它聊，就改大一点，比如 3600。
真正不能漏的是下面「高级设置」里的
环境变量
。展开它，加这三条：
变量名
填什么
OPENAI_API_KEY
你的百炼 API Key，
sk-
开头那串
OPENAI_BASE_URL
你的百炼调用地址
OPENAI_MODEL
qwen3.8-max
这三个必须同时填。
Qwen Code 只有在三个都齐的时候，才会认定「你要用 OpenAI 兼容端点」；只填一个 Key，它会直接报
No auth type is selected
然后退出。这是新手最常踩的坑，记住能省十分钟。
模型想换随时换，比如更偏编码的
qwen3-coder-plus
，改
OPENAI_MODEL
一个值就行。填完点「创建」。
第四步：打开终端
回到「沙箱实例」列表，能看到刚创建的沙箱，状态是「运行中」。点右边的「终端」。
详情页切到
WebShell
页签，看到
user@aliyun:~$
就是连上了。这个终端直接跑在沙箱里，不用 SSH，不用配密钥，浏览器打开就能敲命令。
第五步：敲 qwen，派第一个活
先进工作目录，让产物都落在一个地方，然后启动：
cd
/home/user/workspace
qwen
Qwen Code 的界面就起来了。留意两个地方：
标题下面写着
API Key | qwen3.8-max
，说明它已经认领了你填的端点和模型；
底部是
Auto mode
，安全操作自动批准，有风险的操作会拦下来问你。按
Shift+Tab
可以切换审批模式。
如果这里报的是
No auth type is selected
，说明三个环境变量没填齐或者没生效。在终端里补一遍就好：
export
OPENAI_API_KEY
=
"sk-你的百炼 API Key"
export
OPENAI_BASE_URL
=
"https://dashscope.aliyuncs.com/compatible-mode/v1"
export
OPENAI_MODEL
=
"qwen3.8-max"
然后重新敲
qwen
。
第一条任务别太复杂，先确认链路是通的。在输入框里发这样一句：
读一下当前目录，告诉我这里有什么。先不要修改任何文件。
确认它能正常回话、能读到目录，再让它真的动手：
在当前目录创建 index
.html
，做一个 Hello World 页面，标题写 Hello
from
Qwen
Code
。
它会自己想清楚要调什么工具、写哪个文件，你在旁边看着就行。写完
ls
一下，
index.html
就在那儿。
顺便说一句，沙箱里
node --version
显示 20 是正常的，
qwen
跑在镜像内置的 Node 22 上，不用管它。
第六步：把成果带走
沙箱是一次性的，释放之后里面的文件跟着消失。想留下产物，两个办法：
详情页的「文件」页签，直接把文件下载下来；
需要长期存放、或者多个沙箱共享的，在创建实例时挂上存储卷。
另外记得，沙箱按用量计费，模型调用由百炼单独计费，两笔账分开算。不用的沙箱及时释放，或者交给超时自动回收。
第二条路：用代码派活
页面适合体验，代码适合干活。当你要一次跑几十个任务，或者想把 Agent 接进自己的系统，就该用 SDK 了。
沙箱兼容 E2B 协议，Python 装个
e2b
就能用。
第一步：装 SDK
pip
install e2b==
2
.
31
.
0
第二步：把连接信息放进环境变量
在
你自己的电脑
上执行，本文以深圳地域为例，换地域把
cn-shenzhen
替换掉即可：
export
E2B_API_KEY
=
""
export
E2B_API_URL
=
"https://api.cn-shenzhen.sandbox.aliyuncs.com"
export
E2B_DOMAIN
=
"cn-shenzhen.sandbox.aliyuncs.com"
export
E2B_TEMPLATE
=
"qwen-code-demo"
export
OPENAI_API_KEY
=
""
export
OPENAI_BASE_URL
=
"https://dashscope.aliyuncs.com/compatible-mode/v1"
export
OPENAI_MODEL
=
"qwen3.8-max"
这里有两种 Key，别搞混：
E2B_API_KEY
是沙箱的，在控制台「API Keys」里创建，付的是沙箱资源的钱；
OPENAI_API_KEY
是百炼的，付的是模型调用的钱。
E2B_TEMPLATE
填你复制出来的模板名称或 ID。
第三步：一个能直接跑的完整例子
存成
quickstart.py
：
import
os
from
e2b
import
Sandbox
sandbox = Sandbox.create(
template=os.environ[
"E2B_TEMPLATE"
],
api_key=os.environ[
"E2B_API_KEY"
],
api_url=os.environ[
"E2B_API_URL"
],
domain=os.environ[
"E2B_DOMAIN"
],
timeout=
300
,
envs={
"OPENAI_API_KEY"
: os.environ[
"OPENAI_API_KEY"
],
"OPENAI_BASE_URL"
: os.environ[
"OPENAI_BASE_URL"
],
"OPENAI_MODEL"
: os.environ[
"OPENAI_MODEL"
],
},
)
try
:
# 先确认 CLI 可用，会打印版本号
print
(sandbox.commands.run(
"qwen --version"
).stdout.strip())
# 一次性派活：位置参数就是提示词，--yolo 自动批准所有工具调用
result = sandbox.commands.run(
'cd /home/user/workspace && qwen '
'"在当前目录创建 index.html，内容是一个 Hello World 页面" '
'--yolo < /dev/null'
,
timeout=
300
,
)
print
(result.stdout)
# 把产物读回本地
print
(sandbox.files.read(
"/home/user/workspace/index.html"
))
finally
:
sandbox.kill()
第四步：跑起来
python
quickstart.py
顺利的话你会看到三段输出：版本号
0.27.2
、Qwen Code 干活的过程、最后是
index.html
的内容。跑完沙箱自动释放，不用手动收尾。
两个容易忽略的点：
commands.run
一定要传
timeout
。
写代码比执行
echo
慢得多，默认超时不够用，你会拿到一个超时错误，而不是真实的失败原因，排查方向就跑偏了。
--yolo
是让它自动批准所有工具调用
，包括写文件和执行命令。无人值守必须加；也正因为敢加，才要把它放在沙箱里跑。
更进一步：一次派一堆活
单个任务跑通之后，加个并发就是批量。下面这段同时开三个沙箱，各干一件事，互不干扰，跑完各自释放：
import
os
from
concurrent.futures
import
ThreadPoolExecutor
from
e2b
import
Sandbox
TASKS = [
(
"创建 hello.py，内容是打印 Hello from Qwen Code"
,
"hello.py"
),
(
"创建 README.md，用一句话说明这个项目是做什么的"
,
"README.md"
),
(
"创建 .gitignore，忽略 node_modules 和 .env"
,
".gitignore"
),
]
ENVS = {
"OPENAI_API_KEY"
: os.environ[
"OPENAI_API_KEY"
],
"OPENAI_BASE_URL"
: os.environ[
"OPENAI_BASE_URL"
],
"OPENAI_MODEL"
: os.environ[
"OPENAI_MODEL"
],
}
def
run_task
(
task
):
prompt, artifact = task
sandbox = Sandbox.create(
template=os.environ[
"E2B_TEMPLATE"
],
api_key=os.environ[
"E2B_API_KEY"
],
api_url=os.environ[
"E2B_API_URL"
],
domain=os.environ[
"E2B_DOMAIN"
],
timeout=
600
,
envs=ENVS,
)
try
:
sandbox.commands.run(
f'cd /home/user/workspace && qwen "
{prompt}
" --yolo < /dev/null'
,
timeout=
600
,
)
return
artifact, sandbox.files.read(
f"/home/user/workspace/
{artifact}
"
)
finally
:
sandbox.kill()
with
ThreadPoolExecutor(max_workers=
3
)
as
pool:
for
artifact, content
in
pool.
map
(run_task, TASKS):
print
(
f"=====
{artifact}
====="
)
print
(content)
三个任务、三个独立环境、三份产物。想派十个，把
TASKS
写长一点、
max_workers
调大一点就行。
最后
两条路做的其实是同一件事：把 Qwen Code 放进一个随时能开、用完就扔的环境里。
页面上点几下，你能看清它每一步在干什么，适合摸清脾气；换成代码，同样的东西可以一次开几十个，跑完自动散场，适合真干活。
环境不再是门槛之后，你的注意力可以放回更重要的地方——想清楚要它做什么，以及验收它做得对不对。
Qwen Code 沙箱模板已在模板市场上线。浏览器输入 https://console.aliyun.com/sandbox/cn-hangzhou/template-market/qwen-code 或点击
阅读原文
即可跳转至 Agent Sandbox 控制台，快来一起体验吧！
