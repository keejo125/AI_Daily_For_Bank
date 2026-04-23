#!/usr/bin/env python3
"""
通过 /api/rss/export/{date} 导出接口获取微信公众号文章

用法: python3 fetch_articles.py [YYYY-MM-DD]
不传日期则默认昨天

变更说明（v2）:
- 使用 /api/rss/export/{date} 一键导出接口，替代逐公众号翻页+逐篇抓全文的旧流程
- 旧流程：获取订阅列表 → 逐公众号翻页 → 按时间戳过滤 → 逐篇 fetch 全文 → 保存
- 新流程：一次 GET 请求 → 直接拿到当天所有文章（含 content） → 保存
- 耗时从 4-10 分钟降至 1-3 秒
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_DIR / "config.json"

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2


# ---------- 工具函数 ----------

def load_config():
    """读取 config.json"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


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
    tz = timezone(timedelta(hours=8))
    yesterday = datetime.now(tz) - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def api_get(url, params=None):
    """带重试的 GET 请求"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"   ⚠️ GET 请求失败 (第{attempt}次): {e}")
            if attempt < MAX_RETRIES:
                import time
                time.sleep(RETRY_DELAY * attempt)
    return None


# ---------- HTML → 纯文本简易转换 ----------

def html_to_text(html_str):
    """简易 HTML → 纯文本：去标签、解码常见实体"""
    if not html_str:
        return ""
    # 去除 script/style
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_str, flags=re.S | re.I)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S | re.I)
    # 换行标签
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.I)
    text = re.sub(r'</p>', '\n', text, flags=re.I)
    text = re.sub(r'</div>', '\n', text, flags=re.I)
    text = re.sub(r'</li>', '\n', text, flags=re.I)
    # 移除剩余标签
    text = re.sub(r'<[^>]+>', '', text)
    # 解码常见实体
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&nbsp;', ' ')
    # 清理空白
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ---------- 核心逻辑 ----------

def save_article_md(filepath, title, link, source, content_html):
    """保存文章为 Markdown 文件，content_html 自动转纯文本"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    content_text = html_to_text(content_html)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"> 原文链接：{link}\n")
        f.write(f"> 公众号：{source}\n\n")
        f.write("---\n\n")
        f.write(content_text or "（无正文内容）")
    return filepath


def main():
    start_time = __import__('time').time()

    # 解析日期参数
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    date_str = get_target_date(date_arg)

    # 读取配置
    config = load_config()
    base_url = config["server"]["base_url"]
    project_dir = config["output"]["project_dir"]

    # 创建输出目录
    day_dir = Path(project_dir) / "daily" / date_str
    sources_dir = day_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    print(f"📅 目标日期: {date_str}")
    print(f"   API: {base_url}/api/rss/export/{date_str}")
    print(f"   输出目录: {day_dir}")
    print()

    # Step 1: 一键导出当天文章
    export_url = f"{base_url}/api/rss/export/{date_str}"
    print(f"📡 请求导出接口...")
    data = api_get(export_url)

    if not data:
        print("❌ 导出接口请求失败，退出")
        sys.exit(1)

    if "detail" in data:
        print(f"❌ 接口返回错误: {data['detail']}")
        sys.exit(1)

    articles = data.get("articles", [])
    print(f"   ✅ 获取到 {len(articles)} 篇文章")

    if not articles:
        print("❌ 没有找到文章，退出")
        sys.exit(0)

    # Step 2: 保存文章到本地
    print(f"\n📝 保存文章文件...")
    articles_meta = []

    for idx, art in enumerate(articles, 1):
        aid = art.get("aid", "")
        title = art.get("title", "无标题")
        link = art.get("link", "")
        digest = art.get("digest", "")
        content_html = art.get("content", "")
        pub_time = art.get("publish_time", 0)
        source_name = art.get("source", "")

        # 保存 Markdown 文件
        safe_title = sanitize_filename(title, max_len=50)
        safe_source = sanitize_filename(source_name, max_len=20)
        filename = f"{date_str}_{safe_title}_{safe_source}.md"
        filepath = sources_dir / filename
        save_article_md(filepath, title, link, source_name, content_html)

        # 收集元数据
        articles_meta.append({
            "aid": aid,
            "title": title,
            "source": source_name,
            "link": link,
            "digest": digest,
            "publish_time": pub_time,
            "source_file": f"sources/{filename}"
        })

        if idx % 20 == 0 or idx == len(articles):
            print(f"   进度: {idx}/{len(articles)}")

    # Step 3: 保存 articles_raw.json
    raw_json = {
        "date": date_str,
        "total": len(articles_meta),
        "articles": articles_meta
    }
    raw_path = day_dir / "articles_raw.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_json, f, ensure_ascii=False, indent=2)

    elapsed = __import__('time').time() - start_time
    print(f"\n✅ 完成！(耗时: {elapsed:.1f}s)")
    print(f"   文章文件: {sources_dir} ({len(articles_meta)} 篇)")
    print(f"   元数据: {raw_path}")


if __name__ == "__main__":
    main()
