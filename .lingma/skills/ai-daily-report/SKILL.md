---
name: ai-daily-report
description: >
  生成每日 AI 智能研发早报。从微信公众号获取文章，按关键词过滤，
  智能分类（国际/国内/同业/其他）并生成摘要，渲染为响应式静态 HTML 页面。
  使用场景：当用户要求生成今日/昨日AI早报、获取公众号文章汇总、
  生成智能研发日报时触发。触发词：早报、日报、AI daily、每日汇总。
license: MIT
metadata:
  version: "1.0"
  category: productivity
---

# AI Daily Report Skill

生成每日 AI 智能研发早报。从微信公众号订阅源获取文章，按关键词过滤后由智能体智能分类并生成摘要，最终渲染为响应式静态 HTML 页面。

## 项目路径

`/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/`

---

## 工作流程（5 步骤）

### Step 1: 获取文章

**推荐（优化版）**：
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 fetch_articles_fast.py [YYYY-MM-DD]
```

**原始版本**：
```bash
python3 fetch_articles.py [YYYY-MM-DD]
```

- 不传日期参数则默认获取**昨天**的文章
- 从 `wechat-query-skill` REST API 获取所有订阅公众号的文章列表
- 自动翻页获取每公众号的全部文章，按日期过滤
- **优化版特性**：
  - PAGE_SIZE=50（原始为10），减少翻页次数5倍
  - 降低等待时间，总耗时从5-10分钟降至约1分钟
  - 可选是否获取全文（默认不获取，大幅提升速度）
- 输出：
  - `daily/YYYY-MM-DD/sources/*.md` — 每篇文章的 Markdown 原文
  - `daily/YYYY-MM-DD/articles_raw.json` — 文章元数据汇总

**注意**：`wechat-query-skill` 登录态约 4 天过期，如 fetch 失败需检查登录状态。

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

**注意**：关键词可在 `config.json` 中随时修改，无需重启。

---

### Step 3: 智能分类（由智能体完成）

读取 `daily/YYYY-MM-DD/filtered_articles.json`，对每篇文章执行以下操作：

1. **读取原文**：根据 `source_file` 路径读取对应的 Markdown 文件，了解文章内容
   - **注意**：如果 `sources/` 目录为空（原文未保存），则跳过此步，直接使用 `filtered_articles.json` 中的 `digest`
2. **判断分类**：

| 分类 | 判断标准 |
|------|---------|
| **国际** | 涉及海外公司（OpenAI、Anthropic、Google、Meta、Apple、Nvidia、Microsoft、xAI、Stability AI 等）或国际 AI 动态 |
| **国内** | 涉及国内公司（阿里、腾讯、百度、字节、华为、智谱、商汤、深度求索、月之暗面、MiniMax、阶跃星辰、零一万物、面壁智能 等）或国内 AI 动态 |
| **同业** | 涉及银行、金融机构的 AI 应用（智能客服、风控、信贷、理财、网点、保险、证券 等） |
| **其他** | 不属于以上三类的 AI 相关文章 |

3. **生成摘要**：
   - **优先使用原始 `digest`**：从 `filtered_articles.json` 中获取文章的 `digest` 字段
   - **如果 `digest` 为空**：使用文章标题作为摘要
   - **如果 `digest` 过长（>200字符）**：截取前200字符并添加省略号
   - **理想情况**：如果有原文，可由智能体生成1-2句精炼摘要

**分类优先级规则**：如果文章内容同时涉及国际和国内，按**主要内容**所在区域分类。

**辅助脚本**：如果智能分类未正确执行，可使用 `fix_classification.py` 自动修复：
```bash
python3 fix_classification.py YYYY-MM-DD
```
该脚本会基于关键词自动分类，并使用原始 `digest` 作为摘要。

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
        "source_file": "sources/xxx.md"
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
- 读取 `sources/*.md` 获取文章原文（用于摘要展开展示）
  - **注意**：如果 `sources/` 目录为空，HTML 中仍会显示摘要，但点击“查看原文”将无法加载完整内容
- 基于 `template.html` 模板渲染响应式静态页面
- 生成 `daily/YYYY-MM-DD/index.html`
- 更新 `daily-index.json` 索引文件，追加新日期条目

**关于 viewer.html**：
- `viewer.html` 是用于查看文章完整原文的页面
- 通过 URL 参数 `?file=path/to/source.md` 访问
- 需要 `sources/` 目录中有对应的 Markdown 文件
- 如果 sources 目录为空，viewer.html 无法正常工作

---

### Step 5: 验证

检查以下产出是否完整：

| 检查项 | 预期结果 |
|--------|---------|
| `daily/YYYY-MM-DD/index.html` | 存在且大小 > 0 |
| `daily/YYYY-MM-DD/classification.json` | 存在，包含 4 个分类键 |
| `daily-index.json` | 已更新，包含新日期条目 |

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
- `server.base_url`：`wechat-query-skill` API 地址

---

## 关键规则

1. **分类时务必阅读原文**：不要仅根据标题判断，必须读取 `source_file` 对应的 Markdown 原文来了解文章内容
   - **当前限制**：如果 `sources/` 目录为空，则基于标题和来源进行自动分类
2. **摘要精炼准确**：1-2 句话概括核心内容，避免冗长
   - **当前实现**：优先使用原始 `digest`，如果为空则使用标题，过长则截断
   - **理想情况**：有原文时由智能体生成精炼摘要
3. **分类冲突时取主要方向**：同时涉及国际和国内的内容，按文章主要讨论的对象/区域分类
4. **同业类优先**：如果文章同时涉及同业和其他分类，**优先归为同业**
5. **每日早报以昨日为默认日期**：用户说“生成早报”时，默认使用昨天的日期
6. **sources 目录重要性**：
   - 保存原文到 `sources/` 目录是可选的，但推荐
   - 有原文时：可以查看完整内容，智能体可生成更准确的摘要
   - 无原文时：仍可使用原始 `digest` 生成早报，但无法查看完整内容
