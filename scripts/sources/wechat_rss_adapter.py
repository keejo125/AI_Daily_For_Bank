#!/usr/bin/env python3
"""
公众号RSS适配器 — 处理 decemberpei.cyou 等第三方公众号RSS服务
这些 feed 只有标题+微信链接，全文需通过 article_fetch_api 获取
"""
from datetime import datetime, timedelta, timezone

import feedparser

from .base import BaseSourceAdapter, fetch_wechat_article

# Asia/Shanghai 时区
TZ_SHANGHAI = timezone(timedelta(hours=8))


class WechatRSSAdapter(BaseSourceAdapter):
    """公众号 RSS 服务适配器（best-effort）"""

    def __init__(self, source_config: dict, global_settings: dict, article_fetch_api: str = ""):
        super().__init__(source_config, global_settings, article_fetch_api)

    def fetch(self, date_str: str) -> list:
        """
        获取指定日期的公众号文章
        返回: [{"title", "link", "content", "source", "publish_time"}, ...]
        """
        print(f"   📡 [{self.name}] 获取公众号RSS: {self.url}")
        resp = self._http_get(self.url)
        if not resp:
            print(f"   ⚠️ [{self.name}] RSS 获取失败（跳过，不影响其他源）")
            return []

        text = resp.text.strip()
        if not text.startswith("<?xml") and not text.startswith("<rss") and not text.startswith("<feed"):
            print(f"   ⚠️ [{self.name}] 返回内容非RSS格式（跳过）")
            return []

        feed = feedparser.parse(text)
        if feed.bozo and not feed.entries:
            print(f"   ⚠️ [{self.name}] RSS 解析失败（跳过）: {feed.bozo_exception}")
            return []

        max_articles = self.settings.get("max_articles_per_source", 30)
        articles = []

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "")
            if not title or not link:
                continue

            # 解析发布时间
            pub_time = self._parse_pub_time(entry)

            # 按日期过滤（如果无法解析时间，则保留所有文章由后续流程处理）
            if pub_time and pub_time.strftime("%Y-%m-%d") != date_str:
                continue

            # 通过 API 获取微信文章全文
            content = ""
            if self.article_fetch_api and "mp.weixin.qq.com" in link:
                print(f"      📄 获取微信全文: {title[:30]}...")
                content = fetch_wechat_article(link, self.article_fetch_api)

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
        """解析发布时间"""
        for field in ("published_parsed", "updated_parsed"):
            tp = entry.get(field)
            if tp:
                try:
                    dt = datetime(*tp[:6], tzinfo=timezone.utc)
                    return dt.astimezone(TZ_SHANGHAI)
                except Exception:
                    pass
        return None
