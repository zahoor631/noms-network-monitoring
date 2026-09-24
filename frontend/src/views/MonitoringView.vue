<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold">Monitoring</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          Network devices ka live monitoring — ping, response time, packet loss
        </p>
      </div>
      <button
        :disabled="pingingAll"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition disabled:opacity-50 flex items-center gap-2"
        @click="handlePingAll"
      >
        <span>🔄</span> {{ pingingAll ? 'Pinging...' : 'Ping All' }}
      </button>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="md:col-span-2">
          <label class="block text-xs font-medium text-gray-500 mb-1">Select Device</label>
          <select
            v-model="selectedDeviceId"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="loadMetrics"
          >
            <option :value="null">-- Choose a device --</option>
            <option v-for="d in devices" :key="d.id" :value="d.id">
              {{ d.hostname }} ({{ d.ip_address }}) — {{ d.status }}
            </option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            :disabled="!selectedDeviceId || pingingNow"
            class="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition disabled:opacity-50"
            @click="handlePingNow"
          >
            {{ pingingNow ? '⏳ Pinging...' : '⚡ Ping Now' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="selectedDevice" class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-3">Device Info</h3>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-500">Hostname</span>
            <span class="font-medium">{{ selectedDevice.hostname }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">IP Address</span>
            <span class="font-mono text-xs">{{ selectedDevice.ip_address }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Type</span>
            <span>{{ selectedDevice.device_type }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Status</span>
            <StatusBadge :status="selectedDevice.status" />
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Location</span>
            <span>{{ selectedDevice.location || '—' }}</span>
          </div>
        </div>
      </div>

      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-3">Response Time (last 50 pings)</h3>
        <div v-if="metrics.length" style="height: 200px;">
          <Line :data="chartData" :options="chartOptions" />
        </div>
        <div v-else class="text-center py-12 text-gray-400 text-sm">
          <p class="text-3xl mb-2">📊</p>
          <p>No metrics yet — "Ping Now" click karo</p>
        </div>
      </div>
    </div>

    <div v-if="selectedDevice" class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-semibold text-gray-800">Metrics History</h3>
        <button class="text-xs text-blue-600 hover:underline" @click="loadMetrics">
          🔄 Refresh
        </button>
      </div>

      <div v-if="!metrics.length" class="text-center py-8 text-gray-400 text-sm">
        No metrics recorded
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
            <tr>
              <th class="text-left px-4 py-2 font-medium">Time</th>
              <th class="text-left px-4 py-2 font-medium">Response Time</th>
              <th class="text-left px-4 py-2 font-medium">Packet Loss</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="m in metrics"
              :key="m.id"
              class="border-t border-gray-100 hover:bg-gray-50"
            >
              <td class="px-4 py-2 text-gray-600">{{ formatDate(m.recorded_at) }}</td>
              <td class="px-4 py-2">
                <span v-if="m.response_time_ms" class="font-mono text-green-700 font-medium">
                  {{ m.response_time_ms }} ms
                </span>
                <span v-else class="text-red-500 font-medium">— offline</span>
              </td>
              <td class="px-4 py-2">
                <span :class="m.packet_loss >= 100 ? 'text-red-600' : 'text-green-700'">
                  {{ m.packet_loss }}%
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div
      v-if="!selectedDevice"
      class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center"
    >
      <p class="text-5xl mb-3">📡</p>
      <p class="font-medium text-gray-700">Select a device to begin monitoring</p>
      <p class="text-sm text-gray-500 mt-1">Upar dropdown se device choose karo</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Tooltip, Legend, Filler,
} from 'chart.js'
import { devicesApi } from '@/api/devices'
import { monitoringApi } from '@/api/monitoring'
import { useToast } from '@/composables/useToast'
import { formatDate } from '@/utils/formatters'
import StatusBadge from '@/components/common/StatusBadge.vue'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler)

const toast = useToast()
const devices = ref([])
const selectedDeviceId = ref(null)
const metrics = ref([])
const pingingAll = ref(false)
const pingingNow = ref(false)

const selectedDevice = computed(() =>
  devices.value.find((d) => d.id === selectedDeviceId.value)
)

const chartData = computed(() => ({
  labels: [...metrics.value].reverse().map((m) => new Date(m.recorded_at).toLocaleTimeString()),
  datasets: [{
    label: 'Response (ms)',
    data: [...metrics.value].reverse().map((m) => m.response_time_ms || 0),
    borderColor: '#10b981',
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    fill: true,
    tension: 0.3,
  }],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: true, grid: { color: '#f3f4f6' } },
    x: { grid: { display: false } },
  },
}

onMounted(async () => {
  await loadDevices()
})

async function loadDevices() {
  try {
    const { data } = await devicesApi.list({})
    devices.value = data
  } catch (e) {
    toast.error('Failed to load devices')
  }
}

async function loadMetrics() {
  if (!selectedDeviceId.value) {
    metrics.value = []
    return
  }
  try {
    const { data } = await monitoringApi.metrics(selectedDeviceId.value, 50)
    metrics.value = data
  } catch (e) {
    toast.error('Failed to load metrics')
  }
}

async function handlePingNow() {
  if (!selectedDeviceId.value) return
  pingingNow.value = true
  try {
    const { data } = await monitoringApi.pingNow(selectedDeviceId.value)
    if (data.response_time_ms) {
      toast.success(`Online — ${data.response_time_ms} ms`)
    } else {
      toast.error('Device is offline')
    }
    await loadMetrics()
    await loadDevices()
  } catch (e) {
    toast.error('Ping failed')
  } finally {
    pingingNow.value = false
  }
}

async function handlePingAll() {
  pingingAll.value = true
  try {
    const { data } = await monitoringApi.pingAll()
    toast.success(`Pinged ${data.monitored} devices`)
    await loadDevices()
    if (selectedDeviceId.value) await loadMetrics()
  } catch (e) {
    toast.error('Ping all failed')
  } finally {
    pingingAll.value = false
  }
}
</script>