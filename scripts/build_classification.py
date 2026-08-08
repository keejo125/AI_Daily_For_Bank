#!/usr/bin/env python3
"""
从 sources/*.md front matter + merge_plan.json 纯聚合生成 classification.json

用法: python3 build_classification.py YYYY-MM-DD

v3.5 架构（根治 field 丢失问题）:
  - 单篇文章的所有字段（category, digest, is_model_related, link, source）全部来自 front matter
  - 跨文章合并信息（is_merged, source_items）来自 merge_plan.json
  - 本脚本只做聚合 + 排序 + 重新编号 aid，不做任何"猜测"或"补全"
  - AI Agent 在 Step 3 将分类/摘要写回 front matter，合并信息写入 merge_plan.json
  - 然后运行本脚本一键生成 classification.json

优势:
  - 不再从正文推断 title/link/source（前端 matter 已有，不会丢）
  - link 不会因为 JSON 被覆盖而丢失（源在 front matter）
  - 合并信息独立存储（merge_plan.json 人类可读可检查）
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

    m = re.match(r'^---\s*\n(.*?)\n---', text, re.S)
    if not m:
        return {}

    fm_text = m.group(1)
    result = {}
    current_key = None
    multiline_lines = []

    for line in fm_text.split('\n'):
        if current_key and (line.startswith('  ') or line.startswith('\t')):
            multiline_lines.append(line.strip())
            continue

        if current_key and multiline_lines:
            result[current_key] = '\n'.join(multiline_lines)
            current_key = None
            multiline_lines = []

        kv = re.match(r'^(\w[\w_]*)\s*:\s*(.*)', line)
        if kv:
            key, value = kv.group(1), kv.group(2).strip()
            if value in ('|', '>'):
                current_key = key
                multiline_lines = []
            else:
                result[key] = value

    if current_key and multiline_lines:
        result[current_key] = '\n'.join(multiline_lines)

    return result


def extract_title_from_body(filepath: Path) -> str:
    """从正文提取标题（仅兜底，front matter 无 title 时用）"""
    try:
        text = filepath.read_text(encoding='utf-8')
    except Exception:
        return ""

    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.S)
    for line in body.split('\n')[:5]:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return ""


def load_merge_plan(date_str: str) -> dict:
    """
    读取 merge_plan.json（如果存在）
    
    格式:
    {
      "merged_groups": [
        {
          "main": "sources/主文章.md",
          "items": [
            {"source_file": "sources/从条1.md", "name": "来源A", "link": "..."},
            {"source_file": "sources/从条2.md", "name": "来源B", "link": "..."}
          ]
        }
      ]
    }
    
    返回: {从条source_file -> 主条source_file} 映射 + {主条source_file -> source_items}
    """
    plan_path = PROJECT_DIR / "daily" / date_str / "merge_plan.json"
    if not plan_path.exists():
        return {}, {}
    
    try:
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan = json.load(f)
    except Exception:
        return {}, {}
    
    merged_to_main = {}   # merged source_file -> main source_file
    main_items = {}       # main source_file -> [source_items]
    
    for group in plan.get("merged_groups", []):
        main_sf = group.get("main", "")
        items = group.get("items", [])
        main_items[main_sf] = items
        for item in items:
            merged_sf = item.get("source_file", "")
            if merged_sf:
                merged_to_main[merged_sf] = main_sf
    
    return merged_to_main, main_items


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

    # 加载合并计划
    merged_to_main, main_items = load_merge_plan(date_str)

    confirmed = []
    pending = []

    for md_file in md_files:
        fm = parse_front_matter(md_file)
        sf = f"sources/{md_file.name}"
        
        status = fm.get("status", "pending")
        category = fm.get("category", "")
        
        # 从 front matter 读取所有字段（不再从正文推测）
        article = {
            "title": extract_title_from_body(md_file) or md_file.stem,
            "source": fm.get("source", ""),           # 公众号名称/router
            "link": fm.get("link", ""),                # 原文 URL
            "digest": fm.get("digest", ""),
            "source_file": sf,
            "is_model_related": fm.get("is_model_related", "false").lower() == "true",
            "publish_time": int(fm.get("publish_time", "0")),
        }

        if status == "confirmed" and category:
            confirmed.append((category, article))
        else:
            pending.append(article)

    # 按分类分组
    classification = {"date": date_str, "国际": [], "国内": [], "同业": [], "其他": []}
    for category, article in confirmed:
        bucket = category if category in classification else "其他"
        classification[bucket].append(article)

    # 应用合并计划：从条标记 is_merged=True，主条注入 source_items
    for cat in ["国际", "国内", "同业", "其他"]:
        for art in classification[cat]:
            sf = art["source_file"]
            if sf in merged_to_main:
                # 从条：标记跳过
                art["is_merged"] = True
                art["merged_into"] = merged_to_main[sf]
            elif sf in main_items:
                # 主条：注入 source_items
                items = main_items[sf]
                art["source_items"] = items
                # 主条自己的 source 也要放进列表开头
                own = {
                    "name": art.get("source", ""),
                    "link": art.get("link", "")
                }
                art["source_items"] = [own] + items
            else:
                # 普通文章：构建单元素 source_items
                if not art.get("source_items"):
                    art["source_items"] = [{
                        "name": art.get("source", ""),
                        "link": art.get("link", "")
                    }]

    # 排序: model_related 排前, merged 排后
    for cat in ["国际", "国内", "同业", "其他"]:
        classification[cat].sort(key=lambda x: (
            x.get("is_merged", False),
            not x.get("is_model_related", False),
        ))

    # 重新编号 aid
    aid = 1
    for cat in ["国际", "国内", "同业", "其他"]:
        for art in classification[cat]:
            art["aid"] = aid
            aid += 1

    # stats
    stats = {cat: len([a for a in classification[cat] if not a.get("is_merged")]) 
             for cat in ["国际", "国内", "同业", "其他"]}
    stats["total"] = sum(stats.values())
    classification["stats"] = stats

    # 保存
    out_path = PROJECT_DIR / "daily" / date_str / "classification.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(classification, f, ensure_ascii=False, indent=2)

    # 统计输出
    total_confirmed = len(confirmed)
    merged_count = sum(1 for art in (a for _, a in confirmed) if art.get("is_merged"))
    print(f"📊 build_classification [{date_str}]")
    print(f"   已确认: {total_confirmed} 篇（含合并从条 {merged_count} 篇）")
    for cat in ["国际", "国内", "同业", "其他"]:
        count = stats[cat]
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
