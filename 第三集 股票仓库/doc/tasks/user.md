# 用户模块 (User) - 任务清单

## 后端任务

- [ ] 创建 `backend/app/models/user.py` - 用户数据模型
  - 字段：id, username, password, email, alert_enabled, created_at

- [ ] 创建 `backend/app/routers/auth.py` - 认证路由
  - [ ] POST /api/auth/register - 用户注册
  - [ ] POST /api/auth/login - 用户登录
  - [ ] GET /api/auth/me - 获取当前用户

- [ ] 实现密码加密（bcrypt）
- [ ] 实现 JWT Token 生成和验证

## 前端任务

- [ ] 创建 `frontend/src/views/Login.vue` - 登录页
- [ ] 创建 `frontend/src/views/Register.vue` - 注册页
- [ ] 创建 `frontend/src/router/index.js` - 路由配置
- [ ] 实现 Token 存储和请求拦截器

## 数据库任务

- [ ] 创建 `backend/app/models/__init__.py` - 模型导出
- [ ] 初始化 SQLite 数据库和表结构