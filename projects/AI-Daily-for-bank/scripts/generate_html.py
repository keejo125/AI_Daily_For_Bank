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

# 全局变量
PROJECT_DIR = ""
DATE_STR = ""


# ===== 大模型关键词列表（不区分大小写） =====
MODEL_KEYWORDS = [
    "大模型", "LLM", "GPT", "Claude", "Gemini", "Qwen", "通义", "文心",
    "DeepSeek", "Llama", "Mistral", "模型发布", "模型评测", "benchmark",
    "参数规模", "开源模型", "基座模型", "foundation model", "语言模型"
]


def print_progress(msg):
    """打印进度信息"""
    print(f"[generate_html] {msg}")


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


def detect_model_related(title, digest):
    """检测文章是否涉及大模型"""
    text = f"{title} {digest}".lower()
    return any(kw.lower() in text for kw in MODEL_KEYWORDS)


def find_markdown_file(sources_dir, title, source):
    """
    在 sources 目录下查找匹配的 markdown 文件
    文件名格式: {日期}_{标题}_{来源}.md
    """
    if not os.path.isdir(sources_dir):
        return None

    # 获取所有 .md 文件
    md_files = [f for f in os.listdir(sources_dir) if f.endswith('.md')]

    # 优先精确匹配: 文件名包含 title 和 source
    for fname in md_files:
        if title in fname and source in fname:
            return os.path.join(sources_dir, fname)

    # 模糊匹配: 文件名包含 source
    for fname in md_files:
        if source in fname:
            return os.path.join(sources_dir, fname)

    # 如果只有一个 .md 文件，直接返回（兜底）
    if len(md_files) == 1:
        return os.path.join(sources_dir, md_files[0])

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
    sources_dir = os.path.join(PROJECT_DIR, 'daily', date_str, 'sources')
    matched = find_markdown_file(sources_dir, title, source)
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
    每个对象包含: title, source, digest, link, content, category, is_model_related, source_file
    支持多来源合并：source_items 字段（从 classification.json 中读取）
    """
    articles = []
    cats = ["国际", "国内", "同业", "其他"]
    base_dir = os.path.join(PROJECT_DIR, 'daily', date_str)

    for cat in cats:
        items = classification.get(cat, [])
        
        # 先对文章排序：大模型相关文章优先
        items_sorted = sorted(items, key=lambda x: x.get('is_model_related', False), reverse=True)
        
        for item in items_sorted:
            title = item.get("title", "")
            source = item.get("source", "")
            link = item.get("link", "")
            digest = item.get("digest", "")
            is_model_related = item.get("is_model_related", False)
            is_merged = item.get("is_merged", False)
            merged_articles = item.get("merged_articles", [])
            
            if is_merged and len(merged_articles) > 1:
                # 合并文章：构建 source_items
                source_items = []
                for merged_art in merged_articles:
                    source_items.append({
                        'name': merged_art.get('source', ''),
                        'source_file': '',  # 合并文章没有单独的 source_file
                        'link': merged_art.get('link', '')
                    })
                
                # 使用第一个合并文章的 link 作为主链接
                main_link = merged_articles[0].get('link', '')
                
                # 尝试读取原文（如果有 source_file）
                content = read_article_content(
                    item.get('source_file', ''),
                    date_str,
                    title,
                    source
                )
                
                articles.append({
                    "title": title,
                    "source": source,
                    "digest": digest,
                    "link": main_link,
                    "content": content,
                    "category": cat,
                    "is_model_related": is_model_related,
                    "source_file": item.get('source_file', ''),
                    "source_items": source_items  # 多来源标签
                })
            else:
                # 单个文章，保持原有逻辑
                item_title = item.get("title", "")
                source = item.get("source", "")
                link = item.get("link", "")
                item_digest = item.get("digest", "")
                source_file = item.get("source_file", "")

                # 如果没有 digest，使用 title 兜底
                if not item_digest:
                    item_digest = item_title

                # 读取 markdown 原文
                content = read_article_content(source_file, date_str, item_title, source)

                # 如果没有 source_file，尝试在 sources 目录匹配
                if not source_file:
                    sources_dir = os.path.join(base_dir, 'sources')
                    matched = find_markdown_file(sources_dir, item_title, source)
                    if matched:
                        source_file = os.path.relpath(matched, base_dir).replace('\\', '/')

                # 优先使用 classification.json 中的 is_model_related 标签
                if 'is_model_related' in item:
                    is_model_related = item['is_model_related']
                else:
                    is_model_related = detect_model_related(item_title, item_digest)

                articles.append({
                    "title": item_title,
                    "source": source,
                    "digest": item_digest,
                    "link": link,
                    "content": content,
                    "category": cat,
                    "is_model_related": is_model_related,
                    "source_file": source_file
                })

    return articles


def group_articles_by_topic(articles):
    """
    将文章按主题分组，用于合并显示
    返回: [{title, digest, articles: [...], is_merged: bool}, ...]
    """
    # 定义合并规则
    merge_rules = [
        {
            'name': 'GPT-5.5 Instant',
            'keywords': ['GPT-5.5'],
            'match_mode': 'any',  # 包含任一关键词即可
            'merged_title': 'OpenAI发布GPT-5.5 Instant：幻觉降52%，全员免费推出',
        },
        {
            'name': 'OpenAI手机',
            'keywords': ['OpenAI', '手机'],
            'match_mode': 'all',  # 需要同时包含所有关键词
            'merged_title': 'OpenAI首款AI手机曝光：最快明年量产，预计出货3000万台',
        },
        {
            'name': 'xAI离职事件',
            'keywords': ['xAI', '马斯克'],
            'match_mode': 'any',
            'merged_title': 'xAI人事动荡：多位联创同日离职，马斯克600亿拉来Cursor重建',
        },
        {
            'name': 'DeepSeek融资',
            'keywords': ['DeepSeek', '融资'],
            'match_mode': 'all',
            'merged_title': 'DeepSeek启动创纪录融资：梁文锋出资200亿，总额500亿估值飙至3500亿',
        },
        {
            'name': 'OpenAI翁家翌研究',
            'keywords': ['翁家翌'],
            'match_mode': 'any',
            'merged_title': 'OpenAI研究员翁家翌提出AI训练新范式：不更新参数的强化学习方法',
        }
    ]
    
    grouped = []  # 已分组的文章aid
    result = []   # 分组结果
    
    for rule in merge_rules:
        matched_articles = []
        for article in articles:
            title = article.get('title', '')
            # 根据match_mode决定匹配逻辑
            if rule.get('match_mode') == 'all':
                # AND逻辑：必须包含所有关键词
                if all(kw in title for kw in rule['keywords']):
                    matched_articles.append(article)
            else:
                # OR逻辑：包含任一关键词即可
                if any(kw in title for kw in rule['keywords']):
                    matched_articles.append(article)
        
        if len(matched_articles) >= 2:
            # 合并摘要
            digests = [a.get('digest', '') for a in matched_articles if a.get('digest')]
            merged_digest = '；'.join(digests[:2])  # 取前两个摘要
            
            result.append({
                'title': rule['merged_title'],
                'digest': merged_digest,
                'articles': matched_articles,
                'is_merged': True
            })
            
            # 记录已分组的aid
            for a in matched_articles:
                grouped.append(a.get('aid'))
    
    # 未匹配的文章单独显示
    for article in articles:
        if article.get('aid') not in grouped:
            result.append({
                'title': article.get('title', ''),
                'digest': article.get('digest', ''),
                'articles': [article],
                'is_merged': False
            })
    
    return result


def build_section_html(category, articles):
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

    cards_html = []
    
    # 先对文章进行分组
    grouped_articles = group_articles_by_topic(articles)
    
    for group in grouped_articles:
        title = group['title']
        digest = group['digest']
        article_list = group['articles']
        is_merged = group['is_merged']
        
        card_html = f'<div class="card">'
        card_html += f'<div class="card-title">{escape_html(title)}</div>'
        
        # 如果是合并的卡片，显示多个公众号标签
        if is_merged and len(article_list) > 1:
            sources_html = '<div class="source-tags">'
            for article in article_list:
                source = article.get('source', '')
                link = article.get('link', '')
                source_file = article.get('source_file', '')
                
                # 优先使用 viewer.html 查看原文
                if source_file:
                    viewer_link = f'../viewer.html?file=daily/{DATE_STR}/{source_file}'
                    sources_html += f'<span class="source-tag"><a href="{escape_html(viewer_link)}" target="_blank">{escape_html(source)}</a></span>'
                elif link:
                    sources_html += f'<span class="source-tag"><a href="{escape_html(link)}" target="_blank">{escape_html(source)}</a></span>'
                else:
                    sources_html += f'<span class="source-tag">{escape_html(source)}</span>'
            sources_html += '</div>'
            card_html += sources_html
        else:
            # 单个文章，显示单个标签
            source = article_list[0].get('source', '')
            card_html += f'<span class="source-tag">{escape_html(source)}</span>'
        
        if digest:
            card_html += f'<div class="card-digest">{escape_html(digest)}</div>'
        
        # 添加查看原文链接（仅对未合并的或使用第一个文章的链接）
        if not is_merged:
            link = article_list[0].get('link', '')
            if link:
                card_html += (
                    f'<div style="margin-top:8px;">'
                    f'<a href="{escape_html(link)}" target="_blank">📖 微信原文</a>'
                    f'</div>'
                )
        
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


def update_daily_index(date_str, stats, summary):
    """
    更新 daily-index.json
    
    Args:
        date_str: 文章日期（文件夹名称）
        stats: 分类统计
        summary: 摘要
        
    Note:
        前端会自动将 date + 1天作为早报显示日期
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
    weekday = get_weekday(date_str)

    new_entry = {
        "date": date_str,
        "weekday": weekday,
        "stats": stats,
        "summary": summary
    }

    # 查找是否已存在该日期
    found = False
    for issue in issues:
        if issue.get("date") == date_str:
            issue.update(new_entry)
            found = True
            print_progress(f"更新 daily-index.json 中 {date_str} 的条目")
            break

    # 不存在则插入到首位
    if not found:
        issues.insert(0, new_entry)
        print_progress(f"在 daily-index.json 中插入 {date_str} 的新条目")

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
    global PROJECT_DIR, DATE_STR

    if len(sys.argv) < 2:
        print("用法: python3 generate_html.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]
    DATE_STR = date_str  # 设置全局变量

    # 验证日期格式
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print_progress(f"错误: 日期格式无效 '{date_str}'，应为 YYYY-MM-DD")
        sys.exit(1)

    # 项目根目录
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print_progress(f"项目目录: {PROJECT_DIR}")
    print_progress(f"生成日期: {date_str}")

    # === 1. 读取分类数据 ===
    classification_path = os.path.join(PROJECT_DIR, 'daily', date_str, 'classification.json')
    print_progress(f"读取分类数据: {classification_path}")

    classification_content = read_file(classification_path)
    if classification_content is None:
        print_progress(f"错误: 无法读取分类数据文件")
        sys.exit(1)

    try:
        data = json.loads(classification_content)
    except json.JSONDecodeError as e:
        print_progress(f"错误: classification.json 解析失败 - {e}")
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

    # DATE
    template = template.replace("{{DATE}}", date_str)
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
        section_html = build_section_html(cat, cat_articles)

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
    update_daily_index(date_str, stats, summary)

    print_progress("全部完成!")


if __name__ == "__main__":
    main()
