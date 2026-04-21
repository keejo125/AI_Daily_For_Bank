#!/usr/bin/env python3
"""
智能研发早报生成脚本 v3 — 基于模板

Step 1 (无参数): 拉元数据 → 过滤 → 输出候选清单 + 保存JSON
Step 2 (--classify): 读模板 → 注入数据 → 生成 index.html + 微信摘要
"""
import sqlite3, json, re, os, sys
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = "/tmp/rss.db"
PROJECT_DIR = Path("/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank")
TEMPLATE_FILE = PROJECT_DIR / "template.html"
CACHE_FILE = Path("/tmp/daily_report_cache.json")


# ---------- 共用工具 ----------

def calc_timestamp(date_str):
    """计算日期的Unix时间戳（上海时区），date_str 为汇总日期（早报日期-1天）"""
    import subprocess
    start = int(subprocess.check_output(
        ["date", "-jf", "%Y-%m-%d", date_str, "+%s"]).strip())
    return start, start + 86399


def fetch_meta(start_ts, end_ts):
    """拉元数据（5字段：aid/title/source/link/digest），用|||分隔符避免多行截断"""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    rows = db.execute("""
        SELECT a.aid, a.title, s.nickname as source, a.link, a.digest
        FROM articles a
        JOIN subscriptions s ON a.fakeid = s.fakeid
        WHERE a.publish_time BETWEEN ? AND ?
        ORDER BY a.publish_time DESC
    """, (start_ts, end_ts)).fetchall()
    db.close()
    return [dict(r) for r in rows]


def filter_articles(articles):
    """关键词过滤 + 财经排除"""
    include_kw = [
        '大模型', 'AI', '智能体', 'Agent', 'LLM',
        'GPT', 'Claude', '编码', '编程', '代码生成', 'Copilot',
        'Coding', 'SWE', 'RAG', '推理', '模型', '智能研发', '智能办公',
        '智能运维', '模型发布', 'benchmark', '开源'
    ]
    exclude_kw = [
        '融资', '净利润', '财报', '营收', '市值', '股价',
        'IPO', '上市', '申购', '涨幅', '跌幅', '收盘',
        '买入', '卖出', '评级', '目标价', '追投', '投资额'
    ]

    filtered, excluded = [], []
    for a in articles:
        text = (a['title'] or '') + (a['digest'] or '')
        if not any(kw.lower() in text.lower() for kw in include_kw):
            excluded.append(a)
            continue
        if any(kw in text for kw in exclude_kw):
            excluded.append(a)
            continue
        filtered.append(a)
    return filtered, excluded


def auto_classify(article):
    """自动分类（粗粒度，用户会校正）"""
    text = ((article.get('digest') or '') + (article.get('title') or '')).lower()

    bank_kw = ['银行', '金融', 'atm', '风控', '智能客服', '信贷', '理财',
               '网点', '柜面', '反欺诈', '反洗钱', '信用卡']
    intl_kw = ['openai', 'anthropic', 'google', 'meta ', 'deepmind',
               'stability', 'mistral', 'cohere', 'x.ai', 'apple ', 'nvidia',
               'claude', 'gpt', 'gemini', 'grok', 'strawberry']
    domestic_kw = ['阿里', '腾讯', '百度', '字节', '华为', '智谱', '商汤',
                   '深度求索', '月之暗面', 'minimax', '阶跃', '面壁',
                   '百川', '360', '科大讯飞', '蚂蚁',
                   'qwen', '通义', '腾讯混元', '灵犀', '文心', '荣耀',
                   '小米', 'oppo', 'vivo', '中兴']

    if any(kw in text for kw in bank_kw):
        return '同业'
    if any(kw in text for kw in intl_kw):
        return '国际'
    if any(kw in text for kw in domestic_kw):
        return '国内'
    return '其他'


def auto_tag(article):
    """🤖标签：模型发布/评测/架构突破"""
    text = ((article.get('digest') or '') + (article.get('title') or '')).lower()
    model_kw = ['发布', '评测', '基准', 'benchmark', '排名第一',
                '超越', '架构', '参数规模', '开源', 'gpt-', 'claude',
                'opus', 'sonnet', 'qwen3', 'qwen2', 'gemini', 'deepseek',
                'llama', 'mistral', 'grok', 'Scaling', '训练']
    return any(kw in text for kw in model_kw)


def build_slug(title):
    """从标题提取关键词用于去重匹配"""
    text = re.sub(r'^(刚刚|独家|突发|重磅)', '', title)
    return re.sub(r'[^\w]', '', text)[:18].lower()


def detect_dup_sources(articles):
    """检测同一事件的多来源报道"""
    groups = {}
    for a in articles:
        slug = build_slug(a['title'])
        if slug not in groups:
            groups[slug] = []
        groups[slug].append(a)
    return {k: v for k, v in groups.items() if len(v) > 1}


def format_digest(article, max_len=150):
    """格式化摘要：优先用digest，截断到max_len"""
    d = (article.get('digest') or '').strip()
    if d:
        return d[:max_len] + ('...' if len(d) > max_len else '')
    return article.get('title', '')


# ---------- Step 1 ----------

def step1_run(date_str):
    """拉元数据 → 初筛 → 输出候选清单"""
    start_ts, end_ts = calc_timestamp(date_str)
    print(f"📡 拉取 {date_str} 的文章...")

    articles = fetch_meta(start_ts, end_ts)
    print(f"   原始: {len(articles)} 篇")

    filtered, excluded = filter_articles(articles)
    print(f"   初筛: {len(filtered)} 篇（剔除 {len(excluded)} 篇财经/非AI）")

    for a in filtered:
        a['_auto_cat'] = auto_classify(a)
        a['_auto_tag'] = auto_tag(a)

    cache = {
        'date_str': date_str,
        'start_ts': start_ts,
        'end_ts': end_ts,
        'articles': filtered
    }
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    dups = detect_dup_sources(filtered)
    if dups:
        print(f"\n🔗 检测到 {len(dups)} 组多源报道：")
        for slug, arts in dups.items():
            sources = [a['source'] for a in arts]
            print(f"   → {arts[0]['title'][:40]}... ({', '.join(sources)})")

    print_candidates(filtered, date_str)
    print(f"\n✅ Step 1 完成。")
    print(f"   告诉我分类：python3 daily_report.py {date_str} --classify '国际:aid1,aid2;国内:aid3;其他:aid4'")


def print_candidates(articles, date_str):
    print(f"\n{'='*60}")
    print(f"📋 {date_str} 候选文章清单（{len(articles)} 篇）")
    print(f"{'='*60}")
    for i, a in enumerate(articles, 1):
        digest = format_digest(a, 180).replace('\n', ' ').strip()
        tag = '🤖' if a.get('_auto_tag') else '  '
        cat = a.get('_auto_cat', '?')
        print(f"\n[{i}] {a['title']}")
        print(f"    来源：{a['source']} | 分类：{cat} {tag}")
        print(f"    摘要：{digest}")
        print(f"    ID: {a['aid']}")


# ---------- Step 2 ----------

def step2_run(date_str, classify_str):
    """读模板 → 注入数据 → 生成 HTML + 微信摘要"""
    if not CACHE_FILE.exists():
        print("❌ 未找到缓存，请先运行 Step 1（无参数）")
        sys.exit(1)

    with open(CACHE_FILE, encoding='utf-8') as f:
        cache = json.load(f)

    # 解析分类
    categorized = {cat: [] for cat in ['国际', '国内', '同业', '其他']}
    for group in classify_str.split(';'):
        if ':' not in group:
            continue
        cat, id_list = group.split(':', 1)
        cat = cat.strip()
        if cat not in categorized:
            print(f"⚠️ 未知分类: {cat}")
            continue
        for aid in id_list.split(','):
            aid = aid.strip()
            if not aid:
                continue
            article = next((a for a in cache['articles'] if a['aid'] == aid), None)
            if article:
                categorized[cat].append(article)
            else:
                print(f"⚠️ 未找到文章: {aid}")

    total = sum(len(v) for v in categorized.values())
    print(f"\n📊 分类统计：", end='')
    for cat, items in categorized.items():
        print(f" {cat}{len(items)}篇", end='')
    print(f"，共{total}篇")

    # 多源检测
    dups = detect_dup_sources(sum(categorized.values(), []))
    if dups:
        print(f"\n🔗 多源事件（{len(dups)}组）：")
        for slug, arts in dups.items():
            sources = [f"{a['source']}({a['title'][:20]}...)" for a in arts]
            print(f"   → {', '.join(sources)}")

    # 生成 HTML（读模板）
    html = build_html_from_template(categorized, date_str)
    html_path = PROJECT_DIR / "daily" / date_str / "index.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n📄 HTML: {html_path}")

    # 输出微信摘要
    summary = build_summary(categorized, dups, date_str)
    print(f"\n{'='*60}")
    print("📱 微信摘要（复制发送）：")
    print("="*60)
    print(summary)


def build_html_from_template(categorized, date_str):
    """读取模板，注入数据，生成 index.html"""
    if not TEMPLATE_FILE.exists():
        print(f"❌ 模板文件不存在: {TEMPLATE_FILE}")
        sys.exit(1)

    with open(TEMPLATE_FILE, encoding='utf-8') as f:
        template = f.read()

    # 构建统计行
    stats_parts = []
    for cat in ['国际', '国内', '同业', '其他']:
        n = len(categorized[cat])
        if n > 0:
            stats_parts.append(f"{cat} {n} 篇")
    stats_str = ' · '.join(stats_parts)

    # 构建 articles JSON
    articles_list = []
    for cat, items in categorized.items():
        for item in items:
            articles_list.append({
                'title': item['title'],
                'source': item['source'],
                'digest': format_digest(item, 200),
                'link': item['link'],
                'content': '',  # 前端按需通过 marked.js 渲染 digest
                'category': cat,
                'tag': '🤖' if item.get('_auto_tag') else ''
            })

    articles_json = json.dumps(articles_list, ensure_ascii=False)

    # 替换模板占位符
    html = template.replace('{{DATE}}', date_str)
    html = html.replace('{{STATS}}', stats_str)
    html = html.replace('{{ARTICLES_JSON}}', articles_json)

    # 预渲染分类section骨架（防JS失效时仍有内容显示）
    cat_labels = {
        '国际': '🌍 国际视野',
        '国内': '🇨🇳 国内动态',
        '同业': '🏦 同业观察',
        '其他': '📌 其他'
    }
    cat_section_ids = {'国际': 'section-intl', '国内': 'section-domestic',
                        '同业': 'section-peer', '其他': 'section-other'}
    for cat, label in cat_labels.items():
        items = categorized[cat]
        sid = cat_section_ids[cat]
        if not items:
            placeholder = '<div id="' + sid + '"><div class="empty">暂无</div></div>'
        else:
            cards = []
            for item in items:
                digest = format_digest(item, 200)
                tag = '🤖 ' if item.get('_auto_tag') else ''
                cards.append('<div class="card"><div class="card-inner" onclick="this.classList.toggle(\'expanded\')">' +
                    '<div class="card-title">' + tag + item['title'] + '</div>' +
                    '<span class="source-tag">' + item['source'] + '</span>' +
                    '<div class="card-digest">' + digest + '</div>' +
                    '<div class="card-content"><a href="' + item['link'] + '" target="_blank">📖 微信原文</a></div>' +
                    '</div></div>')
            placeholder = ('<div id="' + sid + '"><div class="section"><h2>' + label + '</h2>' +
                          ''.join(cards) + '</div></div>')
        marker = '{{SECTION_' + cat.upper() + '}}'
        html = html.replace(marker, placeholder)

    # 清理未替换的占位符
    html = re.sub(r'\{\{SECTION_\w+\}\}', '', html)

    return html


def build_summary(categorized, dups, date_str):
    """构建微信摘要文本"""
    cat_icons = {'国际': '🌍', '国内': '🇨🇳', '同业': '🏦', '其他': '📌'}
    lines = [f"【{date_str} 智能研发早报】", ""]

    stats_parts = []
    for cat in ['国际', '国内', '同业', '其他']:
        n = len(categorized[cat])
        if n > 0:
            stats_parts.append(f"{cat_icons[cat]} {n}篇")
    lines.append(' · '.join(stats_parts))
    lines.append("")

    for cat in ['国际', '国内', '同业', '其他']:
        items = categorized[cat]
        if not items:
            continue
        lines.append(f"{cat_icons[cat]} {cat}（{len(items)}篇）：")
        for item in items:
            digest = format_digest(item, 120).replace('\n', '').strip()
            lines.append(f"  • {item['title']}")
            lines.append(f"    [{item['source']}] {digest}")
        lines.append("")

    if dups:
        lines.append("🔗 多源报道（合并阅读）：")
        for slug, arts in dups.items():
            sources = [a['source'] for a in arts]
            main_digest = format_digest(arts[0], 100).replace('\n', '')
            lines.append(f"  ★ {arts[0]['title']}")
            lines.append(f"    多方报道：{', '.join(sources)}")
            lines.append(f"    摘要：{main_digest}")

    return '\n'.join(lines)


# ---------- main ----------

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 daily_report.py YYYY-MM-DD")
        print("  python3 daily_report.py YYYY-MM-DD --classify '国际:aid1;国内:aid2'")
        sys.exit(1)

    date_str = sys.argv[1]
    if '--classify' in sys.argv:
        idx = sys.argv.index('--classify')
        step2_run(date_str, sys.argv[idx + 1] if idx + 1 < len(sys.argv) else '')
    else:
        step1_run(date_str)


if __name__ == "__main__":
    main()
