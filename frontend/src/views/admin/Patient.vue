<template>
  <div class="container-fluid">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h2 class="mb-1">
          <i class="fas fa-hospital-user me-2"></i>
          Manage Patients
        </h2>
        <p class="text-muted mb-0">View and manage all patients in the system</p>
      </div>
    </div>

    <!-- Patients Table -->
    <div class="card">
      <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="fas fa-users me-2"></i>All Patients</h5>
          <span class="badge bg-white text-dark" style="font-size: 1rem; padding: 0.5rem 1rem;">
            {{ patients.length }} Total
          </span>
        </div>
      </div>
      <div class="card-body p-0">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-3 text-muted">Loading patients...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="alert alert-danger m-3">
          {{ error }}
          <button class="btn btn-sm btn-outline-danger ms-3" @click="loadPatients">Retry</button>
        </div>

        <!-- Table -->
        <div v-else-if="patients.length > 0" class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th class="text-nowrap">Patient ID</th>
                <th class="text-nowrap">Name</th>
                <th class="text-nowrap d-none d-xl-table-cell">Username</th>
                <th class="text-nowrap d-none d-md-table-cell">Gender</th>
                <th class="text-nowrap d-none d-xl-table-cell">Date of Birth</th>
                <th class="text-nowrap d-none d-lg-table-cell">Age</th>
                <th class="text-nowrap d-none d-lg-table-cell">Blood Group</th>
                <th class="text-nowrap d-none d-xl-table-cell">Address</th>
                <th class="text-nowrap">Status</th>
                <th class="text-nowrap">Actions</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="patient in patients" :key="patient.id">
                <tr>
                  <td class="text-nowrap"><strong>PAT{{ String(patient.id).padStart(6, '0') }}</strong></td>
                  <td class="text-nowrap">{{ patient.name }}</td>
                  <td class="d-none d-xl-table-cell">{{ patient.username }}</td>
                  <td class="d-none d-md-table-cell">{{ patient.gender }}</td>
                  <td class="d-none d-xl-table-cell">{{ patient.dob || 'N/A' }}</td>
                  <td class="d-none d-lg-table-cell">{{ calculateAge(patient.dob) }}</td>
                  <td class="d-none d-lg-table-cell">
                    <span class="badge bg-danger">{{ patient.blood_group }}</span>
                  </td>
                  <td class="d-none d-xl-table-cell">
                    <small>{{ truncateAddress(patient.address) }}</small>
                  </td>
                  <td>
                    <span class="badge" :class="patient.is_active ? 'bg-success' : 'bg-secondary'">
                      {{ patient.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group btn-group-sm" role="group">
                      <button @click="viewPatient(patient)" class="btn btn-sm btn-outline-info" title="View Details">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button @click="viewTreatments(patient)" class="btn btn-sm btn-outline-primary" title="View Treatments">
                        <i class="fas fa-file-medical"></i>
                      </button>
                      <button 
                        @click="toggleStatus(patient)"
                        class="btn btn-sm"
                        :class="patient.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
                        :title="patient.is_active ? 'Deactivate' : 'Activate'">
                        <i :class="patient.is_active ? 'fas fa-ban' : 'fas fa-check'"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center text-muted py-5">
          <i class="fas fa-hospital-user fa-4x mb-3 opacity-25"></i>
          <h5>No Patients Found</h5>
          <p>No patients have registered yet.</p>
        </div>
      </div>
    </div>

    <!-- Patient Details Modal -->
    <div v-if="showDetailsModal" class="modal-backdrop" @click.self="closeDetailsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-user-circle me-2"></i>Patient Details: {{ selectedPatient?.name }}
            </h5>
            <button type="button" class="btn-close" @click="closeDetailsModal"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <table class="table table-sm table-borderless">
                  <tr><th width="40%">Patient ID:</th><td>PAT{{ String(selectedPatient?.id).padStart(6, '0') }}</td></tr>
                  <tr><th>Full Name:</th><td>{{ selectedPatient?.name }}</td></tr>
                  <tr><th>Username:</th><td>{{ selectedPatient?.username }}</td></tr>
                  <tr><th>Gender:</th><td>{{ selectedPatient?.gender }}</td></tr>
                  <tr><th>Date of Birth:</th><td>{{ selectedPatient?.dob || 'N/A' }}</td></tr>
                </table>
              </div>
              <div class="col-md-6">
                <table class="table table-sm table-borderless">
                  <tr><th width="40%">Blood Group:</th><td><span class="badge bg-danger">{{ selectedPatient?.blood_group }}</span></td></tr>
                  <tr><th>Address:</th><td>{{ selectedPatient?.address || 'N/A' }}</td></tr>
                  <tr><th>Age:</th><td>{{ calculateAge(selectedPatient?.dob) }}</td></tr>
                  <tr><th>Account Status:</th><td>
                    <span class="badge" :class="selectedPatient?.is_active ? 'bg-success' : 'bg-secondary'">
                      {{ selectedPatient?.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td></tr>
                </table>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDetailsModal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Treatments Modal -->
    <div v-if="showTreatmentsModal" class="modal-backdrop" @click.self="closeTreatmentsModal">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-file-medical me-2"></i>Treatment Records: {{ selectedPatient?.name }}
            </h5>
            <button type="button" class="btn-close" @click="closeTreatmentsModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="treatmentsLoading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status"></div>
              <p class="mt-2 text-muted">Loading treatments...</p>
            </div>
            <div v-else>
              <div class="mb-4">
                <h6 class="fw-bold mb-3">Medical History</h6>
                <div class="row">
                  <div class="col-md-6">
                    <p><strong>Allergies:</strong> {{ medicalHistory.allergies || 'None recorded' }}</p>
                    <p><strong>Chronic Conditions:</strong> {{ medicalHistory.chronic_conditions || 'None recorded' }}</p>
                  </div>
                  <div class="col-md-6">
                    <p><strong>Current Medications:</strong> {{ medicalHistory.medications || 'None recorded' }}</p>
                    <p><strong>Notes:</strong> {{ medicalHistory.notes || 'None recorded' }}</p>
                  </div>
                </div>
              </div>
              <hr>
              <div class="mb-4">
                <h6 class="fw-bold mb-3">Treatments ({{ treatments.length }})</h6>
                <div v-if="treatments.length === 0" class="text-muted text-center py-3">No treatments recorded</div>
                <div v-else class="table-responsive">
                  <table class="table table-sm">
                    <thead><tr><th>Date</th><th>Doctor</th><th>Diagnosis</th><th>Prescription</th></tr></thead>
                    <tbody>
                      <tr v-for="treatment in treatments" :key="treatment.id">
                        <td>{{ treatment.date }}</td>
                        <td>{{ treatment.doctor_name }}</td>
                        <td>{{ treatment.diagnosis || '-' }}</td>
                        <td>{{ treatment.prescription || '-' }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <hr>
              <div>
                <h6 class="fw-bold mb-3">Appointments ({{ appointments.length }})</h6>
                <div v-if="appointments.length === 0" class="text-muted text-center py-3">No appointments recorded</div>
                <div v-else class="table-responsive">
                  <table class="table table-sm">
                    <thead><tr><th>Appointment #</th><th>Date</th><th>Time</th><th>Doctor</th><th>Status</th></tr></thead>
                    <tbody>
                      <tr v-for="apt in appointments" :key="apt.id">
                        <td>{{ apt.appointment_number }}</td>
                        <td>{{ apt.date }}</td>
                        <td>{{ apt.time }}</td>
                        <td>{{ apt.doctor_name }}</td>
                        <td><span class="badge" :class="getStatusClass(apt.status)">{{ apt.status }}</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeTreatmentsModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:5000'

const patients = ref([])
const loading = ref(false)
const error = ref(null)

const showDetailsModal = ref(false)
const selectedPatient = ref(null)

const showTreatmentsModal = ref(false)
const treatmentsLoading = ref(false)
const treatments = ref([])
const appointments = ref([])
const medicalHistory = ref({})

const loadPatients = async () => {
  loading.value = true
  error.value = null

  try {
    const res = await fetch(`${API_BASE}/api/admin/patients`, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await res.json()

    if (!res.ok || !data.success) {
      throw new Error(data.message || 'Failed to load patients')
    }

    patients.value = data.patients || []
  } catch (err) {
    error.value = err.message
    console.error('Error loading patients:', err)
  } finally {
    loading.value = false
  }
}

const calculateAge = (dob) => {
  if (!dob) return 'N/A'
  const today = new Date()
  const birthDate = new Date(dob)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  return `${age} years`
}

const truncateAddress = (address) => {
  if (!address) return 'N/A'
  return address.length > 30 ? address.substring(0, 30) + '...' : address
}

const getStatusClass = (status) => {
  switch (status?.toLowerCase()) {
    case 'booked': return 'bg-primary'
    case 'completed': return 'bg-success'
    case 'cancelled': return 'bg-danger'
    default: return 'bg-secondary'
  }
}

const viewPatient = (patient) => {
  selectedPatient.value = patient
  showDetailsModal.value = true
}

const closeDetailsModal = () => {
  showDetailsModal.value = false
  selectedPatient.value = null
}

const viewTreatments = async (patient) => {
  selectedPatient.value = patient
  showTreatmentsModal.value = true
  treatmentsLoading.value = true

  try {
    const res = await fetch(`${API_BASE}/api/admin/patients/${patient.id}/treatments`, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await res.json()

    if (data.success) {
      treatments.value = data.treatments || []
      appointments.value = data.appointments || []
      medicalHistory.value = data.medical_history || {}
    }
  } catch (err) {
    console.error('Error loading treatments:', err)
  } finally {
    treatmentsLoading.value = false
  }
}

const closeTreatmentsModal = () => {
  showTreatmentsModal.value = false
  treatments.value = []
  appointments.value = []
  medicalHistory.value = {}
}

const toggleStatus = async (patient) => {
  const action = patient.is_active ? 'deactivate' : 'activate'
  
  if (!confirm(`Are you sure you want to ${action} this patient?`)) {
    return
  }

  try {
    const res = await fetch(`${API_BASE}/api/admin/patients/${patient.id}/toggle`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await res.json()

    if (data.success) {
      await loadPatients()
    } else {
      alert(data.message || 'Failed to update status')
    }
  } catch (err) {
    console.error('Error toggling status:', err)
    alert('Failed to update status')
  }
}

onMounted(() => {
  loadPatients()
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
  margin-bottom: 1.5rem;
  background: white;
  overflow: hidden;
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
  padding: 0;
}

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
  white-space: nowrap;
}

.table tbody tr {
  transition: all 0.2s ease;
  border-bottom: 1px solid var(--gray-100, #f3f4f6);
}

.table tbody tr:hover {
  background: var(--gray-50, #f9fafb);
}

.table tbody td {
  padding: 1rem 1.25rem;
  vertical-align: middle;
}

.badge {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.75rem;
}

.btn {
  border-radius: 10px;
  padding: 0.625rem 1.25rem;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  border: none;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.8125rem;
}

.btn-outline-info {
  border: 1px solid #3b82f6;
  color: #3b82f6;
}

.btn-outline-info:hover {
  background: #3b82f6;
  color: white;
}

.btn-outline-primary {
  border: 1px solid #6366f1;
  color: #6366f1;
}

.btn-outline-primary:hover {
  background: #6366f1;
  color: white;
}

.btn-outline-danger {
  border: 1px solid #ef4444;
  color: #ef4444;
}

.btn-outline-danger:hover {
  background: #ef4444;
  color: white;
}

.btn-outline-success {
  border: 1px solid #10b981;
  color: #10b981;
}

.btn-outline-success:hover {
  background: #10b981;
  color: white;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 1rem;
}

.modal-dialog {
  width: 100%;
  max-width: 900px;
  margin: 0;
}

.modal-content {
  border: none;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  background: white;
}

.modal-header {
  border-bottom: 1px solid var(--gray-200, #e5e7eb);
  padding: 1.25rem 1.5rem;
  border-radius: 16px 16px 0 0;
}

.modal-title {
  font-weight: 600;
  color: var(--gray-900, #111827);
}

.modal-body {
  padding: 1.5rem;
  max-height: 70vh;
  overflow-y: auto;
}

.modal-footer {
  border-top: 1px solid var(--gray-200, #e5e7eb);
  padding: 1rem 1.5rem;
  border-radius: 0 0 16px 16px;
}

.btn-close {
  opacity: 0.5;
}

.btn-close:hover {
  opacity: 1;
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
