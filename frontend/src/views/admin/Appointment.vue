<template>
  <div class="container-fluid">
    <!-- Page Header -->
    <div class="page-header mb-4">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-calendar-check me-2" style="color: var(--primary);"></i>
            Manage Appointments
          </h2>
          <p class="text-muted mb-0">View and manage all appointments in the system</p>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0"><i class="fas fa-filter me-2"></i>Filter Appointments</h5>
      </div>
      <div class="card-body p-4">
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Status</label>
            <select v-model="filterStatus" @change="loadAppointments" class="form-select">
              <option value="all">All Status</option>
              <option value="Booked">Booked</option>
              <option value="Completed">Completed</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Date Range</label>
            <select v-model="filterDate" @change="loadAppointments" class="form-select">
              <option value="all">All Dates</option>
              <option value="upcoming">Upcoming</option>
              <option value="past">Past</option>
            </select>
          </div>
          <div class="col-md-4 d-flex align-items-end">
            <button @click="resetFilters" class="btn btn-outline-secondary w-100">
              <i class="fas fa-redo me-2"></i>Reset Filters
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Appointments Table -->
    <div class="card">
      <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="mb-0">
            <i class="fas fa-calendar-check me-2"></i>All Appointments
          </h5>
          <span class="badge bg-primary">{{ appointments.length }} Total</span>
        </div>
      </div>

      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-3">Loading appointments...</p>
        </div>

        <div v-else-if="error" class="alert alert-danger m-3">
          {{ error }}
          <button class="btn btn-sm btn-outline-danger ms-3" @click="loadAppointments">Retry</button>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Appointment #</th>
                <th>Patient</th>
                <th class="d-none d-xl-table-cell">Patient ID</th>
                <th class="d-none d-md-table-cell">Doctor</th>
                <th class="d-none d-lg-table-cell">Date</th>
                <th class="d-none d-md-table-cell">Time</th>
                <th>Status</th>
                <th class="d-none d-xl-table-cell">Reason</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="apt in appointments" :key="apt.id">
                <tr>
                  <td><strong>{{ apt.appointment_number || `APT${String(apt.id).padStart(8, '0')}` }}</strong></td>
                  <td>{{ apt.patient_name }}</td>
                  <td class="d-none d-xl-table-cell">{{ apt.patient_id ? `PAT${String(apt.patient_id).padStart(6, '0')}` : '-' }}</td>
                  <td class="d-none d-md-table-cell">{{ apt.doctor_name }}</td>
                  <td class="d-none d-lg-table-cell">{{ apt.date }}</td>
                  <td class="d-none d-md-table-cell">{{ apt.time }}</td>
                  <td>
                    <span class="badge" :class="getStatusClass(apt.status)">
                      {{ apt.status }}
                    </span>
                  </td>
                  <td class="d-none d-xl-table-cell">
                    <small>{{ truncateText(apt.reason, 30) }}</small>
                  </td>
                  <td>
                    <button @click="viewAppointment(apt)" class="btn btn-sm btn-outline-info">
                      <i class="fas fa-eye"></i>
                    </button>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && !error && appointments.length === 0" class="text-center text-muted py-5">
          <i class="fas fa-calendar-check fa-4x mb-3 opacity-25"></i>
          <h5>No Appointments Found</h5>
          <p>No appointments match your current filters.</p>
          <button @click="resetFilters" class="btn btn-primary mt-3">
            <i class="fas fa-redo me-2"></i>View All Appointments
          </button>
        </div>
      </div>
    </div>

    <!-- Appointment Details Modal -->
    <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-info-circle me-2"></i>Appointment Details
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <!-- Patient Information -->
              <div class="col-md-6">
                <h6 class="text-muted mb-3">Patient Information</h6>
                <table class="table table-sm table-borderless">
                  <tr>
                    <th width="40%">Name:</th>
                    <td>{{ selectedAppointment?.patient_name }}</td>
                  </tr>
                  <tr v-if="selectedAppointment?.patient_id">
                    <th>Patient ID:</th>
                    <td>PAT{{ String(selectedAppointment?.patient_id).padStart(6, '0') }}</td>
                  </tr>
                </table>
              </div>
              
              <!-- Doctor Information -->
              <div class="col-md-6">
                <h6 class="text-muted mb-3">Doctor Information</h6>
                <table class="table table-sm table-borderless">
                  <tr>
                    <th width="40%">Name:</th>
                    <td>{{ selectedAppointment?.doctor_name }}</td>
                  </tr>
                </table>
              </div>
            </div>

            <hr>

            <!-- Appointment Information -->
            <div class="row">
              <div class="col-12">
                <h6 class="text-muted mb-3">Appointment Information</h6>
                <table class="table table-sm table-borderless">
                  <tr>
                    <th width="20%">Appointment #:</th>
                    <td>{{ selectedAppointment?.appointment_number || `APT${String(selectedAppointment?.id).padStart(8, '0')}` }}</td>
                  </tr>
                  <tr>
                    <th>Date & Time:</th>
                    <td>{{ selectedAppointment?.date }} at {{ selectedAppointment?.time }}</td>
                  </tr>
                  <tr>
                    <th>Status:</th>
                    <td>
                      <span class="badge" :class="getStatusClass(selectedAppointment?.status)">
                        {{ selectedAppointment?.status }}
                      </span>
                    </td>
                  </tr>
                  <tr>
                    <th>Reason for Visit:</th>
                    <td>{{ selectedAppointment?.reason || 'N/A' }}</td>
                  </tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:5000'

const appointments = ref([])
const loading = ref(false)
const error = ref(null)

const filterStatus = ref('all')
const filterDate = ref('all')

const showModal = ref(false)
const selectedAppointment = ref(null)

const loadAppointments = async () => {
  loading.value = true
  error.value = null

  try {
    const params = new URLSearchParams()
    if (filterStatus.value !== 'all') params.append('status', filterStatus.value)
    if (filterDate.value !== 'all') params.append('date', filterDate.value)

    const url = `${API_BASE}/api/admin/appointments${params.toString() ? '?' + params.toString() : ''}`
    console.log('Loading appointments from:', url)

    const res = await fetch(url, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    console.log('Response status:', res.status)
    const data = await res.json()
    console.log('Response data:', data)

    if (!res.ok || !data.success) {
      throw new Error(data.message || `Failed to load (status ${res.status})`)
    }

    appointments.value = data.appointments || []
  } catch (err) {
    error.value = err.message
    console.error('Error loading appointments:', err)
  } finally {
    loading.value = false
  }
}

const getStatusClass = (status) => {
  switch (status?.toLowerCase()) {
    case 'booked': return 'bg-warning text-dark'
    case 'completed': return 'bg-success'
    case 'cancelled': return 'bg-danger'
    default: return 'bg-secondary'
  }
}

const truncateText = (text, maxLength) => {
  if (!text) return 'N/A'
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const resetFilters = () => {
  filterStatus.value = 'all'
  filterDate.value = 'all'
  loadAppointments()
}

const viewAppointment = (appointment) => {
  selectedAppointment.value = appointment
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedAppointment.value = null
}

onMounted(() => {
  loadAppointments()
})
</script>

<style scoped>
.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 1.25rem;
}

.table th {
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
  border-bottom: 2px solid #e5e7eb;
  padding: 1rem;
}

.table td {
  padding: 0.875rem 1rem;
  vertical-align: middle;
}

.badge {
  font-weight: 500;
  padding: 0.5em 0.75em;
}

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
  max-width: 800px;
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
</style>