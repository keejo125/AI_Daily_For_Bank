#!/usr/bin/env python3
"""
数据源适配器基类 + 工具函数
"""
import re
import time

import requests


class BaseSourceAdapter:
    """
    数据源适配器基类

    架构契约：所有信源适配器（RSS、公众号RSS、官方API、热榜聚合等）都必须：
    1. 继承本类并实现 fetch(date_str) -> list
    2. 返回统一的文章结构: [{"title", "link", "content", "source", "publish_time"}, ...]
    3. 单信源内部异常自行降级（返回空列表或部分结果），不向上抛出中断管线
    编排层（fetch_web_articles.py）只依赖这个统一结构，不感知信源差异。
    """

    def __init__(self, source_config: dict, global_settings: dict, article_fetch_api: str = ""):
        self.config = source_config
        self.settings = global_settings
        self.name = source_config.get("name", "unknown")
        self.url = source_config.get("url", "")
        self.timeout = global_settings.get("fetch_timeout", 30)
        self.user_agent = global_settings.get(
            "user_agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        # 微信全文获取API（仅部分适配器使用，其他忽略）
        self.article_fetch_api = article_fetch_api

    def fetch(self, date_str: str) -> list:
        """
        获取指定日期的文章列表
        返回: [{"title", "link", "content", "source", "publish_time"}, ...]
        子类必须实现此方法
        """
        raise NotImplementedError

    def _get_headers(self):
        """构建请求头"""
        return {
            "User-Agent": self.user_agent,
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        }

    def _http_get(self, url: str, timeout: int = None) -> requests.Response:
        """带重试的 GET 请求"""
        timeout = timeout or self.timeout
        retry_count = self.settings.get("retry_count", 3)
        for attempt in range(1, retry_count + 1):
            try:
                resp = requests.get(url, headers=self._get_headers(), timeout=timeout)
                resp.raise_for_status()
                return resp
            except Exception as e:
                print(f"   ⚠️ [{self.name}] HTTP GET 失败 (第{attempt}次): {e}")
                if attempt < retry_count:
                    time.sleep(2 * attempt)
        return None


def fetch_page_content(url: str, timeout: int = 30, user_agent: str = None) -> str:
    """
    抓取网页正文（用于官网RSS摘要型源）
    优先级：<article> > div.article-content > div.post-content > main
    降级：提取失败返回空字符串
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("   ⚠️ beautifulsoup4 未安装，无法抓取网页正文")
        return ""

    headers = {
        "User-Agent": user_agent or "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        print(f"   ⚠️ 网页抓取失败 {url}: {e}")
        return ""

    soup = BeautifulSoup(resp.text, "lxml")

    # 移除无关元素
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "iframe"]):
        tag.decompose()

    # 按优先级查找正文容器
    selectors = [
        "article",
        "div.article-content",
        "div.post-content",
        "div.entry-content",
        "div.content",
        "main",
    ]
    for selector in selectors:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 100:  # 至少100字才算有效正文
                return text

    # 兜底：取 body 全文
    body = soup.find("body")
    if body:
        text = body.get_text(separator="\n", strip=True)
        if len(text) > 200:
            return text

    return ""


def fetch_wechat_page(url: str, timeout: int = 30, user_agent: str = None) -> dict:
    """
    直接抓取微信公众号文章页面（适用于 mp.weixin.qq.com/s/xxx 短链）
    返回: {"title": str, "content": str, "author": str}
    失败返回空 dict
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return {}

    headers = {
        "User-Agent": user_agent or "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
    except Exception as e:
        print(f"   ⚠️ 微信页面抓取失败 {url[:60]}: {e}")
        return {}

    # 反爬检测
    if '环境异常' in resp.text[:3000] or '请在微信客户端打开' in resp.text[:3000]:
        print(f"   ⚠️ 微信反爬拦截: {url[:60]}")
        return {}

    soup = BeautifulSoup(resp.text, "lxml")

    # 提取标题
    title = ""
    title_el = soup.select_one("#activity-name") or soup.select_one(".rich_media_title")
    if title_el:
        title = title_el.get_text(strip=True)

    # 提取作者/公众号名
    author = ""
    author_el = soup.select_one("#js_name") or soup.select_one(".rich_media_meta_nickname")
    if author_el:
        author = author_el.get_text(strip=True)

    # 提取正文
    content = ""
    content_el = soup.select_one("#js_content") or soup.select_one(".rich_media_content")
    if content_el:
        # 移除图片标签（早报不需要）
        for img in content_el.find_all("img"):
            img.decompose()
        content = content_el.get_text(separator="\n", strip=True)

    if not title and not content:
        return {}

    return {"title": title, "content": content, "author": author}


def fetch_wechat_article(url: str, api_url: str, timeout: int = 60) -> str:
    """
    通过现有API获取微信文章全文
    POST {api_url} json={"url": article_link}
    返回纯文本正文，失败返回空字符串
    """
    try:
        resp = requests.post(api_url, json={"url": url}, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"   ⚠️ 微信文章API请求失败: {e}")
        return ""

    if not data or not isinstance(data, dict):
        return ""

    # 解析返回数据
    content_html = data.get("content", "")
    if not content_html:
        inner_data = data.get("data")
        if isinstance(inner_data, dict):
            content_html = inner_data.get("content", "")
    if not content_html:
        return ""

    return html_to_text(content_html)


def html_to_text(html_str: str) -> str:
    """简易 HTML → 纯文本：去标签、解码常见实体"""
    if not html_str:
        return ""
    # 去除 script/style
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_str, flags=re.S | re.I)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S | re.I)
    # 去除图片标签（含破碎的 "< img" 形式）
    text = re.sub(r'<\s*img[^>]*>', '', text, flags=re.I)
    # 换行标签
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.I)
    text = re.sub(r'</p>', '\n', text, flags=re.I)
    text = re.sub(r'</div>', '\n', text, flags=re.I)
    text = re.sub(r'</li>', '\n', text, flags=re.I)
    # 移除剩余标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除破碎标签（"< img" "< a" 等开头到行尾）
    text = re.sub(r'<\s*\w+[^>]*$', '', text, flags=re.M)
    text = re.sub(r'<\s*\w+[^>]*>', '', text)
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


def clean_article_text(text: str) -> str:
    """
    清洗文章正文：去除网站元数据、导航元素、广告等
    用于 fetch_page_content 和 RSS 全文提取后的后处理
    """
    if not text:
        return ""
    lines = text.split('\n')
    cleaned = []
    skip_patterns = [
        r'^\s*来源[：:]\s*$',       # "来源：" 单独一行
        r'^\s*公众号\s*\w+\s*$',    # "公众号 QbitAI"
        r'^\s*\d{4}-\d{2}-\d{2}\s*$',  # 纯日期行
        r'^\s*\d{2}:\d{2}:\d{2}\s*$',  # 纯时间行
        r'wx_img',                  # 微信图片ID
        r'qbitai-logo',             # 量子位logo
        r'^\s*微信扫一扫',
        r'^\s*扫码关注',
        r'^\s*点击.*关注',
        r'^\s*广告\s*$',
        r'^\s*推广\s*$',
        r'js-khan-academy',
    ]
    for line in lines:
        stripped = line.strip()
        # 跳过空行连续的（保留最多2个）
        if not stripped:
            cleaned.append('')
            continue
        # 跳过匹配模式的行
        skip = False
        for pat in skip_patterns:
            if re.search(pat, stripped):
                skip = True
                break
        if skip:
            continue
        cleaned.append(line)

    # 去除开头和结尾的空行
    result = '\n'.join(cleaned).strip()
    # 压缩连续空行
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result
