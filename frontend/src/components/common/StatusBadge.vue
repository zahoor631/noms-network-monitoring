<template>
  <span :class="badgeClass">
    <span class="inline-block w-2 h-2 rounded-full mr-1.5" :class="dotClass"></span>
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, default: 'unknown' },
})

const label = computed(() => props.status)
const badgeClass = computed(() => {
  const map = {
    online: 'bg-green-100 text-green-700',
    offline: 'bg-red-100 text-red-700',
    unknown: 'bg-gray-100 text-gray-700',
  }
  return `inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${map[props.status] || map.unknown}`
})
const dotClass = computed(() => {
  const map = {
    online: 'bg-green-500',
    offline: 'bg-red-500',
    unknown: 'bg-gray-400',
  }
  return map[props.status] || map.unknown
})
</script>