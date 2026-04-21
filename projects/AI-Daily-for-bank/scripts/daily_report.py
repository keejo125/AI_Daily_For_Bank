#!/usr/bin/env python3
"""
智能研发早报生成脚本 v2

Step 1 (无参数): 拉元数据 → 过滤 → 输出候选清单 + 保存JSON
Step 2 (--classify): 读取缓存 → 生成HTML + 摘要文本
                    多源事件自动合成一句话
"""
import sqlite3, json, re, os, sys, textwrap
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = "/tmp/rss.db"
PROJECT_DIR = Path("/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank")
CACHE_FILE = Path("/tmp/daily_report_cache.json")

# ---------- 共用工具 ----------

def calc_timestamp(date_str):
    """计算日期的Unix时间戳（上海时区）"""
    import subprocess
    start = int(subprocess.check_output(
        ["date", "-jf", "%Y-%m-%d", f"{date_str}", "+%s"]).strip())
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
    include_kw = ['大模型', 'AI', '智能体', 'Agent', 'LLM',
                  'GPT', 'Claude', '编码', '编程', '代码生成', 'Copilot',
                  'Coding', 'SWE', 'RAG', '推理', '模型']
    exclude_kw = ['融资', '净利润', '财报', '营收', '市值', '股价',
                  'IPO', '上市', '申购', '涨幅', '跌幅', '收盘',
                  '买入', '卖出', '评级', '目标价']

    filtered, excluded = [], []
    for a in articles:
        text = (a['title'] or '') + (a['digest'] or '')
        if not any(kw.lower() in text.lower() for kw in include_kw):
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
               '网点', '柜面', '反欺诈', '反洗钱']
    intl_kw = ['openai', 'anthropic', 'google', 'meta ', 'deepmind',
               'stability', 'mistral', 'cohere', 'x.ai', 'apple ', 'nvidia',
               'claude', 'gpt', 'gemini', 'grok', 'strawberry',
               'openai的', 'anthropic的']
    domestic_kw = ['阿里', '腾讯', '百度', '字节', '华为', '智谱', '商汤',
                   '深度求索', '月之暗面', 'minimax', '阶跃', '面壁',
                   '百川', '360', '科大讯飞', '蚂蚁',
                   'qwen', '通义', '腾讯混元', '灵犀', '文心']

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
    # 移除常见前缀和语气词
    text = re.sub(r'^(刚刚|独家|突发|重磅|刚刚|都在说|都在看)', '', title)
    # 提取前6个字符作为slug（跳过标点）
    slug = re.sub(r'[^\w]', '', text)[:18]
    return slug.lower()

def detect_dup_sources(articles):
    """检测同一事件的多来源报道（按标题关键词分组）"""
    groups = {}
    for a in articles:
        slug = build_slug(a['title'])
        if slug not in groups:
            groups[slug] = []
        groups[slug].append(a)

    # 返回有多来源的组
    return {k: v for k, v in groups.items() if len(v) > 1}

def format_digest(article, max_len=150):
    """格式化摘要：优先用digest，不重新生成"""
    d = (article.get('digest') or '').strip()
    if d:
        return d[:max_len] + ('...' if len(d) > max_len else '')
    # 没有digest时，从标题提取
    return article.get('title', '')

# ---------- Step 1 ----------

def step1_run(date_str):
    start_ts, end_ts = calc_timestamp(date_str)
    print(f"📡 拉取 {date_str} 的文章（{start_ts} ~ {end_ts}）...")

    articles = fetch_meta(start_ts, end_ts)
    print(f"   原始: {len(articles)} 篇")

    filtered, excluded = filter_articles(articles)
    print(f"   初筛: {len(filtered)} 篇（剔除 {len(excluded)} 篇财经/非AI）")

    # 自动分类+标签
    for a in filtered:
        a['_auto_cat'] = auto_classify(a)
        a['_auto_tag'] = auto_tag(a)

    # 保存缓存
    cache = {
        'date_str': date_str,
        'start_ts': start_ts,
        'end_ts': end_ts,
        'articles': filtered
    }
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"   缓存已保存: {CACHE_FILE}")

    # 多源检测
    dups = detect_dup_sources(filtered)
    if dups:
        print(f"   🔗 检测到 {len(dups)} 组多源报道（需合成）:")
        for slug, arts in dups.items():
            sources = [a['source'] for a in arts]
            print(f"      - {arts[0]['title'][:40]}... ({', '.join(sources)})")

    print_candidates(filtered, date_str)
    print(f"\n✅ Step 1 完成。")
    print(f"   告诉我分类结果，格式：国际:aid1,aid2;国内:aid3;其他:aid4")

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
    if not CACHE_FILE.exists():
        print("❌ 未找到缓存，请先运行 Step 1")
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

    # 检测多源
    dups = detect_dup_sources(sum(categorized.values(), []))
    if dups:
        print(f"\n🔗 多源事件（{len(dups)}组）：")
        for slug, arts in dups.items():
            sources = [f"{a['source']}({a['title'][:20]})" for a in arts]
            print(f"   → {', '.join(sources)}")

    # 生成HTML
    html = build_html(categorized, date_str)
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

def build_html(categorized, date_str):
    cat_labels = {
        '国际': '🌍 国际视野',
        '国内': '🇨🇳 国内动态',
        '同业': '🏦 同业观察',
        '其他': '📌 其他'
    }
    cards_html = []
    for cat, label in cat_labels.items():
        items = categorized[cat]
        cards_html.append(f'<div class="section"><h2>{label}</h2>')
        if not items:
            cards_html.append('<div class="empty">暂无</div>')
        else:
            for item in items:
                digest = format_digest(item, 200).replace("'", "\\'").replace('\n', ' ')
                title = item['title'].replace("'", "\\'")
                source = item['source']
                link = item['link']
                cards_html.append(f"""<div class="card">
<div class="card-inner" onclick="this.classList.toggle('expanded')">
<div class="card-title">{'🤖 ' if item.get('_auto_tag') else ''}{title}</div>
<div class="card-meta"><span class="source-tag">{source}</span></div>
<div class="card-digest">{digest}...</div>
<div class="card-content"><a href="{link}" target="_blank">微信原文</a></div>
</div></div>""")
        cards_html.append('</div>')

    total = sum(len(v) for v in categorized.values())
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>智能研发早报 {date_str}</title>
<style>
*{{box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:760px;margin:0 auto;padding:20px;background:#f8fafc;color:#1f2937}}
.banner{{background:linear-gradient(135deg,#1e3a5f,#2d5a87);color:#fff;padding:24px 28px;border-radius:14px;margin-bottom:24px;box-shadow:0 4px 12px rgba(0,0,0,0.1)}}
.banner h1{{margin:0;font-size:20px;font-weight:600}}
.banner p{{margin:8px 0 0;color:#93c5fd;font-size:13px}}
.section{{margin-bottom:24px}}
.section h2{{font-size:14px;color:#fff;background:#3b82f6;padding:10px 14px;border-radius:8px 8px 0 0;margin:0}}
.card{{background:#fff;border:1px solid #e2e8f0;border-top:none}}
.card-inner{{padding:14px 16px;cursor:pointer;transition:background .15s}}
.card-inner:hover{{background:#f1f5f9}}
.card-inner.expanded{{background:#f8fafc}}
.card-title{{font-size:14px;font-weight:600;color:#1e293b;line-height:1.4}}
.source-tag{{display:inline-block;background:#dbeafe;color:#1d4ed8;padding:2px 8px;border-radius:12px;font-size:11px;margin:6px 0}}
.card-digest{{font-size:13px;color:#475569;line-height:1.6;margin-top:6px}}
.card-content{{display:none;font-size:13px;color:#374151;margin-top:10px;padding-top:10px;border-top:1px dashed #cbd5e1}}
.card-inner.expanded .card-content{{display:block}}
.empty{{color:#94a3b8;font-style:italic;padding:12px 16px;background:#fff;border:1px solid #e2e8f0;border-top:none}}
</style></head><body>
<div class="banner"><h1>🏦 智能研发早报</h1><p>{date_str} · 国际 {len(categorized['国际'])} 篇 · 国内 {len(categorized['国内'])} 篇 · 同业 {len(categorized['同业'])} 篇 · 其他 {len(categorized['其他'])} 篇</p></div>
{''.join(cards_html)}
</body></html>"""

def build_summary(categorized, dups, date_str):
    cat_icons = {'国际': '🌍', '国内': '🇨🇳', '同业': '🏦', '其他': '📌'}
    lines = [f"【{date_str} 智能研发早报】", ""]

    # 统计行
    stats = ' · '.join(f"{cat_icons[cat]} {len(categorized[cat])}篇"
                       for cat in ['国际', '国内', '同业', '其他'] if categorized[cat])
    lines.append(stats)
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

    # 多源合成
    if dups:
        lines.append("🔗 多源报道（合并阅读）：")
        for slug, arts in dups.items():
            titles = [a['title'] for a in arts]
            sources = [a['source'] for a in arts]
            # 取第一篇digest作为主摘要
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
