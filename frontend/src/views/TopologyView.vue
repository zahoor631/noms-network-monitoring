<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-4 flex-wrap gap-3">
      <div>
        <h1 class="text-2xl font-bold">Network Topology</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          <span class="font-semibold text-blue-600">{{ flowNodes.length }}</span> devices ·
          <span class="font-semibold text-green-600">{{ flowEdges.length }}</span> connections
          <span v-if="lastUpdated" class="ml-2 text-xs text-gray-400">
            · Last: {{ lastUpdated }}
          </span>
        </p>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <select
          v-model="filterType"
          class="bg-white border border-gray-200 px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Types</option>
          <option value="router">📡 Routers</option>
          <option value="switch">🔀 Switches</option>
          <option value="firewall">🛡️ Firewalls</option>
          <option value="server">🖥️ Servers</option>
          <option value="access_point">📶 Access Points</option>
          <option value="pc">💻 PCs</option>
        </select>

        <select
          v-model="filterStatus"
          class="bg-white border border-gray-200 px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Status</option>
          <option value="online">🟢 Online</option>
          <option value="offline">🔴 Offline</option>
          <option value="unknown">⚪ Unknown</option>
        </select>

        <button
          :disabled="discovering"
          class="bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-lg text-sm font-medium transition disabled:opacity-50"
          @click="autoDiscover(true)"
        >
          {{ discovering ? '⏳' : '🔍' }} Discover
        </button>
        <button
          class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm font-medium transition"
          @click="reLayout"
        >
          🌐 Re-Layout
        </button>
        <button
          class="bg-gray-700 hover:bg-gray-800 text-white px-3 py-2 rounded-lg text-sm font-medium transition"
          @click="toggleFullscreen"
        >
          {{ isFullscreen ? '🡼 Exit' : '⛶ Fullscreen' }}
        </button>
      </div>
    </div>

    <!-- Legend -->
    <div
      v-show="!isFullscreen"
      class="bg-white rounded-xl shadow-sm border border-gray-200 p-3 mb-4 flex items-center gap-6 text-sm flex-wrap"
    >
      <span class="text-gray-500 font-medium">Legend:</span>
      <span class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-full bg-green-500"></span> Online
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-full bg-red-500"></span> Offline
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-full bg-gray-400"></span> Unknown
      </span>
      <span class="flex items-center gap-1.5 ml-4">
        <span class="w-6 h-1 bg-blue-500 rounded"></span> Trunk
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-6 h-1 bg-green-500 rounded"></span> Access
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-6 h-1 bg-purple-500 rounded"></span> Subnet
      </span>
      <span class="ml-auto text-xs text-gray-400">
        💡 Right-click device · Hover connection
      </span>
    </div>

    <!-- Canvas -->
    <div
      ref="canvasContainer"
      class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden relative"
      :style="canvasStyle"
    >
      <div v-if="loading || discovering" class="h-full flex items-center justify-center">
        <div class="text-center">
          <div class="animate-spin rounded-full h-10 w-10 border-4 border-blue-200 border-t-blue-600 mx-auto"></div>
          <p class="text-gray-500 mt-3 text-sm">
            {{ discovering ? 'Discovering network...' : 'Loading...' }}
          </p>
        </div>
      </div>

      <div v-else-if="!flowNodes.length" class="h-full flex items-center justify-center">
        <div class="text-center text-gray-400">
          <p class="text-5xl mb-3">🗺️</p>
          <p class="font-medium">No devices to display</p>
          <p class="text-sm mt-1">Filters clear karo ya devices add karo</p>
          <router-link
            to="/devices"
            class="inline-block mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium"
          >
            Go to Devices
          </router-link>
        </div>
      </div>

      <VueFlow
        v-else
        v-model:nodes="flowNodes"
        v-model:edges="flowEdges"
        :node-types="nodeTypes"
        :default-viewport="{ x: 0, y: 0, zoom: 1 }"
        :min-zoom="0.2"
        :max-zoom="3"
        class="topology-flow"
        @node-click="onNodeClick"
        @edge-mouse-enter="onEdgeEnter"
        @edge-mouse-leave="onEdgeLeave"
      >
        <Background :gap="24" :size="1.5" pattern-color="#cbd5e1" />
        <Controls position="bottom-left" />
        <MiniMap
          position="bottom-right"
          pannable
          zoomable
          node-color="#3b82f6"
          mask-color="rgba(0,0,0,0.1)"
        />
      </VueFlow>

      <!-- Edge tooltip -->
      <div
        v-if="hoveredEdge"
        class="absolute bg-white rounded-lg shadow-2xl border border-gray-200 p-3 text-xs z-20 pointer-events-none"
        :style="{ top: hoveredEdge.y + 'px', left: hoveredEdge.x + 'px' }"
      >
        <p class="font-bold text-gray-800 mb-2">🔗 {{ hoveredEdge.label }}</p>
        <div class="space-y-1">
          <p class="text-gray-600">
            <span class="font-medium">Source:</span> {{ hoveredEdge.sourceName }}
          </p>
          <p class="text-gray-600">
            <span class="font-medium">Target:</span> {{ hoveredEdge.targetName }}
          </p>
          <p class="text-gray-600">
            <span class="font-medium">Type:</span> {{ hoveredEdge.type }}
          </p>
        </div>
      </div>

      <div
        v-if="isFullscreen"
        class="absolute top-4 left-1/2 transform -translate-x-1/2 bg-black/70 text-white px-4 py-2 rounded-full text-xs z-10 pointer-events-none"
      >
        💡 ESC dabao fullscreen se bahar aane ke liye
      </div>
    </div>

    <!-- Context Menu -->
    <div
      v-if="contextMenu.show"
      class="fixed bg-white rounded-lg shadow-2xl border border-gray-200 py-1 z-[9999] min-w-[200px]"
      :style="{ top: contextMenu.y + 'px', left: contextMenu.x + 'px' }"
      @click.stop
    >
      <div class="px-3 py-2 border-b border-gray-100 text-xs text-gray-500 font-medium flex items-center gap-2">
        <span>{{ getIcon(contextMenu.device?.type) }}</span>
        {{ contextMenu.device?.label }}
      </div>
      <button
        class="w-full text-left px-4 py-2 hover:bg-blue-50 text-sm flex items-center gap-2"
        @click="ctxAction('ping')"
      >
        ⚡ Ping Now
      </button>
      <button
        class="w-full text-left px-4 py-2 hover:bg-blue-50 text-sm flex items-center gap-2"
        @click="ctxAction('view')"
      >
        👁️ View Details
      </button>
      <button
        class="w-full text-left px-4 py-2 hover:bg-blue-50 text-sm flex items-center gap-2"
        @click="ctxAction('monitor')"
      >
        📊 Monitoring
      </button>
      <div class="border-t border-gray-100 my-1"></div>
      <button
        class="w-full text-left px-4 py-2 hover:bg-orange-50 text-sm flex items-center gap-2 text-orange-700"
        @click="ctxAction('alert')"
      >
        🔔 Create Alert
      </button>
      <button
        class="w-full text-left px-4 py-2 hover:bg-orange-50 text-sm flex items-center gap-2 text-orange-700"
        @click="ctxAction('ticket')"
      >
        🎫 Create Ticket
      </button>
      <div class="border-t border-gray-100 my-1"></div>
      <button
        class="w-full text-left px-4 py-2 hover:bg-gray-50 text-sm flex items-center gap-2"
        @click="ctxAction('copy')"
      >
        📋 Copy IP
      </button>
    </div>

    <!-- Device Detail Panel -->
    <div
      v-if="selectedDevice"
      class="fixed top-20 right-4 bg-white rounded-xl shadow-xl border border-gray-200 p-5 w-80 z-50"
    >
      <div class="flex items-start justify-between mb-3">
        <div class="flex items-center gap-3">
          <span class="text-3xl">{{ getIcon(selectedDevice.type) }}</span>
          <div>
            <h3 class="font-bold text-gray-800">{{ selectedDevice.label }}</h3>
            <p class="text-xs text-gray-500 capitalize">{{ selectedDevice.type }}</p>
          </div>
        </div>
        <button
          class="text-gray-400 hover:text-gray-600"
          @click="selectedDevice = null"
        >
          ✕
        </button>
      </div>

      <div class="space-y-2 text-sm">
        <div class="flex justify-between">
          <span class="text-gray-500">IP Address</span>
          <span class="font-mono text-xs">{{ selectedDevice.ip }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-500">Status</span>
          <span
            :class="statusBadge(selectedDevice.status)"
            class="px-2 py-0.5 rounded text-xs font-medium"
          >
            {{ selectedDevice.status }}
          </span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-500">Location</span>
          <span class="text-xs">{{ selectedDevice.location || '—' }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-500">Connections</span>
          <span class="font-medium">{{ edgesForDevice(selectedDevice.id).length }}</span>
        </div>
      </div>

      <div class="mt-4 grid grid-cols-2 gap-2">
        <button
          class="bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-xs font-medium transition"
          @click="quickPing(selectedDevice)"
        >
          ⚡ Ping
        </button>
        <router-link
          :to="`/devices/${selectedDevice.id}`"
          class="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-xs font-medium transition text-center"
        >
          👁️ Details
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { MarkerType } from '@vue-flow/core'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'
import '@vue-flow/minimap/dist/style.css'

import { topologyApi } from '@/api/topology'
import { monitoringApi } from '@/api/monitoring'
import { useToast } from '@/composables/useToast'
import DeviceNode from '@/components/topology/DeviceNode.vue'

const router = useRouter()
const toast = useToast()

const canvasContainer = ref(null)
const isFullscreen = ref(false)
const loading = ref(true)
const discovering = ref(false)
const nodes = ref([])
const edges = ref([])
const flowNodes = ref([])
const flowEdges = ref([])
const selectedDevice = ref(null)
const lastUpdated = ref('')
const filterType = ref('')
const filterStatus = ref('')
const hoveredEdge = ref(null)

const nodeTypes = { custom: DeviceNode }

const contextMenu = ref({
  show: false,
  x: 0,
  y: 0,
  device: null,
})

const canvasStyle = computed(() => {
  if (isFullscreen.value) {
    return 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 9999; height: 100vh; border-radius: 0;'
  }
  return 'height: calc(100vh - 320px);'
})

const DEVICE_ICONS = {
  router: '📡',
  switch: '🔀',
  server: '🖥️',
  firewall: '🛡️',
  access_point: '📶',
  pc: '💻',
}

function getIcon(type) {
  return DEVICE_ICONS[type] || '📦'
}

function statusBadge(s) {
  return (
    {
      online: 'bg-green-100 text-green-700',
      offline: 'bg-red-100 text-red-700',
      unknown: 'bg-gray-100 text-gray-700',
    }[s] || 'bg-gray-100 text-gray-700'
  )
}

function edgesForDevice(id) {
  return flowEdges.value.filter(
    (e) => e.source === String(id) || e.target === String(id)
  )
}

// ───── FULLSCREEN ─────

async function toggleFullscreen() {
  if (!canvasContainer.value) return
  try {
    if (!document.fullscreenElement) {
      await canvasContainer.value.requestFullscreen()
      isFullscreen.value = true
      toast.success('Fullscreen ON — ESC dabao exit ke liye')
    } else {
      await document.exitFullscreen()
      isFullscreen.value = false
      toast.info('Fullscreen OFF')
    }
  } catch (e) {
    isFullscreen.value = !isFullscreen.value
  }
}

function onKeydown(e) {
  if (e.key === 'Escape' && isFullscreen.value) {
    if (!document.fullscreenElement) isFullscreen.value = false
  }
}

function onFullscreenChange() {
  isFullscreen.value = !!document.fullscreenElement
}

// ───── LIFECYCLE ─────

onMounted(async () => {
  document.addEventListener('keydown', onKeydown)
  document.addEventListener('fullscreenchange', onFullscreenChange)
  document.addEventListener('click', closeContextMenu)
  await reload()
})

onUnmounted(() => {
  document.removeEventListener('click', closeContextMenu)
  document.removeEventListener('keydown', onKeydown)
  document.removeEventListener('fullscreenchange', onFullscreenChange)
  if (document.fullscreenElement) {
    document.exitFullscreen().catch(() => {})
  }
})

function closeContextMenu() {
  contextMenu.value.show = false
}

// ───── DATA LOADING ─────

async function reload() {
  loading.value = true
  try {
    const { data } = await topologyApi.autoDiscover()
    nodes.value = data.nodes || []
    edges.value = data.edges || []
    buildLayout()
    updateTimestamp()
  } catch (e) {
    toast.error('Failed to load topology')
  } finally {
    loading.value = false
  }
}

async function autoDiscover(showToast = false) {
  if (showToast) discovering.value = true
  try {
    const { data } = await topologyApi.autoDiscover()
    nodes.value = data.nodes || []
    edges.value = data.edges || []
    buildLayout()
    updateTimestamp()
    if (showToast)
      toast.success(
        `✅ ${nodes.value.length} devices, ${edges.value.length} connections discovered`
      )
  } catch (e) {
    if (showToast) toast.error('Auto-discovery failed')
  } finally {
    if (showToast) discovering.value = false
  }
}

function reLayout() {
  buildLayout()
  toast.success('Layout refreshed')
}

function updateTimestamp() {
  lastUpdated.value = new Date().toLocaleTimeString()
}

watch([filterType, filterStatus], () => {
  buildLayout()
})

// ───── NODE/EDGE EVENTS ─────

function onNodeClick(event) {
  const id = event.node.id
  selectedDevice.value = nodes.value.find((n) => String(n.id) === id)
}

function onEdgeEnter(event) {
  const edge = event.edge
  const sourceNode = nodes.value.find((n) => String(n.id) === edge.source)
  const targetNode = nodes.value.find((n) => String(n.id) === edge.target)

  hoveredEdge.value = {
    x: event.event.clientX + 15,
    y: event.event.clientY + 15,
    label: edge.label || 'Connection',
    sourceName: sourceNode?.label || 'Unknown',
    targetName: targetNode?.label || 'Unknown',
    type: edge.data?.type || 'ethernet',
  }
}

function onEdgeLeave() {
  hoveredEdge.value = null
}

// ───── CONTEXT MENU ─────

async function ctxAction(action) {
  const device = contextMenu.value.device
  contextMenu.value.show = false
  if (!device) return

  switch (action) {
    case 'ping':
      await quickPing(device)
      break
    case 'view':
      router.push(`/devices/${device.id}`)
      break
    case 'monitor':
      router.push('/monitoring')
      break
    case 'alert':
      router.push('/alerts')
      break
    case 'ticket':
      router.push('/tickets')
      break
    case 'copy':
      try {
        await navigator.clipboard.writeText(device.ip)
        toast.success(`Copied: ${device.ip}`)
      } catch {
        toast.error('Copy failed')
      }
      break
  }
}

async function quickPing(device) {
  try {
    toast.info(`Pinging ${device.label}...`)
    const { data } = await monitoringApi.pingNow(device.id)
    if (data.response_time_ms) {
      toast.success(`✅ ${device.label} — ${data.response_time_ms}ms`)
    } else {
      toast.error(`❌ ${device.label} — offline`)
    }
    await autoDiscover(false)
  } catch (e) {
    toast.error('Ping failed')
  }
}

// ───── LAYOUT ─────

function buildLayout() {
  if (!nodes.value.length) return

  const filteredNodes = nodes.value.filter((n) => {
    if (filterType.value && n.type !== filterType.value) return false
    if (filterStatus.value && n.status !== filterStatus.value) return false
    return true
  })

  const l1_types = ['firewall', 'router']
  const l2_types = ['switch', 'access_point']
  const l3_types = ['server', 'pc']

  const l1 = filteredNodes.filter((n) => l1_types.includes(n.type))
  const l2 = filteredNodes.filter((n) => l2_types.includes(n.type))
  const l3 = filteredNodes.filter((n) => l3_types.includes(n.type))
  const other = filteredNodes.filter(
    (n) => !l1_types.concat(l2_types, l3_types).includes(n.type)
  )

  const NODE_W = 240
  const H_GAP = 100
  const V_GAP = 280
  const CENTER_X = 800
  const TOP_Y = 60

  const layoutRow = (arr, y) => {
    if (!arr.length) return []
    const totalW = arr.length * NODE_W + (arr.length - 1) * H_GAP
    const startX = CENTER_X - totalW / 2
    return arr.map((n, i) => {
      const connectionCount = edges.value.filter(
        (e) =>
          String(e.source) === String(n.id) ||
          String(e.target) === String(n.id)
      ).length

      return {
        id: String(n.id),
        type: 'custom',
        position: { x: startX + i * (NODE_W + H_GAP), y },
        data: {
          id: n.id,
          label: (n.label || '').replace(/\t/g, '').trim(),
          ip: n.ip,
          status: n.status,
          icon: getIcon(n.type),
          device_type: n.type,
          location: n.location,
          uptime: n.status === 'online' ? 100 : 0,
          response_time: null,
          connections: connectionCount,
        },
        draggable: true,
      }
    })
  }

  const rows = []
  let y = TOP_Y
  if (l1.length) {
    rows.push(...layoutRow(l1, y))
    y += V_GAP
  }
  if (l2.length) {
    rows.push(...layoutRow(l2, y))
    y += V_GAP
  }
  if (l3.length) {
    rows.push(...layoutRow(l3, y))
    y += V_GAP
  }
  if (other.length) {
    rows.push(...layoutRow(other, y))
  }

  flowNodes.value = rows

  const visibleIds = new Set(flowNodes.value.map((n) => n.id))
  flowEdges.value = edges.value
    .filter((e) => visibleIds.has(String(e.source)) && visibleIds.has(String(e.target)))
    .map((e, i) => ({
      id: e.id || `e${i}`,
      source: String(e.source),
      target: String(e.target),
      label: e.label || '',
      animated: true,
      type: 'smoothstep',
      data: { type: e.type },
      style: {
        stroke:
          e.type === 'trunk'
            ? '#3b82f6'
            : e.type === 'access'
            ? '#10b981'
            : e.type === 'subnet'
            ? '#8b5cf6'
            : '#94a3b8',
        strokeWidth: 3,
      },
      labelStyle: { fill: '#475569', fontSize: 11, fontWeight: 700 },
      labelBgStyle: { fill: '#ffffff', fillOpacity: 0.95 },
      labelBgPadding: [6, 4],
      labelBgBorderRadius: 4,
      markerEnd: { type: MarkerType.ArrowClosed, color: '#94a3b8' },
    }))

  attachContextMenuListeners()
}

function attachContextMenuListeners() {
  setTimeout(() => {
    document.querySelectorAll('.vue-flow__node').forEach((el) => {
      el.addEventListener('contextmenu', (e) => {
        e.preventDefault()
        const id = el.getAttribute('data-id')
        const node = nodes.value.find((n) => String(n.id) === id)
        if (node) {
          contextMenu.value = {
            show: true,
            x: e.clientX,
            y: e.clientY,
            device: node,
          }
        }
      })
    })
  }, 100)
}
</script>

<style>
.topology-flow {
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}
.topology-flow .vue-flow__node {
  cursor: pointer;
}
.topology-flow .vue-flow__edge-path {
  stroke-dasharray: 5;
}
.topology-flow .vue-flow__minimap {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
}
</style>