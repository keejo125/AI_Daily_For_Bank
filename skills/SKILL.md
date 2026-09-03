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
  version: "3.15"
  category: productivity
  updated: "2026-09-03"
  changelog: |
    v3.15 (2026-09-03): ① 新增 **Step 1.5 内容自检与定点重抓**——fetch 结束后自动扫描正文退化(正文<500字/空正文/缺link),**只重抓问题项的 URL** 并写回原文件,最多 1 轮;新增"只升不降"保护(新正文更短则不写盘)。② **URL 取代文件名成为身份键**:`build_url_index()` 建 URL→文件映射,已存在 URL 一律不写盘(稳态零改动),文件名撞车时追加 URL 短哈希,从根上消灭"同文异名"重复。③ 新增**排除清单** `config/excluded_links.json` + `scripts/exclude_store.py`:filter_articles.py 删除文件前登记 URL,杜绝已删文章下次重抓长回来(实测曾一次跑回 14 篇垃圾)。④ **铁规13**:严禁 rm -rf daily/<date> 目录级清空重建(2026-09-03 事故:误删用户手工投放的建行同业稿),修 bug 的最小作用单位是单个文件。⑤ 修复依赖自检致命 bug:beautifulsoup4 的 pip 包名与导入名(bs4)不一致,原写法 pip 装成功但 import 必失败致脚本崩溃——现改为 (pip名, 导入名) 元组。
    v3.14 (2026-08-26): ① 固化 2026-08-26 实战教训——Step 3 禁止派子 Agent,必须由主 Agent 内联执行(子 Agent 自带写回脚本只替换不新增,致 17/29 文件缺 category/digest,且未断言 build 真实收录数,报"假成功"卡在坏中间态;Step 4 三轮 fork 验证仍须派子 Agent 只读复核,不受本条影响)。② Step 3 写回统一走 scripts/_step3_update_v2.py(缺失字段即新增、不丢 H1),并新增 build 校验闸门:写回后须断言 收录数==confirmed 数 且 pending==0,否则原地修复重跑,严禁"假成功"进 Step 4。
    v3.13 (2026-08-23): ① 3.1 删除规则新增「非AI金融理财/收益宣传」一类(关键词:理财/收益/年化/定存/存款利率/净值/基金申购/保费/加息/降息;判定:纯金融营销且无AI技术内容→删除)。② 固化 eval F07 暴露的误判——来自该 fixture 的实战:独立 agent 曾把"某银行稳健理财年化收益破5%"误归"其他/confirmed",现以显式规则+误判提醒堵住。③ 修正综合资讯 note 的复制粘贴笔误(原错串具身智能/机器人边界保留与注意句,改为综合资讯专用)。
    v3.12 (2026-08-23): ① 新增「🤖 定时任务执行契约」——自动化必须以 Step 1 fetch_web_articles.py 开头,严禁因 sources/ 非空跳过抓取(2026-08-23 实战:自动化跳过 RSS 抓取,早报仅含公众号投稿)。② 综合资讯/多源快讯拼盘由「归其他」改为「直接删除」(3.1 新增删除类 + 3.2/3.4 同步修正,2026-08-23 用户偏好固化)。③ 新增「标题中文化闸门」机器化校验脚本(push 前硬跑,铁规6 兜底,防 R3 被跳过致英文标题漏翻)。④ 自动化配置检查清单(cwds 必须为项目根、prompt 须写全步骤、validUntil 防过期静默停跑)。⑤ 评测闭环(Gate 4):eval/ 新增 F09(综合资讯删除)、F10(英文标题中文化)两 fixture,gold.json + verify.py 新增 title_cjk 校验;独立子智能体跑分 10/11,F09/F10 全过,F07(零AI理财)暴露独立 agent 误入选——已于 v3.13 补「非AI金融理财资讯→排除」规则。
    v3.11 (2026-08-22): ① 固化内容过滤偏好——具身智能/机器人/自动驾驶类内容不计入银行智能研发早报（Step 3 删除规则 3.1 新增一类，按主题语义判断；正文仅顺带提及"机器人"但主题为 LLM/编程/AI4Science/AR 等的文章保留）。② fetch_web_articles.py 新增执行前依赖自检（缺 requests 自动 pip 安装到当前解释器）。
    v3.10 (2026-08-20): ① Git 推送从 HTTPS 改 SSH（HTTPS 在本环境持续失败——出口代理 502 + keychain 存 qclaw 账号非沙箱 git 进程读不到凭据；~/.ssh/id_rsa 已绑 keejo125、SSH 认证稳定，用户明确要求）。② 新增「增量补充批次」经验：手工导入新文章与旧删除项均为 pending，用 mtime 区分；新导入文章须与已 confirmed 旧文章跨批去重（GPT-6/Astra 停训 4 源合并为 1 卡）。
    v3.9 (2026-08-19): 固化 08-19 实战两教训——① Step 3 子 Agent 改写必须保留/补回 `# ` H1 标题行(否则标题 fallback 成文件名、违反铁规6)；② 摘要严禁虚构外部事实(SpaceX收购Cursor幻觉)，R1 检查项新增"摘要事实核查"为第4子项。
    v3.8 (2026-08-14): skill-optimizer 精益化——删除 QClaw 冗余环境段、合并重复标题、补「完成判据/退出条件」、固化 08-13 实践教训(Step4 不可被 Step3 级联跳过；stats 与列表 is_merged 从卡自洽)。完整历史见 CHANGELOG.md。
    v3.7 (2026-08-11): 铁规9 摘要唯一来源 + 铁规12 修正回写 front matter + R3 强制 rebuild。
    （v3.0–v3.6 及更早变更见 CHANGELOG.md）
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

**问题**:合并组中从条如果只作为独立文章 append,会与主条重复显示

**实际生效的合并机制(以 `build_classification.py` 为准,2026-08-14 修正)**:合并**只能通过 `merge_plan.json` 驱动**,**不是**在 front matter 写 `is_merged`(脚本不读它)--
1. Step 3 在 `daily/YYYY-MM-DD/merge_plan.json` 写入 `merged_groups`(`main` + `items`,格式见下)
2. `build_classification.py` 的 `load_merge_plan()` 读取它,建立 `从条 source_file → 主条 source_file` 映射,并把从条(name+link)注入主条的 `source_items`
3. 从条在 classification.json 中标记 `is_merged`+`merged_into`,但 `generate_html.py` 跳过从条渲染,主条卡片渲染多来源标签(每标签可点击跳转对应原文)
4. ⚠️ 关键:`merge_plan.json` 被 `.gitignore` 忽略,但它是合并信息的**唯一来源** → 提交时必须 `git add -f daily/YYYY-MM-DD/merge_plan.json`,否则 clone 后 rebuild 会丢失合并

**铁规**:
- ✅ 主条:**正常渲染**,`source_items` 数组渲染为多来源标签
- ✅ 从条(`is_merged=true`):**不渲染**--其内容已合并入主条的 `source_items`
- ❌ 不允许从条作为独立文章显示(会与主条重复)

**merge_plan.json 格式（v3.7 规范化）**:

与 `build_classification.py` 的 `load_merge_plan()` 严格对齐：

```json
{
  "merged_groups": [
    {
      "main": "sources/主条文件.md",
      "items": [
        {
          "source_file": "sources/从条文件.md",
          "name": "来源名称",
          "link": "原文URL"
        }
      ]
    }
  ]
}
```

- `main` = 主条 source_file（必填）
- `items[].source_file` = 从条 source_file（必填）
- `items[].link` = 从条原文 URL（**必填,不能为空**；为空 → HTML 渲染为 viewer 回退链接）
- 禁止使用 `main_article` / `merged_articles` / `pairs` 等旧键名

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
- `stats.total = 列表数 - is_merged 从卡数`(列表保留从卡,stats 只计主条,**设计如此,非 bug**)

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

**⚠️ v3.7 关键修正**:翻译结果必须写入 source .md 的 `# ` 标题行(而非 `classification.json` 的 `title` 字段),因为 rebuild 时 `extract_title_from_body()` 从 H1 重新读取会覆盖 JSON 修改。

### 铁规 9:摘要保护（v3.7 新增）

**问题**:R3 子会话修改 `classification.json` 时,`digest: |` YAML 多行块标量被误截为字面量 `"digest": "|"`,导致全部摘要丢失。

**规则**:
- ✅ `digest` 的**唯一来源** = source .md front matter 的 `digest: |` 字段
- ❌ 禁止任何步骤修改 `classification.json` 中的 `digest` 字段
- ❌ 禁止 R3 验证子会话触碰 digest(只检查 title/source_file/stats/排序)

### 铁规12:验证修正回写 front matter + 重建串联（v3.7 新增）

**问题**:R1/R2 改正了 `classification.json` 的分类归属,但 source .md 的 front matter 未同步修正 -> 后续 rebuild 时修正全丢(08-11 3 处实际发生)。

**规则**:
- ✅ R1 分类修正 → 改 source .md 的 `category:` 字段
- ✅ R2 is_model_related 修正 → 改 source .md 的 `is_model_related:` 字段
- ✅ R3 标题中文化 → 改 source .md 的 `# ` 标题行
- ✅ R3 source 字段修正 → 改 source .md 的 `source:` 字段
- ❌ 禁止直接编辑 `classification.json` 的 `title` / `category` / `is_model_related` / `source`
- ❌ **R3 验证子会话指令中必须明确禁止修改 digest 字段**

**R3 后强制串联**:
```bash
# R3 完成后 → 重建所有(不可跳过)
python3 build_classification.py YYYY-MM-DD
python3 generate_html.py YYYY-MM-DD
```
此流程确保所有回写 front matter 的修正反映到最终 HTML,且 3 轮验证 mtime 检查（铁规5）仍然适用于此 rebuild 产生的 JSON。

### 铁规13:严禁删除 daily/<date> 目录(v3.15 新增,2026-09-03 事故固化)

**事故**:2026-09-03 自动化为修复"重复抓取"执行 `rm -rf daily/2026-09-02`,把用户前一晚手工投放的稿件(含建行同业文章)一并删除,事后不得不手工找回重建。

**规则**:
- ❌ **绝对禁止** `rm -rf daily/<date>`、`rm -rf daily/<date>/sources` 或任何形式的目录级清空重建
- ❌ 禁止以"重跑一次最省事""反正还没 commit"为理由删除目录——未 commit 恰恰意味着 git 也救不回来
- ✅ 重复问题 → 交给 Step 1.5 的 URL 映射(已存在复用,不新建副本)
- ✅ 内容退化问题 → 交给 Step 1.5 的定点重抓(只重抓问题项,或 `--force`)
- ✅ 需要删除单篇文章 → 只删那一个文件,且**必须把 URL 登记进排除清单**(`scripts/exclude_store.py`),否则下次 fetch 会抓回来
- ✅ 重建前若 `sources/` 已有非本次抓取产出的文件(用户手工投放),必须先 diff 并增量合并

**判断口诀**:修 bug 的最小作用单位是"单个文件",永远不是"整个目录"。

### 铁规 5:3 轮 fork 验证不可省略(2026-07-12 老板新增，v3.6 修正 spawn 路径，WorkBuddy 适配见下段)

**问题**:主 Agent 分类自查后,直接跳到 Step 5 生成 HTML--**违反了 Step 4 的 3 轮 fork 验证强制要求**。本次自查漏判 6 处错误(1 漏删 + 1 国际国内互换 + 1 产业调其他 + 3 模型打标),幸被老板发现,补做 3 轮 fork 才纠正。

**铁规**:
- ✅ Step 4 的 3 轮 fork 验证**不可省略、不可由主 Agent 自查替代**
- ✅ 即使主 Agent 自我感觉"分类很合理",仍必须 spawn 子智能体独立 session 复核
- ✅ 每轮 5/5 检查项全部通过,才进入下一轮
- ❌ **绝对禁止**主 Agent 跳到 Step 5 直接生成 HTML
- ❌ **绝对禁止**"赶时间"省略 3 轮验证

**独立验证实现方式（按运行环境选择）**:
- **WorkBuddy（本安装版）**:用 **Agent 工具**（`subagent_type="general-purpose"`）派生独立上下文子智能体,`prompt` 传入完整验证任务(读 classification.json + 全部 sources/*.md + 本轮检查项)。等价于 QClaw 的 `sessions_spawn(agentId="main")`。
- **QClaw**:`sessions_spawn(agentId="main", task=..., taskName="verify_round_N", mode="run")`。
- 子智能体返回后,主 Agent **必须复核**其结论与落地改动(曾靠此拦截一次子智能体误报)。
- 若独立验证机制彻底不可用,**必须停下来报告老板**,不得自行跳过。
- ⚠️ **08-13 教训(级联跳过)**:若 Step 3 因子 Agent 长任务失败而改由主 Agent 直跑,**Step 4 仍必须派子 Agent 独立验证**,不得以「主 Agent 已直跑」为由跳过。

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
- ⚠️ **WorkBuddy mtime 检查修正（v3.8 实践，08-18 固化）**：WorkBuddy 下子智能体按铁规12/铁规9 **只改 source .md 的 front matter**（`# ` H1 / `status` / `category` / `is_model_related` / `source:`），**不修改 classification.json**。因此 R1/R2/R3 期间 classification.json 的 mtime **本就不会变**——若仍按上两条检查 classification.json，会**误判为"模式 B 静默失败"**让主 Agent 错误接管。正确做法：
  - 每轮 spawn **前** `stat -f '%m %N' sources/*.md | sort` 快照全部 source .md mtime 到临时文件；spawn 返回后**立即比对**。
  - 有文件 mtime 推进 = 子智能体已落地改动（正常，无论它自称零错误还是有修正）；无任何 source mtime 变化且子智能体自称"零错误" = 合理静默（**非**模式 B，勿接管）。
  - 若子智能体**声称有 N 处修正但 source mtime 无一变化** = 真·模式 B 静默失败 → 主 Agent 直接接管该轮检查。
  - classification.json 的 mtime 仅在 R3 后 `build_classification.py` rebuild 时推进，届时再核对它即可。

**本次教训量化**(7-12 + 7-15 早报):主 Agent 一次性分类看似零错误,但 3 轮 fork 共发现 6 处错误(含 1 国际国内互换 + 3 模型打标),静默空跑 1 次靠 mtime 拦截;独立验证不可省。

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

## 🤖 定时任务执行契约（自动化必读，2026-08-23 新增）

**问题（2026-08-23 实战）**：每日 05:00 自动化 prompt 仅写「开始今天的AI早报」，agent 见 `sources/` 已有 5 篇公众号投稿（前一日 wechat-to-wiki 注入的 pending 文章）就**直接从 Step 3 分类**，把 **Step 1（RSS 抓取）整个跳过** → 当日早报只有公众号投稿、完全缺失 RSS 源（36氪/InfoQ/极客公园/量子位/MarkTechPost/Solidot…）。补救：手动补跑 `fetch_web_articles.py` + 重建。

**铁律（自动化必须严格遵守）**：

1. ✅ **自动化必须以 Step 1 `fetch_web_articles.py <date>` 开头**，无论 `sources/` 是否已有文章。fetch 是**幂等 + 增量保护**：已 `confirmed` 的文章不覆盖；手动投稿(wechat-to-wiki)注入的 pending 文章与 RSS 抓取的文章并行存在于同一目录，互不冲突、合并处理。
2. ❌ **严禁**因 `sources/` 非空就跳过 Step 1。Step 1 是"补充新源"，不是"初始化"。
3. ✅ 完整顺序固定为 Step 1 → 2 → 3 → 4(三轮) → 5 → 6，**任何一步都不得因上一步"看起来够用"而跳过**（含 Step 4 三轮验证，见铁规5）。
4. ✅ Step 1 后**必须报告各信源抓取结果**（成功 N 篇 / 失败源清单）。单源失败（如 RSSHub 返回 503）**不得中断整体**，但须在汇报中列出失败源，便于排查。
5. ✅ 推送飞书：**默认不推**，除非自动化 prompt 显式要求或用户当日要求（见 Step 6 / daily-push-to-feishu）。

**自动化配置检查清单（每次建/改自动化时核对）**：
- `cwds` **必须**是项目根 `/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank`（铁规1），不是父仓库。
- `prompt` **必须**显式写出完整步骤或「按 ai-daily-for-bank 技能完整 7 步执行，且以 Step 1 fetch 开头」，不能只写「开始今天的AI早报」。
- `validUntil` 不可早于预期运行期；过期后自动化静默停跑（2026-08-23 曾因 `validUntil=2026-08-23T15:59` 在当日 15:59 后失效）。

---

## ✅ 完成判据 / 退出条件（Gate 4：原缺失，必须补）

「早报做完」的硬判据（**全部满足才算完成，缺一则停下报告老板**）：

- [ ] `build_classification.py` 成功，`classification.json` 的 `stats` 非空且 `total > 0`
- [ ] **Step 4 三轮验证均返回「✅ 第 N 轮通过(零错误)」**，且每轮 `classification.json` 的 mtime 已推进（拦截模式 B 静默空跑）
- [ ] 主 Agent 已逐轮复核子智能体结论与落地改动（非静默接受）
- [ ] digest 覆盖率 100%（0 篇空、0 篇「摘要=标题」占位）
- [ ] `generate_html.py` 生成 `index.html`，抽样 3 篇摘要 ≠ 标题
- [ ] Git 已 `commit` + `push`（严禁 force/reset），`merge_plan.json` 已 `git add -f`
- [ ] 统计自洽：列表含 `is_merged` 从卡时，`stats.total = 列表数 − 从卡数`（**设计如此，非 bug**）
- [ ] **标题中文化闸门（铁规6 机器化校验）**：推送前必须运行下方脚本，所有 `title` 含中文、无全英文标题；命中全英文 → 停下翻译回写 source .md 的 `# ` H1 行并 rebuild，不得带英文标题 push
- [ ] 飞书推送：仅当用户明确要求时执行（默认不推）

> ⚠️ **08-13 教训（级联跳过）**：若 Step 3 因子 Agent 长任务失败而改由主 Agent 直跑，Step 4 仍**必须**派子 Agent 独立验证，不得因 Step 3 跳过而级联跳过 Step 4。

---

## Step 1: 获取文章(多源统一接入)

**命令**:
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/scripts
python3 fetch_web_articles.py 2026-08-09
# ↑ 日期是位置参数，不是 --date flag！
# 脚本已内置格式校验，传 --date 等非法值会直接报错退出
```

⚠️ **铁规11（v3.6 新增）**：日期参数必须是 `YYYY-MM-DD` 位置参数，**严禁**传 `--date`、`-d` 等 flag 前缀。脚本内置正则校验，非法格式直接拒绝。

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

## Step 1.5: 内容自检与定点重抓(v3.15 新增,2026-09-03 事故复盘落地)

**为什么要有这一步**:2026-09-03 自动化为修"重复抓取"执行过 `rm -rf daily/2026-09-02`,
把用户 09-02 23:31 手工投放的稿件(含建行同业文章)一并删除。复盘出三个缺失,现已全部落地为机制:

| 缺失 | 后果 | 修复机制 |
|------|------|----------|
| 身份键用文件名 | 标题清洗随解析器漂移 → 同一文章存成两个文件(曾出现 54 个文件) | **以 `link`(URL) 为身份键**,已存在则复用原文件,绝不新建副本 |
| 无内容质量诊断 | 退化 stub 永久卡死 → 逼人"删目录重抓" | **自动自检**,正文 <500 字判为退化 |
| 删除不留记录 | 已删文章下次重抓必然长回来(实测一次跑回 14 篇垃圾) | **排除清单** `config/excluded_links.json` |

**已内置在 `fetch_web_articles.py`,Step 1 跑完自动执行,无需单独调用**:

1. **L1 URL 映射**:抓取前扫描 `sources/*.md` 建 `URL → 文件` 映射;已存在的 URL **不写盘**(稳态零改动),只有新文章才落盘。
   文件名撞车但 URL 不同时追加 URL 短哈希,绝不误覆盖他人文件。
2. **L2 内容自检**:正文 <500 字 / 空正文 / 缺 `link` → 打印问题清单(见 `settings.content_min_length` 可配)。
3. **L3 定点重抓**:**只重抓问题项的那几个 URL**,写回原文件路径(不新建、不重命名),抓到即覆盖,**最多 1 轮,不循环**。
4. **只升不降**:新正文比旧的还短 → 不写盘,只告警。防止反爬/断网时把好内容劣化。
5. **confirmed 保护**:`status: confirmed` 的问题项默认**只报告不覆盖**(摘要已基于旧正文写好),需 `--force` 才覆盖。

**人工诊断/修复命令**(日期位置参数规则同铁规11):
```bash
python3 fetch_web_articles.py 2026-09-02 --check-only   # 只自检并打印清单,不重抓
python3 fetch_web_articles.py 2026-09-02 --force        # 连 confirmed 的问题项也一并重抓覆盖
```

**排除清单**:`filter_articles.py` 在 `unlink()` 前会把 URL 写入 `config/excluded_links.json`(`scripts/exclude_store.py`)。
**Step 3 若需物理删除文件,必须同样登记**,否则下次 fetch 会把它们抓回来。

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

**默认关键词**(config.json 的 `keywords.include`,已扩充为覆盖模型/LLM/智能体/推理基础设施/机器人等约 60 个词,如 `AI/大模型/LLM/GPT/GLM/Qwen/DeepSeek/推理/vLLM/Triton/机器人/具身/训练/强化学习/...`):

> ⚠️ **include 列表是"删除闸门",覆盖不足会静默误删 AI 文**。2026-08-17 曾因仅 4 词(`AI/大模型/智能体/skill`)导致 5 篇当天重要 AI 文被物理删除:Qwen3.8-27B 工程优化、Netflix Triton/vLLM 服务、GLM-5.3 Coding 测试、共生知行人形机器人赛车、世界机器人大会。其特征(title+digest 不含那 4 词)全部命中失败。已扩充关键词修复。
> - 判断标准:宁可宽松(下游 Step3/4 会再删非AI),不可漏网。新增 AI 厂商/模型/技术名词时,优先补到这里。
> - `config.json` 被 `.gitignore` 忽略(本地配置,含本地路径/密钥),**关键词改动只生效于本地,不进提交**。换机/新环境需重新确认关键词覆盖。

**修改**:编辑项目根目录 `config.json` 的 `keywords.include`,立即生效(无需重启)

---

## Step 3: 智能分类与摘要(增量处理,LLM 主导)

**目标**:对 `sources/*.md` 中 `status: pending` 的文章分类、打标、生成摘要,写回 front matter

> ⚠️ **Step 3 必须由主 Agent 内联执行,禁止派子 Agent(v3.14 固化,2026-08-26 实战教训)**
> 派子 Agent 执行 Step 3 会卡在坏中间态——2026-08-26 实战:子 Agent 自带并修补的写回脚本 `_step3_update.py`(v1)只替换不新增 front matter 字段,导致 17/29 文件缺 `category`/`digest`;且子 Agent 跑完 build 未断言真实收录数(应 29 实 12),报告"假成功",流水线停在坏态需主 Agent 兜底。而 Step 4 三轮 fork 验证仍**必须派子 Agent**(只读复核,不碰文件,主 Agent 逐轮复核),不受本条影响。Step 3 一律主 Agent 内联:逐篇读文 → 判断 → 用已验证的 `scripts/_step3_update_v2.py` 写回 → 重跑 build 并断言。

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

> ⚠️ **Step 3 主 Agent 内联写回 front matter 两大约束（2026-08-19 实战教训，血泪；v3.14 补 build 校验闸门）**
> 主 Agent 内联重写 front matter 时，常因脚本重建整文件而丢失正文 `# ` H1 标题行，或摘要凭空捏造外部事实。必须严格遵守：
> 1. **H1 标题行不可丢**：每篇 .md 必须保留（或补回）`# {文章标题}` 的 H1 行（在 front matter 之后）。`build_classification.py` 的 `extract_title_from_body()` 从 H1 提取标题，缺 H1 → 标题 fallback 成带日期前缀的文件名，HTML 难看且违反铁规 6。主 Agent 在 Step 3 收尾应脚本批量校验"所有保留篇均有 `# ` H1"，缺失则从 front matter `title:` 补回。
> 2. **摘要严禁虚构（幻觉）**：digest 必须严格忠实原文，**禁止**注入原文没有的收购/融资/合作/具体数字/时间节点。实战曾发生子 Agent 在 Cursor 摘要中捏造"被 SpaceX 以 600 亿美元收购"——原文并无此说。R1 验证子项已固化"摘要事实核查"，但**源头应在 Step 3 就禁止**：中文来源报道国外产品时，不得自行补充外部商业信息；凡摘要含原文没有的具体实体/数字，一律不写。
> 3. **build 校验闸门（v3.14 新增，强制）**：写回后必须重跑 `python3 scripts/build_classification.py YYYY-MM-DD` 并断言——`收录数(国际+国内+同业+其他) == confirmed 文件数` 且 `pending == 0`。任一不满足 → 原地修复（优先用 `scripts/_step3_update_v2.py` 缺失字段即新增）后重跑，直至通过。**严禁在"假成功"状态下进入 Step 4**。写回统一走 `scripts/_step3_update_v2.py`（缺失字段即新增，不丢 H1），禁止内联手改导致格式漂移。

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
| 具身智能/机器人/自动驾驶 | 具身、人形机器人、机械臂、灵巧手、世界机器人大会/WRC、宇树、自动驾驶、智能驾驶 | "机器人的GPT-3时刻"、"宇树科技上市首日大涨629%"、"行业首发3+N批量部署亮相WRC" |
| 综合资讯/多源快讯拼盘 | 多家公司动态拼盘、快讯合集、简讯(无主线技术深度) | "微信灰测X；DeepSeek上线Y；车企召回Z"、"9点1氪"、"极客早知道"、"OpenAI/Anthropic/谷歌三角战" |
| 非AI金融理财/收益宣传 | 理财、收益、年化、定存、存款利率、净值、基金申购、保费、加息、降息(无AI技术内容) | "某银行稳健理财年化收益破5%"、"XX银行大额存单利率上调"、"净值型理财本周收益榜单" |

> ⚠️ **具身智能/机器人/自动驾驶排除规则（2026-08-22 用户偏好固化）**：此类内容与「银行智能研发」主题无关，**不计入早报**。判定以「文章主题是否关于具身智能、机器人（含 WRC 世界机器人大会、宇树人形机器人、具身智能）、自动驾驶/智能驾驶」为准，命中即删除（物理删除 sources 下 .md → rebuild 重推）。
> - **边界保留**：正文仅**顺带提及**"机器人"但主题实质为 LLM/编程/AI4Science/AR 眼镜/多模态等的文章（如 Bob大叔编程、Liquid AI、DeepSeek 多模态），**予以保留**——这是语义判断，不能直接靠 `config.json` 的 `keywords.exclude` 机械排除（否则会误删 LLM 文）。
> - 注意：`config.json` 的 `keywords.include` 当前含"机器人/人形机器人/具身/机械臂/自动驾驶/智能驾驶"等词，仅用于 Step 2 不过滤掉这类文章；最终取舍由本删除规则（Step 3 语义判断）决定。

> ⚠️ **非 AI 金融理财/收益宣传排除规则（2026-08-23 用户偏好固化，来自 eval F07）**：银行/金融机构发布的「理财收益、存款/定存利率、基金净值、保费、加息降息」等**纯金融营销资讯**，若**不含任何 AI 技术内容**（未涉及 AI 模型/智能体/风控算法/智能投顾系统等），**不计入早报，直接删除**（物理删除 sources 下 .md → rebuild 重推）。判定以「文章技术主线是否为 AI/智能研发」为准——仅借银行场景包装、实质是收益宣传的，命中即删。
> - **边界保留**：含 AI 技术实质的金融文**保留**——如「AI 智能投顾系统上线」「大模型驱动实时风控引擎」「某行用 LLM 重构信贷审批」应正常分类（归 同业/国内），不在此列。
> - **误判提醒**：`config.json` 的 `keywords.include` 历史遗留含"理财/收益"等词（用于 Step 2 不过滤），但此类纯收益宣传最终由本规则（Step 3 语义判断）排除——**不要因含"理财"词就误判为 AI 入选**（eval F07：独立 agent 曾把"某银行稳健理财年化收益破5%"误归"其他/confirmed"，应排除）。

> ⚠️ **综合资讯/快讯拼盘排除规则（2026-08-23 用户偏好固化）**：多公司动态拼盘、快讯合集、简讯类文章（如极客公园"微信灰测X；DeepSeek上线Y；车企召回Z"、9点1氪、极客早知道）——**无单篇技术主线、仅罗列资讯**，**不计入早报，直接删除**（物理删除 sources 下 .md → rebuild 重推）。
> - 判定标准：一篇文章包含 ≥3 条互不相关公司/产品动态、且无统一技术主题 → 删除。
> - 例外：**单篇有深度的综述/盘点**（如"普惠金融创新盘点"、某技术年度回顾）若主体明确、有技术分析，仍按正常分类流程处理，不在此列。
> - 此规则覆盖旧版「综合资讯 → 其他」的处理（2026-07-01 旧规已废止）。
> - **边界保留**：单篇含多个 AI 厂商动态但**有统一技术主线/深度分析**的（如"大模型一周进展综述"）不算拼盘，仍按正常分类流程处理，不在此列。
> - **注意**：此类拼盘文即便标题含 AI 厂商名（如"DeepSeek 上线多模态功能"），因无单篇技术主线仍删除——不要因含 AI 关键词就误判入选（与本规则判定标准（≥3 条互不相关动态）一致）。

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
- **无明确公司/机构主体的范式·工程文 → 默认归"国内"**(v3.8 新增,08-13 F04 误判教训):
  - 归属看**来源/作者/会议等语境信号**,不要求正文出现公司名:
    - 中文来源(InfoQ、机器之心、CSDN 等) + 中文作者 / 国内会议(QCon 北京、ArchSummit 中国等) → "国内"
    - 英文来源 + 英文作者 / 国外会议(NeurIPS、Google I/O 等) → "国际"
  - 仅当正文**明确指向国外机构**(如"来自 OpenAI 研究院""Stanford 团队")才归"国际"
  - 例:「从"工具"到"同事"——AI 时代的产品进化」(InfoQ 整理苏杰 QCon 北京演讲)→ 无公司主体,但中文来源+国内会议 → "国内"(is_model_related=false)

**特殊情况**:
| 情况 | 处理 |
|------|------|
| 同业优先 | 同时涉及同业和其他 → 优先"同业" |
| 多主题混合 | 标题含多个不相关新闻 → "其他" |
| 主体与场景区分 | OpenAI 总裁辞职 → "其他"(人事变动) |
| 综合资讯(2026-08-23 改为删除) | 多公司动态拼盘/快讯合集(如"微信灰测X；DeepSeek上线Y；车企召回Z"、"9点1氪"、"极客早知道")→ 🗑️ 删除(见 3.1),不计入早报 |
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
- 简讯综合类文章("9点1氪""极客早知道"等)**现已按 3.1 删除规则移除,不再进入早报**;若个别有深度的单篇盘点需保留,按正常摘要规则撰写~300字中文摘要
- 摘要存入 front matter 的 `digest: |` 字段(多行 YAML)
- **不补充原文没有的信息,不添加主观评价**(v3.3 新增)

### 3.5 同主题合并(方式 A,唯一推荐)

**触发**:多篇报道同一核心事件 → 合并为一条

**写法(通过 merge_plan.json,不要手动改 classification.json)**:
在 `daily/YYYY-MM-DD/merge_plan.json` 的 `merged_groups` 中声明(格式与铁规4 一致):
```json
{
  "merged_groups": [
    {
      "main": "sources/主条文件.md",
      "items": [
        {"source_file": "sources/从条A.md", "name": "公众号A", "link": "原文URL_A"},
        {"source_file": "sources/从条B.md", "name": "公众号B", "link": "原文URL_B"}
      ]
    }
  ]
}
```
- 主条、从条的 `status` 都改 `confirmed`(从条无需改其它 front matter,`is_merged` 由 build 自动标记)
- 主条 `source` 写主来源名(如 "DeepSeek"),**不要**写"多源综合"或逗号拼接

**合并操作(build 自动完成,勿手动)**:
- `build_classification.py` 读 merge_plan.json → 从条标记 `is_merged`+`merged_into`、主条注入 `source_items`
- `generate_html.py` 自动跳过从条,主条渲染多来源标签
- 你**不需要**手动从分类列表移除从条、也**不要**手动构造 classification.json 的合并字段

**废弃写法**(请勿使用):
- ❌ 在 source front matter 写 `is_merged: true`(脚本不读它,无效)
- ❌ 手动在 classification.json 写 `is_merged`/`source_items`/`merged_articles`(应由 build 从 merge_plan.json 生成)
- ❌ `"source": "多源综合"` 或 `"机器之心, 新智元"`(逗号拼接)

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

**实战例(2026-07-02 Meta 三篇)**: 子智能体 1+2 轮都漏了合并,主 Agent 才合并为 1。→ **主 Agent 在 Step 3 内联分类时必须亲自扫一遍同公司同事件合并**(v3.14 起 Step 3 已禁用子 Agent,本条转为"主 Agent 内联时也须亲自扫合并")。

**增量补充批次(2026-08-20 实战)**: 用户手工导入新文章到 sources/ 时,新文章是 `status: pending`,而 Step3 已删除项也保持 `pending`,两者**无法靠 status 区分** → 用 mtime 区分新旧批次(旧删除项 mtime 更早,新导入更晚)。且新导入文章可能与本日**已 confirmed 的旧文章**是同一事件,必须**跨批去重**(例:GPT-6/Astra 停训,1 篇已 confirmed InfoQ + 3 篇新导入量子位/财联社/智东西 → 合并为 1 卡 4 源)。合并时 main 仍选 publish_time 最早,从条**可含已 confirmed 的旧文章**(其 front matter 保持 confirmed,由 build 自动标 is_merged)。

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

**主 Agent 跟踪节奏**:
- ✅ 每轮确认子智能体有进展;无进展明显 → 重发一次 Agent 调用(等价"重 fork")。
- ✅ WorkBuddy:Agent 工具默认前台等待返回,或 `run_in_background` 后台完成自动通知,无需轮询。
- ❌ 不设"每轮必须 X 分钟"硬性门限;质量闸门慢而对优于快而错。

**为什么不限时但要跟读**:
- 分类验证是质量闸门,快而错不如慢而对
- 读全文才能判断同主题/技术归属,只读 title+digest 漏判多
- 跟读 = 避免盲等,但不催促;死等 = 浪费时间但能接收完成事件

### 执行规则（WorkBuddy 适配）

> 本安装版运行在 WorkBuddy。QClaw 的 `sessions_spawn` 在此不可用,改用 **Agent 工具**派生独立子智能体实现「独立 session 复核」(等价于 QClaw 的 spawn 主 agent 独立 session)。

**WorkBuddy 做法**（逐轮调用一次 Agent 工具）:
- 调用 `Agent` 工具,设 `subagent_type="general-purpose"`
- `description`:如 "AI早报第 N 轮分类验证"
- `prompt` 传入完整独立的验证任务:
  1. 读取 `{workspace}/daily/{date}/classification.json` 与全部 `sources/*.md`
  2. 按本文档「第 N 轮」检查项严格逐篇检查(读全文判断技术归属/合并,不只看 title+digest)
  3. 发现不符合的:用 Edit 定点回写 source .md front matter(分类 `category:`/模型标记 `is_model_related:`/来源 `source:`)或 `# ` 标题行(中文化);严禁改 `digest`、严禁整体重写 md
  4. 零错误回复「✅ 第 N 轮通过(零错误)」,否则列出每处修正(文件+字段+旧值→新值)
- 子智能体返回后,主 Agent 必须复核其结论与落地改动(铁规5:子智能体可能活跃错误或静默失败,此前已靠主 Agent 复核拦截过一次误报)
- 某一轮未通过 → 同一轮重跑 Agent,直到零错误才进下一轮

**核心约束不变**:3 轮验证不可省略、不可由主 Agent 自查替代、每轮检查项全过才进下一轮。

### 第 1 轮:删除规则 + 技术/非技术判断

**检查项**:
1. 各分类中有应删除但未删除的(命中删除规则)?→ 将对应 source .md 的 `status` 改为 `pending`(rebuild 后自动移到 `excluded`)
2. 「国际/国内/同业」中有非技术内容?→ 移到「其他」或删除
3. 「其他」中有技术内容被误归入?→ 根据公司属地移到国际/国内/同业
   - ⚠️ **v3.3**：重点检查研发范式、工程实践、系统思维类是否被误归"其他"，必须主动上调
4. ⚠️ **摘要事实核查（2026-08-19 固化）**：逐篇核对 digest 是否**忠实于原文、无凭空捏造的外部信息**。尤其警惕"中文来源报道国外产品"时被注入原文没有的收购/融资/合作/具体数字/时间节点（实战曾发生 Cursor 摘要捏造"被 SpaceX 以600亿美元收购"，原文并无此说）。发现虚构句 → **定点 Edit 该 .md 的 `digest: |` 多行块删改**（保留 `digest: |` 标记与 2 空格缩进，严禁截成 `digest: "|"`）。

**通过条件**:4 项全 ✅,无任何移动/删除/虚构。

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
10. `source` 字段空值?→ 推断补充→**回写到 source .md 的 `source:` front matter**
11. `source_file` 路径无效?→ 修正
12. `stats` 各分类之和 == `total`?→ 重新计算
13. **所有 title 字段不含全英文**?→ 翻译为中文→**回写到 source .md 的 `# ` 标题行**(v3.3/v3.7,参照铁规 6)

**⚠️ v3.7 禁止项**:
- 🚫 **严禁修改 `digest` 字段**（会导致 `|` 截断为空）
- 🚫 **严禁直接修改 classification.json 的 `title`/`category`/`is_model_related`**（必须回写 source .md front matter）

**R3 通过后立即执行**:
```bash
python3 build_classification.py YYYY-MM-DD
python3 generate_html.py YYYY-MM-DD
```

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

**⚠️ v3.7: R3 后强制串联 rebuild**（详见铁规12）。R3 验证通过后，**必须先 rebuild 再 generate**，确保所有回写到 front matter 的修正生效。

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

**标题中文化闸门（push 前必跑，铁规6 机器化）**:
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
python3 -c "
import json,re
d=json.load(open('daily/YYYY-MM-DD/classification.json'))
bad=[a['title'] for cat in ['国际','国内','同业','其他'] for a in d.get(cat,[]) if not re.search(r'[\u4e00-\u9fff]', a.get('title',''))]
print('❌ 全英文标题:', bad) if bad else print('✅ 所有标题含中文')
"
# 命中全英文 → 回到 source .md 改 # H1 标题行为中文 → build_classification.py → generate_html.py → 重跑本闸门
```

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

**Git remote 使用 SSH**(2026-08-20 更新,此前为 HTTPS):
```bash
# 默认使用 SSH（本机 ~/.ssh/id_rsa 已绑定 GitHub 账号 keejo125）
git remote set-url origin git@github.com:keejo125/AI_Daily_For_Bank.git
GIT_SSH_COMMAND="ssh -o ConnectTimeout=25 -o StrictHostKeyChecking=accept-new" git push origin master
```
背景:HTTPS 在本环境持续失败,不是单纯超时——① 出口代理 502(`CONNECT tunnel failed, response 502`);② `could not read Username`(keychain 存的是 qclaw 账号,非沙箱 git 进程读不到凭据)。而 SSH 认证稳定(`ssh -T git@github.com` → "Hi keejo125!")。2026-08-20 用户明确要求改用 SSH,remote 已切 SSH,勿再切回 HTTPS。推送需在**非沙箱**环境执行(沙箱内 DNS/网络被阻断)。

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
