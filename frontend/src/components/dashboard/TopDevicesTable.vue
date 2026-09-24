<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
    <h3 class="font-semibold text-gray-800 mb-4">Top Devices</h3>
    <div v-if="!devices.length" class="text-center py-8 text-gray-400 text-sm">
      <p class="text-3xl mb-2">🖥️</p>
      <p>No devices</p>
    </div>
    <table v-else class="w-full text-sm">
      <thead class="text-xs text-gray-500 uppercase">
        <tr>
          <th class="text-left py-2">Hostname</th>
          <th class="text-left py-2">IP</th>
          <th class="text-right py-2">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in devices.slice(0, 5)" :key="d.id" class="border-t border-gray-100">
          <td class="py-2 font-medium text-gray-800">{{ d.hostname }}</td>
          <td class="py-2 font-mono text-xs text-gray-600">{{ d.ip_address }}</td>
          <td class="py-2 text-right"><StatusBadge :status="d.status" /></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import StatusBadge from '@/components/common/StatusBadge.vue'

defineProps({ devices: { type: Array, default: () => [] } })
</script>