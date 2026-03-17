<template>
  <footer class="app-footer">
    <div class="footer-banner">
      <a href="https://sensus.bps.go.id/se2026/" target="_blank" rel="noopener" style="display:block;">
        <img src="../assets/footer_banner.png" alt="Pagar Alam Banner" class="banner-img">
      </a>
    </div>
    <p>&copy; 2026 BPS Kota Pagar Alam. All rights reserved.</p>
  </footer>
</template>

<style scoped>
.app-footer {
  text-align: center;
  padding: 0; /* Remove padding to let banner be full-width if needed */
  background: #fff;
  color: #1a3a5c;
  font-size: 0.75rem;
  font-weight: 600;
  border-top: 1px solid rgba(0,0,0,0.05);
  margin-top: auto;
}

.footer-banner {
  width: 100%;
  aspect-ratio: 10 / 2;
  overflow: hidden;
  margin-bottom: 8px;
}

.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.app-footer p {
  padding: 12px 16px;
  margin: 0;
}
</style>
