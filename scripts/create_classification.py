#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 classification.json 模板
用法: python3 create_classification.py YYYY-MM-DD

功能：
- 基于 filtered_articles.json 自动生成 classification.json 模板
- 自动填充 aid, title, source, link, source_file
- 预分类（根据关键词自动判断国际/国内/同业/其他）
- 保留空的 digest 字段供智能体填写摘要
- 自动处理中文引号
"""

import json
import os
import sys
from datetime import datetime


def print_progress(msg):
    """打印进度信息"""
    print(f"[create_classification] {msg}")


def normalize_chinese_quotes(text):
    """标准化中文引号为方括号，避免 JSON 解析错误"""
    if not text:
        return text
    text = text.replace('\u201c', '【').replace('\u201d', '】')
    text = text.replace('\u2018', '「').replace('\u2019', '」')
    return text


def auto_classify(title, source):
    """
    根据标题和来源自动预分类
    
    返回: '国际', '国内', '同业', 或 '其他'
    """
    text = f"{title} {source}".lower()
    
    # 同业优先：银行、金融机构
    banking_keywords = ['银行', '农商', '金融', '保险', '证券', '信贷', '风控']
    if any(kw in text for kw in banking_keywords):
        return '同业'
    
    # 国际：海外公司
    international_keywords = [
        'openai', 'anthropic', 'google', 'meta', 'apple', 'nvidia', 
        'microsoft', 'xai', 'stability ai', '马斯克', '黄仁勋',
        '硅谷', '美国', '欧洲', '日本'
    ]
    if any(kw in text for kw in international_keywords):
        return '国际'
    
    # 国内：中国公司
    domestic_keywords = [
        '阿里', '腾讯', '百度', '字节', '华为', '智谱', '商汤',
        '深度求索', '月之暗面', 'minimax', '阶跃星辰', '零一万物',
        '面壁智能', 'deepseek', 'kimi', '通义', '文心',
        '中国', '国内', '国产'
    ]
    if any(kw in text for kw in domestic_keywords):
        return '国内'
    
    # 默认为其他
    return '其他'


def main():
    if len(sys.argv) < 2:
        print("用法: python3 create_classification.py YYYY-MM-DD")
        print("示例: python3 create_classification.py 2026-04-25")
        sys.exit(1)
    
    date_str = sys.argv[1]
    
    # 项目根目录
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    daily_dir = os.path.join(project_dir, 'daily', date_str)
    
    # 检查目录是否存在
    if not os.path.exists(daily_dir):
        print_progress(f"错误: 目录不存在 - {daily_dir}")
        sys.exit(1)
    
    # 读取 filtered_articles.json
    filtered_path = os.path.join(daily_dir, 'filtered_articles.json')
    if not os.path.exists(filtered_path):
        print_progress(f"错误: 文件不存在 - {filtered_path}")
        print_progress("请先运行 filter_articles.py")
        sys.exit(1)
    
    with open(filtered_path, 'r', encoding='utf-8') as f:
        filtered_data = json.load(f)
    
    articles = filtered_data.get('articles', [])
    print_progress(f"读取到 {len(articles)} 篇过滤后的文章")
    
    # 初始化分类结构
    classification = {
        "date": (datetime.strptime(date_str, '%Y-%m-%d').replace(day=datetime.strptime(date_str, '%Y-%m-%d').day + 1)).strftime('%Y-%m-%d'),
        "article_date": date_str,
        "generated_at": datetime.now().isoformat(),
        "classification": {
            "国际": [],
            "国内": [],
            "同业": [],
            "其他": []
        },
        "stats": {
            "国际": 0,
            "国内": 0,
            "同业": 0,
            "其他": 0,
            "total": 0
        },
        "excluded": []
    }
    
    # 修正日期逻辑：早报日期 = 文章内容日期 + 1天
    from datetime import timedelta
    article_date = datetime.strptime(date_str, '%Y-%m-%d')
    report_date = article_date + timedelta(days=1)
    classification['date'] = report_date.strftime('%Y-%m-%d')
    
    # 遍历文章，自动分类
    for art in articles:
        title = art.get('title', '')
        source = art.get('source', '')
        aid = art.get('aid', '')
        link = art.get('link', '')
        source_file = art.get('source_file', '')
        
        # 自动分类
        category = auto_classify(title, source)
        
        # 标准化中文字符
        title_normalized = normalize_chinese_quotes(title)
        source_file_normalized = normalize_chinese_quotes(source_file)
        
        # 构建文章条目（digest 留空，供智能体填写）
        article_entry = {
            "aid": aid,
            "title": title_normalized,
            "source": source,
            "link": link,
            "digest": "",  # 留空，需要智能体生成摘要
            "source_file": source_file_normalized
        }
        
        classification['classification'][category].append(article_entry)
        classification['stats'][category] += 1
        classification['stats']['total'] += 1
        
        print_progress(f"  [{category}] {title[:40]}...")
    
    # 输出文件路径
    output_path = os.path.join(daily_dir, 'classification.json')
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(classification, f, ensure_ascii=False, indent=2)
    
    print_progress(f"\n✅ 分类模板已生成: {output_path}")
    print_progress(f"📊 统计: {classification['stats']}")
    print_progress(f"\n⚠️  下一步:")
    print_progress(f"   1. 编辑 {output_path}")
    print_progress(f"   2. 为每篇文章填写 digest 字段（100-200字摘要）")
    print_progress(f"   3. 调整分类（如需要）")
    print_progress(f"   4. 运行: python3 generate_html.py {date_str}")


if __name__ == '__main__':
    main()
