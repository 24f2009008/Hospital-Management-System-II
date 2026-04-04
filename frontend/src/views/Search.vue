<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-search me-2" style="color: var(--primary);"></i>
            Search
          </h2>
          <p class="text-muted mb-0">Search and filter across doctors, patients, and appointments</p>
        </div>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0"><i class="fas fa-filter me-2"></i>Search & Filters</h5>
      </div>
      <div class="card-body p-4">
        <form @submit.prevent="performSearch">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Search Term <span class="text-danger">*</span></label>
              <input
                v-model="searchTerm"
                type="text"
                class="form-control"
                placeholder="Enter name, ID, specialty, appointment number..."
                required
              >
            </div>

            <div class="col-md-3">
              <label class="form-label">Search In</label>
              <select v-model="searchType" class="form-select">
                <option value="all">All</option>
                <option value="doctors">Doctors</option>
                <option value="patients">Patients</option>
                <option value="appointments">Appointments</option>
              </select>
            </div>

            <div class="col-md-3">
              <label class="form-label">Status</label>
              <select v-model="statusFilter" class="form-select">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
          </div>

          <div class="row g-3 mt-2">
            <div class="col-md-3">
              <label class="form-label">Department</label>
              <select v-model="departmentFilter" class="form-select">
                <option value="">All Departments</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                  {{ dept.name }}
                </option>
              </select>
            </div>

            <div class="col-md-3">
              <label class="form-label">Specialization</label>
              <select v-model="specializationFilter" class="form-select">
                <option value="">All Specializations</option>
                <option v-for="spec in specializations" :key="spec" :value="spec">
                  {{ spec }}
                </option>
              </select>
            </div>

            <div class="col-md-3">
              <label class="form-label">Date From</label>
              <input v-model="dateFrom" type="date" class="form-control">
            </div>

            <div class="col-md-3">
              <label class="form-label">Date To</label>
              <input v-model="dateTo" type="date" class="form-control">
            </div>
          </div>

          <div class="row g-3 mt-2">
            <div class="col-md-3">
              <label class="form-label">Gender</label>
              <select v-model="genderFilter" class="form-select">
                <option value="">All Genders</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="col-md-3">
              <label class="form-label">Blood Group</label>
              <select v-model="bloodGroupFilter" class="form-select">
                <option value="">All Blood Groups</option>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
              </select>
            </div>

            <div class="col-md-3">
              <label class="form-label">Appointment Status</label>
              <select v-model="appointmentStatusFilter" class="form-select">
                <option value="">All Appointment Status</option>
                <option value="Booked">Booked</option>
                <option value="Completed">Completed</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>

            <div class="col-md-3">
              <label class="form-label">Doctor</label>
              <select v-model="doctorFilter" class="form-select">
                <option value="">All Doctors</option>
                <option v-for="doc in doctorsList" :key="doc.id" :value="doc.id">
                  {{ doc.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-4">
            <button type="submit" class="btn btn-primary px-4" :disabled="loading">
              <i class="fas fa-search me-2"></i>{{ loading ? 'Searching...' : 'Search' }}
            </button>
            <button type="button" @click="clearForm" class="btn btn-outline-secondary px-4">
              <i class="fas fa-times me-2"></i>Clear
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-md-4">
        <div class="card h-100" style="border-left: 4px solid var(--primary);">
          <div class="card-body">
            <h6 class="fw-bold" style="color: var(--primary);">
              <i class="fas fa-user-md me-2"></i>Doctors
            </h6>
            <ul class="list-unstyled small text-muted mb-0">
              <li><i class="fas fa-check text-success me-2"></i>Search by Name</li>
              <li><i class="fas fa-check text-success me-2"></i>Specialization</li>
              <li><i class="fas fa-check text-success me-2"></i>Department</li>
              <li><i class="fas fa-check text-success me-2"></i>Qualification</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card h-100" style="border-left: 4px solid var(--success);">
          <div class="card-body">
            <h6 class="fw-bold" style="color: var(--success);">
              <i class="fas fa-user me-2"></i>Patients
            </h6>
            <ul class="list-unstyled small text-muted mb-0">
              <li><i class="fas fa-check text-success me-2"></i>Search by Name</li>
              <li><i class="fas fa-check text-success me-2"></i>Gender</li>
              <li><i class="fas fa-check text-success me-2"></i>Blood Group</li>
              <li><i class="fas fa-check text-success me-2"></i>Active Status</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card h-100" style="border-left: 4px solid var(--info);">
          <div class="card-body">
            <h6 class="fw-bold" style="color: var(--info);">
              <i class="fas fa-calendar-check me-2"></i>Appointments
            </h6>
            <ul class="list-unstyled small text-muted mb-0">
              <li><i class="fas fa-check text-success me-2"></i>Appointment Number</li>
              <li><i class="fas fa-check text-success me-2"></i>Patient/Doctor Name</li>
              <li><i class="fas fa-check text-success me-2"></i>Date Range</li>
              <li><i class="fas fa-check text-success me-2"></i>Status</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchTerm = ref('')
const loading = ref(false)
const role = localStorage.getItem('role')

const searchType = ref('all')
const statusFilter = ref('')
const departmentFilter = ref('')
const specializationFilter = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const genderFilter = ref('')
const bloodGroupFilter = ref('')
const appointmentStatusFilter = ref('')
const doctorFilter = ref('')

const departments = ref([])
const specializations = ref([])
const doctorsList = ref([])

const API_BASE = 'http://127.0.0.1:5000'

const loadFilters = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/admin/departments`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      departments.value = data.departments || []
    }
  } catch (e) {
    console.error('Failed to load departments:', e)
  }

  try {
    const res = await fetch(`${API_BASE}/api/admin/doctors`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      doctorsList.value = data.doctors || []
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

onMounted(() => {
  loadFilters()
})

const performSearch = async () => {
  if (!searchTerm.value && !hasActiveFilters()) return

  loading.value = true

  const basePath = role === 'admin'
    ? '/admin/search/results'
    : '/doctor/search/results'

  const query = {
    q: searchTerm.value,
    type: searchType.value,
    status: statusFilter.value,
    department: departmentFilter.value,
    specialization: specializationFilter.value,
    date_from: dateFrom.value,
    date_to: dateTo.value,
    gender: genderFilter.value,
    blood_group: bloodGroupFilter.value,
    appointment_status: appointmentStatusFilter.value,
    doctor: doctorFilter.value
  }

  router.push({
    path: basePath,
    query
  })

  loading.value = false
}

const hasActiveFilters = () => {
  return statusFilter.value || departmentFilter.value || specializationFilter.value ||
    dateFrom.value || dateTo.value || genderFilter.value || bloodGroupFilter.value ||
    appointmentStatusFilter.value || doctorFilter.value
}

const clearForm = () => {
  searchTerm.value = ''
  searchType.value = 'all'
  statusFilter.value = ''
  departmentFilter.value = ''
  specializationFilter.value = ''
  dateFrom.value = ''
  dateTo.value = ''
  genderFilter.value = ''
  bloodGroupFilter.value = ''
  appointmentStatusFilter.value = ''
  doctorFilter.value = ''
}
</script>
