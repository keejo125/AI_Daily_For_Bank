#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3 回写助手 v2 —— 稳健版。
- 解析 front matter，保证 category / is_model_related / digest / status / source 字段一定存在（新增或覆盖）。
- 保留 publish_time / link / title（若存在）。
- digest 以 `|` 多行块写入（与 build_classification 简易解析兼容）。
- 若决策含 h1，则回写正文首个 `# ` 标题行。
- action=delete 直接物理删除文件（已删则跳过）。
用法: python3 scripts/_step3_update_v2.py <decisions.json>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "daily" / "{date}" / "sources"


def parse_fm(text: str):
    m = re.match(r'^---\s*\n(.*?)\n---\n(.*)$', text, re.S)
    if not m:
        return None, text
    return m.group(1), m.group(2)


def write_back(date_str: str, decision: dict):
    fn = decision["file"]
    fp = SOURCES.parent / "{date}" / "sources" / fn  # placeholder
    fp = ROOT / "daily" / date_str / "sources" / fn
    if decision.get("action") == "delete":
        if fp.exists():
            fp.unlink()
            print(f"  [DELETE] {fn}")
        else:
            print(f"  [DELETE-skip 已不存在] {fn}")
        return

    if not fp.exists():
        print(f"  [SKIP 文件不存在] {fn}")
        return

    raw = fp.read_text(encoding="utf-8")
    fm_text, body = parse_fm(raw)
    if fm_text is None:
        print(f"  [ERROR 无front matter] {fn}")
        return

    # 解析已有 front matter 为有序键值
    existing = {}
    cur_key = None
    cur_lines = []
    fm_lines = fm_text.split("\n")
    for line in fm_lines:
        if cur_key is not None and (line.startswith("  ") or line.startswith("\t")):
            cur_lines.append(line.strip())
            continue
        if cur_key is not None and cur_lines:
            existing[cur_key] = "\n".join(cur_lines)
            cur_key = None
            cur_lines = []
        kv = re.match(r'^(\w[\w_]*)\s*:\s*(.*)', line)
        if kv:
            k, v = kv.group(1), kv.group(2).strip()
            if v in ("|", ">"):
                cur_key = k
                cur_lines = []
            else:
                existing[k] = v
    if cur_key is not None and cur_lines:
        existing[cur_key] = "\n".join(cur_lines)

    # 用决策覆盖/新增关键字段
    existing["status"] = "confirmed"
    existing["source"] = decision.get("source") or existing.get("source", "")
    existing["category"] = decision.get("category", "")
    existing["is_model_related"] = "true" if decision.get("is_model_related") else "false"
    digest = (decision.get("digest") or "").strip()
    existing["digest"] = digest

    # H1 标题回写
    if decision.get("h1"):
        body = re.sub(r'^#\s+.*$', "# " + decision["h1"], body, count=1, flags=re.M)

    # 固定顺序重建 front matter（保留 publish_time/link/title 等原值）
    order = ["publish_time", "link", "source", "status",
             "category", "is_model_related", "digest", "title"]
    out = ["---"]
    for k in order:
        if k in existing:
            if k == "digest":
                out.append("digest: |")
                for dl in digest.split("\n"):
                    out.append("  " + dl)
            else:
                out.append(f"{k}: {existing[k]}")
    # 补齐 order 之外的其它原字段（如有）
    for k, v in existing.items():
        if k not in order:
            if "\n" in str(v):
                out.append(f"{k}: |")
                for dl in str(v).split("\n"):
                    out.append("  " + dl)
            else:
                out.append(f"{k}: {v}")
    out.append("---")

    new_text = "\n".join(out) + "\n" + body
    fp.write_text(new_text, encoding="utf-8")
    print(f"  [WRITE] {fn}  cat={existing['category']} model={existing['is_model_related']}")


def main():
    if len(sys.argv) < 2:
        print("usage: _step3_update_v2.py <decisions.json>")
        sys.exit(1)
    dec = json.load(open(sys.argv[1], encoding="utf-8"))
    date_str = dec.get("date")
    if not date_str:
        # 从文件名推断
        import glob
        fs = glob.glob(str(ROOT / "daily" / "*" / "sources" / "*.md"))
        date_str = sorted(fs)[-1].split("/")[-3] if fs else None
    assert date_str, "无法确定 date"
    print(f"date={date_str}, 共 {len(dec['decisions'])} 条决策")
    for d in dec["decisions"]:
        write_back(date_str, d)
    print("done.")


if __name__ == "__main__":
    main()
