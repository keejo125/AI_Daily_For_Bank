---
name: ai-daily-report
description: >
  生成每日 AI 智能研发早报。从微信公众号获取文章，按关键词过滤，
  智能分类（国际/国内/同业/其他）并生成摘要，渲染为响应式静态 HTML 页面。
  使用场景：当用户要求生成今日/昨日AI早报、获取公众号文章汇总、
  生成智能研发日报时触发。触发词：早报、日报、AI daily、每日汇总。
license: MIT
metadata:
  version: "2.0"
  category: productivity
---
# AI Daily Report Skill

生成每日 AI 智能研发早报。从微信公众号订阅源获取文章，按关键词过滤后由智能体智能分类并生成摘要，最终渲染为响应式静态 HTML 页面。

## 项目路径

`/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/`

---

## 工作流程（5 步骤）

### Step 1: 获取文章

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 fetch_articles.py [YYYY-MM-DD]
```

- 不传日期参数则默认获取**昨天**的文章
- 调用 `wechat-query-skill` 的 `/api/rss/export/{date}` 导出接口，一次请求获取当天所有文章
- 耗时 1-3 秒（旧版逐公众号翻页需 4-10 分钟）
- 导出接口从服务器 SQLite 读取，**不依赖微信登录态**
- 输出：
  - `daily/YYYY-MM-DD/sources/*.md` — 每篇文章的 Markdown 原文
  - `daily/YYYY-MM-DD/articles_raw.json` — 文章元数据汇总

**注意**：导出接口本身不依赖登录态，但数据库的更新仍依赖微信登录态（约 4 天过期）。如导出返回空数组，需检查服务器端登录状态。

---

### Step 2: 关键词过滤

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 filter_articles.py YYYY-MM-DD
```

- 读取 `config.json` 中的 `keywords.include` 列表进行过滤
- 默认关键词：`AI`、`大模型`、`智能体`、`skill`
- 同时支持 `keywords.exclude` 排除特定内容
- 匹配标题 + digest 进行判断（不区分大小写）
- 不匹配的文章会从 `sources/` 目录中**删除**
- 输出：`daily/YYYY-MM-DD/filtered_articles.json`

**注意**：

- 关键词可在 `config.json` 中随时修改，无需重启
- 纯标题关键词过滤可能遗漏（如 GPT-5.5 泄露、小米 MiMo 等标题不含关键词），后续分类步骤需人工补充

---

### Step 3: 智能分类（由智能体完成）

读取 `daily/YYYY-MM-DD/filtered_articles.json`，对每篇文章执行以下操作：

1. **读取原文**：根据 `source_file` 路径读取对应的 Markdown 文件，了解文章内容
2. **识别重复主题并合并**：
   - 如果发现多篇文章讲述同一事件/产品（如OpenAI手机的两篇报道），应合并为一篇
   - 合并策略：保留第一篇作为主文章，将其他文章的信息整合到摘要中
   - 在classification.json中添加 `source_items` 字段记录多来源信息：
     ```json
     "source_items": [
       {"name": "公众号1", "source_file": "sources/xxx1.md", "link": "url1"},
       {"name": "公众号2", "source_file": "sources/xxx2.md", "link": "url2"}
     ]
     ```
   - HTML渲染时会自动显示多个来源标签
3. **判断分类**：

| 分类           | 判断标准                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **国际** | 涉及海外公司（OpenAI、Anthropic、Google、Meta、Apple、Nvidia、Microsoft、xAI、Stability AI 等）或国际 AI 动态                        |
| **国内** | 涉及国内公司（阿里、腾讯、百度、字节、华为、智谱、商汤、深度求索、月之暗面、MiniMax、阶跃星辰、零一万物、面壁智能 等）或国内 AI 动态 |
| **同业** | 涉及银行、金融机构的 AI 应用（办公、研发以及运维领域）                                                                               |
| **其他** | 不属于以上三类的 AI 相关文章                                                                                                         |

**分类优先级规则**：如果文章内容同时涉及国际和国内，按**主要内容**所在区域分类。

**产品技术类文章处理**：
- OpenClaw、Gemini CLI 等产品工具类文章，虽然不属于大模型本身，但属于产品技术内容
- 应根据其主体归属分类（如 OpenClaw 是国际开源项目 → 国际；Gemini CLI 是 Google 产品 → 国际）
- **不应放入"其他"类别**，除非是纯商业资讯或广告

**商业/资讯类文章处理**：
- 纯商业资讯（如Meta收购Manus、年轻人投资AI基金）→ 归入"其他"
- 政策监管资讯（如普京谈AI监管）→ 归入"其他"
- 社会现象报道（如AI恐惧导致暗杀）→ 归入"其他"
- 活动广告/促销（如申报截止通知、Qoder优惠）→ **直接删除**，不纳入早报

4. **生成摘要**：为每篇文章生成 100-200字的中文摘要；不要使用原始 `digest`
5. **输出分类理由**：在完成分类后，向用户说明每篇文章的分类依据和打标理由

输出 `daily/YYYY-MM-DD/classification.json`：

```json
{
  "date": "YYYY-MM-DD",
  "generated_at": "2026-04-22T10:30:00+08:00",
  "classification": {
    "国际": [
      {
        "aid": "文章ID",
        "title": "文章标题",
        "source": "公众号名称",
        "link": "微信原文链接",
        "digest": "摘要（智能体生成或原始digest）",
        "source_file": "sources/xxx.md",
        "is_model_related": false,
        "model_tag_reason": "",
        "source_items": [  // 可选，多来源时使用
          {"name": "公众号1", "source_file": "sources/xxx1.md", "link": "url1"},
          {"name": "公众号2", "source_file": "sources/xxx2.md", "link": "url2"}
        ]
      }
    ],
    "国内": [...],
    "同业": [...],
    "其他": [...]
  },
  "stats": {"国际": 3, "国内": 5, "同业": 2, "其他": 4, "total": 14},
  "excluded": [
    {"reason": "排除原因说明", "examples": ["文章标题示例"]}
  ]
}
```

---

### Step 4: 生成 HTML

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 generate_html.py YYYY-MM-DD
```

- 读取 `classification.json` 获取分类和摘要数据
- 读取 `sources/*.md` 获取文章原文（提取多来源信息和关键词匹配）
- 基于 `template.html` 模板渲染响应式静态页面
- **多来源标签**：合并后的文章显示多个公众号来源标签，每个标签可点击跳转到 `viewer.html` 查看对应原文
- **大模型标签**：`generate_html.py` 内置 `detect_model_related()` 函数，会自动根据标题和摘要重新检测是否与大模型相关，并在HTML中显示🤖标签
- **无"阅读原文"按钮**：已用多来源标签替代
- 生成 `daily/YYYY-MM-DD/index.html`
- 更新 `daily-index.json` 和 `search-index.json` 索引文件

**关于 viewer.html**：

- 通过 URL 参数 `?file=daily/YYYY-MM-DD/sources/xxx.md` 访问
- 自动对中文文件路径做 `encodeURIComponent` 编码后 fetch
- 使用 marked.js 渲染 Markdown，自动提取标题和公众号来源

---

### Step 5: 验证与推送

检查以下产出是否完整：

| 检查项                                   | 预期结果               |
| ---------------------------------------- | ---------------------- |
| `daily/YYYY-MM-DD/index.html`          | 存在且大小 > 0         |
| `daily/YYYY-MM-DD/classification.json` | 存在，包含 4 个分类键  |
| `daily-index.json`                     | 已更新，包含新日期条目 |

验证通过后，通过 `wechat-access` 渠道推送到微信（userId: 1729837708）。

---

## 配置文件

`config.json` 位于项目根目录：

```json
{
  "server": {
    "base_url": "https://www.torandom.com/wechat-api"
  },
  "keywords": {
    "include": ["AI", "大模型", "智能体", "skill"],
    "exclude": []
  },
  "categories": ["国际", "国内", "同业", "其他"],
  "output": {
    "project_dir": "/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank"
  }
}
```

- `keywords.include`：过滤文章的关键词列表（可修改）
- `keywords.exclude`：排除文章的关键词列表
- `server.base_url`：`wechat-query-skill` API 地址（导出接口：`/api/rss/export/{date}`）

---

## 关键规则

1. **分类时务必阅读原文**：不要仅根据标题判断，必须读取 `source_file` 对应的 Markdown 原文来了解文章内容
2. **摘要精炼准确**：1-2 句话概括核心内容，避免冗长
3. **分类冲突时取主要方向**：同时涉及国际和国内的内容，按文章主要讨论的对象/区域分类
4. **同业类优先**：如果文章同时涉及同业和其他分类，**优先归为同业**
5. **每日早报以昨日为默认日期**：用户说“生成早报”时，默认使用昨天的日期
6. **中文引号替换**：`generate_html.py` 自动将中文引号（""''）替换为英文引号，避免 HTML 渲染异常
7. **source_file 模糊匹配**：`generate_html.py` 用 4 字符滑动窗口关键词提取 + 2 字符 fallback 解决中文文件名匹配问题
8. **输出分类和打标理由**：完成早报生成后，必须向用户说明：
   - 每篇文章的分类依据（为什么归入国际/国内/同业/其他）
   - 大模型标签的判断理由（为什么打标或不打标）
   - 被删除的广告类文章及原因

---

## 大模型标签判断标准

**应打标的内容**（满足任一即可）：
1. **模型发布**：新模型正式发布、版本更新（如 GPT-5.5 发布、DeepSeek V4 上线）
2. **模型测评**：性能对比、实测报告、IQ/跑分测试（如 GPT-5.5 Pro 视觉智商145）
3. **模型架构**：技术论文、架构创新、底层技术研究（如 ICLR 论文、Balanced Thinking、MathForge）
4. **模型产品化应用**：大模型作为核心能力的产品发布（如 HappyHorse 1.0在千问首发）

**不打标的内容**：
- AI 应用功能（如 Claude 图表功能、剪映 AI 助手）
- 行业资讯（如马斯克诉讼、公司融资）
- 公司动态（如员工退休、裁员、投资并购）
- 基础设施讨论（如 Token 工厂、算力芯片）
- 工具/产品集成（如 OpenClaw 接入 DeepSeek、Gemini CLI）
- 商业促销（如 Qoder 半价优惠）
- 行业应用（如银行业数据分类分级大模型）
- Agent框架/技能平台（如魔搭Agent群体智能框架，即使包含"蒸馏"等技术词）

**核心原则**：需区分“大模型本身”与“大模型应用场景”，只有文章主要讲述大模型技术/发布/评测时才打标。

### 自动检测机制

`generate_html.py` 内置 `detect_model_related()` 函数，会在生成HTML时自动重新检测每篇文章是否与大模型相关：

**确认规则**（满足任一即打标）：
1. 标题明确包含具体模型名称 + 发布/评测/架构关键词（如 "GPT-5.5发布"、"Mythos模型介绍"）
2. 标题包含"大模型"且非应用场景（排除"大模型上车"、"大模型走进医疗"等）
3. 内容包含模型架构术语（ICLR、ACL、注意力机制、MLA、蒸馏、微调等）+ 技术描述
4. 模型安全/漏洞研究（如 "ACL安全漏洞"、"主目录删除风险"）

**排除规则**（满足任一即不打标）：
1. 纯人物新闻（马斯克起诉、奥特曼被暗杀等），除非包含具体模型名称
2. 商业资讯（收购、融资、基金投资等）
3. Agent框架/技能平台（即使包含"蒸馏"、"进化"等技术词）
4. 行业应用报道（AI进入医疗、金融、教育等领域）
5. 产品功能更新（Claude图表、剪映AI助手等）

**注意**：智能体在Step 3分类时可以手动设置 `is_model_related` 和 `model_tag_reason` 字段，但HTML生成时会被自动检测函数覆盖。如需强制保留手动打标，需要修改 `generate_html.py` 的逻辑。

---

## 常见问题

### Q1: 为什么HTML中的大模型标签和我在classification.json中设置的不一致？

**A**: `generate_html.py` 会在生成HTML时调用 `detect_model_related()` 函数自动重新检测。如需保留手动打标，需要修改该函数的逻辑。

### Q2: 如何合并重复主题的文章？

**A**: 在Step 3分类时，如果发现多篇文章讲述同一事件（如OpenAI手机的两篇报道）：
1. 保留第一篇作为主文章
2. 将其他文章的摘要信息整合到主文章的digest中
3. 在classification.json中添加 `source_items` 字段记录所有来源
4. HTML会自动渲染多个来源标签

示例：
```json
{
  "title": "OpenAI自研手机来了！",
  "source_items": [
    {"name": "财联社AI daily", "source_file": "sources/xxx1.md", "link": "url1"},
    {"name": "智东西", "source_file": "sources/xxx2.md", "link": "url2"}
  ]
}
```

### Q3: 哪些文章应该归入"其他"类别？

**A**: 
- ✅ 应归入"其他"：纯商业资讯、政策监管、社会现象报道
- ❌ 不应归入"其他"：产品技术类文章（应根据主体归属国际/国内）
- 🗑️ 应直接删除：活动广告、促销信息

### Q4: 导出接口返回空数组怎么办？

**A**: 这通常意味着服务器端微信登录态过期（约4天有效期）。需要：
1. 检查服务器登录状态：`ssh root@115.29.206.55`
2. 重新执行微信登录流程
3. 或者使用降级方案直接查数据库（见下文）

### Q5: 如何验证生成的HTML是否正确？

**A**: 检查以下项目：
1. `daily/YYYY-MM-DD/index.html` 存在且大小 > 0
2. 打开HTML文件，确认四个分类板块都有内容
3. 检查大模型标签🤖是否正确显示
4. 检查多来源文章是否显示多个来源标签
5. 统计数量是否与classification.json一致

---

## 降级方案

如果导出接口不可用（如服务器重启、接口报错），可通过 SSH 直接查数据库：

```bash
ssh root@115.29.206.55 "sqlite3 /home/claw/wechat-query-skill/services/wechat-download-api/data/rss.db \"
SELECT a.aid, a.title, a.link, a.digest, a.content,
       a.publish_time, s.nickname
FROM articles a
JOIN subscriptions s ON a.fakeid = s.fakeid
WHERE a.publish_time >= strftime('%s','YYYY-MM-DD 00:00:00')
  AND a.publish_time < strftime('%s','YYYY-MM-DD 23:59:59')
ORDER BY a.publish_time DESC
\""
```

服务器回退方案：`git reset --hard eb0bfd9`（备份在 `/home/claw/backup_20260423/`）
