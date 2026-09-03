#!/usr/bin/env python3
"""
多源数据获取主脚本 — 工厂驱动的单一编排流程

用法: python3 fetch_web_articles.py [YYYY-MM-DD]
不传日期则默认昨天

架构原则:
- 编排层完全不感知信源差异：通过 create_adapter() 工厂按 type 实例化适配器，
  所有适配器输出统一结构 [{"title","link","content","source","publish_time"}]。
- 单个信源失败只降级跳过，绝不中断管线。
- 新增信源类型 = 新增适配器类 + 注册到 ADAPTER_REGISTRY + sources.json 加配置。

执行流程:
1. 读取 config/sources.json
2. 处理手动投稿链接（manual_links.json 中 used: false）
3. 遍历统一 sources 数组，工厂实例化适配器并抓取（单源失败自动跳过）
4. 跨源去重：标题前20字符相同视为重复
5. 保存 daily/YYYY-MM-DD/sources/{date}_{title}_{source}.md
6. 输出 daily/YYYY-MM-DD/articles_raw.json
7. 打印统计报告
"""
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
SOURCES_CONFIG_PATH = PROJECT_DIR / "config" / "sources.json"
MANUAL_LINKS_PATH = PROJECT_DIR / "manual_links.json"

TZ_SHANGHAI = timezone(timedelta(hours=8))


# ---------- 依赖自检：确保全部必需依赖可用（缺失则自动 pip 安装到当前解释器） ----------
# 适配器(sources/base.py 等)依赖 requests/feedparser；网页正文抓取依赖 beautifulsoup4；
# 部分信源(量子位/Google DeepMind)的 RSS 解析依赖 lxml 解析器。
# 若当前解释器缺包，先自动安装再继续，避免 ModuleNotFoundError / "Couldn't find a tree builder" 等运行期失败。
import subprocess
# (pip 包名, Python 导入名) —— 两者不一致时必须同时给出，
# 否则会出现 pip 已装但 import 仍失败、脚本直接崩溃的情况（如 beautifulsoup4 的导入名是 bs4）
_REQUIRED_DEPS = [
    ("requests", "requests"),
    ("feedparser", "feedparser"),
    ("beautifulsoup4", "bs4"),
    ("lxml", "lxml"),
]
for _pkg, _imp in _REQUIRED_DEPS:
    try:
        __import__(_imp)
    except ImportError:
        print(f"⚠️ 未检测到 {_pkg} 依赖，正在自动安装...", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", _pkg])
        __import__(_imp)
import requests  # noqa: F401  (其余依赖随用随 import，此处仅确保自检通过)


# ---------- 工具函数 ----------

def sanitize_filename(name, max_len=80):
    """文件名安全化：特殊字符替换为_，限制长度"""
    name = re.sub(r'[\\/:*?"<>|\n\r\t]', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    if len(name) > max_len:
        name = name[:max_len].rstrip('_')
    return name


def get_target_date(date_arg=None):
    """解析日期参数，无参则返回昨天 (Asia/Shanghai)"""
    if date_arg:
        # 校验日期格式，防止 --date / --help 等误传
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_arg):
            print(f"❌ 无效日期格式: '{date_arg}'，期望 YYYY-MM-DD（如 2026-08-08）")
            sys.exit(1)
        return date_arg
    yesterday = datetime.now(TZ_SHANGHAI) - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def load_sources_config():
    """读取 config/sources.json"""
    with open(SOURCES_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_source_list(config):
    """
    获取统一信源列表。
    优先使用新版 "sources" 数组；兼容旧版 web_sources + wechat_rss_sources 拆分格式。
    """
    sources = config.get("sources")
    if isinstance(sources, list):
        return sources
    # 旧格式兼容：合并两个数组
    legacy = config.get("web_sources", []) + config.get("wechat_rss_sources", [])
    return legacy


def save_article_md(filepath, title, link, source, content, publish_time=0):
    """
    保存文章为 Markdown 文件（带 front matter）。
    如果文件已存在且 status=confirmed，不覆盖（保护AI已处理的结果）。
    返回: 'saved' | 'skipped'
    """
    # 检查是否已有确认过的版本
    if filepath.exists():
        try:
            existing = filepath.read_text(encoding='utf-8')
            if 'status: confirmed' in existing[:500]:
                return 'skipped'
        except Exception:
            pass

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        # Front matter — v3.5 强制写入 link 和 source，缺一不可
        f.write("---\n")
        if publish_time:
            f.write(f"publish_time: {publish_time}\n")
        f.write(f"link: {link}\n")
        f.write(f"source: {source}\n")
        f.write("status: pending\n")
        f.write("---\n\n")

        f.write(f"# {title}\n\n")
        f.write(f"> 原文链接：{link}\n")
        f.write(f"> 来源：{source}\n\n")
        f.write(content or "（无正文内容）")
    return 'saved'


# ---------- 手动投稿处理 ----------

def process_manual_links(date_str, article_fetch_api, sources_dir):
    """处理手动投稿链接"""
    if not MANUAL_LINKS_PATH.exists():
        return []

    try:
        with open(MANUAL_LINKS_PATH, "r", encoding="utf-8") as f:
            links = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

    pending = [l for l in links if not l.get("used")]
    if not pending:
        print("   （无待处理的手动投稿链接）")
        return []

    print(f"   📎 发现 {len(pending)} 条手动投稿链接")

    from sources.base import fetch_wechat_page, fetch_wechat_article

    articles = []
    for item in pending:
        url = item["url"]
        source = item.get("source", "手动投稿")
        print(f"      📄 处理: {url[:60]}...")

        title = ""
        content = ""

        if "mp.weixin.qq.com" in url:
            # 优先直接抓取微信页面（短链格式 /s/xxx）
            result = fetch_wechat_page(url)
            if result:
                title = result.get("title", "")
                content = result.get("content", "")
                # 如果未指定来源，用公众号名
                if source == "手动投稿" and result.get("author"):
                    source = result["author"]
            # 降级：尝试旧API（长链格式 /s?__biz=...）
            if not content and article_fetch_api:
                content = fetch_wechat_article(url, article_fetch_api)

        # 从内容第一行提取标题（如果页面未拿到）
        if not title and content:
            first_line = content.strip().split('\n')[0].strip()
            if first_line and len(first_line) > 5:
                title = first_line[:100]
        if not title:
            title = f"手动投稿_{source}_{date_str}"

        articles.append({
            "title": title,
            "link": url,
            "content": content,
            "source": source,
            "publish_time": 0,
        })

        # 标记为已使用
        item["used"] = True

    # 保存更新后的 manual_links.json
    with open(MANUAL_LINKS_PATH, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)

    print(f"   ✅ 手动投稿处理完成: {len(articles)} 篇")
    return articles


# ---------- 去重 ----------

def dedup_articles(articles):
    """跨源去重：标题前20字符相同视为重复"""
    seen = set()
    result = []
    for art in articles:
        title = art.get("title", "")
        key = title[:20].strip().lower()
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        result.append(art)
    return result


# ---------- Step 1.5: 内容自检与定点重抓 ----------
# 设计原则：
#   1) 身份键是 link(URL)，不是文件名——文件名会随解析器/标题清洗漂移，URL 不会。
#   2) 已存在的文章一律跳过（幂等），绝不新建同文异名的副本。
#   3) 内容坏了不靠"删目录重抓"自愈，而靠"先诊断、再只重抓问题项、抓到即覆盖"。
#      这样任何情况下都不需要 rm -rf daily/<date>。

def split_front_matter(text):
    """拆分 front matter 与正文，返回 (fm_text, body_text, has_fm)"""
    if not text.startswith('---'):
        return '', text, False
    end = text.find('\n---', 3)
    if end == -1:
        return '', text, False
    return text[3:end], text[end + 4:], True


def get_fm_field(fm_text, key):
    m = re.search(r'(?m)^' + re.escape(key) + r':\s*(.*)$', fm_text)
    return m.group(1).strip() if m else ''


def body_plain_length(body_text):
    """正文有效长度：剔除 H1 标题行与引用行（原文链接/来源）"""
    count = 0
    for line in body_text.split('\n'):
        s = line.strip()
        if not s or s.startswith('# ') or s.startswith('> '):
            continue
        count += len(s)
    return count


def build_url_index(sources_dir):
    """扫描已落盘文章，建立 URL -> 文件路径 映射（每次运行从磁盘重建，不做持久索引）"""
    index = {}
    for path in sorted(sources_dir.glob('*.md')):
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            continue
        fm, _, _ = split_front_matter(text)
        link = get_fm_field(fm, 'link')
        if link:
            index[link] = path
    return index


def check_article_quality(sources_dir, min_body_len=500):
    """诊断：检出正文退化的文章（不联网）。返回问题项列表。"""
    problems = []
    for path in sorted(sources_dir.glob('*.md')):
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            continue
        fm, body, _ = split_front_matter(text)
        link = get_fm_field(fm, 'link')
        status = get_fm_field(fm, 'status') or 'pending'
        h1 = ''
        for line in body.split('\n'):
            if line.startswith('# '):
                h1 = line[2:].strip()
                break
        length = body_plain_length(body)
        reasons = []
        if length < min_body_len:
            reasons.append(f'正文过短({length}<{min_body_len})')
        if not link:
            reasons.append('缺少 link 字段')
        if '（无正文内容）' in body:
            reasons.append('正文为空占位')
        if reasons:
            problems.append({
                'path': path,
                'title': h1 or path.stem,
                'link': link,
                'status': status,
                'length': length,
                'reasons': reasons,
            })
    return problems


def refetch_article_content(url, article_fetch_api=''):
    """按 URL 重新抓取正文（定点重抓用）。返回 (title, content)"""
    from sources.base import (fetch_wechat_page, fetch_wechat_article,
                              fetch_page_content, html_to_text, clean_article_text)
    title, content = '', ''
    if 'mp.weixin.qq.com' in url:
        result = fetch_wechat_page(url)
        if result:
            title = result.get('title', '')
            content = result.get('content', '')
        if not content and article_fetch_api:
            content = fetch_wechat_article(url, article_fetch_api)
    else:
        html = fetch_page_content(url)
        if html:
            content = clean_article_text(html_to_text(html))
    return title, content


def replace_body(path, new_content):
    """只替换正文，原样保留 front matter 与 H1 标题行（避免冲掉已中文化的标题与 AI 已写字段）"""
    text = path.read_text(encoding='utf-8')
    fm, body, has_fm = split_front_matter(text)
    # 注意 fm 结尾不含换行，需显式补回，否则 front matter 结尾的 --- 会被粘到最后一个字段上
    head = ('---' + fm + '\n---') if has_fm else ''
    keep = []
    for line in body.split('\n'):
        s = line.strip()
        if s.startswith('# ') or s.startswith('> '):
            keep.append(line)
        elif s == '':
            continue          # 标题与引用行之间的空行：跳过，继续收集
        else:
            if keep:
                break         # 真正的正文开始，停止
    new_text = (head + '\n\n' if head else '') + '\n'.join(keep) + '\n\n' + new_content
    path.write_text(new_text, encoding='utf-8')


def repair_problems(problems, article_fetch_api='', force=False):
    """定点重抓：只对诊断出的问题项重新抓取，抓到即覆盖。
    - 默认不覆盖 status=confirmed 的文章（保护 AI 已处理结果），需 force=True
    - 新正文比旧的还短时不写盘，只告警（防止坏 -> 更坏）
    """
    fixed, skipped_confirmed, still_bad, failed = [], [], [], []
    for p in problems:
        path, link = p['path'], p['link']
        if not link:
            failed.append((p, '无 link，无法重抓'))
            continue
        if p['status'] == 'confirmed' and not force:
            skipped_confirmed.append(p)
            continue
        try:
            _, content = refetch_article_content(link, article_fetch_api)
        except Exception as e:
            failed.append((p, f'抓取异常: {e}'))
            continue
        new_len = len(content or '')
        if not content or new_len <= p['length']:
            still_bad.append((p, new_len))
            continue
        replace_body(path, content)
        fixed.append((p, new_len))
    return fixed, skipped_confirmed, still_bad, failed


# ---------- 主流程 ----------

def main():
    start_time = time.time()

    # 解析参数：第一个非 -- 开头的参数为日期，其余为开关
    #   --check-only  只做内容自检并打印问题清单，不重抓
    #   --force       连 status=confirmed 的问题项也一并重抓覆盖
    argv = sys.argv[1:]
    check_only = '--check-only' in argv
    force = '--force' in argv
    date_arg = next((a for a in argv if not a.startswith('--')), None)
    date_str = get_target_date(date_arg)

    # 读取配置
    config = load_sources_config()
    settings = config.get("settings", {})
    article_fetch_api = config.get("article_fetch_api", "")

    # 创建输出目录
    day_dir = PROJECT_DIR / "daily" / date_str
    sources_dir = day_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    print(f"📅 目标日期: {date_str}")
    print(f"   输出目录: {day_dir}")
    print()

    all_articles = []

    # === Step 1: 处理手动投稿链接 ===
    print("📎 [1/2] 处理手动投稿链接...")
    manual_articles = process_manual_links(date_str, article_fetch_api, sources_dir)
    all_articles.extend(manual_articles)
    print()

    # === Step 2: 遍历统一信源数组（工厂驱动，信源无关） ===
    from sources import create_adapter
    from sources.base import clean_article_text

    source_list = get_source_list(config)
    enabled = [s for s in source_list if s.get("enabled", True)]
    disabled = len(source_list) - len(enabled)
    print(f"🌐 [2/2] 抓取信源（共 {len(enabled)} 个启用，{disabled} 个禁用）...")

    ok_sources, fail_sources = [], []
    for src in enabled:
        name = src.get("name", src.get("id", "unknown"))
        try:
            adapter = create_adapter(src, settings, article_fetch_api)
            articles = adapter.fetch(date_str)
            all_articles.extend(articles)
            ok_sources.append(f"{name}({len(articles)})")
        except Exception as e:
            # 单信源失败只降级跳过，绝不中断管线
            print(f"   ❌ [{name}] 处理异常（跳过，不影响管线）: {e}")
            fail_sources.append(name)

    print(f"\n   📊 信源汇总: 成功 {len(ok_sources)} 个，失败 {len(fail_sources)} 个")
    if fail_sources:
        print(f"   ⚠️ 失败信源: {', '.join(fail_sources)}")
    print()

    # === 去重 ===
    before_dedup = len(all_articles)
    all_articles = dedup_articles(all_articles)
    dedup_removed = before_dedup - len(all_articles)
    if dedup_removed > 0:
        print(f"🔄 去重: 移除 {dedup_removed} 篇重复文章")

    # === 保存文件（以 URL 为身份键：已存在则复用原文件，杜绝"同文异名"副本）===
    print(f"\n📝 保存文章文件...")
    articles_meta = []
    saved_count, skipped_count, dup_suppressed, excluded_count = 0, 0, 0, 0
    url_index = build_url_index(sources_dir)
    from exclude_store import load_excluded
    excluded = load_excluded()

    for idx, art in enumerate(all_articles, 1):
        title = art.get("title", "无标题")
        link = art.get("link", "")
        content = art.get("content", "")
        source = art.get("source", "")
        pub_time = art.get("publish_time", 0)

        # 已被规则/人工判定删除的文章：不再抓回（否则每次重跑都会长回来）
        if link and link in excluded:
            excluded_count += 1
            continue

        # 清洗正文
        if content:
            content = clean_article_text(content)

        # 保存 Markdown 文件：URL 已存在 → 不写盘（内容升级交给 Step 1.5 定点重抓，带"只升不降"保护）
        if link and link in url_index:
            filepath = url_index[link]
            dup_suppressed += 1
            result = 'exists'
        else:
            safe_title = sanitize_filename(title, max_len=50)
            safe_source = sanitize_filename(source, max_len=20)
            filename = f"{date_str}_{safe_title}_{safe_source}.md"
            filepath = sources_dir / filename
            # 文件名撞车但 URL 不同 → 追加 URL 短哈希，绝不误覆盖他人文件
            if filepath.exists():
                url_hash = hashlib.md5(link.encode("utf-8")).hexdigest()[:6]
                filepath = sources_dir / f"{date_str}_{safe_title}_{safe_source}_{url_hash}.md"
            if link:
                url_index[link] = filepath

            result = save_article_md(filepath, title, link, source, content, pub_time)
            if result == 'skipped':
                skipped_count += 1
            else:
                saved_count += 1

        # 收集元数据
        articles_meta.append({
            "title": title,
            "source": source,
            "link": link,
            "digest": content[:150] if content else "",
            "publish_time": pub_time,
            "source_file": f"sources/{filepath.name}"
        })

        if idx % 20 == 0 or idx == len(all_articles):
            print(f"   进度: {idx}/{len(all_articles)}")

    # === Step 1.5: 内容自检 + 定点重抓（自动执行，最多 1 轮，绝不循环）===
    min_len = int(settings.get("content_min_length", 500))
    print(f"\n🔍 [Step 1.5] 内容自检（正文 < {min_len} 字视为退化）...")
    problems = check_article_quality(sources_dir, min_body_len=min_len)

    if not problems:
        print("   ✅ 全部文章正文达标，无需重抓")
    else:
        for p in problems:
            print(f"   ⚠️ [{p['status']}] {p['title'][:38]} | {p['length']} 字 | {'; '.join(p['reasons'])}")

        if check_only:
            print(f"   ℹ️ --check-only 模式：共 {len(problems)} 篇待修复，本次不重抓")
        else:
            print(f"   🔧 定点重抓 {len(problems)} 篇问题文章（只动这些文件）...")
            fixed, skipped_confirmed, still_bad, failed = repair_problems(
                problems, article_fetch_api, force=force)
            for p, new_len in fixed:
                print(f"      ✅ 已修复: {p['title'][:34]} ({p['length']} → {new_len} 字)")
            for p in skipped_confirmed:
                print(f"      ⏭️ 已确认跳过(需 --force): {p['title'][:34]}")
            for p, new_len in still_bad:
                print(f"      ⚠️ 重抓后仍不达标({new_len} 字)，保持原状: {p['title'][:30]}")
            for p, err in failed:
                print(f"      ❌ 重抓失败: {p['title'][:30]} | {err}")
            remain = check_article_quality(sources_dir, min_body_len=min_len)
            print(f"   📊 自检结果: 修复 {len(fixed)} 篇，剩余问题 {len(remain)} 篇")

    # === 保存 articles_raw.json ===
    raw_json = {
        "date": date_str,
        "total": len(articles_meta),
        "articles": articles_meta
    }
    raw_path = day_dir / "articles_raw.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_json, f, ensure_ascii=False, indent=2)

    # === 统计报告 ===
    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"✅ 完成！(耗时: {elapsed:.1f}s)")
    print(f"   总文章数: {len(articles_meta)}")
    print(f"   新保存: {saved_count} 篇，跳过已确认: {skipped_count} 篇，复用已有文件: {dup_suppressed} 篇")
    print(f"   命中排除清单跳过: {excluded_count} 篇")
    print(f"   文章文件: {sources_dir}")
    print(f"   元数据: {raw_path}")

    # 按来源统计
    source_stats = {}
    for art in articles_meta:
        src = art.get("source", "未知")
        source_stats[src] = source_stats.get(src, 0) + 1

    print(f"\n📊 来源统计:")
    for src, count in sorted(source_stats.items(), key=lambda x: -x[1]):
        print(f"   {src}: {count} 篇")


if __name__ == "__main__":
    main()
