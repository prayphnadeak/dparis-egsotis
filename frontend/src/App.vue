<template>
  <div id="outer">
    <div class="page-wrapper">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
    <PWAInstallPrompt />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import PWAInstallPrompt from './components/PWAInstallPrompt.vue'

onMounted(async () => {
  try {
    await fetch('/api/v1/statistics/visit', { method: 'POST' });
  } catch (err) {
    console.error('Visit track failed', err);
  }
})
</script>

<style scoped>
#outer {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  background: #e8f5f5;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.22s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
