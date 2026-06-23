#!/usr/bin/env python3
"""聚合5月份所有日期的 classification.json，输出分类汇总。"""
import json
import os
from pathlib import Path
from collections import defaultdict

base = Path("/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/daily")

# 收集所有5月日期
may_dirs = sorted([d for d in base.iterdir() if d.is_dir() and d.name.startswith("2026-05-")])

all_data = {}  # date -> classification
stats = defaultdict(lambda: {"国际": 0, "国内": 0, "同业": 0, "其他": 0})

for d in may_dirs:
    cf = d / "classification.json"
    if not cf.exists():
        continue
    data = json.loads(cf.read_text(encoding="utf-8"))
    all_data[d.name] = data

# 输出摘要
print(f"=== 5月共 {len(all_data)} 天数据 ===\n")

# 按类别汇总所有文章
by_category = defaultdict(list)
for date, data in all_data.items():
    classification = data.get("classification", {})
    for cat, articles in classification.items():
        for a in articles:
            by_category[cat].append({
                "date": date,
                "title": a.get("title", ""),
                "source": a.get("source", ""),
                "digest": a.get("digest", ""),
                "link": a.get("link", ""),
            })

print("=== 各类别文章总数 ===")
for cat in ["国际", "国内", "同业", "其他"]:
    print(f"{cat}: {len(by_category[cat])} 篇")

print("\n=== 同业观察 (所有条目) ===")
for a in by_category["同业"]:
    print(f"\n【{a['date']}】{a['title']}")
    print(f"  来源: {a['source']}")
    print(f"  摘要: {a['digest']}")

# 输出完整 JSON 供后续使用
out_path = Path("/tmp/may2026_aggregated.json")
output = {
    "stats": {cat: len(by_category[cat]) for cat in ["国际", "国内", "同业", "其他"]},
    "by_category": dict(by_category),
}
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n完整数据已输出到: {out_path}")
