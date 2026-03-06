<template>
  <div class="page-wrapper">
    <AppHeader title="PENGADUAN" />

    <div class="teal-block" style="flex:1; overflow-y:auto;">
      <p class="info-text">
        Menurut Kementerian Pendayagunaan Aparatur Negara dan Reformasi Birokrasi (KemenPANRB),
        layanan pengaduan merupakan bagian dari penyelenggaraan pelayanan publik yang menyediakan
        mekanisme bagi masyarakat untuk menyampaikan keluhan, saran, dan aspirasi atas pelayanan
        yang diberikan oleh instansi pemerintah.
      </p>
      <a
        href="https://www.lapor.go.id/admin/laporan/kelola#waiting"
        target="_blank"
        class="btn-teal"
        style="margin-top:24px;"
      >
        Klik untuk LAPOR PENGADUAN
      </a>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
</script>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #fff;
  max-width: 420px;
  width: 100%;
}
.section-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 14px;
  letter-spacing: 0.04em;
}
.info-text {
  color: rgba(255,255,255,0.92);
  font-size: 0.92rem;
  line-height: 1.75;
  font-weight: 500;
  text-align: justify;
}
.info-text strong { color: #fff; font-weight: 800; }
.info-text em { font-style: italic; }
.feature-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.15);
  border-radius: 12px;
  padding: 12px 16px;
  color: #fff;
  font-size: 0.88rem;
  font-weight: 600;
}
.feature-icon {
  font-size: 1.4rem;
  flex-shrink: 0;
}
</style>
