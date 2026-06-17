#!/usr/bin/env python3
"""Build classification.json for 2026-06-15"""
import json, re, unicodedata
from datetime import datetime

def normalize(s):
    """Normalize quotes and dashes for matching"""
    return s.replace('\u201c', '"').replace('\u201d', '"').replace('\u2018', "'").replace('\u2019', "'").replace('\u2013', '-').replace('\u2014', '--')

with open('daily/2026-06-15/filtered_articles.json', 'r') as f:
    data = json.load(f)

articles = data['articles']
deleted = []
classification = {"国际": [], "国内": [], "同业": [], "其他": []}

for i, a in enumerate(articles):
    title = a['title']
    nt = normalize(title)  # normalized title for matching
    digest = a.get('digest', '') or ''
    src = a.get('source', '')
    link = a.get('link', '')
    sf = a.get('source_file', '')
    aid = a.get('aid', '')
    full = f"{title} {digest}".lower()

    # === DELETE RULES ===
    delete_reason = None
    # 活动/培训/展览
    if any(kw in nt for kw in ['金融展抢先看', '金融展 |', '金融展倒计时', '金融展倒计时', '重磅亮相',
                                '实训营','明天北京开幕','大会预告','报名中','金融展邀请函',
                                'AIEC 2026','亮相金融展','重磅亮相金融展']):
        delete_reason = '活动宣传'
    # 人事/薪酬/财富
    elif any(kw in nt for kw in ['已套现', '套现950亿', '亿级富翁', '员工已套现', '富豪榜', '入职', '离职', '招人']):
        delete_reason = '人事/薪酬'
    # 财务/IPO/融资
    elif any(kw in nt for kw in ['发行债券', '融资', 'IPO', '上市', '过会', 'GPU四小龙', '估值', '融资']):
        delete_reason = '财务/IPO'
    # 招投标/采购
    elif '中标' in nt and '公有云' in nt:
        delete_reason = '招投标/采购'
    # 人才招聘
    elif any(kw in nt for kw in ['招聘', '招募', '人才社招', '英雄帖']):
        delete_reason = '人才招聘'

    if delete_reason:
        deleted.append({"index": i, "title": title, "source": src, "reason": delete_reason})
        continue

    # === CLASSIFICATION ===
    cat = None
    is_model = False
    reason = ''

    # --- 国际 ---
    # Fable 5 / GPT-5.6 / Anthropic models
    if 'Fable' in nt and ('暴毙' in nt or '封禁' in nt or '复刻' in nt or 'Orca' in nt):
        if 'OrcaRouter' in nt:
            reason = 'OrcaRouter多模型路由技术复刻Fable 5性能'
        else:
            reason = 'Anthropic旗舰模型Fable 5发布后遭政策封禁'
        cat = '国际'
        is_model = True
    elif 'GPT-5.6' in nt and '延迟' in nt:
        cat = '国际'
        reason = '受Fable 5封禁波及，OpenAI GPT-5.6或延迟发布'
        is_model = True
    elif ('巴西' in nt or 'Rio' in nt or '套壳国产' in nt or '套壳阿里' in nt) and ('套壳' in nt or 'SOTA' in nt or '黑马' in nt):
        cat = '国际'
        reason = '巴西Rio-3.5-Open-397B被指套壳阿里千问，开发者致歉下架，引发开源模型来源争议'
        is_model = True

    # --- 同业 ---
    elif any(kw in nt for kw in ['国开行', '国有银行', '银行']):
        if 'CIO' in nt or 'AI相关平台' in nt or ('AI' in nt and '平台建设' in nt):
            cat = '同业'
            reason = '国开行CIO获批，已启动AI相关平台建设'
            is_model = False

    # --- 国内 ---
    elif '摩尔线程' in nt or ('国产GPU' in nt and '训练' in nt):
        cat = '国内'
        reason = '摩尔线程国产GPU训练代码大模型刷榜硬核基准'
        is_model = False
    elif '循环工程' in nt and 'AI' in nt:
        cat = '国内'
        reason = 'AI工程实践方法论「循环工程」介绍'
        is_model = False
    elif '元宝' in nt and 'ima' in nt:
        cat = '国内'
        reason = '腾讯元宝接入ima知识库，提升搜索准确性和可溯源性'
        is_model = False
    elif 'Token 成本' in nt or 'Token 成本控制' in nt:
        cat = '国内'
        reason = 'AI Coding Agent的Token成本优化工程实践'
        is_model = False
    elif '航行日志' in nt or '航行日志全面开源' in nt:
        cat = '国内'
        reason = 'AI应用安全风险治理实践与航行日志开源'
        is_model = False
    elif 'Noiz' in nt and '音频' in nt:
        cat = '国内'
        reason = '港科大清华联合开源音频生成大模型，单卡0.24秒推理'
        is_model = True
    elif 'FDE' in nt and 'Cloud Agent' in nt:
        cat = '国内'
        reason = 'AI前置部署工程师(FDE)角色的Cloud Agent化演进'
        is_model = False
    elif '阿里云' in nt and 'i茅台' in nt:
        cat = '国内'
        reason = '阿里云中标i茅台公有云平台项目'
        is_model = False

    # --- 其他 ---
    elif '理想' in nt and '具身智能' in nt:
        cat = '其他'
        reason = '理想汽车具身智能产品演示'
        is_model = False
    elif 'AI在医疗' in nt or ('医疗' in nt and 'AI' in nt):
        cat = '其他'
        reason = 'AI在医疗领域应用的行业评论'
        is_model = False
    elif '谷歌CEO' in nt or ('谷歌' in nt and '斯坦福' in nt):
        cat = '其他'
        reason = '谷歌CEO斯坦福校园事件'
        is_model = False
    elif 'AI 眼镜' in nt or ('夏勇峰' in nt and '眼镜' in nt):
        cat = '其他'
        reason = 'AI眼镜产品经历与行业反思'
        is_model = False
    elif 'AI汽车' in nt or ('AI' in nt and '汽车' in nt and '物理世界' in nt):
        cat = '其他'
        reason = 'AI在汽车物理世界的应用展望'
        is_model = False
    elif '微软CEO' in nt or ('Token资本' in nt and '微软' in nt):
        cat = '其他'
        reason = '微软CEO纳德拉提出Token资本概念'
        is_model = False
    elif '极客公园' in src and ('苹果' in nt or 'Meta' in nt):
        cat = '其他'
        reason = '综合资讯快报（苹果机器人/Meta/北航）'
        is_model = False
    elif '腾讯研究院AI速递' in nt:
        cat = '其他'
        reason = '腾讯研究院AI综合资讯速递'
        is_model = False
    else:
        cat = '其他'
        reason = '暂未明确归类'
        is_model = False

    # Fill empty source
    if not src:
        if '腾讯研究院' in nt:
            src = '腾讯研究院'
        elif 'AI在医疗' in nt:
            src = '未知来源'
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

# Post-processing: sort & merge duplicates
for cat in classification:
    classification[cat].sort(key=lambda a: (not a.get('is_model_related', False), a['title']))

# Merge articles about same topic (套壳国产)
# Articles 4 and 14 from original are about the same event
merged_sources = {}
for art in classification['国际']:
    nt = normalize(art['title'])
    if '套壳' in nt:
        if 'rio' in nt.lower() or '黑马' in nt:
            merged_sources['rio'] = art
        elif 'SOTA' in nt:
            merged_sources['sota'] = art

if len(merged_sources) >= 2:
    a = merged_sources.get('rio', merged_sources.get('sota'))
    b = merged_sources.get('sota', merged_sources.get('rio'))
    # Create merged entry
    a['is_merged'] = True
    a['source_items'] = [{"name": a['source'], "source_file": a['source_file']}]
    if b and b != a:
        a['source_items'].append({"name": b['source'], "source_file": b['source_file']})
        a['digest'] = '巴西Rio-3.5-Open-397B模型全球走红后被指套壳阿里千问，开发者已下架模型并致歉，引发开源模型来源争议'
        # Remove the other entry
        classification['国际'] = [x for x in classification['国际'] if x != b]

stats = {cat: len(classification[cat]) for cat in classification}
stats['total'] = sum(stats.values())

result = {
    "date": "2026-06-15",
    "generated_at": datetime.now().isoformat(),
    "classification": classification,
    "stats": stats,
    "deleted": deleted
}

with open('daily/2026-06-15/classification.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"📊 分类结果: 国际{stats['国际']} 国内{stats['国内']} 同业{stats['同业']} 其他{stats['其他']} 总计{stats['total']}")
print(f"🗑️ 删除{len(deleted)}篇")
for d in deleted:
    print(f"   [{d['reason']}] {d['title'][:60]}")
for cat in classification:
    print(f"\n--- {cat} ---")
    for a in classification[cat]:
        m = '⭐' if a.get('is_model_related') else '  '
        mg = ' [合并]' if a.get('is_merged') else ''
        print(f"  {m} [{a['source']}] {a['title'][:60]}{mg}")
