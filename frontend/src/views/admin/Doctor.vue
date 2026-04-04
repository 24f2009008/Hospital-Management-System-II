<template>
  <div class="container-fluid">
    <!-- Page Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div class="mb-2 mb-md-0">
          <h2 class="mb-1">
            <i class="fas fa-user-md me-2"></i>
            Manage Doctors
          </h2>
          <p class="text-muted mb-0">View, update, and manage all doctors in the system</p>
        </div>
        <button @click="showAddModal = true" class="btn btn-primary">
          <i class="fas fa-user-plus me-2"></i><span class="d-none d-sm-inline">Add New </span>Doctor
        </button>
      </div>
    </div>

    <!-- Doctors Table -->
    <div class="card">
      <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="fas fa-users-cog me-2"></i>All Doctors</h5>
          <span class="badge bg-white text-dark" style="font-size: 1rem; padding: 0.5rem 1rem;">
            {{ doctors.length }} Total
          </span>
        </div>
      </div>
      <div class="card-body p-0">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-3 text-muted">Loading doctors...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="alert alert-danger m-3">
          {{ error }}
          <button class="btn btn-sm btn-outline-danger ms-3" @click="loadDoctors">Retry</button>
        </div>

        <!-- Table -->
        <div v-else-if="doctors.length > 0" class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th class="text-nowrap">ID</th>
                <th class="text-nowrap">Name</th>
                <th class="text-nowrap d-none d-xl-table-cell">License</th>
                <th class="text-nowrap">Specialization</th>
                <th class="text-nowrap d-none d-lg-table-cell">Department</th>
                <th class="text-nowrap d-none d-xl-table-cell">Qualification</th>
                <th class="text-nowrap d-none d-lg-table-cell">Experience</th>
                <th class="text-nowrap d-none d-md-table-cell">Gender</th>
                <th class="text-nowrap">Status</th>
                <th class="text-nowrap">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="doctor in doctors" :key="doctor.id">
                <td class="text-nowrap"><strong>DR{{ String(doctor.id).padStart(3, '0') }}</strong></td>
                <td class="text-nowrap">{{ doctor.name }}</td>
                <td class="d-none d-xl-table-cell"><small>{{ doctor.license_number }}</small></td>
                <td>{{ doctor.specialization }}</td>
                <td class="d-none d-lg-table-cell">{{ doctor.department }}</td>
                <td class="d-none d-xl-table-cell">{{ doctor.qualification }}</td>
                <td class="d-none d-lg-table-cell">{{ doctor.experience }} years</td>
                <td class="d-none d-md-table-cell">{{ doctor.gender }}</td>
                <td>
                  <span class="badge" :class="doctor.status === 'active' ? 'bg-success' : 'bg-secondary'">
                    {{ doctor.status ? doctor.status.charAt(0).toUpperCase() + doctor.status.slice(1) : 'Active' }}
                  </span>
                </td>
                <td>
                  <div class="btn-group btn-group-sm" role="group">
                    <button @click="editDoctor(doctor)" class="btn btn-sm btn-outline-primary" title="Edit">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button 
                      @click="toggleStatus(doctor)"
                      class="btn btn-sm"
                      :class="doctor.status === 'active' ? 'btn-outline-danger' : 'btn-outline-success'"
                      :title="doctor.status === 'active' ? 'Deactivate' : 'Activate'">
                      <i :class="doctor.status === 'active' ? 'fas fa-ban' : 'fas fa-check'"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center text-muted py-5">
          <i class="fas fa-user-md fa-4x mb-3 opacity-25"></i>
          <h5>No Doctors Found</h5>
          <p>Start by adding your first doctor to the system.</p>
          <button @click="showAddModal = true" class="btn btn-primary mt-3">
            <i class="fas fa-user-plus me-2"></i>Add First Doctor
          </button>
        </div>
      </div>
    </div>

    <!-- Add Doctor Modal -->
    <AddDoctorModal 
      v-if="showAddModal" 
      @close="showAddModal = false" 
      @added="handleDoctorAdded" 
    />

    <!-- Edit Doctor Modal -->
    <EditDoctorModal 
      v-if="showEditModal" 
      :doctor="selectedDoctor"
      @close="closeEditModal" 
      @updated="handleDoctorUpdated" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AddDoctorModal from '@/components/AddDoctorModal.vue'
import EditDoctorModal from '@/components/EditDoctorModal.vue'

const doctors = ref([])
const loading = ref(false)
const error = ref(null)
const showAddModal = ref(false)
const showEditModal = ref(false)
const selectedDoctor = ref(null)

const API_BASE = 'http://127.0.0.1:5000'

const loadDoctors = async () => {
  loading.value = true
  error.value = null

  try {
    const res = await fetch(`${API_BASE}/api/admin/doctors`, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await res.json()

    if (!res.ok || !data.success) {
      throw new Error(data.message || 'Failed to load doctors')
    }

    doctors.value = data.doctors || []
  } catch (err) {
    error.value = err.message
    console.error('Error loading doctors:', err)
  } finally {
    loading.value = false
  }
}

const toggleStatus = async (doctor) => {
  const newStatus = doctor.status === 'active' ? 'inactive' : 'active'
  const action = newStatus === 'active' ? 'activate' : 'deactivate'
  
  if (!confirm(`Are you sure you want to ${action} this doctor?`)) {
    return
  }

  try {
    const res = await fetch(`${API_BASE}/api/admin/doctors/${doctor.id}/status`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    })

    const data = await res.json()

    if (data.success) {
      await loadDoctors()
    } else {
      alert(data.message || 'Failed to update status')
    }
  } catch (err) {
    console.error('Error toggling status:', err)
    alert('Failed to update status')
  }
}

const editDoctor = (doctor) => {
  selectedDoctor.value = { ...doctor }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  selectedDoctor.value = null
}

const handleDoctorAdded = async () => {
  showAddModal.value = false
  await loadDoctors()
}

const handleDoctorUpdated = async () => {
  showEditModal.value = false
  selectedDoctor.value = null
  await loadDoctors()
}

onMounted(() => {
  loadDoctors()
})
</script>

<style scoped>
.page-header {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.page-header h2 {
  color: var(--gray-900, #111827);
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.page-header h2 i {
  color: var(--primary, #6366f1);
}

.page-header p {
  color: var(--gray-600, #4b5563);
  margin: 0;
}

.card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  background: white;
  overflow: hidden;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  background: white;
  border-bottom: 1px solid var(--gray-200, #e5e7eb);
  padding: 1.25rem 1.5rem;
  font-weight: 600;
  color: var(--gray-900, #111827);
}

.card-body {
  padding: 0;
}

.table {
  margin-bottom: 0;
}

.table thead th {
  background: var(--gray-50, #f9fafb);
  border-bottom: 2px solid var(--gray-200, #e5e7eb);
  color: var(--gray-700, #374151);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  padding: 1rem 1.25rem;
  white-space: nowrap;
}

.table tbody tr {
  transition: all 0.2s ease;
  border-bottom: 1px solid var(--gray-100, #f3f4f6);
}

.table tbody tr:hover {
  background: var(--gray-50, #f9fafb);
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

.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.btn-outline-primary {
  border: 1px solid #6366f1;
  color: #6366f1;
}

.btn-outline-primary:hover {
  background: #6366f1;
  color: white;
}

.btn-outline-danger {
  border: 1px solid #ef4444;
  color: #ef4444;
}

.btn-outline-danger:hover {
  background: #ef4444;
  color: white;
}

.btn-outline-success {
  border: 1px solid #10b981;
  color: #10b981;
}

.btn-outline-success:hover {
  background: #10b981;
  color: white;
}

.btn-group-sm .btn {
  padding: 0.375rem 0.75rem;
  font-size: 0.8125rem;
}

.spinner-border {
  color: var(--primary, #6366f1);
}

.alert {
  border: none;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>
