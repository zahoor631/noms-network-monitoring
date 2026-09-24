<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold">Alerts</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          Network alerts aur notifications — severity ke hisaab se
        </p>
      </div>
      <button
        v-if="auth.canEdit"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2"
        @click="openCreate"
      >
        <span>➕</span> Create Alert
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Total Alerts</p>
        <p class="text-2xl font-bold text-gray-800">{{ alerts.length }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Active</p>
        <p class="text-2xl font-bold text-orange-600">{{ activeCount }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Resolved</p>
        <p class="text-2xl font-bold text-green-600">{{ resolvedCount }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Critical</p>
        <p class="text-2xl font-bold text-red-600">{{ criticalCount }}</p>
      </div>
    </div>

    <!-- Filter -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4 flex flex-wrap items-center gap-3">
      <span class="text-sm text-gray-500 font-medium">Filter:</span>
      <button
        v-for="f in filters"
        :key="f.value"
        :class="severity === f.value ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        class="px-3 py-1.5 rounded-lg text-xs font-medium transition"
        @click="setFilter(f.value)"
      >
        {{ f.label }}
      </button>
      <button
        v-if="severity || resolved !== null"
        class="ml-auto text-xs text-blue-600 hover:underline"
        @click="clearFilters"
      >
        ✕ Clear filters
      </button>
    </div>

    <!-- Loading -->
    <Loader v-if="loading" />

    <!-- Alert list -->
    <div v-else-if="!filteredAlerts.length" class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
      <p class="text-5xl mb-3">🔔</p>
      <p class="font-medium text-gray-700">No alerts found</p>
      <p class="text-sm text-gray-500 mt-1">
        {{ hasFilters ? 'Filters clear karo' : 'Abhi tak koi alert nahi aaya' }}
      </p>
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="a in filteredAlerts"
        :key="a.id"
        class="bg-white rounded-xl shadow-sm border-l-4 border border-gray-200 p-4 flex items-start gap-4 hover:shadow-md transition"
        :class="borderColor(a.severity)"
      >
        <span class="text-2xl">{{ severityIcon(a.severity) }}</span>

        <div class="flex-1 min-w-0">
          <div class="flex items-start justify-between gap-3">
            <div>
              <h3 class="font-semibold text-gray-800">{{ a.title }}</h3>
              <p v-if="a.message" class="text-sm text-gray-600 mt-1">{{ a.message }}</p>
            </div>
            <div class="flex flex-col items-end gap-1 shrink-0">
              <span :class="severityBadge(a.severity)" class="px-2 py-0.5 rounded text-xs font-medium">
                {{ a.severity }}
              </span>
              <span
                v-if="a.is_resolved"
                class="px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-700"
              >
                ✓ resolved
              </span>
            </div>
          </div>

          <div class="flex items-center gap-4 mt-3 text-xs text-gray-500">
            <span>🕐 {{ timeAgo(a.created_at) }}</span>
            <span v-if="a.device_id">📡 Device #{{ a.device_id }}</span>
          </div>

          <div class="flex items-center gap-2 mt-3">
            <button
              v-if="!a.is_resolved && auth.canEdit"
              class="text-xs bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded-lg font-medium transition"
              @click="handleResolve(a)"
            >
              ✓ Resolve
            </button>
            <button
              v-if="!a.is_resolved"
              class="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg font-medium transition"
              @click="openTicketFromAlert(a)"
            >
              🎫 Create Ticket
            </button>
            <router-link
              v-if="a.device_id"
              :to="`/devices/${a.device_id}`"
              class="text-xs text-blue-600 hover:underline"
            >
              View Device →
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <BaseModal v-model="showForm" title="Create Alert">
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Title <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.title"
            type="text"
            required
            placeholder="Router Offline"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Severity <span class="text-red-500">*</span>
          </label>
          <select
            v-model="form.severity"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="info">ℹ️ Info</option>
            <option value="warning">⚠️ Warning</option>
            <option value="critical">🔴 Critical</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Message</label>
          <textarea
            v-model="form.message"
            rows="3"
            placeholder="Additional details..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Device (optional)</label>
          <select
            v-model.number="form.device_id"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option :value="null">-- None --</option>
            <option v-for="d in devices" :key="d.id" :value="d.id">
              {{ d.hostname }} ({{ d.ip_address }})
            </option>
          </select>
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg">
          {{ error }}
        </div>

        <div class="flex justify-end gap-2 pt-2 border-t border-gray-100">
          <button
            type="button"
            class="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-lg font-medium transition"
            @click="showForm = false"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition disabled:opacity-50"
          >
            {{ saving ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { alertsApi } from '@/api/alerts'
import { devicesApi } from '@/api/devices'
import { ticketsApi } from '@/api/tickets'
import { useAuthStore } from '@/store/auth'
import { useToast } from '@/composables/useToast'
import { timeAgo } from '@/composables/useTimeAgo'
import BaseModal from '@/components/common/BaseModal.vue'
import Loader from '@/components/common/Loader.vue'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const alerts = ref([])
const devices = ref([])
const loading = ref(true)
const saving = ref(false)
const showForm = ref(false)
const severity = ref('')
const resolved = ref(null)
const error = ref('')

const form = reactive({
  title: '',
  severity: 'info',
  message: '',
  device_id: null,
})

const filters = [
  { value: '', label: 'All' },
  { value: 'info', label: 'ℹ️ Info' },
  { value: 'warning', label: '⚠️ Warning' },
  { value: 'critical', label: '🔴 Critical' },
]

const activeCount = computed(() => alerts.value.filter((a) => !a.is_resolved).length)
const resolvedCount = computed(() => alerts.value.filter((a) => a.is_resolved).length)
const criticalCount = computed(
  () => alerts.value.filter((a) => a.severity === 'critical' && !a.is_resolved).length
)

const hasFilters = computed(() => severity.value || resolved.value !== null)

const filteredAlerts = computed(() => {
  let list = alerts.value
  if (severity.value) list = list.filter((a) => a.severity === severity.value)
  if (resolved.value !== null) list = list.filter((a) => a.is_resolved === resolved.value)
  return list
})

onMounted(async () => {
  await Promise.all([loadAlerts(), loadDevices()])
})

async function loadAlerts() {
  loading.value = true
  try {
    const { data } = await alertsApi.list()
    alerts.value = data
  } catch (e) {
    toast.error('Failed to load alerts')
  } finally {
    loading.value = false
  }
}

async function loadDevices() {
  try {
    const { data } = await devicesApi.list({})
    devices.value = data
  } catch (e) {
    console.error(e)
  }
}

function setFilter(value) {
  severity.value = value
}

function clearFilters() {
  severity.value = ''
  resolved.value = null
}

function borderColor(s) {
  return {
    info: 'border-l-blue-500',
    warning: 'border-l-orange-500',
    critical: 'border-l-red-500',
  }[s] || 'border-l-gray-400'
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

function openCreate() {
  Object.assign(form, { title: '', severity: 'info', message: '', device_id: null })
  error.value = ''
  showForm.value = true
}

async function handleCreate() {
  error.value = ''
  saving.value = true
  try {
    const payload = { ...form }
    if (!payload.device_id) delete payload.device_id
    if (!payload.message) delete payload.message
    await alertsApi.create(payload)
    toast.success('Alert created')
    showForm.value = false
    await loadAlerts()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Create failed'
  } finally {
    saving.value = false
  }
}

async function handleResolve(alert) {
  try {
    await alertsApi.resolve(alert.id)
    toast.success('Alert resolved')
    await loadAlerts()
  } catch (e) {
    toast.error('Resolve failed')
  }
}

async function openTicketFromAlert(alert) {
  try {
    const { data } = await ticketsApi.create({
      title: alert.title,
      description: alert.message || `Auto-generated from alert #${alert.id}`,
      priority: alert.severity === 'critical' ? 'critical' : 'medium',
      device_id: alert.device_id,
    })
    toast.success('Ticket created')
    router.push(`/tickets/${data.id}`)
  } catch (e) {
    toast.error('Failed to create ticket')
  }
}

// Auto-refresh har 30 sec
let timer = null
onMounted(() => {
  timer = setInterval(() => loadAlerts(), 30000)
})
import { onUnmounted } from 'vue'
onUnmounted(() => clearInterval(timer))
</script>