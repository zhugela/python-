"""
统计分析模块
对清洗后的数据进行统计分析
"""
from typing import Dict, List
import pandas as pd
from utils.logger import logger


class StatsAnalyzer:
    """统计分析器"""
    
    def __init__(self, df: pd.DataFrame):
        """
        初始化分析器
        
        Args:
            df: 清洗后的岗位数据
        """
        self.df = df
    
    def get_overview(self) -> Dict:
        """
        获取数据概览
        
        Returns:
            统计摘要
        """
        if self.df.empty:
            return {"total": 0}
        
        overview = {
            "total": len(self.df),                    # 总岗位数
            "companies": self.df["company"].nunique(), # 公司数
            "cities": self.df["city"].nunique(),       # 城市数
        }
        
        # 薪资统计
        valid_salary = self.df[self.df["salary_max"] > 0]
        if not valid_salary.empty:
            overview["salary"] = {
                "avg_min": round(valid_salary["salary_min"].mean(), 1),
                "avg_max": round(valid_salary["salary_max"].mean(), 1),
                "avg_mid": round((valid_salary["salary_min"] + valid_salary["salary_max"]).mean() / 2, 1),
                "max": valid_salary["salary_max"].max(),
                "min": valid_salary["salary_min"].min(),
            }
        
        return overview
    
    def get_top_cities(self, n: int = 10) -> pd.DataFrame:
        """
        获取岗位最多的城市
        
        Args:
            n: 返回前 N 个
            
        Returns:
            城市统计 DataFrame
        """
        if self.df.empty:
            return pd.DataFrame()
        
        top = self.df["city"].value_counts().head(n).reset_index()
        top.columns = ["city", "count"]
        top["percentage"] = (top["count"] / len(self.df) * 100).round(1)
        
        return top
    
    def get_top_companies(self, n: int = 10) -> pd.DataFrame:
        """
        获取招聘最多的公司
        
        Args:
            n: 返回前 N 个
            
        Returns:
            公司统计 DataFrame
        """
        if self.df.empty:
            return pd.DataFrame()
        
        top = self.df["company"].value_counts().head(n).reset_index()
        top.columns = ["company", "count"]
        
        return top
    
    def get_top_skills(self, n: int = 20) -> pd.DataFrame:
        """
        获取最热门的技能
        
        Args:
            n: 返回前 N 个
            
        Returns:
            技能统计 DataFrame
        """
        if self.df.empty:
            return pd.DataFrame()
        
        # 展开技能列表
        all_skills = []
        for skills_str in self.df["skills"]:
            if skills_str:
                skills = [s.strip() for s in skills_str.split(",") if s.strip()]
                all_skills.extend(skills)
        
        if not all_skills:
            return pd.DataFrame()
        
        skill_counts = pd.Series(all_skills).value_counts().head(n).reset_index()
        skill_counts.columns = ["skill", "count"]
        skill_counts["percentage"] = (skill_counts["count"] / len(all_skills) * 100).round(1)
        
        return skill_counts
    
    def get_salary_by_city(self) -> pd.DataFrame:
        """
        获取各城市薪资水平
        
        Returns:
            城市薪资统计
        """
        if self.df.empty:
            return pd.DataFrame()
        
        valid_salary = self.df[self.df["salary_max"] > 0]
        
        salary_by_city = valid_salary.groupby("city").agg({
            "salary_min": "mean",
            "salary_max": "mean",
            "title": "count"
        }).round(1)
        
        salary_by_city.columns = ["avg_min", "avg_max", "jobs"]
        salary_by_city["avg_mid"] = ((salary_by_city["avg_min"] + salary_by_city["avg_max"]) / 2).round(1)
        salary_by_city = salary_by_city.sort_values("avg_max", ascending=False)
        
        return salary_by_city.reset_index()
    
    def get_salary_by_exp(self) -> pd.DataFrame:
        """
        获取各经验要求薪资水平
        
        Returns:
            经验薪资统计
        """
        if self.df.empty:
            return pd.DataFrame()
        
        valid_salary = self.df[self.df["salary_max"] > 0]
        
        exp_order = ["不限", "1年以下", "1-3年", "3-5年", "5-10年", "10年以上"]
        
        salary_by_exp = valid_salary.groupby("experience").agg({
            "salary_min": "mean",
            "salary_max": "mean",
            "title": "count"
        }).round(1)
        
        salary_by_exp.columns = ["avg_min", "avg_max", "jobs"]
        salary_by_exp["avg_mid"] = ((salary_by_exp["avg_min"] + salary_by_exp["avg_max"]) / 2).round(1)
        
        # 按顺序排列
        salary_by_exp = salary_by_exp.reindex([e for e in exp_order if e in salary_by_exp.index])
        
        return salary_by_exp.reset_index()
    
    def get_salary_by_edu(self) -> pd.DataFrame:
        """
        获取各学历要求薪资水平
        
        Returns:
            学历薪资统计
        """
        if self.df.empty:
            return pd.DataFrame()
        
        valid_salary = self.df[self.df["salary_max"] > 0]
        
        edu_order = ["不限", "高中/中专", "大专", "本科", "硕士", "博士"]
        
        salary_by_edu = valid_salary.groupby("education").agg({
            "salary_min": "mean",
            "salary_max": "mean",
            "title": "count"
        }).round(1)
        
        salary_by_edu.columns = ["avg_min", "avg_max", "jobs"]
        salary_by_edu["avg_mid"] = ((salary_by_edu["avg_min"] + salary_by_edu["avg_max"]) / 2).round(1)
        
        # 按顺序排列
        salary_by_edu = salary_by_edu.reindex([e for e in edu_order if e in salary_by_edu.index])
        
        return salary_by_edu.reset_index()
    
    def get_all_stats(self) -> Dict:
        """
        获取所有统计结果
        
        Returns:
            完整统计字典
        """
        logger.info("开始生成统计分析...")
        
        stats = {
            "overview": self.get_overview(),
            "top_cities": self.get_top_cities(10).to_dict("records"),
            "top_companies": self.get_top_companies(10).to_dict("records"),
            "top_skills": self.get_top_skills(20).to_dict("records"),
            "salary_by_city": self.get_salary_by_city().to_dict("records"),
            "salary_by_exp": self.get_salary_by_exp().to_dict("records"),
            "salary_by_edu": self.get_salary_by_edu().to_dict("records"),
        }
        
        logger.success("统计分析完成")
        return stats


def analyze_jobs(df: pd.DataFrame) -> Dict:
    """便捷函数：分析岗位数据"""
    analyzer = StatsAnalyzer(df)
    return analyzer.get_all_stats()


if __name__ == "__main__":
    # 测试
    from analyzer.cleaner import clean_jobs
    
    logger.info("测试 stats 模块")
    
    test_data = [
        {"title": "Python开发", "company": "字节", "city": "北京", "salary": "20K-40K", "experience": "3-5年", "education": "本科", "skills": "Python,Django,MySQL"},
        {"title": "Java开发", "company": "阿里", "city": "杭州", "salary": "15K-30K", "experience": "1-3年", "education": "本科", "skills": "Java,Spring,MySQL"},
        {"title": "Go开发", "company": "腾讯", "city": "深圳", "salary": "25K-50K", "experience": "5-10年", "education": "硕士", "skills": "Go,Docker,Kubernetes"},
        {"title": "Python后端", "company": "字节", "city": "北京", "salary": "30K-60K", "experience": "5-10年", "education": "本科", "skills": "Python,Go,Redis"},
        {"title": "Python爬虫", "company": "百度", "city": "北京", "salary": "15K-30K", "experience": "1-3年", "education": "本科", "skills": "Python,爬虫,MySQL"},
    ]
    
    df = clean_jobs(test_data)
    stats = analyze_jobs(df)
    
    print("=== 数据概览 ===")
    print(f"总岗位数: {stats['overview']['total']}")
    print(f"平均薪资: {stats['overview']['salary']['avg_mid']}K/月")
    
    print("\n=== Top 城市 ===")
    for city in stats["top_cities"]:
        print(f"  {city['city']}: {city['count']} 个 ({city['percentage']}%)")
    
    print("\n=== Top 技能 ===")
    for skill in stats["top_skills"][:5]:
        print(f"  {skill['skill']}: {skill['count']} 次")
