"""
数据导出模块
将数据导出为 CSV、Excel 等格式
"""
import os
from datetime import datetime
from typing import Dict, List
import pandas as pd
from utils.logger import logger
from utils.config import DATA_PATH


class Exporter:
    """数据导出器"""
    
    def __init__(self, data_path: str = None):
        """
        初始化导出器
        
        Args:
            data_path: 数据保存根目录
        """
        self.data_path = data_path or DATA_PATH
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        os.makedirs(self.data_path["raw"], exist_ok=True)
        os.makedirs(self.data_path["clean"], exist_ok=True)
    
    def export_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        导出为 CSV
        
        Args:
            df: DataFrame
            filename: 文件名（不含路径）
            
        Returns:
            保存的文件路径
        """
        if filename is None:
            filename = f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # 保存到 clean 目录
        filepath = os.path.join(self.data_path["clean"], filename)
        
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
        logger.success(f"CSV 已导出: {filepath}")
        
        return filepath
    
    def export_excel(self, df: pd.DataFrame, filename: str = None, include_analysis: bool = True, stats: Dict = None) -> str:
        """
        导出为 Excel（支持多 sheet）
        
        Args:
            df: 岗位数据 DataFrame
            filename: 文件名
            include_analysis: 是否包含分析 sheet
            stats: 统计分析结果
            
        Returns:
            保存的文件路径
        """
        if filename is None:
            filename = f"jobs_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        filepath = os.path.join(self.data_path["clean"], filename)
        
        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            # 岗位详情 sheet
            df.to_excel(writer, sheet_name="岗位详情", index=False)
            
            # 统计分析 sheet
            if include_analysis and stats:
                # 数据概览
                overview = pd.DataFrame([stats.get("overview", {})])
                overview.to_excel(writer, sheet_name="数据概览", index=False)
                
                # Top 城市
                if "top_cities" in stats and stats["top_cities"]:
                    pd.DataFrame(stats["top_cities"]).to_excel(writer, sheet_name="Top城市", index=False)
                
                # Top 公司
                if "top_companies" in stats and stats["top_companies"]:
                    pd.DataFrame(stats["top_companies"]).to_excel(writer, sheet_name="Top公司", index=False)
                
                # Top 技能
                if "top_skills" in stats and stats["top_skills"]:
                    pd.DataFrame(stats["top_skills"]).to_excel(writer, sheet_name="Top技能", index=False)
                
                # 城市薪资
                if "salary_by_city" in stats and stats["salary_by_city"]:
                    pd.DataFrame(stats["salary_by_city"]).to_excel(writer, sheet_name="城市薪资", index=False)
                
                # 经验薪资
                if "salary_by_exp" in stats and stats["salary_by_exp"]:
                    pd.DataFrame(stats["salary_by_exp"]).to_excel(writer, sheet_name="经验薪资", index=False)
                
                # 学历薪资
                if "salary_by_edu" in stats and stats["salary_by_edu"]:
                    pd.DataFrame(stats["salary_by_edu"]).to_excel(writer, sheet_name="学历薪资", index=False)
        
        logger.success(f"Excel 已导出: {filepath}")
        return filepath
    
    def export_json(self, data: any, filename: str = None) -> str:
        """
        导出为 JSON
        
        Args:
            data: 要导出的数据（dict 或 DataFrame）
            filename: 文件名
            
        Returns:
            保存的文件路径
        """
        if filename is None:
            filename = f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.data_path["clean"], filename)
        
        if isinstance(data, pd.DataFrame):
            data = data.to_dict("records")
        
        import json
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.success(f"JSON 已导出: {filepath}")
        return filepath
    
    def save_raw_html(self, html: str, keyword: str) -> str:
        """
        保存原始 HTML（用于调试）
        
        Args:
            html: HTML 内容
            keyword: 搜索关键词
            
        Returns:
            保存的文件路径
        """
        filename = f"raw_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(self.data_path["raw"], filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        logger.debug(f"原始 HTML 已保存: {filepath}")
        return filepath
    
    def load_csv(self, filename: str = None) -> pd.DataFrame:
        """
        读取 CSV 文件
        
        Args:
            filename: 文件名（不含路径），None 则读取最新
            
        Returns:
            DataFrame
        """
        if filename is None:
            # 读取最新的 CSV
            files = [f for f in os.listdir(self.data_path["clean"]) if f.endswith(".csv")]
            if not files:
                logger.warning("没有找到 CSV 文件")
                return pd.DataFrame()
            filename = max(files)
        
        filepath = os.path.join(self.data_path["clean"], filename)
        df = pd.read_csv(filepath, encoding="utf-8-sig")
        logger.info(f"已加载: {filepath} ({len(df)} 条)")
        return df


def export_jobs(df: pd.DataFrame, stats: Dict = None) -> str:
    """便捷函数：导出岗位数据和分析结果"""
    exporter = Exporter()
    
    # 先导出 CSV
    csv_path = exporter.export_csv(df)
    
    # 再导出带分析的 Excel
    excel_path = exporter.export_excel(df, stats=stats)
    
    return excel_path


if __name__ == "__main__":
    # 测试
    from analyzer.cleaner import clean_jobs
    
    logger.info("测试 exporter 模块")
    
    test_data = [
        {"title": "Python开发", "company": "字节", "city": "北京", "salary": "20K-40K", "experience": "3-5年", "education": "本科", "skills": "Python,Django,MySQL"},
        {"title": "Java开发", "company": "阿里", "city": "杭州", "salary": "15K-30K", "experience": "1-3年", "education": "本科", "skills": "Java,Spring,MySQL"},
    ]
    
    df = clean_jobs(test_data)
    exporter = Exporter()
    
    # 测试 CSV
    csv_path = exporter.export_csv(df)
    print(f"CSV: {csv_path}")
    
    # 测试 Excel（带分析）
    from analyzer.stats import analyze_jobs
    stats = analyze_jobs(df)
    excel_path = exporter.export_excel(df, stats=stats)
    print(f"Excel: {excel_path}")
