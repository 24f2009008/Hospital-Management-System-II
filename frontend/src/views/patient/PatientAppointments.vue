<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-calendar-alt me-2" style="color: var(--primary);"></i>
            My Appointments
          </h2>
          <p class="text-muted mb-0">View and manage your appointments</p>
        </div>
        <div>
          <router-link to="/patient/appointments/book" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Book New Appointment
          </router-link>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12">
        <ul class="nav nav-pills mb-3" id="appointmentTab" role="tablist">
          <li class="nav-item">
            <button class="nav-link active" id="upcoming-tab" data-bs-toggle="pill" data-bs-target="#upcoming" type="button">
              <i class="fas fa-clock me-1"></i>Upcoming
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" id="past-tab" data-bs-toggle="pill" data-bs-target="#past" type="button">
              <i class="fas fa-history me-1"></i>Past
            </button>
          </li>
        </ul>

        <div class="tab-content" id="appointmentTabContent">
          <div class="tab-pane fade show active" id="upcoming" role="tabpanel">
            <div class="card shadow-sm border-0">
              <div class="card-body">
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead class="table-light">
                      <tr>
                        <th>Doctor</th>
                        <th>Department</th>
                        <th>Date & Time</th>
                        <th>Reason</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="apt in upcomingAppointments" :key="apt.id">
                        <td>
                          <strong>{{ apt.doctor_name }}</strong>
                          <br>
                          <small class="text-muted">{{ apt.specialization }}</small>
                        </td>
                        <td>{{ apt.department }}</td>
                        <td>
                          {{ apt.date }}
                          <br>
                          <small class="text-muted">{{ apt.time }}</small>
                        </td>
                        <td>{{ apt.reason || '-' }}</td>
                        <td>
                          <span class="badge" :class="getStatusClass(apt.status)">
                            {{ apt.status }}
                          </span>
                        </td>
                        <td>
                          <button class="btn btn-sm btn-outline-danger" @click="cancelAppointment(apt.id)">
                            <i class="fas fa-times me-1"></i>Cancel
                          </button>
                        </td>
                      </tr>
                      <tr v-if="upcomingAppointments.length === 0">
                        <td colspan="6" class="text-center text-muted py-4">
                          <i class="fas fa-calendar-times fa-2x mb-2"></i>
                          <p class="mb-0">No upcoming appointments</p>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <div class="tab-pane fade" id="past" role="tabpanel">
            <div class="card shadow-sm border-0">
              <div class="card-body">
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead class="table-light">
                      <tr>
                        <th>Doctor</th>
                        <th>Department</th>
                        <th>Date & Time</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="apt in pastAppointments" :key="apt.id">
                        <td>
                          <strong>{{ apt.doctor_name }}</strong>
                          <br>
                          <small class="text-muted">{{ apt.specialization }}</small>
                        </td>
                        <td>{{ apt.department }}</td>
                        <td>
                          {{ apt.date }}
                          <br>
                          <small class="text-muted">{{ apt.time }}</small>
                        </td>
                        <td>
                          <span class="badge" :class="getStatusClass(apt.status)">
                            {{ apt.status }}
                          </span>
                        </td>
                        <td>
                          <button class="btn btn-sm btn-outline-primary" @click="viewDetails(apt.id)">
                            <i class="fas fa-eye me-1"></i>View Details
                          </button>
                        </td>
                      </tr>
                      <tr v-if="pastAppointments.length === 0">
                        <td colspan="5" class="text-center text-muted py-4">
                          <i class="fas fa-history fa-2x mb-2"></i>
                          <p class="mb-0">No past appointments</p>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="detailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Appointment Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedAppointment">
            <div class="row g-3">
              <div class="col-md-6">
                <p><strong>Doctor:</strong> {{ selectedAppointment.doctor_name }}</p>
                <p><strong>Specialization:</strong> {{ selectedAppointment.specialization }}</p>
                <p><strong>Date:</strong> {{ selectedAppointment.date }}</p>
                <p><strong>Time:</strong> {{ selectedAppointment.time }}</p>
              </div>
              <div class="col-md-6">
                <p><strong>Status:</strong> {{ selectedAppointment.status }}</p>
                <p><strong>Reason:</strong> {{ selectedAppointment.reason || 'N/A' }}</p>
              </div>
            </div>
            <div v-if="selectedAppointment.treatment" class="mt-4">
              <h6>Treatment Details</h6>
              <div class="card bg-light">
                <div class="card-body">
                  <p><strong>Diagnosis:</strong> {{ selectedAppointment.treatment.diagnosis }}</p>
                  <p><strong>Prescription:</strong> {{ selectedAppointment.treatment.prescription }}</p>
                  <p><strong>Notes:</strong> {{ selectedAppointment.treatment.notes }}</p>
                </div>
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
import { useRouter } from 'vue-router'

const router = useRouter()
const API_BASE = 'http://127.0.0.1:5000'

const appointments = ref([])
const selectedAppointment = ref(null)

const upcomingAppointments = computed(() => 
  appointments.value.filter(a => a.status === 'Booked')
)

const pastAppointments = computed(() => 
  appointments.value.filter(a => a.status !== 'Booked')
)

const getStatusClass = (status) => {
  const classes = { 'Completed': 'bg-success', 'Cancelled': 'bg-danger' }
  return classes[status] || 'bg-secondary'
}

const loadAppointments = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/patient/appointments`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      appointments.value = data.appointments || []
    }
  } catch (e) {
    console.error('Failed to load appointments:', e)
  }
}

const cancelAppointment = async (id) => {
  if (!confirm('Are you sure you want to cancel this appointment?')) return
  try {
    const res = await fetch(`${API_BASE}/api/patient/appointments/${id}/cancel`, {
      method: 'PUT',
      credentials: 'include'
    })
    const data = await res.json()
    if (data.success) {
      alert('Appointment cancelled successfully')
      loadAppointments()
    } else {
      alert(data.message || 'Failed to cancel appointment')
    }
  } catch (e) {
    console.error('Failed to cancel appointment:', e)
  }
}

const viewDetails = async (id) => {
  try {
    const res = await fetch(`${API_BASE}/api/patient/appointments/${id}/details`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      selectedAppointment.value = data.appointment
      const modal = new bootstrap.Modal(document.getElementById('detailsModal'))
      modal.show()
    }
  } catch (e) {
    console.error('Failed to load appointment details:', e)
  }
}

onMounted(() => {
  loadAppointments()
})
</script>

<style scoped>
.card { border-radius: 1rem; }
</style>
