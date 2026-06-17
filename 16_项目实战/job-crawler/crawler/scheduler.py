"""
爬虫调度器模块
管理爬虫的运行、分页、任务队列
"""
import time
from typing import List, Dict, Optional
from crawler.fetcher import Fetcher
from crawler.parser import Parser
from utils.logger import logger
from utils.config import TARGET_URL, CRAWLER_CONFIG


class Scheduler:
    """爬虫调度器"""
    
    def __init__(self, keyword: str = "Python", city: str = "北京", pages: int = 5):
        """
        初始化调度器
        
        Args:
            keyword: 搜索关键词
            city: 城市
            pages: 抓取页数
        """
        self.keyword = keyword
        self.city = city
        self.pages = pages
        self.fetcher = Fetcher()
        self.parser = Parser()
        self.all_jobs: List[Dict] = []
    
    def run(self) -> List[Dict]:
        """
        运行爬虫
        
        Returns:
            所有抓取的岗位列表
        """
        logger.info(f"开始抓取: 关键词={self.keyword}, 城市={self.city}, 页数={self.pages}")
        
        for page in range(1, self.pages + 1):
            logger.info(f"正在抓取第 {page}/{self.pages} 页...")
            
            # 构建 URL（不同网站需要不同处理）
            url = self._build_url(page)
            
            # 获取网页
            html = self.fetcher.fetch(url)
            if not html:
                logger.warning(f"第 {page} 页抓取失败，跳过")
                continue
            
            # 解析岗位
            jobs = self.parser.parse_job_list(html, source="lagou")
            
            if not jobs:
                logger.info(f"第 {page} 页无数据，可能已到最后一页")
                break
            
            # 添加到结果集
            self.all_jobs.extend(jobs)
            logger.success(f"第 {page} 页: 获取 {len(jobs)} 个岗位")
            
            # 请求间隔
            time.sleep(CRAWLER_CONFIG["delay"])
        
        logger.success(f"抓取完成，总计获取 {len(self.all_jobs)} 个岗位")
        return self.all_jobs
    
    def _build_url(self, page: int) -> str:
        """构建请求 URL"""
        # 拉勾网示例 URL 格式
        # 实际需要根据目标网站调整
        base = TARGET_URL["base"]
        keyword_encoded = self.keyword  # URL 编码
        return f"{base}{keyword_encoded}?px=new&city={self.city}&pn={page}"
    
    def close(self):
        """关闭资源"""
        self.fetcher.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def crawl_jobs(keyword: str = "Python", city: str = "北京", pages: int = 5) -> List[Dict]:
    """
    便捷函数：抓取岗位
    
    Args:
        keyword: 搜索关键词
        city: 城市
        pages: 抓取页数
        
    Returns:
        岗位列表
    """
    with Scheduler(keyword, city, pages) as scheduler:
        return scheduler.run()


if __name__ == "__main__":
    # 测试
    logger.info("测试 scheduler 模块")
    
    # 由于真实网站需要登录/反爬，这里只演示结构
    # 实际运行时请确保目标网站允许爬取
    logger.warning("注意: 实际使用请遵守网站 robots.txt 和使用条款")
