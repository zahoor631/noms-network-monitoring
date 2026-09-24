<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
    <h3 class="font-semibold text-gray-800 mb-4">CPU & Memory</h3>
    <div style="height: 240px;">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

const props = defineProps({
  cpu: { type: Number, default: 0 },
  memory: { type: Number, default: 0 },
})

const chartData = computed(() => ({
  labels: ['CPU %', 'Memory %'],
  datasets: [{
    data: [props.cpu, props.memory],
    backgroundColor: ['#3b82f6', '#8b5cf6'],
    borderRadius: 8,
    barThickness: 60,
  }],
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
</script>