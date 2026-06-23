#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成 classification.json
使用 filtered_articles.json 中的正确 source_file 路径
"""

import json
from datetime import datetime

# 读取 filtered_articles.json
with open('daily/2026-05-17/filtered_articles.json', 'r', encoding='utf-8') as f:
    filtered_data = json.load(f)

# 建立 aid 到完整文章数据的映射
articles_map = {}
for article in filtered_data['articles']:
    articles_map[article['aid']] = article

print(f"已加载 {len(articles_map)} 篇文章")

# 根据之前的分类逻辑重建 classification
classification = {
    "date": "2026-05-17",
    "generated_at": datetime.now().isoformat(),
    "classification": {
        "国际": [
            {
                "aid": "2651284462_1",
                "title": "Hermes团队改写预训练：算力成本降六成，DeepSeek之后提效新路径",
                "source": "InfoQ",
                "link": "https://mp.weixin.qq.com/s/g2fD_i3rMDdsMeySdl6Rhw",
                "digest": "模型能力还需往上走，但训练成本却不能再无止境堆砌了——这可能是当前 AI 行业最强烈的共识。",
                "source_file": articles_map.get("2651284462_1", {}).get("source_file", ""),
                "category_reason": "Hermes团队预训练技术优化研究，属于国际技术研究",
                "is_model_related": True
            },
            {
                "aid": "2651284462_4",
                "title": "谷歌 DORA 团队发布新报告：扎实的工程基础决定了 AI 投资回报",
                "source": "InfoQ",
                "link": "https://mp.weixin.qq.com/s/Bejnn2xvuJbn3wcYGziSNw",
                "digest": "谷歌云DORA团队发布报告，提出软件开发AI投资回报率评估框架，强调AI落地成效重在组织体系而非单纯工具，引入价值实现J曲线模型，并指出留存人才、重构流程是获取长期收益的关键。",
                "source_file": articles_map.get("2651284462_4", {}).get("source_file", ""),
                "category_reason": "Google DORA团队工程实践研究报告，属于国际工程方法论",
                "is_model_related": False
            }
        ],
        "国内": [
            {
                "aid": "2652701076_1",
                "title": "中国机器狗撕开英伟达垄断！70亿大模型跑通，成本仅1/10",
                "source": "新智元",
                "link": "https://mp.weixin.qq.com/s/YfZ-bvXAmMBO3LFQ6eUPKA",
                "digest": "",
                "source_file": articles_map.get("2652701076_1", {}).get("source_file", ""),
                "category_reason": "国内大模型训练优化技术突破",
                "is_model_related": True
            },
            {
                "aid": "2651033487_2",
                "title": "CVPR 2026 Oral | 清华+阿里发布ViT³：解锁「视觉TTT」新架构，突破Transformer复杂度瓶颈",
                "source": "机器之心",
                "link": "https://mp.weixin.qq.com/s/yJDuMj9gY6JLQtjng2p_FQ",
                "digest": "Vision Test-Time Training",
                "source_file": articles_map.get("2651033487_2", {}).get("source_file", ""),
                "category_reason": "清华+阿里CVPR学术研究，模型架构创新",
                "is_model_related": True
            }
        ],
        "同业": [],
        "其他": [
            {
                "aid": "merged_token_cost",
                "title": "龙虾之父月烧130万美元token账单：OpenAI全包复杂需求还得Claude",
                "source": "多源综合",
                "link": "https://mp.weixin.qq.com/s/mYnv6TEwGK4VsXurvH3URg",
                "digest": "整合两篇报道：龙虾之父自曝每月消耗130万美元token费用，由OpenAI全额承担；但复杂需求仍需Claude处理，显示不同模型的适用场景差异。",
                "source_file": "",
                "category_reason": "AI使用成本和体验报道，属于非技术内容",
                "is_model_related": False,
                "is_merged": True,
                "merged_articles": [
                    {
                        "aid": "2247891254_1",
                        "title": "龙虾之父月烧940万元的token！要不是入职OpenAI还真用不起",
                        "source": "量子位",
                        "link": "https://mp.weixin.qq.com/s/mYnv6TEwGK4VsXurvH3URg"
                    },
                    {
                        "aid": "2651033486_1",
                        "title": "一个月狂烧130万美元！龙虾之父自曝token账单，费用OpenAI全包",
                        "source": "机器之心",
                        "link": "https://mp.weixin.qq.com/s/2viAFaRVKPtNWjh6uhMEww"
                    }
                ]
            },
            {
                "aid": "2652701076_2",
                "title": "全球首个全民免费用ChatGPT Plus的国家，OpenAI官宣了",
                "source": "新智元",
                "link": "https://mp.weixin.qq.com/s/4CLplE8K_RWcbbs9FMfUaw",
                "digest": "一场大型社会实验。",
                "source_file": articles_map.get("2652701076_2", {}).get("source_file", ""),
                "category_reason": "OpenAI产品运营策略，属于非技术内容",
                "is_model_related": False
            },
            {
                "aid": "2652701014_1",
                "title": "3个人带100个AI程序员，一个月烧掉130万美元！OpenAI：钱我出",
                "source": "新智元",
                "link": "https://mp.weixin.qq.com/s/5O0b8Q0xTKU6_jHq93IUwA",
                "digest": "",
                "source_file": articles_map.get("2652701014_1", {}).get("source_file", ""),
                "category_reason": "OpenAI内部运营成本披露，属于公司动态",
                "is_model_related": False
            },
            {
                "aid": "2652701014_2",
                "title": "贝佐斯380亿物理AI黑马杀出！联手斯坦福科学家，不卷OpenAI",
                "source": "新智元",
                "link": "https://mp.weixin.qq.com/s/Ds07QVVYMwsTY7sUwY6Wjw",
                "digest": "",
                "source_file": articles_map.get("2652701014_2", {}).get("source_file", ""),
                "category_reason": "投资融资新闻，属于非技术内容",
                "is_model_related": False
            },
            {
                "aid": "2651284478_1",
                "title": "皮衣战神认证！黄仁勋胡同狂炫蜜雪冰城；关闭支付仍被扣款184万，支付宝回应；起步即独角兽！林俊旸AI Lab首轮估值136亿",
                "source": "InfoQ",
                "link": "https://mp.weixin.qq.com/s/6FmvsRX3gt4W0hWOL76nzA",
                "digest": "有瓜？！",
                "source_file": articles_map.get("2651284478_1", {}).get("source_file", ""),
                "category_reason": "多主题资讯汇总，包含多个不相关新闻",
                "is_model_related": False
            },
            {
                "aid": "2651284462_2",
                "title": "38万应用暴露、2000+应用泄密！AI编程把\"内网\"变公网",
                "source": "InfoQ",
                "link": "https://mp.weixin.qq.com/s/NXWpAWhtT73D7cY_fcC_yg",
                "digest": "整理 | 华卫\"vibe coding 工具正在泄露大量个人和企业数据。",
                "source_file": articles_map.get("2651284462_2", {}).get("source_file", ""),
                "category_reason": "安全事件报道，非技术研发",
                "is_model_related": False
            },
            {
                "aid": "2651284462_3",
                "title": "鼠标每动一下都在训练AI，Meta员工\"造反\"：不想在\"员工数据提取工厂\"工作",
                "source": "InfoQ",
                "link": "https://mp.weixin.qq.com/s/jZ2OqTyKcR-9u6h_zGZs7w",
                "digest": "传单上写道：\"不想在'员工数据提取工厂'工作吗？\"",
                "source_file": articles_map.get("2651284462_3", {}).get("source_file", ""),
                "category_reason": "Meta公司治理争议，员工抗议活动",
                "is_model_related": False
            },
            {
                "aid": "2651033486_3",
                "title": "花了1000倍的token，效果可能却没有更好：AI Agent的\"隐性账单\"长什么样",
                "source": "机器之心",
                "link": "https://mp.weixin.qq.com/s/ulZyoQZgxJfwGhqYwC9KKw",
                "digest": "分析了 8 个 frontier 模型在 swe-bench-verified 上的轨迹。",
                "source_file": articles_map.get("2651033486_3", {}).get("source_file", ""),
                "category_reason": "AI Agent应用层面性能分析，非模型本身技术研究",
                "is_model_related": False
            },
            {
                "aid": "2247891239_2",
                "title": "SFT别急着接RL！你的多模态大模型可能一直在\"带伤训练\"",
                "source": "量子位",
                "link": "https://mp.weixin.qq.com/s/2e-lyzzyn6IcfFH05Mm2AQ",
                "digest": "先把SFT挖的坑填了！",
                "source_file": articles_map.get("2247891239_2", {}).get("source_file", ""),
                "category_reason": "多模态大模型训练技术讨论，无明确主体归属",
                "is_model_related": True
            },
            {
                "aid": "2653106703_1",
                "title": "特斯拉解封17 份Robotaxi 碰撞报告；卢伟冰：部分国产旗舰手机售价或突破万元；警告：AI 可轻松从高分辨率自拍照中窃取指纹",
                "source": "极客公园",
                "link": "https://mp.weixin.qq.com/s/rbifu5ZEAfb9APRDo2k3Hw",
                "digest": "OpenAI 在美国遭集体诉讼；比尔 · 盖茨基金会出售最后持有的 770 万股微软股票；三星电子会长李在镕就公司「内部问题」公开道歉",
                "source_file": articles_map.get("2653106703_1", {}).get("source_file", ""),
                "category_reason": "多主题资讯汇总，包含多个不相关新闻",
                "is_model_related": False
            }
        ]
    },
    "stats": {
        "国际": 2,
        "国内": 2,
        "同业": 0,
        "其他": 11,
        "total": 15
    },
    "excluded": [
        {
            "aid": "2247891356_1",
            "title": "Agent、多模态、应用、算力一天看尽，峰会亮点在此｜5.20日，来现场一起AI",
            "reason": "活动宣传类内容（峰会预告）"
        },
        {
            "aid": "2247487739_1",
            "title": "阿里云 AI 创享日Qoder 专场·昆明站：AI Coding 的企业实践",
            "reason": "活动宣传类内容（专场活动）"
        }
    ]
}

# 写入文件
output_path = 'daily/2026-05-17/classification.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(classification, f, ensure_ascii=False, indent=2)

print(f"✅ classification.json 已重新生成: {output_path}")

# 验证文件
with open(output_path, 'r', encoding='utf-8') as f:
    verified = json.load(f)
    print(f"✅ 验证成功：共 {verified['stats']['total']} 篇文章")
    print(f"   国际: {verified['stats']['国际']}")
    print(f"   国内: {verified['stats']['国内']}")
    print(f"   同业: {verified['stats']['同业']}")
    print(f"   其他: {verified['stats']['其他']}")
    
    # 检查 source_file 字段
    total_with_source = 0
    for category in ['国际', '国内', '同业', '其他']:
        for article in verified['classification'][category]:
            if article.get('source_file'):
                total_with_source += 1
    
    print(f"✅ 有 source_file 的文章: {total_with_source}/{verified['stats']['total']}")
