# 对话窗口太小、爬楼查看历史对话？Qoder支持一键切换Markdown编写Prompt

> 原文链接：https://mp.weixin.qq.com/s/kU059TaRUYHUE5iwDGr9rA
> 公众号：Qoder

---

最近，Qoder JetBrains 插件 0.16.1 率先支持了一键切换Markdown编写Prompt。

使用独立的qoder.amd文档来编写prompt可以：

提升prompt编辑体验

：通过专用AI Markdown文件提供更大编辑窗口，直接在文件中编写、修改长提示词，避免在对话框中受限于空间，提升输入效率。

增强编辑与转换能力

：支持在文件内直接调用inline chat进行内容补全、格式转换（如Markdown转JSON/XML）、代码片段引用等操作，使编辑器具备更强的原生交互能力。

简化上下文引入方式

：支持拖拽文件或代码片段直接嵌入AI Markdown文档，替代原有复杂的“add files”或“@file”操作，降低上下文关联门槛。

实现交互历史可视化

：AI Markdown文件可以记录用户与AI的完整对话过程，每次新增需求时添加一个分页符(---)，然后以多页方式追加，形成可追溯的演进记录，无需翻查之前的AI需求记录。

方便版本管理与扩展

：AI Markdown文件(New->Qoder Files -> AI Markdown)可纳入Git版本控制，便于团队协作与历史回溯；未来可扩展高亮约束、专家模式、搜索历史等功能，作为AI任务的统一承载载体。

下面是一个演示视频：

关注我，掌握Qoder最新动态