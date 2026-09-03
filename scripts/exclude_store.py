"""
排除清单：记录已被判定删除的文章 URL。

存在的理由：
    filter_articles.py 用 filepath.unlink() 物理删除不匹配的文章，若不留下记录，
    下次 fetch 会因为"磁盘上没有这个文件"而把已删除的文章重新抓回来，
    导致每次重跑 sources/ 目录都会重新长出一堆已被人工/规则淘汰的垃圾。

用法：
    from exclude_store import load_excluded, add_excluded
    excluded = load_excluded()            # fetch 时跳过这些 URL
    add_excluded([url1, url2])            # filter/删除时登记
"""
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
EXCLUDE_PATH = PROJECT_DIR / "config" / "excluded_links.json"


def load_excluded():
    """读取排除清单，返回 URL 集合"""
    if not EXCLUDE_PATH.exists():
        return set()
    try:
        data = json.loads(EXCLUDE_PATH.read_text(encoding="utf-8"))
        return set(data.get("urls", []))
    except (json.JSONDecodeError, IOError):
        return set()


def add_excluded(links, reason="filtered"):
    """登记 URL 到排除清单（去重、保持顺序），返回新增条数"""
    links = [l for l in links if l]
    if not links:
        return 0

    if EXCLUDE_PATH.exists():
        try:
            data = json.loads(EXCLUDE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            data = {}
    else:
        data = {}

    urls = data.get("urls", [])
    history = data.get("history", [])
    known = set(urls)
    added = 0
    for link in links:
        if link not in known:
            urls.append(link)
            history.append({"url": link, "reason": reason})
            known.add(link)
            added += 1

    EXCLUDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["urls"] = urls
    data["history"] = history[-2000:]
    EXCLUDE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return added
