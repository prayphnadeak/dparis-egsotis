import { createRouter, createWebHistory } from 'vue-router'
import WelcomeView from '../views/WelcomeView.vue'
import AkomodasiView from '../views/AkomodasiView.vue'
import AkomodasiDetailView from '../views/AkomodasiDetailView.vue'
import WisataView from '../views/WisataView.vue'
import WisataDetailView from '../views/WisataDetailView.vue'
import KulinerView from '../views/KulinerView.vue'
import KulinerDetailView from '../views/KulinerDetailView.vue'
import OlehOlehView from '../views/OlehOlehView.vue'
import OlehOlehDetailView from '../views/OlehOlehDetailView.vue'
import InfografiView from '../views/InfografiView.vue'
import CadasBesemahView from '../views/CadasBesemahView.vue'
import PengaduanView from '../views/PengaduanView.vue'
import TentangKamiView from '../views/TentangKamiView.vue'

const routes = [
  { path: '/', name: 'welcome', component: WelcomeView },
  { path: '/akomodasi', name: 'akomodasi', component: AkomodasiView },
  { path: '/akomodasi/:id', name: 'akomodasi-detail', component: AkomodasiDetailView },
  { path: '/wisata', name: 'wisata', component: WisataView },
  { path: '/wisata/:id', name: 'wisata-detail', component: WisataDetailView },
  { path: '/kuliner', name: 'kuliner', component: KulinerView },
  { path: '/kuliner/:id', name: 'kuliner-detail', component: KulinerDetailView },
  { path: '/oleholeh', name: 'oleholeh', component: OlehOlehView },
  { path: '/oleholeh/:id', name: 'oleholeh-detail', component: OlehOlehDetailView },
  { path: '/infografis', name: 'infografis', component: InfografiView },
  { path: '/cadas-besemah', name: 'cadas-besemah', component: CadasBesemahView },
  { path: '/pengaduan', name: 'pengaduan', component: PengaduanView },
  { path: '/tentang-kami', name: 'tentang-kami', component: TentangKamiView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
