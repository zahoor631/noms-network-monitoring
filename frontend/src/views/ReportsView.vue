<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold">Reports</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          Network analytics aur insights — uptime, incidents, performance
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button
          v-for="r in ranges"
          :key="r.value"
          :class="days === r.value ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          class="px-3 py-2 rounded-lg text-sm font-medium transition"
          @click="setRange(r.value)"
        >
          {{ r.label }}
        </button>
        <button
          class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2"
          @click="exportCSV"
        >
          📥 Export CSV
        </button>
      </div>
    </div>

    <!-- Loading -->
    <Loader v-if="loading" />

    <div v-else class="space-y-5">
      <!-- Stats Cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <p class="text-sm text-gray-500">Total Devices</p>
          <p class="text-3xl font-bold text-blue-600 mt-1">{{ stats.total_devices }}</p>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <p class="text-sm text-gray-500">Avg Uptime</p>
          <p class="text-3xl font-bold text-green-600 mt-1">{{ stats.avg_uptime }}%</p>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <p class="text-sm text-gray-500">Incidents</p>
          <p class="text-3xl font-bold text-orange-600 mt-1">{{ stats.total_incidents }}</p>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <p class="text-sm text-gray-500">Resolved</p>
          <p class="text-3xl font-bold text-purple-600 mt-1">{{ stats.resolved }}</p>
        </div>
      </div>

      <!-- Uptime Chart -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">📊 Device Uptime ({{ days }}d)</h3>
          <span class="text-xs text-gray-500">{{ uptime.length }} devices</span>
        </div>
        <div v-if="!uptime.length" class="text-center py-12 text-gray-400 text-sm">
          <p class="text-4xl mb-2">📊</p>
          <p>No uptime data available</p>
        </div>
        <div v-else style="height: 300px;">
          <Bar :data="chartData" :options="chartOptions" />
        </div>
      </div>

      <!-- Uptime Table -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">📋 Device Uptime Report</h3>

        <div v-if="!uptime.length" class="text-center py-8 text-gray-400 text-sm">
          No data
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th class="text-left px-4 py-3 font-medium">Hostname</th>
                <th class="text-left px-4 py-3 font-medium">Uptime %</th>
                <th class="text-left px-4 py-3 font-medium">Samples</th>
                <th class="text-left px-4 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="u in uptime"
                :key="u.device_id"
                class="border-t border-gray-100 hover:bg-gray-50"
              >
                <td class="px-4 py-3 font-medium text-gray-800">{{ u.hostname }}</td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2">
                    <div class="w-24 bg-gray-200 rounded-full h-2 overflow-hidden">
                      <div
                        class="h-full rounded-full transition"
                        :class="uptimeColor(u.uptime_percent)"
                        :style="{ width: u.uptime_percent + '%' }"
                      ></div>
                    </div>
                    <span class="font-mono text-xs font-medium">{{ u.uptime_percent }}%</span>
                  </div>
                </td>
                <td class="px-4 py-3 text-gray-600">{{ u.samples }}</td>
                <td class="px-4 py-3">
                  <span :class="uptimeBadge(u.uptime_percent)" class="px-2 py-0.5 rounded text-xs font-medium">
                    {{ uptimeLabel(u.uptime_percent) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Incident Report -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">🎫 Incident Report (Tickets)</h3>

        <div v-if="!incidents.length" class="text-center py-8 text-gray-400 text-sm">
          <p class="text-4xl mb-2">🎫</p>
          <p>No incidents recorded</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th class="text-left px-4 py-3 font-medium">#</th>
                <th class="text-left px-4 py-3 font-medium">Title</th>
                <th class="text-left px-4 py-3 font-medium">Priority</th>
                <th class="text-left px-4 py-3 font-medium">Status</th>
                <th class="text-left px-4 py-3 font-medium">Created</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="i in incidents"
                :key="i.id"
                class="border-t border-gray-100 hover:bg-gray-50"
              >
                <td class="px-4 py-3 font-mono text-xs text-gray-500">#{{ i.id }}</td>
                <td class="px-4 py-3">
                  <router-link :to="`/tickets/${i.id}`" class="font-medium text-gray-800 hover:text-blue-600">
                    {{ i.title }}
                  </router-link>
                </td>
                <td class="px-4 py-3">
                  <span :class="priorityBadge(i.priority)" class="px-2 py-0.5 rounded text-xs font-medium">
                    {{ i.priority }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <span :class="statusBadge(i.status)" class="px-2 py-0.5 rounded text-xs font-medium">
                    {{ i.status.replace('_', ' ') }}
                  </span>
                </td>
                <td class="px-4 py-3 text-xs text-gray-500">
                  {{ formatDate(i.created_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend,
} from 'chart.js'
import { reportsApi } from '@/api/reports'
import { useToast } from '@/composables/useToast'
import { formatDate } from '@/utils/formatters'
import Loader from '@/components/common/Loader.vue'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

const toast = useToast()

const days = ref(1)
const loading = ref(true)
const uptime = ref([])
const incidents = ref([])

const ranges = [
  { value: 1, label: '1 Day' },
  { value: 7, label: '7 Days' },
  { value: 30, label: '30 Days' },
]

const stats = computed(() => {
  const total = uptime.value.length
  const avg = total ? uptime.value.reduce((s, u) => s + u.uptime_percent, 0) / total : 0
  return {
    total_devices: total,
    avg_uptime: avg.toFixed(1),
    total_incidents: incidents.value.length,
    resolved: incidents.value.filter((i) => i.status === 'resolved' || i.status === 'closed').length,
  }
})

const chartData = computed(() => ({
  labels: uptime.value.map((u) => u.hostname),
  datasets: [
    {
      label: 'Uptime %',
      data: uptime.value.map((u) => u.uptime_percent),
      backgroundColor: uptime.value.map((u) => {
        if (u.uptime_percent >= 95) return '#10b981'
        if (u.uptime_percent >= 70) return '#f59e0b'
        return '#ef4444'
      }),
      borderRadius: 6,
      barThickness: 50,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: true, max: 100, grid: { color: '#f3f4f6' } },
    x: { grid: { display: false } },
  },
}

function uptimeColor(pct) {
  if (pct >= 95) return 'bg-green-500'
  if (pct >= 70) return 'bg-orange-500'
  return 'bg-red-500'
}

function uptimeBadge(pct) {
  if (pct >= 95) return 'bg-green-100 text-green-700'
  if (pct >= 70) return 'bg-orange-100 text-orange-700'
  return 'bg-red-100 text-red-700'
}

function uptimeLabel(pct) {
  if (pct >= 95) return '✓ Healthy'
  if (pct >= 70) return '⚠ Degraded'
  return '✕ Down'
}

function priorityBadge(p) {
  return {
    low: 'bg-green-100 text-green-700',
    medium: 'bg-yellow-100 text-yellow-700',
    high: 'bg-orange-100 text-orange-700',
    critical: 'bg-red-100 text-red-700',
  }[p] || 'bg-gray-100 text-gray-700'
}

function statusBadge(s) {
  return {
    open: 'bg-orange-100 text-orange-700',
    in_progress: 'bg-blue-100 text-blue-700',
    resolved: 'bg-green-100 text-green-700',
    closed: 'bg-gray-100 text-gray-700',
  }[s] || 'bg-gray-100 text-gray-700'
}

onMounted(load)

async function load() {
  loading.value = true
  try {
    const [upRes, incRes] = await Promise.all([
      reportsApi.uptime(days.value),
      reportsApi.incidents(),
    ])
    uptime.value = upRes.data
    incidents.value = incRes.data
  } catch (e) {
    toast.error('Failed to load reports')
  } finally {
    loading.value = false
  }
}

function setRange(d) {
  days.value = d
  load()
}

function exportCSV() {
  if (!uptime.value.length) {
    toast.error('No data to export')
    return
  }
  const headers = ['Hostname', 'Uptime %', 'Samples']
  const rows = uptime.value.map((u) => [u.hostname, u.uptime_percent, u.samples])
  const csv = [headers, ...rows].map((r) => r.join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `noms-uptime-report-${days.value}d-${Date.now()}.csv`
  a.click()
  URL.revokeObjectURL(url)
  toast.success('CSV downloaded')
}
</script>