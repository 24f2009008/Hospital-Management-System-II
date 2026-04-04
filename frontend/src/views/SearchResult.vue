<template>
  <div class="container-fluid">
    <div class="page-header mb-4">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-search-plus me-2" style="color: var(--primary);"></i>
            Search Results
          </h2>
          <p class="text-muted mb-0">
            Results for "<strong>{{ query }}</strong>"
          </p>
        </div>
          <router-link :to="isAdmin ? '/admin/search' : '/doctor/search'" class="btn btn-primary">
            <i class="fas fa-search me-2"></i> New Search
          </router-link>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="fas fa-list me-2"></i>Results</h5>
          <span class="badge bg-primary">
            {{ doctors.length + patients.length + appointments.length }} Found
          </span>
        </div>
      </div>

      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-3">Searching...</p>
        </div>

        <div v-else-if="doctors.length === 0 && patients.length === 0 && appointments.length === 0" class="text-center py-5 text-muted">
          <i class="fas fa-search fa-4x mb-3 opacity-25"></i>
          <h5>No results found</h5>
          <p>Try adjusting your search criteria.</p>
          <router-link to="/admin/search" class="btn btn-primary mt-3">
            <i class="fas fa-search me-2"></i>Try Another Search
          </router-link>
        </div>

        <div v-else>
          <!-- Doctors Section -->
          <div v-if="doctors.length" class="mb-4">
            <div class="px-3 pt-3 pb-2 bg-light">
              <h6 class="mb-0"><i class="fas fa-user-md me-2"></i>Doctors ({{ doctors.length }})</h6>
            </div>
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Username</th>
                    <th class="d-none d-lg-table-cell">Department</th>
                    <th class="d-none d-md-table-cell">Specialization</th>
                    <th class="d-none d-md-table-cell">Experience</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="doctor in doctors" :key="doctor.id">
                    <td><strong>DR{{ String(doctor.id).padStart(3, '0') }}</strong></td>
                    <td>{{ doctor.name }}</td>
                    <td>{{ doctor.username }}</td>
                    <td class="d-none d-lg-table-cell">{{ doctor.department }}</td>
                    <td class="d-none d-md-table-cell">{{ doctor.specialization }}</td>
                    <td class="d-none d-md-table-cell">{{ doctor.experience }} years</td>
                    <td>
                      <span class="badge" :class="doctor.status === 'active' ? 'bg-success' : 'bg-secondary'">
                        {{ doctor.status ? doctor.status.charAt(0).toUpperCase() + doctor.status.slice(1) : 'Unknown' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Patients Section -->
          <div v-if="patients.length" class="mb-4">
            <div class="px-3 pt-3 pb-2 bg-light">
              <h6 class="mb-0"><i class="fas fa-user me-2"></i>Patients ({{ patients.length }})</h6>
            </div>
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Patient ID</th>
                    <th>Name</th>
                    <th>Username</th>
                    <th class="d-none d-md-table-cell">Gender</th>
                    <th class="d-none d-lg-table-cell">Blood Group</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="patient in patients" :key="patient.id">
                    <td><strong>PAT{{ String(patient.id).padStart(6, '0') }}</strong></td>
                    <td>{{ patient.name }}</td>
                    <td>{{ patient.username }}</td>
                    <td class="d-none d-md-table-cell">{{ patient.gender }}</td>
                    <td class="d-none d-lg-table-cell">{{ patient.blood_group }}</td>
                    <td>
                      <span class="badge" :class="patient.is_active ? 'bg-success' : 'bg-secondary'">
                        {{ patient.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Appointments Section -->
          <div v-if="appointments.length">
            <div class="px-3 pt-3 pb-2 bg-light">
              <h6 class="mb-0"><i class="fas fa-calendar-check me-2"></i>Appointments ({{ appointments.length }})</h6>
            </div>
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Appointment #</th>
                    <th>Patient</th>
                    <th class="d-none d-md-table-cell">Doctor</th>
                    <th class="d-none d-lg-table-cell">Date</th>
                    <th class="d-none d-md-table-cell">Time</th>
                    <th>Status</th>
                    <th class="d-none d-xl-table-cell">Reason</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="apt in appointments" :key="apt.id">
                    <td><strong>{{ apt.appointment_number }}</strong></td>
                    <td>{{ apt.patient_name }}</td>
                    <td class="d-none d-md-table-cell">{{ apt.doctor_name }}</td>
                    <td class="d-none d-lg-table-cell">{{ apt.date }}</td>
                    <td class="d-none d-md-table-cell">{{ apt.time }}</td>
                    <td>
                      <span class="badge" :class="getStatusClass(apt.status)">
                        {{ apt.status }}
                      </span>
                    </td>
                    <td class="d-none d-xl-table-cell">{{ apt.reason }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const isAdmin = computed(() => localStorage.getItem('role') === 'admin')

const query = ref('')
const doctors = ref([])
const patients = ref([])
const appointments = ref([])
const loading = ref(true)
const error = ref('')

const getStatusClass = (status) => {
  const map = {
    'Booked': 'bg-primary',
    'Completed': 'bg-success',
    'Cancelled': 'bg-danger',
    'In Progress': 'bg-warning'
  }
  return map[status] || 'bg-secondary'
}

const API_BASE = 'http://127.0.0.1:5000'

const loadResults = async () => {
  query.value = route.query.q || ''
  loading.value = true
  error.value = ''

  if (!query.value) {
    loading.value = false
    return
  }

  try {
    console.log('Searching for:', query.value)
    const role = localStorage.getItem('role')
    const endpoint = role === 'admin'
      ? '/api/admin/search'
      : '/api/doctor/search'

    const url = `${API_BASE}${endpoint}?q=${encodeURIComponent(query.value)}`
    console.log('URL:', url)
    
    const res = await fetch(url, { credentials: 'include' })
    console.log('Response status:', res.status)
    
    const text = await res.text()
    console.log('Response text:', text)
    
    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`)
    }
    
    const data = JSON.parse(text)
    console.log('Search response:', data)

    if (data.success) {
      doctors.value = data.doctors || []
      patients.value = data.patients || []
      appointments.value = data.appointments || []
    } else {
      error.value = data.message || 'Search failed'
    }
  } catch (err) {
    console.error('Search failed', err)
    error.value = 'Search failed: ' + err.message
  } finally {
    loading.value = false
  }
}

onMounted(loadResults)
watch(() => route.query.q, loadResults)
</script>