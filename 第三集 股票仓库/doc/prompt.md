# 股票仓库管理网站 - Vibe Coding Prompt

## 项目信息

- **项目名称**：股票仓库管理网站
- **项目类型**：Web 监控平台
- **核心功能**：多市场股票持仓监控，支持 A股、台股、美股，实时数据展示，价格提醒，数据导出
- **目标用户**：个人投资者/小团队（不超过10人）

## 技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| 后端 | Python FastAPI | 高性能 API 框架 |
| 前端 | Vue 3 + Vite | 主流前端框架 |
| 数据库 | SQLite | 轻量级关系型数据库 |
| 数据源 | AKShare / Yahoo Finance | 免费股票数据 API |
| 代码检测 | mypy (strict) + ruff | 类型检查 + 代码风格 |
| 测试框架 | pytest | 单元测试 |

## 项目结构

```
stock-portfolio-manager/
├── backend/              # 后端 (Python FastAPI)
│   ├── app/
│   │   ├── main.py       # FastAPI 入口
│   │   ├── models/       # 数据模型 (SQLAlchemy)
│   │   ├── routers/      # API 路由
│   │   ├── services/    # 业务逻辑
│   │   └── utils/        # 工具函数
│   ├── tests/            # pytest 测试
│   ├── requirements.txt   # Python 依赖
│   └── database.db       # SQLite 数据库
├── frontend/             # 前端 (Vue 3)
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   ├── components/   # 通用组件
│   │   ├── stores/       # 状态管理 (Pinia)
│   │   ├── router/       # 路由配置
│   │   └── assets/       # 静态资源
│   └── package.json
├── doc/
│   ├── proposal.md       # 需求文档
│   ├── design.md         # 概要设计
│   └── tasks/            # 任务清单
└── .git/                 # Git 仓库
```

## 模块列表

### 1. 用户模块 (User)
- 用户注册/登录（JWT 认证）
- 密码加密存储（bcrypt）
- 用户设置（提醒偏好）

### 2. 持仓模块 (Portfolio)
- CRUD：添加、编辑、删除持仓股票
- 按市场分类展示（A股、台股、美股）
- 持仓盈亏计算

### 3. 股票数据模块 (StockData)
- 调用 AKShare 获取 A股/台股数据
- 调用 Yahoo Finance 获取美股数据
- 内存缓存机制（降低 API 调用）
- 货币转换（美元/台币 → 人民币）

### 4. 提醒模块 (Alert)
- 价格监控（高于/低于阈值）
- 应用内 WebSocket 实时通知
- 提醒历史记录

### 5. 导出模块 (Export)
- Excel 导出 (.xlsx)
- CSV 导出 (.csv)
- 按市场筛选

## 数据库表结构

### users
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| username | VARCHAR(50) | 用户名（唯一） |
| password | VARCHAR(255) | 加密密码 |
| email | VARCHAR(100) | 邮箱 |
| alert_enabled | BOOLEAN | 提醒开关 |
| created_at | DATETIME | 创建时间 |

### portfolios
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| user_id | INTEGER | 外键 → users |
| market | VARCHAR(10) | A股/台股/美股 |
| symbol | VARCHAR(20) | 股票代码 |
| name | VARCHAR(50) | 股票名称 |
| shares | FLOAT | 持仓数量 |
| cost_price | FLOAT | 成本价 |
| created_at | DATETIME | 创建时间 |

### alerts
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| user_id | INTEGER | 外键 → users |
| symbol | VARCHAR(20) | 股票代码 |
| condition | VARCHAR(10) | 高于/低于 |
| target_price | FLOAT | 目标价格 |
| triggered | BOOLEAN | 是否触发 |
| created_at | DATETIME | 创建时间 |

## API 接口

### 认证 (/api/auth)
- POST /api/auth/register - 用户注册
- POST /api/auth/login - 用户登录
- GET /api/auth/me - 获取当前用户

### 持仓 (/api/portfolios)
- GET /api/portfolios - 获取持仓列表
- POST /api/portfolios - 添加持仓
- PUT /api/portfolios/{id} - 更新持仓
- DELETE /api/portfolios/{id} - 删除持仓

### 股票数据 (/api/stocks)
- GET /api/stocks/quote/{symbol} - 获取实时报价
- GET /api/stocks/batch - 批量获取报价

### 提醒 (/api/alerts)
- GET /api/alerts - 获取提醒列表
- POST /api/alerts - 创建提醒
- DELETE /api/alerts/{id} - 删除提醒

### 导出 (/api/export)
- GET /api/export/excel - 导出 Excel
- GET /api/export/csv - 导出 CSV

## 代码质量要求

### Python
- 类型注解完整（mypy strict 检查通过）
- ruff 检查通过（无 warnings/errors）
- pytest 单元测试（覆盖率 ≥ 60%）
- 关键函数有 docstring

### 前端
- Vue 3 Composition API
- TypeScript（如使用）
- ESLint 检查通过

## 界面风格

- **主题**：深色 Linear 风格
- **布局**：按市场分类，每个市场一个卡片/区块
- **响应式**：支持桌面端 + 移动端
- **字体**：等宽字体显示股票代码和价格

## 执行要求

1. **主 Agent** 负责跟踪整体进度，协调子 Agent
2. **子 Agent** 实现每个模块，完成开发 + 测试
3. **无人工参与**：所有代码由 Agent 生成和修改
4. **测试通过**：pytest 单元测试 100% 通过
5. **检测通过**：mypy strict + ruff 检查通过
6. **Git 提交**：每个模块完成后提交一次

---

*Prompt 生成时间：2026-05-22*