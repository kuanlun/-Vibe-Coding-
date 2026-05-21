# 盲盒展示网页 - 概要设计文档

## 1. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                            │
│  ┌─────────────────┐          ┌─────────────────────────┐  │
│  │   前台展示页面    │          │      后台管理页面         │  │
│  │  (index.html)   │          │  (admin/*.html)         │  │
│  └────────┬────────┘          └───────────┬─────────────┘  │
│           │                               │                │
│           └───────────────┬────────────────┘                │
│                           ▼                                │
│                   ┌───────────────┐                       │
│                   │   Python后端   │                       │
│                   │  (website.py)  │                       │
│                   └───────┬───────┘                       │
│                           │                                │
│                           ▼                                │
│                   ┌───────────────┐                       │
│                   │    SQLite     │                       │
│                   │   数据库文件    │                       │
│                   └───────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

**架构模式**: 前后端分离，后端提供RESTful API

---

## 2. 模块划分

### 2.1 前台展示模块 (Public)

| 模块 | 职责 | 端口/路由 |
|------|------|-----------|
| 首页 | 展示盲盒商品列表 | `GET /` |
| 详情页 | 展示单个盲盒详情 | `GET /box/<id>` |
| 图片服务 | 提供图片访问 | `GET /uploads/` |

### 2.2 后台管理模块 (Admin)

| 模块 | 职责 | 端口/路由 |
|------|------|-----------|
| 登录页 | 管理员登录 | `GET /admin/login` |
| 登录API | 验证登录 | `POST /api/admin/login` |
| 登出API | 退出登录 | `POST /api/admin/logout` |
| 管理首页 | 后台仪表盘 | `GET /admin` |
| 列表页 | 盲盒列表(分页) | `GET /admin/boxes` |
| 新增页 | 添加盲盒表单 | `GET /admin/boxes/new` |
| 编辑页 | 编辑盲盒表单 | `GET /admin/boxes/<id>/edit` |
| 新增API | 创建盲盒 | `POST /api/boxes` |
| 更新API | 更新盲盒 | `PUT /api/boxes/<id>` |
| 删除API | 删除盲盒 | `DELETE /api/boxes/<id>` |
| 图片上传API | 上传图片 | `POST /api/upload` |

### 2.3 数据模型模块

| 模型 | 职责 |
|------|------|
| BlindBox | 盲盒商品CRUD |
| Admin | 管理员认证 |

---

## 3. 模块关系

```
                    ┌─────────────┐
                    │   Public    │
                    │  (前台展示)  │
                    └──────┬──────┘
                           │ 读取
                           ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Admin     │◄──►│  DataModel  │◄──►│  Database   │
│  (后台管理)  │    │  (数据模型)  │    │  (SQLite)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

## 4. 数据模型设计

### 4.1 BlindBox 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT NOT NULL | 盲盒名称 |
| description | TEXT | 描述信息 |
| price | REAL | 价格 |
| image_path | TEXT | 本地图片路径 |
| is_secret | INTEGER DEFAULT 0 | 是否隐藏内容(0=否,1=是) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 4.2 Admin 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| username | TEXT UNIQUE | 用户名 |
| password | TEXT | 密码(BCrypt加密) |
| created_at | DATETIME | 创建时间 |

---

## 5. API设计

### 5.1 公开API

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| GET | /api/boxes | 获取盲盒列表 | `{boxes: [...]}` |
| GET | /api/boxes/<id> | 获取盲盒详情 | `{box: {...}}` |

### 5.2 管理API (需认证)

| 方法 | 路径 | 说明 | 响应 |
|------|------|------|------|
| POST | /api/admin/login | 管理员登录 | `{success: bool}` |
| POST | /api/admin/logout | 登出 | `{success: bool}` |
| POST | /api/boxes | 创建盲盒 | `{box: {...}}` |
| PUT | /api/boxes/<id> | 更新盲盒 | `{box: {...}}` |
| DELETE | /api/boxes/<id> | 删除盲盒 | `{success: bool}` |
| POST | /api/upload | 上传图片 | `{image_path: string}` |

---

## 6. 目录结构

```
d:\VSProject\
├── Python/
│   └── website.py          # Python后端主程序
│
├── static/                  # 静态资源
│   ├── css/
│   │   └── style.css       # 样式文件
│   ├── js/
│   │   └── main.js         # 前台脚本
│   └── images/             # 静态图片
│
├── templates/              # HTML模板
│   ├── index.html         # 前台首页
│   ├── detail.html        # 盲盒详情页
│   └── admin/             # 后台模板
│       ├── login.html     # 登录页
│       ├── dashboard.html # 管理首页
│       ├── list.html      # 列表页
│       └── form.html      # 新增/编辑表单
│
├── uploads/               # 上传文件目录
│
├── data/                  # 数据目录
│   └── database.db        # SQLite数据库
│
└── doc/
    ├── proposal.md       # 需求文档
    └── high-level-design.md  # 本文档
```

---

## 7. 安全设计

- 管理员密码使用BCrypt加密存储
- 管理后台通过Session认证
- 图片上传限制类型和大小
- SQL语句使用参数化查询

---

## 8. 后续步骤

1. 创建数据库表结构
2. 实现Python后端 (website.py)
3. 开发前端页面 (HTML/CSS/JS)
4. 开发后台管理页面
5. 集成测试