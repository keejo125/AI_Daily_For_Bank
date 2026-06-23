#!/usr/bin/env python3
import json

with open('filtered_articles.json', 'r') as f:
    fa = json.load(f)
articles = fa['articles']

def build_entry(a, digest, category, reason, model=False):
    return {
        "aid": a.get('aid',''),
        "title": a['title'],
        "source": a.get('source',''),
        "link": a.get('link',''),
        "digest": digest,
        "source_file": a.get('source_file',''),
        "category": category,
        "category_reason": reason,
        "is_model_related": model
    }

cl = {
    "date": "2026-06-13",
    "article_date": "2026-06-12",
    "generated_at": "2026-06-13T10:00:00",
    "classification": {"国际": [], "国内": [], "同业": [], "其他": []},
    "excluded": [],
    "stats": {}
}

# Track which indices are handled
handled = set()

# === Exclude by index ===
exclude_indices = {
    9: '纯商业资讯（价格调整），非技术内容',   # 腾讯云降价
    16: '收购合并，非技术商业资讯',              # OpenAI收购Ona
    21: '人事八卦，非技术内容',                  # Anthropic老大八卦
    23: '收购合并，非技术商业资讯',              # OpenAI突然收购
    30: '商业资讯（价格策略），非技术内容',       # Token降价
}
# Duplicate LoongSuite - index 31 is the second one (0-indexed)
exclude_indices[31] = '重复文章，与第一篇同主题'

for idx, reason in exclude_indices.items():
    a = articles[idx]
    handled.add(idx)
    cl['excluded'].append({'aid': a['aid'], 'title': a['title'], 'reason': reason,
                           'source_file': a.get('source_file','')})

# === International ===
intl_indices = [
    (3, 'Claude Fable 5最难档零分！智能体的最后考试来了',
     'Anthropic发布Fable 5智能体基准测试，最难档所有模型均得零分，揭示当前Agent在复杂任务上的能力边界。',
     '国际AI公司Anthropic推出的智能体基准测试', False),
    (13, 'Claude Fable 5「发疯」！高数算网络攻击，问癌症直接封号？',
     'Fable 5安全机制引争议：高等数学被视为网络攻击、癌症被封号，AI安全过度管控引讨论。',
     '国际AI公司Anthropic的Claude Fable 5安全机制分析', False),
    (22, '微软 Foundry 新增生产级智能体运行时、工具链与管控能力',
     '微软Build 2026推出Foundry重大更新，补齐生产级智能体所需的全套能力：运行时、工具链与治理。',
     '国际AI平台（微软）产品技术更新，智能体基础设施', False),
    (25, '田渊栋创业公司首个成果：GPU内核优化，英伟达官方榜单SOTA',
     '田渊栋创业公司Recursive发布首个成果，AI驱动的GPU内核优化在英伟达官方榜单取得SOTA。',
     '国际AI创业公司（Recursive）GPU优化技术突破', False),
    (27, 'Anthropic警告的递归AI，田渊栋新公司刚刚走出了「第一步」',
     'Anthropic警示递归自我改进AI风险，同日Recursive发布首个能自主推进AI研究的闭环系统。',
     '国际AI研究（递归自我改进），Anthropic警示+Recursive实践', True),
    (26, '"智能体最后的考试"，Fable 5竟然不敌GPT 5.5',
     'Fable 5基准测试显示Claude及Anthropic自身Agent最高难度全部零分，GPT-5.5在部分场景表现更优。',
     '国际AI模型对比评测，Claude/GPT技术比较', True),
]

for idx, title, digest, reason, model in intl_indices:
    cl['classification']['国际'].append(build_entry(articles[idx], digest, '国际', reason, model))
    handled.add(idx)

# === Domestic ===
domestic_indices = [
    (0, '「AI春晚」又来了！智源研究院推出的世界模型，成今年最硬一盘菜',
     '智源大会发布世界模型等重磅成果，被称"AI春晚"级别的技术盛会。',
     '国内机构（智源研究院）发布世界模型', True),
    (1, '不改工作流，多智能体系统也能继续涨性能｜ICML 2026 Spotlight',
     'ICML 2026 Spotlight论文：无需修改工作流即可持续提升多智能体系统性能。',
     '国内团队的ICML 2026 Spotlight论文', False),
    (4, '刚刚，余承东发誓把盘古大模型做到世界第一',
     '华为余承东鸿蒙7发布会上宣布盘古大模型升级，立志打造世界第一。',
     '国内企业（华为）大模型规划发布', True),
    (5, '对话面壁CEO李大海：端侧AI模型赶上GPT-4，国产芯软件要补课',
     '面壁智能CEO谈端侧AI模型能力跨越、国产芯片适配与开源生态策略。',
     '国内AI公司CEO访谈，端侧模型/算力技术讨论', True),
    (7, '每周节省10小时，QoderWork，老师的AI教学搭档（内含福利）',
     'QoderWork作为AI桌面助手进入教师群体应用，每周可节省10小时工作时间。',
     '国内AI产品（Qoder/通义系）应用案例', False),
    (11, '微信测试团队斩获 CVPR 2026 NTIRE RAIM挑战赛冠军',
     '腾讯微信测试团队在CVPR 2026 NTIRE RAIM挑战赛夺冠，展示AI驱动测试Agent能力。',
     '国内企业（腾讯）技术团队国际赛事夺冠', False),
    (19, '智源连甩1个大脑3个大模型4个智能体，图灵奖得主：2050机器智能将主宰世界',
     '智源大会集中发布：1个通用大脑+3个大模型+4个智能体。',
     '国内机构（智源研究院）多项大模型及智能体发布', True),
    (8, '当 AI Coding Agent 成为基础设施：我们为什么要开源 LoongSuite Pilot',
     '阿里云开源LoongSuite Pilot，将AI Coding Agent作为基础设施向开发者开放。',
     '国内企业（阿里云）开源AI编程工具', False),
    (28, '数字员工的第 1 天和第 30 天：QoderWake 自进化能力升级',
     'QoderWake升级自进化能力，数字员工将从对话沉淀经验为Skills，越用越聪明。',
     '国内AI产品（Qoder/通义系）功能更新', False),
    (29, '北大联手让AI跨界「造物」，业界最强复合纤维诞生！',
     '北京大学利用AI技术跨界材料科学，研发出业界最强复合纤维。',
     '国内高校（北大）AI+材料科学研究', False),
]

for idx, title, digest, reason, model in domestic_indices:
    cl['classification']['国内'].append(build_entry(articles[idx], digest, '国内', reason, model))
    handled.add(idx)

# === Peer (Banking) ===
peer_idx = 15  # Kimi与国有银行发行AI原生信用卡
cl['classification']['同业'].append(build_entry(
    articles[peer_idx],
    '月之暗面Kimi正与大型国有银行及国际卡组织联合推出AI原生信用卡产品。',
    '同业', '银行业务创新（AI+信用卡），同业优先', False
))
handled.add(peer_idx)

# === Other ===
other_indices = [
    (2, '2026智源大会记述：从世界模型到具身智能，AI正叩响触达实体世界的大门。',
     '会议活动综述，属活动报道类'),
    (6, '折叠屏手机下半场从硬件屏幕转向AI任务驱动，交互范式变革。',
     '消费电子+AI概念，非纯技术'),
    (10, 'OpenAI CEO萨姆·奥尔特曼原定访韩计划推迟。',
     '公司人事动态'),
    (12, '反思AI时代的人类认知危机：当平庸分析触手可及，人类思考的底线何在？',
     'AI社会影响/哲学思考'),
    (14, '探讨AI服务订阅制模式的弊端与替代方案。',
     '商业模式分析'),
    (17, '王坚深度访谈：AI时代中国机遇、中美差距与坚定乐观主义。',
     '行业领袖观点分享'),
    (18, '小米罗福莉等AI大牛讨论Fable 5评测结果与AI发展方向。',
     '行业讨论/观点交锋'),
    (20, 'AI领域Token价格战分析，中国企业转向性价比更高的国产模型。',
     '市场分析'),
    (24, '中国车企将AI与物理机器人结合，从屏幕交互走向具身智能。',
     'AI应用案例/行业报道'),
    (32, '腾讯AI资讯速览：混元AI Infra开源、HPC-Ops升级、AI监管政策等。',
     '综合资讯速递'),
]

for idx, digest, reason in other_indices:
    cl['classification']['其他'].append(build_entry(articles[idx], digest, '其他', reason, False))
    handled.add(idx)

# Verify coverage
unhandled = set(range(len(articles))) - handled
if unhandled:
    print(f"⚠️ 未处理的文章索引: {unhandled}")
    for i in sorted(unhandled):
        print(f"  [{i}] {articles[i]['title'][:50]}")
else:
    print("✅ 全部33篇文章已处理完毕")

# Stats
cl['stats'] = {
    '国际': len(cl['classification']['国际']),
    '国内': len(cl['classification']['国内']),
    '同业': len(cl['classification']['同业']),
    '其他': len(cl['classification']['其他']),
    'total': len(cl['classification']['国际']) + len(cl['classification']['国内']) + len(cl['classification']['同业']) + len(cl['classification']['其他'])
}

with open('classification.json', 'w') as f:
    json.dump(cl, f, ensure_ascii=False, indent=2)

print(f"📊 统计:")
print(f"   国际: {cl['stats']['国际']} | 国内: {cl['stats']['国内']} | 同业: {cl['stats']['同业']} | 其他: {cl['stats']['其他']}")
print(f"   合计: {cl['stats']['total']} 篇")
print(f"   删除: {len(cl['excluded'])} 篇")
