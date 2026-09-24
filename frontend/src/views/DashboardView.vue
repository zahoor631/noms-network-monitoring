<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold">Dashboard</h1>
      <p class="text-sm text-gray-500 mt-0.5">
        Welcome back, {{ auth.user?.username }} — aaj ka network overview
      </p>
    </div>

    <Loader v-if="loading" />

    <div v-else class="space-y-5">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Devices" :value="stats.total" color="blue" icon="🖥️" />
        <StatCard title="Online" :value="stats.online" color="green" icon="🟢" />
        <StatCard title="Offline" :value="stats.offline" color="red" icon="🔴" />
        <StatCard title="Active Alerts" :value="stats.active_alerts" color="orange" icon="🔔" />
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <DeviceStatusChart :stats="stats" />
        <div class="lg:col-span-2">
          <BandwidthChart :data="bandwidth" />
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <CpuMemoryChart :cpu="cpu" :memory="memory" />
        <RecentAlerts :alerts="recentAlerts" />
        <TopDevicesTable :devices="devices" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { reportsApi } from '@/api/reports'
import { devicesApi } from '@/api/devices'
import StatCard from '@/components/dashboard/StatCard.vue'
import DeviceStatusChart from '@/components/dashboard/DeviceStatusChart.vue'
import BandwidthChart from '@/components/dashboard/BandwidthChart.vue'
import CpuMemoryChart from '@/components/dashboard/CpuMemoryChart.vue'
import RecentAlerts from '@/components/dashboard/RecentAlerts.vue'
import TopDevicesTable from '@/components/dashboard/TopDevicesTable.vue'
import Loader from '@/components/common/Loader.vue'

const auth = useAuthStore()
const loading = ref(true)
const stats = ref({ total: 0, online: 0, offline: 0, unknown: 0, active_alerts: 0, open_tickets: 0 })
const bandwidth = ref([])
const cpu = ref(0)
const memory = ref(0)
const recentAlerts = ref([])
const devices = ref([])

onMounted(async () => {
  try {
    const [dashRes, devRes] = await Promise.all([
      reportsApi.dashboard(),
      devicesApi.list({}),
    ])
    const d = dashRes.data
    stats.value = d.stats
    bandwidth.value = d.bandwidth
    cpu.value = d.cpu
    memory.value = d.memory
    recentAlerts.value = d.recent_alerts
    devices.value = devRes.data
  } catch (e) {
    console.error('Dashboard load failed:', e)
  } finally {
    loading.value = false
  }
})
</script>