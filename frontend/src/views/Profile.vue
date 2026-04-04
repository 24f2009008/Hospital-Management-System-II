<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-user-circle me-2" style="color: var(--primary);"></i>
            My Profile
          </h2>
          <p class="text-muted mb-0">{{ roleTitle }} - Manage your personal information</p>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-lg-8">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-address-card me-2"></i>{{ sectionTitle }}
            </h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="saveProfile">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-semibold">Full Name</label>
                  <input type="text" class="form-control" v-model="profile.name" readonly>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-semibold">Username</label>
                  <input type="text" class="form-control" v-model="profile.username" readonly>
                </div>
              </div>

              <template v-if="role === 'patient'">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Gender</label>
                    <select class="form-select" v-model="profile.gender">
                      <option value="">Select Gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Date of Birth</label>
                    <input type="date" class="form-control" v-model="profile.dob">
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Blood Group</label>
                    <select class="form-select" v-model="profile.blood_group">
                      <option value="">Select Blood Group</option>
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
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Address</label>
                    <input type="text" class="form-control" v-model="profile.address">
                  </div>
                </div>
              </template>

              <template v-else-if="role === 'doctor'">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Department</label>
                    <input type="text" class="form-control" v-model="profile.department" readonly>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">License Number</label>
                    <input type="text" class="form-control" v-model="profile.license_number" readonly>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Specialization</label>
                    <input type="text" class="form-control" v-model="profile.specialization">
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Experience (Years)</label>
                    <input type="number" class="form-control" v-model="profile.experience" min="0" max="50">
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Gender</label>
                    <select class="form-select" v-model="profile.gender">
                      <option value="">Select Gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Status</label>
                    <div class="d-flex align-items-center">
                      <span class="badge" :class="profile.status === 'active' ? 'bg-success' : 'bg-secondary'">
                        {{ profile.status || 'Unknown' }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-semibold">Qualifications</label>
                  <textarea class="form-control" v-model="profile.qualification" rows="3" placeholder="Enter your qualifications..."></textarea>
                </div>
              </template>

              <template v-else-if="role === 'admin'">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Role</label>
                    <input type="text" class="form-control" v-model="profile.role" readonly>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">User ID</label>
                    <input type="text" class="form-control" :value="profile.id" readonly>
                  </div>
                </div>
              </template>

              <div class="text-end">
                <button type="submit" class="btn btn-primary px-4" :disabled="saving">
                  <i class="fas fa-save me-2"></i>{{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <template v-if="role === 'patient'">
          <div class="card shadow-sm border-0 mt-4">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0" style="color: var(--primary);">
                <i class="fas fa-heartbeat me-2"></i>Medical History
              </h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="saveMedicalHistory">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Allergies</label>
                    <textarea class="form-control" v-model="medicalHistory.allergies" rows="2" placeholder="List any allergies..."></textarea>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Chronic Conditions</label>
                    <textarea class="form-control" v-model="medicalHistory.chronic_conditions" rows="2" placeholder="List chronic conditions..."></textarea>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Current Medications</label>
                    <textarea class="form-control" v-model="medicalHistory.current_medications" rows="2" placeholder="List current medications..."></textarea>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Previous Surgeries</label>
                    <textarea class="form-control" v-model="medicalHistory.previous_surgeries" rows="2" placeholder="List previous surgeries..."></textarea>
                  </div>
                </div>
                <div class="text-end">
                  <button type="submit" class="btn btn-primary px-4" :disabled="savingHistory">
                    <i class="fas fa-save me-2"></i>{{ savingHistory ? 'Saving...' : 'Save Medical History' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </template>

        <template v-if="role === 'doctor'">
          <div class="card shadow-sm border-0 mt-4">
            <div class="card-header bg-white border-bottom">
              <h5 class="card-title mb-0" style="color: var(--primary);">
                <i class="fas fa-clock me-2"></i>Availability Schedule
              </h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Day</th>
                      <th>Date</th>
                      <th>Start Time</th>
                      <th>End Time</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="slot in availability" :key="slot.id">
                      <td>{{ formatDay(slot.available_date) }}</td>
                      <td>{{ slot.available_date }}</td>
                      <td>{{ slot.start_time }}</td>
                      <td>{{ slot.end_time }}</td>
                      <td>
                        <span class="badge" :class="slot.available ? 'bg-success' : 'bg-danger'">
                          {{ slot.available ? 'Available' : 'Not Available' }}
                        </span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-danger" @click="removeAvailability(slot.id)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </td>
                    </tr>
                    <tr v-if="availability.length === 0">
                      <td colspan="6" class="text-center text-muted">No availability set. Add your schedule below.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <hr>
              <h6 class="fw-bold mb-3">Add New Availability</h6>
              <form @submit.prevent="addAvailability" class="row g-3">
                <div class="col-md-3">
                  <label class="form-label">Date</label>
                  <input type="date" class="form-control" v-model="newAvailability.date" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Start Time</label>
                  <input type="time" class="form-control" v-model="newAvailability.start_time" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">End Time</label>
                  <input type="time" class="form-control" v-model="newAvailability.end_time" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Notes</label>
                  <input type="text" class="form-control" v-model="newAvailability.notes" placeholder="Optional notes">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                  <button type="submit" class="btn btn-primary w-100">
                    <i class="fas fa-plus me-1"></i>Add
                  </button>
                </div>
              </form>
            </div>
          </div>
        </template>
      </div>

      <div class="col-lg-4">
        <div class="card shadow-sm border-0">
          <div class="card-body text-center">
            <div class="profile-avatar mx-auto mb-3" :style="avatarStyle">
              {{ profile.name ? profile.name[0].toUpperCase() : roleChar }}
            </div>
            <h5 class="fw-bold">{{ profile.name }}</h5>
            <p class="text-muted mb-1" v-if="role === 'doctor'">{{ profile.department }}</p>
            <p class="text-muted mb-1" v-if="role === 'patient'">PAT{{ String(profile.id).padStart(6, '0') }}</p>
            <span class="badge" :class="profile.status === 'active' ? 'bg-success' : 'bg-secondary'" v-if="role === 'doctor'">
              {{ profile.status === 'active' ? 'Active' : 'Inactive' }}
            </span>
            <span class="badge bg-success" v-if="role === 'patient'">Active</span>
            <span class="badge bg-primary" v-if="role === 'admin'">Admin</span>
            <hr>
            <div class="text-start small">
              <template v-if="role === 'patient'">
                <p><strong>Gender:</strong> {{ profile.gender || 'Not specified' }}</p>
                <p><strong>Blood Group:</strong> {{ profile.blood_group || 'Not specified' }}</p>
                <p><strong>Age:</strong> {{ calculateAge(profile.dob) }}</p>
              </template>
              <template v-else-if="role === 'doctor'">
                <p class="mb-2"><strong>License:</strong> {{ profile.license_number || 'Not assigned' }}</p>
                <p class="mb-2"><strong>Experience:</strong> {{ profile.experience || 0 }} years</p>
                <p class="mb-2"><strong>Specialization:</strong> {{ profile.specialization || 'Not specified' }}</p>
              </template>
              <template v-else-if="role === 'admin'">
                <p><strong>Role:</strong> Administrator</p>
                <p><strong>User ID:</strong> {{ profile.id }}</p>
              </template>
              <p><strong>Username:</strong> {{ profile.username }}</p>
            </div>
          </div>
        </div>

        <div class="card shadow-sm border-0 mt-4">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0">
              <i class="fas fa-chart-line me-2"></i>Quick Stats
            </h5>
          </div>
          <div class="card-body">
            <div class="row text-center">
              <div class="col-6 mb-3">
                <h4 class="text-primary">{{ stats.totalAppointments }}</h4>
                <small class="text-muted">Total Appointments</small>
              </div>
              <div class="col-6 mb-3">
                <h4 class="text-success">{{ stats.upcomingAppointments }}</h4>
                <small class="text-muted">{{ role === 'doctor' ? 'Pending' : 'Upcoming' }}</small>
              </div>
              <div class="col-12" v-if="role === 'doctor'">
                <h4 class="text-info">{{ stats.totalPatients }}</h4>
                <small class="text-muted">Total Patients</small>
              </div>
              <div class="col-12" v-if="role === 'patient'">
                <h4 class="text-info">{{ stats.completedTreatments }}</h4>
                <small class="text-muted">Treatments</small>
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

const API_BASE = 'http://127.0.0.1:5000'

const role = ref('')

const roleTitle = computed(() => {
  const titles = { patient: 'Patient', doctor: 'Doctor', admin: 'Administrator' }
  return titles[role.value] || 'User'
})

const sectionTitle = computed(() => {
  const titles = { patient: 'Personal Information', doctor: 'Professional Information', admin: 'Admin Information' }
  return titles[role.value] || 'Profile Information'
})

const roleChar = computed(() => {
  const chars = { patient: 'P', doctor: 'D', admin: 'A' }
  return chars[role.value] || 'U'
})

const avatarStyle = computed(() => {
  return role.value === 'doctor' ? 'background: linear-gradient(135deg, #27ae60, #2ecc71);' : ''
})

const profile = ref({
  id: null, name: '', username: '', gender: '', dob: '', blood_group: '', address: '',
  department: '', license_number: '', specialization: '', qualification: '', experience: 0, status: '', role: 'patient'
})

const medicalHistory = ref({ allergies: '', chronic_conditions: '', current_medications: '', previous_surgeries: '' })
const availability = ref([])
const newAvailability = ref({ date: '', start_time: '', end_time: '', notes: '' })
const stats = ref({ totalAppointments: 0, upcomingAppointments: 0, completedTreatments: 0, totalPatients: 0 })
const saving = ref(false)
const savingHistory = ref(false)

const calculateAge = (dob) => {
  if (!dob) return 'Not specified'
  const birth = new Date(dob)
  const today = new Date()
  let age = today.getFullYear() - birth.getFullYear()
  const m = today.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--
  return age > 0 ? `${age} years` : 'Not specified'
}

const formatDay = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { weekday: 'long' })
}

const loadProfile = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/dashboard`, { credentials: 'include' })
    const userData = await res.json()
    if (userData.success) role.value = userData.user.role
    if (!role.value) return

    let endpoint = role.value === 'patient' ? '/api/patient/profile' : role.value === 'doctor' ? '/api/doctor/profile' : '/api/admin/profile'
    const res2 = await fetch(`${API_BASE}${endpoint}`, { credentials: 'include' })
    const data = await res2.json()
    if (data.success) {
      profile.value = { ...profile.value, ...data.profile }
      if (data.stats) {
        stats.value = {
          totalAppointments: data.stats.total_appointments || data.stats.todays_appointments || 0,
          upcomingAppointments: data.stats.upcoming_appointments || data.stats.pending_consultations || 0,
          totalPatients: data.stats.total_patients || 0,
          completedTreatments: data.stats.completed_appointments || 0
        }
      }
    }
  } catch (e) {
    console.error('Failed to load profile:', e)
  }
}

const loadMedicalHistory = async () => {
  if (role.value !== 'patient') return
  try {
    const res = await fetch(`${API_BASE}/api/patient/history`, { credentials: 'include' })
    const data = await res.json()
    if (data.success && data.medical_history) {
      medicalHistory.value = {
        allergies: data.medical_history.allergies || '',
        chronic_conditions: data.medical_history.chronic_conditions || '',
        current_medications: data.medical_history.medications || '',
        previous_surgeries: data.medical_history.notes || ''
      }
    }
  } catch (e) {
    console.error('Failed to load medical history:', e)
  }
}

const loadAvailability = async () => {
  if (role.value !== 'doctor') return
  try {
    const res = await fetch(`${API_BASE}/api/doctor/availability`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      availability.value = data.availability.map(slot => ({
        ...slot, available_date: slot.date, start_time: slot.start_time, end_time: slot.end_time
      }))
    }
  } catch (e) {
    console.error('Failed to load availability:', e)
  }
}

const loadStats = async () => {
  if (!role.value) return
  if (role.value === 'admin') { stats.value = { totalAppointments: 0, upcomingAppointments: 0, totalPatients: 0, completedTreatments: 0 }; return }
  try {
    let endpoint = role.value === 'patient' ? '/api/patient/dashboard' : '/api/doctor/dashboard'
    const res = await fetch(`${API_BASE}${endpoint}`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      if (role.value === 'patient') {
        stats.value = { totalAppointments: data.stats?.total_appointments || 0, upcomingAppointments: data.stats?.upcoming || 0, completedTreatments: 0 }
      } else if (role.value === 'doctor') {
        stats.value = { totalAppointments: data.stats?.todays_appointments || 0, upcomingAppointments: data.stats?.pending_consultations || 0, totalPatients: data.assigned_patients?.length || 0, completedTreatments: 0 }
      }
    }
  } catch (e) {
    console.error('Failed to load stats:', e)
  }
}

const saveProfile = async () => {
  saving.value = true
  try {
    let endpoint = '', payload = {}
    if (role.value === 'patient') {
      endpoint = '/api/patient/profile'
      payload = { gender: profile.value.gender, dob: profile.value.dob, blood_group: profile.value.blood_group, address: profile.value.address }
    } else if (role.value === 'doctor') {
      endpoint = '/api/doctor/profile'
      payload = { specialization: profile.value.specialization, qualification: profile.value.qualification, experience: profile.value.experience, gender: profile.value.gender }
    } else if (role.value === 'admin') {
      alert('Admin profile cannot be modified')
      saving.value = false
      return
    }
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: (role.value === 'patient' || role.value === 'doctor') ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    if (data.success) alert('Profile updated successfully!')
    else alert(data.message || 'Failed to update profile')
  } catch (e) {
    console.error('Failed to save profile:', e)
    alert('Error updating profile')
  } finally {
    saving.value = false
  }
}

const saveMedicalHistory = async () => {
  savingHistory.value = true
  try {
    const res = await fetch(`${API_BASE}/api/patient/medical-history/update`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'include',
      body: JSON.stringify(medicalHistory.value)
    })
    const data = await res.json()
    if (data.success) alert('Medical history updated successfully!')
    else alert(data.message || 'Failed to update medical history')
  } catch (e) {
    console.error('Failed to save medical history:', e)
    alert('Error updating medical history')
  } finally {
    savingHistory.value = false
  }
}

const addAvailability = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/doctor/availability/add`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'include',
      body: JSON.stringify(newAvailability.value)
    })
    const data = await res.json()
    if (data.success) {
      alert('Availability added successfully!')
      newAvailability.value = { date: '', start_time: '', end_time: '', notes: '' }
      loadAvailability()
    } else {
      alert(data.message || 'Failed to add availability')
    }
  } catch (e) {
    console.error('Failed to add availability:', e)
    alert('Error adding availability')
  }
}

const removeAvailability = async (id) => {
  if (!confirm('Are you sure you want to remove this availability?')) return
  try {
    const res = await fetch(`${API_BASE}/api/doctor/availability/${id}/delete`, { method: 'DELETE', credentials: 'include' })
    const data = await res.json()
    if (data.success) loadAvailability()
    else alert(data.message || 'Failed to remove availability')
  } catch (e) {
    console.error('Failed to remove availability:', e)
  }
}

onMounted(async () => {
  await loadProfile()
  if (role.value === 'patient') loadMedicalHistory()
  if (role.value === 'doctor') loadAvailability()
  loadStats()
})
</script>

<style scoped>
.profile-avatar {
  width: 90px; height: 90px; border-radius: 50%;
  background: linear-gradient(135deg, #20c997, #198754);
  color: #fff; font-size: 1.75rem; font-weight: bold;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 10px rgba(25, 135, 84, 0.4);
}
.card { border-radius: 1rem; }
</style>
