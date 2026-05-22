<template>
  <div class="portfolio">
    <header class="header">
      <h1>持仓管理</h1>
      <button @click="showAddForm = true" class="btn-primary">添加持仓</button>
    </header>

    <div v-if="showAddForm" class="modal">
      <div class="modal-content">
        <h2>添加持仓</h2>
        <form @submit.prevent="handleAdd">
          <div class="form-group">
            <label>市场</label>
            <select v-model="newPortfolio.market" required>
              <option value="">选择市场</option>
              <option value="A股">A股</option>
              <option value="台股">台股</option>
              <option value="美股">美股</option>
            </select>
          </div>
          <div class="form-group">
            <label>股票代码</label>
            <input v-model="newPortfolio.symbol" type="text" required />
          </div>
          <div class="form-group">
            <label>股票名称</label>
            <input v-model="newPortfolio.name" type="text" required />
          </div>
          <div class="form-group">
            <label>持仓数量</label>
            <input v-model="newPortfolio.shares" type="number" step="0.01" required />
          </div>
          <div class="form-group">
            <label>成本价</label>
            <input v-model="newPortfolio.cost_price" type="number" step="0.01" required />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showAddForm = false" class="btn-secondary">取消</button>
            <button type="submit" class="btn-primary">添加</button>
          </div>
        </form>
      </div>
    </div>

    <div class="portfolio-list">
      <div v-if="portfolios.length === 0" class="empty-state">
        暂无持仓，点击上方按钮添加
      </div>
      <div v-for="p in portfolios" :key="p.id" class="portfolio-item">
        <div class="portfolio-info">
          <span class="portfolio-market">{{ p.market }}</span>
          <span class="portfolio-symbol">{{ p.symbol }}</span>
          <span class="portfolio-name">{{ p.name }}</span>
        </div>
        <div class="portfolio-details">
          <span>{{ p.shares }} 股</span>
          <span>成本: ¥{{ p.cost_price }}</span>
        </div>
        <div class="portfolio-actions">
          <button @click="handleDelete(p.id)" class="btn-danger">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const portfolios = ref([])
const showAddForm = ref(false)
const token = localStorage.getItem('token')
const newPortfolio = ref({
  market: '',
  symbol: '',
  name: '',
  shares: 0,
  cost_price: 0,
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

const handleAdd = async () => {
  try {
    await axios.post('/api/portfolios', newPortfolio.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    showAddForm.value = false
    newPortfolio.value = { market: '', symbol: '', name: '', shares: 0, cost_price: 0 }
    fetchPortfolios()
  } catch (error) {
    alert('添加失败')
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定删除？')) return
  try {
    await axios.delete(`/api/portfolios/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchPortfolios()
  } catch (error) {
    alert('删除失败')
  }
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
.portfolio {
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

.btn-primary {
  padding: 12px 24px;
  background: #4f46e5;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-secondary {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.btn-danger {
  padding: 8px 16px;
  background: #dc2626;
  border: none;
  border-radius: 6px;
  color: #fff;
  font-size: 12px;
  cursor: pointer;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background: #1a1a2e;
  padding: 32px;
  border-radius: 16px;
  width: 400px;
}

.modal-content h2 {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #a0a0a0;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.portfolio-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: #666;
}

.portfolio-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.portfolio-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.portfolio-market {
  padding: 4px 8px;
  background: #4f46e5;
  border-radius: 4px;
  font-size: 12px;
}

.portfolio-symbol {
  font-family: monospace;
  font-size: 16px;
  font-weight: 600;
}

.portfolio-name {
  color: #888;
}

.portfolio-details {
  font-family: monospace;
  color: #888;
}

.portfolio-details span {
  margin-left: 16px;
}
</style>