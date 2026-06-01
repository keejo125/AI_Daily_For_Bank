---
name: ai-daily-report
description: >
  生成每日 AI 智能研发早报。从微信公众号获取文章，按关键词过滤，
  智能分类（国际/国内/同业/其他）并生成摘要，渲染为响应式静态 HTML 页面。
  使用场景：当用户要求生成今日/昨日AI早报、获取公众号文章汇总、
  生成智能研发日报时触发。触发词：早报、日报、AI daily、每日汇总。
license: MIT
metadata:
  version: "1.4"
  category: productivity
  updated: "2026-05-27"
  changelog: |
    v1.4 (2026-05-27):
    - 新增：分类决策流程（三步判断法：技术内容 → 主体归属 → 特殊情况）
    - 新增：常见分类错误对照表（7种典型错误场景）
    - 新增：大模型打标决策流程和边界案例判定指南
    - 新增：强制验证清单（6项检查，含Agent框架/工程优化示例）
    - 优化：主体归属判断要点（看项目归属，不看报道语言）
    - 优化：验证失败处理流程和快速验证命令
    v1.3 (2026-05-22):
    - 新增：Step 3.5 中的 1.5步验证 - source_file 路径符号标准化检查
    - 新增：中文标点符号（引号、书名号等）的 Unicode 转义规范
    - 新增：文件路径模糊匹配和自动修正机制
    - 新增：历史案例库（皇马文章、腾讯马维斯文章）
    - 优化：预防措施代码示例，在生成 classification.json 时自动验证路径
    v1.2 (2026-05-14):
    - 新增：产品功能更新属于技术内容（Qoder Browser Use、Buddy产品迭代）
    - 新增：工具设计/工程实践属于技术内容（Skill工程化、LLM Wiki知识管理）
    - 新增：必须删除的内容类型（活动宣传类、招聘类）
    - 新增：纯商业资讯判定标准（财报、营收、资本支出、ARR收入）
    - 新增：source字段为空时的检查和补充规则
    - 优化：技术内容vs非技术内容的细化分类标准
    v1.1 (2026-05-08):
    - 新增：明确国际/国内/同业仅放技术内容，非技术内容归入“其他”
    - 新增：相同主题多源报道合并规则（merged_articles字段）
    - 优化：OpenAI等美国公司归类为国际的示例
    - 优化：技术内容vs非技术内容判定标准
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

# Step 3: 智能分类与合并（需要人工干预，见下方详细说明）
# 分两步执行：
#   第一步：分类与大模型打标
#   第二步：同主题合并判断
# 这一步由 AI 智能体完成，读取 filtered_articles.json 并生成 classification.json

# ⚠️⚠️⚠️ Step 3.5: 分类验证（强制执行！）⚠️⚠️⚠️
# 
# 【重要】在生成 HTML 之前，AI 助手必须执行分类验证！
# 这是强制步骤，不可跳过！
#
# 验证目标：
# 1. ✅ 国际/国内/同业是否只包含技术内容？
# 2. ✅ 非技术内容是否都归入“其他”？
# 3. ✅ 开发工具、工程实践、技术路线是否被正确识别为技术内容？
# 4. ✅ 公司属地是否正确（Anthropic/Google/CMU等应归入国际）？
# 5. ✅ 大模型打标是否准确？
# 6. ✅ source_file 路径是否正确？中文标点是否已转义？文件是否存在？
# 7. ✅ 同主题文章是否正确合并？
# 8. ✅ 合并标记和 merged_articles 字段是否正确？
#
# 验证方法：
# - AI 助手必须逐项检查 classification.json 中的每篇文章
# - 对照 skill 中的"技术内容 vs 非技术内容"判定标准
# - 发现错误立即修正，然后重新保存 classification.json
# - 验证通过后才能进入 Step 4
#
# 常见错误类型：
# ❌ 人事变动（招聘、离职、薪酬）→ 应归入"其他"
# ❌ 产品营销（表情包、发布会）→ 应归入"其他"
# ❌ 会议活动（论坛预告、报名通道）→ 应归入"其他"
# ❌ 行业资讯（就业数据、融资新闻）→ 应归入"其他"
# ❌ 企业战略观点 → 应归入"其他"
# ❌ 消费产品发布 → 应归入"其他"
# ❌ 行业应用落地（医疗器械认证）→ 应归入"其他"
#
# 验证命令示例：
# cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
# python3 -c "
# import json, os
# with open('daily/YYYY-MM-DD/classification.json', 'r') as f:
#     data = json.load(f)
# errors = []
# for category in ['国际', '国内', '同业', '其他']:
#     for article in data['classification'][category]:
#         if article.get('source_file'):
#             full_path = os.path.join('daily/YYYY-MM-DD', article['source_file'])
#             if not os.path.exists(full_path):
#                 errors.append(f'{category}: {article[\"title\"][:40]}... - 文件不存在')
# if errors:
#     print('❌ 发现问题:')
#     for error in errors:
#         print(f'  - {error}')
# else:
#     print('✅ 所有文件路径正确!')
# "
#
# 【警告】如果验证发现错误，必须修正后重新验证，直到完全通过！

# Step 4: 生成 HTML
python3 generate_html.py $TARGET_DATE

echo "✅ 早报生成完成！"
echo "📱 访问: file:///Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/daily/$TARGET_DATE/index.html"
```

### 方式 2：分步执行（调试用）

按照下面的 6 个步骤逐一执行。

---

## 📋 详细工作流程（6 步骤）

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

### Step 3: 智能分类与合并（由 AI 智能体完成）

**目标**：对过滤后的文章进行智能分类、大模型打标、同主题合并

**输入文件**：`daily/YYYY-MM-DD/filtered_articles.json`

**输出文件**：`daily/YYYY-MM-DD/classification.json`

#### 🤖 智能体操作流程（分两步执行）

---

### 🔹 第一步：分类与大模型打标

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

**b) 判断分类(四选一)**

**⚠️ 核心原则：国际/国内/同业仅放技术内容，非技术内容全部归入"其他"**

### 📋 分类决策流程（按顺序执行）

**第一步：判断是否为技术内容？**

```
文章内容 → 是技术内容？ → 是 → 进入第二步
              ↓
             否 → 直接归入"其他"
```

**技术内容判定标准**：
- ✅ 模型发布、版本更新、架构创新
- ✅ 算法研究、技术论文、benchmark测评
- ✅ 工程实践、开发工具、技术标准
- ✅ 底层技术研究、框架开源
- ✅ 产品功能更新（如Qoder Browser Use、Buddy产品迭代）
- ✅ 工具设计/工程实践（如Skill工程化、LLM Wiki知识管理）
- ✅ 技术路线规划

**非技术内容判定标准**（必须归入"其他"）：
- ❌ 融资新闻、估值报道、收购合并
- ❌ 法律纠纷、人事变动、公司动态
- ❌ 行业应用案例、产品体验评测
- ❌ 培训认证、会议活动、榜单评选
- ❌ 基础设施投资、算力建设（纯商业角度）
- ❌ 纯商业资讯（财报、营收、资本支出、ARR收入）
- ❌ 招聘类内容（岗位招聘、人才需求）

**第二步：判断主体归属？**

```
技术内容 → 主体是银行/金融机构？ → 是 → "同业"
              ↓ 否
         主体是国内公司/机构？ → 是 → "国内"
              ↓ 否
         → "国际"
```

**主体归属判断要点**：
- **看项目/作者归属，不看报道语言**
  - 例：Hermes Agent（NousResearch）→ 国际开源项目 → "国际"
  - 例：龙虾之父Peter的Skill优化 → 国际开发者 → "国际"
  - 例：中文媒体报道国外技术 → 仍按技术归属判断

- **国内公司/机构**：阿里、腾讯、百度、字节、华为、智谱、商汤、DeepSeek、月之暗面、MiniMax、阶跃星辰、零一万物、面壁智能、通义、文心；中科院、清华、北大等

- **海外公司/机构**：OpenAI、Anthropic、Google、Meta、Apple、Nvidia、Microsoft、xAI、Stability AI、CMU、哈佛等

- **银行/金融机构**：各大银行、支付宝、蚂蚁集团、保险公司、证券公司等

**第三步：特殊情况处理**

| 情况 | 处理方式 | 示例 |
|------|---------|------|
| 同业优先 | 同时涉及同业和其他分类 → 优先"同业" | 银行采用AI技术 → "同业" |
| 多主题混合 | 标题包含多个不相关新闻 → "其他" | "A公司融资+B公司发布+C公司动态" → "其他" |
| 主体与场景区分 | 区分"技术研发"与"商业资讯" | OpenAI总裁辞职 → "其他"（人事变动） |
| 不确定性 | 无法明确判断 → "其他" | - |

---

**⚠️ 常见分类错误对照表**

| 文章类型 | 常见错误 | 正确分类 | 原因 |
|---------|---------|---------|------|
| 国际开源项目(Agent框架) | 误判为"国内"(因为中文报道) | 国际 | 看项目归属,不看报道语言 |
| 国际开发者技术分享 | 误判为"国内" | 国际 | 看作者/主体归属 |
| OpenAI人事变动 | 误判为"国际" | 其他 | 人事变动是非技术内容 |
| Agent框架工程优化 | 误标 is_model_related=true | false | 不是大模型本身 |
| 融资新闻(即使有技术公司) | 误判为技术分类 | 其他 | 融资本身是非技术内容 |
| 产品营销/表情包 | 误判为技术内容 | 其他 | 属于商业营销 |
| 会议活动预告 | 误判为技术内容 | 其他 | 属于活动宣传 |

---

| 分类 | 判断标准 | 典型关键词 |
|------|---------|----------|
| **国际** | 涉及海外公司或国际 AI **技术动态** | OpenAI, Anthropic, Google, Meta, Apple, Nvidia, Microsoft, xAI, Stability AI, GPT, Claude, Gemini |
| **国内** | 涉及国内公司、研究机构、学术会议的 AI **技术动态** | 阿里, 腾讯, 百度, 字节, 华为, 智谱, 商汤, DeepSeek, 月之暗面, MiniMax, 阶跃星辰, 零一万物, 面壁智能, 通义, 文心；ACL, ICLR, NeurIPS, CVPR, AAAI, EMNLP 等学术会议；中科院、清华、北大等研究机构 |
| **同业** | 涉及银行、金融机构的 AI **技术应用** | 银行, 金融, 保险, 证券, 风控, 信贷, 理财, 智能客服, 网点, 支付 |
| **其他** | **所有非技术内容** + 不属于以上三类的 AI 相关文章 | **商业资讯**（融资、估值、法律纠纷、人事变动）；**行业应用**（企业案例、产品体验）；**教育培训**（认证、公开课）；**行业资讯**（趋势分析、投资新闻）；多主题混合资讯 |

**技术内容 vs 非技术内容判定**：
- ✅ **技术内容**（可放入国际/国内/同业）：
  - 模型发布、版本更新、架构创新
  - 算法研究、技术论文、benchmark测评
  - 工程实践、开发工具、技术标准
  - 底层技术研究、框架开源
  - **产品功能更新**（如Qoder Browser Use、Buddy产品迭代）
  - **工具设计/工程实践**（如Skill工程化、LLM Wiki知识管理）
  
- ❌ **非技术内容**（必须归入"其他"）：
  - 融资新闻、估值报道、收购合并
  - 法律纠纷、人事变动、公司动态
  - 行业应用案例、产品体验评测
  - 培训认证、会议活动、榜单评选
  - 基础设施投资、算力建设（纯商业角度）
  - **纯商业资讯**（财报、营收、资本支出、ARR收入）
  - **招聘类内容**（岗位招聘、人才需求）

**⚠️ 必须删除的内容类型**：
- 🗑️ **活动宣传类**：专场、创享日、峰会预告、年会、培训邀请
  - 关键词：`专场`、`创享日`、`峰会`、`年会`、`培训`、`邀你`、`共赴`、`落地`、`XX站`
  - 示例："阿里云AI创享日Qoder专场·重庆站"、"520来量子位峰会一起聊AI"
- 🗑️ **招聘类**：岗位招聘、人才需求、冲浪选手招募
  - 关键词：`招`、`招聘`、`求职`、`候选人`
  - 示例："量子位招小红书AI冲浪选手"

**示例**：
- ✅ “OpenAI公开大规模稳定训练的秘密” → **国际**（技术内容：模型训练技术）
- ✅ “Anthropic估值冲爆1.2万亿” → **其他**（非技术：融资估值）
- ✅ “马斯克解散xAI，22万张GPU租给Anthropic” → **其他**（非技术：商业合作）
- ✅ “北大团队提出SEAlign对齐框架” → **国内**（技术内容：学术研究）
- ✅ “苏州银行智能体项目采购” → **同业**（技术内容：银行AI应用）

**分类优先级规则**：
1. **同业优先**：如果文章同时涉及同业和其他分类，**优先归为同业**
2. **技术优先原则**：先判断是否为技术内容，非技术内容一律归入“其他”
3. **主体与场景区分原则**：区分“技术研发”与“商业资讯”。即使主体是国际/国内大厂，若内容本质是商业行为（如豆包收费、OpenAI总裁认罪、斯坦福HAI重组），应归为“其他”
4. **多主题混合资讯归为其他**：如果标题包含多个不相关的新闻主题，属于资讯汇总类，归为"其他"
5. **不确定性时**：如果无法明确判断，归为"其他"

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

### 📋 大模型打标决策流程

```
文章内容 → 涉及大模型关键词？ → 否 → is_model_related = false
              ↓ 是
         是模型本身的技术？ → 是 → is_model_related = true
              ↓ 否
         是应用层/框架层？ → 是 → is_model_related = false
```

**应打标的情况**（is_model_related = true）：
1. **模型发布**：新模型正式发布、版本更新（如 "GPT-5 发布"、"Claude 3.5 更新"）
2. **模型测评**：性能对比、实测报告、benchmark 结果（如 "GPT vs Claude 对比测试"）
3. **模型架构**：技术论文、架构创新、底层技术研究（如 "MoE 架构优化"、"RLHF 新方法"）

**不应打标的情况**（is_model_related = false）：
- ❌ AI 应用功能（工具集成、行业应用、企业试用）
- ❌ 行业资讯（公司动态、融资新闻、裁员消息）
- ❌ 基础设施讨论（芯片适配、服务器采购、算力建设）
- ❌ 应用类文章（AI CEO、AI 客服、AI 教育等应用场景）
- ❌ 行业活动报道（开发者日、技术大会、会议资讯）
- ❌ 公司榜单评选、社会影响分析
- ❌ **智能体（Agent）相关研究**：除非直接涉及大模型底层架构，否则 Agent 的环境协同、应用进化等通常视为应用层研究，不打标
- ❌ **Agent 框架工程优化**：如 Hermes Agent 的性能优化、启动速度改进等，属于框架层而非模型层

### ⚠️ 边界案例判定指南

**Q1: Agent 框架算大模型相关吗？**
- A: ❌ **不算**。Agent 框架是应用层工具，不是大模型本身。
- 例：Hermes Agent 框架优化 → `false`
- 例：AgentScope 2.0 发布 → `false`

**Q2: 工程优化算大模型相关吗？**
- A: ❌ **不算**。除非优化的是模型本身的训练/推理算法。
- 例：Hermes 启动速度优化（缓存、延迟加载）→ `false`
- 例：模型训练算法改进 → `true`

**Q3: 产品功能更新算大模型相关吗？**
- A: 视情况而定:
  - 底层模型能力升级 → `true`
  - 应用层功能集成 → `false`
  - UI/交互改进 → `false`

**Q4: 学术研究一定算大模型相关吗？**
- A: 不一定。看研究内容:
  - 模型架构/训练方法研究 → `true`
  - Agent 应用/环境研究 → `false`
  - 行业应用研究 → `false`

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

**⚠️ 重要：相同主题文章合并规则**

在构建分类结果后，需要检查是否有多个公众号报道同一事件，如有则进行合并：

**合并条件**：
- 多篇文章报道同一核心事件（如“马斯克解散xAI”、“Anthropic融资”等）
- 标题关键词高度重合或语义相同
- 来自不同公众号但内容相似

**合并操作**：
1. 选择一篇作为主文章（通常是最早发布或最详细的）
2. 创建综合标题和摘要，整合各来源关键信息
3. 保留所有原始文章的链接，作为多源标签
4. 在 `classification.json` 中使用 `merged_articles` 字段记录被合并的文章

**合并示例**：

```python
# 检测到5篇关于“马斯克解散xAI”的报道
merged_article = {
    "aid": "merged_xai_anthropic",
    "title": "马斯克解散xAI，22万张GPU租给Anthropic助力Claude",
    "source": "多源综合",
    "link": "https://mp.weixin.qq.com/s/NsQ1siqUVWZ04bIuB_m9Jg",  # 主文章链接
    "digest": "马斯克官宣解散xAI，将22万张GPU算力全部租给Anthropic用于Claude训练；同时与Cursor合作提供数万GPU，联手对抗OpenAI。Anthropic创始人透露ARR增速达80倍，Claude调用限制全放开、速率拉满。",
    "source_file": "sources/xxx.md",
    "category_reason": "xAI与Anthropic商业合作，属于商业资讯",
    "is_model_related": false,
    "merged_articles": [  # 记录所有被合并的原始文章
        {
            "aid": "2651031726_1",
            "title": "刚刚，马斯克官宣xAI解散，22万张GPU算力租给Anthropic",
            "source": "机器之心",
            "link": "https://mp.weixin.qq.com/s/NsQ1siqUVWZ04bIuB_m9Jg"
        },
        {
            "aid": "2652698173_1",
            "title": "突发，马斯克xAI解散了！22万张GPU忍痛全给Claude",
            "source": "新智元",
            "link": "https://mp.weixin.qq.com/s/L0dQcKVZ45f5MXd7GzJ8kQ"
        },
        # ... 其他被合并的文章
    ]
}

# 从分类列表中移除被合并的原始文章，只保留合并后的条目
```

**合并好处**：
- ✅ 避免信息重复，提升阅读体验
- ✅ 读者可一眼看到核心事件
- ✅ 通过多源标签查看不同媒体的详细报道
- ✅ 前端展示时会在卡片下方显示所有相关公众号标签

**⚠️ 重要：检查并补充 source 字段**

在保存 classification.json 之前，必须检查每篇文章的 `source` 字段是否为空。如果为空，需要根据文章标题或内容推断合适的来源名称。

**常见情况**：
- 腾讯研究院发布的综合资讯 → `source = "腾讯研究院"`
- 阿里云开发者技术文章 → `source = "阿里云开发者"`
- 机器之心转载 → `source = "机器之心"`
- 量子位原创 → `source = "量子位"`

**检查代码示例**：
```python
for category in ['国际', '国内', '同业', '其他']:
    for article in classification[category]:
        if not article.get('source') or article['source'].strip() == '':
            # 根据标题或链接推断来源
            title = article.get('title', '')
            link = article.get('link', '')
            
            if '腾讯研究院' in title or 'tencent' in link:
                article['source'] = '腾讯研究院'
            elif '阿里云' in title or 'aliyun' in link:
                article['source'] = '阿里云开发者'
            elif '机器之心' in link:
                article['source'] = '机器之心'
            else:
                # 默认使用公众号名称或其他标识
                article['source'] = '未知来源'
            
            print(f"⚠️ 已补充 source 字段: {article['title'][:30]}... -> {article['source']}")
```

**为什么重要**：
- ❌ 如果 `source` 为空，前端无法显示公众号标签按钮
- ✅ 用户无法点击跳转到原始文章
- ✅ 影响阅读体验和溯源能力

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

**d) 保存中间结果（可选）**

在完成所有文章的分类和打标后，可以先保存一个中间版本用于验证：

```python
# 保存分类和打标结果（不含合并）
intermediate_result = {
    "date": "YYYY-MM-DD",
    "generated_at": datetime.datetime.now().isoformat(),
    "classification": classification,  # 此时还未合并
    "stats": {
        "国际": len(classification["国际"]),
        "国内": len(classification["国内"]),
        "同业": len(classification["同业"]),
        "其他": len(classification["其他"]),
        "total": sum(len(v) for v in classification.values())
    }
}

with open('daily/YYYY-MM-DD/classification_temp.json', 'w', encoding='utf-8') as f:
    json.dump(intermediate_result, f, ensure_ascii=False, indent=2)

print(f"✅ 第一步完成：国际{len(classification['国际'])}篇, 国内{len(classification['国内'])}篇, "
      f"同业{len(classification['同业'])}篇, 其他{len(classification['其他'])}篇")
```

---

### 🔹 第二步：同主题合并判断

在完成分类和打标后，智能体需要识别报道同一事件的多篇文章并进行合并。

**合并判断标准**：
1. **主体相同**：涉及相同的公司、机构或人物（如 xAI、DeepSeek、翁家翌）
2. **事件类型相同**：都是人事变动、融资新闻、产品发布等
3. **时间窗口相同**：都是当天的报道
4. **语义相似**：标题关键词高度重合或描述同一核心事件

**合并操作流程**：

```python
# 示例：检测到3篇关于"DeepSeek融资"的报道
merged_article = {
    "aid": "merged_deepseek_funding",
    "title": "DeepSeek启动创纪录融资：梁文锋出资200亿，总额500亿估值飙至3500亿",
    "source": "多源综合",
    "link": "https://mp.weixin.qq.com/s/kfhTyxosjbNAKTvx3FI2Wg",  # 主文章链接
    "digest": "整合后的摘要，概括各来源关键信息...",
    "source_file": "",
    "category_reason": "DeepSeek（国内公司）融资新闻，属于非技术内容",
    "is_model_related": false,
    "is_merged": true,  # 标记为合并文章
    "merged_articles": [  # 记录所有被合并的原始文章
        {
            "aid": "2651032137_2",
            "title": "曝DeepSeek融资500亿元：梁文锋自掏四成，估值飙至3500亿",
            "source": "机器之心",
            "link": "https://mp.weixin.qq.com/s/468uA3g9RZCZEepuS_yp4g"
        },
        {
            "aid": "2651283654_1",
            "title": "DeepSeek被曝融资500亿，阿里或无缘参投",
            "source": "InfoQ",
            "link": "https://mp.weixin.qq.com/s/bmiQT8SU8kL-ex4PnqwQrA"
        },
        {
            "aid": "2247889415_1",
            "title": "梁文锋出资200亿！DeepSeek首轮创纪录融资500亿，V4.1定档6月",
            "source": "量子位",
            "link": "https://mp.weixin.qq.com/s/kfhTyxosjbNAKTvx3FI2Wg"
        }
    ]
}

# 从分类列表中移除被合并的原始文章，只保留合并后的条目
```

**常见合并场景**：
- 重大融资事件（多家媒体报道）
- 公司人事变动（离职、加入等）
- 重要产品发布（GPT新版本、新模型等）
- 学术研究突破（同一论文被多家媒体解读）

**注意事项**：
- 合并仅在 `classification.json` 层面进行，Python 脚本负责渲染
- 合并后的文章使用 `is_merged: true` 标记
- `merged_articles` 字段保留所有原始文章的元数据（aid、title、source、link）
- 前端会根据 `source_items` 显示多公众号标签

**最终保存**：

```python
# 保存最终的分类结果（包含合并）
result = {
    "date": "YYYY-MM-DD",
    "generated_at": datetime.datetime.now().isoformat(),
    "classification": classification,  # 此时已包含合并后的文章
    "stats": {
        "国际": len(classification["国际"]),
        "国内": len(classification["国内"]),
        "同业": len(classification["同业"]),
        "其他": len(classification["其他"]),
        "total": sum(len(v) for v in classification.values())
    }
}

with open('daily/YYYY-MM-DD/classification.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✅ 第二步完成：合并后共{result['stats']['total']}个展示卡片")
```

#### ✅ Step 3.5: 分类与合并验证（重要！）

**目标**：在生成 HTML 前，根据 skill 中的分类规则重新验证 classification.json 的准确性

**为什么需要这一步？**
- ✅ 避免分类错误导致的技术内容被归入“其他”
- ✅ 确保非技术内容不会出现在国际/国内/同业分类中
- ✅ 检查公司属地是否正确（如 Anthropic、Google DeepMind、CMU 等应归入国际）
- ✅ 验证开发工具、工程实践、技术路线是否被正确识别为技术内容
- ✅ 检查同主题文章是否正确合并

**验证流程（分两步）**：

---

### 🔹 第一步验证：检查分类和大模型标签

**1. 读取 classification.json**

```python
import json

with open('daily/YYYY-MM-DD/classification.json', 'r') as f:
    data = json.load(f)
    
classification = data['classification']
```

**2. 逐项检查分类准确性**

对每个分类中的文章进行验证：

**a) 检查“国际”分类**

验证点：
- ✅ 是否只包含海外公司/机构的技术内容？
- ❌ 是否有非技术内容（融资、治理、产品动态）？→ 移到“其他”
- ❌ 是否有国内公司内容？→ 移到“国内”

典型错误案例：
- ❌ “Anthropic估值冲爆1.2万亿” → 应归入“其他”（融资新闻）
- ❌ “马斯克解散xAI” → 应归入“其他”（公司重组）
- ✅ “Anthropic发布NLA技术” → 正确（技术研究）
- ✅ “Anthropic技术路线图：无限记忆、多智能体” → 正确（技术路线规划）

**b) 检查“国内”分类**

验证点：
- ✅ 是否只包含国内公司/机构的技术内容？
- ❌ 是否有海外公司内容（Anthropic、Google、CMU等）？→ 移到“国际”
- ❌ 是否有非技术内容？→ 移到“其他”

典型错误案例：
- ❌ “Anthropic NLA技术” → 应归入“国际”（Anthropic是美国公司）
- ❌ “AlphaEvolve（Google DeepMind）” → 应归入“国际”
- ❌ “CVPR论文CMU×哈佛” → 应归入“国际”
- ✅ “阿里QoderWork工程实践” → 正确（国内开发工具）
- ✅ “哈工大华为框架” → 正确（国内合作研究）

**c) 检查“同业”分类**

验证点：
- ✅ 是否只包含银行/金融机构的AI技术应用？
- ❌ 是否有非金融行业内容？→ 移到相应分类

**d) 检查“其他”分类**

验证点：
- ✅ 是否包含所有非技术内容？
- ❌ 是否有技术内容被误归入？→ 移到国际/国内/同业

常见被误归入“其他”的技术内容：
- ❌ 开发工具（OpenAI CLI、灵码、QoderWork）→ 应归入技术分类
- ❌ 工程实践案例 → 应根据公司属地归入国际/国内
- ❌ 技术路线规划 → 应根据公司属地归入国际/国内

**3. 技术内容判定标准回顾**

根据 skill 文档第 213-232 行：

**✅ 技术内容**（可放入国际/国内/同业）：
- 模型发布、版本更新、架构创新
- 算法研究、技术论文、benchmark测评
- **工程实践、开发工具、技术标准** ← 重要！
- **底层技术研究、框架开源**
- **技术路线规划** ← 重要！

**❌ 非技术内容**（必须归入“其他”）：
- 融资新闻、估值报道、收购合并
- 法律纠纷、人事变动、公司动态
- 行业应用案例、产品体验评测
- 培训认证、会议活动、榜单评选
- 基础设施投资、算力建设（纯商业角度）

**4. 大模型打标验证**

检查 `is_model_related` 字段是否准确：

**✅ 应该打标**：
- 模型发布（GPT-5、Claude 3.5等）
- 模型测评（性能对比、benchmark）
- 模型架构（技术论文、架构创新）

**❌ 不应打标**：
- AI应用功能（工具集成、行业应用）
- 行业资讯（公司动态、融资新闻）
- 基础设施讨论（芯片适配、服务器采购）
- 智能体应用研究（除非直接涉及大模型底层架构）

---

### 🔹 1.5步验证：检查 source_file 路径的符号标准化（⚠️ 高频问题！）

**为什么需要这一步？**
- ⚠️ **历史问题**：多次出现文件名中的中文引号与 JSON 转义不匹配导致 404 错误
- ⚠️ **根本原因**：文件系统使用中文标点（""''），但 JSON 中使用了英文引号转义（\"\'）
- ✅ **解决方案**：统一使用 Unicode 转义序列表示所有非ASCII字符

**必须检查的字段**：
- `source_file` - Markdown 原文文件路径
- `title` - 文章标题（可能包含特殊符号）
- `digest` - 摘要内容（可能包含引号）

**常见符号问题**：

| 符号类型 | 文件系统中的实际字符 | JSON 中错误的写法 | JSON 中正确的写法 |
|---------|-------------------|-----------------|-----------------|
| 中文左双引号 | " (U+201C) | `"` 或 `\"` | `\u201c` |
| 中文右双引号 | " (U+201D) | `"` 或 `\"` | `\u201d` |
| 中文左单引号 | ' (U+2018) | `'` 或 `\'` | `\u2018` |
| 中文右单引号 | ' (U+2019) | `'` 或 `\'` | `\u2019` |
| 中文破折号 | — (U+2014) | `—` | `\u2014` |
| 中文省略号 | … (U+2026) | `...` | `\u2026` |
| 中文书名号 | 《》 | `《》` | `\u300a\u300b` |

**检查步骤**：

```python
import json
import os
import re

# 读取 classification.json
with open('daily/YYYY-MM-DD/classification.json', 'r') as f:
    data = json.load(f)

errors = []

# 遍历所有分类
for category in ['国际', '国内', '同业', '其他']:
    for article in data['classification'][category]:
        source_file = article.get('source_file', '')
        
        if not source_file:
            continue
        
        # 1. 检查文件是否存在
        full_path = os.path.join('daily/YYYY-MM-DD', source_file)
        if not os.path.exists(full_path):
            errors.append({
                'article': article['title'][:30],
                'issue': '文件不存在',
                'path': source_file
            })
            continue
        
        # 2. 检查路径中是否包含未转义的中文标点
        # 检测中文引号、书名号等特殊字符
        chinese_punctuation = re.findall(r'[""''《》【】（）]', source_file)
        if chinese_punctuation:
            # 尝试从文件系统获取实际文件名
            actual_files = os.listdir('daily/YYYY-MM-DD/sources/')
            
            # 查找最相似的文件名
            import difflib
            base_name = os.path.basename(source_file)
            matches = difflib.get_close_matches(base_name, actual_files, n=1, cutoff=0.8)
            
            if matches:
                correct_path = 'sources/' + matches[0]
                if correct_path != source_file:
                    errors.append({
                        'article': article['title'][:30],
                        'issue': '路径符号不匹配',
                        'current': source_file,
                        'correct': correct_path,
                        'hint': '需要使用Unicode转义序列'
                    })

# 输出检查结果
if errors:
    print(f"\n⚠️ 发现 {len(errors)} 个路径问题：")
    for err in errors:
        print(f"  - {err['article']}...")
        print(f"    问题: {err['issue']}")
        if 'current' in err:
            print(f"    当前: {err['current']}")
            print(f"    正确: {err['correct']}")
else:
    print("\n✅ 所有 source_file 路径检查通过")
```

**修复方法**：

当发现路径不匹配时，使用 Python 的 `json.dumps()` 自动处理 Unicode 转义：

```python
# 方法1：让 json.dump 自动处理（推荐）
import json

# 读取原始数据
with open('daily/YYYY-MM-DD/classification.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修正 source_file 路径
for category in ['国际', '国内', '同业', '其他']:
    for article in data['classification'][category]:
        if article.get('source_file'):
            # 从文件系统获取实际文件名
            sources_dir = 'daily/YYYY-MM-DD/sources/'
            actual_files = os.listdir(sources_dir)
            
            # 模糊匹配找到正确文件名
            import difflib
            base_name = os.path.basename(article['source_file'])
            matches = difflib.get_close_matches(base_name, actual_files, n=1, cutoff=0.8)
            
            if matches:
                article['source_file'] = 'sources/' + matches[0]

# 保存时使用 ensure_ascii=False 保持可读性，或使用默认设置自动转义
with open('daily/YYYY-MM-DD/classification.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)  # 保持中文可读
    # 或者使用默认设置：json.dump(data, f, indent=2)  # 自动转义所有非ASCII
```

**最佳实践**：

1. **生成 classification.json 时**：
   - 从 `filtered_articles.json` 复制 `source_file` 字段时，直接使用原始值
   - 不要手动修改或转义路径字符串
   - 让 `json.dump()` 自动处理编码

2. **合并文章时**：
   - 合并后的文章 `source_file` 设为空字符串 `""`
   - 因为合并文章没有对应的单个 Markdown 文件

3. **验证时**：
   - 每次生成 classification.json 后，立即运行上述检查脚本
   - 确保所有 `source_file` 指向的文件真实存在
   - 特别注意包含中文标点的文件名

**历史案例**：

- ❌ **2026-05-21 皇马文章**：
  - 错误：`"source_file": "sources/2026-05-21_皇马主席弗洛伦蒂诺居然是\"AI超级大赢家\"！_财联社AI daily.md"`
  - 实际文件：`2026-05-21_皇马主席弗洛伦蒂诺居然是"AI超级大赢家"！_财联社AI daily.md`
  - 修复：使用 Unicode 转义 `\u201c` 和 `\u201d` 表示中文引号

- ❌ **2026-05-20 腾讯马维斯文章**：
  - 错误：路径中使用英文引号 `"`
  - 实际文件：使用中文引号 `""`
  - 修复：generate_html.py 已实现模糊匹配容错

**预防措施**：

在 Step 3 生成 classification.json 时，添加以下检查代码：

```python
# 在保存 classification.json 之前
import os

print("\n🔍 验证 source_file 路径...")
for category in ['国际', '国内', '同业', '其他']:
    for article in classification[category]:
        source_file = article.get('source_file', '')
        if source_file:
            full_path = os.path.join('daily/YYYY-MM-DD', source_file)
            if not os.path.exists(full_path):
                print(f"⚠️ 文件不存在: {article['title'][:40]}...")
                print(f"   路径: {source_file}")
                # 尝试模糊匹配修正
                import difflib
                base_name = os.path.basename(source_file)
                actual_files = os.listdir('daily/YYYY-MM-DD/sources/')
                matches = difflib.get_close_matches(base_name, actual_files, n=1, cutoff=0.8)
                if matches:
                    article['source_file'] = 'sources/' + matches[0]
                    print(f"   ✅ 已修正为: {article['source_file']}")
```

---

### 🔹 第二步验证：检查合并逻辑

在完成分类和打标后，智能体需要识别报道同一事件的多篇文章并进行合并。

**合并判断标准**：
1. **主体相同**：涉及相同的公司、机构或人物（如 xAI、DeepSeek、翁家翌）
2. **事件类型相同**：都是人事变动、融资新闻、产品发布等
3. **时间窗口相同**：都是当天的报道
4. **语义相似**：标题关键词高度重合或描述同一核心事件

**合并操作流程**：

```python
# 示例：检测到3篇关于"DeepSeek融资"的报道
merged_article = {
    "aid": "merged_deepseek_funding",
    "title": "DeepSeek启动创纪录融资：梁文锋出资200亿，总额500亿估值飙至3500亿",
    "source": "多源综合",
    "link": "https://mp.weixin.qq.com/s/kfhTyxosjbNAKTvx3FI2Wg",  # 主文章链接
    "digest": "整合后的摘要，概括各来源关键信息...",
    "source_file": "",
    "category_reason": "DeepSeek（国内公司）融资新闻，属于非技术内容",
    "is_model_related": false,
    "is_merged": true,  # 标记为合并文章
    "merged_articles": [  # 记录所有被合并的原始文章
        {
            "aid": "2651032137_2",
            "title": "曝DeepSeek融资500亿元：梁文锋自掏四成，估值飙至3500亿",
            "source": "机器之心",
            "link": "https://mp.weixin.qq.com/s/468uA3g9RZCZEepuS_yp4g"
        },
        {
            "aid": "2651283654_1",
            "title": "DeepSeek被曝融资500亿，阿里或无缘参投",
            "source": "InfoQ",
            "link": "https://mp.weixin.qq.com/s/bmiQT8SU8kL-ex4PnqwQrA"
        },
        {
            "aid": "2247889415_1",
            "title": "梁文锋出资200亿！DeepSeek首轮创纪录融资500亿，V4.1定档6月",
            "source": "量子位",
            "link": "https://mp.weixin.qq.com/s/kfhTyxosjbNAKTvx3FI2Wg"
        }
    ]
}

# 从分类列表中移除被合并的原始文章，只保留合并后的条目
```

**常见合并场景**：
- 重大融资事件（多家媒体报道）
- 公司人事变动（离职、加入等）
- 重要产品发布（GPT新版本、新模型等）
- 学术研究突破（同一论文被多家媒体解读）

**注意事项**：
- 合并仅在 `classification.json` 层面进行，Python 脚本负责渲染
- 合并后的文章使用 `is_merged: true` 标记
- `merged_articles` 字段保留所有原始文章的元数据（aid、title、source、link）
- 前端会根据 `source_items` 显示多公众号标签

**最终保存**：

```python
# 保存最终的分类结果（包含合并）
result = {
    "date": "YYYY-MM-DD",
    "generated_at": datetime.datetime.now().isoformat(),
    "classification": classification,  # 此时已包含合并后的文章
    "stats": {
        "国际": len(classification["国际"]),
        "国内": len(classification["国内"]),
        "同业": len(classification["同业"]),
        "其他": len(classification["其他"]),
        "total": sum(len(v) for v in classification.values())
    }
}

with open('daily/YYYY-MM-DD/classification.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✅ 第二步完成：合并后共{result['stats']['total']}个展示卡片")
```

---

## ⚠️⚠️⚠️ 强制验证要求（不可跳过！）⚠️⚠️⚠️

**【重要提醒】** 在完成 Step 3（分类与合并）后，**AI 助手必须执行完整的分类验证**，确认无误后才能进入 Step 4（生成 HTML）。

### 📋 强制验证清单

AI 助手必须逐项检查以下内容（使用 ✅/❌ 标记）：

#### ✅ 1. 技术内容判定（最重要！）

**检查国际/国内/同业分类中的每篇文章**：
- [ ] 是否为真正的技术内容？（模型发布、算法研究、工程实践、开发工具、技术路线）
- [ ] 是否混入了非技术内容？（人事变动、产品营销、会议活动、行业资讯、企业战略）
- [ ] 如有非技术内容，立即移到"其他"分类

**典型错误案例**：
- ❌ "Anthropic招聘文科生" → 应归入"其他"（人事变动）
- ❌ "Qoder表情包上线" → 应归入"其他"（产品营销）
- ❌ "智源大会预告" → 应归入"其他"（会议活动）
- ❌ "AI就业数据分析" → 应归入"其他"（行业资讯）
- ❌ "OpenAI总裁辞职" → 应归入"其他"（人事变动）
- ✅ "面壁智能开源BitCPM-CANN" → 正确（技术研究）
- ✅ "腾讯AI Infra实践" → 正确（工程实践）

#### ✅ 2. 公司属地判定

**检查国际/国内分类的公司归属**：
- [ ] 国际分类是否都是海外公司/项目？（OpenAI、Anthropic、Google、Meta等）
- [ ] 国内分类是否都是国内公司/项目？（阿里、腾讯、华为、字节等）
- [ ] **关键原则**：看项目/作者归属，不看报道语言
  - 例：Hermes Agent（NousResearch）→ 国际
  - 例：龙虾之父Peter的Skill优化 → 国际
- [ ] 是否有公司属地错误？立即修正

#### ✅ 3. 大模型打标准确性

**检查 `is_model_related` 字段**：
- [ ] 模型发布/测评/架构研究 → 应该打标 `true`
- [ ] AI应用/行业资讯/公司动态 → 应该打标 `false`
- [ ] **Agent框架/工程优化** → 应该打标 `false`（不是大模型本身）
- [ ] 智能体应用研究（非底层架构）→ 应该打标 `false`

**常见错误**：
- ❌ Hermes Agent框架优化 → 误标为 `true` → 应为 `false`
- ❌ AgentScope发布 → 误标为 `true` → 应为 `false`

#### ✅ 4. source_file 路径验证

**运行验证脚本**：
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
python3 -c "
import json, os
with open('daily/YYYY-MM-DD/classification.json', 'r') as f:
    data = json.load(f)
errors = []
for category in ['国际', '国内', '同业', '其他']:
    for article in data['classification'][category]:
        if article.get('source_file'):
            full_path = os.path.join('daily/YYYY-MM-DD', article['source_file'])
            if not os.path.exists(full_path):
                errors.append(f'{category}: {article[\"title\"][:40]}...')
if errors:
    print('❌ 发现文件路径错误:')
    for error in errors:
        print(f'  {error}')
else:
    print('✅ 所有文件路径正确!')
"
```

- [ ] 所有 source_file 指向的文件是否存在？
- [ ] 中文标点是否正确使用 Unicode 转义？（\u201c, \u201d 等）
- [ ] 如有错误，立即修正路径

#### ✅ 5. source 字段完整性

**检查每篇文章的 source 字段**：
- [ ] 是否有空值的 source 字段？
- [ ] 综合资讯类是否标注了来源公众号？
- [ ] 如有空值，根据标题或链接推断并补充

#### ✅ 6. 统计信息一致性

**检查 stats 字段**：
- [ ] 各分类文章数之和是否等于 total？
- [ ] 是否与实际情况一致？

```bash
# 快速验证命令
python3 -c "
import json
data = json.load(open('daily/YYYY-MM-DD/classification.json'))
total_calc = sum(len(data['classification'][c]) for c in ['国际', '国内', '同业', '其他'])
if total_calc != data['stats']['total']:
    print(f'❌ 统计不一致: 计算={total_calc}, stats={data[\"stats\"][\"total\"]}')
else:
    print(f'✅ 统计一致: {data[\"stats\"]}')
"
```

### 🚨 验证失败处理流程

如果验证发现任何错误：

1. **立即停止**，不要进入 Step 4
2. **修正错误**：根据验证结果修改 classification.json
3. **重新验证**：再次运行验证脚本
4. **循环执行**：直到验证完全通过（无任何错误）
5. **确认通过**：看到 "✅ 所有文件路径正确!" 和其他验证项都通过后，才能继续

### ⚡ 快速验证命令

复制以下命令，替换 `YYYY-MM-DD` 为实际日期后执行：

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank && python3 -c "
import json, os
with open('daily/YYYY-MM-DD/classification.json', 'r') as f:
    data = json.load(f)
print('=== 分类验证报告 ===\n')
errors = []
for category in ['国际', '国内', '同业', '其他']:
    for article in data['classification'][category]:
        if not article.get('source') or article['source'].strip() == '':
            errors.append(f'{category}: source为空 - {article[\"title\"][:30]}')
        if article.get('source_file'):
            full_path = os.path.join('daily/YYYY-MM-DD', article['source_file'])
            if not os.path.exists(full_path):
                errors.append(f'{category}: 文件不存在 - {article[\"title\"][:30]}')
total_calc = sum(len(data['classification'][c]) for c in ['国际', '国内', '同业', '其他'])
if total_calc != data['stats']['total']:
    errors.append(f'统计不一致: 计算={total_calc}, stats={data[\"stats\"][\"total\"]}')
if errors:
    print(f'❌ 发现 {len(errors)} 个错误:')
    for e in errors: print(f'  {e}')
else:
    print('✅ 验证通过！可以进入 Step 4')
print(f'\n📊 统计: 国际{data[\"stats\"][\"国际\"]} 国内{data[\"stats\"][\"国内\"]} 同业{data[\"stats\"][\"同业\"]} 其他{data[\"stats\"][\"其他\"]} 总计{data[\"stats\"][\"total\"]}')
"
```

**【警告】跳过验证步骤将导致HTML页面出现错误（404链接、分类混乱等），影响用户体验！**
            full_path = os.path.join('daily', date, source_file)
            if not os.path.exists(full_path):
                print(f"  ⚠️ 文件不存在: {source_file}")
                print(f"     文章: {article['title'][:40]}...")
                # 尝试模糊匹配
                sources_dir = os.path.join('daily', date, 'sources')
                if os.path.exists(sources_dir):
                    actual_files = os.listdir(sources_dir)
                    import difflib
                    base_name = os.path.basename(source_file)
                    matches = difflib.get_close_matches(base_name, actual_files, n=1, cutoff=0.7)
                    if matches:
                        print(f"     建议: sources/{matches[0]}")
                        article['source_file'] = 'sources/' + matches[0]
                        print(f"     ✅ 已修正")

print("✅ 路径验证完成\n")
```

---

### 🔹 第二步验证：检查合并逻辑

**1. 检查是否有遗漏的合并机会**

遍历所有分类，查找可能未合并的同主题文章：

```python
# 示例：检查是否有相同事件的多篇报道
for category in ['国际', '国内', '同业', '其他']:
    articles = classification[category]
    # 提取标题关键词，查找相似事件
    for i, article in enumerate(articles):
        if article.get('is_merged'):
            print(f"✅ {category} - 已合并: {article['title'][:40]}...")
            print(f"   来源数: {len(article.get('merged_articles', []))}")
```

**2. 检查合并是否正确**

验证点：
- ✅ 合并后的文章是否有 `is_merged: true` 标记？
- ✅ `merged_articles` 字段是否包含所有原始文章？
- ✅ 合并后的标题是否准确概括了核心事件？
- ✅ 合并后的摘要是否整合了各来源的关键信息？
- ✅ 被合并的原始文章是否已从分类列表中移除？

**3. 常见合并场景检查清单**

| 场景 | 检查方法 | 预期结果 |
|------|---------|----------|
| 重大融资事件 | 搜索“融资”、“估值”关键词 | 同一事件的多个报道应合并 |
| 人事变动 | 搜索“离职”、“加入”、“任命” | 同一人物的多篇报道应合并 |
| 产品发布 | 搜索“发布”、“推出”、“上线” | 同一产品的多篇报道应合并 |
| 学术研究 | 搜索论文标题、作者名 | 同一研究的多篇解读应合并 |

**4. 修正合并错误**

如果发现遗漏或错误的合并，手动调整 classification.json：

```python
# 示例：将两篇关于“DeepSeek融资”的文章合并
# 1. 找到这两篇文章
article1 = None
article2 = None
for article in classification['其他']:
    if 'DeepSeek' in article['title'] and '融资' in article['title']:
        if not article1:
            article1 = article
        else:
            article2 = article
            break

# 2. 创建合并后的文章
if article1 and article2:
    merged = {
        "aid": "merged_deepseek_funding",
        "title": "DeepSeek启动创纪录融资：梁文锋出资200亿，总额500亿估值飙至3500亿",
        "source": "多源综合",
        "link": article1['link'],
        "digest": "整合后的摘要...",
        "source_file": "",
        "category_reason": "DeepSeek（国内公司）融资新闻，属于非技术内容",
        "is_model_related": False,
        "is_merged": True,
        "merged_articles": [
            {
                "aid": article1['aid'],
                "title": article1['title'],
                "source": article1['source'],
                "link": article1['link']
            },
            {
                "aid": article2['aid'],
                "title": article2['title'],
                "source": article2['source'],
                "link": article2['link']
            }
        ]
    }
    
    # 3. 从分类列表中移除原始文章，添加合并后的文章
    classification['其他'].remove(article1)
    classification['其他'].remove(article2)
    classification['其他'].append(merged)
    
    # 4. 更新统计
    data['stats']['其他'] = len(classification['其他'])
    data['stats']['total'] = sum(len(v) for v in classification.values())
    
    # 5. 保存修正后的结果
    with open('daily/YYYY-MM-DD/classification.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 合并修正完成")
```

---

### 🔹 最终验证

**1. 总数一致性检查**

```bash
# 检查总数是否正确
python3 -c "
import json
data = json.load(open('daily/YYYY-MM-DD/classification.json'))
total = sum(len(v) for v in data['classification'].values())
print(f'总文章数: {total}')
print(f'统计值: {data[\"stats\"][\"total\"]}')
assert total == data['stats']['total'], '总数不匹配！'
print('✅ 验证通过')
"
```

**2. 验证清单**

| 检查项 | 命令/方法 | 预期结果 |
|--------|----------|----------|
| 国际分类纯度 | 人工检查每篇文章 | 仅含海外技术内容 |
| 国内分类纯度 | 人工检查每篇文章 | 仅含国内技术内容 |
| 其他分类完整性 | 检查是否有技术内容遗漏 | 仅含非技术内容 |
| 总数一致性 | `python3 -c "..."` | 总数 = 国际+国内+同业+其他 |
| 大模型打标 | 抽查打标文章 | 仅模型相关技术打标 |
| 合并完整性 | 检查同主题文章 | 相同事件已合并 |
| 合并标记 | 检查 is_merged 字段 | 合并文章有正确标记 |

**3. 如果发现问题**

- **分类错误**：手动移动文章到正确的分类
- **标签错误**：修改 `is_model_related` 字段
- **合并不当**：手动合并或拆分文章组
- 每次修改后重新保存 classification.json

---

### Step 4: 生成 HTML

**目标**：将分类结果渲染为响应式 HTML 页面

**命令**：
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 generate_html.py YYYY-MM-DD
```

**工作流程**：
1. 读取 `classification.json` 获取分类和摘要数据（包含合并信息）
2. **优先使用 classification.json 中的 `is_model_related` 标签**（不会重新检测）
3. 读取 `sources/*.md` 获取文章原文（用于 viewer.html 查看完整内容）
4. 基于 `template.html` 模板渲染页面
5. 生成 `daily/YYYY-MM-DD/index.html`
6. 更新 `daily-index.json` 索引文件，追加新日期条目

**重要说明**：
- ✅ `generate_html.py` 会**优先使用** classification.json 中的人工标注标签
- ✅ 每个分类板块内，有大模型标签的文章会**自动排在最上方**
- ✅ 支持合并文章的展示：显示多公众号标签，点击可跳转到对应来源
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

# 4. 智能分类与合并（由 AI 智能体完成）
# 分两步执行：
#   第一步：分类与大模型打标
#   第二步：同主题合并判断
# 读取 filtered_articles.json，生成 classification.json

# 5. 分类与合并验证（重要！）
# 分两步验证：
#   第一步：检查分类和大模型标签
#   第二步：检查合并逻辑
# 根据 skill 中的分类规则重新验证 classification.json 的准确性
# 检查点：
# - 国际/国内/同业是否只包含技术内容？
# - 非技术内容是否都归入“其他”？
# - 开发工具、工程实践、技术路线是否被正确识别为技术内容？
# - 公司属地是否正确（Anthropic/Google/CMU等应归入国际）？
# - 大模型打标是否准确？
# - 同主题文章是否正确合并？
# - 合并标记和 merged_articles 字段是否正确？

# 6. 生成 HTML
python3 generate_html.py $TARGET_DATE

# 7. 验证
ls -lh ../daily/$TARGET_DATE/index.html
open ../daily/$TARGET_DATE/index.html

# 8. 推送（可选）
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
