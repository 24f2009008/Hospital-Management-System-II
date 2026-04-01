<template>
  <div class="container-fluid">
    <!-- Page Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-tachometer-alt me-2" style="color: var(--primary);"></i>
            Admin Dashboard
          </h2>
          <p class="mb-0">Welcome back, <strong>{{ currentUser?.name || 'Admin' }}</strong>!</p>
        </div>
        <div class="text-end">
          <small class="text-muted d-block">Last Login</small>
          <strong style="color: var(--primary);">{{ formattedLastLogin }}</strong>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="dashboardStore.loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-3">Loading dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="dashboardStore.error" class="alert alert-danger">
      {{ dashboardStore.error }}
      <button class="btn btn-sm btn-outline-danger ms-3" @click="loadDashboard">
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
                  <p class="text-muted mb-2 text-uppercase stats-label">Total Doctors</p>
                  <h2 class="mb-0 fw-bold" style="color: var(--primary); font-size: 2.5rem;">
                    {{ dashboardStore.stats.doctors }}
                  </h2>
                  <small class="text-muted"><i class="fas fa-user-md me-1"></i>Active in system</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);">
                  <i class="fas fa-user-md fa-2x text-white"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Similar cards for Patients and Appointments (update numbers) -->
        <div class="col-md-4 mb-3">
          <div class="stat-card">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="text-muted mb-2 text-uppercase stats-label">Total Patients</p>
                  <h2 class="mb-0 fw-bold" style="color: var(--success); font-size: 2.5rem;">
                    {{ dashboardStore.stats.patients }}
                  </h2>
                  <small class="text-muted"><i class="fas fa-procedures me-1"></i>Registered</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--success) 0%, #059669 100%);">
                  <i class="fas fa-procedures fa-2x text-white"></i>
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
                  <p class="text-muted mb-2 text-uppercase stats-label">Total Appointments</p>
                  <h2 class="mb-0 fw-bold" style="color: var(--info); font-size: 2.5rem;">
                    {{ dashboardStore.stats.appointments }}
                  </h2>
                  <small class="text-muted"><i class="fas fa-calendar-check me-1"></i>All time</small>
                </div>
                <div class="stat-icon" style="background: linear-gradient(135deg, var(--info) 0%, #2563eb 100%);">
                  <i class="fas fa-calendar-check fa-2x text-white"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions (same as before) -->
      <!-- ... your quick actions row ... -->

      <!-- Recent Doctors -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="fas fa-user-md me-2"></i>Recent Doctors</h5>
              <router-link to="/admin/doctors" class="btn btn-sm btn-outline-primary">View All</router-link>
            </div>
            <div class="card-body">
              <div v-if="dashboardStore.recentDoctors.length" class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="table-light">
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Specialization</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="doctor in dashboardStore.recentDoctors" :key="doctor.id">
                      <td><strong>DR{{ String(doctor.id).padStart(3, '0') }}</strong></td>
                      <td>{{ doctor.name }}</td>
                      <td>{{ doctor.specialization }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center text-muted py-5">
                <i class="fas fa-user-md fa-4x mb-3 opacity-25"></i>
                <p>No doctors found</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Patients (similar structure) -->
      <!-- You can add Recent Appointments too using recentAppointments -->

    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useDashboardStore } from '@/stores/dashboard'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const router = useRouter()

const currentUser = computed(() => authStore.user)

const formattedLastLogin = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
})

const loadDashboard = async () => {
  await dashboardStore.fetchDashboard('admin')
}

onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
.stats-label {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Optional: Make cards look better */
.stat-card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}
</style>