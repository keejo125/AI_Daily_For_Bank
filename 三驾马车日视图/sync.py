#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 daily-trends.json 注入到 index.html 的 `let DATA = {...};` 中（幂等）。
幂等：无论 index.html 当前是占位符还是已内嵌数据，都替换现有 DATA 声明，
因此可被 build 之后反复调用，也支持「审核 → 重跑 build → 重跑 sync」的闭环。

用法:
    python3 sync.py            # 用 json 重建 index.html 内嵌数据
    python3 sync.py --check    # 仅校验 json 合法性
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(HERE, "daily-trends.json")
HTML_PATH = os.path.join(HERE, "index.html")


def load_json():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    data = load_json()
    assert "meta" in data and "trends" in data, "json 缺少 meta / trends"
    days = data["meta"]["days"]
    car_ids = {c["id"] for c in data["meta"]["carriages"]}
    src_ids = {s["id"] for s in data["meta"]["sources"]}
    for i, t in enumerate(data["trends"]):
        for k in ("id", "term", "sub", "carriage", "source", "first", "last", "status", "examples"):
            assert k in t, f"trend #{i} 缺少字段 {k}"
        assert t["carriage"] in car_ids, f"trend {t['id']} 的 carriage 无效"
        assert t["first"] in days and t["last"] in days, f"trend {t['id']} 的日期越界"
        assert t["source"] and all(s in src_ids for s in t["source"]), f"trend {t['id']} 的 source 无效"

    if "--check" in sys.argv:
        print(f"OK: {len(data['trends'])} 条趋势，天数 {len(days)}")
        return

    payload = json.dumps(data, ensure_ascii=False, indent=2)
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    anchor = "let DATA = "
    i = html.find(anchor)
    if i < 0:
        raise SystemExit("index.html 未找到 `let DATA = ` 声明")
    start = i + len(anchor)
    # 用括号匹配找 DATA 对象的结束 '}'，再吃掉其后的 ';'
    depth, instr, esc, q = 0, False, False, ""
    end = None
    for k in range(start, len(html)):
        c = html[k]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == q:
                instr = False
            continue
        if c in "\"'":
            instr, q = True, c
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = k + 1
                break
    if end is None:
        raise SystemExit("无法定位 DATA 对象结束位置")
    semi = html.find(";", end)
    if semi < 0:
        raise SystemExit("DATA 声明后未找到分号")
    # 用函数作为 repl，避免 payload 中的 \\n 被 re.sub 当成转义
    html = html[:i] + anchor + payload + ";" + html[semi + 1:]
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已注入 {len(data['trends'])} 条趋势到 index.html")


if __name__ == "__main__":
    main()
