<template>
  <div class="register-container">
    <div class="register-card">
      <h1>注册账号</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="username" type="text" required />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" class="btn-primary">注册</button>
      </form>
      <p class="login-link">
        已有账号？ <router-link to="/login">登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('')
const email = ref('')
const password = ref('')
const router = useRouter()

const handleRegister = async () => {
  try {
    await axios.post('/api/auth/register', {
      username: username.value,
      password: password.value,
      email: email.value,
    })
    alert('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    alert('注册失败，用户名可能已存在')
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.register-card {
  background: rgba(255, 255, 255, 0.05);
  padding: 40px;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  width: 360px;
}

h1 {
  text-align: center;
  margin-bottom: 32px;
  font-size: 24px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #a0a0a0;
  font-size: 14px;
}

input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #4f46e5;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background: #4f46e5;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #4338ca;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #a0a0a0;
  font-size: 14px;
}

.login-link a {
  color: #4f46e5;
  text-decoration: none;
}
</style>