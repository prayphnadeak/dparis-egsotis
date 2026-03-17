<template>
  <header class="app-header">
    <div class="header-icon" @click="goHome" title="Beranda">
      <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
      </svg>
    </div>
    <h1 class="header-title">{{ title }}</h1>
    <div class="header-icon" @click="showSurveyPopup = true" title="Keluar">
      <img src="../assets/exit.png" alt="Exit" class="exit-img" />
    </div>
  </header>

  <!-- Survey Popup Modal -->
  <div class="survey-modal-overlay" v-if="showSurveyPopup">
    <div class="survey-modal">
      <div class="survey-modal-content">
        <p>
          Terima Kasih telah menggunakan D'Paris Egsotis! Namun, sebelum Anda beranjak pergi, mohon kiranya untuk mengisi survei berikut ini untuk peningkatan pelayanan publik kami ke depannya
        </p>
        <div class="survey-modal-actions">
          <button class="btn-cancel" @click="showSurveyPopup = false">Batal</button>
          <a href="https://skd.bps.go.id/skd/s/1673" class="btn-survey">Isi Survei</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

defineProps({
  title: {
    type: String,
    required: true
  }
})

const router = useRouter()
const goHome = () => router.push('/')
const showSurveyPopup = ref(false)
</script>

<style scoped>
.exit-img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

/* Survey Popup Modal */
.survey-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}
.survey-modal {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  max-width: 340px;
  width: 100%;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  text-align: center;
  animation: modalPop 0.3s ease-out;
}
@keyframes modalPop {
  0% { transform: scale(0.9); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.survey-modal-content p {
  color: #1a3a5c;
  line-height: 1.6;
  font-size: 0.95rem;
  margin-bottom: 24px;
  font-weight: 500;
}
.survey-modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}
.btn-cancel, .btn-survey {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s ease;
  text-decoration: none;
  display: inline-block;
}
.btn-cancel {
  background: #f1f5f9;
  color: #64748b;
}
.btn-survey {
  background: #2EC4C4;
  color: #fff;
}
.btn-cancel:hover, .btn-survey:hover {
  opacity: 0.9;
}
</style>
