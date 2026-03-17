<template>
  <div class="page-wrapper">
    <AppHeader title="TENTANG KAMI" />

    <div class="teal-block" style="flex:1; overflow-y:auto;">
      <p class="info-text">
        Direktori Statistik Pariwisata Dengan Pemanfaatan Global Positioning System dan Unsur Infografis
        <strong>(D'Paris Egsotis)</strong> adalah inovasi yang digagas oleh sdr. Muhammad Iqbal, S.E.
        dan dikembangkan lebih jauh lagi oleh tim Sistem Pemerintahan Berbasis Elektronik (SPBE) dan
        BPS Kota Pagar Alam untuk membantu para wisatawan yang berkunjung ke Kota Pagar Alam dalam
        mencari informasi terkait fasilitas penunjang dalam berwisata di Kota Pagar Alam. Data dalam aplikasi
        ini bersumber dari Updating Direktori berkait pariwisata yang dilakukan oleh BPS Kota Pagar Alam, mulai
        dari Updating Direktori Jasa Akomodasi (VHTL), Updating Direktori Daya Tarik Wisata (DTW), Updating database
        usaha target SE2026 melalui inovasi digital Cari Data Seputar Usaha (Cadas Usaha) yang dibangun oleh tim SPBE
        BPS Kota Pagar Alam serta kegiatan updating direktori sejenis yang disinkronisasi dengan data spasial dari Google Map
        terkait pariwisata.
      </p>

      <!-- Profil tim -->
      <br>
      <div class="team-section">
        <div class="team-title">TIM PENGEMBANG D'PARIS EGSOTIS 1.0</div>
        <div class="team-card">
          <div class="team-info">
            <div class="team-name">Muhammad Iqbal, S.E.</div>
            <div class="team-role">Leader</div>
          </div>
          <div class="team-info">
            <div class="team-name">Yeny Oktavia, S.Si.</div>
            <div class="team-role">Co-Leader</div>
          </div>
          <div class="team-info">
            <div class="team-name">Pray Putra Hasianro Nadeak, S.ST.</div>
            <div class="team-role">Developer</div>
          </div>
        </div>
        <br>
        <div class="team-title">TIM PENGEMBANG D'PARIS EGSOTIS 2.0</div>
        <div class="team-card">
          <div class="team-avatar">👨‍💼</div>
          <div class="team-info">
            <div class="team-name">Pray Putra Hasianro Nadeak, S.ST.</div>
            <div class="team-role">Leader</div>
          </div>
        </div>
        <div class="team-card">
          <div class="team-avatar">🏛️</div>
          <div class="team-info">
            <div class="team-name">Tim SPBE BPS Kota Pagar Alam</div>
            <div class="team-role">Developer</div>
          </div>
        </div>
        <div class="team-card">
          <div class="team-avatar">📊</div>
          <div class="team-info">
            <div class="team-name">Tim DLS BPS Kota Pagar Alam</div>
            <div class="team-role">Supporting System</div>
          </div>
        </div>
      </div>

      <!-- Kontak -->
      <br>
      <div class="contact-section">
        <div class="contact-title">KONTAK INSTANSI</div>
        <div class="contact-item">
          <span>📍</span>
          <span>Jl. Laskar Wanita Mentarjo Komp Perkantoran Gunung Gare, Kota Pagar Alam, Sumatera Selatan</span>
        </div>
        <div class="contact-item">
          <span>📞</span>
          <span>(0730) 623 511</span>
        </div>
        <div class="contact-item">
          <span>📧</span>
          <span>bps1673@bps.go.id</span>
        </div>
        <div class="contact-item">
          <span>🌐</span>
          <span>pagaralamkota.bps.go.id</span>
        </div>
      </div>
  
      <br>
      <button class="btn-white" @click="openYoutube">
        Apa kata mereka tentang DPARIS EGSOTIS?
      </button>

      <transition name="fade">
        <div v-if="showTestimoni" class="testimoni-section">
          <div v-for="t in testimoni" :key="t.id" class="testimoni-card">
            <div class="testimoni-avatar">{{ t.initial }}</div>
            <div class="testimoni-body">
              <div class="testimoni-name">{{ t.name }}</div>
              <div class="testimoni-text">"{{ t.text }}"</div>
              <div class="stars">{{ '⭐'.repeat(t.stars) }}</div>
            </div>
          </div>
        </div>
      </transition>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'

const showTestimoni = ref(false)

const testimoni = [
  { id: 1, initial: 'A', name: 'Ahmad R.', text: 'Aplikasi yang sangat membantu saat berwisata ke Pagar Alam!', stars: 5 },
  { id: 2, initial: 'S', name: 'Siti M.', text: 'Informasi akomodasi sangat lengkap dan mudah ditemukan.', stars: 5 },
  { id: 3, initial: 'B', name: 'Budi K.', text: 'CADAS Besemah sangat responsif dalam menjawab pertanyaan saya.', stars: 4 },
]

const openYoutube = () => {
  window.open('https://www.youtube.com/watch?v=JePkPjSLKFc&t=2s', '_blank')
}
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
.info-text {
  color: rgba(255,255,255,0.92);
  font-size: 0.9rem;
  line-height: 1.75;
  font-weight: 500;
  text-align: justify;
  margin-bottom: 20px;
}
.info-text strong { color: #fff; font-weight: 800; }
.team-section, .contact-section { margin-bottom: 20px; }
.team-title, .contact-title {
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.7);
  text-transform: uppercase;
  margin-bottom: 10px;
}
.team-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.15);
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 8px;
}
.team-avatar {
  font-size: 1.8rem;
  width: 44px;
  height: 44px;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.team-name { color: #fff; font-weight: 700; font-size: 0.9rem; }
.team-role { color: rgba(255,255,255,0.75); font-size: 0.76rem; margin-top: 2px; }
.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: rgba(255,255,255,0.88);
  font-size: 0.85rem;
  margin-bottom: 8px;
  line-height: 1.5;
}
.testimoni-section { margin-top: 20px; }
.testimoni-card {
  display: flex;
  gap: 12px;
  background: rgba(255,255,255,0.15);
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 10px;
}
.testimoni-avatar {
  width: 40px;
  height: 40px;
  background: rgba(255,255,255,0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.testimoni-name { color: #fff; font-weight: 700; font-size: 0.87rem; margin-bottom: 4px; }
.testimoni-text { color: rgba(255,255,255,0.85); font-size: 0.82rem; line-height: 1.5; font-style: italic; }
.stars { margin-top: 6px; font-size: 0.85rem; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
