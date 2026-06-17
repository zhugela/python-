"""
HTTP 请求模块
负责发送请求、获取网页内容
"""
import time
import requests
from typing import Optional
from utils.logger import logger
from utils.config import CRAWLER_CONFIG


class Fetcher:
    """网页请求器"""
    
    def __init__(self):
        self.timeout = CRAWLER_CONFIG["timeout"]
        self.retry_times = CRAWLER_CONFIG["retry_times"]
        self.delay = CRAWLER_CONFIG["delay"]
        self.headers = {
            "User-Agent": CRAWLER_CONFIG["user_agent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        # 创建 session 保持连接
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch(self, url: str, encoding: str = "utf-8") -> Optional[str]:
        """
        获取网页内容
        
        Args:
            url: 目标 URL
            encoding: 响应编码
            
        Returns:
            网页内容（str）或 None
        """
        for attempt in range(self.retry_times):
            try:
                # 请求间隔，防止被封
                if attempt > 0:
                    time.sleep(self.delay * 2)
                
                logger.info(f"请求: {url} (尝试 {attempt + 1}/{self.retry_times})")
                
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # 自动检测编码
                if encoding == "auto":
                    response.encoding = response.apparent_encoding
                else:
                    response.encoding = encoding
                
                logger.debug(f"响应状态: {response.status_code}, 长度: {len(response.text)}")
                return response.text
                
            except requests.RequestException as e:
                logger.warning(f"请求失败: {e}")
                if attempt == self.retry_times - 1:
                    logger.error(f"最终放弃: {url}")
                    return None
        
        return None
    
    def close(self):
        """关闭 session"""
        self.session.close()


# 方便直接调用
_default_fetcher = None

def get_html(url: str, encoding: str = "utf-8") -> Optional[str]:
    """便捷函数：获取网页"""
    global _default_fetcher
    if _default_fetcher is None:
        _default_fetcher = Fetcher()
    return _default_fetcher.fetch(url, encoding)


if __name__ == "__main__":
    # 测试
    logger.info("测试 fetcher 模块")
    html = get_html("https://httpbin.org/html")
    if html:
        logger.success(f"获取成功，内容长度: {len(html)}")
    else:
        logger.error("获取失败")
