---
publish_time: 1794314959
link: https://mp.weixin.qq.com/s/ws-AOgs7ZiqL4EExGZdBrA
source: 阿里云基础设施
status: confirmed
category: 国内
is_model_related: false
digest: |
  阿里云智能体沙箱 Agent Sandbox 极速版引入 Agent Identity（智能体身份）机制，为沙箱内运行的 Agent 发放独立电子身份与临时凭据，替代把真实密钥写入环境变量或文件的做法，降低凭据泄露风险；临时凭证到期自动更新、用户授权失效可重新授权，使多服务编排下的权限与凭据管理更可控。
title: 阿里云 Agent Sandbox 极速版：让沙箱拥有电子身份
---

# 阿里云 Agent Sandbox 极速版：让沙箱拥有电子身份

来源：阿里云基础设施
原文链接：https://mp.weixin.qq.com/s/ws-AOgs7ZiqL4EExGZdBrA

一个知识助手整理资料，往往要先从 OSS 读取文件，调用模型生成摘要，再把结果写入用户的在线文档。一次任务涉及多个服务，每个服务都有自己的认证方式和权限范围。
开发者既要让 Agent 调用这些服务，也要妥善管理凭据。真实密钥一旦放进沙箱的环境变量或文件，执行任务的脚本和依赖就可能读取它们。临时凭证到期需要更新，用户授权失效后也可能需要重新授权。
阿里云智能体沙箱 Agent sandbox 极速版
通过
Agent Identity
管
理这些访问所需的凭据。应用为沙箱指定工作负载身份，配置访问权限和凭证注入规则；沙箱内的代码通过目标服务的 SDK 或 HTTP 客户端发出请求，平台在请求出网时填入认证信息或重新签名。真实凭据由平台在沙箱外管理和使用。
身份配置由应用后端提交，业务请求由沙箱发出。平台校验请求的网络来源，找到沙箱绑定的身份，再选择访问目标服务所需的凭据。沙箱内的代码自行声明另一个身份，不会改变这一绑定关系。
沙箱如何使用身份访问服务
访问不同的服务，需要准备的凭据也不同。阿里云资源的访问权限由工作负载身份关联的 RAM 角色授予；模型和业务 API 使用的密钥、OAuth 应用信息，则保存在
Agent Identity
的
凭证提供商中。下面四种方式对应常见的访问场景：
访问场景
使用的凭据
平台的处理方式
调用模型或业务 API
API Key
从提供商获取密钥，填入认证请求头
访问 OSS 等云资源
RAM 角色的 STS 临时凭证
按受支持的阿里云签名协议重新签名
以应用身份调用业务服务
OAuth 应用访问令牌
通过客户端凭据流程（M2M）取得并注入令牌
以用户身份访问服务
OAuth 用户访问令牌
用户完成授权后，通过授权码流程取得并注入令牌
选择 OAuth 接入方式时，先确定任务使用谁的权限。以应用自身的权限访问服务，使用客户端凭据流程（M2M）；代表某位用户执行操作，使用用户委托授权，并由该用户确认授权范围（scope）。
接入模型、云资源和业务服务
准
备身份与沙箱环境
下面以
knowledge-assistant
工作负载身份说明接入过程。先按
工作负载
身份管理[1]
创建身份并关联 RAM 角色，再配置业务所需的
资源与出站凭
据权限[2]
。使用托管凭据时，还需要授权该工作负载身份使用相应的凭证提供商。
RAM 角色需要哪些权限，取决于任务的访问方式：访问 OSS 等云资源，需要相应的资源操作权限；获取托管 API Key，需要
agentidentitydata:GetResourceAPIKey
；获取 OAuth 令牌，需要
agentidentitydata:GetResourceOAuth2Token
。
使用提示
：真实凭据由平台在沙箱外管理，沙箱中的代码仍可通过绑定身份访问已授权的资源和服务。请按任务需要配置资源范围、操作权限和访问目标，避免将其他业务的权限一并授予沙箱，减少异常调用或恶意代码可能造成的影响。
身份准备好后，在应用后端按
接入指南[3]
安装 E2B SDK，配置
E2B_API_KEY
、
E2B_API_URL
和
E2B_DOMAIN
，并确认目标账号和地域支持该能力。后面的创建沙箱示例都在后端运行；访问目标服务的代码在沙箱内执行。
E2B_API_KEY
用于管理沙箱，应保存在后端，与调用模型或业务服务的 API Key 区分开。
沙箱环境也需要满足 HTTPS 凭证注入和请求重签的要求：客户端必须信任平台 CA。符合版本要求的官方模板和受支持的
Debian/Ubuntu
自定义模板已配好平台 CA；Java、使用私有证书库的客户端等需要额外配置信任。请求头注入当前支持 HTTP 80 和 HTTPS 443 端口，以下示例均使用 HTTPS。模板版本、证书和协议要求见
凭证使用限制[4]
。
使用托管 API Key 调用模型
以百炼模型调用为例，先
在
Agent Identity
中创建名为
summary-model
的
API Key 凭证提供商[5]
，保存具备对应模型调用权限的 API Key，并授权
knowledge-assistant
获取其中的密钥。
创建沙箱时，应用后端指定工作负载身份，并配置模型域名和 API Key 的引用方式：
import { Sandbox }
from
"e2b"
;
const
sandbox
= await Sandbox.
create
(
"code-interpreter-v1"
, {
metadata
: {
"fc.sandbox.identity.name"
:
"knowledge-assistant"
},
network
: {
allowOut
: [
"dashscope.aliyuncs.com"
],
denyOut
: [
"0.0.0.0/0"
],
rules
: {
"dashscope.aliyuncs.com"
: [{
transform
: {
headers
: {
"Authorization"
:
"Bearer ${fc.sandbox.identity.apiKey:summary-model}"
}
}
}]
}
}
});
Authorization
中的表达式引用了
summary-model
凭证提供商。请求发往模型服务时，平台获取其中的 API Key，写入认证请求头。
配置完成后，在沙箱内调用百炼北京地域的
OpenAI 兼容接口[6]
，无需自行设置
Authorization
：
curl
--fail --silent --show-error
\
https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
\
-H 'Content-Type: application/json'
\
-d '{
"model"
:
"qwen-plus"
,
"messages"
:[{
"role"
:
"user"
,
"content"
:
"请将这段资料概括为一句话：本季度完成了知识库整理，新增了搜索功能，并更新了团队文档。"
}]}'
模型服务仍按 API Key 和模型权限校验请求，并返回生成结果。如果改用强制要求传入 API Key 的模型 SDK，可以传入占位值，平台会覆盖对应的认证请求头。
这份配置还通过
allowOut
和
denyOut
放行模型域名，拒绝其他 IPv4 出站访问。只配置
allowOut
不会默认拒绝其他目标，凭证注入规则也不会自动放行网络；具体规则见
网络访问控制[7]
。
更换模型服务或使用业务空间专属域名时，请求地址中的域名必须与注入规则配置的域名一致，子域名需要单独配置。其他认证格式和配置方式见
托管凭证注入[8]
。
使用 STS 重签访问阿里云服务
访问 OSS、ECS、VPC、FC 等阿里云服务时，可以使用 STS 请求重签。沙箱内的阿里云 SDK 使用占位 AK/SK 生成签名请求，平台在出网时使用真实 STS 临时凭证重新签名。接入前需确认目标接口采用平台支持的签名协议，并配置相应的角色权限和网络访问规则。
同一个工作负载身份和 RAM 角色可以用于多个任务，再通过会话策略（Session Policy）限定每次任务的资源范围。下面以 OSS 为例：资料保存在
project-materials
Bucket
中，本次任务的读取范围限定为
task-42/
前缀下的对象。
身份关联的 RAM 角色需具备 OSS 读取权限。本例通过 OSS Python SDK（
oss2
）调用 OSS API，无需将 Bucket 挂载到沙箱文件系统。平台负责请求重签，OSS 仍根据角色权限、会话策略和资源侧访问控制规则完成鉴权。
运行示例前，先确保沙箱中已安装
OSS Python SDK V1[9]
（包名
oss2
）。可以预装到模板，也可以在创建沙箱后安装。示例将网络限制为 OSS 域名；若创建后在线安装依赖，需要先放行相应包源，安装后再收紧访问范围，也可以离线安装。
应用后端创建沙箱时，提交会话策略和 OSS 重签域名。将下面示例中的 Bucket、地域、对象键前缀和模板 ID 替换为实际值，后续 Python 代码使用同一组 OSS 资源：
import
{
Sandbox
}
from
"e2b"
;
const
ossHost =
"project-materials.oss-cn-hangzhou.aliyuncs.com"
;
const
rolePolicy = {
Version
:
"1"
,
Statement
: [{
Effect
:
"Allow"
,
Action
: [
"oss:GetObject"
],
Resource
: [
"acs:oss:*:*:project-materials/task-42/*"
]
}]
};
const
sandbox =
await
Sandbox
.
create
(
""
, {
metadata
: {
"fc.sandbox.identity.name"
:
"knowledge-assistant"
,
"fc.sandbox.identity.role.policy"
:
JSON
.
stringify
(rolePolicy),
"fc.sandbox.identity.role.domains"
:
JSON
.
stringify
([ossHost])
},
network
: {
allowOut
: [ossHost],
denyOut
: [
"0.0.0.0/0"
]
}
});
本次任务的实际权限，是 RAM 角色权限与会话策略的交集。
fc.sandbox.identity.role.domains
用显式配置的域名列表替换默认的
*.aliyuncs.com
重签范围；网络规则则控制请求能否到达目标。字段和默认值见
阿里云 STS 注入[10]
。
接下来，在沙箱内用占位凭据初始化 OSS Python SDK，并读取对象：
import oss2
auth = oss2.Auth(
"fake-access-key-id"
,
"fake-access-key-secret"
)
bucket = oss2.Bucket(
auth,
"https://oss-cn-hangzhou.aliyuncs.com"
,
"project-materials"
,
)
result = bucket.get_object(
"task-42/input.txt"
)
print(result.read().decode(
"utf-8"
))
应用继续使用
get_object()
读取数据，STS 临时凭证的获取和使用由平台完成。角色权限与会话策略共同限定读取范围，因此可以复用角色，为不同任务分别配置资源权限。
通过 OA
uth 以应用身份访问
服务
有些业务 API 使用 OAuth 访问令牌进行认证。任务无需用户参与、使用应用自身权限时，可以采用客户端凭据流程（M2M）。在 Agent Identity 中配置支持
M2M 的
OAuth 凭证提供商[11]
，保存客户端 ID（Client ID）、客户端密钥（Client Secret）等信息，平台便可据此申请应用访问令牌。
下面以查询业务记录为例，使用名为
business-
api
的凭证提供商获取令牌。业务域名、接口路径和
records:read
scope 都需按目标服务调整：
import { Sandbox }
from
"e2b"
;
const
sandbox
= await Sandbox.
create
(
"code-interpreter-v1"
, {
metadata
: {
"fc.sandbox.identity.name"
:
"knowledge-assistant"
},
network
: {
allowOut
: [
"api.example.com"
],
denyOut
: [
"0.0.0.0/0"
],
rules
: {
"@fc.sandbox.identity"
: [{
transform
: {
headers
: {
"fc.sandbox.identity.oauth.m2m.options"
: JSON.
stringify
({
"business-api"
: {
scopes
: [
"records:read"
] }
})
}
}
}],
"api.example.com"
: [{
transform
: {
headers
: {
"Authorization"
:
"Bearer ${fc.sandbox.identity.oauth.m2m:business-api}"
}
}
}]
}
}
});
配置完成后，沙箱内直接调用业务接口，平台在请求出网时注入 Bearer 令牌：
curl
--fail
--silent
--show-error
\
https://api.example.com/v1/records
业务服务根据应用已获得的权限和令牌中的 scope 处理请求。业务代码沿用原有 HTTP 接口，无需自行申请和保存真实令牌。
示例中的
@fc.sandbox.identity
是供平台读取的保留控制项，用来提交获取令牌所需的参数。
allowOut
中配置实际访问的服务域名；控制项中的参数由平台处理，不会作为业务请求头发送。options 中的提供商名称必须与引用表达式一致，且区分大小写；是否需要
scopes
、
audience
等参数，取决于目标服务，详见
M2M OAuth[12]
注入
。
如果任务需要使用某位用户的权限，接入时还需要提交用户身份，并处理该用户的授权。
通过 OAuth 代表用户访问服务
当知识助手需要读取用户自己的在线文档时，可以采用
OAuth 用户委托授权[13]
。用户在文档服务中确认权限后，Agent Identity 通过授权码流程取得代表该用户的访问令牌。
应用后端创建沙箱时，一并提交当前用户身份。需要用户授权时，创建接口返回 HTTP 403 和授权链接。后端将链接展示给用户，待用户完成全部授权后，再重试创建请求；创建成功后，应用再让沙箱执行文档任务。如果用户已有所需的有效授权，平台可直接取得令牌，无需再次引导授权。
应用还可以在工作负载身份中开启会话绑定，要求后端在授权回调中核对当前用户，并向 Agent Identity 确认授权会话。下图和后面的示例采用这一方式，因此重试创建前需要完成回调确认。未开启会话绑定时，无需提交
state
和
callbackUrl
，用户完成全部授权后即可重试。
1. 提交用户身份和访问范围
先配置支持用户委托的
OAuth 凭证提供商[14]
，命名为
document-service
。授权端点、令牌端点、Client ID、Client Secret 和重定向地址需与目标文档服务对应。本例开启了会话绑定，因此还需在工作负载身份中登记应用回调地址，并为处理回调的后端 RAM 身份配置
会话确认权限[15]
。
后端根据已验证的登录会话确定用户 ID。该 ID 在业务系统中应保持稳定且唯一，多租户应用可使用
t
e
nantId:userId
。
发起创建前，后端生成随机
state
，将它与当前登录会话的关联保存在自己的存储中，供回调时校验。随后提交用户 ID、回调参数和所需的文档访问范围。示例域名、接口和 scope 需替换为目标服务的实际配置：
const
createRequest = {
templateID
:
"code-interpreter-v1"
,
timeout
:
300
,
// HTTP API 的沙箱超时单位为秒
secure
:
true
,
metadata
: {
"fc.sandbox.identity.name"
:
"knowledge-assistant"
},
network
: {
allowOut
: [
"docs.example.com"
],
denyOut
: [
"0.0.0.0/0"
],
rules
: {
"@fc.sandbox.identity"
: [{
transform
: {
headers
: {
"fc.sandbox.identity.oauth.userFederation.userId"
:
""
,
"fc.sandbox.identity.oauth.userFederation.state"
:
""
,
"fc.sandbox.identity.oauth.userFederation.callbackUrl"
:
"https://app.example.com/oauth/callback"
,
"fc.sandbox.identity.oauth.userFederation.options"
:
JSON
.
stringify
({
"document-service"
: {
scopes
: [
"documents:read"
] }
})
}
}
}],
"docs.example.com"
: [{
transform
: {
headers
: {
"Authorization"
:
"Bearer ${fc.sandbox.identity.oauth.userFederation:document-service}"
}
}
}]
}
}
};
2. 从创建响应中取得授权链接
需要用户授权时，创建接口返回 HTTP 403，错误码为
ResourceAuthorizationRequired
。后端从
details.authorizations[].authorizationUrl
取得授权链接，响应示例如下：
{
"
code
":
"ResourceAuthorizationRequired"
,
"message"
:
"User authorization is required."
,
"details"
: {
"authorizations": [{
"providerName":
"document-service"
,
"authorizationUrl"
:
"https://auth.example.com/authorize?..."
}]
}
}
将响应中的真实链接展示给当前用户，不要自行拼接。如果多个凭证提供商都需要授权，用户需完成全部授权，后端再重试原请求。返回这一错误时，沙箱尚未创建；若是更新操作，则整次更新不生效，原配置继续保留。
下面的后端函数直接读取创建接口响应，返回待授权信息或已创建的沙箱 ID：
async
function
createDocumentSandbox
(
requestBody
) {
const
apiUrl = process.
env
.
E2B_API_URL
;
const
apiKey = process.
env
.
E2B_API_KEY
;
if
(!apiUrl || !apiKey)
throw
new
Error
(
"缺少 E2B_API_URL 或 E2B_API_KEY"
);
const
response =
await
fetch
(
`
${apiUrl.replace(/\/+$/,
""
)}
/sandboxes`
, {
method
:
"POST"
,
headers
: {
"Content-Type"
:
"application/json"
,
"X-API-KEY"
: apiKey
},
body
:
JSON
.
stringify
(requestBody),
signal
:
AbortSignal
.
timeout
(
60000
)
});
const
payload =
await
response.
json
();
if
(response.
status
===
403
&& payload.
code
===
"ResourceAuthorizationRequired"
) {
const
authorizations = payload.
details
?.
authorizations
;
if
(!
Array
.
isArray
(authorizations) || authorizations.
length
===
0
) {
throw
new
Error
(
"未收到用户授权链接"
);
}
return
{
status
:
"authorization_required"
, authorizations };
}
if
(response.
status
!==
201
|| !payload.
sandboxID
) {
throw
new
Error
(
`创建沙箱失败，HTTP
${response.status}
`
);
}
return
{
status
:
"ready"
,
sandboxId
: payload.
sandboxID
};
}
let
result =
await
createDocumentSandbox
(createRequest);
3. 确认授权并重试创建
本例开启了会话绑定。用户在文档服务完成授权后，Agent Identity 将
session_uri
和
s
tate
返回应用回调地址。后端先核对
state
及当前登录会话，确认回调来自最初发起任务的用户。
核对通过后，后端调用
CompleteResourceTokenAuth
，传入
session_uri
和与创建请求一致的用户身份，完成授权会话确认。接口调用成功后，再重试创建请求。回调处理见
获取 OAuth Access Token[16]
；未开启会话绑定时，用户完成全部授权后直接重试即可。
后端再次执行
result = await createDocumentSandbox(createRequest)
。若仍返回
authorization_required
，继续处理本次返回的授权链接；取得
ready
状态和
res
ult.sa
ndboxId
后，通过 E2B SDK 的
Sandbox.connect(result.sandboxId
)
连接沙箱。随后可在沙箱内运行文档请求，无需设置认证请求头：
curl
--fail
--silent
--show-error
\
https://docs.example.com/v1/documents
平台为请求填入当前用户的访问令牌，文档服务根据用户权限和已授予的 scope 决定可读取的内容。需要写入文档时，还应申请服务要求的写入 scope，并取得相应授权。
4. 已有用户 JWT 时
上面的示例由可信后端提交 UserId。如果登录系统已提供 Agent Identity 信任的用户 JWT，也可以将
fc.sandbox.identity.oauth.userFederation.userId
换成
fc.sandbox.identity.oauth.userFederation.jwt
，提交有效 JWT 的原始串，不加
Bearer
。JWT 与 UserId 二选一；使用 JWT 前需配置并关联
入站身份提供商[17]
。
任务运行中的访问管理
调整访问配置
任务执行过程中，应用可能需要访问新的服务，或改用另一位用户的授权。沙箱运行期间，可以通过
updateNetwork
调整出网范围、凭证注入规则、引用的凭证提供商和 OAuth 授权参数，也可以提交新的 JWT 或 UserId 切换委托用户。
平台会用本次提交的网络配置替换已有配置。因此，每次更新都应包含要保留的完整配置，包括
allowInternetAccess
、
allowOut
、
denyOut
和
rules
。省略
rules
、传入
null
或
{}
都会清空已有注入规则。具体操作见
更新网络配置[18]
。
M2M options 单独处理：不传时保留原配置；传入时替换所有提供商的 options；传入
{}
时清空。因此，修改某个提供商的 options 时，其他需要保留的配置也要一并提交。具体字段要求见前面的 OAuth 配置文档。
如果更新返回用户待授权错误，原配置会继续生效。应用按前一节的流程引导用户完成全部授权；开启会话绑定时，还需完成回调确认，然后重试更新。
请在沙箱运行状态下提交更新；如果沙箱已暂停，先恢复后再更新。已有网络配置会跨暂停与恢复保留。
工作负载身份、会话策略和 STS 重签域名在沙箱创建后保持固定。更换这些配置时，需使用新配置创建沙箱。
配置这些访问时，工作负载身份和 RAM 角色可以复用，每次任务的资源范围、OAuth 授权范围和访问目标仍需按实际需要设置。目标服务会收到真实凭据，因此凭证注入规则应指向可信服务，并确认对方不会在响应中回显或在日志中记录认证请求头。
令牌刷新与重新授权
接入完成后，OAuth 访问令牌仍有有效期。M2M 令牌由平台按有效期自动刷新；目标服务返回的 401/403 会原样传回，平台不会因这些响应立即刷新令牌或自动重放业务请求。
用户委托授权的访问令牌（Access Token）由 Agent Identity 缓存。令牌到期后，如果提供商返回过有效的刷新令牌（Refresh Token），Agent Identity 会用它换取新的访问令牌，用户无需为每次请求重新授权。若没有 Refresh Token，或它已过期、被撤销，访问令牌到期后就需要用户重新授权，详见
令牌的保存和刷新[19]
。
用户登录态和申请的授权范围由应用管理。需要重新授权或补充权限时，应用仍需引导用户确认，再按相应流程继续任务。
结语
对开发者来说，沙箱电子身份带来的变化很直接：Agent 可以继续通过熟悉的 SDK 和接口访问服务，真实凭据由平台在沙箱外管理，访问权限则根据任务需要和用户授权配置。开发者可以把更多精力放在 Agent 如何完成任务上。
随着 Agent 参与更多业务，身份和授权也将成为应用接入真实业务系统时需要持续解决的问题。我们希望以 Agent sandbox 极速版的沙箱电子身份为起点，让更多 Agent 在获得工具和服务访问能力的同时，每一次调用都有明确的身份，每一项操作都有相应的授权依据。
相关文档
[1]
工作
负载身份管理
https://help.aliyun.com/zh/agentidentity/workload-identity-management
[2] 资源与出站凭据权限
https://help.aliyun.com/zh/agentidentity/outbound/
[3] 接入指南
https://github.com/aliyun-fc/fc-docs/blob/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1/01.%E5%BC%80%E5%A7%8B%E4%BD%BF%E7%94%A8/03.%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8/01.%E9%80%9A%E8%BF%87%20SDK%20%E4%BD%BF%E7%94%A8%E4%BA%91%E6%B2%99%E7%AE%B1.md
[4] 凭证使用限制
https://github.com/aliyun-fc/fc-docs/blob/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1/04.%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E/06.%E7%BD%91%E7%BB%9C/03.%E5%87%AD%E8%AF%81%E6%B3%A8%E5%85%A5/07.%E5%87%AD%E8%AF%81%E4%BD%BF%E7%94%A8%E9%99%90%E5%88%B6.md
[5]
API Key 凭证提供商
https://help.aliyun.com/zh/agentidentity/api-key-credential-provider-management
[6] OpenAI 兼容接口
https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions
[7]
网络访问控制
https://github.com/aliyun-fc/fc-docs/blob/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1/04.%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E/06.%E7%BD%91%E7%BB%9C/02.%E5%87%BA%E7%BD%91%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6.md
[8] 托管凭证注入
https://github.com/aliyun-fc/fc-docs/blob/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1/04.%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E/06.%E7%BD%91%E7%BB%9C/03.%E5%87%AD%E8%AF%81%E6%B3%A8%E5%85%A5/04.%E6%89%98%E7%AE%A1%E5%87%AD%E8%AF%81%E6%B3%A8%E5%85%A5.md
[9] OSS Python SDK V1
https://help.aliyun.com/zh/oss/developer-reference/python-sdk-v1/
[10] 阿里云 STS 注入
https://github.com/aliyun-fc/fc-docs/blob/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1/04.%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E/06.%E7%BD%91%E7%BB%9C/03.%E5%87%AD%E8%AF%81%E6%B3%A8%E5%85%A5/03.%E9%98%BF%E9%87%8C%E4%BA%91%20STS%20%E6%B3%A8%E5%85%A5.md
[11] OAuth 凭证提供商
https://help.aliyun.com/zh/agentidentity/oauth-credential-provider-management
[12] M2M OAuth 注入
https://github.com/aliyun-fc/fc-docs/blob/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1/04.%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E/06.%E7%BD%91%E7%BB%9C/03.%E5%87%AD%E8%AF%81%E6%B3%A8%E5%85%A5/05.M2M%20OAuth%20%E6%B3%A8%E5%85%A5.md
[13] OAuth 用户委托授权
https://github.com/aliyun-fc/fc-docs/blob/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1/04.%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E/06.%E7%BD%91%E7%BB%9C/03.%E5%87%AD%E8%AF%81%E6%B3%A8%E5%85%A5/06.%E7%94%A8%E6%88%B7%E5%A7%94%E6%89%98%20OAuth%20%E6%B3%A8%E5%85%A5.md
[14] OAuth 凭证提供商
https://help.aliyun.com/zh/agentidentity/oauth-credential-provider-management
[15] 会话确认权限
https://help.aliyun.com/zh/ram/developer-reference/aliyunagentidentitydatacompleteauthaccess
[16] 获取 OAuth Access Token
https://help.aliyun.com/zh/agentidentity/obtain-oauth-access-token
[17] 入站身份提供商
https://help.aliyun.com/zh/agentidentity/identity-provider-management
[18] 更新网络配置
https://github.com/aliyun-fc/fc-docs/blob/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1/04.%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%9
8%8E/06.%E7%BD%91%E7%BB%9C/
04.%E6%9B%B4%E6%96%B0%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE.md
[19] 令牌的保存和刷新
https://help.aliyun.com/zh/agentidentity/obtain-oauth-access-token
[20] Agent sandbox 极速版用户文档
https://github.com/aliyun-fc/fc-docs/tree/main/docs/zh-CN/01.%E4%BA%91%E6%B2%99%E7%AE%B1
[21]
工作负载身份管理
https://help.aliyun.com/zh/agentidentity/workload-identity-management
[22]
Agent Identity 产品文档
https://help.aliyun.com/zh/agentidentity/
