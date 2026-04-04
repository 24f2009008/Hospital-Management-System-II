<template>
  <div class="container-fluid">
    <!-- Page Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="mb-1">
            <i class="fas fa-tachometer-alt me-2"></i>
            Admin Dashboard
          </h2>
          <p class="mb-0">Welcome back, <strong>{{ currentUser?.name }}</strong>! Here's your hospital overview.</p>
        </div>
        <div class="text-end">
          <small class="text-muted d-block">Last Login</small>
          <strong class="text-primary">{{ formattedLastLogin }}</strong>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="dashboardStore.loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-3 text-muted">Loading dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="dashboardStore.error" class="alert alert-danger">
      {{ dashboardStore.error }}
      <button class="btn btn-sm btn-outline-danger ms-3" @click="loadDashboard">Retry</button>
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
                  <h2 class="mb-0 fw-bold text-primary-custom">{{ dashboardStore.stats.doctors }}</h2>
                  <small class="text-muted"><i class="fas fa-user-md me-1"></i>Active in system</small>
                </div>
                <div class="stat-icon stat-icon-primary">
                  <i class="fas fa-user-md fa-2x text-white"></i>
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
                  <p class="text-muted mb-2 text-uppercase stats-label">Total Patients</p>
                  <h2 class="mb-0 fw-bold text-success-custom">{{ dashboardStore.stats.patients }}</h2>
                  <small class="text-muted"><i class="fas fa-procedures me-1"></i>Registered</small>
                </div>
                <div class="stat-icon stat-icon-success">
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
                  <h2 class="mb-0 fw-bold text-info-custom">{{ dashboardStore.stats.appointments }}</h2>
                  <small class="text-muted"><i class="fas fa-calendar-check me-1"></i>All time</small>
                </div>
                <div class="stat-icon stat-icon-info">
                  <i class="fas fa-calendar-check fa-2x text-white"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0"><i class="fas fa-bolt me-2"></i>Quick Actions</h5>
            </div>
            <div class="card-body p-4">
              <div class="row g-3">
                <div class="col-md-3 col-sm-6">
                  <router-link to="/admin/addDoctor" class="btn btn-outline-primary w-100 py-3 quick-action-btn">
                    <i class="fas fa-user-plus fa-lg mb-2 d-block"></i>
                    <span class="fw-semibold">Add Doctor</span>
                  </router-link>
                </div>
                <div class="col-md-3 col-sm-6">
                  <router-link to="/admin/doctors" class="btn btn-outline-success w-100 py-3 quick-action-btn">
                    <i class="fas fa-user-md fa-lg mb-2 d-block"></i>
                    <span class="fw-semibold">View Doctors</span>
                  </router-link>
                </div>
                <div class="col-md-3 col-sm-6">
                  <router-link to="/admin/patients" class="btn btn-outline-warning w-100 py-3 quick-action-btn">
                    <i class="fas fa-users fa-lg mb-2 d-block"></i>
                    <span class="fw-semibold">View Patients</span>
                  </router-link>
                </div>
                <div class="col-md-3 col-sm-6">
                  <router-link to="/admin/search" class="btn btn-outline-info w-100 py-3 quick-action-btn">
                    <i class="fas fa-search fa-lg mb-2 d-block"></i>
                    <span class="fw-semibold">Search</span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Data -->
      <div class="row">
        <!-- Recent Doctors -->
        <div class="col-lg-6 mb-4">
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="fas fa-user-md me-2"></i>Recent Doctors</h5>
              <router-link to="/admin/doctors" class="btn btn-sm btn-outline-primary">View All</router-link>
            </div>
            <div class="card-body">
              <div v-if="dashboardStore.recentDoctors.length" class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead>
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
              <div v-else class="text-center text-muted py-4">
                <i class="fas fa-user-md fa-3x mb-3 opacity-25"></i>
                <p class="mb-0">No doctors found</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Patients -->
        <div class="col-lg-6 mb-4">
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="fas fa-procedures me-2"></i>Recent Patients</h5>
              <router-link to="/admin/patients" class="btn btn-sm btn-outline-primary">View All</router-link>
            </div>
            <div class="card-body">
              <div v-if="dashboardStore.recentPatients.length" class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="patient in dashboardStore.recentPatients" :key="patient.id">
                      <td><strong>PT{{ String(patient.id).padStart(3, '0') }}</strong></td>
                      <td>{{ patient.name }}</td>
                      <td>
                        <router-link :to="`/admin/patients/${patient.id}/treatments`" class="btn btn-sm btn-outline-info">
                          <i class="fas fa-file-medical"></i>
                        </router-link>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center text-muted py-4">
                <i class="fas fa-procedures fa-3x mb-3 opacity-25"></i>
                <p class="mb-0">No patients found</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Appointments -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="fas fa-calendar-check me-2"></i>Recent Appointments</h5>
              <router-link to="/admin/appointments" class="btn btn-sm btn-outline-primary">View All</router-link>
            </div>
            <div class="card-body">
              <div v-if="dashboardStore.recentAppointments.length" class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead>
                    <tr>
                      <th>Doctor</th>
                      <th>Patient</th>
                      <th>Date</th>
                      <th>Time</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="apt in dashboardStore.recentAppointments" :key="apt.id">
                      <td>{{ apt.doctor }}</td>
                      <td>{{ apt.patient }}</td>
                      <td>{{ apt.date }}</td>
                      <td>{{ apt.time }}</td>
                      <td>
                        <span :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center text-muted py-4">
                <i class="fas fa-calendar-check fa-3x mb-3 opacity-25"></i>
                <p class="mb-0">No appointments found</p>
              </div>
            </div>
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

const currentUser = computed(() => ({
  id: authStore.userId,
  username: authStore.username,
  role: authStore.role,
  name: authStore.username || 'Admin'
}))

const formattedLastLogin = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
})

const loadDashboard = async () => {
  await dashboardStore.fetchDashboard('admin')
}

const getStatusClass = (status) => {
  const classes = {
    'Booked': 'badge bg-primary',
    'Completed': 'badge bg-success',
    'Cancelled': 'badge bg-danger'
  }
  return classes[status] || 'badge bg-secondary'
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

.text-primary-custom { color: var(--primary); }
.text-success-custom { color: var(--success); }
.text-info-custom { color: var(--info); }

.stat-card {
  border: none;
  border-radius: 16px;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-primary { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); }
.stat-icon-success { background: linear-gradient(135deg, var(--success) 0%, #059669 100%); }
.stat-icon-info { background: linear-gradient(135deg, var(--info) 0%, #2563eb 100%); }

.quick-action-btn {
  border-width: 2px;
  transition: all 0.2s ease;
}

.quick-action-btn:hover {
  transform: translateY(-2px);
}

.page-header {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.page-header h2 {
  color: var(--gray-900);
  font-weight: 700;
  font-size: 1.875rem;
  margin-bottom: 0.5rem;
}

.page-header h2 i {
  color: var(--primary);
}

.page-header p {
  color: var(--gray-600);
  margin-bottom: 0;
  font-size: 0.9375rem;
}

.card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  background: white;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  background: white;
  border-bottom: 1px solid var(--gray-200);
  padding: 1.5rem;
  font-weight: 600;
  color: var(--gray-900);
}

.card-body {
  padding: 1.5rem;
}

.table thead th {
  background: var(--gray-50);
  border-bottom: 2px solid var(--gray-200);
  color: var(--gray-700);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  padding: 1rem 1.25rem;
  white-space: nowrap;
}

.table tbody tr {
  transition: all 0.2s ease;
  border-bottom: 1px solid var(--gray-100);
}

.table tbody tr:hover {
  background: var(--gray-50);
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
  letter-spacing: 0.025em;
}

.btn {
  border-radius: 10px;
  padding: 0.625rem 1.25rem;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  border: none;
}

.btn-outline-primary {
  border: 2px solid var(--primary);
  color: var(--primary);
  background: transparent;
}

.btn-outline-primary:hover {
  background: var(--primary);
  color: white;
}
</style>
