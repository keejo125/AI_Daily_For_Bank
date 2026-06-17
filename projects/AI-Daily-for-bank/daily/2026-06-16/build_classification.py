#!/usr/bin/env python3
"""Build classification.json for 2026-06-16"""
import json
from datetime import datetime

with open('daily/2026-06-16/filtered_articles.json', 'r') as f:
    data = json.load(f)

articles = data['articles']
deleted = []
classification = {"国际": [], "国内": [], "同业": [], "其他": []}

for i, a in enumerate(articles):
    title = a['title']
    digest = a.get('digest', '') or ''
    src = a.get('source', '')
    link = a.get('link', '')
    sf = a.get('source_file', '')
    aid = a.get('aid', '')
    full = f"{title} {digest}"

    # === DELETE RULES ===
    delete_reason = None
    # 财务/融资（林俊旸融资新闻）
    if ('林俊旸' in full or '估值135亿' in full or '投后估值' in full) and \
       ('投了' in title or '入局' in title or '估值' in title):
        delete_reason = '财务/融资'
    
    if delete_reason:
        deleted.append({"index": i, "title": title, "source": src, "reason": delete_reason})
        continue

    # === CLASSIFICATION ===
    cat = None
    is_model = False
    reason = ''

    # --- 国际 ---
    if '谷歌' in full and '大模型' in full and '10倍' in full:
        cat = '国际'
        reason = '谷歌首席工程师论大模型对软件工程生态的10倍提速冲击'
        is_model = True
    elif '华盛顿' in full and 'AI末日' in full:
        cat = '国际'
        reason = '全球40名顶尖专家在华盛顿举行AI安全闭门会议'
        is_model = False

    # --- 同业 ---
    elif '银行' in src or ('银行' in full and 'AI' in full):
        if 'AI规划' in full or '华瑞' in full:
            cat = '同业'
            reason = '华瑞银行构建AI规划体系，科技罚单后强化合规'
            is_model = False

    # --- 国内 ---
    elif 'AgentSociety' in full and '清华' in full:
        cat = '国内'
        reason = '清华团队推出AgentSociety²：AI Scientists进军社会科学'
        is_model = True
    elif 'Harness' in full and '工程化' in full:
        cat = '国内'
        reason = '阿里云AI Coding的Harness工程化实践分享'
        is_model = False
    elif '前沿部署工程师' in full and '录屏教学' in full:
        cat = '国内'
        reason = 'AI前沿部署工程师(FDE)角色变革：录屏教学替代300万年薪专家'
        is_model = False
    elif '支付宝' in full and '内测' in full:
        cat = '国内'
        reason = 'AI版支付宝内测曝光，搭载"阿宝"助手'
        is_model = False
    elif '支付宝' in full and '重做' in full:
        cat = '国内'
        reason = '支付宝全端AI化重塑，首个超级应用AI转型样本'
        is_model = False
    elif '电商' in full and 'AI 操作系统' in full:
        cat = '国内'
        reason = '电商AI操作系统：从工具人到All-in-One智能大脑的演进'
        is_model = False

    # --- 其他 ---
    elif '人大附中' in full or 'AI原住人才' in full:
        cat = '其他'
        reason = '人大附中校长谈AI人才培养'
        is_model = False
    elif '腾讯研究院AI速递' in title:
        cat = '其他'
        reason = '腾讯研究院AI综合资讯速递'
        is_model = False
    elif 'iPhone' in title or ('极客早知道' in digest and 'SpaceX' in title):
        cat = '其他'
        reason = '综合资讯快报（消费电子+航天+招行AI信用卡）'
        is_model = False
    else:
        cat = '其他'
        reason = '暂未明确归类'
        is_model = False

    # Fix empty source
    if not src:
        if '腾讯研究院' in title:
            src = '腾讯研究院'
        else:
            src = '未知来源'

    entry = {
        "aid": aid,
        "title": title,
        "source": src,
        "link": link,
        "digest": digest if digest else title,
        "source_file": sf,
        "category_reason": reason,
        "is_model_related": is_model
    }
    classification[cat].append(entry)

# Sort: model-related first
for cat in classification:
    classification[cat].sort(key=lambda a: (not a.get('is_model_related', False), a['title']))

stats = {cat: len(classification[cat]) for cat in classification}
stats['total'] = sum(stats.values())

result = {
    "date": "2026-06-16",
    "generated_at": datetime.now().isoformat(),
    "classification": classification,
    "stats": stats,
    "deleted": deleted
}

with open('daily/2026-06-16/classification.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"📊 分类: 国际{stats['国际']} 国内{stats['国内']} 同业{stats['同业']} 其他{stats['其他']} 共{stats['total']}")
print(f"🗑️ 删除{len(deleted)}篇")
for d in deleted:
    print(f"   [{d['reason']}] {d['title'][:70]}")
for cat in classification:
    print(f"\n--- {cat} ---")
    for a in classification[cat]:
        m = '⭐' if a.get('is_model_related') else '  '
        print(f"  {m} [{a['source']}] {a['title'][:65]}")
