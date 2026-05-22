# 提醒模块 (Alert) - 任务清单

## 后端任务

- [ ] 创建 `backend/app/models/alert.py` - 提醒数据模型
  - 字段：id, user_id, symbol, condition, target_price, triggered, created_at

- [ ] 创建 `backend/app/routers/alert.py` - 提醒路由
  - [ ] GET /api/alerts - 获取提醒列表
  - [ ] POST /api/alerts - 创建提醒
  - [ ] DELETE /api/alerts/{id} - 删除提醒
  - [ ] PUT /api/alerts/{id}/triggered - 更新触发状态

- [ ] 创建 `backend/app/services/alert_service.py` - 提醒服务
  - [ ] 价格监控逻辑
  - [ ] 定时检查提醒（每分钟）

## WebSocket 任务

- [ ] 实现 WebSocket 连接（Socket.io）
- [ ] 实现实时推送提醒到前端

## 前端任务

- [ ] 创建 `frontend/src/components/AlertItem.vue` - 提醒项组件
- [ ] 创建提醒设置表单
- [ ] 实现应用内通知展示
- [ ] 实现提醒开关功能