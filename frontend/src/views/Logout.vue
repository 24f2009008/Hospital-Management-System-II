<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {
  try {
    await fetch('http://127.0.0.1:5000/api/logout', {
      method: 'POST'
    })
  } catch (err) {
    console.error(err)
  }

  // Always logout locally
  authStore.logout()
  router.push('/login')
})
</script>

<template>
  <p>Logging out...</p>
</template>