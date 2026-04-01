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
  <div class="register-wrapper">
    <div class="register-card">
      <h3 class="text-center mb-4 fw-bold text-primary">
        Patient Registration
      </h3>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleRegister" novalidate>

        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input v-model="name" type="text" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Gender</label>
          <select v-model="gender" class="form-select" required>
            <option value="">Select gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">Date of Birth</label>
          <input v-model="dob" type="date" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Blood Group</label>
          <input v-model="bloodGrp" type="text" class="form-control" placeholder="e.g. O+" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Address</label>
          <textarea v-model="address" class="form-control" rows="2" required></textarea>
        </div>

        <button :disabled="loading" type="submit" class="btn btn-primary w-100">
          {{ loading ? 'Creating...' : 'Create Patient Account' }}
        </button>
      </form>

      <hr class="my-4">

      <p class="text-center text-muted">
        Already have an account?
        <router-link to="/login" class="fw-semibold text-decoration-none">
          Sign In
        </router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-wrapper {
  min-height: 125vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, #e3f2fd, #f8f9fa);
}

.register-card {
  background: #fff;
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 600px;
}

.btn-primary {
  background-color: #0d6efd;
  border: none;
  padding: 0.75rem;
  font-weight: 600;
  border-radius: 0.5rem;
  transition: all 0.3s;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
}
</style>