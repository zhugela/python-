"""
HTML 解析模块
从网页中提取岗位信息
"""
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from utils.logger import logger


class Parser:
    """HTML 解析器"""
    
    # 技能关键词（用于提取技术栈）
    SKILL_KEYWORDS = [
        "Python", "Java", "Go", "C++", "C#", "PHP", "Ruby", "Node.js", "JavaScript",
        "Spring", "Django", "Flask", "FastAPI", "Vue", "React", "Angular",
        "MySQL", "Redis", "MongoDB", "PostgreSQL", "Oracle", "SQLite",
        "Linux", "Docker", "Kubernetes", "K8S", "Jenkins", "Git", "GitLab",
        "AWS", "Azure", "GCP", "阿里云", "腾讯云",
        "Elasticsearch", "Kafka", "RabbitMQ", "Nginx", "Tomcat",
        "TCP", "HTTP", "REST", "API", "GraphQL", "RPC",
        "数据结构", "算法", "设计模式", "架构", "分布式", "微服务",
        "机器学习", "深度学习", "TensorFlow", "PyTorch", "NLP",
    ]
    
    def __init__(self):
        self.skill_keywords = [s.lower() for s in self.SKILL_KEYWORDS]
    
    def parse_job_list(self, html: str, source: str = "lagou") -> List[Dict]:
        """
        解析岗位列表页
        
        Args:
            html: 网页 HTML
            source: 来源网站
            
        Returns:
            岗位信息列表
        """
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        
        if source == "lagou":
            jobs = self._parse_lagou(soup)
        elif source == "boss":
            jobs = self._parse_boss(soup)
        elif source == "zhilian":
            jobs = self._parse_zhilian(soup)
        else:
            logger.warning(f"未知来源: {source}")
        
        logger.info(f"解析到 {len(jobs)} 个岗位")
        return jobs
    
    def _parse_lagou(self, soup: BeautifulSoup) -> List[Dict]:
        """解析拉勾网"""
        jobs = []
        
        # 拉勾网岗位列表的 CSS 选择器（需要根据实际页面调整）
        # 这里用通用的职位卡片选择器
        job_items = soup.select(".job-list .job-info") or soup.select(".position-list .position-list-item")
        
        for item in job_items:
            try:
                job = {
                    "title": self._extract_text(item, [".position-name", ".job-name", "h3"]),
                    "company": self._extract_text(item, [".company-name", ".company", ".name"]),
                    "city": self._extract_text(item, [".city", ".job-address"]),
                    "salary": self._extract_text(item, [".money", ".salary", ".job-salary"]),
                    "experience": self._extract_text(item, [".experience", ".job-exp"]),
                    "education": self._extract_text(item, [".education", ".job-degree"]),
                    "skills": self._extract_skills(item.get_text()),
                    "source": "lagou",
                }
                if job["title"]:
                    jobs.append(job)
            except Exception as e:
                logger.debug(f"解析岗位失败: {e}")
        
        return jobs
    
    def _parse_boss(self, soup: BeautifulSoup) -> List[Dict]:
        """解析BOSS直聘"""
        jobs = []
        job_items = soup.select(".job-list .job-card") or soup.select(".job-primary")
        
        for item in job_items:
            try:
                job = {
                    "title": self._extract_text(item, [".job-title", ".title"]),
                    "company": self._extract_text(item, [".company-name", ".company-text"]),
                    "city": self._extract_text(item, [".city", ".location-name"]),
                    "salary": self._extract_text(item, [".salary"]),
                    "experience": self._extract_text(item, [".experience"]),
                    "education": self._extract_text(item, [".edu"]),
                    "skills": self._extract_skills(item.get_text()),
                    "source": "boss",
                }
                if job["title"]:
                    jobs.append(job)
            except Exception as e:
                logger.debug(f"解析岗位失败: {e}")
        
        return jobs
    
    def _parse_zhilian(self, soup: BeautifulSoup) -> List[Dict]:
        """解析智联招聘"""
        jobs = []
        job_items = soup.select(".joblist-box .job-info")
        
        for item in job_items:
            try:
                job = {
                    "title": self._extract_text(item, [".job-name", ".title"]),
                    "company": self._extract_text(item, [".company-name", ".name"]),
                    "city": self._extract_text(item, [".city", ".address"]),
                    "salary": self._extract_text(item, [".salary"]),
                    "experience": self._extract_text(item, [".experience"]),
                    "education": self._extract_text(item, [".edu"]),
                    "skills": self._extract_skills(item.get_text()),
                    "source": "zhilian",
                }
                if job["title"]:
                    jobs.append(job)
            except Exception as e:
                logger.debug(f"解析岗位失败: {e}")
        
        return jobs
    
    def _extract_text(self, element, selectors: List[str]) -> str:
        """尝试多个选择器获取文本"""
        for selector in selectors:
            el = element.select_one(selector)
            if el:
                return el.get_text(strip=True)
        return ""
    
    def _extract_skills(self, text: str) -> str:
        """从文本中提取技术关键词"""
        text_lower = text.lower()
        found = []
        for skill in self.SKILL_KEYWORDS:
            if skill.lower() in text_lower:
                found.append(skill)
        return ",".join(found) if found else ""
    
    def parse_salary_range(self, salary_str: str) -> tuple:
        """
        解析薪资字符串，返回 (min, max) 千元/月
        
        例如: "15K-30K" -> (15, 30)
              "15-30K" -> (15, 30)
              "1.5万-3万" -> (15, 30)
        """
        import re
        
        if not salary_str:
            return (0, 0)
        
        # 统一转为小写处理
        salary_str = salary_str.lower()
        
        # 处理 "15k-30k" 或 "15k-30k" 格式
        match = re.search(r"(\d+)[kK]?-(\d+)[kK]?", salary_str)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        
        # 处理 "1.5万-3万" 格式
        match = re.search(r"([\d.]+)万?-([\d.]+)万?", salary_str)
        if match:
            return (float(match.group(1)) * 10, float(match.group(2)) * 10)
        
        # 处理 "面议" 等
        if "面议" in salary_str:
            return (0, 0)
        
        return (0, 0)


# 便捷函数
def parse_jobs(html: str, source: str = "lagou") -> List[Dict]:
    """解析岗位列表"""
    parser = Parser()
    return parser.parse_job_list(html, source)


if __name__ == "__main__":
    # 测试解析器
    logger.info("测试 parser 模块")
    
    # 模拟 HTML（实际使用时请替换为真实网页）
    test_html = """
    <div class="job-info">
        <h3 class="position-name">Python开发工程师</h3>
        <div class="company-name">字节跳动</div>
        <div class="city">北京</div>
        <div class="money">25K-50K</div>
        <div class="experience">3-5年</div>
        <div class="education">本科</div>
    </div>
    """
    
    jobs = parse_jobs(test_html, "lagou")
    logger.info(f"解析结果: {jobs}")
