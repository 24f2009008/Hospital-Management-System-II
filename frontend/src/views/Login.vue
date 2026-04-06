<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)
const showPassword = ref(false)

const handleLogin = async () => {
  errorMessage.value = ''
  loading.value = true
  try {
    const response = await fetch('http://127.0.0.1:5000/api/login', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    const data = await response.json()
    if (response.ok && data.success) {
      authStore.loginSuccess({ userId: data.user_id, role: data.role, username: username.value })
      if (data.role === 'admin') router.push('/admin/dashboard')
      else if (data.role === 'doctor') router.push('/doctor/dashboard')
      else router.push('/patient/dashboard/')
    } else {
      errorMessage.value = data.message || 'Invalid username or password'
    }
  } catch (err) {
    console.error(err)
    errorMessage.value = 'Server error. Please try again later.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-left">
      <div class="login-brand">
        <div class="brand-icon"><i class="fas fa-hospital"></i></div>
        <h1>HMS Hospital</h1>
        <p>Your health is our priority</p>
      </div>
      <div class="login-features">
        <div class="feature-item">
          <i class="fas fa-shield-alt"></i>
          <span>Secure &amp; Private</span>
        </div>
        <div class="feature-item">
          <i class="fas fa-clock"></i>
          <span>24/7 Access</span>
        </div>
        <div class="feature-item">
          <i class="fas fa-user-md"></i>
          <span>Expert Doctors</span>
        </div>
      </div>
    </div>

    <div class="login-right">
      <div class="login-card">
        <div class="login-header">
          <div class="login-icon"><i class="fas fa-sign-in-alt"></i></div>
          <h2>Welcome Back</h2>
          <p>Sign in to your account</p>
        </div>

        <div v-if="errorMessage" class="alert alert-danger">
          <i class="fas fa-exclamation-circle me-2"></i>{{ errorMessage }}
        </div>

        <form @submit.prevent="handleLogin" novalidate>
          <div class="form-group">
            <label class="form-label">Username</label>
            <div class="input-group">
              <span class="input-group-text"><i class="fas fa-user"></i></span>
              <input v-model="username" type="text" class="form-control"
                placeholder="Enter your username" required autocomplete="username">
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <div class="input-group">
              <span class="input-group-text"><i class="fas fa-lock"></i></span>
              <input v-model="password" :type="showPassword ? 'text' : 'password'"
                class="form-control" placeholder="Enter your password"
                required autocomplete="current-password">
              <button type="button" class="input-group-text btn-toggle-pw"
                @click="showPassword = !showPassword" tabindex="-1">
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
          </div>

          <button type="submit" class="btn btn-primary w-100 btn-login" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-sign-in-alt me-2"></i>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <div class="login-footer">
          <p>Don't have an account?
            <router-link to="/register" class="link-primary">Register here</router-link>
          </p>
          <router-link to="/" class="link-back">
            <i class="fas fa-arrow-left me-1"></i>Back to Home
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page { min-height: 100vh; display: flex; }

.login-left {
  flex: 1;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #0f172a 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}

.login-left::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 40%, rgba(99,102,241,.25) 0%, transparent 65%);
}

.login-brand { text-align: center; color: white; position: relative; z-index: 1; margin-bottom: 3rem; }

.brand-icon {
  width: 80px; height: 80px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 24px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 2rem; color: white;
  box-shadow: 0 12px 30px rgba(99,102,241,.4);
}

.login-brand h1 { font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem; letter-spacing: -0.03em; }
.login-brand p  { opacity: 0.7; font-size: 1rem; }

.login-features { display: flex; flex-direction: column; gap: 1rem; position: relative; z-index: 1; }

.feature-item {
  display: flex; align-items: center; gap: 1rem;
  color: rgba(255,255,255,.8);
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 12px;
  padding: 0.875rem 1.25rem;
  font-size: 0.9375rem; font-weight: 500;
}

.feature-item i { color: #818cf8; font-size: 1.1rem; width: 20px; text-align: center; }

.login-right {
  flex: 1;
  display: flex; align-items: center; justify-content: center;
  padding: 2rem;
  background: #f8fafc;
}

.login-card {
  width: 100%; max-width: 440px;
  background: white;
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0,0,0,.1);
}

.login-header { text-align: center; margin-bottom: 2rem; }

.login-icon {
  width: 60px; height: 60px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.4rem; color: white;
  box-shadow: 0 8px 20px rgba(99,102,241,.3);
}

.login-header h2 { font-size: 1.6rem; font-weight: 800; color: #111827; margin-bottom: 0.25rem; }
.login-header p  { color: #6b7280; margin: 0; }

.form-group { margin-bottom: 1.25rem; }

.input-group { border-radius: 12px; overflow: hidden; }

.input-group-text {
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  color: #9ca3af;
  padding: 0.75rem 1rem;
}

.input-group-text:first-child { border-right: none; }
.input-group-text:last-child  { border-left: none; }

.btn-toggle-pw { cursor: pointer; transition: color 0.2s; }
.btn-toggle-pw:hover { color: #6366f1; }

.form-control {
  border: 1.5px solid #e5e7eb;
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  border-radius: 0;
}

.form-control:focus { border-color: #6366f1; box-shadow: none; z-index: 1; }

.btn-login { padding: 0.875rem; font-size: 1rem; border-radius: 12px; margin-top: 0.5rem; }

.login-footer {
  margin-top: 1.75rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
  text-align: center;
  color: #6b7280;
  font-size: 0.9rem;
}

.login-footer p { margin-bottom: 0.75rem; }

.link-primary { color: #6366f1; font-weight: 600; text-decoration: none; }
.link-primary:hover { color: #4f46e5; text-decoration: underline; }

.link-back { color: #9ca3af; font-size: 0.875rem; text-decoration: none; transition: color 0.2s; }
.link-back:hover { color: #6366f1; }

@media (max-width: 768px) {
  .login-left { display: none; }
  .login-right { background: linear-gradient(135deg, #0f172a, #1e1b4b); }
  .login-card { box-shadow: 0 20px 60px rgba(0,0,0,.3); }
}
</style>
