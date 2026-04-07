<template>
  <div class="layout">
    <!-- Mobile overlay -->
    <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false"></div>

    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'sidebar-open': sidebarOpen }">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <i class="fas fa-hospital-alt"></i>
        </div>
        <div>
          <h4>{{ roleName }}</h4>
          <span class="sidebar-subtitle">Portal</span>
        </div>
        <button class="sidebar-close d-lg-none" @click="sidebarOpen = false">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="sidebar-nav">
        <div class="nav-section-title">Main Menu</div>
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="nav-link"
          :class="{ active: isActive(link.to) }"
          @click="sidebarOpen = false">
          <i :class="link.icon"></i>
          <span>{{ link.label }}</span>
        </router-link>

        <div 
          v-if="role !== 'admin'"
          class="nav-section-title">Settings</div>
        <router-link
          v-if="role !== 'admin'"
          :to="profileRoute"
          class="nav-link"
          :class="{ active: isActive(profileRoute) }"
          @click="sidebarOpen = false">
          <i class="fas fa-user-cog"></i>
          <span>My Profile</span>
        </router-link>

        <router-link
          v-if="role === 'doctor'"
          to="/doctor/availability"
          class="nav-link"
          :class="{ active: isActive('/doctor/availability') }"
          @click="sidebarOpen = false">
          <i class="fas fa-calendar-alt"></i>
          <span>Availability</span>
        </router-link>
      </div>

      <div class="user-info-card">
        <div class="d-flex align-items-center gap-3 mb-3">
          <div class="user-avatar">{{ userInitials }}</div>
          <div class="user-details">
            <div class="user-name">{{ currentUser?.name || `${roleName} User` }}</div>
            <div class="user-role">{{ roleName }}</div>
          </div>
        </div>
        <router-link to="/logout" class="btn-logout">
          <i class="fas fa-sign-out-alt me-2"></i>Logout
        </router-link>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Mobile topbar -->
      <div class="mobile-topbar d-lg-none">
        <button class="topbar-toggle" @click="sidebarOpen = true">
          <i class="fas fa-bars"></i>
        </button>
        <span class="topbar-title">
          <i class="fas fa-hospital-alt me-2"></i>HMS {{ roleName }}
        </span>
        <div class="user-avatar-sm">{{ userInitials }}</div>
      </div>

      <div class="content-wrapper">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const sidebarOpen = ref(false)

const props = defineProps({
  role: {
    type: String,
    required: true,
    validator: (v) => ['admin', 'doctor', 'patient'].includes(v)
  }
})

const currentUser = computed(() => ({
  id: authStore.userId,
  username: authStore.username,
  role: authStore.role,
  name: authStore.username || 'User'
}))

const roleName = computed(() => props.role.charAt(0).toUpperCase() + props.role.slice(1))

const userInitials = computed(() => {
  const name = currentUser.value?.name || 'User'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const navLinks = computed(() => {
  if (props.role === 'admin') {
    return [
      { to: '/admin/dashboard',    label: 'Dashboard',        icon: 'fas fa-tachometer-alt' },
      { to: '/admin/doctors',      label: 'Manage Doctors',   icon: 'fas fa-user-md' },
      { to: '/admin/patients',     label: 'Manage Patients',  icon: 'fas fa-procedures' },
      { to: '/admin/appointments', label: 'Appointments',     icon: 'fas fa-calendar-check' },
      { to: '/admin/search',       label: 'Search',           icon: 'fas fa-search' }
    ]
  } else if (props.role === 'doctor') {
    return [
      { to: '/doctor/dashboard',    label: 'Dashboard',     icon: 'fas fa-tachometer-alt' },
      { to: '/doctor/appointments', label: 'Appointments',  icon: 'fas fa-calendar-check' },
      { to: '/doctor/patients',     label: 'My Patients',   icon: 'fas fa-users' },
      { to: '/doctor/treatments',   label: 'Treatments',    icon: 'fas fa-file-medical' },
    ]
  } else {
    return [
      { to: '/patient/dashboard',           label: 'Dashboard',        icon: 'fas fa-tachometer-alt' },
      { to: '/patient/appointments',        label: 'My Appointments',  icon: 'fas fa-calendar-check' },
      { to: '/patient/appointments/book',   label: 'Book Appointment', icon: 'fas fa-calendar-plus' },
      { to: '/patient/history',             label: 'Medical History',  icon: 'fas fa-file-medical-alt' },
      { to: '/patient/departments',          label: 'Departments',     icon: 'fas fa-hospital' },
      { to: '/patient/doctors',              label: 'Find Doctors',    icon: 'fas fa-user-md' }
    ]
  }
})

const profileRoute = computed(() => `/${props.role}/profile`)
const isActive = (path) => route.path === path
</script>

<style scoped>
/* ── Layout shell ─────────────────────────────────────────── */
.layout {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ──────────────────────────────────────────────── */
.sidebar {
  position: fixed;
  top: 0; left: 0;
  height: 100vh;
  width: 268px;
  background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
  box-shadow: 4px 0 24px rgba(0,0,0,.18);
  z-index: 1040;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  z-index: 1039;
  backdrop-filter: blur(2px);
}

/* ── Sidebar Header ───────────────────────────────────────── */
.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.75rem 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,.08);
}

.sidebar-logo {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; color: white;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(99,102,241,.4);
}

.sidebar-header h4 {
  color: white;
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
}

.sidebar-subtitle {
  color: rgba(255,255,255,.45);
  font-size: 0.75rem;
  font-weight: 500;
}

.sidebar-close {
  margin-left: auto;
  background: none;
  border: none;
  color: rgba(255,255,255,.5);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.25rem;
}

/* ── Nav ──────────────────────────────────────────────────── */
.sidebar-nav {
  flex: 1;
  padding: 0.75rem 0;
}

.nav-section-title {
  color: rgba(255,255,255,.35);
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0 1.5rem;
  margin: 1.25rem 0 0.5rem;
}

.sidebar .nav-link {
  color: rgba(255,255,255,.65);
  padding: 0.75rem 1.25rem;
  margin: 0.125rem 0.75rem;
  border-radius: 10px;
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.sidebar .nav-link i {
  width: 18px;
  text-align: center;
  font-size: 1rem;
  opacity: 0.8;
}

.sidebar .nav-link:hover {
  background: rgba(99,102,241,.15);
  color: white;
}

.sidebar .nav-link:hover i { opacity: 1; }

.sidebar .nav-link.active {
  background: linear-gradient(90deg, rgba(99,102,241,.25), rgba(139,92,246,.12));
  color: white;
  font-weight: 600;
  border-left: 3px solid #6366f1;
  padding-left: calc(1.25rem - 3px);
}

.sidebar .nav-link.active i { opacity: 1; color: #a5b4fc; }

/* ── User card ────────────────────────────────────────────── */
.user-info-card {
  margin: 0.75rem;
  padding: 1rem 1.125rem;
  background: rgba(255,255,255,.05);
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,.08);
}

.user-avatar {
  width: 42px; height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(99,102,241,.3);
}

.user-name {
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  line-height: 1.3;
}

.user-role {
  color: rgba(255,255,255,.5);
  font-size: 0.75rem;
}

.btn-logout {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.55rem;
  background: rgba(239,68,68,.1);
  border: 1px solid rgba(239,68,68,.2);
  color: rgba(255,255,255,.75);
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn-logout:hover {
  background: rgba(239,68,68,.25);
  border-color: rgba(239,68,68,.4);
  color: white;
}

/* ── Main content ─────────────────────────────────────────── */
.main-content {
  margin-left: 268px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
  flex: 1;
}

.content-wrapper {
  padding: 2rem;
  animation: fadeInUp 0.35s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Mobile topbar ────────────────────────────────────────── */
.mobile-topbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1.25rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar-toggle {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #374151;
  cursor: pointer;
  padding: 0.25rem;
}

.topbar-title {
  font-weight: 700;
  color: #111827;
  font-size: 1rem;
  flex: 1;
}

.user-avatar-sm {
  width: 34px; height: 34px;
  border-radius: 10px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 991px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar.sidebar-open {
    transform: translateX(0);
  }
  .main-content {
    margin-left: 0;
  }
  .content-wrapper {
    padding: 1.25rem;
  }
}
</style>
