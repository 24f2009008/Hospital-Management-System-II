<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-calendar-alt me-2"></i>My Appointments
          </h2>
          <p class="text-muted mb-0">View and manage your appointments</p>
        </div>
        <router-link to="/patient/appointments/book" class="btn btn-primary">
          <i class="fas fa-plus me-2"></i>Book New
        </router-link>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tab-pills mb-4">
      <button class="tab-pill" :class="{ active: activeTab === 'upcoming' }" @click="activeTab = 'upcoming'">
        <i class="fas fa-clock me-2"></i>Upcoming
        <span class="tab-count">{{ upcomingAppointments.length }}</span>
      </button>
      <button class="tab-pill" :class="{ active: activeTab === 'past' }" @click="activeTab = 'past'">
        <i class="fas fa-history me-2"></i>Past
        <span class="tab-count">{{ pastAppointments.length }}</span>
      </button>
    </div>

    <!-- Upcoming -->
    <div v-if="activeTab === 'upcoming'" class="card">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>Doctor</th>
                <th>Department</th>
                <th>Date &amp; Time</th>
                <th>Reason</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in upcomingAppointments" :key="apt.id">
                <td>
                  <div class="fw-semibold">{{ apt.doctor_name }}</div>
                  <small class="text-muted">{{ apt.specialization }}</small>
                </td>
                <td>{{ apt.department }}</td>
                <td>
                  <div>{{ apt.date }}</div>
                  <small class="text-muted">{{ apt.time }}</small>
                </td>
                <td>{{ apt.reason || '—' }}</td>
                <td>
                  <span class="badge" :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-danger" @click="cancelAppointment(apt.id)">
                    <i class="fas fa-times me-1"></i>Cancel
                  </button>
                </td>
              </tr>
              <tr v-if="upcomingAppointments.length === 0">
                <td colspan="6" class="text-center py-5 text-muted">
                  <i class="fas fa-calendar-times fa-3x mb-3 opacity-25 d-block"></i>
                  No upcoming appointments.
                  <router-link to="/patient/appointments/book" class="ms-1 text-primary">Book one now</router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Past -->
    <div v-if="activeTab === 'past'" class="card">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>Doctor</th>
                <th>Department</th>
                <th>Date &amp; Time</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in pastAppointments" :key="apt.id">
                <td>
                  <div class="fw-semibold">{{ apt.doctor_name }}</div>
                  <small class="text-muted">{{ apt.specialization }}</small>
                </td>
                <td>{{ apt.department }}</td>
                <td>
                  <div>{{ apt.date }}</div>
                  <small class="text-muted">{{ apt.time }}</small>
                </td>
                <td>
                  <span class="badge" :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-primary" @click="viewDetails(apt)">
                    <i class="fas fa-eye me-1"></i>Details
                  </button>
                </td>
              </tr>
              <tr v-if="pastAppointments.length === 0">
                <td colspan="5" class="text-center py-5 text-muted">
                  <i class="fas fa-history fa-3x mb-3 opacity-25 d-block"></i>
                  No past appointments
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title"><i class="fas fa-info-circle me-2"></i>Appointment Details</h5>
            <button type="button" class="btn-close" @click="showModal = false"></button>
          </div>
          <div class="modal-body" v-if="selectedAppointment">
            <div class="detail-row">
              <span class="detail-label">Doctor</span>
              <span>{{ selectedAppointment.doctor_name }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Specialization</span>
              <span>{{ selectedAppointment.specialization || '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Date</span>
              <span>{{ selectedAppointment.date }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Time</span>
              <span>{{ selectedAppointment.time }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Status</span>
              <span class="badge" :class="getStatusClass(selectedAppointment.status)">{{ selectedAppointment.status }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Reason</span>
              <span>{{ selectedAppointment.reason || '—' }}</span>
            </div>
            <div v-if="selectedAppointment.treatment" class="mt-3">
              <div class="treatment-box">
                <h6 class="fw-semibold mb-3"><i class="fas fa-file-medical me-2 text-primary"></i>Treatment Details</h6>
                <div class="detail-row">
                  <span class="detail-label">Diagnosis</span>
                  <span>{{ selectedAppointment.treatment.diagnosis }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Prescription</span>
                  <span>{{ selectedAppointment.treatment.prescription }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Notes</span>
                  <span>{{ selectedAppointment.treatment.notes }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:5000'
const appointments = ref([])
const selectedAppointment = ref(null)
const showModal = ref(false)
const activeTab = ref('upcoming')

const upcomingAppointments = computed(() => appointments.value.filter(a => a.status === 'Booked'))
const pastAppointments = computed(() => appointments.value.filter(a => a.status !== 'Booked'))

const getStatusClass = (status) => {
  const map = { 'Completed': 'bg-success', 'Cancelled': 'bg-danger', 'Booked': 'bg-warning text-dark' }
  return map[status] || 'bg-secondary'
}

const loadAppointments = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/patient/appointments`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) appointments.value = data.appointments || []
  } catch (e) {
    console.error('Failed to load appointments:', e)
  }
}

const cancelAppointment = async (id) => {
  if (!confirm('Cancel this appointment?')) return
  try {
    const res = await fetch(`${API_BASE}/api/patient/appointments/${id}/cancel`, {
      method: 'PUT', credentials: 'include'
    })
    const data = await res.json()
    if (data.success) { alert('Appointment cancelled'); loadAppointments() }
    else alert(data.message || 'Failed to cancel')
  } catch (e) {
    console.error(e)
  }
}

const viewDetails = async (apt) => {
  selectedAppointment.value = apt
  showModal.value = true
  try {
    const res = await fetch(`${API_BASE}/api/patient/appointments/${apt.id}/details`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) selectedAppointment.value = data.appointment
  } catch (e) {
    console.error(e)
  }
}

onMounted(loadAppointments)
</script>

<style scoped>
.tab-pills { display: flex; gap: 0.5rem; }

.tab-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.25rem;
  border-radius: 10px;
  border: 1.5px solid #e5e7eb;
  background: white;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-pill:hover { border-color: #6366f1; color: #6366f1; }

.tab-pill.active {
  background: #6366f1;
  border-color: #6366f1;
  color: white;
  box-shadow: 0 4px 12px rgba(99,102,241,.3);
}

.tab-count {
  background: rgba(255,255,255,.25);
  border-radius: 20px;
  padding: 0.1rem 0.5rem;
  font-size: 0.75rem;
}

.tab-pill:not(.active) .tab-count { background: #f3f4f6; color: #374151; }

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0.6rem 0;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.9rem;
}

.detail-row:last-child { border-bottom: none; }

.detail-label { color: #6b7280; font-weight: 600; font-size: 0.8rem; flex-shrink: 0; margin-right: 1rem; }

.treatment-box {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
}
</style>
