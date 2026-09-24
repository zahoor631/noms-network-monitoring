<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
    <h3 class="font-semibold text-gray-800 mb-4">🧮 Subnet Calculator</h3>

    <div class="space-y-3 mb-4">
      <div>
        <label class="block text-xs font-medium text-gray-500 mb-1">IP Address</label>
        <input
          v-model="ip"
          type="text"
          placeholder="192.168.1.10"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-500 mb-1">CIDR</label>
        <select
          v-model.number="cidr"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option v-for="c in cidrOptions" :key="c" :value="c">/{{ c }}</option>
        </select>
      </div>

      <button
        :disabled="loading"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition disabled:opacity-50"
        @click="calculate"
      >
        {{ loading ? 'Calculating...' : 'Calculate' }}
      </button>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-xs p-2 rounded mb-3">
      {{ error }}
    </div>

    <div v-if="result" class="space-y-2 text-sm border-t border-gray-100 pt-4">
      <div class="flex justify-between">
        <span class="text-gray-500">Network</span>
        <span class="font-mono font-medium text-gray-800">{{ result.network }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">Broadcast</span>
        <span class="font-mono text-gray-700">{{ result.broadcast }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">Netmask</span>
        <span class="font-mono text-gray-700">{{ result.netmask }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">First Host</span>
        <span class="font-mono text-gray-700">{{ result.first_host }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">Last Host</span>
        <span class="font-mono text-gray-700">{{ result.last_host }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">Total Hosts</span>
        <span class="font-medium text-gray-800">{{ result.total_hosts }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">Usable Hosts</span>
        <span class="font-bold text-green-600">{{ result.usable_hosts }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ipamApi } from '@/api/ipam'

const ip = ref('192.168.1.10')
const cidr = ref(24)
const result = ref(null)
const error = ref('')
const loading = ref(false)

const cidrOptions = [8, 16, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30]

async function calculate() {
  error.value = ''
  result.value = null
  loading.value = true
  try {
    const { data } = await ipamApi.calculate(ip.value, cidr.value)
    result.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Calculation failed'
  } finally {
    loading.value = false
  }
}
</script>