<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
      <!-- Search -->
      <div class="md:col-span-2">
        <label class="block text-xs font-medium text-gray-500 mb-1">Search</label>
        <input
          :value="filters.search"
          type="text"
          placeholder="Hostname ya IP se search karo..."
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          @input="$emit('update:search', $event.target.value)"
        />
      </div>

      <!-- Type -->
      <div>
        <label class="block text-xs font-medium text-gray-500 mb-1">Type</label>
        <select
          :value="filters.device_type"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          @change="$emit('update:type', $event.target.value)"
        >
          <option value="">All Types</option>
          <option v-for="t in DEVICE_TYPES" :key="t.value" :value="t.value">
            {{ t.icon }} {{ t.label }}
          </option>
        </select>
      </div>

      <!-- Status -->
      <div>
        <label class="block text-xs font-medium text-gray-500 mb-1">Status</label>
        <select
          :value="filters.status"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          @change="$emit('update:status', $event.target.value)"
        >
          <option value="">All Status</option>
          <option v-for="s in DEVICE_STATUS" :key="s.value" :value="s.value">
            {{ s.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Reset -->
    <div v-if="hasFilters" class="mt-3 flex justify-end">
      <button
        class="text-xs text-blue-600 hover:text-blue-800 font-medium"
        @click="$emit('reset')"
      >
        ✕ Clear Filters
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { DEVICE_TYPES, DEVICE_STATUS } from '@/utils/constants'

const props = defineProps({
  filters: { type: Object, required: true },
})

defineEmits(['update:search', 'update:type', 'update:status', 'reset'])

const hasFilters = computed(
  () =>
    props.filters.search ||
    props.filters.device_type ||
    props.filters.status
)
</script>