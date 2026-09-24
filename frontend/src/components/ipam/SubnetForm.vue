<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <!-- Network -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Network <span class="text-red-500">*</span>
      </label>
      <input
        v-model="form.network"
        type="text"
        required
        placeholder="192.168.1.0"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <p class="text-xs text-gray-400 mt-1">Network address (e.g. 192.168.1.0)</p>
    </div>

    <!-- CIDR -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        CIDR <span class="text-red-500">*</span>
      </label>
      <select
        v-model.number="form.cidr"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option v-for="c in cidrOptions" :key="c" :value="c">/{{ c }}</option>
      </select>
    </div>

    <!-- Gateway -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Gateway</label>
      <input
        v-model="form.gateway"
        type="text"
        placeholder="192.168.1.1"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- VLAN -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">VLAN</label>
      <input
        v-model.number="form.vlan"
        type="number"
        min="1"
        max="4094"
        placeholder="10"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Description -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
      <input
        v-model="form.description"
        type="text"
        placeholder="Office LAN"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
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

const props = defineProps({
  initial: { type: Object, default: null },
  submitLabel: { type: String, default: 'Save' },
})

const emit = defineEmits(['submit', 'cancel'])

const cidrOptions = [8, 16, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30]

const form = reactive({
  network: '',
  cidr: 24,
  gateway: '',
  vlan: null,
  description: '',
})

const error = ref('')
const loading = ref(false)

watch(
  () => props.initial,
  (val) => {
    if (val) {
      form.network = val.network ?? ''
      form.cidr = val.cidr ?? 24
      form.gateway = val.gateway ?? ''
      form.vlan = val.vlan ?? null
      form.description = val.description ?? ''
    } else {
      form.network = ''
      form.cidr = 24
      form.gateway = ''
      form.vlan = null
      form.description = ''
    }
  },
  { immediate: true }
)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    const payload = { ...form }
    if (payload.gateway === '') payload.gateway = null
    if (payload.vlan === '') payload.vlan = null
    emit('submit', payload)
  } catch (e) {
    error.value = e.message || 'Something went wrong'
  } finally {
    loading.value = false
  }
}

defineExpose({ setError: (msg) => (error.value = msg) })
</script>