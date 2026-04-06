<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const isHome = computed(() => route.path === '/')
</script>

<template>
  <nav v-if="isHome" class="navbar navbar-expand-lg fixed-top">
    <div class="container">
      <router-link class="navbar-brand" to="/">
        <i class="fas fa-hospital me-2"></i>HMS Hospital
      </router-link>

      <button class="navbar-toggler" type="button"
        data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="#services">Services</a></li>
          <li class="nav-item"><a class="nav-link" href="#features">Features</a></li>
          <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
        </ul>
        <div class="ms-3 d-flex gap-2">
          <router-link to="/login" class="btn btn-outline-light btn-sm px-3">Login</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm px-3">Register</router-link>
        </div>
      </div>
    </div>
  </nav>

  <RouterView />
</template>

<style>
/* Ensure register btn in navbar uses white text */
nav .btn-primary {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  color: white !important;
}
nav .btn-outline-light:hover { background: rgba(255,255,255,.15); }
</style>
