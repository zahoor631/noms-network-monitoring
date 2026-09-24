<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
    <h3 class="font-semibold text-gray-800 mb-4">Bandwidth (24h)</h3>
    <div style="height: 240px;">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Title, Tooltip, Legend, Filler,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const props = defineProps({ data: { type: Array, default: () => [] } })

const chartData = computed(() => ({
  labels: props.data.map((p) => p.time),
  datasets: [{
    label: 'Mbps',
    data: props.data.map((p) => p.value),
    borderColor: '#3b82f6',
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    fill: true,
    tension: 0.4,
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
</script>