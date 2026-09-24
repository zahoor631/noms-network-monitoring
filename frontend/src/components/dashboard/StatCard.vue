<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex items-center justify-between">
    <div>
      <p class="text-sm text-gray-500">{{ title }}</p>
      <p class="text-3xl font-bold mt-1" :class="textColor">{{ value }}</p>
    </div>
    <div class="text-3xl">{{ icon }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  value: [Number, String],
  color: { type: String, default: 'blue' },
  icon: { type: String, default: '📊' },
})

const textColor = computed(() => {
  const map = {
    blue: 'text-blue-600',
    green: 'text-green-600',
    red: 'text-red-600',
    orange: 'text-orange-600',
    gray: 'text-gray-600',
  }
  return map[props.color] || map.blue
})
</script>