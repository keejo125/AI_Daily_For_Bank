---
publish_time: 1788951552
link: https://mp.weixin.qq.com/s/GqDaoteq20DSPHHg74GTrQ
source: 阿里云基础设施
status: confirmed
category: 国内
is_model_related: false
digest: |
  阿里云容器服务 Knative 将“会话（Session）”从业务概念下沉为 Serverless 平台原语，应对 Agent 作为有状态长会话负载对算力的极致消耗。传统 Kubernetes 按请求分流会打碎会话、按 CPU 弹性误判负载、常驻副本烧穿预算；Knative 让平台原生理解会话——路由按会话绑定、灰度按会话放量、弹性按会话计数、休眠按会话——实现“不用即缩到零、用时秒级拉起”，在算力紧缺下最大化每份算力价值，并构建会话级流量治理与全链路可观测。
title: 破局算力紧缺：阿里云 Knative 将"会话"升级为平台原语，重塑 AI Agent 基础设施
---

# 破局算力紧缺：阿里云 Knative 将"会话"升级为平台原语，重塑 AI Agent 基础设施

来源：阿里云基础设施
原文链接：https://mp.weixin.qq.com/s/GqDaoteq20DSPHHg74GTrQ

AI Agent 正在以前所未有的速度吞噬算力：一个 Agent 背后往往是一个独占的沙箱环境，而全球算力供给却日趋紧张。
一边是爆发式增长的 Agent 负载，一边是战略瓶颈级的算力约束
——如何极致释放每一份算力的价值，成为 AI 基础设施的核心命题。阿里云容器服务 Knative 给出的答案是：
全面拥抱 AI Agent，在完全兼容社区标准的基础上，将"会话（Session）"从业务概念下沉为 Serverless 平台原语
，并围绕 Agent 工程化落地的真实痛点，构建了一套完整的运行时能力矩阵——会话级流量治理、极致弹性与成本优化、会话维度全链路可观测。
本文基于 KubeCon + CloudNativeCon + OpenInfra Summit + PyTorch Conference 2026 大会上，Lightning Talk 议题《Can Stateful AI Agents Scale to Zero?》- 让“会话”成为 Serverless 平台的一等公⺠，进行了深度解析与拓展。
算力紧缺时代，Agent 是"最贵"也"最难伺候"的工作负载
传统 Web 服务是无状态的：任意请求打到任意副本，结果都一样，算力可以被切成任意小的碎片自由调度。而 AI Agent 完全相反——它是典型的
有状态长会话
工作负载：
会话即状态
：一个 Agent 会话背后是一个沙箱，保存着代码执行环境、文件系统、运行中的进程与上下文记忆。请求一旦"串门"到别的副本，上下文直接丢失；
负载即会话数
：Agent 的资源消耗与"活跃会话数"强相关，而不是 QPS 或 CPU。一个会话可能十分钟不发请求（用户在思考），但沙箱必须留着；
算力成本极度敏感
：GPU/大规格沙箱按秒计费，空闲即烧钱。在算力紧缺的今天，"不用就缩到零、用时秒级拉起"不是加分项，是生存刚需。
把这三个特性放到传统 Kubernetes 的发布与弹性体系面前，结论很残酷：
按请求分流的灰度会打碎会话，按 CPU/并发的弹性会误判负载，常驻副本的部署模式会烧穿预算
。
问题的根源只有一个：在传统平台的世界观里，"会话"不存在——它只是业务层的概念，平台看不见、管不着。
破局思路：把"会话"升级为 Serverless 原语
阿里云容器服务 Knative 的解法是釜底抽薪：
让平台原生理解会话
。
路由按会话绑定、灰度按会话放量、弹性按会话计数、休眠按会话冻结、唤醒按会话恢复、监控按会话透出——"会话"与 Pod 一样，成为平台的一等公民。
为什么是 Knative：标准化底座，天生可扩展
把会话能力做在哪一层，是个关键选择。常见的做法是每个 Agent 平台在业务层自建一套：自建会话网关、自建弹性控制器、自建休眠调度——重复造轮子，且每一套都要重新踩一遍分布式一致性的坑。我们选择把它沉淀到 Knative，基于两个判断：
其一，Knative 是 CNCF 标准化的 Serverless 能力底座，Agent 需要的地基能力都是现成的。
一份 Knative Service YAML，天生自带四样东西：
不可变版本（Revision）
——会话灰度的版本地基
声明式流量切分（Route/traffic）
——会话比例放量的语义载体
缩容至零与请求驱动弹性
——休眠唤醒的前提
标准 API 与开放生态
——无厂商锁定，社区工具链直接可用。
在这之上做会话，是"补一块拼图"；离开它另起炉灶，则要重建整张拼图。
其二，Knative 的架构为扩展而生，会话原语恰好能"长"在它的扩展点上。
Knative 扩展点
会话原语的落点
Activator 本就位于请求路径，handler 链可插拔
会话提取、绑定路由、唤醒等待队列直接插入链路，无需新增网关跳数
弹性指标可插拔（concurrency / rps / ...）
新增
session
指标，复用整套指标采集-决策-执行链路
PodAutoscaler 抽象解耦"算什么"与"操作什么"
弹性结果可以驱动 Deployment，也可以驱动 Sandbox 工作负载（冻结/唤醒）
正因为这些扩展点的存在，会话原语才能以"
原位增强
"而非"平行私有体系"的方式落地——这既是工程成本的节约，也是对社区兼容性的结构性保障。
这一切建立在
完全兼容社区标准
的前提上：
标准 Knative Service API 不变，能力通过注解按需开启（opt-in）；
未开启会话注解的服务，行为与社区版完全一致，存量负载零影响；
社区的缩容至零、按需弹性、版本灰度等核心能力全部保留并增强。
围绕这个原语，形成三大能力矩阵：
能力
解决的问题
算力价值
会话级流量治理
会话保持、1:1 精准转发、会话比例灰度
交互连续稳定，发布不重建会话、不浪费重算算力
极致弹性与成本优化
会话弹性 + Sandbox 休眠/唤醒 + 暖池
算力占用随真实活跃会话数线性，闲置成本趋零
全链路可观测
会话维度指标透出
运行状态透明可控，容量决策有据可依
架构实现：一张图看懂会话原语如何落地
所有能力都是对标准 Knative Serving 组件的
原位增强
，没有引入平行的私有控制面：
各组件的职责分工一句话版：
组件
社区职责
会话原语增强
Activator
缩零时缓冲请求、上报并发
会话提取与双层绑定路由、灰度版本选择、唤醒等待队列、会话指标
Queue-Proxy
并发控制、指标、优雅排空
会话活跃度上报，支撑冷启动后的会话恢复
Autoscaler
按并发/RPS 弹性
新增
session
指标：会话数并集 + 阻塞需求驱动副本计算
Sandbox 控制器
—（新增）
沙箱生命周期：冻结/唤醒/暖池认领，与弹性链路正交协同
共享会话存储
—（新增）
Redis/OSS 持久化绑定关系，跨网关一致、故障可恢复
请求链路上只有一个关键动作被改变：
路由决策从“选一个副本”变成“先认会话、再定版本、最后到实例”
；控制面的弹性与休眠唤醒则完全异步，不阻塞业务请求。
下面逐一展开。
会话级流量治理：1:1 精准转发与会话灰度
会话保持：交互连续性的地基
开启会话保持后，Activator 从请求中自动提取会话标识，将「会话 → 后端实例」的绑定关系持久化到共享存储（Redis 或 OSS），多Activator实例视图一致、重启不丢。
配合
autoscaling.knative.dev/target: "1"
，可实现
严格的 1:1 精准转发
——每个沙箱独占服务一个会话，物理隔离，互不污染。
会话灰度： 新版本放量，存量会话无感
传统按请求比例的灰度对 Agent 是灾难：同一会话的第 1 个请求进 v1、第 2 个请求进 v2，上下文当场错乱。而重建会话意味着沙箱重建、上下文重算——
每一次被打断的会话，都是白白烧掉的算力
。
启用会话灰度后，流量比例的语义升级为
新会话比例
，路由决策变成三级优先级：
优先级
路由依据
用途
1
显式版本 Header（
Knative-Serving-Header-Tag
）
发布前定向验证、调试
2
会话已绑定的版本
存量会话精准回源，全程无感
3
流量比例加权轮询
仅对
新会话
生效
首次绑定，持久化存储
：新会话按比例选版本后，「会话 → 版本」绑定写入共享存储；
绑定优先于比例
：即使旧版本比例已调到 0%，存量会话依然精准路由回去，直到会话过期；
自然收敛
：旧版本不再接新会话，存量会话随
session-expiry
陆续过期后自动缩容至零——发布全程无一次强制断连，无一次会话重建。
极致弹性与成本优化
会话驱动的自动弹性
Agent 沙箱在用户思考时 CPU 接近于零、并发请求为零——但它承载着活跃会话，绝不能缩掉。传统基于 CPU（HPA）或请求并发（KPA）的弹性都会误判。我们引入
session
弹性指标，让扩缩容"看得懂"Agent：
期望副本数 =
ceil
( (活跃会话数 + 阻塞需求) / 每实例目标会话数 )
两个工程细节保证了这个公式在生产环境的正确性：
多Activator会话数取并集
：各Activator实例只知道自己路由的会话，全局会话数必须做去重并集，避免副本数抖动；
阻塞需求（Blocked Demand）兜底冷启动
：缩容至零后请求到来，阻塞在Activator的请求数直接计入弹性信号，破解"没实例 → 没指标 → 不扩容"的死锁。
Sandbox 休眠/唤醒：闲置算力即刻归还
这是算力节约的核心机制，分两层：
会话空闲休眠
：会话超过
session-timeout
无请求，其绑定的沙箱被
冻结或删除
——计算资源（CPU/GPU/内存）立即释放归还资源池；
服务整体归零
：所有会话过期后副本归零，成本归零。
唤醒的关键在"
精准
"二字：用户回来时，唤醒控制器从Activator拉取等待中的会话清单，
只恢复该会话绑定的那一个沙箱
，而不是全量拉起。100 个休眠会话中只有 1 个用户回来，就只为 1 个沙箱付费——这正是"按需使用"的字面含义。
三级成本-体验梯度
对不同延迟敏感度的服务，平台提供完整的梯度选择：
状态
算力成本
唤醒延迟
适用
预热池（
serving.knative.dev/warm-pool
）
全额
0（直接服务）
延迟敏感的头部服务
冻结暖池（预创建待认领沙箱）
近似存储成本
毫秒级
通用新会话加速，跳过镜像拉取与环境初始化
缩容至零
0
秒到十秒级
长尾服务
全链路可观测：让每一份算力的去向透明可控
弹性和发布都建立在"会话"这个抽象上，可观测性也必须跟上。平台在网关侧原生透出会话维度的Prometheus 指标：
指标
含义
典型用法
activator_session_count
各版本当前活跃会话数
灰度放量时对比新旧版本会话分布；容量水位 = 会话数 / (副本数 × 每副本会话上限)
activator_session_blocked_demand
阻塞等待会话槽位/后端的请求数
持续 > 0 说明扩容不及时或唤醒链路异常，直接告警
activator_request_count
/
activator_request_latencies
版本请求量与延迟分布
传统流量视角，与会话视角互补
所有指标携带标签——既支持按版本切片，也支持下钻到单个会话：灰度的每一步放量，新版本的会话分布、阻塞情况、错误率、会话延迟都能在大盘上直接对比。
这些指标与
request_count
、
request_latencies
等经典请求指标一起，以原生 Prometheus 格式在网关既有的指标端口上暴露——
无需修改抓取配置，升级不炸大盘、不改告警规则
。
一次典型的灰度放量，看四个数就够了：
# 新版本是否在正常接收新会话
activator_session_count
{revision_name=
"my-agent-00002"
}
# 新版本是否出现请求阻塞（扩容/唤醒是否健康）
activator_session_blocked_demand
{revision_name=
"my-agent-00002"
} >
0
# 新旧版本错误率对比
sum
by (revision_name) (rate(activator_request_count{response_code_class=
"5xx"
}[
5
m]))
# 新版本每个会话的 P95 响应延迟（下钻定位变慢的会话）
histogram_quantile
(
0
.
95
, sum by (le, context_id) (
rate
(activator_request_latencies_bucket{revision_name=
"my-agent-00002"
}[
5
m])))
会话维度的指标同样是算力治理的仪表盘：
session_count
是真实负载水位，
blocked_demand
是算力缺口信号，会话级延迟是体验基线——
Agent 的每一份算力用在哪、缺在哪、慢在哪，一目了然
。
动手实践：15 分钟完成一次会话级灰度发布
环境准备
：
已开通阿里云 ACK/ACS 集群, 并安装
ack-agent-sandbox-controller 组件
部署 Knative
生产环境或多副本Activator：提前创建云数据库 Tair（兼容 Redis）实例作为共享会话存储。
单 Activator副本且测试环境
，可用默认内存模式。
第 1 步：部署开启会话保持的 Agent 服务
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
name: my-agent
spec:
template:
metadata:
annotations:
# 启用 Sandbox 工作负载类型
serving.knative.dev/workload-type:
"sandbox"
# 开启会话保持（灰度会话绑定随之生效）
serving.knative.dev/session-affinity:
"true"
# 指定用于提取会话标识的 Cookie 名称
serving.knative.dev/session-affinity-cookie:
"app"
# 会话空闲超时（默认 30m），超时后实例可被休眠
serving.knative.dev/session-timeout:
"30m"
# 会话过期时间（版本绑定的生命周期与其一致，随请求滑动续期）
serving.knative.dev/session-expiry:
"2h"
# 按活跃会话数扩缩容，每实例严格绑定 1 个会话
autoscaling.knative.dev/metric:
"session"
autoscaling.knative.dev/target:
"1"
spec:
containers:
- image: registry-cn-wulanchabu-vpc.ack.aliyuncs.com/acs/knative-samples-helloworld-go-session:v1.0-bfdce98
第 2 步：发布新版本，声明新会话比例
更新镜像生成新 Revision 后，在
spec.traffic
中将 5% 的
新会话
导入新版本：
spec:
traffic:
- revisionName:
my
-agent-
00001
percent:
95
- revisionName:
my
-agent-
00002
percent:
5
第 3 步：三步验证
# ① 会话粘性：同一会话标识连续请求，应始终返回同一版本
for
i in $(seq
1
10
); do
curl
-s -H
"Host: my-agent.default.example.com"
\
-H
"Cookie: app=11"
http://<ALB地址>
done
# ② 新会话分流：不同会话标识约按 95:5 比例分布到两个版本
for
i in $(seq
1
20
); do
curl
-s -H
"Host: my-agent.default.example.com"
\
-H
"Cookie: app=$i"
http://<ALB地址>
done
# ③ Tag 定向路由：显式指定新版本验证（该会话随之重新绑定到新版本）
curl
-H
"Host: my-agent.default.example.com"
\
-H
"X-Session-ID: test-session-001"
\
-H
"Knative-Serving-Header-Tag: my-agent-00002"
\
http://<ALB地址>/version
发布节奏
：验证（percent: 0 + Tag 定向）→ 放量（5% → 20% → 50% → 100%，每步观察会话成功率与延迟）→ 收敛（旧版本存量会话自然排干、缩容至零）→ 回滚（比例调回即止血）。
写在最后：面向 Agent 时代的算力节约型基础设施
回看这套体系，核心只做了一件事：
把"会话"从业务概念升格为 Serverless 平台原语
——
路由按会话绑定，灰度按会话放量，发布对存量会话零感知，不浪费一次重算；
弹性按会话计数，阻塞需求兜底冷启动，热备水位兜底突发，算力占用随真实活跃度线性；
休眠按会话粒度冻结，唤醒按会话粒度精准恢复，闲置即归还、使用才计费；
监控按会话维度透出，算力的去向与缺口透明可控。
对业务团队而言，这一切收敛为 Knative Service 上的几行注解：
annotations:
serving.knative.dev/workload-type:
"sandbox"
serving.knative.dev/session-affinity:
"true"
serving.knative.dev/session-affinity-cookie:
"app"
serving.knative.dev/session-timeout:
"30m"
autoscaling.knative.dev/metric:
"session"
autoscaling.knative.dev/target:
"1"
剩下的——流量治理、弹性伸缩、休眠唤醒、可观测——交给平台。
在算力成为战略瓶颈的今天，按需使用的 Serverless 是降本增效的关键路径。阿里云容器服务正以开放的姿态、完全兼容社区标准的方式，将 Knative 打造为
面向 Agent 时代的算力节约型基础设施
，助力开发者在有限算力下高效、低成本地规模化部署 AI Agent。
AI Agent 的生产化浪潮才刚刚开始，欢迎在阿里云容器服务 Knative 中体验上述能力，也欢迎有兴趣的开发者多交流。
阿里云 Knative 钉钉技术交流群
钉群号：23302777
相关产品
上手指路：复制链接到浏览器查看
容器服务 Knative
:
https://help.aliyun.com/zh/ack/ack-managed-and-ack-dedicated/user-guide/knative-overview
Agent Sandbox
：
https://help.aliyun.com/zh/cs/user-guide/agent-sandbox
