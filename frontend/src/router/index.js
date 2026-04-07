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
import MedicalHistory from '@/views/patient/MedicalHistory.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/logout', component: Logout },

  {
    path: '/admin',
    component: BaseLayout,
    props: { role: 'admin' },
    children: [
      { path: '', redirect: 'dashboard' },
      { path: 'dashboard', component: AdminDashboard },
      { path: 'doctors', component: Doctor },
      { path: 'patients', component: AdminPatient },
      { path: 'appointments', component: AdminAppointment },
      { path: 'search', component: Search },
      { path: 'search/results', component: SearchResult },
      { path: 'profile', component: Profile }
    ]
  },

  {
    path: '/doctor',
    component: BaseLayout,
    props: { role: 'doctor' },
    children: [
      { path: '', redirect: 'dashboard' },
      { path: 'dashboard', component: DoctorDashboard },
      { path: 'patients', component: DoctorPatient },
      { path: 'appointments', component: DoctorAppointment },
      { path: 'search', component: Search },
      { path: 'search/results', component: SearchResult },
      { path: 'treatments', component: Treatment },
      { path: 'profile', component: Profile },
      { path: 'availability', component: Availability }
    ]
  },

  {
    path: '/patient',
    component: BaseLayout,
    props: { role: 'patient' },
    children: [
      { path: '', redirect: 'dashboard' },
      { path: 'dashboard', component: PatientDashboard },
      { path: 'departments', component: PatientDoctors },
      { path: 'doctors', component: PatientDoctors },
      { path: 'appointments', component: PatientAppointments },
      { path: 'appointments/book', component: BookAppointment },
      { path: 'history', component: MedicalHistory },
      { path: 'profile', component: Profile }
    ]
  },

  // Catch-all redirect
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

import { useAuthStore } from '@/stores/auth'

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (!authStore.isLoggedIn) {
    authStore.loadFromStorage()
  }

  const publicPaths = ['/', '/login', '/register']
  if (publicPaths.includes(to.path)) return next()

  if (to.path.startsWith('/admin')) {
    if (!authStore.isLoggedIn) return next('/login')
    if (authStore.role !== 'admin') return next(`/${authStore.role}/dashboard`)
  }

  if (to.path.startsWith('/doctor')) {
    if (!authStore.isLoggedIn) return next('/login')
    if (authStore.role !== 'doctor') return next(`/${authStore.role}/dashboard`)
  }

  if (to.path.startsWith('/patient')) {
    if (!authStore.isLoggedIn) return next('/login')
    if (authStore.role !== 'patient') return next(`/${authStore.role}/dashboard`)
  }

  next()
})

export default router
