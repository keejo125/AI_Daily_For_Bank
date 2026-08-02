#!/usr/bin/env python3
"""
36氪官方API适配器 — 直连 36氪热榜公开接口（无需认证）

接口: {base_url}/{date}/24h_hot_list.json
返回: {"date": "...", "data": [{"publishTime", "author", "rank", "title", "content", "url"}, ...]}

说明:
- 该接口按"天"提供24小时热榜，date=D 的榜单覆盖的是 D-1 发布的内容。
- 因此获取目标日期 T 的文章时，需要拉取 T+1 的榜单，再按 publishTime 过滤出 T 的文章。
- API 的 content 字段仅为编辑摘要（一句话），适配器会进一步抓取原文页面获取全文。
"""
import time
from datetime import datetime, timedelta, timezone

from .base import BaseSourceAdapter, fetch_page_content

# Asia/Shanghai 时区
TZ_SHANGHAI = timezone(timedelta(hours=8))


class Kr36APIAdapter(BaseSourceAdapter):
    """36氪官方热榜API适配器"""

    def fetch(self, date_str: str) -> list:
        """
        获取指定日期的36氪热榜文章
        返回: [{"title", "link", "content", "source", "publish_time"}, ...]
        """
        base_url = self.url.rstrip("/")
        target = datetime.strptime(date_str, "%Y-%m-%d").date()

        # 拉取 target+1 和 target 两天的榜单（覆盖日期边界），再按 publishTime 过滤
        candidate_dates = [target + timedelta(days=1), target]

        seen_urls = set()
        articles = []
        max_articles = self.settings.get("max_articles_per_source", 30)

        for d in candidate_dates:
            api_url = f"{base_url}/{d.strftime('%Y-%m-%d')}/24h_hot_list.json"
            print(f"   📡 [{self.name}] 获取官方API: {api_url}")
            resp = self._http_get(api_url)
            if not resp:
                continue

            try:
                payload = resp.json()
            except Exception as e:
                print(f"   ⚠️ [{self.name}] API返回非JSON: {e}")
                continue

            items = payload.get("data", []) if isinstance(payload, dict) else []
            if not isinstance(items, list):
                continue

            for item in items:
                if not isinstance(item, dict):
                    continue
                title = (item.get("title") or "").strip()
                link = item.get("url") or ""
                if not title or not link:
                    continue
                if link in seen_urls:
                    continue

                # 解析发布时间并按目标日期过滤
                pub_time = self._parse_pub_time(item.get("publishTime", ""))
                if pub_time and pub_time.strftime("%Y-%m-%d") != date_str:
                    continue

                seen_urls.add(link)
                # API 的 content 仅为一句话摘要，需抓取原文页面获取全文
                summary = (item.get("content") or "").strip()
                articles.append({
                    "title": title,
                    "link": link,
                    "content": summary,  # 暂存摘要，后续批量抓取全文
                    "source": self.name,
                    "publish_time": int(pub_time.timestamp()) if pub_time else 0,
                })

                if len(articles) >= max_articles:
                    break

            if len(articles) >= max_articles:
                break

        # 批量抓取原文全文（替代一句话摘要）
        if articles:
            print(f"   📄 [{self.name}] 抓取 {len(articles)} 篇原文全文...")
            for art in articles:
                full = self._fetch_full_article(art["link"])
                if full:
                    art["content"] = full
                # 抓取失败保留原摘要（降级）
                time.sleep(1)  # 礼貌延迟

        print(f"   ✅ [{self.name}] 获取到 {len(articles)} 篇文章")
        return articles

    def _fetch_full_article(self, url: str) -> str:
        """
        抓取36氪文章页面全文。
        优先使用 div[class*=text]（纯正文，不含标题/日期头部），
        降级到通用 fetch_page_content。
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            return ""

        try:
            resp = self._http_get(url)
            if not resp:
                return ""
            soup = BeautifulSoup(resp.text, "lxml")

            # 36氪特有：div[class*=text] 是纯正文容器
            for el in soup.select("div[class*=text]"):
                text = el.get_text(separator="\n", strip=True)
                if len(text) > 200:
                    return text

            # 降级：div.article-content（含标题头部，由 clean_article_text 清洗）
            ac = soup.select_one("div.article-content")
            if ac:
                text = ac.get_text(separator="\n", strip=True)
                if len(text) > 200:
                    return text
        except Exception as e:
            print(f"   ⚠️ [{self.name}] 全文抓取失败 {url[:50]}: {e}")

        # 最终降级：通用抓取
        return fetch_page_content(url, timeout=self.timeout, user_agent=self.user_agent)

    def _parse_pub_time(self, pub_str: str) -> datetime:
        """解析 'YYYY-MM-DD HH:MM:SS' 格式时间（视为北京时间）"""
        if not pub_str:
            return None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(pub_str.strip(), fmt).replace(tzinfo=TZ_SHANGHAI)
            except ValueError:
                continue
        return None
