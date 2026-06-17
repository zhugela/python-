"""
日志工具模块
使用 loguru，比 Python 内置 logging 更简单美观
"""
import sys
from loguru import logger

# 移除默认处理器
logger.remove()

# 添加控制台输出（带颜色）
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level="INFO"
)

# 添加文件输出
logger.add(
    "logs/crawler.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="DEBUG",
    rotation="10 MB",      # 单文件最大 10MB
    retention="7 days",    # 保留 7 天
    encoding="utf-8"
)

# 导出 logger 供其他模块使用
__all__ = ["logger"]
