<template>
  <div class="welcome-page">
    <!-- Logo Section -->
    <div class="welcome-header">
      <div class="logo-wrap">
        <div class="logo-icon">
          <img src="../assets/logo.png" alt="Logo D'Paris Egsotis" />
        </div>
        <div class="logo-text">
          <div class="logo-main">D'PARIS 2.0</div>
          <div class="logo-sub">EGSOTIS</div>
          <div class="logo-tagline">Direktori Statistik Pariwisata</div>
          <div class="logo-tagline">GPS & Infografis</div>
        </div>
      </div>
      <br>
      <div class="welcome-title">SELAMAT DATANG</div>
      <div class="welcome-title-sub"><em>Mau cari apa di Kota Pagar Alam?</em></div>
    </div>

    <!-- Menu Grid -->
    <div class="menu-grid-wrap">
      <div class="menu-grid">
        <div
          v-for="menu in menus"
          :key="menu.name"
          class="menu-btn"
          @click="navigate(menu.route)"
        >
          <div class="menu-icon" v-html="menu.icon"></div>
          <div class="menu-label">{{ menu.name }}</div>
        </div>
      </div>
    </div>
    <br>
    <AppFooter />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import AppFooter from '../components/AppFooter.vue'

const router = useRouter()
const navigate = (route) => router.push(route)

const menus = [
  {
    name: 'AKOMODASI',
    route: '/akomodasi',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 13c1.66 0 3-1.34 3-3S8.66 7 7 7s-3 1.34-3 3 1.34 3 3 3zm12-6h-8v7H3V5H1v15h2v-3h18v3h2v-9c0-2.21-1.79-4-4-4z"/></svg>`
  },
  {
    name: 'WISATA',
    route: '/wisata',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 6l-1-2H5v17h2v-7h5l1 2h7V6h-6zm4 8h-4l-1-2H7V6h5l1 2h5v6z"/></svg>`
  },
  {
    name: 'KULINER',
    route: '/kuliner',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M11 9H9V2H7v7H5V2H3v7c0 2.12 1.66 3.84 3.75 3.97V22h2.5v-9.03C11.34 12.84 13 11.12 13 9V2h-2v7zm5-3v8h2.5v8H21V2c-2.76 0-5 2.24-5 4z"/></svg>`
  },
  {
    name: 'OLEH-OLEH',
    route: '/oleholeh',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 6h-2c0-2.76-2.24-5-5-5S7 3.24 7 6H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-7-3c1.66 0 3 1.34 3 3H9c0-1.66 1.34-3 3-3zm0 10c-1.66 0-3-1.34-3-3h2c0 .55.45 1 1 1s1-.45 1-1h2c0 1.66-1.34 3-3 3z"/></svg>`
  },
    {
    name: 'TRANSPORTASI',
    route: '/transportasi',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 16c0 .88.39 1.67 1 2.22v1.28c0 .83.67 1.5 1.5 1.5S8 20.33 8 19.5V19h8v.5c0 .82.67 1.5 1.5 1.5.82 0 1.5-.67 1.5-1.5v-1.28c.61-.55 1-1.34 1-2.22V6c0-3.5-3.58-4-8-4s-8 .5-8 4v10zm3.5 1c-.83 0-1.5-.67-1.5-1.5S6.67 14 7.5 14s1.5.67 1.5 1.5S8.33 17 7.5 17zm9 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm1.5-6H6V6h12v5z"/></svg>`
  },
  {
    name: 'INFOGRAFIS',
    route: '/infografis',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>`
  },
  {
    name: 'DASHBOARD',
    route: '/dashboard',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>`
  },
  {
    name: 'CADAS BESEMAH',
    route: '/cadas-besemah',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/></svg>`
  },
  {
    name: 'PENGADUAN',
    route: '/pengaduan',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>`
  },
  {
    name: 'TENTANG KAMI',
    route: '/tentang-kami',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>`
  }
]
</script>

<style scoped>
.welcome-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #fff;
}

.welcome-header {
  background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), url('../assets/Pagaralam.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 30px 24px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.logo-wrap {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #e0f7f7, #b2eeee);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(46,196,196,0.3);
}

.logo-icon img {
  width: 100%;
  height: 100%;
  border-radius: 20px;
  object-fit: cover;
}

.logo-main {
  font-size: 1.7rem;
  font-weight: 800;
  color: #1a3a5c;
  line-height: 1;
}

.logo-sub {
  font-size: 1rem;
  font-weight: 700;
  color: #2EC4C4;
  letter-spacing: 0.12em;
}

.logo-tagline {
  font-size: 0.68rem;
  color: #888;
  font-weight: 500;
  line-height: 1.4;
}

.welcome-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1a3a5c;
  letter-spacing: 0.18em;
  margin-top: 2px;
}

.welcome-title-sub {
  font-size: 0.825rem;
  font-weight: 500;
  color: #1a3a5c;
  letter-spacing: 0.05em;
  margin-top: 1px;
}

.menu-grid-wrap {
  background: #2EC4C4;
  border-radius: 0;
  flex: 1;
  padding: 28px 20px 40px;
}

.menu-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.menu-btn {
  background: #fff;
  border-radius: 16px;
  padding: 22px 12px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
  box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.menu-btn:hover, .menu-btn:active {
  transform: translateY(-4px) scale(1.03);
  box-shadow: 0 8px 22px rgba(0,0,0,0.14);
}

.menu-icon {
  width: 48px;
  height: 48px;
  color: #2EC4C4;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.menu-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #2EC4C4;
  text-align: center;
  letter-spacing: 0.06em;
  line-height: 1.3;
}
</style>
