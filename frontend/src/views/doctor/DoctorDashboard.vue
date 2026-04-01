<template>
  <div class="container-fluid">
    <!-- Page Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-tachometer-alt me-2" style="color: var(--primary);"></i>
            Doctor Dashboard
          </h2>
          <p class="mb-0">
            Welcome back, <strong>Dr. {{ currentUser?.name || 'Doctor' }}</strong>! 
            Here's your overview.
          </p>
        </div>
        <div class="text-end">
          <small class="text-muted d-block">Today</small>
          <strong style="color: var(--primary);">{{ todayDate }}</strong>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="dashboardStore.loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-3">Loading your dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="dashboardStore.error" class="alert alert-danger d-flex justify-content-between align-items-center">
      <span>{{ dashboardStore.error }}</span>
      <button class="btn btn-sm btn-outline-danger" @click="loadDashboard">
        Retry
      </button>
    </div>

    <!-- Main Content -->
    <template v-else>
      <!-- Statistics Cards -->
      <div class="row mb-4">
        <div class="col-md-4 mb-3">
          <div class="stat-card">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="text-muted mb-2 text-uppercase small fw-semibold">My Patients</p>
                  <h2 class="mb-0 fw-bold text-primary">
                    {{ dashboardStore.stats.assigned_patients?.length || 0 }}
                  </h2>
                  <small class="text-muted">
                    <i class="fas fa-users me-1"></i>Total patients
                  </small>
                </div>
                <div class="stat-icon bg-primary bg-gradient text-white">
                  <i class="fas fa-users fa-2x"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-3">
          <div class="stat-card">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="text-muted mb-2 text-uppercase small fw-semibold">Today's Appointments</p>
                  <h2 class="mb-0 fw-bold text-info">
                    {{ dashboardStore.stats.todays_appointments || 0 }}
                  </h2>
                  <small class="text-muted">
                    <i class="fas fa-calendar-day me-1"></i>Scheduled today
                  </small>
                </div>
                <div class="stat-icon bg-info bg-gradient text-white">
                  <i class="fas fa-calendar-day fa-2x"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-3">
          <div class="stat-card">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="text-muted mb-2 text-uppercase small fw-semibold">Upcoming Week</p>
                  <h2 class="mb-0 fw-bold text-warning">
                    {{ dashboardStore.stats.upcoming_appointments || 0 }}
                  </h2>
                  <small class="text-muted">
                    <i class="fas fa-calendar-check me-1"></i>Next 7 days
                  </small>
                </div>
                <div class="stat-icon bg-warning bg-gradient text-white">
                  <i class="fas fa-calendar-check fa-2x"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="mb-0">
            <i class="fas fa-bolt me-2"></i>Quick Actions
          </h5>
        </div>
        <div class="card-body p-4">
          <div class="row g-3">
            <div class="col-md-3 col-sm-6">
              <router-link to="/doctor/appointments" 
                class="btn btn-outline-primary w-100 py-3 fw-semibold border-2 d-flex flex-column align-items-center">
                <i class="fas fa-calendar-check fa-lg mb-2"></i>
                View Appointments
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/doctor/patients" 
                class="btn btn-outline-success w-100 py-3 fw-semibold border-2 d-flex flex-column align-items-center">
                <i class="fas fa-users fa-lg mb-2"></i>
                My Patients
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/doctor/availability" 
                class="btn btn-outline-info w-100 py-3 fw-semibold border-2 d-flex flex-column align-items-center">
                <i class="fas fa-calendar-alt fa-lg mb-2"></i>
                Set Availability
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/doctor/profile" 
                class="btn btn-outline-warning w-100 py-3 fw-semibold border-2 d-flex flex-column align-items-center">
                <i class="fas fa-user-cog fa-lg mb-2"></i>
                My Profile
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Patients -->
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">
            <i class="fas fa-users me-2"></i>Recent Patients
          </h5>
          <router-link to="/doctor/patients" class="btn btn-sm btn-outline-success">
            View All
          </router-link>
        </div>
        <div class="card-body">
          <div v-if="dashboardStore.assigned_patients && dashboardStore.assigned_patients.length" class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="patient in dashboardStore.assigned_patients" :key="patient.id">
                  <td>
                    <strong>PT{{ String(patient.id).padStart(3, '0') }}</strong>
                  </td>
                  <td>{{ patient.name }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center text-muted py-5">
            <i class="fas fa-users fa-4x mb-3 opacity-25"></i>
            <h5>No Patients Yet</h5>
            <p>Your patient list will appear here once you start seeing patients.</p>
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

const todayDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
})

const loadDashboard = async () => {
  await dashboardStore.fetchDashboard('doctor')
}

onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
.page-header {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(13, 110, 253, 0.1);
  margin-bottom: 2rem;
}

.stat-card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease;
  background: white;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.btn.border-2 {
  border-width: 2px !important;
}
</style>