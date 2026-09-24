<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[100] flex flex-col gap-2">
      <TransitionGroup name="toast">
        <div
          v-for="t in toasts"
          :key="t.id"
          :class="toastClass(t.type)"
          class="min-w-[280px] max-w-sm px-4 py-3 rounded-lg shadow-lg flex items-start gap-2"
        >
          <span class="text-lg">{{ icon(t.type) }}</span>
          <p class="text-sm flex-1">{{ t.message }}</p>
          <button class="text-white/80 hover:text-white" @click="remove(t.id)">✕</button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from '@/composables/useToast'

const { toasts } = useToast()

function toastClass(type) {
  return {
    success: 'bg-green-600 text-white',
    error: 'bg-red-600 text-white',
    info: 'bg-blue-600 text-white',
  }[type] || 'bg-gray-800 text-white'
}

function icon(type) {
  return { success: '✅', error: '❌', info: 'ℹ️' }[type] || 'ℹ️'
}

function remove(id) {
  const idx = toasts.value.findIndex((t) => t.id === id)
  if (idx !== -1) toasts.value.splice(idx, 1)
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>