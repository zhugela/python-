# 学生成绩管理系统

## 📌 项目简介
基于 Python 开发的学生成绩管理系统，支持学生信息管理、成绩录入、统计分析、可视化图表、Excel 报表导出等功能。本项目为《Python程序设计》课程期末考查项目。

## 🛠 技术栈
- Python 3.x
- matplotlib — 数据可视化图表
- openpyxl — Excel 报表导出
- JSON — 数据持久化存储

## 📁 项目结构
```
student-grade-manager/
├── main.py          # 主程序入口 + 交互菜单
├── student.py       # 学生数据模型
├── file_handler.py  # JSON 文件读写与 CRUD
├── analyzer.py      # 统计分析 + 图表
├── exporter.py      # Excel 导出
├── data.json        # 数据文件（自动生成）
├── requirements.txt # 依赖清单
└── README.md        # 项目说明
```

## 🚀 运行方式
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行程序
python main.py
```

## 📋 功能列表
| 功能 | 说明 |
|------|------|
| 添加学生 | 录入学号、姓名 |
| 查看所有学生 | 显示全部学生及成绩概况 |
| 查找学生 | 按学号或姓名查找 |
| 录入/修改成绩 | 按科目录入成绩 |
| 统计分析 | 最高分/最低分/平均分/分数段分布 |
| 成绩排名 | 按总分降序排名 |
| 显示图表 | 柱状图 + 饼图可视化 |
| 导出 Excel | 生成格式化学业报表 |
| 删除学生 | 删除学生记录 |
