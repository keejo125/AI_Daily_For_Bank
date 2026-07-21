#!/usr/bin/env python3
"""Build classification.json for 2026-07-21"""
import json, os

date = "2026-07-21"
base = f"daily/{date}"

with open(f"{base}/filtered_articles.json") as f:
    data = json.load(f)
articles = data["articles"]

# ---- Manual classification decisions ----
# (index, category, is_model_related)
# category: 国际|国内|同业|其他|X(delete)

decisions = {
    # Delete
    0:  ("X",  False, "纯商业营销"),       # Qoder极致包
    4:  ("X",  False, "活动宣传"),          # Qoder Security直播预告
    
    # 国际 (7)
    15: ("国际", False),  # 西门子工业AI (德国)
    26: ("国际", False),  # WordPress 7.0 (开源国际项目)
    27: ("国际", False),  # vLLM多模态推理 (UC Berkeley/国际开源)
    30: ("国际", False),  # 谷歌Frozen v2芯片
    35: ("国际", False),  # Agent Primitives (UIUC)
    38: ("国际", True),   # Fable 5推翻雅可比猜想
    39: ("国际", True),   # OpenAI叫停GPT-6
    
    # 同业 (3)
    19: ("同业", False),  # 摩根大通控制AI支出
    23: ("同业", False),  # 智能体开启数智反诈
    24: ("同业", False),  # 生成式AI养老金融
    
    # 其他 (9)
    5:  ("其他", False),  # 高薪岗位人才报告
    6:  ("其他", False),  # 运维行业变天(职业趋势)
    9:  ("其他", False),  # LibTV Agent体验(产品体验)
    13: ("其他", False),  # AI女神假慈善(AI滥用/社会)
    21: ("其他", False),  # AI理解因果(科普讨论)
    29: ("其他", False),  # WAIC闭幕(综合资讯)
    36: ("其他", False),  # 中国企业All in AI(综合资讯)
    37: ("其他", False),  # 财经下午茶(会议讨论)
    40: ("其他", False),  # 腾讯研究院AI速递(综合资讯)
    
    # 国内 (rest, 20)
    1:  ("国内", False),   # 斑马鱼→空天AI平台
    2:  ("国内", False),   # 世界模型六小龙WAIC
    3:  ("国内", True),    # 小红书大模型IMO
    7:  ("国内", False),   # 大模型重塑运维
    8:  ("国内", False),   # 聆思端侧AI芯片
    10: ("国内", False),   # 具身智能WAIC
    11: ("国内", False),   # Vibe Coding→AI原生团队
    12: ("国内", False),   # 中国AI交卷(算账)
    14: ("国内", False),   # AI终端标准化
    16: ("国内", False),   # Qoder CLI + tldraw
    17: ("国内", False),   # 平头哥开源SAIL
    18: ("国内", False),   # 超算+智算底座
    20: ("国内", False),   # 苏度具身智能
    22: ("国内", True),    # ProLaViT视觉推理
    25: ("国内", False),   # OpenSQZ Glass
    28: ("国内", False),   # Qoder Security
    31: ("国内", True),    # Matrix-Game 3.5
    32: ("国内", False),   # 物理AI闭环(日冕+远图)
    33: ("国内", False),   # AI超级电网Token
    34: ("国内", False),   # 图灵鉴X
}

classified = {"国际": [], "国内": [], "同业": [], "其他": []}
excluded = []

for i, a in enumerate(articles):
    src = a.get('source', '') or ''
    title = a.get('title', '')
    digest = a.get('digest', '') or ''
    link = a.get('link', '')
    sf = a.get('source_file', '')
    aid = a.get('aid', '')
    
    # Fix source for #40
    if i == 40 and not src:
        src = "腾讯研究院"
    
    if i in decisions:
        dec = decisions[i]
        cat = dec[0]
        if cat == "X":
            reason = dec[2]
            excluded.append({"title": title, "source": src, "reason": reason, "aid": aid, "source_file": sf})
            continue
        is_model = dec[1]
    else:
        raise ValueError(f"未分类: #{i} {title[:40]}")
    
    entry = {
        "aid": aid,
        "title": title,
        "source": src,
        "link": link,
        "digest": digest,
        "source_file": sf,
        "is_model_related": is_model
    }
    classified[cat].append(entry)

# Sort: model-related first within each category
for cat in classified:
    classified[cat].sort(key=lambda x: (not x.get('is_model_related', False), x.get('title', '')))

stats = {cat: len(classified[cat]) for cat in classified}
stats["total"] = sum(stats.values())

output = {
    "date": date,
    "generated_at": "2026-07-22T06:40:00+08:00",
    "classification": classified,
    "stats": stats,
    "excluded": excluded
}

with open(f"{base}/classification.json", 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("=== 分类完成 ===")
for cat in ["国际","国内","同业","其他"]:
    arts = classified[cat]
    model_n = sum(1 for a in arts if a.get('is_model_related'))
    print(f"{cat}: {len(arts)} 篇 (模型相关: {model_n})")
print(f"删除: {len(excluded)} 篇")
print(f"总计: {stats['total']} + {len(excluded)} = {len(articles)}")

# Print per-cat breakdown
for cat in ["国际","国内","同业","其他"]:
    print(f"\n--- {cat} ---")
    for a in classified[cat]:
        m = "🧠" if a.get('is_model_related') else "  "
        print(f"  {m} [{a['source']}] {a['title'][:60]}")

print(f"\n--- 删除 ---")
for e in excluded:
    print(f"  [{e['source']}] {e['title'][:50]} ({e['reason']})")
