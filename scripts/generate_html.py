#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成日报 HTML 文件
用法: python3 generate_html.py YYYY-MM-DD
"""

import json
import os
import sys
from datetime import datetime


# ===== 大模型关键词列表（不区分大小写） =====
# 核心关键词：直接指向大模型本身的文章
MODEL_CORE_KEYWORDS = [
    # 模型发布/更新
    "发布", "上线", "开源", "更新", "升级", "新版本",
    # 模型评测/性能
    "评测", "benchmark", "榜单", "排名", "测试", "对比",
    # 模型技术特性
    "参数规模", "参数量", "上下文", "token", "训练", "预训练",
    "微调", "对齐", "蒸馏", "量化", "推理能力",
    # 模型架构/类型
    "基座模型", "foundation model", "语言模型", "多模态模型",
    # 具体模型名称（当作为主语时）
    "GPT-5", "GPT-4", "Claude", "Gemini", "Qwen", "通义千问",
    "文心一言", "DeepSeek", "Llama", "Mistral", "Kimi",
]

# 排除关键词：这些词出现时，说明是应用而非模型本身
MODEL_EXCLUDE_PATTERNS = [
    # 应用场景
    "已用", "使用", "应用", "落地", "实践", "案例",
    # 工具/产品集成
    "内置", "支持", "集成", "接入", "搭载", "适配",
    # 行业应用
    "上车", "医疗", "诊室", "医生", "金融", "银行",
    "教育", "法律", "客服", "办公",
    # 非技术性描述
    "杀入", "走进", "进入", "赋能",
]


def print_progress(msg):
    """打印进度信息"""
    print(f"[generate_html] {msg}")


def normalize_chinese_quotes(text):
    """
    标准化中文引号为方括号，避免 JSON 解析错误
    
    generate_html.py 会将中文引号替换为英文引号，这会破坏 JSON 结构。
    因此在写入 classification.json 前，必须将中文引号替换为方括号。
    
    Args:
        text: 原始文本
    Returns:
        处理后的文本
    """
    if not text:
        return text
    # 替换中文双引号 U+201C/U+201D 为方括号
    text = text.replace('\u201c', '【').replace('\u201d', '】')
    # 替换中文单引号 U+2018/U+2019 为方括号
    text = text.replace('\u2018', '「').replace('\u2019', '」')
    return text


def read_file(path, encoding='utf-8'):
    """读取文件内容，处理文件不存在的情况"""
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print_progress(f"警告: 文件不存在 - {path}")
        return None
    except Exception as e:
        print_progress(f"错误: 读取文件失败 {path} - {e}")
        return None


def write_file(path, content, encoding='utf-8'):
    """写入文件内容"""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print_progress(f"错误: 写入文件失败 {path} - {e}")
        return False


def extract_original_url(content):
    """从 markdown 内容中提取原文链接"""
    import re
    match = re.search(r'原文链接[：:]\s*(https?://[^\s>]+)', content)
    return match.group(1) if match else ''


def extract_source_name_from_md(content):
    """从 markdown 内容中提取公众号名称"""
    import re
    match = re.search(r'公众号[：:]\s*(.+)', content)
    return match.group(1).strip() if match else ''


def detect_model_related(title, digest):
    """
    检测文章是否主要讲述大模型本身（而非应用）
    
    判断标准：仅针对模型发布、测评、架构的内容
    - 模型发布：新模型正式发布、版本更新
    - 模型测评：模型性能对比、实测报告  
    - 模型架构：技术论文、架构创新、底层技术研究
    
    不添加标签的内容：
    - AI应用功能（如Chronicle屏幕记忆）
    - 行业资讯（如量化公司创始人背景）
    - 基础设施讨论（如Token工厂概念）
    - 公司动态（如OpenAI裁员、投资并购）
    """
    text = f"{title} {digest}".lower()
    title_lower = title.lower()
    
    # === 明确排除的内容（即使包含模型关键词）===
    
    # 1. 排除产品功能发布（非模型本身）
    if any(kw in text for kw in ["chronicle", "屏幕记忆", "功能", "订阅"]):
        # Chronicle是OpenAI的功能，不是模型
        if "chronicle" in text or ("屏幕记忆" in text and "模型" not in text):
            return False
    
    # 2. 排除基础设施/算力讨论
    if any(kw in text for kw in ["token工厂", "数据中心", "算力", "芯片", "tpu", "gpu"]):
        # 黄仁勋访谈讲Token工厂，不是模型
        if "token工厂" in text or "黄仁勋" in text:
            return False
    
    # 3. 排除行业人物/公司动态
    if any(kw in text for kw in ["创始人", "实习生", "量化", "融资", "投资", "收购", "裁员", "离职"]):
        # 量化公司培养创始人，不是模型
        if "量化" in text and "模型" not in text:
            return False
    
    # 4. 排除企业战略/市场竞争
    if any(kw in text for kw in ["年化收入", "烧钱率", "估值", "市场份额", "反超"]):
        # OpenAI危机四伏讲的是商业竞争，不是模型技术
        if ("openai" in text or "anthropic" in text) and "模型" not in title_lower:
            # 如果标题没有明确提到模型，且内容是商业新闻，排除
            if any(kw in text for kw in ["收入", "估值", "融资", "裁员", "转型"]):
                return False
    
    # === 确认是大模型相关的内容 ===
    
    # 1. 模型发布/更新（必须包含具体模型名称或"模型"字样）
    model_names = ["gpt", "claude", "gemini", "qwen", "deepseek", "llama", "kimi", "mimo", "mistral"]
    has_model_name = any(name in text for name in model_names)
    
    if has_model_name and any(kw in text for kw in ["发布", "上线", "开源", "v4", "v3", "5.5", "新版本"]):
        return True
    
    # 2. 模型评测/对比（必须有"模型"+评测词）
    if "模型" in text and any(kw in text for kw in ["评测", "benchmark", "对比", "实测", "性能"]):
        return True
    
    # 3. 模型架构/技术论文（必须有技术术语）
    if any(kw in text for kw in ["llm dna", "注意力机制", "mla", "muon优化器", "残差连接", "蒸馏", "微调", "系统发育树"]):
        return True
    
    # 4. 标题明确以模型名称开头
    if any(title_lower.startswith(name) for name in model_names):
        return True
    
    # 默认：不是大模型相关内容
    return False


def normalize_for_match(text):
    """标准化文本用于模糊匹配：去空格、去标点、小写"""
    import re
    text = text.lower().strip()
    text = re.sub(r'[\s\-_！？。，、：；""''（）【】《》…—·]+', '', text)
    return text


def find_markdown_file(sources_dir, title, source):
    """
    在 sources 目录下查找匹配的 markdown 文件
    文件名格式: {日期}_{标题}_{来源}.md
    
    匹配策略：
    1. 精确匹配：文件名包含 title 和 source
    2. 来源+关键词匹配：source 匹配 + title 中任一≥4字关键词匹配
    3. 纯来源匹配：source 匹配（多结果时按 title 关键词重叠度排序）
    """
    if not os.path.isdir(sources_dir):
        return None

    md_files = [f for f in os.listdir(sources_dir) if f.endswith('.md')]
    if not md_files:
        return None

    title_norm = normalize_for_match(title)
    source_norm = normalize_for_match(source)

    # 策略1: 精确匹配
    for fname in md_files:
        fname_norm = normalize_for_match(fname)
        if title_norm in fname_norm and source_norm in fname_norm:
            return os.path.join(sources_dir, fname)

    # 策略2: 来源+关键词匹配
    # 从 title 中提取≥4字的候选关键词，长中文串拆为4字滑窗
    import re as _re
    candidates = []
    # 中文词（≥4字，长串拆为4字滑窗）
    cn_runs = _re.findall(r'[\u4e00-\u9fff]+', title)
    for run in cn_runs:
        if len(run) >= 4:
            if len(run) <= 6:
                candidates.append(run)
            else:
                # 滑动窗口，步长2
                for i in range(0, len(run) - 3, 2):
                    candidates.append(run[i:i+4])
    # 英文词（≥3字母）
    en_words = _re.findall(r'[a-zA-Z]{3,}', title)
    keywords = candidates + en_words

    source_matched = []
    for fname in md_files:
        fname_norm = normalize_for_match(fname)
        if source_norm in fname_norm:
            source_matched.append(fname)

    if source_matched and keywords:
        best_match = None
        best_score = 0
        for fname in source_matched:
            fname_norm = normalize_for_match(fname)
            score = sum(1 for kw in keywords if normalize_for_match(kw) in fname_norm)
            if score > best_score:
                best_score = score
                best_match = fname
        if best_match and best_score > 0:
            return os.path.join(sources_dir, best_match)

    # 策略3: 纯来源匹配，多结果时按关键词重叠度排序
    if source_matched:
        if len(source_matched) == 1:
            return os.path.join(sources_dir, source_matched[0])
        # 多个同来源文件，按 title 关键词重叠度排序
        if keywords:
            scored = []
            for fname in source_matched:
                fname_norm = normalize_for_match(fname)
                score = sum(1 for kw in keywords if normalize_for_match(kw) in fname_norm)
                scored.append((score, fname))
            scored.sort(key=lambda x: x[0], reverse=True)
            if scored[0][0] > 0:
                return os.path.join(sources_dir, scored[0][1])
        # 4字关键词无匹配，尝试2字短词补充匹配
        short_kws = []
        cn_runs = _re.findall(r'[\u4e00-\u9fff]+', title)
        for run in cn_runs:
            if len(run) >= 2:
                for i in range(len(run) - 1):
                    short_kws.append(run[i:i+2])
        # 去重，排除通用词
        generic = {'发布','推出','开源','上线','发布前','首次','新增','最新','重要','重大','突破','领先'}
        short_kws = [kw for kw in dict.fromkeys(short_kws) if kw not in generic and len(kw) >= 2]
        if short_kws:
            scored = []
            for fname in source_matched:
                fname_norm = normalize_for_match(fname)
                score = sum(1 for kw in short_kws if normalize_for_match(kw) in fname_norm)
                scored.append((score, fname))
            scored.sort(key=lambda x: x[0], reverse=True)
            if scored[0][0] > 0:
                return os.path.join(sources_dir, scored[0][1])
        # 仍无匹配，返回第一个
        return os.path.join(sources_dir, source_matched[0])

    # 策略4: 仅关键词匹配（无来源匹配时）
    if keywords:
        best_match = None
        best_score = 0
        for fname in md_files:
            fname_norm = normalize_for_match(fname)
            score = sum(1 for kw in keywords if normalize_for_match(kw) in fname_norm)
            if score > best_score:
                best_score = score
                best_match = fname
        if best_match and best_score >= max(1, len(keywords) // 2):
            return os.path.join(sources_dir, best_match)

    return None


def read_article_content(source_file, date_str, title, source):
    """
    读取文章 markdown 内容
    优先使用 source_file，否则尝试查找匹配文件
    """
    # 方案1: 直接使用 source_file（相对 daily/YYYY-MM-DD/ 的路径）
    if source_file:
        base_dir = os.path.join(PROJECT_DIR, 'daily', date_str)
        if os.path.isabs(source_file):
            path = source_file
        else:
            path = os.path.join(base_dir, source_file)
        content = read_file(path)
        if content is not None:
            return content

    # 方案2: 根据 title 和 source 在 sources 目录查找
    # source 可能是合并后的多来源（如"机器之心、极客公园"），需拆分逐个匹配
    sources_dir = os.path.join(PROJECT_DIR, 'daily', date_str, 'sources')
    source_list = [s.strip() for s in source.replace('、', ',').replace('，', ',').split(',') if s.strip()]
    for single_source in source_list:
        matched = find_markdown_file(sources_dir, title, single_source)
        if matched:
            content = read_file(matched)
            if content is not None:
                return content

    return ""


def build_stats_string(stats):
    """构建统计信息字符串"""
    cats = ["国际", "国内", "同业", "其他"]
    parts = []
    for cat in cats:
        count = stats.get(cat, 0)
        if count > 0:
            parts.append(f"{cat} {count} 篇")
    return " · ".join(parts)


def build_articles_json(classification, date_str):
    """
    构建 ARTICLES_JSON 数据
    每个对象包含: title, source, digest, content, category, is_model_related, source_items, publish_time
    source_items: [{name, source_file, link}, ...] 每个来源单独一项
    
    排序规则：在每个分类内，有大模型标签的文章排在前面
    """
    articles = []
    cats = ["国际", "国内", "同业", "其他"]
    base_dir = os.path.join(PROJECT_DIR, 'daily', date_str)
    
    # 读取 articles_raw.json 获取 publish_time
    raw_path = os.path.join(base_dir, 'articles_raw.json')
    time_map = {}
    if os.path.exists(raw_path):
        try:
            with open(raw_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            for article in raw_data.get('articles', []):
                aid = article.get('aid')
                if aid and 'publish_time' in article:
                    time_map[aid] = article['publish_time']
        except Exception as e:
            print_progress(f"警告: 读取 articles_raw.json 失败 - {e}")

    for cat in cats:
        items = classification.get(cat, [])
        cat_articles = []
        
        for item in items:
            title = item.get("title", "")
            source = item.get("source", "")
            digest = item.get("digest", "")
            aid = item.get("aid", "")
            publish_time = time_map.get(aid)  # 获取发布时间戳
            
            # 如果 time_map 中没有，尝试从 classification.json 的 source_file 中提取时间
            # fallback: 如果没有时间，设置为 0（排序时会排在最后）
            if publish_time is None:
                print_progress(f"警告: 文章 '{title[:30]}...' 缺少 publish_time，使用默认值 0")
                publish_time = 0

            # 如果没有 digest，使用 title 兜底
            if not digest:
                digest = title

            # 拆分多来源，逐个匹配 source 文件
            sources_dir = os.path.join(base_dir, 'sources')
            source_list = [s.strip() for s in source.replace('、', ',').replace('，', ',').split(',') if s.strip()]

            source_items = []
            all_content_parts = []

            for single_source in source_list:
                matched = find_markdown_file(sources_dir, title, single_source)
                if matched:
                    relative_path = os.path.relpath(matched, base_dir).replace('\\', '/')
                    file_content = read_file(matched)
                    original_url = extract_original_url(file_content) if file_content else ''
                    source_items.append({
                        "name": single_source,
                        "source_file": relative_path,
                        "link": original_url
                    })
                    if file_content:
                        all_content_parts.append(file_content)
                else:
                    # 未找到文件，仍保留来源标签（不可点击）
                    source_items.append({
                        "name": single_source,
                        "source_file": "",
                        "link": ""
                    })

            # 合并所有来源的原文内容
            content = '\n\n---\n\n'.join(all_content_parts) if all_content_parts else ''

            is_model_related = detect_model_related(title, digest)

            # 兼容旧字段
            primary_source_file = source_items[0]['source_file'] if source_items else ''
            primary_link = source_items[0].get('link', '') if source_items else ''

            cat_articles.append({
                "title": title,
                "source": source,
                "digest": digest,
                "link": primary_link,
                "content": content,
                "category": cat,
                "is_model_related": is_model_related,
                "source_file": primary_source_file,
                "source_items": source_items,
                "publish_time": publish_time  # 添加发布时间戳
            })
        
        # 在当前分类内排序：
        # 1. 有大模型标签的排在前面
        # 2. 同组内按时间从早到晚排序（publish_time小的在前）
        def sort_key(article):
            is_model = article.get("is_model_related", False)
            publish_time = article.get("publish_time", 0) or 0  # 如果没有时间，默认为0
            # 返回元组：(是否非大模型, 发布时间)
            # not is_model: False(大模型)=0, True(非大模型)=1，所以大模型排前面
            # publish_time: 时间戳小的（早的）排前面
            return (not is_model, publish_time)
        
        cat_articles.sort(key=sort_key)
        articles.extend(cat_articles)

    return articles


def build_section_html(category, articles, date_str, classification_data=None):
    """
    生成 fallback section HTML
    参照 template.html 中 #fallback-content 的 CSS 结构
    """
    cat_icons = {
        "国际": "🌍",
        "国内": "🇨🇳",
        "同业": "🏦",
        "其他": "📌"
    }
    cat_labels = {
        "国际": "国际视野",
        "国内": "国内动态",
        "同业": "同业观察",
        "其他": "其他资讯"
    }

    icon = cat_icons.get(category, "")
    label = cat_labels.get(category, category)

    # Section header（参照 #fallback-content .section-header）
    header_html = (
        f'<div class="section-header">'
        f'<div class="section-title">{escape_html(icon + " " + label)}</div>'
        f'</div>'
    )

    # 空分类：返回 header + "暂无"
    if not articles:
        return header_html + '<div class="empty">暂无</div>'

    # 在当前分类内排序：
    # 1. 有大模型标签的排在前面
    # 2. 同组内按时间从早到晚排序
    def sort_key(article):
        is_model = article.get("is_model_related", False)
        publish_time = article.get("publish_time", 0) or 0
        return (not is_model, publish_time)
    
    sorted_articles = sorted(articles, key=sort_key)

    cards_html = []
    for article in sorted_articles:
        title = article.get("title", "")
        source = article.get("source", "")
        digest = article.get("digest", "")
        source_items = article.get("source_items", [])
        publish_time = article.get("publish_time")  # 获取发布时间戳
        
        # 获取文章日期（使用早报日期，即今天）
        article_display_date = classification_data.get("date", date_str) if classification_data else date_str
        
        # 格式化发布时间
        # 早报页面：只显示时间 hh:mm
        publish_time_str = ""
        if publish_time:
            from datetime import datetime
            dt = datetime.fromtimestamp(publish_time)
            publish_time_str = dt.strftime("%H:%M")

        # 多来源标签
        source_tags_html = ''
        if source_items:
            for si in source_items:
                name = si.get("name", "")
                if si.get("source_file"):
                    source_tags_html += f'<a href="../../viewer.html?file=daily/{date_str}/{escape_html(si["source_file"])}" class="source-tag">{escape_html(name)}</a> '
                else:
                    source_tags_html += f'<span class="source-tag">{escape_html(name)}</span> '
        elif source:
            source_tags_html = f'<span class="source-tag">{escape_html(source)}</span>'

        card_html = (
            f'<div class="card">'
            f'<div class="card-title">{escape_html(title)}</div>'
        )
        
        # 早报页面：只显示时间 hh:mm
        if publish_time_str:
            card_html += f'<div class="card-date"><span class="card-time">{publish_time_str}</span></div>'
        elif article_display_date:
            card_html += f'<div class="card-date">{article_display_date}</div>'
        
        card_html += f'{source_tags_html}'
        
        if digest:
            card_html += f'<div class="card-digest">{escape_html(digest)}</div>'
        card_html += '</div>'
        cards_html.append(card_html)

    cards_str = '\n'.join(cards_html)
    return header_html + cards_str


def escape_html(text):
    """转义 HTML 特殊字符"""
    if not text:
        return ""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def detect_placeholders(template):
    """
    检测模板中存在的 section 占位符
    返回: {category: [placeholders]}
    """
    result = {
        "国际": [],
        "国内": [],
        "同业": [],
        "其他": []
    }
    mapping = {
        "国际": ["{{SECTION_INTL}}", "{{SECTION_国际}}"],
        "国内": ["{{SECTION_DOMESTIC}}", "{{SECTION_国内}}"],
        "同业": ["{{SECTION_PEER}}", "{{SECTION_同业}}"],
        "其他": ["{{SECTION_OTHER}}", "{{SECTION_其他}}"]
    }

    for cat, placeholders in mapping.items():
        for ph in placeholders:
            if ph in template:
                result[cat].append(ph)

    return result


def generate_summary(classification):
    """
    从分类数据生成 summary
    取各分类前1-2篇标题拼接，限制总长度
    """
    parts = []
    cats = ["国际", "国内", "同业", "其他"]
    for cat in cats:
        items = classification.get(cat, [])
        for item in items[:2]:
            title = item.get("title", "")
            if title:
                parts.append(title)

    summary = "/".join(parts)
    # 限制长度约 80 字符
    if len(summary) > 80:
        summary = summary[:77] + "..."
    return summary


def get_weekday(date_str):
    """根据日期字符串计算星期几（中文）"""
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return weekdays[dt.weekday()]


def update_daily_index(date_str, report_date_str, stats, summary):
    """更新 daily-index.json
    
    Args:
        date_str: 文章内容日期（昨天）
        report_date_str: 早报日期（今天）
        stats: 分类统计
        summary: 摘要
    """
    index_path = os.path.join(PROJECT_DIR, 'daily-index.json')
    index_data = {"issues": []}

    content = read_file(index_path)
    if content:
        try:
            index_data = json.loads(content)
        except json.JSONDecodeError as e:
            print_progress(f"警告: daily-index.json 解析失败，将重建 - {e}")

    issues = index_data.get("issues", [])
    # 使用早报日期计算星期几
    weekday = get_weekday(report_date_str)

    new_entry = {
        "date": report_date_str,
        "article_date": date_str,  # 添加文章内容日期用于文件夹路径
        "weekday": weekday,
        "stats": stats,
        "summary": summary
    }

    # 查找是否已存在该日期（使用早报日期）
    found = False
    for issue in issues:
        if issue.get("date") == report_date_str:
            issue.update(new_entry)
            found = True
            print_progress(f"更新 daily-index.json 中 {report_date_str} 的条目")
            break

    # 不存在则插入到首位
    if not found:
        issues.insert(0, new_entry)
        print_progress(f"在 daily-index.json 中插入 {report_date_str} 的新条目")

    index_data["issues"] = issues

    if write_file(index_path, json.dumps(index_data, ensure_ascii=False, indent=2)):
        print_progress("daily-index.json 更新完成")
    else:
        print_progress("daily-index.json 更新失败")


def update_search_index(date_str, articles):
    """
    在项目根目录生成/更新 search-index.json
    """
    index_path = os.path.join(PROJECT_DIR, 'search-index.json')
    index_data = {"updated_at": "", "total": 0, "articles": []}

    # 读取现有数据
    content = read_file(index_path)
    if content:
        try:
            index_data = json.loads(content)
        except json.JSONDecodeError as e:
            print_progress(f"警告: search-index.json 解析失败，将重建 - {e}")

    existing_articles = index_data.get("articles", [])

    # 移除同日期的旧数据
    filtered = [a for a in existing_articles if a.get("date") != date_str]
    removed_count = len(existing_articles) - len(filtered)
    if removed_count > 0:
        print_progress(f"从 search-index.json 移除 {date_str} 的 {removed_count} 条旧数据")

    # 构建当天文章数据
    day_articles = []
    for article in articles:
        day_articles.append({
            "date": date_str,
            "title": article.get("title", ""),
            "source": article.get("source", ""),
            "digest": article.get("digest", ""),
            "link": article.get("link", ""),
            "source_file": article.get("source_file", ""),
            "category": article.get("category", ""),
            "is_model_related": article.get("is_model_related", False)
        })

    # 追加当天文章
    filtered.extend(day_articles)

    # 按日期降序排列
    filtered.sort(key=lambda a: a.get("date", ""), reverse=True)

    index_data["updated_at"] = datetime.now().isoformat()
    index_data["total"] = len(filtered)
    index_data["articles"] = filtered

    if write_file(index_path, json.dumps(index_data, ensure_ascii=False, indent=2)):
        print_progress(f"search-index.json 更新完成，共 {len(filtered)} 篇文章")
    else:
        print_progress("search-index.json 更新失败")


def main():
    global PROJECT_DIR

    if len(sys.argv) < 2:
        print("用法: python3 generate_html.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]  # 文章内容日期（昨天）

    # 验证日期格式
    try:
        article_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print_progress(f"错误: 日期格式无效 '{date_str}'，应为 YYYY-MM-DD")
        sys.exit(1)
    
    # 计算早报日期（今天 = 昨天 + 1天）
    from datetime import timedelta
    report_date = article_date + timedelta(days=1)
    report_date_str = report_date.strftime('%Y-%m-%d')

    # 项目根目录
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print_progress(f"项目目录: {PROJECT_DIR}")
    print_progress(f"文章内容日期: {date_str}（昨天）")
    print_progress(f"早报日期: {report_date_str}（今天）")

    # === 1. 读取分类数据 ===
    classification_path = os.path.join(PROJECT_DIR, 'daily', date_str, 'classification.json')
    print_progress(f"读取分类数据: {classification_path}")

    classification_content = read_file(classification_path)
    if classification_content is None:
        print_progress(f"错误: 无法读取分类数据文件")
        sys.exit(1)

    try:
        # 预处理：标准化中文引号为方括号（避免破坏 JSON 结构）
        cleaned = normalize_chinese_quotes(classification_content)
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print_progress(f"错误: classification.json 解析失败 - {e}")
        print_progress("提示: 请检查 JSON 格式，确保所有中文引号已替换为方括号")
        sys.exit(1)

    classification = data.get("classification", {})
    stats = data.get("stats", {})
    
    # 如果 classification 为空，尝试从根级别读取（兼容旧格式）
    if not classification and ("国际" in data or "国内" in data):
        classification = {
            "国际": data.get("国际", []),
            "国内": data.get("国内", []),
            "同业": data.get("同业", []),
            "其他": data.get("其他", [])
        }

    print_progress(f"分类统计: {stats}")
    
    # 保存完整的classification_data用于build_section_html
    classification_data = data

    # === 2. 构建文章数据 ===
    print_progress("构建文章数据并读取原文...")
    articles = build_articles_json(classification, date_str)
    print_progress(f"共处理 {len(articles)} 篇文章")

    # === 3. 读取模板 ===
    template_path = os.path.join(PROJECT_DIR, 'template.html')
    print_progress(f"读取模板: {template_path}")

    template = read_file(template_path)
    if template is None:
        print_progress("错误: 无法读取模板文件")
        sys.exit(1)

    # === 4. 替换占位符 ===
    print_progress("替换模板占位符...")

    # DATE（使用早报日期，即今天）
    template = template.replace("{{DATE}}", report_date_str)
    print_progress("  -> DATE 替换完成")

    # STATS
    stats_str = build_stats_string(stats)
    template = template.replace("{{STATS}}", stats_str)
    print_progress(f"  -> STATS: {stats_str}")

    # ARTICLES_JSON
    articles_json_str = json.dumps(articles, ensure_ascii=False)
    template = template.replace("{{ARTICLES_JSON}}", articles_json_str)
    print_progress("  -> ARTICLES_JSON 替换完成")

    # SECTION 占位符
    placeholders = detect_placeholders(template)
    print_progress("  -> 检测到 Section 占位符:")
    for cat, phs in placeholders.items():
        print_progress(f"      {cat}: {phs}")

    cats = ["国际", "国内", "同业", "其他"]
    for cat in cats:
        cat_articles = [a for a in articles if a.get("category") == cat]
        section_html = build_section_html(cat, cat_articles, date_str, classification_data)

        phs = placeholders.get(cat, [])
        if not phs:
            # 模板中没有该分类的占位符，跳过
            continue

        # 如果同时存在英文和中文占位符：
        # 第一个（优先英文）替换为 HTML，其余替换为空字符串
        for i, ph in enumerate(phs):
            if i == 0:
                template = template.replace(ph, section_html)
            else:
                template = template.replace(ph, "")

        print_progress(f"  -> SECTION_{cat} 替换完成 ({len(cat_articles)} 篇文章)")

    # === 5. 输出 HTML ===
    output_path = os.path.join(PROJECT_DIR, 'daily', date_str, 'index.html')
    print_progress(f"输出 HTML: {output_path}")

    if write_file(output_path, template):
        print_progress("HTML 生成成功!")
    else:
        print_progress("HTML 生成失败!")
        sys.exit(1)

    # === 6. 更新 search-index.json ===
    print_progress("更新 search-index.json...")
    update_search_index(date_str, articles)

    # === 7. 更新 daily-index.json ===
    print_progress("更新 daily-index.json...")
    summary = generate_summary(classification)
    update_daily_index(date_str, report_date_str, stats, summary)

    print_progress("全部完成!")


if __name__ == "__main__":
    main()
