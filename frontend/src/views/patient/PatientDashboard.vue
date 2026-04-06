<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-tachometer-alt me-2"></i>Patient Dashboard
          </h2>
          <p class="mb-0">Welcome back, <strong>{{ currentUser?.name || 'Patient' }}</strong>! Here's your health overview.</p>
        </div>
        <div class="text-end">
          <small class="text-muted d-block">Today</small>
          <strong style="color: var(--primary);">{{ todayDate }}</strong>
        </div>
      </div>
    </div>

    <div v-if="dashboardStore.loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
      <p class="mt-3 text-muted">Loading your dashboard...</p>
    </div>

    <div v-else-if="dashboardStore.error" class="alert alert-danger">
      {{ dashboardStore.error }}
      <button class="btn btn-sm btn-outline-danger ms-3" @click="loadDashboard">Retry</button>
    </div>

    <template v-else>
      <!-- Stats -->
      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="stat-card">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="stat-label">Upcoming</p>
                  <h2 class="stat-value" style="color: var(--success);">{{ dashboardStore.stats.upcoming || 0 }}</h2>
                  <small class="text-muted">Appointments</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--success), #059669);">
                  <i class="fas fa-calendar-check fa-lg text-white"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="stat-label">Total</p>
                  <h2 class="stat-value" style="color: var(--info);">{{ dashboardStore.stats.total_appointments || 0 }}</h2>
                  <small class="text-muted">All Appointments</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--info), #2563eb);">
                  <i class="fas fa-calendar fa-lg text-white"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="stat-label">Available</p>
                  <h2 class="stat-value" style="color: var(--primary);">{{ dashboardStore.doctors?.length || 0 }}</h2>
                  <small class="text-muted">Doctors</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--primary), var(--primary-dark));">
                  <i class="fas fa-user-md fa-lg text-white"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="mb-0"><i class="fas fa-bolt me-2" style="color: var(--warning);"></i>Quick Actions</h5>
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-3 col-sm-6">
              <router-link to="/patient/doctors" class="quick-action-btn btn-qa-primary">
                <i class="fas fa-search fa-lg mb-2"></i>
                <span>Find Doctors</span>
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/patient/appointments/book" class="quick-action-btn btn-qa-success">
                <i class="fas fa-calendar-plus fa-lg mb-2"></i>
                <span>Book Appointment</span>
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <button @click="exportTreatments" class="quick-action-btn btn-qa-info">
                <i class="fas fa-file-export fa-lg mb-2"></i>
                <span>Export History</span>
              </button>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/patient/profile" class="quick-action-btn btn-qa-warning">
                <i class="fas fa-user-cog fa-lg mb-2"></i>
                <span>Update Profile</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Available Doctors -->
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="fas fa-user-md me-2" style="color: var(--primary);"></i>Available Doctors</h5>
          <router-link to="/patient/doctors" class="btn btn-sm btn-primary">View All</router-link>
        </div>
        <div class="card-body">
          <div v-if="dashboardStore.doctors && dashboardStore.doctors.length" class="row g-3">
            <div v-for="doctor in dashboardStore.doctors.slice(0, 6)" :key="doctor.id" class="col-md-4">
              <div class="doctor-card">
                <div class="d-flex align-items-center mb-3">
                  <div class="doc-avatar me-3">{{ doctor.name?.charAt(0) || 'D' }}</div>
                  <div>
                    <h6 class="mb-0 fw-semibold">{{ doctor.name }}</h6>
                    <small class="text-muted">{{ doctor.department }}</small>
                  </div>
                </div>
                <div class="doc-meta mb-3">
                  <span><i class="fas fa-graduation-cap me-1"></i>{{ doctor.qualification || 'N/A' }}</span>
                  <span><i class="fas fa-briefcase me-1"></i>{{ doctor.experience || 0 }} yrs</span>
                </div>
                <router-link :to="`/patient/appointments/book?doctor_id=${doctor.id}`"
                  class="btn btn-sm btn-outline-primary w-100">
                  <i class="fas fa-calendar-plus me-1"></i>Book
                </router-link>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4 text-muted">
            <i class="fas fa-user-md fa-3x mb-3 opacity-25"></i>
            <p class="mb-0">No doctors available at the moment</p>
          </div>
        </div>
      </div>

      <!-- Recent Appointments -->
      <div v-if="dashboardStore.appointments && dashboardStore.appointments.length" class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="fas fa-calendar-check me-2" style="color: var(--primary);"></i>Recent Appointments</h5>
          <router-link to="/patient/appointments" class="btn btn-sm btn-primary">View All</router-link>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead>
                <tr>
                  <th>Doctor</th>
                  <th>Date &amp; Time</th>
                  <th>Reason</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="apt in dashboardStore.appointments" :key="apt.id">
                  <td>{{ apt.doctor_name }}</td>
                  <td>{{ apt.date }} <small class="text-muted">{{ apt.time }}</small></td>
                  <td>{{ apt.reason || '-' }}</td>
                  <td>
                    <span class="badge" :class="{
                      'bg-success': apt.status === 'Completed',
                      'bg-warning text-dark': apt.status === 'Booked',
                      'bg-danger': apt.status === 'Cancelled'
                    }">{{ apt.status }}</span>
                  </td>
                  <td>
                    <button v-if="apt.status === 'Booked'"
                      @click="cancelAppointment(apt.id)"
                      class="btn btn-sm btn-outline-danger">
                      <i class="fas fa-times"></i>
                    </button>
                    <span v-else class="text-muted">—</span>
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
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useDashboardStore } from '@/stores/dashboard'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

const currentUser = computed(() => authStore.user)

const todayDate = computed(() =>
  new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
)

const loadDashboard = () => dashboardStore.fetchDashboard('patient')

const cancelAppointment = async (id) => {
  if (!confirm('Cancel this appointment?')) return
  console.log('Cancel appointment:', id)
  await loadDashboard()
}

const exportTreatments = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/patient/treatments/export', { credentials: 'include' })
    if (res.ok) {
      const contentType = res.headers.get('content-type') || ''
      if (contentType.includes('text/csv') || contentType.includes('application/octet-stream')) {
        const blob = await res.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `treatment_history_${new Date().toISOString().split('T')[0]}.csv`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        a.remove()
      } else {
        // JSON response (e.g. no treatments)
        const data = await res.json()
        alert(data.message || 'Export failed')
      }
    } else {
      const data = await res.json().catch(() => ({}))
      alert(data.message || 'Failed to export treatment history')
    }
  } catch (e) {
    console.error('Export error:', e)
    alert('Error exporting treatments')
  }
}

onMounted(loadDashboard)
</script>

<style scoped>
.stat-label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gray-500, #6b7280);
  margin-bottom: 0.25rem;
}

.stat-value { font-size: 2rem; font-weight: 800; margin-bottom: 0; line-height: 1; }

.stat-icon {
  width: 52px; height: 52px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,.15);
}

/* Quick action buttons */
.quick-action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 1.25rem 1rem;
  border-radius: 14px;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  border: 2px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
  background: none;
}

.quick-action-btn:hover { transform: translateY(-3px); }

.btn-qa-primary  { border-color: #6366f1; color: #6366f1; }
.btn-qa-primary:hover  { background: #6366f1; color: white; box-shadow: 0 6px 16px rgba(99,102,241,.3); }

.btn-qa-success  { border-color: #10b981; color: #10b981; }
.btn-qa-success:hover  { background: #10b981; color: white; box-shadow: 0 6px 16px rgba(16,185,129,.3); }

.btn-qa-info     { border-color: #3b82f6; color: #3b82f6; }
.btn-qa-info:hover     { background: #3b82f6; color: white; box-shadow: 0 6px 16px rgba(59,130,246,.3); }

.btn-qa-warning  { border-color: #f59e0b; color: #f59e0b; }
.btn-qa-warning:hover  { background: #f59e0b; color: white; box-shadow: 0 6px 16px rgba(245,158,11,.3); }

/* Doctor cards */
.doctor-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1.25rem;
  transition: all 0.25s ease;
  height: 100%;
}

.doctor-card:hover {
  background: white;
  border-color: #c7d2fe;
  box-shadow: 0 6px 20px rgba(99,102,241,.12);
  transform: translateY(-3px);
}

.doc-avatar {
  width: 46px; height: 46px;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 1.1rem;
  flex-shrink: 0;
}

.doc-meta {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  font-size: 0.8rem;
  color: #6b7280;
}

.doc-meta i { color: #9ca3af; }
</style>
