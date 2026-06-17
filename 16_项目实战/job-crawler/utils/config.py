# 项目配置文件
# =============

# 爬虫配置
CRAWLER_CONFIG = {
    "timeout": 30,           # 请求超时时间（秒）
    "retry_times": 3,        # 重试次数
    "delay": 1,              # 请求间隔（秒），避免被封
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 数据保存路径
DATA_PATH = {
    "raw": "data/raw/",      # 原始数据
    "clean": "data/clean/"   # 清洗后数据
}

# 分析配置
ANALYSIS_CONFIG = {
    "top_skills": 20,        # 显示Top N 技能
    "top_cities": 10,        # 显示Top N 城市
}

# 目标网站（可替换为你想爬的招聘网站）
# 这里以拉勾网为例（需要登录可换其他公开站点）
TARGET_URL = {
    "base": "https://www.lagou.com/jobs/list_",
    "page_param": "p",
}
