<template>
  <div class="page-wrapper">
    <AppHeader title="OLEH-OLEH" />

    <!-- Search Bar -->
    <div class="search-bar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <input v-model="search" type="text" placeholder="Cari toko oleh-oleh..." @input="onSearch" />
    </div>

    <!-- Most Viewed Banner -->
    <div v-if="mostViewed" class="most-viewed-banner">
      <span class="most-viewed-text">
        Jumlah Pencarian Terbanyak: 
        <span class="most-viewed-name">{{ mostViewed.name }}</span> 
        dengan <span class="most-viewed-count">{{ mostViewed.view_count || 0 }}</span> views
      </span>
    </div>

    <!-- Filters -->
    <div class="filters-container">
      <!-- Dropdown Backdrop -->
      <div v-if="showLimitDropdown || showSortDropdown" class="dropdown-backdrop" @click="closeDropdowns"></div>

      <!-- Row 1: Tampil & Urutkan -->
      <div class="filter-row">
        <!-- Limit Filter -->
        <div class="filter-dropdown" style="flex: 0.4; min-width: 120px;">
          <div class="filter-select" @click="showLimitDropdown = !showLimitDropdown; showSortDropdown = false">
            <span class="filter-label">TAMPIL: {{ itemsLimit }}</span>
          </div>
          <div v-if="showLimitDropdown" class="dropdown-menu teal-block-scroll">
            <label v-for="opt in [10, 20, 30, 40, 50, 75, 100]" :key="opt" class="dropdown-item" @click="itemsLimit = opt; showLimitDropdown = false">
              {{ opt }}
            </label>
          </div>
        </div>

        <!-- Sort Filter -->
        <div class="filter-dropdown" style="flex: 0.8; min-width: 150px;">
          <div class="filter-select" @click="showSortDropdown = !showSortDropdown; showLimitDropdown = false">
            <span class="filter-label">URUTKAN: {{ sortLabel }}</span>
          </div>
          <div v-if="showSortDropdown" class="dropdown-menu teal-block-scroll">
            <label v-for="opt in sortOptions" :key="opt.label" class="dropdown-item" @click="applySort(opt)">
              {{ opt.label }}
            </label>
          </div>
        </div>
      </div>

      <!-- Row 2: filter lainnya (Empty for now) -->
      <div class="filter-row" v-if="false"></div>
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
    <div v-else class="teal-block-scroll" style="margin-top:14px; position:relative; padding-bottom: 70px;">
      <div
        v-for="item in paginatedData"
        :key="item.id"
        class="list-card shop-card"
        @click="goToDetail(item.id)"
      >
        <div class="shop-info">
          <div class="list-card-name">{{ item.name }}</div>
          <div class="star-row" v-if="item.rating !== null && item.rating !== undefined">
            <span v-for="s in 5" :key="s" class="star" :class="starClass(item.rating, s)">&#9733;</span>
            <span class="rating-val">{{ item.rating ? item.rating.toFixed(1) : '' }}</span>
          </div>
          <div v-else class="shop-link-label">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
            </svg>
            Lihat di Google Maps
          </div>
        </div>
        <svg class="chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
        <!-- Hit view badge -->
        <div v-if="item.view_count !== undefined" class="hit-badge-card">
          👁 {{ item.view_count }} views
        </div>
      </div>
      <div v-if="filtered.length === 0" class="empty-msg">
        Tidak ada hasil ditemukan.
      </div>

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
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'

const API_BASE = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : ''
const router = useRouter()

const search  = ref('')
const shops   = ref([])
const loading = ref(true)
const error   = ref('')

const mostViewed = computed(() => {
  if (!shops.value.length) return null
  return [...shops.value].sort((a, b) => (b.view_count || 0) - (a.view_count || 0))[0]
})

async function fetchData() {
  loading.value = true
  error.value   = ''
  try {
    const url = `${API_BASE}/api/v1/souvenirs/`
    const res = await fetch(url)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    shops.value = await res.json()
  } catch (e) {
    error.value = e.message.includes('fetch')
      ? 'Server backend tidak dapat dihubungi. Jalankan: uvicorn app.main:app --reload (dari folder backend/)'
      : e.message
  } finally {
    loading.value = false
  }
}

// Client-side filter
const filtered = computed(() => {
  const q = search.value.toLowerCase()
  if (!q) return shops.value
  return shops.value.filter(s => s.name.toLowerCase().includes(q))
})

let searchTimer = null
function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchData, 350)
}

// Filters & Pagination
const showLimitDropdown = ref(false)
const showSortDropdown = ref(false)
const closeDropdowns = () => { 
  showLimitDropdown.value = false 
  showSortDropdown.value = false
}

const sortBy = ref('name')
const sortOrder = ref('asc')

const sortOptions = [
  { label: 'Nama (A-Z)', key: 'name', order: 'asc' },
  { label: 'Nama (Z-A)', key: 'name', order: 'desc' },
  { label: 'Rating (Tertinggi)', key: 'rating', order: 'desc' },
  { label: 'Rating (Terrendah)', key: 'rating', order: 'asc' },
  { label: 'Hit View (Terbanyak)', key: 'view_count', order: 'desc' },
  { label: 'Hit View (Tersedikit)', key: 'view_count', order: 'asc' }
]

const sortLabel = computed(() => {
  const opt = sortOptions.find(o => o.key === sortBy.value && o.order === sortOrder.value)
  return opt ? opt.label : 'Nama (A-Z)'
})

const applySort = (opt) => {
  sortBy.value = opt.key
  sortOrder.value = opt.order
  showSortDropdown.value = false
  currentPage.value = 1
}

const sorted = computed(() => {
  return [...filtered.value].sort((a, b) => {
    let vA = a[sortBy.value]
    let vB = b[sortBy.value]
    if (vA === null || vA === undefined) vA = sortBy.value === 'name' ? '' : 0
    if (vB === null || vB === undefined) vB = sortBy.value === 'name' ? '' : 0
    if (sortBy.value === 'name') {
      return sortOrder.value === 'asc' ? vA.localeCompare(vB) : vB.localeCompare(vA)
    }
    return sortOrder.value === 'asc' ? vA - vB : vB - vA
  })
})
const itemsLimit = ref(10)
const currentPage = ref(1)

watch([search, itemsLimit], () => {
  currentPage.value = 1
})

const totalPages = computed(() => Math.ceil(filtered.value.length / itemsLimit.value))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsLimit.value
  const end = start + itemsLimit.value
  return sorted.value.slice(start, end)
})

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const goToDetail = (id) => router.push({ name: 'oleholeh-detail', params: { id } })

function starClass(rating, starIndex) {
  if (rating >= starIndex) return 'full'
  if (rating >= starIndex - 0.5) return 'half'
  return 'empty'
}

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

function hasDistances(item) {
  return item && landmarks.some(lm => item[lm.key] !== null && item[lm.key] !== undefined)
}

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
.teal-block-scroll { flex: 1; }

/* Card override for clickable links */
.shop-card {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.12s, background 0.12s;
}
.shop-card:active {
  transform: scale(0.97);
  background: rgba(255,255,255,0.12);
}

.shop-no {
  min-width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  color: #fff;
  font-weight: 800;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.shop-info {
  flex: 1;
  min-width: 0;
}

.list-card-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.shop-link-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.72rem;
  color: rgba(255,255,255,0.75);
  margin-top: 3px;
  font-weight: 500;
}

.chevron {
  color: rgba(255,255,255,0.6);
  flex-shrink: 0;
}

.empty-msg {
  text-align: center;
  color: rgba(255,255,255,0.7);
  padding: 30px 0;
  font-size: 0.9rem;
}

/* Filters */
.filters-container { display: flex; flex-direction: column; gap: 8px; padding: 0 10px; margin-top: 14px; position: relative; }
.filter-row { display: flex; gap: 6px; width: 100%; }
.filter-dropdown { position: relative; min-width: 0; }
.filter-select { padding: 7px 8px; border-radius: 12px; border: 1px solid rgba(0,0,0,0.1); background: #f7f9fa; font-size: 0.74rem; color: #1a3a5c; outline: none; font-weight: 600; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
.filter-select::after { content: ''; display: block; width: 10px; height: 10px; background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" stroke="%231a3a5c" stroke-width="2" xmlns="http://www.w3.org/2000/svg"><polyline points="6 9 12 15 18 9"/></svg>'); background-repeat: no-repeat; background-position: center; background-size: contain; margin-left: 2px; }
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

.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 20px;
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

/* Star rating */
.star-row { display: flex; align-items: center; gap: 1px; margin-top: 5px; }
.star { font-size: 0.95rem; line-height: 1; color: rgba(255,255,255,0.3); }
.star.full  { color: #f5c518; }
.star.half  { color: #f5c518; opacity: 0.6; }
.star.empty { color: rgba(255,255,255,0.25); }
.rating-val { font-size: 0.72rem; font-weight: 700; color: rgba(255,255,255,0.85); margin-left: 5px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: flex-end; z-index: 100; }
.modal-card { background: #fff; border-radius: 24px 24px 0 0; width: 100%; max-width: 420px; margin: 0 auto; overflow: hidden; max-height: 80vh; overflow-y: auto; }
.modal-header { background: #2EC4C4; padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; color: #fff; font-weight: 700; font-size: 1.05rem; }
.modal-close { background: none; border: none; color: #fff; font-size: 1.1rem; cursor: pointer; }
.modal-body { padding: 20px; background: #2EC4C4; }
.detail-row { border-bottom: 1px solid rgba(255,255,255,0.25); padding: 10px 0; }
.detail-label { font-size: 0.68rem; font-weight: 700; color: rgba(255,255,255,0.85); letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 4px; }
.detail-value { font-size: 0.92rem; font-weight: 600; color: #fff; }
.star-row-modal { display: flex; align-items: center; gap: 2px; }
.star-modal { font-size: 1.05rem; line-height: 1; color: rgba(255,255,255,0.3); }
.star-modal.full  { color: #f5c518; }
.star-modal.half  { color: #f5c518; opacity: 0.6; }
.star-modal.empty { color: rgba(255,255,255,0.25); }
.rating-val-modal { font-size: 0.8rem; font-weight: 700; color: rgba(255,255,255,0.9); margin-left: 6px; }
.lokasi-btn { display: flex; align-items: center; justify-content: center; gap: 8px; margin: 16px 0 4px; padding: 12px 20px; background: rgba(255,255,255,0.95); color: #1BA8A8; border-radius: 30px; font-weight: 700; font-size: 0.88rem; text-decoration: none; box-shadow: 0 3px 12px rgba(0,0,0,0.15); }
.no-link-msg { margin-top: 16px; text-align: center; color: rgba(255,255,255,0.7); font-size: 0.85rem; }
.slide-up-enter-active { animation: slideUp 0.3s ease; }
.slide-up-leave-active { animation: slideUp 0.3s ease reverse; }
@keyframes slideUp { from { transform: translateY(100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
</style>
