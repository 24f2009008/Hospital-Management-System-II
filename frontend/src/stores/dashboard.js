import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDashboardStore = defineStore('dashboard', () => {
  // Common state
  const loading = ref(false)
  const error = ref(null)

  // Role-specific state
  const stats = ref({})
  const recentDoctors = ref([])
  const recentPatients = ref([])
  const recentAppointments = ref([])
  const departments = ref([])
  const doctors = ref([])           // Used by Patient
  const appointments = ref([])      // Used by Patient
  const chartData = ref({})         // Used by Doctor (future)

  // Reusable fetch function
  const fetchDashboard = async (role = 'admin') => {
  loading.value = true
  error.value = null

  let url = ''
  switch (role.toLowerCase()) {
    case 'admin':   url = 'http://127.0.0.1:5000/api/admin/dashboard'; break
    case 'patient': url = 'http://127.0.0.1:5000/api/patient/dashboard'; break
    case 'doctor':  url = 'http://127.0.0.1:5000/api/doctor/dashboard'; break
    default:
      error.value = 'Invalid role'
      loading.value = false
      return
  }

  try {
    const response = await fetch(url, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    // ← NEW: Check content type first
    const contentType = response.headers.get('content-type')

    if (!response.ok) {
      if (response.status === 401) {
        error.value = "Please log in"
        window.location.href = '/login'
        return
      }
      if (response.status === 403) {
        error.value = "Access denied"
        return
      }
    }


    const data = await response.json()

    if (!data.success) {
      throw new Error(data.message || `Failed to load ${role} dashboard`)
    }

    // Clear previous data
    stats.value = {}
    recentDoctors.value = []
    recentPatients.value = []
    recentAppointments.value = []
    departments.value = []
    doctors.value = []
    appointments.value = []
    chartData.value = {}

    // Populate based on role (your existing logic)
    if (role === 'admin') {
      stats.value = data.stats || {}
      recentDoctors.value = data.recent_doctors || []
      recentPatients.value = data.recent_patients || []
      recentAppointments.value = data.recent_appointments || []
      departments.value = data.departments || []
    } else if (role === 'patient') {
      stats.value = data.stats || {}
      doctors.value = data.doctors || []
      appointments.value = data.appointments || []
    } else if (role === 'doctor') {
      stats.value = {
        todays_appointments: data.todays_appointments || 0,
        pending_consultations: data.pending_consultations || 0,
        upcoming_appointments: data.upcoming_appointments || 0
      }
    }

  } catch (err) {
    error.value = err.message || 'Failed to load dashboard'
    console.error(`[Dashboard Fetch Error - ${role}]`, err)
  } finally {
    loading.value = false
  }
}
  return {
    loading,
    error,
    stats,
    recentDoctors,
    recentPatients,
    recentAppointments,
    departments,
    doctors,
    appointments,
    chartData,
    fetchDashboard
  }
})