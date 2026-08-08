---
name: ai-daily-for-bank
description: >
  生成每日 AI 智能研发早报。从多个来源(自建RSSHub、官网RSS、手动投稿)获取文章,
  按关键词过滤,智能分类(国际/国内/同业/其他)并生成~300字摘要,
  渲染为响应式静态 HTML 页面。支持增量处理(已确认文章不重复消耗token)。
  使用场景:当用户要求生成今日/昨日AI早报、获取AI文章汇总、
  生成智能研发日报时触发。触发词:早报、日报、AI daily、每日汇总。
license: MIT
metadata:
  version: "3.3"
  category: productivity
  updated: "2026-08-05"
  changelog: |
    v3.3 (2026-08-05):
    - 新增:铁规6 标题中文化(所有英文标题必须翻译为中文)
    - 改变:摘要从~300字精简为~300字中文
    - 改变:其他分类不做非技术自动判定(范式/工程实践内容可能在其中,由人工审核上调)
    v3.2 (2026-08-03):
    - 新增:build_classification.py 自动匹配 is_merged 从条到主条(关键词重叠算法)
    - 新增:classification.json 每篇文章自动生成 source_items 数组
    - 新增:generate_html.py 来源标签优先链接真实原文URL(回退到 viewer.html)
    - 新增:合并主条渲染多来源标签(如 36氪+智东西),各标签独立点击跳转原文
    - 改变:移除独立「查看原文」按钮(来源标签已可点击)
    - 改变:template.html JS 渲染改用 source_items 数组(支持任意数量来源)
    - 改变:Git 推送策略 - HTTPS 和 SSH 均可能超时,优先 HTTPS,失败则切换 SSH
    v3.1 (2026-08-02):
    - 新增:generate_html.py Step 8 自动同步根 index.html INLINE_DAILY_INDEX
    - 新增:daily-index.json 插入后自动按日期降序排列
    - 新增:Step 5 索引数量检查(stats 为空 bug 教训)
    - 新增:Step 6 git add 补充 search-index.json + index.html
    - 改变:Git remote 从 SSH 切换为 HTTPS(端口22超时教训)
    v3.0 (2026-08-02):
    - 重构:信源架构升级为自建RSSHub + 官网RSS统一接入(废弃微信公众号通道)
    - 新增:InfoQ、快手技术信源(via RSSHub)
    - 新增:增量处理机制(front matter status: pending/confirmed,已确认不重跑)
    - 新增:build_classification.py 从 front matter 自动聚合 classification.json
    - 新增:手动投稿支持微信短链直接抓取(fetch_wechat_page)
    - 改变:摘要升级为~300字中文多段落,存入 source md front matter
    - 改变:HTML展示改为"AI摘要 + 查看原文↗",不再嵌入全文(132KB→37KB)
    - 废弃:fetch_articles.py 微信原始通道、decemberpei公众号RSS、kr36_api适配器
    v2.4 (2026-07-16):
    - 新增:铁规 5 补充 spawn 完成后必查 JSON mtime(静默空跑 R2 教训)
    - 新增:Step 4 R2 合并检查拆为独立子项
    - 新增:Step 5 HTML 生成后抽样 3 篇摘要 ≠ 标题
    v2.3 (2026-07-12):
    - 新增:铁规 5 3 轮 fork 验证不可省略
    v2.2 (2026-07-10):
    - 新增:铁规 4 合并从条渲染铁规
    v2.1 (2026-07-03):
    - 新增:Step 6 部署权限检查、Step 3 强合并检查清单
    v2.0 (2026-07-03):
    - 重构:1533行→800行(-48%),新增铁规章节
---

# AI Daily Report Skill

生成每日 AI 智能研发早报。从自建RSSHub、官网RSS、手动投稿等多源获取文章,按关键词过滤后由智能体分类并生成~300字摘要,最终渲染为响应式静态 HTML 页面。支持增量处理,已确认文章不重复消耗token。

---

## 🚨 铁规(最高优先级,先看再动)

### 铁规 1:项目根目录(2026-07-03 老板新增)

**项目根目录(全程唯一)**:
```
/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/
```

- ✅ 所有 cd、脚本执行、文件读写、git 操作**必须**在此目录下进行
- ❌ 严禁在 `/Users/zhengk/GitProjects/agent-docs/` 仓库根目录或 workspace 其他位置误操作
- ⚠️ 这是个**独立的 git 仓库**,与父目录 `agent-docs` 是不同 git 树
- 进入项目后第一件事:`pwd` 确认当前位置

### 铁规 2:严禁 force push 和 reset(2026-07-03 老板新增)

**Git 操作硬性约束**:
- 🚫 **严禁 `git push --force` / `git push -f` / `--force-with-lease`** 等任何 force 变体:会覆盖远程历史,造成数据丢失
- 🚫 **严禁 `git reset --hard`**:会丢弃未提交的工作
- 🚫 **严禁 `git reset --mixed HEAD~` 回滚提交**:会变成"假汇报"--已推 commit 被偷偷回滚

**遇到 push 冲突时,正确做法**:
1. ✅ `git fetch origin` 拉取最新
2. ✅ `git pull --rebase origin master`(用 rebase 整理本地提交,**禁止 force**)
3. ✅ 若 rebase 失败:`git rebase --abort` 放弃
4. ✅ 若需要覆盖远程:**停下来,先告知老板,等明确批准**

**遇到"误操作"时**:
- ❌ 不要试图用 `git reset` 抹掉错误 commit
- ✅ 追加修复 commit 说明问题(`fix: 回滚 XXX 误操作`)

### 铁规 3:铁规违反后的汇报规范

- 发现违反铁规的操作要执行前,**先停下报告老板**,等批准
- 已经误执行了,要**主动报告**,不要隐瞒或事后回滚

### 铁规 4:合并从条渲染铁规(2026-07-10, v3.2 更新)

**问题**:合并组中从条(`is_merged=true`)如果只作为独立文章 append,会与主条重复显示

**v3.2 机制变更**:`build_classification.py` 自动处理合并--
1. 扫描所有文章,找到 `is_merged=true` 从条
2. 通过标题关键词重叠算法匹配到同主题主条
3. 将从条(name + link)追加到主条的 `source_items` 数组
4. `generate_html.py` 跳过从条渲染,主条卡片渲染多来源标签(每标签可点击跳转对应原文)

**铁规**:
- ✅ 主条:**正常渲染**,`source_items` 数组渲染为多来源标签
- ✅ 从条(`is_merged=true`):**不渲染**--其内容已合并入主条的 `source_items`
- ❌ 不允许从条作为独立文章显示(会与主条重复)

**generate_html.py 实现点**(`build_articles_json`):
```python
# v3.2: 跳过合并从条(已并入主条 source_items)
if item.get('is_merged') is True:
    stats['skipped_merged'] += 1
    continue
```

**验证标准**:
- 输出日志必须有 `跳过从条: N`(N = 从条数)
- 主条卡片的 source-tag 链接指向真实原文 URL(优先),回退到 viewer.html
- 渲染卡片数 = 总文章数 - 从条数(不重复不遗漏)

### 铁规 6:标题中文化(2026-08-05 老板新增)

**规则**:所有英文标题必须翻译为中文,HTML 中不得出现英文标题。

**适用范围**:`classification.json` 中 `title` 字段为纯英文或含英文的标题

**执行时机**:Step 3 分类完成后,主 Agent 逐篇检查,英文标题→翻译为中文→写回 `classification.json`

**示例**:
- ❌ `Cogent VR-1: A 3D Object Hallucination Benchmark` → ✅ `3D物体幻觉评测基准 Cogent VR-1`
- ❌ `Circles: A Self-Organizing Multi-Agent System` → ✅ `自组织多智能体系统 Circles`
- ❌ `Hermes Agent 3.0 Released with Self-Improvement` → ✅ `自我改进型智能体 Hermes 3.0 发布`
- ❌ `GPT-Live Real-Time Voice API Now Available` → ✅ `GPT-Live 实时语音 API 上线`

**要点**:
- 保留核心产品/项目名(如 Cogent VR-1、Circles、Hermes、GPT-Live)
- 正文描述部分翻译为中文
- 翻译后标题需保持语义准确,不能丢失关键信息

**验证方式**:Step 4 第 3 轮增加检查项 13:所有 title 字段不含全英文(允许含英文专有名词)

### 铁规 5:3 轮 fork 验证不可省略(2026-07-12 老板新增)

**问题**:主 Agent 分类自查后,直接跳到 Step 5 生成 HTML--**违反了 Step 4 的 3 轮 fork 验证强制要求**。本次自查漏判 6 处错误(1 漏删 + 1 国际国内互换 + 1 产业调其他 + 3 模型打标),幸被老板发现,补做 3 轮 fork 才纠正。

**铁规**:
- ✅ Step 4 的 3 轮 fork 验证**不可省略、不可由主 Agent 自查替代**
- ✅ 即使主 Agent 自我感觉"分类很合理",仍必须 spawn 子智能体独立 session 复核
- ✅ 每轮 5/5 检查项全部通过,才进入下一轮
- ❌ **绝对禁止**主 Agent 跳到 Step 5 直接生成 HTML
- ❌ **绝对禁止**"赶时间"省略 3 轮验证

**自查 ≠ 验证**:程序员测自己的代码 = 认知盲区无法消除。子智能体独立 session 才有意义。

**spawn 完成后必查 JSON mtime**(2026-07-16 静默空跑教训):
- 子智能体存在两种失败模式:
  - **模式 A(活跃错误)**:做错但修改了 JSON(7-12 6 处错误),通过 diff 检出
  - **模式 B(静默失败)**:跑了但未修改 JSON(7-15 R2 空跑 5 分钟仅输出半句话)
- **每轮 spawn 完成后必须立即检查 `classification.json` 的修改时间**:
  ```bash
  python3 -c "import os,time; t=os.path.getmtime('daily/YYYY-MM-DD/classification.json'); print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t)))"
  ```
- mtime 未变 = 子智能体未产出 → 该轮视为 ❌ 不过 → **主 Agent 直接接管该轮检查**
- mtime 已变 → 做 diff 比对修改内容 → 按正常流程通过/重来

**本次教训量化**(7-12 + 7-15 早报):
- 主 Agent 一次性分类:看似零错误
- 7-12 子智能体 3 轮 fork:发现 6 处错误(1 + 4 + 0)(模式 A)
- 7-15 R2:静默空跑,mtime 未变 → 主 Agent 接管 5 项修正(模式 B)
- 修正耗时:6 分钟(子智能体 2-3 分钟 × 3 轮)
- 节省后续返工:老板指出前已推送 6 处错误,影响行业认知

---

## 📅 日期规则

**默认行为**:用户说"生成早报"时,**默认生成昨天的早报**

```bash
# macOS
date -v-1d +%Y-%m-%d
# Linux
date -d "yesterday" +%Y-%m-%d
```

**例外**:用户明确指定日期(如"生成 2026-05-01 的早报")→ 使用用户指定的日期

---

## 📋 工作流程(7 步骤)

```
Step 1  获取文章    → articles_raw.json + sources/*.md
Step 2  关键词过滤  → filtered_articles.json
Step 3  智能分类合并 → classification.json(LLM 主导)
Step 4  三轮验证    → fork 子智能体逐轮检查
Step 5  生成 HTML   → daily/YYYY-MM-DD/index.html
Step 6  验证与推送  → git add/commit/push(严禁 force)
Step 7  反思与优化  → 写反思 / 改 skill
```

---

## Step 1: 获取文章(多源统一接入)

**命令**:
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 fetch_web_articles.py [YYYY-MM-DD]  # 不传参数则用昨天
```

**信源架构(v3.0 重构)**:

所有信源统一输出标准 RSS,经工厂模式适配器转换为统一文章结构:

| 信源 | 类型 | 接入方式 | 内容特点 |
|------|------|----------|----------|
| 36氪 | RSSHub | `torandom.com/rsshub/36kr/information/web_news` | 全文在feed(5000-8000字) |
| InfoQ | RSSHub | `torandom.com/rsshub/infoq/topic/AI` | 全文在feed(7000-11000字) |
| 美团技术 | RSSHub | `torandom.com/rsshub/meituan/tech` | feed无正文,需爬原文 |
| 快手技术 | RSSHub | `torandom.com/rsshub/csdn/blog/kuaishoutech` | 全文在feed,低频源 |
| 极客公园 | 官网RSS | `geekpark.net/rss` | 全文在feed |
| 量子位 | 官网RSS | `qbitai.com/feed` | 需爬原文 |
| Solidot | 官网RSS | `solidot.org/index.rss` | 全文在feed |
| OpenAI | 官网RSS | `openai.com/news/rss.xml` | 需爬原文 |
| DeepMind | 官网RSS | `deepmind.google/blog/rss.xml` | 需爬原文 |
| TLDR AI | 官网RSS | `tldr.tech/api/rss/ai` | 全文在feed |
| MarkTechPost | 官网RSS | `marktechpost.com/feed/` | 全文在feed |
| 手动投稿 | 微信短链 | `manual_links.json` | 直接抓取mp.weixin.qq.com |

**配置文件**:`config/sources.json`(统一sources数组 + 工厂模式适配器)

**输出**:
- `daily/YYYY-MM-DD/sources/*.md` - 每篇文章 Markdown(带 front matter,`status: pending`)
- `daily/YYYY-MM-DD/articles_raw.json` - 文章元数据汇总

**增量保护**:已存在且 `status: confirmed` 的文件不会被覆盖(保护AI已处理的结果)

**手动投稿**:
```bash
python3 add_manual_link.py "https://mp.weixin.qq.com/s/xxx" "来源名称"
```
链接存入 `manual_links.json`,下次执行 fetch 时自动抓取微信页面全文。

**wechat-to-wiki 集成(v3.2 新增)**:
用户每天手工发的公众号文章(经 wechat-to-wiki skill 处理入库时),同步写入对应日期的 `sources/` 目录:
- 按**文章发布日期**(`publish_time`)归入 `daily/{文章日期}/sources/`
- 写入标准 front matter(`status: pending`),由早报流程 Step 3 自动分类
- 该日期早报已生成时→提示用户是否重建;未生成→静默纳入下次生成
- 详见 wechat-to-wiki skill 的 Step 8

**RSSHub 运维**(详见 `RSSHUB-DEPLOY.md`):
- 地址:`https://www.torandom.com/rsshub/<路由>`
- 服务器:阿里云 115.29.206.55,Docker + Redis 缓存
- 首次请求较慢(冷启动),缓存后 <1s

---

## Step 2: 关键词过滤

**命令**:
```bash
python3 filter_articles.py YYYY-MM-DD
```

**逻辑**:
- 读 `config.json` 的 `keywords.include` 列表
- 匹配标题 + digest,不区分大小写
- 不匹配的文章从 `sources/` 删除

**默认关键词**:`["AI", "大模型", "智能体", "skill"]`

**修改**:编辑项目根目录 `config.json`,立即生效

---

## Step 3: 智能分类与摘要(增量处理,LLM 主导)

**目标**:对 `sources/*.md` 中 `status: pending` 的文章分类、打标、生成摘要,写回 front matter

**核心原则(v3.0 新增)**:
- 分类和摘要结果写回每篇文章的 Markdown front matter
- 已确认的文章(`status: confirmed`)直接跳过,不消耗token
- classification.json 由 `build_classification.py` 自动从 front matter 派生,不再手写

**增量处理流程**:
1. 扫描 `daily/YYYY-MM-DD/sources/*.md`,找出 `status: pending` 的文章
2. 对每篇 pending 文章:读取原文 → 判断分类 → 生成~300字摘要 → 写回 front matter
3. 运行 `python3 build_classification.py YYYY-MM-DD` 聚合生成 classification.json

**写回 front matter 格式**:
```markdown
---
publish_time: 1785548482
status: confirmed
category: 国内
is_model_related: false
digest: |
  AI正在重塑大厂的管理层级。字节跳动率先更新领导力原则...

  未来中层需要转型为AI增强型领导者...
---
```

### 3.1 删除规则(7 类,直接删除不归入任何分类)

匹配任一 → 🗑️ 删除,记录到 `classification.json` 的 `excluded` 字段

| 类型 | 关键词 | 示例 |
|------|--------|------|
| 活动宣传 | 专场、创享日、峰会、年会、培训、邀你、共赴、落地、XX站 | "阿里云AI创享日Qoder专场·重庆站" |
| 招聘 | 招、招聘、求职、候选人 | "量子位招小红书AI冲浪选手" |
| 人事变动 | 入职、离职、裁员、转投、富豪榜、荣誉博士、薪酬、身家 | "苏炜杰入职OpenAI"、"Anthropic七子进富豪榜" |
| 财务/IPO | IPO、上市、估值、筹资、股价、市值、营收、ARR、资源包上线 | "SpaceX启动IPO路演"、"Qoder CN资源包上线" |
| 纯商业营销 | 抢购、限时、购买、促销 | "Qoder CN资源包限时优惠" |
| 低空/无关AI融资 | (语义判断) | "金融活水润低空,中银金租助腾飞" |
| 招投标/采购 | 建设项目、招标、中标、采购项目、选型采购、入围 | "河北农信智能信贷风控建设项目" |

### 3.2 分类决策(三步判断法)

```
文章 → 是技术内容? ─否→ 归"其他"(除非触发删除规则)
         ↓ 是
       主体是银行/金融机构? ─是→ "同业"
         ↓ 否
       主体是国内公司/机构? ─是→ "国内"
         ↓ 否
       → "国际"
```

**技术内容判定**(可入国际/国内/同业):
- 模型发布/版本更新/架构创新
- 算法研究、技术论文、benchmark 测评
- 工程实践、开发工具、技术标准
- 框架开源、底层技术研究
- **产品功能更新**(Qoder Browser Use、Buddy 迭代)
- **工具设计/工程实践**(Skill 工程化、LLM Wiki 知识管理)

**非技术内容判定**(归"其他"或删除):
- 融资/估值/收购/法律纠纷 → 🗑️ 删除或归"其他"
- 人事变动/公司动态 → 🗑️ 删除
- 行业应用案例/产品体验 → "其他"
- 培训认证/会议活动/榜单评选 → 🗑️ 删除
- 基础设施投资/算力建设(纯商业角度) → "其他"
- 纯商业资讯(财报/营收/资本支出/ARR) → 🗑️ 删除
- 招聘类内容 → 🗑️ 删除

**主体归属判断要点**:
- **看项目/作者归属,不看报道语言**
  - Hermes Agent(NousResearch)→ 国际开源项目 → "国际"
  - 中文媒体报道国外技术 → 仍按技术归属
- **公司名 > 机构名**(v1.5 新增):标题同时含国际公司(如英伟达)和国内机构(如清华),看核心研究主体
  - "英伟达清华团队γ-World" → 英伟达是主体 → "国际"
  - "阿里达摩院与MIT合作" → 阿里是主体 → "国内"

**特殊情况**:
| 情况 | 处理 |
|------|------|
| 同业优先 | 同时涉及同业和其他 → 优先"同业" |
| 多主题混合 | 标题含多个不相关新闻 → "其他" |
| 主体与场景区分 | OpenAI 总裁辞职 → "其他"(人事变动) |
| 综合资讯(2026-07-01 新增) | 多公司动态拼盘(如"OpenAI/Anthropic/谷歌三角战")→ "其他" |
| 不确定性 | 无法明确判断 → "其他" |

**⚠️ 研发范式/工程实践类内容必须识别上调(v3.3 新增)**:
- 研发范式、工程实践、系统思维、技术方法论等内容属于技术内容,**必须主动识别并归入国际/国内/同业**,不得归入"其他"
- 分类时遇到以下类型 → 直接归前三类,不走"其他":
  - 研发范式讨论(如「AI终成协议」、软件工程方法演进)
  - 工程实践/系统思维(如「组织级AI转型」、DevOps实践)
  - 技术方法论/行业影响力(如「1%法则」、AI应用架构设计)
- 主 Agent 在 Step 3 分类 + Step 4 第 1 轮验证中**双重确认**无此类误归
- 人工审核为兜底确认,不作为首轮分类的依赖

**基础设施边界案例**(2026-07-10 老板明确):
- ✅ **基础设施讨论**(Kubernetes、芯片适配、Agent 编排平台架构)→ 归前三类
- ✅ **基础设施投资/算力建设**(纯商业角度)→ "其他" 或删除
- ❌ **基础设施物理事故**(如 AI 超算高温瘫痪、机房故障、服务器宕机事件)→ **不属技术内容,直接删除**
  - 依据:纯运维/事件报道,无 AI 技术突破,不符合"技术内容"定义
  - 案例(7-9):《37.7°C 热晕了!剑桥大学 AI 超算瘫癈》→ 虽出现"AI 超算"关键词,但内容是散热/运维事故,删除

### 3.3 大模型打标(is_model_related)

**核心原则**:区分"大模型本身" vs "大模型应用场景"

```
涉及大模型关键词? ─否→ False
       ↓ 是
是模型本身的技术(发布/测评/架构)? ─是→ True
       ↓ 否
→ False(应用层/框架层/产品功能)
```

**应打标 = True**:
- 模型发布/版本更新(GPT-5 发布、Claude 3.5 更新)
- 模型测评/benchmark(GPT vs Claude 对比)
- 模型架构/训练新方法(MoE 优化、RLHF 新方法、学术基准突破)

**不应打标 = False**:
- AI 应用功能、Agent 框架、智能体应用
- 基础设施讨论(Kubernetes、芯片适配、Agent 编排平台)
- 产品功能展示/评分系统("Claude 评分标准曝光"、"Codex 升级")
- 公司动态/融资/人事/应用场景

**边界案例**:
- ❌ Agent 框架工程优化(Hermes Agent 启动速度)→ False
- ❌ 产品功能更新(AI 图像压缩)→ False
- ❌ 学术 Agent 研究(Agent-World)→ False
- ✅ 世界模型/学术基准突破 → True
- ✅ 训练技术研究(重卷 ImageNet)→ True

### 3.4 摘要生成(v3.3 升级)

**规则**:
- 每篇文章生成 **~300字中文摘要**,可分多段(用空行分段)
- 外文文章(OpenAI、DeepMind、TLDR AI、MarkTechPost等)摘要必须用**中文**撰写
- 简讯综合类文章("9点1氪""极客早知道"等)不做摘要,digest填"综合简讯,包含N条快讯"
- 摘要存入 front matter 的 `digest: |` 字段(多行 YAML)
- **不补充原文没有的信息,不添加主观评价**(v3.3 新增)

### 3.5 同主题合并(方式 A,唯一推荐)

**触发**:多篇报道同一核心事件 → 合并为一条

**写法**:
```json
{
  "aid": "主文章aid",
  "title": "主文章标题",
  "source": "主来源公众号名",  // ✅ 不要写"多源综合"或逗号拼接
  "link": "主文章链接",
  "digest": "整合后摘要",
  "source_file": "sources/主文章_主来源.md",
  "is_model_related": true,
  "is_merged": true,  // ✅ 必填
  "source_items": [  // ✅ 必填:所有来源
    {"name": "公众号A", "source_file": "sources/A_xxx.md", "link": "..."},
    {"name": "公众号B", "source_file": "sources/B_xxx.md", "link": "..."}
  ],
  "merged_articles": [  // 可选:全量原始信息(注意字段名用 name)
    {"name": "公众号A", "source_file": "...", "link": "..."},
    {"name": "公众号B", "source_file": "...", "link": "..."}
  ]
}
```

**合并操作**:
- 从分类列表中**移除被合并的原始文章**
- 只保留合并后条目
- ⚠️ 字段名规范:`merged_articles` 内必须用 `name`(不用 `source`),`generate_html.py` 只认 `name`

**废弃写法**(请勿使用):
- ❌ `"source": "多源综合"`
- ❌ `"source": "机器之心, 新智元"`(逗号拼接)
- ❌ 只写 `is_merged: true` 但不写 `source_items`

**合并粒度原则**:
- ❌ 不要把同一家公司的所有文章都合并(除非确实是同一事件)
- ✅ 合并的是:同一核心事件/产品的多角度报道
- 例:Qwen3.7 发布(2 篇)合并;Qoder 接入 Qwen3.7(1 篇)独立(主体不同)

**强合并检查清单(2026-07-03 血泪教训)**:

首次分类时必须主动检查这些同题名场景:
- ✈️ 主题词完全重叠(例:Meta 卖算力、华为发布、Qwen3.X 发布)
- ✈️ 同一公司同一事件(发布/融资/新品/合作)
- ✈️ 同一数据/同一报告(2026年AI报告、Q1榜单)

**合并主条选择原则**:
- publish_time **最早**的为主条
- 标题更抽象/总括的为主条
- 多个同选其中一个,其他全放 `source_items`

**实战例(2026-07-02 Meta 三篇)**: 子智能体 1+2 轮都漏了合并,主 Agent 才合并为 1。→ **主 Agent 在 Step 3 分类时必须亲自扫一遍同公司同事件**,不要完全依赖子智能体。

### 3.6 输出格式

**重要:classification.json 不再手写**,由 `build_classification.py` 自动从 front matter 派生:

```bash
python3 build_classification.py YYYY-MM-DD
```

生成的 classification.json 结构:
```json
{
  "date": "YYYY-MM-DD",
  "国际": [
    {
      "aid": 1,
      "title": "文章标题",
      "source": "信源名",
      "link": "原文链接",
      "digest": "~300字摘要(从 front matter 读取)",
      "source_file": "sources/xxx.md",
      "is_model_related": false,
      "publish_time": 1785548482
    }
  ],
  "国内": [...],
  "同业": [...],
  "其他": [...]
}
```

**注意**:只有 `status: confirmed` 的文章才会进入 classification.json,pending 文章会被列出提醒。

### 3.7 排序强制要求

**每分类内,大模型打标的文章(`is_model_related=True`)必须排在前面**:

```
[True, True, False, False, ...]
```

保存前自检,False 排在 True 之后就要重排序。

### 3.8 source 字段空值补全

保存前检查每篇 `source` 字段,空值根据标题/链接推断:
- 腾讯研究院发布的综合资讯 → "腾讯研究院"
- 阿里云开发者 → "阿里云开发者"
- 机器之心转载 → "机器之心"
- 兜底:用公众号名称

### 3.9 source_file 路径验证(2026-07-03 血泪教训)

**教训**: 生成 classification.json 时,JSON 字符串里的中文引号、转义符、手打路径都可能跟 sources/*.md 实际文件名不匹配,子智能体查文件时 404。

**保存前必查**:
```bash
python3 << 'EOF'
import json, os
d = json.load(open('daily/YYYY-MM-DD/classification.json'))
all_articles = sum(d['classification'].values(), []) + d.get('excluded', [])
errors = []
for a in all_articles:
    sf = a.get('source_file','')
    if not sf: continue
    full = f'daily/YYYY-MM-DD/{sf}'
    if not os.path.exists(full):
        errors.append(f"{a['title'][:30]}: {sf}")
if errors:
    print('❌ source_file 错误:')
    for e in errors: print(' -', e)
else:
    print('✅ 全部 source_file 路径正确')
EOF
```

**写法规范**:
- ✅ 从 sources/*.md **直接读**文件名,不要手打
- ✅ 使用 JSON 标准的 `\"` 转义双引号(或者用全角 `""`)
- ✅ `source_items[].source_file` 同理,查主条示例验证

---

## Step 4: 三轮分类验证(强制!)

**目标**:fork 子智能体,独立 session 逐轮检查,发现错误→子智能体自动修正→主 Agent 收到结果→零错误才进入下一轮。

**为什么 fork**:主 Agent 自己验 = 程序员测自己的代码,认知盲区无法消除。

### ⏱️ 运行原则(2026-07-03 老板明确)

**不限制轮次时间**:
- ❌ 不要设"每轮必须 X 分钟"等硬性时间限制
- ✅ 子智能体要读全文就读全文,仔细检查最重要
- ✅ 只要**有进展**就让它跑,不盲等

**主 Agent 跟踪节奏(2026-07-03 老板明确)**:
- ✅ **每 3 分钟确认一次子智能体是否还在运行/有进展**
- ✅ 确认方式:`subagents` list 看状态,或 fetch 一次结果
- ✅ 有进展 → 继续等;无进展超过 1 轮确认点 → fetch;卡死明显 → 重 fork
- ❌ 不需要"3 分钟内必须完成"这类硬性门限

**为什么不限时但要跟读**:
- 分类验证是质量闸门,快而错不如慢而对
- 读全文才能判断同主题/技术归属,只读 title+digest 漏判多
- 跟读 = 避免盲等,但不催促;死等 = 浪费时间但能接收完成事件

### 执行规则

```python
for round_num in [1, 2, 3]:
    result = sessions_spawn(
        task=f"""你是 AI 早报分类验证员,负责第 {round_num} 轮检查。

请读取:
1. {workspace}/daily/{date}/classification.json
2. 本文档「第 {round_num} 轮」规则

严格逐篇检查,发现不符合的:立即修正→写回 classification.json→报告。
零错误回复「✅ 第 {round_num} 轮通过(零错误)」。""",
        runtime="subagent",
        mode="run"
    )
    if "通过" in result:
        continue  # 下一轮
    else:
        round_num -= 1  # 同一轮重 fork
```

### 第 1 轮:删除规则 + 技术/非技术判断

**检查项**:
1. `filtered_articles.json` 中有应删除但未删除的?→ 移除并记到 `excluded`
2. 「国际/国内/同业」中有非技术内容?→ 移到「其他」或删除
3. 「其他」中有技术内容被误归入?→ 根据公司属地移到国际/国内/同业
   - ⚠️ **v3.3**：重点检查研发范式、工程实践、系统思维类是否被误归"其他"，必须主动上调

**通过条件**:3 项全 ✅,无任何移动/删除。

### 第 2 轮:分类归属 + 模型打标 + 合并检查

**检查项**:
4. 国际分类中有国内公司内容?→ 移到「国内」
5. 国内分类中有国际公司/项目内容?→ 移到「国际」
6. 金融同业内容不在「同业」?→ 移到「同业」
7. `is_model_related` 字段错误?→ 修正
8. 同主题文章未合并?→ 合并(参照 3.5 方式 A)
   - 必须跨分类扫描:同一事件/同一产品/同一报告,不同公众号同天发布
   - 多篇报道同一事件时,以最早 publish_time 为主线,其他为 source_items

**通过条件**:5 项全 ✅。

**⚠️ 重要**:合并检查是独立子项(第 8 项),不可因归属/打标检查通过就跳过。由于合并需要跨分类看同主题文章,子智能体必须完整阅读所有文章标题+摘要才能判断。

### 第 3 轮:排序 + source 字段 + 统计自洽 + 标题中文化

**检查项**:
9. 每分类内模型打标文章排在前面?→ 重排序
10. `source` 字段空值?→ 推断补充
11. `source_file` 路径无效?→ 修正
12. `stats` 各分类之和 == `total`?→ 重新计算
13. **所有 title 字段不含全英文**?→ 翻译为中文(v3.3 新增,参照铁规 6)

**通过条件**:5 项全 ✅ → 输出最终报告后进入 Step 5。

### 最终确认报告

```
✅ 第 1 轮通过(删除/技术内容判断)
✅ 第 2 轮通过(分类归属/模型打标/合并检查)
✅ 第 3 轮通过(排序/source字段/统计/标题中文化)
───────────────────────────
📊 最终统计: 国际{N} 国内{M} 同业{K} 其他{L} 总计{T}
🗑️  已删除: {D} 篇
🔗 合并: {C} 篇 → {M} 篇
✅✅✅ 分类验证全部通过,进入 Step 5
```

---

## Step 5: 生成 HTML

**命令**:
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 build_classification.py YYYY-MM-DD   # 先聚合 front matter → classification.json
python3 generate_html.py YYYY-MM-DD          # 再生成 HTML
```

**做了什么**:
1. `build_classification.py`:扫描所有 `status: confirmed` 的 md 文件,汇总生成 classification.json
2. `generate_html.py`:读 classification.json,渲染 template.html 模板
3. 生成 `daily/YYYY-MM-DD/index.html`
4. 更新 `daily-index.json` 和 `search-index.json` 索引
5. 同步根 `index.html` 的 `INLINE_DAILY_INDEX`(file:// 协议 fallback,2026-08-02 新增)

**注意**:`daily-index.json` 按日期降序自动排列,补生成历史日期不会打乱顺序。

**展示方式(v3.2)**:
- 每篇文章显示 AI 摘要(~300字,多段落)+ **来源标签(可点击跳转原文)**
- **不嵌入原文全文**:HTML 体积小(~37KB),加载快
- 摘要从 classification.json 的 digest 字段读取(来源于 front matter)
- 合并主条显示多个来源标签(如 36氪 + 智东西),每个标签独立可点击
- 已移除独立「查看原文」按钮(来源标签已可直接跳转)

**验证**:
```bash
ls -lh daily/YYYY-MM-DD/index.html
```

**索引数量检查**(2026-08-02 stats 为空 bug 教训):
```bash
python3 -c "
import json
with open('daily-index.json') as f:
    d = json.load(f)
for item in d['issues'][:3]:
    s = item.get('stats', {})
    print(f\"{item['date']}: total={s.get('total','❌空')} 国际={s.get('国际','-')} 国内={s.get('国内','-')} 同业={s.get('同业','-')}\")
"
```
检查标准:
- ✅ stats 非空,total > 0
- ❌ stats={} → 检查 `generate_html.py` 的 `update_daily_index` 是否正确传入 stats

**摘要质量检查**(2026-07-16 摘要=标题 bug 教训):
每期 HTML 生成后必须抽样 3 篇检查摘要:
```bash
python3 -c "
import re, html as h
with open('daily/YYYY-MM-DD/index.html') as f:
    c = f.read()
digests = re.findall(r'<div class=\"card-digest\">(.*?)</div>', c)
for i, d in enumerate(digests[:3], 1):
    txt = h.unescape(d)
    print(f'#{i}: {txt[:80]}')
"
```
检查标准:
- ✅ 摘要 ≠ 标题(不是标题的重复)
- ✅ 摘要包含正文实质内容(事实/数据/引述)
- ✅ 摘要 ≥ 20 字符
- ❌ 摘要=标题=检测到 bug → 检查 `classification.json` 是否缺 `digest` 字段,修 `generate_html.py`

---

## Step 6: 验证与推送

### ⛑️ GitHub Actions 部署权限(2026-07-03 血泪教训)

**事故复现**:`deploy-pages@v4` 报错 deploy failure,但 build success。根因是 `deploy.yml` 的 `permissions` 缺 `actions: write`。

**必需 permissions**:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
  actions: write   # ← 关键!deploy-pages@v4 必需
```

**自检命令**(每次 push 前必查):
```bash
cat .github/workflows/deploy.yml | grep -A 6 'permissions:'
```

若 `actions: write` 缺失 → 立即补全,再 push。

**部署超时处理**:
```bash
sleep 30 && gh run list --limit 1
# 或
curl -s "https://api.github.com/repos/keejo125/AI_Daily_For_Bank/actions/runs?per_page=1" \
  | python3 -c "import json,sys; r=json.load(sys.stdin)['workflow_runs'][0]; print(f'#{r[\"run_number\"]} {r[\"conclusion\"]}')"
```

连续 2 次 deploy fail → 查 workflow YAML,不要盲目重试空 commit。

### 本地验证

| 检查项 | 命令 |
|--------|------|
| HTML 存在 | `ls daily/YYYY-MM-DD/index.html` |
| 分类文件完整 | `cat daily/YYYY-MM-DD/classification.json \| python3 -m json.tool \| grep stats` |
| 索引已更新 | `cat daily-index.json \| python3 -m json.tool \| grep YYYY-MM-DD` |
| 页面可访问 | `open daily/YYYY-MM-DD/index.html` |

### 推送到 GitHub

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank

git add daily/YYYY-MM-DD/
git add daily-index.json search-index.json index.html
git commit -m "Add daily report for YYYY-MM-DD"

# 🚫 严禁 --force / -f / --force-with-lease
# 🚫 严禁 reset --hard / reset --mixed HEAD~ 回滚
# ✅ 如遇 push 冲突,先 rebase,再 push
git pull --rebase origin master
git push origin master
```

**Git remote 使用 HTTPS**(2026-08-03 v3.2 更新):
```bash
# 默认使用 HTTPS
git remote set-url origin https://github.com/keejo125/AI_Daily_For_Bank.git
```
若 HTTPS(443) 超时(如 2026-08-03 实际发生),**临时切换 SSH 推送后立即切回**:
```bash
git remote set-url origin git@github.com:keejo125/AI_Daily_For_Bank.git
GIT_SSH_COMMAND="ssh -o ConnectTimeout=20 -o StrictHostKeyChecking=accept-new" git push origin master
git remote set-url origin https://github.com/keejo125/AI_Daily_For_Bank.git
```
**不要永久切换到 SSH**(端口22不稳定),SSH 仅作为 HTTPS 失败时的临时后备。

**在线预览**:`https://keejo125.github.io/AI_Daily_For_Bank/daily/YYYY-MM-DD/`

---

## Step 7: 反思与优化(每次全流程结束后)

**目标**:回顾本次执行的问题、异常、手动修正,判断是否可优化技能本身。

**反思清单**:

| 关注点 | 反思问题 |
|--------|----------|
| 合并问题 | 重复渲染?合并条目未移除? |
| 文件匹配 | 中文引号/角括号匹配失败? |
| 分类偏差 | 有人工纠偏?纠偏模式可固化? |
| 来源为空 | `source` 字段空值?需更新订阅表? |
| 删除规则 | 过滤的非技术内容有新类型?需更新关键词? |
| 模型打标 | `is_model_related` 漏判/误判? |
| 脚本缺陷 | `generate_html.py` 可改进? |

**输出**:
1. 有优化空间 → 直接改 skill / 脚本,提交
2. 是分类 Agent 执行偏差 → 记录到 `memory/reflections/`
3. 简洁汇报到微信(≤3 条)

---

## 📂 文件结构

```
AI-Daily-for-bank/                   # ← 项目根目录(铁规1)
├── scripts/                          # Python 脚本
│   ├── fetch_web_articles.py        # 多源获取(工厂模式适配器)
│   ├── filter_articles.py           # 关键词过滤
│   ├── build_classification.py      # 从 front matter 聚合 classification.json
│   ├── generate_html.py             # 生成 HTML
│   ├── add_manual_link.py           # 手动投稿
│   └── sources/                     # 适配器模块
│       ├── __init__.py              # ADAPTER_REGISTRY + create_adapter()
│       ├── base.py                  # 基类 + fetch_wechat_page()
│       ├── rss_adapter.py           # 标准RSS适配器(主力)
│       └── kr36_adapter.py          # 36氪API适配器(已废弃)
├── config/
│   └── sources.json                 # 统一信源配置
├── daily/                            # 早报数据
│   └── YYYY-MM-DD/
│       ├── index.html               # 最终产出
│       ├── sources/                  # Markdown 原文(带 front matter)
│       ├── articles_raw.json
│       ├── filtered_articles.json
│       └── classification.json      # 派生索引(build_classification生成)
├── template.html                     # HTML 模板
├── daily-index.json
├── search-index.json
├── manual_links.json                 # 手动投稿队列
├── config.json                       # 过滤关键词配置
├── RSSHUB-DEPLOY.md                  # RSSHub 部署运维文档
└── README.md
```

---

## ⚙️ 配置文件 `config.json`

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

---

## 🔗 相关资源

- **GitHub**: https://github.com/keejo125/AI_Daily_For_Bank
- **在线预览**: https://keejo125.github.io/AI_Daily_For_Bank/
