# 数据库模块任务

## 概述
- 职责: 创建SQLite数据库和表结构
- 依赖: 无
- 完成标准: 数据库可正常读写

## 子任务

- [ ] 创建 `data/` 目录
- [ ] 创建 `uploads/` 目录
- [ ] 创建 BlindBox 表 (id, name, description, price, image_path, is_secret, created_at, updated_at)
- [ ] 创建 Admin 表 (id, username, password, created_at)
- [ ] 初始化默认管理员账号 (admin/admin)

## 验证

完成后执行以下SQL验证:
```sql
SELECT name FROM sqlite_master WHERE type='table';
INSERT INTO admin (username, password) VALUES ('admin', 'hashed_password');
```