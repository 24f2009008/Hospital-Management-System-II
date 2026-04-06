<template>
  <div class="container-fluid">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-tachometer-alt me-2"></i>Doctor Dashboard
          </h2>
          <p class="mb-0">Welcome back, <strong>Dr. {{ currentUser?.name || 'Doctor' }}</strong>!</p>
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

    <div v-else-if="dashboardStore.error" class="alert alert-danger d-flex justify-content-between align-items-center">
      <span>{{ dashboardStore.error }}</span>
      <button class="btn btn-sm btn-outline-danger" @click="loadDashboard">Retry</button>
    </div>

    <template v-else>
      <!-- Stats -->
      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="stat-card">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="stat-label">My Patients</p>
                  <h2 class="stat-value" style="color: var(--primary);">{{ totalPatients }}</h2>
                  <small class="text-muted">Total assigned</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--primary), var(--primary-dark));">
                  <i class="fas fa-users fa-lg text-white"></i>
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
                  <p class="stat-label">Today</p>
                  <h2 class="stat-value" style="color: var(--info);">{{ dashboardStore.stats.todays_appointments || 0 }}</h2>
                  <small class="text-muted">Appointments</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--info), #2563eb);">
                  <i class="fas fa-calendar-day fa-lg text-white"></i>
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
                  <p class="stat-label">Upcoming Week</p>
                  <h2 class="stat-value" style="color: var(--warning);">{{ dashboardStore.stats.upcoming_appointments || 0 }}</h2>
                  <small class="text-muted">Next 7 days</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--warning), #d97706);">
                  <i class="fas fa-calendar-check fa-lg text-white"></i>
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
              <router-link to="/doctor/appointments" class="quick-action-btn btn-qa-primary">
                <i class="fas fa-calendar-check fa-lg mb-2"></i>
                <span>View Appointments</span>
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/doctor/patients" class="quick-action-btn btn-qa-success">
                <i class="fas fa-users fa-lg mb-2"></i>
                <span>My Patients</span>
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/doctor/availability" class="quick-action-btn btn-qa-info">
                <i class="fas fa-calendar-alt fa-lg mb-2"></i>
                <span>Set Availability</span>
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/doctor/profile" class="quick-action-btn btn-qa-warning">
                <i class="fas fa-user-cog fa-lg mb-2"></i>
                <span>My Profile</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Patients -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="fas fa-users me-2" style="color: var(--primary);"></i>Recent Patients</h5>
          <router-link to="/doctor/patients" class="btn btn-sm btn-primary">View All</router-link>
        </div>
        <div class="card-body p-0">
          <div v-if="recentPatients.length" class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="patient in recentPatients" :key="patient.id">
                  <td><strong>PT{{ String(patient.id).padStart(3, '0') }}</strong></td>
                  <td>{{ patient.name }}</td>
                  <td><span class="badge bg-success">Active</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center text-muted py-5">
            <i class="fas fa-users fa-3x mb-3 opacity-25"></i>
            <p class="mb-0">No patients yet. Your list will appear here once you start seeing patients.</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useDashboardStore } from '@/stores/dashboard'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const recentPatients = ref([])

const currentUser = computed(() => authStore.user)

const todayDate = computed(() =>
  new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
)

const totalPatients = computed(() => recentPatients.value.length)

const loadDashboard = async () => {
  await dashboardStore.fetchDashboard('doctor')
  // Load patients separately for the recent list
  try {
    const res = await fetch('http://127.0.0.1:5000/api/doctor/patients', { credentials: 'include' })
    const data = await res.json()
    if (data.success) recentPatients.value = (data.patients || []).slice(0, 5)
  } catch (e) {
    console.error('Failed to load patients:', e)
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
  color: #6b7280;
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

.btn-qa-primary { border-color: #6366f1; color: #6366f1; }
.btn-qa-primary:hover { background: #6366f1; color: white; box-shadow: 0 6px 16px rgba(99,102,241,.3); }

.btn-qa-success { border-color: #10b981; color: #10b981; }
.btn-qa-success:hover { background: #10b981; color: white; box-shadow: 0 6px 16px rgba(16,185,129,.3); }

.btn-qa-info { border-color: #3b82f6; color: #3b82f6; }
.btn-qa-info:hover { background: #3b82f6; color: white; box-shadow: 0 6px 16px rgba(59,130,246,.3); }

.btn-qa-warning { border-color: #f59e0b; color: #f59e0b; }
.btn-qa-warning:hover { background: #f59e0b; color: white; box-shadow: 0 6px 16px rgba(245,158,11,.3); }
</style>
