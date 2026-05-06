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

## 📍 项目路径

**工作目录**：`/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/`

**重要提示**：
- 这是一个独立的 Git 项目，有自己的 `.git` 目录
- 所有脚本都在 `scripts/` 子目录中
- 生成的早报保存在 `daily/YYYY-MM-DD/` 目录

---

## 📅 日期规则（非常重要）

**默认行为**：用户说"生成早报"时，**默认生成昨天的早报**

**如何确定日期**：
```bash
# macOS 系统获取昨天的日期
date -v-1d +%Y-%m-%d

# Linux 系统获取昨天的日期
date -d "yesterday" +%Y-%m-%d
```

**示例**：
- 今天是 2026-05-03 → 生成 2026-05-02 的早报
- 今天是 2026-05-01 → 生成 2026-04-30 的早报

**手动指定日期**：如果用户明确要求生成特定日期的早报，使用用户指定的日期

---

## 🚀 快速开始（一键生成）

### 方式 1：完整自动化流程（推荐）

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts

# 获取昨天的日期
TARGET_DATE=$(date -v-1d +%Y-%m-%d)
echo "生成 $TARGET_DATE 的早报"

# Step 1: 获取文章
python3 fetch_articles.py $TARGET_DATE

# Step 2: 关键词过滤
python3 filter_articles.py $TARGET_DATE

# Step 3: 智能分类（需要人工干预，见下方详细说明）
# 这一步由 AI 智能体完成，读取 filtered_articles.json 并生成 classification.json

# Step 4: 生成 HTML
python3 generate_html.py $TARGET_DATE

echo "✅ 早报生成完成！"
echo "📱 访问: file:///Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/daily/$TARGET_DATE/index.html"
```

### 方式 2：分步执行（调试用）

按照下面的 5 个步骤逐一执行。

---

## 📋 详细工作流程（5 步骤）

### Step 1: 获取文章

**目标**：从微信公众号 API 获取指定日期的所有文章

**命令**：
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 fetch_articles.py YYYY-MM-DD
```

**参数说明**：
- `YYYY-MM-DD`：要获取文章的日期（格式：2026-05-02）
- **不传参数时**：自动使用昨天的日期

**输出文件**：
- `daily/YYYY-MM-DD/sources/*.md` — 每篇文章的 Markdown 原文（可能为空，取决于 API 响应）
- `daily/YYYY-MM-DD/articles_raw.json` — 文章元数据汇总（包含标题、来源、链接、摘要等）

**特性**：
- ✅ PAGE_SIZE=50，减少翻页次数，速度提升 5 倍
- ✅ 并行获取全文（5 线程），但可能因 API 限制而失败
- ✅ 智能降级：全文获取失败时使用 digest 作为备选
- ⏱️ 总耗时：约 1-3 分钟（取决于文章数量）

**常见问题**：
- ❌ **登录态过期**：`wechat-query-skill` 登录态约 4 天过期
  - 解决：在浏览器中重新登录 wechat-query-skill，然后重试
- ❌ **API 返回空**：该日期可能没有新文章
  - 解决：检查日期是否正确，或尝试其他日期

**验证**：
```bash
ls -lh daily/YYYY-MM-DD/
# 应该看到 articles_raw.json 和 sources/ 目录
```

---

### Step 2: 关键词过滤

**目标**：根据配置的关键词过滤出 AI 相关文章

**命令**：
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 filter_articles.py YYYY-MM-DD
```

**过滤逻辑**：
- 读取 `config.json` 中的 `keywords.include` 列表
- 匹配文章的**标题**和**摘要（digest）**
- 不区分大小写
- 不匹配的文章会从 `sources/` 目录中**删除**

**默认关键词**：
```json
{
  "include": ["AI", "大模型", "智能体", "skill"],
  "exclude": []
}
```

**输出文件**：
- `daily/YYYY-MM-DD/filtered_articles.json` — 过滤后的文章列表

**修改关键词**：
编辑项目根目录的 `config.json`，修改后立即生效，无需重启。

**验证**：
```bash
cat daily/YYYY-MM-DD/filtered_articles.json | python3 -m json.tool | head -20
# 查看过滤后的文章数量和字段
```

---

### Step 3: 智能分类（由 AI 智能体完成）

**目标**：对过滤后的文章进行智能分类和摘要生成

**输入文件**：`daily/YYYY-MM-DD/filtered_articles.json`

**输出文件**：`daily/YYYY-MM-DD/classification.json`

#### 🤖 智能体操作流程

**1. 读取文章数据**
```python
import json
with open('daily/YYYY-MM-DD/filtered_articles.json', 'r') as f:
    articles = json.load(f)
```

**2. 对每篇文章执行分类**

对于 `articles` 列表中的每篇文章：

**a) 尝试读取原文（可选）**
```python
# 如果 source_file 存在且 sources/ 目录有文件
if article.get('source_file'):
    try:
        with open(article['source_file'], 'r') as f:
            full_content = f.read()
    except:
        full_content = None
else:
    full_content = None
```

**b) 判断分类（四选一）**

| 分类 | 判断标准 | 典型关键词 |
|------|---------|----------|
| **国际** | 涉及海外公司或国际 AI 动态（技术类） | OpenAI, Anthropic, Google, Meta, Apple, Nvidia, Microsoft, xAI, Stability AI, GPT, Claude, Gemini |
| **国内** | 涉及国内公司、研究机构、学术会议的 AI 动态（技术类） | 阿里, 腾讯, 百度, 字节, 华为, 智谱, 商汤, DeepSeek, 月之暗面, MiniMax, 阶跃星辰, 零一万物, 面壁智能, 通义, 文心；ACL, ICLR, NeurIPS, CVPR, AAAI, EMNLP 等学术会议；中科院、清华、北大等研究机构 |
| **同业** | 涉及银行、金融机构的 AI 应用 | 银行, 金融, 保险, 证券, 风控, 信贷, 理财, 智能客服, 网点, 支付 |
| **其他** | 不属于以上三类的 AI 相关文章，或多主题混合资讯、商业资讯 | 开源项目, 技术教程, 行业分析, 非技术内容；**多主题混合资讯**（如"iPhone销量+安卓动态+腾讯投资"等多条新闻汇总）；**商业资讯**（如产品收费、高层法律纠纷、人事变动等） |

**分类优先级规则**：
1. **同业优先**：如果文章同时涉及同业和其他分类，**优先归为同业**
2. **主体与场景区分原则**：区分“技术研发”与“商业资讯”。即使主体是国际/国内大厂，若内容本质是商业行为（如豆包收费、OpenAI总裁认罪、斯坦福HAI重组），应归为“其他”
3. **多主题混合资讯归为其他**：如果标题包含多个不相关的新闻主题，属于资讯汇总类，归为"其他"
4. **不确定性时**：如果无法明确判断，归为"其他"

**c) 生成摘要**

**优先级顺序**：
1. ✅ **优先使用原始 `digest`**：从 `filtered_articles.json` 中获取
2. ⚠️ **如果 `digest` 为空**：使用文章标题作为摘要
3. ✂️ **如果 `digest` 过长（>200字符）**：截取前200字符并添加"..."
4. 🎯 **理想情况**（有原文时）：由智能体生成1-2句精炼摘要

**示例代码**：
```python
def generate_summary(article):
    digest = article.get('digest', '')
    title = article.get('title', '')
    
    if digest and len(digest) > 0:
        # 使用原始 digest
        if len(digest) > 200:
            return digest[:200] + '...'
        return digest
    else:
        # 降级使用标题
        return title
```

**3. 大模型打标规则（非常重要）**

在分类和生成摘要后，需要判断文章是否涉及**大模型技术本身**，并设置 `is_model_related` 字段。

**⚠️ 核心原则**：需区分"大模型本身"与"大模型应用场景"
- ✅ **应该打标**：模型发布、模型测评、模型架构（技术论文、架构创新、底层技术研究）
- ❌ **不应打标**：AI 应用功能、行业资讯、公司动态、基础设施讨论、应用类文章

**应打标的情况**：
1. **模型发布**：新模型正式发布、版本更新（如 "GPT-5 发布"、"Claude 3.5 更新"）
2. **模型测评**：性能对比、实测报告、benchmark 结果（如 "GPT vs Claude 对比测试"）
3. **模型架构**：技术论文、架构创新、底层技术研究（如 "MoE 架构优化"、"RLHF 新方法"）

**不应打标的情况**：
- AI 应用功能（工具集成、行业应用、企业试用）
- 行业资讯（公司动态、融资新闻、裁员消息）
- 基础设施讨论（芯片适配、服务器采购、算力建设）
- 应用类文章（AI CEO、AI 客服、AI 教育等应用场景）
- 行业活动报道（开发者日、技术大会、会议资讯）
- 公司榜单评选、社会影响分析
- **智能体（Agent）相关研究**：除非直接涉及大模型底层架构，否则 Agent 的环境协同、应用进化等通常视为应用层研究，不打标。

**示例**：
- ✅ "OpenAI 参与，重卷 ImageNet：终于把 FID 做成训练" → `true`（模型训练技术研究）
- ✅ "斯坦福重磅研究登 Nature！AI 凭空造出前所未有蛋白质" → `true`（AI 研究突破）
- ✅ "AI 大模型的「中文税」：中文比英文更费 Token" → `true`（大模型技术分析）
- ❌ "Anthropic 惊悚报告：当 AI 开始破坏实验室代码" → `false`（AI 安全应用，非模型本身）
- ❌ "第一个全职 AI CEO 来了" → `false`（AI 应用场景）
- ❌ "乌鲁木齐银行 AI 专项工作采购" → `false`（金融应用，非模型技术）
- ❌ "大学春招与 AI 求职焦虑" → `false`（社会影响报道）
- ❌ "Agent-World：扩展真实世界环境，让智能体与环境协同进化！" → `false`（智能体应用环境研究，非大模型本身）

**判断逻辑**：
```python
def is_model_related(title, digest):
    """检测文章是否涉及大模型技术本身"""
    # 首先检查是否包含大模型关键词
    MODEL_KEYWORDS = [
        "大模型", "LLM", "GPT", "Claude", "Gemini", "Qwen", "通义", "文心",
        "DeepSeek", "Llama", "Mistral", "模型发布", "模型评测", "benchmark",
        "参数规模", "开源模型", "基座模型", "foundation model", "语言模型"
    ]
    text = f"{title} {digest}".lower()
    has_keyword = any(kw.lower() in text for kw in MODEL_KEYWORDS)
    
    if not has_keyword:
        return False
    
    # 即使有关键词，也要判断是否是"应用类"内容
    APPLICATION_KEYWORDS = [
        "采购", "外包", "招聘", "裁员", "收购", "融资",
        "客服", "教育", "医疗", "金融", "银行", "保险",
        "CEO", "管理", "应用", "落地", "试用"
    ]
    is_application = any(kw in text for kw in APPLICATION_KEYWORDS)
    
    # 如果是应用类内容，即使有大模型关键词也不打标
    if is_application:
        return False
    
    return True
```

---

**4. 构建分类结果**

```python
classification = {
    "国际": [],
    "国内": [],
    "同业": [],
    "其他": []
}

for article in articles:
    category = classify_article(article)  # 你的分类逻辑
    summary = generate_summary(article)   # 你的摘要逻辑
    model_tag = is_model_related(article.get('title', ''), summary)  # 大模型打标
    
    classified_article = {
        "aid": article.get('aid'),
        "title": article.get('title'),
        "source": article.get('source'),
        "link": article.get('link'),
        "digest": summary,
        "source_file": article.get('source_file', ''),
        "category_reason": "分类理由（可选，便于调试）",
        "is_model_related": model_tag  # 大模型标签
    }
    
    classification[category].append(classified_article)
```

**4. 保存结果**

```python
import datetime

result = {
    "date": "YYYY-MM-DD",
    "generated_at": datetime.datetime.now().isoformat(),
    "classification": classification,
    "stats": {
        "国际": len(classification["国际"]),
        "国内": len(classification["国内"]),
        "同业": len(classification["同业"]),
        "其他": len(classification["其他"]),
        "total": sum(len(v) for v in classification.values())
    },
    "excluded": []  # 如果有被排除的文章，在这里说明
}

with open('daily/YYYY-MM-DD/classification.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✅ 分类完成：国际{result['stats']['国际']}篇, 国内{result['stats']['国内']}篇, "
      f"同业{result['stats']['同业']}篇, 其他{result['stats']['其他']}篇, "
      f"共{result['stats']['total']}篇")
```

#### 🔧 辅助工具

如果智能分类效果不佳，可以使用自动分类脚本：

```bash
python3 fix_classification.py YYYY-MM-DD
```

该脚本基于关键词自动分类，并使用原始 `digest` 作为摘要，适合快速生成 baseline。

#### ✅ 验证分类结果

```bash
cat daily/YYYY-MM-DD/classification.json | python3 -m json.tool | grep -A 5 '"stats"'
# 应该看到各分类的文章数量统计
```

---

### Step 4: 生成 HTML

**目标**：将分类结果渲染为响应式 HTML 页面

**命令**：
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 generate_html.py YYYY-MM-DD
```

**工作流程**：
1. 读取 `classification.json` 获取分类和摘要数据
2. **优先使用 classification.json 中的 `is_model_related` 标签**（不会重新检测）
3. 读取 `sources/*.md` 获取文章原文（用于 viewer.html 查看完整内容）
4. 基于 `template.html` 模板渲染页面
5. 生成 `daily/YYYY-MM-DD/index.html`
6. 更新 `daily-index.json` 索引文件，追加新日期条目

**重要说明**：
- ✅ `generate_html.py` 会**优先使用** classification.json 中的人工标注标签
- ✅ 每个分类板块内，有大模型标签的文章会**自动排在最上方**
- ❌ 不会通过关键词重新检测覆盖人工标注

**输出文件**：
- `daily/YYYY-MM-DD/index.html` — 早报主页
- `daily-index.json` — 更新的索引（包含所有日期的列表）

**关于原文查看**：
- `viewer.html` 是用于查看文章完整原文的页面
- 通过 URL 参数访问：`viewer.html?file=daily/YYYY-MM-DD/sources/xxx.md`
- **需要** `sources/` 目录中有对应的 Markdown 文件
- 如果 sources 目录为空，点击"查看原文"将无法加载完整内容（但不影响早报展示）

**验证**：
```bash
# 检查 HTML 文件是否存在且大小正常
ls -lh daily/YYYY-MM-DD/index.html

# 在浏览器中打开预览
open daily/YYYY-MM-DD/index.html
```

---

### Step 5: 验证与推送

**本地验证清单**：

| 检查项 | 命令 | 预期结果 |
|--------|------|----------|
| HTML 文件存在 | `ls daily/YYYY-MM-DD/index.html` | 文件存在且大小 > 0 |
| 分类文件完整 | `cat daily/YYYY-MM-DD/classification.json \| python3 -m json.tool \| grep stats` | 包含 4 个分类键和统计数据 |
| 索引已更新 | `cat daily-index.json \| python3 -m json.tool \| grep YYYY-MM-DD` | 包含新日期条目 |
| 页面可访问 | `open daily/YYYY-MM-DD/index.html` | 浏览器正常显示 |

**推送到 GitHub（可选）**：

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank

# 添加新文件
git add daily/YYYY-MM-DD/
git add daily-index.json

# 提交
git commit -m "Add daily report for YYYY-MM-DD"

# 推送
git push origin master
```

**在线访问**：
```
https://keejo125.github.io/AI_Daily_For_Bank/daily/YYYY-MM-DD/
```

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

## ⚠️ 关键规则（必须遵守）

### 1. 日期计算规则

**默认行为**：用户说"生成早报"、"生成日报"时，**默认使用昨天的日期**

**如何计算昨天**：
```bash
# macOS
date -v-1d +%Y-%m-%d

# Linux
date -d "yesterday" +%Y-%m-%d
```

**示例**：
- 当前系统时间：2026-05-03 → 生成 2026-05-02 的早报
- 当前系统时间：2026-04-28 → 生成 2026-04-27 的早报

**例外情况**：如果用户明确指定日期（如"生成 2026-05-01 的早报"），则使用用户指定的日期

---

### 2. 分类规则

**分类优先级**（从高到低）：
1. **同业优先**：涉及银行、金融机构的 AI 应用 → 归为"同业"
2. **主要内容原则**：同时涉及国际和国内 → 按文章主要讨论的对象分类
3. **不确定性处理**：无法明确判断 → 归为"其他"

**分类判断要点**：
- ✅ **阅读原文**：不要仅根据标题判断，尽量读取 `source_file` 对应的 Markdown 原文
- ✅ **关注主体**：识别文章主要讨论的公司/机构/技术
- ✅ **考虑语境**：同一公司可能有国际/国内不同业务线

**如果 sources 目录为空**：
- 基于标题、来源公众号名称进行自动分类
- 使用 `fix_classification.py` 脚本辅助

---

### 3. 摘要生成规则

**优先级顺序**：
1. ✅ **优先使用原始 `digest`**（来自 `filtered_articles.json`）
2. ✂️ **过长截断**：如果 `digest` > 200字符，截取前200字符 + "..."
3. 📝 **降级使用标题**：如果 `digest` 为空，使用文章标题
4. 🎯 **理想情况**：有原文时由智能体生成1-2句精炼摘要

**摘要质量要求**：
- 长度：1-2 句话，不超过 200 字符
- 内容：概括核心观点或关键信息
- 避免：冗长描述、重复标题、无关细节

---

### 4. sources 目录的重要性

**有原文时**（推荐）：
- ✅ 可以查看完整文章内容（通过 viewer.html）
- ✅ 智能体可生成更准确的分类和摘要
- ✅ 支持深度阅读和研究

**无原文时**（仍可工作）：
- ⚠️ 仍可使用原始 `digest` 生成早报
- ❌ 无法查看完整内容（viewer.html 无法加载）
- ⚠️ 分类准确性可能降低

**建议**：尽量保存原文到 `sources/` 目录，即使 API 获取全文失败也要保留 digest

---

### 5. 错误处理与调试

**Step 1 失败（获取文章）**：
- 检查 `wechat-query-skill` 登录态是否过期
- 在浏览器中重新登录，然后重试
- 检查网络连接和 API 地址配置

**Step 2 失败（过滤后为空）**：
- 检查 `config.json` 中的关键词是否过于严格
- 尝试放宽关键词或添加更多同义词
- 检查该日期是否有相关文章

**Step 3 失败（分类不准确）**：
- 使用 `fix_classification.py` 自动修复
- 手动编辑 `classification.json` 调整分类
- 检查分类规则是否需要优化

**Step 4 失败（HTML 生成错误）**：
- 检查 `classification.json` 格式是否正确
- 检查 `template.html` 是否存在
- 查看脚本输出的错误信息

---

### 6. 文件清理规则

**每次生成新日期的早报前**：
- ✅ 创建新的 `daily/YYYY-MM-DD/` 目录
- ✅ 不要删除历史日期的数据
- ❌ 不要修改已生成的历史早报

**Git 提交时**：
- ✅ 只提交新生成的日期目录
- ✅ 更新 `daily-index.json`
- ❌ 不提交 `scripts/` 目录（已被 .gitignore 排除）
- ❌ 不提交 `config.json`（包含敏感信息）

---

## 📚 快速参考

### 常用命令速查

```bash
# 1. 确定日期
TARGET_DATE=$(date -v-1d +%Y-%m-%d)  # macOS
echo "目标日期: $TARGET_DATE"

# 2. 获取文章
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 fetch_articles.py $TARGET_DATE

# 3. 过滤文章
python3 filter_articles.py $TARGET_DATE

# 4. 智能分类（由 AI 智能体完成）
# 读取 filtered_articles.json，生成 classification.json

# 5. 生成 HTML
python3 generate_html.py $TARGET_DATE

# 6. 验证
ls -lh ../daily/$TARGET_DATE/index.html
open ../daily/$TARGET_DATE/index.html

# 7. 推送（可选）
cd ..
git add daily/$TARGET_DATE/
git add daily-index.json
git commit -m "Add daily report for $TARGET_DATE"
git push origin master
```

### 文件结构

```
AI-Daily-for-bank/
├── scripts/                  # Python 脚本（不提交到 Git）
│   ├── fetch_articles.py     # 获取文章（注意：不是 fetch_articles_fast.py）
│   ├── filter_articles.py
│   ├── generate_html.py
│   └── fix_classification.py
├── daily/                    # 早报数据
│   ├── 2026-05-01/
│   │   ├── index.html       # 早报主页
│   │   ├── sources/         # Markdown 原文
│   │   ├── articles_raw.json
│   │   ├── filtered_articles.json
│   │   └── classification.json
│   └── ...
├── template.html             # HTML 模板
├── viewer.html              # 原文查看器
├── daily-index.json         # 日期索引
├── search-index.json        # 搜索索引
├── config.json              # 配置文件（不提交到 Git）
└── README.md                # 项目说明
```

### 常见问题速查

| 问题 | 解决方案 |
|------|----------|
| API 登录态过期 | 在浏览器中重新登录 wechat-query-skill |
| 过滤后文章数为 0 | 检查关键词配置，尝试放宽条件 |
| 分类不准确 | 使用 `fix_classification.py` 或手动调整 |
| HTML 无法打开 | 检查 classification.json 格式是否正确 |
| viewer.html 无法加载 | 检查 sources/ 目录是否有对应的 .md 文件 |

---

## 🔗 相关资源

- **GitHub 仓库**: https://github.com/keejo125/AI_Daily_For_Bank
- **在线预览**: https://keejo125.github.io/AI_Daily_For_Bank/
- **推送技能**: `/push-daily-to-github` - 将早报推送到 GitHub
