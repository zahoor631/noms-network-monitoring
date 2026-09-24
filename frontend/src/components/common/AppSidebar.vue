<template>
  <aside class="w-64 bg-gray-900 text-white flex flex-col">
    <div class="p-4 border-b border-gray-700">
      <h1 class="text-xl font-bold">NOMS</h1>
      <p class="text-xs text-gray-400 mt-1">Network Monitoring</p>
    </div>

    <nav class="flex-1 overflow-y-auto py-4">
      <router-link
        v-for="item in menu"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 px-4 py-2.5 hover:bg-gray-800 transition"
        :class="{ 'bg-blue-600 hover:bg-blue-700': isActive(item.to) }"
      >
        <span class="text-lg">{{ item.icon }}</span>
        <span class="text-sm">{{ item.label }}</span>
      </router-link>
    </nav>

    <div class="p-4 border-t border-gray-700 text-xs text-gray-400">
      v0.1.0
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const auth = useAuthStore()

const menu = computed(() => {
  const items = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/devices', label: 'Devices', icon: '🖥️' },
  { to: '/monitoring', label: 'Monitoring', icon: '📡' },
  { to: '/ipam', label: 'IPAM', icon: '🌐' },
  { to: '/topology', label: 'Topology', icon: '🗺️' },
  { to: '/organization', label: 'Organization', icon: '🏢' },  // ← YE ADD KARO
  { to: '/alerts', label: 'Alerts', icon: '🔔' },
  { to: '/tickets', label: 'Tickets', icon: '🎫' },
  { to: '/reports', label: 'Reports', icon: '📈' },
]
  if (auth.isAdmin) {
    items.push({ to: '/users', label: 'Users', icon: '👥' })
  }
  items.push({ to: '/settings', label: 'Settings', icon: '⚙️' })
  return items
})

function isActive(path) {
  return path === '/' ? route.path === '/' : route.path.startsWith(path)
}
</script>