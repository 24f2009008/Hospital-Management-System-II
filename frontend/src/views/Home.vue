<template>
  <!-- Hero Section -->
  <section id="home" class="hero-section">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-6">
          <div class="hero-content">
            <h1 class="hero-title">Your Health is Our Priority</h1>
            <p class="hero-subtitle">
              Experience world-class healthcare with cutting-edge technology and 
              compassionate medical professionals dedicated to your well-being.
            </p>
            <div class="d-flex gap-3 flex-wrap">
              <router-link to="/register" class="btn btn-light btn-lg">Get Started</router-link>
              <a href="#services" class="btn btn-outline-light btn-lg">Our Services</a>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="hero-stats">
            <div class="row text-center">
              <div class="col-4">
                <div class="stat-number">500+</div>
                <div class="stat-label">Expert Doctors</div>
              </div>
              <div class="col-4">
                <div class="stat-number">50K+</div>
                <div class="stat-label">Patients Treated</div>
              </div>
              <div class="col-4">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Emergency Care</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section id="features" class="features-section">
    <div class="container">
      <h2 class="section-title">Why Choose HMS Hospital?</h2>
      <div class="row g-4">
        <div class="col-lg-4 col-md-6">
          <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-user-md"></i></div>
            <h4 class="feature-title">Expert Doctors</h4>
            <p class="feature-description">Our team of highly qualified and experienced medical professionals provides personalized care.</p>
          </div>
        </div>
        <div class="col-lg-4 col-md-6">
          <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-clock"></i></div>
            <h4 class="feature-title">24/7 Availability</h4>
            <p class="feature-description">Round-the-clock emergency services and support to ensure you receive care whenever you need it.</p>
          </div>
        </div>
        <div class="col-lg-4 col-md-6">
          <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-laptop-medical"></i></div>
            <h4 class="feature-title">Digital Health Records</h4>
            <p class="feature-description">Secure and accessible digital health records for seamless healthcare management.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Services Section -->
  <section id="services" class="services-section">
    <div class="container">
      <h2 class="section-title">Our Medical Services</h2>
      <div class="row">
        <div class="col-lg-6">
          <div class="service-card">
            <i class="fas fa-heartbeat service-icon"></i>
            <h4>Cardiology</h4>
            <p>Comprehensive heart care with advanced diagnostic and treatment facilities.</p>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="service-card">
            <i class="fas fa-brain service-icon"></i>
            <h4>Neurology</h4>
            <p>Expert care for neurological disorders with state-of-the-art technology.</p>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="service-card">
            <i class="fas fa-baby service-icon"></i>
            <h4>Pediatrics</h4>
            <p>Specialized healthcare services for children of all age groups.</p>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="service-card">
            <i class="fas fa-bone service-icon"></i>
            <h4>Orthopedics</h4>
            <p>Advanced bone and joint care with minimally invasive procedures.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="cta-section">
    <div class="container">
      <h2 class="cta-title">Ready to Get Started?</h2>
      <p class="cta-description">Join thousands of patients who trust HMS Hospital for their healthcare needs.</p>
      <div class="d-flex gap-3 justify-content-center flex-wrap">
        <router-link to="/register" class="btn btn-light btn-lg">Create Account</router-link>
        <router-link to="/login" class="btn btn-outline-light btn-lg">Login Now</router-link>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 mb-4">
          <div class="footer-brand">
            <i class="fas fa-hospital"></i> HMS Hospital
          </div>
          <p>Providing exceptional healthcare services with compassion and cutting-edge technology since 2005.</p>
        </div>
        <div class="col-lg-2 col-md-6 mb-4">
          <div class="footer-links">
            <h5>Quick Links</h5>
            <a href="#home">Home</a>
            <a href="#services">Services</a>
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-4">
          <div class="footer-links">
            <h5>Services</h5>
            <a href="#">Emergency Care</a>
            <a href="#">Primary Care</a>
            <a href="#">Specialist Care</a>
            <a href="#">Surgery</a>
            <a href="#">Diagnostics</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
