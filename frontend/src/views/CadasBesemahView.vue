<template>
  <div class="page-wrapper">
    <AppHeader title="CADAS BESEMAH" />

    <div class="teal-block" style="flex:1; overflow-y:auto;">
      <div class="section-title">CADAS BESEMAH</div>
      <p class="info-text">
        <strong>CADAS BESEMAH</strong> (Cari Data Seputar Besemah) adalah layanan data berbasis
        Whatsapp yang dimiliki oleh BPS Kota Pagar Alam. Layanan ini berfungsi selama 7 × 24 jam
        untuk <em>chatting</em> dengan bot dan berfungsi juga untuk <em>chatting</em> dengan petugas
        layanan BPS Kota Pagar Alam.
      </p>
      <p class="info-text" style="margin-top:14px;">
        Layanan ini memberikan kemudahan bagi masyarakat dalam mengakses data statistik terkini
        tentang Kota Pagar Alam, mulai dari kependudukan, pariwisata, ekonomi, hingga sosial
        budaya Besemah.
      </p>

      <div class="feature-list">
        <div class="feature-item">
          <div class="feature-icon">💬</div>
          <div>Chat dengan bot 24 jam</div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">📊</div>
          <div>Akses data statistik terkini</div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">👨‍💼</div>
          <div>Terhubung langsung dengan petugas BPS</div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🏙️</div>
          <div>Data Kota Pagar Alam lengkap</div>
        </div>
      </div>

      <a
        href="https://wa.me/6285178683009"
        target="_blank"
        class="btn-teal"
        style="margin-top:24px;"
      >
        Klik untuk akses CADAS Besemah
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
