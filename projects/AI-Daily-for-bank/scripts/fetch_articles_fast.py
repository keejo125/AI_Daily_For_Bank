#!/usr/bin/env python3
"""
优化版：通过 /api/rss/export/{date} 导出接口获取微信公众号文章

与 fetch_articles.py 功能相同，保留此文件以兼容旧调用方式。
所有优化已在 fetch_articles.py v2 中完成：单次 API 调用替代翻页+逐篇抓取。

用法: python3 fetch_articles_fast.py [YYYY-MM-DD]
不传日期则默认昨天
"""
import sys
import os

# 直接调用主脚本的 main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 复用 fetch_articles.py 的逻辑
from fetch_articles import main

if __name__ == "__main__":
    main()
