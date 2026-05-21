# 松下传感器选型 v1.0.0

松下 CX 系列光电传感器选型系统（国内版）

前后端选型工具，**全部本地运行，不依赖国外 CDN**。已配置国内 npm / pip 镜像，支持 **单端口** 打开页面。

## 国内用户快速开始（推荐）

1. 安装 [Python 3.8+](https://www.python.org/downloads/) 和 [Node.js 18+](https://nodejs.org/)（安装时勾选「添加到 PATH」）
2. 双击 **`安装依赖.bat`**（使用清华 pip 镜像 + npmmirror npm 镜像）
3. 双击 **`启动.bat`**
4. 浏览器自动打开：**http://127.0.0.1:8000**

> 无需输入 `uvicorn` 命令，也无需开两个终端。前端已打包进后端，只访问 8000 端口即可。

### 开发调试（改代码时）

双击 **`开发模式.bat`**，会打开：

- 后端：http://127.0.0.1:8000（API）
- 前端：http://127.0.0.1:5173（热更新）

## 功能

- **前端**：检测方式、距离、透明体/小光点/基板/耐油等需求
- **后端**：型号推荐、内置 CX-400 型号库、本地 PDF 解析
- **PDF 目录**：`backend\data\pdfs\`

## 手动安装（可选）

### 后端（清华镜像）

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
$env:PIP_CONFIG_FILE = "$PWD\pip.ini"
python -m pip install -r requirements.txt
python run.py
```

### 前端（npmmirror）

```powershell
cd frontend
npm install
npm run build
```

构建完成后，在 `backend` 目录执行 `python run.py`，访问 http://127.0.0.1:8000

## 常见问题

| 问题 | 解决 |
|------|------|
| `uvicorn` 不是内部命令 | 使用 `python run.py`，不要直接敲 uvicorn |
| pip 很慢或失败 | 运行 `安装依赖.bat`，或设置 `PIP_CONFIG_FILE=backend\pip.ini` |
| npm 很慢 | 项目已含 `frontend\.npmrc` 指向 npmmirror |
| 页面打不开 | 确认 `frontend\dist\index.html` 存在，没有则重新运行 `安装依赖.bat` |
| 仅 API 无界面 | 先 `cd frontend` 再 `npm run build` |

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 服务状态 |
| POST | `/api/recommend` | 型号推荐 |
| POST | `/api/pdf/import` | 扫描 PDF 目录 |
| POST | `/api/pdf/upload` | 上传 PDF |

文档：http://127.0.0.1:8000/docs

## 项目结构

```
panasonic-cx-selector/
├── 安装依赖.bat      # 国内镜像一键安装
├── 启动.bat          # 单端口启动（推荐）
├── 开发模式.bat      # 前后端分离热更新
├── backend/
│   ├── run.py        # python run.py 启动
│   ├── pip.ini       # 清华 pip 源
│   └── data/
└── frontend/
    ├── .npmrc        # npmmirror 源
    └── dist/         # 构建后由后端托管
```
