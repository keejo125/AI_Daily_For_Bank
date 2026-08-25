#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标题中文化机器化闸门（铁规6）。
检查 classification.json 中每篇 title 与对应 source .md 的 H1 是否含中文（非纯英文）。
命中纯英文标题 -> 退出码 1（阻断 push）。
同时校验 digest 覆盖率与 stats 一致性。
用法: python3 scripts/_title_gate.py <date>
"""
import json, re, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def has_cjk(s: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', s or ''))

def main():
    date = sys.argv[1] if len(sys.argv) > 1 else None
    if not date:
        print("usage: _title_gate.py <date>"); sys.exit(2)
    cj = ROOT / "daily" / date / "classification.json"
    d = json.load(open(cj, encoding="utf-8"))
    arts = []
    for c in ["国际", "国内", "同业", "其他"]:
        arts += d.get(c, [])

    errors = []
    # 1. title 中文闸门
    for a in arts:
        t = a.get("title", "")
        if not has_cjk(t):
            errors.append(f"[纯英文标题-分类] {a.get('source_file')}: {t!r}")
        dig = (a.get("digest") or "").strip()
        if len(dig) < 20:
            errors.append(f"[摘要过短] {a.get('source_file')}: len={len(dig)}")
        if dig == t:
            errors.append(f"[摘要=标题] {a.get('source_file')}")
    # 2. source .md H1 中文闸门
    for a in arts:
        p = ROOT / "daily" / date / a["source_file"]
        if not p.exists():
            errors.append(f"[source_file缺失] {a['source_file']}")
            continue
        txt = p.read_text(encoding="utf-8")
        m = re.search(r'^#\s+(.+)$', txt, re.M)
        h1 = m.group(1) if m else ""
        if not has_cjk(h1):
            errors.append(f"[纯英文H1] {a['source_file']}: {h1!r}")
    # 3. stats 一致性（category 是数组键，不在 article 内；按数组分别计数）
    stats = d.get("stats", {})
    expect = {c: 0 for c in ["国际", "国内", "同业", "其他"]}
    for c in ["国际", "国内", "同业", "其他"]:
        expect[c] = len([a for a in d.get(c, []) if not a.get("is_merged")])
    expect["total"] = sum(expect[c] for c in ["国际", "国内", "同业", "其他"])
    if stats != expect:
        errors.append(f"[stats不一致] actual={stats} expect={expect}")

    if errors:
        print("❌ 标题中文化闸门未通过，阻断 push：")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"✅ 标题中文化闸门通过：{len(arts)} 篇，全部含中文标题；digest覆盖率100%；stats一致={stats}")
    sys.exit(0)

if __name__ == "__main__":
    main()
