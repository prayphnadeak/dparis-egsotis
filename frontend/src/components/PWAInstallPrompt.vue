<template>
  <transition name="slide-up">
    <div v-if="showPrompt" class="install-prompt-overlay">
      <div class="install-prompt-card">
        <div class="header">
          <img src="/icon-192.png" alt="Logo" class="app-logo" />
          <div class="info">
            <div class="title">Pasang D'Paris Egsotis</div>
            <div class="subtitle">Akses cepat dari layar utama Anda</div>
          </div>
          <button class="close-btn" @click="closePrompt">✕</button>
        </div>
        
        <div class="body">
          <!-- If in iframe (Hugging Face) -->
          <p v-if="isInIframe">
            Anda sedang membuka aplikasi di dalam tampilan Website. <br/>
            <b>Klik tombol di bawah</b> untuk membuka versi penuh agar bisa diinstal ke HP.
          </p>
          <p v-else-if="isIOS">
            Ketuk ikon <b>Bagikan</b> di navigasi bawah browser, lalu pilih <b>"Tambah ke Layar Utama"</b>.
          </p>
          <p v-else>
            Instal aplikasi ini untuk pengalaman yang lebih baik dan akses tanpa internet.
          </p>
        </div>

        <div class="footer">
          <button v-if="isInIframe" class="install-btn" @click="openDirectUrl">Buka Mode Penuh</button>
          <button v-else-if="deferredPrompt" class="install-btn" @click="installApp">Instal Sekarang</button>
          <button v-else-if="isIOS" class="install-btn" @click="closePrompt">Saya Mengerti</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const showPrompt = ref(false)
const deferredPrompt = ref(null)
const isIOS = ref(false)
const isInIframe = ref(false)

onMounted(() => {
  // Check if already in standalone mode
  if (window.matchMedia('(display-mode: standalone)').matches) {
    return
  }

  // Detect iframe context (Hugging Face)
  try {
    isInIframe.value = window.self !== window.top
  } catch (e) {
    isInIframe.value = true
  }

  // Detect iOS
  const userAgent = window.navigator.userAgent.toLowerCase()
  isIOS.value = /iphone|ipad|ipod/.test(userAgent)

  if (isInIframe.value) {
    // Automatically show prompt in Hugging Face to guide user out of the iframe
    setTimeout(() => {
      showPrompt.value = true
    }, 2000)
    return
  }

  // Android/Chrome event (only works on direct domain, not in iframe)
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt.value = e
    showPrompt.value = true
  })

  // iOS logic: show prompt after a short delay if not installed
  if (isIOS.value) {
    const hasSeenPrompt = localStorage.getItem('pwa_prompt_seen')
    if (!hasSeenPrompt) {
      setTimeout(() => {
        showPrompt.value = true
      }, 3000)
    }
  }
})

const openDirectUrl = () => {
  // Hugging Face direct space URL extraction
  // Pattern: huggingface.co/spaces/USER/SPACE
  const match = window.location.href.match(/huggingface\.co\/spaces\/([^/?#]+)\/([^/?#]+)/)
  
  if (match) {
    const user = match[1]
    const space = match[2]
    // Hugging Face direct URLs use hyphens instead of underscores or slashes
    // and the format is user-space.hf.space
    const directDomain = `${user}-${space}`.replace(/[\/_]/g, '-')
    window.open(`https://${directDomain}.hf.space`, '_blank')
  } else {
    // Fallback to known direct URL if extraction fails
    window.open('https://prayphnadeak-dparis-egsotis.hf.space', '_blank')
  }
  showPrompt.value = false
}

const installApp = async () => {
  try {
    await fetch('/api/v1/statistics/download', { method: 'POST' })
  } catch (e) {
    console.error('Download track failed', e)
  }

  if (!deferredPrompt.value) return
  
  deferredPrompt.value.prompt()
  const { outcome } = await deferredPrompt.value.userChoice
  
  if (outcome === 'accepted') {
    deferredPrompt.value = null
    showPrompt.value = false
  }
}

const closePrompt = () => {
  showPrompt.value = false
  if (isIOS.value) {
    localStorage.setItem('pwa_prompt_seen', 'true')
  }
}
</script>

<style scoped>
.install-prompt-overlay {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 16px;
  display: flex;
  justify-content: center;
  pointer-events: none;
}

.install-prompt-card {
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  padding: 16px;
  pointer-events: auto;
  border: 1px solid rgba(46, 196, 196, 0.2);
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.app-logo {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  object-fit: contain;
  background: #f0fafa;
  padding: 4px;
}

.info {
  flex: 1;
}

.title {
  font-weight: 800;
  font-size: 1rem;
  color: #1a3a5c;
}

.subtitle {
  font-size: 0.75rem;
  color: #666;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #999;
  cursor: pointer;
  padding: 4px;
}

.body {
  font-size: 0.85rem;
  color: #444;
  line-height: 1.4;
  margin-bottom: 16px;
}

.footer {
  display: flex;
  justify-content: flex-end;
}

.install-btn {
  background: #2EC4C4;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: transform 0.1s;
}

.install-btn:active {
  transform: scale(0.95);
}

/* Animations */
.slide-up-enter-active, .slide-up-leave-active {
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
}

.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
