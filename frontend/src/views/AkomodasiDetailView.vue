<template>
  <div class="page-wrapper">
    <AppHeader title="AKOMODASI" />

    <!-- Loading -->
    <div v-if="loading" class="state-msg">
      <div class="spinner"></div>
      <span>Memuat detail akomodasi...</span>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="state-msg error-msg">
      ⚠️ {{ error }}
      <button class="retry-btn" @click="fetchDetail">Coba Lagi</button>
    </div>

    <!-- Content -->
    <template v-else-if="item">
      <!-- Name hero -->
      <div class="detail-hero">
        <h2>{{ item.name }}</h2>
        <div class="detail-hero-sub">{{ item.category }}</div>
      </div>

      <!-- Detail body -->
      <div class="detail-body" style="flex:1; overflow-y:auto;">
        <div class="detail-row">
          <div class="detail-label">NO</div>
          <div class="detail-value">{{ item.id }}</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">ALAMAT</div>
          <div class="detail-value">{{ item.address || '-' }}</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">NOMOR TELEPON</div>
          <div class="detail-value">
            <a v-if="item.phone" :href="`tel:${item.phone}`" class="tel-link">
              {{ item.phone }}
            </a>
            <span v-else>-</span>
          </div>
        </div>
        <div class="detail-row">
          <div class="detail-label">KATEGORI AKOMODASI</div>
          <div class="detail-value">{{ item.category }}</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">JUMLAH KAMAR</div>
          <div class="detail-value">{{ item.total_rooms }} kamar</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">JUMLAH TEMPAT TIDUR</div>
          <div class="detail-value">{{ item.total_beds }} tempat tidur</div>
        </div>

        <!-- Facilities -->
        <div class="detail-row">
          <div class="detail-label">FASILITAS</div>
          <div class="facility-grid">
            <div v-for="f in facilities" :key="f.key" class="facility-item">
              <div class="check" :class="{ active: item[f.key] }">
                {{ item[f.key] ? '✓' : '✗' }}
              </div>
              <span>{{ f.name }}</span>
            </div>
          </div>
        </div>

        <!-- Location button -->
        <a
          v-if="item.maps_link"
          :href="item.maps_link"
          target="_blank"
          rel="noopener"
          class="lokasi-btn"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
          </svg>
          LOKASI: Lihat di Google Maps
        </a>
      </div>
    </template>

    <!-- Not found -->
    <div v-else class="state-msg">Data tidak ditemukan.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppHeader from '../components/AppHeader.vue'

const API_BASE = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : ''

const route  = useRoute()
const router = useRouter()
const id     = parseInt(route.params.id)

const item    = ref(null)
const loading = ref(true)
const error   = ref('')

// Daftar fasilitas yang ditampilkan
const facilities = [
  { key: 'hot_water',    name: 'Air Panas/Dingin' },
  { key: 'tv_cable',     name: 'TV Kabel'         },
  { key: 'free_wifi',    name: 'Free Wifi'         },
  { key: 'restaurant',   name: 'Restoran'          },
  { key: 'swimming_pool',name: 'Kolam Renang'      },
  { key: 'gym',          name: 'Kebugaran'         },
  { key: 'meeting_room', name: 'Ruang Meeting'     },
]

async function fetchDetail() {
  loading.value = true
  error.value   = ''
  try {
    const res = await fetch(`${API_BASE}/api/v1/accommodations/${id}`)
    if (res.status === 404) {
      error.value = `Akomodasi dengan ID ${id} tidak ditemukan.`
      return
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    item.value = await res.json()
  } catch (e) {
    if (e.message.includes('fetch')) {
      error.value = 'Server backend tidak dapat dihubungi. Jalankan: uvicorn app.main:app --reload (dari folder backend/)'
    } else {
      error.value = e.message
    }
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
.detail-body {
  background: #2EC4C4;
  flex: 1;
  padding: 10px 16px 20px;
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
.tel-link {
  color: #fff;
  font-weight: 700;
  text-decoration: underline;
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
  transition: transform 0.15s, box-shadow 0.15s;
}
.lokasi-btn:active {
  transform: scale(0.97);
  box-shadow: 0 1px 6px rgba(0,0,0,0.12);
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
  margin-top: 8px;
  padding: 8px 20px;
  background: #2EC4C4;
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
}
</style>
