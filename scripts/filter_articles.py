#!/usr/bin/env python3
"""
关键词过滤文章脚本

用法: python3 filter_articles.py YYYY-MM-DD
读取 config.json 中的 keywords，过滤 articles_raw.json，
移除不匹配的 source .md 文件，输出 filtered_articles.json
"""
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_DIR / "config.json"


def load_config():
    """读取 config.json"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def matches_include(text, include_keywords):
    """检查文本是否匹配任一 include 关键词（不区分大小写）"""
    text_lower = text.lower()
    for kw in include_keywords:
        if kw.lower() in text_lower:
            return True
    return False


def matches_exclude(text, exclude_keywords):
    """检查文本是否匹配任一 exclude 关键词（不区分大小写）"""
    if not exclude_keywords:
        return False
    text_lower = text.lower()
    for kw in exclude_keywords:
        if kw.lower() in text_lower:
            return True
    return False


def main():
    if len(sys.argv) < 2:
        print("用法: python3 filter_articles.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]

    # 读取配置
    config = load_config()
    include_keywords = config["keywords"]["include"]
    exclude_keywords = config["keywords"]["exclude"]
    project_dir = config["output"]["project_dir"]

    # 读取 articles_raw.json
    day_dir = Path(project_dir) / "daily" / date_str
    raw_path = day_dir / "articles_raw.json"

    if not raw_path.exists():
        print(f"❌ 文件不存在: {raw_path}")
        print("   请先运行 fetch_articles.py 获取文章")
        sys.exit(1)

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    articles = raw_data.get("articles", [])
    total_raw = len(articles)

    print(f"📅 日期: {date_str}")
    print(f"📋 原始文章: {total_raw} 篇")
    print(f"🔍 Include 关键词: {include_keywords}")
    if exclude_keywords:
        print(f"🚫 Exclude 关键词: {exclude_keywords}")
    print()

    # 过滤
    filtered = []
    removed = []

    for art in articles:
        title = art.get("title", "")
        digest = art.get("digest", "")
        text = title + " " + digest

        # 检查 include
        if not matches_include(text, include_keywords):
            removed.append(art)
            print(f"   ❌ [不匹配include] {title[:60]}")
            continue

        # 检查 exclude
        if matches_exclude(text, exclude_keywords):
            removed.append(art)
            print(f"   🚫 [匹配exclude] {title[:60]}")
            continue

        filtered.append(art)
        print(f"   ✅ {title[:60]}")

    # 删除不匹配文章的 .md 文件
    sources_dir = day_dir / "sources"
    deleted_count = 0
    for art in removed:
        source_file = art.get("source_file", "")
        if source_file:
            filepath = day_dir / source_file
            if filepath.exists():
                try:
                    filepath.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"   ⚠️ 删除失败: {filepath} - {e}")

    # 输出 filtered_articles.json
    filtered_data = {
        "date": date_str,
        "total_raw": total_raw,
        "total_filtered": len(filtered),
        "removed": len(removed),
        "articles": [
            {
                "aid": art.get("aid", ""),
                "title": art.get("title", ""),
                "source": art.get("source", ""),
                "link": art.get("link", ""),
                "digest": art.get("digest", ""),
                "source_file": art.get("source_file", "")
            }
            for art in filtered
        ]
    }

    filtered_path = day_dir / "filtered_articles.json"
    with open(filtered_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    # 打印统计
    print(f"\n{'='*50}")
    print(f"📊 过滤统计")
    print(f"{'='*50}")
    print(f"   原始文章: {total_raw} 篇")
    print(f"   保留文章: {len(filtered)} 篇")
    print(f"   移除文章: {len(removed)} 篇")
    print(f"   删除文件: {deleted_count} 个")
    print(f"   输出文件: {filtered_path}")


if __name__ == "__main__":
    main()
