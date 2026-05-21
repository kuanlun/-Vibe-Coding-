@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "backend\.venv\Scripts\python.exe" (
    echo 请先双击运行「安装依赖.bat」
    pause
    exit /b 1
)

if not exist "frontend\dist\index.html" (
    echo 未检测到前端构建产物，正在构建...
    cd frontend
    call npm run build
    cd ..
)

echo 正在启动服务...
echo 启动后请在浏览器打开: http://127.0.0.1:8000
echo 按 Ctrl+C 可停止服务
echo.

cd backend
call .venv\Scripts\activate.bat
start "" "http://127.0.0.1:8000"
python run.py

pause
