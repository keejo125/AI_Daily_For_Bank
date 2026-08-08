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


# ---------- 主流程 ----------

def main():
    start_time = time.time()

    # 解析日期参数
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
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

    # === 保存文件 ===
    print(f"\n📝 保存文章文件...")
    articles_meta = []
    saved_count, skipped_count = 0, 0

    for idx, art in enumerate(all_articles, 1):
        title = art.get("title", "无标题")
        link = art.get("link", "")
        content = art.get("content", "")
        source = art.get("source", "")
        pub_time = art.get("publish_time", 0)

        # 清洗正文
        if content:
            content = clean_article_text(content)

        # 保存 Markdown 文件（已确认的不覆盖）
        safe_title = sanitize_filename(title, max_len=50)
        safe_source = sanitize_filename(source, max_len=20)
        filename = f"{date_str}_{safe_title}_{safe_source}.md"
        filepath = sources_dir / filename
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
            "source_file": f"sources/{filename}"
        })

        if idx % 20 == 0 or idx == len(all_articles):
            print(f"   进度: {idx}/{len(all_articles)}")

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
    print(f"   新保存: {saved_count} 篇，跳过已确认: {skipped_count} 篇")
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
