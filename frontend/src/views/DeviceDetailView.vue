<template>
  <div>
    <!-- Header -->
    <div class="flex items-center gap-3 mb-5">
      <router-link to="/devices" class="text-gray-500 hover:text-gray-700 text-xl">
        ←
      </router-link>
      <div class="flex-1">
        <h1 class="text-2xl font-bold flex items-center gap-3">
          {{ device?.hostname || 'Device Detail' }}
          <StatusBadge v-if="device" :status="device.status" />
        </h1>
        <p class="text-sm text-gray-500 mt-0.5">
          {{ device?.device_type }} · {{ device?.ip_address }}
        </p>
      </div>
      <div v-if="auth.canEdit" class="flex items-center gap-2">
        <button
          class="bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2"
          :disabled="pinging"
          @click="pingNow"
        >
          <span>⚡</span> {{ pinging ? 'Pinging...' : 'Ping Now' }}
        </button>
        <button
          class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm font-medium transition"
          @click="openEdit"
        >
          ✏️ Edit
        </button>
        <button
          class="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg text-sm font-medium transition"
          @click="confirmDelete"
        >
          🗑️ Delete
        </button>
      </div>
    </div>

    <Loader v-if="loading" />

    <div v-else-if="!device" class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
      <p class="text-5xl mb-3">🖥️</p>
      <p class="font-medium text-gray-700">Device not found</p>
      <router-link to="/devices" class="inline-block mt-4 text-blue-600 hover:underline">
        ← Back to Devices
      </router-link>
    </div>

    <div v-else class="space-y-5">
      <!-- Row 1: Info + Uptime + Chart -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-5">
        <!-- Device Info -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h3 class="font-semibold text-gray-800 mb-4">📋 Device Info</h3>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-500">Hostname</span>
              <span class="font-medium">{{ device.hostname }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">IP Address</span>
              <span class="font-mono text-xs">{{ device.ip_address }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">MAC</span>
              <span class="font-mono text-xs">{{ device.mac_address || '—' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Type</span>
              <span class="capitalize">{{ device.device_type }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Location</span>
              <span>{{ device.location || '—' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Created</span>
              <span class="text-xs">{{ formatDate(device.created_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Uptime Stats -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h3 class="font-semibold text-gray-800 mb-4">📊 Uptime</h3>
          <div class="space-y-4">
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-500">Last 24h</span>
                <span class="font-bold" :class="uptimeColor(uptime24)">{{ uptime24 }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="h-full rounded-full transition"
                  :class="uptimeBar(uptime24)"
                  :style="{ width: uptime24 + '%' }"
                ></div>
              </div>
            </div>
            <div class="pt-3 border-t border-gray-100 space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Total Pings</span>
                <span class="font-medium">{{ metrics.length }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Online</span>
                <span class="font-medium text-green-600">{{ onlineCount }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Offline</span>
                <span class="font-medium text-red-600">{{ metrics.length - onlineCount }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Avg Response</span>
                <span class="font-medium">{{ avgResponse }} ms</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Response Chart -->
        <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h3 class="font-semibold text-gray-800 mb-4">📈 Response Time (last 50 pings)</h3>
          <div v-if="metrics.length" style="height: 200px;">
            <Line :data="chartData" :options="chartOptions" />
          </div>
          <div v-else class="text-center py-12 text-gray-400 text-sm">
            <p class="text-3xl mb-2">📊</p>
            <p>No metrics yet — "⚡ Ping Now" click karo</p>
          </div>
        </div>
      </div>

      <!-- Row 2: Alerts + Tickets -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <!-- Recent Alerts -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-800">🔔 Recent Alerts</h3>
            <router-link to="/alerts" class="text-xs text-blue-600 hover:underline">
              View all →
            </router-link>
          </div>
          <div v-if="!deviceAlerts.length" class="text-center py-6 text-gray-400 text-sm">
            <p class="text-2xl mb-1">🔔</p>
            <p>No alerts for this device</p>
          </div>
          <ul v-else class="space-y-2">
            <li
              v-for="a in deviceAlerts.slice(0, 5)"
              :key="a.id"
              class="flex items-start gap-3 p-2 rounded hover:bg-gray-50"
            >
              <span class="text-lg">{{ severityIcon(a.severity) }}</span>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-800 truncate">{{ a.title }}</p>
                <p class="text-xs text-gray-500">{{ timeAgo(a.created_at) }}</p>
              </div>
              <span :class="severityBadge(a.severity)" class="text-xs px-2 py-0.5 rounded font-medium">
                {{ a.severity }}
              </span>
            </li>
          </ul>
        </div>

        <!-- Recent Tickets -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-800">🎫 Recent Tickets</h3>
            <router-link to="/tickets" class="text-xs text-blue-600 hover:underline">
              View all →
            </router-link>
          </div>
          <div v-if="!deviceTickets.length" class="text-center py-6 text-gray-400 text-sm">
            <p class="text-2xl mb-1">🎫</p>
            <p>No tickets for this device</p>
          </div>
          <ul v-else class="space-y-2">
            <li
              v-for="t in deviceTickets.slice(0, 5)"
              :key="t.id"
              class="flex items-start gap-3 p-2 rounded hover:bg-gray-50"
            >
              <span class="text-lg">🎫</span>
              <div class="flex-1 min-w-0">
                <router-link
                  :to="`/tickets/${t.id}`"
                  class="text-sm font-medium text-gray-800 hover:text-blue-600 truncate block"
                >
                  #{{ t.id }} {{ t.title }}
                </router-link>
                <p class="text-xs text-gray-500">{{ timeAgo(t.created_at) }}</p>
              </div>
              <span :class="statusBadge(t.status)" class="text-xs px-2 py-0.5 rounded font-medium">
                {{ t.status.replace('_', ' ') }}
              </span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Metrics History Table -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">📊 Metrics History</h3>
          <button class="text-xs text-blue-600 hover:underline" @click="loadMetrics">
            🔄 Refresh
          </button>
        </div>

        <div v-if="!metrics.length" class="text-center py-8 text-gray-400 text-sm">
          No metrics recorded — "⚡ Ping Now" click karo
        </div>

        <div v-else class="overflow-x-auto max-h-96">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-600 uppercase text-xs sticky top-0">
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
                <td class="px-4 py-2 text-gray-600 text-xs">
                  {{ formatDate(m.recorded_at) }}
                </td>
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
    </div>

    <!-- Edit Modal -->
    <BaseModal v-model="showEdit" title="Edit Device">
      <DeviceForm
        ref="formRef"
        :initial="device"
        submit-label="Update"
        @submit="handleEdit"
        @cancel="showEdit = false"
      />
    </BaseModal>

    <!-- Delete Confirm -->
    <ConfirmDialog
      v-model="showDelete"
      title="Delete Device"
      :message="`Kya aap '${device?.hostname}' ko delete karna chahte ho?`"
      @confirm="handleDelete"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Tooltip, Legend, Filler,
} from 'chart.js'
import { devicesApi } from '@/api/devices'
import { monitoringApi } from '@/api/monitoring'
import { alertsApi } from '@/api/alerts'
import { ticketsApi } from '@/api/tickets'
import { useAuthStore } from '@/store/auth'
import { useToast } from '@/composables/useToast'
import { timeAgo } from '@/composables/useTimeAgo'
import { formatDate } from '@/utils/formatters'
import Loader from '@/components/common/Loader.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import DeviceForm from '@/components/devices/DeviceForm.vue'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler)

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const device = ref(null)
const metrics = ref([])
const alerts = ref([])
const tickets = ref([])
const loading = ref(true)
const pinging = ref(false)
const showEdit = ref(false)
const showDelete = ref(false)
const formRef = ref(null)

const onlineCount = computed(() =>
  metrics.value.filter((m) => m.response_time_ms !== null).length
)

const uptime24 = computed(() => {
  if (!metrics.value.length) return 0
  return Math.round((onlineCount.value / metrics.value.length) * 100)
})

const avgResponse = computed(() => {
  const vals = metrics.value.filter((m) => m.response_time_ms).map((m) => m.response_time_ms)
  if (!vals.length) return 0
  return Math.round(vals.reduce((a, b) => a + b, 0) / vals.length)
})

const deviceAlerts = computed(() =>
  alerts.value.filter((a) => a.device_id === parseInt(route.params.id))
)

const deviceTickets = computed(() =>
  tickets.value.filter((t) => t.device_id === parseInt(route.params.id))
)

const chartData = computed(() => ({
  labels: [...metrics.value].reverse().map((m) =>
    new Date(m.recorded_at).toLocaleTimeString()
  ),
  datasets: [
    {
      label: 'Response (ms)',
      data: [...metrics.value].reverse().map((m) => m.response_time_ms || 0),
      borderColor: '#10b981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      fill: true,
      tension: 0.3,
      pointRadius: 3,
    },
  ],
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

function uptimeColor(pct) {
  if (pct >= 95) return 'text-green-600'
  if (pct >= 70) return 'text-orange-600'
  return 'text-red-600'
}

function uptimeBar(pct) {
  if (pct >= 95) return 'bg-green-500'
  if (pct >= 70) return 'bg-orange-500'
  return 'bg-red-500'
}

function severityIcon(s) {
  return { info: 'ℹ️', warning: '⚠️', critical: '🔴' }[s] || 'ℹ️'
}

function severityBadge(s) {
  return {
    info: 'bg-blue-100 text-blue-700',
    warning: 'bg-orange-100 text-orange-700',
    critical: 'bg-red-100 text-red-700',
  }[s] || 'bg-gray-100 text-gray-700'
}

function statusBadge(s) {
  return {
    open: 'bg-orange-100 text-orange-700',
    in_progress: 'bg-blue-100 text-blue-700',
    resolved: 'bg-green-100 text-green-700',
    closed: 'bg-gray-100 text-gray-700',
  }[s] || 'bg-gray-100 text-gray-700'
}

onMounted(loadAll)
watch(() => route.params.id, loadAll)

async function loadAll() {
  loading.value = true
  try {
    const [devRes, metRes, altRes, ticRes] = await Promise.all([
      devicesApi.get(route.params.id),
      monitoringApi.metrics(route.params.id, 50),
      alertsApi.list({}),
      ticketsApi.list({}),
    ])
    device.value = devRes.data
    metrics.value = metRes.data
    alerts.value = altRes.data
    tickets.value = ticRes.data
  } catch (e) {
    toast.error('Failed to load device')
    device.value = null
  } finally {
    loading.value = false
  }
}

async function loadMetrics() {
  try {
    const { data } = await monitoringApi.metrics(route.params.id, 50)
    metrics.value = data
  } catch (e) {
    toast.error('Failed to load metrics')
  }
}

async function pingNow() {
  pinging.value = true
  try {
    const { data } = await monitoringApi.pingNow(device.value.id)
    if (data.response_time_ms) {
      toast.success(`Online — ${data.response_time_ms} ms`)
    } else {
      toast.error('Device is offline')
    }
    await Promise.all([loadMetrics(), loadAll()])
  } catch (e) {
    toast.error('Ping failed')
  } finally {
    pinging.value = false
  }
}

function openEdit() {
  showEdit.value = true
}

async function handleEdit(payload) {
  try {
    await devicesApi.update(device.value.id, payload)
    toast.success('Device updated')
    showEdit.value = false
    await loadAll()
  } catch (e) {
    formRef.value?.setError(e.response?.data?.detail || 'Update failed')
  }
}

function confirmDelete() {
  showDelete.value = true
}

async function handleDelete() {
  try {
    await devicesApi.remove(device.value.id)
    toast.success('Device deleted')
    router.push('/devices')
  } catch (e) {
    toast.error('Delete failed')
  } finally {
    showDelete.value = false
  }
}
</script>