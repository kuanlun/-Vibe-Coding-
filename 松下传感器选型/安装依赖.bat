@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo  松下 CX 选型系统 - 国内镜像安装依赖
echo ========================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8 及以上
    pause
    exit /b 1
)

where node >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18 及以上
    pause
    exit /b 1
)

echo [1/3] 创建 Python 虚拟环境并安装后端依赖（清华镜像）...
cd backend
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
set PIP_CONFIG_FILE=%cd%\pip.ini
set HTTP_PROXY=
set HTTPS_PROXY=
set ALL_PROXY=
set http_proxy=
set https_proxy=
set all_proxy=
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --default-timeout=120
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --default-timeout=120
if errorlevel 1 (
    echo [错误] 后端依赖安装失败
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo [2/3] 安装前端依赖（npmmirror 镜像）...
cd frontend
call npm install --registry=https://registry.npmmirror.com
if errorlevel 1 (
    echo [错误] 前端依赖安装失败
    cd ..
    pause
    exit /b 1
)

echo.
echo [3/3] 构建前端（打包进后端，单端口访问）...
call npm run build
if errorlevel 1 (
    echo [错误] 前端构建失败
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo  安装完成！请双击「启动.bat」运行程序
echo  浏览器访问: http://127.0.0.1:8000
echo ========================================
pause
