<template>
  <div class="page-wrapper">
    <AppHeader title="INFOGRAFIS" />

    <div class="teal-block" style="flex:1; overflow-y:auto;">
      <p class="info-text">
        Infografis adalah produk diseminasi statistik dengan desain dan tata letak yang menarik
        untuk menyampaikan beragam data yang menceritakan suatu topik atau fenomena tertentu.
        BPS Kota Pagar Alam telah mendesain beberapa infografis menarik untuk memperkarya
        wawasan pengguna data.
      </p>

      <a
        href="https://pagaralamkota.bps.go.id/id/infographic"
        target="_blank"
        class="btn-primary"
        style="margin-top:28px;"
      >
        Klik untuk Lihat Infografis
      </a>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'

const infografis = [
  { id: 1, title: 'Statistik Pariwisata 2024', year: '2024' },
  { id: 2, title: 'Kunjungan Wisatawan 2023', year: '2023' },
  { id: 3, title: 'Akomodasi Kota Pagar Alam', year: '2023' },
  { id: 4, title: 'Infografis Kuliner Besemah', year: '2022' },
]
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
  font-size: 0.93rem;
  line-height: 1.75;
  font-weight: 500;
  text-align: justify;
  margin-bottom: 24px;
}
.infographic-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 8px;
}
.infographic-card {
  background: rgba(255,255,255,0.15);
  border-radius: 14px;
  padding: 14px 12px;
  cursor: pointer;
  transition: background 0.2s ease;
  text-align: center;
}
.infographic-card:hover { background: rgba(255,255,255,0.25); }
.infographic-thumb { margin-bottom: 10px; }
.infographic-thumb svg { width: 60px; height: 60px; }
.infographic-title {
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  line-height: 1.35;
}
.infographic-year {
  color: rgba(255,255,255,0.7);
  font-size: 0.7rem;
  margin-top: 4px;
}
</style>
