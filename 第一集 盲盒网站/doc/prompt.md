# 盲盒展示网页 - Vibe Coding Prompt

## 项目概述

**项目名称**: 盲盒展示网页
**项目类型**: 前后端分离Web应用
**技术栈**: Python (Flask) + SQLite + 原生HTML/CSS/JavaScript
**部署方式**: 本地运行

---

## 功能需求

### 1. 前台展示页面
- 首页: 展示所有盲盒商品列表（图片、名称、价格）
- 详情页: 展示单个盲盒的详细信息（图片、名称、描述、价格、是否隐藏内容）
- 响应式设计: 适配电脑和手机浏览器

### 2. 后台管理系统
- 登录验证: 管理员账号登录（默认: admin/admin123）
- 盲盒管理: 添加、编辑、删除盲盒商品
- 图片上传: 上传盲盒封面图片到本地
- 数据列表: 分页展示和管理盲盒数据

### 3. 界面风格
- 简约小清新风格
- 马卡龙色系配色
- 圆角设计、柔和阴影效果、简洁留白布局

---

## 项目结构

```
d:\VSProject\
├── Python/
│   └── website.py          # Python后端主程序
├── static/
│   ├── css/
│   │   └── style.css       # 马卡龙色系样式
│   ├── js/
│   │   └── main.js         # 前台脚本
│   └── images/             # 静态图片
├── templates/
│   ├── index.html         # 前台首页
│   ├── detail.html        # 盲盒详情页
│   └── admin/
│       ├── login.html     # 登录页
│       ├── dashboard.html # 管理首页
│       ├── list.html      # 列表页
│       └── form.html      # 新增/编辑表单
├── uploads/               # 上传文件目录
├── data/
│   └── database.db        # SQLite数据库
└── doc/
    ├── proposal.md        # 需求文档
    ├── high-level-design.md  # 概要设计
    └── tasks/             # 任务分解
        ├── database.md
        ├── backend-api.md
        ├── public-frontend.md
        └── admin-frontend.md
```

---

## 模块划分

按以下顺序开发（依赖关系）:

### 1. database.md - 数据库模块
**负责人**: Sub-agent 1
**职责**: 创建SQLite数据库和表结构
**交付物**:
- `data/` 目录
- `uploads/` 目录
- BlindBox 表 (id, name, description, price, image_path, is_secret, created_at, updated_at)
- Admin 表 (id, username, password, created_at)
- 初始化默认管理员 (admin/admin123，BCrypt加密)

### 2. backend-api.md - 后端API模块
**负责人**: Sub-agent 2
**职责**: Python后端RESTful API
**交付物**:
- Flask应用 (website.py)
- 公共API: GET /api/boxes, GET /api/boxes/<id>
- 管理API: POST /api/admin/login, POST /api/admin/logout, POST /api/boxes, PUT /api/boxes/<id>, DELETE /api/boxes/<id>, POST /api/upload
- 页面路由: /, /box/<id>, /admin/login, /admin, /admin/boxes, /admin/boxes/new, /admin/boxes/<id>/edit

### 3. public-frontend.md - 前台展示模块
**负责人**: Sub-agent 3
**职责**: 用户可见的盲盒展示页面
**交付物**:
- `templates/index.html` - 首页盲盒列表
- `templates/detail.html` - 盲盒详情页
- `static/css/style.css` - 马卡龙色系样式
- `static/js/main.js` - 前台交互脚本

### 4. admin-frontend.md - 后台管理模块
**负责人**: Sub-agent 4
**职责**: 管理员盲盒管理界面
**交付物**:
- `templates/admin/login.html` - 登录页
- `templates/admin/dashboard.html` - 管理首页
- `templates/admin/list.html` - 盲盒列表页
- `templates/admin/form.html` - 新增/编辑表单

---

## 开发约束

### 代码质量
- 所有Python代码必须通过mypy类型检查
- 所有Python代码必须通过ruff lint检查
- 所有Python代码必须有完整的pytest单元测试
- 使用BCrypt加密存储密码
- 使用参数化查询防止SQL注入

### 测试覆盖
- 数据库模块: 表创建、初始数据验证
- 后端API: 所有端点的正确/错误响应测试
- 前台模块: 页面渲染、响应式布局验证
- 后台模块: 登录、CRUD操作验证

---

## 安全要求

- 管理员密码使用BCrypt加密存储
- 管理后台通过Session认证
- 未登录访问重定向到登录页
- 图片上传限制类型(仅图片)和大小(最大5MB)
- SQL语句使用参数化查询

---

## 数据模型

### BlindBox 表
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

### Admin 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| username | TEXT UNIQUE | 用户名 |
| password | TEXT | 密码(BCrypt加密) |
| created_at | DATETIME | 创建时间 |

---

## 执行流程

主Agent步骤:
1. 读取并理解所有输入文档
2. 创建Sub-agent 1 (database模块)，等待完成
3. 创建Sub-agent 2 (backend-api模块)，等待完成
4. 创建Sub-agent 3 (public-frontend模块)，等待完成
5. 创建Sub-agent 4 (admin-frontend模块)，等待完成
6. 运行完整测试套件验证
7. 更新doc/tasks/progress.md标记完成状态

---

## 验证标准

每个模块完成后必须:
1. 通过pytest单元测试
2. 通过mypy类型检查
3. 通过ruff lint检查
4. 手动验证功能正常

---

## 联系方式

如有任何不明确之处，请联系用户确认后再继续。