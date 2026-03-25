<template>
  <div class="page-wrapper" ref="pdfContent">
    <AppHeader title="WISATA" />
    <div style="text-align: center; padding: 10px 20px 0; background: #fff;" data-html2canvas-ignore="true" v-if="item">
      <button @click="handleDownloadPdf" class="pdf-btn" :disabled="isExporting">
        {{ isExporting ? 'Mengekspor...' : 'Download PDF' }}
      </button>
    </div>
    <br>
    <!-- Loading -->
    <div v-if="loading" class="state-msg">
      <div class="spinner"></div>
      <span>Memuat detail wisata...</span>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="state-msg error-msg">
      ⚠️ {{ error }}
      <button class="retry-btn" @click="fetchDetail">Coba Lagi</button>
    </div>

    <!-- Content -->
    <template v-else-if="item">
      <!-- Hero -->
      <div class="detail-hero">
        <h2>{{ item.name }}</h2>
        <div class="detail-hero-sub">{{ item.category }}</div>
        <div class="star-row" v-if="item.rating !== null && item.rating !== undefined">
          <span v-for="s in 5" :key="s" class="star" :class="starClass(item.rating, s)">&#9733;</span>
          <span class="rating-val">{{ item.rating ? item.rating.toFixed(1) : '' }}</span>
        </div>
      </div>

      <!-- Detail body -->
      <div class="detail-body">

        <!-- Info Umum -->
        <div class="section-title">INFORMASI UMUM</div>
        <div class="detail-row">
          <div class="detail-label">NO</div>
          <div class="detail-value">{{ item.id }}</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">NAMA OBJEK WISATA</div>
          <div class="detail-value">{{ item.name }}</div>
        </div>

        <div class="detail-row">
          <div class="detail-label">RATING</div>
          <div class="detail-value">
            <div class="star-row-detail" v-if="item.rating !== null && item.rating !== undefined">
              <span v-for="s in 5" :key="s" class="star-detail" :class="starClass(item.rating, s)">&#9733;</span>
              <span class="rating-val-detail">{{ item.rating ? item.rating.toFixed(1) : '-' }} / 5</span>
            </div>
            <span v-else>-</span>
          </div>
        </div>
        <div class="detail-row" v-if="item.daya_tarik">
          <div class="detail-label">DESKRIPSI</div>
          <div class="detail-value">{{ item.daya_tarik }}</div>
        </div>
        <div class="detail-row" v-if="item.address">
          <div class="detail-label">ALAMAT</div>
          <div class="detail-value">{{ item.address }}</div>
        </div>
        <div class="detail-row" v-if="item.phone">
          <div class="detail-label">TELEPON</div>
          <div class="detail-value">
            <a :href="`tel:${item.phone}`" class="tel-link">{{ item.phone }}</a>
          </div>
        </div>
        <div class="detail-row" v-if="item.opening_hours">
          <div class="detail-label">JAM BUKA</div>
          <div class="detail-value">{{ item.opening_hours }}</div>
        </div>

        <!-- Jenis Wisata -->
        <div class="section-title" style="margin-top:14px;">JENIS WISATA</div>
        <div class="detail-row">
          <div class="facility-grid">
            <div v-for="t in tourTypes" :key="t.key" class="facility-item">
              <div class="check" :class="{ active: item[t.key] }">
                {{ item[t.key] ? '✓' : '✗' }}
              </div>
              <span>{{ t.name }}</span>
            </div>
          </div>
        </div>


        <!-- Distances to landmarks -->
        <div class="section-title" style="margin-top:14px;">JARAK KE LANDMARK (KM)</div>
        <div class="detail-row" v-for="lm in landmarks" :key="lm.key">
          <div class="detail-label">
            <a :href="lm.maps_link" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">{{ lm.label }}</a>
          </div>
          <div class="detail-value dist-val">
            <span v-if="item[lm.key] !== null && item[lm.key] !== undefined">
              ± {{ Number(item[lm.key]).toFixed(2) }} km
            </span>
            <span v-else>-</span>
          </div>
        </div>

        <!-- Maps button -->
        <a v-if="item.maps_link" :href="item.maps_link" target="_blank" rel="noopener" class="lokasi-btn" data-html2canvas-ignore="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
          </svg>
          LOKASI: Lihat di Google Maps
        </a>
      </div>
    </template>

    <div v-else class="state-msg">Data tidak ditemukan.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '../components/AppHeader.vue'
import { exportToPdf } from '../utils/exportPdf'

const API_BASE = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : ''

const route  = useRoute()
const id     = parseInt(route.params.id)

const item    = ref(null)
const loading = ref(true)
const error   = ref('')

const pdfContent = ref(null)
const isExporting = ref(false)

const handleDownloadPdf = async () => {
  if (isExporting.value) return;
  isExporting.value = true;
  await exportToPdf(pdfContent.value, 'WisataDetailView');
  isExporting.value = false;
}



const tourTypes = [
  { key: 'wisata_alam', name: 'Wisata Alam' },
  { key: 'wisata_budaya', name: 'Wisata Budaya' },
  { key: 'wisata_buatan', name: 'Wisata Buatan' }
]

const landmarks = [
  { key: 'dist_gunung_dempo',         label: 'GUNUNG DEMPO',         maps_link: 'https://www.google.com/maps/place/Gn.+Dempo/@-4.0230239,103.0933106,14z/data=!4m7!3m6!1s0x2e3714981bba2b89:0x244b9373653089dc!8m2!3d-4.0158333!4d103.1283333!15sCgxHVU5VTkcgREVNUE-SAQd2b2xjYW5v4AEA!16s%2Fm%2F027bxph?entry=tts&g_ep=EgoyMDI2MDMxMS4wIPu8ASoASAFQAw%3D%3D&skid=bcf6c2fb-51c1-4317-a2c7-f2a81e2fb1b3' },
  { key: 'dist_pasar_dempo_permai',   label: 'PASAR DEMPO PERMAI',   maps_link: 'https://www.google.com/maps/place/Toko+Mebel+FARIDAH/@-4.0201116,103.2518451,20.33z/data=!4m6!3m5!1s0x2e376bc28e915775:0x90f2ce495902e219!8m2!3d-4.0204016!4d103.2523519!16s%2Fg%2F11c2prpkkw?entry=tts&g_ep=EgoyMDI2MDMxMS4wIPu8ASoASAFQAw%3D%3D&skid=28e75fe6-e63c-4098-b1cd-4016bfa2e870' },
  { key: 'dist_bandara_atung_bungsu', label: 'BANDARA ATUNG BUNGSU', maps_link: 'https://www.google.com/maps/place/Bandar+Udara+Atungbungsu/@-4.0213102,103.3788864,17z/data=!3m1!4b1!4m6!3m5!1s0x2e3766152954d919:0x91108547f6480b38!8m2!3d-4.0213102!4d103.3814613!16s%2Fg%2F12q4_4z3t?entry=tts&g_ep=EgoyMDI2MDMxMS4wIPu8ASoASAFQAw%3D%3D&skid=202a4bc3-eaa0-4702-9702-928e0d781ecc' },
  { key: 'dist_rsud_besemah',         label: 'RSUD BESEMAH',         maps_link: 'https://www.google.com/maps/place/Rumah+Sakit+Besemah,+Alun+Dua,+Kec.+Pagar+Alam+Utara,+Kota+Pagar+Alam,+Sumatera+Selatan+31518/@-4.009688,103.251616,19z/data=!3m1!4b1!4m6!3m5!1s0x2e376bcfa6a1309b:0x25f9b4934af9e23!8m2!3d-4.0097485!4d103.2522801!16s%2Fg%2F11b8tb2nvs?entry=tts&g_ep=EgoyMDI2MDMxMS4wIPu8ASoASAFQAw%3D%3D&skid=dc3db14b-0448-4323-9532-19dad4733dc8' },
  { key: 'dist_spbu_air_perikan',     label: 'SPBU AIR PERIKAN',     maps_link: 'https://www.google.com/maps/place/SPBU+Air+Perikan/@-4.0293718,103.2331468,17z/data=!3m1!4b1!4m6!3m5!1s0x2e376b91a3f0dc05:0x6203371061a1520d!8m2!3d-4.0293718!4d103.2357164!16s%2Fg%2F11fylstx8f?entry=tts&g_ep=EgoyMDI2MDMxMS4wIPu8ASoASAFQAw%3D%3D&skid=0a0a4a5e-118d-4e3d-bed2-2cf86c8b7a50' },
  { key: 'dist_spbu_simpang_manna',   label: 'SPBU SIMPANG MANNA',   maps_link: 'https://www.google.com/maps/place/SPBU+Simpang+Manna/@-4.0338592,103.2615509,17z/data=!3m1!4b1!4m6!3m5!1s0x2e376bfdaf413cbb:0x26a62f638809e04f!8m2!3d-4.0338592!4d103.2641258!16s%2Fg%2F11cjkvdm4g?entry=tts&g_ep=EgoyMDI2MDMxMS4wIPu8ASoASAFQAw%3D%3D&skid=4086c1d7-c80b-4374-861b-75c745b3b2cb' },
  { key: 'dist_spbu_pengandonan',     label: 'SPBU PENGANDONAN',     maps_link: 'https://www.google.com/maps/place/Pertamina+SPBU+24.315.50+Selibar/@-3.9955929,103.0895486,9.7z/data=!4m7!3m6!1s0x2e376a4c14023641:0xd6b08af48af0de4c!8m2!3d-3.9975673!4d103.236383!15sCg9TUEJVIFBlcmFuZG9uYW5aESIPc3BidSBwZXJhbmRvbmFukgELZ2FzX3N0YXRpb26aASNDaFpEU1VoTk1HOW5TMFZKUTBGblNVUXRkazVIUkdOUkVBReABAPoBBAgAEAw!16s%2Fg%2F11c5zwqfqt?entry=tts&g_ep=EgoyMDI2MDMxMS4wIPu8ASoASAFQAw%3D%3D&skid=5d717224-a3b1-44de-a561-d155cd9fba77' },
  { key: 'dist_spbu_karang_dalo',     label: 'SPBU KARANG DALO',     maps_link: 'https://www.google.com/maps/place/SPBU+KARANG+DALO/@-4.0543492,103.2912487,17z/data=!3m1!4b1!4m6!3m5!1s0x2e376f76b3560495:0xf85d84e2e090cb35!8m2!3d-4.0543492!4d103.2938236!16s%2Fg%2F11fppg5bff?entry=tts&g_ep=EgoyMDI2MDMxMS4wIPu8ASoASAFQAw%3D%3D&skid=6a444ca2-31ed-4cc6-b5ac-62c66f78dc12' },
]

function starClass(rating, starIndex) {
  if (rating >= starIndex) return 'full'
  if (rating >= starIndex - 0.5) return 'half'
  return 'empty'
}

async function fetchDetail() {
  loading.value = true
  error.value   = ''
  try {
    const res = await fetch(`${API_BASE}/api/v1/tourism/${id}`)
    if (res.status === 404) {
      error.value = `Wisata dengan ID ${id} tidak ditemukan.`
      return
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    item.value = await res.json()
  } catch (e) {
    error.value = e.message.includes('fetch')
      ? 'Server backend tidak dapat dihubungi. Jalankan: uvicorn app.main:app --reload'
      : e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchDetail)
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
.detail-hero {
  background: linear-gradient(135deg, #2EC4C4 0%, #1BA8A8 100%);
  color: #fff;
  padding: 18px 20px 16px;
  text-align: center;
}
.detail-hero h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: 0.5px;
}
.detail-hero-sub {
  font-size: 0.8rem;
  opacity: 0.88;
  margin-top: 4px;
  font-weight: 500;
}
.star-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  margin-top: 8px;
}
.star { font-size: 1.2rem; line-height: 1; }
.star.full  { color: #f5c518; }
.star.half  { color: #f5c518; opacity: 0.6; }
.star.empty { color: rgba(255,255,255,0.4); }
.rating-val {
  font-size: 0.8rem;
  font-weight: 700;
  color: rgba(255,255,255,0.9);
  margin-left: 6px;
}
.star-row-detail {
  display: flex;
  align-items: center;
  gap: 2px;
}
.star-detail { font-size: 1.1rem; line-height: 1; }
.star-detail.full  { color: #f5c518; }
.star-detail.half  { color: #f5c518; opacity: 0.65; }
.star-detail.empty { color: rgba(255,255,255,0.35); }
.rating-val-detail {
  font-size: 0.82rem;
  font-weight: 700;
  color: rgba(255,255,255,0.9);
  margin-left: 6px;
}
.detail-body {
  background: #2EC4C4;
  flex: 1;
  padding: 10px 16px 20px;
  overflow-y: auto;
}
.section-title {
  font-size: 0.7rem;
  font-weight: 800;
  color: rgba(255,255,255,0.6);
  letter-spacing: 1.2px;
  text-transform: uppercase;
  padding: 10px 0 4px;
  border-bottom: 1px solid rgba(255,255,255,0.15);
  margin-bottom: 2px;
}
.detail-row {
  border-bottom: 1px solid rgba(255,255,255,0.25);
  padding: 10px 0;
}
.detail-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: rgba(255,255,255,0.85);
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.detail-value {
  font-size: 0.92rem;
  font-weight: 600;
  color: #fff;
}

.facility-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px 10px;
  margin-top: 6px;
}
.facility-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  font-size: 0.84rem;
  font-weight: 500;
}
.check {
  width: 22px; height: 22px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem;
  font-weight: 800;
  background: rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.5);
  flex-shrink: 0;
}
.check.active {
  background: #fff;
  color: #1BA8A8;
}

.dist-val { font-size: 0.88rem; font-weight: 700; }
.tel-link { color: #fff; font-weight: 700; text-decoration: underline; }
.lokasi-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 18px 0 4px;
  padding: 12px 20px;
  background: rgba(255,255,255,0.95);
  color: #1BA8A8;
  border-radius: 30px;
  font-weight: 700;
  font-size: 0.88rem;
  text-decoration: none;
  box-shadow: 0 3px 12px rgba(0,0,0,0.15);
}
.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 50px 20px;
  color: #1a3a5c;
  font-size: 0.9rem;
  text-align: center;
}
.error-msg { color: #c0392b; }
.spinner {
  width: 36px; height: 36px;
  border: 4px solid #e0f5f5;
  border-top-color: #2EC4C4;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.retry-btn {
  padding: 8px 20px;
  background: #2EC4C4;
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
}
.pdf-btn {
  background: #ff8c8c;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.pdf-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
