<template>
  <div class="container-fluid">
    <!-- Page Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div class="mb-2 mb-md-0">
          <h2 class="mb-1">
            <i class="fas fa-user-md me-2"></i>
            Find Doctors
          </h2>
          <p class="text-muted mb-0">Browse doctors and their availability</p>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <!-- Filters Sidebar -->
      <div class="col-lg-3">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0"><i class="fas fa-filter me-2"></i>Filters</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Search by Name</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="filters.search" 
                placeholder="Enter doctor name..."
              >
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Department</label>
              <select class="form-select" v-model="filters.department">
                <option value="">All Departments</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.name">
                  {{ dept.name }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Specialization</label>
              <select class="form-select" v-model="filters.specialization">
                <option value="">All Specializations</option>
                <option v-for="spec in specializations" :key="spec" :value="spec">
                  {{ spec }}
                </option>
              </select>
            </div>
            <button class="btn btn-primary w-100" @click="applyFilters">
              <i class="fas fa-search me-2"></i>Apply Filters
            </button>
          </div>
        </div>
      </div>

      <!-- Doctors Grid -->
      <div class="col-lg-9">
        <div class="row g-3">
          <div v-for="doctor in filteredDoctors" :key="doctor.id" class="col-lg-6">
            <div class="card h-100 doctor-card">
              <div class="card-body">
                <div class="d-flex align-items-start mb-3">
                  <div class="doctor-avatar me-3">
                    {{ getInitials(doctor.name) }}
                  </div>
                  <div class="flex-grow-1">
                    <h5 class="card-title mb-1">{{ doctor.name }}</h5>
                    <span class="badge bg-primary-light text-primary">{{ doctor.specialization }}</span>
                  </div>
                </div>
                
                <div class="doctor-info mb-3">
                  <div class="info-item">
                    <i class="fas fa-building me-2"></i>
                    <span>{{ doctor.department }}</span>
                  </div>
                  <div class="info-item">
                    <i class="fas fa-graduation-cap me-2"></i>
                    <span>{{ doctor.qualification || 'N/A' }}</span>
                  </div>
                  <div class="info-item">
                    <i class="fas fa-briefcase me-2"></i>
                    <span>{{ doctor.experience || 0 }} years experience</span>
                  </div>
                </div>
                
                <div class="availability-section mb-3">
                  <small class="text-muted fw-semibold d-block mb-2">
                    <i class="fas fa-calendar-alt me-2"></i>Next 7 Days Availability
                  </small>
                  <div class="d-flex flex-wrap gap-1">
                    <span 
                      v-for="day in doctor.availability" 
                      :key="day.date"
                      class="badge availability-badge"
                      :class="day.available ? 'bg-success' : 'bg-secondary'"
                    >
                      {{ formatShortDate(day.date) }}
                    </span>
                  </div>
                </div>
                
                <router-link 
                  :to="`/patient/appointments/book?doctor_id=${doctor.id}`"
                  class="btn btn-primary w-100"
                >
                  <i class="fas fa-calendar-plus me-2"></i>Book Appointment
                </router-link>
              </div>
            </div>
          </div>
          
          <div v-if="filteredDoctors.length === 0" class="col-12">
            <div class="card">
              <div class="card-body text-center text-muted py-5">
                <i class="fas fa-user-md fa-4x mb-3 opacity-25"></i>
                <p class="mb-0">No doctors found matching your criteria</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:5000'

const doctors = ref([])
const departments = ref([])
const specializations = ref([])
const filters = ref({
  search: '',
  department: '',
  specialization: ''
})

const filteredDoctors = computed(() => {
  let result = doctors.value
  if (filters.value.search) {
    const query = filters.value.search.toLowerCase()
    result = result.filter(d => d.name.toLowerCase().includes(query))
  }
  if (filters.value.department) {
    result = result.filter(d => d.department === filters.value.department)
  }
  if (filters.value.specialization) {
    result = result.filter(d => d.specialization === filters.value.specialization)
  }
  return result
})

const getInitials = (name) => {
  return name?.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'DR'
}

const formatShortDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
}

const loadDoctors = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/patient/doctors`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      doctors.value = data.doctors || []
      const specs = new Set()
      data.doctors.forEach(d => {
        if (d.specialization) specs.add(d.specialization)
      })
      specializations.value = Array.from(specs)
    }
  } catch (e) {
    console.error('Failed to load doctors:', e)
  }
}

const loadDepartments = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/admin/departments/list`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      departments.value = data.departments || []
    }
  } catch (e) {
    console.error('Failed to load departments:', e)
  }
}

const applyFilters = () => {
  // Filters applied via computed property
}

onMounted(() => {
  loadDoctors()
  loadDepartments()
})
</script>

<style scoped>
.page-header {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.page-header h2 {
  color: var(--gray-900, #111827);
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.page-header h2 i {
  color: var(--primary, #6366f1);
}

.page-header p {
  color: var(--gray-600, #4b5563);
  margin: 0;
}

.card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
  background: white;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  background: white;
  border-bottom: 1px solid var(--gray-200, #e5e7eb);
  padding: 1.25rem 1.5rem;
  font-weight: 600;
  color: var(--gray-900, #111827);
}

.card-body {
  padding: 1.5rem;
}

.form-control, .form-select {
  border-radius: 10px;
  border: 1px solid var(--gray-300, #d1d5db);
  padding: 0.625rem 1rem;
  transition: all 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: var(--primary, #6366f1);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.btn {
  border-radius: 10px;
  padding: 0.625rem 1.25rem;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.doctor-card {
  position: relative;
  overflow: hidden;
}

.doctor-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
}

.doctor-avatar {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.125rem;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.card-title {
  color: var(--gray-900, #111827);
  font-weight: 600;
  font-size: 1.125rem;
}

.badge {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.75rem;
  letter-spacing: 0.025em;
}

.bg-primary-light {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
}

.doctor-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  color: var(--gray-600, #4b5563);
  font-size: 0.875rem;
}

.info-item i {
  width: 20px;
  color: var(--gray-400, #9ca3af);
}

.availability-badge {
  font-size: 0.7rem;
  padding: 0.25rem 0.5rem;
}
</style>
