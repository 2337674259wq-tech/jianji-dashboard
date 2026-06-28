@echo off
chcp 65001 >nul
cd /d "D:\抖音剪辑账号"
echo.
echo 🎬 拍摄+剪辑教学 · 每日选题系统
echo ═══════════════════════════════════
echo.
echo [1] 运行每日选题采集 + 刷新仪表盘
echo [2] 仅刷新可视化仪表盘
echo [3] 打开仪表盘
echo.
set /p choice="请选择 (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo 🔍 正在采集今日选题...
    set PYTHONIOENCODING=utf-8
    python 脚本/daily_topics.py
    echo.
    echo 🚀 正在打开仪表盘...
    start "" "D:\抖音剪辑账号\仪表盘.html"
)

if "%choice%"=="2" (
    echo.
    echo 🎨 正在刷新仪表盘...
    set PYTHONIOENCODING=utf-8
    python 脚本/generate_dashboard.py
    echo.
    echo 🚀 正在打开仪表盘...
    start "" "D:\抖音剪辑账号\仪表盘.html"
)

if "%choice%"=="3" (
    start "" "D:\抖音剪辑账号\仪表盘.html"
)

pause
