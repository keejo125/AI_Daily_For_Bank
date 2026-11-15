---
publish_time: 1794104100
link: https://mp.weixin.qq.com/s/G3bgxrcKHjkAAPamu3GMRg
source: InfoQ
status: confirmed
category: 国际
is_model_related: false
digest: |
  编程培训机构创始人 Chidi Nwaogu 因学生常因网络掉线流失，开发 Efiwe 平台：直接在智能手机浏览器运行、一次初始设置后可离线使用，已被 160 国 2.2 万余名学习者使用。工程取舍上，选 PWA 而非原生应用以降低安装流量门槛、借 Service Worker 静默更新；代码执行不依赖服务器，用编译为 WebAssembly 的 sql.js（SQLite）与 Pyodide（CPython）在本地跑 Python/SQL，并规定运行时只在 Worker 中按需初始化、缓存优先，使断网一周仍可启动。文章聚焦存储配额、冷启动与失败路径等被忽视的难题。
title: AI 编程导师挑战低端 Android 手机！不用服务器，Python 和 SQL 直接在浏览器里运行
---

# AI 编程导师挑战低端 Android 手机！不用服务器，Python 和 SQL 直接在浏览器里运行

来源：InfoQ
原文链接：https://mp.weixin.qq.com/s/G3bgxrcKHjkAAPamu3GMRg

作者 ｜ Chidi Nwaogu
译者 ｜ 田橙
我花了一年时间，看着学生一个接一个地消失。当时我经营着一家编程培训机构，学生们会进入直播课堂，积极参与，然后突然在上课途中掉线。后来我逐个跟进才发现，几乎没有人是主动退出的。他们的网络连接根本撑不到一节课结束。在一批报名的 80 名学生中，最终只有 6 人毕业。
这段经历让我意识到，大多数编程教育平台都建立在四个默认前提之上。这些前提太过普遍，以至于人们几乎忘了它们只是一些假设：学习者有笔记本电脑、有宽带网络、能够轻松阅读英语，而且付得起订阅费，或者所在机构已经替他们付了费。
我开发的 Efiwe 平台，就是要打破所有这些假设。它可以直接在智能手机浏览器中运行，只需完成一次初始设置，之后就能离线使用。学生提交的代码也在本地执行，首次加载完成后，不再需要消耗移动数据流量。目前，Efiwe 已被 160 个国家的 22,000 多名学习者使用，并在尼日利亚的拉各斯州、奥贡州，以及印度北阿坎德邦的学校开展了有组织的试点。
这篇文章不讨论教学方法，而是讨论工程实践，尤其是那些曾经出过问题的地方。在这个领域，真正棘手的问题并不在于模型质量，而在于存储、配额、冷启动和失败路径的设计。这些问题也远不止存在于教育产品中。只要产品面向的是设备性能有限、网络连接时断时续的用户，就很可能遇到同样的挑战。
为什么选择 PWA，而不是原生应用
我们首先要决定的是如何分发产品。开发一款原生 Android 应用似乎是最自然的选择，但我们最终没有这么做，原因有三个。
首先是安装门槛。即使还没有下载任何课程内容，从应用商店安装一个 APK，也往往需要消耗几十 MB 的流量，而学生可能正精打细算地使用自己的流量套餐。渐进式 Web 应用（PWA）则允许学生点开就开始学习，缓存可以在后台逐步完成，流量开销也随之分摊到学习过程中。
其次是更新频率。我们会持续发布更新。使用 Service Worker，新版本可以在用户下次访问时生效。应用商店发布新版本却做不到这一点。在那些用户为了节省流量而推迟更新应用的市场中，可能有相当一部分用户仍在运行几个月前就已经修复过问题的旧代码。
第三，Web 平台让我们可以用一套运行时解决代码执行问题。我们需要学生能够编写 Python、SQL、JavaScript 和 HTML，并立即看到运行结果，而且整个过程不能依赖服务器。浏览器中的 WebAssembly 让我们可以一次实现，在各个平台上运行。
我们也考虑过用原生应用外壳包装一个 WebView。这样同样可以使用 Web 运行时，如果加载的是远程内容，也能解决更新问题。但它解决不了安装门槛：学生仍然需要先下载 APK，才能开始学习，而这笔流量可能正是他们舍不得花的。对于一个从根本上就是为了降低学习门槛而设计的产品来说，这一点已经足以让我们作出决定。
这个选择也有代价：我们必须接受浏览器的存储机制，包括它的配额限制。而我们在生产环境中遇到的大部分麻烦，恰恰都来自这里。
不依赖服务器执行代码
通常，评判一道编程题的答案，需要把学生提交的代码发送到服务器，在沙箱中执行，再把判定结果返回给学生。这意味着每尝试一次，都要经历一次网络往返。在尼日利亚伊杰布奥德的一间教室里，网络连接并不稳定，而学生往往需要尝试十到十二次才能解出一道题。这种模式根本行不通。
所以，我们让代码直接在设备上执行。SQL 使用 sql.js，也就是编译为 WebAssembly 的 SQLite；Python 使用 Pyodide，也就是编译为 WebAssembly 的 CPython。两者的体积都不小，初始化也都很慢。如果处理不当，它们都会阻塞主线程，让页面卡住。
最后我们定下了一条规则：任何运行时都不能在主线程初始化，也不能在真正需要之前初始化。学生选择课程时，才会按需启动 Worker，而且挑战页面的首次渲染绝不能等待运行时初始化完成。下面这段代码展示了这种做法：
// runtime-host.js（主线程）
let
workerPromise =
null
;
export
function
getRuntime
(
kind
) {
if
(!workerPromise) {
workerPromise =
new
Promise
(
(
resolve, reject
) =>
{
const
worker =
new
Worker
(
'/workers/runtime.js'
, {
type
:
'module'
});
const
timer =
setTimeout
(
() =>
reject
(
new
Error
(
'runtime-init-timeout'
)),
45_000
);
worker.
addEventListener
(
'message'
,
function
onReady
(
e
) {
if
(e.
data
?.
type
!==
'ready'
)
return
;
clearTimeout
(timer);
worker.
removeEventListener
(
'message'
, onReady);
resolve
(worker);
});
worker.
postMessage
({
type
:
'init'
, kind });
});
}
return
workerPromise;
}
在 Worker 内部，我们还对初始化做了保护，确保第二次收到初始化消息时不会重复执行。模块文件也会优先从缓存中加载，这样即使设备已经离线一周，学生再次打开应用时，运行时依然能够启动。
// workers/runtime.js
let
runtime =
null
;
self
.
addEventListener
(
'message'
,
async
(e) => {
const
{
type
, kind, code, fixture } = e.
data
;
if
(
type
===
'init'
) {
if
(!runtime) runtime =
await
boot
(kind);
self
.
postMessage
({
type
:
'ready'
});
return
;
}
if
(
type
===
'run'
) {
try
{
const
result =
await
runtime.
exec
(code, fixture);
self
.
postMessage
({
type
:
'result'
, result });
}
catch
(err) {
// 学生代码出错是正常数据，不是系统异常，绝不能因此终止 Worker。
self
.
postMessage
({
type
:
'result'
,
error
:
String
(err?.
message
?? err) });
}
}
});
最后这段代码里的区别值得多说几句。在普通应用中，执行代码时抛出异常通常意味着出现了 Bug。但在这里，大多数时候这恰恰是预期行为，因为学生都是初学者，学习过程本来就少不了犯错。因此，代码执行链路中的每一层，都必须把失败当作正常情况来处理。
对于 SQL 题目的判定，我们不会直接比较输出字符串，而是比较结果的结构和内容。这样一来，只要题目允许，即使学生使用了不同的格式、别名或列顺序，只要查询正确，就仍然能够通过。
export
function
gradeSql
(
actual, expected, opts = {}
) {
if
(!actual || !actual.
length
)
return
{
pass
:
false
,
reason
:
'empty'
};
const
[got] = actual;
const
cols = got.
columns
.
map
(
(
c
) =>
c.
toLowerCase
());
const
want = expected.
columns
.
map
(
(
c
) =>
c.
toLowerCase
());
if
(!opts.
orderedColumns
) {
cols.
sort
();
want.
sort
();
}
if
(cols.
join
(
'|'
) !== want.
join
(
'|'
)) {
return
{
pass
:
false
,
reason
:
'columns'
,
got
: cols, want };
}
const
norm
= (
rows
) =>
rows.
map
(
(
r
) =>
r.
map
(
String
).
join
(
'\u0001'
)).
sort
().
join
(
'\u0002'
);
const
rowsMatch = opts.
orderMatters
?
JSON
.
stringify
(got.
values
) ===
JSON
.
stringify
(expected.
values
)
:
norm
(got.
values
) ===
norm
(expected.
values
);
return
rowsMatch ? {
pass
:
true
} : {
pass
:
false
,
reason
:
'rows'
};
}
这里的
reason
字段并不是可有可无的装饰。它会作为后面介绍的反馈系统的输入，让我们能够告诉学生：你的列选对了，但筛选条件有问题，而不只是简单地告诉他答案错了。
持久化存储：为什么 localStorage 不够用了
Efiwe 提供 246 种语言的内容。翻译后的编程题文本会缓存在设备上，这样选择约鲁巴语或印地语的学生，就不需要每次学习都重新下载相同的内容，而且离线后也能继续使用翻译。
最初，我们用 localStorage 来保存这些缓存。后来证明，这是个错误的选择，而且同时暴露了两个问题。
第一个问题是容量。localStorage 通常对每个源设置大约 5MB 的容量上限，具体限制会因浏览器和平台而异。一门包含数百道编程题的课程，即使只缓存几种语言的翻译内容，也很容易超过这个限制。一旦超出，写入操作就会抛出
QuotaExceededError
。如果没有对每次写入都做好异常处理，错误就可能在意想不到的地方冒出来。
第二个问题更严重，也更隐蔽：localStorage 是同步的。每次读取和写入都会阻塞主线程。在一台中端笔记本电脑上，这可能只是几毫秒，没人会注意。但在一部入门级 Android 手机上，闪存控制器速度慢，CPU 又已经满负荷运行，启动时一次较大的同步读取就可能造成明显卡顿，而这恰恰发生在最经不起卡顿的设备上。我们花了不少精力优化 JavaScript 代码体积，却在存储层里悄悄埋下了一个主线程阻塞点。
于是，我们迁移到了 IndexedDB。IndexedDB 是异步的，存储配额通常根据可用磁盘空间按比例分配，而不是固定的几 MB，并且可以直接存储结构化数据，不必经过 JSON 序列化和反序列化。
选择 IndexedDB 很容易，真正费工夫的是如何让现有用户平稳迁移，又不丢失数据。已经上线的用户仍然在旧存储中保存着数据，其中不少人会连续离线好几天，因此他们什么时候能运行到新代码，完全无法预测。如果直接切换，缓存的翻译和未完成的学习进度就可能悄无声息地丢失。所以，我们设置了一个双重读取的过渡期：先读取新存储，如果没有找到，就读取一次旧存储；找到后将数据迁移过去，再删除旧的键。
import
{ get
as
idbGet, set
as
idbSet }
from
'./idb.js'
;
const
LEGACY_PREFIX
=
'efiwe.tr.'
;
export
async
function
readTranslation
(
key
) {
const
fresh =
await
idbGet
(
'translations'
, key);
if
(fresh !==
undefined
)
return
fresh;
// 从旧的同步存储中执行一次性迁移。
let
legacy =
null
;
try
{
const
raw =
localStorage
.
getItem
(
LEGACY_PREFIX
+ key);
legacy = raw ?
JSON
.
parse
(raw) :
null
;
}
catch
{
legacy =
null
;
// 数据损坏或无法读取，按不存在处理
}
if
(legacy ===
null
)
return
undefined
;
try
{
await
idbSet
(
'translations'
, key, legacy);
localStorage
.
removeItem
(
LEGACY_PREFIX
+ key);
}
catch
{
// 迁移尽力而为。让用户拿到内容比完成迁移更重要。
}
return
legacy;
}
这个函数里有两个细节，几乎就是我们从这次迁移中学到的全部经验。首先，读取旧数据的操作被包在异常处理中，因为如果上次会话中断，导致 localStorage 中的数据只写入了一部分，那么
JSON.parse
就可能抛出异常。我们绝不希望一次缓存解析错误把整个页面搞崩。其次，迁移写入被单独包在另一个异常处理中，因为设备存储空间已满时，读取可能成功，写入却会失败。这种情况下，正确的做法仍然是先把内容交给学生，下次再尝试迁移。
将存储配额问题视为一种必须考虑的故障场景
如果这篇文章只能让其他工程师记住一件事，我最希望是下面这次事故。
在尼日利亚的试点期间，一位老师反馈说，有些学生在手机上创建账户后，学习页面始终无法显示。账户创建成功了，登录也没有问题，但课程就是加载不出来。屏幕一片空白。
我们最初怀疑是低端 Android 设备的硬件兼容性问题。这个猜测看起来很合理，但事实证明我们错了。由于问题集中出现在更便宜的设备上，我们还因此浪费了不少排查时间。实际上，这只是一种相关性，并非真正的因果关系：便宜的设备往往存储容量更小，而容量越小，就越容易被占满。
真正的原因，是课程启动流程中的一个
await
。启动时，我们会先把初始课程清单写入缓存，然后再继续执行后续操作。但如果设备已经没有剩余空间，写入就可能失败。由于没有捕获这个错误，Promise 链会在执行渲染调用之前中断。学生也看不到任何报错，因为程序并没有以 UI 能够检测到的方式崩溃。只是课程的渲染函数根本没有机会被调用。
原来的代码大致是这样的：
// 修改前：存储失败会悄无声息地中断渲染流程。
async
function
startCourse
(
courseId
) {
const
manifest =
await
fetchManifest
(courseId);
await
cacheManifest
(courseId, manifest);
// 设备存储已满时会被拒绝
renderCourse
(manifest);
// 永远执行不到这里
}
修改后的代码：
// 修改后：持久化存储只是一项优化，不再是前置条件。
async
function
startCourse
(
courseId
) {
const
manifest =
await
fetchManifest
(courseId);
cacheManifest
(courseId, manifest).
catch
(
(
err
) =>
{
reportNonFatal
(
'manifest-cache-failed'
, err);
setOfflineAvailability
(courseId,
false
);
});
renderCourse
(manifest);
}
现在，即使无法把数据保存到设备上，课程也能正常启动。离线功能会受到影响，我们也会明确告知学生，但不会因此阻止他们继续学习。修复后，我们在不同存储条件下进行了验证，包括一台被故意填满存储空间的设备，确认问题解决后才关闭这次故障记录。从收到反馈到完成修复和验证，整个过程都在当天完成。
后来，我们总结出了一条可以普遍适用的规则：启动流程中的持久化写入操作，必须采用发起后不等待结果的方式，并明确捕获异常，绝不能用
await
等待写入完成。 如果页面渲染必须等到写入成功才能继续，那么用户只要把手机存储空间用满，就可能遇到白屏。
我们还增加了一项预检查机制，让系统能够主动进行功能降级，而不是等到写入失败时才发现问题。
export
async
function
storageBudget
() {
if
(!navigator.
storage
?.
estimate
) {
return
{
known
:
false
,
freeBytes
:
Infinity
};
}
const
{ quota =
0
, usage =
0
} =
await
navigator.
storage
.
estimate
();
return
{
known
:
true
,
freeBytes
:
Math
.
max
(
0
, quota - usage), quota, usage };
}
export
async
function
canCacheCourse
(
estimatedBytes
) {
const
{ known, freeBytes } =
await
storageBudget
();
if
(!known)
return
true
;
// 无法确定容量，不应成为阻止缓存的理由
return
freeBytes > estimatedBytes *
1.25
;
// 为额外开销预留空间
}
出于隐私保护的考虑，
navigator.storage.estimate()
返回的数值本身就经过了填充处理，而且只是近似值，因此它只能作为规划依据，不能当作保证。但这些信息已经足够帮助我们判断，是应该尝试预缓存整门课程，还是按需加载；也足以让我们提前提醒学生，如果想使用离线模式，就需要先清理一些存储空间。
两级 AI 反馈机制，以及明确的降级规则
Efiwe 会针对每个学生的错误答案提供个性化反馈。在尼日利亚的试点中，这是实地调研评分最高的一项功能，平均得分为 4.3 分（满分 5 分），10 位老师中有 9 位给出了 4 分或 5 分。
但这也是与离线优先理念冲突最大的一项功能，因为质量最好的反馈来自通过 API 调用的云端模型，而这个产品最基本的设计前提，恰恰就是网络可能根本不存在。
我们最终采用了两级方案，并明确规定了它们之间的切换机制。第一级是云端模型，在网络可用时调用，并设置严格的超时时间。第二级是能力较小的端侧方案，将对提交代码的确定性分析与本地模型结合起来。第二级始终可用，而且对事实的判断始终准确，因为事实判断由确定性分析部分负责。
const
HOSTED_TIMEOUT_MS
=
4000
;
export
async
function
getFeedback
(
submission, challenge
) {
const
local =
analyseLocally
(submission, challenge);
// 始终执行，开销始终很低
if
(!navigator.
onLine
)
return
{ ...local,
tier
:
'device'
};
try
{
const
hosted =
await
withTimeout
(
requestHostedFeedback
(submission, challenge, local),
HOSTED_TIMEOUT_MS
);
return
{ ...hosted,
tier
:
'hosted'
};
}
catch
{
return
{ ...local,
tier
:
'device'
};
}
}
function
withTimeout
(
promise, ms
) {
return
Promise
.
race
([
promise,
new
Promise
(
(
_, rej
) =>
setTimeout
(
() =>
rej
(
new
Error
(
'timeout'
)), ms)),
]);
}
这里有三个设计细节，我们花了比预想更长的时间才真正想明白。
首先，本地分析总是先执行，而且无条件执行，并不是等云端失败后才作为备用方案启动。它的运行开销很低，结果也是确定的，同时还会作为上下文传递给云端请求。这意味着云端模型面对的是一份已经完成初步诊断的代码，而不必从零开始分析，因此输出会更稳定，提示词也更短。
其次，我们会检查
navigator.onLine
，但绝不会完全相信它。这个属性只能告诉我们设备是否存在网络接口，并不能证明网络真的可用。即使手机连接的是一个需要登录认证的 Wi-Fi 网络，或者移动网络已经卡住，它仍然可能返回
true
。因此，我们只把它当作快速判断离线状态的信号。真正保护学生不被长时间等待拖住的，是超时机制。
最后，我们会在响应中记录反馈来自哪一级。我们不会隐瞒答案究竟由哪条路径生成。这不仅关系到我们自己的遥测数据，也很重要，因为来自能力较弱的第二级方案的反馈，会采用不同的表达方式。
让反馈真正有助于学习
我们早期的反馈非常简单，基本只有对错之分。无论学生提交的是
consolee.log("hi")
，还是根本没有理解函数是什么，收到的反馈都差不多：“这里错了，应该改成这样。”
试点中的一位老师准确指出了这个问题。她的学生虽然收到了纠正意见，但如果没有她坐在旁边指导，学生根本不知道该怎么改。这就违背了我们开发一个能够规模化服务学生的编程导师的初衷。
解决办法是，先衡量学生提交的答案距离正确答案有多近，再决定应该提供哪种反馈。如果只是差一点点，就提示具体哪个字符有问题；如果是代码结构上的错误，就解释背后的概念。
export
function
proximityHint
(
submitted, expected
) {
const
d =
levenshtein
(submitted, expected);
if
(d ===
0
)
return
null
;
if
(d >
2
||
Math
.
abs
(submitted.
length
- expected.
length
) >
2
) {
return
null
;
// 并非细微错误，转为提供概念性反馈
}
const
diff =
firstDivergence
(submitted, expected);
if
(diff.
kind
===
'extra'
) {
return
`快答对了！你多写了一个 "
${diff.char}
"。删掉它就对了。`
;
}
if
(diff.
kind
===
'missing'
) {
return
`快答对了！你漏写了字母 "
${diff.char}
"。加上它就对了。`
;
}
return
`快答对了！检查一下第
${diff.index +
1
}
个字符。`
;
}
我在团队内部常用一个比喻：两位老师批改同一份作业。经验不足的老师会在错误答案旁边打一个红叉，再写上正确答案。经验更丰富的老师则会准确圈出错误所在，并针对需要修改的地方写下提示。这次调整，让我们的反馈从第一种批改方式变成了第二种。而且整个过程完全由确定性逻辑实现，这意味着即使离线，反馈效果也完全一样。
多人共用设备，必须从架构层面考虑
在尼日利亚的试点中，10 位老师有 8 位认为，学生没有自己的设备是最大的障碍。有些手机由兄弟姐妹共用，有些是从老师那里借来的，还有些是在一节课上由一组学生轮流使用。
当时，我们的身份认证模型默认一台设备对应一名学生。如果两名学生共用一部手机，就必须不断退出和重新登录。在网络缓慢的情况下，每次切换都可能浪费一分钟的课堂时间。更糟糕的是，学生还可能因此丢失尚未同步到服务器的本地学习进度。
因此，账户切换并不是一项锦上添花的便利功能，而是实际使用环境提出的必然要求。现在，一台设备最多可以保存 20 个用户档案，只需轻点一下就能切换，无须彻底退出登录。从架构上看，这意味着我们必须按用户档案为每个本地存储空间设置独立的命名空间，让学习进度、翻译缓存和运行时状态彼此隔离，而不是在全局范围内共享。
const
scoped
= (
profileId, store
) =>
`
${store}
::
${profileId}
`
;
export
const
progressStore
= (
profileId
) => ({
get
:
(
k
) =>
idbGet
(
scoped
(profileId,
'progress'
), k),
set
:
(
k, v
) =>
idbSet
(
scoped
(profileId,
'progress'
), k, v),
});
如果你的产品面向的是多人共用设备的市场，就应该尽早加入这套机制。产品上线后再拆分一个全局共享的本地存储系统，成本远高于从第一天起就做好命名空间隔离。
实地数据改变了什么
我们前面提到的大多数经验，都来自两次实际部署。在印度北阿坎德邦，有四家机构使用受统一管理的设备运行我们的平台。在尼日利亚的拉各斯州和奥贡州，来自十所学校的十位老师开展了为期八周的试点，几乎完全依赖学生自己的手机。
这两次试点的对比，让我们能够区分哪些是平台本身的问题，哪些是使用环境带来的问题。对工程开发路线来说，这也是试点最有价值的地方。在尼日利亚，离线可靠性的平均评分为 4.0 分（满分 5 分），而所有低分都指向同一种情况：首次缓存尚未完成，网络就已经断开。这并不是离线功能本身不可靠，而是首次运行时的任务执行顺序出了问题。通过优先缓存离线运行必需的最小内容，再处理其他可选内容，就能在代码层面解决它。相比之下，学生能否获得设备，根本不是代码能够解决的问题。如果假装技术可以解决一切，只会浪费工程开发时间。
最让我感到挫败的发现，与语言有关。支持 246 种语言，本来就是我们开发这个平台的重要原因之一。但在试点中，10 位老师有 4 位从未尝试过本地语言界面，还有 1 位虽然试过，却不知道该怎么使用。而且，所有老师都在入门培训时看过这项功能的演示。
问题在于，语言切换按钮被放在页面底部。一个正在不断完成编程挑战的学生，根本没有理由特意滚动到页面底部。功能明明存在，有文档说明，也做过演示，但在实际使用中，它几乎就是隐形的。
功能是否容易被发现，与是否好用是两回事。如果用户必须事先知道该去哪里找，才能发现某个功能，那么对大多数人来说，这个功能实际上就等于不存在。我们正在把语言切换控件移到学生学习过程中自然能看到的位置。但更重要的收获，是我们现在会在发布任何功能前检查一个问题：不再问“如果告诉用户它在哪里，用户能不能找到”，而是问“用户按照自己的实际操作路径使用产品时，会不会自然遇到它”。
尚未解决的问题
还有三个问题没有解决。与其写一个看起来圆满的结尾，我更愿意把它们如实说出来。
在性能最弱的设备上，WebAssembly 运行时的冷启动速度仍然达不到我的预期。如果模块必须从缓存而不是网络加载，流式编译也只能解决其中一部分问题。
端侧模型的质量，是离线反馈能力真正的上限。目前，确定性分析承担的工作量仍然超出了我的期望。它之所以能够表现不错，很大程度上是因为编程题有可以验证的正确答案。如果换成答案没那么明确的领域，就没有这样的备用手段了。
存储仍然是个难缠的问题。配额数据经过填充处理，缓存清理机制不透明，而且不同浏览器对
persist()
持久化存储请求的支持也不一致。本文介绍的这些防御性设计，只是在弥补 Web 平台自身的不足，并没有真正解决这些问题。
但这些都不足以成为放弃这种开发方式的理由。另一种选择，是继续假设每个学生都有笔记本电脑和宽带网络，而这会把大多数真正需要这类产品的人拒之门外。这条路在工程实现上确实更难，但能够服务的人群规模，也因此扩大了数十亿。
原文链接：
https://www.infoq.com/articles/building-offline-first-android-app-low-end-devices/
声明：本文为
InfoQ 翻译，
不代表平台观点，也不构成投资建议，未经许可禁止转载。
END
转发，点赞，在看，安排一下？
今日好文推荐
顶尖 AI 实验室正在成为“人才黑洞”！Claude Code 团队工程师离职后首次受访
2.5小时一个零日，400多个root提权：Linux被AI挖成了筛子，人类逆向几周才看懂一个
DeepSeek Harness 日活154万，官方开始给插件作者发Token：Agent 生态要靠开发者了
刚刚，OpenAI 发布 GPT‑6 Cyber，横扫两大开源项目：Firefox 挖出 81 个高危漏洞，Linux 曝光 948 条提权路径
