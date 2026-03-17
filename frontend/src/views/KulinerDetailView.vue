<template>
  <div class="page-wrapper">
    <AppHeader title="KULINER" />

    <!-- Loading -->
    <div v-if="loading" class="state-msg">
      <div class="spinner"></div>
      <span>Memuat detail kuliner...</span>
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
          <div class="detail-label">NAMA TEMPAT MAKAN</div>
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
        <div class="detail-row" v-if="item.menu_highlights">
          <div class="detail-label">MENU UNGGULAN</div>
          <div class="detail-value">{{ item.menu_highlights }}</div>
        </div>
        <div class="detail-row" v-if="item.description">
          <div class="detail-label">DESKRIPSI</div>
          <div class="detail-value">{{ item.description }}</div>
        </div>

        <!-- Distances to landmarks -->
        <div class="section-title" style="margin-top:14px;">JARAK KE LANDMARK (KM)</div>
        <div class="detail-row" v-for="lm in landmarks" :key="lm.key">
          <div class="detail-label">{{ lm.label }}</div>
          <div class="detail-value dist-val">
            <span v-if="item[lm.key] !== null && item[lm.key] !== undefined">
              {{ Number(item[lm.key]).toFixed(2) }} km
            </span>
            <span v-else>-</span>
          </div>
        </div>

        <!-- Maps button -->
        <a v-if="item.maps_link" :href="item.maps_link" target="_blank" rel="noopener" class="lokasi-btn">
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

const API_BASE = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : ''

const route  = useRoute()
const id     = parseInt(route.params.id)

const item    = ref(null)
const loading = ref(true)
const error   = ref('')

const landmarks = [
  { key: 'dist_gunung_dempo',         label: 'GUNUNG DEMPO'         },
  { key: 'dist_pasar_dempo_permai',   label: 'PASAR DEMPO PERMAI'   },
  { key: 'dist_bandara_atung_bungsu', label: 'BANDARA ATUNG BUNGSU' },
  { key: 'dist_rsud_besemah',         label: 'RSUD BESEMAH'         },
  { key: 'dist_spbu_air_perikan',     label: 'SPBU AIR PERIKAN'     },
  { key: 'dist_spbu_simpang_manna',   label: 'SPBU SIMPANG MANNA'   },
  { key: 'dist_spbu_pengandonan',     label: 'SPBU PENGANDONAN'     },
  { key: 'dist_spbu_karang_dalo',     label: 'SPBU KARANG DALO'     },
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
    const res = await fetch(`${API_BASE}/api/v1/culinary/${id}`)
    if (res.status === 404) {
      error.value = `Kuliner dengan ID ${id} tidak ditemukan.`
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
.star-row-detail { display: flex; align-items: center; gap: 2px; }
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
</style>
