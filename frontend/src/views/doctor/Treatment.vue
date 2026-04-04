<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-user-md me-2" style="color: var(--primary);"></i>
            Treatments & Appointments
          </h2>
          <p class="text-muted mb-0">Manage patient treatments and view medical history</p>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-lg-4">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-users me-2"></i>My Patients
            </h5>
          </div>
          <div class="card-body p-0">
            <div class="list-group list-group-flush">
              <button 
                v-for="patient in patients" 
                :key="patient.id"
                class="list-group-item list-group-item-action"
                :class="{ 'active': selectedPatient?.id === patient.id }"
                @click="selectPatient(patient)"
              >
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{{ patient.name }}</strong>
                    <br>
                    <small class="text-muted">PAT{{ String(patient.id).padStart(6, '0') }}</small>
                  </div>
                  <span class="badge bg-primary rounded-pill">{{ patient.appointment_count }}</span>
                </div>
              </button>
              <div v-if="patients.length === 0" class="text-center text-muted py-4">
                <p class="mb-0">No patients yet</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card shadow-sm border-0 mt-4">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0">
              <i class="fas fa-calendar-check me-2"></i>Today's Appointments
            </h5>
          </div>
          <div class="card-body p-0">
            <div class="list-group list-group-flush">
              <div 
                v-for="apt in todayAppointments" 
                :key="apt.id"
                class="list-group-item"
              >
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{{ apt.patient_name }}</strong>
                    <br>
                    <small class="text-muted">{{ apt.time }}</small>
                  </div>
                  <span class="badge" :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                </div>
              </div>
              <div v-if="todayAppointments.length === 0" class="text-center text-muted py-4">
                <p class="mb-0">No appointments today</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-8" v-if="selectedPatient">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0" style="color: var(--primary);">
                <i class="fas fa-user me-2"></i>{{ selectedPatient.name }}
              </h5>
              <span class="badge bg-secondary">Patient ID: {{ selectedPatient.id }}</span>
            </div>
          </div>
          <div class="card-body">
            <ul class="nav nav-tabs mb-3" id="patientTab" role="tablist">
              <li class="nav-item">
                <button class="nav-link active" id="history-tab" data-bs-toggle="tab" data-bs-target="#history" type="button">
                  <i class="fas fa-file-medical me-1"></i>Medical History
                </button>
              </li>
              <li class="nav-item">
                <button class="nav-link" id="appointments-tab" data-bs-toggle="tab" data-bs-target="#appointments" type="button">
                  <i class="fas fa-calendar me-1"></i>Appointments
                </button>
              </li>
              <li class="nav-item">
                <button class="nav-link" id="treatment-tab" data-bs-toggle="tab" data-bs-target="#treatment" type="button">
                  <i class="fas fa-pills me-1"></i>New Treatment
                </button>
              </li>
            </ul>

            <div class="tab-content" id="patientTabContent">
              <div class="tab-pane fade show active" id="history" role="tabpanel">
                <div class="row g-3">
                  <div class="col-md-6">
                    <div class="card bg-light">
                      <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-allergies me-2 text-danger"></i>Allergies</h6>
                      </div>
                      <div class="card-body">
                        <p class="mb-0">{{ medicalHistory.allergies || 'No known allergies' }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card bg-light">
                      <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-heartbeat me-2 text-primary"></i>Chronic Conditions</h6>
                      </div>
                      <div class="card-body">
                        <p class="mb-0">{{ medicalHistory.chronic_conditions || 'None' }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card bg-light">
                      <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-pills me-2 text-success"></i>Current Medications</h6>
                      </div>
                      <div class="card-body">
                        <p class="mb-0">{{ medicalHistory.medications || 'None' }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card bg-light">
                      <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-notes-medical me-2 text-warning"></i>Previous Surgeries</h6>
                      </div>
                      <div class="card-body">
                        <p class="mb-0">{{ medicalHistory.notes || 'None' }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="mt-4">
                  <h6><i class="fas fa-history me-2"></i>Treatment History</h6>
                  <div class="table-responsive">
                    <table class="table table-sm table-hover">
                      <thead class="table-light">
                        <tr>
                          <th>Date</th>
                          <th>Diagnosis</th>
                          <th>Prescription</th>
                          <th>Notes</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="treatment in treatments" :key="treatment.id">
                          <td>{{ treatment.date }}</td>
                          <td>{{ treatment.diagnosis }}</td>
                          <td>{{ treatment.prescription }}</td>
                          <td>{{ treatment.notes }}</td>
                        </tr>
                        <tr v-if="treatments.length === 0">
                          <td colspan="4" class="text-center text-muted">No treatment history</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              <div class="tab-pane fade" id="appointments" role="tabpanel">
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead class="table-light">
                      <tr>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Status</th>
                        <th>Reason</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="apt in patientAppointments" :key="apt.id">
                        <td>{{ apt.date }}</td>
                        <td>{{ apt.time }}</td>
                        <td>
                          <span class="badge" :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                        </td>
                        <td>{{ apt.reason }}</td>
                      </tr>
                      <tr v-if="patientAppointments.length === 0">
                        <td colspan="4" class="text-center text-muted">No appointments</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div class="tab-pane fade" id="treatment" role="tabpanel">
                <form @submit.prevent="saveTreatment">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label">Diagnosis <span class="text-danger">*</span></label>
                      <input type="text" class="form-control" v-model="newTreatment.diagnosis" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Follow-up Date</label>
                      <input type="date" class="form-control" v-model="newTreatment.follow_up_date">
                    </div>
                  </div>
                  <div class="mt-3">
                    <label class="form-label">Prescription</label>
                    <textarea class="form-control" v-model="newTreatment.prescription" rows="3" placeholder="Enter medications..."></textarea>
                  </div>
                  <div class="mt-3">
                    <label class="form-label">Notes</label>
                    <textarea class="form-control" v-model="newTreatment.notes" rows="3" placeholder="Additional notes..."></textarea>
                  </div>
                  <div class="mt-3">
                    <button type="submit" class="btn btn-primary" :disabled="saving">
                      <i class="fas fa-save me-2"></i>{{ saving ? 'Saving...' : 'Save Treatment' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-8" v-else>
        <div class="card shadow-sm border-0">
          <div class="card-body text-center text-muted py-5">
            <i class="fas fa-user-plus fa-3x mb-3"></i>
            <p class="mb-0">Select a patient from the list to view details and create treatments</p>
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
const selectedPatient = ref(null)
const medicalHistory = ref({})
const treatments = ref([])
const patientAppointments = ref([])
const todayAppointments = ref([])
const saving = ref(false)

const newTreatment = ref({
  diagnosis: '',
  prescription: '',
  notes: '',
  follow_up_date: ''
})

const getStatusClass = (status) => {
  const classes = {
    'Booked': 'bg-success',
    'Completed': 'bg-primary',
    'Cancelled': 'bg-danger',
    'In Progress': 'bg-warning'
  }
  return classes[status] || 'bg-secondary'
}

const loadPatients = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/doctor/patients`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      patients.value = data.patients || []
    }
  } catch (e) {
    console.error('Failed to load patients:', e)
  }
}

const loadTodayAppointments = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/doctor/appointments`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      const today = new Date().toISOString().split('T')[0]
      todayAppointments.value = data.appointments?.filter(a => a.date === today) || []
    }
  } catch (e) {
    console.error('Failed to load appointments:', e)
  }
}

const selectPatient = async (patient) => {
  selectedPatient.value = patient
  await Promise.all([
    loadMedicalHistory(patient.id),
    loadTreatments(patient.id),
    loadPatientAppointments(patient.id)
  ])
}

const loadMedicalHistory = async (patientId) => {
  try {
    const res = await fetch(`${API_BASE}/api/admin/patients/${patientId}/history`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      medicalHistory.value = data.medical_history || {}
    }
  } catch (e) {
    console.error('Failed to load medical history:', e)
  }
}

const loadTreatments = async (patientId) => {
  try {
    const res = await fetch(`${API_BASE}/api/admin/patients/${patientId}/treatments`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      treatments.value = data.treatments || []
    }
  } catch (e) {
    console.error('Failed to load treatments:', e)
  }
}

const loadPatientAppointments = async (patientId) => {
  try {
    const res = await fetch(`${API_BASE}/api/doctor/appointments`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      patientAppointments.value = data.appointments?.filter(a => a.patient_id === patientId) || []
    }
  } catch (e) {
    console.error('Failed to load appointments:', e)
  }
}

const saveTreatment = async () => {
  if (!selectedPatient.value) return
  if (!newTreatment.value.diagnosis) {
    alert('Diagnosis is required')
    return
  }

  saving.value = true
  try {
    const appointments = patientAppointments.value.filter(a => a.status === 'Booked')
    if (appointments.length === 0) {
      alert('No active appointment found for this patient')
      saving.value = false
      return
    }
    
    const res = await fetch(`${API_BASE}/api/doctor/appointments/${appointments[0].id}/diagnose`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        diagnosis: newTreatment.value.diagnosis,
        treatment_plan: newTreatment.value.notes,
        prescription: newTreatment.value.prescription,
        notes: newTreatment.value.notes,
        next_visit_date: newTreatment.value.follow_up_date
      })
    })
    const data = await res.json()
    if (data.success) {
      alert('Treatment saved successfully!')
      newTreatment.value = { diagnosis: '', prescription: '', notes: '', follow_up_date: '' }
      loadTreatments(selectedPatient.value.id)
    } else {
      alert(data.message || 'Failed to save treatment')
    }
  } catch (e) {
    console.error('Failed to save treatment:', e)
    alert('Error saving treatment')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadPatients()
  loadTodayAppointments()
})
</script>

<style scoped>
.card { border-radius: 1rem; }
.list-group-item.active { background-color: var(--primary); border-color: var(--primary); }
</style>
