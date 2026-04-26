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

- 不传日期参数则默认获取**昨天**的文章，生成**今天**的早报
- **日期逻辑**：传入的日期是**文章内容日期**（昨天），生成的早报日期是**当天**（昨天+1天）
  - 例如：传入 `2026-04-24`，获取 2026-04-24 的文章，生成 2026-04-25 的早报
- 调用 `wechat-query-skill` 的 `/api/rss/export/{date}` 导出接口，一次请求获取当天所有文章
- 耗时 1-3 秒（旧版逐公众号翻页需 4-10 分钟）
- 导出接口从服务器 SQLite 读取，**不依赖微信登录态**
- 输出：
  - `daily/YYYY-MM-DD/sources/*.md` — 每篇文章的 Markdown 原文
  - `daily/YYYY-MM-DD/articles_raw.json` — 文章元数据汇总

**重要说明**：
- **早报日期 = 文章内容日期 + 1天**
- 例如今天是 2026-04-25，执行脚本时传入 2026-04-24，获取 2026-04-24 的文章，生成 2026-04-25 的早报
- 文件夹命名使用**文章内容日期**（如 `daily/2026-04-24/`）
- HTML页面中的日期显示为**早报日期**（如 `<title>智能研发早报 2026-04-25</title>`）
- classification.json 中包含两个字段：
  - `"date": "2026-04-25"` - 早报日期（今天）
  - `"article_date": "2026-04-24"` - 文章内容日期（昨天）

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

**推荐：使用辅助脚本生成模板**

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 create_classification.py YYYY-MM-DD
```

该脚本会：
- 基于 `filtered_articles.json` 自动生成 `classification.json` 模板
- 自动填充 aid, title, source, link, source_file
- 根据关键词预分类（国际/国内/同业/其他）
- 自动处理中文引号（替换为方括号）
- 保留空的 digest 字段供智能体填写摘要

**然后智能体执行以下操作：**

读取 `daily/YYYY-MM-DD/classification.json`，对每篇文章执行以下操作：

1. **读取原文**：根据 `source_file` 路径读取对应的 Markdown 文件，了解文章内容
2. **判断分类**：

| 分类           | 判断标准                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **国际** | 涉及海外公司（OpenAI、Anthropic、Google、Meta、Apple、Nvidia、Microsoft、xAI、Stability AI 等）或国际 AI 动态                        |
| **国内** | 涉及国内公司（阿里、腾讯、百度、字节、华为、智谱、商汤、深度求索、月之暗面、MiniMax、阶跃星辰、零一万物、面壁智能 等）或国内 AI 动态 |
| **同业** | 涉及银行、金融机构的 AI 应用（办公、研发以及运维领域），**优先归类**                                                                               |
| **其他** | 不属于以上三类的 AI 相关文章，包括：<br>- 活动广告类（会议、榜单申报等）<br>- 资讯类（人事变动、行业八卦等）<br>- 泛文化类（读书、生活等） |

3. **生成摘要**：为每篇文章生成 100-200字的中文摘要；不要使用原始 `digest`
4. **中文字符处理（重要）**：
   - **问题**：`generate_html.py` 会将中文引号替换为英文引号，破坏 JSON 结构
   - **解决方案**：在写入 `classification.json` 前，必须将所有文本字段中的中文引号替换为方括号
   - **执行步骤**（Python示例）：
     ```python
     # 在写入 classification.json 前，对所有文本字段执行
     text = text.replace('\u201c', '【').replace('\u201d', '】')  # 中文双引号
     text = text.replace('\u2018', '「').replace('\u2019', '」')  # 中文单引号
     ```
   - **影响字段**：title、digest、source_file 三个字段都需要处理
   - **注意**：即使手动创建 classification.json，也必须预先处理中文引号
5. **大模型标签规则**（重要）：
   - **添加标签的条件**（必须满足以下之一）：
     - ✅ **模型发布**：新模型正式发布、版本更新（如 DeepSeek V4、GPT-5.5）
     - ✅ **模型测评**：性能对比、实测报告、benchmark 评测
     - ✅ **模型架构**：技术论文、底层技术研究（LLM DNA、注意力机制、Muon优化器等）
   - **不添加标签的情况**：
     - ❌ AI应用功能（如 Chronicle 屏幕记忆、Copilot 集成）
     - ❌ 行业资讯（如量化公司创始人背景、人事变动）
     - ❌ 基础设施讨论（如 Token 工厂、算力芯片、数据中心）
     - ❌ 公司动态（如 OpenAI 裁员、投资并购、商业竞争、收入估值）
   - **判断技巧**：看主语是谁——模型本身 vs 其他产品/行业/公司
5. **特殊内容处理**：
   - **活动广告类内容直接剔除**：如"Qoder Together 长沙站"、"榜单申报"等纯活动推广内容
   - **无关内容归入其他**：如"鹅厂员工读书"等与AI技术无直接关联的内容
   - **资讯类内容归入其他**：如"华人CTO任职"等人事变动资讯
6. **多公众号整合规则**：
   - **同一事件多篇报道**：如果同一事件有多篇不同公众号的报道，按各篇侧重点独立分类
   - **整合展示**：在 HTML 中合并为一篇文章卡片，但显示多个来源标签
   - **示例**：DeepSeek V4 发布有机器之心（技术架构）、InfoQ（成本实测）、量子位（市场影响）三篇
     - 合并后标题：DeepSeek V4 发布：技术突破与成本优势
     - 来源标签：[机器之心] [InfoQ] [量子位]
     - 点击不同标签跳转到对应公众号的原文
7. **分类优先级规则**：如果文章内容同时涉及国际和国内，按**主要内容**所在区域分类。

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
- 读取 `sources/*.md` 获取文章原文（提取多来源信息和关键词匹配）
- 基于 `template.html` 模板渲染响应式静态页面
- **多来源标签**：合并后的文章显示多个公众号来源标签，每个标签可点击跳转到 `viewer.html` 查看对应原文
- **无"阅读原文"按钮**：已用多来源标签替代
- 生成 `daily/YYYY-MM-DD/index.html`
- 更新 `daily-index.json` 和 `search-index.json` 索引文件
- **文章排序规则**：在每个分类（国际/国内/同业/其他）内，有大模型标签的文章自动排在前面
  - 判断依据：`generate_html.py` 中的 `detect_model_related()` 函数自动检测
  - 例如："国内动态"中，DeepSeek-V4相关文章会排在非大模型文章之前

**关于 viewer.html**：

- 通过 URL 参数 `?file=daily/YYYY-MM-DD/sources/xxx.md` 访问
- 自动对中文文件路径做 `encodeURIComponent` 编码后 fetch
- 使用 marked.js 渲染 Markdown，自动提取标题和公众号来源

---

### Step 5: 验证与反馈

检查以下产出是否完整：

| 检查项                                   | 预期结果               |
| ---------------------------------------- | ---------------------- |
| `daily/YYYY-MM-DD/index.html`          | 存在且大小 > 0         |
| `daily/YYYY-MM-DD/classification.json` | 存在，包含 4 个分类键  |
| `daily-index.json`                     | 已更新，包含新日期条目 |

验证通过后，**不要推送到服务器部署**，而是将生成的 HTML 页面内容或访问链接提供给用户预览。

同时，主动向用户请求分类反馈：
- 询问用户对文章分类是否满意
- 收集用户对分类规则的建议
- 记录用户指出的分类错误案例

根据用户反馈优化 Step 3 的分类规则：
1. 如果用户指出某篇文章分类错误，分析错误原因
2. 更新分类判断标准，补充特殊情况的处理规则
3. 在后续生成中应用优化后的规则

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
5. **日期逻辑规范**：
   - 用户说"生成早报"时，默认使用昨天的日期作为**文章内容日期**，生成今天的早报
   - **早报日期 = 文章内容日期 + 1天**
   - 例如：今天是 2026-04-25，传入 2026-04-24，获取昨天的文章，生成今天的早报
   - 文件夹命名：使用文章内容日期（`daily/2026-04-24/`）
   - HTML标题：显示早报日期（`<title>智能研发早报 2026-04-25</title>`）
6. **中文字符处理规范**：
   - **问题根源**：`generate_html.py` 会将中文引号（U+201C/U+201D "" 和 U+2018/U+2019 ''）替换为英文引号，这会破坏 JSON 结构
   - **解决方案**：在生成 `classification.json` 时，所有文本字段（title、digest、source_file）中的中文引号必须预先替换为方括号【】或「」
   - **执行步骤**：
     ```python
     # 在写入 classification.json 前执行
     text = text.replace('\u201c', '【').replace('\u201d', '】')  # 双引号
     text = text.replace('\u2018', '「').replace('\u2019', '」')  # 单引号
     ```
   - **影响字段**：title、digest、source_file 三个字段都需要处理
   - **原因说明**：generate_html.py 第564-565行会执行中文引号替换，如果 classification.json 中包含中文引号，替换后会破坏 JSON 语法
7. **source_file 模糊匹配**：`generate_html.py` 用 4 字符滑动窗口关键词提取 + 2 字符 fallback 解决中文文件名匹配问题
8. **不推送服务器**：生成完成后仅提供本地预览，不执行任何服务器部署或推送操作
9. **持续优化分类**：根据用户反馈不断调整和完善分类规则，提高分类准确性
10. **活动广告类内容处理**：
    - **纯活动推广内容应归入"其他"或直接剔除**：如会议通知、榜单申报、线下活动等
    - **判断标准**：如果文章主要内容是宣传活动本身而非AI技术/产品，则归为其他
    - **示例**："Qoder Together 长沙站"、"倒计时3天！榜单申报"等
11. **大模型标签自动检测**：
    - `generate_html.py` 中的 `detect_model_related()` 函数会自动判断是否为大模型相关文章
    - **判断标准**：仅针对模型发布、测评、架构的内容（见 Step 3 第4条）
    - **排除规则**：产品功能、行业资讯、基础设施、公司动态等均不添加标签
    - **标签显示**：在摘要前添加 `【大模型】` 前缀，并在排序时优先展示
    - **实现细节**：通过关键词精准匹配 + 排除规则，避免误判

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
