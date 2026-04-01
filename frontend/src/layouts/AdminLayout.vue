<script setup>
</script>

<template>
  <div class="admin-layout d-flex">

    <!-- Sidebar -->
    <div class="sidebar">
      <ul>
        <li><router-link to="/admin/dashboard">Dashboard</router-link></li>
        <li><router-link to="/admin/doctors">Doctors</router-link></li>
        <li><router-link to="/admin/patients">Patients</router-link></li>
      </ul>
    </div>

    <!-- Main Content -->
    <div class="main-content flex-grow-1 p-3">
      <RouterView />
    </div>

  </div>
</template>