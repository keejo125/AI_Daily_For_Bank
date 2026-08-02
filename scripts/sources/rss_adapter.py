#!/usr/bin/env python3
"""
官网RSS适配器 — 处理极客公园、量子位、36氪、Solidot、国际源等
"""
import re
import time
from datetime import datetime, timedelta, timezone

import feedparser

from .base import BaseSourceAdapter, fetch_page_content, html_to_text

# Asia/Shanghai 时区
TZ_SHANGHAI = timezone(timedelta(hours=8))


class RSSAdapter(BaseSourceAdapter):
    """官网 RSS/Atom 适配器"""

    def fetch(self, date_str: str) -> list:
        """
        获取指定日期的文章
        返回: [{"title", "link", "content", "source", "publish_time"}, ...]
        """
        print(f"   📡 [{self.name}] 获取 RSS: {self.url}")
        resp = self._http_get(self.url)
        if not resp:
            print(f"   ❌ [{self.name}] RSS 获取失败")
            return []

        # 验证是否为有效 RSS/XML
        content_type = resp.headers.get("Content-Type", "")
        text = resp.text.strip()
        if not text.startswith("<?xml") and not text.startswith("<rss") and not text.startswith("<feed"):
            # 可能返回了网页而非RSS（反爬）
            if "<html" in text[:500].lower():
                print(f"   ❌ [{self.name}] 返回了网页而非RSS（可能被反爬拦截）")
                return []

        feed = feedparser.parse(text)
        if feed.bozo and not feed.entries:
            print(f"   ❌ [{self.name}] RSS 解析失败: {feed.bozo_exception}")
            return []

        full_text_in_feed = self.config.get("full_text_in_feed", False)
        max_articles = self.settings.get("max_articles_per_source", 30)

        articles = []
        for entry in feed.entries:
            # 解析发布时间
            pub_time = self._parse_pub_time(entry)

            # 按日期过滤
            if pub_time and not self._is_target_date(pub_time, date_str):
                continue

            title = entry.get("title", "").strip()
            link = entry.get("link", "")
            if not title:
                continue

            # 获取正文
            content = ""
            if full_text_in_feed:
                # 从 feed 中直接提取全文
                content = self._extract_content_from_entry(entry)
            else:
                # 需要抓取原文页面
                if link:
                    print(f"      📄 抓取正文: {title[:30]}...")
                    content = fetch_page_content(link, timeout=self.timeout, user_agent=self.user_agent)
                    time.sleep(1)  # 礼貌延迟
                # 网页抓取失败时，用RSS摘要兜底
                if not content:
                    content = self._extract_content_from_entry(entry)
                    if content:
                        print(f"      ℹ️ 网页抓取失败，使用RSS摘要兜底")

            articles.append({
                "title": title,
                "link": link,
                "content": content,
                "source": self.name,
                "publish_time": int(pub_time.timestamp()) if pub_time else 0,
            })

            if len(articles) >= max_articles:
                break

        print(f"   ✅ [{self.name}] 获取到 {len(articles)} 篇文章")
        return articles

    def _parse_pub_time(self, entry) -> datetime:
        """解析 RSS entry 的发布时间"""
        # feedparser 统一解析为 time.struct_time
        for field in ("published_parsed", "updated_parsed"):
            tp = entry.get(field)
            if tp:
                try:
                    dt = datetime(*tp[:6], tzinfo=timezone.utc)
                    return dt.astimezone(TZ_SHANGHAI)
                except Exception:
                    pass

        # 尝试手动解析 pubDate 字符串
        pub_str = entry.get("published", "") or entry.get("updated", "")
        if pub_str:
            for fmt in (
                "%Y-%m-%d %H:%M:%S %z",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%SZ",
                "%a, %d %b %Y %H:%M:%S %z",
                "%a, %d %b %Y %H:%M:%S %Z",
            ):
                try:
                    dt = datetime.strptime(pub_str.strip(), fmt)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt.astimezone(TZ_SHANGHAI)
                except ValueError:
                    continue

        # 兜底：部分 feed（如美团技术）无日期字段，尝试从 URL 路径提取 /YYYY/MM/DD/
        link = entry.get("link", "")
        if link:
            m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", link)
            if m:
                try:
                    dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                                  tzinfo=TZ_SHANGHAI)
                    return dt
                except ValueError:
                    pass

        return None

    def _is_target_date(self, pub_time: datetime, date_str: str) -> bool:
        """判断发布时间是否为目标日期"""
        return pub_time.strftime("%Y-%m-%d") == date_str

    def _extract_content_from_entry(self, entry) -> str:
        """从 RSS entry 中提取全文内容"""
        # 优先使用 content 字段（Atom feed）
        if hasattr(entry, "content") and entry.content:
            html = entry.content[0].get("value", "")
            if html:
                return html_to_text(html)

        # 其次使用 description / summary
        desc = entry.get("description", "") or entry.get("summary", "")
        if desc:
            return html_to_text(desc)

        return ""
