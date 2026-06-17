#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
招聘信息采集与岗位分析系统
主入口文件

功能：
1. 抓取招聘网站岗位信息
2. 数据清洗与去重
3. 统计分析（城市分布、技能热度、薪资水平）
4. 导出 CSV/Excel 报表

使用方法：
    python main.py                    # 默认配置抓取
    python main.py -k Python -c 北京   # 指定关键词和城市
    python main.py --pages 10         # 指定抓取页数
    python main.py --demo            # 使用演示数据测试

作者：亮哥（Java转Python学习者）
日期：2026-03-22
"""

import argparse
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import logger
from crawler.scheduler import Scheduler
from analyzer.cleaner import Cleaner
from analyzer.stats import StatsAnalyzer
from analyzer.exporter import Exporter


def run_crawler(keyword: str, city: str, pages: int, use_demo: bool = False):
    """
    运行爬虫
    
    Args:
        keyword: 搜索关键词
        city: 城市
        pages: 抓取页数
        use_demo: 是否使用演示数据
    """
    logger.info("=" * 50)
    logger.info("招聘信息采集与岗位分析系统")
    logger.info("=" * 50)
    
    # 步骤1: 抓取数据
    logger.info("\n【步骤1】抓取岗位数据...")
    
    if use_demo:
        # 演示数据（用于测试）
        logger.info("使用演示数据测试...")
        jobs = get_demo_data()
    else:
        # 实际抓取
        logger.info(f"关键词: {keyword}, 城市: {city}, 页数: {pages}")
        try:
            with Scheduler(keyword, city, pages) as scheduler:
                jobs = scheduler.run()
        except Exception as e:
            logger.error(f"抓取失败: {e}")
            logger.info("自动切换到演示数据模式...")
            jobs = get_demo_data()
    
    if not jobs:
        logger.warning("没有抓取到数据，切换到演示数据模式...")
        jobs = get_demo_data()
    
    # 步骤2: 数据清洗
    logger.info("\n【步骤2】清洗数据...")
    cleaner = Cleaner()
    df = cleaner.clean_jobs(jobs)
    
    if df.empty:
        logger.error("清洗后没有有效数据")
        return
    
    # 步骤3: 统计分析
    logger.info("\n【步骤3】统计分析...")
    analyzer = StatsAnalyzer(df)
    stats = analyzer.get_all_stats()
    
    # 打印概览
    overview = stats["overview"]
    logger.info(f"  总岗位数: {overview['total']}")
    logger.info(f"  公司数量: {overview['companies']}")
    logger.info(f"  城市数量: {overview['cities']}")
    if "salary" in overview:
        logger.info(f"  平均薪资: {overview['salary']['avg_mid']}K/月")
    
    # 步骤4: 导出数据
    logger.info("\n【步骤4】导出数据...")
    exporter = Exporter()
    
    # 导出 CSV
    csv_path = exporter.export_csv(df)
    
    # 导出 Excel（带分析）
    excel_path = exporter.export_excel(df, stats=stats)
    
    # 打印统计结果
    print_statistics(stats)
    
    logger.success("\n" + "=" * 50)
    logger.success("处理完成！")
    logger.success(f"CSV: {csv_path}")
    logger.success(f"Excel: {excel_path}")
    logger.success("=" * 50)


def print_statistics(stats: dict):
    """打印统计结果到控制台"""
    print("\n" + "=" * 50)
    print("📊 统计分析结果")
    print("=" * 50)
    
    # Top 城市
    print("\n🏙️  Top 城市:")
    for i, city in enumerate(stats.get("top_cities", [])[:5], 1):
        print(f"  {i}. {city['city']}: {city['count']}个 ({city['percentage']}%)")
    
    # Top 技能
    print("\n💻 Top 技能:")
    for i, skill in enumerate(stats.get("top_skills", [])[:8], 1):
        print(f"  {i}. {skill['skill']}: {skill['count']}次")
    
    # 薪资统计
    print("\n💰 薪资统计 (K/月):")
    salary_by_exp = stats.get("salary_by_exp", [])
    for exp_salary in salary_by_exp:
        if exp_salary.get("avg_mid", 0) > 0:
            print(f"  {exp_salary['experience']}: {exp_salary['avg_mid']}K (平均)")
    
    print("=" * 50)


def get_demo_data():
    """
    获取演示数据
    用于没有网络或目标网站无法访问时测试
    """
    return [
        # Python 岗位
        {"title": "Python开发工程师", "company": "字节跳动", "city": "北京", "salary": "25K-50K", "experience": "3-5年", "education": "本科", "skills": "Python,Django,Flask,MySQL,Redis"},
        {"title": "Python后端开发", "company": "快手", "city": "北京", "salary": "30K-60K", "experience": "5-10年", "education": "本科", "skills": "Python,Go,Docker,Kafka"},
        {"title": "Python爬虫工程师", "company": "百度", "city": "北京", "salary": "15K-30K", "experience": "1-3年", "education": "本科", "skills": "Python,Scrapy,Redis,MongoDB"},
        {"title": "Python数据分析师", "company": "美团", "city": "北京", "salary": "20K-40K", "experience": "3-5年", "education": "本科", "skills": "Python,Pandas,SQL,Excel"},
        {"title": "Python开发工程师", "company": "阿里云", "city": "杭州", "salary": "25K-45K", "experience": "3-5年", "education": "本科", "skills": "Python,Spring,Docker,K8s"},
        {"title": "Python算法工程师", "company": "阿里", "city": "杭州", "salary": "35K-70K", "experience": "5-10年", "education": "硕士", "skills": "Python,TensorFlow,深度学习,NLP"},
        {"title": "Python全栈工程师", "company": "腾讯", "city": "深圳", "salary": "28K-55K", "experience": "3-5年", "education": "本科", "skills": "Python,Vue,React,MySQL"},
        {"title": "Python开发", "company": "滴滴", "city": "北京", "salary": "22K-40K", "experience": "1-3年", "education": "本科", "skills": "Python,Flask,MySQL,Docker"},
        
        # Java 岗位（对比）
        {"title": "Java开发工程师", "company": "字节跳动", "city": "北京", "salary": "25K-50K", "experience": "3-5年", "education": "本科", "skills": "Java,Spring Boot,MySQL,Redis"},
        {"title": "Java后端开发", "company": "阿里", "city": "杭州", "salary": "28K-55K", "experience": "5-10年", "education": "本科", "skills": "Java,Spring,Dubbo,Kafka"},
        {"title": "Java工程师", "company": "腾讯", "city": "深圳", "salary": "25K-45K", "experience": "3-5年", "education": "本科", "skills": "Java,MySQL,Redis,Docker"},
        
        # Go 岗位
        {"title": "Go开发工程师", "company": "字节跳动", "city": "北京", "salary": "30K-60K", "experience": "3-5年", "education": "本科", "skills": "Go,Python,Docker,K8s"},
        {"title": "Golang后端", "company": "快手", "city": "北京", "salary": "28K-55K", "experience": "3-5年", "education": "本科", "skills": "Go,Redis,Kafka,MongoDB"},
        
        # 前端
        {"title": "前端开发工程师", "company": "阿里", "city": "杭州", "salary": "20K-40K", "experience": "1-3年", "education": "本科", "skills": "JavaScript,Vue,React,Node.js"},
        
        # 其他城市
        {"title": "Python开发工程师", "company": "网易", "city": "广州", "salary": "18K-35K", "experience": "1-3年", "education": "本科", "skills": "Python,Flask,Django"},
        {"title": "Python后端", "company": "京东", "city": "北京", "salary": "22K-42K", "experience": "3-5年", "education": "本科", "skills": "Python,Java,Spring"},
        {"title": "Python开发", "company": "拼多多", "city": "上海", "salary": "25K-50K", "experience": "3-5年", "education": "本科", "skills": "Python,Go,MySQL"},
        {"title": "数据工程师", "company": "字节", "city": "北京", "salary": "28K-55K", "experience": "3-5年", "education": "本科", "skills": "Python,Spark,Hive,SQL"},
    ]


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="招聘信息采集与岗位分析系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py                           # 默认抓取 Python 北京 5页
  python main.py -k Java -c 上海 -p 10     # 抓取 Java 上海 10页
  python main.py --demo                   # 使用演示数据测试
        """
    )
    
    parser.add_argument("-k", "--keyword", default="Python", help="搜索关键词 (默认: Python)")
    parser.add_argument("-c", "--city", default="北京", help="城市 (默认: 北京)")
    parser.add_argument("-p", "--pages", type=int, default=5, help="抓取页数 (默认: 5)")
    parser.add_argument("--demo", action="store_true", default=True, help="使用演示数据测试 (默认开启)")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细日志")
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        import logging
        logger.remove()
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
            level="DEBUG"
        )
    
    # 运行
    run_crawler(
        keyword=args.keyword,
        city=args.city,
        pages=args.pages,
        use_demo=args.demo
    )


if __name__ == "__main__":
    main()
