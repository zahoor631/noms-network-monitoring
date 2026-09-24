<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
    <h3 class="font-semibold text-gray-800 mb-4">Recent Alerts</h3>
    <div v-if="!alerts.length" class="text-center py-8 text-gray-400 text-sm">
      <p class="text-3xl mb-2">🔔</p>
      <p>No alerts</p>
    </div>
    <ul v-else class="space-y-3">
      <li v-for="a in alerts" :key="a.id" class="flex items-start gap-3 pb-3 border-b border-gray-100 last:border-0">
        <span class="text-lg">{{ severityIcon(a.severity) }}</span>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-800 truncate">{{ a.title }}</p>
          <p class="text-xs text-gray-500 mt-0.5">{{ formatDate(a.created_at) }}</p>
        </div>
        <span :class="severityClass(a.severity)" class="text-xs px-2 py-0.5 rounded font-medium whitespace-nowrap">
          {{ a.severity }}
        </span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { formatDate } from '@/utils/formatters'

defineProps({ alerts: { type: Array, default: () => [] } })

function severityIcon(s) {
  return { info: 'ℹ️', warning: '⚠️', critical: '🔴' }[s] || 'ℹ️'
}
function severityClass(s) {
  return {
    info: 'bg-blue-100 text-blue-700',
    warning: 'bg-orange-100 text-orange-700',
    critical: 'bg-red-100 text-red-700',
  }[s] || 'bg-gray-100 text-gray-700'
}
</script>