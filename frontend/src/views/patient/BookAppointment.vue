<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-calendar-plus me-2" style="color: var(--primary);"></i>
            Book Appointment
          </h2>
          <p class="text-muted mb-0">Schedule an appointment with a doctor</p>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-lg-8">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-user-md me-2"></i>Select Doctor
            </h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <input type="text" class="form-control" v-model="searchQuery" placeholder="Search doctors by name or specialization..." @input="filterDoctors">
            </div>
            <div class="table-responsive">
              <table class="table table-hover">
                <thead class="table-light">
                  <tr>
                    <th>Select</th>
                    <th>Doctor Name</th>
                    <th>Specialization</th>
                    <th>Department</th>
                    <th>Experience</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="doctor in filteredDoctors" :key="doctor.id">
                    <td>
                      <input type="radio" name="doctor" :value="doctor.id" v-model="selectedDoctor" @change="selectDoctor(doctor)">
                    </td>
                    <td><strong>{{ doctor.name }}</strong></td>
                    <td>{{ doctor.specialization }}</td>
                    <td>{{ doctor.department }}</td>
                    <td>{{ doctor.experience }} years</td>
                  </tr>
                  <tr v-if="filteredDoctors.length === 0">
                    <td colspan="5" class="text-center text-muted py-3">No doctors found</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="card shadow-sm border-0 mt-4" v-if="selectedDoctor">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-calendar me-2"></i>Select Date & Time
            </h5>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-4">
                <label class="form-label">Appointment Date <span class="text-danger">*</span></label>
                <input type="date" class="form-control" v-model="appointment.date" :min="minDate" @change="loadAvailableSlots">
              </div>
              <div class="col-md-4">
                <label class="form-label">Available Slots</label>
                <select class="form-select" v-model="appointment.time" :disabled="!appointment.date">
                  <option value="">Select a time</option>
                  <option v-for="slot in availableSlots" :key="slot" :value="slot">{{ slot }}</option>
                </select>
              </div>
              <div class="col-md-4">
                <label class="form-label">Reason for Visit</label>
                <input type="text" class="form-control" v-model="appointment.reason" placeholder="Brief description...">
              </div>
            </div>
          </div>
        </div>

        <div class="card shadow-sm border-0 mt-4" v-if="selectedDoctor && appointment.date && appointment.time">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-check-circle me-2"></i>Confirm Appointment
            </h5>
          </div>
          <div class="card-body">
            <div class="alert alert-info">
              <h6><strong>Appointment Summary</strong></h6>
              <p class="mb-1"><strong>Doctor:</strong> {{ selectedDoctorData?.name }}</p>
              <p class="mb-1"><strong>Specialization:</strong> {{ selectedDoctorData?.specialization }}</p>
              <p class="mb-1"><strong>Date:</strong> {{ appointment.date }}</p>
              <p class="mb-1"><strong>Time:</strong> {{ appointment.time }}</p>
              <p class="mb-0"><strong>Reason:</strong> {{ appointment.reason || 'Not specified' }}</p>
            </div>
            <div class="text-end">
              <button class="btn btn-success px-4" @click="bookAppointment" :disabled="booking">
                <i class="fas fa-check me-2"></i>{{ booking ? 'Booking...' : 'Confirm Appointment' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0">
              <i class="fas fa-info-circle me-2"></i>Instructions
            </h5>
          </div>
          <div class="card-body">
            <ol class="small">
              <li class="mb-2">Search and select a doctor</li>
              <li class="mb-2">Choose an available date</li>
              <li class="mb-2">Pick a time slot</li>
              <li class="mb-2">Provide reason for visit (optional)</li>
              <li>Confirm your appointment</li>
            </ol>
          </div>
        </div>

        <div class="card shadow-sm border-0 mt-4">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0">
              <i class="fas fa-history me-2"></i>My Upcoming Appointments
            </h5>
          </div>
          <div class="card-body">
            <div v-if="myAppointments.length === 0" class="text-center text-muted">
              <p>No upcoming appointments</p>
            </div>
            <div v-else>
              <div v-for="apt in myAppointments" :key="apt.id" class="border-bottom pb-2 mb-2">
                <p class="mb-1"><strong>{{ apt.doctor_name }}</strong></p>
                <p class="mb-0 small text-muted">{{ apt.date }} at {{ apt.time }}</p>
                <span class="badge" :class="apt.status === 'Booked' ? 'bg-success' : 'bg-secondary'">{{ apt.status }}</span>
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

const doctors = ref([])
const filteredDoctors = ref([])
const searchQuery = ref('')
const selectedDoctor = ref(null)
const selectedDoctorData = ref(null)
const availableSlots = ref([])
const myAppointments = ref([])
const booking = ref(false)

const appointment = ref({
  date: '',
  time: '',
  reason: ''
})

const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const filterDoctors = () => {
  const query = searchQuery.value.toLowerCase()
  filteredDoctors.value = doctors.value.filter(d => 
    d.name.toLowerCase().includes(query) || 
    d.specialization.toLowerCase().includes(query)
  )
}

const loadDoctors = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/patient/doctors`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      doctors.value = data.doctors || []
      filteredDoctors.value = doctors.value
    }
  } catch (e) {
    console.error('Failed to load doctors:', e)
  }
}

const selectDoctor = (doctor) => {
  selectedDoctorData.value = doctor
  appointment.value.date = ''
  appointment.value.time = ''
  availableSlots.value = []
}

const loadAvailableSlots = async () => {
  if (!selectedDoctor.value || !appointment.value.date) return
  
  try {
    const res = await fetch(`${API_BASE}/api/doctor/${selectedDoctor.value}/availability?date=${appointment.value.date}`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      availableSlots.value = data.slots || []
    }
  } catch (e) {
    console.error('Failed to load slots:', e)
  }
}

const loadMyAppointments = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/patient/appointments`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      myAppointments.value = data.appointments?.filter(a => a.status === 'Booked') || []
    }
  } catch (e) {
    console.error('Failed to load appointments:', e)
  }
}

const bookAppointment = async () => {
  if (!selectedDoctor.value || !appointment.value.date || !appointment.value.time) {
    alert('Please fill in all required fields')
    return
  }
  
  booking.value = true
  try {
    const res = await fetch(`${API_BASE}/api/patient/appointments/book`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        doctor_id: selectedDoctor.value,
        appoint_date: appointment.value.date,
        appoint_time: appointment.value.time,
        reason: appointment.value.reason
      })
    })
    const data = await res.json()
    if (data.success) {
      alert('Appointment booked successfully!')
      router.push('/patient/appointments')
    } else {
      alert(data.message || 'Failed to book appointment')
    }
  } catch (e) {
    console.error('Failed to book appointment:', e)
    alert('Error booking appointment')
  } finally {
    booking.value = false
  }
}

onMounted(() => {
  loadDoctors()
  loadMyAppointments()
})
</script>

<style scoped>
.card { border-radius: 1rem; }
.table th { font-weight: 600; }
</style>
