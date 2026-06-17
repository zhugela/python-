"""
数据清洗模块
对原始数据进行清洗、去重、规范化
"""
import re
from typing import List, Dict
import pandas as pd
from pandas import DataFrame
from utils.logger import logger


class Cleaner:
    """数据清洗器"""
    
    def __init__(self):
        self.required_fields = ["title", "company", "city", "salary"]
    
    def clean_jobs(self, jobs: List[Dict]) -> pd.DataFrame:
        """
        清洗岗位数据
        
        Args:
            jobs: 原始岗位列表
            
        Returns:
            清洗后的 DataFrame
        """
        if not jobs:
            logger.warning("没有数据需要清洗")
            return pd.DataFrame()
        
        df = pd.DataFrame(jobs)
        original_count = len(df)
        
        logger.info(f"开始清洗数据，原始数量: {original_count}")
        
        # 1. 去除重复
        df = self._remove_duplicates(df)
        
        # 2. 清洗必填字段
        df = self._clean_required_fields(df)
        
        # 3. 标准化城市
        df["city"] = df["city"].apply(self._normalize_city)
        
        # 4. 解析薪资
        df[["salary_min", "salary_max"]] = df["salary"].apply(
            lambda x: pd.Series(self._parse_salary(x))
        )
        
        # 5. 处理经验要求
        df["experience"] = df["experience"].apply(self._normalize_experience)
        
        # 6. 处理学历要求
        df["education"] = df["education"].apply(self._normalize_education)
        
        # 7. 过滤无效数据
        df = self._filter_invalid(df)
        
        cleaned_count = len(df)
        logger.success(f"清洗完成: {original_count} -> {cleaned_count} (去除 {original_count - cleaned_count} 条)")
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """去除重复数据"""
        before = len(df)
        df = df.drop_duplicates(subset=["title", "company"], keep="first")
        removed = before - len(df)
        if removed > 0:
            logger.info(f"去除重复: {removed} 条")
        return df
    
    def _clean_required_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗必填字段"""
        for field in self.required_fields:
            if field in df.columns:
                df[field] = df[field].fillna("").astype(str).str.strip()
                # 过滤掉为空的必填字段
                df = df[df[field] != ""]
        return df
    
    def _normalize_city(self, city: str) -> str:
        """标准化城市名称"""
        if not city:
            return "未知"
        
        # 去除多余字符
        city = city.strip()
        
        # 常见城市映射
        city_map = {
            "北京": "北京",
            "上海": "上海", 
            "深圳": "深圳",
            "广州": "广州",
            "杭州": "杭州",
            "南京": "南京",
            "成都": "成都",
            "武汉": "武汉",
            "西安": "西安",
            "苏州": "苏州",
            "天津": "天津",
            "重庆": "重庆",
            "长沙": "长沙",
            "郑州": "郑州",
            "东莞": "东莞",
            "佛山": "佛山",
            "宁波": "宁波",
            "青岛": "青岛",
            "无锡": "无锡",
            "厦门": "厦门",
        }
        
        for key, value in city_map.items():
            if key in city:
                return value
        
        return city[:4] if len(city) > 4 else city
    
    def _parse_salary(self, salary: str) -> tuple:
        """
        解析薪资字符串
        
        Returns:
            (最低薪资, 最高薪资) 单位：K/月
        """
        if not salary or salary == "未知":
            return (0, 0)
        
        salary = salary.lower().replace(",", "")
        
        # 匹配 15K-30K 或 15-30K 格式
        match = re.search(r"(\d+(?:\.\d+)?)[kK]?\s*[-~]\s*(\d+(?:\.\d+)?)[kK]?", salary)
        if match:
            return (float(match.group(1)), float(match.group(2)))
        
        # 匹配 1.5万-3万 格式
        match = re.search(r"([\d.]+)\s*万\s*[-~]\s*([\d.]+)\s*万", salary)
        if match:
            return (float(match.group(1)) * 10, float(match.group(2)) * 10)
        
        # 匹配 15K 格式（只有最高薪）
        match = re.search(r"(\d+(?:\.\d+)?)[kK]", salary)
        if match:
            val = float(match.group(1))
            return (val * 0.8, val)  # 估算最低薪为最高薪的 80%
        
        return (0, 0)
    
    def _normalize_experience(self, exp: str) -> str:
        """标准化经验要求"""
        if not exp or exp == "未知":
            return "不限"
        
        exp = exp.strip()
        
        if "应届" in exp or "不限" in exp or "经验不限" in exp:
            return "不限"
        if "1年" in exp:
            return "1年以下"
        if "1-3" in exp or "1-5" in exp:
            return "1-3年"
        if "3-5" in exp:
            return "3-5年"
        if "5-10" in exp:
            return "5-10年"
        if "10" in exp:
            return "10年以上"
        
        return exp
    
    def _normalize_education(self, edu: str) -> str:
        """标准化学历要求"""
        if not edu or edu == "未知":
            return "不限"
        
        edu = edu.strip()
        
        if "不限" in edu or "学历不限" in edu:
            return "不限"
        if "博士" in edu:
            return "博士"
        if "硕士" in edu:
            return "硕士"
        if "本科" in edu:
            return "本科"
        if "大专" in edu or "专科" in edu:
            return "大专"
        if "高中" in edu or "中专" in edu:
            return "高中/中专"
        
        return edu
    
    def _filter_invalid(self, df: pd.DataFrame) -> pd.DataFrame:
        """过滤无效数据"""
        before = len(df)
        
        # 过滤薪资为0的（可能是无效数据）
        df = df[~((df["salary_min"] == 0) & (df["salary_max"] == 0))]
        
        removed = before - len(df)
        if removed > 0:
            logger.info(f"过滤无效数据: {removed} 条")
        
        return df


def clean_jobs(jobs: List[Dict]) -> pd.DataFrame:
    """便捷函数：清洗岗位数据"""
    cleaner = Cleaner()
    return cleaner.clean_jobs(jobs)


if __name__ == "__main__":
    # 测试
    logger.info("测试 cleaner 模块")
    
    test_data = [
        {"title": "Python开发", "company": "字节", "city": "北京", "salary": "20K-40K", "experience": "3-5年", "education": "本科"},
        {"title": "Python开发", "company": "字节", "city": "北京", "salary": "20K-40K", "experience": "3-5年", "education": "本科"},  # 重复
        {"title": "Java开发", "company": "阿里", "city": "杭州", "salary": "15K-30K", "experience": "1-3年", "education": "本科"},
        {"title": "Go开发", "company": "腾讯", "city": "深圳", "salary": "25K-50K", "experience": "5-10年", "education": "硕士"},
    ]
    
    df = clean_jobs(test_data)
    print(df)
