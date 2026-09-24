<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold">Organization Structure</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          Company network hierarchy — sites, departments aur teams
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-lg text-sm font-medium transition"
          @click="reload"
        >
          🔄 Refresh
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-3 mb-4">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Sites / Groups</p>
        <p class="text-2xl font-bold text-blue-600">{{ sites.length }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Departments</p>
        <p class="text-2xl font-bold text-purple-600">{{ totalDepartments }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Total Devices</p>
        <p class="text-2xl font-bold text-gray-800">{{ totalDevices }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Online</p>
        <p class="text-2xl font-bold text-green-600">{{ totalOnline }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Offline</p>
        <p class="text-2xl font-bold text-red-600">{{ totalOffline }}</p>
      </div>
    </div>

    <!-- Search + Filters -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
        <div class="md:col-span-2">
          <input
            v-model="search"
            type="text"
            placeholder="🔎 Search sites, departments, devices..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <select
            v-model="filterType"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Device Types</option>
            <option value="router">📡 Routers</option>
            <option value="switch">🔀 Switches</option>
            <option value="firewall">🛡️ Firewalls</option>
            <option value="server">🖥️ Servers</option>
            <option value="access_point">📶 Access Points</option>
            <option value="pc">💻 PCs</option>
          </select>
        </div>
        <div>
          <select
            v-model="filterStatus"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Status</option>
            <option value="online">🟢 Online</option>
            <option value="offline">🔴 Offline</option>
            <option value="unknown">⚪ Unknown</option>
          </select>
        </div>
      </div>
    </div>

    <Loader v-if="loading" />

    <!-- Groups -->
    <div v-else class="space-y-3">
      <div
        v-for="site in filteredSites"
        :key="site.name"
        class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
      >
        <!-- Site Header -->
        <div
          class="flex items-center justify-between p-4 cursor-pointer hover:bg-gray-50 transition"
          @click="toggleSite(site.name)"
        >
          <div class="flex items-center gap-3">
            <span
              class="text-xl transition-transform"
              :class="expanded[site.name] ? 'rotate-90' : ''"
            >
              ▶
            </span>
            <span class="text-2xl">{{ site.icon }}</span>
            <div>
              <h3 class="font-semibold text-gray-800">{{ site.name }}</h3>
              <p class="text-xs text-gray-500">
                {{ site.devices.length }} devices · {{ site.subDepartments.length }} departments
              </p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <p class="text-xs text-gray-500">Status</p>
              <div class="flex items-center gap-3 text-xs">
                <span class="text-green-600 font-medium">🟢 {{ site.online }}</span>
                <span class="text-red-600 font-medium">🔴 {{ site.offline }}</span>
                <span v-if="site.unknown" class="text-gray-500 font-medium">⚪ {{ site.unknown }}</span>
              </div>
            </div>
            <div class="text-right">
              <p class="text-xs text-gray-500">Availability</p>
              <p
                v-if="site.devices.length > 0 && site.uptime !== null"
                class="text-sm font-bold"
                :class="uptimeColor(site.uptime)"
              >
                {{ site.uptime }}%
              </p>
              <p v-else class="text-xs text-gray-400">No data</p>
            </div>
          </div>
        </div>

        <!-- Availability bar -->
        <div v-if="site.devices.length > 0" class="h-1 bg-gray-100">
          <div
            class="h-full transition"
            :class="site.uptime >= 95 ? 'bg-green-500' : site.uptime >= 70 ? 'bg-orange-500' : 'bg-red-500'"
            :style="{ width: (site.uptime || 0) + '%' }"
          ></div>
        </div>

        <!-- Sub-departments -->
        <div v-if="expanded[site.name]" class="border-t border-gray-100">
          <!-- Sub-departments -->
          <div
            v-for="sub in site.subDepartments"
            :key="sub.name"
            class="pl-12 pr-4 py-3 hover:bg-gray-50 border-b border-gray-100 last:border-b-0 cursor-pointer"
            @click.stop="viewDevices(sub.name)"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="text-lg">📁</span>
                <span class="font-medium text-gray-700 text-sm">{{ sub.name }}</span>
              </div>
              <div class="flex items-center gap-3 text-xs">
                <span class="text-gray-600">{{ sub.devices.length }} devices</span>
                <span class="text-green-600">🟢 {{ sub.online }}</span>
                <span class="text-red-600">🔴 {{ sub.offline }}</span>
              </div>
            </div>
          </div>

          <!-- Direct devices -->
          <div
            v-if="site.directDevices.length"
            class="pl-12 pr-4 py-3 bg-blue-50 border-b border-gray-100"
          >
            <p class="text-xs text-gray-500 mb-2 font-medium uppercase tracking-wide">
              Direct devices
            </p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="d in site.directDevices.slice(0, 15)"
                :key="d.id"
                class="px-2 py-1 bg-white border border-gray-200 rounded text-xs font-mono"
                :class="statusTextColor(d.status)"
              >
                {{ d.hostname }}
              </span>
              <span
                v-if="site.directDevices.length > 15"
                class="px-2 py-1 text-xs text-gray-500"
              >
                +{{ site.directDevices.length - 15 }} more
              </span>
            </div>
          </div>

          <!-- Alerts -->
          <div
            v-if="site.activeAlerts.length"
            class="pl-12 pr-4 py-3 bg-red-50 border-t border-red-100"
          >
            <p class="text-xs text-red-700 font-medium mb-2">
              ⚠️ {{ site.activeAlerts.length }} active alert(s)
            </p>
            <div class="space-y-1">
              <div
                v-for="a in site.activeAlerts.slice(0, 3)"
                :key="a.id"
                class="text-xs text-red-700 flex items-center gap-2"
              >
                <span>{{ severityIcon(a.severity) }}</span>
                <span>{{ a.title }}</span>
              </div>
              <div v-if="site.activeAlerts.length > 3" class="text-xs text-red-500">
                +{{ site.activeAlerts.length - 3 }} more alerts...
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="pl-12 pr-4 py-3 bg-gray-50 flex items-center gap-3">
            <button
              class="text-sm text-blue-600 hover:text-blue-800 font-medium"
              @click.stop="viewDevices(site.name)"
            >
              View all {{ site.devices.length }} devices →
            </button>
            <router-link
              to="/topology"
              class="text-sm text-purple-600 hover:text-purple-800 font-medium"
              @click.stop
            >
              View Topology →
            </router-link>
          </div>
        </div>
      </div>

      <!-- Empty -->
      <div
        v-if="!filteredSites.length"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center text-gray-400"
      >
        <p class="text-5xl mb-3">🏢</p>
        <p class="font-medium">No sites or departments found</p>
        <p class="text-sm mt-1">
          Devices ke location field mein site name daalo (e.g. "Data Center", "Head Office")
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { devicesApi } from '@/api/devices'
import { alertsApi } from '@/api/alerts'
import { useToast } from '@/composables/useToast'
import Loader from '@/components/common/Loader.vue'

const router = useRouter()
const toast = useToast()

const devices = ref([])
const alerts = ref([])
const loading = ref(true)
const search = ref('')
const filterType = ref('')
const filterStatus = ref('')
const expanded = reactive({})

// Keywords for classifying device locations
const EXTERNAL_KEYWORDS = ['internet', 'external', 'public', 'wan', 'cloud']
const LOCAL_KEYWORDS = ['local', 'localhost', 'loopback']

onMounted(load)

async function load() {
  loading.value = true
  try {
    const [devRes, altRes] = await Promise.all([
      devicesApi.list({}),
      alertsApi.list({}),
    ])
    devices.value = devRes.data
    alerts.value = altRes.data
  } catch (e) {
    toast.error('Failed to load organization')
  } finally {
    loading.value = false
  }
}

function reload() {
  load()
  toast.success('Refreshed')
}

// ───── GROUPING LOGIC ─────

const sites = computed(() => {
  // Group by top-level location (before " > " or "/")
  const groups = {}

  devices.value.forEach((d) => {
    const rawLocation = (d.location || '').trim()
    const loc = rawLocation.replace(/\t/g, '').trim()

    // Determine site type (external, local, or normal)
    const lower = loc.toLowerCase()
    const isExternal = EXTERNAL_KEYWORDS.some((k) => lower.includes(k))
    const isLocal = LOCAL_KEYWORDS.some((k) => lower.includes(k))

    let siteName
    let siteIcon

    if (isExternal) {
      siteName = 'External Network'
      siteIcon = '🌐'
    } else if (isLocal) {
      siteName = 'Local Monitoring'
      siteIcon = '🖥️'
    } else if (!loc) {
      siteName = 'Unassigned'
      siteIcon = '❓'
    } else {
      // Take first part before > or /
      const parts = loc.split(/[>\/\\]/).map((s) => s.trim()).filter(Boolean)
      siteName = parts[0] || 'Unassigned'
      siteIcon = '🏢'
    }

    if (!groups[siteName]) {
      groups[siteName] = { icon: siteIcon, direct: [], subs: {} }
    }

    // Sub-department (only for non-external/local)
    const parts = loc.split(/[>\/\\]/).map((s) => s.trim()).filter(Boolean)
    if (parts.length > 1 && !isExternal && !isLocal && parts[0] !== 'Unassigned') {
      const subName = parts.slice(1).join(' > ')
      if (!groups[siteName].subs[subName]) groups[siteName].subs[subName] = []
      groups[siteName].subs[subName].push(d)
    } else {
      groups[siteName].direct.push(d)
    }
  })

  // Build output
  return Object.entries(groups)
    .map(([name, { icon, direct, subs }]) => {
      const allDevices = [...direct, ...Object.values(subs).flat()]
      const online = allDevices.filter((d) => d.status === 'online').length
      const offline = allDevices.filter((d) => d.status === 'offline').length
      const unknown = allDevices.filter((d) => d.status === 'unknown').length

      // Uptime only if we have monitored data
      const monitoredDevices = allDevices.filter((d) => d.status !== 'unknown')
      const uptime =
        monitoredDevices.length > 0
          ? Math.round((online / monitoredDevices.length) * 100)
          : null

      const subDepartments = Object.entries(subs).map(([subName, subDevices]) => {
        const subOnline = subDevices.filter((d) => d.status === 'online').length
        const subOffline = subDevices.filter((d) => d.status === 'offline').length
        return {
          name: subName,
          devices: subDevices,
          online: subOnline,
          offline: subOffline,
        }
      })

      // Alerts for this site
      const deviceIds = new Set(allDevices.map((d) => d.id))
      const activeAlerts = alerts.value.filter(
        (a) => !a.is_resolved && a.device_id && deviceIds.has(a.device_id)
      )

      return {
        name,
        icon,
        devices: allDevices,
        directDevices: direct,
        subDepartments,
        online,
        offline,
        unknown,
        uptime,
        activeAlerts,
      }
    })
    .sort((a, b) => {
      // Sort: External/Local last, others first
      const order = (n) =>
        n === 'External Network' ? 2 : n === 'Local Monitoring' ? 3 : n === 'Unassigned' ? 4 : 1
      const diff = order(a.name) - order(b.name)
      if (diff !== 0) return diff
      return b.devices.length - a.devices.length
    })
})

const filteredSites = computed(() => {
  let list = sites.value

  if (search.value.trim()) {
    const q = search.value.toLowerCase()
    list = list.filter((s) => {
      if (s.name.toLowerCase().includes(q)) return true
      if (s.subDepartments.some((sub) => sub.name.toLowerCase().includes(q))) return true
      if (s.devices.some((d) => d.hostname.toLowerCase().includes(q))) return true
      return false
    })
  }

  if (filterType.value || filterStatus.value) {
    list = list
      .map((s) => {
        const filtered = s.devices.filter((d) => {
          if (filterType.value && d.device_type !== filterType.value) return false
          if (filterStatus.value && d.status !== filterStatus.value) return false
          return true
        })
        if (!filtered.length) return null
        const online = filtered.filter((d) => d.status === 'online').length
        const offline = filtered.filter((d) => d.status === 'offline').length
        const unknown = filtered.filter((d) => d.status === 'unknown').length
        const monitored = filtered.filter((d) => d.status !== 'unknown')
        const uptime =
          monitored.length > 0 ? Math.round((online / monitored.length) * 100) : null
        return { ...s, devices: filtered, online, offline, unknown, uptime }
      })
      .filter(Boolean)
  }

  return list
})

const totalDevices = computed(() => devices.value.length)
const totalOnline = computed(() => devices.value.filter((d) => d.status === 'online').length)
const totalOffline = computed(() => devices.value.filter((d) => d.status === 'offline').length)
const totalDepartments = computed(() =>
  sites.value.reduce((sum, s) => sum + s.subDepartments.length, 0)
)

// ───── HELPERS ─────

function toggleSite(name) {
  expanded[name] = !expanded[name]
}

function viewDevices(locationFilter) {
  router.push({ path: '/devices', query: { search: locationFilter } })
}

function uptimeColor(pct) {
  if (pct >= 95) return 'text-green-600'
  if (pct >= 70) return 'text-orange-600'
  return 'text-red-600'
}

function statusTextColor(status) {
  return {
    online: 'text-green-700',
    offline: 'text-red-700',
    unknown: 'text-gray-600',
  }[status] || 'text-gray-600'
}

function severityIcon(s) {
  return { info: 'ℹ️', warning: '⚠️', critical: '🔴' }[s] || 'ℹ️'
}
</script>