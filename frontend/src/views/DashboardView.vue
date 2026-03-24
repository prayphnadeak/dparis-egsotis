<template>
  <div class="page-wrapper">
    <AppHeader title="DASHBOARD" />

    <div class="teal-block" style="flex:1; overflow-y:auto;">
      <div v-if="loading" class="loading-state">
        <p>Memuat Data...</p>
      </div>
      <div v-else class="dashboard-content">
        <!-- Visitors and Downloaders -->
        <h3 class="section-title">Aktivitas Pengguna (Akumulatif)</h3>
        <div class="stats-card">
          <div class="range-controls" v-if="rawLabels.length > 0">
            <div class="range-labels">
              <span>{{ rawLabels[startIndex] }}</span>
              <span style="opacity: 0.5;">HINGGA</span>
              <span>{{ rawLabels[endIndex] }}</span>
            </div>
            <div class="slider-container">
              <div class="slider-track" :style="trackStyle"></div>
              <input type="range" :min="0" :max="rawLabels.length - 1" v-model.number="startIndex" @input="enforceRange" class="slider-thumb slider-left" />
              <input type="range" :min="0" :max="rawLabels.length - 1" v-model.number="endIndex" @input="enforceRange" class="slider-thumb slider-right" />
            </div>
          </div>
          <div style="height: 250px; margin-top: 10px;">
            <Line v-if="chartData" :data="chartData" :options="chartOptions" />
          </div>
        </div>

        <h3 class="section-title">Konten Direktori</h3>
        
        <div class="stats-card">
          <h4 class="card-title">Wisata ({{ wisataTotal }})</h4>
          <h5 class="sub-title" style="margin-top:16px;">Menurut Daya Tarik Utama</h5>
          <div class="category-list">
            <div class="category-item" v-for="(count, name) in wisataDayaTarik" :key="'dt-' + name">
              <span>{{ name || 'Lainnya' }}</span>
              <span class="badge">{{ count }}</span>
            </div>
          </div>
        </div>

        <div class="stats-card">
          <h4 class="card-title">Akomodasi ({{ akomodasiTotal }})</h4>
          <div style="height: 180px; margin-top: 10px; display: flex; justify-content: center;">
            <Pie v-if="akomodasiChartData" :data="akomodasiChartData" :options="pieOptions" />
          </div>
        </div>

        <div class="stats-card">
          <h4 class="card-title">Kuliner ({{ kulinerTotal }})</h4>
          <div class="category-list">
            <div class="category-item" v-for="(count, name) in kulinerCategories" :key="name">
              <span>{{ name || 'Lainnya' }}</span>
              <span class="badge">{{ count }}</span>
            </div>
          </div>
        </div>

        <div class="stats-card">
          <h4 class="card-title">Oleh-Oleh ({{ oleholehTotal }})</h4>
          <div class="category-list">
            <div class="category-item" v-for="(count, name) in oleholehCategories" :key="name">
              <span>{{ name || 'Lainnya' }}</span>
              <span class="badge">{{ count }}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
    
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'

import { Line, Pie } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler, ArcElement } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler, ArcElement)

const API_BASE = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : ''

const loading = ref(true)

const rawLabels = ref([])
const rawVisData = ref([])
const rawDlData = ref([])

const startIndex = ref(0)
const endIndex = ref(0)

const trackStyle = computed(() => {
  if (rawLabels.value.length <= 1) return { left: '0%', width: '100%' }
  const total = rawLabels.value.length - 1
  const left = (startIndex.value / total) * 100
  const width = ((endIndex.value - startIndex.value) / total) * 100
  return { left: `${left}%`, width: `${width}%` }
})

const enforceRange = () => {
  if (startIndex.value > endIndex.value) {
    const temp = startIndex.value
    startIndex.value = endIndex.value
    endIndex.value = temp
  }
  updateChartData()
}

const updateChartData = () => {
  if (rawLabels.value.length === 0) return

  const s = startIndex.value
  const e = endIndex.value + 1

  chartData.value = {
    labels: rawLabels.value.slice(s, e),
    datasets: [
      {
        label: 'Total Pengunjung',
        data: rawVisData.value.slice(s, e),
        borderColor: '#20b2aa',
        backgroundColor: 'rgba(32, 178, 170, 0.2)',
        fill: true,
        tension: 0.3,
        pointRadius: 3
      },
      {
        label: 'Total Pengunduh',
        data: rawDlData.value.slice(s, e),
        borderColor: '#ff9800',
        backgroundColor: 'rgba(255, 152, 0, 0.3)',
        fill: true,
        tension: 0.3,
        pointRadius: 3
      }
    ]
  }
}

const chartData = ref(null)
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } },
    tooltip: { mode: 'index', intersect: false }
  },
  interaction: { mode: 'index', intersect: false },
  scales: {
    y: { display: true, beginAtZero: false, ticks: { precision: 0 } },
    x: { display: true }
  }
}

const wisataTotal = ref(0)
const wisataCategories = ref({})
const wisataDayaTarik = ref({})

const akomodasiTotal = ref(0)
const akomodasiCategories = ref({})
const akomodasiChartData = ref(null)

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'right', labels: { boxWidth: 12, font: { size: 10 } } },
    tooltip: { enabled: true }
  }
}

const kulinerTotal = ref(0)
const kulinerCategories = ref({})

const oleholehTotal = ref(0)
const oleholehCategories = ref({})

const fetchStats = async () => {
  try {
    const [dailyRes, countsRes] = await Promise.all([
      fetch(`${API_BASE}/api/v1/statistics/daily`),
      fetch(`${API_BASE}/api/v1/statistics/dashboard_counts`)
    ])
    
    if (dailyRes.ok) {
      const dailyLogs = await dailyRes.json()
      
      let curVisitor = 238
      let curDl = 30
      const labels = ['24/03/2026']
      const visData = [curVisitor]
      const dlData = [curDl]

      dailyLogs.forEach(row => {
        curVisitor += row.visitor_count
        curDl += row.downloader_count
        
        const [y, m, d] = row.date.split('-')
        labels.push(`${d}/${m}/${y}`)
        visData.push(curVisitor)
        dlData.push(curDl)
      })

      rawLabels.value = labels
      rawVisData.value = visData
      rawDlData.value = dlData

      startIndex.value = 0
      endIndex.value = labels.length - 1

      updateChartData()
    }

    if (countsRes.ok) {
      const counts = await countsRes.json()
      
      wisataTotal.value = counts.wisata?.total || 0
      wisataCategories.value = counts.wisata?.categories || {}
      wisataDayaTarik.value = counts.wisata?.daya_tarik || {}
      
      akomodasiTotal.value = counts.akomodasi?.total || 0
      akomodasiCategories.value = counts.akomodasi?.categories || {}
      
      const akomLabels = Object.keys(akomodasiCategories.value)
      const akomData = []
      const akomFormattedLabels = []
      
      akomLabels.forEach(cat => {
        const count = akomodasiCategories.value[cat]
        akomData.push(count)
        const pct = akomodasiTotal.value > 0 ? Math.round((count / akomodasiTotal.value) * 100) : 0
        akomFormattedLabels.push(`${cat || 'Lainnya'} - ${count} (${pct}%)`)
      })
      
      if (akomData.length > 0) {
        akomodasiChartData.value = {
          labels: akomFormattedLabels,
          datasets: [{
            data: akomData,
            backgroundColor: ['#20b2aa', '#ff9800', '#f44336', '#9c27b0', '#3f51b5', '#00bcd4', '#4caf50'],
            borderWidth: 1
          }]
        }
      }
      
      kulinerTotal.value = counts.kuliner?.total || 0
      kulinerCategories.value = counts.kuliner?.categories || {}
      
      oleholehTotal.value = counts.oleholeh?.total || 0
      oleholehCategories.value = counts.oleholeh?.categories || {}
    }

  } catch (e) {
    console.error('Error fetching dashboard data:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
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
.teal-block {
  background: #20b2aa;
  padding: 16px;
  flex: 1;
  overflow-y: auto;
}
.loading-state {
  text-align: center;
  color: #fff;
  font-weight: 500;
  margin-top: 40px;
}
.section-title {
  color: #fff;
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 12px;
  margin-top: 8px;
  text-transform: uppercase;
}
.stats-card {
  background: rgba(255,255,255,0.95);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.card-title {
  margin: 0 0 12px 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: #1a3a5c;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 8px;
  margin-bottom: 12px;
}
.sub-title {
  margin: 0 0 8px 0;
  font-size: 0.8rem;
  font-weight: 700;
  color: #2EC4C4;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.stat-row:last-child {
  margin-bottom: 0;
}
.stat-label {
  font-size: 0.85rem;
  color: #444;
  font-weight: 600;
}
.stat-value {
  font-size: 1.1rem;
  color: #20b2aa;
  font-weight: 800;
}
.category-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.82rem;
  color: #555;
  background: #f8fafc;
  padding: 6px 12px;
  border-radius: 6px;
}
.badge {
  background: #1a3a5c;
  color: #fff;
  font-weight: 700;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
}

/* Range Slider */
.range-controls {
  margin-bottom: 20px;
  padding: 0 5px;
}
.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  font-weight: 700;
  color: #1a3a5c;
  margin-bottom: 12px;
}
.slider-container {
  position: relative;
  width: 100%;
  height: 24px;
}
.slider-track {
  position: absolute;
  top: 10px;
  height: 4px;
  background: #20b2aa;
  border-radius: 2px;
  z-index: 1;
}
.slider-container::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 0;
  width: 100%;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
}
.slider-thumb {
  position: absolute;
  pointer-events: none;
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 0; 
  top: 12px;
  background: transparent;
  outline: none;
  margin: 0;
  z-index: 2;
}
.slider-thumb::-webkit-slider-thumb {
  pointer-events: all;
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  border: 4px solid #20b2aa;
  box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
</style>
