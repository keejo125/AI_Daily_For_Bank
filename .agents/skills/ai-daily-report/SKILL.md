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

## ⚠️ 重要提醒

**本技能仅负责生成早报数据，不负责推送到 GitHub！**

- ✅ **ai-daily-report**: 生成早报（fetch → filter → classify → generate HTML）
- ✅ **push-daily-to-github**: 推送数据到 GitHub（git add → commit → push）

**工作流程**：先调用 `ai-daily-report` 生成早报，验证无误后，再调用 `push-daily-to-github` 进行推送。

---

## 项目路径

`/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/`

---

## 工作流程（6 步骤）

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

### Step 3: 智能分类（由Agent完成）

**核心原则**：分类和大模型标签判断完全由Agent智能完成，程序不做自动检测。

读取 `daily/YYYY-MM-DD/filtered_articles.json`，对每篇文章执行以下操作：

1. **读取原文**：根据 `source_file` 路径读取对应的 Markdown 文件，了解文章内容
2. **判断分类**：

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

3. **生成摘要**：为每篇文章生成 100-200字的中文摘要；不要使用原始 `digest`
4. **合并重复内容**：同一事件的多篇报道需要整合展示
   - 按各篇侧重点独立分类，整合后列出多个公众号名称
   - 在 `classification.json` 中添加 `sources` 字段（公众号名称列表）
   - 设置 `source` 字段为 "综合报道"
   - 保留 `merged_from` 字段记录原始 aid 列表
5. **标注大模型标签**：Agent需手动判断每篇文章是否应打标
   - 在 `classification.json` 中为每篇文章添加 `is_model_related` 字段（true/false）
   - **必须明确标注**，不能留空让程序自动检测

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
        "source": "公众号名称或综合报道",
        "link": "微信原文链接",
        "digest": "摘要（Agent生成）",
        "source_file": "sources/xxx.md",
        "is_model_related": true,  // ⭐ Agent必须标注：true或false
        "sources": ["公众号1", "公众号2"],  // 合并文章时添加
        "merged_from": ["aid1", "aid2"]     // 合并文章时添加
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

**关键字段说明**：
- `is_model_related`: **必须由Agent明确标注**（true/false），程序不再自动检测
- `sources`: 合并文章时的多来源公众号列表
- `merged_from`: 合并文章的原始aid列表

---

### Step 3.5: 分类和打标复核（重要！）

在完成初步分类后，**必须执行复核环节**，确认分类和打标无误：

#### 复核清单

**1. 分类复核**

检查以下常见错误：

- ❌ **OpenClaw/Gemini CLI等产品工具类文章**：应根据主体归属分类（国际开源项目→国际，Google产品→国际），不应放入"其他"
- ❌ **汽车行业应用文章**：如"汽车的OpenClaw时刻"，讲的是行业应用场景，非OpenClaw本身，应归为国内而非国际
- ❌ **中文访谈文章**：如"深度访谈|OpenClaw引爆Agent元年"，虽然讨论国际项目，但这是中文媒体访谈，聚焦企业应用场景，应归为国内
- ❌ **商业诉讼/资讯类**：如"马斯克大战奥尔特曼诉讼案"，属于商业资讯，应归为其他而非国际
- ❌ **综合资讯汇总**：如"极客早知道"，包含多个不相关话题，应归为其他
- ✅ **同业优先原则**：银行、金融机构的AI应用优先归为同业

**2. 大模型标签复核**

根据标签判断标准重新检查：

✅ **应打标的情况**（满足任一）：
- 模型发布：新模型正式发布、版本更新（如 MiniCPM-o 4.5 技术报告）
- 模型测评：性能对比、实测报告、IQ/跑分测试
- 模型架构：技术论文、架构创新、底层技术研究（如 ICLR 论文）

❌ **不应打标的情况**：
- AI 应用功能（如 QoderWork、剪映 AI 助手）
- 行业资讯（如马斯克诉讼、公司融资、网信部门查处）
- 公司动态（如 OpenAI 与微软分手、员工退休、裁员）
- 基础设施讨论（如 Token 工厂、算力芯片）
- 工具/产品集成（如 OpenClaw 更新、灵码 MCP 支持）
- 商业促销（如 Qoder 优惠）
- 行业应用（如南京银行、宁波银行的 AI 应用）

**核心原则**：区分"大模型本身"与"大模型应用场景"，只有文章主要讲述大模型技术/发布/评测时才打标。

**3. 合并内容复核**

- 检查是否有同一事件的多篇报道需要合并
- 合并后的文章应设置 `sources` 字段包含所有来源公众号
- 确保每个来源都有对应的 `source_file` 可点击跳转

#### 复核输出

复核完成后，向用户输出：

```
📋 分类和打标复核报告

【分类调整】
- 文章A：从国际调整为国内（原因：...）
- 文章B：从国际调整为其他（原因：商业资讯）
- 文章C&D：合并为一篇（原因：同一事件）

【打标确认】
- 应打标文章（X篇）：文章1、文章2...
- 不应打标文章（Y篇）：文章3、文章4...

【最终统计】
- 国际：X篇 | 国内：Y篇 | 同业：Z篇 | 其他：W篇
- 总计：N篇（原始M篇，合并后减少K篇）
```

**只有在复核确认无误后，才能进入 Step 4 生成 HTML。**

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
- **无"阅读原文"按钮**：已用多来源标签替代
- 生成 `daily/YYYY-MM-DD/index.html`
- 更新 `daily-index.json` 和 `search-index.json` 索引文件

**关于 viewer.html**：

- 通过 URL 参数 `?file=daily/YYYY-MM-DD/sources/xxx.md` 访问
- 自动对中文文件路径做 `encodeURIComponent` 编码后 fetch
- 使用 marked.js 渲染 Markdown，自动提取标题和公众号来源

---

### Step 5: 验证产出

检查以下产出是否完整：

| 检查项                                   | 预期结果               |
| ---------------------------------------- | ---------------------- |
| `daily/YYYY-MM-DD/index.html`          | 存在且大小 > 0         |
| `daily/YYYY-MM-DD/classification.json` | 存在，包含 4 个分类键  |
| `daily-index.json`                     | 已更新，包含新日期条目 |

**重要**：验证通过后，**不要在此技能中执行 git push**。

如需推送到 GitHub，请使用 **`push-daily-to-github`** 技能：
```bash
# 调用 push-daily-to-github 技能进行推送
# 该技能会正确处理 Git 提交流程并推送到正确的远程仓库
```

**为什么需要分开**：
- `ai-daily-report` 负责生成早报数据（fetch → filter → classify → generate HTML）
- `push-daily-to-github` 负责推送数据到 GitHub（git add → commit → push）
- 两个技能职责分离，避免推送错误

---

### Step 6: 微信推送（可选）

如需通过微信渠道推送，可使用 `wechat-access` 渠道发送到 userId: 1729837708。

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
8. **多来源整合规范**：
   - 同一事件的多篇报道需要整合展示
   - 合并后的文章 `source` 字段设为 "综合报道"
   - 添加 `sources` 字段（公众号名称列表）
   - 添加 `merged_from` 字段（原始 aid 列表）
   - HTML 中显示多个公众号标签，每个标签可点击跳转到对应原文
9. **分类和打标复核**：完成初步分类后，必须执行复核环节
   - 检查分类是否符合主体优先原则
   - 确认大模型标签判断准确
   - 识别并合并重复内容
   - **复核确认无误后，才能生成 HTML**
10. **输出分类和打标理由**：复核完成后，向用户说明：
   - 每篇文章的分类依据（为什么归入国际/国内/同业/其他）
   - 大模型标签的判断理由（为什么打标或不打标）
   - 被删除的广告类文章及原因
11. **⭐ Agent职责：分类和标签完全由Agent智能判断**
    - **程序不做自动检测**：`generate_html.py` 只读取 `classification.json` 中的 `is_model_related` 字段
    - **Agent必须明确标注**：每篇文章都必须设置 `is_model_related: true` 或 `false`
    - **不留空字段**：如果留空，程序虽然会fallback到自动检测，但容易误判
12. **商业资讯一律归入"其他"**
    - 财报数据、营收增长、利润变化
    - IPO融资、估值变化、投资并购
    - 诉讼纠纷、法律案件
    - 组织调整、部门成立/撤销
13. **招聘/活动类直接删除**
    - 招聘信息不保留在任何分类
    - 纯活动预告（无技术内容）删除
    - 会议报道如无具体技术分享，移至"其他"或删除

---

## 大模型标签判断标准（Agent判断依据）

**重要说明**：此标准供Agent在Step 3中手动判断使用，程序不做自动检测。

**应打标的内容**（满足任一即可）：
1. **模型发布**：新模型正式发布、版本更新（如 GPT-5.5 发布、DeepSeek V4 上线）
2. **模型测评**：性能对比、实测报告、IQ/跑分测试（如 GPT-5.5 Pro 视觉智商145）
3. **模型架构**：技术论文、架构创新、底层技术研究（如 ICLR 论文、Balanced Thinking、MathForge）

**不打标的内容**：
- AI 应用功能（如 Claude 图表功能、剪映 AI 助手）
- 行业资讯（如马斯克诉讼、公司融资）
- 公司动态（如员工退休、裁员、投资并购）
- 基础设施讨论（如 Token 工厂、算力芯片）
- 工具/产品集成（如 OpenClaw 接入 DeepSeek、Gemini CLI）
- 商业促销（如 Qoder 半价优惠）
- 行业应用（如银行业数据分类分级大模型）
- 活动报道（如开发者日、大会、峰会）
- 榜单排名（如《时代》十大AI公司）
- 招聘启事（如社招、岗位需求）

**核心原则**：需区分“大模型本身”与“大模型应用场景”，只有文章主要讲述大模型技术/发布/评测时才打标。

**常见误判案例**：
- ❌ "AMD开发者日聚焦AI Agent、RLHF、MoE" → 活动报道，不打标
- ❌ "阿里、字节入选《时代》十大AI公司" → 榜单资讯，不打标
- ❌ "兴业银行社招AI研发工程师" → 招聘信息，应删除
- ✅ "美团发布LongCat-2.0万亿参数模型" → 模型发布，打标
- ✅ "ACL 2026综述：大模型内生可解释性" → 技术论文，打标

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
