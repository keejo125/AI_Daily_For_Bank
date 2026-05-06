#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 classification.json 模板
用法: python3 create_classification.py YYYY-MM-DD

功能：
- 基于 filtered_articles.json 生成 classification.json 模板
- 自动填充 aid, title, source, link, source_file
- 保留空的 category 和 digest 字段供 AI Agent 填写
- 自动处理中文引号

注意：此脚本只生成模板，真正的分类和摘要由 AI Agent 根据 SKILL.md 中的规则完成
"""

import json
import os
import sys
from datetime import datetime, timedelta


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
    
    # 计算早报日期 = 文章日期 + 1天
    article_date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    report_date = article_date_obj + timedelta(days=1)
    
    # 初始化分类结构（所有文章先放入 "待分类"）
    classification = {
        "date": report_date.strftime('%Y-%m-%d'),
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
            "total": len(articles)
        },
        "excluded": []
    }
    
    # 遍历文章，生成待分类模板
    for art in articles:
        title = art.get('title', '')
        source = art.get('source', '')
        aid = art.get('aid', '')
        link = art.get('link', '')
        source_file = art.get('source_file', '')
        digest = art.get('digest', '')  # 保留原始摘要
        
        # 标准化中文字符
        title_normalized = normalize_chinese_quotes(title)
        source_file_normalized = normalize_chinese_quotes(source_file)
        
        # 构建文章条目（category 和 digest 留空，供 AI Agent 填写）
        article_entry = {
            "aid": aid,
            "title": title_normalized,
            "source": source,
            "link": link,
            "digest": "",  # 留空，需要 AI Agent 生成摘要
            "source_file": source_file_normalized,
            "category": "",  # 留空，需要 AI Agent 分类
            "category_reason": ""  # 留空，需要 AI Agent 说明分类理由
        }
        
        # 暂时放入 "其他" 分类，AI Agent 会重新分配
        classification['classification']['其他'].append(article_entry)
        
        print_progress(f"  [待分类] {title[:50]}...")
    
    # 输出文件路径
    output_path = os.path.join(daily_dir, 'classification.json')
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(classification, f, ensure_ascii=False, indent=2)
    
    print_progress(f"\n✅ 分类模板已生成: {output_path}")
    print_progress(f"📊 待处理文章数: {len(articles)} 篇")
    print_progress(f"\n⚠️  下一步:")
    print_progress(f"   1. AI Agent 读取 {output_path}")
    print_progress(f"   2. 根据 SKILL.md 中的规则对每篇文章进行分类（国际/国内/同业/其他）")
    print_progress(f"   3. 为每篇文章填写 digest 字段（100-200字摘要）")
    print_progress(f"   4. 填写 category_reason 字段（说明分类理由）")
    print_progress(f"   5. 运行: python3 generate_html.py {date_str}")


if __name__ == '__main__':
    main()
