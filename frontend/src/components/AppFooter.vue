<template>
  <footer class="app-footer">
    <div class="statistics-container">
      <div class="stat-text">Total Pengunjung : {{ visitorTotal }}</div>
      <div class="stat-text">Total Pengunduh : {{ downloaderTotal }}</div>
    </div>
    <div class="footer-banner">
      <a href="https://sensus.bps.go.id/se2026/" target="_blank" rel="noopener" style="display:block;">
        <img src="../assets/footer_banner.png" alt="Pagar Alam Banner" class="banner-img">
      </a>
    </div>
    <p>&copy; 2026 BPS Kota Pagar Alam. All rights reserved.</p>
  </footer>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const visitorTotal = ref(238)
const downloaderTotal = ref(30)

onMounted(async () => {
  try {
    const res = await fetch('/api/v1/statistics/total')
    if (res.ok) {
      const data = await res.json()
      visitorTotal.value = data.visitor_total || 0
      downloaderTotal.value = data.downloader_total || 0
    }
  } catch (err) {
    console.error('Failed to fetch statistics', err)
  }
})
</script>

<style scoped>
.app-footer {
  text-align: center;
  padding: 0;
  background: #fff;
  color: #1a3a5c;
  font-size: 0.75rem;
  font-weight: 600;
  border-top: 1px solid rgba(0,0,0,0.05);
  margin-top: auto;
}

.statistics-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: #fcfcfc;
  font-size: 0.8rem;
}

.stat-text {
  margin-bottom: 0;
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
