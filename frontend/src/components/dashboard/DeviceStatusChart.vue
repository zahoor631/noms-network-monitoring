<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
    <h3 class="font-semibold text-gray-800 mb-4">Device Status</h3>
    <div class="relative" style="height: 220px;">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
    <div class="mt-4 grid grid-cols-3 gap-2 text-center">
      <div>
        <p class="text-xs text-gray-500">Online</p>
        <p class="font-bold text-green-600">{{ stats.online }}</p>
      </div>
      <div>
        <p class="text-xs text-gray-500">Offline</p>
        <p class="font-bold text-red-600">{{ stats.offline }}</p>
      </div>
      <div>
        <p class="text-xs text-gray-500">Unknown</p>
        <p class="font-bold text-gray-600">{{ stats.unknown }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  stats: { type: Object, default: () => ({ online: 0, offline: 0, unknown: 0 }) },
})

const chartData = computed(() => ({
  labels: ['Online', 'Offline', 'Unknown'],
  datasets: [{
    data: [props.stats.online, props.stats.offline, props.stats.unknown],
    backgroundColor: ['#10b981', '#ef4444', '#9ca3af'],
    borderWidth: 0,
  }],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '65%',
  plugins: {
    legend: { position: 'bottom', labels: { boxWidth: 12, padding: 12, font: { size: 11 } } },
  },
}
</script>