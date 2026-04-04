<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-calendar-alt me-2" style="color: var(--primary);"></i>
            My Availability
          </h2>
          <p class="text-muted mb-0">Manage your appointment availability schedule</p>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-clock me-2"></i>Weekly Schedule
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead class="table-light">
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
                  <tr v-for="slot in availability" :key="slot.id || slot.date">
                    <td><strong>{{ formatDay(slot.date) }}</strong></td>
                    <td>{{ slot.date }}</td>
                    <td>{{ slot.start_time || '--:--' }}</td>
                    <td>{{ slot.end_time || '--:--' }}</td>
                    <td>
                      <span class="badge" :class="slot.available ? 'bg-success' : 'bg-secondary'">
                        {{ slot.available ? 'Available' : 'Not Available' }}
                      </span>
                    </td>
                    <td>
                      <button 
                        v-if="slot.available" 
                        class="btn btn-sm btn-outline-danger" 
                        @click="removeAvailability(slot.id)"
                      >
                        <i class="fas fa-trash me-1"></i>Remove
                      </button>
                      <span v-else class="text-muted small">No action</span>
                    </td>
                  </tr>
                  <tr v-if="availability.length === 0">
                    <td colspan="6" class="text-center text-muted py-4">
                      <i class="fas fa-calendar-times fa-2x mb-2"></i>
                      <p class="mb-0">No availability set. Add your schedule below.</p>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-6">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-plus-circle me-2"></i>Add Single Day Availability
            </h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="addAvailability">
              <div class="row g-3">
                <div class="col-md-4">
                  <label class="form-label">Date <span class="text-danger">*</span></label>
                  <input type="date" class="form-control" v-model="newAvailability.date" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Start Time <span class="text-danger">*</span></label>
                  <input type="time" class="form-control" v-model="newAvailability.start_time" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">End Time <span class="text-danger">*</span></label>
                  <input type="time" class="form-control" v-model="newAvailability.end_time" required>
                </div>
                <div class="col-md-2 d-flex align-items-end">
                  <button type="submit" class="btn btn-primary w-100">
                    <i class="fas fa-plus me-1"></i>Add
                  </button>
                </div>
              </div>
              <div class="mt-3">
                <label class="form-label">Notes (Optional)</label>
                <input type="text" class="form-control" v-model="newAvailability.notes" placeholder="E.g., Morning shift, Emergency only...">
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-6">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-calendar-week me-2"></i>Quick Add Week
            </h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="addWeekAvailability">
              <div class="row g-3">
                <div class="col-md-4">
                  <label class="form-label">Start Date</label>
                  <input type="date" class="form-control" v-model="weekAvailability.start_date" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Start Time</label>
                  <input type="time" class="form-control" v-model="weekAvailability.start_time" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">End Time</label>
                  <input type="time" class="form-control" v-model="weekAvailability.end_time" required>
                </div>
                <div class="col-md-2 d-flex align-items-end">
                  <button type="submit" class="btn btn-success w-100">
                    <i class="fas fa-plus me-1"></i>Add Week
                  </button>
                </div>
              </div>
              <div class="mt-3">
                <label class="form-label">Select Days</label>
                <div class="d-flex flex-wrap gap-2">
                  <div class="form-check" v-for="day in weekDays" :key="day.value">
                    <input class="form-check-input" type="checkbox" :value="day.value" v-model="weekAvailability.days" :id="'day-'+day.value">
                    <label class="form-check-label" :for="'day-'+day.value">{{ day.label }}</label>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom">
            <h5 class="card-title mb-0" style="color: var(--primary);">
              <i class="fas fa-info-circle me-2"></i>Instructions
            </h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4">
                <h6><i class="fas fa-clock text-primary me-2"></i>Set Your Hours</h6>
                <p class="text-muted small">Specify the start and end times for when you're available to see patients.</p>
              </div>
              <div class="col-md-4">
                <h6><i class="fas fa-calendar-week text-success me-2"></i>Weekly Schedule</h6>
                <p class="text-muted small">Use "Add Week" to quickly set availability for multiple days at once.</p>
              </div>
              <div class="col-md-4">
                <h6><i class="fas fa-trash text-danger me-2"></i>Manage Slots</h6>
                <p class="text-muted small">Remove availability by clicking the trash icon. Patients won't see unavailable slots.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:5000'

const availability = ref([])
const newAvailability = ref({ date: '', start_time: '', end_time: '', notes: '' })
const weekAvailability = ref({ start_date: '', start_time: '', end_time: '', days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] })
const weekDays = [
  { value: 'Monday', label: 'Mon' },
  { value: 'Tuesday', label: 'Tue' },
  { value: 'Wednesday', label: 'Wed' },
  { value: 'Thursday', label: 'Thu' },
  { value: 'Friday', label: 'Fri' },
  { value: 'Saturday', label: 'Sat' },
  { value: 'Sunday', label: 'Sun' }
]

const formatDay = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { weekday: 'long' })
}

const loadAvailability = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/doctor/availability`, { credentials: 'include' })
    const data = await res.json()
    if (data.success) {
      availability.value = data.availability || []
    }
  } catch (e) {
    console.error('Failed to load availability:', e)
  }
}

const addAvailability = async () => {
  if (!newAvailability.value.date || !newAvailability.value.start_time || !newAvailability.value.end_time) {
    alert('Please fill in all required fields')
    return
  }
  try {
    const res = await fetch(`${API_BASE}/api/doctor/availability/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
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

const addWeekAvailability = async () => {
  if (!weekAvailability.value.start_date || !weekAvailability.value.start_time || !weekAvailability.value.end_time) {
    alert('Please fill in all required fields')
    return
  }
  if (weekAvailability.value.days.length === 0) {
    alert('Please select at least one day')
    return
  }
  
  let addedCount = 0
  const startDate = new Date(weekAvailability.value.start_date)
  
  for (let i = 0; i < 14; i++) {
    const currentDate = new Date(startDate)
    currentDate.setDate(startDate.getDate() + i)
    const dayName = currentDate.toLocaleDateString('en-US', { weekday: 'long' })
    
    if (weekAvailability.value.days.includes(dayName)) {
      try {
        const res = await fetch(`${API_BASE}/api/doctor/availability/add`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
            date: currentDate.toISOString().split('T')[0],
            start_time: weekAvailability.value.start_time,
            end_time: weekAvailability.value.end_time,
            notes: 'Weekly schedule'
          })
        })
        const data = await res.json()
        if (data.success) addedCount++
      } catch (e) {
        console.error('Failed to add availability:', e)
      }
    }
  }
  
  alert(`Added ${addedCount} availability slots!`)
  loadAvailability()
}

const removeAvailability = async (id) => {
  if (!confirm('Are you sure you want to remove this availability?')) return
  try {
    const res = await fetch(`${API_BASE}/api/doctor/availability/${id}/delete`, {
      method: 'DELETE',
      credentials: 'include'
    })
    const data = await res.json()
    if (data.success) {
      loadAvailability()
    } else {
      alert(data.message || 'Failed to remove availability')
    }
  } catch (e) {
    console.error('Failed to remove availability:', e)
  }
}

onMounted(() => {
  loadAvailability()
})
</script>

<style scoped>
.card { border-radius: 1rem; }
.table th { font-weight: 600; }
</style>
