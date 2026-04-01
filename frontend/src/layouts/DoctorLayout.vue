<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

// Check if current route matches for active link
const isActive = (path) => route.path === path
</script>

<template>
  <div class="admin-layout d-flex">

    <!-- Sidebar -->
    <div class="sidebar" id="sidebar">
      <!-- Sidebar Header -->
      <div class="sidebar-header">
        <h4>
          <i class="fas fa-user-md"></i>
          Doctor Portal
        </h4>
      </div>

      <!-- Navigation -->
      <div class="sidebar-nav">
        <div class="nav-section-title">Main Menu</div>
        
        <router-link 
          to="/doctor/dashboard" 
          class="nav-link"
          :class="{ active: isActive('/doctor/dashboard') }">
          <i class="fas fa-tachometer-alt"></i>
          <span>Dashboard</span>
        </router-link>

        <router-link 
          to="/doctor/appointments" 
          class="nav-link"
          :class="{ active: isActive('/doctor/appointments') }">
          <i class="fas fa-calendar-check"></i>
          <span>Appointments</span>
        </router-link>

        <router-link 
          to="/doctor/patients" 
          class="nav-link"
          :class="{ active: isActive('/doctor/patients') }">
          <i class="fas fa-users"></i>
          <span>My Patients</span>
        </router-link>

        <router-link 
          to="/doctor/treatments" 
          class="nav-link"
          :class="{ active: isActive('/doctor/treatments') }">
          <i class="fas fa-prescription-bottle-alt"></i>
          <span>Treatments</span>
        </router-link>

        <div class="nav-section-title">Settings</div>

        <router-link 
          to="/doctor/availability" 
          class="nav-link"
          :class="{ active: isActive('/doctor/availability') }">
          <i class="fas fa-calendar-alt"></i>
          <span>Set Availability</span>
        </router-link>

        <router-link 
          to="/doctor/profile" 
          class="nav-link"
          :class="{ active: isActive('/doctor/profile') }">
          <i class="fas fa-user-cog"></i>
          <span>My Profile</span>
        </router-link>
      </div>

      <!-- User Info Card -->
      <div class="user-info-card">
        <div class="d-flex align-items-center mb-3">
          <div class="user-avatar me-3">JD</div>
          <div class="user-details">
            <div class="user-name">Dr. John Doe</div>
            <div class="user-role">Cardiologist</div>
          </div>
        </div>
        <router-link to="/logout" class="btn btn-logout">
          <i class="fas fa-sign-out-alt me-2"></i>Logout
        </router-link>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Flash Messages / Notifications Area -->
      <slot name="notifications"></slot>

      <!-- Page Content -->
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
/* ===== Blue Corporate Theme ===== */
:root {
  --primary: #0d6efd;
  --primary-dark: #084298;
  --primary-light: #3d8bfd;
  --dark: #1e293b;
  --light: #f8fafc;
  --gray-800: #1f2937;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: linear-gradient(135deg, #f8fafc 0%, #e3eeff 100%);
  color: var(--gray-800);
  font-size: 14px;
  line-height: 1.6;
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 280px;
  background: linear-gradient(180deg, #084298 0%, #001d3d 100%);
  box-shadow: 4px 0 20px rgba(13, 110, 253, 0.15);
  z-index: 1040;
  overflow-y: auto;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.3s ease;
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
  letter-spacing: 0.3px;
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
  box-shadow: 0 3px 10px rgba(13, 110, 253, 0.3);
}

/* Navigation */
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
  opacity: 0.9;
}

.nav-link:hover {
  background: rgba(13, 110, 253, 0.18);
  color: #fff;
  transform: translateX(2px);
}

.nav-link.active {
  background: linear-gradient(90deg, rgba(13, 110, 253, 0.25) 0%, rgba(0, 123, 255, 0.2) 100%);
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

/* User Info Card */
.user-info-card {
  margin: 1.5rem 1rem 1.5rem;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: inset 0 0 12px rgba(13, 110, 253, 0.08);
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
  box-shadow: 0 4px 10px rgba(13, 110, 253, 0.4);
}

.user-name {
  color: white;
  font-weight: 600;
}

.user-role {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.8125rem;
}

.btn-logout {
  margin-top: 1rem;
  width: 100%;
  padding: 0.625rem;
  background: rgba(13, 110, 253, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
}

.btn-logout:hover {
  background: rgba(13, 110, 253, 0.3);
  border-color: rgba(13, 110, 253, 0.3);
  box-shadow: 0 0 12px rgba(13, 110, 253, 0.4);
}

/* Main Content */
.main-content {
  margin-left: 280px;
  min-height: 100vh;
  padding: 2.25rem;
  background: linear-gradient(135deg, #f9fbff 0%, #edf3ff 100%);
  transition: all 0.3s ease;
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

/* Card & General Styles */
.card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
  background: white;
  margin-bottom: 1.5rem;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(13, 110, 253, 0.15);
}
</style>