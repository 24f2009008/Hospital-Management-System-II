<script setup>
</script>

<template>
  <!-- Navigation -->
  <nav class="navbar navbar-expand-lg navbar-light fixed-top">
    <div class="container ">
      <router-link class="navbar-brand position-absolute " to="/">
        <i class="fas fa-hospital"></i> HMS Hospital
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="#services">Services</a></li>
          <li class="nav-item"><a class="nav-link" href="#features">Features</a></li>
          <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
          <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
        </ul>
        <div class="ms-3">
          <router-link to="/login" class="btn btn-primary">Login</router-link>
        </div>
      </div>
    </div>
  </nav>

  <!-- Page Content rendered here -->
  <RouterView />
</template>

<style>
</style>
