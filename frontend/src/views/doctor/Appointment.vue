<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-calendar-check me-2"></i>My Appointments
          </h2>
          <p class="text-muted mb-0">View and manage your appointments</p>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
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
          <div class="col-md-4">
            <button @click="resetFilters" class="btn btn-outline-secondary w-100">
              <i class="fas fa-redo me-2"></i>Reset
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0"><i class="fas fa-list me-2"></i>Appointments</h5>
        <span class="badge bg-primary">{{ appointments.length }} Total</span>
      </div>
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border" role="status"></div>
          <p class="mt-3 text-muted">Loading...</p>
        </div>

        <div v-else-if="error" class="alert alert-danger m-3">
          {{ error }}
          <button class="btn btn-sm btn-outline-danger ms-3" @click="loadAppointments">Retry</button>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>Appt #</th>
                <th>Patient</th>
                <th>Date &amp; Time</th>
                <th>Status</th>
                <th>Reason</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in appointments" :key="apt.id">
                <td><strong>{{ apt.appointment_number }}</strong></td>
                <td>{{ apt.patient_name }}</td>
                <td>
                  <div>{{ apt.date }}</div>
                  <small class="text-muted">{{ apt.time }}</small>
                </td>
                <td>
                  <span class="badge" :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                </td>
                <td><small>{{ truncateText(apt.reason, 30) }}</small></td>
                <td>
                  <div class="d-flex gap-1">
                    <button @click="viewAppointment(apt)" class="btn btn-sm btn-outline-info" title="View">
                      <i class="fas fa-eye"></i>
                    </button>
                    <button v-if="apt.status === 'Booked'"
                      @click="markComplete(apt.id)" class="btn btn-sm btn-outline-success" title="Mark Complete">
                      <i class="fas fa-check"></i>
                    </button>
                    <button v-if="apt.status === 'Booked'"
                      @click="markCancel(apt.id)" class="btn btn-sm btn-outline-danger" title="Cancel">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!loading && appointments.length === 0">
                <td colspan="6" class="text-center py-5 text-muted">
                  <i class="fas fa-calendar-check fa-3x mb-3 opacity-25 d-block"></i>
                  No appointments found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title"><i class="fas fa-info-circle me-2"></i>Appointment Details</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body" v-if="selectedAppointment">
            <div class="row g-3">
              <div class="col-md-6">
                <div class="detail-group">
                  <label>Patient</label>
                  <p>{{ selectedAppointment.patient_name }}</p>
                </div>
                <div class="detail-group">
                  <label>Date &amp; Time</label>
                  <p>{{ selectedAppointment.date }} at {{ selectedAppointment.time }}</p>
                </div>
              </div>
              <div class="col-md-6">
                <div class="detail-group">
                  <label>Status</label>
                  <p><span class="badge" :class="getStatusClass(selectedAppointment.status)">{{ selectedAppointment.status }}</span></p>
                </div>
                <div class="detail-group">
                  <label>Reason</label>
                  <p>{{ selectedAppointment.reason || '—' }}</p>
                </div>
              </div>
            </div>

            <!-- Diagnose form for Booked appointments -->
            <div v-if="selectedAppointment.status === 'Booked'" class="mt-4">
              <hr>
              <h6 class="fw-semibold mb-3"><i class="fas fa-stethoscope me-2 text-primary"></i>Add Diagnosis &amp; Treatment</h6>
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Diagnosis <span class="text-danger">*</span></label>
                  <input type="text" class="form-control" v-model="diagnoseForm.diagnosis" placeholder="Enter diagnosis">
                </div>
                <div class="col-md-6">
                  <label class="form-label">Follow-up Date</label>
                  <input type="date" class="form-control" v-model="diagnoseForm.next_visit_date">
                </div>
                <div class="col-12">
                  <label class="form-label">Prescription</label>
                  <textarea class="form-control" v-model="diagnoseForm.prescription" rows="2" placeholder="Medications..."></textarea>
                </div>
                <div class="col-12">
                  <label class="form-label">Notes</label>
                  <textarea class="form-control" v-model="diagnoseForm.notes" rows="2" placeholder="Additional notes..."></textarea>
                </div>
              </div>
              <div class="mt-3">
                <button class="btn btn-primary" @click="saveDiagnosis" :disabled="saving">
                  <i class="fas fa-save me-2"></i>{{ saving ? 'Saving...' : 'Save &amp; Complete' }}
                </button>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Close</button>
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
const saving = ref(false)

const diagnoseForm = ref({ diagnosis: '', prescription: '', notes: '', next_visit_date: '' })

const loadAppointments = async () => {
  loading.value = true
  error.value = null
  try {
    const params = new URLSearchParams()
    if (filterStatus.value !== 'all') params.append('status', filterStatus.value)
    if (filterDate.value !== 'all') params.append('date', filterDate.value)
    const res = await fetch(`${API_BASE}/api/doctor/appointments?${params}`, {
      credentials: 'include'
    })
    const data = await res.json()
    if (!data.success) throw new Error(data.message)
    appointments.value = data.appointments || []
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const getStatusClass = (s) => ({
  'Booked': 'bg-warning text-dark',
  'Completed': 'bg-success',
  'Cancelled': 'bg-danger'
}[s] || 'bg-secondary')

const truncateText = (t, n) => !t ? '—' : t.length > n ? t.slice(0, n) + '...' : t

const resetFilters = () => { filterStatus.value = 'all'; filterDate.value = 'all'; loadAppointments() }

const viewAppointment = (apt) => {
  selectedAppointment.value = apt
  diagnoseForm.value = { diagnosis: '', prescription: '', notes: '', next_visit_date: '' }
  showModal.value = true
}

const closeModal = () => { showModal.value = false; selectedAppointment.value = null }

const markComplete = async (id) => {
  if (!confirm('Mark this appointment as completed?')) return
  try {
    const res = await fetch(`${API_BASE}/api/doctor/appointments/${id}/complete`, {
      method: 'PUT', credentials: 'include'
    })
    const data = await res.json()
    if (data.success) loadAppointments()
    else alert(data.message)
  } catch (e) { alert('Error updating appointment') }
}

const markCancel = async (id) => {
  if (!confirm('Cancel this appointment?')) return
  try {
    const res = await fetch(`${API_BASE}/api/doctor/appointments/${id}/cancel`, {
      method: 'PUT', credentials: 'include'
    })
    const data = await res.json()
    if (data.success) loadAppointments()
    else alert(data.message)
  } catch (e) { alert('Error cancelling appointment') }
}

const saveDiagnosis = async () => {
  if (!diagnoseForm.value.diagnosis) { alert('Diagnosis is required'); return }
  saving.value = true
  try {
    const res = await fetch(`${API_BASE}/api/doctor/appointments/${selectedAppointment.value.id}/diagnose`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        diagnosis: diagnoseForm.value.diagnosis,
        prescription: diagnoseForm.value.prescription,
        notes: diagnoseForm.value.notes,
        treatment_plan: diagnoseForm.value.notes,
        next_visit_date: diagnoseForm.value.next_visit_date || null
      })
    })
    const data = await res.json()
    if (data.success) {
      closeModal()
      loadAppointments()
    } else {
      alert(data.message)
    }
  } catch (e) {
    alert('Error saving diagnosis')
  } finally {
    saving.value = false
  }
}

onMounted(loadAppointments)
</script>

<style scoped>
.detail-group { margin-bottom: 1rem; }
.detail-group label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #6b7280; display: block; margin-bottom: 0.25rem; }
.detail-group p { margin: 0; color: #111827; font-weight: 500; }
</style>
