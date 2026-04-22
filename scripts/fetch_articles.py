#!/usr/bin/env python3
"""
通过 REST API 获取微信公众号文章

用法: python3 fetch_articles.py [YYYY-MM-DD]
不传日期则默认昨天
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_DIR / "config.json"

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


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


def date_to_timestamps(date_str):
    """将日期字符串转为当天的起止 Unix 时间戳（秒），上海时区"""
    tz = timezone(timedelta(hours=8))
    start_dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=tz)
    end_dt = start_dt + timedelta(days=1) - timedelta(seconds=1)
    return int(start_dt.timestamp()), int(end_dt.timestamp())


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
                time.sleep(RETRY_DELAY * attempt)
    return None


def api_post(url, body):
    """带重试的 POST 请求"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(url, json=body, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"   ⚠️ POST 请求失败 (第{attempt}次): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)
    return None


# ---------- 核心逻辑 ----------

def fetch_subscriptions(base_url):
    """获取订阅公众号列表"""
    url = f"{base_url}/api/rss/subscriptions"
    print(f"📡 获取订阅列表: {url}")
    data = api_get(url)
    if not data or not data.get("success"):
        print(f"   ❌ 获取订阅列表失败: {data}")
        return []
    subs = data.get("data", [])
    print(f"   ✅ 获取到 {len(subs)} 个公众号")
    return subs


def fetch_article_list(base_url, fakeid):
    """获取某公众号的文章列表（自动翻页）"""
    all_articles = []
    begin = 0
    count = 10

    while True:
        url = f"{base_url}/api/public/articles"
        params = {"fakeid": fakeid, "begin": begin, "count": count}
        data = api_get(url, params=params)

        if not data or not data.get("success"):
            if begin == 0:
                print(f"      ⚠️ 获取文章列表失败: fakeid={fakeid}")
            break

        resp_data = data.get("data", {})
        articles = resp_data.get("articles", [])
        if not articles:
            break

        all_articles.extend(articles)

        # 检查分页: total 表示总数
        total = resp_data.get("total", 0)
        if begin + count >= total:
            break

        begin += count
        time.sleep(0.3)  # 避免请求过快

    return all_articles


def fetch_full_article(base_url, link):
    """获取文章全文内容"""
    url = f"{base_url}/api/article/fetch"
    body = {"url": link}
    data = api_post(url, body)
    if not data or data.get("code") != 0:
        return None
    return data.get("data", {})


def save_article_md(filepath, title, link, source, content):
    """保存文章为 Markdown 文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"> 原文链接：{link}\n")
        f.write(f"> 公众号：{source}\n\n")
        f.write("---\n\n")
        f.write(content or "（无正文内容）")
    return filepath


def main():
    # 解析日期参数
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    date_str = get_target_date(date_arg)
    start_ts, end_ts = date_to_timestamps(date_str)

    # 读取配置
    config = load_config()
    base_url = config["server"]["base_url"]
    project_dir = config["output"]["project_dir"]

    # 创建输出目录
    day_dir = Path(project_dir) / "daily" / date_str
    sources_dir = day_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    print(f"📅 目标日期: {date_str}")
    print(f"   时间范围: {start_ts} - {end_ts}")
    print(f"   输出目录: {day_dir}")
    print()

    # Step 1: 获取订阅列表
    subscriptions = fetch_subscriptions(base_url)
    if not subscriptions:
        print("❌ 未获取到任何公众号，退出")
        sys.exit(1)

    # Step 2: 遍历公众号，获取文章
    all_articles = []
    for idx, sub in enumerate(subscriptions, 1):
        fakeid = sub.get("fakeid", "")
        nickname = sub.get("nickname", "未知")
        print(f"[{idx}/{len(subscriptions)}] 📰 {nickname} (fakeid={fakeid})")

        articles = fetch_article_list(base_url, fakeid)
        print(f"      获取到 {len(articles)} 篇文章")

        # 按日期过滤 (使用 create_time 作为发布时间)
        matched = []
        for art in articles:
            pub_ts = art.get("create_time", 0)
            if start_ts <= pub_ts <= end_ts:
                art["_source_nickname"] = nickname
                matched.append(art)

        print(f"      匹配日期: {len(matched)} 篇")
        all_articles.extend(matched)
        time.sleep(0.5)  # 避免请求过快

    print(f"\n📊 共获取 {len(all_articles)} 篇目标日期文章")

    if not all_articles:
        print("❌ 没有找到文章，退出")
        sys.exit(0)

    # Step 3: 获取全文 & 保存
    print(f"\n📝 开始获取全文并保存...")
    articles_meta = []

    for idx, art in enumerate(all_articles, 1):
        aid = art.get("aid", "")
        title = art.get("title", "无标题")
        link = art.get("link", "")
        digest = art.get("digest", "")
        pub_time = art.get("create_time", 0)
        source_name = art.get("_source_nickname", "")
        list_content = art.get("content", "")

        print(f"   [{idx}/{len(all_articles)}] {title[:50]}...")

        # 尝试获取全文
        full_content = ""
        if link:
            full_data = fetch_full_article(base_url, link)
            if full_data:
                # 优先 plain_content，其次 content
                full_content = full_data.get("plain_content") or full_data.get("content") or ""
            time.sleep(0.3)

        # 最终正文：优先全文API的 plain_content，其次全文API的 content，
        # 再其次列表的 content，最后用 digest
        body_text = full_content or list_content or digest or ""

        # 保存 Markdown 文件
        safe_title = sanitize_filename(title, max_len=50)
        safe_source = sanitize_filename(source_name, max_len=20)
        filename = f"{date_str}_{safe_title}_{safe_source}.md"
        filepath = sources_dir / filename
        save_article_md(filepath, title, link, source_name, body_text)

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

    # Step 4: 保存 articles_raw.json
    raw_json = {
        "date": date_str,
        "total": len(articles_meta),
        "articles": articles_meta
    }
    raw_path = day_dir / "articles_raw.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_json, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成！")
    print(f"   文章文件: {sources_dir} ({len(articles_meta)} 篇)")
    print(f"   元数据: {raw_path}")


if __name__ == "__main__":
    main()
