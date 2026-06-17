@echo off
chcp 65001 >nul
title Python招聘信息采集系统

echo.
echo ========================================
echo   招聘信息采集与岗位分析系统
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查依赖是否安装...
python -c "import requests, bs4, pandas, openpyxl, loguru, tqdm" 2>nul
if %errorlevel% neq 0 (
    echo 发现缺少依赖，正在安装...
    pip install -r requirements.txt
    echo.
)

echo [2/3] 启动爬虫...
echo.
echo 请选择运行模式:
echo   1. 使用演示数据（无需网络，推荐首次运行）
echo   2. 抓取真实 Python 岗位（北京）
echo   3. 自定义参数
echo.
set /p choice=请输入选项 (1/2/3): 

if "%choice%"=="1" (
    python main.py --demo
) else if "%choice%"=="2" (
    python main.py -k Python -c 北京 -p 5
) else (
    set /p keyword=请输入搜索关键词: 
    set /p city=请输入城市: 
    set /p pages=请输入抓取页数: 
    python main.py -k %keyword% -c %city% -p %pages%
)

echo.
echo [3/3] 完成！
echo.
pause
