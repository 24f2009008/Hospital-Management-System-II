<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const name = ref('')
const username = ref('')
const password = ref('')
const gender = ref('')
const dob = ref('')
const bloodGrp = ref('')
const address = ref('')
const errorMessage = ref('')
const loading = ref(false)

const handleRegister = async () => {
  errorMessage.value = ''

  if (
    !name.value ||
    !username.value ||
    !password.value ||
    !gender.value ||
    !dob.value ||
    !bloodGrp.value ||
    !address.value
  ) {
    errorMessage.value = 'Please fill all fields'
    return
  }

  loading.value = true

  try {
    const response = await fetch('http://127.0.0.1:5000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: name.value,
        username: username.value,
        password: password.value,
        gender: gender.value,
        dob: dob.value,
        bloodGrp: bloodGrp.value,
        address: address.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      errorMessage.value = data.message || 'Registration failed'
      return
    }

    if (data.success) {
      alert('Registration successful!')
      router.push('/login')
    } else {
      errorMessage.value = data.message
    }

  } catch (error) {
    console.error('Register error:', error)
    errorMessage.value = 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <div class="logo-icon">
            <i class="fas fa-user-plus"></i>
          </div>
          <h2>Patient Registration</h2>
          <p class="text-muted">Create your account</p>
        </div>

        <div v-if="errorMessage" class="alert alert-danger">
          <i class="fas fa-exclamation-circle me-2"></i>
          {{ errorMessage }}
        </div>

        <form @submit.prevent="handleRegister" novalidate>
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label class="form-label">Full Name</label>
                <div class="input-group">
                  <span class="input-group-text"><i class="fas fa-user"></i></span>
                  <input v-model="name" type="text" class="form-control" placeholder="Enter full name" required>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label class="form-label">Username</label>
                <div class="input-group">
                  <span class="input-group-text"><i class="fas fa-at"></i></span>
                  <input v-model="username" type="text" class="form-control" placeholder="Choose username" required>
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <div class="input-group">
              <span class="input-group-text"><i class="fas fa-lock"></i></span>
              <input v-model="password" type="password" class="form-control" placeholder="Create password" required>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label class="form-label">Gender</label>
                <select v-model="gender" class="form-select" required>
                  <option value="">Select gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label class="form-label">Date of Birth</label>
                <input v-model="dob" type="date" class="form-control" required>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label class="form-label">Blood Group</label>
                <select v-model="bloodGrp" class="form-select" required>
                  <option value="">Select blood group</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                </select>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label class="form-label">Address</label>
                <textarea v-model="address" class="form-control" rows="1" placeholder="Enter address" required></textarea>
              </div>
            </div>
          </div>

          <button :disabled="loading" type="submit" class="btn btn-primary w-100 btn-register">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <span v-else><i class="fas fa-user-plus me-2"></i></span>
            {{ loading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>

        <div class="register-footer">
          <p class="mb-0">Already have an account? 
            <router-link to="/login" class="text-primary fw-semibold">Sign In</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  padding: 2rem;
}

.register-container {
  width: 100%;
  max-width: 600px;
}

.register-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 2.5rem;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}

.logo-icon i {
  font-size: 1.5rem;
  color: white;
}

.register-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.25rem;
}

.register-header p {
  color: #6b7280;
  margin: 0;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  display: block;
}

.input-group {
  border-radius: 12px;
  overflow: hidden;
}

.input-group-text {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-right: none;
  color: #9ca3af;
  padding: 0.625rem 1rem;
}

.form-control, .form-select {
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.alert-danger {
  background: #fef2f2;
  border: none;
  border-radius: 12px;
  color: #dc2626;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  margin-bottom: 1.25rem;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border: none;
  border-radius: 12px;
  padding: 0.875rem 1.5rem;
  font-weight: 600;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.register-footer {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
  text-align: center;
  color: #6b7280;
}

.text-primary {
  color: #6366f1 !important;
}
</style>
