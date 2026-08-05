#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_daily.py —— 把 AI-Daily-for-bank 的每日早报（classification.json）重新组织成
「三驾马车日度趋势泳道图」所需的单一事实源 daily-trends.json。

与月度三驾马车泳道图（前瞻月报/view）完全对齐的思路：
  - 泳道 = 三驾马车下的 12 个细分项（新基建展开 4 子行）。
  - 每条「趋势」是一段时间内反复出现、可归到某个细分的主题（模型名 / 技术方向 / 组织动作…）。
  - 每条趋势按【日】计算生命周期状态，完全照搬月度口径：
        萌芽 = 首现日 == 最新日（即只在最新一天冒头，还没续上）
        持续 = 活跃到最新日且之前就出现过（在发展）
        休眠 = 最后活跃日早于最新日（早期热过、后来消失）
  - 横轴 = 各个日报日（而非月）。

趋势如何来：日报没有像月度那样人工维护的 trends.json，这里用一套「领域主题词表」自动抽取——
  1) TOPIC_SEEDS：三驾马车各细分下「具体到能成为一条趋势」的种子词（领域确定的重要主题）；
  2) EN_PRODUCTS：英文产品/模型/厂商名白名单（带版本号的英文名如 GPT-5 还会被自动捕获）；
  3) 中文新词发现：jieba 抽取的高频名词，仅保留命中强停用词过滤且达到高阈值的，作为补充发现。
  三者合并、按日聚合、过噪声阈值、去重，得到 trends 数组。

用法:
    python3 build_daily.py            # 重新生成 daily-trends.json
    python3 build_daily.py --check    # 仅打印趋势统计与样例，不写文件
    python3 build_daily.py --disc     # 仅打印「中文新词发现」部分，用于调阈值
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DAILY_ROOT = os.path.abspath(os.path.join(HERE, "..", "daily"))
OUT_PATH = os.path.join(HERE, "daily-trends.json")

# ---------------------------------------------------------------------------
# 三驾马车分类体系（与月度三驾马车泳道图保持一致）
# ---------------------------------------------------------------------------
CARRIAGES = [
    {"id": "paradigm", "name": "范式", "color": "#534AB7",
     "subs": ["组织改革", "推广运营", "岗位智能体与技能建设", "人才培养"]},
    {"id": "agent", "name": "智能体能力", "color": "#0F6E56",
     "subs": ["Harness工程能力建设", "智能研发平台Agent能力深化", "多Agent协同与自主交付", "AI自进化闭环"]},
    {"id": "infra", "name": "新基建", "color": "#854F0B",
     "subs": ["模型", "算力", "知识", "安全"]},
]
CARRIAGE_OF_SUB = {sub: c["id"] for c in CARRIAGES for sub in c["subs"]}

SUB_COLORS = {
    "组织改革": "#6E63C4", "推广运营": "#877EDE", "岗位智能体与技能建设": "#9B91E8", "人才培养": "#B3ABEF",
    "Harness工程能力建设": "#2E8B6F", "智能研发平台Agent能力深化": "#39A583",
    "多Agent协同与自主交付": "#57C29E", "AI自进化闭环": "#7FD3B5",
    "模型": "#A85514", "算力": "#B07D12", "知识": "#6E4F2A", "安全": "#9B3B2E",
}
SUB_TINTS = {
    "组织改革": {"bg": "#ECEAF7", "fg": "#412F8F"}, "推广运营": {"bg": "#EEEAFA", "fg": "#4B3DA0"},
    "岗位智能体与技能建设": {"bg": "#F0EDFB", "fg": "#534AB7"}, "人才培养": {"bg": "#F2F0FC", "fg": "#534AB7"},
    "Harness工程能力建设": {"bg": "#E4F1EC", "fg": "#0F6E56"}, "智能研发平台Agent能力深化": {"bg": "#E7F3EF", "fg": "#0F6E56"},
    "多Agent协同与自主交付": {"bg": "#EBF6F1", "fg": "#0F6E56"}, "AI自进化闭环": {"bg": "#EFF9F4", "fg": "#0F6E56"},
    "模型": {"bg": "#F5C4B3", "fg": "#712B13"}, "算力": {"bg": "#FAC775", "fg": "#633806"},
    "知识": {"bg": "#F1E4CB", "fg": "#6E4F2A"}, "安全": {"bg": "#F7C1C1", "fg": "#791F1F"},
}

SOURCES = [
    {"id": "国际", "color": "#185FA5"},
    {"id": "国内", "color": "#993C1D"},
    {"id": "同业", "color": "#3B6D11"},
    {"id": "其他", "color": "#6B6B6B"},
]

# ---------------------------------------------------------------------------
# 关键词分类器（把每篇文章归到细分项，供趋势的 sub 投票；同时作为主题种子来源）
# ---------------------------------------------------------------------------
SUB_KEYWORDS = [
    ("infra", "安全", ["安全", "供应链", "防锁定", "防钳制", "合规", "漏洞", "泄露", "后门", "攻击", "隐私",
                      "加密", "权限", "防护", "风险", "监管", "处罚", "数据保护", "越狱", "注入", "网络攻击",
                      "黑客", "钓鱼", "防务", "审计", "滥用", "封杀", "断供", "制裁", "可信", "自律公约",
                      "反洗钱", "筛查", "风控", "反欺诈", "诈"]),
    ("infra", "算力", ["算力", "GPU", "芯片", "智算", "数据中心", "英伟达", "推理卡", "集群", "信创", "昇腾",
                      "寒武纪", "显卡", "HBM", "液冷", "算力租赁", "云算力", "算力中心", "半导体", "台积电",
                      "晶圆", "光模块", "存力", "存储", "服务器", "机房", "Arm", "CPU", "NPU", "手机芯片",
                      "通信芯片", "光芯片"]),
    ("infra", "模型", ["模型", "GPT", "Claude", "大模型", "Opus", "Gemini", "Qwen", "DeepSeek", "评测", "榜单",
                      "参数", "推理模型", "多模态", "文生图", "文生视频", "图生视频", "视频生成", "训练", "微调",
                      "蒸馏", "上下文", "长上下文", "MoE", "权重", "幻觉", "Llama", "千问", "智谱", "混元", "豆包",
                      "阶跃", "Kimi", "月之暗面", "百川", "MiniMax", "基座模型", "端侧模型", "小模型", "LLM",
                      "开源模型", "发布模型", "模型发布", "模型能力", "Scaling", "RL", "强化学习", "论文", "研究",
                      "基准", "benchmark", "ICML", "NeurIPS", "顶会", "综述", "SOTA", "刷榜", "评测榜", "文心"]),
    ("infra", "知识", ["知识库", "知识工程", "本体", "业务宪法", "隐性知识", "RAG", "检索增强", "知识图谱",
                      "语料", "知识管理", "文档库", "知识沉淀", "记忆", "数据库", "OceanBase", "湖仓", "数据管理",
                      "数仓", "向量"]),
    ("agent", "智能研发平台Agent能力深化", ["平台", "CodeBuddy", "Claude Code", "Cursor", "Copilot", "研发助手",
                                      "IDE", "编程", "代码", "软件开发", "智能体平台", "研发平台", "编辑器",
                                      "程序员", "自动化测试", "代码生成", "补全", "Devin", "编码", "调试", "仓库",
                                      "提交", "PR", "代码审查", "软件工程", "DevOps", "低代码", "Agent编程",
                                      "Codex", "Qoder", "QoderWork", "Qoder Cloud", "开发", "开发者", "软件",
                                      "工程", "GitHub", "插件", "CLI", "研发", "云图", "连接器", "工作助理",
                                      "React", "前端", "Native", "组件", "UI框架", "前端框架"]),
    ("agent", "多Agent协同与自主交付", ["多Agent", "多智能体", "自主交付", "端到端", "协同", "虚拟同事",
                                  "Agent协作", "群智能", "自主", "协作", "数字员工", "虚拟团队", "团队智能体",
                                  "Agent", "智能体", "自主智能体", "智能体协作", "Builder", "生产", "交付",
                                  "数字分身", "AI员工", "数字柜员", "AI同事", "同事"]),
    ("agent", "AI自进化闭环", ["自进化", "自我提升", "自改进", "递归", "自我修复", "自学习", "自我迭代",
                          "自我修正", "自我进化", "自我反思", "自蒸馏"]),
    ("agent", "Harness工程能力建设", ["Harness", "脚手架", "编排", "工作流", "图工程", "工程化", "框架",
                                "工具链", "Agent框架", "Loop", "调度", "流水线", "编排层"]),
    ("paradigm", "组织改革", ["组织", "架构", "部门", "重组", "转型战略", "顶层", "治理", "中台", "集团", "委员会",
                        "一把手", "行长", "董事长", "改革", "体制", "机制", "汇报", "统筹", "成立", "中心",
                        "事业部", "调整", "设立", "AI原生", "经营重构", "全行级", "战略", "AI原生银行", "银行转型",
                        "银行业", "银行AI", "银行卡", "AI信用卡", "投入与收益", "经营底层", "经营逻辑"]),
    ("paradigm", "岗位智能体与技能建设", ["岗位", "技能", "智能体岗位", "上岗", "角色", "培训", "数字人",
                                  "员工", "岗位智能体", "上岗", "AI员工", "数字柜员", "用工", "岗位重塑"]),
    ("paradigm", "人才培养", ["人才", "招聘", "培养", "CAIO", "首席AI", "认证", "校招", "社招", "团队扩充", "人力",
                        "薪酬", "裁员", "录用", "人才争夺", "人力", "组织部", "学堂", "训练营", "实训", "高考",
                        "志愿", "大学", "教育", "学校", "专业"]),
    ("paradigm", "推广运营", ["All in AI", "AI First", "推广", "运营", "落地", "全员", "普及", "应用推广", "规模化",
                        "最佳实践", "标杆", "试点", "全面", "战略共识", "赋能业务", "推广应用", "宣贯", "投产",
                        "应用", "场景", "落地"]),
]

# —— 主题种子词：从分类关键词里挑出「具体到能成为一条趋势」的词，作为强趋势来源 ——
TOPIC_SEEDS = {
    "模型": ["GPT-5", "GPT5", "Opus", "Gemini", "Claude", "Qwen", "千问", "DeepSeek", "Kimi", "智谱", "GLM",
            "混元", "豆包", "阶跃", "百川", "MiniMax", "文心", "多模态", "文生视频", "文生图", "图生视频", "视频生成",
            "推理模型", "开源模型", "端侧模型", "MoE", "Scaling Law", "强化学习", "长上下文", "评测榜", "SOTA",
            "基准测试", "世界模型", "Agent模型", "模型竞赛"],
    "算力": ["英伟达", "NVIDIA", "昇腾", "寒武纪", "信创", "智算中心", "算力中心", "HBM", "光模块", "液冷",
            "台积电", "半导体", "AI芯片", "存力", "GPU", "NPU", "算力租赁", "云算力"],
    "知识": ["知识库", "知识工程", "RAG", "检索增强", "知识图谱", "本体", "业务宪法", "向量数据库", "湖仓", "记忆"],
    "安全": ["供应链安全", "防锁定", "后门", "漏洞", "泄露", "合规", "越狱", "注入", "数据保护", "断供", "制裁", "反洗钱"],
    "Harness工程能力建设": ["Harness", "脚手架", "编排", "工作流", "图工程", "Agent框架", "Loop", "流水线"],
    "智能研发平台Agent能力深化": ["CodeBuddy", "Claude Code", "Cursor", "Copilot", "Codex", "Devin", "Qoder",
                            "GitHub", "代码生成", "IDE", "研发平台", "低代码", "编程", "前端框架"],
    "多Agent协同与自主交付": ["多Agent", "多智能体", "虚拟同事", "自主交付", "端到端", "数字员工", "智能体协作",
                        "群智能", "自主智能体"],
    "AI自进化闭环": ["自进化", "自我提升", "自我改进", "自我修复", "自我迭代", "自我修正", "自我反思", "自蒸馏"],
}

# ---------------------------------------------------------------------------
# 范式（paradigm）专用「事件模板」抽取
# 不再用「落地/治理/人才」这类维度占位词当趋势；改为抽取具体范式动作，
# 同一模板命中的多篇文章聚合成一条以「动作标签」命名的趋势（如「设立AI组织」）。
# 每条模板带一个人类可读的 label；命中即归入对应细分。
# 模板用「共现窗口」正则（.{0,n} 表示中间可夹 n 字），既具体又不过死。
# ---------------------------------------------------------------------------
PARADIGM_TEMPLATES = [
    # —— 组织改革 ——
    ("组织改革", "设立AI组织", [
        r"(设立|成立|组建|新设|增设|挂牌|落地).{0,8}(AI|人工智能|智能).{0,10}(委员会|部门|中心|实验室|研究院|办公室|专班|工作组|事业部|集团|架构)",
        r"(AI|人工智能|智能).{0,8}(委员会|部门|中心|实验室|研究院|办公室|专班|工作组).{0,10}(成立|设立|组建|挂牌)",
        r"AI转型战略(集团|部门|架构|组织)",
    ]),
    ("组织改革", "AI原生战略/经营重构", [
        r"AI原生(银行|战略|转型|经营|组织|架构)",
        r"经营重构|经营底层|经营逻辑",
        r"顶层(组织|设计|架构).{0,6}(AI|人工智能|智能)",
        r"(体制改革|机制改革|治理重构).{0,8}(AI|人工智能|智能)",
        r"(中台|前台|后台).{0,4}(AI|人工智能|智能).{0,8}(重构|重组|改革)",
    ]),
    ("组织改革", "一把手/高管谈AI战略", [
        r"(行长|董事长|CEO|一把手).{0,14}(AI|人工智能|智能).{0,16}(战略|布局|推进|转型|讲话|表示|强调|投入)",
        r"(谈|论|说|指出|强调).{0,10}(AI|人工智能|智能).{0,12}(战略|转型|布局|重构)",
    ]),
    ("组织改革", "AI治理/合规体制", [
        r"(AI|人工智能|智能).{0,6}(治理|监管|体制|机制|立法|标准|规范)",
        r"治理.{0,6}(AI|人工智能|智能)",
    ]),
    # —— 推广运营 ——
    ("推广运营", "All in AI / AI First", [
        r"All in AI|AI First|AI优先|全员.{0,4}(AI|人工智能|智能化)|全员智能化",
    ]),
    ("推广运营", "规模化推广/标杆落地", [
        r"(规模化|全面|普及|大规模|全行级).{0,8}(推广|落地|应用|部署|上线)",
        r"标杆.{0,8}(案例|实践|应用|场景)",
        r"最佳实践.{0,8}(AI|人工智能|智能)",
        r"战略共识|赋能业务|应用推广.{0,6}(全面|规模化)",
        r"(投产|规模化).{0,6}(AI|人工智能|智能).{0,6}(应用|场景|助手)",
    ]),
    # —— 岗位智能体与技能建设 ——
    ("岗位智能体与技能建设", "数字员工/岗位智能体上岗", [
        r"(数字员工|数字人|AI员工|虚拟同事|智能体岗位|岗位智能体|数字柜员|AI同事).{0,12}(上岗|入职|部署|启用|应用|落地|试点)",
        r"(岗位|角色|工种).{0,4}(重塑|重构|再造|升级)",
        r"上下文减法|技能图谱|技能重塑",
    ]),
    ("岗位智能体与技能建设", "CAIO/首席AI任命", [
        r"(CAIO|首席AI|首席人工智能|AI负责人|AI主管).{0,12}(任命|加盟|到位|设立|到任)",
        r"任命.{0,12}(CAIO|首席AI|AI负责人|AI主管)",
    ]),
    # —— 人才培养 ——
    ("人才培养", "AI人才培养/认证", [
        r"(AI|人工智能|智能).{0,6}(人才|培养|认证|培训|实训|训练营|学院)",
        r"人才.{0,4}(争夺|培养|认证|体系|梯队)",
        r"(校招|社招|招聘|录用).{0,10}(AI|人工智能|大模型|智能)",
        r"(CAIO|首席AI).{0,12}(培养|认证|体系|梯队)",
    ]),
]

# 英文产品/模型/厂商白名单（作为趋势；带版本号如 GPT-5 也会被正则自动捕获）
EN_PRODUCTS = set("""
openai anthropic google microsoft meta nvidia xai cursor copilot codex devin qoder replit warp zed
claude gemini deepseek qwen kimi llama minimax manus nexus perplexity midjourney runway mistral cohere
huggingface github gitlab langchain llamaindex pinecone vectara weaviate chroma vllm ollama openrouter
characterai inflection grok bard bardai geminiultra 月之暗面 智谱 百川 阶跃 寒武纪 商汤 科大讯飞
""".split())

# 短英文但确定为趋势的技术词
EN_KEEP = set(["RAG", "MoE", "LoRA", "MCP", "LLM", "GPU", "NPU", "HBM", "SOTA", "TTS", "ASR", "NLP", "CV",
               "API", "SDK", "CLI", "IDE", "Agent", "Loop", "OCR", "ETL", "ACP"])

# 过于宽泛、不适合作为「趋势」的词（即便高频也丢弃）
GENERIC = set("""
模型 大模型 平台 智能体 智能 框架 工具 能力 工程 开发 研究 学习 训练 数据 系统 应用 服务 产品 技术
公司 企业 中国 美国 全球 报告 发布 推出 新 银行 金融 数字 AI 人工智能 分析 用户 场景 方案 市场 行业
领域 时代 未来 生态 布局 合作 上线 升级 支持 开源 融资 收购 获批 首发 重磅 突破 重大 首次 我们 一个
如何 为什么 什么 这些 那些 已经 可以 通过 进行 实现 提供 包括 以及 方面 一种 这个 那个 不是 就是 没有
今天 昨日 近日 本周 本月 年度 季度 消息 资讯 动态 早报 日报 快讯 观点 评论 解读 观察 看看 一文 盘点
团队 生成 提出 正在 提升 理解 架构 真实 项目 联合 进入 持续 自主 手机 开放 测试 范式 极客 亿美元 探索
模式 助手 重新 统一 认为 表示 指出 强调 透露 发现 看到 了解 关注 期待 希望 需要 应该 可能 似乎 据说 据悉
消息 资讯 动态 观点 评论 解读 观察 盘点 一文 一文读懂 正式 宣布 旗下 推出 发布 上线 曝光 传闻 回应 涉嫌
计划 目标 预计 将在 将于 将于 成功 完成 获得 拿下 成为 全球 国内 国际 同业 其他 每日 每周 每月 专题 深度
""".split())

# 中文结巴分词停用词
ZH_STOP = set("""
的 了 是 在 和 与 及 或 也 都 就 而 等 中 为 对 从 到 被 把 让 使 给 向 于 以 之 其 它 他 她 我 你 您
我们 他们 它们 这个 那个 这些 那些 一个 一种 一些 没有 不是 就是 还是 已经 可以 通过 进行 实现 提供 包括
以及 方面 如何 为什么 什么 怎么 哪些 为了 因为 所以 但是 如果 虽然 然而 于是 那么 并且 而且 不过
今天 昨日 近日 本周 本月 年度 季度 消息 资讯 动态 早报 日报 快讯 观点 评论 解读 观察 一文 盘点 一文读懂
表示 认为 指出 强调 透露 发现 看到 了解 关注 期待 希望 需要 应该 可能 似乎 据说 据悉 据 称 名 款 项 位
公司 企业 银行 金融 行业 领域 技术 产品 服务 系统 平台 模型 数据 用户 场景 方案 市场 生态 时代 未来 战略
发布 推出 上线 升级 支持 开源 融资 收购 获批 首发 重磅 突破 重大 首次 落地 应用 智能 能力 工程 框架 工具
团队 生成 提出 正在 提升 理解 架构 真实 项目 联合 进入 持续 自主 手机 开放 测试 范式 极客 亿美元 探索
模式 助手 重新 统一 计划 目标 预计 将在 将于 成功 完成 获得 拿下 成为 正式 宣布 旗下 曝光 传闻 回应 涉嫌
使用 利用 推动 引领 打造 构建 推出 发布 上线 升级 支持 开源 融资 收购 获批 首发 重磅 突破 重大 首次
""".split())

EN_RE = re.compile(r"[A-Za-z][A-Za-z0-9\.\+\-]{1,}")
EN_STOP = set("""
the and for with from this that https www com cn app pro new via use using chat free now get day way
their your our are was were will can may not but you all who how what when where why out up off about
into over after before between during within without against per each both few more most other some
such same own said say says report reports week month year time world china global ai tech news token
agent gpt api sdk ceo app
""".split())


def classify(text):
    if not text:
        return ("uncat", None, True)
    for carriage, sub, kws in SUB_KEYWORDS:
        for kw in kws:
            if kw.lower() in text.lower():
                return (carriage, sub, False)
    return ("uncat", None, True)


def extract_terms(text):
    """从文本抽取候选主题词，返回 [(term, origin, sub_hint), ...]。
    origin: 'seed' | 'en' | 'zh'；sub_hint 仅 seed 有。"""
    terms = []
    low = text.lower()
    # 1) 种子词（强趋势）
    for sub, seeds in TOPIC_SEEDS.items():
        for s in seeds:
            if s.lower() in low:
                terms.append((s, "seed", sub))
    # 2) 英文产品/模型名
    for m in EN_RE.findall(text):
        tok = m.strip(".-+")
        if not tok:
            continue
        tlow = tok.lower()
        if tlow in EN_STOP:
            continue
        has_digit = any(c.isdigit() for c in tok)
        if has_digit or tlow in EN_PRODUCTS or tlow in (x.lower() for x in EN_KEEP):
            terms.append((tok, "en", None))
    # 注：早期版本用 jieba 做中文新词发现，但无命名实体模型时无法区分「趋势主题」与
    # 高频内容词（代码/编程/安全/论文…），噪声过大；中文趋势主题已由 TOPIC_SEEDS 覆盖。
    return terms


def norm_term(t):
    t = t.strip().strip(".-+")
    if re.match(r"^[A-Za-z0-9\.\+\-]+$", t):
        return t.lower()
    return t


def get_categories(data):
    CATS = ["国际", "国内", "同业", "其他"]
    if isinstance(data.get("classification"), dict):
        return {c: data["classification"].get(c, []) or [] for c in CATS}
    return {c: data.get(c, []) or [] for c in CATS}


def load_days():
    result = []
    if not os.path.isdir(DAILY_ROOT):
        print("未找到 daily 目录:", DAILY_ROOT)
        return result
    for name in sorted(os.listdir(DAILY_ROOT)):
        cj = os.path.join(DAILY_ROOT, name, "classification.json")
        if os.path.isfile(cj):
            try:
                with open(cj, "r", encoding="utf-8") as f:
                    data = json.load(f)
                result.append((name, get_categories(data)))
            except Exception as e:
                print(f"跳过 {name}: {e}")
    return result


# 各来源的噪声阈值（days=出现日报天数, docs=命中文章数）
THRESH = {
    "seed": {"days": 1, "docs": 2},   # 种子词很具体，低阈值；但需 days>=2 或 docs>=4 避免单日脉冲
    "en":   {"days": 1, "docs": 2},
    "zh":   {"days": 3, "docs": 6},   # 中文新词发现要求高，宁缺毋滥
}


def detect_trends(items):
    agg = {}
    for it in items:
        text = (it["title"] + " " + it.get("digest", ""))
        for term, origin, sub_hint in extract_terms(text):
            nt = norm_term(term)
            if not nt or len(nt) < 2 or nt in GENERIC:
                continue
            d = agg.setdefault(nt, {"docs": [], "days": set(), "origins": set()})
            d["docs"].append((it["date"], it, sub_hint))
            d["days"].add(it["date"])
            d["origins"].add(origin)

    trends = []
    for term, d in agg.items():
        days = sorted(d["days"])
        th = THRESH["zh"] if d["origins"] == {"zh"} else THRESH["seed"]
        # 单日脉冲抑制：days==1 时需 docs 较高
        if len(days) < th["days"] or len(d["docs"]) < th["docs"]:
            continue
        if len(days) == 1 and len(d["docs"]) < 4:
            continue
        seed_subs = [sh for (_, _, sh) in d["docs"] if sh]
        if seed_subs:
            sub = max(set(seed_subs), key=seed_subs.count)
        else:
            # fallback 投票只参考非范式细分，避免英文/通用词被误归到范式
            vote = [it["sub"] for (_, it, _) in d["docs"]
                    if it.get("sub") and CARRIAGE_OF_SUB.get(it["sub"]) != "paradigm"]
            sub = max(set(vote), key=vote.count) if vote else None
        if sub is None:
            continue
        carriage = CARRIAGE_OF_SUB.get(sub, "uncat")
        if carriage in ("uncat", "paradigm"):
            continue
        sources = sorted({it["source"] for (_, it, _) in d["docs"]})
        daily = {}
        for date, it, _ in d["docs"]:
            daily[date] = daily.get(date, 0) + 1
        daily_list = [{"date": dt, "count": daily[dt]} for dt in days]
        seen = set()
        examples = []
        for date, it, _ in sorted(d["docs"], key=lambda x: x[0]):
            if it["title"] in seen:
                continue
            seen.add(it["title"])
            examples.append({"date": date, "source": it["source"],
                             "title": it["title"], "link": it.get("link", "")})
            if len(examples) >= 6:
                break
        trends.append({
            "term": term, "sub": sub, "carriage": carriage, "origin": sorted(d["origins"]),
            "source": sources, "first": days[0], "last": days[-1],
            "days": days, "daily": daily_list,
            "total": len(d["docs"]), "peak": max(daily.values()), "examples": examples,
        })

    # 去重：短词是长词的近似子集时（重叠>=0.85）并入长词
    trends.sort(key=lambda t: t["total"], reverse=True)
    kept = []
    for t in trends:
        dup = False
        for k in kept:
            if (t["term"] in k["term"] or k["term"] in t["term"]):
                ta = {(dt, id(it)) for dt, it, _ in agg[t["term"]]["docs"]}
                ka = {(dt, id(it)) for dt, it, _ in agg[k["term"]]["docs"]}
                a, b = (ta, ka) if len(ta) <= len(ka) else (ka, ta)
                if a and len(a & b) / len(a) >= 0.85:
                    dup = True
                    break
        if not dup:
            kept.append(t)

    kept.sort(key=lambda t: (t["first"], -t["total"]))
    for i, t in enumerate(kept):
        t["id"] = f"trend-{i+1:03d}"
    return kept


def generate_paradigm_trends(items):
    """用事件模板把文章聚合成范式趋势；同一模板(label)的多篇聚成一条。"""
    groups = {}  # (sub, label) -> [(date, item), ...]
    compiled = [(sub, label, [re.compile(p) for p in pats])
                for sub, label, pats in PARADIGM_TEMPLATES]
    for it in items:
        text = (it["title"] + " " + it.get("digest", ""))
        for sub, label, pats in compiled:           # 取首个命中模板（列表顺序=优先级）
            if any(p.search(text) for p in pats):
                groups.setdefault((sub, label), []).append((it["date"], it))
                break
    trends = []
    for (sub, label), docs in groups.items():
        dates = sorted({d for d, _ in docs})
        first, last = dates[0], dates[-1]
        sources = sorted({it["source"] for _, it in docs})
        daily = {}
        for d, it in docs:
            daily[d] = daily.get(d, 0) + 1
        daily_list = [{"date": dt, "count": daily[dt]} for dt in dates]
        seen, examples = set(), []
        for d, it in sorted(docs, key=lambda x: x[0]):
            if it["title"] in seen:
                continue
            seen.add(it["title"])
            examples.append({"date": d, "source": it["source"],
                             "title": it["title"], "link": it.get("link", "")})
            if len(examples) >= 6:
                break
        total = len(docs)
        conf = round(min(1.0, len(dates) / 3 + total / 12), 2)   # 跨日越多/篇数越多越自信
        trends.append({
            "term": label, "sub": sub, "carriage": "paradigm", "origin": ["tpl"],
            "source": sources, "first": first, "last": last, "days": dates,
            "daily": daily_list, "total": total, "peak": max(daily.values()),
            "examples": examples, "conf": conf, "reviewed": False,
        })
    return trends


FEEDBACK_PATH = os.path.join(HERE, "feedback.json")


def load_feedback():
    if not os.path.isfile(FEEDBACK_PATH):
        return {"paradigm": {}}
    try:
        with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.setdefault("paradigm", {})
        return d
    except Exception:
        return {"paradigm": {}}


def apply_paradigm_feedback(par_trends, fb):
    """根据人工审核覆盖范式趋势：reject 剔除；reclass 改细分；confirm 保留并打标。"""
    out = []
    for t in par_trends:
        rec = fb["paradigm"].get(t["term"])
        if not rec:
            out.append(t)
            continue
        t["reviewed"] = True
        dec = rec.get("decision")
        if dec == "reject":
            continue
        if dec == "reclass" and rec.get("sub") and CARRIAGE_OF_SUB.get(rec["sub"]) == "paradigm":
            t["sub"] = rec["sub"]
        out.append(t)
    return out


def main():
    days = load_days()
    if not days:
        print("没有可处理的日报数据。")
        return

    items = []
    by_source = {s["id"]: 0 for s in SOURCES}
    for date, data in days:
        for cat in ["国际", "国内", "同业", "其他"]:
            for art in data.get(cat, []) or []:
                title = (art.get("title") or "").strip()
                if not title:
                    continue
                digest = (art.get("digest") or "").strip()
                text = title + " " + digest
                carriage, sub, unc = classify(text)
                items.append({
                    "date": date, "title": title, "carriage": carriage, "sub": sub,
                    "source": cat, "unclassified": unc,
                    "link": art.get("link", "") or "", "digest": digest,
                })
                by_source[cat] = by_source.get(cat, 0) + 1

    dates = [d for d, _ in days]
    latest = dates[-1]

    # 范式：事件模板抽取具体动作 → 聚合趋势；再叠加人工审核反馈（人审核 → 智能体调整判断逻辑）
    fb = load_feedback()
    par = apply_paradigm_feedback(generate_paradigm_trends(items), fb)
    trends = detect_trends(items) + par

    for t in trends:
        if t["last"] == latest:
            t["status"] = "萌芽" if t["first"] == t["last"] else "持续"
        else:
            t["status"] = "休眠"

    # 合并后统一排序并分配 id
    trends.sort(key=lambda t: (t["first"], -t["total"]))
    for i, t in enumerate(trends):
        t["id"] = f"trend-{i+1:03d}"

    if "--disc" in sys.argv:
        print("（已停用中文新词发现；趋势仅来自 TOPIC_SEEDS + 英文产品/模型名）")
        return

    meta = {
        "title": "智能研发前瞻 · 三驾马车日度趋势泳道图",
        "subtitle": "范式 / 智能体能力 / 新基建 —— 按日追踪新趋势的萌芽、生长、持续与休眠",
        "updated": latest,
        "days": dates,
        "futureLabel": "待续",
        "carriages": CARRIAGES,
        "lanes": [
            {"id": "paradigm", "label": "范式", "carriage": "paradigm", "expand": False, "color": "#534AB7"},
            {"id": "agent", "label": "智能体能力", "carriage": "agent", "expand": False, "color": "#0F6E56"},
            {"id": "infra", "label": "新基建", "carriage": "infra", "expand": True, "color": "#854F0B"},
        ],
        "subColors": SUB_COLORS,
        "subTints": SUB_TINTS,
        "sources": SOURCES,
        "stats": {
            "dayCount": len(dates),
            "articleCount": len(items),
            "trendCount": len(trends),
            "bySource": by_source,
            "byStatus": {s: sum(1 for t in trends if t["status"] == s) for s in ["萌芽", "持续", "休眠"]},
            "byOrigin": {o: sum(1 for t in trends if o in t["origin"]) for o in ["seed", "en", "zh", "tpl"]},
        },
    }

    if "--check" in sys.argv:
        print(f"天数: {len(dates)}（{dates[0]} ~ {latest}）| 文章: {len(items)} | 趋势: {len(trends)}")
        print("状态分布:", meta["stats"]["byStatus"], "| 来源构成:", meta["stats"]["byOrigin"])
        print("来源:", by_source)
        print("\n--- 趋势样例（按首现日 / 总量）---")
        for t in trends[:50]:
            print(f"  [{t['status']:>2}] {t['first']}~{t['last']} {t['sub']:10} ×{t['total']:>2} {t['term']}  ({'/'.join(t['source'])})")
        return

    payload = {"meta": meta, "trends": trends}
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"已生成 {OUT_PATH}")
    print(f"  · 天数 {len(dates)}（{dates[0]} ~ {latest}）| 文章 {len(items)} | 趋势 {len(trends)}")
    print(f"  · 状态: {meta['stats']['byStatus']} | 来源: {meta['stats']['byOrigin']}")


if __name__ == "__main__":
    main()
