# 股票数据模块 (StockData) - 任务清单

## 数据获取任务

- [ ] 创建 `backend/app/services/stock_service.py` - 股票服务
  - [ ] 获取 A股数据（使用 AKShare）
  - [ ] 获取美股数据（使用 Yahoo Finance）
  - [ ] 获取台股数据（使用 AKShare）

- [ ] 创建 `backend/app/services/exchange_service.py` - 汇率服务
  - [ ] 获取美元/人民币汇率
  - [ ] 获取台币/人民币汇率

## 缓存任务

- [ ] 实现内存缓存机制
- [ ] 设置缓存过期时间（5分钟）
- [ ] 降低 API 调用频率

## 前端任务

- [ ] 创建 `frontend/src/stores/stock.js` - 股票状态管理
- [ ] 实现实时价格展示组件
- [ ] 实现涨跌幅颜色显示（红涨绿跌）
- [ ] 实现货币转换显示