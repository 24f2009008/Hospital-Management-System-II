<template>
  <!-- Hero Section -->
  <section id="home" class="hero-section">
    <div class="container">
      <div class="row align-items-center g-5">
        <div class="col-lg-6">
          <div class="hero-content">
            <div class="hero-badge">
              <i class="fas fa-star me-2"></i>Trusted by 50,000+ patients
            </div>
            <h1 class="hero-title">
              Your Health is<br><span>Our Priority</span>
            </h1>
            <p class="hero-subtitle">
              Experience world-class healthcare with cutting-edge technology and
              compassionate medical professionals dedicated to your well-being.
            </p>
            <div class="d-flex gap-3 flex-wrap">
              <router-link to="/register" class="btn btn-light btn-lg hero-btn-primary">
                <i class="fas fa-user-plus me-2"></i>Get Started
              </router-link>
              <a href="#services" class="btn btn-outline-light btn-lg">
                <i class="fas fa-stethoscope me-2"></i>Our Services
              </a>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="hero-stats">
            <div class="row text-center g-0">
              <div class="col-4">
                <div class="stat-number">500+</div>
                <div class="stat-label">Expert Doctors</div>
              </div>
              <div class="col-4 stat-divider">
                <div class="stat-number">50K+</div>
                <div class="stat-label">Patients Treated</div>
              </div>
              <div class="col-4">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Emergency Care</div>
              </div>
            </div>
          </div>
          <div class="hero-cards">
            <div class="hero-card">
              <i class="fas fa-calendar-check text-primary"></i>
              <div>
                <div class="fw-semibold">Easy Booking</div>
                <small class="text-muted">Schedule in seconds</small>
              </div>
            </div>
            <div class="hero-card">
              <i class="fas fa-file-medical text-success"></i>
              <div>
                <div class="fw-semibold">Digital Records</div>
                <small class="text-muted">Always accessible</small>
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
      <div class="section-label">Why Choose Us</div>
      <h2 class="section-title">Why Choose HMS Hospital?</h2>
      <div class="row g-4">
        <div class="col-lg-4 col-md-6">
          <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-user-md"></i></div>
            <h4 class="feature-title">Expert Doctors</h4>
            <p class="feature-description">Our team of highly qualified and experienced medical professionals provides personalized care tailored to your needs.</p>
          </div>
        </div>
        <div class="col-lg-4 col-md-6">
          <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-clock"></i></div>
            <h4 class="feature-title">24/7 Availability</h4>
            <p class="feature-description">Round-the-clock emergency services and support to ensure you receive care whenever you need it most.</p>
          </div>
        </div>
        <div class="col-lg-4 col-md-6">
          <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-laptop-medical"></i></div>
            <h4 class="feature-title">Digital Health Records</h4>
            <p class="feature-description">Secure and accessible digital health records for seamless healthcare management across all visits.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Services Section -->
  <section id="services" class="services-section">
    <div class="container">
      <div class="section-label">What We Offer</div>
      <h2 class="section-title">Our Medical Services</h2>
      <div class="row g-4">
        <div class="col-lg-6">
          <div class="service-card">
            <div class="service-icon-wrap"><i class="fas fa-heartbeat service-icon"></i></div>
            <div>
              <h4>Cardiology</h4>
              <p>Comprehensive heart care with advanced diagnostic and treatment facilities.</p>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="service-card">
            <div class="service-icon-wrap"><i class="fas fa-brain service-icon"></i></div>
            <div>
              <h4>Neurology</h4>
              <p>Expert care for neurological disorders with state-of-the-art technology.</p>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="service-card">
            <div class="service-icon-wrap"><i class="fas fa-baby service-icon"></i></div>
            <div>
              <h4>Pediatrics</h4>
              <p>Specialized healthcare services for children of all age groups.</p>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="service-card">
            <div class="service-icon-wrap"><i class="fas fa-bone service-icon"></i></div>
            <div>
              <h4>Orthopedics</h4>
              <p>Advanced bone and joint care with minimally invasive procedures.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="cta-section">
    <div class="container">
      <div class="cta-inner">
        <h2 class="cta-title">Ready to Get Started?</h2>
        <p class="cta-description">Join thousands of patients who trust HMS Hospital for their healthcare needs.</p>
        <div class="d-flex gap-3 justify-content-center flex-wrap">
          <router-link to="/register" class="btn btn-light btn-lg">
            <i class="fas fa-user-plus me-2"></i>Create Account
          </router-link>
          <router-link to="/login" class="btn btn-outline-light btn-lg">
            <i class="fas fa-sign-in-alt me-2"></i>Login Now
          </router-link>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="row g-4">
        <div class="col-lg-4 mb-2">
          <div class="footer-brand">
            <i class="fas fa-hospital me-2"></i>HMS Hospital
          </div>
          <p class="footer-desc">Providing exceptional healthcare services with compassion and cutting-edge technology since 2005.</p>
        </div>
        <div class="col-lg-2 col-md-6">
          <div class="footer-links">
            <h5>Quick Links</h5>
            <a href="#home">Home</a>
            <a href="#services">Services</a>
            <a href="#features">Features</a>
            <a href="#about">About</a>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <div class="footer-links">
            <h5>Services</h5>
            <a href="#">Emergency Care</a>
            <a href="#">Primary Care</a>
            <a href="#">Specialist Care</a>
            <a href="#">Diagnostics</a>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <div class="footer-links">
            <h5>Account</h5>
            <router-link to="/login">Sign In</router-link>
            <router-link to="/register">Register</router-link>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2025 HMS Hospital. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
/* Hero extras */
.hero-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(99,102,241,.15);
  border: 1px solid rgba(99,102,241,.3);
  color: #a5b4fc;
  padding: 0.4rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.hero-btn-primary { background: white; color: #1e1b4b; font-weight: 700; }
.hero-btn-primary:hover { background: #f0f0ff; color: #1e1b4b; transform: translateY(-2px); }

.hero-cards {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.hero-card {
  flex: 1;
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 14px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.875rem;
  color: white;
  backdrop-filter: blur(8px);
}

.hero-card i { font-size: 1.5rem; flex-shrink: 0; }

.stat-divider {
  border-left: 1px solid rgba(255,255,255,.15);
  border-right: 1px solid rgba(255,255,255,.15);
}

/* Section label */
.section-label {
  text-align: center;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #6366f1;
  margin-bottom: 0.75rem;
}

/* Service icon wrap */
.service-icon-wrap {
  width: 52px; height: 52px;
  background: linear-gradient(135deg, rgba(99,102,241,.12), rgba(139,92,246,.12));
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.service-icon { font-size: 1.5rem; color: #6366f1; }

/* CTA inner */
.cta-inner { position: relative; z-index: 1; }

/* Footer desc */
.footer-desc { color: rgba(255,255,255,.55); font-size: 0.9rem; line-height: 1.7; margin-top: 0.5rem; }

.footer-bottom {
  border-top: 1px solid rgba(255,255,255,.1);
  margin-top: 3rem;
  padding-top: 1.5rem;
  text-align: center;
  color: rgba(255,255,255,.4);
  font-size: 0.875rem;
}

.footer-bottom p { margin: 0; }
</style>
