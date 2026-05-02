# 百炼 Token Plan 来了，Qoder 已同步支持

> 原文链接：https://mp.weixin.qq.com/s/DAefdulm5O3BenOzQa6tdA
> 公众号：Qoder

---

阿里云百炼推出了 Token Plan （团队版）。这是继 Coding Plan 之外的另一种订阅方案，主要面向团队和企业场景（也包括独立开发者和一人公司），按 Token 用量抵扣，不限调用频次。详细规则、价格档位和模型清单，可以去百炼官方了解。

与此同时，Qoder 也同步支持百炼 Token Plan。

IDE、CLI、JetBrains 插件三端均已支持，一次配置，三端可用。

Qoder 侧不消耗 Credits，费用全部走你自己的 Token Plan 额度。

三步配置

以 Qoder IDE 为例：

下载或更新 Qoder IDE 到最新版，进入设置 > 模型。

点击添加自定义模型，提供商选「阿里云百炼 - 国内」，类型下拉选

Token Plan

，勾选要用的模型。

粘贴以

sk-sp-

开头的专属 API Key（注意和 Coding Plan 的普通 Key 前缀不同，容易填错），系统自动校验连接。

完成后，新加的模型会出现在模型选择器的 Custom（自定义）分组下，和内置模型一样使用。

Qoder CLI 和 JetBrains 插件的配置方式一样。

CLI 里输入

/model

，在 Custom 下选择提供商和 Token Plan 类型，粘贴 API Key 即可。

JetBrains 插件在 Settings > Qoder > Models 里点

Add Model

，同样选提供商、类型选 Token plan、勾选模型、填 API Key。

当前 Qoder 个人版（Pro Trial、Pro、Pro+、Ultra）支持百炼 Token Plan 。新用户注册即送 14 天 Pro Trial + 全球顶尖编程模型 300 Credits。

关注我，掌握Qoder最新动态