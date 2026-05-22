<template>
  <div class="dashboard">
    <header class="header">
      <h1>仪表盘</h1>
      <div class="header-actions">
        <button @click="exportCSV" class="btn-secondary">导出 CSV</button>
        <button @click="handleLogout" class="btn-secondary">退出</button>
      </div>
    </header>

    <div class="markets">
      <div v-for="market in markets" :key="market.name" class="market-card">
        <div class="market-header">
          <h2>{{ market.name }}</h2>
          <span class="total-value">总价值: ¥{{ market.totalValue.toFixed(2) }}</span>
        </div>
        <div class="stocks-list">
          <div v-if="market.stocks.length === 0" class="empty-state">
            暂无持仓
          </div>
          <div v-for="stock in market.stocks" :key="stock.id" class="stock-item">
            <div class="stock-info">
              <span class="stock-symbol">{{ stock.symbol }}</span>
              <span class="stock-name">{{ stock.name }}</span>
            </div>
            <div class="stock-details">
              <span class="stock-shares">{{ stock.shares }} 股</span>
              <span class="stock-cost">成本: ¥{{ stock.cost_price }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const portfolios = ref([])
const token = localStorage.getItem('token')

const markets = computed(() => {
  const marketMap = {
    'A股': { name: 'A股', stocks: [], totalValue: 0 },
    '台股': { name: '台股', stocks: [], totalValue: 0 },
    '美股': { name: '美股', stocks: [], totalValue: 0 },
  }
  portfolios.value.forEach(p => {
    if (marketMap[p.market]) {
      marketMap[p.market].stocks.push(p)
      marketMap[p.market].totalValue += p.shares * p.cost_price
    }
  })
  return Object.values(marketMap)
})

const fetchPortfolios = async () => {
  try {
    const response = await axios.get('/api/portfolios', {
      headers: { Authorization: `Bearer ${token}` }
    })
    portfolios.value = response.data
  } catch (error) {
    if (error.response && error.response.status === 401) {
      handleLogout()
    }
  }
}

const exportCSV = () => {
  window.open('/api/export/csv', '_blank')
}

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  if (!token) {
    router.push('/login')
    return
  }
  fetchPortfolios()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 24px;
  background: #0f0f0f;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.header h1 {
  font-size: 28px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-secondary {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.markets {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.market-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
}

.market-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.market-header h2 {
  font-size: 20px;
  font-weight: 600;
}

.total-value {
  color: #4f46e5;
  font-weight: 600;
}

.stocks-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.stock-item {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
}

.stock-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stock-symbol {
  font-family: monospace;
  font-size: 16px;
  font-weight: 600;
}

.stock-name {
  color: #888;
  font-size: 14px;
}

.stock-details {
  text-align: right;
  font-family: monospace;
}

.stock-shares {
  display: block;
  font-size: 14px;
}

.stock-cost {
  display: block;
  color: #888;
  font-size: 12px;
  margin-top: 4px;
}
</style>