# 股票仓库监控网站 - 概要设计文档

## 1. 模块架构

```
┌─────────────────────────────────────────────────────────┐
│                      前端 (Vue 3)                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │  登录   │ │ 仪表盘  │ │ 持仓管理 │ │  设置   │       │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘       │
└───────┼───────────┼───────────┼───────────┼─────────────┘
        │           │           │           │
        └───────────┴───────────┴───────────┘
                    │   REST API   │
┌───────────────────┼──────────────┼───────────────────┐
│                   ▼              ▼                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │   用户模块   │ │   持仓模块   │ │  股票数据模块  │      │
│  │ (User)      │ │ (Portfolio) │ │ (StockData) │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
│  ┌─────────────┐ ┌─────────────┐                      │
│  │   提醒模块   │ │   导出模块   │                      │
│  │ (Alert)     │ │ (Export)    │                      │
│  └─────────────┘ └─────────────┘                      │
│                                                         │
│                    后端 (FastAPI)                       │
│                   SQLite 数据库                        │
└─────────────────────────────────────────────────────────┘
```

## 2. 模块说明

### 2.1 用户模块 (User)

| 功能 | 说明 |
|------|------|
| 注册 | 用户名、密码、邮箱 |
| 登录 | JWT Token 认证 |
| 密码加密 | bcrypt 加密 |
| 用户设置 | 提醒偏好、货币单位 |

### 2.2 持仓模块 (Portfolio)

| 功能 | 说明 |
|------|------|
| CRUD | 添加、编辑、删除持仓股票 |
| 分类展示 | 按 A股/台股/美股 分类 |
| 盈亏计算 | 持仓盈亏 = (当前价 - 成本价) × 数量 |

### 2.3 股票数据模块 (StockData)

| 功能 | 说明 |
|------|------|
| 数据获取 | 调用 AKShare / Yahoo Finance API |
| 数据缓存 | Redis/内存缓存，降低 API 调用 |
| 货币转换 | 美元/台币 → 人民币 |

### 2.4 提醒模块 (Alert)

| 功能 | 说明 |
|------|------|
| 价格监控 | 高于/低于阈值时触发 |
| 应用内通知 | WebSocket 实时推送 |
| 提醒历史 | 用户可查看历史提醒 |

### 2.5 导出模块 (Export)

| 功能 | 说明 |
|------|------|
| Excel 导出 | 支持 .xlsx 格式 |
| CSV 导出 | 支持 .csv 格式 |
| 按市场筛选 | 可选择导出的市场 |

## 3. 数据库设计

### 3.1 用户表 (users)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| username | VARCHAR(50) | 用户名（唯一） |
| password | VARCHAR(255) | 加密密码 |
| email | VARCHAR(100) | 邮箱 |
| alert_enabled | BOOLEAN | 提醒开关 |
| created_at | DATETIME | 创建时间 |

### 3.2 持仓表 (portfolios)

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

### 3.3 提醒表 (alerts)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| user_id | INTEGER | 外键 → users |
| symbol | VARCHAR(20) | 股票代码 |
| condition | VARCHAR(10) | 高于/低于 |
| target_price | FLOAT | 目标价格 |
| triggered | BOOLEAN | 是否触发 |
| created_at | DATETIME | 创建时间 |

## 4. API 设计

### 4.1 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录 |
| GET | /api/auth/me | 获取当前用户 |

### 4.2 持仓接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/portfolios | 获取持仓列表 |
| POST | /api/portfolios | 添加持仓 |
| PUT | /api/portfolios/{id} | 更新持仓 |
| DELETE | /api/portfolios/{id} | 删除持仓 |

### 4.3 股票数据接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/stocks/quote/{symbol} | 获取实时报价 |
| GET | /api/stocks/batch | 批量获取报价 |

### 4.4 提醒接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/alerts | 获取提醒列表 |
| POST | /api/alerts | 创建提醒 |
| DELETE | /api/alerts/{id} | 删除提醒 |

### 4.5 导出接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/export/excel | 导出 Excel |
| GET | /api/export/csv | 导出 CSV |

## 5. 前端页面结构

```
src/
├── views/
│   ├── Login.vue          # 登录页
│   ├── Register.vue       # 注册页
│   ├── Dashboard.vue      # 仪表盘（主页）
│   ├── Portfolio.vue      # 持仓管理
│   └── Settings.vue       # 个人设置
├── components/
│   ├── StockCard.vue     # 股票卡片
│   ├── MarketSection.vue # 市场分区（A股/台股/美股）
│   ├── AlertItem.vue     # 提醒项
│   └── ExportButton.vue   # 导出按钮
└── router/
    └── index.js          # 路由配置
```

## 6. 项目目录结构

```
stock-portfolio-monitor/
├── backend/              # 后端
│   ├── app/
│   │   ├── main.py       # FastAPI 入口
│   │   ├── models/       # 数据模型
│   │   ├── routers/     # API 路由
│   │   ├── services/    # 业务逻辑
│   │   └── utils/       # 工具函数
│   ├── requirements.txt
│   └── main.py
├── frontend/             # 前端
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── doc/
    ├── proposal.md
    └── design.md
```

## 7. 技术要点

| 模块 | 技术选型 |
|------|----------|
| 后端框架 | FastAPI |
| ORM | SQLAlchemy |
| 数据库 | SQLite |
| 前端框架 | Vue 3 + Vite |
| 状态管理 | Pinia |
| HTTP 客户端 | Axios |
| WebSocket | Socket.io（实时提醒） |
| 数据导出 | openpyxl / pandas |

---

*文档生成时间：2026-05-22*