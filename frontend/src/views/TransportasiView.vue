<template>
  <div class="page-wrapper">
    <AppHeader title="TRANSPORTASI" />

    <!-- Search Bar -->
    <div class="search-bar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <input v-model="search" type="text" placeholder="Cari transportasi..." @input="onSearch" />
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
      <div v-if="showCategoryDropdown || showFacilityDropdown || showLimitDropdown || showSortDropdown" class="dropdown-backdrop" @click="closeDropdowns"></div>

      <!-- Row 1: Tampil & Urutkan -->
      <div class="filter-row">
        <!-- Limit Filter -->
        <div class="filter-dropdown" style="flex: 0.4;">
          <div class="filter-select" @click="showLimitDropdown = !showLimitDropdown; showCategoryDropdown = false; showFacilityDropdown = false; showSortDropdown = false">
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
          <div class="filter-select" @click="showSortDropdown = !showSortDropdown; showCategoryDropdown = false; showFacilityDropdown = false; showLimitDropdown = false">
            <span class="filter-label">URUTKAN: {{ sortLabel }}</span>
          </div>
          <div v-if="showSortDropdown" class="dropdown-menu teal-block-scroll">
            <label v-for="opt in sortOptions" :key="opt.label" class="dropdown-item" @click="applySort(opt)">
              {{ opt.label }}
            </label>
          </div>
        </div>
      </div>

      <!-- Row 2: Moda & Rute -->
      <div class="filter-row">
        <!-- Category Filter -->
        <div class="filter-dropdown" style="flex: 1;">
          <div class="filter-select" @click="showCategoryDropdown = !showCategoryDropdown; showFacilityDropdown = false; showLimitDropdown = false">
            <span class="filter-label">MODA TRANSPORTASI <span v-if="selectedCategories.length">({{ selectedCategories.length }})</span></span>
          </div>
          <div v-if="showCategoryDropdown" class="dropdown-menu teal-block-scroll">
            <label class="dropdown-item">
              <input type="checkbox" :checked="selectedCategories.length === uniqueCategories.length && uniqueCategories.length > 0" @change="toggleAllCategories" />
              Pilih Semua
            </label>
            <label v-for="cat in uniqueCategories" :key="cat" class="dropdown-item">
              <input type="checkbox" :value="cat" v-model="selectedCategories" />
              {{ cat }}
            </label>
          </div>
        </div>

        <!-- Facility Filter -->
        <div class="filter-dropdown" style="flex: 1;">
          <div class="filter-select" @click="showFacilityDropdown = !showFacilityDropdown; showCategoryDropdown = false; showLimitDropdown = false">
            <span class="filter-label">RUTE <span v-if="selectedFacilities.length">({{ selectedFacilities.length }})</span></span>
          </div>
          <div v-if="showFacilityDropdown" class="dropdown-menu teal-block-scroll">
            <label class="dropdown-item">
              <input type="checkbox" :checked="selectedFacilities.length === facilityOptions.length && facilityOptions.length > 0" @change="toggleAllFacilities" />
              Pilih Semua
            </label>
            <label v-for="opt in facilityOptions" :key="opt.value" class="dropdown-item">
              <input type="checkbox" :value="opt.value" v-model="selectedFacilities" />
              {{ opt.label }}
            </label>
          </div>
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
    <div v-else class="teal-block-scroll" style="margin-top:14px; position:relative; padding-bottom: 70px;">
      <div
        v-for="item in paginatedData"
        :key="item.id"
        class="list-card"
        @click="goDetail(item.id)"
      >
        <div class="list-card-name">{{ item.name }}</div>
        <div class="list-card-sub">{{ item.category }}</div>
        <div class="star-row" v-if="item.rating !== null && item.rating !== undefined">
          <span v-for="s in 5" :key="s" class="star" :class="starClass(item.rating, s)">&#9733;</span>
          <span class="rating-val">{{ item.rating ? item.rating.toFixed(1) : '' }}</span>
        </div>
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

const router  = useRouter()
const search  = ref('')
const akomodasi = ref([])
const loading = ref(true)
const error   = ref('')

const mostViewed = computed(() => {
  if (!akomodasi.value.length) return null
  return [...akomodasi.value].sort((a, b) => (b.view_count || 0) - (a.view_count || 0))[0]
})

async function fetchData() {
  loading.value = true
  error.value   = ''
  try {
    const url = search.value
      ? `${API_BASE}/api/v1/transportations/?q=${encodeURIComponent(search.value)}`
      : `${API_BASE}/api/v1/transportations/`
    const res = await fetch(url)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    akomodasi.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

// Dropdown states
const showCategoryDropdown = ref(false)
const showFacilityDropdown = ref(false)
const showLimitDropdown = ref(false)
const showSortDropdown = ref(false)
const closeDropdowns = () => {
  showCategoryDropdown.value = false
  showFacilityDropdown.value = false
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

// Client-side filter as fallback and for dropdowns
const itemsLimit = ref(10)
const selectedCategories = ref([])
const selectedFacilities = ref([])

function toggleAllCategories(e) {
  if (e.target.checked) {
    selectedCategories.value = [...uniqueCategories.value]
  } else {
    selectedCategories.value = []
  }
}

function toggleAllFacilities(e) {
  if (e.target.checked) {
    selectedFacilities.value = facilityOptions.map(opt => opt.value)
  } else {
    selectedFacilities.value = []
  }
}

const uniqueCategories = computed(() => {
  const cats = new Set(akomodasi.value.map(a => a.category))
  return Array.from(cats).filter(Boolean).sort()
})

const facilityOptions = [
  { label: 'Palembang', value: 'route_palembang' },
  { label: 'Bengkulu', value: 'route_bengkulu' },
  { label: 'Lampung', value: 'route_lampung' },
  { label: 'Jabodetabek', value: 'route_jabodetabek' },
  { label: 'Jawa', value: 'route_jawa' }
]

const filtered = computed(() => {
  let result = akomodasi.value

  const q = search.value.toLowerCase()
  if (q) {
    result = result.filter(
      a => a.name.toLowerCase().includes(q) || a.category.toLowerCase().includes(q)
    )
  }

  if (selectedCategories.value.length > 0) {
    result = result.filter(a => selectedCategories.value.includes(a.category))
  }

  if (selectedFacilities.value.length > 0) {
    // Memfilter transportasi yang melayani SEMUA rute yang dipilih (AND logic)
    result = result.filter(a => selectedFacilities.value.every(f => a[f]))
  }

  return result
})

// Pagination logic
const currentPage = ref(1)

watch([search, selectedCategories, selectedFacilities, itemsLimit], () => {
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

let searchTimer = null
function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchData, 350)
}

function starClass(rating, starIndex) {
  if (rating >= starIndex) return 'full'
  if (rating >= starIndex - 0.5) return 'half'
  return 'empty'
}

const goDetail = (id) => router.push(`/transportasi/${id}`)

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
.list-card-name {
  font-size: 1rem;
  font-weight: 700;
}
.list-card-sub {
  font-size: 0.78rem;
  opacity: 0.8;
  margin-top: 3px;
  font-weight: 500;
}
.star-row {
  display: flex;
  align-items: center;
  gap: 1px;
  margin-top: 6px;
}
.star {
  font-size: 1rem;
  line-height: 1;
  color: #ccc;
  transition: color 0.15s;
}
.star.full  { color: #f5c518; }
.star.half  { color: #f5c518; opacity: 0.6; }
.star.empty { color: #ddd; }
.rating-val {
  font-size: 0.75rem;
  font-weight: 700;
  color: rgba(255,255,255,0.85);
  margin-left: 5px;
}
.empty-msg {
  text-align: center;
  color: rgba(255,255,255,0.7);
  padding: 30px 0;
  font-size: 0.9rem;
}
.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 20px;
  color: #1a3a5c;
  font-size: 0.9rem;
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

/* Filters */
.filters-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 10px;
  margin-top: 14px;
  position: relative;
}
.filter-row { display: flex; gap: 6px; width: 100%; }
.filter-dropdown {
  position: relative;
  flex: 1;
  min-width: 0;
}
.filter-select {
  padding: 7px 8px;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.1);
  background: #f7f9fa;
  font-size: 0.74rem;
  color: #1a3a5c;
  outline: none;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.filter-select::after {
  content: '';
  display: block;
  width: 10px;
  height: 10px;
  background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" stroke="%231a3a5c" stroke-width="2" xmlns="http://www.w3.org/2000/svg"><polyline points="6 9 12 15 18 9"/></svg>');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  margin-left: 2px;
}
.filter-label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.dropdown-backdrop {
  position: fixed;
  inset: 0;
  z-index: 40;
}
.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  min-width: 100%;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 50;
  max-height: 250px;
  overflow-y: auto;
  padding: 8px 0;
  border: 1px solid rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
}
.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  font-size: 0.85rem;
  color: #333;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}
.dropdown-item:hover {
  background: #f0f4f8;
}
.dropdown-item input[type="checkbox"] {
  margin-right: 10px;
  width: 16px;
  height: 16px;
  accent-color: #2EC4C4;
  cursor: pointer;
}

/* Pagination */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px 0;
  background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.9) 30%, rgba(255,255,255,1) 100%);
}
.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #2EC4C4;
  color: #fff;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 6px rgba(46, 196, 196, 0.3);
}
.page-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(46, 196, 196, 0.4);
}
.page-btn:disabled {
  background: #cad5d5;
  color: #8fa5a5;
  cursor: not-allowed;
  box-shadow: none;
}
.page-info {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1a3a5c;
  background: #f0f4f8;
  padding: 6px 14px;
  border-radius: 20px;
}
</style>
