<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

// Initialize auth store
const authStore = useAuthStore()
const route = useRoute()

// Check active route for navigation highlighting
const isActive = (path) => route.path === path

// Current user info
const currentUser = computed(() => authStore.user)

const currentUserInitial = computed(() => {
  const name = currentUser.value?.name || ''
  return name ? name.charAt(0).toUpperCase() : 'P'
})
</script>

<template>
  <div class="patient-layout d-flex">

    <!-- Sidebar -->
    <div class="sidebar" id="sidebar">
      <!-- Sidebar Header -->
      <div class="sidebar-header">
        <h4>
          <i class="fas fa-user-injured"></i>
          Patient Portal
        </h4>
      </div>

      <!-- Navigation -->
      <div class="sidebar-nav">
        <div class="nav-section-title">Main Menu</div>
        
        <router-link 
          to="/patient/dashboard" 
          class="nav-link"
          :class="{ active: isActive('/patient/dashboard') }">
          <i class="fas fa-tachometer-alt"></i>
          <span>Dashboard</span>
        </router-link>

        <router-link 
          to="/patient/appointments" 
          class="nav-link"
          :class="{ active: isActive('/patient/appointments') }">
          <i class="fas fa-calendar-check"></i>
          <span>My Appointments</span>
        </router-link>

        <router-link 
          to="/patient/appointments/book" 
          class="nav-link"
          :class="{ active: isActive('/patient/appointments/book') }">
          <i class="fas fa-calendar-plus"></i>
          <span>Book Appointment</span>
        </router-link>

        <router-link 
          to="/patient/doctors" 
          class="nav-link"
          :class="{ active: isActive('/patient/doctors') }">
          <i class="fas fa-search"></i>
          <span>Find Doctors</span>
        </router-link>

        <div class="nav-section-title">Health Records</div>

        <router-link 
          to="/patient/treatments" 
          class="nav-link"
          :class="{ active: isActive('/patient/treatments') }">
          <i class="fas fa-file-medical"></i>
          <span>Treatment History</span>
        </router-link>

        <router-link 
          to="/patient/profile" 
          class="nav-link"
          :class="{ active: isActive('/patient/profile') }">
          <i class="fas fa-user-cog"></i>
          <span>My Profile</span>
        </router-link>
      </div>

      <!-- User Info Card -->
      <div class="user-info-card">
        <div class="d-flex align-items-center mb-3">
          <div class="user-avatar me-3">
            {{ currentUserInitial }}
          </div>
          <div class="user-details">
            <div class="user-name">{{ currentUser?.name || 'Patient' }}</div>
            <div class="user-role">Patient</div>
          </div>
        </div>
        <router-link to="/logout" class="btn btn-logout">
          <i class="fas fa-sign-out-alt me-2"></i>Logout
        </router-link>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Notifications / Flash Messages Slot -->
      <slot name="notifications"></slot>

      <!-- Page Content -->
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
/* ===== Green/Emerald Theme - Patient Portal ===== */
:root {
  --primary: #10b981;
  --primary-dark: #059669;
  --primary-light: #34d399;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  color: #1f2937;
  font-size: 14px;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 280px;
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12);
  z-index: 1040;
  overflow-y: auto;
}

.sidebar-header {
  padding: 2rem 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.sidebar-header h4 {
  color: white;
  font-size: 1.35rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar-header h4 i {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-dark) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
}

.nav-section-title {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 1rem 1.5rem 0.5rem;
  font-weight: 500;
}

.nav-link {
  color: rgba(255, 255, 255, 0.75);
  padding: 0.875rem 1.5rem;
  margin: 0.25rem 1rem;
  border-radius: 10px;
  transition: all 0.25s ease;
  font-weight: 500;
  font-size: 0.9375rem;
  display: flex;
  align-items: center;
  gap: 0.875rem;
  text-decoration: none;
}

.nav-link i {
  width: 20px;
  text-align: center;
  font-size: 1.1rem;
}

.nav-link:hover {
  background: rgba(16, 185, 129, 0.18);
  color: white;
  transform: translateX(2px);
}

.nav-link.active {
  background: linear-gradient(90deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.2) 100%);
  color: white;
  font-weight: 600;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.2);
  position: relative;
}

.nav-link.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 60%;
  width: 3px;
  background: linear-gradient(180deg, var(--primary-light) 0%, var(--primary) 100%);
  border-radius: 0 3px 3px 0;
}

.user-info-card {
  margin: 1.5rem 1rem 1.5rem;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-light), var(--primary-dark));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.125rem;
}

.user-name {
  color: white;
  font-weight: 600;
  font-size: 0.9375rem;
}

.user-role {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8125rem;
}

.btn-logout {
  margin-top: 1rem;
  width: 100%;
  padding: 0.625rem;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.25s ease;
}

.btn-logout:hover {
  background: rgba(16, 185, 129, 0.3);
}

.main-content {
  margin-left: 280px;
  min-height: 100vh;
  padding: 2.25rem;
  background: linear-gradient(135deg, #f9fbff 0%, #edf3ff 100%);
}

/* Responsive */
@media (max-width: 992px) {
  .sidebar {
    left: -280px;
  }
  .main-content {
    margin-left: 0;
    padding: 1.25rem;
    padding-top: 5rem;
  }
}
</style>