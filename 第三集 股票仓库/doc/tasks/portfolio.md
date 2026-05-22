# 持仓模块 (Portfolio) - 任务清单

## 后端任务

- [ ] 创建 `backend/app/models/portfolio.py` - 持仓数据模型
  - 字段：id, user_id, market, symbol, name, shares, cost_price, created_at

- [ ] 创建 `backend/app/routers/portfolio.py` - 持仓路由
  - [ ] GET /api/portfolios - 获取持仓列表
  - [ ] POST /api/portfolios - 添加持仓
  - [ ] PUT /api/portfolios/{id} - 更新持仓
  - [ ] DELETE /api/portfolios/{id} - 删除持仓

- [ ] 实现持仓盈亏计算逻辑
- [ ] 实现按市场分类查询

## 前端任务

- [ ] 创建 `frontend/src/views/Portfolio.vue` - 持仓管理页
- [ ] 创建 `frontend/src/components/StockCard.vue` - 股票卡片组件
- [ ] 创建 `frontend/src/components/MarketSection.vue` - 市场分区组件
- [ ] 实现持仓表单（添加/编辑）
- [ ] 实现持仓删除确认对话框

## API 集成任务

- [ ] 股票搜索自动补全
- [ ] 股票代码验证