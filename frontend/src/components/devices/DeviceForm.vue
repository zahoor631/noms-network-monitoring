<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <!-- Hostname -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Hostname <span class="text-red-500">*</span>
      </label>
      <input
        v-model="form.hostname"
        type="text"
        required
        placeholder="core-router-01"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Type -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Device Type <span class="text-red-500">*</span>
      </label>
      <select
        v-model="form.device_type"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Select type...</option>
        <option v-for="t in DEVICE_TYPES" :key="t.value" :value="t.value">
          {{ t.icon }} {{ t.label }}
        </option>
      </select>
    </div>

    <!-- IP -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        IP Address <span class="text-red-500">*</span>
      </label>
      <input
        v-model="form.ip_address"
        type="text"
        required
        placeholder="192.168.1.1"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- MAC -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">MAC Address</label>
      <input
        v-model="form.mac_address"
        type="text"
        placeholder="AA:BB:CC:DD:EE:FF"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Location -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Location</label>
      <input
        v-model="form.location"
        type="text"
        placeholder="Data Center Rack 1"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Description -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
      <textarea
        v-model="form.description"
        rows="2"
        placeholder="Extra details..."
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      ></textarea>
    </div>

    <!-- Error -->
    <div
      v-if="error"
      class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg"
    >
      {{ error }}
    </div>

    <!-- Footer -->
    <div class="flex justify-end gap-2 pt-2 border-t border-gray-100">
      <button
        type="button"
        class="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-lg font-medium transition"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
      <button
        type="submit"
        :disabled="loading"
        class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition disabled:opacity-50"
      >
        {{ loading ? 'Saving...' : submitLabel }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { DEVICE_TYPES } from '@/utils/constants'

const props = defineProps({
  initial: { type: Object, default: null },
  submitLabel: { type: String, default: 'Save' },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  hostname: '',
  device_type: '',
  ip_address: '',
  mac_address: '',
  location: '',
  description: '',
})

const error = ref('')
const loading = ref(false)

// Populate form when editing
watch(
  () => props.initial,
  (val) => {
    if (val) {
      Object.keys(form).forEach((k) => {
        form[k] = val[k] ?? ''
      })
    } else {
      Object.keys(form).forEach((k) => (form[k] = ''))
    }
  },
  { immediate: true }
)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    const payload = { ...form }
    // Clean empty fields
    Object.keys(payload).forEach((k) => {
      if (payload[k] === '') payload[k] = null
    })
    emit('submit', payload)
  } catch (e) {
    error.value = e.message || 'Something went wrong'
  } finally {
    loading.value = false
  }
}

defineExpose({ setError: (msg) => (error.value = msg) })
</script>