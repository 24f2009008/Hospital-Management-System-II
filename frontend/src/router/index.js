import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Logout from '@/views/Logout.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import DoctorLayout from '@/layouts/DoctorLayout.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import PatientLayout from '@/layouts/PatientLayout.vue'
import DoctorDashboard from '../views/doctor/DoctorDashboard.vue'
import PatientDashboard from '@/views/patient/PatientDashboard.vue'
// import PatientDashboard from '../views/Pat ientDashboard.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/logout', component: Logout },
  { path: '/admin', component: AdminLayout,
    children: [
      {
        path: 'dashboard', component: AdminDashboard
      }
    ]
  },
  { path: '/doctor', component: DoctorLayout,
    children: [
      {
        path: 'dashboard',component: DoctorDashboard
      }
    ]
  },
  {path: '/patient', component: PatientLayout,
    children: [
      {
        path: 'dashboard', component: PatientDashboard
      }
    ]
  }
  // { path: '/doctor', component: DoctorDashboard },
  // { path: '/patient', component: PatientDashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

import { useAuthStore } from '@/stores/auth'

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Load from localStorage if needed
  if (!authStore.isLoggedIn) {
    authStore.loadFromStorage()
  }

  // Protect admin routes
  if (to.path.startsWith('/admin')) {
    if (!authStore.isLoggedIn) {
      alert("Unauthorized")
      return next('/login')
    }

    if (authStore.role !== 'admin') {
      return next(`/${authStore.role}/dashboard`)
    }
  }

  if (to.path.startsWith('/doctor')) {
    if (!authStore.isLoggedIn) {
      return next('/login')
    }

    if (authStore.role !== 'doctor') {
      alert("Unauthorized")
      return next(`/${authStore.role}/dashboard`)
    }
}

  if (to.path.startsWith('/patient')) {
    if (!authStore.isLoggedIn) {
      return next('/login')
    }

    if (authStore.role !== 'patient') {
      alert("Unauthorized")
      return next(`/${authStore.role}/dashboard`)
    }
  }

  next()
})
export default router
