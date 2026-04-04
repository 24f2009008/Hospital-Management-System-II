import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Logout from '@/views/Logout.vue'
import BaseLayout from '@/layouts/BaseLayout.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import DoctorDashboard from '../views/doctor/DoctorDashboard.vue'
import PatientDashboard from '@/views/patient/PatientDashboard.vue'
import Doctor from '@/views/admin/Doctor.vue'
import AdminPatient from '@/views/admin/Patient.vue'
import AdminAppointment from '@/views/admin/Appointment.vue'
import Search from '@/views/Search.vue'
import SearchResult from '@/views/SearchResult.vue'
import DoctorPatient from '@/views/doctor/Patient.vue'
import DoctorAppointment from '@/views/doctor/Appointment.vue'
import Treatment from '@/views/doctor/Treatment.vue'
import Profile from '@/views/Profile.vue'
import Availability from '@/views/doctor/Availability.vue'
import BookAppointment from '@/views/patient/BookAppointment.vue'
import PatientAppointments from '@/views/patient/PatientAppointments.vue'
import PatientDoctors from '@/views/patient/PatientDoctors.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/logout', component: Logout },
  { path: '/admin', component: BaseLayout, 
    props: { role: 'admin' },
    children: [
      {
        path: 'dashboard', component: AdminDashboard
      },
      {
        path: 'doctors', component: Doctor
      },
      {
        path: 'patients', component: AdminPatient
      },
      {
        path: 'appointments', component: AdminAppointment
      },
      {
        path: 'search', component: Search
      },
      {
        path: 'search/results', component: SearchResult
      }
    ]
  },
  { path: '/doctor', component: BaseLayout,
    props: { role: 'doctor' },
    children: [
      {
        path: 'dashboard',component: DoctorDashboard
      },
      {
        path: 'patients', component: DoctorPatient
      },
      {
        path: 'appointments', component: DoctorAppointment
      },
      {
        path: 'search', component: Search
      },
      {
        path: 'search/results', component: SearchResult
      },
      {
        path: 'treatments', component: Treatment
      },
      {
        path: 'profile', component: Profile
      },
      {
        path: 'availability', component: Availability
      }
    ]
  },
  {path: '/patient', component: BaseLayout,
    props: { role: 'patient' },
    children: [
      {
        path: 'dashboard', component: PatientDashboard
      },
      {
        path: 'doctors', component: PatientDoctors
      },
      {
        path: 'appointments', component: PatientAppointments
      },
      {
        path: 'appointments/book', component: BookAppointment
      },
      {
        path: 'history', component: Search
      },
      {
        path: 'profile', component: Profile
      }
    ]
  }
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
