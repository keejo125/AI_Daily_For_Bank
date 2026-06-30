---
publish_time: 1782712800
---

# Spring 近期新闻：Boot、Security、Integration、Modulith 发布增量版本及 Spring AI 2.0 正式发布

> 原文链接：https://mp.weixin.qq.com/s/i0usyFj_rNc1X8KlK-8wDw
> 公众号：InfoQ

在 2026 年 6 月 8 日这一周，Spring 生态系统呈现出一片繁忙的景象，其中包括发布以下组件的增量版本：Spring Boot、Spring Security、Spring Session、Spring Integration、Spring Modulith、Spring AMQP 和 Spring Vault，以及 Spring AI 2.0 和 Spring Data 2026.0.0 的正式版本。

Spring Boot

Spring Boot4.1.0 发布，带来 Bug 修复、文档改进、依赖项升级以及以下新特性：支持 Spring gRPC；在

InvalidConfigurationPropertyValueException

类中新增了一个公共构造函数，它可以接受一个字符串用于描述异常原因；降低多次调用

WritableJson

接口中定义的 toByteArray() 方法时的内存消耗。要了解有关该版本的更多详情，请参阅 发布说明 及这篇 InfoQ 新闻报道。

Spring Data

Spring Data 2026.0.0 版本 发布，带来了以下新特性：兼容 Kotlin 2.3.20 和 Vavr 0.11.0；新增带注解的 Redis 发布 / 订阅 消息监听器；类型安全的属性路径。要了解有关该版本的更多详细信息，请参阅其 维基页面。

Spring Security

Spring Security 7.1.0 发布，带来 Bug 修复、依赖项升级以及一些新特性，例如：新增

InetAddressMatcher

功能接口，可以作为 lambda 表达式或方法引用的赋值目标；在

AllRequiredFactorsAuthorizationManager

类中新增 anyOf() 方法，用于返回

AuthorizationManager

接口的实例，从而向满足多种身份验证因素组合中任意一种的用户授予访问权限。要了解有关该版本的更多详细信息，请参阅 发布说明 和 新功能介绍页面。

Spring Session

Spring Session 4.1.0 发布，带来 Bug 修复以及以下值得注意的依赖项升级：Spring Boot 4.1.0、Spring Security 7.1.0、Spring Framework 7.0.8、Spring Data 2025.1.6、Reactor 2025.0.6、Jackson 3.1.4 以及 Testcontainers 2.0.5。要了解有关该版本的更多详细信息，请参阅 发布说明。

Spring Integration

Spring Integration 7.1.0 版本发布，带来 Bug 修复、文档改进、依赖项升级以及以下新特性：在 Spring Framework 注解

@CrossOrigin

中禁用

allowCredentials

元素，转而使用

originPatterns

元素，以便与 Spring MVC 保持一致；改进

ExpressionEvaluatingMessageProcessor

类的构造函数，移除了异常处理逻辑，转而使用 Spring Framework 的

Assert

类。要了解有关该版本的更多详细信息，请参阅 发布说明 和 新功能介绍页面。

Spring HATEOAS

Spring HATEOAS 3.1.0 发布，带来 Bug 修复、依赖项升级以及一些新特性，包括：改进

StringLinkRelation

类的缓存机制，确保缓存条目不会超过 256 个；修改

TypeConstrainedJacksonJsonHttpMessageConverter

类中定义的

canWrite()

方法，使其与 Spring Framework

AbstractSmartHttpMessageConverter

类中定义的同名方法保持一致。

该版本还修复了两个 CVE：

CVE-2026-41006：该漏洞会绕过 Jackson 的访问控制注解，导致安全敏感属性被泄露。

CVE-2026-41007：因为前面提到的

StringLinkRelation

类的静态缓存无边界问题，该漏洞使得攻击者能够提供自定义的恶意超媒体内容。

要了解有关该版本的更多详细信息，请参阅 发布说明。

Spring Modulith

Spring Modulith 2.1.0 发布，带来 Bug 修复、依赖项升级以及一些新特性，包括：新增一组类（如

NamastackOutboxEventRecorder

），利用 Namastack 支持事件发送引擎；新增

JobRunrEventExternalizer

类，利用 JobRunr 支持事件外部化；新增

@ModuleSlicing

注解，与 Spring Boot 的切片测试注解结合使用，可以实现应用程序模块的切片。要了解有关该版本的更多详细信息，请参阅 发布说明。

Spring AI

Spring AI 2.0.0 版本 发布，带来 Bug 修复、文档改进、依赖项升级以及一些新特性，包括：Google GenAI 模型的更新，这些更新定义在

GoogleGenAiChatModel.ChatModel

枚举类中，其中包括废弃

GEMINI_2_0_FLASH

、

GEMINI_2_0_FLASH_LIGHT

和

GEMINI_3_PRO_PREVIEW

枚举，转而采用新的

GEMINI_3_1_PRO_PREVIEW

枚举；此外，通过替换抽象类 Jackson Databind

JsonNode

中已经弃用的方法，改进

org.springframework.ai.image.observation

包中的空值安全机制。要了解有关该版本的更多详细信息，请参阅 发布说明。

Spring AMQP

Spring AMQP 4.1.0 发布，带来 Bug 修复、依赖项升级以及以下新特性：兼容 RabbitMQ 4.3.0 ；从所有 Jackson 消息转换器中移除通配符，默认采用“不信任任何人”原则；新增

spring-amqp-client

模块，支持与通用 AMQP 1.0 协议进行交互。要了解有关该版本的更多详情，请参阅 发布说明 及 新功能介绍页面。

Spring for Apache Kafka

Spring for Apache Kafka 4.1.0 版本 发布，带来了 Bug 修复、文档改进、依赖项升级以及一项新特性：调整

FailedRecordProcessor

类中定义的方法

setBackOffFunction()

，使其能够批量处理消息。

该版本还修复了三个 CVE：

CVE-2026-41726 ：由于消费者堆大小无限制，导致垃圾回收（GC）剧烈波动并引发

OutOfMemoryError

异常，使攻击者能够发送恶意的 selector 头。

CVE-2026-41727 ：该漏洞允许攻击者发送包含恶意

retry_topic-attempts

头的记录，“提供超出范围的尝试次数，使重试主题路由器错误地识别消息在重试序列中的位置”。这可能导致任意时长的暂停，使监听器的停滞时间远远超出预期的重试窗口。

CVE-2026-41731 漏洞允许攻击者针对受信任的包（隐式信任所有子包）向

JsonKafkaHeaderMapper

和已弃用的

DefaultKafkaHeaderMapper

类实例提供恶意的消息头。利用前缀检查机制，可以诱使消费者反序列化任意 JDK 类型。

要了解有关该版本的更多详细信息，请参阅 发布说明。

Spring LDAP

Spring LDAP 4.1.0 版本 发布，带来多项依赖项升级，并新增了一项功能：将

toEntry()

、

toObject()

、

toList()

和

toStream()

方法标记为弃用，转而推荐使用已经添加到

LdapClient

接口中的新方法

map()

、

single()

、

optional()

、

list()

和

stream()

。

该版本还修复了 CVE-2026-41720 漏洞。该漏洞允许攻击者仅提供有效的用户名，即可通过输入空密码或 null 密码获得授权，这源于

DirContextAuthenticationStrategy

接口的实现未能拒绝此类密码。

要了解有关该版本的更多详细信息，请参阅 发布说明 及 更新日志页面。

Spring Vault

Spring Vault 4.1.0 发布，带来 Bug 修复、文档改进、依赖项升级以及一些新特性，包括：新增接口

VaultClient

和

ReactiveVaultClient

，目的是在配置了

VaultEndpoint

类的实例时，提供一个“中间抽象层，强制以相对路径处理为核心，防止意外地使用绝对路径”；新增

ManagedSecret

类，用于简化托管密钥的使用。要了解有关该版本的更多详细信息，请参阅 发布说明 和这个 维基页面。

Spring gRPC

Spring gRPC 1.1.0 版本 发布，带来 Bug 修复以及以下值得注意的变更：支持在应用程序属性文件中通过名称配置进程内通道；为 gRPC 服务新增了基于注解的异常处理。要了解有关该版本的更多详细信息，请参阅 发布说明。

原文链接：

https://www.infoq.com/news/2026/06/spring-news-roundup-jun08-2026/

声明：本文由 InfoQ 翻译，未经许可禁止转载。

点击底部

阅读原文

访问 InfoQ 官网，获取更多精彩内容！

今日好文推荐

GPT-5.6首发，比Fable 5便宜一半！深度评估者“开麦”吐槽：能力测试中疯狂作弊

AI 设计9个月就能媲美Blackwell？OpenAI “辣芯”绕开英伟达正面战场，但老黄的GPU大盘不稳了

AI可以用任何手段、写任何东西，但你得是个“中年老登”

拿下OpenAI Offer后，她复盘了57场面试：Transformer要会手写，LeetCode还得刷