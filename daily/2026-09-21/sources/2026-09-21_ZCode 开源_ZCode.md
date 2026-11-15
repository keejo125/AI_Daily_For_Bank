---
link: https://mp.weixin.qq.com/s/QCHjEye57BUKUNInPKb4cA
source: ZCode
status: confirmed
category: 国内
is_model_related: false
digest: |
  开源编程工具 ZCode（zai-org）因产品安全问题完成整改并正式开源（github.com/zai-org/ZCode），将全部代码交社区监督，让产品开放透明。团队承诺相关代码数据无留存、从未用于模型训练，并邀请中国信息通信研究院与绿盟科技开展安全审计——确认阿里云 OSS 存储桶云端零数据、客户端已移除 Repo Wiki 功能并切断本地仓库快照上传链路。ZCode 表示将建立常态化安全漏洞机制，按问题严重程度给予反馈开发者相应回报。
---

# ZCode 开源

> 原文链接：https://mp.weixin.qq.com/s/QCHjEye57BUKUNInPKb4cA
> 来源：ZCode

针对社区反馈的 ZCode 产品安全问题，我们已经完成整改，并向所有用户道歉。
我们已将 ZCode 开源 (
https://github.com/zai-org/ZCode)
，把代码交给社区监督，让 ZCode 变得开放、透明。
非常感谢此前发现 ZCode 问题的社区开发者，接下来我们将建立常态化的产品安全漏洞机制，欢迎开发者伙伴持续检查和反馈问题，我们会根据问题严
重程度给予相应回报。
对于社区中提及的代码数据，我们承诺无留存，也从未将其用于模型训练。完成整改后，
我们
邀请中国信息通信研究院和绿盟科技开展安全审计，结果如下：
经中国信息通信研究院技术评测，确认 zcode-prod 阿里云OSS存储桶状态为云端零数据。ZCode v3.14.0 客户端已完成安全整改，已经移除 Repo Wiki 功能，已切断本地仓库快照生成与上传链路。
经绿盟科技审查，确认 zcode-prod (阿里云对象存储OSS) 内全部数据对象及存储桶本身已删除。ZCode v3.14.0 客户端已完成整改，Repo Wiki 入口及相应生成链路已移除，未发现可触发本地仓库快照或文件外发的功能路径。
再次向大家致歉，请大家持续监督。