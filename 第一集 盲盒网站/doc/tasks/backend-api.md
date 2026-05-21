# 后端API模块任务

## 概述
- 职责: Python后端RESTful API
- 依赖: database.md
- 完成标准: 所有API返回正确JSON

## 子任务

### 公共API
- [ ] `GET /api/boxes` - 获取盲盒列表
- [ ] `GET /api/boxes/<id>` - 获取盲盒详情

### 管理API (需认证)
- [ ] `POST /api/admin/login` - 管理员登录
- [ ] `POST /api/admin/logout` - 登出
- [ ] `POST /api/boxes` - 创建盲盒
- [ ] `PUT /api/boxes/<id>` - 更新盲盒
- [ ] `DELETE /api/boxes/<id>` - 删除盲盒
- [ ] `POST /api/upload` - 上传图片

### 页面路由
- [ ] `GET /` - 前台首页
- [ ] `GET /box/<id>` - 盲盒详情页
- [ ] `GET /admin/login` - 登录页
- [ ] `GET /admin` - 管理首页
- [ ] `GET /admin/boxes` - 盲盒列表页
- [ ] `GET /admin/boxes/new` - 新增页
- [ ] `GET /admin/boxes/<id>/edit` - 编辑页

## 安全要求
- [ ] Session认证中间件
- [ ] BCrypt密码加密
- [ ] 参数化SQL查询

## 验证

使用curl测试:
```bash
curl http://localhost:5000/api/boxes
curl -X POST http://localhost:5000/api/admin/login -d "username=admin&password=admin123"
```