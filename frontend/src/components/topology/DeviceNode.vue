<template>
  <div
    class="device-node bg-white rounded-2xl border-2 shadow-md px-4 py-3 min-w-[200px] text-center transition-all cursor-pointer hover:shadow-xl"
    :class="borderClass"
    @contextmenu.prevent="$emit('contextmenu', { event: $event, data })"
  >
    <Handle type="target" :position="Position.Top" class="!bg-slate-400 !w-3 !h-3 !border-2 !border-white" />

    <div
      class="absolute -top-1 -right-1 w-3 h-3 rounded-full border-2 border-white"
      :class="dotClass"
    ></div>

    <div class="text-4xl mb-2">{{ data.icon }}</div>
    <div class="font-bold text-sm text-gray-800 truncate">{{ data.label }}</div>
    <div class="text-xs text-gray-500 font-mono truncate mt-0.5">{{ data.ip }}</div>

    <div class="text-[10px] text-gray-400 uppercase tracking-wide mt-1 font-semibold">
      {{ data.device_type?.replace('_', ' ') }}
    </div>

    <div class="mt-2 pt-2 border-t border-gray-100 grid grid-cols-2 gap-1 text-[10px]">
      <div class="text-center">
        <div class="text-gray-400">Uptime</div>
        <div class="font-bold" :class="uptimeColor">{{ data.uptime || 0 }}%</div>
      </div>
      <div class="text-center">
        <div class="text-gray-400">Ping</div>
        <div class="font-bold text-blue-600">
          {{ data.response_time ? data.response_time + 'ms' : '—' }}
        </div>
      </div>
    </div>

    <div
      v-if="data.connections !== undefined"
      class="mt-1 text-[10px] text-gray-500"
    >
      🔗 {{ data.connections }} link{{ data.connections === 1 ? '' : 's' }}
    </div>

    <div class="mt-2">
      <span
        class="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full font-semibold"
        :class="badgeClass"
      >
        <span class="w-1.5 h-1.5 rounded-full" :class="dotClass"></span>
        {{ data.status }}
      </span>
    </div>

    <Handle
      type="source"
      :position="Position.Bottom"
      class="!bg-slate-400 !w-3 !h-3 !border-2 !border-white"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Handle, Position } from '@vue-flow/core'

const props = defineProps({
  data: { type: Object, required: true },
})

defineEmits(['contextmenu'])

const borderClass = computed(() => {
  return {
    online: 'border-green-400',
    offline: 'border-red-400',
    unknown: 'border-slate-300',
  }[props.data.status] || 'border-slate-300'
})

const badgeClass = computed(() => {
  return {
    online: 'bg-green-100 text-green-700',
    offline: 'bg-red-100 text-red-700',
    unknown: 'bg-slate-100 text-slate-600',
  }[props.data.status] || 'bg-slate-100 text-slate-600'
})

const dotClass = computed(() => {
  return {
    online: 'bg-green-500 animate-pulse',
    offline: 'bg-red-500',
    unknown: 'bg-slate-400',
  }[props.data.status] || 'bg-slate-400'
})

const uptimeColor = computed(() => {
  const u = props.data.uptime || 0
  if (u >= 95) return 'text-green-600'
  if (u >= 70) return 'text-orange-600'
  return 'text-red-600'
})
</script>

<style scoped>
.device-node {
  font-family: inherit;
  position: relative;
}
.device-node:hover {
  transform: translateY(-2px);
}
</style>