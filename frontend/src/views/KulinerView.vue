<template>
  <div class="page-wrapper">
    <AppHeader title="KULINER" />

    <!-- Search Bar -->
    <div class="search-bar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <input v-model="search" type="text" placeholder="Cari tempat makan..." @input="onSearch" />
    </div>

    <!-- Filters -->
    <div class="filters-container">
      <!-- Dropdown Backdrop -->
      <div v-if="showLimitDropdown" class="dropdown-backdrop" @click="closeDropdowns"></div>

      <div style="flex: 1;"></div> <!-- Spacer -->

      <!-- Limit Filter -->
      <div class="filter-dropdown" style="flex: 0.4; min-width: 120px;">
        <div class="filter-select" @click="showLimitDropdown = !showLimitDropdown">
          <span class="filter-label">TAMPIL: {{ itemsLimit }}</span>
        </div>
        <div v-if="showLimitDropdown" class="dropdown-menu teal-block-scroll">
          <label v-for="opt in [10, 20, 30, 40, 50, 75, 100]" :key="opt" class="dropdown-item" @click="itemsLimit = opt; showLimitDropdown = false">
            {{ opt }}
          </label>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="state-msg">
      <div class="spinner"></div>
      <span>Memuat data...</span>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="state-msg error-msg">
      ⚠️ Gagal memuat data. Pastikan server backend berjalan.<br/>
      <small>{{ error }}</small>
      <button class="retry-btn" @click="fetchData">Coba Lagi</button>
    </div>

    <!-- List -->
    <div v-else class="teal-block-scroll" style="margin-top:14px; flex:1; position:relative; padding-bottom: 70px;">
      <div
        v-for="item in paginatedData"
        :key="item.id"
        class="list-card"
        @click="showDetail(item)"
      >
        <div class="list-card-name">{{ item.name }}</div>
        <div class="list-card-sub">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor" style="opacity:.7">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
          </svg>
          Tap untuk lihat lokasi
        </div>
      </div>
      <div v-if="filtered.length === 0" class="empty-msg">Tidak ada hasil ditemukan.</div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination-container">
        <button class="page-btn" :disabled="currentPage === 1" @click="prevPage">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
        <span class="page-info">Hal {{ currentPage }} dari {{ totalPages }}</span>
        <button class="page-btn" :disabled="currentPage === totalPages" @click="nextPage">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      </div>
    </div>

    <!-- Modal -->
    <transition name="slide-up">
      <div v-if="selected" class="modal-overlay" @click.self="selected = null">
        <div class="modal-card">
          <div class="modal-header">
            <span>{{ selected.name }}</span>
            <button class="modal-close" @click="selected = null">✕</button>
          </div>
          <div class="modal-body">
            <div class="detail-row">
              <div class="detail-label">NO</div>
              <div class="detail-value">{{ selected.id }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">NAMA TEMPAT</div>
              <div class="detail-value">{{ selected.name }}</div>
            </div>
            <a
              v-if="selected.maps_link"
              :href="selected.maps_link"
              target="_blank"
              rel="noopener"
              class="lokasi-btn"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
              LOKASI: Lihat di Google Maps
            </a>
            <div v-else class="no-link-msg">📍 Link lokasi belum tersedia</div>
          </div>
        </div>
      </div>
    </transition>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'

const API_BASE = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : ''

const search   = ref('')
const places   = ref([])
const loading  = ref(true)
const error    = ref('')
const selected = ref(null)

async function fetchData() {
  loading.value = true
  error.value   = ''
  try {
    const res = await fetch(`${API_BASE}/api/v1/culinary/`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    places.value = await res.json()
  } catch (e) {
    error.value = e.message.includes('fetch')
      ? 'Server backend tidak dapat dihubungi. Jalankan: uvicorn app.main:app --reload (dari folder backend/)'
      : e.message
  } finally {
    loading.value = false
  }
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  if (!q) return places.value
  return places.value.filter(p => p.name.toLowerCase().includes(q))
})

let searchTimer = null
function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchData, 350)
}

// Filters & Pagination
const showLimitDropdown = ref(false)
const closeDropdowns = () => { showLimitDropdown.value = false }
const itemsLimit = ref(10)
const currentPage = ref(1)

watch([search, itemsLimit], () => {
  currentPage.value = 1
})

const totalPages = computed(() => Math.ceil(filtered.value.length / itemsLimit.value))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsLimit.value
  const end = start + itemsLimit.value
  return filtered.value.slice(start, end)
})

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const showDetail = (item) => { selected.value = item }

onMounted(fetchData)
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
.list-card-name { font-size: 1rem; font-weight: 700; }
.list-card-sub {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.76rem;
  opacity: 0.8;
  margin-top: 3px;
  font-weight: 500;
}
.empty-msg { text-align: center; color: rgba(255,255,255,0.7); padding: 30px 0; font-size: 0.9rem; }

/* Filters */
.filters-container { display: flex; gap: 10px; padding: 0 16px; margin-top: 14px; position: relative; }
.filter-dropdown { position: relative; }
.filter-select { padding: 10px 12px; border-radius: 20px; border: 1px solid rgba(0,0,0,0.1); background: #f7f9fa; font-size: 0.82rem; color: #1a3a5c; outline: none; font-weight: 600; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
.filter-select::after { content: ''; display: block; width: 14px; height: 14px; background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" stroke="%231a3a5c" stroke-width="2" xmlns="http://www.w3.org/2000/svg"><polyline points="6 9 12 15 18 9"/></svg>'); background-repeat: no-repeat; background-position: center; background-size: contain; }
.filter-label { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.dropdown-backdrop { position: fixed; inset: 0; z-index: 40; }
.dropdown-menu { position: absolute; top: calc(100% + 8px); right: 0; min-width: 100%; background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 50; max-height: 250px; overflow-y: auto; padding: 8px 0; border: 1px solid rgba(0,0,0,0.05); display: flex; flex-direction: column; }
.dropdown-item { display: flex; align-items: center; padding: 10px 16px; font-size: 0.85rem; color: #333; cursor: pointer; transition: background 0.2s; white-space: nowrap; }
.dropdown-item:hover { background: #f0f4f8; }

/* Pagination */
.pagination-container { display: flex; justify-content: center; align-items: center; gap: 12px; position: absolute; bottom: 0; left: 0; right: 0; padding: 16px 0; background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.9) 30%, rgba(255,255,255,1) 100%); z-index: 10; }
.page-btn { display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: #2EC4C4; color: #fff; border: none; border-radius: 50%; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 6px rgba(46, 196, 196, 0.3); }
.page-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 10px rgba(46, 196, 196, 0.4); }
.page-btn:disabled { background: #cad5d5; color: #8fa5a5; cursor: not-allowed; box-shadow: none; }
.page-info { font-size: 0.82rem; font-weight: 700; color: #1a3a5c; background: #f0f4f8; padding: 6px 14px; border-radius: 20px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: flex-end; z-index: 100; }
.modal-card { background: #fff; border-radius: 24px 24px 0 0; width: 100%; max-width: 420px; margin: 0 auto; overflow: hidden; }
.modal-header { background: #2EC4C4; padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; color: #fff; font-weight: 700; font-size: 1.05rem; }
.modal-close { background: none; border: none; color: #fff; font-size: 1.1rem; cursor: pointer; }
.modal-body { padding: 20px; background: #2EC4C4; }
.detail-row { border-bottom: 1px solid rgba(255,255,255,0.25); padding: 10px 0; }
.detail-label { font-size: 0.68rem; font-weight: 700; color: rgba(255,255,255,0.85); letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 4px; }
.detail-value { font-size: 0.92rem; font-weight: 600; color: #fff; }
.lokasi-btn {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  margin: 16px 0 4px; padding: 12px 20px;
  background: rgba(255,255,255,0.95); color: #1BA8A8;
  border-radius: 30px; font-weight: 700; font-size: 0.88rem;
  text-decoration: none; box-shadow: 0 3px 12px rgba(0,0,0,0.15);
}
.no-link-msg {
  margin-top: 16px; text-align: center;
  color: rgba(255,255,255,0.7); font-size: 0.85rem;
}

/* State messages */
.state-msg { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 40px 20px; color: #1a3a5c; font-size: 0.9rem; text-align: center; }
.error-msg { color: #c0392b; }
.spinner { width: 36px; height: 36px; border: 4px solid #e0f5f5; border-top-color: #2EC4C4; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.retry-btn { margin-top: 8px; padding: 8px 20px; background: #2EC4C4; color: #fff; border: none; border-radius: 20px; cursor: pointer; font-weight: 600; }

/* Animation */
.slide-up-enter-active { animation: slideUp 0.3s ease; }
.slide-up-leave-active { animation: slideUp 0.3s ease reverse; }
@keyframes slideUp { from { transform: translateY(100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
</style>
