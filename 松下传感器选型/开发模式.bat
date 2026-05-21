@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "backend\.venv\Scripts\python.exe" (
    echo 请先双击运行「安装依赖.bat」
    pause
    exit /b 1
)

echo 开发模式：将打开两个窗口（后端 8000 + 前端 5173）
echo 浏览器访问: http://127.0.0.1:5173
echo.

start "CX-后端" cmd /k "cd /d %~dp0backend && call .venv\Scripts\activate.bat && python run.py --reload"
timeout /t 2 /nobreak >nul
start "CX-前端" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5173"
