# 招聘信息采集与岗位分析系统

> Python 实战项目，适合 Java 转 Python 的开发者练手

## 项目简介

抓取公开招聘网站的岗位信息，进行数据清洗和统计分析，生成可视化报表。

## 技术栈

| 类别 | 技术 | 作用 |
|------|------|------|
| HTTP 请求 | `requests` | 抓取网页 |
| HTML 解析 | `BeautifulSoup` | 解析 HTML |
| 数据处理 | `pandas` | 数据清洗、分析 |
| Excel 导出 | `openpyxl` | 生成 Excel 报表 |
| 日志 | `loguru` | 日志记录 |

## 项目结构

```
job-crawler/
├── main.py                 # 主入口
├── requirements.txt        # 依赖列表
├── README.md              # 项目说明
├── logs/                  # 日志目录（自动创建）
├── data/
│   ├── raw/               # 原始数据
│   └── clean/             # 清洗后数据
├── crawler/
│   ├── __init__.py
│   ├── fetcher.py         # HTTP 请求模块
│   ├── parser.py          # HTML 解析模块
│   └── scheduler.py       # 爬虫调度器
├── analyzer/
│   ├── __init__.py
│   ├── cleaner.py         # 数据清洗
│   ├── stats.py           # 统计分析
│   └── exporter.py        # 数据导出
└── utils/
    ├── __init__.py
    ├── logger.py          # 日志工具
    └── config.py          # 配置文件
```

## 快速开始

### 1. 安装依赖

```bash
cd D:\code\Python入门到精通\16_项目实战\job-crawler
pip install -r requirements.txt
```

### 2. 运行项目

```bash
# 使用演示数据测试（无需网络）
python main.py --demo

# 抓取真实数据
python main.py -k Python -c 北京 -p 5

# 查看更多选项
python main.py --help
```

### 3. 输出文件

- `data/clean/jobs_*.csv` - 岗位数据 CSV
- `data/clean/jobs_analysis_*.xlsx` - 带分析的 Excel 报表

## 功能说明

### 抓取模块 (crawler/)

- **fetcher.py**: HTTP 请求，支持重试、请求间隔
- **parser.py**: 解析 HTML，支持多网站适配
- **scheduler.py**: 爬虫调度，处理分页

### 分析模块 (analyzer/)

- **cleaner.py**: 数据清洗、去重、字段规范化
- **stats.py**: 统计分析（城市分布、技能热度、薪资水平）
- **exporter.py**: 导出 CSV/Excel

### 工具模块 (utils/)

- **logger.py**: 日志记录（控制台 + 文件）
- **config.py**: 配置文件

## 成果展示

运行后生成的分析报表包含：

- 📊 数据概览（岗位数、公司数、城市数、平均薪资）
- 🏙️ 城市分布 Top 10
- 💼 招聘最多的公司 Top 10
- 💻 热门技能 Top 20
- 💰 各城市薪资水平
- 📈 各经验/学历薪资水平

## 进阶扩展

### 添加 Flask 查询接口

```python
# 添加一个简单的查询接口
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/jobs')
def get_jobs():
    from analyzer.exporter import Exporter
    exporter = Exporter()
    df = exporter.load_csv()
    return jsonify(df.to_dict('records'))
```

### 动态页面处理

如果目标网站是 JS 动态渲染，替换为 Playwright：

```python
from playwright.sync_api import sync_playwright

def fetch_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        return html
```

## 注意事项

⚠️ **合规提示**：
1. 请遵守目标网站的 `robots.txt`
2. 控制请求频率，避免对服务器造成压力
3. 不要抓取需要登录的私人数据
4. 本项目仅供学习研究使用

## 对比 Java

| Python | Java |
|--------|------|
| `requests` | HttpClient / OkHttp |
| `BeautifulSoup` | Jsoup |
| `pandas` | Stream API + 外部库 |
| `openpyxl` | Apache POI |
| 函数式写法多 | 面向对象严谨 |

---

*Created by 小鱼 🐟 for 亮哥的学习项目*
