<template>
  <div class="container-fluid">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="h3 mb-1">Welcome, {{ currentUser?.name || 'Patient' }}!</h2>
        <p class="text-muted">Here's your health overview and quick actions.</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="dashboardStore.loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-3">Loading your dashboard...</p>
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
      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-4 mb-3">
          <div class="card stat-card border-success">
            <div class="card-body">
              <div class="d-flex align-items-center">
                <div class="flex-grow-1">
                  <h6 class="text-muted mb-1">Upcoming Appointments</h6>
                  <h3 class="text-success mb-0">
                    {{ dashboardStore.stats.upcoming || 0 }}
                  </h3>
                </div>
                <div class="flex-shrink-0">
                  <i class="fas fa-calendar-check text-success fs-2"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-3">
          <div class="card stat-card border-info">
            <div class="card-body">
              <div class="d-flex align-items-center">
                <div class="flex-grow-1">
                  <h6 class="text-muted mb-1">Total Appointments</h6>
                  <h3 class="text-info mb-0">
                    {{ dashboardStore.stats.total_appointments || 0 }}
                  </h3>
                </div>
                <div class="flex-shrink-0">
                  <i class="fas fa-calendar text-info fs-2"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-3">
          <div class="card stat-card border-primary">
            <div class="card-body">
              <div class="d-flex align-items-center">
                <div class="flex-grow-1">
                  <h6 class="text-muted mb-1">Available Doctors</h6>
                  <h3 class="text-primary mb-0">
                    {{ dashboardStore.doctors?.length || 0 }}
                  </h3>
                </div>
                <div class="flex-shrink-0">
                  <i class="fas fa-user-md text-primary fs-2"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="card-title mb-0">Quick Actions</h5>
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-3 col-sm-6">
              <router-link to="/patient/doctors" 
                class="btn btn-outline-primary w-100 py-3">
                <i class="fas fa-search me-2"></i>Find Doctors
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/patient/appointments/book" 
                class="btn btn-outline-success w-100 py-3">
                <i class="fas fa-calendar-plus me-2"></i>Book Appointment
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/patient/treatments" 
                class="btn btn-outline-info w-100 py-3">
                <i class="fas fa-file-medical me-2"></i>Medical History
              </router-link>
            </div>
            <div class="col-md-3 col-sm-6">
              <router-link to="/patient/profile" 
                class="btn btn-outline-warning w-100 py-3">
                <i class="fas fa-user-cog me-2"></i>Update Profile
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Available Doctors -->
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">Available Doctors</h5>
          <router-link to="/patient/doctors" class="btn btn-sm btn-primary">
            View All
          </router-link>
        </div>
        <div class="card-body">
          <div v-if="dashboardStore.doctors && dashboardStore.doctors.length" class="row">
            <div v-for="doctor in dashboardStore.doctors.slice(0, 6)" 
                 :key="doctor.id" 
                 class="col-md-4 mb-3">
              <div class="card doctor-card h-100">
                <div class="card-body">
                  <div class="d-flex align-items-center mb-3">
                    <div class="user-avatar me-3">
                      {{ doctor.name?.charAt(0) || 'D' }}
                    </div>
                    <div>
                      <h6 class="card-title mb-0">{{ doctor.name }}</h6>
                      <small class="text-muted">{{ doctor.department }}</small>
                    </div>
                  </div>
                  <p class="card-text small">
                    <strong>Qualification:</strong> {{ doctor.qualification }}<br>
                    <strong>Experience:</strong> {{ doctor.experience || 'N/A' }} years
                  </p>
                  <router-link 
                    :to="`/patient/appointments/book?doctor_id=${doctor.id}`"
                    class="btn btn-sm btn-outline-primary w-100">
                    Book Appointment
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4">
            <i class="fas fa-user-md text-muted fs-1 mb-3"></i>
            <h6 class="text-muted">No doctors available at the moment</h6>
          </div>
        </div>
      </div>

      <!-- Recent Appointments -->
      <div v-if="dashboardStore.appointments && dashboardStore.appointments.length" class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">Recent Appointments</h5>
          <router-link to="/patient/appointments" class="btn btn-sm btn-primary">
            View All
          </router-link>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead class="table-light">
                <tr>
                  <th>Doctor</th>
                  <th>Date & Time</th>
                  <th>Reason</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="apt in dashboardStore.appointments" :key="apt.id">
                  <td>{{ apt.doctor_name }}</td>
                  <td>{{ apt.date }} {{ apt.time }}</td>
                  <td>{{ apt.reason }}</td>
                  <td>
                    <span class="badge"
                          :class="{
                            'bg-success': apt.status === 'Completed',
                            'bg-warning text-dark': apt.status === 'Booked',
                            'bg-danger': apt.status === 'Cancelled'
                          }">
                      {{ apt.status }}
                    </span>
                  </td>
                  <td>
                    <div v-if="apt.status === 'Booked'" class="btn-group">
                      <router-link 
                        :to="`/patient/appointments/${apt.id}/reschedule`"
                        class="btn btn-sm btn-outline-primary"
                        title="Reschedule">
                        <i class="fas fa-edit"></i>
                      </router-link>
                      <!-- Cancel button can be implemented with a method -->
                      <button 
                        @click="cancelAppointment(apt.id)"
                        class="btn btn-sm btn-outline-danger"
                        title="Cancel">
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                    <span v-else class="text-muted">-</span>
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
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const router = useRouter()

const currentUser = computed(() => authStore.user)

const loadDashboard = async () => {
  await dashboardStore.fetchDashboard('patient')
}

const cancelAppointment = async (id) => {
  if (!confirm('Are you sure you want to cancel this appointment?')) return
  // TODO: Implement cancel API call if needed
  console.log('Cancel appointment:', id)
  // Refresh dashboard after cancel
  await loadDashboard()
}

onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
.stat-card {
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
}

.doctor-card {
  transition: transform 0.2s ease-in-out;
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.doctor-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
}
</style>