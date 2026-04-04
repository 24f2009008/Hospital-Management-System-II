<template>
  <div class="layout d-flex">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h4>
          <i class="fas fa-user-shield"></i>
          {{ roleName }} Portal
        </h4>
      </div>

      <div class="sidebar-nav">
        <div class="nav-section-title">Main Menu</div>
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="nav-link"
          :class="{ active: isActive(link.to) }">
          <i :class="link.icon"></i>
          <span>{{ link.label }}</span>
        </router-link>

        <div class="nav-section-title">Settings</div>
        <router-link            
          :to="profileRoute"
          class="nav-link"
          :class="{ active: isActive(profileRoute) }">
          <i class="fas fa-user-cog"></i>
          <span>My Profile</span>
        </router-link>

        <router-link
          v-if="role === 'doctor'"
          to="/doctor/availability"
          class="nav-link"
          :class="{ active: isActive('/doctor/availability') }">
          <i class="fas fa-calendar-alt"></i>
          <span>Availability</span>
        </router-link>
      </div>

      <!-- User Info Card -->
      <div class="user-info-card">
        <div class="d-flex align-items-center mb-3">
          <div class="user-avatar">{{ userInitials }}</div>
          <div class="user-details">
            <div class="user-name">{{ currentUser?.name || `${roleName} User` }}</div>
            <div class="user-role">{{ roleName }}</div>
          </div>
        </div>
        <router-link to="/logout" class="btn btn-logout">
          <i class="fas fa-sign-out-alt me-2"></i>Logout
        </router-link>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content" id="mainContent">
      <slot name="notifications"></slot>
      <slot name="title"></slot>
      <slot name="actions"></slot>
      <div class="content-wrapper">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const props = defineProps({
  role: {
    type: String,
    required: true,
    validator: (value) => ['admin', 'doctor', 'patient'].includes(value)
  }
})

const currentUser = computed(() => ({
  id: authStore.userId,
  username: authStore.username,
  role: authStore.role,
  name: authStore.username || 'User'
}))

const roleName = computed(() => 
  props.role.charAt(0).toUpperCase() + props.role.slice(1)
)

const userInitials = computed(() => {
  const name = currentUser.value?.name || 'User'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const navLinks = computed(() => {
  if (props.role === 'admin') {
    return [
      { to: '/admin/dashboard', label: 'Dashboard', icon: 'fas fa-tachometer-alt' },
      { to: '/admin/doctors', label: 'Manage Doctors', icon: 'fas fa-user-md' },
      { to: '/admin/patients', label: 'Manage Patients', icon: 'fas fa-procedures' },
      { to: '/admin/appointments', label: 'Appointments', icon: 'fas fa-calendar-check' },
      { to: '/admin/treatments', label: 'Treatment Records', icon: 'fas fa-file-medical' },
      { to: '/admin/departments', label: 'Departments', icon: 'fas fa-building' },
      { to: '/admin/search', label: 'Search', icon: 'fas fa-search' }
    ]
  } 
  else if (props.role === 'doctor') {
    return [
      { to: '/doctor/dashboard', label: 'Dashboard', icon: 'fas fa-tachometer-alt' },
      { to: '/doctor/appointments', label: 'Appointments', icon: 'fas fa-calendar-check' },
      { to: '/doctor/patients', label: 'My Patients', icon: 'fas fa-users' },
      { to: '/doctor/treatments', label: 'Treatments', icon: 'fas fa-file-medical' },
      { to: '/doctor/search', label: 'Search', icon: 'fas fa-search' }
    ]
  } 
  else if (props.role === 'patient') {
    return [
      { to: '/patient/dashboard', label: 'Dashboard', icon: 'fas fa-tachometer-alt' },
      { to: '/patient/appointments', label: 'My Appointments', icon: 'fas fa-calendar-check' },
      { to: '/patient/appointments/book', label: 'Book Appointment', icon: 'fas fa-calendar-plus' },
      { to: '/patient/doctors', label: 'Find Doctors', icon: 'fas fa-user-md' },
      { to: '/patient/treatments', label: 'My Treatments', icon: 'fas fa-file-medical' }
    ]
  }
  return []
})

const profileRoute = computed(() => `/${props.role}/profile`)

const isActive = (path) => route.path === path || route.path.startsWith(path)
</script>

<style scoped>
.layout { min-height: 100vh; }

:root {
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --primary-light: #818cf8;
  --secondary: #8b5cf6;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
  --dark: #1e293b;
  --light: #f8fafc;
  --white: #ffffff;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
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
  padding: 2rem 1.5rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h4 {
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar-header h4 i {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
}

.nav-section-title {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0 1.5rem;
  margin: 1.5rem 0 0.75rem;
}

.sidebar .nav-link {
  color: rgba(255, 255, 255, 0.7);
  padding: 0.875rem 1.5rem;
  margin: 0.25rem 1rem;
  border-radius: 10px;
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 0.9375rem;
  display: flex;
  align-items: center;
  gap: 0.875rem;
  text-decoration: none;
}

.sidebar .nav-link i {
  width: 20px;
  text-align: center;
  font-size: 1.125rem;
}

.sidebar .nav-link:hover {
  background: rgba(99, 102, 241, 0.15);
  color: white;
}

.sidebar .nav-link.active {
  background: linear-gradient(90deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.1) 100%);
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.user-info-card {
  margin: 1.5rem 1rem 1rem;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.125rem;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.user-details {
  flex: 1;
}

.user-name {
  color: white;
  font-weight: 600;
  font-size: 0.9375rem;
  margin-bottom: 0.25rem;
}

.user-role {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8125rem;
}

.btn-logout {
  margin-top: 1rem;
  width: 100%;
  padding: 0.625rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
  display: block;
  text-align: center;
}

.btn-logout:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.3);
  color: white;
}

.main-content {
  margin-left: 280px;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.content-wrapper {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 992px) {
  .sidebar {
    left: -280px;
  }
  .main-content {
    margin-left: 0;
    padding: 1rem;
    padding-top: 4rem;
  }
}
</style>
