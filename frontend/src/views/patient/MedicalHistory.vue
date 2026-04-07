<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-file-medical-alt me-2"></i>My Medical History
          </h2>
          <p class="text-muted mb-0">View your complete medical records and treatment history</p>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-3 text-muted">Loading your medical history...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
      <button class="btn btn-sm btn-outline-danger ms-3" @click="loadMedicalHistory">Retry</button>
    </div>

    <template v-else>
      <!-- Medical History Card -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="mb-0"><i class="fas fa-heartbeat me-2"></i>Medical Information</h5>
        </div>
        <div class="card-body">
          <div class="row g-4">
            <div class="col-md-6">
              <div class="info-box">
                <div class="info-icon bg-danger-subtle">
                  <i class="fas fa-allergies text-danger"></i>
                </div>
                <div>
                  <small class="text-muted d-block">Allergies</small>
                  <strong>{{ medicalHistory.allergies || 'No known allergies' }}</strong>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="info-box">
                <div class="info-icon bg-primary-subtle">
                  <i class="fas fa-heart text-primary"></i>
                </div>
                <div>
                  <small class="text-muted d-block">Chronic Conditions</small>
                  <strong>{{ medicalHistory.chronic_conditions || 'None' }}</strong>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="info-box">
                <div class="info-icon bg-success-subtle">
                  <i class="fas fa-pills text-success"></i>
                </div>
                <div>
                  <small class="text-muted d-block">Current Medications</small>
                  <strong>{{ medicalHistory.medications || 'None' }}</strong>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="info-box">
                <div class="info-icon bg-warning-subtle">
                  <i class="fas fa-procedures text-warning"></i>
                </div>
                <div>
                  <small class="text-muted d-block">Previous Surgeries</small>
                  <strong>{{ medicalHistory.notes || 'None' }}</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Treatment History -->
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="fas fa-user-md me-2"></i>Treatment History</h5>
          <span class="badge bg-primary">{{ treatments.length }} Visits</span>
        </div>
        <div class="card-body p-0">
          <div v-if="treatments.length === 0" class="text-center text-muted py-4">
            <i class="fas fa-file-medical fa-3x mb-3 opacity-25"></i>
            <p class="mb-0">No treatments recorded yet</p>
          </div>
          <div v-else class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Doctor</th>
                  <th>Diagnosis</th>
                  <th>Prescription</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="treatment in treatments" :key="treatment.id">
                  <td>{{ treatment.date || 'N/A' }}</td>
                  <td>{{ treatment.doctor_name }}</td>
                  <td>{{ treatment.diagnosis || '-' }}</td>
                  <td>{{ treatment.prescription || '-' }}</td>
                  <td>{{ treatment.notes || '-' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Appointments History -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="fas fa-calendar-check me-2"></i>Appointment History</h5>
          <span class="badge bg-primary">{{ appointments.length }} Total</span>
        </div>
        <div class="card-body p-0">
          <div v-if="appointments.length === 0" class="text-center text-muted py-4">
            <i class="fas fa-calendar-times fa-3x mb-3 opacity-25"></i>
            <p class="mb-0">No appointments yet</p>
          </div>
          <div v-else class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Doctor</th>
                  <th>Reason</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="apt in appointments" :key="apt.id">
                  <td>{{ apt.date || 'N/A' }}</td>
                  <td>{{ apt.time || 'N/A' }}</td>
                  <td>{{ apt.doctor_name }}</td>
                  <td>{{ apt.reason || '-' }}</td>
                  <td>
                    <span class="badge" :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:5000'

const loading = ref(true)
const error = ref(null)
const medicalHistory = ref({})
const treatments = ref([])
const appointments = ref([])

const loadMedicalHistory = async () => {
  loading.value = true
  error.value = null

  try {
    const res = await fetch(`${API_BASE}/api/patient/history`, {
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await res.json()

    if (!res.ok || !data.success) {
      throw new Error(data.message || 'Failed to load medical history')
    }

    medicalHistory.value = data.medical_history || {}
    treatments.value = data.treatments || []
    appointments.value = data.appointments || []
  } catch (err) {
    error.value = err.message
    console.error('Error loading medical history:', err)
  } finally {
    loading.value = false
  }
}

const getStatusClass = (status) => {
  switch (status?.toLowerCase()) {
    case 'booked': return 'bg-primary'
    case 'completed': return 'bg-success'
    case 'cancelled': return 'bg-danger'
    default: return 'bg-secondary'
  }
}

onMounted(() => {
  loadMedicalHistory()
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

.card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  background: white;
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

.info-box {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 12px;
  background: var(--gray-50, #f9fafb);
}

.info-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.bg-danger-subtle { background: #fee2e2; }
.bg-primary-subtle { background: #dbeafe; }
.bg-success-subtle { background: #d1fae5; }
.bg-warning-subtle { background: #fef3c7; }

.table {
  margin-bottom: 0;
}

.table thead th {
  background: var(--gray-50, #f9fafb);
  border-bottom: 2px solid var(--gray-200, #e5e7eb);
  color: var(--gray-700, #374151);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  padding: 1rem 1.25rem;
}

.table tbody tr {
  border-bottom: 1px solid var(--gray-100, #f3f4f6);
}

.table tbody td {
  padding: 1rem 1.25rem;
}

.badge {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.75rem;
}

.spinner-border {
  color: var(--primary, #6366f1);
}

.alert {
  border: none;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>