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
获取 → 过滤 → 分类 → 生成 → 验证
 │       │       │       │       │
 ▼       ▼       ▼       ▼       ▼
Step1   Step2   Step3   Step4   Step5
脚本    脚本    智能体   脚本    人工
```

| 步骤 | 执行者 | 脚本/操作 | 输入 | 输出 |
|:----:|:------:|:---------|:-----|:-----|
| **1. 获取** | 脚本 | `fetch_articles.py` | `/api/rss/export/{date}` 导出接口 | `sources/*.md` + `articles_raw.json` |
| **2. 过滤** | 脚本 | `filter_articles.py` | `articles_raw.json` + `config.json` 关键词 | `filtered_articles.json`（不匹配的 .md 会被删除） |
| **3. 分类** | 智能体 | 人工阅读原文 → 判断分类 + 生成摘要 | `filtered_articles.json` + `sources/*.md` | `classification.json` |
| **4. 生成** | 脚本 | `generate_html.py` | `classification.json` + `template.html` | `daily/YYYY-MM-DD/index.html` + 更新索引 |
| **5. 验证** | 人工 | 检查产出 | 生成的文件 | 确认完整 |

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

# Step 3: 智能分类（由智能体完成，生成 classification.json）

# Step 4: 生成 HTML
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
- ✅ 大模型相关文章自动标记 `大模型` 标签

---

## 📊 数据文件说明

| 文件 | 位置 | 说明 |
|------|------|------|
| `articles_raw.json` | `daily/YYYY-MM-DD/` | 获取阶段产出的原始文章元数据（aid、title、source、link、digest、source_file） |
| `filtered_articles.json` | `daily/YYYY-MM-DD/` | 关键词过滤后的文章列表，含过滤统计（total_raw / total_filtered / removed） |
| `classification.json` | `daily/YYYY-MM-DD/` | 智能分类结果，按 国际/国内/同业/其他 分组，含摘要和统计 |
| `daily-index.json` | 项目根目录 | 所有日期的索引，含 weekday、stats、summary，按日期降序 |
| `search-index.json` | 项目根目录 | 全文搜索索引，所有文章的标题/摘要/来源/分类，按日期降序 |

---

## 🤖 智能体技能

本项目是一个 **Qoder 智能体技能**，技能定义位于 `.agents/skills/ai-daily-report/SKILL.md`。

### 触发方式

对智能体说 **"生成今日AI早报"** 即可触发完整流程。

触发词：`早报`、`日报`、`AI daily`、`每日汇总`

### 分类规则

| 分类 | 判断标准 |
|------|---------|
| 🌍 **国际** | 海外公司（OpenAI、Anthropic、Google、Meta、Apple、Nvidia、Microsoft、xAI 等）或国际 AI 动态 |
| 🇨🇳 **国内** | 国内公司（阿里、腾讯、百度、字节、华为、智谱、DeepSeek、月之暗面、MiniMax 等）或国内 AI 动态 |
| 🏦 **同业** | 银行/金融机构 AI 应用（智能客服、风控、信贷、理财、保险、证券等） |
| 📌 **其他** | 不属于以上三类的 AI 相关文章 |

> **优先级**：同业 > 其他分类；国际/国内冲突时按主要内容方向归类。

---

## ⚠️ 注意事项

1. **登录态过期**：`wechat-query-skill` 的微信登录态约 **4 天**过期，如导出接口返回空数组，需检查并重新登录
2. **API 地址**：`server.base_url` 通过 Nginx 反向代理访问，确保反代服务正常运行
3. **导出接口**：`fetch_articles.py` v2 使用 `/api/rss/export/{date}` 一键导出，替代旧的逐公众号翻页流程，耗时从 4-10 分钟降至 1-3 秒
3. **分类必须阅读原文**：不要仅凭标题分类，务必读取 `source_file` 对应的 Markdown 原文
4. **默认日期为昨天**：用户说"生成早报"时，默认使用昨天的日期
