<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
          <tr>
            <th class="text-left px-4 py-3 font-medium">Hostname</th>
            <th class="text-left px-4 py-3 font-medium">Type</th>
            <th class="text-left px-4 py-3 font-medium">IP Address</th>
            <th class="text-left px-4 py-3 font-medium">MAC</th>
            <th class="text-left px-4 py-3 font-medium">Location</th>
            <th class="text-left px-4 py-3 font-medium">Status</th>
            <th class="text-right px-4 py-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody>
          <!-- Empty state -->
          <tr v-if="!devices.length">
            <td colspan="7" class="text-center py-12">
              <div class="text-gray-400">
                <p class="text-4xl mb-2">📭</p>
                <p class="font-medium">No devices found</p>
                <p class="text-xs mt-1">
                  {{ hasFilters ? 'Filters clear karo ya naya device add karo' : '"Add Device" button se shuru karo' }}
                </p>
              </div>
            </td>
          </tr>

          <!-- Device rows -->
          <tr
            v-for="device in devices"
            :key="device.id"
            class="border-t border-gray-100 hover:bg-gray-50 transition"
          >
            <td class="px-4 py-3">
              <router-link
                :to="`/devices/${device.id}`"
                class="font-medium text-gray-800 hover:text-blue-600"
              >
                {{ device.hostname }}
              </router-link>
            </td>
            <td class="px-4 py-3">
              <span class="inline-flex items-center gap-1.5">
                <span>{{ getDeviceTypeIcon(device.device_type) }}</span>
                <span class="text-gray-700">{{ getDeviceTypeLabel(device.device_type) }}</span>
              </span>
            </td>
            <td class="px-4 py-3 font-mono text-xs text-gray-700">
              {{ device.ip_address }}
            </td>
            <td class="px-4 py-3 font-mono text-xs text-gray-500">
              {{ device.mac_address || '—' }}
            </td>
            <td class="px-4 py-3 text-gray-600">
              {{ device.location || '—' }}
            </td>
            <td class="px-4 py-3">
              <StatusBadge :status="device.status" />
            </td>
            <td class="px-4 py-3 text-right">
              <button
                class="text-blue-600 hover:text-blue-800 text-xs font-medium mr-3"
                @click="$emit('edit', device)"
              >
                ✏️ Edit
              </button>
              <button
                class="text-red-600 hover:text-red-800 text-xs font-medium"
                @click="$emit('delete', device)"
              >
                🗑️ Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import StatusBadge from '@/components/common/StatusBadge.vue'
import { getDeviceTypeIcon, getDeviceTypeLabel } from '@/utils/constants'

defineProps({
  devices: { type: Array, default: () => [] },
  hasFilters: Boolean,
})

defineEmits(['edit', 'delete'])
</script>