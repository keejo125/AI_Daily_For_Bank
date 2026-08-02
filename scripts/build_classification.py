#!/usr/bin/env python3
"""
从 sources/*.md 的 front matter 汇总生成 classification.json

用法: python3 build_classification.py YYYY-MM-DD

工作原理:
- 扫描 daily/YYYY-MM-DD/sources/*.md
- 解析每个文件的 YAML front matter（status, category, digest, is_model_related 等）
- 只有 status=confirmed 的文章才会进入 classification.json
- status=pending 的文章会被列出提醒（尚未被AI处理）
- 输出 daily/YYYY-MM-DD/classification.json（供 generate_html.py 消费）

架构定位:
- 本脚本是"派生索引生成器"，classification.json 不再由AI手写
- AI Agent 在 Step 3 中将分类/摘要结果写回每个 md 的 front matter
- 然后运行本脚本自动聚合
"""
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent


def parse_front_matter(filepath: Path) -> dict:
    """
    解析 markdown 文件的 YAML front matter（简易解析，不依赖 PyYAML）
    支持: key: value 和 key: | 多行文本
    """
    try:
        text = filepath.read_text(encoding='utf-8')
    except Exception:
        return {}

    # 提取 --- ... --- 之间的内容
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.S)
    if not m:
        return {}

    fm_text = m.group(1)
    result = {}
    current_key = None
    multiline_lines = []

    for line in fm_text.split('\n'):
        # 多行值续行（以空格开头）
        if current_key and (line.startswith('  ') or line.startswith('\t')):
            multiline_lines.append(line.strip())
            continue

        # 保存上一个多行值
        if current_key and multiline_lines:
            result[current_key] = '\n'.join(multiline_lines)
            current_key = None
            multiline_lines = []

        # 解析 key: value
        kv = re.match(r'^(\w[\w_]*)\s*:\s*(.*)', line)
        if kv:
            key, value = kv.group(1), kv.group(2).strip()
            if value == '|' or value == '>':
                # 多行文本开始
                current_key = key
                multiline_lines = []
            else:
                result[key] = value

    # 处理最后一个多行值
    if current_key and multiline_lines:
        result[current_key] = '\n'.join(multiline_lines)

    return result


def extract_title_and_meta(filepath: Path) -> dict:
    """从 markdown 正文提取标题、链接、来源"""
    try:
        text = filepath.read_text(encoding='utf-8')
    except Exception:
        return {}

    # 去掉 front matter
    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.S)

    title = ""
    link = ""
    source = ""

    for line in body.split('\n')[:10]:
        line = line.strip()
        if line.startswith('# ') and not title:
            title = line[2:].strip()
        elif '原文链接' in line:
            m = re.search(r'原文链接[：:]\s*(.+)', line)
            if m:
                link = m.group(1).strip()
        elif '来源' in line and not source:
            m = re.search(r'来源[：:]\s*(.+)', line)
            if m:
                source = m.group(1).strip()

    return {"title": title, "link": link, "source": source}


def main():
    if len(sys.argv) < 2:
        print("用法: python3 build_classification.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]
    sources_dir = PROJECT_DIR / "daily" / date_str / "sources"

    if not sources_dir.exists():
        print(f"❌ 目录不存在: {sources_dir}")
        sys.exit(1)

    md_files = sorted(sources_dir.glob("*.md"))
    if not md_files:
        print(f"❌ 无 markdown 文件: {sources_dir}")
        sys.exit(1)

    confirmed = []
    pending = []

    for md_file in md_files:
        fm = parse_front_matter(md_file)
        meta = extract_title_and_meta(md_file)

        status = fm.get("status", "pending")
        category = fm.get("category", "")
        digest = fm.get("digest", "")
        is_model_related = fm.get("is_model_related", "false").lower() == "true"
        publish_time = fm.get("publish_time", "0")

        article = {
            "aid": len(confirmed) + len(pending) + 1,
            "title": meta.get("title", md_file.stem),
            "source": meta.get("source", ""),
            "link": meta.get("link", ""),
            "digest": digest,
            "source_file": f"sources/{md_file.name}",
            "is_model_related": is_model_related,
            "publish_time": int(publish_time) if publish_time.isdigit() else 0,
        }

        if status == "confirmed" and category:
            confirmed.append((category, article))
        else:
            pending.append(article)

    # 按分类分组
    classification = {"date": date_str, "国际": [], "国内": [], "同业": [], "其他": []}
    for category, article in confirmed:
        if category in classification:
            classification[category].append(article)
        else:
            classification["其他"].append(article)

    # 重新编号 aid
    aid = 1
    for cat in ["国际", "国内", "同业", "其他"]:
        for art in classification[cat]:
            art["aid"] = aid
            aid += 1

    # 保存
    out_path = PROJECT_DIR / "daily" / date_str / "classification.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(classification, f, ensure_ascii=False, indent=2)

    # 统计
    total_confirmed = len(confirmed)
    print(f"📊 build_classification [{date_str}]")
    print(f"   已确认: {total_confirmed} 篇")
    for cat in ["国际", "国内", "同业", "其他"]:
        count = len(classification[cat])
        if count:
            print(f"     {cat}: {count}")
    if pending:
        print(f"   ⏳ 待处理(pending): {len(pending)} 篇")
        for p in pending[:5]:
            print(f"     - {p['title'][:40]}")
        if len(pending) > 5:
            print(f"     ... 还有 {len(pending)-5} 篇")
    print(f"   输出: {out_path}")


if __name__ == "__main__":
    main()
