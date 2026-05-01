# AI-Daily for Bank 🤖📰

> 智能研发早报 — 每日自动从微信公众号获取 AI 相关文章，关键词过滤，智能分类（国际/国内/同业/其他），生成响应式静态 HTML 早报页面。

---

## 📁 项目结构

```
AI-Daily-for-bank/
├── config.json              # 项目配置（API 地址、关键词、分类）
├── index.html               # 首页（历史归档 + 全文搜索）
├── template.html            # 早报详情页模板
├── viewer.html              # Markdown 原文查看器
├── daily-index.json         # 日报索引（日期、统计、摘要）
├── search-index.json        # 全文搜索索引
├── scripts/
│   ├── fetch_articles.py    # Step 1: 获取文章
│   ├── filter_articles.py   # Step 2: 关键词过滤
│   └── generate_html.py     # Step 4: 生成 HTML
└── daily/
    └── YYYY-MM-DD/          # 每日数据目录
        ├── articles_raw.json      # 原始文章元数据
        ├── filtered_articles.json # 过滤后的文章
        ├── classification.json    # 智能分类结果
        ├── index.html             # 当日早报页面
        └── sources/               # 文章 Markdown 原文
            └── *.md
```

---

## 🔄 工作流程

```
获取 → 过滤 → 分类(Agent) → 生成 → 验证
 │       │       │            │       │
 ▼       ▼       ▼            ▼       ▼
Step1   Step2   Step3        Step4   Step5
脚本    脚本    Agent智能判断  脚本    人工
```

| 步骤 | 执行者 | 脚本/操作 | 输入 | 输出 |
|:----:|:------:|:---------|:-----|:-----|
| **1. 获取** | 脚本 | `fetch_articles.py` | `/api/rss/export/{date}` 导出接口 | `sources/*.md` + `articles_raw.json` |
| **2. 过滤** | 脚本 | `filter_articles.py` | `articles_raw.json` + `config.json` 关键词 | `filtered_articles.json`（不匹配的 .md 会被删除） |
| **3. 分类** | **Agent** | **智能体完成** | `filtered_articles.json` + `sources/*.md` | `classification.json`（含is_model_related字段） |
| **4. 生成** | 脚本 | `generate_html.py` | `classification.json` + `template.html` | `daily/YYYY-MM-DD/index.html` + 更新索引 |
| **5. 验证** | 人工 | 检查产出 | 生成的文件 | 确认完整 |

**核心原则**：分类和大模型标签判断完全由Agent智能完成，程序不做自动检测。

---

## 🚀 快速使用

### 前置条件

- Python 3.x
- `requests` 库：`pip3 install requests`
- `wechat-query-skill` 导出接口可访问：`https://www.torandom.com/wechat-api/api/health` 返回 healthy

### 一键运行

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts

# Step 1: 获取昨日文章（不传日期默认昨天，1-3秒完成）
python3 fetch_articles.py

# Step 2: 关键词过滤
python3 filter_articles.py 2026-04-22

# Step 3: 智能分类（由Agent完成）
# Agent读取 filtered_articles.json 和 sources/*.md
# Agent判断每篇文章的分类（国际/国内/同业/其他）
# Agent生成摘要并标注 is_model_related (true/false)
# Agent输出 classification.json

# Step 4: 生成 HTML（直接读取Agent输出的classification.json）
python3 generate_html.py 2026-04-22
```

### 各脚本独立用法

```bash
# 获取指定日期的文章（调用 /api/rss/export/{date} 一键导出）
python3 fetch_articles.py 2026-04-22

# 过滤指定日期的文章（日期参数必填）
python3 filter_articles.py 2026-04-22

# 生成指定日期的 HTML（日期参数必填）
python3 generate_html.py 2026-04-22
```

---

## ⚙️ 配置说明

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

| 字段 | 说明 |
|------|------|
| `server.base_url` | wechat-query-skill API 地址（通过 Nginx 反代，导出接口：`/api/rss/export/{date}`） |
| `keywords.include` | 🔍 保留文章的关键词列表（匹配标题 + digest，不区分大小写） |
| `keywords.exclude` | 🚫 排除文章的关键词列表 |
| `categories` | 分类类别，固定为国际/国内/同业/其他 |
| `output.project_dir` | 项目输出根目录 |

### 修改关键词

直接编辑 `config.json` 中的 `keywords.include` / `keywords.exclude` 即可，无需重启任何服务。

---

## 🖥️ 页面说明

### `index.html` — 首页

- 展示最新一期早报卡片 + 历史归档列表
- 🔍 内置全文搜索：搜索标题、摘要、来源，实时高亮匹配
- 加载 `daily-index.json` 渲染列表，加载 `search-index.json` 实现搜索

### `template.html` — 早报详情页模板

- 占位符：`{{DATE}}`、`{{STATS}}`、`{{ARTICLES_JSON}}`、`{{SECTION_INTL}}` 等
- 包含 No-JS 降级内容 + JS 动态渲染两种模式
- 按 4 个分类展示文章卡片，带摘要、来源标签、原文链接

### `viewer.html` — Markdown 原文查看器

- 通过 URL 参数 `?file=daily/YYYY-MM-DD/sources/xxx.md` 加载文章原文
- 使用 marked.js 渲染 Markdown，自动提取标题和公众号来源

### 🎨 页面特性

- ✅ 响应式布局（手机 / 平板 / 桌面）
- ✅ 亮色调为主，暗色模式自动适配（`prefers-color-scheme: dark`）
- ✅ 纯静态，无需后端服务
- ✅ 大模型相关文章自动标记 `【大模型】` 标签（仅针对模型发布、测评、架构内容）
- ✅ 文章卡片显示发布时间（hh:mm格式），位于标题下方
- ✅ 排序规则：每个分类内，大模型标签文章优先展示，同组按时间升序

---

## 📊 数据文件说明

| 文件 | 位置 | 说明 |
|------|------|------|
| `articles_raw.json` | `daily/YYYY-MM-DD/` | 获取阶段产出的原始文章元数据（aid、title、source、link、digest、source_file） |
| `filtered_articles.json` | `daily/YYYY-MM-DD/` | 关键词过滤后的文章列表，含过滤统计（total_raw / total_filtered / removed） |
| `classification.json` | `daily/YYYY-MM-DD/` | **Agent智能分类结果**，按 国际/国内/同业/其他 分组，含摘要、统计和**is_model_related字段**（必须由Agent明确标注true/false） |
| `daily-index.json` | 项目根目录 | 所有日期的索引，含 weekday、stats、summary，按日期降序 |
| `search-index.json` | 项目根目录 | 全文搜索索引，所有文章的标题/摘要/来源/分类，按日期降序 |

---

## 📋 输出分类和打标理由

完成早报生成后，必须向用户说明：

1. **每篇文章的分类依据**：为什么归入国际/国内/同业/其他
2. **大模型标签的判断理由**：为什么打标或不打标
3. **被删除的广告类文章及原因**

示例输出格式：
```
✅ 有大模型标签的（4篇）- 模型发布/测评/架构
1. GPT-5.5 Pro 视觉智商145 - 模型测评 ✅
2. 医疗视频理解大模型开源 - 模型发布 ✅
...

❌ 无大模型标签的（15篇）- 应用/产品/资讯
- Claude 图表功能、Gemini CLI - 产品功能
- OpenClaw 相关 - 工具集成
...
```

---

## 🤖 智能体技能

本项目是一个 **Qoder 智能体技能**，技能定义位于 `.agents/skills/ai-daily-report/SKILL.md`。

### 触发方式

对智能体说 **"生成今日AI早报"** 即可触发完整流程。

触发词：`早报`、`日报`、`AI daily`、`每日汇总`

### 分类规则

| 分类 | 判断标准 |
|------|----------|
| 🌍 **国际** | 海外公司（OpenAI、Anthropic、Google、Meta、Apple、Nvidia、Microsoft、xAI 等）或国际 AI 动态 |
| 🇨🇳 **国内** | 国内公司（阿里、腾讯、百度、字节、华为、智谱、DeepSeek、月之暗面、MiniMax 等）或国内 AI 动态 |
| 🏦 **同业** | 银行/金融机构 AI 应用（智能客服、风控、信贷、理财、保险、证券等） |
| 📌 **其他** | 不属于以上三类的 AI 相关文章 |

> **优先级**：同业 > 其他分类；国际/国内冲突时按主要内容方向归类。

**产品技术类文章处理**：
- OpenClaw、Gemini CLI 等产品工具类文章，虽然不属于大模型本身，但属于产品技术内容
- 应根据其主体归属分类（如 OpenClaw 是国际开源项目 → 国际；Gemini CLI 是 Google 产品 → 国际）
- **不应放入“其他”类别**，除非是纯商业资讯或广告

**商业资讯一律归入"其他"**：
- 财报数据、营收增长、利润变化
- IPO融资、估值变化、投资并购
- 诉讼纠纷、法律案件
- 组织调整、部门成立/撤销

**招聘/活动类直接删除**：
- 招聘信息不保留在任何分类
- 纯活动预告（无技术内容）删除
- 会议报道如无具体技术分享，移至"其他"或删除

### 大模型标签判断标准（Agent判断依据）

**重要说明**：此标准供Agent在Step 3中手动判断使用，程序不做自动检测。Agent必须在classification.json中明确标注`is_model_related: true`或`false`。

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

> **核心原则**：需区分“大模型本身”与“大模型应用场景”，只有文章主要讲述大模型技术/发布/评测时才打标。

**常见误判案例**：
- ❌ "AMD开发者日聚焦AI Agent、RLHF、MoE" → 活动报道，不打标
- ❌ "阿里、字节入选《时代》十大AI公司" → 榜单资讯，不打标
- ❌ "兴业银行社招AI研发工程师" → 招聘信息，应删除
- ✅ "美团发布LongCat-2.0万亿参数模型" → 模型发布，打标
- ✅ "ACL 2026综述：大模型内生可解释性" → 技术论文，打标

---

## 📝 更新日志

### 2026-04-26

- 🛠️ **新增辅助脚本** `create_classification.py`：
  - 基于 `filtered_articles.json` 自动生成 `classification.json` 模板
  - 自动填充 aid, title, source, link, source_file 字段
  - 根据关键词预分类（国际/国内/同业/其他）
  - 自动处理中文引号（替换为方括号）
  - 保留空的 digest 字段供智能体填写摘要
  - **使用方法**：`python3 create_classification.py YYYY-MM-DD`
- 🔧 **增强容错性**：`generate_html.py` 读取 classification.json 时自动标准化中文引号
  - 使用 `normalize_chinese_quotes()` 函数统一处理
  - 添加更详细的错误提示信息
- 🎯 **优化大模型标签判断规则**：`generate_html.py` 中的 `detect_model_related()` 函数全面重构
  - **新标准**：仅针对模型发布、测评、架构的内容添加标签
    - ✅ 模型发布：DeepSeek V4、GPT-5.5 等新模型正式发布
    - ✅ 模型测评：性能对比、实测报告、benchmark 评测
    - ✅ 模型架构：技术论文、底层技术研究（LLM DNA、注意力机制等）
  - **明确排除**：
    - ❌ AI应用功能（如 Chronicle 屏幕记忆）
    - ❌ 行业资讯（如量化公司创始人背景）
    - ❌ 基础设施讨论（如 Token 工厂、算力芯片）
    - ❌ 公司动态（如 OpenAI 裁员、投资并购、商业竞争）
  - **实现方式**：通过关键词精准匹配 + 排除规则，避免误判
- 🔧 **修正分类错误案例**：
  - 黄仁勋访谈从"国内"移至"国际"（涉及英伟达、Token工厂等国际话题）
  - 删除重复的广告文章（量子位AIGC评选申报通知）

### 2026-04-25

- ✨ **新增时间显示功能**：文章卡片现在显示发布时间（hh:mm格式）
  - 时间位于标题下方、摘要上方
  - 数据来源：`articles_raw.json` 中的 `publish_time` 字段（Unix 时间戳）
  - JavaScript 和 Fallback 两种模式均支持
  - 样式优化：中等粗细、次要文本颜色，视觉柔和不突兀
- 🔧 **优化卡片布局**：调整元素顺序为 标题 → 时间 → 来源标签 → 摘要

---

## ⚠️ 注意事项

1. **登录态过期**：`wechat-query-skill` 的微信登录态约 **4 天**过期，如导出接口返回空数组，需检查并重新登录
2. **API 地址**：`server.base_url` 通过 Nginx 反向代理访问，确保反代服务正常运行
3. **导出接口**：`fetch_articles.py` v2 使用 `/api/rss/export/{date}` 一键导出，替代旧的逐公众号翻页流程，耗时从 4-10 分钟降至 1-3 秒
4. **⭐ Agent职责**：分类和大模型标签判断完全由Agent智能完成
   - Agent必须读取 `source_file` 对应的 Markdown 原文来了解文章内容
   - Agent必须在 `classification.json` 中为每篇文章明确标注 `is_model_related: true` 或 `false`
   - 程序不做自动检测，只读取Agent输出的JSON
5. **默认日期为昨天**：用户说“生成早报”时，默认使用昨天的日期
