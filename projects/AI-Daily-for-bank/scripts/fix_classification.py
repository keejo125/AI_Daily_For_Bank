#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 classification.json 格式
从 filtered_articles.json 读取数据，重新生成正确格式的 classification.json
"""

import json
import os
import sys
from datetime import datetime


def main():
    if len(sys.argv) < 2:
        print("用法: python3 fix_classification.py YYYY-MM-DD")
        sys.exit(1)
    
    date_str = sys.argv[1]
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 读取 filtered_articles.json
    filtered_path = os.path.join(project_dir, 'daily', date_str, 'filtered_articles.json')
    with open(filtered_path, 'r', encoding='utf-8') as f:
        filtered_data = json.load(f)
    
    articles = filtered_data.get('articles', [])
    
    # 分类规则（简化版，基于标题和来源关键词）
    def classify_article(article):
        title = article.get('title', '')
        source = article.get('source', '')
        digest = article.get('digest', '')
        
        # 同业类优先判断
        peer_keywords = ['银行', '金融', '信贷', '风控', '保险', '证券', '基金', '理财', 'ESG']
        if any(kw in title or kw in digest for kw in peer_keywords):
            return '同业'
        
        # 国际类
        intl_keywords = ['OpenAI', 'Anthropic', 'Claude', 'Google', 'Meta', 'Apple', '苹果', 
                        'Microsoft', '微软', 'Amazon', '亚马逊', 'Nvidia', '英伟达', 
                        'SpaceX', '马斯克', 'Musk', 'Sam Altman', 'Altman']
        if any(kw in title or kw in source for kw in intl_keywords):
            return '国际'
        
        # 国内类
        domestic_keywords = ['阿里', '腾讯', '百度', '字节', '华为', '智谱', '商汤', 
                           'DeepSeek', 'Qwen', '通义', '月之暗面', 'MiniMax', 
                           '阶跃星辰', '零一万物', '面壁', '360', '宇视']
        if any(kw in title or kw in source for kw in domestic_keywords):
            return '国内'
        
        # 默认为其他
        return '其他'
    
    # 分类文章
    classification = {
        '国际': [],
        '国内': [],
        '同业': [],
        '其他': []
    }
    
    for article in articles:
        category = classify_article(article)
        
        # 处理 digest：如果为空或过长，进行优化
        digest = article.get('digest', '').strip()
        title = article.get('title', '')
        
        if not digest:
            # digest为空，使用标题
            digest = title
        elif len(digest) > 200:
            # digest过长，截取前200字符并添加省略号
            digest = digest[:200].rstrip() + '...'
        
        # 清理digest中的多余空格和换行
        digest = ' '.join(digest.split())
        
        item = {
            'title': title,
            'source': article.get('source', ''),
            'link': article.get('link', ''),
            'digest': digest,
            'source_file': article.get('source_file', '')
        }
        
        classification[category].append(item)
    
    # 构建输出
    output = {
        'date': date_str,
        'generated_at': datetime.now().isoformat(),
        'classification': classification,
        'stats': {
            '国际': len(classification['国际']),
            '国内': len(classification['国内']),
            '同业': len(classification['同业']),
            '其他': len(classification['其他']),
            'total': len(articles)
        }
    }
    
    # 写入文件
    output_path = os.path.join(project_dir, 'daily', date_str, 'classification.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ classification.json 已修复")
    print(f"   国际: {output['stats']['国际']} 篇")
    print(f"   国内: {output['stats']['国内']} 篇")
    print(f"   同业: {output['stats']['同业']} 篇")
    print(f"   其他: {output['stats']['其他']} 篇")
    print(f"   总计: {output['stats']['total']} 篇")


if __name__ == '__main__':
    main()
