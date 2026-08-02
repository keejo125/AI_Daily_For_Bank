#!/usr/bin/env python3
"""
手动投稿链接管理脚本

用法:
  python3 add_manual_link.py <url> [来源名称]
  python3 add_manual_link.py --list          # 查看待处理链接
  python3 add_manual_link.py --clear-used    # 清理已使用的链接

示例:
  python3 add_manual_link.py "https://mp.weixin.qq.com/s/xxx" "银行科技研究社"
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
MANUAL_LINKS_PATH = PROJECT_DIR / "manual_links.json"

TZ_SHANGHAI = timezone(timedelta(hours=8))


def load_links() -> list:
    """读取 manual_links.json"""
    if not MANUAL_LINKS_PATH.exists():
        return []
    try:
        with open(MANUAL_LINKS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_links(links: list):
    """保存 manual_links.json"""
    with open(MANUAL_LINKS_PATH, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)


def add_link(url: str, source: str = "手动投稿"):
    """添加一条手动投稿链接"""
    links = load_links()

    # 检查是否已存在
    for item in links:
        if item["url"] == url:
            print(f"⚠️ 链接已存在: {url}")
            if item.get("used"):
                print("   （该链接已被使用过）")
            return

    now = datetime.now(TZ_SHANGHAI).strftime("%Y-%m-%d")
    links.append({
        "url": url,
        "source": source,
        "added_at": now,
        "used": False
    })
    save_links(links)
    print(f"✅ 已添加: {url}")
    print(f"   来源: {source}")
    print(f"   日期: {now}")


def list_pending():
    """列出待处理的链接"""
    links = load_links()
    pending = [l for l in links if not l.get("used")]
    used = [l for l in links if l.get("used")]

    print(f"📋 手动投稿链接 ({len(pending)} 待处理, {len(used)} 已使用)")
    if pending:
        print("\n待处理:")
        for item in pending:
            print(f"  • [{item.get('added_at', '?')}] {item.get('source', '?')}: {item['url']}")
    if not pending:
        print("\n  （无待处理链接）")


def clear_used():
    """清理已使用的链接"""
    links = load_links()
    pending = [l for l in links if not l.get("used")]
    removed = len(links) - len(pending)
    save_links(pending)
    print(f"🧹 已清理 {removed} 条已使用链接，保留 {len(pending)} 条待处理")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg1 = sys.argv[1]

    if arg1 == "--list":
        list_pending()
    elif arg1 == "--clear-used":
        clear_used()
    elif arg1.startswith("http"):
        source = sys.argv[2] if len(sys.argv) > 2 else "手动投稿"
        add_link(arg1, source)
    else:
        print(f"❌ 无效参数: {arg1}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
