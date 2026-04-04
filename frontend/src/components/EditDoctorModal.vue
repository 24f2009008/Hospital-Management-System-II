<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-user-edit me-2"></i>Edit Doctor
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
          </div>

          <form @submit.prevent="submitForm">
            <div class="row g-3">
              <!-- Personal Information -->
              <div class="col-12">
                <h6 class="text-muted mb-3">Personal Information</h6>
              </div>
              
              <div class="col-md-6">
                <label class="form-label">Full Name</label>
                <input 
                  v-model="form.name" 
                  type="text" 
                  class="form-control" 
                  placeholder="Dr. John Doe"
                >
              </div>

              <div class="col-md-6">
                <label class="form-label">Doctor ID</label>
                <input 
                  :value="`DR${String(doctor.id).padStart(3, '0')}`"
                  type="text" 
                  class="form-control" 
                  disabled
                >
              </div>

              <!-- Professional Information -->
              <div class="col-12 mt-4">
                <h6 class="text-muted mb-3">Professional Information</h6>
              </div>

              <div class="col-md-6">
                <label class="form-label">Department</label>
                <select v-model="form.department" class="form-select">
                  <option value="">Select Department</option>
                  <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                    {{ dept.name }}
                  </option>
                </select>
              </div>

              <div class="col-md-6">
                <label class="form-label">Specialization</label>
                <input 
                  v-model="form.specialization" 
                  type="text" 
                  class="form-control" 
                  placeholder="Cardiology, Neurology, etc."
                >
              </div>

              <div class="col-md-6">
                <label class="form-label">Qualification</label>
                <input 
                  v-model="form.qualification" 
                  type="text" 
                  class="form-control" 
                  placeholder="MBBS, MD, etc."
                >
              </div>

              <div class="col-md-6">
                <label class="form-label">Experience (years)</label>
                <input 
                  v-model="form.experience" 
                  type="number" 
                  class="form-control" 
                  placeholder="5"
                  min="0"
                >
              </div>

              <!-- Current Info Display -->
              <div class="col-12 mt-4">
                <h6 class="text-muted mb-3">Current Information</h6>
                <div class="row">
                  <div class="col-md-4">
                    <small class="text-muted">License Number</small>
                    <p class="mb-2">{{ doctor.license_number || 'N/A' }}</p>
                  </div>
                  <div class="col-md-4">
                    <small class="text-muted">Gender</small>
                    <p class="mb-2">{{ doctor.gender || 'N/A' }}</p>
                  </div>
                  <div class="col-md-4">
                    <small class="text-muted">Username</small>
                    <p class="mb-2">{{ doctor.username || 'N/A' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            Cancel
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="submitForm"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const props = defineProps({
  doctor: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'updated'])

const API_BASE = 'http://127.0.0.1:5000'

const loading = ref(false)
const errorMessage = ref('')
const departments = ref([])

const form = reactive({
  name: props.doctor.name || '',
  department: '',
  specialization: props.doctor.specialization || '',
  qualification: props.doctor.qualification || '',
  experience: props.doctor.experience || 0
})

const loadDepartments = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/admin/departments`, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await res.json()

    if (data.success) {
      departments.value = data.departments || []
    }
  } catch (err) {
    console.error('Error loading departments:', err)
  }
}

const submitForm = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const res = await fetch(`${API_BASE}/api/admin/doctors/${props.doctor.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: form.name,
        department: form.department,
        specialization: form.specialization,
        qualification: form.qualification,
        experience: form.experience
      })
    })

    const data = await res.json()

    if (data.success) {
      emit('updated')
    } else {
      errorMessage.value = data.message || 'Failed to update doctor'
    }
  } catch (err) {
    console.error('Error updating doctor:', err)
    errorMessage.value = 'Server error. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDepartments()
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 1rem;
}

.modal-dialog {
  width: 100%;
  max-width: 700px;
  margin: 0;
}

.modal-content {
  border: none;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  border-bottom: 1px solid #e5e7eb;
  padding: 1.25rem 1.5rem;
}

.modal-body {
  padding: 1.5rem;
  max-height: 70vh;
  overflow-y: auto;
}

.modal-footer {
  border-top: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
}

.form-label {
  font-weight: 500;
  font-size: 0.9rem;
}

h6 {
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>