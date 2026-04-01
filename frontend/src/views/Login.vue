<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'   // Make sure path is correct

const authStore = useAuthStore()
const router = useRouter()

// Reactive variables
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

// Login Function
const handleLogin = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    const response = await fetch('http://127.0.0.1:5000/api/login', {
      method: 'POST',
      credentials: 'include', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok && data.success) {
      // Store user info in Pinia + localStorage
      authStore.loginSuccess({
        userId: data.user_id,
        role: data.role,
        username: username.value
      })

      // Redirect based on role
      if (data.role === 'admin') {
        router.push('/admin/dashboard')
      } else if (data.role === 'doctor') {
        router.push('/doctor/dashboard')
      } else {
        router.push('/patient/dashboard/')   // default for patient
      }
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
  <div class="login-container">
    <div class="login-card">
      <div class="text-center mb-4">
        <i class="fas fa-hospital fa-3x text-primary mb-3"></i>
        <h2>HMS Hospital</h2>
        <p class="text-muted">Sign in to your account</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input 
            v-model="username" 
            type="text" 
            class="form-control" 
            placeholder="Enter your username"
            required
          >
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input 
            v-model="password" 
            type="password" 
            class="form-control" 
            placeholder="Enter your password"
            required
          >
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="alert alert-danger py-2">
          {{ errorMessage }}
        </div>

        <button 
          type="submit" 
          class="btn btn-primary w-100 py-2 mt-2"
          :disabled="loading"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>


      <div class="text-center mt-4">
        <p>
          Don't have an account? 
          <a href="/register" class="text-primary fw-medium">Register here</a>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .login-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }

  .login-card {
    padding: 2.5rem 2rem;
    border-radius: 16px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    width: 100%;
    max-width: 420px;
  }

  .form-control {
    padding: 12px 15px;
    border-radius: 8px;
  }

  .btn-primary {
    border-radius: 8px;
    font-weight: 600;
  }
</style>